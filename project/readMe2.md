<!DOCTYPE html><html><head><meta charset="utf-8"><title>readMe.md</title><style></style></head><body id="preview">
<h1 class="code-line" data-line-start="0" data-line-end="1"><a id="Comparing_Three_Models_of_Word_Acceptability_0"></a>Comparing Three Models of Word Acceptability</h1>
<hr>
<p class="has-line-data" data-line-start="2" data-line-end="3">Wellformedness judgments of nonce words are gradient (Hammond, 2004). Both blick and bnick are nonce words, however, some intuition dictates that blick could be a word of English, while bnick could not (Chomsky &amp; Halle, 1965).</p>
<p class="has-line-data" data-line-start="4" data-line-end="5">This project presents three models which score monosyllabic words on their English wellformedness, and determines which model best matches gradient human intuition.</p>
<hr>
<h2 class="code-line" data-line-start="7" data-line-end="8"><a id="The_Models_7"></a>The Models</h2>
<h5 class="code-line" data-line-start="9" data-line-end="10"><a id="Trigram_Model_9"></a>Trigram Model</h5>
<p class="has-line-data" data-line-start="10" data-line-end="11">The first model is a trigram model (Jurafsky &amp; Martin, 2023; Özkan, 2014). Trigram models calculate the probablity of a word by multiplying the probablilities of smaller segments within the word together.For example, the trigram probability of ‘dog’ is calculated as follows,</p>
<pre><code class="has-line-data" data-line-start="13" data-line-end="15">P(dog) = P(##d|##)P(#do|#d)P(dog|do)P(og@|og)P(g@@|g@)
</code></pre>
<p class="has-line-data" data-line-start="15" data-line-end="16">where ‘#’ and ‘@’ denote placeholder positions at the beginning and end of a word respectivly.</p>
<p class="has-line-data" data-line-start="18" data-line-end="19">The trigram model implement here makse use of Laplace, or add-one, smooth-ing. Laplace smoothing takes any trigrams which have a count of zero, and gives them a count of one. The vocabulary size is incremented accordingly (Jurafsky &amp; Martin, 2023). Laplace smoothing was implemented by generating all possible trigrams and adding them to the training data, which was an edited version of the Brown Corpus, where any non-alphabetic characters are re-moved. Each word was formatted with characters marking its beginning and end (##word@@), to allow for the model to account for a segment’s position within a word. Probabilities were normalized for lenght.</p>
<h5 class="code-line" data-line-start="20" data-line-end="21"><a id="Neighborhood_Model_20"></a>Neighborhood Model</h5>
<p class="has-line-data" data-line-start="22" data-line-end="23">The second model implemented is a neighborhood density model. Neighborhood density scores are calculated by changing one letter of a given word at at time, either by insertion, deletion, or substitution, and checking if the resulting form is an actual English word (Bailey and Hahn, 2001; Hammond, 2004). For example, given the word “at” the forms checked by neighborhood density are ‘t’, ‘at’, ‘bt’, ‘ct’, …, ‘a’, ‘aa’, ‘ab’, ‘ac’, …, ‘aat’, ‘bat’, ‘cat’, …, ‘aat’, ‘abt’, ‘act’, …, and ‘ata’, ‘atb’, ‘atc’.</p>
<p class="has-line-data" data-line-start="24" data-line-end="25">The higher a form’s neighborhood density score, the more wellformed said form is (Hammond, 2004). Neighborhood density scores were normalized for length.</p>
<h5 class="code-line" data-line-start="26" data-line-end="27"><a id="Linear_Regression_Model_26"></a>Linear Regression Model</h5>
<h1 class="code-line" data-line-start="27" data-line-end="28"><a id="_27"></a></h1>
<h1 class="code-line" data-line-start="28" data-line-end="29"><a id="_28"></a></h1>
<h1 class="code-line" data-line-start="29" data-line-end="30"><a id="_29"></a></h1>
<h1 class="code-line" data-line-start="30" data-line-end="31"><a id="_30"></a></h1>
<h1 class="code-line" data-line-start="31" data-line-end="32"><a id="_31"></a></h1>
<h6 class="code-line" data-line-start="33" data-line-end="34"><a id="Vector_Structure_33"></a>Vector Structure</h6>
<hr>
<h2 class="code-line" data-line-start="35" data-line-end="36"><a id="Gathering_and_Evaluating_Data_35"></a>Gathering and Evaluating Data</h2>
<h5 class="code-line" data-line-start="37" data-line-end="38"><a id="Creating_Training_and_Testing_Data_37"></a>Creating Training and Testing Data</h5>
<p class="has-line-data" data-line-start="39" data-line-end="40">Three types of monosyllabic words were used as training and testing data.</p>
<ul>
<li class="has-line-data" data-line-start="41" data-line-end="42">Valid Words: English words sourced from the Oxford English Dictionary.</li>
<li class="has-line-data" data-line-start="42" data-line-end="43">Nonce Words: Words that could be words of English, but aren’t. These were created by combining valid English onsets, nuclei, and codas in ways that did not result in actual words of English. For example, ‘scr’ is a valid English onset, ‘au’ is a valid English nucleus, and ‘shed’ is a valid English coda, but ‘scraushed’ is not a word of English. Valid English syllable constiuants were sourced from Hammond (1999).</li>
<li class="has-line-data" data-line-start="43" data-line-end="45">Invalid Words: Words that could not be words of English. These were created by combining two valid English syllable consituents with one invalid English syllable consituent. For example, ‘str’ is a valid English onset, ‘i’ is a valid English nucleus, but ‘brg’ is an invalid English coda, resulting in the invalid word ‘stribrg’.</li>
</ul>
<p class="has-line-data" data-line-start="45" data-line-end="46">To elimate possible biases, generated words that were valid German or French words, or were common proper nouns were rejected.</p>
<p class="has-line-data" data-line-start="47" data-line-end="48">A total of 1,080 word were generated (360 from each category). 864 words were used as training data (288 from each category) and 216 words were used as testing data (72 from each category).</p>
<h5 class="code-line" data-line-start="49" data-line-end="50"><a id="Data_Annotation_49"></a>Data Annotation</h5>
<p class="has-line-data" data-line-start="50" data-line-end="51">The 1,080 generated words were divided into three data sets, with each data set containing 120 words from each category in random order. Each data set was given to X annotators. The annotators were asked to rate each word on the following 3-point scale.</p>
<p class="has-line-data" data-line-start="52" data-line-end="55">1: This word does not look like English: reject<br>
3: This word sort of looks like English: moderately accept<br>
5: This word looks like English: accept</p>
<p class="has-line-data" data-line-start="56" data-line-end="57">Final scores for each word were found by averaging the X ratings.</p>
<hr>
<h2 class="code-line" data-line-start="60" data-line-end="61"><a id="Results_60"></a>Results</h2>
<p class="has-line-data" data-line-start="62" data-line-end="63">To evauate which model best matched the annatator scores, annatotar scores of the testing data were corrolated with model scores of the testing data. The correlation coeficiants are as follows.</p>
<p class="has-line-data" data-line-start="64" data-line-end="67">Trigram Model:<br>
Neighborhood Model:<br>
Linear Regression Model</p>
<p class="has-line-data" data-line-start="68" data-line-end="69">Based on these corrlation coefiicnat, the X model best approximade human jugments of word accptability.</p>
<hr>
<h2 class="code-line" data-line-start="71" data-line-end="72"><a id="Discussion_71"></a>Discussion</h2>
<hr>
<hr>
<h1 class="code-line" data-line-start="76" data-line-end="77"><a id="How_to_Run_the_Program_76"></a>How to Run the Program</h1>
<h4 class="code-line" data-line-start="78" data-line-end="79"><a id="Required_Modules_78"></a>Required Modules</h4>
<table class="table table-striped table-bordered">
<thead>
<tr>
<th>Module</th>
<th>Link</th>
</tr>
</thead>
<tbody>
<tr>
<td>panphon</td>
<td><a href="https://pypi.org/project/panphon/0.5/">https://pypi.org/project/panphon/0.5/</a></td>
</tr>
<tr>
<td>epitran</td>
<td><a href="https://pypi.org/project/epitran/0.22/">https://pypi.org/project/epitran/0.22/</a></td>
</tr>
<tr>
<td>pyenchant</td>
<td><a href="https://pypi.org/project/pyenchant/">https://pypi.org/project/pyenchant/</a></td>
</tr>
<tr>
<td>scikit-learn</td>
<td><a href="https://pypi.org/project/scikit-learn/">https://pypi.org/project/scikit-learn/</a></td>
</tr>
<tr>
<td>numpy</td>
<td><a href="https://pypi.org/project/numpy/">https://pypi.org/project/numpy/</a></td>
</tr>
</tbody>
</table>
<hr>
<h1 class="code-line" data-line-start="88" data-line-end="89"><a id="References_88"></a>References</h1>
<p class="has-line-data" data-line-start="90" data-line-end="92">Bailey, T. and Hahn, U. (2001). Determinants of wordlikeness: Phonotactics or<br>
lexical neighborhoods? Journal of Memory and Language, 44:568–591.</p>
<p class="has-line-data" data-line-start="94" data-line-end="96">Chomsky, N. and Halle, M. (1965). Some controversial questions in phonological<br>
theory. Journal of Linguistics, 1(2):97–138.</p>
<p class="has-line-data" data-line-start="97" data-line-end="99">Hammond, M. (1999). The Phonology of English, chapter Chapter 3. English Sylla-<br>
bles: Margins and Consonants. Oxford University Press.</p>
<p class="has-line-data" data-line-start="100" data-line-end="102">Hammond, M. (2004). Gradience, phonotactics and the lexicon in english phonology.<br>
International Journal of English Studies (IJES), 4.</p>
<p class="has-line-data" data-line-start="103" data-line-end="104">Jurafsky and Martin (2023). Speech and Language Processing, chapter 3. 3rd edition.</p>
<p class="has-line-data" data-line-start="105" data-line-end="108">Özkan, K. (2014). Using corpus statistics to evaluate nonce words. In Pristine Per-<br>
spectives on Logic, Language, and Computation. ESSLLI ESSLLI 2013 2012, pages<br>
26–35, Berlin, Heidelberg.</p>
<h3 class="code-line" data-line-start="109" data-line-end="110"><a id="Corpora_109"></a>Corpora</h3>
<table class="table table-striped table-bordered">
<thead>
<tr>
<th>Title</th>
<th>Link</th>
</tr>
</thead>
<tbody>
<tr>
<td>Brown Corpus</td>
<td><a href="http://www.sls.hawaii.edu/bley-vroman/brown_corpus.html">http://www.sls.hawaii.edu/bley-vroman/brown_corpus.html</a></td>
</tr>
<tr>
<td>Oxford English Dictionary</td>
<td><a href="https://github.com/sujithps/Dictionary/blob/master/Oxford%20English%20Dictionary.txt">https://github.com/sujithps/Dictionary/blob/master/Oxford%20English%20Dictionary.txt</a></td>
</tr>
<tr>
<td>Common Male Names</td>
<td><a href="https://www.cs.cmu.edu/Groups/AI/areas/nlp/corpora/names/male.txt">https://www.cs.cmu.edu/Groups/AI/areas/nlp/corpora/names/male.txt</a></td>
</tr>
<tr>
<td>Common Female Names</td>
<td><a href="https://www.cs.cmu.edu/Groups/AI/areas/nlp/corpora/names/female.txt">https://www.cs.cmu.edu/Groups/AI/areas/nlp/corpora/names/female.txt</a></td>
</tr>
</tbody>
</table>
<pre><code class="has-line-data" data-line-start="121" data-line-end="123" class="language-sh"><span class="hljs-number">127.0</span>.<span class="hljs-number">0.1</span>:<span class="hljs-number">8000</span>
</code></pre>
</body></html>