#!/usr/bin/python
# -*- coding: utf8 -*-


# implements the test for the padma ('lotus') figure

from SyllableTools import parseSyllables
from VerseTools import Verse



# the most basic requirement of the padma figure is that
# the first and last syllables of all the quarters be the same
def isPadma(verse):
	#pada_ab = parseSyllables(verse[1])
	#pada_cd = parseSyllables(verse[2])
	
	#half_length = len(pada_ab)
	#quarter_length = half_length / 2
	
	pada_a = verse.getPada(Verse.A) 
	pada_b = verse.getPada(Verse.B) 
	pada_c = verse.getPada(Verse.C) 
	pada_d = verse.getPada(Verse.D) 
	
	if pada_a[0] == pada_a[-1]\
		and  pada_a[-1] == pada_b[0]\
		and pada_b[0] == pada_b[-1]\
		and pada_b[-1] == pada_c[0]\
		and pada_c[0] == pada_c[-1]\
		and pada_c[-1] == pada_d[0]\
		and pada_d[0] == pada_d[-1]:
		return True
	
	return False