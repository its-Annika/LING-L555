# Comparing Three Models of Word Acceptability
***
Wellformedness judgments of nonce words are gradient (Hammond, 2004). Both blick and bnick are nonce words, however, some intuition dictates that blick could be a word of English, while bnick could not (Chomsky & Halle, 1965).

This project presents three models which score monosyllabic words on their English wellformedness, and determines which model best matches gradient human intuition.

***
## The Models

##### Trigram Model
The first model is a trigram model (Jurafsky & Martin, 2023; Özkan, 2014). Trigram models calculate the probablity of a word by multiplying the probablilities of smaller segments within the word together.For example, the trigram probability of 'dog' is calculated as follows, 

```
P(dog) = P(##d|##)P(#do|#d)P(dog|do)P(og@|og)P(g@@|g@)
```
where '#' and '@' denote placeholder positions at the beginning and end of a word respectivly. 


The trigram model implement here makse use of Laplace, or add-one, smooth-ing. Laplace smoothing takes any trigrams which have a count of zero, and gives them a count of one. The vocabulary size is incremented accordingly (Jurafsky & Martin, 2023). Laplace smoothing was implemented by generating all possible trigrams and adding them to the training data, which was an edited version of the Brown Corpus, where any non-alphabetic characters are re-moved. Each word was formatted with characters marking its beginning and end (##word@@), to allow for the model to account for a segment’s position within a word. Probabilities were normalized for lenght. 

##### Neighborhood Model

The second model implemented is a neighborhood density model. Neighborhood density scores are calculated by changing one letter of a given word at at time, either by insertion, deletion, or substitution, and checking if the resulting form is an actual English word (Bailey and Hahn, 2001; Hammond, 2004). For example, given the word “at” the forms checked by neighborhood density are ‘t’, ‘at’, ‘bt’, ‘ct’, ..., ‘a’, ‘aa’, ‘ab’, ‘ac’, ..., 'aat', 'bat', 'cat', ..., 'aat', 'abt', 'act', ..., and 'ata', 'atb', 'atc'. 

The higher a form’s neighborhood density score, the more wellformed said form is (Hammond, 2004). Neighborhood density scores were normalized for length. 

##### Linear Regression Model
#
#
#
#
#

###### Vector Structure
***
## Gathering and Evaluating Data

##### Creating Training and Testing Data

Three types of monosyllabic words were used as training and testing data.

 - Valid Words: English words sourced from the Oxford English Dictionary. 
 - Nonce Words: Words that could be words of English, but aren't. These were created by combining valid English onsets, nuclei, and codas in ways that did not result in actual words of English. For example, 'scr' is a valid English onset, 'au' is a valid English nucleus, and 'shed' is a valid English coda, but 'scraushed' is not a word of English. Valid English syllable constiuants were sourced from Hammond (1999).
 - Invalid Words: Words that could not be words of English. These were created by combining two valid English syllable consituents with one invalid English syllable consituent. For example, 'str' is a valid English onset, 'i' is a valid English nucleus, but 'brg' is an invalid English coda, resulting in the invalid word 'stribrg'.
 
To elimate possible biases, generated words that were valid German or French words, or were common proper nouns were rejected. 

A total of 1,080 word were generated (360 from each category). 864 words were used as training data (288 from each category) and 216 words were used as testing data (72 from each category). 

##### Data Annotation 
The 1,080 generated words were divided into three data sets, with each data set containing 120 words from each category in random order. Each data set was given to X annotators. The annotators were asked to rate each word on the following 3-point scale. 

1: This word does not look like English: reject
3: This word sort of looks like English: moderately accept
5: This word looks like English: accept

Final scores for each word were found by averaging the X ratings. 


***
## Results

To evauate which model best matched the annatator scores, annatotar scores of the testing data were corrolated with model scores of the testing data. The correlation coeficiants are as follows.

Trigram Model: 
Neighborhood Model:
Linear Regression Model

Based on these corrlation coefiicnat, the X model best approximade human jugments of word accptability. 

***
## Discussion


***
***
# How to Run the Program

#### Required Modules
| Module | Link |
| ------ | ------ |
| panphon | [https://pypi.org/project/panphon/0.5/][panphon] |
| epitran | [https://pypi.org/project/epitran/0.22/][epitran] |
| pyenchant | [https://pypi.org/project/pyenchant/][pyenchant] |
| scikit-learn | [https://pypi.org/project/scikit-learn/][scikit-learn] |
| numpy | [https://pypi.org/project/numpy/][numpy]|

***
# References

Bailey, T. and Hahn, U. (2001). Determinants of wordlikeness: Phonotactics or
lexical neighborhoods? Journal of Memory and Language, 44:568–591.


Chomsky, N. and Halle, M. (1965). Some controversial questions in phonological
theory. Journal of Linguistics, 1(2):97–138.

Hammond, M. (1999). The Phonology of English, chapter Chapter 3. English Sylla-
bles: Margins and Consonants. Oxford University Press.

Hammond, M. (2004). Gradience, phonotactics and the lexicon in english phonology.
International Journal of English Studies (IJES), 4.

Jurafsky and Martin (2023). Speech and Language Processing, chapter 3. 3rd edition.

Özkan, K. (2014). Using corpus statistics to evaluate nonce words. In Pristine Per-
spectives on Logic, Language, and Computation. ESSLLI ESSLLI 2013 2012, pages
26–35, Berlin, Heidelberg.

### Corpora
| Title | Link |
| ------ | ------ |
| Brown Corpus | [http://www.sls.hawaii.edu/bley-vroman/brown_corpus.html][brown] |
|Oxford English Dictionary | [https://github.com/sujithps/Dictionary/blob/master/Oxford%20English%20Dictionary.txt][oxford]
|Common Male Names| [https://www.cs.cmu.edu/Groups/AI/areas/nlp/corpora/names/male.txt][mens names]|
|Common Female Names |[https://www.cs.cmu.edu/Groups/AI/areas/nlp/corpora/names/female.txt][womens names]|




```sh
127.0.0.1:8000
```



[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [panphon]: <https://pypi.org/project/panphon/0.5/>
   [epitran]: <https://pypi.org/project/epitran/0.22/>
   [pyenchant]: <https://pypi.org/project/pyenchant/>
   [scikit-learn]: <https://pypi.org/project/scikit-learn/>
   [numpy]: <https://pypi.org/project/numpy/>
   
   [brown]: <http://www.sls.hawaii.edu/bley-vroman/brown_corpus.html>
   [oxford]: <https://github.com/sujithps/Dictionary/blob/master/Oxford%20English%20Dictionary.txt>
   [mens names]: <https://www.cs.cmu.edu/Groups/AI/areas/nlp/corpora/names/male.txt>
   [womens names]: <https://www.cs.cmu.edu/Groups/AI/areas/nlp/corpora/names/female.txt>
   
   [trigram]: <https://web.stanford.edu/~jurafsky/slp3/3.pdf>
   
