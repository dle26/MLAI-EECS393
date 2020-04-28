#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 23:40:12 2020

@author: anibaljt
"""


from .Technique import Technique
from sklearn.naive_bayes import GaussianNB as GNB 
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler


class NaiveBayes(Technique):
    
    TECHNIQUE_TYPE = "supervised"
    ISDEEP = False
    
    def get_name():
        return 'naive bayes'

    def get_category():
        return 'bayes'
    
    
    def get_website():
        return 'https://scikit-learn.org/stable/modules/svm.html#classification'
    
    
    def get_class_name():
        return 'NaiveBayes'
    
    
    def preprocess(data):
        
        if data.data_type == 'image':
            features = StandardScaler().fit_transform(data.data)
            if data.prior_test_data is not None:
                test_features = StandardScaler().fit_transform(data.data)
                return features,test_features
            return features,None
        
        if data.data_type == 'numeric':
            features = StandardScaler().fit_transform(data.data)
            if data.prior_test_data is not None:
                test_features = StandardScaler().fit_transform(data.data)
                return features,test_features
            return features,None

    
    def train(data):
 
        X,Xtest = NaiveBayes.preprocess(data)
        y = np.asarray(data.labels)
        test_labels = []
        test_data = []
        time_constraint = data.time_constraint
        results = []
        
        blind_results = None
        
        if data.prior_test_data is not None:
            model = GNB()
            model.fit(X,y)
            blind_results = model.predict(Xtest)
        
        
        if time_constraint == 1:
            
            model = GNB()
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
            model.fit(X_train,y_train)
            results = model.predict(X_test)
            test_data = X_test
            test_labels = y_test

        if time_constraint == 2:
            
            for i in range(2):
                model = GNB()
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
                model.fit(X_train,y_train)
                results.extend(model.predict(X_test))
                test_data.extend(X_test)
                test_labels.extend(y_test)
                
        if time_constraint > 2:
            
            model = GNB()
            results = []
            cv = StratifiedKFold(n_splits=5,shuffle=True)
            for train, test in cv.split(X,y):
                 model.fit(X[train],y[train])
                 results.extend(model.predict(X[test]))
                 test_data.extend(X[test])
                 test_labels.extend(y[test])
                 
        return test_data,test_labels,results,None,blind_results
    
    
