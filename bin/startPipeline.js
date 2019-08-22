#! /usr/bin/env node
var aws=require('./aws')
var sns=new aws.SNS()
var cloudformation=new aws.CloudFormation()
var step=new aws.StepFunctions()
var args=require('args')
var ssm=new aws.SSM()
var config=require('../config')
var GetOutput=require('./output').run
const { exec } = require('child_process')

args.option('pipeline',"layout or shoot, which pipeline to start")
    .example("startPipline --pipeline layout","starts the Layout pipeline")
    .example("startPipline --pipeline shoot","starts the Shoot pipeline")
const flags=args.parse(process.argv)
if(!flags.pipeline.match(/shoot|layout/)){
    console.log("pipeline must be either shoot or layout")
    process.exit()
}
var pipeline=flags.pipeline==="shoot" ? "ShootLaunchTopic" : "LayoutLaunchTopic"
var paramstore=flags.pipeline==="shoot" ? "ShootParams" : "LayoutParams"
var statemachine=flags.pipeline==="shoot" ? "ShootStateMachine" : "LayoutStateMachine"

console.log("building and uploading code")
run('npm run upload').then(console.log)
.then(x=>{
    console.log("getting stack output")
    return GetOutput()
})
.then(async output=>{
    console.log("Updating Parameter store")
    var params=JSON.parse((await ssm.getParameter({
        Name:output[paramstore]
    }).promise()).Parameter.Value)
    Object.assign(params, require(`../${flags.pipeline}-config`))
    
    await ssm.putParameter({
        Name:output[paramstore],
        Type:"String",
        Value:JSON.stringify(params),
        Overwrite:true
    }).promise()

    console.log("Starting pipeline")
    var result=await sns.publish({
        Message:"{}",
        TopicArn:output[pipeline]   
    }).promise()
    console.log("pipeline started succesfully. waiting to finish")
    return output
})
.then(async output=>{
    count=0
    return new Promise(async (res,rej)=>{
        setTimeout(x=>next(),5000)
        async function next(){
            var executions=await step.listExecutions({
                stateMachineArn:output[statemachine],
                statusFilter:"RUNNING"
            }).promise()

            if(executions.executions.length>0){
                count++
                process.stdout.write(count%20===0 ? '\n' : '.')
                setTimeout(x=>next(),5000)
            }else{
                console.log('finished: check execution for status')
                res()
            }
        }
    })
})
.catch(e=>{
    console.log("SageBuild pipeline failed")
    console.log(e)
})

function run(cmd) {
  return new Promise((resolve, reject) => {
    exec(cmd, (error, stdout, stderr) => {
      if (error) return reject(error)
      if (stderr) return reject(stderr)
      resolve(stdout)
    })
  })
}
