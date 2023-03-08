# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 09:43:59 2020

@author: Simon Zihlmann
"""

# This file contains all necessary steps that need to be done before importing qcodes

import os
# create environment variable in order to get the qcodes logs on the dataserver
os.environ["QCODES_USER_PATH"] = "../log/qcodes"