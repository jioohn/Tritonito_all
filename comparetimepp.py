# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 13:03:01 2021

@author: G-GRE-GRE050402
"""

t=time.time()

T=time.time()-t
print(T)

T=0
for i in range(0,10):
    t=time.time()
    phase_trigS()
    T+=time.time()-t
T=T/10
print(T)

T=0
for i in range(0,10):
    t=time.time()
    a,val=daqtrig.get_data_pulseseq(60e-6,100)
    T+=time.time()-t
T=T/10
print(T)
