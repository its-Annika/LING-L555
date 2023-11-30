"""
trigramModel.py gathers unicounts and tricounts from the brown corpus,
and stores them in dictionaries. Add-One smoothing is implemented. 

calculateTrigramProbability calculates the probability of a given word.

trigramAcceptibility determines the acceptabibility of a given word. 
"""



import os
from pathlib import Path
import re
import math
from collections import defaultdict


#path stuff
current = os.getcwd()
corpusFolder = Path(current + "/corpera")



#formats the brown corpus into a list of individual characters
def setupBrown(filename):

    brownCharacterSequence = []

    #opens the file
    #in this case the brown corpus without any puctuation or numbers
    with open(filename, 'r') as f:
        data = f.readlines()
        #removes duplicate newline characters, strips the line, splits by spaces
        for line in data:
            line = re.sub(r'\n+', '\n', line).strip("\n").split(" ")
            #marks the begining of a word with '##' and the end with '@'
            for word in line:
                if word != "":
                    brownCharacterSequence += "##" + word.lower() + "@@"

    return brownCharacterSequence 



#gets tricounts from the Brown Character Sequence
#add one smoothing
def findTricounts(brownCharacterSequence):

    tricounts = defaultdict(lambda:0)
    allPossibleTricounts = []

    #generates all possible combinations
    letters = ["a","b","c","d","e","f","g","h", "i", "j", "k", "l", "m","n","o", "p",
                "q", "r","s","t","u","v","w","x","y","z", "#", "@"]
    for a in letters:
        for b in letters:
            for c in letters:
                allPossibleTricounts.append(str(a + b + c))  

    #throws out all illegal combinations and duplicates
    for tricount in allPossibleTricounts:
        if not re.search(r'(@@[a-z])|(@[a-z]+)|([a-z]##)|([a-z]+#)|([a-z]#[a-z])|([a-z]@[a-z])|(#@[a-z])|(@#[a-z])|([a-z]#@)|([a-z]@#)|([^a-z][^a-z][^a-z])', tricount) and tricount not in tricounts: 
            #updates the dictionary
            #add one smoothing
            tricounts[tricount] += 1
  
    #takes trigrams from the brown sequence
    for i in range(len(brownCharacterSequence) + 2):
        bit = "".join(brownCharacterSequence [i: i + 3])
        tricounts[bit] += 1

    return tricounts



#gets tricounts from the Brown Character Sequence
#add one smoothing
def findBicounts(brownCharacterSequence):

    bicounts = defaultdict(lambda:0)
    allPossibleBicounts = []

    #generates all possible combinations
    letters = ["a","b","c","d","e","f","g","h", "i", "j", "k", "l", "m","n","o", "p", "q", "r","s","t","u","v","w","x","y","z", "#", "@"]
    for a in letters:
        for b in letters:
            allPossibleBicounts.append(str(a + b))  

    #throws out all illegal combinations and duplicates
    for bicount in allPossibleBicounts:
        if not re.search(r'(@[a-z])|(@[a-z])|([a-z]#)|([a-z]#)|([a-z]#)|(@[a-z])|(#@)|(@#)', bicount) and bicount not in bicounts: 
            #updates the dictionary
            #add one smoothing
            bicounts[bicount] += 1
  
    #takes trigrams from the brown sequence
    for i in range(len(brownCharacterSequence) + 1):
        bit = "".join(brownCharacterSequence [i: i + 2])
        bicounts[bit] += 1

    return bicounts



#gets unitgram counts from the Brown Character Sequence
#add one smoothing
def findUnicounts(brownCharacterSequence ):
    unicounts = defaultdict(lambda:0)

    #add one smoothing
    letters = ["a","b","c","d","e","f","g","h", "i", "j", "k", "l", "m","n","o", "p", "q", "r","s","t","u","v","w","x","y","z", "#", "@"]
    for a in letters:
        unicounts[str(a)] += 1

    #takes unicounts from the brown sequence
    for i in range(len(brownCharacterSequence )):
        bit = "".join(brownCharacterSequence [i: i + 1])
        unicounts[bit] += 1

    return unicounts



#formats brown corpus
brownCharacterSequence = setupBrown(corpusFolder / "brownCorpusClean.txt")

#generates the counts
# unicounts = findUnicounts(brownCharacterSequence)
bicounts = findBicounts(brownCharacterSequence)
tricounts = findTricounts(brownCharacterSequence)



#gets probabilities
def calculateTrigramProbability(word):

    #format the word
    formated = "##" + word.lower() + "@@"

    #collects the probabilities
    probability = 1

    for i in range(len(formated) - 2):

        numerator = tricounts[str(formated[i:i+3])]
        denominator = bicounts[str(formated[i:i+2])]

        probability += math.log(numerator/denominator)
    
    #normalize for length
    finalProbability = probability/len(formated)

    return finalProbability



#gets the acceptability judgment
def trigramAcceptability(score):

    pass