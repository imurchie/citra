#!/usr/bin/python
# -*- coding: utf8 -*-


# script for identifying possible citra figures in text files of Sanskrit works
# 

import sys
import gomutrika


# Opens a file and figures out what figure to look for


# pass in argument to tell what figure to look for
# for the moment, hard-code for "gomutrika" (which is the only one being worked on)
figure = 'gomutrika'
try:
	if figure == 'gomutrika':
		file = open('./data/gomutrika_test.txt', 'r')
		verses = gomutrika.identifyGomutrika(file)
	else:
		print 'No other figure implemented yet.'
		sys.exit(1)
except IOError, io:
	print "There was an error reading file: " + str(io)
	sys.exit(1)

print verses