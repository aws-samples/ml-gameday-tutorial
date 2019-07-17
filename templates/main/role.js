module.exports={
    "MyQueuePolicy":{
      "Type":"AWS::SQS::QueuePolicy",
      "Properties":{        
        "PolicyDocument":{
          "Version":"2012-10-17",
          "Id":"MyQueuePolicy",
          "Statement":[{
              "Sid":"Allow-SendMessage-To-Both-Queues-From-SNS-Topic",
              "Effect":"Allow",           
              "Principal":"*",
              "Action":["sqs:SendMessage"],
              "Resource":"*",
              "Condition":{
                "ArnEquals":{
                  "aws:SourceArn":{"Ref":"ErrorTopic"}
                }
              }
          }]
        },
        "Queues":[{"Ref":"ErrorQueue"}]
      }
    },
	"ErrorQueue":{
        "Type":"AWS::SQS::Queue",
        "Properties":{}
    },
    "ErrorTopic":{
        "Type" : "AWS::SNS::Topic",
        "Properties" :{
            "Subscription":[ {
                "Endpoint":{"Fn::GetAtt":["ErrorQueue","Arn"]},
                "Protocol":"sqs"
            }]        
        }
    },
    "CrossAccountRole":{
      "Type": "AWS::IAM::Role",
      "Properties": {
        "AssumeRolePolicyDocument": {
          "Version": "2012-10-17",
          "Statement": [
            {
              "Effect": "Allow",
              "Principal": {
                "AWS":{"Fn::Sub":"arn:aws:iam::${MasterAccount}:root"}
              },
              "Action": "sts:AssumeRole"
            }
          ]
        },
        "Path": "/",
        "ManagedPolicyArns": [
            "arn:aws:iam::aws:policy/AmazonSageMakerFullAccess",
            "arn:aws:iam::aws:policy/AmazonSNSFullAccess"
        ]
      }
    },
}
