"""
neigborhoodModel.py finds the neighborhood score of a given word. 

The neighborhood score is determined by changing one letter of the inputed
word at a time, and seeing if that alteration created a valid English word.

The judgeAcceptability function determines the acceptability judgment of an
imputted word. 
"""



import enchant

# dict of English words
dict = enchant.Dict("en_US")

#TODO if the similar word is really low frequency, decrese the neighborhood score?


#calculates the neighborhood score
def calculateNeighborhoodScore(word):
    formatedWord = word.lower().strip(" ")
    score = 0

    characters = ["a","b","c","d","e","f","g","h", "i", "j", "k", "l", "m","n","o", "p", "q", "r","s","t","u","v","w","x","y","z"]
    
    #alter one character of the word at a time
    #check if that alteration created a valid English word
    for i in range(len(formatedWord)):

        #delete a character, if the word is long enough
        if len(formatedWord) > 1:
                tempWordDeletion = str(formatedWord[0:i] + formatedWord[i+1:])
                #and count it
                if dict.check(tempWordDeletion):
                    score += 1

        for character in characters:
            #add swap a character
            tempWordSubsiution = str(formatedWord[0:i] + character + formatedWord[i+1:])
            #add an aditional character
            tempWordAddition = str(formatedWord[0:i] + character + formatedWord[i:])

    #count valid forms
            if dict.check(tempWordSubsiution):
                score += 1
            if dict.check(tempWordAddition):
                score += 1
    
    
    #return the score, normalized by length
    return score/len(formatedWord)


#determines the acceptability judgment
#values determined based on the training data
def judgeAcceptability(score):

    if score <= 0:
        return "Reject"
    if score < 1:
        return "Moderatly Accept"
    else:
        return "Accept"