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
from Prep.DATAPREP import eval_data



raw_data = pd.read_csv('training.csv')
train_data = raw_data[[col for col in raw_data if col != 'label']].values

labels = raw_data['label'].values

description = "This dataset contains 21,000 images corresponding to handwritten digits. These digits range from zero to nine."

words =  word_tokenize(description) 

words = [word.lower() for word in words if word not in string.punctuation or word == '.']

tagged_words = nltk.pos_tag(words)

search_words = []
for n,word in enumerate(tagged_words):
    if word[1][0] == 'N':
        search_words.append(word[0])

data = DATA()
data.data = train_data
data.labels = labels
data.time_constraint = 1
data.add_descriptive_info = search_words


newdata = eval_data(data)
           
def test_eval():

    assert (True == ("multiclass images" in newdata.descriptive_info)),"Structural Eval. Failed"
    assert (True == (newdata.eval_score is not None and newdata.evalscore > 0.25 and newdata.evalscore < 1.1)),"Data Scoring Failed"
    

def test_textmining():
    pass
    
def test_selection():
    pass

def test_analysis():
    pass

def test_interpretation():
    pass

    
