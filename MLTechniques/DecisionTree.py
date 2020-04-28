#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 23:58:28 2020

@author: anibaljt
"""


from .Technique import Technique
from sklearn.tree import DecisionTreeClassifier
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import RobustScaler


class DecisionTree(Technique):
    
    ISDEEP = False
    
    TECHNIQUE_TYPE = "supervised"
    
    
    def get_website():
        return 'https://scikit-learn.org/stable/modules/tree.html#tree'
    
    def get_class_name():
        return 'DecisionTree'
    
    def get_name():
        return 'decision tree'

    def get_category():
        return 'decision tree'
        
  
    def preprocess(data):
        return data.data,data.prior_test_data

        
    def train(data):
 
        X,Xtest= DecisionTree.preprocess(data)
        y = np.asarray(data.labels)
        test_labels = []
        test_data = []
        time_constraint = data.time_constraint
        blind_results = None
        results = []
        
        if data.prior_test_data is not None:
            model = DecisionTreeClassifier()
            model.fit(X,y)
            blind_results = model.predict(Xtest)
            
        if time_constraint == 1:
            
            model = DecisionTreeClassifier()
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
            model.fit(X_train,y_train)
            results = model.predict(X_test)
            test_data = X_test
            test_labels = y_test
            feature_importances = list(model.feature_importances_)
            print(list(model.feature_importances_))

        if time_constraint == 2:
            
            model = DecisionTreeClassifier()
            
            for i in range(2):
                model = DecisionTreeClassifier()
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
                model.fit(X_train,y_train)
                results.extend(model.predict(X_test))
                test_data.extend(X_test)
                test_labels.extend(y_test)
            feature_importances = list(model.feature_importances_)
                
        if time_constraint == 3:
            
            model = DecisionTreeClassifier()
            results = []
            cv = StratifiedKFold(n_splits=5,shuffle=True)
            for train, test in cv.split(X,y):
                 model.fit(X[train],y[train])
                 results.extend(model.predict(X[test]))
                 test_data.extend(X[test])
                 test_labels.extend(y[test])
            feature_importances = list(model.feature_importances_)
                 
            
        if time_constraint == 4:
            model = DecisionTreeClassifier()
            parameters = {'criterion':('gini', 'entropy'), 'splitter': ('best','random')}
            clf = GridSearchCV(model, parameters)
            cv = StratifiedKFold(n_splits=5,shuffle=True)
            results = []
            for train, test in cv.split(X,y):
                 clf.fit(X[train],y[train])
                 results.extend(clf.predict(X[test]))
                 test_labels.extend(y[test])
                 test_data.extend(X[test])
            feature_importances = list(clf.best_estimator_.feature_importances_)
                 
        if time_constraint == 5:
            
            model = DecisionTreeClassifier(n_estimators=50)
            parameters = {'criterion':('gini', 'entropy'), 'splitter': ('best','random'),
                          'max_features':('auto','log2','sqrt')}
            clf = GridSearchCV(model, parameters)
            results = []
            cv = StratifiedKFold(n_splits=5,shuffle=True)
            for train, test in cv.split(X,y):
                 clf.fit(X[train],y[train])
                 results.extend(clf.predict(X[test]))
                 test_labels.extend(y[test])
                 test_data.extend(X[test])
            feature_importances = list(clf.best_estimator_.feature_importances_)
                 
        
        return test_data,test_labels,results,feature_importances,blind_results
