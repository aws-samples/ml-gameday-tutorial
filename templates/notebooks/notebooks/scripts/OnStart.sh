#! /bin/bash
set -ex 

curl -sL https://rpm.nodesource.com/setup_8.x | bash -
yum install -y nodejs
