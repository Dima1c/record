#!/usr/bin/env make

all:
	python Banner/Banner.py -t wr -b "Unit test of record facility."
	./record.py -u
