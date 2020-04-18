#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: anibaljt

"""




from .Technique import Technique
from sklearn.neighbors import KNeighborsClassifier as KNC
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler


class KNN(Technique):
    
    GENERAL_USE = True
    
    TECHNIQUE_TYPE = "supervised"
    
        
    def get_website():
        return 'https://scikit-learn.org/stable/modules/neighbors.html#classification'
    
    def get_class_name():
        return 'KNN'
    
    def get_name():
        return 'knn'

    def get_category():
        return 'nearest neighbours'
        
    
    def preprocess(data):
        
        if data.data_type == 'image':
            features = StandardScaler().fit_transform(data.data)
            return features
        
        if data.data_type == 'numeric':
            features = StandardScaler().fit_transform(data.data)
            return features

        
        if data.data_type == 'text':
            pass
        
        return -1 
        
    
    def train(data):
 
        X = KNN.preprocess(data)
        y = np.asarray(data.labels)
        test_labels = []
        test_data = []
        time_constraint = data.time_constraint
        
        if time_constraint == 1:
            
            model = KNC()
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
            model.fit(X_train,y_train)
            results = model.predict(X_test)
            test_data = X_test
            test_labels = y_test

        if time_constraint == 2:
            
            for i in range(2):
                model = KNC()
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
                model.fit(X_train,y_train)
                results = model.predict(X_test)
                test_data.extend(X_test)
                test_labels.extend(y_test)
                
        if time_constraint == 3:
            
            model = KNC()
            results = []
            cv = StratifiedKFold(n_splits=5,shuffle=True)
            for train, test in cv.split(X,y):
                 model.fit(X[train],y[train])
                 results.extend(model.predict(X[test]))
                 test_data.extend(X[test])
                 test_labels.extend(y[test])
                 
            
        if time_constraint == 4:
            model = KNC()
            parameters = {'n_neighbors':(5,6,7,8,9), 'algorithm':['ball_tree','kd_tree']}
            clf = GridSearchCV(model, parameters)
            cv = StratifiedKFold(n_splits=5,shuffle=True)
            
            for train, test in cv.split(X,y):
                 clf.fit(X[train],y[train])
                 results.extend(clf.predict(X[test]))
                 test_labels.extend(y[test])
                 test_data.extend(X[test])
                 
        if time_constraint == 5:
            
            model = KNC()
            parameters = {'n_neighbors':(2,3,4,5,6,7,8,9,10,11,12), 'algorithm':['ball_tree','kd_tree','brute','auto'],
                          'p':(1,2)}
            clf = GridSearchCV(model, parameters)
            
            cv = StratifiedKFold(n_splits=5,shuffle=True)
            for train, test in cv.split(X,y):
                 clf.fit(X[train],y[train])
                 results.extend(clf.predict(X[test]))
                 test_labels.extend(y[test])
                 test_data.extend(X[test])
                 
        
        return test_data,test_labels,results,None
    
    
