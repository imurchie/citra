#!/usr/bin/python
# -*- coding: utf8 -*-

# implements a test for 'niyama' (i.e., lipogrammatic) verses

import re

from VerseTools import Verse
from SyllableTools import isVowel
from SyllableTools import isVisarga
from SyllableTools import isAnusvara


# since we only care about consonants for this figure, we need to get rid of vowels
def getConsonants(line):
  consonants = []
  for syllable in line:
    for i in xrange(len(syllable)):
      letter = syllable[i]

      # only unique non-vowels and non-visarga/anusvāra
      if (not isVowel(letter)) and (not isVisarga(letter)) and (not isAnusvara(letter)) and (not letter in consonants):
        consonants.append(letter)
  return consonants


# for now we will have a threshold of 4 consonants
def isNiyama(verse):
  unique_syllables = []

  for pada in verse:
    consonants = getConsonants(pada)
    if len(consonants) >= 4:
      return False



  return True
