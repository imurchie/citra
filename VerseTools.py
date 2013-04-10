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
	
	# for Iterator implementation
	current = 0
	
	# initialize the object with an id
	def __init__(self, verse_id):
		self.id = verse_id
		self.current = 0
	
	
	# it is difficult to split a half-verse into two quarters
	# with just a string
	# input: verse_id as String
	#				pada_ab, pada_cd as Strings
	def __init__(self, verse_id, pada_ab, pada_cd):
		self.id = verse_id
		self.current = 0
		
		if type(pada_ab) is UnicodeType:
			ab = parseSyllables(pada_ab)
		elif type(pada_ab) is ListType:
			ab = pada_ab
		else:
			raise ValueException('First half of verse of wrong type (\'' + str(type(pada_ab)) + '\')')
		if type(pada_cd) is UnicodeType:
			cd = parseSyllables(pada_cd)
		elif type(pada_cd) is ListType:
			cd = pada_cd
		else:
			raise ValueException('Second half of verse of wrong type (\'' + str(type(pada_cd)) + '\')')
		
		half_length = len(ab)
		quarter_length = half_length / 2
		
		self.pada_a = ab[0:quarter_length]
		self.pada_b = ab[quarter_length:half_length]
		self.pada_c = cd[0:quarter_length]
		self.pada_d = cd[quarter_length:half_length]
	
		
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
		verse_string = self.getId() + '\n'
		verse_string += self.getPadaString(Verse.A) + '\n'
		verse_string += self.getPadaString(Verse.B) + '\n'
		verse_string += self.getPadaString(Verse.C) + '\n'
		verse_string += self.getPadaString(Verse.D) + '\n'
		return verse_string
	
	
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
	
	
	""" implement Iterator """
	def __iter__(self):
		return self

	
	def next(self):
		if self.current == 4:		# there can only be four quarters
			self.current = 0			# reset so we can iterate multiple times if need be
			raise StopIteration
		else:
			pada = None
			if self.current == 0:
				pada = self.getPada(Verse.A)
			elif self.current == 1:
				pada = self.getPada(Verse.B)
			elif self.current == 2:
				pada = self.getPada(Verse.C)
			elif self.current == 3:
				pada = self.getPada(Verse.D)
			self.current += 1
            
			return pada
	


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
# Return:	Verse object
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
							# oops. The line is not empty but we have two lines already
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
		
		print 'ab: ', pada_ab
		print 'cd: ', pada_cd
		
		# now assemble the result and pass it back
		return  Verse(identifier, pada_ab, pada_cd)
	except IOError, io:
		print 'IOError reading file', io
		sys.exit(1)




