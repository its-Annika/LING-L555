import panphon
import sys
import os
from pathlib import Path
sys.path.insert(1, os.getcwd())
import tools.miscTools as miscTools
import panphon
import panphon.sonority
import panphon.segment

son = panphon.sonority.Sonority()
ft = panphon.FeatureTable()


def makeVector(word):

    vector = []

    print("word: " + word)
    ipaForm = miscTools.getIPAForm(word)
    print(ipaForm)

    #sometimes epitran tries to repair forms by adding vowels
    #I don't want that repair
    acceptable = input()

    if acceptable == "no":
        ipaForm = input()


    onset = miscTools.getOnset(ipaForm)
    nuclus = miscTools.getNucleus(ipaForm)
    coda = miscTools.getCoda(ipaForm)

    print(onset, nuclus, coda)

    #no onset
    vector.append(noSegment(onset))
        
    #oneplace onset
    vector.append(onePlaceSegment(onset))

    #two place onset
    vector.append(twoPlaceSegment(onset))

    #three place onset
    vector.append(threePlaceSegment(onset))

    #four+ place onset
    vector.append(fourPlusPlaceSegment(onset))

    #no coda
    vector.append(noSegment(coda))

    #one place coda
    vector.append(onePlaceSegment(coda))

    #two place coda
    vector.append(twoPlaceSegment(coda))

    #three place coda
    vector.append(threePlaceSegment(coda))
    
    #four+ place coda
    vector.append(fourPlusPlaceSegment(coda))

    #sonority violation onset
    vector.append(sonorityViolationOnset(onset))

    #sonority violation coda
    vector.append(sonorityViolationCoda(coda))

    #duplicate manner of articulation onset
    vector.append(duplicateMOA(onset))

    #duplicate manner of articulation coda
    vector.append(duplicateMOA(coda))
    
    #voicing missmatch onset
    vector.append(voicingMismatch(onset))

    #vocing missmatch coda
    vector.append(voicingMismatch(coda))

    #tense vowel 
    #tense vowels can apperar in open syllables
    vector.append(findTenseness(nuclus))

    #dipthong
    vector.append(isDipthong(nuclus))

    #s as inital consonant
    #
    vector.append(findSOnset(onset))

    #l, m, n in onset, but not inital
    #if theres a sonorant, it's probably behind an [s]
    vector.append(secondSonorant(onset))

    #r in onset, but not inital
    vector.append(secondR(onset))

    #ng in onset
    vector.append(findOnsetEngma(onset))

    #h coda
    vector.append(findCodaH(coda))

    finalVector = ""
    
    for i in range(len(vector)):
        if i == len(vector) -1:
            finalVector += str(vector[i])
        else:
            finalVector += str(vector[i]) + " "

    return finalVector


#the many many constraints
def noSegment(segment):

    if len(segment) == 0:
        return '1'
    else:
        return '0'
    
def onePlaceSegment(segment):

    if len(segment) == 1:
        return '1'
    else:
        return '0'

def twoPlaceSegment(segment):

    if len(segment) == 2:
        return '1'
    else:
        return '0'

def threePlaceSegment(segment):

    if len(segment) == 3:
        return '1'
    else:
        return '0'

def fourPlusPlaceSegment(segment):

    if len(segment) >= 4:
        return '1'
    else:
        return '0'

def sonorityViolationOnset(onset):

    if len(onset) <= 1:
        return '0'
    
    if ft.word_fts(onset[0])[0].match({'son': -1, 'cont': 1}):
        onset = onset[1:]

    for i in range(len(onset) - 1):
        if son.sonority(onset[i]) >= son.sonority(onset[i+1]) + 1:
            return '1'
    
    return '0'

def sonorityViolationCoda(coda):

    if len(coda) <= 1:
        return '0'

    for i in range(len(coda) - 1):
        if son.sonority(coda[i]) + 1 <= son.sonority(coda[i+1]) and not ft.word_fts(coda[i])[0].match({'delrel': 1}) and not ft.word_fts(coda[i+1])[0].match({'son': -1, 'cont': 1}):
            return '1'
    
    return '0'

def duplicateMOA(segment):

    if len(segment) <= 1:
        return '0'

    for i in range(len(segment) -1):
        if (ft.word_array(['syl', 'cons', 'son', 'cont', 'delrel'], segment[i]) == ft.word_array(['syl', 'cons', 'son', 'cont', 'delrel'], segment[i+1])).all():
            return '1'
    
    return '0'

def findOnsetEngma(onset):

    if 'ŋ' in onset:
        return '1'
    else:
        return '0' 
    
def findTenseness(nucleus):

    if len(nucleus) == 1 and ft.word_fts(nucleus)[0].match({'tense': 1}):
        return '1'
    else:
        return '0'
    
def isDipthong(nucleus):
    
    if len(nucleus) > 1:
        return '1'
    else:
        return '0'

def findCodaH(coda):
    
    if 'h' in coda:
        return '1'
    else:
        return '0'

def findSOnset(onset):

    if onset != "":
        if onset[0] == 's':
            return '1'
        
    return '0'

def voicingMismatch(segment):

    if len(segment) <= 1:
        return '0'

    voicingRecord = []

    for i in range(len(segment)):

        if segment[i] in ['b', 'p', 'f', 'v', 't', 'd', 's', 'z', 'k', 'g', 'ʃ', 'θ', 'ð', 'ʒ', 'x']:
            if ft.word_fts(segment[i])[0].match({'voi': -1}):
                voicingRecord.append(0)
            else:
                voicingRecord.append(1)
                
    
    voice = voicingRecord[0]

    for score in voicingRecord[1:]:
        if score != voice:
            return '1'
    
    return '0'

def secondSonorant(onset):

    if len(onset) <= 1:
        return '0'

    if onset[1] in ['m', 'n', 'l', 'w']:
        return '1'

    return '0'

def secondR(onset):

    if len(onset) <= 1:
        return '0'

    if onset[1] == 'ɹ':
        return '1'

    return '0'


#path stuff
current = os.getcwd()
wordsFolder = Path(current + "/words")
linearFolder = Path(current + "/LinearRegression")


#training
def train():

    finalData = []

    with open(wordsFolder / "trainingWords.txt", 'r') as f:
        data = f.readlines()
    
    for line in data:
        word = line.split(",")[0]
        score = line.split(",")[1].strip("\n")
        vector = makeVector(word)

        allThree = [word, vector, score]
        finalData.append(allThree)
    
    with open(linearFolder / 'trainingVectors.txt', 'w') as f2:
        
        for tripple in finalData:
            f2.write(str(tripple[0]) + "," + tripple[1] + "," + str(tripple[2]) + "\n") 



#makes the training data
# train()

    
    

























# vectors = []

#temp runner
# inputWord = input()

# while inputWord != "Q":

#     x = makeVector(inputWord)

#     vectors.append(x)

#     inputWord = input()


# current = os.getcwd()
# scoresFolder = Path(current + "/LinearRegressionModel")

# with open(scoresFolder /'vectorsAndScores.txt', 'w') as f:
#     for vector in vectors:
#         f.write(" ".join(vector) + "\n")



