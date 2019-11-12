#! /usr/local/bin/python3
import os
import json

_train=True
_inference=False
os.environ["SM_MODEL_DIR"]="./mock/out"
os.environ["SM_CHANNEL_TRAIN"]="./mock/data"
os.environ["SM_CHANNEL_MODEL"]="./mock/out"

from train import *
if _train:
    train({
        "epochs":10,
        "warm_up":1,
        "depth":15,
        "width":8,
        "early_stopping":1,
        "learning_rate":.0005
    },[],0,out_dir=os.environ["SM_MODEL_DIR"],current_host="local")

if _inference:
    from host import *
    model=model_fn(os.environ["SM_MODEL_DIR"])
    width=10
    height=10
    
    body={
        "opponent":"test",
        "board":[[0]*width for x in range(height)],
        "session":{
            "count":12
        }
    }
    body["board"][3][5]=1
    body=json.dumps(body)
    response=transform_fn(model,body,"application/json","application/json")
    print(response)




