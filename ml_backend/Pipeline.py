#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: anibaljt
"""

from Prep import DATAPREP
from SelectionAgent import SELECT
from AnalysisAgent import ANALYZE
from Interpret import INTERPRET

class Pipeline:
    
    ''' 
    function: run_MLAI
    
    params:
        
        datafiles - list of filehandler objects or single object
        
        datafilenames - list of file names corresponding to the files in
                        datafiles
        
        datafilesizes - list of file sizes corresponding to the files in 
                        datafiles
                        
        
       labelfile - filehandler object corresponding to labels
            - if it does not exist, simply input "None"
              into the run_MLAI method
              
       labelfilename - string, name of the labelfile
       
       labelfilesize - int, size of the labelfile
              
        user_info - dictionary containing the following keys
             1. time, int 1-5
             2. userid (string, i.e. email address)
             3. user_input (string of words) 
             
    
    returns:
        
        interpreted_results
        
        nested dictionary containing, for each technique:
            
            1. The evaluation metrics (int)
            2. The interpreted natural language results (string)
        
        All contains the best model out of the fitted approaches (string)
        and the type of analysis (supervised or unsupervised)
        
        Example:
            
            {"SVM":{"F1 Score: 0.75, "NL Results": "...."},"best: "SVM","analysis type":supervised}

   '''
             



    def run_MLAI(datafiles,datafilenames,datafilesizes,
                 labelfile,labelfilename,labelfilesize,user_info):
        
        
        data_object = DATAPREP(datafiles,datafilenames,datafilesizes,
                 labelfile,labelfilename,labelfilesize,user_info).run()
        
        data_object = SELECT(data_object).selectAnalysisApproach()
        
        data_object = ANALYZE(data_object).train_approaches()
        
        data_object = INTERPRET(data_object).interpret()
        
        
        return data_object.interpreted_results
