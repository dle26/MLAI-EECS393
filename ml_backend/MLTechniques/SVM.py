#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: anibaljt

Implementation for SkLearn's SVC class

"""

from Technique import Technique 
from sklearn.svm import SVC
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold


class SVM(Technique):
    
  
    custom = False
    
    def __init__(self):
        self.model = None
 

    def get_name():
        return 'SVM'

    def train(self,data,time_constraint):
 
        X = np.asarray(data.preprocessed_data) 
        y = np.asarray(data.labels)
        model = SVC()
        
        if time_constraint == 1:

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
            model.fit(X_train,y_train)
            results = model.predict(X_test)

        if time_constraint == 2:
            
            for i in range(time_constraint):
                
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
                model.fit(X_train,y_train)
                results = model.predict(X_test)
                
        if time_constraint == 0 or time_constraint == 3:
            
            cv = StratifiedKFold(n_splits=5,shuffle=True)
            
            for train, test in cv.split(X,y):
                 model.fit(X[train],y[train])
                 results = model.predict(X[test])
            
        if time_constraint == 4:
            parameters = {'kernel':('linear', 'rbf'), 'C':[1/len(X),1, 10]}
            clf = GridSearchCV(model, parameters)
            gcv = clf.fit(X[train], X[test])
            results = gcv.predict(X[test])
            model = gcv.estimator

        if time_constraint == 5:
            
            parameters = {'kernel':('linear','rbf','poly','sigmoid'), 'C':[1/len(X),0.1,0.5,1,5,10],
                          'gamma':('auto','scale')}
            
            clf = GridSearchCV(model, parameters)
            gcv = clf.fit(X[train], X[test])
            results = gcv.predict(X[test])
            model = gcv.estimator
            
        data.prediction_results = (results,SVM.get_name())
        data.current_models.extend((self,SVM.get_name()))
        data.feat_importances.extend((None,SVM.get_name()))
  
        return data
    
    
    
    def predict(self,data,labels,model):
        
        results = model.predict(data.preprocessed_data)
        data.set_results(results)
        
        return data
    
    
    def set_model(self,model):
        self.model = model
    
    
    def get_model(self):
        return self.model
    

    