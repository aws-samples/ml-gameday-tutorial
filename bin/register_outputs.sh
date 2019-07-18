#! /bin/bash

__dirname="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
$__dirname/../templates/main/bin/output.js | jq '{"layoutEndpoint":.LayoutEndpoint,"shootEndpoint":.ShootEndpoint,"RoleArn":.CrossAccountRole,"ErrorSNSTopicArn":.ErrorTopic}'
