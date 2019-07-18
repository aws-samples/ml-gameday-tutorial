.PHONY:build

all:build ../assets/notebooks.zip

build:
	mkdir -p build && node ./bin/check.js 

../assets/notebooks.zip:sagebuild/notebook
	zip -rvj ../../assets/notebooks.zip sagebuild/notebook/*;
