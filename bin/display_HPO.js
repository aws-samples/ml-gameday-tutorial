#! /usr/bin/env node
var config=require('../config')
process.env.AWS_PROFILE=config.profile
var aws=require('aws-sdk')
aws.config.region=config.region
var sagemaker=new aws.SageMaker()
var _=require('lodash')

var job=process.argv[2]
var state=process.argv[3] || "InProgress"
var blessed = require('blessed')
     , contrib = require('blessed-contrib')
     , screen = blessed.screen()

var grid = new contrib.grid({rows: 12, cols: 12, screen: screen})

var table_completed = grid.set(0,0,6,12,contrib.table,{ 
    keys: true
     , fg: 'white'
     , selectedFg: 'white'
     , selectedBg: 'blue'
     , interactive: true
     , label: `Completed Jobs for ${job}`
     , width: '100%'
     , height: '40%'
     , border: {type: "line", fg: "cyan"}
     , columnSpacing: 8 //in chars
     , columnWidth: [12,12,12,12,12] /*in chars*/ })
var table_inprogress = grid.set(6,0,6,12,contrib.table,
 { keys: true
 , fg: 'white'
 , selectedFg: 'white'
 , selectedBg: 'blue'
 , interactive: true
 , label: `InProgress Jobs for ${job}`
 , width: '100%'
 , height: '40%'
 , border: {type: "line", fg: "cyan"}
 , columnSpacing: 8 //in chars
 , columnWidth: [12,12,12,12] /*in chars*/ })
//allow control the table with the keyboard
screen.key(['c'], function(ch, key) {
    table_completed.focus()
});
screen.key(['i'], function(ch, key) {
    table_inprogress.focus()
});

screen.key(['escape', 'q', 'C-c'], function(ch, key) {
 return process.exit(0);
});

Promise.all([
    sagemaker.listTrainingJobsForHyperParameterTuningJob({
        HyperParameterTuningJobName:job,
        MaxResults:100,
        //SortBy:"FinalObjectiveMetricValue",
        //SortOrder:"Ascending",
        StatusEquals:"Completed"
    }).promise().then(result=>{
        out=_.get(result,"TrainingJobSummaries",[])
            .map(x=>{
                out=_.mapValues(x.TunedHyperParameters,
                    x=>parseFloat(x).toFixed(5))
                //out.id=x.TrainingJobName
                out.Score=_.get(x,"FinalHyperParameterTuningJobObjectiveMetric.Value",0)
                return out
            })

        out.sort((a,b)=>b.Score-a.Score)

        screen.append(table_completed) //must append before setting data
        
        table_completed.setData({ 
            headers:_.keys(out[0]) ,
            data:out.map(_.values)
        })
    }),
    sagemaker.listTrainingJobsForHyperParameterTuningJob({
        HyperParameterTuningJobName:job,
        MaxResults:100,
        StatusEquals:"InProgress"
    }).promise().then(result=>{
        out=_.get(result,"TrainingJobSummaries",[])
            .map(x=>{
                out=_.mapValues(x.TunedHyperParameters,
                    x=>x)
                return out
            })

        //screen.append(table_inprogress) //must append before setting data
        
        table_inprogress.setData({ 
            headers:_.keys(out[0]) ,
            data:out.map(_.values)
        })
    })
]).then(x=>{
    screen.render()
})

function get_data(){
        out=_.get(result,"TrainingJobSummaries",[])
            .map(x=>{
                out=_.mapValues(x.TunedHyperParameters,
                    x=>parseFloat(x).toFixed(5))
                return out
            })

        //screen.append(table_inprogress) //must append before setting data
        
        table_inprogress.setData({ 
            headers:_.keys(out[0]) ,
            data:out.map(_.values)
        })
}
