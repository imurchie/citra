#!/usr/bin/python
# -*- coding: utf8 -*-


# script for identifying possible citra figures in text files of Sanskrit works
# 

import sys
import codecs

import gomutrika
import VerseTools


# Opens a file and figures out what figure to look for


def logWrite(log, verse):
	if verse[0] != None:
		log.write(verse[0])
	else:
		log.write('No id')
	log.write('\n')
	if verse[1] != None:
		log.write('    ab: ' + verse[1])
	else:
		log.write('    ab: ')
	log.write('\n')
	if verse[2] != None:
		log.write('    cd: ' + verse[2])
	else:
		log.write('    cd: ')
	log.write('\n\n')
	


# pass in argument to tell what figure to look for
# for the moment, hard-code for "gomutrika" (which is the only one being worked on)
figure = 'gomutrika'
try:
	if figure == 'gomutrika':
		#file = codecs.open('./data/gomutrika_test.txt', encoding='utf-8')
		file = codecs.open('./data/Kirātārjunīya.txt', encoding='utf-8')
		
		log = codecs.open('./log.txt', 'w', encoding='utf-8')
		
		try:
			count_gm = 0
			count_vs = 0
			while file:
				verse = VerseTools.parseVerse(file)
				count_vs += 1
				logWrite(log, verse)
				
				gm = gomutrika.isGomutrika(verse)
				if gm:
					count_gm += 1
		except StopIteration, si:
			print 'We\'re done: ', count_gm, 'gomūtrikā figure(s) in', count_vs, 'verses.'
	else:
		print 'No other figure implemented yet.'
		sys.exit(1)
except IOError, io:
	print 'There was an error reading file: ' + str(io)
	sys.exit(1)