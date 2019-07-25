TEMPLATES=$(shell for l in $$(ls ./templates );do echo templates/$$l;done)
.PHONY: build containers lambda website assets

all: build containers lambda templates assets

assets: build 
	cp -r ./assets/* ./build

lambda: build
	make -C lambda

build:
	mkdir -p build; mkdir -p build/templates ; mkdir -p build/lambda; mkdir -p build/sagebuild/lambda

containers: build
	make -C containers

templates: build
	for l in $(TEMPLATES); do	\
		$$l/bin/check.js; \
	done;			

