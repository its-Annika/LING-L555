'''
This file makes vectors for the linear regression model.

It also creates the training data for the model. 

'''
import panphon
import sys
import os
from pathlib import Path
sys.path.insert(1, os.getcwd())
import tools.miscTools as miscTools
import panphon
import panphon.sonority
import panphon.segment
import numpy as np
son = panphon.sonority.Sonority()
ft = panphon.FeatureTable()


#takes a word and generates its feature vector
def makeVector(word):

    #gets the automatically generated IPA transcription
    print("word: " + word)
    ipaForm = miscTools.getIPAForm(word)
    print(ipaForm)

    #tries to divide the IPA transcription into onset, nucleus, and coda
    try:
        onset = miscTools.getOnset(ipaForm)
        nuclus = miscTools.getNucleus(ipaForm)
        coda = miscTools.getCoda(ipaForm)
        print(onset, nuclus, coda)
    #if something goes wrong, tell the user to enter a corrected IPA form
    except:
        print("An IPA form with a nucleus must be entered in order to continue.")

    #sometimes epitran tries to repair forms by adding vowels
    #to prevent the use of poor IPA transcriptions, 
    #the user is able to enter corrected IPA transcirptions
    acceptable = input()

    if len(acceptable) > 1:
        ipaForm = acceptable
        onset = miscTools.getOnset(ipaForm)
        nuclus = miscTools.getNucleus(ipaForm)
        coda = miscTools.getCoda(ipaForm)

        print(onset, nuclus, coda, "\n")

    #if the word is shorter than 9 phones, a place holder row is used
    placeHolder = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]

    #pads the form
    #for example, if the onset is 'k'
    # the onset portion of the vector is placeHolder, placeHolder, k
    onsetPadded = '@'*(3- len(onset)) + onset
    nuclusPadded = nuclus + "@"*(2-len(nuclus))
    codaPadded = coda + '@'*(4- len(coda))

    paddedWord = onsetPadded + nuclusPadded + codaPadded

    tempVector = []

    #fill in the vector rows
    for character in paddedWord:
        if character == '@':
            tempVector.append(placeHolder)
        else:
            features = ft.word_array(['syl', 'son', 'cons', 'cont', 'delrel', 'lat', 'nas', 'strid', 'voi', 'sg', 'cg', 'ant', 'cor', 'distr', 'lab', 'hi', 'lo', 'back', 'round', 'velaric', 'tense', 'long'], character)
            tempVector.append(features.flatten().tolist())

    return np.array(tempVector)



#path stuff
current = os.getcwd()
wordsFolder = Path(current + "/words")
linearFolder = Path(current + "/LinearRegression")


#processes training data
def train():

    finalData = []
    
    #read in the training words
    with open(wordsFolder / "minitrainingWords.txt", 'r') as f:
        data = f.readlines()
    
    for line in data:
        word = line.split("\t")[0]
        score = line.split("\t")[1].strip("\n")

        #try to make a vector
        try:
            vector = " ".join(str(x) for x in (makeVector(word).flatten().tolist()))
        
        #saves your work if the program crashes
        #panphon gives up sometimes
        except:
            with open(linearFolder / 'minitrainingVectors.txt', 'w') as f2:
                for tripple in finalData:
                    f2.write(str(tripple[0]) + "," + tripple[1] + "," + str(tripple[2]) + "\n") 
            quit()


        allThree = [word, vector, score]
        finalData.append(allThree)
    
    #writes the word, vector, score for each training word
    with open(linearFolder / 'minitrainingVectors.txt', 'w') as f2:
        
        for tripple in finalData:
            f2.write(str(tripple[0]) + "," + tripple[1] + "," + str(tripple[2]) + "\n") 

#makes the training data
train()
#comment out after training is complete
