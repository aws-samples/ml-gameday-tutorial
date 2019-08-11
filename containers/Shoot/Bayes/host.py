#! /usr/bin/env python
import json
import random
import traceback
import mxnet.ndarray as nd
def model_fn(model_dir):
    print("loading from %s"%(model_dir))
    p_a=nd.load("%s/model.p_a"%(model_dir))
    p_b=nd.load("%s/model.p_b"%(model_dir))
    return {"p_a":p_a,"p_b":p_b}


def transform_fn(model, request_body, content_type, accept_type):
    try:
        input_object=json.loads(request_body)
        if sum([sum(x) for x in input_object["board"]]) == 0: 
            x=random.randint(0,len(input_object["board"])-1)
            y=random.randint(0,len(input_object["board"][0])-1)
            shot={"x":x,"y":y}
        else:
            board=input_object["board"]
            p_b=model["p_b"]
            print(len(p_b))
            for x,row in enumerate(board):
                for y,column in enumerate(row):
                    if column==1:
                        p_b=[l for l in p_b if l[x][y]==1]
                    elif column==2:
                        p_b=[l for l in p_b if l[x][y]==0]
            if len(p_b)!=0:
                p=sum(p_b)/len(p_b)
                p_ab=p*(-(nd.array(board).clip(0,1)-1))
                print(p_ab)
                p_max=p_ab.max()
                choices=[]
                for x,row in enumerate(board):
                    for y,column in enumerate(row):
                        if p_ab[x][y]==p_max and board:
                            choices.append({"x":x,"y":y})
                shot=random.choice(choices)
            else:
                while True:
                    x=random.randint(0,len(input_object["board"])-1)
                    y=random.randint(0,len(input_object["board"][0])-1)
                    shot={"x":x,"y":y}
                    if input_object["board"][x][y]==0:
                        break

        input_object["session"]["shoot-type"]="Bayes"
        return bytearray(json.dumps({
            "shot":shot,
            "session":input_object["session"]
        }),'utf-8'),accept_type
    except Exception as e:
        print(traceback.format_exc())
        print(e)

