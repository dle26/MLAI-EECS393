#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 23:20:06 2020

@author: anibaljt
"""

from UniversalScores import UniversalScores



class UpdateAgent:

     
    def update(technique_score_tups):
        
        UpdateAgent.update_boost(technique_score_tups)
        UpdateAgent.update_score_dict(technique_score_tups)
    
        
    def update_boost(technique_score_tups,analysis_type):
        
        for tup in technique_score_tups:
            words = tup[2]

            for w in words:
              if w in list(UniversalScores.BOOST[tup[0]].keys()):
                  ### rando_threshold for now
                  if UniversalScores.BOOST[tup[0]][w][1] > 20:
                      UniversalScores.TECHNIQUE_SCORES[tup[0]][w] = (UniversalScores.BOOST[tup[0]][w][0],20)
                      del UniversalScores.BOOST[tup[0]][w]
                  else:
                      newscore = ((UniversalScores.BOOST[tup[0]][w][0] * 
                                 (UniversalScores.BOOST[tup[0]][w][1]+1))+tup[1])/(UniversalScores.BOOST[tup[0]][w][1]+1)
                      UniversalScores.BOOST[tup[0]][w] = (newscore,UniversalScores.BOOST[tup[0]][w][1]+1)
                      

    def update_score_dict(technique_score_tups):
           
        for tup in technique_score_tups:
            words = tup[2]

            for w in words:
              if w in list(UniversalScores.TECHNIQUE_SCORES[tup[0]].keys()):
                 newscore = ((UniversalScores.BOOST[tup[0]][w][0] * 
                                 (UniversalScores.BOOST[tup[0]][w][1]+1))+tup[1])/(UniversalScores.BOOST[tup[0]][w][1]+1)
                 
                 if newscore < 0.5:
                     del UniversalScores.TECHNIQUE_SCORES[tup[0]][w]
                 else:
                     UniversalScores.BOOST[tup[0]][w] = (newscore,UniversalScores.BOOST[tup[0]][w][1]+1)
                      
                  ### rando_threshold for now
                 if UniversalScores.TECHNIQUE_SCORES[tup[0]][w][1] > 20:
                      UniversalScores.TECHNIQUE_SCORES[tup[0]][w] = (UniversalScores.TECHNIQUE_SCORES[tup[0]][w][0],20)
                      del UniversalScores.TECHNIQUE_SCORES[tup[0]][w]
                 else:
                      UniversalScores.TECHNIQUE_SCORE[tup[0]][w] = (UniversalScores.TECHNIQUE_SCORES[tup[0]][w][0],20)
        