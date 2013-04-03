#!/usr/bin/python
# -*- coding: utf8 -*-

# template for find possible instances of the gomūtrikā ('cow-piss') formation in Sanskrit literature

import SyllableTools


# a verse is gomūtrikā if even syllables match
def isGomutrika(firstline, secondline):
	count =len(firstline)
	print count, ' + ', len(secondline)
	for i in xrange(count):
		if  i % 2 == 0:
			print firstline[i] + ' : ' + secondline[i]
			if firstline[i] != secondline[i]:
				return False
	return True

# input: 		File object
# output: 
def identifyGomutrika(file):
	verses = dict()	# this will have the verse number and the line ( I think)
	syl1 = []	# syllables in first line
	syl2 = []	# syllables in second line
	for line in file:
		line = line.rstrip()
		if len(syl1) == 0:
			syl1 = SyllableTools.parseSyllables(line)
		elif len(syl2) == 0:
			syl2 = SyllableTools.parseSyllables(line)
		else:
			# both lists are full, so we have a complete verse
			print 'Gomūtrikā? ', isGomutrika(syl1, syl2)
			
			# last thing to do is empty the lists
			syl1 = []
			syl2 = []
	
	return verses