
module.exports={
  "Parameters":{
    "MasterAccount":{
        "Type":"String"
    },
    "GameArchiveBucket":{
        "Type":"String"
    }
  },
  "Outputs":{
       
  },
  "Resources":Object.assign(
    require('./cfn'),
    require('./codecommit'),
    require('./notebooks'),
    require('./s3')
  ),
  "AWSTemplateFormatVersion": "2010-09-09",
  "Description": ""
}
