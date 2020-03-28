#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Created on Mon Mar 23 17:54:04 2020

@author: anibaljt
"""


## testing script in PYTEST

import pytest
import pandas as pd
import nltk
import string
from nltk.tokenize import word_tokenize
from Data import DATA



raw_data = pd.read_csv('training.csv')
train_data = raw_data[[col for col in raw_data if col != 'label']].values

labels = raw_data['label'].values

time_constraint = 1

description = "This dataset contains 21,000 images corresponding to handwritten digits. These digits range from zero to nine."

words =  word_tokenize(description) 

words = [word.lower() for word in words if word not in string.punctuation or word == '.']

tagged_words = nltk.pos_tag(words)

search_words = []
for n,word in enumerate(tagged_words[0:len(tagged_words)-1]):
    if word[1][0] == 'N' and tagged_words[n+1][1][0] == 'N':
            search_words.append(word[0] + " " + tagged_words[n+1][0])


#data = DATA(train_data,labels,time_constraint=1,user_input = search_words)


### testing my pytest installation on MacOS
            
def test_file1_method1():
	x=5
	y=6
	assert x+1 == y,"test failed"
	assert x == y,"test failed"
               