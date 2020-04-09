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
     
  
    GENERAL_USE = True
    TECHNIQUE_TYPE = "supervised"
    
    def __init__(self):
        self.model = None
 
    
    def get_class_name():
        return 'SVM'
    
    def get_name():
        return 'support vector machine'

    def get_category():
        return 'support vector machine'
        
    def preprocess(self,data):
        
        if data.type == 'image':
            features = StandardScaler().fit_transform(data.data)
            return features
        
        if data.type == 'numeric':
            pass
        
        if data.type == 'text':
            pass
        
        return -1 
        
    
    def train(self,data,time_constraint):
 
        X = self.preprocess(data)
        y = np.asarray(data.labels)
       
        
        if time_constraint == 1:
            model = SVC(gamma = 'auto')
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
            model.fit(X_train,y_train)
            results = model.predict(X_test)
            data.test_labels = y_test
            k = 0
            for n,ii in enumerate(y_test):
                if ii == results[n]:
                    k += 1


        if time_constraint == 2:
            
            for i in range(time_constraint):
                model = SVC(gamma = 'auto')
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
                model.fit(X_train,y_train)
                results = model.predict(X_test)
                data.test_labels = y_test
                
        if time_constraint == 3:
            
            model = SVC(gamma = 'auto')
            results = []
            cv = StratifiedKFold(n_splits=5,shuffle=True)
            for train, test in cv.split(X,y):
                 model.fit(X[train],y[train])
                 results.extend(model.predict(X[test]))
                 data.test_labels.extend(y[test])
                 
            
        if time_constraint == 4:
            model = SVC(gamma = 'auto')
            parameters = {'kernel':('linear', 'rbf'), 'C':[1/len(X),1, 10]}
            clf = GridSearchCV(model, parameters)
            gcv = clf.fit(X[train], X[test])
            results.extend(gcv.predict(X[test]))
            data.test_labels.extend(y[test])
            model = gcv.estimator

        if time_constraint == 5:
            
            model = SVC()
            parameters = {'kernel':('linear','rbf','poly','sigmoid'), 'C':[1/len(X),0.1,0.5,1,5,10],
                          'gamma':('auto','scale')}
            
            clf = GridSearchCV(model, parameters)
            gcv = clf.fit(X[train], X[test])
            results.extend(gcv.predict(X[test]))
            data.test_labels.extend(y[test])
            model = gcv.estimator
        
        self.model = model
        data.prediction_results.append((results,SVM.get_name()))
        data.current_models.append((self,SVM.get_name()))
        data.feature_importances.append((None,SVM.get_name()))
        print()
  
        return data
    
    
    def set_model(self,model):
        self.model = model
    
    
    def get_model(self):
        return self.model
    


