#! /usr/bin/env node
var aws=require('./aws')
var fs=require('fs')
var Promise=require('bluebird')
var cf=new aws.CloudFormation()
var s3=new aws.S3()
var chalk=require('chalk')
var config=require('../config')
var bucket=config.templateBucket

if(require.main === module){
    run()
}
module.exports=run
async function run(){
    var obj=require('../')
    var template=JSON.stringify(obj,null,2)
    
    var result=await cf.validateTemplate({
        TemplateBody:template
    }).promise()

    console.log(result)
    console.log(`Resources: ${Object.keys(obj.Resources).length}`)
    return JSON.stringify(obj,null,2)
}
