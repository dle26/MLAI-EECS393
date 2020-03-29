#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: anibaljt

"""


import copy
from TextMine import TEXTMINE
from UniversalScores import UniversalScores


class SELECT:
    
    def __init__(self,data,threshold=0.25):
        
        self.data = copy.deepcopy(data)
        self.mining_threshold = threshold

        
        
    def selectAnalysisApproach(self,time_constraint,no_labels=False):

        analysis_type = "supervised"
        if no_labels:
            analysis_type = "unsupervised"
            
        user_input = self.data.descriptive_info
        top3_approaches,top3scores,matches = UniversalScores.reference(user_input,analysis_type)
        
        #### HOW TO HANDLE CUSTOM HERE - find a way to remove custom
        preprocessing,pscore,pmatches = UniversalScores.reference(user_input,"preprocessing",top3_approaches)
        
        
        if (len(matches)/len(self.data.descriptive_info)) < self.mining_threshold:
            
            self.data = TEXTMINE(self.data).from_database()
            user_input = self.data.descriptive_info
            top3_approaches,top3scores = UniversalScores.reference(user_input,analysis_type)
            

        if (len(pmatches)/len(self.data.descriptive_info)) < self.mining_threshold:
            self.data = TEXTMINE(self.data).from_database()
            user_input = self.data.descriptive_info
            preprocessing,pscore = UniversalScores.reference(user_input,"preprocessing",top3_approaches)
            
        self.data.data_for_update = zip(top3_approaches,top3scores,matches)
        self.data.ppr_data_for_update = zip(preprocessing,pscore,matches)

        return self.data
        
    
    