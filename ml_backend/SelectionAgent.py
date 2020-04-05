#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: anibaljt

"""

import MLTechniques
import copy
from TextMine import TEXTMINE
from UniversalScores import UniversalScores
import inspect
import numpy as np
#from UniversalScores import UNIVERSALSCORES


class SELECT:
    
    def __init__(self,data,run_id,threshold=0.25):
        
        self.data = copy.deepcopy(data)
        self.mining_threshold = threshold
        self.run_id = run_id

        
        
    def selectAnalysisApproach(self,time_constraint,no_labels=False):

        analysis_type = "supervised"
        if no_labels:
            analysis_type = "unsupervised"
            
        user_input = self.data.descriptive_info
        top2_approaches,matches = UniversalScores.reference(user_input,analysis_type)
        

        if (len(matches)/len(self.data.descriptive_info)) < self.mining_threshold:
        
            keywords,keyword_scores,searchwords = TEXTMINE(self.data.descriptive_info,self.run_id).from_database()
            top2_approaches = self.select_from_textmine(keywords,keyword_scores,searchwords,analysis_type)
            
        self.data.data_for_update = zip(top2_approaches,[user_input,user_input])
        self.data.techniques.extend(top2_approaches)
        return self.data
    
    
    
    
    def select_from_textmine(self,keywords,keywordscores,searchwords,analysis_type):
        
        #### 3 tiered approach here - need adaskipgram here
        names = []
        scores = []
        approaches = []
        
        for word in searchwords['names']:
            if word in keywords:
                names.append(word)
                scores.append(keywordscores[keywords.index(word)])
                
        final_approaches = []
        if len(names) > 1:
            return two_list_sort(names,scores)[[-2,-1]]
        
        elif len(names) == 1:
            final_approaches.append(names[0])
            
            
            
        else:
           names = []
           scores = []
           technique_names = []
           for word in searchwords['specific']:
              if word in keywords:
                  names.append(word)
                  scores.append(keywordscores[keywords.index(word)])
            
           if len(approaches) == 0 and len(names) > 1:
                approaches = list(two_list_sort(names,scores)[[-2,-1]])
                for a in approaches:
                    technique_names = select_approach(a,"specific",analysis_type)
                    
                ### TODO: add selection method and add to approaches
                return approaches
            
           elif len(final_approaches) == 1 and len(names) > 0:
                technique_names = select_approach(two_list_sort(names,scores)[-1],'specific',analysis_type)
                
                final_approaches.append(UniversalScores.select_from_usage(technique_names,1))
                
                return final_approaches
            
           elif len(names) == 0:
               names = []
               scores = []
               for word in searchwords['general']:
                  if word in keywords:
                     names.append(word)
                     scores.append(keywordscores[keywords.index(word)])
               technique_names = select_approach(two_list_sort(names,scores)[-1])
               if len(final_approaches) == 0:
                   final_approaches.append(UniversalScores.select_from_usage(technique_names,2))
               else:
                  final_approaches.append(UniversalScores.select_from_usage(technique_names,1))
               
        return final_approaches
        
            
                
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
        
      return np.array(tosort)
              
            
  
#### TODO: UPDATE w/more elegant code          
def select_approach(name,select,analysis_type):

    
        approaches_to_select = []
        for name, obj in inspect.getmembers(MLTechniques):
            if inspect.isclass(obj):
                if obj.TECHNIQUE_TYPE == analysis_type:
                    if select =='specific':
                        if obj.get_category() == name:
                            approaches_to_select.append(obj.get_name())
                    else:
                         if obj.get_general_category() == name:
                            approaches_to_select.append(obj.get_name())
        
        return approaches_to_select