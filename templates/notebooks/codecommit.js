module.exports={
    "Repo":{
        "Type" : "AWS::CodeCommit::Repository",
        "Properties" : {
            "RepositoryDescription" : "Repository of your code for the ml gameday",
            "RepositoryName":{"Fn::Sub":"GameDayRepo-${AWS::StackName}"}
        }
    }
}
