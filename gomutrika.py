#!/usr/bin/python
# -*- coding: utf8 -*-

# template for find possible instances of the gomūtrikā ('cow-piss') formation in Sanskrit literature

import SyllableTools

# input: 		File object
# output: 
def identifyGomutrika(file):
	verses = dict()	# this will have the verse number and the line ( I think)
	for line in file:
		line = line.rstrip()
		syllables = SyllableTools.parseSyllables(line)
		
		# at this point we have the line parsed into valid syllables
		print syllables
	
	return verses