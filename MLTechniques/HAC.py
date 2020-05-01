#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: anibaljt
"""


from .Technique import Technique
from sklearn.decomposition import PCA
from sklearn.cluster import AgglomerativeClustering as agg
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score


class HAC(Technique):
    
    ISDEEP = False
    
    TECHNIQUE_TYPE = "unsupervised"
    
    def get_website():
        return 'https://en.wikipedia.org/wiki/Hierarchical_clustering'

    def get_class_name():
        return 'HAC'
    
    def get_name():
        return 'hierarchical'

    def get_category():
        return 'hierarchical'
    
    
    def preprocess(data):
                
        features = StandardScaler().fit_transform(data.data)
        features = PCA().fit_transform(data.data)
            
        return features,None
    
        
    def train(data):
        
                
        X,_ = HAC.preprocess(data)
        test_data = X
        time_constraint = data.time_constraint

        ### optimize by number of clusters
        
        if time_constraint ==  1:
            best_score = -1.1
            best_results = None
            for number in [2,4,8]:
                results = agg(n_clusters=number).fit_predict(test_data)
                if silhouette_score(test_data,results) > best_score:
                    best_score = silhouette_score(test_data,results)
                    best_results = results
        
        if time_constraint == 2:
            best_score = -1.1
            best_results = None
            for number in [2,3,4,5,6,7,8,9,10]:
                results = agg(n_clusters=number).fit_predict(test_data)
                if silhouette_score(test_data,results) > best_score:
                    best_score = silhouette_score(test_data,results)
                    best_results = results
        
        if time_constraint == 3:
            best_score = -1.1
            best_results = None
            for number in [2,4,8]:
                for func in ['euclidean','manhattan']:
                    if func != 'euclidean':
                        results = agg(n_clusters=number,affinity=func,linkage='complete').fit_predict(test_data)
                    else:
                        results = agg(n_clusters=number,affinity=func).fit_predict(test_data)
                    if silhouette_score(test_data,results) > best_score:
                        best_score = silhouette_score(test_data,results)
                        best_results = results
    
        if time_constraint == 4:
            best_score = -1.1
            best_results = None
            for number in [2,3,4,5,6,7,8]:
                for func in ['euclidean','manhattan']:
                    if func != 'euclidean':
                        results = agg(n_clusters=number,affinity=func,linkage='complete').fit_predict(test_data)
                    else:
                        results = agg(n_clusters=number,affinity=func).fit_predict(test_data)
                    if silhouette_score(test_data,results) > best_score:
                        best_score = silhouette_score(test_data,results)
                        best_results = results
                    
        if time_constraint == 5:
            best_score = -1.1
            best_results = None
            for number in [2,3,4,5,6,7,8]:
                for func in ['euclidean','manhattan','l1','l2','cosine']:
                    if func != 'euclidean':
                        results = agg(n_clusters=number,affinity=func,linkage='complete').fit_predict(test_data)
                    else:
                        results = agg(n_clusters=number,affinity=func).fit_predict(test_data)
                    
                    if silhouette_score(test_data,results) > best_score:
                        best_score = silhouette_score(test_data,results)
                        best_results = results
            

        return test_data,None,results,None,None
    

