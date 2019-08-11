from __future__ import print_function
import mxnet as mx
import numpy as np
import mxnet.gluon as gluon
from mxnet.gluon import nn
import os
import logging
import random

###############################
###     UNet Architecture   ###
###############################
class Block(gluon.HybridBlock):
    def __init__(self, num_filter,kernel,pad,**kwargs):
        super(Block, self).__init__()
        with self.name_scope():
            self.conv_1=nn.Conv2D(num_filter,kernel,padding=pad,groups=4)
            self.conv_2=nn.Conv2D(num_filter,kernel,padding=pad,groups=2)
            self.norm_1=nn.BatchNorm()
            self.norm_2=nn.BatchNorm()
            self.act_1=nn.Activation("relu")
            self.act_2=nn.Activation("relu")

    def hybrid_forward(self, F, x):
        one=self.act_1(self.norm_1(self.conv_1(x)))
        return self.act_2(x+self.norm_2(self.conv_2(one)))

        
class CNN(gluon.HybridBlock):
    def __init__(self, width=16,depth=8,**kwargs):
        super(CNN, self).__init__()
        with self.name_scope():
            self.conv_first=nn.Conv2D(width,1,padding=0)
            self.conv=[Block(width,3,1) for x in range(depth)]
            [self.register_child(x) for x in self.conv]
           
            self.conv_last=nn.Conv2D(1,1,padding=0)
            self.last_act=nn.Activation("sigmoid")

    def collect_params_layers(self,layer):
        ret=self.conv[-layer].collect_params()
        ret.update(self.conv_last.collect_params())
        return ret

    def hybrid_forward(self, F, x):
        state=self.conv_first(x)
        for conv in self.conv:
            state=conv(state)
        return  self.last_act(self.conv_last(state))

if __name__ == "__main__":
    print("testing")
    size=10
    test=mx.ndarray.zeros((4,2,size,size))
    
    net=CNN()
    net.hybridize()
    net.initialize(ctx=mx.cpu(0))
    print(net(test))
