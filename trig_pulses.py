# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 14:45:02 2019

@author: G-GRE-GRE050402
"""
# slopeG3G2
# Out[162]: -0.22933333333336728

# slopeG4G2
# Out[163]: -0.026666666666642413

continuous_acquisition()
#set_triggeracquisition
trigger_mode() 
tc=0.02
acquisition_duration = 2e-3  # length of time to record (s)
repetitions = 10            # number of repetitions for the averaging
points = 440    # number of points in the acquisition window (min=2)

#efftc=acquisition_duration/10
efftc=2e-6

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
print('timeperpoint='+str(repetitions*3000e-6))

ziUhf.daq.setInt('/dev2010/sigouts/1/on', 1)    
t=np.linspace(0,2e-3,440)
phasearray=[]
amp=[]
phase=[]
for i in range(0,101):
    amp.append(ampliAWG()*4.8)
    ampliAWG(i*0.01)
    phasearray.append(phase_trig())
ziUhf.daq.setInt('/dev2010/sigouts/1/on', 0)    


for i in range(0,101):
    phase.append(phasearray[i][0])

plt.plot(phase)
Y= amp
X = t
Z1=phase


f = plt.figure()
plt.pcolor(X,Y,Z1,cmap='viridis')
# plt.pcolor(ax,'i')
plt.colorbar(label='phi(deg)')
plt.xlabel('t(s)')
plt.ylabel('pulse amplitude_pp (mV)')

now=datetime.datetime.now()
dayFolder=datetime.date.isoformat(now)
name='Tpulsevspulse_amplitude'
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt''',phase)










phaseZerotrig()


filename='C:\\Users\\g-gre-gre050402\\Documents\\Zurich Instruments\\LabOne\\WebServer\\awg\\src\\Morello_Tritonito.seqc'
continuous_acquisition()
changetpulse(filename,10e-6)
run_seq('dev2010','Morello_Tritonito.seqc')
ziUhf.daq.setInt('/dev2010/demods/1/enable', 1)
ziUhf.daq.setInt('/dev2010/sigouts/1/enables/3', 1)
rampVT2(526)
rampVB2(218)
phaseZero()
phaseZero()
loop = qc.Loop(VT2.sweep(526,516,0.1)).loop(VB2.sweep(218,232,0.1),delay=0.1).each(phase)
data = loop.get_data_set(name='StabilityVT2vsVB2_pulsingB2_3stage_10us_B-0T_'+dacnames())#nopulsingB2_10msdutycycle
plot = qc.QtPlot()
plot.add(data.phi)
_ = loop.with_bg_task(plot.update, plot.save).run()

time=np.linspace(0,acquisition_duration,points)
phaseintime=phase_pulsed()[0]
plot = qc.QtPlot()
plot.add(time,phaseintime, xlabel='time (s)', ylabel='phase (rad)',title='Z:\\110-PHELIQS\\110.05-LATEQS\\110.05.01-QuantumSilicon\\Tritonito\\data\\2019-08-28\\unloading_time'+dacnames())
foldername="Z:\\110-PHELIQS\\110.05-LATEQS\\110.05.01-QuantumSilicon\\Tritonito\\data\\2019-08-28\\"
filename=('unloadingtime_green_'+str(ampliAWG()/88*1000)+'mV_pulse60us_Bfield_0T'+dacnames()+'.txt')
np.savetxt(foldername+filename,phaseintime)
plot.save()

Bfield(4)

VB2(226.6)
VT2(523.2)


VB2vector = np.linspace(493.5,496.5,31)
MatrixData = np.zeros((len(VB2vector),352))


#acquire full pulse_response 2D
for i in range(len(VB2vector)):
    print(i)
    VB2(VB2vector[i])
    MatrixData[i] = phase_pulsed()[0]
    
plotTrig = qc.QtPlot()
plotTrig.add(time, VB2vector, MatrixData, xlabel='time (s)', ylabel='VB2', zlabel='phase (rad)',title='TP7_POSITIVEpulseamplitude'+str(ampliAWG())+'-Bfield'+str(BfieldS())+'_pulsing'+str(twait())+'s_ramp'+dacnames())
foldername="Z:\\110-PHELIQS\\110.05-LATEQS\\110.05.01-QuantumSilicon\\Tritonito\\data\\2019-07-11\\"
filename=('TP7_POSITIVEpulseamplitude'+str(ampliAWG()/88*1000)+'mV_pulse100us_ramp50us_wait50us_field'+str(BfieldS())+'.txt')
np.savetxt(foldername+filename,MatrixData)
plotTrig.save()

    















#1dscan
VB2(493)
loop=qc.Loop(VB2.sweep(493,494,0.1),delay=0.1).each(phase_pulsed)
data = loop.get_data_set(name='VB2_ramp_acquire1point_bckgremoved_twait_'+str(twait())+'triggerdelay_'+str(t_trigger()))
plot = qc.QtPlot()
plot.add(data.phase_pulse)
_ = loop.with_bg_task(plot.update, plot.save).run()
#_ = loop.run()




#triggered_acquisition_varying t_trigger
#t_triggerS()
#twait(0.2e-3)
VB2(492)
phase_pulsed()


#VB2(493.38)
VB2(493.8)
#VT2(565)
#for i in range(0,2):
#    print(i)    
loop=qc.Loop(t_trigger.sweep(10e-6,90e-6,10e-6),delay=0.2).each(phase_pulsed)
data = loop.get_data_set(name='VB2_wait500us_balancedramp200us_window_10us_triggeredacquisition')
plot = qc.QtPlot()
plot.add(data.phase_pulse)
_ = loop.with_bg_task(plot.update, plot.save).run()
#line = data.phase[:]
#    if i==0:
#           average = line[:]
#    else:
#           average = (average + line)
#
#phiaverage=average/(i+1)
#plot = qc.QtPlot()
#plot.add(data.DAQ_delay_set,data.phase_pulse,title='VB2_wait500us_balancedramp200us_window_10us_triggeredacquisition')




x = VB2
y = ampliAWG
A = [494.9, 0.05] #   in units [mV, ampliAWG()] for tuamadre
B = [492.5, 0.5]

a = (A[1]-B[1])/(A[0]-B[0])   # slope 
b = A[1]-a*A[0]               # intercept

w = Span(x, y, a, b) 
deltaY = 0.05    #step along y axis
deltaX = 0.05   #step along x axis

loop = qc.Loop(y.sweep(A[1],B[1], deltaY), progress_interval = 30).loop(w.sweep(-0.6,0.6, deltaX), delay=0).each(phase_pulsed)
data = loop.get_data_set(name='TP7-pulseAmplitudevsVB2_diagonal_2T')#-theta%dphi%d-MWm%ddBm-dac2_%.1fmV-dac3_%.1fmV-a_%gTperHz-b_%gT' % (round(magnet.theta.get()), round(magnet.phi.get()), -rfGenerator.power.get(), dac.dac2.get(), dac.dac3.get(), a, b))
plotDiag = qc.QtPlot()
plotDiag.add(data.phase_pulse)
_ = loop.with_bg_task(plotDiag.update, plotDiag.save).run()


     
VB2(493.85)

loop=qc.Loop(ampliAWG.sweep(0.1,1,0.05),delay=0.2).each(phase_pulsed)
data = loop.get_data_set(name='VB2_amplivsbackgroundresponse'+dacnames())
plot = qc.QtPlot()
plot.add(data.phase_pulse)
_ = loop.with_bg_task(plot.update, plot.save).run()








#pulsingwithramps
phaseZerotrig()

filename='C:\\Users\\g-gre-gre050402\\Documents\\Zurich Instruments\\LabOne\\WebServer\\awg\\src\\varyramp.seqc'   
times=np.linspace(0,200e-6,352)
ramp_time=np.linspace(0,100e-6,21)
MatrixData = np.zeros((21,352)) 
for i in range(0,21):

    pulse_time=100e-6
    wait_time=pulse_time-ramp_time[i]
    changetramp(filename, pulse_time,ramp_time[i],wait_time)    
    run_seq('dev2010','varyramp.seqc')   
    ziUhf.daq.setInt('/dev2010/demods/1/enable', 1)
    ziUhf.daq.setInt('/dev2010/sigouts/0/enables/3', 1)
    
    pulsepos=peakpos(ampliAWG(),494.85,ramp_time[i],pulse_time,wait_time)#tramp,tpulse,twait
    print(i)
    VB2(pulsepos)
    MatrixData[i] = phase_pulsed()[0]
    
plotTrig = qc.QtPlot()
plotTrig.add(times,ramp_time, MatrixData, xlabel='time (s)', ylabel='ramptime(us)', zlabel='phase (rad)',title='TP7_rampPOSITIVEpulseamplitude'+str(ampliAWG())+'-Bfield'+str(BfieldS())+'_pulsing'+str(twait())+'s_ramp'+dacnames())
foldername="Z:\\110-PHELIQS\\110.05-LATEQS\\110.05.01-QuantumSilicon\\Tritonito\\data\\2019-07-11\\"
filename=('TP7_rampPOSITIVEpulseamplitude'+str(ampliAWG()/88*1000)+'mV_pulse100us_ramp50us_wait50us_field'+str(BfieldS())+'.txt')
np.savetxt(foldername+filename,MatrixData)
plotTrig.save()