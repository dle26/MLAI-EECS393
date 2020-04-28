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

raw_data = pd.read_csv('training.csv')
train_data = raw_data[[col for col in raw_data if col != 'label']].values
labels = raw_data['label'].values
description = "This dataset contains pitching statistics from the 2016 major league baseball season"

bigram = False

dp = DATAPREP(None,None,None,None,None,None,None)
search_words = dp.process_user_info(description,True)
dp.data.search_queries = dp.process_user_info(description,False)
dp.data.data = train_data
dp.data.data_type = 'image'
dp.data.analysis_type = 'supervised'
dp.data.dimensions = (28,28)
dp.data.labels = labels
dp.data.time_constraint = 2
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
