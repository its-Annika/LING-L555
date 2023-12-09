"""
This file outputs a .txt file of words from three different categories:
valid/English words, nonce words, and invalid words.

The amount of generated words of each category can be changed by giving 
different numbers to the makeData function. The function call can be found 
at the end of the file. 

the functions which generate English, nonce, and random words all 
check each generated word with the user. This was implemented to manually 
filter out inappropriate language or multisyllabic words which weren't 
succsesfully filtered out. 
"""
import random 
from pathlib import Path
import os
import enchant
from tools.miscTools import getIPAForm, monosyllabic

#pathing stuff
current = os.getcwd()
corpusFolder = Path(current + "/corpera/")
invalidFolder = Path(current + "/invalidBits/")
wordsFolder = Path(current + "/words/")

# German, English, French, and name dictionaries
germanDict = enchant.Dict('de_DE')
ENdict = enchant.Dict('en')
frenchDict = enchant.Dict("fr")

# https://www.cs.cmu.edu/Groups/AI/areas/nlp/corpora/names/female.txt
# https://www.cs.cmu.edu/Groups/AI/areas/nlp/corpora/names/male.txt

firstNames = Path(corpusFolder / "first-names.txt")
nameDict = enchant.request_pwl_dict(firstNames.as_posix())



#pulls random words from the inputed file
def pullFromFile(filename, num):

    gatheredWords = []
    numberTracker = []

    with open(filename, 'r') as f:
        data = f.readlines()

    #for however many words are wanted
    for i in range(num):

        #generate a random number within that range
        randomStuff = pullHelper(numberTracker, len(data) - 1)

        #store the random number and get the coresponding word
        word = data[randomStuff[0]]
        numberTracker = randomStuff[1]

        #give the user facts about the word
        print(word.strip("\n"))
        print("This word is...")
        print("German: " + str(germanDict.check(word.strip("\n"))) + ", " + str(germanDict.check(word.strip("\n")[0].upper() + word.strip("\n")[1:])))
        print('French: ' +  str(frenchDict.check(word.strip("\n"))) + ", " + str(frenchDict.check(word.strip("\n")[0].upper() + word.strip("\n")[1:])))
        print('a name: ' + str(nameDict.check(word.strip("\n")[0].upper() + word.strip("\n")[1:])))
        choice = input()

        #if they didn't press enter, they rejected the pulled form, so
        while len(choice) > 0:

            #get a new random number
            randomStuff = pullHelper(numberTracker, len(data) - 1)

            #store the random number, and get the coresponding words
            word = data[randomStuff[0]]
            numberTracker = randomStuff[1]

            #show the user facts about the word
            print(word.strip("\n"))
            print("This word is...")
            print("German: " + str(germanDict.check(word.strip("\n"))) + ", " + str(germanDict.check(word.strip("\n")[0].upper() + word.strip("\n")[1:])))
            print('French: ' +  str(frenchDict.check(word.strip("\n"))) + ", " + str(frenchDict.check(word.strip("\n")[0].upper() + word.strip("\n")[1:])))
            print('a name: ' + str(nameDict.check(word.strip("\n")[0].upper() + word.strip("\n")[1:])))
            choice = input()
        
        #rinse and repeat until the word is accepted
        gatheredWords.append(word.strip("\n"))
    
    return gatheredWords



def pullHelper(numberTracker, max):

    randomNumber = random.randint(1,max)

    #makes sure each random number
    #hasn't been pulled before
    while randomNumber in numberTracker:
        randomNumber = random.randint(1,max)
    
    numberTracker.append(randomNumber)

    return randomNumber, numberTracker



#generates random EnglishWords by combining English onsets, nucelus, and coda
#I did not end up using this function
def randomEnglishWords(num, seenWords):

    createdEnglishWords = []

    for i in range(num):

        randomEnglishWord = nonceHelper(createdEnglishWords)

        #if the word is not an actual English word, or is more than one syllable, is in the brown corpus, throw it out
        while not ENdict.check(randomEnglishWord) or not ENdict.check(randomEnglishWord[0].upper() + randomEnglishWord[1:] or randomEnglishWord in seenWords or not monosyllabic(getIPAForm(randomEnglishWord))):
            
            randomEnglishWord = nonceHelper(createdEnglishWords)
        
        createdEnglishWords.append(randomEnglishWord)

    return createdEnglishWords



#generates random Nonce words
def nonceWordMaker(num):

    createdNonceWords = []

    #for the number of requested words
    for i in range(num):

        #make a nonce word
        randomNonceWord = nonceHelper(createdNonceWords)

        #show it to the user
        print(randomNonceWord)
        choice = input()

        #if the word is an actual English word, throw it out
        #if the user regects the word...
        while (ENdict.check(randomNonceWord) or ENdict.check(randomNonceWord[0].upper() + randomNonceWord[1:]) or len(choice) > 0):
            
            #make a new one
            randomNonceWord = nonceHelper(createdNonceWords)
            print(randomNonceWord)
            choice = input()

        #rinse and repeat until the nonce word is accepted
        createdNonceWords.append(randomNonceWord)

    return createdNonceWords



#combines a valid onset, nucleus, and coda to make a nonce word
def nonceHelper(createdWords):

    #options for valid English syllable constituents
    onsets = ['', 'p', 'b', 't', 'd', 'k', 'c', 'g', 'f', 'ph', 'v', 'th', 's', 'sc', 'z', 'sh', 'h'
            'ch', 'j', 'm', 'n', 'ny', 'kn', 'gn', 'l', 'ly', 'r', 'rh', 'wr', 'w', 'wh', 'h'
            'pl', 'pr', 'bl', 'br', 'tr', 'tw', 'dr', 'dw', 'cl', 'cr', 'kr', 'qu',
            'cu', 'gl', 'gr', 'gw', 'fl', 'fr', 'thr', 'sp', 'st', 'sk', 'sc',
            'sch', 'squ', 'sph', 'sm', 'sn', 'sl', 'sw', 'schl', 'shr', 'spr', 'str', 'scr',
            'skr', 'spl', 'scl', 'skl', 'squ']
   
    nucleus = ['a', 'e', 'i', 'o', 'u', 'ai', 'au', 'ee', 'oo', 'ou', 'ea', 'eau', 'ae']

    coda = ['', 'p', 'pe', 'b', 'be', 't', 'te', 'ed', 'k', 'ck', 'ke', 'g', 'f', 'ff', 'gh'
            'fe', 've', 'th', 's', 'ss', 'se', 'z', 'sh', 'ge', 'ch', 'tch', 'dge', 'm', 'mb',
            'mm', 'gm', 'n', 'gn', 'l', 'el', 'r', 'ng', 'w', 'pt', 'pth', 'pse', 'bed', 'bbed'
            'bes', 'bs', 'tz', 'dth', 'dz', 'ds', 'ct', 'x', 'gged', 'gs', 'ft', 'fth', 
            'ghs', 'ffs', 'ved', 'ves', 'thed', 'thes', 'ths', 'sp', 'st', 'ssed', 'sk', 'sque',
            'sed', 'zed', 'shed', 'dged', 'ged', 'tched', 'mp', 'mt', 'med', 'mph', 'nth', 'nthe',
            'ms', 'nt', 'nd', 'nce', 'ns', 'nze', 'nge', 'nch', 'lp', 'lb', 'lt', 'ld', 'lf', 'lve', 
            'lth', 'lse', 'lls', 'ls', 'lsh', 'lch', 'lge', 'lm', 'ln', 'rp', 'rb', 'rt', 'rd',
            'rk', 'rque', 'rgue', 'rl', 'rph', 'rve', 'rth', 'rce', 'rs', 'res', 'rsh', 'rge',
            'rch', 'rm', 'rn', 'rl', 'mpt', 'mpse', 'mps', 'ntz', 'nts', 'nx', 'nct', 'ngst', 'ntz',
            'nts', 'nched', 'mpsed', 'mphed', 'mphs', 'nths', 'nst', 'nced', 'nds', 'nged', 'nzed', 
            'sped', 'sps', 'sts', 'stes', 'sked', 'sls', 'ques', 'ltz', 'lts', 'lped', 'lps', 'lked',
            'lks', 'lched', 'lbs', 'lds', 'lged', 'lft', 'lfed', 'lfth', 'lfs', 'lsed', 'lved', 'lves',
            'lmed', 'lms', 'lns', 'ltzed', 'rpse', 'ps', 'rtz', 'rts', 'rped', 'rked', 'rks', 'tched', 'rbed',
            'rbs', 'rds', 'rgues', 'rged', 'rfed', 'rfs', 'rths', 'rsed', 'rced', 'rved', 'rves', 'rled',
            'rls', 'rmed', 'rms', 'mth', 'rned', 'rns', 'xt', 'xed', 'pts', 'lpts', 'cts', 'fts', 'psed',
            'dst', 'xts']
    
    #chooses a random onset, nucleus, and coda
    onsetChoice = random.randint(0, len(onsets) -1)
    nucleusChoice = random.randint(0, len(nucleus) -1)
    codaChoice = random.randint(0, len(coda) -1)
    
    randomWord = str(onsets[onsetChoice] + nucleus[nucleusChoice] + coda[codaChoice])

    #if the word is a german word, a french word, a proper name, or longer than one syllable...
    while (germanDict.check(randomWord) or germanDict.check(randomWord[0].upper() + randomWord[1:])
           or frenchDict.check(randomWord) or frenchDict.check(randomWord[0].upper() + randomWord[1:]) 
           or nameDict.check(randomWord[0].upper() + randomWord[1:])
           or randomWord in createdWords or not monosyllabic(getIPAForm(randomWord))):
            
            #get a new word
            randomWord = nonceHelper(createdWords)

    #rinse and repeat until a valid nonce word is created
    return randomWord



#generates invalid English words
def invalidWordMaker(num):

    gatheredWords = []

    #for the number of requested words
    for i in range(num):

        #calls the helper function, makes an invalid word
        #and shows it to the user
        invalidWord = invalidHelper()
        print(invalidWord)
        choice = input()

        #if they reject the form, make a new one
        while len(choice) > 0:
            invalidWord = invalidHelper()
            print(invalidWord)
            choice = input()

        #rinse and repeat until a form is accepted
        gatheredWords.append(invalidWord)
        
    return gatheredWords



#given a length, generates a random string of characters
def invalidHelper():

    #reads in the invalid onsets and codas, as they are too large to store in a list
    with open(invalidFolder / "invalidOnsets.txt", 'r') as f:
        invalidOnsets = f.read().splitlines() 

    invalidNucleai = ['aa', 'ao', 'ay', 'ei', 'eo', 'eu', 'ia', 'ie', 'ii', 'io', 'iu', 'iy', 'oa', 'oe', 'oi',
                       'oy', 'ua', 'ue', 'ui', 'uo', 'uu', 'uy', 'ya', 'ye', 'yi', 'yo', 'yu', 'yy']
    
    with open(invalidFolder / "invalidCodas.txt", 'r') as f:
        invalidCodas = f.read().splitlines() 
    
    #Here are the valid options
    validOnsets = ['', 'p', 'b', 't', 'd', 'k', 'c', 'g', 'f', 'ph', 'v', 'th', 's', 'sc', 'z', 'sh', 'h'
            'ch', 'j', 'm', 'n', 'ny', 'kn', 'gn', 'l', 'ly', 'r', 'rh', 'wr', 'w', 'wh', 'h'
            'pl', 'pr', 'bl', 'br', 'bw', 'tr', 'tw', 'dr', 'dw', 'cl', 'chl', 'cr', 'kr', 'qu',
            'cu', 'gl', 'gr', 'gw', 'fl', 'phl', 'fr', 'vl', 'thr', 'thw', 'sp', 'st', 'sk', 'sc',
            'sch', 'squ', 'sph', 'sth', 'sm', 'sn', 'sl', 'sw', 'schl', 'shr', 'spr', 'str', 'scr',
            'skr', 'spl', 'scl', 'skl', 'squ', 'sphr']
   
    validNucleus = ['a', 'e', 'i', 'o', 'u', 'y', 'ai', 'au', 'ee', 'oo', 'ou', 'ea', 'ey', 'eau', 'ae']

    validCodas = ['', 'p', 'pe', 'b', 'be', 't', 'te', 'ed', 'k', 'ck', 'ke', 'g', 'f', 'ff', 'gh'
            'fe', 've', 'th', 's', 'ss', 'se', 'z', 'sh', 'ge', 'ch', 'tch', 'dge', 'm', 'mb',
            'mm', 'gm', 'n', 'gn', 'l', 'el', 'r', 'ng', 'w', 'pt', 'pth', 'pse', 'bed', 'bbed'
            'bes', 'bs', 'ghth', 'tz', 'dth', 'dz', 'ds', 'ct', 'x', 'gged', 'gs', 'ft', 'fth', 
            'ghs', 'ffs', 'ved', 'ves', 'thed', 'thes', 'ths', 'sp', 'st', 'ssed', 'sk', 'sque',
            'sed', 'zed', 'shed', 'dged', 'ged', 'tched', 'mp', 'mt', 'med', 'mph', 'nth', 'nthe',
            'ms', 'nt', 'nd', 'nce', 'ns', 'nze', 'nge', 'nch', 'lp', 'lb', 'lt', 'ld', 'lf', 'lve', 
            'lth', 'lse', 'lls', 'ls', 'lsh', 'lch', 'lge', 'lm', 'ln', 'rp', 'rb', 'rt', 'rd',
            'rk', 'rque', 'rgue', 'rl', 'rph', 'rve', 'rth', 'rce', 'rse', 'rs', 'res', 'rsh', 'rge',
            'rch', 'rm', 'rn', 'rl', 'mpt', 'mpse', 'mps', 'ntz', 'nts', 'nx', 'nct', 'ngst', 'ntz',
            'nts', 'nched', 'mpsed', 'mphed', 'mphs', 'nths', 'nst', 'nced', 'nds', 'nged', 'nzed', 
            'sped', 'sps', 'sts', 'stes', 'sked', 'sls', 'ques', 'ltz', 'lts', 'lped', 'lps', 'lked',
            'lks', 'lched', 'lbs', 'lds', 'lged', 'lft', 'lfed', 'lfth', 'lfs', 'lsed', 'lved', 'lves',
            'lmed', 'lms', 'lns', 'ltzed', 'rpse', 'ps', 'rtz', 'rts', 'rped', 'rked', 'rks', 'tched', 'rbed',
            'rbs', 'rds', 'rgues', 'rged', 'rfed', 'rfs', 'rths', 'rsed', 'rced', 'rved', 'rves', 'rled',
            'rls', 'rmed', 'rms', 'mth', 'rned', 'rns', 'xt', 'xed', 'pts', 'lpts', 'cts', 'fts', 'psed',
            'dst', 'xts']
    
    #generate a random number to choose which part of the word is invalid
    invalidChooser = random.randint(0, 2)

    #if the number is 0, the onset will be invalid, but the nucleus and coda will be valid
    if invalidChooser == 0:
        onset = invalidOnsets[random.randint(0, len(invalidOnsets) -1)]
        nucleus = validNucleus[random.randint(0, len(validNucleus) -1)]
        coda = validCodas[random.randint(0, len(validCodas) -1)]

    #if the number is 1, the nuvelus will be invalid, but the onset and coda will be valid
    elif invalidChooser == 1:
        nucleus = invalidNucleai[random.randint(0, len(invalidNucleai) -1)]
        onset = validOnsets[random.randint(0, len(validOnsets) -1)]
        coda = validCodas[random.randint(0, len(validCodas) -1)]
    
    #if the number is 2, the coda will be invalid, but the onset and nucleus will be valid
    else:
        coda = invalidCodas[random.randint(0, len(invalidCodas) -1)]
        nucleus = validNucleus[random.randint(0, len(validNucleus) -1)]
        onset = validOnsets[random.randint(0, len(validOnsets) -1)]

    #put the word together
    randomString = onset + nucleus + coda

    #if the random string happens to be a real wordn (somehow)
    #make a new random string
    while ENdict.check(randomString):
        randomString = invalidHelper()

    return randomString



#generates testing data
def makeData(engNum, nonceNum, invalidNum):

    #gather the english words
    engData = pullFromFile(corpusFolder / "monosyllabicOxfordWords.txt", engNum)
 

    #gather the nonce words
    print("The gathering of English words is complete. Starting the gathering of nonce words. ")
    nonceData = nonceWordMaker(nonceNum)

    #gather the invalid words
    print("The gathering of nonce words is complete. Starting the gathering of invalid words. ")
    invalidData = invalidWordMaker(invalidNum)

    data = engData + nonceData + invalidData

    return data



#writes to a file
def writeWords(list, outputname):
    with open(outputname, 'w') as f:
        for i in range(len(list)):
            #don't add a newline character to the end
            #of the file
            if i == len(list) -1:
                f.write(list[i])
            else:
                f.write(list[i] + '\n')



#Run the function here
writeWords(makeData(15, 15, 15), wordsFolder / 'allWordsMini.txt')