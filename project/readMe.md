# Comparing Three Models of Word Acceptability

Wellformedness judgments of nonce words are gradient (Hammond, 2004). Both 'blick' and 'bnick' are nonce words, however, some intuition dictates that 'blick' could be a word of English, while 'bnick' could not (Chomsky & Halle, 1965).

This project presents three models which score monosyllabic words on their English wellformedness or acceptability, and determines which model best matches gradient human intuition.

***
## The Models

##### Trigram Model
The first model is a trigram model (Jurafsky & Martin, 2023; Özkan, 2014). Grapheme level trigram models calculate the probability of a word by multiplying the probabilities of smaller segments within the word. For example, the trigram probability of 'cat' is calculated as follows:

```
P(cat) = P(##c|##)P(#ca|#c)P(cat|ca)P(at@|at)P(t@@|t@)
```
where '#' and '@' denote placeholder positions at the beginning and end of a word respectively.


The trigram model implemented here makes use of Laplace, or add-one, smoothing. Laplace smoothing takes any trigrams which have a count of zero, and gives them a count of one. The vocabulary size is incremented accordingly (Jurafsky & Martin, 2023). Laplace smoothing was implemented by generating all possible trigrams and adding them to the training data, which was an edited version of the Brown Corpus, with any non-alphabetic characters removed. Each word was formatted with characters marking its beginning and end (##word@@), to allow for the model to account for a segment’s position within a word. Probabilities were normalized for length.

##### Neighborhood Model

The second model implemented is a neighborhood density model. Neighborhood density scores are calculated by changing one letter of a given word at a time, either by insertion, deletion, or substitution, and checking if the resulting form is an actual English word (Bailey and Hahn, 2001; Hammond, 2004). The forms check by neighborhood density for the word 'cat' are as follows:

    deletion: 'at', 'ct', 'ca'
    insertion: 'acat', 'bcat', 'ccat', ..., 'caat', 'cbat', 'cdat', ..., 'cabt', 'cact', 'cadt', ..., 'cata', 'catb', 'cact', ...
    substituion: 'aat', 'bat', 'dat', ..., 'cbt', 'cct', 'cdt', ..., 'caa', 'cab', 'cac', ...
Duplicate forms are not counted; insertion before 'c' and after 'c' both result in the form 'ccat', but 'ccat' is only checked once. Additionally, neighborhood density scores were normalized for length.

The higher a form’s neighborhood density score, the more wellformed said form is (Hammond, 2004).  

##### Linear Regression Model

The third model is a linear regression model, more specifically, [scikit-learn][scikit-learn]'s prebuilt linear regression model. Linear regression functions by training on data made up of independent variable-dependent variable pairs, from which a linear function of best fit is determined. For this implementation, the independent variables were feature vectors extracted from IPA forms and the dependent variables were scores from human annotators (the process of attaining these scores is described below). 

Feature extraction consists of converting IPA forms into 2-Dimensional feature vectors with 9 rows and 22 columns, where each row corresponds to a phone in the IPA form (with rows 1-3 reserved for the onset, rows 4-5 for the nucleus, and rows 6-9 for the coda) and where each column corresponds to a phonological feature (syllabic, sonorant, consonantal, continuant, delayed release, lateral, nasal, strident, voice, spread glottis, constricted glottis, anterior, coronal, distributed, labial, high, low, back, round, velaric, tense, and long). A feature can have one of three values: -1 meaning the phone is [-feature], 1 meaning the phone is [+feature], and 0 meaning said feature is not applicable to the phone. Features values for phones are found using [panphon][panphon]. If a given IPA form is shorter than 9 phones, the form is padded with rows of -1. The feature vector for the word 'cat' is as follows:
 

            [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]
             [-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]
      k      [-1 -1  1 -1 -1 -1 -1  0 -1 -1 -1 -1 -1  0 -1  1 -1  1 -1 -1  0 -1]
      æ      [ 1  1 -1  1 -1 -1 -1  0  1 -1 -1  0 -1  0 -1 -1  1 -1 -1 -1  1 -1]
             [-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]
      t      [-1 -1  1 -1 -1 -1 -1  0 -1 -1 -1  1  1 -1 -1 -1 -1 -1 -1 -1  0 -1]
             [-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]
             [-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]
             [-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]]




***
## Gathering and Evaluating Data

##### Creating Training and Testing Data

Three types of monosyllabic words were used as training and testing data.

 - **Valid Words**: English words sourced from the [Oxford English Dictionary][oxford], which did not appear in the [Brown Corpus][brown]. 
 - **Nonce Words**: Words that could be words of English, but aren't. These were created by combining valid English onsets, nuclei, and codas in ways that did not result in actual words of English. For example, 'scr' is a valid English onset, 'au' is a valid English nucleus, and 'shed' is a valid English coda, but 'scraushed' is not a word of English. Valid English syllable constituents were sourced from Hammond (1999).
 - **Invalid Words**: Words that could not be words of English. These were created by combining two valid English syllable constituents with one invalid English syllable constituent. For example, 'str' is a valid English onset, 'i' is a valid English nucleus, but 'brg' is an invalid English coda, resulting in the invalid word 'stribrg'.
 
To eliminate possible biases, generated words that were valid German or French words, or were common proper nouns, were rejected. 

A total of 1,080 word were generated (360 from each category). 864 words were used as training data (288 from each category) and 216 words were used as testing data (72 from each category).


##### Data Annotation 
The 1,080 generated words were divided into three data sets, with each data set containing 120 words from each category. Each data set was given to 4 annotators. The annotators were asked to rate each word on the following 3-point scale. 

1 : This word does not look like English - reject  
3 : This word sort of looks like English - moderately accept  
5 : This word looks like English - accept  

Final scores for each word were found by averaging the four annotator ratings. 


***
## Results

To evaluate which model best matched human intuition, annotator scores of the testing data were correlated with model scores of the testing data. The correlation coefficients are as follows:

**Trigram Model** : 0.733216289  
**Neighborhood Model** : 0.5276891809  
**Linear Regression Model** : 0.6998836032  

Based on these correlation coefficients, the **trigram model** best approximates human judgments of word acceptability.


***
## Discussion

###### Poor Performance of the Neighborhood Model
Given its correlation coefficient of only  0.53, the neighborhood model can be said to do a poor job of predicting word acceptability. While this is certainly true of the current implementation of the neighborhood model, the model's poor performance could be due to the conflict between its evaluation process and the structure of the testing data. 

As stated above, testing data was created by combining syllable constituents, that is valid and invalid English onsets, nuclei, and codas. By contrast, the neighborhood model makes edits involving only  one grapheme by insertion, deletion, or substitution. The following example illustrates why this mismatch is problematic. 

Consider the English word 'blotch', which received an average score of 5 from annotators, indicating that it is highly phototactically acceptable. The neighborhood model, however, gave the same form a score of 0.5, indicating that it is far from phototactically acceptable. This may seem strange, as 'blotch' is similar to many other English words: 'scotch', 'crotch', 'block', 'blob', etc. The key is that these similar words are found by editing an entire syllable constituent. Given that the neighborhood model is restricted to an edit distance of one, it never evaluates these forms. Instead, the neighborhood model evaluates forms like the following: 'btlotch', 'blotc', 'blotchb', etc, which aren't word-like in the slightest. This implementation of the neighborhood model is incapable of swapping out syllable constituents, making it a poor model of word acceptability.

A neighborhood model which may lend itself to the task of word acceptability is a model which is capable of swapping syllable constituents. Instead of deleting a single grapheme, it would delete the onset or the coda. Instead of substituting a single grapheme, it would swap onsets for onsets, nuclei for nuclei, and codas for codas. Instead of inserting a single phone, it would combine onsets or codas (the onsets 's' and 't' would become 'st'). This behavior would likely result in a better model of word acceptability, given that it would enable the model to evaluate forms such as 'scotch', 'crotch', 'block', 'blob', which were previously unavailable.

###### Graphemes vs Phonemes
The two best performing models, the trigram model and the linear regression model, have relatively similar correlation coefficients: .73 and .7 respectively. This similarity in performance is interesting considering that the trigram model operates on orthographic forms, while the linear regression model operates on IPA transcriptions. It is then reasonable to question if the trigram model preforms better because of how it calculates scores, or because it uses orthographic forms. To resolve this question, two additional models require implementation: a trigram model which operates on IPA forms and a linear regression model which operates on orthographic forms. These models would be relatively simple to implement. For the trigram model, simply swap the training data to a corpus of IPA transcriptions. For the linear regression model, create vectors that are 26 column across, one position for each letter of the alphabet, and however many rows down as the longest word it would be expected to process (which [Wikipedia][records] suggests to be 10 or 11 characters).

###### Difficulty of Using Tools 'Incorrectly'
A significant difficulty encountered during this project was the 'incorrect' use of tools, especially in regard to [epitran][epitran]. [epitran][epitran] takes orthographic forms and transcribes them into IPA based on a chosen transliteration language, which for this project was English. Given that [epitran][epitran] expects to receive valid English words, i.e. words that align with English phonotactics, it often produced incorrect or poorly repaired IPA transcriptions of invalid English words, i.e. phototactically ill-formed words. In order to combat this issue, this project requires every IPA transcription to be manually checked, which while solving the problem of poor transcription, drastically increases the skill and patience required of the user. While manual checking was successful for the relatively small training and testing data sets used in this project, a better solution would need to be found to cope with larger data sets.

***
## Possible Model Improvements

###### Trigram model
The current implementation of the trigram model is trained on the [Brown Corpus][brown], which includes monosyllabic and multisyllabic words. Given that the training and testing data used in this project is monosyllabic, training the trigram model on a corpus consisting of only monosyllabic words may improve results.


###### Neighborhood Model
As was stated above, the neighborhood model would likely be improved if editing of syllabic constituents was implemented. 

###### Linear Regression Model
While the current implementation of this model has  exhaustive phonological feature knowledge, it receives no information about the graphemes that make up a given word. Because of this, some strange looking words lose their strangeness, as their transcriptions can't reflect their orthographic peculiarity. For example, 'phoiffs' looks strange, as evidenced by its annotator score of 1.5, but has the relatively normal looking IPA transcription of [flɔjfs], reflected it its linear regression score of 2.7. If the model had access to both phonological and orthographic information, it would be able to identify not only unlikely combinations of phones, but also of graphemes, likely improving model performance.

***
# The Program
The following modules are required to run the program. 
| Module | Link |
| ------ | ------ |
| panphon | [https://pypi.org/project/panphon/0.5/][panphon] |
| epitran | [https://pypi.org/project/epitran/0.22/][epitran] |
| pyenchant | [https://pypi.org/project/pyenchant/][pyenchant] |
| scikit-learn | [https://pypi.org/project/scikit-learn/][scikit-learn] |
| numpy | [https://pypi.org/project/numpy/][numpy]|

## Running the Program

The program is currently set up to run a mini-demo. Text files used in this demo are indicated by the 'mini' keyword. To exit demo-mode, remove 'mini' from the file names in gatherScores.py, wordGenerator.py, makeVectors.py, and linearRegressionModel.py. 

##### Step 1: Generate Words
Use wordGenerator.py to generate words from three categories: English/valid words, nonce words, and invalid words. Change the number of generated words by altering the integer arguments in the makeData() function call at the end of the file. The user must approve every word in order to manually filter out inappropriate language or multisyllabic words which weren't successfully filtered out earlier on. This program writes to allWords.txt/allWordMini.txt within the words folder. An example of this process is as follows:

    tights
    This word is...
    German: False, False
    French: False, False
    a name: False

The program then waits for the user to either press enter, indicating that the word is acceptable, or for the user to hit any key, indicating that the word is not acceptable. 

##### Step 2: Split Data into Training and Testing 
- Place the training data into trainingWords.txt/minitrainingWords.txt within the words folder. This data must be annotated with scores. One tab delineated word-score pair per line. 
- Place the testing data into testingWords.txt/minitestingWords.txt within the words folder, one word per line.

##### Step 3: Train the Linear Regression Model
Run vectorMaker.py located within the LinearRegression folder. Make sure the **train() function call** at the end of the file is **uncommented**. For each word in trainingWords.txt/minitrainingWords.txt, word,feature vector,score will be written to trainingVectors.txt/minitrainingVectors.txt within the LinearRegression folder. 

When creating vectors, the user will be required to check the IPA form created for each inputted word. This is to prevent any repairs (usually vowel epenthesis) made by [epitran][epitran] to illformed English words. It will look as follows:

    word: cat
    kæt
    k æ t

where the first line is the orthographic form, the second line is the IPA transcription, and the last line is the IPA transcription segmented into onset, nucleus, and coda. The program then waits for the user to either press enter, indicating that this IPA form is correct, or for the user to enter a corrected IPA form. The corrected IPA form must have **at maximum**, a three place onset, a two place nucleus, and a four place coda. Please adhere to the following guidelines:
 
|If you'd like this symbol... |Enter this one|
|-|-|
|ɹ̩|ɻ|
| tʃ|x|
|dʒ|ɣ|

**Do not use any diacritics**. A helpful IPA keyboard can be found [here][IPAkey].



##### Step 4: Gather Scores
Run gatherScores.py. This file calculates scores from each model for words in testingWords.txt/minitestingWords.txt. The trigram and neighborhood scores will be gathered automatically, but once again, the linear regression model will require hand checking of IPA forms. Scores for each model are written to their corresponding scores file within the modelScores folder. Before running this file, make sure the **train() function call in vectorMaker.py** is **commented out**.
***
## Comprehensive Description of the Program

Assume that demo-specific text files serve the same function as the text files which share the same name without the 'mini' keyword.
#### corpora Folder
This folder contains various corpora used in the project. These include:

- brownCorpusClean.txt : The [Brown Corpus][brown] with all punctuation and numeric characters removed. 
- first-names.txt : A list of common [male][mens names] and [female][womens names] names.
- monosyllabicBrownTypes.txt : Monosyllabic unique types from the [Brown Corpus][brown].
- monosyllabicOxfordWords.txt : Monosyllabic words from the [Oxford English Dictionary][oxford] that aren't in the [Brown Corpus][brown].
- oxfordWords.txt : All words from the [Oxford English Dictionary][oxford].
- topBrownTypes.txt : The 2,000 most frequent monosyllabic types from the [Brown Corpus][brown].

#### invalidBits Folder
This folder contains invalid English syllable constituents. 
- invalidCodas.txt : invalid English codas.
- invalidOnsets.txt : invalid English onsets.

#### tools Folder
This folder contains tools for processing data.
- brownProcesser.py : Finds monosyllabic types in the [Brown Corpus][brown], and writes them to monosyllabicBrownTypes.txt. The top 2,000 of these types are written to topBrownTypes.txt.
- miscTools.py : Contains various functions used to create and process IPA forms. 
- writeOxfordDict.py : Finds monosyllabic words from the [Oxford English Dictionary][oxford] that aren't in the [Brown Corpus][brown] and writes them to monosyllabicOxfordWords.txt. 

#### words Folder
This folder contains the training and testing data. 
- allWords.txt : where all words generated by wordGenerator. py are written to. 
- testingWords.txt : the testing data read in by gatherScores. py.
- trainingWords.txt : the training data used to train the linear regression model.  

#### modelScores Folder
This folder contains scores given to the testing data by each model.
- linearRegressionScores.txt : scores of the testing data from the linear regression model.
- neighborhoodScores.txt : scores of the testing data from the neighborhood model.
- trigramScores.txt : scores of the testing data from the trigram model. 

#### LinearRegression Folder
This folder contains the linear regression model. 
-   linearRegressionModel.py : contains the model itself and the function which determines scores of inputted words. 
-   vectorMaker. py: contains the function which extracts features from imputed words, and the function which creates training vectors.
-   trainingVectors.txt : stores vectors created from training data to train the linear regression model. 

#### neighborhoodModel.py
This file contains the neighborhood model, which calculates neighborhood density scores for imputed forms. 

#### trigramModel.py
This file contains the trigram model, and the function which calculates trigram probabilities for imputed forms. 

#### wordGenerator.py
This file generates words to be used as training and testing data. Words are written to allWords.txt within the words folder.

#### gatherScores.py
This file gets the trigram probabilities, neighborhood density scores, and linear regression scores for the testing data. Scores are written to the modelScores folder.
***
## References

Bailey, T. and Hahn, U. (2001). Determinants of wordlikeness: Phonotactics or
lexical neighborhoods? Journal of Memory and Language, 44:568–591.

Chomsky, N. and Halle, M. (1965). Some controversial questions in phonological
theory. Journal of Linguistics, 1(2):97–138.

Hammond, M. (1999). The Phonology of English, chapter Chapter 3. English Syllables: Margins and Consonants. Oxford University Press.

Hammond, M. (2004). Gradience, phonotactics and the lexicon in english phonology.
International Journal of English Studies (IJES), 4.

Jurafsky and Martin (2023). Speech and Language Processing, chapter 3. 3rd edition.

Özkan, K. (2014). Using corpus statistics to evaluate nonce words. In Pristine Perspectives on Logic, Language, and Computation. ESSLLI ESSLLI 2013 2012, pages
26–35, Berlin, Heidelberg.

***
## Corpora
| Title | Link |
| ------ | ------ |
| Brown Corpus | [http://www.sls.hawaii.edu/bley-vroman/brown_corpus.html][brown] |
|Oxford English Dictionary | [https://github.com/sujithps/Dictionary/blob/master/Oxford%20English%20Dictionary.txt][oxford]
|Common Male Names| [https://www.cs.cmu.edu/Groups/AI/areas/nlp/corpora/names/male.txt][mens names]|
|Common Female Names |[https://www.cs.cmu.edu/Groups/AI/areas/nlp/corpora/names/female.txt][womens names]|
***




[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [panphon]: <https://pypi.org/project/panphon/0.5/>
   [epitran]: <https://pypi.org/project/epitran/>
   [pyenchant]: <https://pypi.org/project/pyenchant/>
   [scikit-learn]: <https://pypi.org/project/scikit-learn/>
   [numpy]: <https://pypi.org/project/numpy/>
   
   [brown]: <http://www.sls.hawaii.edu/bley-vroman/brown_corpus.html>
   [oxford]: <https://github.com/sujithps/Dictionary/blob/master/Oxford%20English%20Dictionary.txt>
   [mens names]: <https://www.cs.cmu.edu/Groups/AI/areas/nlp/corpora/names/male.txt>
   [womens names]: <https://www.cs.cmu.edu/Groups/AI/areas/nlp/corpora/names/female.txt>
   
   [trigram]: <https://web.stanford.edu/~jurafsky/slp3/3.pdf>
   
   [records]: <https://en.wikipedia.org/wiki/List_of_the_longest_English_words_with_one_syllable>
   
   [IPAkey]: <https://westonruter.github.io/ipa-chart/keyboard>
   
