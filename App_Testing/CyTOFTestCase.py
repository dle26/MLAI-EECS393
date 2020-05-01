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
import warnings
warnings.filterwarnings("ignore")
import itertools


def separate_bigrams(lst):
    
    lst2 = []
    for tup in lst:
        if len(tup[0].split()) > 1:
            if (tup[0],"") not in lst2:
                lst2.append((tup[0],""))
            if len(tup[1].split()) > 1:
                if (tup[1],"") not in lst2:
                    lst2.append((tup[1],""))
                continue
            continue
        lst2.append(tup)
    
    return lst2



time = datetime.now()


''' DATA PREPARATION/SIMULATION OF FRONT END PROCESSES '''

### Clinical scores
raw_data = pd.read_csv('cytof_xmen.csv')
train_data = raw_data[[col for col in raw_data if col != 'Labels']]
cols = list(train_data.columns)

train_data = train_data.values
str_labels = raw_data['Labels'].values

labels = []
for n,l in enumerate(list(set(str_labels))):
    for ll in str_labels:
        if ll == l:
            labels.append(n)

description = "This dataset contains surface antibody expression values from phenotypes obtained by mass cytometry analysis of samples containing human T-cells"

bigram = False

dp = DATAPREP(None,None,None,None,None,None,None)
search_words = dp.process_user_info(description,True)
dp.data.search_queries = dp.process_user_info(description,False)
dp.data.data = train_data
dp.data.data_type = 'numeric'
dp.data.analysis_type = 'unsupervised'
dp.data.labels = None #labels
dp.data.time_constraint = 2
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

