#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 23:20:06 2020

@author: anibaljt
"""

import pickle
import numpy as np


''' THIS WILL BE CALLED AT THE END OF PIPELINE '''

'''

Structure of FeatureDict

{'BOOST':{'SVM': [('images',0.73,num_uses,num_possibilies,'supervised')]},"TECHNIQUES:"{same as boost}}

 
TODO: ENSURE NO DUPLICATE KEYWORD WITH ADASKIPGRAM - DO NOT WANT AN EXCESS OF KEYWORDS

'''



class UpdateAgent:

 
    def update(technique_score_tups):
        
        UpdateAgent.update_boost(technique_score_tups)
        UpdateAgent.update_score_dict(technique_score_tups)
    
        
    def update_boost(technique_score_tups,data_score):
        
        '''
        technique_score_tup
            (classname,score,keywords)
            
        TODO: EXPLICTLY DEFINE THE SCORING FUNCTION
        '''

        model = pickle.load('MODEL.pkl')

        boost = model['BOOST']

        for tup in technique_score_tups:
            total_uses = []
            words = tup[2]
            for w in words:
                for entry in boost[tup[0]]:
                    if w in entry:
                        if tup[0] < boost[tup[0]][w][0]:
                            adj_score = min(tup[0]+data_score,boost[tup[0]][w][0])
                        else:
                            adj_score = max(tup[0]-data_score,boost[tup[0]][w][0])
                            
                        newscore = ((entry[1] * entry[2]+1)+adj_score)/(entry[1]+1)
                        newtup = (w,newscore,entry[2]+1,entry[3]+1)
                        
                    else:
                        newtup = (w,entry[1],entry[2],entry[3]+1)
                    total_uses.append(newtup[2])
                        
                        
                      
                  ### rando_threshold for now
            if np.median(total_uses) == 20:
                
                model["TECHNIQUES"][tup[0]] = boost[tup[0]]
                del boost[tup[0]]

            model["BOOST"] = boost
          
        pickle.dump(model,open('MODEL.pkl',"wb"))
      
        

    '''
    TODO
    def update_score_dict(technique_score_tups,data_score):
           
        
        tech_scores = pickle.load(open('MODEL.pkl','rb'))['TECHNIQUES']
        
        for tup in technique_score_tups:
            words = tup[2]

            for w in words:
              if w in list(tech_scores[tup[0]].keys()):
                 if tup[0] < tech_scores[tup[0]][w][0]:
                    adj_score = min(tup[0]+data_score,tech_scores[tup[0]][w][0])
                 else:
                    adj_score = max(tup[0]-data_score,tech_scores[tup[0]][w][0])
                    
                 newscore = ((tech_scores[tup[0]][w][0] * 
                                 (tech_scores[tup[0]][w][1]+1))+adj_score)/(tech_scores[tup[0]][w][1]+1)
                 
                 if newscore < 0.5:
                     del tech_scores[tup[0]][w]
                 else:
                     tech_scores[tup[0]][w] = (newscore,tech_scores[tup[0]][w][1]+1)
                     
        pickle.dump(tech_scores,open('TECHNIQUE_SCORES.pkl',"wb"))
     '''