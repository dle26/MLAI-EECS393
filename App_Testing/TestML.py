#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 00:48:44 2020

@author: anibaljt
"""


import MLTechniques

import pytest 
from sklearn.datasets import make_classification
from ml_backend.Prep import DATA

def testmltechniques():
    
    ### toy data
    X, y = make_classification(n_samples=30, n_features=4,
                              n_informative=2, n_redundant=0,
                            random_state=0, shuffle=False)
    
    data = DATA()
    data.data = X
    data.data_type = 'numeric'
    data.labels = y
    data.analysis_type = 'supervised'
    data.prior_test_data = None
    
    ### FOR ALL TIME CONSTRAINTS
    for i in range(1,3):
    
        data.time_constraint = i
    
        test_data,test_labels,results,fi, blind_results = MLTechniques.RandomForest.train(data)
        assert (True == (test_data is not None and test_labels is not None and results is not None and fi is not None and blind_results is None)),"Algorithm error"
        
        test_data,test_labels,results,fi, blind_results = MLTechniques.DecisionTree.train(data)
        assert (True == (test_data is not None and test_labels is not None and results is not None and fi is not None and blind_results is None)),"Algorithm error"

        test_data,test_labels,results,fi, blind_results = MLTechniques.SVM.train(data)
        assert (True == (test_data is not None and test_labels is not None and results is not None and fi is None and blind_results is None)),"Algorithm error"
    
        test_data,test_labels,results,fi, blind_results = MLTechniques.KNN.train(data)
        assert (True == (test_data is not None and test_labels is not None and results is not None and fi is None and blind_results is None)),"Algorithm error"
        
        test_data,test_labels,results,fi, blind_results = MLTechniques.NaiveBayes.train(data)
        assert (True == (test_data is not None and test_labels is not None and results is not None and fi is None and blind_results is None)),"Algorithm error"       

        if i > 1:
          test_data,test_labels,results,fi, blind_results = MLTechniques.VGG_CNN.train(data)
          assert (True == (test_data is not None and test_labels is not None and results is not None and fi is None and blind_results is None)),"Algorithm error"
        
        if i > 1:
          test_data,test_labels,results,fi, blind_results = MLTechniques.MLP.train(data)
          assert (True == (test_data is not None and test_labels is not None and results is not None and fi is None and blind_results is None)),"Algorithm error"
        
        test_data,test_labels,results,fi, blind_results = MLTechniques.GradientBoost.train(data)
        assert (True == (test_data is not None and test_labels is not None and results is not None and fi is not None and blind_results is None)),"Algorithm error"
    
    

    data.labels = None
    data.analysis_type = 'unsupervised'
    
    for i in range(1,3):
        
        data.time_constraint = i
        
        test_data,test_labels,results,fi, blind_results = MLTechniques.KMeans.train(data)
        assert (True == (test_data is not None and results is not None)),"Algorithm error"
        
        test_data,test_labels,results,fi, blind_results = MLTechniques.HAC.train(data)
        assert (True == (test_data is not None and results is not None)),"Algorithm error"
        
        test_data,test_labels,results,fi, blind_results = MLTechniques.MeanShift.train(data)
        assert (True == (test_data is not None and results is not None)),"Algorithm error"
        
