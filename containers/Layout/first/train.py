#! /usr/bin/env python3
import json
import sys
import traceback
import os
import mxnet.ndarray as nd
###############################
###     Training Script     ###
###############################

def train(hyperparameters, hosts, num_gpus,**kwargs):
    data_dir=os.environ["SM_CHANNEL_TRAIN"]
    data_file=os.listdir(data_dir)[0]
    num_shots=int(hyperparameters.get("num_shots",30))
    team=hyperparameters.get("team")
    create_board=True
    games=0
    with open(data_dir+'/'+data_file) as f:
        for x in f:
            games+=1
            record=json.loads(x)
            if create_board:
                board=nd.zeros_like(nd.array(record["TeamB"]["board"]))
                create_board=False
            if record["TeamB"]["TeamName"]!=team:
                for shot in record["TeamB"]["shots"][:num_shots]:
                    board[shot["y"]][shot["x"]]+=1
            if record["TeamA"]["TeamName"]!=team:
                for shot in record["TeamA"]["shots"][:num_shots]:
                    board[shot["y"]][shot["x"]]+=1
    print(board)
    board=1/(board+0.01)
    board=board/board.sum()
    print(board)
    save(board)

def save(board):
    path=os.environ["SM_MODEL_DIR"]
    print("saving to %s"%(path))
    nd.save("%s/board"%(path),[board])

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


