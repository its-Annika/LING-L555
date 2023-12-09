"""
These are functions used throughout the project with process/create IPA forms.
"""
import panphon
import panphon.sonority
import panphon.segment
import epitran
import re

epi = epitran.Epitran('eng-Latn')
son = panphon.sonority.Sonority()
ft = panphon.FeatureTable()

#returns the ipa form of a word
def getIPAForm(word):
            
    #get the IPA form
    ipaForm = epi.transliterate(word)

    #panPhon doesn't accept supersegmentals
    #also, affriactes are considered as two seperate sounds instead of one.
    # meaning they look like sonority jumps.
    # 
    # because of this
    # t͡ʃ is replaced with x and d͡ʒ with ɣ
    #
    #syllabic r is replaced with ɻ

    ipaForm = ipaForm.replace('d͡ʒ', 'ɣ')
    ipaForm = ipaForm.replace('t͡ʃ', 'x')
    ipaForm = ipaForm.replace('ɹ̩', 'ɻ')
    
    return ipaForm 



#----------------------------------
    #SONORITY KEY

    # 9 [e, ɛ, æ, ə, ʌ, o, ɔ, ɑ]
    # 8 [i, ɪ, ʊ, u]
    # 7 [ɹ, w, j]
    # 6 [l]
    # 5 [m, n, ŋ]
    # 4 [v, ð, z, ʒ]
    # 3 [f, θ, s, ʃ, x]
    # 2 [b, d, g]
    # 1 [p, t, k]
#----------------------------------




#returns a boolean if the word is monosyllabic or not
def monosyllabic(IPAForm):

    foundPeak = False

    peakIndex = 0

    #for the letters in the word
    for i in range(len(IPAForm) -1):

        #find the peak, it can be a vowel or a syllabic r
        if son.sonority(IPAForm[i]) >= 8 or IPAForm[i] == 'ɻ':
            foundPeak = True
            peakIndex = i


        #checks the onset
        if (not foundPeak):

            #allows for fricitve followed by stop in word inital position
            if (i == 0 and not ft.word_fts(IPAForm[i])[0].match({'son': 1}) and ft.word_fts(IPAForm[i])[0].match({'cont': 1}) and not ft.word_fts(IPAForm[i+1])[0].match({'delrel': 1})):
                continue

            #default case, make sure sonority is increasing
            if son.sonority(IPAForm[i]) > son.sonority(IPAForm[i+1]):
                return False


        #if you've found the peak, make sure the segments are getting less sonorous
        if (foundPeak): 

            #if the peak is found, a syllabic r is a new syllable
            #make sure you don't catch the syllabic r if it's the nuceuls
            if (IPAForm[i] == 'ɻ' or IPAForm[i+1] == 'ɻ' and i != peakIndex):
                return False

            #unless it's a suffixed coda, like in 'tasks'
            if (not ft.word_fts(IPAForm[i+1])[0].match({'son': 1}) and ft.word_fts(IPAForm[i+1])[0].match({'cont': 1}) and not ft.word_fts(IPAForm[i])[0].match({'delrel': 1}) ):
                continue

            #or vowel hiatus, like in 'going' from getting through
            #dipthongs are written as [Vj] or [Vw], so this holds
            #had to specify this case because some vowels are more sonorous than others
            if (ft.word_fts(IPAForm[i])[0].match({'syl': 1}) and ft.word_fts(IPAForm[i+1])[0].match({'syl': 1})):
                return False

            #default case, make sure sonority is decreasing
            elif son.sonority(IPAForm[i]) < son.sonority(IPAForm[i+1]):
                return False
    
    #if the word got all the way through, it's monosylabic
    return True



#returns the onset of an IPA form
def getOnset(ipaForm):

    onset = ''

    #if you find part of the nucleus, the onset is over, so return it
    for symbol in ipaForm:
        if son.sonority(symbol) >= 8 or symbol == 'ɻ' or (symbol == 'j' and len(onset) >= 1):
            return onset
        
        onset += symbol


#returns the nucelus of an IPA form
def getNucleus(ipaForm):

    nuclaus = ''

    #remove the onset
    for symbol in re.sub(re.escape(getOnset(ipaForm)), '',ipaForm):

        #if the segment is very sonorus, or a syllabic r, or a w that follows a vowel, or a j that follows a vowel, or a j that is an onglide
        try:
            if son.sonority(symbol) >= 8 or symbol == 'ɻ' or (symbol == 'w' and len(nuclaus) >= 1) or (symbol == 'j' and len(nuclaus) >= 1) or (symbol == 'j' and  'j' not in getOnset(ipaForm)):
                nuclaus += symbol
            
            #if you've found a character that isn't one of these, the nucleus is over, so return it
            else:
                return nuclaus
            
        #sometimes panphon gives up, hence the try-else. The output is still correct, but sometimes son.sonority throws weird errors
        except:
            return nuclaus
    
    #sometimes there is no coda, so if you run out of characters without triggering the else block, return the nucleus
    return nuclaus
    


#returns the coda of an IPA form
def getCoda(ipaForm):

    coda = ''

    nucelaus = getNucleus(ipaForm)

    #remove all characters before and within the nucleus
    coda = re.sub(r'.*' + re.escape(nucelaus), '', ipaForm)

    return coda