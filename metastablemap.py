# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 15:52:28 2021

@author: G-GRE-GRE050402
"""

name='fakegatevstime_tot_time30min'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
a,dataid,c=sweep1D(VGfake,0,100,1800,1,ph1,ph2)

plot_by_id(dataid)
save2plots(name,dataid)





rampVG3(-895)
rampVG4(-835)
VG5now=VG5()
VG2now=VG2()
VG6now=VG6()
VG1now=VG1()

# VG6onmin_phD(VG6now-10,VG6now+10,401,1)
VG5onmin_phD(VG5now-2.5,VG5now+2.5,401,1)

# VG1onmin_phS(VG1now-10,VG1now+10,401,1)
VG2onmin_phS(VG2now-2.5,VG2now+2.5,401,1)

name='G3compvsG4comp_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
a,dataid,c,d=sweep2D(VG3comp,-880,-900,51,0.02,VG4comp,-790,-840,51,0.012,ph1,ph2)

plot_by_id(dataid)
save2plots(name,dataid)


Bfield(0)
VG3comp(-892)
VG4comp(-825)
VG5onmin_phD(VG5now-40,VG5now+40,401,1)

# VG1onmin_phS(VG1now-10,VG1now+10,401,1)
VG2onmin_phS(VG2now-40,VG2now+40,401,1)

# ziUhf.daq.setInt('/dev2010/awgs/0/enable', 1)
name='G3compvsG4compcontinuoum_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
a,dataid,c,d=sweep2D(VG3comp,-891,-896,41,0.02,VG4comp,-823,-828,41,0.01,ph1,ph2)

plot_by_id(dataid)
save2plots(name,dataid)
plt.close()
plot_by_id(dataid)


 
# if time_traces == True:
#     #Enregistre les times traces dans un sous dossier time_traces qui seront a post traité dans la partie suivante     
#     path3 = pathh + f'/time_traces'
#     #pas de 2microVolt donc haute résolution 
#     nb_elements=51
#     # def register_time_trace(DAM,start,stop,num_point,tc,total_time,demod,path,coeff_dir)
    
#     # path_ex=register_time_trace(daq,-0.2,0.2,nb_elements,1e-5,3,1,path3,a)#300k repetitions like this
    
#     path_ex=register_time_trace(daq,-0.6,0.6,nb_elements,1e-5,4,1,path3,a)
    
#  #Post traitement des gammas rates et de la probabilité d'occupation dans le dot 
# # Threshold2=5
#     gammarate=analyse_time_traces(pathh,-0.6,0.6,Threshold,str(round(j,3)),str(round(i,3)))
  
#     Gamma.append(gammarate)




####prepare metastable maps


acquisition_duration =50e-6  # length of time to record (s)
repetitions = 1000         # number of repetitions for the averaging
delay=100e-6

efftc=4e-6
ziUhf.daq.setDouble('/dev2010/demods/1/rate', 4e6)
ziUhf.daq.setDouble('/dev2010/demods/0/rate', 4e6)
# ziUhf.daq.setDouble('/dev2010/demods/1/rate', 1e6)
# ziUhf.daq.setDouble('/dev2010/demods/0/rate', 1e6)


repetitions=500

ziUhf.daq.setInt('/dev2010/demods/1/trigger', 33554432) # demodulator trigger set on AWGtrigger2 High
ziUhf.daq.setInt('/dev2010/demods/0/trigger', 33554432) # demodulator trigger set on AWGtrigger2 High

ziUhf.daq.setInt('/dev2010/demods/1/order', 1)
ziUhf.daq.setInt('/dev2010/demods/0/order', 1)
points=int(acquisition_duration*ziUhf.daq.getDouble('/dev2010/demods/0/rate'))
# points=3

ziUhf.daq.setDouble('/dev2010/demods/0/timeconstant', efftc)
ziUhf.daq.setDouble('/dev2010/demods/1/timeconstant', efftc)
#ziUhf.daq.setInt('/dev2365/awgs/0/enable', 1)      # 1 = enable;   0 = disabled
#add also check if meas start, otherwise restart AWG
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
                   ['dataAcquisitionModule/delay', delay], #0                                       # trigger delay (s)
                   ##
                   ['dataAcquisitionModule/endless', 0]]                                            # endless disabled = 0


grid_setting =    [['dataAcquisitionModule/grid/mode', 2],                          # mode. 2 = Linear interpolation 
                   ['dataAcquisitionModule/grid/cols', points],                     # number of points in the acquisition window
                   ['dataAcquisitionModule/duration', acquisition_duration],        # length of time to record (s)
                   ['dataAcquisitionModule/grid/rows', 1],                        # rows
                   ['dataAcquisitionModule/grid/direction', 0],                     # scan direction. 0 = forwardphase_pulsed = SpecialParameters.Pulsed_readout(ziUhf, repetitions, returnOnePoint=False)
                   ['dataAcquisitionModule/grid/repetitions', repetitions],         # number of repetitions for the averaging
                   ['dataAcquisitionModule/awgcontrol', 1],                         # set the AWG control
                   ['dataAcquisitionModule/save/fileformat', 1]]                    # 1 = CSV format 

phase_trigS= SpecialParameters.Pulsed_readout_S(ziUhf, repetitions, returnOnePoint=True)
phase_trigD= SpecialParameters.Pulsed_readout_D(ziUhf, repetitions, returnOnePoint=True)

phase_trigS.setSettings(trigger_setting, grid_setting)
phase_trigD.setSettings(trigger_setting, grid_setting)

ziUhf.daq.setInt('/dev2010/sigouts/0/enables/5', 1)
ziUhf.daq.setInt('/dev2010/sigouts/0/enables/4', 1)



print('tc='+str(efftc)+'  rep='+str(repetitions))
#for symmetric pulses
#print('timeperpoint='+str(repetitions*twait()*2))
print('timeperpoint='+str(repetitions*acquisition_duration))

# ziUhf.daq.setInt('/dev2010/sigouts/1/on', 0)    
ziUhf.daq.setInt('/dev2010/sigouts/0/enables/4', 1)
ziUhf.daq.setInt('/dev2010/sigouts/0/enables/5', 1)
# ziUhf.daq.setInt('/dev2010/sigouts/0/on', 0)    
# ziUhf.daq.set('/module/c0p1t10p1cf0/awgModule/awg/enable', 0)
ziUhf.daq.setInt('/dev2010/awgs/0/enable', 1)
# ziUhf.daq.setInt('/dev2010/awgs/0/enable', 0)





name=str(Bfield())+'T_phiS_METASTABLE_acquire1usin02_delay'+str(delay)+'_G3vsG4comp_AWG'+str(ampliAWG())+'_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G5'+str(VG5())+'mV'
a,dataid,c,d=sweep2D(VG3comp,-861,-865,81,0.02,VG4comp,-809,-813.2,81,0.02,phase_trigS,phase_trigD)

plot_by_id(dataid)
save2plots(name,dataid)


















acquisition_duration =50e-6  # length of time to record (s)

delay=0e-6

# efftc=500e-9
ziUhf.daq.setDouble('/dev2010/demods/1/rate', 4e6)
ziUhf.daq.setDouble('/dev2010/demods/0/rate', 4e6)
efftc=4e-6
# ziUhf.daq.setDouble('/dev2010/demods/1/rate', 400e3)
# ziUhf.daq.setDouble('/dev2010/demods/0/rate', 400e3)


repetitions=500

ziUhf.daq.setInt('/dev2010/demods/1/trigger', 33554432) # demodulator trigger set on AWGtrigger2 High
ziUhf.daq.setInt('/dev2010/demods/0/trigger', 33554432) # demodulator trigger set on AWGtrigger2 High

ziUhf.daq.setInt('/dev2010/demods/1/order', 1)
ziUhf.daq.setInt('/dev2010/demods/0/order', 1)
points=int(acquisition_duration*ziUhf.daq.getDouble('/dev2010/demods/0/rate'))
# points=3

ziUhf.daq.setDouble('/dev2010/demods/0/timeconstant', efftc)
ziUhf.daq.setDouble('/dev2010/demods/1/timeconstant', efftc)
#ziUhf.daq.setInt('/dev2365/awgs/0/enable', 1)      # 1 = enable;   0 = disabled
#add also check if meas start, otherwise restart AWG
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
                   ['dataAcquisitionModule/delay', delay], #0                                       # trigger delay (s)
                   ##
                   ['dataAcquisitionModule/endless', 0]]                                            # endless disabled = 0


grid_setting =    [['dataAcquisitionModule/grid/mode', 2],                          # mode. 2 = Linear interpolation 
                   ['dataAcquisitionModule/grid/cols', points],                     # number of points in the acquisition window
                   ['dataAcquisitionModule/duration', acquisition_duration],        # length of time to record (s)
                   ['dataAcquisitionModule/grid/rows', 1],                        # rows
                   ['dataAcquisitionModule/grid/direction', 0],                     # scan direction. 0 = forwardphase_pulsed = SpecialParameters.Pulsed_readout(ziUhf, repetitions, returnOnePoint=False)
                   ['dataAcquisitionModule/grid/repetitions', repetitions],         # number of repetitions for the averaging
                   ['dataAcquisitionModule/awgcontrol', 1],                         # set the AWG control
                   ['dataAcquisitionModule/save/fileformat', 1]]                    # 1 = CSV format 

phase_trigS= SpecialParameters.Pulsed_readout_S(ziUhf, repetitions, returnOnePoint=True)
phase_trigD= SpecialParameters.Pulsed_readout_D(ziUhf, repetitions, returnOnePoint=True)

phase_trigS.setSettings(trigger_setting, grid_setting)
phase_trigD.setSettings(trigger_setting, grid_setting)

ziUhf.daq.setInt('/dev2010/sigouts/0/enables/5', 1)
ziUhf.daq.setInt('/dev2010/sigouts/0/enables/4', 1)



print('tc='+str(efftc)+'  rep='+str(repetitions))
#for symmetric pulses
#print('timeperpoint='+str(repetitions*twait()*2))
print('timeperpoint='+str(repetitions*acquisition_duration))

# ziUhf.daq.setInt('/dev2010/sigouts/1/on', 0)    
ziUhf.daq.setInt('/dev2010/sigouts/0/enables/4', 1)
ziUhf.daq.setInt('/dev2010/sigouts/0/enables/5', 1)
# ziUhf.daq.setInt('/dev2010/sigouts/0/on', 0)    
# ziUhf.daq.set('/module/c0p1t10p1cf0/awgModule/awg/enable', 0)
ziUhf.daq.setInt('/dev2010/awgs/0/enable', 1)
# ziUhf.daq.setInt('/dev2010/awgs/0/enable', 0)





name=str(Bfield())+'T_phiS_METASTABLE_acquire50usinN,M+1_delay'+str(delay)+'_G3vsG4comp_AWG'+str(ampliAWG())+'_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G5'+str(VG5())+'mV'
a,dataid,c,d=sweep2D(VG3comp,-859,-864,81,0.02,VG4comp,-806,-811,81,0.02,phase_trigS,phase_trigD)

plot_by_id(dataid)
save2plots(name,dataid)
