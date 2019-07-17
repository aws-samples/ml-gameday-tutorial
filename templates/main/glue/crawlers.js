var _=require('lodash')

module.exports={
    "ArchiveCrawler":{
        "Type" : "AWS::Glue::Crawler",
        "Properties" : {
            Role:{"Fn::GetAtt":["CrawlerRole","Arn"]},
            DatabaseName:{"Ref":"DataCatalog"},
            Targets:{
                S3Targets:[{
                    Path:{"Fn::Sub":"${GameArchiveBucket}/"}
                }]
            },
            Schedule:{
                ScheduleExpression:"cron(0 * * * ? *)"
            },
            Configuration:JSON.stringify({
                "Version": 1.0,
                "CrawlerOutput": {
                    "Partitions": { 
                        "AddOrUpdateBehavior": "InheritFromTable" 
                    },
                    Tables:{
                        AddOrUpdateBehavior:"MergeNewColumns"
                    }
               }
            })
        }
    }
}
