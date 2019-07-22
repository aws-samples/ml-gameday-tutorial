module.exports={
  "Parameters":{
    "CodeCommitRepoName":{
        "Type":"String",
        "Description":"the name of the AWS CodeCommit repository for your teams code"
    }
  },
  "Outputs":{
    "JuypterURL":{
        "Value":{"Fn::Sub":"https://console.aws.amazon.com/sagemaker/home?region=${AWS::Region}#/notebook-instances/openNotebook/${Notebook.NotebookInstanceName}"},
        "Description":"URL to access jupyter notebook"
    },
  },
  "Resources":Object.assign(
    {},
    require('./notebook')
  ),
  "AWSTemplateFormatVersion": "2010-09-09",
  "Description": "Creates a SageMaker Notebook instance with admin permissions",
  "Metadata":{
    "AWS::CloudFormation::Interface" : {
        "ParameterGroups":[],
        "ParameterLabels":{
        }
    }
  }
}
