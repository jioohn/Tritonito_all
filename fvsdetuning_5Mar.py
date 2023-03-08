# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 12:42:49 2021

@author: G-GRE-GRE050402
"""

######################



#####################
continuous_acquisition()
continuous_acquisition_ch2()

# Bfield(0)

mwgen.off()
#Drain detector calib in 02
rampVG3(-845)
rampVG4(-833)
VG5now=VG5()
VG2now=VG2()
VG6now=VG6()
VG1now=VG1()
VG3now=VG3()
VG4now=VG4()
# 1089_0.899T_MWon10dB_5GHz_G3vsG4COMP_G1-1672.3mV_G2-1377.1969mV_G3-845.0mV_G4-834.0mV_G5-1471.0487mV_G6-1593.2417mV2
# VG6onmin_phD(VG6now-20,VG6now+20,801,1)
VG5onmin_phD(VG5now-5,VG5now+5,401,1)


#Source detector calib in 11
VG3comp(-847)
VG4comp(-831)
VG5now=VG5()
VG2now=VG2()
VG6now=VG6()
VG1now=VG1()
VG3now=VG3()
VG4now=VG4()
# VG1onmin_phS(VG1now-20,VG1now+20,801,1)
VG2onmin_phS(VG2now-5,VG2now+5,401,1)

# mwgen.on()
# mwgen.power(16)
name=str(Bfield())+'T_G3vsG4COMP_mWoff_nom_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
a,dataid,c,d=sweep2D(VG3comp,-848,-844,51,0.05,VG4comp,-830,-834,51,0.02,ph1,ph2)
# a,dataid,c,d=sweep2D(VG3comp,-847,-845,101,0.05,VG4comp,-831,-833,101,0.02,ph1,ph2)
plot_by_id(dataid)
save2plots(name,dataid)



name=str(Bfield())+'T_G3vsG4COMP_mWoff_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
# a,dataid,c,d=sweep2D(VG3comp,-849,-846,41,0.05,VG4comp,-830,-833,41,0.015,ph1,ph2)
a,dataid,c,d=sweep2D(VG3comp,-850,-845,51,0.05,VG4comp,-829,-834,51,0.012,ph1,ph2)
plot_by_id(dataid)
save2plots(name,dataid)
plt.close()
plot_by_id(dataid)

mwgen.on()
mwgen.power(22)
name=str(Bfield())+'T_G3vsG4COMP_mWon20Db_nom_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
# a,dataid,c,d=sweep2D(VG3comp,-850,-845,51,0.05,VG4comp,-829,-834,51,0.012,ph1,ph2)
a,dataid,c,d=sweep2D(VG3comp,-847,-845,101,0.05,VG4comp,-831,-833,101,0.02,ph1,ph2)


plot2d_diff(dataid)
name=str(Bfield())+'T_G4vsG3COMP_mWon20Db_nom_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
a,dataid,c,d=sweep2D(VG4comp,-831,-833,101,0.05,VG3comp,-847,-845,101,0.02,ph1,ph2)
plot_by_id(dataid)

save2plots(name,dataid)

plot2d_diff(dataid)


VG3comp(-846)
VG4comp(-832.5)
# G4detuning(-831.75)

# Bfield(0.7)
mwgen.off()
mwgen.power(15)
ziUhf.daq.setInt('/dev2010/awgs/0/enable', 1)
ampliAWG(0.1)

name=str(Bfield())+'T_fvsdet_pulsing_P'+str(mwgen.power()-65)+'dBG1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
a,dataid,c,d=sweep2D(Bfield_Hon,0.8,0.7,21,1,mwgen.frequency,12e9,18e9,3000,0.005,ph1,ph2)
plot_by_id(dataid)
save2plots(name,dataid)




tc=0.5
# acquisition_duration =t02+tramp*2+t11+tread  # length of time to record (s)
acquisition_duration =10e-6 # length of time to record (s)
repetitions = 10            # number of repetitions for the averaging
points = 9 # number of points in the acquisition window (min=2)

#efftc=acquisition_duration/10
efftc=1e-6

# such that the effective Tc is 100ms 
# repetitions=tc/efftc/5

repetitions=400

ziUhf.daq.setInt('/dev2010/demods/0/trigger', 33554432) # demodulator trigger set on AWGtrigger2 High
ziUhf.daq.setDouble('/dev2010/demods/0/rate', 800e3)
ziUhf.daq.setDouble('/dev2010/demods/1/rate', 800e3)
ziUhf.daq.setInt('/dev2010/demods/0/order', 1)
ziUhf.daq.setDouble('/dev2010/demods/0/timeconstant', efftc)

ziUhf.daq.setInt('/dev2010/demods/1/order', 1)
ziUhf.daq.setDouble('/dev2010/demods/1/timeconstant', efftc)
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
                   ['dataAcquisitionModule/delay', 20e-6], #0                                       # trigger delay (s)
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

phase_trigS= SpecialParameters.Pulsed_readout_S(ziUhf, repetitions, returnOnePoint=True)
phase_trigD= SpecialParameters.Pulsed_readout_D(ziUhf, repetitions, returnOnePoint=True)
#phase_pulsed_B3= Pulsed_readout_B3(ziUhf, repetitions, returnOnePoint=True)
phase_trigS.setSettings(trigger_setting, grid_setting)
phase_trigD.setSettings(trigger_setting, grid_setting)

# mwgen.on()
# mwgen.power(30)

# name=str(Bfield())+'T_phS_freq_scan_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
# a,dataid,c=sweep1D(mwgen.frequency,11e9,17e9,3001,0.012,phase_trigS)
# plot_by_id(dataid)
# saveplot(name,dataid)


# name=str(Bfield())+'T_phD_freq_scan_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
# a,dataid,c=sweep1D(mwgen.frequency,13.2e9,13.8e9,1201,0.012,phase_trigD)
# plot_by_id(dataid)
# saveplot(name,dataid)

VG3comp(-845.9)
VG4comp(-832.05)

# mwgen.off()
# #test detuning
# name=str(Bfield())+'T_detuningscan_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
# a,dataid,c=sweep1D(VG4comp,-831,-833,101,0.012,ph1,ph2)
# plot_by_id(dataid)
# save2plots(name,dataid)
# plt.show()



mwgen.on()

mwgen.power(18)
ziUhf.daq.setInt('/dev2010/awgs/0/enable', 1)
ampliAWG(0.1)

name=str(Bfield())+'T_fvsBpulsing_'+str(ampliAWG())+'_AWG_Prf'+str(mwgen.power()-45)+'dB_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
a,dataid,c,d=sweep2D(Bfield_Hon,0.8,0.7,41,1,mwgen.frequency,14e9,18e9,3000,0.005,phase_trigS)
plot_by_id(dataid)
save2plots(name,dataid)




# mwgen.on()
# mwgen.power(25)
# # ziUhf.daq.setInt('/dev2010/awgs/0/enable', 1)
# ampliAWG(0.07)

# name=str(Bfield())+'T_fvsBpulsing_'+str(ampliAWG())+'_AWG_Prf'+str(mwgen.power()-45)+'dB_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
# a,dataid,c,d=sweep2D(Bfield_Hon,0.8,0.7,41,1,mwgen.frequency,16e9,13e9,2500,0.005,phase_trigD)
# plot_by_id(dataid)
# save2plots(name,dataid)



VG3comp(-845.4)
VG4comp(-831.5)
detuningPoint1 = [-845.8,-830.5]  #TPC #G3,G4
detuningPoint2 = [-845,-832.5] 
# VG3comp(detuningPoint1[0])
# VG4comp(detuningPoint1[1])
DeltaG4G3=(detuningPoint1[0]-detuningPoint2[0])/(detuningPoint1[1]-detuningPoint2[1])


G4detuning=  SpecialParameters.CompensateG4(VG4,VG3,DeltaG4G3)

Bfield(0.8)
mwgen.on()
mwgen.power(17)
name=str(Bfield())+'T_freqvsdetuning_power-10dBm_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
mwgen.on()
a,dataid,c,d=sweep2D(mwgen.frequency,13e9,18e9,5000,0.01,G4detuning,-831,-832.5,201,0.01,ph1,ph2)
plot_by_id(dataid)
save2plots(name,dataid)
