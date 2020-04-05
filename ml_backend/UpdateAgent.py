#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 23:20:06 2020

@author: anibaljt
"""

import pickle

''' THIS WILL BE CALLED AT THE END OF PIPELINE '''

### TODO: ENSURE NO DUPLICATE KEYWORD WITH ADASKIPGRAM - DO NOT WANT AN EXCESS OF KEYWORDS

class UpdateAgent:

 
    def update(technique_score_tups):
        
        UpdateAgent.update_boost(technique_score_tups)
        UpdateAgent.update_score_dict(technique_score_tups)
    
        
    def update_boost(technique_score_tups,data_score,analysis_type="supervised"):
        
        
        boost = pickle.load('BOOST.pkl')[analysis_type]
        tech_scores = pickle.load('TECHNIQUE_SCORES.pkl')[analysis_type]
        
        for tup in technique_score_tups:
            words = tup[2]

            for w in words:
              if w in list(boost[tup[0]].keys()):
                  
                  if tup[0] < boost[tup[0]][w][0]:
                      adj_score = min(tup[0]+data_score,boost[tup[0]][w][0])
                  else:
                       adj_score = max(tup[0]-data_score,boost[tup[0]][w][0])
                      
                  ### rando_threshold for now
                  if boost[tup[0]][w][1] == 20:
                      
                      newscore = ((boost[tup[0]][w][0] * 
                                 (boost[tup[0]][w][1]+1))+adj_score)/(boost[tup[0]][w][1]+1)
                      
                      tech_scores[tup[0]][w] = (newscore,20)
                      ## TODO: fix dict iteration error
                      del boost[tup[0]][w]
                      
                  else:
                      newscore = ((boost[tup[0]][w][0] * 
                                 (boost[tup[0]][w][1]+1))+adj_score)/(boost[tup[0]][w][1]+1)
                      boost[tup[0]][w] = (newscore,boost[tup[0]][w][1]+1)
          
        pickle.dump(boost,open('BOOST.pkl',"wb"))
        pickle.dump(tech_scores,open('TECHNIQUE_SCORES.pkl','wb'))
        

    def update_score_dict(technique_score_tups,data_score):
           
        
        tech_scores = pickle.load(open('TECHNIQUE_SCORES.pkl','rb'))
        
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