# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 02:49:22 2021

@author: G-GRE-GRE050402
"""
def plotmeta():    
    acquisition_duration =40e-6  # length of time to record (s)
    repetitions = 1000         # number of repetitions for the averaging
    delay=200e-6
    
    efftc=4e-6
    ziUhf.daq.setDouble('/dev2010/demods/1/rate', 400e3)
    ziUhf.daq.setDouble('/dev2010/demods/0/rate', 400e3)
    # ziUhf.daq.setDouble('/dev2010/demods/1/rate', 1e6)
    # ziUhf.daq.setDouble('/dev2010/demods/0/rate', 1e6)
    
    
    repetitions=200
    
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
    
    
    
    
    
    name=str(Bfield())+'T_METASTABLE__acquire30usin02_delay'+str(delay)+'_G3vsG4comp_AWG'+str(np.round(ampliAWG(),3))+'_VG3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G3overG4ampli'+str(np.round(ziUhf.daq.getDouble('/dev2010/auxouts/0/scale')/ziUhf.daq.getDouble('/dev2010/auxouts/1/scale'),3))
    a,dataid,c,d=sweep2D(VG3comp,-857,-850,51,0.02,VG4comp,-804,-797,51,0.02,phase_trigS,phase_trigD)
    
    plot_by_id(dataid)
    save2plots(name,dataid)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # acquisition_duration =50e-6  # length of time to record (s)
    
    # delay=0e-6
    
    # # efftc=500e-9
    # # ziUhf.daq.setDouble('/dev2010/demods/1/rate', 4e6)
    # # ziUhf.daq.setDouble('/dev2010/demods/0/rate', 4e6)
    # efftc=4e-6
    # ziUhf.daq.setDouble('/dev2010/demods/1/rate', 400e3)
    # ziUhf.daq.setDouble('/dev2010/demods/0/rate', 400e3)
    
    
    # repetitions=200
    
    # ziUhf.daq.setInt('/dev2010/demods/1/trigger', 33554432) # demodulator trigger set on AWGtrigger2 High
    # ziUhf.daq.setInt('/dev2010/demods/0/trigger', 33554432) # demodulator trigger set on AWGtrigger2 High
    
    # ziUhf.daq.setInt('/dev2010/demods/1/order', 1)
    # ziUhf.daq.setInt('/dev2010/demods/0/order', 1)
    # points=int(acquisition_duration*ziUhf.daq.getDouble('/dev2010/demods/0/rate'))
    # # points=3
    
    # ziUhf.daq.setDouble('/dev2010/demods/0/timeconstant', efftc)
    # ziUhf.daq.setDouble('/dev2010/demods/1/timeconstant', efftc)
    # #ziUhf.daq.setInt('/dev2365/awgs/0/enable', 1)      # 1 = enable;   0 = disabled
    # #add also check if meas start, otherwise restart AWG
    # ziUhf.daq.sync()
    
    # #Trigger type used. Some parameters are only valid for special trigger types.
    #     #0 = trigger off
    #     #1 = analog edge trigger on source
    #     #2 = digital trigger mode on DIO source
    #     #3 = analog pulse trigger on source
    #     #4 = analog tracking trigger on source
    #     #5 = change trigger
    #     #6 = hardware trigger on trigger line source
    #     #7 = tracking edge trigger on source
    #     #8 = event count trigger on counter source
        
    # ziUhf.daq.sync()
    # trigger_setting = [['dataAcquisitionModule/triggernode', '/dev2010/demods/0/sample.TrigAWGTrig3'],  # trigger node is AWG trigger number 3 
    # #                   ['dataAcquisitionModule/type', 2],      
    #                    ['dataAcquisitionModule/type', 6],                                          # this setting is related to the AWG trigger
    #                    ['dataAcquisitionModule/edge', 1],                                               # trigger on the positive edge. 1 = positive, 2=negative
    #                    ['dataAcquisitionModule/count', 1],                                              # number of trigger events to count
    #                    ['dataAcquisitionModule/holdoff/time', 0],                                       # hold off time
    #                    ['dataAcquisitionModule/holdoff/count', 0],                                      # hold off count
    #                    ##careful
    #                    ['dataAcquisitionModule/delay', delay], #0                                       # trigger delay (s)
    #                    ##
    #                    ['dataAcquisitionModule/endless', 0]]                                            # endless disabled = 0
    
    
    # grid_setting =    [['dataAcquisitionModule/grid/mode', 2],                          # mode. 2 = Linear interpolation 
    #                    ['dataAcquisitionModule/grid/cols', points],                     # number of points in the acquisition window
    #                    ['dataAcquisitionModule/duration', acquisition_duration],        # length of time to record (s)
    #                    ['dataAcquisitionModule/grid/rows', 1],                        # rows
    #                    ['dataAcquisitionModule/grid/direction', 0],                     # scan direction. 0 = forwardphase_pulsed = SpecialParameters.Pulsed_readout(ziUhf, repetitions, returnOnePoint=False)
    #                    ['dataAcquisitionModule/grid/repetitions', repetitions],         # number of repetitions for the averaging
    #                    ['dataAcquisitionModule/awgcontrol', 1],                         # set the AWG control
    #                    ['dataAcquisitionModule/save/fileformat', 1]]                    # 1 = CSV format 
    
    # phase_trigS= SpecialParameters.Pulsed_readout_S(ziUhf, repetitions, returnOnePoint=True)
    # phase_trigD= SpecialParameters.Pulsed_readout_D(ziUhf, repetitions, returnOnePoint=True)
    
    # phase_trigS.setSettings(trigger_setting, grid_setting)
    # phase_trigD.setSettings(trigger_setting, grid_setting)
    
    # ziUhf.daq.setInt('/dev2010/sigouts/0/enables/5', 1)
    # ziUhf.daq.setInt('/dev2010/sigouts/0/enables/4', 1)
    
    
    
    # print('tc='+str(efftc)+'  rep='+str(repetitions))
    # #for symmetric pulses
    # #print('timeperpoint='+str(repetitions*twait()*2))
    # print('timeperpoint='+str(repetitions*acquisition_duration))
    
    # # ziUhf.daq.setInt('/dev2010/sigouts/1/on', 0)    
    # ziUhf.daq.setInt('/dev2010/sigouts/0/enables/4', 1)
    # ziUhf.daq.setInt('/dev2010/sigouts/0/enables/5', 1)
    # # ziUhf.daq.setInt('/dev2010/sigouts/0/on', 0)    
    # # ziUhf.daq.set('/module/c0p1t10p1cf0/awgModule/awg/enable', 0)
    # ziUhf.daq.setInt('/dev2010/awgs/0/enable', 1)
    # # ziUhf.daq.setInt('/dev2010/awgs/0/enable', 0)
    
    
    
    
    
    # name=str(Bfield())+'T_phiS_METASTABLE_acquire50usin02_delay'+str(delay)+'_G3vsG4comp_AWG'+str(ampliAWG())+'_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G5'+str(VG5())+'mV'
    # a,dataid,c,d=sweep2D(VG3comp,-863.5,-867,31,0.02,VG4comp,-807,-811,31,0.02,phase_trigS,phase_trigD)
    
    # plot_by_id(dataid)
    # save2plots(name,dataid)


# ampliAWG(0.1)
# plotmeta()
# ampliAWG(0.2)
# plotmeta()

ampliAWG(0.2)
plotmeta()


VG4comp(-801)
VG3comp(-853)
VG6now=VG6()
VG1now=VG1()
continuous_acquisition()
continuous_acquisition_ch2()
VG6onmin_phD(VG6now-2,VG6now+2,601,1)
VG1onmin_phS(VG1now-2,VG1now+2,601,1)

ampliAWG(0.4)
plotmeta()

ziUhf.daq.setDouble('/dev2010/auxouts/0/scale', 0.15)
ziUhf.daq.setDouble('/dev2010/auxouts/1/scale', 0.15*0.2)
ziUhf.daq.setDouble('/dev2010/auxouts/2/scale', -0.03)
ziUhf.daq.setDouble('/dev2010/auxouts/3/scale', -0.03*0.2)
VG4comp(-801)
VG3comp(-853)
VG6now=VG6()
VG1now=VG1()
continuous_acquisition()
continuous_acquisition_ch2()
VG6onmin_phD(VG6now-2,VG6now+2,601,1)
VG1onmin_phS(VG1now-2,VG1now+2,601,1)

ampliAWG(0.2)
plotmeta()
VG4comp(-801)
VG3comp(-853)
VG6now=VG6()
VG1now=VG1()
continuous_acquisition()
continuous_acquisition_ch2()
VG6onmin_phD(VG6now-2,VG6now+2,601,1)
VG1onmin_phS(VG1now-2,VG1now+2,601,1)

ampliAWG(0.4)
plotmeta()







ziUhf.daq.setDouble('/dev2010/auxouts/0/scale', 0.15)
ziUhf.daq.setDouble('/dev2010/auxouts/1/scale', 0.15*0.5)
ziUhf.daq.setDouble('/dev2010/auxouts/2/scale', -0.03)
ziUhf.daq.setDouble('/dev2010/auxouts/3/scale', -0.03*0.5)

VG4comp(-801)
VG3comp(-853)
VG6now=VG6()
VG1now=VG1()
continuous_acquisition()
continuous_acquisition_ch2()
VG6onmin_phD(VG6now-2,VG6now+2,601,1)
VG1onmin_phS(VG1now-2,VG1now+2,601,1)

plotmeta()
VG4comp(-801)
VG3comp(-853)
VG6now=VG6()
VG1now=VG1()
continuous_acquisition()
continuous_acquisition_ch2()
VG6onmin_phD(VG6now-2,VG6now+2,601,1)
VG1onmin_phS(VG1now-2,VG1now+2,601,1)

ampliAWG(0.2)
VG4comp(-801)
VG3comp(-853)
VG6now=VG6()
VG1now=VG1()
continuous_acquisition()
continuous_acquisition_ch2()
VG6onmin_phD(VG6now-2,VG6now+2,601,1)
VG1onmin_phS(VG1now-2,VG1now+2,601,1)

plotmeta()
VG4comp(-801)
VG3comp(-853)
VG6now=VG6()
VG1now=VG1()
continuous_acquisition()
continuous_acquisition_ch2()
VG6onmin_phD(VG6now-2,VG6now+2,601,1)
VG1onmin_phS(VG1now-2,VG1now+2,601,1)

ampliAWG(0.4)
plotmeta()







