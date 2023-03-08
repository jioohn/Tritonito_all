# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 02:58:35 2020

@author: G-GRE-GRE050402
"""


import matplotlib.pyplot as plt
import numpy as np
from numpy import exp, linspace, random
from scipy.optimize import curve_fit
from scipy import asarray as ar,exp

rampVG4(-797)
rampVG3(-937)

rampVG5(0)

G1now=VG1()
G2now=VG2()
G3now=VG3()
G4now=VG4()
G5now=VG5()
VG3comp()
VG4comp()
# VG1onmin(G1now-60,G1now+60,801,1)
G1now=VG1()
VG1onmin(G1now-4,G1now+4,801,1)
G1now=VG1()
VG2onmin(G2now-4,G2now+4,801,1)
G2now=VG2()

continuous_acquisition()
name=str(Bfield())+'T_TPC_G4vsG3_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
# a,dataid,c,d=sweep2D(VG3comp,-800,-1000,801,0.1,VG4comp,-700,-900,801,0.01111,ph1)
# a,dataid,c,d=sweep2D(VG3comp,-870,-850,201,0.1,VG4comp,-780,-850,281,0.01111,ph1)
a,dataid,c,d=sweep2D(VG3comp,-934,-940,61,0.1,VG4comp,-795,-805,51,0.01317777,ph1)
plot_by_id(dataid)
saveplot(name,dataid)
    

#set_triggeracquisition
# trigger_mode() 
tc=0.10
acquisition_duration =400e-6  # length of time to record (s)
repetitions = 10            # number of repetitions for the averaging
points = 88  # number of points in the acquisition window (min=2)

#efftc=acquisition_duration/10
efftc=5e-6

# such that the effective Tc is 100ms 
# repetitions=tc/efftc/5

repetitions=1000

ziUhf.daq.setInt('/dev2010/demods/0/trigger', 33554432) # demodulator trigger set on AWGtrigger2 High
ziUhf.daq.setDouble('/dev2010/demods/0/rate', 200e3)
ziUhf.daq.setInt('/dev2010/demods/0/order', 1)
ziUhf.daq.setDouble('/dev2010/demods/0/timeconstant', efftc)
#ziUhf.daq.setInt('/dev2365/awgs/0/enable', 1)      # 1 = enable;   0 = disabled
ziUhf.daq.sync()

#Trigger type used. Some parameters are only valid for special trigger types.
    #0 = trigger off
    #1 = analog edge trigger on source
    #2 = digital trigger mode on DIO source
    #3 = analog pulse trigger on source
    #4 = analog tracking trigger on source
    #5 = change trigger
    #6 = hardware trigger on trigger line source
    #7 = tracking edge trigger on source
    #8 = event count trigger on counter source
    
ziUhf.daq.sync()
trigger_setting = [['dataAcquisitionModule/triggernode', '/dev2010/demods/0/sample.TrigAWGTrig3'],  # trigger node is AWG trigger number 3 
#                   ['dataAcquisitionModule/type', 2],      
                   ['dataAcquisitionModule/type', 6],                                          # this setting is related to the AWG trigger
                   ['dataAcquisitionModule/edge', 1],                                               # trigger on the positive edge. 1 = positive, 2=negative
                   ['dataAcquisitionModule/count', 1],                                              # number of trigger events to count
                   ['dataAcquisitionModule/holdoff/time', 0],                                       # hold off time
                   ['dataAcquisitionModule/holdoff/count', 0],                                      # hold off count
                   ##careful
                   ['dataAcquisitionModule/delay', 0], #0                                       # trigger delay (s)
                   ##
                   ['dataAcquisitionModule/endless', 0]]                                            # endless disabled = 0


grid_setting =    [['dataAcquisitionModule/grid/mode', 2],                          # mode. 2 = Linear interpolation 
                   ['dataAcquisitionModule/grid/cols', points],                     # number of points in the acquisition window
                   ['dataAcquisitionModule/duration', acquisition_duration],        # length of time to record (s)
                   ['dataAcquisitionModule/grid/rows', 1],                          # rows
                   ['dataAcquisitionModule/grid/direction', 0],                     # scan direction. 0 = forwardphase_pulsed = SpecialParameters.Pulsed_readout(ziUhf, repetitions, returnOnePoint=False)
                   ['dataAcquisitionModule/grid/repetitions', repetitions],         # number of repetitions for the averaging
                   ['dataAcquisitionModule/awgcontrol', 1],                         # set the AWG control
                   ['dataAcquisitionModule/save/fileformat', 1]]                    # 1 = CSV format 

phase_trig= SpecialParameters.Pulsed_readout_G1(ziUhf, repetitions, returnOnePoint=False)
#phase_pulsed_B3= Pulsed_readout_B3(ziUhf, repetitions, returnOnePoint=True)
phase_trig.setSettings(trigger_setting, grid_setting)


print('tc='+str(efftc)+'  rep='+str(repetitions))
#for symmetric pulses
#print('timeperpoint='+str(repetitions*twait()*2))
print('timeperpoint='+str(repetitions*acquisition_duration))

for i in range(1,5):
    Bfield(0.5*i)
    continuous_acquisition()
    # G1now=VG1()
    # G2now=VG2()
    # G3now=VG3()
    # G4now=VG4()
    # G5now=VG5()
    # VG3comp()
    # VG4comp()
    # # VG1onmin(G1now-60,G1now+60,801,1)
    # G1now=VG1()
    # VG1onmin(G1now-4,G1now+4,801,1)
    # G1now=VG1()
    # VG2onmin(G2now-4,G2now+4,801,1)
    # G2now=VG2()
    # VG5onmin(G5now-4,G5now+4,801,1)
    if i!=0:
        name=str(Bfield())+'T_TPC_G4vsG3_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
        # a,dataid,c,d=sweep2D(VG3comp,-800,-1000,801,0.1,VG4comp,-700,-900,801,0.01111,ph1)
        a,dataid,c,d=sweep2D(VG3comp,-937,-941,41,0.1,VG4comp,-785,-805,101,0.01111,ph1)
        # a,dataid,c,d=sweep2D(VG3comp,-939,-946,101,0.1,VG4comp,-794,-798,81,0.01777,ph1)
        plot_by_id(dataid)
        saveplot(name,dataid)
    
    for j in range(0,1):
        # VG3comp(-937+0.3*j)
        VG3comp(-936.5)
        continuous_acquisition()
        sensor_on_interdot_sweepG4comp(-802,-797,201,1)
        
        
        trigger_mode()
        ziUhf.daq.setInt('/dev2010/sigouts/1/on', 1)    
        t=np.linspace(0,2e-3,points)
        phasearray=[]
        amp=[]
        
        for k in range(0,61):
            amp.append(ampliAWG())
            ampliAWG(k*0.005)
            phasearray.append(phase_trig())
        ziUhf.daq.setInt('/dev2010/sigouts/1/on', 0)    
        
        phase=[]
        for k in range(0,61):
            phase.append(phasearray[k][0])
        
        plt.plot(phase)
        Y= amp
        X = t
        Z1=phase
        
        
        f = plt.figure()
        plt.pcolor(X,Y,Z1,cmap='viridis')
        # plt.clim(vmin=None,vmax=0.3)
        plt.colorbar(label='phi(deg)')
        plt.xlabel('t(s)')
        # plt.ylabel('pulse amplitude_pp (mV)')
        plt.ylabel('pulse amplitude_pp (AWG)')
        
        now=datetime.datetime.now()
        dayFolder=datetime.date.isoformat(now)
        name='TPC_pulsevspulse_amplitude_1000rep_B'+str(Bfield())+'T_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
        plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
        np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt''',phase)
        
        if j==0:
            ampliAWG(0.2)
            ziUhf.daq.setInt('/dev2010/sigouts/1/on', 1)    
            t=np.linspace(0,acquisition_duration,points)
            phasearray=[]
            amp=[]
            
            for k in range(0,101):
                VG4comp(-796-0.05*k)
                amp.append(VG4())
                phasearray.append(phase_trig())
            ziUhf.daq.setInt('/dev2010/sigouts/1/on', 0)    
            
            phase=[]
            for k in range(0,101):
                phase.append(phasearray[k][0])
            
            plt.plot(phase)
            Y= amp
            X = t
            Z1=phase
            
            
            f = plt.figure()
            plt.pcolor(X,Y,Z1,cmap='viridis')
            # plt.clim(vmin=None,vmax=0.3)
            plt.colorbar(label='phi(deg)')
            plt.xlabel('t(s)')
            # plt.ylabel('pulse amplitude_pp (mV)')
            plt.ylabel('VG4 (mV)')
            
            now=datetime.datetime.now()
            dayFolder=datetime.date.isoformat(now)
            name='TPC_pulsevsG4_amplitude_pp_'+str(ampliAWG()*11)+'mV_1000rep_B'+str(Bfield())+'T_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
            plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
            np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',phase)
            
            
            
            
####fit decayvsfield
def fit_double_exponential(x,*p):
       return p[2]*(np.abs(p[1])*np.exp(-x/tsinglet)+(np.abs(1-p[1]))*np.exp(-x/p[0]))   +p[3]  
   

def fit_exponential(x,*p):
     return p[1]*np.exp(-x/p[0]+ p[3]) +p[2]    
     
def fit_exponential2(x,*p):
        phimin=-0.012
        return p[1]*np.exp(-x/p[0]) +phimin#phimax-phimin)*np.exp(-x/p[0])+phimin    
   
    