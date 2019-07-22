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
            LifecycleConfigName:{"Fn::GetAtt":["SageMakerNotebookLifecycle","NotebookInstanceLifecycleConfigName"]}
        }
    },
    "SageMakerNotebookLifecycle":{
        "Type" : "AWS::SageMaker::NotebookInstanceLifecycleConfig",
        "Properties" : {
            OnStart:[{
                Content:{"Fn::Base64":{"Fn::Sub":fs.readFileSync(`${__dirname}/scripts/OnStart.sh`,"utf-8")}}
            }]
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
