'''
This file contains the linear regression model. 

calculateLRScore() calculates the score for a given word
based on the created model. 
'''

from sklearn.linear_model import LinearRegression
from pathlib import Path
import os
from .vectorMaker import *
import numpy as np

#path stuff
current = os.getcwd()
wordsFolder = Path(current + "/words")
linearFolder = Path(current + "/LinearRegression")


#convers the data into a format the model can use
x = []
y = []
words = []

#reads in the training vectors
with open(linearFolder / 'minitrainingVectors.txt', 'r') as f:
    uglyData = f.readlines()

for line in uglyData:

    lineFormated = line.split(",")
    word = lineFormated[0].strip()
    features = lineFormated[1].strip()

    #turns the string of numbers back into an array
    tempVector = np.fromstring(features, dtype=int, sep=' ')
   
    score = float(lineFormated[2].strip())
    
    x.append(np.array(tempVector))
    y.append(score)
    words.append(word)


#makes the model
reg = LinearRegression().fit(x, y)

print("Linear Regression Model Coefficient of Determination of the Prediction: ", reg.score(x, y))


#calculates the score for any given word
def calculateLRScore(word):

    features = makeVector(word).flatten()

    return(reg.predict(list(([features]))))