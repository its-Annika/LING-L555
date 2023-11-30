from tools.miscTools import *
import os
from pathlib import Path


#path stuff
current = os.getcwd()
corpusFolder = Path(current + "/corpera")


with open(corpusFolder / 'oxfordWords.txt', 'r') as f:
    words = f.readlines()


with open( corpusFolder / 'monosyllabicBrownTypes.txt', 'r') as f:
    brownWords = f.readlines()


finalWords = []

print('reading done')

for word in words:
    if monosyllabic(getIPAForm(word).strip('\n')) and word.lower() not in brownWords and word.lower() not in finalWords:
        print(word)
        finalWords.append(word.lower())


with open(corpusFolder / 'monosyllabicOxfordWords.txt', 'w') as f:
    for word in finalWords:
        f.write(word)


