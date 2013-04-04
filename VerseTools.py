#!/usr/bin/python
# -*- coding: utf8 -*-


# Tools for working with verses.
# Main external function is 'parseVerse()', in which is encapsulated the means to
# isolate a single verse from a file

import sys
import re


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
			line = line.rstrip()
			line = line.strip()

			print 'l: ', line

			if line != None and len(line) != 0:
				print '    processing...'
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
		
		# now assemble the result and pass it back
		return (identifier, pada_ab, pada_cd)
	except IOError, io:
		print 'IOError reading file', io
		sys.exit(1)




