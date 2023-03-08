# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 11:52:27 2020

@author: G-GRE-GRE050402
"""
name='detuningvsBfield_TP6'

###
detuningPoint1 = [-924.6,-806.2]          # [G3(x), G4(y)]
detuningPoint2 = [-923,-807.8] 
detpoints=201
detuning = qc.combine(VG3, VG4, name = 'detuning', unit= 'points')
eps=np.sqrt((detuningPoint1[0]-detuningPoint2[0])**2 +(detuningPoint1[1]-detuningPoint2[1])**2) 
VG3(detuningPoint1[0])
VG4(detuningPoint1[1])

det=generateEpsilonAxis(detuningPoint1, detuningPoint2, detpoints)
eps=np.sqrt((detuningPoint1[0]-detuningPoint2[0])**2 +(detuningPoint1[1]-detuningPoint2[1])**2) 
epsilon=np.linspace(-eps/2,eps/2,detpoints)
phasedet=[]
phases=[]
Barr=[]

for j in range(0,31):
    Bfield_Hon(1.5-0.05*j)
    Barr.append(Bfield())
    for i in range(0,len(det)):
        VG3comp(det[i][0])
        VG4comp(det[i][1])
        time.sleep(0.01)
        phasedet.append(ph1)
    phases.append(phasedet)    
        
plt.plot(phase)
Y= Barr
X = epsilon
Z1=phases


f = plt.figure()
plt.pcolor(X,Y,Z1,cmap='viridis')
# plt.clim(vmin=None,vmax=0.3)
plt.colorbar(label='phi(deg)')
plt.xlabel('detuning (mV)')
# plt.ylabel('pulse amplitude_pp (mV)')
plt.ylabel('B (T)')

now=datetime.datetime.now()
dayFolder=datetime.date.isoformat(now)
# name='detuningvsBfield_TP6'
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt''',phase)        

Bfield(0)



############################
# name='TP6_G4compvsBfield_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
# a,dataid,c,d=sweep2D(Bfield_Hon,1.5,0,51,1,VG4comp,-805,-809,21,0.02,ph1)
# plot_by_id(dataid)
# saveplot(name,dataid)
# Bfield(1.5)




name='0T_TP6G4vsG3_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
continuous_acquisition()
ziUhf.daq.setInt('/dev2010/sigouts/1/on', 0)    
VG2onmin(G2now-3,G2now+3,301,1)
VG4(-810)
VG3(-926)

G1now=VG1()
G2now=VG2()
G3now=VG3()
G4now=VG4()
G5now=VG5()
VG3comp()
VG4comp()
VG1onmin(G1now-4,G1now+4,801,1)
VG1now=VG1()
VG2onmin(G2now-4,G2now+4,801,1)
G2now=VG2()
a,dataid,c,d=sweep2D(VG3comp,-921,-926,51,0.1,VG4comp,-802,-811,91,0.02,ph1)
plot_by_id(dataid)
saveplot(name,dataid)





#################
name='0T_TP6_triggeron_negativespulse_first500us_amplitude'+str(ampliAWG()*4.8)+'mV_50rep_3mseachpulse'
trigger_mode() 
tc=0.05
acquisition_duration = 500e-6 # length of time to record (s)
repetitions = 10            # number of repetitions for the averaging
points = 110  # number of points in the acquisition window (min=2)

#efftc=acquisition_duration/10
efftc=5e-6

# such that the effective Tc is 100ms 
# repetitions=tc/efftc/5

repetitions=50



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

phase_trig= SpecialParameters.Pulsed_readout_G1(ziUhf, repetitions, returnOnePoint=True)
#phase_pulsed_B3= Pulsed_readout_B3(ziUhf, repetitions, returnOnePoint=True)
phase_trig.setSettings(trigger_setting, grid_setting)


print('tc='+str(efftc)+'  rep='+str(repetitions))
#for symmetric pulses
#print('timeperpoint='+str(repetitions*twait()*2))
print('timeperpoint='+str(repetitions*acquisition_duration))
 

ziUhf.daq.setInt('/dev2010/sigouts/1/on', 1)    
a,dataid,c,d=sweep2D(VG3comp,-922,-926,31,0.1,VG4comp,-803,-810,51,0.02,phase_trig)
plot_by_id(dataid)
saveplot(name,dataid)