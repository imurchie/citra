#!/usr/bin/python
# -*- coding: utf8 -*-


# Tools for working with verses.
# Main external function is 'parseVerse()', in which is encapsulated the means to
# isolate a single verse from a file

import sys, io, codecs
import re
from types import *
from SyllableTools import parseSyllables


"""
Pada Class
- Used in Verse
"""
class Pada(list):
	_syllables = None
	_current = None
	
	def __init__(self, pada):
		self._syllables = []
		self._current = -1
		
		# input can be a string, or a list of syllables
		if isinstance(pada, UnicodeType):
			self._syllables = parseSyllables(pada)
		elif isinstance(pada, ListType):
			# deep copy
			for syllable in pada:
				self._syllables.append(syllable)
		else:
			raise ValueError('Pada should be string or list of syllables: ' + str(type(pada)))
	
	def __str__(self):
		return unicode(self).encode('utf-8')
	
	def __unicode__(self):
		string = u''
		for syllable in self._syllables:
			string += syllable
		return string
		
	def __len__(self):
		return len(self._syllables)
	
	""" implement Iterator """
	def __iter__(self):
		return self

	
	def next(self):
		self._current += 1
		if self._current == len(self._syllables):
			self._current = -1		# reset so we can iterate multiple times if need be
			raise StopIteration
		else:
			return self._syllables[self._current]
# End Pada class


"""
Verse Class
Refactored version of a class to hold a Sanskrit verse.
- Extended handling of the verse quarters to be able to deal with verses that don't have four quarters.
"""
class Verse:
	_id = None				# Verse id as <string>
	_text = None			# Text identifier as <string>
	_padas = None		# Verse quarters as <list>
	_current = None	# Counter for Iterator implementation
	
	def __init__(self, verse_id, padas=[]):
		self._id = verse_id
		self._current = -1	# this will increment to 0 in the first iteration of next()
		
		# deep copy the quarters, so they are immutable from outside
		# the input can be a list of either lists of syllables, or of strings
		self._padas = []
		for pada in padas:
			if isinstance(pada, Pada):
				self._padas.append(pada)
			elif isinstance(pada, UnicodeType):
				self._padas.append(Pada(pada))
			else:
				raise ValueError('Padas should be strings or Padas: ' + str(type(pada)))
	
	def __str__(self):
		return unicode(self).encode('utf-8')
	
	def __unicode__(self):
		# first build a string
		string = u''
		if  not isinstance(self._id, NoneType):
			string += self._id
		string += u'\n'
		for pada in self._padas:
			string += unicode(pada)
			string += u'\n'
			
		return string
	
	def __len__(self):
		return len(self._padas)
	
	""" implement Iterator """
	def __iter__(self):
		return self

	
	def next(self):
		self._current += 1
		if self._current == len(self._padas):
			self._current = -1		# reset so we can iterate multiple times if need be
			raise StopIteration
		else:
			return self._padas[self._current]
	
	def get_id(self):
		return self._id
		
	def get_padas(self):
		return self._padas
	
	def get_pada_len(self):
		if len(self._padas) != 0:
			return len(self._padas[0])
		else:
			return 0
#End Verse class

	


# returns any numbers, perhaps separated by a period.
def _get_identifier(line, identifier):
	numbers = re.search('[\d]+\.[\d]+', line)
	if numbers != None:
		if identifier == None:
			identifier = str(numbers.group())
		else:
			identifier = identifier + '/' + str(numbers.group())
	
	return identifier



# This function assumes that a valid Sanskrit line will have either a '|' or '/' at the end of it
def _is_sanskrit_line(line):
	delim = re.search('[\|\/]', line)
	
	# however, many files, especially from GRETIL, have a url in the preface
	# luckily 'www' is NEVER a valid Sanskrit sequence
	try:
		line.index('www')
		return False
	except ValueError, ve:
		return delim != None



# returns any non-digits that are not '|' or '/'
def _get_text(line):
	letters = re.match('[^\d\|\/]*', line)
	
	if letters != None:
		return letters.group()
	else: 
		return None


# Expects a file opened as a Unicode stream
# Verses are taken to be two lines long, with verses separated by spaces
# Return:	Verse object
def parse_verse(file):
	identifier = None
	lines = []
	
	try:
		for line in file:
			line = line.replace(' ', '')
			line = line.strip()
			
			if len(line) != 0:
				if _is_sanskrit_line(line):
					identifier = _get_identifier(line, identifier)		# get any numbers in the line
					
					text = _get_text(line)
					if text != None:
						lines.append(text)
				else:
					# this is not a Sanskrit line
					continue
			else:
				# this line is empty
				# if we have anything, then return, otherwise continue
				if len(lines) != 0:
					break
				else:
					continue
		
		# if there are no lines to report, raise exception to end
		if len(lines) == 0:
			raise StopIteration('End')
		
		# at this point we have the lines of text in 'lines'
		lines_syl = []
		for line in lines:
			lines_syl.append(parseSyllables(line))
		
		# if there are only two, at this point assume that they are verse halves that need to be split
		padas = []
		for line in lines_syl:
			padas.append(Pada(line[0:len(line) / 2]))
			padas.append(Pada(line[len(line) / 2:len(line)]))
		return Verse(identifier, padas)
	except IOError, io:
		print 'IOError reading file', io
		sys.exit(1)
		



# unit test
if __name__ == '__main__':
	pada_string = u'athāgre hasatā sācisthitena sthirakīrtinā'
	pada_string2 = u'senānyā te jagadire kiṃcidāyastacetasā'
	pada = Pada(pada_string)
	
	verse = Verse('2', [pada, pada_string2])
	print verse.get_id()
	for pada in verse:
		print pada
	
	verse2 = Verse('3', [pada_string2])
	print verse2
	
	try:
		print 'Testing verse parsing'
		file = codecs.open('./data/niyama_test.txt', encoding='utf-8')
		print parse_verse(file)
	except IOError, io:
		print 'There was an error reading file: ' + str(io)
		sys.exit(1)

