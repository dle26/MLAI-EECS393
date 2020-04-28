#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: anibaljt

Implementation for SkLearn's SVC class

"""

from .Technique import Technique
from sklearn.svm import SVC
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler


class SVM(Technique):
     
    TECHNIQUE_TYPE = "supervised"
    ISDEEP = False
    
    def get_website():
        return 'https://scikit-learn.org/stable/modules/svm.html#classification'
    
    def get_class_name():
        return 'SVM'
    
    def get_name():
        return 'svm'

    def get_category():
        return 'svm'
        
    def preprocess(data):
        
        if data.data_type == 'image':
            features = StandardScaler().fit_transform(data.data)
            if data.prior_test_data is not None:
                test_features = StandardScaler().fit_transform(data.prior_test_data)
                return features,test_features
            return features,None
        
        if data.data_type == 'numeric':
            features = StandardScaler().fit_transform(data.data)
            if data.prior_test_data is not None:
                test_features = StandardScaler().fit_transform(data.prior_test_data)
                return features,test_features
            return features,None
        
    
    def train(data):
 
        X,Xtest = SVM.preprocess(data)
        y = np.asarray(data.labels)
        test_labels = []
        test_data = []
        time_constraint = data.time_constraint
        blind_results = None
        results = []
        
        if data.prior_test_data is not None:
            model = SVC(gamma = 'auto')
            model.fit(X,y)
            blind_results = model.predict(Xtest)
 

        if time_constraint == 1:
            model = SVC(gamma = 'auto')
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
            model.fit(X_train,y_train)
            results = model.predict(X_test)
            test_data = X_test
            test_labels = y_test

        if time_constraint == 2:
            
            for i in range(2):
                model = SVC(gamma = 'auto')
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
                model.fit(X_train,y_train)
                results.extend(model.predict(X_test))
                test_data.extend(X_test)
                test_labels.extend(y_test)
                
        if time_constraint == 3:
            
            model = SVC(gamma = 'auto')
            results = []
            cv = StratifiedKFold(n_splits=5,shuffle=True)
            for train, test in cv.split(X,y):
                 model.fit(X[train],y[train])
                 results.extend(model.predict(X[test]))
                 test_data.extend(X[test])
                 test_labels.extend(y[test])
                 
            
        if time_constraint == 4:
            model = SVC(gamma = 'auto')
            parameters = {'kernel':('linear', 'rbf'), 'C':[1/len(X),1, 10]}
            clf = GridSearchCV(model, parameters)
            cv = StratifiedKFold(n_splits=5,shuffle=True)
            results = []
            
            for train, test in cv.split(X,y):
                 clf.fit(X[train],y[train])
                 results.extend(clf.predict(X[test]))
                 test_labels.extend(y[test])
                 test_data.extend(X[test])
                 
        if time_constraint == 5:
            
            model = SVC()
            parameters = {'kernel':('linear','rbf','poly','sigmoid'), 'C':[1/len(X),0.1,0.5,1,5,10],
                          'gamma':('auto','scale')}
            clf = GridSearchCV(model, parameters)
            results = []
            cv = StratifiedKFold(n_splits=5,shuffle=True)
            for train, test in cv.split(X,y):
                 clf.fit(X[train],y[train])
                 results.extend(clf.predict(X[test]))
                 test_labels.extend(y[test])
                 test_data.extend(X[test])
        
        
        if data.prior_test_data is not None:
            model.fit(X,y)
            blind_results = model.predict(Xtest)



        return test_data,test_labels,results,None, blind_results
