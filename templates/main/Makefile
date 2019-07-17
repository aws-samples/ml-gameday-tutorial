.PHONY:build
all:build ../assets/notebooks.zip

build:index.js cfn/* 
	node ./bin/check.js 

../assets/notebooks.zip:sagebuild/notebook
	zip -rvj ../../assets/notebooks.zip sagebuild/notebook/*;
