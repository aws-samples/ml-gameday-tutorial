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

class Conv_Block(gluon.HybridBlock):
    def __init__(self, num_filter,kernel,pad,activation,**kwargs):
        super(Conv_Block, self).__init__(**kwargs)
        with self.name_scope():
            self.conv=nn.Conv2D(num_filter,kernel,padding=pad)
            self.norm=nn.BatchNorm()
            if activation=="swish":
                self.act=nn.Swish()
            else:
                self.act=nn.Activation(activation)

    def hybrid_forward(self, F, x):
        return self.act(self.norm(self.conv(x)))
        
class Down_Block(gluon.HybridBlock):
    def __init__(self, num_filter,kernel,pad,activation,pool="avg",**kwargs):
        super(Down_Block, self).__init__(**kwargs)
        
        with self.name_scope():
            self.conv1=Conv_Block(num_filter,kernel,pad,activation)
            self.conv1_a=Conv_Block(num_filter,1,0,activation)
            self.conv2=Conv_Block(num_filter,kernel,pad,activation)
            self.conv2_a=Conv_Block(num_filter,1,0,activation)
            if(pool=="avg"):
                self.pool=nn.AvgPool2D(pool_size=(2,2),strides=(2,2))
            else:
                self.pool=nn.MaxPool2D(pool_size=(2,2),strides=(2,2))

    def hybrid_forward(self, F, x):
        out=self.conv2_a(self.conv2(self.conv1_a(self.conv1(x))))
        if(self.pool):
            return self.pool(out),out
        else:
            return None,out

class Down_Branch(gluon.HybridBlock):
    def __init__(self, activation,depth=5,pool='avg',width=5,**kwargs):
        super(Down_Branch, self).__init__(**kwargs)
        kernel=(3,3)
        pad=(1,1)

        with self.name_scope():
            self.blocks=[
                Down_Block(pow(2,width+i),kernel=kernel,pad=pad,pool=(i!=depth-1),activation=activation) 
            for i in range(depth)]
            [self.register_child(x) for x in self.blocks]

    def hybrid_forward(self, F, x):
        cur_pool=x
        convs=[]
        for block in self.blocks: 
            pool,conv=block(cur_pool)
            convs.append(conv)
            cur_pool=pool

        convs.reverse()
        return convs

class Up_Block(gluon.HybridBlock):
    def __init__(self, num_filter,kernel,activation,pad=0,**kwargs):
        super(Up_Block, self).__init__(**kwargs)
        with self.name_scope():
            self.conv1=Conv_Block(num_filter,kernel,pad,activation)
            self.conv1_a=Conv_Block(num_filter,1,0,activation)
            self.conv2=Conv_Block(num_filter,kernel,pad,activation)
            self.conv2_a=Conv_Block(num_filter,1,0,activation)
            self.de_conv=nn.Conv2DTranspose(
                num_filter,
                kernel_size=2,
                padding=0,
                weight_initializer="Bilinear",
                strides=2,
                use_bias=False)

    def hybrid_forward(self, F, x,y):
        up_sample=self.de_conv(x)
        concat=F.concat(up_sample,y)

        return self.conv2_a(self.conv2(self.conv1_a(self.conv1(concat))))

class Up_Branch(gluon.HybridBlock):
    def __init__(self, depth=5,activation="relu",width=8,**kwargs):
        super(Up_Branch, self).__init__(**kwargs)
        kernel=(3,3)
        pad=(1,1)

        with self.name_scope():
            self.blocks=[
                Up_Block(pow(2,width-i),kernel=3,pad=1,activation=activation)
            for i in range(depth)]
            [self.register_child(x) for x in self.blocks]
            self.conv=nn.Conv2D(1,kernel_size=1)

    def hybrid_forward(self, F, x,y):
        cur=x
        for (i,block) in enumerate(self.blocks): 
            cur=block(cur,y[i])
        return self.conv(cur)

class Unet(gluon.HybridBlock):
    def __init__(self, depth=5,activation="relu",drop_out=.1,pool="max",width=5,pad_width=16,**kwargs):
        super(Unet, self).__init__(**kwargs)
        self.config={
            "pad_width":pad_width,
            "depth":depth,
            "activation":activation,
            "drop_out":drop_out,
            "pool":pool,
            "width":width
        }
        self.pad_width=pad_width
        with self.name_scope():
            self.down_branch=Down_Branch(depth=depth,activation=activation,pool=pool,width=width)
            self.up_branch=Up_Branch(depth=depth-1,activation=activation,width=width+3)
            self.activation=nn.Activation("sigmoid")
            self.drop_out=nn.Dropout(drop_out)

    def hybrid_forward(self, F, x):
        pad_width=self.pad_width
        pad=(0,0,0,0,pad_width,pad_width,pad_width,pad_width)
        
        scaled_x=x
        padded=x.pad(mode="reflect",pad_width=pad)
        convs=self.down_branch(padded)
        up=self.up_branch(self.drop_out(convs[0]),convs[1:])
        
        up_cropped=up.slice_axis(
            axis=2,begin=pad_width,end=-pad_width
        ).slice_axis(
            axis=3,begin=pad_width,end=-pad_width
        )
        return self.activation(up_cropped)

if __name__ == "__main__":
    print("testing")
    size=10
    test=mx.ndarray.zeros((4,2,size,size))
    
    net=Unet(depth=3,width=6,pad_width=3)
    net.hybridize()
    net.initialize(ctx=mx.cpu(0))
    print(net(test))
