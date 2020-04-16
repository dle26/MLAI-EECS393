#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: anibaljt

"""

import MLTechniques
import copy
from .TextMine import TEXTMINE
from .UniversalScores import UniversalScores
import inspect
import numpy as np


class SELECT:
    
    def __init__(self,data,threshold=0.25):
        
        self.data = copy.deepcopy(data)
        self.mining_threshold = threshold

        
        
    def selectAnalysisApproach(self):
        print()
        print("----SELECTING APPROACH-----")
        print()

        user_input = self.data.descriptive_info
        top2_approaches,matches = UniversalScores.reference(user_input)
        

        if (len(np.ravel(matches))/len(self.data.descriptive_info)) < self.mining_threshold:
        
            keywords,keyword_scores,searchwords = TEXTMINE(self.data.descriptive_info,self.data.userid,self.data.analysis_type).from_database()
            top2_approaches = self.select_from_textmine(keywords,keyword_scores,searchwords,self.data.analysis_type)
            
    
        
        self.data.techniques = list(np.ravel(np.asarray(top2_approaches)))
        print()
        print("-----TECHNIQUES SELECTED----")
        print()
        for x in self.data.techniques:
            print(x.upper())
            

        return self.data
    
    
    
    def select_from_textmine(self,keywords,keywordscores,searchwords,analysis_type):
        
        #### 2 tiered approach here - need adaskipgram here
        names = []
        scores = []

        for n,word in enumerate(list(set(searchwords['specific']))):
            if word in keywords:
                names.append(word)
                scores.append(keywordscores[keywords.index(word)])
                
        approaches,scores = two_list_sort(names,scores)
        
        approaches = approaches[[-2,-1]]
        scores = scores[[-2,-1]]
        
        technique_names = np.random.choice(approaches,2,replace=False,p=np.asarray(scores)/np.sum(scores))
        
        specific_names = []
        classes = []

        for app in technique_names:
             specific_names,class_names = select_approach(app,"specific",analysis_type)
             classes.append(UniversalScores.select_from_usage(class_names,1))

        return classes


                      
def two_list_sort(tosort,basis):
    
      for i in range(1, len(basis)):
        key = basis[i]
        key2 = tosort[i]
        j = i-1
        while j >=0 and key <basis[j] : 
                basis[j+1] = basis[j] 
                tosort[j+1] = tosort[j]
                j -= 1
                
        basis[j+1] = key 
        tosort[j+1] = key2
        
      return np.array(tosort),np.asarray(basis)
              
            
  
#### TODO: UPDATE w/more elegant code          
def select_approach(app_name,select,analysis_type):

        approaches_to_select = []
        class_names = []
    
        for name, obj in inspect.getmembers(MLTechniques):
            if inspect.isclass(obj):
                if obj.TECHNIQUE_TYPE == analysis_type:
                    if select =='specific':
                        if obj.get_category() == app_name:
                            approaches_to_select.append(obj.get_name())
                            class_names.append(obj.get_class_name())
                    else:
                         if obj.get_general_category() == name:
                            approaches_to_select.append(obj.get_name())
                            class_names.append(obj.get_class_name())

        return approaches_to_select,class_names
