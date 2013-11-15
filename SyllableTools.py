#!/usr/bin/python
# -*- coding: utf8 -*-



# input:		letter as string
# output:	boolean
def isVowel(letter):
	return letter == u'a' \
		or letter == u'ā' \
		or letter == u'i' \
		or letter == u'ī' \
		or letter == u'u' \
		or letter == u'ū' \
		or letter == u'ṛ' \
		or letter == u'ṝ' \
		or letter == u'ḷ' \
		or letter == u'ḹ' \
		or letter == u'o' \
		or letter == u'e'


def isVisarga(letter):
	return letter == u'ḥ'


def isAnusvara(letter):
	return letter == u'ṃ' or letter == u'ṁ'


# this will be abstracted out to use for all the figures.
# a syllable in this context:
#			0-N consonants
#			one vowel
#			trailing visarga or anusvāra
#
# input: 		line of text
# output: 	tuple (syllable, remainder of line)
def getNextSyllable(line):
	syllable = ''	# we will fill this with the syllable

	# loop through the line until a syllable is found
	vowel = False	# not yet found a vowel
	while len(line) > 0:
		letter = line[0]

		if letter == ' ':
			# do nothing
			letter = ' '
		elif isVowel(letter):
			vowel = True
			syllable += letter
		elif vowel == False:
			# if we haven't found a vowel, whatever it is, it goes in the syllable
			syllable += letter
		else:
			# if we're here, we've already found a vowel, and what we have is NOT a vowel
			# we want to put it in the syllable if it is a visarga or anusvāra
			if isVisarga(letter):
				syllable += letter
				line = line[1:len(line)]
			elif isAnusvara(letter):
				syllable += letter
				line = line[1:len(line)]
			#else:
			break

		# take the letter off the line, as it is in the syllable
		line = line[1:len(line)]

	# make and return the requisite tuple
	return (syllable, line)



# parses a line into its syllables
# input:		line as string
# output:	syllables as list
def parseSyllables(line):
	syllables = []

	# for now we're just stripping off the daṇḍas
	line = line.rstrip('|')

	while len(line) > 0:
		temp = getNextSyllable(line)
		syllable = temp[0]
		line = temp[1]
		syllables.append(syllable)

	return syllables
