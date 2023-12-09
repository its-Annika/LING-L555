"""
neigborhoodModel.py finds the neighborhood score of a given word. 

nNeighborhood scores are determined by changing one letter of the inputed
word at a time, either by insertion, deletion, or substitution,
and seeing if that alteration created a valid English word.
"""
import enchant

# dict of English words
dict = enchant.Dict("en_US")


#calculates the neighborhood score
def calculateNeighborhoodScore(word):
    formatedWord = word.lower().strip(" ")
    score = 0
    foundForms = []

    characters = ["a","b","c","d","e","f","g","h", "i", "j", "k", "l", "m","n","o", "p", "q", "r","s","t","u","v","w","x","y","z"]
    
    #alter one character of the word at a time
    #check if that alteration created a valid English word
    for i in range(len(formatedWord)):

        #delete a character, if the word is long enough
        if len(formatedWord) > 1:
                tempWordDeletion = str(formatedWord[0:i] + formatedWord[i+1:])
                #and count it
                if dict.check(tempWordDeletion) and tempWordDeletion != word and tempWordDeletion not in foundForms:
                    score += 1
                    foundForms.append(tempWordDeletion)

        for character in characters:
            #add swap a character
            tempWordSubsiution = str(formatedWord[0:i] + character + formatedWord[i+1:])
            #add an aditional character
            tempWordAddition = str(formatedWord[0:i] + character + formatedWord[i:])

    #count valid forms
            if dict.check(tempWordSubsiution) and tempWordSubsiution != word and tempWordSubsiution not in foundForms:
                score += 1
                foundForms.append(tempWordSubsiution)
       
            if dict.check(tempWordAddition) and tempWordAddition != word and tempWordAddition not in foundForms:
                score += 1
                foundForms.append(tempWordAddition)
            
            #covers epenthis at the end of the word, when i is out of range
            if i == len(formatedWord) -1:                                                                            
                tempWordAddition2 = str(formatedWord + character)
                
                if dict.check(tempWordAddition2) and tempWordAddition2 != word and tempWordAddition2 not in foundForms:
                    score += 1
                    foundForms.append(tempWordAddition2)
    

    #return the score, normalized by length
    return score/len(formatedWord)
