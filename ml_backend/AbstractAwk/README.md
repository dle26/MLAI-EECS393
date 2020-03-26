# EECS397-P2
Project 2 for EECS 397

James Anibal (james.anibal@case.edu) & Jinny Hong (jinny.hong@case.edu)

# Introduction and Purpose

PubMed is search engine that provides access to over 30 million abstracts spanning decades of health related research. For any student or researcher exploring the various approaches to a given research question, PubMed is the obvious choice. However, given the massive number of resources, it is an inefficient albeit valuable tool. For this project, we aimed to provide a more efficient approach to pubmed searches by developing AbstractAwk, a straightforward command line tool that will run on any Ubuntu or Mac OS. 

# User Inputs
AbstractAwk is ran from a bash script. The script first reads in user input about the topic and range of dates to be searched. Multiword scripts are handled with the "+" operator. 

Example queries:
coronavirus, hay+fever

AbstractAwk then queries the user for a range of dates to search (i.e. 2016-2020), the number of papers to search per year, and the number of related papers (per abstract) to include in the search. Including related papers adds to the depth of the search based on more specific keywords. 

# Lynx
AbstractAwk will then pull the selected number of abstracts (by year) + the selected number of related papers for each abstract by downloading webpage data from a PubMed URL relating to the query words. The data from these webpages is converted into a file for further analysis.

# Sed
Sed commands are then used to clean and format the file for mining (i.e. remove punctuation, special characters, tabs)

# Stopwords
We use a large corpus (credit: Google's NLP research) to eliminate common words, verbs, and adverbs. The objective of AbstractAwk is to provide searchable terms, and verbs/adverbs do not typically qualify. We also use a large corpus of Spanish words to limit our results to the English language.

# Awk 
Once the text data has been formatted, word+bigram frequencies are obtained (exluding stopwords and the actual query) using awk. AbstractAwk does not consider absolute frequencies, but instead sums the result of (max(0,1) per n lines). This allows AbstractAwk to find keywords+bigrams that are used across many projects, rather than keywords that are simply used repetitively in a small number of projects. If there are duplicate papers, the score will (and should) reflect this: papers that are included in related paper searches are more signficant, as are the keywords contained within. AbstractAwk then removes a percentage of the most frequent remaining words on the assumption these will be relatively generic scientific words not included in the stopwords corpus. The final set of keywords+bigrams is sorted by score and displayed via html (improved cgi in progress).

# Conclusions
Overall, AbstractAwk returns a sizeable number of useful terms in <10 minutes for ~10000 abstracts. This allows AbstractAwk to serve as a convenient project guide, particulalry for students. However, the tool does not perfectly filter all irrelevant words, leaving room for signifcant future development (to be explored in Project 3). 
