#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: anibaljt
"""

class Pipeline:
    
    ''' 
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


   '''
             


    def run_MLAI(datafiles,datafilenames,datafilesizes,
                 labelfile,labelfilename,labelfilesize,user_info):
        
        pass
        
        

    def create_output_dict(data):
        
        pass
