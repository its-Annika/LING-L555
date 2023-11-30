from sklearn.linear_model import LinearRegression
from pathlib import Path
import os
from vectorMaker import makeVector

#path stuff
current = os.getcwd()
wordsFolder = Path(current + "/words")
linearFolder = Path(current + "/LinearRegression")


#convers the data into a format the model can use
x = []
y = []
words = []

with open(linearFolder / 'trainingVectors.txt', 'r') as f:
    uglyData = f.readlines()

for line in uglyData:

    lineFormated = line.split(",")
    word = lineFormated[0].strip()
    features = list(map(float, lineFormated[1].split(" ")))
    score = float(lineFormated[2].strip())
    
    x.append(features)
    y.append(score)
    words.append(word)


#makes the model
reg = LinearRegression().fit(x, y)

print("Coefficient of Determination of the Prediction: ", reg.score(x, y))



#calculates the score for any given word
def calculateLRScore(word):

    features = list(map(float, makeVector(word).split(" ")))

    return(reg.predict(list(([features]))))