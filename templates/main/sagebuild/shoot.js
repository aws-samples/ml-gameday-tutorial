var _=require('lodash')

module.exports=Object.assign({
    "ShootPipeline":{
        "Type" : "AWS::CloudFormation::Stack",
        "Properties" : {
            TemplateURL:{"Fn::Sub":
                "https://s3.amazonaws.com/${AssetBucket}/${AssetPrefix}/sagebuild/templates/main.json"},
            Parameters:{
                "AssetBucket":{"Ref":"AssetBucket"},
                "AssetPrefix":{"Fn::Sub":"${AssetPrefix}/sagebuild"},
                "ConfigFramework":"MXNET",
                "NoteBookInstanceType":"NONE",
                ExternalDataBucket:{"Ref":"DataBucket"},
                "Parameters":{"Fn::Sub":JSON.stringify({
                    deployEndpoint:true,
                    maxtrainingjobs:30,
                    maxparalleltrainingjobs:2,
                    trainmaxrun:5,
                    inputmode:"File",
                    trainsourcefile:"s3://${AssetBucket}/${AssetPrefix}/shoot-line.tar.gz",
                    trainentrypoint:"train.py",
                    hostsourcefile:"s3://${AssetBucket}/${AssetPrefix}/shoot-line.tar.gz",
                    hostentrypoint:"host.py",
                    frameworkversion:"1.3.0",
                    configtrain:"SAGEMAKER",
                    hyperparameters:{},
                    metrics:[{
                        Name:"Validation",
                        Regex:"Testing loss: (.*?);"
                    },{
                        Name:"Training",
                        Regex:"Training loss: (.*?);"
                    },{
                        Name:"Throughput",
                        Regex:"Throughput=(.*?);"
                    }],
                    tuningobjective:{
                        Name:"best_model",
                        Type:"Maximize",
                        Regex:"best model: (.*?);"
                    },
                    channels:{
                    },
                    trainvolumesize:"5",
                    traininstancecount:1,
                    hostinstancetype:"ml.m5.xlarge",
                    traininstancetype:"ml.m5.large",
                })}
            }
        }
    }
}
)
