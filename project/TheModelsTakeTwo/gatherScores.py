"""
gatherScores.py gathers scores for the testing words.
The scores are then written to the modelScores folder.
"""

from trigramModel import *
from neighborhoodModel import *
from LinearRegression import vectorMaker
from LinearRegression import linearRegressionModel as LRM
from pathlib import Path
import os


def gatherScores(filename, mode):
    scoresAndWords = []

    with open(filename, 'r') as f:
        data = f.read()
    
    words = data.lower().split("\n")
    

    if mode == "T":
        for word in words:
            score = calculateTrigramProbability(word)
            scoresAndWords.append((word,score))

    elif mode == "N":
        for word in words:
            score = calculateNeighborhoodScore(word)
            scoresAndWords.append((word,score))
    
    elif mode == "L":
        for word in words:
            score = LRM.calculateLRScore(word)
            scoresAndWords.append((word,score))

    
    # scoresAndWords.sort(key = lambda x: x[1]) 

    return scoresAndWords



#writes out data to a text file
def writeData(words, filename):
    with open(filename, 'w') as f:
        for x, y in words:
            f.write(str(x) + "\t" + str(y) + "\n")



#path stuff
current = os.getcwd()
wordsFolder = Path(current + "/words")
scoresFolder = Path(current + "/modelScores")

modes = ['L', 'N', 'T']

for mode in modes:

    if mode == "T":
        name = 'trigramScores.txt'

    elif mode == "N":
        name = 'neighborhoodScores.txt'
    
    elif mode == "L":
        name = 'linearRegressionScores.txt'
    
    writeData(gatherScores(wordsFolder / 'testingWords.txt', mode), scoresFolder / name)


   