#!/usr/bin/python
# -*- coding: utf8 -*-

# implements a test for the 'sarvatobhadra' figure

from VerseTools import Verse

"""
This figure is essentially a double palindrome, consisting of a verse that can be read forward, backward, and vertically.

e.g., Kirātārjunīya 15.25:
devākānini kāvāde 
vāhikāsvasvakāhi vā /
kākārebhabhare kākā 
nisvabhavyavyabhasvani // BhKir_15.25 //

The test: Each line must be a palindrome
"""


def isPalindrome(line):
	palindrome = True
	i = 0
	j = len(line) - 1
	
	while i < j:
		print line[i], '...', line[j]
		if line[i] != line[j]:
			palindrome = False
			break
		
		i += 1
		j -= 1
	
	return palindrome


# expects a Verse object
def isSarvatobhadra(verse):
	for line in verse:
		palindrome = isPalindrome(line)
		print palindrome
	
	return False
	