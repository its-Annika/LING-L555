"""
gatherScores.py gathers scores from all models for inputed words. 

See the end of the file for the function call. 
"""

from trigramModel import *
from neighborhoodModel import *
from LinearRegression.linearRegressionModel import calculateLRScore
from pathlib import Path
import os


def gatherScores(filename, mode):

    scoresAndWords = []

    #reads in all the words in the provided file
    with open(filename, 'r') as f:
        data = f.read()
    
    words = data.lower().split("\n")
    
    #calls the model specific calculate function depending on which mode
    # gatherScores() recieved as an argument
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
            try:
                score = calculateLRScore(word)
                scoresAndWords.append((word,score))

            #sometimes panphone gives up
            #the except block saves your work if the program ends up crashing
            except:
                print('There was an error processing the following word: ' + word)
                print("All previous vectors have been saved.")
                return scoresAndWords

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


#if you'd like to change which file that is read from/written to, do so here. 
# to change the file that each model writes to, change the 'name' variable.
modes = ['L', 'N', 'T']

for mode in modes:

    if mode == "T":
        name = 'trigramScoresMini.txt'

    elif mode == "N":
        name = 'neighborhoodScoresMini.txt'
    
    elif mode == "L":
        name = 'linearRegressionScoresMini.txt'

    # to change the read from file, replace 'testingWords.txt' with the desired file name.
    writeData(gatherScores(wordsFolder / 'minitestingWords.txt', mode), scoresFolder / name)


   