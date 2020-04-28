#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: anibaljt

"""


from .Technique import Technique
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans as km
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score


class KMeans(Technique):
    
    
    ISDEEP  = False
    TECHNIQUE_TYPE = "unsupervised"
    
    def get_website():
        return 'https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html'
      
    def get_class_name():
        return 'KMeans'
    
    def get_name():
        return 'k-means'

    def get_category():
        return 'k-means'
    
    def preprocess(data):
                
        features = StandardScaler().fit_transform(data.data)
        features = PCA().fit_transform(data.data)
            
        return features,None
    

    def train(data):
        
        X,_ = KMeans.preprocess(data)
        test_data = X
        time_constraint = data.time_constraint

        ### optimize by number of clusters
        
        if time_constraint < 3:
            best_score = -1.1
            best_results = None
            for number in [2,4,8]:
                results = km(n_clusters=number).fit_predict(test_data)
                if silhouette_score(test_data,results) > best_score:
                    best_score = silhouette_score(test_data,results)
                    best_results = results
        
        else:
            best_score = -1.1
            best_results = None
            for number in [2,3,4,5,6,7,8,9,10]:
                results = km(n_clusters=number).fit_predict(test_data)
                if silhouette_score(test_data,results) > best_score:
                    best_score = silhouette_score(test_data,results)
                    best_results = results
            
        
        return test_data,None,best_results,None,None
    
