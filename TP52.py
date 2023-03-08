# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 12:22:55 2020

@author: G-GRE-GRE050402
"""

slopeG3G2=-0.16799999999996848
slopeG4G2=-0.018666666666680005
# rampVG5(-2000)

rampVG5(-1530)

# Bfield(0)
bias()
VG4comp(-780)
VG3comp(-871)
rampVG1(-1490.1)
rampVG2(-1137.2)
# rampVG5(0)
# VG1(-1490)
# VG2(-1135)

continuous_acquisition()

ziUhf.daq.setInt('/dev2010/sigouts/1/on', 0)
G1now=VG1()
G2now=VG2()
G3now=VG3()
G4now=VG4()
G5now=VG5()
VG3comp()
VG4comp()
# VG1onmin(G1now-10,G1now+10,801,1)
G1now=VG1()
VG1onmin(G1now-4,G1now+4,801,1)
G1now=VG1()
VG2onmin(G2now-4,G2now+4,801,1)
G2now=VG2()
# VG5onmin_ph2(G5now-10,G5now+10,801,1)
G5now=VG5()

continuous_acquisition()
name=str(Bfield())+'G4vsG3_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'

# a,dataid,c,d=sweep2D(VG3comp,-880,-1000,101,0.1,VG4comp,-900,-1000,101,0.01111,ph1,ph2)
a,dataid,c,d=sweep2D(VG3comp,-850,-900,51,0.02,VG4comp,-750,-800,101,0.01,ph1)
# a,dataid,c,d=sweep2D(VG3comp,-874,-867,41,0.01,VG4comp,-795,-809,141,0.01,ph1)
# a,dataid,c,d=sweep2D(VG3comp,-871,-869.5,101,0.01,VG4comp,-806,-808,101,0.01,ph1)
# a,dataid,c,d=sweep2D(VG3comp,-868,-880,121,0.1,VG4comp,-750,-850,201,0.02,ph1)
plot_by_id(dataid)
saveplot(name,dataid)


#########################
continuous_acquisition()
VG3comp(-872.65)
sensor_on_interdot_sweepG4comp(-768,-769.5,201,1)
#########################
tc=0.10
acquisition_duration =600e-6  # length of time to record (s)
repetitions = 10            # number of repetitions for the averaging
points = 132 # number of points in the acquisition window (min=2)

#efftc=acquisition_duration/10
efftc=5e-6

# such that the effective Tc is 100ms 
# repetitions=tc/efftc/5

repetitions=400

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
                   ['dataAcquisitionModule/delay', -5e-6], #0                                       # trigger delay (s)
                   #7
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



trigger_mode()
ziUhf.daq.setInt('/dev2010/sigouts/1/on', 1)    
t=np.linspace(0,acquisition_duration,points)
phasearray=[]
amp=[]


for i in range(0,51):
    ampliAWG(-0.25+i*0.01)
    amp.append(ampliAWG())
    phasearray.append(phase_trig())
ziUhf.daq.setInt('/dev2010/sigouts/1/on', 0)    

phase=[]
for i in range(0,51):
    phase.append(phasearray[i][0])

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
name=str(Bfield())+'T_TP5_pulsevspulse_amplitude_300rep_B'+str(Bfield())+'T_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV'
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',phase)



######
#ss analysis
acquisition_duration =1000e-6  # length of time to record (s)
points =220# number of points in the acquisition window (min=2)


efftc=5e-6

repetitions=1

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
                   ['dataAcquisitionModule/delay', -5e-6], #0                                       # trigger delay (s)
                   #7
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


ampliAWG(0.18)
taxis=np.linspace(0,acquisition_duration*1e6,points)
phase_ss=phase_trig()[0]
# threshold=-2.5095
phase_ss_smooth=scipy.signal.savgol_filter(phase_ss,11, 3)
# marker=0
# for k in range(20,len(phase_ss_smooth)):

#     if phase_ss_smooth[k]<threshold and marker==0:
#      decaytime=taxis[k]
#      marker=1

fig, ax = plt.subplots()

ax.set_ylabel('$\phi$(rad)',fontsize=fontSize)
ax.set_xlabel('time ($\mu$s) ',fontsize=fontSize)
plt.plot(taxis,phase_ss,label='original')
plt.plot(taxis,phase_ss_smooth,label='smooth')

plt.legend()

name='TP52_single_shot_trace_App'+str(ampliAWG()*11)+'mV_B'+str(Bfield())+'T_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV' 

plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')

np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',phase_ss)    

def step_detection(phase_ss,taxis):
    # https://stackoverflow.com/questions/48000663/step-detection-in-one-dimensional-data
    
    ####understand this stepfunction
    step=2
    ###
    dary = np.array(phase_ss)
    
    dary -= np.average(dary)
    
    step = np.hstack((np.ones(len(dary)), -1*np.ones(len(dary))))
    
    dary_step = np.convolve(dary, step, mode='valid')
    
    # get the peak of the convolution, its index
    
    step_indx = np.argmax(np.abs(dary_step))
    # yes, cleaner than np.where(dary_step == dary_step.max())[0][0]
    
    # plots
    fig, ax = plt.subplots()
    plt.plot(taxis,dary)
    
    plt.plot(taxis,dary_step[0:-1]/10)
    # plt.plot(taxis,phase_ss)
    plt.plot((taxis[step_indx], taxis[step_indx]), (dary_step[step_indx]/10, 0), 'r')
    ax.set_ylabel('$\phi$(rad)',fontsize=fontSize)
    ax.set_xlabel('time ($\mu$s) ',fontsize=fontSize)
    # plt.savefig(folder2+'\\'+dayFolder+'\\stepdetection.png')
    # if step_indx==len(taxis):
    #     step_indx=len(taxis)-1
    return(taxis[step_indx-1])

ampliAWG(0.1)
taxis=np.linspace(0,acquisition_duration*1e6,points)
decay02_array=[]
for k in range(0,5000):
    phase_ss=phase_trig()[0]
    tdecay=step_detection(phase_ss[20:],taxis[20:])
    decay02_array.append(tdecay-500)
    
fig, ax = plt.subplots()
ax.set_xlabel(r'$\tau_{02}(\mu s)$',fontsize=fontSize)
ax.set_ylabel('$counts$ ',fontsize=fontSize)


counts_hist02=np.histogram(decay02_array,bins=110)[0]
t_hist02=np.histogram(decay02_array,bins=110)[1]

plt.hist(decay02_array,bins=110)


name=str(Bfield())+'decay_distribution_tc5us_histogram_'+str(len(decay02_array))+'counts_A_pp_'+str(ampliAWG()*11)+'mV_B'+str(Bfield())+'T_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4()) 
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',decay02_array)       

####decaytimevsfield
tc=0.10
acquisition_duration =300e-6  # length of time to record (s)
repetitions = 10            # number of repetitions for the averaging
points = 66  # number of points in the acquisition window (min=2)

#efftc=acquisition_duration/10
efftc=5e-6

# such that the effective Tc is 100ms 
# repetitions=tc/efftc/5

repetitions=500

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
trigger_setting02 = [['dataAcquisitionModule/triggernode', '/dev2010/demods/0/sample.TrigAWGTrig3'],  # trigger node is AWG trigger number 3 
#                   ['dataAcquisitionModule/type', 2],      
                   ['dataAcquisitionModule/type', 6],                                          # this setting is related to the AWG trigger
                   ['dataAcquisitionModule/edge', 1],                                               # trigger on the positive edge. 1 = positive, 2=negative
                   ['dataAcquisitionModule/count', 1],                                              # number of trigger events to count
                   ['dataAcquisitionModule/holdoff/time', 0],                                       # hold off time
                   ['dataAcquisitionModule/holdoff/count', 0],                                      # hold off count
                   ##careful
                   ['dataAcquisitionModule/delay', 295e-6], #0                                       # trigger delay (s)
                   #7
                   ['dataAcquisitionModule/endless', 0]]                                            # endless disabled = 0
trigger_setting11 = [['dataAcquisitionModule/triggernode', '/dev2010/demods/0/sample.TrigAWGTrig3'],  # trigger node is AWG trigger number 3 
#                   ['dataAcquisitionModule/type', 2],      
                   ['dataAcquisitionModule/type', 6],                                          # this setting is related to the AWG trigger
                   ['dataAcquisitionModule/edge', 1],                                               # trigger on the positive edge. 1 = positive, 2=negative
                   ['dataAcquisitionModule/count', 1],                                              # number of trigger events to count
                   ['dataAcquisitionModule/holdoff/time', 0],                                       # hold off time
                   ['dataAcquisitionModule/holdoff/count', 0],                                      # hold off count
                   ##careful
                   ['dataAcquisitionModule/delay', -5e-6], #0                                       # trigger delay (s)
                   #7
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
phase_trig.setSettings(trigger_setting02, grid_setting)




