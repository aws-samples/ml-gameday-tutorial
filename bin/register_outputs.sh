#! /bin/bash

__dirname="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
$__dirname/output.js | jq '{"layoutEndpoint":.LayoutEndpoint,"shootEndpoint":.ShootEndpoint,"ErrorSNSTopicArn":.ErrorTopic,"RoleArn":.CrossAccountRole}'
