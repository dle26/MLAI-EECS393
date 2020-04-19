#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: anibaljt
"""

import copy 
import MLTechniques
import inspect
import numpy as np


class ANALYZE:
    
    def __init__(self,data):
        
        self.data = copy.deepcopy(data)
        
        
    def train_approaches(self):

        ml_package = list(np.asarray(inspect.getmembers(MLTechniques)).flatten())

        for technique in self.data.techniques:
            
            mlmodel = ml_package[ml_package.index(technique)+1]
            test_data,test_labels,prediction_results,feature_importances,blind_results = mlmodel.train(self.data)
            
            self.data.test_data.append(test_data)
            self.data.educational_info.append(mlmodel.get_website())
            self.data.test_labels.append(test_labels)
            self.data.prediction_results.append(prediction_results)
            self.data.blind_prediction_results.append(blind_results)
            self.data.feature_importances.append(feature_importances)
            
            if self.data.analysis_type == 'unsupervised':
                self.data.test_labels = None
            
        print("-----ANALYSIS COMPLETE: INTERPRETING RESULTS NOW-----")
        print()

        return self.data
    
    
