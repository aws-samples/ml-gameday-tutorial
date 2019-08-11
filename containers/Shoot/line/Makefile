NAME:=$(shell basename $(shell pwd) )
DST=../../../build/shoot-$(NAME).tar.gz

all: $(DST)

$(DST): host.py train.py
	echo "Building $(NAME) tar"; rm $(DST);  tar -zcvf $(DST) --exclude='./tmp/' --exclude='./mock/' . 


