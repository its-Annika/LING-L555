import sys
import re

#reads in the data from segmenter.py as sentences
sentences = sys.stdin.readlines()


#outputs the header
sys.stdout.write("ID\tLEMMA\tUPOS\tXPOS\tFEATS\tHEAD\tDEPREL\tDEPS\tMISC")

sentenceCount = 1

#flips through the sentences
for sentence in sentences:
	
	#print the entire sentence
	sys.stdout.write("\n")
	sys.stdout.write("# sent_id = " + str(sentenceCount) + "\n")
	sentenceCount +=1
	sys.stdout.write("# text = " + sentence)
	

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
	#and removes leading and trailing \ns
	temp2  = re.sub(r'\n+', '\n', temp).strip("\n")
	
	#list of words in the sentences
	words = temp2.split("\n")

	#word in sentence counts
	count = 1
	
	#for each word in the sentence, print out the ID, the word, and all the other things
	for word in words:
			#print('%d\t%s\t_\t_\t_\t_\t_\t_\t_\t_' % (count, word.strip()))
		sys.stdout.write(str(count) + "\t" +word.strip() + "\t_\t_\t_\t-\t_\t_\t_\t_\n")
		count += 1

	
	















