#!/usr/bin/python
# -*- coding: utf8 -*-


# script for identifying possible citra figures in text files of Sanskrit works
# 

import sys
import codecs

import gomutrika
import Padma
import Sarvatobhadra
import Niyama

import VerseTools




# possible figures
FIGURES = ['gomūtrikā', 'padma', 'sarvatobhadra', 'niyama']


def logWrite(log, verse):
	log.write(unicode(verse))
	

def processRequest(figure, filename):
	try:
		#file = codecs.open('./data/gomutrika_test.txt', encoding='utf-8')
		#file = codecs.open('./data/Kirātārjunīya.txt', encoding='utf-8')
		#file = codecs.open('./data/Kumārasaṃbhava.txt', encoding='utf-8')
		#file = codecs.open('./data/padma_test.txt', encoding='utf-8')
		file = codecs.open(filename, encoding='utf-8')
		
		log = codecs.open('./log.txt', 'w', encoding='utf-8')
	
	
		# get the correct function to call
		function = None
		if figure == 'gomutrika' or figure == u'gomūtrikā':
			function = gomutrika.isGomutrika
		elif figure == 'padma':
			function = Padma.isPadma
		elif figure == 'sarvatobhadra':
			function = Sarvatobhadra.isSarvatobhadra
		elif figure == 'niyama':
			function = Niyama.isNiyama
		else:
			print 'No other figure implemented yet.'
			sys.exit(1)
	
		# process the file
		verses = []
		try:
			count_figure = 0
			count_verse = 0
			while file:
				verse = VerseTools.parse_verse(file)
				count_verse += 1
				logWrite(log, verse)
				
				figure = function(verse)
				if figure:
					count_figure += 1
					verses.append(verse)
		except StopIteration, si:
			print 'We\'re done: ', count_figure, 'figure(s) in', count_verse, 'verses.'
	except IOError, io:
		print 'There was an error reading file: ' + str(io)
		sys.exit(1)

	print 'Verses: ', verses
	return verses