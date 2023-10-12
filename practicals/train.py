import sys
from collections import defaultdict

#reads in the data
data = sys.stdin.readlines()

#variables
tokenCounter = 0
tagFrequency = defaultdict(lambda:0)
matrix = defaultdict(lambda:0)
seenWords = []

for line in data:
	if "\t" not in line:
		continue
	else:
		#finds the word and the tag
		row = line.split("\t")
		word = row[1]
		tag = row[3]

		#increments token count
		tokenCounter += 1
	
		#updates the tag dictionary
		tagFrequency[tag] += 1

		#updates the matrix
		if word not in seenWords:
			matrix[word] = defaultdict(lambda:0)
			matrix[word][tag] = 1
		else:
			matrix[word][tag] += 1

		#keeps track of what words have been seen
		seenWords.append(word)
	

#output time

sys.stdout.write("# P \t count \t tag \t form\n")

for tag in tagFrequency.keys():
	sys.stdout.write('%.2f' % (tagFrequency[tag]/tokenCounter))
	sys.stdout.write("\t" + str(tagFrequency[tag]) + "\t" + tag + "\t_\n")

for word in matrix:
	
	tags = []
	wordCount = 0

	for tag in matrix[word]:
		
		#collect the tags
		tags.append(tag)

		#find the total occuraces of the word
		#by adding up all its tags
		wordCount += matrix[word][tag]

	for tag in tags:
		p = matrix[word][tag]/wordCount
		count = matrix[word][tag]
		form = word
		
		sys.stdout.write(str(p) +"\t"+ str(count) +"\t"+ tag 
+"\t"+ form +"\n")	
		
	
