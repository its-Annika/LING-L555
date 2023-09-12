import sys
 
#gets the orginal text
originalText = sys.stdin.read()

#removes the existing new line characters
#because they aren't meaningful yet
noNewLines = originalText.replace('\n', ' ')

#finds the pattern '. ' 
#and replaces it with '.\n'
finalText = noNewLines.replace('. ', '.\n')

#outputs the new version of the text
sys.stdout.write(finalText)
