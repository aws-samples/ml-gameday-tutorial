#! /usr/local/bin/python3
import os
import json

_train=True
_inference=True
from train import *
os.environ["SM_MODEL_DIR"]="./mock/out"

if _train:
    train({
    },{
        
    },[],0,out_dir=os.environ["SM_MODEL_DIR"],current_host="local")

if _inference:
    from host import *
    model=model_fn("./tmp/out")
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




