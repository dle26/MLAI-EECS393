#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""


@author: anibaljt
"""

from .Technique import Technique
from sklearn.ensemble import GradientBoostingClassifier
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler


class GradientBoost(Technique):
     
  
    ISDEEP = False
    TECHNIQUE_TYPE = "supervised"
    
    def get_website():
        return 'https://scikit-learn.org/stable/modules/ensemble.html#gradient-boosting'
    
    def get_class_name():
        return 'GradientBoost'
    
    def get_name():
        return 'gradient boosting classifier'

    def get_category():
        return 'gradient boost'
        
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
 
        X,Xtest = GradientBoost.preprocess(data)
        y = np.asarray(data.labels)
        test_labels = []
        test_data = []
        results = []
        time_constraint = data.time_constraint
        blind_results = None
        
        if data.prior_test_data is not None:
            model = GradientBoostingClassifier()
            model.fit(X,y)
            blind_results = model.predict(Xtest)
    
        if time_constraint == 1:
            
            model = GradientBoostingClassifier()
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
            model.fit(X_train,y_train)
            results = model.predict(X_test)
            test_data = X_test
            test_labels = y_test
            feature_importances = list(model.feature_importances_)

        if time_constraint == 2:
            
            model = GradientBoostingClassifier()
            for i in range(2):
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
                model.fit(X_train,y_train)
                results.extend(model.predict(X_test))
                test_data.extend(X_test)
                test_labels.extend(y_test)
            feature_importances = list(model.feature_importances_)
                
        if time_constraint == 3:
            
            model = GradientBoostingClassifier()
            results = []
            cv = StratifiedKFold(n_splits=5,shuffle=True)
            for train, test in cv.split(X,y):
                 model.fit(X[train],y[train])
                 results.extend(model.predict(X[test]))
                 test_data.extend(X[test])
                 test_labels.extend(y[test])
            feature_importances = list(model.feature_importances_)
                 
            
        if time_constraint == 4:
            model = GradientBoostingClassifier()
            parameters = {'learning_rate':(0.01,0.1,1),'n_estimators':(25,50,100)}
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
            
            model = GradientBoostingClassifier()
            parameters = {'loss':('deviance', 'exponential'), 'learning_rate':(0.001,0.01,0.1,1,10),'n_estimators':(5,10,25,50,100,500), 
                          'criterion':('friedman_mse','mae')}
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
