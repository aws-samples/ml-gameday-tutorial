#! /usr/bin/env python3
import json
import sys
import traceback
import os
import mxnet as mx
import mxnet.ndarray as nd
###############################
###     Training Script     ###
###############################

def train(hyperparameters, hosts, num_gpus,**kwargs):
    data_dir=os.environ["SM_CHANNEL_TRAIN"]
    data_file=os.listdir(data_dir)[0]
    layouts=[]
    with open(data_dir+'/'+data_file) as f:
        for x in f:
            record=json.loads(x)
            layouts.append(nd.array(record["TeamA"]["layout"]))
            layouts.append(nd.array(record["TeamB"]["layout"]))
    p_a=sum(layouts)/len(layouts)
    p_b=layouts
    save(p_a,p_b)
    pass

def save(p_a,p_b):
    path=os.environ["SM_MODEL_DIR"]
    print("saving to %s"%(path))
    nd.save("%s/model.p_a"%(path),[p_a])
    nd.save("%s/model.p_b"%(path),p_b)

if __name__ =='__main__':
    try:
        model=train(
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


