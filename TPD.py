# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 11:06:37 2021

@author: G-GRE-GRE050402
"""

continuous_acquisition()
continuous_acquisition_ch2()
mwgen.off()
#Drain detector calib in 02
VG3comp(-812)
VG4comp(-807)

VG5now=VG5()
VG2now=VG2()
VG6now=VG6()
VG1now=VG1()
VG3now=VG3()
VG4now=VG4()
# 1089_0.899T_MWon10dB_5GHz_G3vsG4COMP_G1-1672.3mV_G2-1377.1969mV_G3-845.0mV_G4-834.0mV_G5-1471.0487mV_G6-1593.2417mV2
VG6onmin_phD(VG6now-10,VG6now+10,801,1)
VG5onmin_phD(VG5now-5,VG5now+5,401,1)


#Source detector calib in 1
# rampVG3(-814)
# rampVG4(-805)
VG5now=VG5()
VG2now=VG2()
VG6now=VG6()
VG1now=VG1()
VG3now=VG3()
VG4now=VG4()
VG1onmin_phS(VG1now-10,VG1now+10,801,1)
VG2onmin_phS(VG2now-5,VG2now+5,401,1)

# mwgen.on()
# mwgen.power(16)
name=str(Bfield())+'T_G3vsG4COMP_pulsing_mWoff_nom_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
# a,dataid,c,d=sweep2D(VG3comp,-812.5,-814.,151,0.05,VG4comp,-805.5,-807,151,0.02,ph1,ph2)
a,dataid,c,d=sweep2D(VG3comp,-812,-815,41,0.05,VG4comp,-804.5,-807.5,41,0.02,ph1,ph2)
plot_by_id(dataid)
save2plots(name,dataid)
plt.close()
plot_by_id(dataid)
plot2d_diff(dataid)




# Bfield(1.4)
# Bfield(0.5)
name=str(Bfield())+'T_G3vsG4COMP_mWoff_nom_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
# a,dataid,c,d=sweep2D(VG3comp,-815,-804.,41,0.05,VG4comp,-800,-810,51,0.02,ph1,ph2)
a,dataid,c,d=sweep2D(VG3comp,-800,-820,61,0.05,VG4comp,-750,-800,101,0.013,ph1,ph2)
plot_by_id(dataid)
save2plots(name,dataid)
plt.close()
plot_by_id(dataid)
plot2d_diff(dataid)



####siton interdot
VG3comp(-812.35)
VG4comp(-806.1)
continuous_acquisition()
continuous_acquisition_ch2()
sensor_on_interdot_sweepG4comp_phS(-805,807,101,1)

#### seems that there is an asymmetry on decay, acquiring full time traces

#set_triggeracquisition
trigger_mode() 
trigger_mode_ch2() 
###################

acquisition_duration = 150e-6  # length of time to record (s)
# repetitions = 1000           # number of repetitions for the averaging
points = 132# number of points in the acquisition window (min=2)

#efftc=acquisition_duration/10
efftc=2e-6

# such that the effective Tc is 100ms 
# repetitions=tc/efftc/5

repetitions=500

ziUhf.daq.setInt('/dev2010/demods/0/trigger', 33554432) # demodulator trigger set on AWGtrigger2 High
ziUhf.daq.setDouble('/dev2010/demods/0/rate', 800e3)
ziUhf.daq.setDouble('/dev2010/demods/1/rate', 800e3)
ziUhf.daq.setInt('/dev2010/demods/0/order', 1)
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
                   ['dataAcquisitionModule/delay', 0e-6], #0                                       # trigger delay (s)
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

print('tc='+str(efftc)+'  rep='+str(repetitions))
#for symmetric pulses
#print('timeperpoint='+str(repetitions*twait()*2))
print('timeperpoint='+str(repetitions*acquisition_duration))

ziUhf.daq.setInt('/dev2010/sigouts/1/on', 0)    
# ziUhf.daq.set('/module/c0p1t10p1cf0/awgModule/awg/enable', 0)
ziUhf.daq.setInt('/dev2010/awgs/0/enable', 1)
# ziUhf.daq.setInt('/dev2010/awgs/0/enable', 0)

#############################################"
# VG3comp(-812.35)
# VG4comp(-806.1)

t=np.linspace(0,acquisition_duration,points)
phaseDarray=[]
phaseSarray=[]
amp=[]

for i in range(0,201):
    # ampliAWG(i*0.005)
    ampliAWG(-0.2+i*0.002)
    amp.append(ampliAWG())
    phaseSarray.append(phase_trigS())
    phaseDarray.append(phase_trigD())
# ziUhf.daq.setInt('/dev2010/sigouts/1/on', 0)    

phaseS=[]
for i in range(0,201):
    phaseS.append(phaseSarray[i][0])
    
phaseD=[]
for i in range(0,201):
    phaseD.append(phaseDarray[i][0])

# plt.plot(phase)
Y= amp
X = t
Z1=phaseS


f = plt.figure()
plt.pcolor(X,Y,Z1,cmap='viridis')
# plt.clim(vmin=None,vmax=0.3)
plt.colorbar(label='$\phi_S$(rad)')
plt.xlabel('t(s)')
# plt.ylabel('pulse amplitude_pp (mV)')
plt.ylabel('pulse amplitude_pp (AWG)')

now=datetime.datetime.now()
dayFolder=datetime.date.isoformat(now)
name=str(Bfield())+'T_nocomponddetector_TPD_pulsevspulse_amplitude_500rep_phS'
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',phaseS)


# plt.plot(phase)
Y= amp
X = t
Z1=phaseD


f = plt.figure()
plt.pcolor(X,Y,Z1,cmap='viridis')
# plt.clim(vmin=None,vmax=0.3)
plt.colorbar(label='$\phi_D$(rad)')
plt.xlabel('t(s)')
# plt.ylabel('pulse amplitude_pp (mV)')
plt.ylabel('pulse amplitude_pp (AWG)')

now=datetime.datetime.now()
dayFolder=datetime.date.isoformat(now)
name=str(Bfield())+'T_nocompon detector__TPD_pulsevspulse_amplitude_500rep_phD'
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',phaseD)

#############################################



t=np.linspace(0,acquisition_duration,points)
phaseDarray=[]
phaseSarray=[]
amp=[]
Npoints=201
alist=np.linspace(-0.2,+0.2,Npoints)##real amplitudes in 

for i in range(0,Npoints):
    # ampliAWG(i*0.005)
    amplimV=alist[i]

    
    A=amplimV/ampliAWG()/5.5

    changeAread(namefile, A) 
    # changet11(namefile, t11) 
    # changet11(namefile, tramp) 
    run_seq('dev2010','diagonal_pulse.seqc')   
    ziUhf.daq.setInt('/dev2010/demods/1/enable', 1)
    ziUhf.daq.setInt('/dev2010/demods/0/enable', 1)
    ziUhf.daq.setInt('/dev2010/sigouts/0/enables/4', 1)
    ziUhf.daq.setInt('/dev2010/sigouts/0/enables/5', 1)

    phaseSarray.append(phase_trigS())
    phaseDarray.append(phase_trigD())
# ziUhf.daq.setInt('/dev2010/sigouts/1/on', 0)    

phaseS=[]
for i in range(0,Npoints):
    phaseS.append(phaseSarray[i][0])
    
phaseD=[]
for i in range(0,Npoints):
    phaseD.append(phaseDarray[i][0])




now=datetime.datetime.now()
dayFolder=datetime.date.isoformat(now)

#######
tag='_Elzermann3stage_'
name=tag+'phid_epsreadvstime G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV__G6'+str(VG6())+'mV'
Y= alist[0:len(phaseD)]
X = t

Z1=phaseD
Z=np.reshape(Z1,(len(Y),len(X)))


f = plt.figure()
plt.pcolor(X,Y,Z,cmap='viridis')
# plt.clim(vmin=None,vmax=0.3)
plt.colorbar(label='$\phi_D(rad)$')
plt.ylabel('$\epsilon_R$ (mV)')
# plt.ylabel('pulse amplitude_pp (mV)')
plt.xlabel('t(s)')
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',Z)




#######
# tag='_seq3stage_'
name=tag+'phiS_epsreadvstime G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV__G6'+str(VG6())+'mV'
Y= alist[0:len(phaseD)]
X = t

Z1=phaseS
Z=np.reshape(Z1,(len(Y),len(X)))


f = plt.figure()
plt.pcolor(X,Y,Z,cmap='viridis')
# plt.clim(vmin=None,vmax=0.3)
plt.colorbar(label='$\phi_S(rad)$')
plt.ylabel('$\epsilon_R$ (mV)')
# plt.ylabel('pulse amplitude_pp (mV)')
plt.xlabel('t(s)')
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',Z)


