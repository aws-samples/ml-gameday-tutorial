var _=require('lodash')
var fs=require('fs')
module.exports=Object.assign(
    {},bucket("Data")
)

function bucket(name,opts={}){
    var out=_.fromPairs([
        [`${name}Bucket`,{
            "Type" : "AWS::S3::Bucket",
            "Properties" : {
            }
        }],
        [`${name}BucketClear`,{
            "Type": "Custom::S3Clear",
            "Properties": {
                "ServiceToken": { "Fn::GetAtt" : ["S3ClearLambda", "Arn"] },
                "Bucket":{"Ref":`${name}Bucket`}
            }
        }],
        opts.lambda ? [`${name}BucketNotification`,{
            "Type": "Custom::S3Notification",
            "DependsOn":["CFNLambdaPolicy",`${name}BucketNotificationPermission`],
            "Properties": {
                "ServiceToken": { "Fn::GetAtt" : ["S3NotificationLambda", "Arn"] },
                "Bucket":{"Ref":`${name}Bucket`},
                NotificationConfiguration:{
                    LambdaFunctionConfigurations:[{
                        Events:["s3:ObjectCreated:*"],
                        LambdaFunctionArn:{"Fn::GetAtt":[opts.lambda,"Arn"]}
                    }]
                }
            }
        }]:null,
        opts.lambda ? [`${name}BucketNotificationPermission`,{
			"Type": "AWS::Lambda::Permission",
			"Properties": {
				"FunctionName":{"Fn::GetAtt":[opts.lambda,"Arn"]},
				"Action": "lambda:InvokeFunction",
				"Principal": "s3.amazonaws.com",
				"SourceAccount": {"Ref": "AWS::AccountId"},
				"SourceArn": {"Fn::GetAtt": [`${name}Bucket`,"Arn"]}
			}
		}]:null
    ].filter(x=>x))
    return out
}
