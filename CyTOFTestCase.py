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
from ml_backend.Prep import DATAPREP,DATA
from datetime import datetime
from ml_backend.SelectionAgent import SELECT
from ml_backend.AnalysisAgent import ANALYZE
from ml_backend.Interpret import INTERPRET
import os
import MLTechniques
import pickle



time = datetime.now()


''' DATA PREPARATION/SIMULATION OF FRONT END PROCESSES '''

### Clinical scores
raw_data = pd.read_csv('cytof.csv')
train_data = raw_data[[col for col in raw_data if col != 'labels']]
cols = list(train_data.columns)

train_data = train_data.values
labels = raw_data['labels'].values

description = "This dataset contains surface antibody expression values from phenotypes obtained by mass cytometry analysis of samples containing human T-cells"
words =  word_tokenize(description) 
words = [word.lower() for word in words if word not in string.punctuation or word == '.']
tagged_words = nltk.pos_tag(words)

#### this is simulating the user input function
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
dp.data.data_type = 'numeric'
dp.data.analysis_type = 'supervised'
dp.data.labels = labels
dp.data.time_constraint = 1
dp.data.descriptive_info = search_words
dp.data.userinfo = "jta54"

newdata = dp.eval_data()
newdata.original_features = cols


''' TEST FOR DATA PROCESSING'''

def test_preparation():
    
    assert (True == (('antibody expression', '') in newdata.descriptive_info)),"Structural Eval. Failed"
    assert (True == (newdata.eval_score is not None and newdata.eval_score > 0.5 and newdata.eval_score < 1.01)),"Data Scoring Failed"



''' TESTS FOR SELECTION FRAMEWORK '''

newdata = SELECT(newdata).selectAnalysisApproach()

print(newdata.techniques[0])

def test_select():
    
    assert (True == ('RandomForest' in newdata.techniques)),"Selection Failed"
    assert (True == os.path.exists("MODEL.pkl")),"Scoring System not initialized"



''' TESTS FOR ANALYSIS FRAMEWORK '''

newdata = ANALYZE(newdata).train_approaches()

def test_analysis():

    assert (True == (newdata.prediction_results is not None)),"Prediction was not completed"
    if newdata.techniques[-1] == "RandomForest":
        assert(True == (newdata.feature_importances[0] is not None)),"Invalid Feature Importances"
    else:
        assert(True == (newdata.feature_importances[0] is None)),"Invalid Feature Importances"


newdata = INTERPRET(newdata,0.75).interpret()
print(newdata.interpreted_results)
#print(newdata.interpreted_results['DECISIONTREE']['Accuracy'] > 0.75)

def test_interpretation():
    if newdata.techniques[-1] == "RandomForest":
        key = "RandomForest"
    else: key = "SVM"
    assert(True == (['samples', 'results','Feature Importances','Accuracy','F1 Score','Confusion Matrix'] == list(newdata.interpreted_results[key].keys()))),"Intepretation Incomplete"
    assert(True == (newdata.interpreted_results[key]['Accuracy'] > 0)),"Model performance Failed"

