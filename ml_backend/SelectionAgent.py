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
        
        ''' general approaches - if the user screws up '''
        if len(user_input) == 0:

            if self.data.analysis_type == 'supervised':
                self.data.techniques = ['SVM','GradientBoost']
            else:
                 self.data.techniques = ['KMeans','HAC']
                 
            return self.data
        
        top2_approaches,matches = UniversalScores.reference(user_input)
        

        if (len(np.ravel(matches))/len(self.data.descriptive_info)) < self.mining_threshold:
        
            keywords,keyword_scores,searchwords = TEXTMINE(self.data.search_queries,self.data.descriptive_info,self.data.userid,self.data.analysis_type).from_database(self.data.time_constraint)
            top2_approaches = self.select_from_textmine(keywords,keyword_scores,searchwords,self.data.analysis_type)
            
    
        
        self.data.techniques = list(np.ravel(np.asarray(top2_approaches)))
        print()
        print("-----TECHNIQUES SELECTED----")
        print()
        for x in self.data.techniques:
            print(x.upper())
            

        return self.data
    
    
    
    def select_from_textmine(self,keywords,keywordscores,searchwords,analysis_type):
        
        names = []
        scores = []
        allwords =  list(searchwords['category'])
        allwords.extend(list(searchwords['specific']))
        
        for n,word in enumerate(list(set(allwords))):
            if word in keywords:
                names.append(word)
                scores.append(keywordscores[keywords.index(word)])
        
        scores = np.asarray(scores)
        top_vals = np.where(scores > np.percentile(scores,75))
   

        if len(top_vals[0]) == 1:
            approaches,scores = two_list_sort(names,scores)
            approaches = list(approaches[[-2,-1]])
            scores = scores[[-2,-1]]
        else:
            approaches = np.asarray(names)[top_vals[0]]
            scores = scores[top_vals[0]]
            approaches = list(approaches)
        
   
        technique_names = []
        scores = list(scores)
        
        for n,app in enumerate(approaches):
            if app in searchwords['specific']:
                technique_names.append(app)
                approaches.remove(app)
                scores.remove(scores[n])
   
        if len(technique_names) == 0:
            technique_names.extend(np.random.choice(approaches,2,replace=False,p=np.asarray(scores)/np.sum(scores)))
        elif len(technique_names) == 1:
             technique_names.append(np.random.choice(approaches,1,replace=False,p=np.asarray(scores)/np.sum(scores)))
        

        specific_names = []
        classes = []

        for app in technique_names:
             print(app)
             specific_names,class_names = select_approach(app,analysis_type)
             print(class_names)
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
              
            
   
def select_approach(app_name,analysis_type):

        approaches_to_select = []
        class_names = []
    
        for name, obj in inspect.getmembers(MLTechniques):
            if inspect.isclass(obj):
                if obj.TECHNIQUE_TYPE == analysis_type:
                    if obj.get_name() == app_name or obj.get_category() == app_name:
                            approaches_to_select.append(obj.get_name())
                            class_names.append(obj.get_class_name())

        return approaches_to_select,class_names
