#! /bin/bash
set -ex 
cd /home/ec2-user

curl -sL https://rpm.nodesource.com/setup_8.x | bash -
yum install -y nodejs
