BATCHES=$(shell for l in $$(ls . | grep -v tmp | grep -v README.md | grep -v Makefile);do echo ./$$l;done)

.PHONY: build 

build: $(BATCHES)
	for container in $(BATCHES); do\
		$(MAKE) -C $$container;	\
	done	\
		
