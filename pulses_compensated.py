# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 18:21:35 2021

@author: G-GRE-GRE050402
"""

slopeG3G2=-0.30199999999999816
slopeG4G2=-0.022000000000025464
slopeG3G5=-0.013999999999987267
slopeG4G5=-0.21200000000003455




#########################################"

VG3comp(-847.3)
sensor_on_interdot_sweepG4comp_phD(-832,-830,201,1)
#######################################################

#set_triggeracquisition
trigger_mode() 
trigger_mode_ch2() 
tc=0.10
acquisition_duration = 150e-6  # length of time to record (s)
repetitions = 100            # number of repetitions for the averaging
points = 66 # number of points in the acquisition window (min=2)

#efftc=acquisition_duration/10
efftc=2e-6

# such that the effective Tc is 100ms 
# repetitions=tc/efftc/5

repetitions=100

ziUhf.daq.setInt('/dev2010/demods/0/trigger', 33554432) # demodulator trigger set on AWGtrigger2 High
ziUhf.daq.setDouble('/dev2010/demods/0/rate', 400e3)
ziUhf.daq.setDouble('/dev2010/demods/1/rate', 400e3)
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

print('tc='+str(efftc)+'  rep='+str(repetitions))
#for symmetric pulses
#print('timeperpoint='+str(repetitions*twait()*2))
print('timeperpoint='+str(repetitions*acquisition_duration))

ziUhf.daq.setInt('/dev2010/sigouts/1/on', 0)    
# ziUhf.daq.set('/module/c0p1t10p1cf0/awgModule/awg/enable', 0)
ziUhf.daq.setInt('/dev2010/awgs/0/enable', 1)
# ziUhf.daq.setInt('/dev2010/awgs/0/enable', 0)

t=np.linspace(0,acquisition_duration,points)
phaseDarray=[]
phaseSarray=[]
amp=[]
Npoints=100
for i in range(0,Npoints):
    ampliAWG(0.01+i*0.005)
    amp.append(ampliAWG())

    phaseSarray.append(phase_trigS())
    phaseDarray.append(phase_trigD())
# ziUhf.daq.setInt('/dev2010/sigouts/1/on', 0)    

phaseS=[]
for i in range(0,Npoints):
    phaseS.append(phaseSarray[i][0])
    
phaseD=[]
for i in range(0,Npoints):
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
name=str(dataid)+'_'+str(Bfield())+'T_TPC_pulsevspulse_amplitude_100rep_phS'
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
name=str(dataid)+'_'+str(Bfield())+'T_TPC_pulsevspulse_amplitude_100rep_phD'
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',phaseD)



#####################################pulses with rf applied
mwgen.on()
mwgen.trigpulses(0)
ampliAWG(0.2)
t=np.linspace(0,acquisition_duration,points)
phaseDarray=[]
phaseSarray=[]
amp=[]
Npoints=10000
ampliAWG=0.1
for i in range(0,Npoints):

    mwgen.frequency(0.01+i*0.005)
    amp.append(ampliAWG())

    phaseSarray.append(phase_trigS())
    # phaseDarray.append(phase_trigD())
# ziUhf.daq.setInt('/dev2010/sigouts/1/on', 0)    

phaseS=[]
for i in range(0,Npoints):
    phaseS.append(phaseSarray[i][0])
    
# phaseD=[]
# for i in range(0,Npoints):
#     phaseD.append(phaseDarray[i][0])

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
name=str(dataid)+'_'+str(Bfield())+'T_TPC_pulsevspulse_amplitude_100rep_phS'
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',phaseS)


# # plt.plot(phase)
# Y= amp
# X = t
# Z1=phaseD


# f = plt.figure()
# plt.pcolor(X,Y,Z1,cmap='viridis')
# # plt.clim(vmin=None,vmax=0.3)
# plt.colorbar(label='$\phi_D$(rad)')
# plt.xlabel('t(s)')
# # plt.ylabel('pulse amplitude_pp (mV)')
# plt.ylabel('pulse amplitude_pp (AWG)')

# now=datetime.datetime.now()
# dayFolder=datetime.date.isoformat(now)
# name=str(dataid)+'_'+str(Bfield())+'T_TPC_pulsevspulse_amplitude_100rep_phD'
# plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
# np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',phaseD)




    

