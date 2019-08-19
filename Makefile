TEMPLATES=$(shell for l in $$(ls ./templates );do echo templates/$$l;done)
.PHONY: build containers lambda website assets

all: build containers 

build:
	mkdir -p build; mkdir -p build

containers: build
	make -C containers
