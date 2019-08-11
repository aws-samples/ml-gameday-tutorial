#! /usr/bin/env python3
import json
import random
import traceback
import math
import mxnet.ndarray as nd
from numpy.random import choice

def model_fn(model_dir):
    print("loading from %s"%(model_dir))
    board=nd.load("%s/board"%(model_dir))
    return board[0].reshape((-1,)).asnumpy()


def transform_fn(model, request_body, content_type, accept_type):
    p=model
    candidates=list(range(0,len(model)))
    try:
        print(request_body)
        input_object=json.loads(request_body)

        height=input_object["height"]
        width=input_object["width"]
        ships=input_object["ruleSet"]["shipCells"]

        size=2
        num_ships=math.ceil(ships/2)
        extra=ships-size*num_ships

        while True: #iterate till we generate a valid layout
            print("trying layout")
            try:
                layout=[[0]*width for x in range(height)]

                cords=choice(candidates,num_ships,False,p)
                cords=[[x%width,x//width] for x in cords]

                for (x,y) in cords:
                    layout[y][x]=1
                    layout[y][x+1]=1

                #gerenate ships of size 1 incase ships is not a multiple of 2
                cords=[(random.randint(0,width-1),random.randint(0,width-1)) 
                    for z in range(extra)]
                
                for (x,y) in cords:
                    layout[y][x]=1
                
                if sum([sum(x) for x in layout])==ships: #test for valid layout
                    break
            except IndexError:
                pass

        return bytearray(json.dumps({
            "layout":layout,
            "session":{
                "type":"random-first-10"
            }
        }),'utf-8'),accept_type
    except Exception as e:
        print(traceback.format_exc())
        print(e)
