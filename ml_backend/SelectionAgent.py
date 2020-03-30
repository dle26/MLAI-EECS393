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
        ##### PUT CURRENT APPROACHES IN A LIST HERE
        top3preprocessing,top3pscore,top3pmatches = UniversalScores.reference(user_input,"preprocessing",top3_approaches)
        ##### NOTHING HERE TO HANDLE EMPTY ONES - NOVEL APPROACHES
       
        all_approaches,all_ppr = "",""

        for name, obj in inspect.getmembers(MLTechniques):
            if inspect.isclass(obj):
                if obj.TECHNIQUE_TYPE == analysis_type:
                    all_approaches += obj.get_name()
                if obj.TECHNIQUE_TYPE == 'preprocessing':
                    all_ppr += obj.get_name()

        if (len(matches)/len(self.data.descriptive_info)) < self.mining_threshold:
        
            keywords,keyword_scores = TEXTMINE(self.data).from_database()
            top3_approaches,top3ppr,matches,ppr_matches = self.select_from_textmine(keywords,keyword_scores,all_approaches,all_ppr)

        else:
            top3_approaches,top3ppr,matches,ppr_matches = UniversalScores.reference(user_input,analysis_type)
            
            
        self.data.data_for_update = zip(top3_approaches,matches)
        self.data.ppr_data_for_update = zip(top3ppr,matches)

        return self.data
    
    

    def select_from_textmine(self,keywords,keywordscores,allapproaches,all_pr_approaches):
        
        approach_scores = {}
        ppr_approach_scores = {}
        
        #### need adagram for this as well!!!!
        for num,key in enumerate(keywords):
           if key[0:key.index('+')] in allapproaches:
               if key[0:key.index('+')] in approach_scores:
                   approach_scores[key[0:key.index('+')]] += 1
               else:
                   approach_scores[key[0:key.index('+')]] = 1
               if key[key.index('+'):len(key)] in all_pr_approaches:
                   if key[key.index('+'):len(key)] in ppr_approach_scores:
                       ppr_approach_scores[key] += 1
                   else:
                       ppr_approach_scores[key] = 1
          
        ranked_approaches,approach_scores = UniversalScores.sort_dict_values(approach_scores.keys(),approach_scores.values())
        ranked_ppr_approaches,ppr_scores = UniversalScores.sort_dict_values(ppr_approach_scores.keys(),ppr_approach_scores.values())
        
        ### TODO: weighted select here
        top3approaches = UniversalScores.weighted_selected(ranked_approaches,approach_scores)
        
        ###TODO: handle custom, built-in PPR - may have to switch to this anyway
        
        top3ppr = []
        for a in top3approaches:
           for key in range(len(ranked_ppr_approaches)-1,0,-1):
               ppr_key = list(ranked_ppr_approaches.keys())
               if a in ranked_ppr_approaches[ppr_key]:
                   top3ppr.append(ranked_ppr_approaches)
                   break
        
        ml_match,ppr_match = [],[]
        
        for group in zip(top3approaches,top3ppr):
            matches,p_matches = [],[]
            for word in keywords:
                if word in group[0] and word not in group[1]:
                   matches.append(word[word.index('+'):len(word)])
                if word not in group[0] and word in group[1]:
                    p_matches.append(word[word.index('+'):len(word)])
                    
            ml_match.append(matches)
            ppr_match.append(p_matches)
        
        
        return top3approaches,top3ppr,ml_match,ppr_match
