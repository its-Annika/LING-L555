""" 
runner.py allows the user to get a score from one of the models (trigram, neighborhood) 
for an inputted word. 
"""


from trigramModel import *
from neighborhoodModel import *

print("T. Trigram Model \nN. Neighborhood Model")

#takes continous input from the user
choices = input("Please enter word,mode. Q to quit: ").split(',')
word = choices[0]
mode = choices[1]

while(word != 'Q'):

    if mode == "T":
        probability = calculateTrigramProbability(word.strip(" "))
        print("Trigram Probability: " + str(probability) + "\n")
    
    elif mode == "N":
        score = calculateNeighborhoodScore(word.strip(" "))
        print("Neighborhood Score: " + str(score))

        acceptability = judgeAcceptability(score)
        print("Acceptability: " + str(acceptability) + "\n")
    
    choices = input().split(',')
    word = choices[0]
    mode = choices[1]

    

   