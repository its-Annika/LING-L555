"""
writeOxfordDict.py reads in from the oxfordWords.txt file, which contains
all the words in the Oxford English Dictionary, and keeps only monosyllabic words 
that aren't in the brown corpus. These words are written to the 
monosyllabicOxfordWords.txt file. 
"""

from miscTools import *
import os
from pathlib import Path


#path stuff
current = os.getcwd()
corpusFolder = Path(current + "/corpera")


#read the oxford dictionary
with open(corpusFolder / 'oxfordWords.txt', 'r') as f:
    words = f.readlines()

#read the brown corpus
with open( corpusFolder / 'monosyllabicBrownTypes.txt', 'r') as f:
    brownWords = f.readlines()


finalWords = []

print('reading done')

#for each word in the oxford dictionry 
for word in words:
    #if its monosyllabic and not in the brown dictonary
    if monosyllabic(getIPAForm(word).strip('\n')) and word.lower() not in brownWords and word.lower() not in finalWords:
        #grab it
        finalWords.append(word.lower())

#write the unique oxford dictionary monosyllabic words
with open(corpusFolder / 'monosyllabicOxfordWords.txt', 'w') as f:
    for word in finalWords:
        f.write(word)


