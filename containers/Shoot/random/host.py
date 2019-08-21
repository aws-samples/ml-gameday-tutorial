#! /usr/bin/env python
import json
import random
import traceback

def model_fn(model_dir):
    return {}


def transform_fn(model, request_body, content_type, accept_type):
    try:
        print(request_body)
        input_object=json.loads(request_body)
        print(input_object)

        x=random.randint(0,len(input_object["board"])-1)
        y=random.randint(0,len(input_object["board"][0])-1)

        input_object["session"]["shootType"]="random"
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

