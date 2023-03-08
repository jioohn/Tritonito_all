# -*- coding: utf-8 -*-
"""
Created on Wed May 12 17:45:21 2021

@author: G-GRE-GRE050402
"""
import numpy as np
h=4.135667662e-15 #eV*s
planck=h


deltaE=planck/10e3 #1meV
deltaT=10e-3
nu=deltaE/deltaT

t=10e3
delta=2*planck/10e3


plz=np.exp(-2*np.pi*delta**2/(planck*nu))