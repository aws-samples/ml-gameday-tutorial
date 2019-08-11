#! /bin/bash
__dirname="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export AWS_PROFILE=$(node -e "console.log(require('$__dirname'+'/../config').profile)")
export AWS_DEFAULT_REGION=$(node -e "console.log(require('$__dirname'+'/../config').region)")

BUCKET=$(node -e "console.log(require('$__dirname'+'/../config').parameters.GameArchiveBucket)")

BLUE=$(tput setaf 4)
RESET=$(tput sgr0)
echo bootstrap bucket is $BLUE$BUCKET/$PREFIX$RESET

DATA_DIR=$__dirname/../data
mkdir -p $DATA_DIR/tmp 
rm -rf $DATA_DIR/tmp/*;
mkdir -p $DATA_DIR/all 
echo "Downloading data"
aws s3 sync s3://$BUCKET $DATA_DIR/tmp/

echo "uncompressing data"
rm $DATA_DIR/data.json;
for file in $(find $DATA_DIR/tmp/ -name '*.gz'); do
    name=$(basename $file | cut  -d. -f1)
    cat $file | gunzip >> $DATA_DIR/data.json
done
head -n 10 $DATA_DIR/data.json > $DATA_DIR/data.min.json

echo "Data file is located at $DATA_DIR/data.json"
echo "sample data file is located at $DATA_DIR/data.json"
