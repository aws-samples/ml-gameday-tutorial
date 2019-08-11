#! /usr/bin/env python
import json
import random
import traceback
import mxnet.ndarray as nd
import mxnet as mx
from mxnet import nd, autograd, gluon
#from unet import Unet as model
from cnn import CNN as model
ctx =  mx.cpu()

def model_fn(model_dir):
    print("loading from %s"%(model_dir))
    with open('%s/hyperparameters.json'%(model_dir), 'r') as fp:
        hyperparameters = json.load(fp)
    
    net=model(
        depth=int(hyperparameters.get("depth",2)),
        width=int(hyperparameters.get("width",3)),
    )
    try:
        print("trying to load float16")
        net.cast("float16") 
        net.collect_params().load("%s/model-0000.params"%(model_dir), ctx)
    except Exception as e: 
        print(e)
        print("trying to load float32")
        net.cast("float32") 
        net.collect_params().load("%s/model-0000.params"%(model_dir), ctx)

    net.cast("float32")

    return net

def transform_fn(model, request_body, content_type, accept_type):
    try:
        input_object=json.loads(request_body)
        board=input_object["board"]
        count=input_object["session"].get("count",0)
        input_object["session"]["count"]=count+1

        if count>10:
            board=nd.array(board)
            board=nd.concat(
                (board==1).expand_dims(axis=0),
                (board==2).expand_dims(axis=0),dim=0
            )

            board=board.expand_dims(axis=0)

            mask=board.clip(0,1)
            mask=-(mask-1)
            mask=mask.reshape((2,-1)) 
            
            p=nd.softmax(model(board).reshape((-1,)))
            p=p*mask[0]*mask[1]
            
            while True:
                loc=int(p.argmax(axis=0).asscalar())
                y=loc//board.shape[2]
                x=loc%board.shape[2]
                if input_object["board"][y][x]==0:
                    break
                else:
                    p[loc]=0
        else:
            while True:
                x=random.randint(0,len(input_object["board"][0])-1)
                y=random.randint(0,len(input_object["board"])-1)
                if input_object["board"][y][x]==0:
                    break

        input_object["session"]["shoot-type"]="DenseNet"
        return bytearray(json.dumps({
            "shot":{
                "x":x,
                "y":y
            },
            "session":input_object["session"]
        }),'utf-8'),accept_type
    except Exception as e:
        print(traceback.format_exc())
        print(e)

