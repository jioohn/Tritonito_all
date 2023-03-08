# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 12:32:37 2020

@author: G-GRE-GRE050402
"""


#big maps with different detector values



rampVG4(-914)
rampVG3(-932)
VG1(-1504)
VG2(-1126.7)
rampVG5(0)
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

continuous_acquisition()
name=str(Bfield())+'T_TP9G4vsG3_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
# a,dataid,c,d=sweep2D(VG3comp,-800,-1000,801,0.1,VG4comp,-700,-900,801,0.01111,ph1)
# a,dataid,c,d=sweep2D(VG3comp,-960,-860,201,0.1,VG4comp,-790,-840,161,0.01111,ph1)
a,dataid,c,d=sweep2D(VG3comp,-932,-929,31,0.1,VG4comp,-914,-917,31,0.01317777,ph1)
plot_by_id(dataid)
saveplot(name,dataid)



##################
VG3comp(-930.63)
sensor_on_interdot_sweepG4comp(-914.5,-916.5,201,1)
name='TP9vsBsG3_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
a,dataid,c,d=sweep2D(Bfield_Hon,0,2.5,126,1,VG4comp,-914.5,-916.5,201,0.03,ph1)
plot_by_id(dataid)
saveplot(name,dataid)
Bfield(2.5)
####################



name='detuningvsBfield_TP9_reset_G1_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'

###
detuningPoint1 = [-930.2,-916.2] 
detuningPoint2 = [-931,-915.2]          # [G3(x), G4(y)]

detpoints=201
detuning = qc.combine(VG3, VG4, name = 'detuning', unit= 'points')
eps=np.sqrt((detuningPoint1[0]-detuningPoint2[0])**2 +(detuningPoint1[1]-detuningPoint2[1])**2) 
VG3comp(detuningPoint1[0])
VG4comp(detuningPoint1[1])

det=generateEpsilonAxis(detuningPoint1, detuningPoint2, detpoints)
eps=np.sqrt((detuningPoint1[0]-detuningPoint2[0])**2 +(detuningPoint1[1]-detuningPoint2[1])**2) 
epsilon=np.linspace(-eps/2,eps/2,detpoints)

name='detuningvsBfield_TP9_resetG1__G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'

phases=[]
Barr=[]
G1pos=[]
G2pos=[]
G1min=[]
for j in range(0,101):
    Bfield_Hon(0.025*j)
    Barr.append(Bfield())
    phasedet=[]
    VG3comp(det[0][0])
    VG4comp(det[0][1])
    VG1now=VG1()
    VG1onmin(G1now-1,G1now+1,201,0)
    G1now=VG1()
    # VG2onmin(G2now-1,G2now+1,201,0)
    # G2now=VG2()
    phimin=ph1()
    # G1min.append(ph1())
    G1pos.append(G1now)
    G2pos.append(G2now)
    for i in range(0,len(det)):
        VG3comp(det[i][0])
        VG4comp(det[i][1])
        time.sleep(0.01)
        phasedet.append(ph1())
    G1min.append(phimin-ph1())
    phases.append(phasedet)    




f= plt.figure()       
plt.plot(Barr,G2pos)
# ax.x
plt.xlabel('B (T)')
# plt.ylabel('pulse amplitude_pp (mV)')
plt.ylabel('G2 position(mV)')
plt.savefig(folder2+'\\'+dayFolder+'\\G2pos_Bfrom2p5to0T.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'G2pos_Bfrom2p5to0T.txt',G1pos)  


f= plt.figure()       
plt.plot(Barr,G1pos)
# ax.x
plt.xlabel('B (T)')
# plt.ylabel('pulse amplitude_pp (mV)')
plt.ylabel('G1 position(mV)')
plt.savefig(folder2+'\\'+dayFolder+'\\G1pos_Bfrom2p5to0T.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'G1pos_Bfrom2p5to0T.txt',G1pos)  

f= plt.figure()       
plt.plot(Barr,G1min)
# ax.x
plt.xlabel('B (T)')
# plt.ylabel('pulse amplitude_pp (mV)')
plt.ylabel('G1 contrast(rad)')
plt.savefig(folder2+'\\'+dayFolder+'\\G1minminusmax_Bfrom2p5to0T.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'G1min_Bfrom2p5to0T.txt',G1min)  

Y= Barr
X = epsilon
Z1=phases
Z=np.reshape(Z1,(len(Y),len(X)))
def removeBackground(data,rangeMin=0, rangeMax=-1):
    for i in range(len(data)):
        data[i] = data[i] - data[i][rangeMin:rangeMax].mean() 
    return(data)

Z2=removeBackground(Z)

f = plt.figure()
plt.pcolor(X,Y,Z2,cmap='viridis')
# plt.clim(vmin=None,vmax=0.3)
plt.colorbar(label='phi(deg)')
plt.xlabel('detuning (mV)')
# plt.ylabel('pulse amplitude_pp (mV)')
plt.ylabel('B (T)')



now=datetime.datetime.now()
dayFolder=datetime.date.isoformat(now)
# name='detuningvsBfield_TP6'
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'_Bgsub.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'_Bgsub.txt',Z2)   
     
f = plt.figure()
plt.pcolor(X,Y,Z,cmap='viridis')
# plt.clim(vmin=None,vmax=0.3)
plt.colorbar(label='phi(deg)')
plt.xlabel('detuning (mV)')
# plt.ylabel('pulse amplitude_pp (mV)')
plt.ylabel('B (T)')
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',Z)  
 # 
Bfield(2.5) 




















rampVG4(-810)
rampVG3(-900)

rampVG5(0)
VG1(-1490)
VG2(-1440)



continuous_acquisition()
name=str(Bfield())+'TSENSORNOT_TUNED_TP7G4vsG3_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
# a,dataid,c,d=sweep2D(VG3comp,-800,-1000,801,0.1,VG4comp,-700,-900,801,0.01111,ph1)
a,dataid,c,d=sweep2D(VG3comp,-950,-850,201,0.1,VG4comp,-780,-820,161,0.01111,ph1)
# a,dataid,c,d=sweep2D(VG3comp,-934,-940,61,0.1,VG4comp,-795,-805,51,0.01317777,ph1)
plot_by_id(dataid)
saveplot(name,dataid)




rampVG4(-810)
rampVG3(-900)
continuous_acquisition()
name=str(Bfield())+'G1vsG2_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
# a,dataid,c,d=sweep2D(VG3comp,-800,-1000,801,0.1,VG4comp,-700,-900,801,0.01111,ph1)
a,dataid,c,d=sweep2D(VG1,-1700,-1400,301,0.1,VG2,-1000,-1400,401,0.007,ph1)
# a,dataid,c,d=sweep2D(VG3comp,-934,-940,61,0.1,VG4comp,-795,-805,51,0.01317777,ph1)
plot_by_id(dataid)
saveplot(name,dataid)

Bfield(2)
rampVG4(-810)
rampVG3(-900)
continuous_acquisition()
name=str(Bfield())+'G1vsG2_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
# a,dataid,c,d=sweep2D(VG3comp,-800,-1000,801,0.1,VG4comp,-700,-900,801,0.01111,ph1)
a,dataid,c,d=sweep2D(VG1,-1700,-1400,301,0.1,VG2,-1000,-1400,401,0.007,ph1)
# a,dataid,c,d=sweep2D(VG3comp,-934,-940,61,0.1,VG4comp,-795,-805,51,0.01317777,ph1)
plot_by_id(dataid)
saveplot(name,dataid)



Bfield(2)
rampVG4(-810)
rampVG3(-900)
continuous_acquisition()
name=str(Bfield())+'G1vsG2_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
# a,dataid,c,d=sweep2D(VG3comp,-800,-1000,801,0.1,VG4comp,-700,-900,801,0.01111,ph1)
a,dataid,c,d=sweep2D(VG1,-1520,-1480,321,0.1,VG2,-1150,-1250,401,0.007,ph1)
# a,dataid,c,d=sweep2D(VG3comp,-934,-940,61,0.1,VG4comp,-795,-805,51,0.01317777,ph1)
plot_by_id(dataid)
saveplot(name,dataid)

Bfield(0)
rampVG4(-810)
rampVG3(-900)
continuous_acquisition()
name=str(Bfield())+'G1vsG2_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
# a,dataid,c,d=sweep2D(VG3comp,-800,-1000,801,0.1,VG4comp,-700,-900,801,0.01111,ph1)
a,dataid,c,d=sweep2D(VG1,-1520,-1480,321,0.1,VG2,-1150,-1250,401,0.007,ph1)
# a,dataid,c,d=sweep2D(VG3comp,-934,-940,61,0.1,VG4comp,-795,-805,51,0.01317777,ph1)
plot_by_id(dataid)
saveplot(name,dataid)




######check metastable_ integration 18us
tc=0.10
acquisition_duration =10e-6  # length of time to record (s)
repetitions = 10            # number of repetitions for the averaging
points = 9# number of points in the acquisition window (min=2)

#efftc=acquisition_duration/10
efftc=1e-6

# such that the effective Tc is 100ms 
# repetitions=tc/efftc/5

repetitions=100

ziUhf.daq.setInt('/dev2010/demods/0/trigger', 33554432) # demodulator trigger set on AWGtrigger2 High
ziUhf.daq.setDouble('/dev2010/demods/0/rate', 800e3)
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
                   ['dataAcquisitionModule/delay', 200e-6], #0                                       # trigger delay (s)
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

t=time.time()
phase_trig()
t2=time.time()-t
print('t='+str(t2)+'s')


# trigger_mode()
# VG3comp(-930.5)
ampliAWG(0.1)
name=str(Bfield())+'T'+str(ampliAWG()*11)+'_mV_trigin02_TP7G4vsG3_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'

a,dataid,c,d=sweep2D(VG3comp,-932,-929,31,0.1,VG4comp,-914,-917,61,0.01317777,phase_trig)
plot_by_id(dataid)
saveplot(name,dataid)

ampliAWG(-0.1)
name=str(Bfield())+'T'+str(ampliAWG()*11)+'_mV_trigin02_TP7G4vsG3_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'


a,dataid,c,d=sweep2D(VG3comp,-932,-929,31,0.1,VG4comp,-914,-917,61,0.01317777,phase_trig)
plot_by_id(dataid)
saveplot(name,dataid)


ampliAWG(0.2)
name=str(Bfield())+'T'+str(ampliAWG()*11)+'_mV_trigin02_TP7G4vsG3_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'


a,dataid,c,d=sweep2D(VG3comp,-932,-929,31,0.1,VG4comp,-914,-917,61,0.01317777,phase_trig)
plot_by_id(dataid)
saveplot(name,dataid)

ampliAWG(-0.2)
name=str(Bfield())+'T'+str(ampliAWG()*11)+'_mV_trigin02_TP7G4vsG3_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'


a,dataid,c,d=sweep2D(VG3comp,-932,-929,31,0.1,VG4comp,-914,-917,61,0.01317777,phase_trig)
plot_by_id(dataid)
saveplot(name,dataid)


Bfield(0)
ampliAWG(0.2)
name=str(Bfield())+'T'+str(ampliAWG()*11)+'_mV_trigin02_TP7G4vsG3_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'


a,dataid,c,d=sweep2D(VG3comp,-932,-929,31,0.1,VG4comp,-914,-917,61,0.01317777,phase_trig)
plot_by_id(dataid)
saveplot(name,dataid)

ampliAWG(-0.2)
name=str(Bfield())+'T'+str(ampliAWG()*11)+'_mV_trigin02_TP7G4vsG3_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'

a,dataid,c,d=sweep2D(VG3comp,-932,-929,31,0.1,VG4comp,-914,-917,61,0.01317777,phase_trig)
plot_by_id(dataid)
saveplot(name,dataid)


#6 December


rampVG4(-917)
rampVG3(-930)

rampVG5(0)
VG1(-1504)
VG2(-1126.6)

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

continuous_acquisition()
name=str(Bfield())+'T_TP9G4vsG3_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
# a,dataid,c,d=sweep2D(VG3comp,-800,-1000,801,0.1,VG4comp,-700,-900,801,0.01111,ph1)
# a,dataid,c,d=sweep2D(VG3comp,-960,-860,201,0.1,VG4comp,-790,-840,161,0.01111,ph1)
a,dataid,c,d=sweep2D(VG3comp,-932,-929,31,0.1,VG4comp,-914,-917,31,0.01317777,ph1)
plot_by_id(dataid)
saveplot(name,dataid)

##################""
continuous_acquisition()
ziUhf.daq.setInt('/dev2010/sigouts/1/on', 0)
VG3comp(-930.6)
sensor_on_interdot_sweepG4comp(-914,-917,301,1)



#########################################"
trigger_mode() 
tc=0.10
acquisition_duration = 600e-6  # length of time to record (s)
repetitions = 10            # number of repetitions for the averaging
points = 132  # number of points in the acquisition window (min=2)

#efftc=acquisition_duration/10
efftc=5e-6

# such that the effective Tc is 100ms 
# repetitions=tc/efftc/5

repetitions=200

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
print('timeperpoint='+str(repetitions*acquisition_duration))


ziUhf.daq.setInt('/dev2010/sigouts/1/on', 1)    
t=np.linspace(0,600e-6,points)
phasearray=[]
amp=[]

for i in range(0,101):
    ampliAWG(i*0.001)
    amp.append(ampliAWG())

    phasearray.append(phase_trig())
ziUhf.daq.setInt('/dev2010/sigouts/1/on', 0)    

phase=[]
for i in range(0,101):
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
name=str(Bfield())+'T_TP9_timevspulse_amplitudeonAWG_500rep_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',phase)


###############pulsevsG4pos

ziUhf.daq.setInt('/dev2010/sigouts/1/on', 1)    
t=np.linspace(0,400e-6,points)
phasearray=[]
amp=[]

for i in range(0,101):

    ampliAWG(0.1)
    VG4comp(-914.5-0.02*i)
    amp.append(VG4())
    phasearray.append(phase_trig())
ziUhf.daq.setInt('/dev2010/sigouts/1/on', 0)    

phase=[]
for i in range(0,101):
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
plt.ylabel('VG4(mV)')

now=datetime.datetime.now()
dayFolder=datetime.date.isoformat(now)
name=str(Bfield())+'T_TP9_pulsing_ampli'+str(ampliAWG)+'_timevsG4_amplitude_200rep_'
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',phase)









##turnoff pulsesbefore
continuous_acquisition()
VG3comp(-930.5)
sensor_on_interdot_sweepG4comp(-914.5,-916.5,201,1)

###fit decayvsB
tc=0.10
acquisition_duration =200e-6  # length of time to record (s)
repetitions = 10            # number of repetitions for the averaging
points = 44  # number of points in the acquisition window (min=2)

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
trigger_setting = [['dataAcquisitionModule/triggernode', '/dev2010/demods/0/sample.TrigAWGTrig3'],  # trigger node is AWG trigger number 3 
#                   ['dataAcquisitionModule/type', 2],      
                   ['dataAcquisitionModule/type', 6],                                          # this setting is related to the AWG trigger
                   ['dataAcquisitionModule/edge', 1],                                               # trigger on the positive edge. 1 = positive, 2=negative
                   ['dataAcquisitionModule/count', 1],                                              # number of trigger events to count
                   ['dataAcquisitionModule/holdoff/time', 0],                                       # hold off time
                   ['dataAcquisitionModule/holdoff/count', 0],                                      # hold off count
                   ##careful
                   ['dataAcquisitionModule/delay', 196e-6], #0                                       # trigger delay (s)
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






################
G4val=[]
Binit=1
Bfinal=2
Bpoints=21
dB=(Bfinal-Binit)/(Bpoints-1)
# M=np.zeros((Bpoints,points)) #y,x
M=[]
ydata=np.linspace(Binit,Bfinal,Bpoints)
tempty=[]
# tguessarray=[]
# tguessarray2=[]
# tguessgoodarray=[]

temptyfitarray=[]
# temptyfitarray2=[]
temptyfitarray_nodelay=[]
temptyerrorfitarray_nodelay=[]
Tarray=[]
# foldername="O:\\132-PHELIQS\\132.05-LATEQS\\132.05.01-QuantumSilicon\\Tritonito\\data\\2019-11-05\\"
errorTarray=[]
tunnelarray=[]
tunnelarrayerr=[]
T=0.44

taxis=np.linspace(0,200e-6,points)

for i in range(0,Bpoints):
    print('field='+str(Bfield()))
#    Bfield(Binit+Bfinal/(Bpoints-1)*i)
    Bfield_Hon(Binit+dB*i)
    # time.sleep(30)
#    tguessarray2.append(tguess2)

    ampliAWG(0.05)
    # continuous_acquisition()
    # VG4comp(-799)
    # VG3comp(-936.7)
    # ziUhf.daq.setInt('/dev2010/sigouts/1/on', 0)
    # sensor_on_interdot_sweepG4comp(-802,-797,201,0)
    # G4val.append(VG4())
    trigger_mode()
    ziUhf.daq.setInt('/dev2010/sigouts/1/on', 1)
    ziUhf.daq.setDouble('/dev2010/demods/0/rate', 200e3)
    ziUhf.daq.setDouble('/dev2010/demods/0/timeconstant', 5e-6)
    
    phase=phase_trig()[0]
    M.append(phase)
    
    
    fig, ax = plt.subplots()
    ax.set_xlabel('time(s)',fontsize=fontSize)
    ax.set_ylabel('$\phi $(rad)',fontsize=fontSize)
    plt.plot(taxis,phase,'b+',label='data')

    #check@1mV

    def fit_exponential(x,*p):
     return p[1]*np.exp(-x/p[0]+ p[3]) +p[2]#phimax-phimin)*np.exp(-x/p[0])+phimin  
 
    
    
    def fit_exponential2(x,*p):
        phimin=-0.012
        return p[1]*np.exp(-x/p[0]) +phimin#phimax-phimin)*np.exp(-x/p[0])+phimin    
    
    def fit_exponential_nodelay(x,*p):
        return p[1]*np.exp(-x/p[0]) +p[2]  
    
    
    phimax=np.max(phase)
    phimin=np.min(phase)
    popt,pcov = curve_fit(fit_exponential_nodelay,taxis,M[i],p0=[100e-6,phimax-phimin,phimin],maxfev=10000)    
    
    er=np.sqrt(np.diag(pcov))
    tempty_nodelay=popt[0]
    errortempty_nodelay=er[0]
    temptyfitarray_nodelay.append(tempty_nodelay)
    temptyerrorfitarray_nodelay.append(errortempty_nodelay)
    plt.plot(taxis,fit_exponential_nodelay(taxis,*popt),'r',label='tempty='+str( round(tempty_nodelay*1000000,3)) +'$\pm$'+str( round(errortempty_nodelay*1000000,3))+'_us')#',phimin='+str(round(popt[2]*1000,3))+'mrad_phimax='+str(round((popt[1]+popt[2])*1000,3))+'mrad')
        
  
 
    plt.legend(loc='upper right')
    plt.show()
    name='TP9_decayfitin02_amplitude_pp_'+str(ampliAWG()*11)+'mV_1000rep_B'+str(Bfield())+'T_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV'+str(VG5())+'mV'
    # name='TP7__decayfitin11_amplitude_pp_'+str(ampliAWG()*11)+'mV_1000rep_B'+str(Bfield())+'T_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV'+str(VG5())+'mV'
    try:
        plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
        np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',phase)
    except FileNotFoundError:
        print('BUG, file not saved, name too long probably')
        
    print('tau_empty_nodelay='+str(tempty_nodelay*1000)+'ms')
    print('phimin_nodelay='+str(popt[2]*1000)+'mrad')
    print('phimax_nodelay='+str( (popt[1]+popt[2])*1000)+'mrad')
    


ydata=np.linspace(Binit,Bfinal,Bpoints)
# Brange='2to0T'

#2dmap of signalvsfield
fig, ax = plt.subplots()
ax.set_xlabel('time(s)',fontsize=fontSize)
ax.set_ylabel('$B$ (T)',fontsize=fontSize)
name='TP9____timevsfield_amplitude_pp_'+str(ampliAWG()*11)+'mV_1000rep_B'+str(Bfield())+'T_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
# name='TP7____timein11sfield_amplitude_pp_'+str(np.round(ampliAWG()*11,4))+'mV_1000rep_B'+str(Bfield())+'T_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV'

def removeBackground(data,rangeMin=0, rangeMax=-1):
    for i in range(len(data)):
        data[i] = data[i] - data[i][rangeMin:rangeMax].mean() 
    return(data)

Z=removeBackground(M)


plt.pcolor(taxis,ydata,Z,cmap='viridis')
# plt.clim(vmin=None,vmax=0.3)
plt.colorbar(label='phi(rad)')
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',Z)


tempty=np.multiply(temptyfitarray_nodelay,1e6)#convert in us
terror=np.multiply(temptyerrorfitarray_nodelay,1e6)
#extracted_decay_vsfield
fig, ax = plt.subplots()
ax.set_xlabel('B(T)',fontsize=fontSize)
ax.set_ylabel(r'$\tau$ ($\mu$s)',fontsize=fontSize)

name='TP9____decaytimevsfield_amplitude_pp_'+str(ampliAWG()*11)+'mV_500rep_B'+str(Bfield())+'T_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV'
# name='TP7____decaytimein11sfield_amplitude_pp_'+str(np.round(ampliAWG()*11,4))+'mV_1000rep_B'+str(Bfield())+'T_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV'
# plt.plot(ydata,tempty,'b+',label='data')
plt.errorbar(ydata,tempty,yerr=terror,fmt='b+')
# plt.clim(vmin=None,vmax=0.3)
# plt.colorbar(label='phi(rad)')
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',tempty)
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'errors.txt',terror)

np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'G4val.txt',G4val)

Bfield(Bfinal)















#######################fit charge sensor signal

continuous_acquisition()
VG3comp(-930.5)
# sensor_on_interdot_sweepG4comp(-914.5,-916.5,201,1)

a,dataid,c=sweep1D(VG4comp, -914.5,-916.5,201,0.01,ph1)


folder=r'S:\132-PHELIQS\132.05-LATEQS\132.05.01-QuantumSilicon\Tritonito\2020\20201029_5G23_2\\data'
name=str(dataid)+'_G4scan_calibrate_cs'
xlabel='$V_{G4}$(mV)'
ylabel='$\phi_{G1}$(deg)'
data_set,data_get,parameters_name=Extract_data(a)
datasmooth=scipy.signal.savgol_filter(np.ravel(data_get[0]),11, 3)
phimin=np.min(datasmooth)
phimax=np.max(datasmooth)
argmin=np.argmin(datasmooth)
kmin=0
kmax=0
philim=phimin+(phimax-phimin)/2

sigmaphi=0.05
for k in range(0,len(data_set)):
        if ((data_get[0][k]>=(philim-sigmaphi) and data_get[0][k]<=(philim+sigmaphi)) and kmax==0):
            kmax=k


def interdotfit_chargesensor(x,*p):
     T=0.44
     return( p[2]+p[1]*(np.tanh(x*p[0]/(2*kb*T))) ) 

xaxis=np.multiply(np.subtract(data_set,data_set[kmax]),1e-3)
datasmooth2=np.subtract(datasmooth,phimin)

xaxis2=np.array(xaxis,dtype=float)
datasmooth2=np.array(datasmooth2,dtype=float)


xaxis2=np.reshape(xaxis2,201)
datasmooth2=np.reshape(datasmooth2,201)

fig, ax = plt.subplots()
ax.set_xlabel('$\epsilon$ (V)',fontsize=fontSize)
ax.set_ylabel('$\phi $(rad)',fontsize=fontSize)

plt.title('Fit at T='+str(T)+'K')
plt.plot(xaxis,datasmooth2,'b+',label='data@'+str(T)+'K')#mV on x  
plt.legend(loc='upper left')
plt.show()



alpha=0.5
const=phimin
offset=phimin+(phimax-phimin)
tunnelguess=4e-6#eV=1GHz
  
popt,pcov = curve_fit(interdotfit_chargesensor,xaxis2,datasmooth2,p0=[alpha,0,1],maxfev=10000) 
plt.plot(xaxis2,interdotfit_chargesensor(xaxis2,*popt))    


alpha=popt[0] 

er=np.sqrt(np.diag(pcov))
erroralpha=er[0]
# errortunnel=er[3]
# print('Teff='+str(Teff))
# Tarray.append(Teff)
errorTarray.append(errortemp)

tunnelarray.append(tunnel)
tunnelarrayerr.append(errortunnel)

errortunnel=errortunnel/h*10e-9#conv to Ghz
plt.plot(xaxis,interdotfit_chargesensor(xaxis2,*popt),'r',label='alpha='+str( round(alpha,2)) +'$\pm$'+str( round(erroralpha,2))+'_eV/V')#,t='+str( round(tunnel,3))+'$\pm$'+str(round(errortunnel,3))+'_GHz, alpha='+str(alpha))
#    plt.plot(xaxis,interdotfit_chargesensor(xaxis,*popt),'r',label='Teff='+str( round(Teff,2)) +'$\pm$'+str( round(errortemp,2))+'_K,t='+str( round(tunnel,3))+'$\pm$'+str(round(errortunnel,3))+'_GHz, alpha='+str(alpha))
plt.legend(loc='upper left')
plt.show()
name='0p44K_findalpha_tnegligible_TP9_1dscan-'+str(Bfield())+'_T_'
# fig.savefig(foldername2+'0.44K_Tonly_TP9_1dscan-'+str(Bfield())+'_T_ampliAWG'+str(ampliAWG())+'.png') 
# np.savetxt(foldername2+'0.44K_Tonly_TP9_1dscan-'+str(Bfield())+'_T_ampliAWG'+str(ampliAWG())+'.txt',datasmooth2)

plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',datasmooth2)



######## detuningloop
###
detuningPoint1 = [-930.2,-916.2] 
detuningPoint2 = [-931,-915.2]          # [G3(x), G4(y)]

detpoints=201
detuning = qc.combine(VG3, VG4, name = 'detuning', unit= 'points')
eps=np.sqrt((detuningPoint1[0]-detuningPoint2[0])**2 +(detuningPoint1[1]-detuningPoint2[1])**2) 
VG3comp(detuningPoint1[0])
VG4comp(detuningPoint1[1])

det=generateEpsilonAxis(detuningPoint1, detuningPoint2, detpoints)
eps=np.sqrt((detuningPoint1[0]-detuningPoint2[0])**2 +(detuningPoint1[1]-detuningPoint2[1])**2) 
epsilon=np.linspace(0,eps,detpoints)

name='detuningvsBfield_TP9_resetG1__G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'

phases=[]
Barr=[]
G1pos=[]
G2pos=[]
G1min=[]

VG3comp(det[0][0])
VG4comp(det[0][1])
# VG1now=VG1()
# VG1onmin(G1now-1,G1now+1,201,0)
# G1now=VG1()
# # VG2onmin(G2now-1,G2now+1,201,0)
# # G2now=VG2()
# phimin=ph1()
# # G1min.append(ph1())
# G1pos.append(G1now)
# G2pos.append(G2now)
phasedet=[]
for i in range(0,len(det)):
    VG3comp(det[i][0])
    VG4comp(det[i][1])
    time.sleep(0.01)
    phasedet.append(ph1())
G1min.append(phimin-ph1())
phases.append(phasedet)    



datasmooth=scipy.signal.savgol_filter(np.ravel(phasedet),11, 3)

phimin=np.min(datasmooth)
phimax=np.max(datasmooth)
argmin=np.argmin(datasmooth)
kmin=0
kmax=0
philim=phimin+(phimax-phimin)/2
T=0.44
sigmaphi=0.05
for k in range(0,len(epsilon)):
        if ((datasmooth[k]>=(philim-sigmaphi) and datasmooth[k]<=(philim+sigmaphi)) and kmax==0):
            kmax=k


def interdotfit_chargesensor(x,*p):

     return( p[2]+p[1]*(np.tanh(x*p[0]/(2*kb*T))) ) 

xaxis=np.multiply(np.subtract(epsilon,epsilon[kmax]),1e-3)
datasmooth2=np.subtract(datasmooth,phimin)

xaxis2=np.array(xaxis,dtype=float)
datasmooth2=np.array(datasmooth2,dtype=float)


xaxis2=np.reshape(xaxis2,201)
datasmooth2=np.reshape(datasmooth2,201)

fig, ax = plt.subplots()
ax.set_xlabel('$\epsilon$ (V)',fontsize=fontSize)
ax.set_ylabel('$\phi $(rad)',fontsize=fontSize)

plt.title('Fit at T='+str(T)+'K')
plt.plot(xaxis,datasmooth2,'b+',label='data@'+str(T)+'K')#mV on x  
plt.legend(loc='upper left')
plt.show()



alpha=0.5
const=phimin
offset=phimin+(phimax-phimin)
tunnelguess=4e-6#eV=1GHz
  
popt,pcov = curve_fit(interdotfit_chargesensor,xaxis2,datasmooth2,p0=[alpha,0,1],maxfev=10000) 
plt.plot(xaxis2,interdotfit_chargesensor(xaxis2,*popt))    


alpha=popt[0] 

er=np.sqrt(np.diag(pcov))
erroralpha=er[0]


# tunnelarray.append(tunnel)
# tunnelarrayerr.append(errortunnel)

# errortunnel=errortunnel/h*10e-9#conv to Ghz

plt.plot(xaxis,interdotfit_chargesensor(xaxis2,*popt),'r',label='alpha='+str( round(alpha,2)) +'$\pm$'+str( round(erroralpha,2))+'_eV/V')#,t='+str( round(tunnel,3))+'$\pm$'+str(round(errortunnel,3))+'_GHz, alpha='+str(alpha))
#    plt.plot(xaxis,interdotfit_chargesensor(xaxis,*popt),'r',label='Teff='+str( round(Teff,2)) +'$\pm$'+str( round(errortemp,2))+'_K,t='+str( round(tunnel,3))+'$\pm$'+str(round(errortunnel,3))+'_GHz, alpha='+str(alpha))
plt.legend(loc='upper left')
plt.show()
name='0p44K_findalpha_tnegligible_detuningcut_TP9_1dscan-'+str(Bfield())+'_T_'
# fig.savefig(foldername2+'0.44K_Tonly_TP9_1dscan-'+str(Bfield())+'_T_ampliAWG'+str(ampliAWG())+'.png') 
# np.savetxt(foldername2+'0.44K_Tonly_TP9_1dscan-'+str(Bfield())+'_T_ampliAWG'+str(ampliAWG())+'.txt',datasmooth2)

plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',datasmooth2)














# #############
# # VG3comp(-930.5)
# # sensor_on_interdot_sweepG4comp(-915,-916.5,201,1)
# name='TP9vsBsG3_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
# a,dataid,c,d=sweep2D(Bfield_Hon,0,2,101,1,VG4comp,-914.5,-916.5,201,0.03,ph1)
# plot_by_id(dataid)
# saveplot(name,dataid)
# Bfield(2)
# #####Bfieldon
# #need to know interdot position

# # continuous_acquisition()
# # ziUhf.daq.setInt('/dev2010/sigouts/1/on', 0)    
# # VG2onmin(G2now-3,G2now+3,301,1)
# # VG4(-806)
# # VG3(-923.4)

# rampVG4(-917)
# rampVG3(-930)
# VG2(-1126.67)
# rampVG5(0)
# # VG1(-1490)
# # VG2(-1135)

# continuous_acquisition()

# ziUhf.daq.setInt('/dev2010/sigouts/1/on', 0)
# G1now=VG1()
# G2now=VG2()
# G3now=VG3()
# G4now=VG4()
# G5now=VG5()
# VG3comp()
# VG4comp()
# # VG1onmin(G1now-10,G1now+10,801,1)
# G1now=VG1()
# VG1onmin(G1now-4,G1now+4,801,1)
# G1now=VG1()
# VG2onmin(G2now-4,G2now+4,801,1)
# G2now=VG2()

#  continuous_acquisition()
# VG3comp(-930.5)
# sensor_on_interdot_sweepG4comp(-914.5,-916.5,201,1)

# name=str(Bfield())+'T_TP9G4vsG3_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
# # a,dataid,c,d=sweep2D(VG3comp,-800,-1000,801,0.1,VG4comp,-700,-900,801,0.01111,ph1)
# # a,dataid,c,d=sweep2D(VG3comp,-960,-860,201,0.1,VG4comp,-790,-840,161,0.01111,ph1)
# a,dataid,c,d=sweep2D(VG3comp,-932,-929,31,0.1,VG4comp,-914,-917,31,0.01317777,ph1)
# plot_by_id(dataid)
# saveplot(name,dataid)
# VG3comp(-930.5)
# sensor_on_interdot_sweepG4comp(-914.5,-916.5,201,1)
