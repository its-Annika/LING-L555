import sys
import re

#reads in the data from segmenter.py
data = sys.stdin.read()

#the .replace method.
#replaces a given punctuation with a the pattern
# \n punctuation \n
#this could be repeated until all the chosen punctuation
#were accounted for
a = data.replace(" ", '\n')
b = a.replace('.', "\n.\n")
c = b.replace(',', "\n,\n")
d = c.replace('(', "\n(\n")
e = d.replace(')', "\n)\n")

#this corrects having too many \n in a row
#if one or more \n are found in a row, replace them with a single \n
#which prevents empty lines in the output
f = re.sub(r'\n+', '\n', e)

#output it
sys.stdout.write(f)

####################################################################################

#for loop method
#I tried out a for loop version because manualy replacing each type of punctuation
#seemed like more work than replacing everything in one process

#storage
#finalString = ""

#for each character
#if it's a space, turn add a \n to the finalString
#elif it's a peice of punctuation in this list, add the pattern
# \n punctuation \n to finalString
# else, add the character as it is to finalString

#for character in data:
#	if character == " ":
#		finalString += '\n'
#	elif character in ",.():\"\'?!":
#		finalString += '\n' +  character + '\n'
#	else:
#		finalString += character 

#gets rid of duplicate \n characters
#finalStringV2  = re.sub(r'\n+', '\n', finalString)

#output
#sys.stdout.write(finalStringV2)
