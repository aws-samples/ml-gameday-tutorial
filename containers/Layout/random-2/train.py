#! /usr/bin/env python3
import json
import sys
import traceback
import os
###############################
###     Training Script     ###
###############################

def train(channel_input_dirs, hyperparameters, hosts, num_gpus,**kwargs):
    save()
    pass

def save():
    path=os.environ["SM_MODEL_DIR"]
    with open('%s/model.tmp'%(path),"w") as f:
        f.write("hello")

if __name__ =='__main__':
    try:
        model=train({},
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


