#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 23:20:06 2020

@author: anibaljt
"""

from UniversalScores import UniversalScores

''' THIS WILL BE CALLED AT THE END OF PIPELINE '''

### TODO: ENSURE NO DUPLICATE KEYWORD WITH ADASKIPGRAM - DO NOT WANT AN EXCESS OF KEYWORDS

class UpdateAgent:

 
    def update(technique_score_tups):
        
        UpdateAgent.update_boost(technique_score_tups)
        UpdateAgent.update_score_dict(technique_score_tups)
    
        
    def update_boost(technique_score_tups,data_score):
        
        for tup in technique_score_tups:
            words = tup[2]

            for w in words:
                
              if w in list(UniversalScores.BOOST[tup[0]].keys()):
                  
                  if tup[0] < UniversalScores.BOOST[tup[0]][w][0]:
                      adj_score = min(tup[0]+data_score,UniversalScores.BOOST[tup[0]][w][0])
                  else:
                       adj_score = max(tup[0]-data_score,UniversalScores.BOOST[tup[0]][w][0])
                      
                  ### rando_threshold for now
                  if UniversalScores.BOOST[tup[0]][w][1] == 20:
                      
                      newscore = ((UniversalScores.BOOST[tup[0]][w][0] * 
                                 (UniversalScores.BOOST[tup[0]][w][1]+1))+adj_score)/(UniversalScores.BOOST[tup[0]][w][1]+1)
                      
                      UniversalScores.TECHNIQUE_SCORES[tup[0]][w] = (newscore,20)
                      
                      del UniversalScores.BOOST[tup[0]][w]
                      
                  else:
                      newscore = ((UniversalScores.BOOST[tup[0]][w][0] * 
                                 (UniversalScores.BOOST[tup[0]][w][1]+1))+adj_score)/(UniversalScores.BOOST[tup[0]][w][1]+1)
                      UniversalScores.BOOST[tup[0]][w] = (newscore,UniversalScores.BOOST[tup[0]][w][1]+1)
                      
                      

    def update_score_dict(technique_score_tups,data_score):
           
        
        for tup in technique_score_tups:
            words = tup[2]

            for w in words:
              if w in list(UniversalScores.TECHNIQUE_SCORES[tup[0]].keys()):
                 if tup[0] < UniversalScores.BOOST[tup[0]][w][0]:
                    adj_score = min(tup[0]+data_score,UniversalScores.BOOST[tup[0]][w][0])
                 else:
                    adj_score = max(tup[0]-data_score,UniversalScores.BOOST[tup[0]][w][0])
                    
                 newscore = ((UniversalScores.TECHNIQUE_SCORES[tup[0]][w][0] * 
                                 (UniversalScores.TECHNIQUE_SCORES[tup[0]][w][1]+1))+adj_score)/(UniversalScores.TECHNIQUE_SCORES[tup[0]][w][1]+1)
                 
                 if newscore < 0.5:
                     del UniversalScores.TECHNIQUE_SCORES[tup[0]][w]
                 else:
                     UniversalScores.BOOST[tup[0]][w] = (newscore,UniversalScores.BOOST[tup[0]][w][1]+1)
                      
          