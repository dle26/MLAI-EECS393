# AbstractAwk

Developed by James Anibal (james.anibal@case.edu)

# Introduction and Purpose
We aim to provide a more efficient approach to jounral article searches searches by developing AbstractAwk, a straightforward command line tool that will run on any Ubuntu or Mac OS. 

# Sed
Sed commands are then used to clean and format the file for mining (i.e. remove punctuation, special characters, tabs)

# Stopwords
We use a large corpus (credit: Google's NLP research) to eliminate common words, verbs, and adverbs. The objective of AbstractAwk is to provide searchable terms, and verbs/adverbs do not typically qualify. We also use a large corpus of Spanish words to limit our results to the English language.

# Awk 
Once the text data has been formatted, word+bigram frequencies are obtained (exluding stopwords and the actual query) using awk. AbstractAwk does not consider absolute frequencies, but instead sums the result of (max(0,1) per n lines). This allows AbstractAwk to find keywords+bigrams that are used across many projects, rather than keywords that are simply used repetitively in a small number of projects. If there are duplicate papers, the score will (and should) reflect this: papers that are included in related paper searches are more signficant, as are the keywords contained within. AbstractAwk then removes a percentage of the most frequent remaining words on the assumption these will be relatively generic scientific words not included in the stopwords corpus. The final set of keywords+bigrams is sorted by score and displayed via html (improved cgi in progress).
