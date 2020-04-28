#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 16:25:59 2020

@author: anibaljt
""" 

import inspect
import numpy as np
import MLTechniques
import pickle
import os

'''

Structure of FeatureDict

{'BOOST':{'SVM': [('images',0.73,num_uses,num_possibilies,'supervised')]},"TECHNIQUES:"{}}


'''



class UniversalScores:
    
    
    def reference(keywords):

     
        model = UniversalScores.initialize()
        results,values,matched_words = UniversalScores.compare_keywords(model,keywords)
        if np.sum(values) > 0:
            results = UniversalScores.weighted_select(results,values)
    
        return results,matched_words
    
    
    ### TODO!!!!!!!
    
    def apply_skipgram():
        pass
    
    
    def weighted_select(keywords,scores):
        
        scores = np.asarray(scores)
        indicies = np.random.choice(len(keywords),2,scores/np.sum(scores))
        return np.asarray(keywords)[indicies],scores[indicies]
        

    
    def initialize():
        
        if os.path.exists(os.getcwd() + '/MODEL.pkl'):
            model = pickle.load(open('MODEL.pkl','rb'))
        else:
            model = {"BOOST":{},"TECHNIQUES":{}}
        
        for name, obj in inspect.getmembers(MLTechniques):
            if inspect.isclass(obj):
          
               if obj.get_class_name() not in list(model['BOOST'].keys()) and obj.get_name() not in list(model['TECHNIQUES'].keys()):
                     model['BOOST'][obj.get_class_name()] = []

        
        pickle.dump(model,open("MODEL.pkl","wb"))

        return model
        
        
    
    def key_sort(keys,values): 
      if len(list(values)) > 0:
        for i in range(1, len(values)): 
            
            key = values[i] 
            key2 = keys[i]
            
            j = i-1
            while j >=0 and key < values[j] : 
                values[j+1] = values[j] 
                keys[j+1] = values[j]
                j -= 1
            values[j+1] = key 
            keys[j+1] = key2
            
      return keys,values
    
    

    def compare_keywords(model,keywords):
        
        #### which techniques correspond to which words? - need adagram here!!!!
        technique_matches = {}
        match_percentage = {}
        matches = []
        for dic in model:
            for technique in model[dic]:
                num_matches = 0
                technique_matches[technique] = []
                matched_words = []
                for tup in model[dic][technique]:
                    if len(list(set(keywords) & set(tup))) > 0:
                        technique_matches[technique].append(tup[0])
                        num_matches += 1
                        matched_words.append(tup[0])
                        
                match_percentage[technique] = num_matches/len(keywords)
                matches.append(matched_words)

            if num_matches > 0:
                for scoreset in list(technique_matches.values()):
                   technique_matches[technique] = np.average([sum(list(scoreset)),match_percentage[technique]],weights=[0.75,0.25])
    
        results,values = UniversalScores.key_sort(list(technique_matches.keys()),list(technique_matches.values()))

        return results,values,matches  
    
    
    
    def select_from_usage(names,number):
        
        
        ''' TODO: UPDATE WITH NEW TUPLE SET '''

        techniques = []
        
        if os.path.exists('MODEL.pkl'):
            model= pickle.load(open('MODEL.pkl','rb'))
        else:
            model = {}

        all_scores = []
        for name in names:
            name_score = []
            name_uses = []
            found = False
            for tup in model["BOOST"][name]:
                if tup[0] == name:
                   name_score.append(tup[1])
                   name_uses.append(tup[2])
            if len(name_score) > 0:
                ### WEIGHTS scores based on num uses + presence in boost
                all_scores.append((np.median(name_score)+np.median(np.array(name_uses)/np.sum(name_uses))*1)+0.1) ###adjust the weights (currently 1/0.1) as needed 
                found = True
            name_score = []
            name_uses = []
            
            if name in model["TECHNIQUES"].keys():
              for tup in model["TECHNIQUES"][name]:
                if tup[0] == name:
                   name_score.append(tup[1])
                   name_uses.append(tup[2])
                   
            if len(name_score) > 0:  
              all_scores.append((np.median(name_score)+np.median(np.array(name_uses)/np.sum(name_uses))*1))
            elif len(name_score) == 0 and not found:
                all_scores.append(0)
   
        if np.sum(all_scores) == 0: #### arbitrary threshold for handling very sparse info (early uses) - optimize this
            all_scores = None
        else:
            all_scores = np.array(all_scores)/np.sum(all_scores)
            
        techniques.append(np.random.choice(names,number,p=all_scores))

        return list(np.ravel(np.asarray(techniques)))
        
    
