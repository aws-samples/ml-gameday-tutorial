var _=require('lodash')

module.exports=Object.assign({
    "LayoutPipeline":{
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
                    trainsourcefile:"s3://${AssetBucket}/${AssetPrefix}/layout-first.tar.gz",
                    trainentrypoint:"train.py",
                    hostsourcefile:"s3://${AssetBucket}/${AssetPrefix}/layout-first.tar.gz",
                    hostentrypoint:"host.py",
                    frameworkversion:"1.3.0",
                    configtrain:"SAGEMAKER",
                    hyperparameters:{
                        team:"jmc",
                        num_shots:"30"
                    },
                    metrics:[],
                    channels:{
                        train:{
                            path:"all/data.json"
                        }
                    },
                    trainvolumesize:"5",
                    traininstancecount:1,
                    hostinstancetype:"ml.t2.medium",
                    traininstancetype:"ml.m5.large",
                })}
            }
        }
    },
}
)
