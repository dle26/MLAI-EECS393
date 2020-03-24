#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 22:38:17 2020

@author: anibaljt
"""

from sklearn.metrics import confusion_matrix 
import numpy as np


x = confusion_matrix([0, 2,1,2, 0, 1,2], [2,2,2,1, 1, 1, 0]).ravel()


