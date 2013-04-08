#!/usr/bin/python
# -*- coding: utf8 -*-


# Tools for working with verses.
# Main external function is 'parseVerse()', in which is encapsulated the means to
# isolate a single verse from a file

import sys
import re
from types import *
from SyllableTools import parseSyllables


# Verse: a class to encapsulate a verse (which I've been using a tuple for to this point
class Verse:
	id = None
	pada_a = None
	pada_b = None
	pada_c = None
	pada_d = None
	
	# pāda names
	A = 'pada_a'
	B = 'pada_b'
	C = 'pada_c'
	D = 'pada_d'
	
	# initialize the object with an id
	def __init__(self, verse_id):
		self.id = verse_id
	
	# can take strings or lists of syllables
	# stores them as lists of syllables
	def __init__(self, verse_id, pada_a, pada_b, pada_c, pada_d):
		self.id = verse_id
		
		# need to add error handling
		if type(pada_a) is UnicodeType:
			self.pada_a = parseSyllables(pada_a)
		elif type(pada_a) is ListType:
			self.pada_a = pada_a
		if type(pada_b) is UnicodeType:
			self.pada_b = parseSyllables(pada_b)
		elif type(pada_b) is ListType:
			self.pada_b = pada_b
		if type(pada_c) is UnicodeType:
			self.pada_c = parseSyllables(pada_c)
		elif type(pada_c) is ListType:
			self.pada_c = pada_c
		if type(pada_d) is UnicodeType:
			self.pada_d = parseSyllables(pada_d)
		elif type(pada_d) is ListType:
			self.pada_d = pada_d
		
	def getId(self):
		if self.id == None:
			return ''
		return str(self.id)	# cast to string, just in case.
	
	
	# returns a list with the lines of the verse
	def getVerse(self):
		verse = []
		
		# a later pāda will only be valid if an earlier one is non-empty
		if self.pada_a != None:
			verse.append(self.pada_a)
			if self.pada_b != None:
				verse.append(self.pada_b)
				if self.pada_c != None:
					verse.append(self.pada_c)
					if self.pada_d != None:
						verse.append(self.pada_d)
		return verse
	
	def getVerseString(self):
		verse = self.getVerse()
		
		return str(verse)
	
	
	def getPada(self, pada_name):
		pada = None
		if pada_name == self.A:
			pada = self.pada_a
		elif pada_name == self.B:
			pada = self.pada_b
		elif pada_name == self.C:
			pada = self.pada_c
		elif pada_name == self.D:
			pada = self.pada_d
		else:
			# we have a problem
			raise ValueError('No verse quarter \'' + str(pada_name) + '\'.')
		
		if pada == None:
			raise ValueError('Verse quarter \'' + str(pada_name) + '\' empty.')
			
		return pada
	
	def getPadaString(self, pada_name):
		pada = self.getPada(pada_name)
		
		# now make a string from the list of syllables
		pada_string = ''
		for syllable in pada:
			pada_string += syllable
		
		return pada_string
	
	
	# alias of getPada()
	def getQuarter(self, quarter):
		return self.getPada(quarter)
	def getQuarterString(self, quarter):
		return self.getPadaString(quarter)
	


# returns any numbers, perhaps separated by a period.
def getIdentifier(line, identifier):
	numbers = re.search('[\d]+\.[\d]+', line)
	if numbers != None:
		if identifier == None:
			identifier = str(numbers.group())
		else:
			identifier = identifier + '/' + str(numbers.group())
	
	return identifier



# This function assumes that a valid Sanskrit line will have either a '|' or '/' at the end of it
def isSanskritLine(line):
	delim = re.search('[\|\/]', line)
	
	# however, many files, especially from GRETIL, have a url in the preface
	# luckily 'www' is NEVER a valid Sanskrit sequence
	try:
		line.index('www')
		return False
	except ValueError, ve:
		return delim != None



# returns any non-digits that are not '|' or '/'
def getText(line):
	letters = re.match('[^\d\|\/]*', line)
	
	if letters != None:
		return letters.group()
	else: 
		return None


# Expects a file opened as a Unicode stream
# Verses are taken to be two lines long, with verses separated by spaces
# Return:	a tuple
#						identifier (as string, format at the moment varies)
#						First half of verse
#						Second half of verse
def parseVerse(file):
	identifier = None
	pada_ab = None
	pada_cd = None
	
	try:
		for line in file:
			line = line.replace(' ', '')

			if line != None and len(line) != 0:
				# at this point I am going to assume that a Sanskrit line will have a '|' or '/'
				# the problem is arbitrary information before the actual text begins in an etext
				if isSanskritLine(line):
					identifier = getIdentifier(line, identifier)		# get any numbers in the line
					
					text = getText(line) 		# get any text in the line
					if text != None:
						if pada_ab == None:
							pada_ab = text
						elif pada_cd == None:
							pada_cd = text
						else:
							# oops. The line is not empty but  we have two lines already
							# we need to adjust in order to account for multi-line verses
							if len(text) != 0:
								print 'Verse too long: (', identifier, ') ', text
								print '      Pāda ab: ', pada_ab
								print '      Pāda cd: ', pada_cd
							break

			# if we get here an everything is full, we have a verse!
			if pada_ab != None and pada_cd != None:
				break
		
		# if we get here and everything is empty still, we're done.	
		if pada_ab == None and pada_cd == None:
			raise StopIteration('End')
		
		print pada_ab
		print pada_cd
		
		half_length = len(pada_ab)
		quarter_length = half_length / 2
		
		pada_a = pada_ab[0:quarter_length]
		pada_b = pada_ab[quarter_length:half_length]
		pada_c = pada_cd[0:quarter_length]
		pada_d = pada_cd[quarter_length:half_length]
		
		# now assemble the result and pass it back
		#return (identifier, pada_ab, pada_cd)
		print identifier
		print '    ', pada_a
		print '    ', pada_b
		print '    ', pada_c
		print '    ', pada_d
		return  Verse(identifier, pada_a, pada_b, pada_c, pada_d)
	except IOError, io:
		print 'IOError reading file', io
		sys.exit(1)




