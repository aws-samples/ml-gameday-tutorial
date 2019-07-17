#! /bin/bash

../templates/main/bin/output.js | jq '{"layoutEndpoint":.LayoutEndpoint,"shootEndpoint":.ShootEndpoint,"RoleArn":.CrossAccountRole,"ErrorSNSTopicArn":.ErrorTopic}'
