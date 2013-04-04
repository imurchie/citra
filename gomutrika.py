#!/usr/bin/python
# -*- coding: utf8 -*-

# template for find possible instances of the gomūtrikā ('cow-piss') formation in Sanskrit literature

import SyllableTools


# a verse is gomūtrikā if even syllables match, or odd syllables match
#
# input:		firstline as list of syllables
#					secondline as list of syllables
#					even as Boolean (True if searching even syllables, False if odd
# ouput:		Boolean, True if syllables are equal, False otherwise.
def isGomutrikaInternal(firstline, secondline, even):
	if len(firstline) != len(secondline):
		return False
	
	# go through the syllables and compare them
	for i in xrange(len(firstline)):
		if  (even == True and i % 2 == 0) or (even == False and i % 2 != 0):
			if firstline[i] != secondline[i]:
				return False
	return True



# input: 		Verse as tuple (identifier, Pada ab, Pada cd)
# output: 	Boolean 
def isGomutrika(verse):
	if verse[1]  == None or verse[2] == None:
		print "Something is wrong: ", verse
		return
		
	syl1 = SyllableTools.parseSyllables(verse[1])
	syl2 = SyllableTools.parseSyllables(verse[2])
	
	if isGomutrikaInternal(syl1, syl2, True) or isGomutrikaInternal(syl1, syl2, False):
		print 'GOMŪTRIKĀ: ', verse
		return True
