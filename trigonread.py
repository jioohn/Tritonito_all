# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 22:05:16 2021

@author: G-GRE-GRE050402
"""


continuous_acquisition()
continuous_acquisition_ch2()
name=str(Bfield())+'T_G4vsG5_N4to5_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
a,dataid,c,d=sweep2D(VG5,-1201,-1197,61,0.05,VG4,-819,-816,61,0.01,ph1)
plot_by_id(dataid)
saveplot(name,dataid)

VG5onmin_phD(-1201,-1198,201,1)




trigger_mode() 
trigger_mode_ch2() 
###################

acquisition_duration = 40e-6  # length of time to record (s)
# repetitions = 1000           # number of repetitions for the averaging
# points = 71# number of points in the acquisition window (min=2)
points=264
#efftc=acquisition_duration/10
efftc=1e-6

# such that the effective Tc is 100ms 
# repetitions=tc/efftc/5

repetitions=2000

ziUhf.daq.setInt('/dev2010/demods/0/trigger', 33554432) # demodulator trigger set on AWGtrigger2 High
# ziUhf.daq.setDouble('/dev2010/demods/0/rate', 800e3)
# ziUhf.daq.setDouble('/dev2010/demods/1/rate', 800e3)
# ziUhf.daq.setDouble('/dev2010/demods/0/rate', 2e6)
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



#############################################

namefile='C:\\Users\\g-gre-gre050402\\Documents\\Zurich Instruments\\LabOne\\WebServer\\awg\\src\\pulse_triggerdata_transfer.seqc'
# namefile='C:\\Users\\g-gre-gre050402\\Documents\\Zurich Instruments\\LabOne\\WebServer\\awg\\src\\diagonal_pulse.seqc'

t=np.linspace(0,acquisition_duration,points)
phaseDarray=[]
phaseSarray=[]
amp=[]
Npoints=101
alist=np.linspace(-0.3,+0.1,Npoints)##real amplitudes in 

for i in range(0,Npoints):

    amplimV=alist[i]

    
    A=amplimV/ampliAWG()/5.5

    changeAread(namefile, A) 
    # changet11(namefile, t11) 
    # changet11(namefile, tramp) 
    run_seq('dev2010','pulse_triggerdata_transfer.seqc')   
    # run_seq('dev2010','diagonal_pulse.seqc')   
    ziUhf.daq.setInt('/dev2010/demods/1/enable', 1)
    ziUhf.daq.setInt('/dev2010/demods/0/enable', 1)
    ziUhf.daq.setInt('/dev2010/sigouts/0/enables/4', 1)
    ziUhf.daq.setInt('/dev2010/sigouts/0/enables/5', 1)

    # phaseSarray.append(phase_trigS())
    phaseDarray.append(phase_trigD())
# ziUhf.daq.setInt('/dev2010/sigouts/1/on', 0)    

# phaseS=[]
# for i in range(0,Npoints):
#     phaseS.append(phaseSarray[i][0])
    
phaseD=[]
for i in range(0,Npoints):
    phaseD.append(phaseDarray[i][0])




now=datetime.datetime.now()
dayFolder=datetime.date.isoformat(now)

#######
tag='_Elzermann3stage_awg0p2_otherlead'


#######
# tag='_seq3stage_'
name=tag+'phiD-__epsreadvstime G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV__G6'+str(VG6())+'mV'
Y= alist[0:len(phaseS)]
X = t

Z=phaseD
# Z=np.reshape(Z1,(len(Y),len(X)))


f = plt.figure()
plt.pcolor(X,Y,Z,cmap='viridis')
# plt.clim(vmin=None,vmax=0.3)
plt.colorbar(label='$\phi_D(rad)$')
plt.ylabel('$\epsilon_R$ (mV)')
# plt.ylabel('pulse amplitude_pp (mV)')
plt.xlabel('t(s)')
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',Z)