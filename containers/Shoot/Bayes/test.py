#! /usr/local/bin/python3
import os
import json

_train=True
_inference=True
os.environ["SM_MODEL_DIR"]="./mock/out"
os.environ["SM_CHANNEL_TRAIN"]="./mock/data"

from train import *
if _train:
    train({
    },[],0,out_dir=os.environ["SM_MODEL_DIR"],current_host="local")

if _inference:
    from host import *
    model=model_fn(os.environ["SM_MODEL_DIR"])
    width=10
    height=10
    
    body={
        "opponent":"test",
        "board":[[0]*width for x in range(height)],
        "session":{}
    }
    body["board"][0][0]=1
    body=json.dumps(body)
    response=transform_fn(model,body,"application/json","application/json")
    print(response)




