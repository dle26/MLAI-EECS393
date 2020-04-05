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
from Prep import DATAPREP,DATA
from datetime import datetime
from SelectionAgent import SELECT

import pickle

time = datetime.now()

raw_data = pd.read_csv('training.csv')
train_data = raw_data[[col for col in raw_data if col != 'label']].values

labels = raw_data['label'].values

description = "This dataset contains 21,000 images corresponding to handwritten digits. These digits range from zero to nine."

words =  word_tokenize(description) 

words = [word.lower() for word in words if word not in string.punctuation or word == '.']

tagged_words = nltk.pos_tag(words)

search_words = []
for n,word in enumerate(tagged_words[0:len(tagged_words)-1]):
    
    if (word[1][0] == 'N' and tagged_words[n+1][1][0] == 'J') or (word[1][0] == 'N' and tagged_words[n+1][1][0] == 'N'):
        search_words.append(word[0] + " " + tagged_words[n+1][1][0])

    elif (word[1][0] == 'N'):
        search_words.append(word[0])
        

data = DATA()
data.data = train_data
data.labels = labels
data.time_constraint = 1
data.descriptive_info = search_words


newdata = DATAPREP(data).eval_data()

userid = 'JTA001'

print(newdata.descriptive_info)


newdata = pickle.load(open('nd.pkl','rb'))
newdata2 = SELECT(newdata,"JTA001").selectAnalysisApproach(1)
print(newdata2.techniques)
print('Prep Time: ' + str(datetime.now()-time))


def test_eval():

    assert (True == (('multiclass', 'images') in newdata.descriptive_info) or ('images', 'multiclass') in newdata.descriptive_info),"Structural Eval. Failed"
    assert (True == (newdata.eval_score is not None and newdata.eval_score > 0.25 and newdata.eval_score < 1.1)),"Data Scoring Failed"

def test_select():
    pass

def test_analysis():
    pass

def test_predictions():
    pass

def test_interpretation():
    pass

def test_results():
    pass
 
