#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""


@author: anibaljt

"""


from .Technique import Technique
from sklearn.decomposition import PCA
from sklearn.cluster import MeanShift as ms
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score


class MeanShift(Technique):
    
    
    GENERAL_USE = False
    
    TECHNIQUE_TYPE = "unsupervised"
    
    def get_class_name():
        return 'MeanShift'
    
    def get_name():
        return 'mean shift'

    def get_category():
        return 'density'

    def get_wesbite():
        return 'https://scikit-learn.org/stable/modules/generated/sklearn.cluster.MeanShift.html'
    
    
    def preprocess(data):
                
        features = StandardScaler().fit_transform(data.data)
        features = PCA().fit_transform(data.data)
            
        return features,None
    
        
    def train(data):
        
                
        X,_ = MeanShift.preprocess(data)
        test_data = X
        time_constraint = data.time_constraint

        results = ms().fit_predict(test_data)

        return test_data,None,results,None,None
    


    
    
    
