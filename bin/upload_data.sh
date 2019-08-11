#! /bin/bash

__dirname="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BUCKET=$($__dirname/../templates/main/bin/output.js | jq ".DataBucket" --raw-output)

aws s3 cp $__dirname/../data/data.json s3://$BUCKET/all/data.json
