#! /usr/bin/env python3
import json
import random
import traceback

def model_fn(model_dir):
    return {}


def transform_fn(model, request_body, content_type, accept_type):
    try:
        print(request_body)
        input_object=json.loads(request_body)

        height=input_object["height"]
        width=input_object["width"]
        ships=input_object["ruleSet"]["shipCells"]

        layout=[[0]*width for x in range(height)]
      
        cords=[(random.randint(0,width-2),random.randint(0,width-2)) for z in range(ships//2)]
        
        for (x,y) in cords:
            layout[x][y]=1
            layout[x][y+1]=1
        
        return bytearray(json.dumps({
            "layout":layout,
            "session":{}
        }),'utf-8'),accept_type
    except Exception as e:
        print(traceback.format_exc())
        print(e)
