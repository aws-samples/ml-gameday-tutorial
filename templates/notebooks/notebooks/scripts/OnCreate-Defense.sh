#! /bin/bash
set -ex 
cd /home/ec2-user/SageMaker

TEAM=layout
curl -sL https://rpm.nodesource.com/setup_8.x | bash -
yum install -y nodejs

sudo -u ec2-user git config --global credential.helper '!aws codecommit credential-helper $@'
sudo -u ec2-user git config --global credential.UseHttpPath true

sudo -u ec2-user git clone ${Repo.CloneUrlHttp}

mv ${Repo.Name} GameDayRepo
cd GameDayRepo

git checkout -b $TEAM
cat << EOF > config.json
{
    "namespace":"$TEAM",
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
