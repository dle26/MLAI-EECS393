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
        
        
        
    def train_approaches(self,unsupervised=False):

        ml_package = list(np.asarray(inspect.getmembers(MLTechniques)).flatten())

        for technique in [self.data.techniques[-1]]:
            mlmodel = ml_package[ml_package.index(technique.upper())+1]
            self.data = mlmodel().train(self.data,1)
            
        print("-----ANALYSIS COMPLETE: INTERPRETING RESULTS NOW-----")
        print()

        return self.data