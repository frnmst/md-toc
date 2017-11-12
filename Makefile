#!/usr/bin/env make

default: test

install:
	python setup.py install

test:
	python setup.py test

.PHONY: test install

