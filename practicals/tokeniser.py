import sys
import re

#reads in the data from segmenter.py as sentences
sentences = sys.stdin.readlines()


#outputs the header
sys.stdout.write("ID\tLEMMA\tUPOS\tXPOS\tFLEATS\tHEAD\tDEPREL\tDEPS\tMISC")

#flips through the sentences
for sentence in sentences:
	
	#print the entire sentence
	sys.stdout.write(sentence)
	

	#formats the sentence so that puctuation is wrapped in \ns
	#and spaces are replaced with \ns

	temp = "" 
	
	for character in sentence:

		if character in ":.,\'\"()<>{}!?":
			temp += "\n" + character + "\n"
		elif character == " ":
			temp += "\n"
		else:
			temp += character
	
	#corrects any duplicate \ns
	temp2  = re.sub(r'\n+', '\n', temp)
	
	#list of words in the sentences
	words = temp2.split("\n")

	#word in sentence counts
	count = 1
	
	#for each word in the sentence, print out the ID, the word, and all the other things
	for word in words:
		sys.stdout.write(str(count) + "\t" + word + "\t" + "\t-\t-\t-\t-\t-\t-\t-\t-\t\n")
		count += 1

	
	















