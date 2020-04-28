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

 
TODO: ENSURE NO DUPLICATE KEYWORD WITH SpaCY - DO NOT WANT AN EXCESS OF KEYWORDS

'''



class UpdateAgent:

 
    def update(technique_score_tups,eval_score):
        
        UpdateAgent.update_boost(technique_score_tups,eval_score)
    #UpdateAgent.update_score_dict(technique_score_tups)
    
        
    def update_boost(technique_score_tups,data_score):
        
        '''
        technique_score_tup
            (classname,score,keywords)
            
        TODO: EXPLICTLY DEFINE THE SCORING FUNCTION
        '''
        model = pickle.load(open('MODEL.pkl','rb'))

        boost = model['BOOST']
        allword_lists = []
        for tup in technique_score_tups:
            allwords = []
            for words in tup[2]:
                for ww in words:
                  for w in ww.split():
                    if w != "" and w not in allwords:
                        allwords.append(w)
            allword_lists.append(allwords)

        for n,tup in enumerate(technique_score_tups):
           # total_uses = []
            words = tup[2]
            for w in allword_lists[n]:
                for entry in boost.keys():
                  if entry == tup[0]:
                    for wordtup in boost[entry]:
                        if w in wordtup:
                            if tup[1] < wordtup[1]:
                                adj_score = min(tup[1]+data_score,wordtup[1])
                            else:
                                adj_score = max(tup[1]-data_score,wordtup[1])
                            newscore = ((wordtup[1] * wordtup[2]+1)+adj_score)/(wordtup[1]+1)
                            newtup = (w,newscore,wordtup[2]+1)
                            boost[tup[0]].append(newtup)
                        
                    else:
                        newtup = (w,tup[1],1)
                        boost[tup[0]].append(newtup)
                   # total_uses.append(newtup[2])
                        
            '''
            ### rando_threshold for now
            if np.median(total_uses) == 20:
                
                model["TECHNIQUES"][tup[0]] = boost[tup[0]]
                del boost[tup[0]]
            '''
            print(boost)
            fveejnid
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
