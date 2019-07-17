#! /usr/bin/env node
var aws=require('../templates/main/bin/aws')
var sns=new aws.SNS()
var cloudformation=new aws.CloudFormation()
var step=new aws.StepFunctions()
var config=require('../config')
var GetOutput=require('../templates/main/bin/output').run

GetOutput().then(async output=>{
    var result=await sns.publish({
        Message:"{}",
        TopicArn:output.ShootLaunchTopic   
    }).promise()
    console.log("Layout pipeline started succesfully")
    console.log(result)
    return output
})
.then(async output=>{
    return new Promise(async (res,rej)=>{
        setTimeout(x=>next(),5000)
        async function next(){
            var executions=await step.listExecutions({
                stateMachineArn:output.ShootStateMachine,
                statusFilter:"RUNNING"
            }).promise()

            if(executions.executions.length>0){
                process.stdout.write('.')
                setTimeout(x=>next(),5000)
            }else{
                console.log('finished')
                res()
            }
        }
    })
})
.catch(e=>{
    console.log("SageBuild pipeline failed")
    console.log(e)
})
