# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 14:42:43 2021

@author: Rami EZZOUCH
"""
import os
import progressbar

search_dir = r'S:\532-PHELIQS\532.1-QuantumDevice\Quantumsilicon\Triton Experiments\data'
search_str = r'#117_TP13-twaitCOMPVsFreq-B0p62T-theta60phi0-MWm5p5dBmBURST100ns-Pulse64mV250ns-Twait8e-06_20-47-04'
files = []

date_folders = [f.path for f in os.scandir(search_dir) if f.is_dir()]
progbar = progressbar.ProgressBar(widgets=[progressbar.Percentage(),' ',progressbar.Bar(), '\n' ,progressbar.widgets.ETA(), '\n'], maxval=len(date_folders)).start()

found = False
for i, date_folder in enumerate(date_folders):
    measurements = [f.path for f in os.scandir(date_folder) if f.is_dir()]
    for measurement in measurements:
        if search_str in measurement:
            print(measurement)
            found = True
            break
    if found:
       break
    progbar.update(i+1)
progbar.finish()