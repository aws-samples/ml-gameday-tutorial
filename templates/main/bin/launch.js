#! /usr/bin/env node
var config=require('../config')
console.log(config)
var check=require('./check')
var aws=require('./aws')
var cf=new aws.CloudFormation({region:config.region})
var name=require('./name')
var wait=require('./wait')
var _=require('lodash')

var bootstrap=require('../../bootstrap/bin/output')
if(require.main===module){
    run()
}

async function run(){
    await name.inc()
    var outputs=await bootstrap() 
    var template=await check()
    
    var result=await cf.createStack({
        StackName:name.get(),
        Capabilities:["CAPABILITY_NAMED_IAM"],
        DisableRollback:true,
        TemplateURL:`http://s3.amazonaws.com/${outputs.AssetBucket}/${outputs.AssetPrefix}/templates/main.json`,
        Parameters:_.map(Object.assign(config.parameters,outputs),
            (value,key)=>{return{
                ParameterKey:key,
                ParameterValue:value
            }})
    }).promise()
    await wait()
}
