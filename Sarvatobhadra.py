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
	i = 0
	j = len(line) - 1
	while i < j:
		if line[i] != line[j]:
			return False
		i += 1
		j -= 1
	
	return True


# expects a Verse object
def isSarvatobhadra(verse):
	matrix = []
	for line in verse:
		if not isPalindrome(line):
			# if any line is not a palindrome, the whole thing is False
			return False
		
		# no point in doing anything with the matrix until here
		matrix.append(line)
		
	# at this point the lines are all palindromes in their own right
	# and the matrix is half full
	# but needs to have the verse in reverse 
	# i.e., we want to end up with [[a], [b], [c], [d], [d], [c], [b], [a]]
	for line in reversed(matrix):
		matrix.append(line)
		
	# now we need to find the 'vertical' palindrome
	# go through the verse and compare to matrix
	i = 0
	j = 0
	while i < len(matrix):
		while j < len(matrix):
			print matrix[i][j], '...', matrix[j][i]
			if matrix[i][j] != matrix[j][i]:
				return False
			j += 1
		i += 1
		
	return True
	