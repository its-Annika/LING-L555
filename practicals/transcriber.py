#setting up our translation dictionary
key = open('transcriptKey.txt', 'r')
keyLines = key.readlines()

#graphemes, phonemes
transKey = {}

for line in keyLines:
	parts = line.strip("\n").split("\t")
	transKey[parts[0]] = parts[1]

key.close()



###################################################


#I reused your code :)

import sys

for line in sys.stdin.readlines(): 
    # strip any excess newlines
	line = line.strip('\n')
    # if there is no tab character, skip the line
	if '\t' not in line:
		sys.stdout.write(line + "\n")
		continue
    # make a list of the cells in the row
	row = line.split('\t')
    # if there are not 10 cells, skip the line
	if len(row) != 10:
		continue
    # the form is the value of the second cell
	form = row[1].lower()

###################################################

#translation time 
	newForm = ""
	i = 0
	
	while(i < len(form)):
		
		#first checks if three character sequences are in the dict: "sch"			
		if i < (len(form)) -2 and  str(form[i]+ form[i+1] +form[i+2]) in transKey.keys():
			newForm += transKey[str(form[i]+ form[i+1]+form[i+2])]
			#adjusts i accordingly	
			i += 2

		#then if two character sequences are in the dict: dipthongs,...
		elif i < (len(form))-1 and str(form[i] + form[i+1]) in transKey.keys():
			newForm += transKey[str(form[i]+ form[i+1])]
			#adjusts i accordingly
			i += 1
		
		#if not
		else:
			#don't replace certain double vowels
			if i < (len(form))-2 and form[i] == form[i+1] and form[i] in "aeiourlmn":
				newForm += transKey[form[i]]
				i += 1
			
			#just replace single characters
			elif form[i] in transKey.keys():
				newForm += transKey[form[i]]
	
		#makes sure the loop moves for characters not in the dict	
		i += 1	

				
	row[9] = "IPA=" + newForm

	#output
	sys.stdout.write("\t".join(row) + "\n")
