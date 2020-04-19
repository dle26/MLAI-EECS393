#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
@author: anibaljt
"""


## testing script in PYTEST

import pytest
import pandas as pd
import nltk
import string
from nltk.tokenize import word_tokenize
import ml_backend
from ml_backend.Prep import DATAPREP,DATA
from datetime import datetime
from ml_backend.SelectionAgent import SELECT
from ml_backend.AnalysisAgent import ANALYZE
from ml_backend.Interpret import INTERPRET
import os
import MLTechniques



time = datetime.now()


''' DATA PREPARATION/SIMULATION OF FRONT END PROCESSES '''

raw_data = pd.read_csv('training.csv')
train_data = raw_data[[col for col in raw_data if col != 'label']].values
labels = raw_data['label'].values
description = "This dataset contains 21,000 images corresponding to handwritten digits. These digits range from zero to nine."
words =  word_tokenize(description) 
words = [word.lower() for word in words if word not in string.punctuation or word == '.']
tagged_words = nltk.pos_tag(words)


search_words = []
print(tagged_words)
for n,word in enumerate(tagged_words):
    
    if n < len(tagged_words)-1:
        if (word[1][0] == 'N' and tagged_words[n+1][1][0] == 'J') or (word[1][0] == 'J' and tagged_words[n+1][1][0] == 'N') or (word[1][0] == 'N' and tagged_words[n+1][1][0] == 'N'):
            if word[0] + " " + tagged_words[n+1][0] not in search_words:
                search_words.append(word[0] + " " + tagged_words[n+1][0])


    if (word[1][0] == 'N') and word[0].find('data') == -1:
        if str(search_words).find(word[0]) == -1:
            search_words.append(word[0])


print(search_words)

bigram = False

dp = DATAPREP(None,None,None,None,None,None,None)
dp.data.data = train_data
dp.data.data_type = 'image'
dp.data.analysis_type = 'supervised'
dp.data.dimensions = (28,28)
dp.data.labels = labels
dp.data.time_constraint = 1
dp.data.descriptive_info = search_words
dp.data.userinfo = "jta54"
newdata = dp.eval_data()


''' TEST FOR DATA PROCESSING'''

def test_preparation():
    
    assert (True == ('images' in newdata.descriptive_info[0])),"Structural Eval. Failed"
    assert (True == (newdata.eval_score is not None and newdata.eval_score > 0.5 and newdata.eval_score < 1.01)),"Data Scoring Failed"

     

''' TESTS FOR SELECTION FRAMEWORK '''

newdata = SELECT(newdata).selectAnalysisApproach()


def test_select():
    
    assert (True == ('VGG_CNN' in newdata.techniques)),"Selection Failed"
    assert (True == os.path.exists("MODEL.pkl")),"Scoring System not initialized"

    

''' TESTS FOR ANALYSIS FRAMEWORK '''

newdata = ANALYZE(newdata).train_approaches()

def test_analysis():

    assert (True == (newdata.prediction_results is not None)),"Prediction was not completed"
    assert(True == (newdata.feature_importances[0] is None)),"Invalid Feature Importances"

newdata = INTERPRET(newdata,0.75).interpret()

print(newdata.interpreted_results)

def test_interpretation():
    
    assert(True == (['samples','results','Feature Importances','Accuracy','F1 Score','Confusion Matrix'] == list(newdata.interpreted_results['SVM'].keys()))),"Intepretation Incomplete"
    assert(True == (newdata.interpreted_results['SVM']['F1 Score'] > 0.75)),"Model performance Failed"
