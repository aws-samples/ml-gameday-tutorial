var fs=require('fs')
var Promise=require('bluebird')
var _=require('lodash')

module.exports=Object.assign({
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
},
notebook("Opperations"),
notebook("Offense"),
notebook("Defense"),
)

function notebook(name){
    return _.fromPairs([
        [`${name}Notebook`,{
            "Type" : "AWS::SageMaker::NotebookInstance",
            "DependsOn":name!=="Opperations" ? ["OpperationsNotebook"] : [],
            "Properties" : {
                InstanceType:"ml.t2.medium",
                RoleArn:{"Fn::GetAtt":["NotebookRole","Arn"]},
                NotebookInstanceName:{"Fn::Sub":`\${AWS::StackName}-${name}`},
                LifecycleConfigName:{"Fn::GetAtt":[`${name}SageMakerNotebookLifecycle`,"NotebookInstanceLifecycleConfigName"]},
            }
        }],
        [`${name}SageMakerNotebookLifecycle`,{
            "Type" : "AWS::SageMaker::NotebookInstanceLifecycleConfig",
            "Properties" : {
                OnStart:[{
                    Content:{"Fn::Base64":{"Fn::Sub":fs.readFileSync(`${__dirname}/scripts/OnStart.sh`,"utf-8")}}
                }],
                OnCreate:[{
                Content:{"Fn::Base64":{"Fn::Sub":fs.readFileSync(`${__dirname}/scripts/OnCreate-${name}.sh`,"utf-8")}}
            }]
            }
        }]
    ])
}
