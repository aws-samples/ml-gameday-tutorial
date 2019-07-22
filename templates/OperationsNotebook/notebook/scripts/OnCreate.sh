#! /bin/bash
set -ex 
cd /home/ec2-user

cd SageMaker
git clone https://github.com/zackchase/mxnet-the-straight-dope.git

chown "ec2-user" * --recursive 
