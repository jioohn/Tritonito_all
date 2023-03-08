# -*- coding: utf-8 -*-
"""
Created on Fri May  7 03:02:39 2021

@author: G-GRE-GRE050402
"""
# rampVG3(-770)
# rampVG4(-870)
# VG1(-1684)
# VG2(-1060)
# VG3(-763.5)
# VG4(-974)
# VG5(-1347)
# VG6(-1860)


# rampVG3(-768)
# rampVG4(-879)

# VG3comp(-775)
# VG4comp(-816)
# VG5now=VG5()
# VG2now=VG2()
# VG6now=VG6()
# VG1now=VG1()

# # VG6onmin_phD(VG6now-10,VG6now+10,401,1)


# # VG1onmin_phS(VG1now-10,VG1now+10,401,1)


# # VG5onmin_phD(VG5now-10,VG5now+10,401,1)
# # VG2onmin_phS(VG2now-10,VG2now+10,201,1)

# continuous_acquisition()
# continuous_acquisition_ch2()
# VG6now=VG6()
# VG1now=VG1()
# VG6onmin_phD(VG6now-3,VG6now+3,201,1)
# # VG5onmin_phD(VG5now-30,VG5now+30,201,1)

# # VG1onmin_phS(VG1now-10,VG1now+10,+2001,1)


# VG1onmin_phS(VG1now-10,VG1now+10,+201,1)

# continuous_acquisition()
# continuous_acquisition_ch2()

# name=str(Bfield())+'T_G3vsG4_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'

# a,dataid,c,d=sweep2D(VG3comp,-775,-779,31,0.02,VG4comp,-813,-816,31,0.013,ph1,ph2)
# # a,dataid,c,d=sweep2D(VG3comp,-768,-772,31,0.02,VG4comp,-876,-879,31,0.013,ph1,ph2)
# # a,dataid,c,d=sweep2D(VG3comp,-765,-780,41,0.02,VG4comp,-875,-885,41,0.013,ph1,ph2)
# plot_by_id(dataid)
# save2plots(name,dataid)
# plt.close()
# plot_by_id(dataid)


# VG3comp(-766)
# VG4comp(-976)
# VG5now=VG5()
# VG2now=VG2()
# VG6now=VG6()
# VG1now=VG1()

# # VG6onmin_phD(VG6now-10,VG6now+10,401,1)


# # VG1onmin_phS(VG1now-10,VG1now+10,401,1)


# # VG5onmin_phD(VG5now-10,VG5now+10,401,1)
# # VG2onmin_phS(VG2now-10,VG2now+10,201,1)

# continuous_acquisition()
# continuous_acquisition_ch2()
# VG6now=VG6()
# VG1now=VG1()
# # VG6onmin_phD(VG6now-30,VG6now+10,2001,1)
# # VG5onmin_phD(VG5now-10,VG5now+10,201,1)
# VG6onmin_phD(VG6now-5,VG6now+5,201,1)
# VG1onmin_phS(VG1now-5,VG1now+5,201,1)
# # VG6onmin_phD(VG6now-3,VG6now+3,201,1)


# # VG2onmin_phS(VG2now-10,VG2now+10,+201,1)

# continuous_acquisition()
# continuous_acquisition_ch2()

# name=str(Bfield())+'T_G3vsG4_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'

# a,dataid,c,d=sweep2D(VG3comp,-765,-768,31,0.02,VG4comp,-973,-976,31,0.013,ph1,ph2)
# # a,dataid,c,d=sweep2D(VG3comp,-768,-772,31,0.02,VG4comp,-876,-879,31,0.013,ph1,ph2)
# # a,dataid,c,d=sweep2D(VG3comp,-765,-780,41,0.02,VG4comp,-875,-885,41,0.013,ph1,ph2)
# plot_by_id(dataid)
# save2plots(name,dataid)
# plt.close()
# plot_by_id(dataid)


VG3comp(-869)
VG4comp(-790)
VG5now=VG5()
VG2now=VG2()
VG6now=VG6()
VG1now=VG1()

# VG6onmin_phD(VG6now-10,VG6now+10,401,1)


# VG1onmin_phS(VG1now-10,VG1now+10,401,1)


# VG5onmin_phD(VG5now-10,VG5now+10,401,1)
# VG2onmin_phS(VG2now-10,VG2now+10,201,1)

continuous_acquisition()
continuous_acquisition_ch2()
VG6now=VG6()
VG1now=VG1()

# VG1onmin_phS(VG1now-30,VG1now+30,601,1)
# VG6onmin_phD(VG6now-30,VG6now+10,2001,1)
# VG5onmin_phD(VG5now-10,VG5now+10,201,1)
VG1onmin_phS(VG1now-5,VG1now+5,201,1)
VG6onmin_phD(VG6now-5,VG6now+5,201,1)

# VG6onmin_phD(VG6now-3,VG6now+3,201,1)


# VG2onmin_phS(VG2now-10,VG2now+10,+201,1)

continuous_acquisition()
continuous_acquisition_ch2()

name=str(Bfield())+'T_G3vsG4_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'

a,dataid,c,d=sweep2D(VG3comp,-868,-874,31,0.02,VG4comp,-780,-800,31,0.013,ph1,ph2)
plot_by_id(dataid)
save2plots(name,dataid)
plt.close()
plot_by_id(dataid)



######
num_point=101
tc=5e-6
total_time=1
demod_S=2
demod_D=1
startG4=-974
stopG4=-975.4
startG3=-767
stopG3=-766.4

pathS=folder2+'\\'+dayFolder+'\\'+str(Bfield())+'_T_interdot_VG3'+str(startG3)+'_mV_VG4='+str(startG4)+'mV_phS_3'
path2S = pathS + f'/time_traces'
pathD=folder2+'\\'+dayFolder+'\\'+str(Bfield())+'_T_interdot-VG3='+str(startG3)+'_mV_VG4='+str(startG4)+'mV_phD_3'
path2D = pathD + f'/time_traces'

continuous_acquisition()
continuous_acquisition_ch2()
Threshold_S,Threshold_D=fit_interdot(startG4,stopG4,startG3,stopG3)#plot, fit and sit on interdot
######
# VG3comp(-766.66)
# VG4comp(-974.66)
# VG3comp(-865.35)
# VG4comp(-810.72)
# VG3comp(-870.8)
# VG4comp(-807.3)





VG3comp(-864.1)
VG4comp(-812.05)

ampliAWG(0.04)

acquisition_duration=400e-6
efftc=5e-6
delay=0e-6
# such that the effective Tc is 100ms 
# repetitions=tc/efftc/5

repetitions=1

ziUhf.daq.setInt('/dev2010/demods/0/trigger', 33554432) # demodulator trigger set on AWGtrigger2 High
ziUhf.daq.setDouble('/dev2010/demods/0/rate', 200e3)
ziUhf.daq.setDouble('/dev2010/demods/1/rate', 200e3)

# ziUhf.daq.setDouble('/dev2010/demods/1/rate', 2e6)
# ziUhf.daq.setDouble('/dev2010/demods/0/rate', 2e6)
ziUhf.daq.setInt('/dev2010/demods/0/order', 1)
ziUhf.daq.setInt('/dev2010/demods/1/order', 1)

points=int(acquisition_duration*ziUhf.daq.getDouble('/dev2010/demods/0/rate'))


ziUhf.daq.setDouble('/dev2010/demods/0/timeconstant', efftc)
ziUhf.daq.setDouble('/dev2010/demods/1/timeconstant', efftc)
#ziUhf.daq.setInt('/dev2365/awgs/0/enable', 1)      # 1 = enable;   0 = disabled


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

phase_trigS= SpecialParameters.Pulsed_readout_S(ziUhf, repetitions, returnOnePoint=False)
phase_trigD= SpecialParameters.Pulsed_readout_D(ziUhf, repetitions, returnOnePoint=False)

phase_trigS.setSettings(trigger_setting, grid_setting)
phase_trigD.setSettings(trigger_setting, grid_setting)

# phases_trig= SpecialParameters.Pulsed_readout_both(ziUhf, repetitions, returnOnePoint=False)
phases_trig= SpecialParameters.Pulsed_readout_both(ziUhf, repetitions, returnOnePoint=False)
phases_trig.setSettings(trigger_setting, grid_setting)
ziUhf.daq.setInt('/dev2010/awgs/0/enable', 1)    




Ntraces=100
c,data=daqtrig_S.get_data_pulseseq(acquisition_duration,delay,Ntraces)
traceavgS=[]
threshold=-0.1#rad

for i in range(0,len(data)):
    traceavgS.append(np.nanmean(data[i]))
    
Ntraces=100
c,data=daqtrig_D.get_data_pulseseq(acquisition_duration,delay,Ntraces)
traceavgD=[]
# threshold=-0.1#rad

for i in range(0,len(data)):
    traceavgD.append(np.nanmean(data[i]))
    
 
    

# s,d=phases_trig()

taxis=np.linspace(delay,acquisition_duration+delay,points)


plt.figure()

plt.plot(taxis*1e6,traceavgS, label='$\phi_{G3}$ averaged '+str(Ntraces)+' times' )
plt.plot(taxis*1e6,traceavgD, label='$\phi_{G4}$ averaged '+str(Ntraces)+' times' )

# plt.plot(taxis,phase_trigD()[0])

s,d=phases_trig()
plt.plot(taxis*1e6,s[0],label='$\phi_{G3}$')
plt.plot(taxis*1e6,d[0],label='$\phi_{G4}$')
plt.show()
plt.xlabel('$t(\mu s)$')
plt.ylabel('$\phi(rad)$')
plt.legend()
plt.title('AWG-'+str(np.round(ampliAWG()*11,3))+'mV G3/G4 ampli'+str(np.round(ziUhf.daq.getDouble('/dev2010/auxouts/0/scale')/0.15,3)))
title=str(dataid)+'_sstraces'+str(Ntraces)+'_SSvsaverages_AWG-'+str(np.round(ampliAWG(),3))+'G3ampli'+str(np.round(ziUhf.daq.getDouble('/dev2010/auxouts/0/scale'),3))+'VG3_'+str(VG3())+'mV'
plt.savefig(folder2+'\\'+dayFolder+'\\'+title+'.png')
plt.show()
np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'.txt',traceavgS)







ampliAWG(0.1)
acquisition_duration=400e-6
efftc=5e-6
delay=0e-6
# such that the effective Tc is 100ms 
# repetitions=tc/efftc/5

repetitions=1




Ntraces=100
c,data=daqtrig_S.get_data_pulseseq(acquisition_duration,delay,Ntraces)
traceavgS=[]
threshold=-0.1#rad

for i in range(0,len(data)):
    traceavgS.append(np.nanmean(data[i]))
    
Ntraces=100
c,data=daqtrig_D.get_data_pulseseq(acquisition_duration,delay,Ntraces)
traceavgD=[]
# threshold=-0.1#rad

for i in range(0,len(data)):
    traceavgD.append(np.nanmean(data[i]))
    
 
    


s,d=phases_trig()

taxis=np.linspace(delay,acquisition_duration+delay,points)


plt.figure()

plt.plot(taxis*1e6,traceavgS, label='$\phi_{G3}$ averaged '+str(Ntraces)+' times' )
plt.plot(taxis*1e6,traceavgD, label='$\phi_{G4}$ averaged '+str(Ntraces)+' times' )

# plt.plot(taxis,phase_trigD()[0])

plt.plot(taxis*1e6,s[0],label='$\phi_{G3}$')
plt.plot(taxis*1e6,d[0],label='$\phi_{G4}$')
plt.xlabel('$t(\mu s)$')
plt.ylabel('$\phi(rad)$')
plt.legend()
plt.title('AWG-'+str(np.round(ampliAWG()*11,3))+'mV G3/G4 ampli'+str(np.round(ziUhf.daq.getDouble('/dev2010/auxouts/0/scale')/0.15,3)))
title=str(dataid)+'_sstraces'+str(Ntraces)+'_SSvsaverages_AWG-'+str(np.round(ampliAWG(),3))+'G3ampli'+str(np.round(ziUhf.daq.getDouble('/dev2010/auxouts/0/scale'),3))+'VG3_'+str(VG3())+'mV'
plt.savefig(folder2+'\\'+dayFolder+'\\'+title+'.png')
plt.show()
np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'.txt',traceavgS)
plt.show()


ampliAWG(0.2)



Ntraces=100
c,data=daqtrig_S.get_data_pulseseq(acquisition_duration,delay,Ntraces)
traceavgS=[]
threshold=-0.1#rad

for i in range(0,len(data)):
    traceavgS.append(np.nanmean(data[i]))
    
Ntraces=100
c,data=daqtrig_D.get_data_pulseseq(acquisition_duration,delay,Ntraces)
traceavgD=[]
# threshold=-0.1#rad

for i in range(0,len(data)):
    traceavgD.append(np.nanmean(data[i]))
    
 
    

s,d=phases_trig()

taxis=np.linspace(delay,acquisition_duration+delay,points)


plt.figure()

plt.plot(taxis*1e6,traceavgS, label='$\phi_{G3}$ averaged '+str(Ntraces)+' times' )
plt.plot(taxis*1e6,traceavgD, label='$\phi_{G4}$ averaged '+str(Ntraces)+' times' )

# plt.plot(taxis,phase_trigD()[0])

plt.plot(taxis*1e6,s[0],label='$\phi_{G3}$')
plt.plot(taxis*1e6,d[0],label='$\phi_{G4}$')
plt.xlabel('$t(\mu s)$')
plt.ylabel('$\phi(rad)$')
plt.legend()
plt.title('AWG-'+str(np.round(ampliAWG()*11,3))+'mV G3/G4 ampli'+str(np.round(ziUhf.daq.getDouble('/dev2010/auxouts/0/scale')/0.15,3)))
title=str(dataid)+'_sstraces'+str(Ntraces)+'_SSvsaverages_AWG-'+str(np.round(ampliAWG(),3))+'G3ampli'+str(np.round(ziUhf.daq.getDouble('/dev2010/auxouts/0/scale'),3))+'VG3_'+str(VG3())+'mV'
plt.savefig(folder2+'\\'+dayFolder+'\\'+title+'.png')
plt.show()
np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'.txt',traceavgS)


ampliAWG(0.4)
acquisition_duration=400e-6

phase_trigS= SpecialParameters.Pulsed_readout_S(ziUhf, repetitions, returnOnePoint=False)
phase_trigD= SpecialParameters.Pulsed_readout_D(ziUhf, repetitions, returnOnePoint=False)

phase_trigS.setSettings(trigger_setting, grid_setting)
phase_trigD.setSettings(trigger_setting, grid_setting)

# phases_trig= SpecialParameters.Pulsed_readout_both(ziUhf, repetitions, returnOnePoint=False)
phases_trig= SpecialParameters.Pulsed_readout_both(ziUhf, repetitions, returnOnePoint=False)
phases_trig.setSettings(trigger_setting, grid_setting)
  # 1 = enable;   0 = disabled


Ntraces=100
c,data=daqtrig_S.get_data_pulseseq(acquisition_duration,delay,Ntraces)
traceavgS=[]
threshold=-0.1#rad

for i in range(0,len(data)):
    traceavgS.append(np.nanmean(data[i]))
    
Ntraces=100
c,data=daqtrig_D.get_data_pulseseq(acquisition_duration,delay,Ntraces)
traceavgD=[]
# threshold=-0.1#rad

for i in range(0,len(data)):
    traceavgD.append(np.nanmean(data[i]))
    
 
    

s,d=phases_trig()

taxis=np.linspace(delay,acquisition_duration+delay,points)


plt.figure()

plt.plot(taxis*1e6,traceavgS, label='$\phi_{G3}$ averaged '+str(Ntraces)+' times' )
plt.plot(taxis*1e6,traceavgD, label='$\phi_{G4}$ averaged '+str(Ntraces)+' times' )

# plt.plot(taxis,phase_trigD()[0])

plt.plot(taxis*1e6,s[0],label='$\phi_{G3}$')
plt.plot(taxis*1e6,d[0],label='$\phi_{G4}$')
plt.xlabel('$t(\mu s)$')
plt.ylabel('$\phi(rad)$')
plt.legend()
plt.title('AWG-'+str(np.round(ampliAWG()*11,3))+'mV G3/G4 ampli'+str(np.round(ziUhf.daq.getDouble('/dev2010/auxouts/0/scale')/0.15,3)))
title=str(dataid)+'_sstraces'+str(Ntraces)+'_SSvsaverages_AWG-'+str(np.round(ampliAWG(),3))+'G3ampli'+str(np.round(ziUhf.daq.getDouble('/dev2010/auxouts/0/scale'),3))+'VG3_'+str(VG3())+'mV'
plt.savefig(folder2+'\\'+dayFolder+'\\'+title+'.png')
plt.show()
np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'.txt',traceavgS)