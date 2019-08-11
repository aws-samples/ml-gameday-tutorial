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
                    trainsourcefile:"s3://${AssetBucket}/${AssetPrefix}/shoot-CNN.tar.gz",
                    trainentrypoint:"train.py",
                    hostsourcefile:"s3://${AssetBucket}/${AssetPrefix}/shoot-CNN.tar.gz",
                    hostentrypoint:"host.py",
                    frameworkversion:"1.3.0",
                    configtrain:"SAGEMAKER",
                    hyperparameters:{
                        epochs:200,
                        learning_rate:"0.005",
                        width:"64",
                        depth:"15",
                        patience:"10",
                        batch_size:"1024"
                    },
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
                        train:{
                            path:"all/data.json"
                        },
                        model:{
                            uri:"s3://ai-command-dev-5-shootpipeline-70r-artifactbucket-dhab788wzmi0/ai-command-dev-5-ShootPipeline-70RCEKQOT261-v3-1565463332612/output/model.tar.gz"
                        }
                    },
                    trainvolumesize:"5",
                    traininstancecount:1,
                    hostinstancetype:"ml.m5.xlarge",
                    traininstancetype:"ml.p3.8xlarge",
                })}
            }
        }
    }
}
)
