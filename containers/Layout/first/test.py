#! /usr/local/bin/python3
import os
import json

_train=True
_inference=True
from train import *
os.environ["SM_MODEL_DIR"]="./mock/out"
os.environ["SM_CHANNEL_TRAIN"]="./mock/data"

if _train:
    train({
        "team":"jmc"
    },[],0,out_dir=os.environ["SM_MODEL_DIR"],current_host="local")

if _inference:
    from host import *
    model=model_fn("./mock/out")
    body=json.dumps({
        "opponent":"test",
        "width":10,
        "height":10,
        "ruleSet":{
            "shipCells":11,
            "connectedShipCells":5
        }
    })
    response=transform_fn(model,body,'image/jpeg','image/jpeg')
    print(response)




