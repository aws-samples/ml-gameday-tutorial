#! /usr/bin/env python
import boto3
import json
import subprocess

# need to gather the config and the AWS credential profile to use
config=subprocess.check_output(
    ['node','-e',"console.log(JSON.stringify(require('../config')))"]).decode('utf-8')
config=json.loads(config)
session = boto3.Session(profile_name=config["profile"])

# need to get the outputs of the cloudformation so we know what endpoints to send requests to
output=subprocess.check_output(
    ['../templates/main/bin/output.js']).decode('utf-8')
output=json.loads(output)

client = session.client('sagemaker-runtime')
def invoke(endpoint,body):
    response = client.invoke_endpoint(
        EndpointName=output[endpoint],
        Body=json.dumps(body),
        ContentType="application/json",
        Accept="application/json"
    )
    return json.loads(response["Body"].read())

if __name__ == "__main__":
    resp=invoke("LayoutEndpoint",{
        "opponent":"test",
        "width":10,
        "height":10,
        "ruleSet":{
            "shipCells":10,
            "connectedShipCells":5
        }
    })
    print(resp)
