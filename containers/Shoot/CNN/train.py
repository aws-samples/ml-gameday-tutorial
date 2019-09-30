#! /usr/bin/env python3
import json
import sys
import random
import traceback
import shutil
import os
import time
import random
import mxnet.ndarray as nd
import mxnet as mx
# from unet import Unet as model
from cnn import CNN as model
from mxnet import nd, autograd, gluon
from multiprocessing import cpu_count

CPU_COUNT = cpu_count()


###############################
###     Training Script     ###
###############################


def train(hyperparameters, hosts, num_gpus, **kwargs):
    try:
        _ = mx.nd.array([1], ctx=mx.gpu(0))
        ctx = [mx.gpu(i) for i in range(num_gpus)]
        print("using GPU")
        DTYPE = "float16"
        host_ctx = mx.cpu_pinned(0)
    except mx.MXNetError:
        ctx = [mx.cpu()]
        print("using CPU")
        DTYPE = "float32"
        host_ctx = mx.cpu(0)

    model_dir = os.environ.get("SM_CHANNEL_MODEL")
    if model_dir:
        print("using prebuild model")
        shutil.unpack_archive("%s/model.tar.gz" % (model_dir), model_dir)
        with open('%s/hyperparameters.json' % (model_dir), 'r') as fp:
            saved_hyperparameters = json.load(fp)

        net = model(
            depth=int(saved_hyperparameters.get("depth", 2)),
            width=int(saved_hyperparameters.get("width", 3)),
        )
        try:
            print("trying to load float16")
            net.cast("float16")
            net.collect_params().load("%s/model-0000.params" % (model_dir), ctx)
        except Exception as e:
            print(e)
            print("trying to load float32")
            net.cast("float32")
            net.collect_params().load("%s/model-0000.params" % (model_dir), ctx)
        net.cast(DTYPE)
    else:
        print("building model from scratch")
        net = model(
            depth=int(hyperparameters.get("depth", 2)),
            width=int(hyperparameters.get("width", 3)),
        )
        net.cast(DTYPE)
    net.collect_params().initialize(mx.init.Xavier(), ctx=ctx)
    net.hybridize()
    print(net)

    dice = DiceLoss()
    dice.cast(DTYPE)
    dice.hybridize()

    trainer = gluon.Trainer(
        net.collect_params_layers(2) if model_dir else net.collect_params(),
        'adam',
        {
            "multi_precision": (DTYPE == 'float16'),
            'learning_rate': float(hyperparameters.get("learning_rate", .001))
        })
    train_iter, test_iter = get_data(int(hyperparameters.get("batch_size", 8)), DTYPE, host_ctx)

    Loss = gluon.loss.SoftmaxCrossEntropyLoss(sparse_label=False)

    best = float("inf")
    warm_up = int(hyperparameters.get("warm_up", 30))
    patience = int(hyperparameters.get("patience", 10))
    wait = 0

    for e in range(hyperparameters.get("epochs", 11)):
        print("Epoch %s" % (e))
        val_loss = 0
        st = time.time()
        training_count = 0
        testing_count = 0
        training_loss = 0

        for batch in train_iter:
            batch_size = batch.data[0].shape[0]
            training_count += batch_size
            data = gluon.utils.split_and_load(batch.data[0].astype(DTYPE), ctx)
            label = gluon.utils.split_and_load(batch.label[0].astype(DTYPE).reshape((batch_size, -1)), ctx)
            mask = gluon.utils.split_and_load(batch.label[1].astype(DTYPE).reshape((batch_size, -1)), ctx)

            with autograd.record():
                output = [net(x) for x in data]
                losses = [-dice(x, y, z) for x, y, z in zip(output, label, mask)]
            for loss in losses:
                loss.backward()
            trainer.step(batch_size)
            training_loss += sum(loss.sum().asscalar() for loss in losses)

        for batch in test_iter:
            batch_size = batch.data[0].shape[0]
            testing_count += batch_size

            data = gluon.utils.split_and_load(batch.data[0].astype(DTYPE), ctx)
            label = gluon.utils.split_and_load(batch.label[0].astype(DTYPE).reshape((batch_size, -1)), ctx)
            mask = gluon.utils.split_and_load(batch.label[1].astype(DTYPE).reshape((batch_size, -1)), ctx)

            output = [net(x) for x in data]
            losses = [-dice(x, y, z) for x, y, z in zip(output, label, mask)]

            val_loss += sum(loss.sum().asscalar() for loss in losses)

        et = time.time()
        print("Hyperparameters: %s;" % (hyperparameters))
        print("Training loss: %s;" % (-training_loss / training_count))
        print("Testing loss: %s;" % (-val_loss / (testing_count)))
        print("Throughput=%2.2f;" % ((training_count + testing_count) / (et - st)))
        print("Validation Loss=%2.2f;" % val_loss)
        print("Best=%2.2f;" % best)

        if e >= warm_up:
            if val_loss < best:
                print("best model: %s;" % (-val_loss / (testing_count)))
                save(net, hyperparameters)
                best = val_loss
                wait = 0
            else:
                wait += 1
        if wait > patience:
            print("stoping early")
            break
        train_iter.reset()
        test_iter.reset()


def save(net, hyperparameters):
    path = os.environ["SM_MODEL_DIR"]
    print("saving to %s" % (path))
    net.export("%s/model" % (path))
    with open('%s/hyperparameters.json' % (path), 'w') as fp:
        json.dump(hyperparameters, fp)


def create_board(record, team, DTYPE):
    layout = nd.array(record[team]["layout"])
    out = []
    board = nd.zeros((2, layout.shape[0], layout.shape[1]))
    mask = nd.ones((layout.shape[0], layout.shape[1]))
    for i in range(len(record[team]["shots"])):
        if i > 10:
            x = random.randint(0, layout.shape[0] - 1)
            y = random.randint(0, layout.shape[1] - 1)

            result = 0 if layout[x][y].asscalar() == 1 else 1
            board[result][x][y] = 1
            mask[x][y] = 0
            out.append([
                board.copy().astype(DTYPE),
                layout.astype(DTYPE),
                mask.astype(DTYPE)
            ])
    return out


def get_data(batch_size, dtype, host_ctx):
    data_dir = os.environ["SM_CHANNEL_TRAIN"]
    data_file = os.listdir(data_dir)[0]
    layouts = []
    with open(data_dir + '/' + data_file) as f:
        for x in f:
            record = json.loads(x)
            layouts.append(create_board(record, "TeamA", dtype))
            layouts.append(create_board(record, "TeamB", dtype))

    boards = [item for sublist in layouts for item in sublist]
    random.shuffle(boards)
    split = int(len(boards) * .7)
    with host_ctx:
        d_t = nd.concat(*[x[0].expand_dims(0) for x in boards[:split]], dim=0)
        l_t = nd.concat(*[x[1].expand_dims(0) for x in boards[:split]], dim=0)
        m_t = nd.concat(*[x[2].expand_dims(0) for x in boards[:split]], dim=0)

        d_v = nd.concat(*[x[0].expand_dims(0) for x in boards[split:]], dim=0)
        l_v = nd.concat(*[x[1].expand_dims(0) for x in boards[split:]], dim=0)
        m_v = nd.concat(*[x[2].expand_dims(0) for x in boards[split:]], dim=0)

    return (mx.io.NDArrayIter(
        data=d_t,
        label=[l_t, m_t],
        shuffle=True,
        batch_size=batch_size,
        last_batch_handle="pad"
    ),
            mx.io.NDArrayIter(
                data=d_v,
                label=[l_v, m_v],
                shuffle=False,
                last_batch_handle="pad",
                batch_size=2 * batch_size,
            )
    )


class DiceLoss(gluon.HybridBlock):
    def __init__(self, **kwargs):
        super(DiceLoss, self).__init__(**kwargs)

    def hybrid_forward(self, F, y_pred, y_true, mask):
        y_pred_f = y_pred.flatten() * mask
        y_true_f = y_true.flatten() * mask

        intersection = F.sum(F.broadcast_mul(y_true_f, y_pred_f), axis=1, )
        out = F.broadcast_div(
            (2. * intersection + 1.),
            (F.broadcast_add(F.sum(y_true_f, axis=1), F.sum(y_pred_f, axis=1)) + 1.)
        )
        return out


if __name__ == '__main__':
    try:
        model = train(
            json.loads(os.environ['SM_HPS']),
            json.loads(os.environ['SM_HOSTS']),
            int(os.environ['SM_NUM_GPUS']),
            out_dir=os.environ["SM_MODEL_DIR"],
            current_host=os.environ["SM_CURRENT_HOST"]
        )
    except Exception as e:
        print(sys.exc_info()[0])
        print(e)
        print(e.args)
        traceback.print_exc(file=sys.stdout)
        raise e
