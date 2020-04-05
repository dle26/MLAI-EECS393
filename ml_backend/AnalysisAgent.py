#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: anibaljt
"""

import copy 
import MLTechniques
import inspect
import numpy as np


class AnalysisAgent:
    
    def __init__(self,data):
        
        self.data = copy.deepcopy(data)
        
    def fitApproaches(self,unsupervised=False):

        ml_package = list(np.asarray(inspect.getmembers(MLTechniques)).flatten())
            
        for technique in self.data.techniques:
            
            mlmodel = ml_package[ml_package.index(technique+1)]
            self.data = mlmodel().train(self.data)
        
        return self.data