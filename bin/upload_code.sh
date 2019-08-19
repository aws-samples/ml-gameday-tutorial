#! /bin/bash
__dirname="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export AWS_PROFILE=$(node -e "console.log(require('$__dirname'+'/../config').profile)")
export AWS_DEFAULT_REGION=$(node -e "console.log(require('$__dirname'+'/../config').region)")

LAYOUTBUCKET=$($__dirname/output.js | jq .LayoutCodeBucket --raw-output)
SHOOTBUCKET=$($__dirname/output.js   | jq .ShootCodeBucket --raw-output)

echo "Layout Bucket: $LAYOUTBUCKET"
echo "Shoot Bucket: $SHOOTBUCKET"
aws s3 sync $__dirname/../build s3://$LAYOUTBUCKET --exclude "shoot-*"
aws s3 sync $__dirname/../build s3://$SHOOTBUCKET --exclude "layout-*"
