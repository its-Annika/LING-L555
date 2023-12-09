"""
brownProcesser finds the monosyllabic types(unique words) in the brown corpus.

It then outputs all the types to the monosyllabicBrownTypes.txt.

writeBrownTop reads in from the monosyllabicBrownTypes.txt and prints the top 2000 words.
"""
from collections import defaultdict
from pathlib import Path
import os
import enchant
import re
from miscTools import getIPAForm, monosyllabic

#set up 
dict = enchant.Dict("en_US")

#gets unique types from the brown corpus
def gatherTypes():

    with open(corpusFolder / "BrownCorpusClean.txt", 'r') as f:
        lines = f.readlines()
    
    temp = []
    for line in lines:
        temp += line.lower().split(" ")

    #frequency dictionary
    monosyllables = defaultdict(lambda:0)

    counter = 0

    for word in temp:
        
        word = word.strip("\n")

        #the enchant dictionary accepts single letters as word
        #the only valid single letter words are 'a' and 'i'
        if (len(word) == 1 and not re.search(r'[ai]', word)):
            continue

        #make sure the word is a valid word of English
        if len(word) != 0 and dict.check(word):

            #get the IPA form
            ipaForm = getIPAForm(word)

            #make sure it's monosyllabic
            if monosyllabic(ipaForm):
                monosyllables[word] += 1

        counter += 1

        #lets the user know how many words have been processed
        if counter % 5000 == 0:
            print("Processed words: " + str(counter))

    #sorts the word by frequency
    return sorted(monosyllables.items(), key=lambda x: x[1], reverse=True)



#writes unique types from the brown corpus
def writeBrownUnique(words):
    with open(corpusFolder / "monosyllabicBrownTypes.txt", 'w') as f:
        for word in words:
            f.write(word[0] +"\n")



#write top 10,000 unique types from the brown corpus
def writeBrownTop(numOfWords):

    with open(corpusFolder / "monosyllabicBrownTypes.txt", 'r') as f:
        lines = f.readlines()
    
    if numOfWords > len(lines):
        print("The chosen number is too large. Please choose a number less than " + str(len(lines)) + ".\n")
        numOfWords = int(input())

    with open(corpusFolder / "topBrownTypes.txt", 'w') as f:
        count = 0
        for word in lines:
            f.write(word)
            count += 1
            if count >= numOfWords:
                break



#path stuff
current = os.getcwd()  
corpusFolder = Path(current + "/corpera/")


#do things
brownWords = gatherTypes()
writeBrownUnique(brownWords)
writeBrownTop(2000)