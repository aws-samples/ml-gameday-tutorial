var fs=require('fs')

module.exports={
    "AssetBucket": {
      "Type": "AWS::S3::Bucket",
      "Properties": {
        "VersioningConfiguration":{
            "Status":"Enabled"
        },
        "LifecycleConfiguration":{
            "Rules":[{
                "Status":"Enabled",
                "NoncurrentVersionExpirationInDays":1
            }]
        }
      }
    },
    "AssetBucketClear":{
        "Type": "Custom::S3Clear",
        "DependsOn":["CFNLambdaPolicy"],
        "Properties": {
            "ServiceToken": { "Fn::GetAtt" : ["S3ClearLambda", "Arn"] },
            "Bucket":{"Ref":"AssetBucket"}
        }
    },
  }
