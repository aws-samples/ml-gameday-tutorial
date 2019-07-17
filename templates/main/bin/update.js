#! /usr/bin/env node

var check=require('./check')
var aws=require('aws-sdk')
var config=require('../config')
var cf=new aws.CloudFormation({region:config.region})
var name=require('./name')
var wait=require('./wait')
var bucket=config.templateBucket
var bootstrap=require('../../bootstrap/bin/output')
var _=require('lodash')
if(require.main===module){
    run()
}

async function run(){
    var template=await check()
    var outputs=await bootstrap() 
 
    var result=await cf.updateStack({
        StackName:await name.get(),
        Capabilities:["CAPABILITY_NAMED_IAM"],
        TemplateURL:`http://s3.amazonaws.com/${outputs.AssetBucket}/${outputs.AssetPrefix}/templates/main.json`,
        Parameters:_.map(Object.assign(config.parameters,outputs)
            ,(value,key)=>{return{
                ParameterKey:key,
                ParameterValue:value
            }})
    }).promise()
    await wait()
}
