var fs=require('fs')
var Promise=require('bluebird')
var _=require('lodash')

module.exports=Object.assign({},{
    "Notebook":{
        "Type" : "AWS::SageMaker::NotebookInstance",
        "Properties" : {
            InstanceType:"ml.t2.large",
            RoleArn:{"Fn::GetAtt":["NotebookRole","Arn"]},
            NotebookInstanceName:{"Ref":"AWS::StackName"},
            DefaultCodeRepository:{"Fn::Sub":"https://git-codecommit.${AWS::Region}.amazonaws.com/v1/repos/${CodeCommitRepoName}"}
        }
    },
    "NotebookRole":{
      "Type": "AWS::IAM::Role",
      "Properties": {
        "AssumeRolePolicyDocument": {
          "Version": "2012-10-17",
          "Statement": [
            {
              "Effect": "Allow",
              "Principal": {
                "Service": "sagemaker.amazonaws.com"
              },
              "Action": "sts:AssumeRole"
            }
          ]
        },
        "Path": "/",
        "ManagedPolicyArns": ["arn:aws:iam::aws:policy/AdministratorAccess"]
      }
    },
})
