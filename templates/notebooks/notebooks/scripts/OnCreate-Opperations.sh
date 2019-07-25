#! /bin/bash
set -ex 
cd /home/ec2-user/SageMaker
curl -sL https://rpm.nodesource.com/setup_8.x | bash -
yum install -y nodejs

sudo -u ec2-user git config --global credential.helper '!aws codecommit credential-helper $@'
sudo -u ec2-user git config --global credential.UseHttpPath true

sudo -u ec2-user git clone https://github.com/aws-samples/ml-gameday-tutorial.git

mv ml-gameday-tutorial GameDayRepo
cd GameDayRepo

git remote set-url origin ${Repo.CloneUrlHttp}
git branch layout
git branch shoot
git branch dev
sudo -u ec2-user git push --all -u 

cat << EOF > config.json
{
    "namespace":"prod",
    "project":"ml-gameday",
    "profile":"default",
    "region":"us-east-1",
    "assetBucket":"${AssetBucket}",
    "assetPrefix":"$TEAM",
    "parameters":{
        "MasterAccount":"${MasterAccount}",
        "GameArchiveBucket":"${GameArchiveBucket}"
    }
}
EOF

chown "ec2-user" * --recursive 
sudo -u ec2-user npm install
