# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 15:45:37 2020

@author: G-GRE-GRE050402
"""
#############
slopeG3G2= -0.22933333333336728
slopeG4G2=-0.026666666666642413
VG3comp=  SpecialParameters.CompensateG3(VG3,VG2,slopeG3G2)
VG4comp=  SpecialParameters.CompensateG4(VG4,VG2,slopeG4G2)
############################
name='2T_TP7G4vsG3_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'

continuous_acquisition()
ziUhf.daq.setInt('/dev2010/sigouts/1/on', 0)    

# rampVG4(0)
# rampVG3(-0)
# rampVG2(0)
# rampVG1(0)
# rampVG5(0)
# time.sleep(30)


rampVG2(-1135)
rampVG1(-1530)


rampVG4(-802)
rampVG3(-944)

rampVG5(0)

G1now=VG1()
G2now=VG2()
G3now=VG3()
G4now=VG4()
G5now=VG5()
VG3comp()
VG4comp()
VG1onmin(G1now-60,G1now+60,801,1)
VG1now=VG1()
VG1onmin(G1now-4,G1now+4,801,1)
VG1now=VG1()
VG2onmin(G2now-4,G2now+4,801,1)
G2now=VG2()
# VG5onmin(G5now-4,G5now+4,801,1)

name='0T_TP7G4vsG3_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
a,dataid,c,d=sweep2D(VG3comp,-930,-960,61,0.1,VG4comp,-780,-820,81,0.01111,ph1)
# a,dataid,c,d=sweep2D(VG3comp,-942,-946,71,0.1,VG4comp,-794,-802,111,0.01111,ph1)
# a,dataid,c,d=sweep2D(VG3comp,-939,-946,101,0.1,VG4comp,-794,-798,81,0.01777,ph1)
plot_by_id(dataid)
saveplot(name,dataid)

#####sit on interdot
VG3comp(-944.8)
sensor_on_interdot_sweepG4comp(-797,-800.5,301,1)
#######


####pulse vs amplitude
trigger_mode()
ziUhf.daq.setInt('/dev2010/sigouts/1/on', 1)    
t=np.linspace(0,6e-3,points)
phasearray=[]
amp=[]

for i in range(0,201):
    amp.append(ampliAWG())
    ampliAWG(i*0.005)
    phasearray.append(phase_trig())
ziUhf.daq.setInt('/dev2010/sigouts/1/on', 0)    

phase=[]
for i in range(0,201):
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
name='TP7_pulsevspulse_amplitude_200repB_'+str(Bfield())
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt''',phase)
ziUhf.daq.setInt('/dev2010/sigouts/1/on', 1)  
continuous_acquisition()

###TP7 vs field
continuous_acquisition()
name='TP7_G4compvsBfield_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
a,dataid,c,d=sweep2D(Bfield_Hon,0,2,101,1,VG4comp,-801,-798,301,0.03,ph1)
plot_by_id(dataid)
saveplot(name,dataid)
Bfield(2)




####set pulses
#set_triggeracquisition
trigger_mode() 
tc=0.10
acquisition_duration = 6e-3  # length of time to record (s)
repetitions = 10            # number of repetitions for the averaging
points = 1319   # number of points in the acquisition window (min=2)

#efftc=acquisition_duration/10
efftc=2e-6

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
print('timeperpoint='+str(repetitions*acquisition_duration))

ziUhf.daq.setInt('/dev2010/sigouts/1/on', 1)    
t=np.linspace(0,6e-3,points)
phasearray=[]
amp=[]

for i in range(0,11):
    amp.append(ampliAWG())
    ampliAWG(i*0.005)
    phasearray.append(phase_trig())
ziUhf.daq.setInt('/dev2010/sigouts/1/on', 0)    

phase=[]
for i in range(0,11):
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
name='0T_TP7_pulsevspulse_amplitude_200rep'
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt''',phase)



# name='TP7_G4compvsBfield_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
# a,dataid,c,d=sweep2D(Bfield_Hon,1.5,0,51,1,VG4comp,-805,-809,21,0.02,ph1)
# plot_by_id(dataid)
# saveplot(name,dataid)
# Bfield(1.5)


################## TP0
name='detuningvsBfield_TP0_'

###
detuningPoint1 = [-907.5,-812.5] 
detuningPoint2 = [-905.8,-814]          # [G3(x), G4(y)]

detpoints=201
detuning = qc.combine(VG3, VG4, name = 'detuning', unit= 'points')
eps=np.sqrt((detuningPoint1[0]-detuningPoint2[0])**2 +(detuningPoint1[1]-detuningPoint2[1])**2) 
VG3(detuningPoint1[0])
VG4(detuningPoint1[1])

det=generateEpsilonAxis(detuningPoint1, detuningPoint2, detpoints)
eps=np.sqrt((detuningPoint1[0]-detuningPoint2[0])**2 +(detuningPoint1[1]-detuningPoint2[1])**2) 
epsilon=np.linspace(-eps/2,eps/2,detpoints)

phases=[]
Barr=[]

for j in range(0,41):
    Bfield_Hon(2-0.05*j)
    Barr.append(Bfield())
    phasedet=[]
    for i in range(0,len(det)):
        VG3comp(det[i][0])
        VG4comp(det[i][1])
        time.sleep(0.02)
        phasedet.append(ph1())
    phases.append(phasedet)    


f= plt.figure()       
plt.plot(phasedet)
# ax.x
plt.xlabel('detuning (mV)')
# plt.ylabel('pulse amplitude_pp (mV)')
plt.ylabel('phi (deg)')

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
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'_Bgsub.txt''',phase)        

Bfield(0) 






#####TP6
rampVG4(-809)
rampVG3(-924.5)

rampVG5(0)

G1now=VG1()
G2now=VG2()
G3now=VG3()
G4now=VG4()
G5now=VG5()
VG3comp()
VG4comp()
# VG1onmin(G1now-60,G1now+60,801,1)
VG1now=VG1()
VG1onmin(G1now-4,G1now+4,801,1)
VG1now=VG1()
VG2onmin(G2now-4,G2now+4,801,1)
G2now=VG2()
# VG5onmin(G5now-4,G5now+4,801,1)

name='0T_TP6G4vsG3_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
a,dataid,c,d=sweep2D(VG3comp,-922,-927,51,0.1,VG4comp,-804,-811,71,0.01111,ph1)
# a,dataid,c,d=sweep2D(VG3comp,-942,-946,71,0.1,VG4comp,-794,-802,111,0.01111,ph1)
# a,dataid,c,d=sweep2D(VG3comp,-939,-946,101,0.1,VG4comp,-794,-798,81,0.01777,ph1)
plot_by_id(dataid)
saveplot(name,dataid)



################## TP6
name='detuningvsBfield_TP6_'

###
detuningPoint1 = [-925.6,-806.3] 
detuningPoint2 = [-924,-807.8]          # [G3(x), G4(y)]

detpoints=201
detuning = qc.combine(VG3, VG4, name = 'detuning', unit= 'points')
eps=np.sqrt((detuningPoint1[0]-detuningPoint2[0])**2 +(detuningPoint1[1]-detuningPoint2[1])**2) 
VG3(detuningPoint1[0])
VG4(detuningPoint1[1])

det=generateEpsilonAxis(detuningPoint1, detuningPoint2, detpoints)
eps=np.sqrt((detuningPoint1[0]-detuningPoint2[0])**2 +(detuningPoint1[1]-detuningPoint2[1])**2) 
epsilon=np.linspace(-eps/2,eps/2,detpoints)

phases=[]
Barr=[]
G1pos=[]
G2pos=[]
for j in range(0,51):
    Bfield_Hon( 0.05*j)
    Barr.append(Bfield())
    phasedet=[]
    VG3comp(det[-1][0])
    VG4comp(det[-1][1])
    VG1now=VG1()
    VG1onmin(G1now-1.5,G1now+1.5,201,1)
    G1now=VG1()
    VG2onmin(G2now-1,G2now+1,201,1)
    G2now=VG2()
    G1pos.append(G1now)
    G2pos.append(G2now)
    for i in range(0,len(det)):
        VG3comp(det[i][0])
        VG4comp(det[i][1])
        time.sleep(0.02)
        phasedet.append(ph1())
    phases.append(phasedet)    


f= plt.figure()       
plt.plot(G2pos)
# ax.x
plt.xlabel('B (A.U.)')
# plt.ylabel('pulse amplitude_pp (mV)')
plt.ylabel('G2 position')
plt.savefig(folder2+'\\'+dayFolder+'\\G2position_Bfrom2.5to0T.png')

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
 
Bfield(0) 





############TP7

#####TP7
rampVG4(-802)
rampVG3(-941)

rampVG5(0)

G1now=VG1()
G2now=VG2()
G3now=VG3()
G4now=VG4()
G5now=VG5()
VG3comp()
VG4comp()
VG1onmin(G1now-60,G1now+60,801,1)
G1now=VG1()
VG1onmin(G1now-4,G1now+4,801,1)
VG1now=VG1()
VG2onmin(G2now-4,G2now+4,801,1)
G2now=VG2()
# VG5onmin(G5now-4,G5now+4,801,1)

name=str(Bfield())+'T_TP7G4vsG3_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
a,dataid,c,d=sweep2D(VG3comp,-938,-943,51,0.1,VG4comp,-797,-802,51,0.01111,ph1)
# a,dataid,c,d=sweep2D(VG4comp,-797,-802,51,0.1,VG3comp,-938,-943,51,0.03,ph1)
# a,dataid,c,d=sweep2D(VG3comp,-942,-946,71,0.1,VG4comp,-794,-802,111,0.01111,ph1)
# a,dataid,c,d=sweep2D(VG3comp,-939,-946,101,0.1,VG4comp,-794,-798,81,0.01777,ph1)
plot_by_id(dataid)
saveplot(name,dataid)



################## TP7
name='detuningvsBfield_TP7_noreset_initin02_'

###
detuningPoint1 = [-940.9,-799.2] 
detuningPoint2 = [-939.7,-800.7]          # [G3(x), G4(y)]

detpoints=201
detuning = qc.combine(VG3, VG4, name = 'detuning', unit= 'points')
eps=np.sqrt((detuningPoint1[0]-detuningPoint2[0])**2 +(detuningPoint1[1]-detuningPoint2[1])**2) 
VG3(detuningPoint1[0])
VG4(detuningPoint1[1])

det=generateEpsilonAxis(detuningPoint1, detuningPoint2, detpoints)
eps=np.sqrt((detuningPoint1[0]-detuningPoint2[0])**2 +(detuningPoint1[1]-detuningPoint2[1])**2) 
epsilon=np.linspace(-eps/2,eps/2,detpoints)

phases=[]
Barr=[]
G1pos=[]
G2pos=[]
G1min=[]
for j in range(0,121):
    Bfield_Hon(0.025*j)
    Barr.append(Bfield())
    phasedet=[]
    VG3comp(det[0][0])
    VG4comp(det[0][1])
    # VG1now=VG1()
    VG1onmin(G1now-1,G1now+1,201,0)
    G1now=VG1()
    # VG2onmin(G2now-1,G2now+1,201,0)
    # G2now=VG2()
    phimin=ph1()
    G1min.append(ph1())
    G1pos.append(G1now)
    # G2pos.append(G2now)
    for i in range(0,len(det)):
        VG3comp(det[i][0])
        VG4comp(det[i][1])
        time.sleep(0.01)
        phasedet.append(ph1())
    G1min.append(phimin-ph1())
    phases.append(phasedet)    


f= plt.figure()       
plt.plot(G1pos)
# ax.x
plt.xlabel('B (A.U.)')
# plt.ylabel('pulse amplitude_pp (mV)')
plt.ylabel('G1 position(mV)')
plt.savefig(folder2+'\\'+dayFolder+'\\G1pos_Bfrom3to0T.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'G1pos_Bfrom3to0T.txt',G1pos)  

f= plt.figure()       
plt.plot(G1min)
# ax.x
plt.xlabel('B (A.U.)')
# plt.ylabel('pulse amplitude_pp (mV)')
plt.ylabel('G1 contrast(rad)')
plt.savefig(folder2+'\\'+dayFolder+'\\G1minminusmax_Bfrom3to0T.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'G1min_Bfrom3to0T.txt',G1min)  

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
 
Bfield(0) 


G1now=VG1()
G2now=VG2()
VG1onmin(G1now-4,G1now+4,201,0)
G1now=VG1()
VG2onmin(G2now-4,G2now+4,201,0)



############TP7

#####TP7
rampVG4(-802)
rampVG3(-940)

rampVG5(0)

G1now=VG1()
G2now=VG2()
G3now=VG3()
G4now=VG4()
G5now=VG5()
VG3comp()
VG4comp()
VG1onmin(G1now-60,G1now+60,801,1)
VG1now=VG1()
VG1onmin(G1now-4,G1now+4,801,1)
G1now=VG1()
VG2onmin(G2now-4,G2now+4,801,1)
G2now=VG2()
# VG5onmin(G5now-4,G5now+4,801,1)

name='3T_TP7G4vsG3_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
a,dataid,c,d=sweep2D(VG3comp,-935,-945,41,0.1,VG4comp,-795,-852,51,0.01111,ph1)
# a,dataid,c,d=sweep2D(VG3comp,-942,-946,71,0.1,VG4comp,-794,-802,111,0.01111,ph1)
# a,dataid,c,d=sweep2D(VG3comp,-939,-946,101,0.1,VG4comp,-794,-798,81,0.01777,ph1)
plot_by_id(dataid)
saveplot(name,dataid)

VG3comp(-940.6)
sensor_on_interdot_sweepG4comp(-797,-802,401,1)


################## TP7
name='detuningvsBfield_TP7_noreset_initin11_'

###
detuningPoint2 = [-940,-800.5] 
detuningPoint1 = [-940.6,-798.5]          # [G3(x), G4(y)]

detpoints=201
detuning = qc.combine(VG3, VG4, name = 'detuning', unit= 'points')
eps=np.sqrt((detuningPoint1[0]-detuningPoint2[0])**2 +(detuningPoint1[1]-detuningPoint2[1])**2) 
VG3comp(detuningPoint1[0])
VG4comp(detuningPoint1[1])

det=generateEpsilonAxis(detuningPoint1, detuningPoint2, detpoints)
eps=np.sqrt((detuningPoint1[0]-detuningPoint2[0])**2 +(detuningPoint1[1]-detuningPoint2[1])**2) 
epsilon=np.linspace(+eps/2,-eps/2,detpoints)

phases=[]
Barr=[]
G1pos=[]
G2pos=[]
G1min=[]
phases_smooth=[]
for j in range(0,61):
    Bfield_Hon(3-0.05*j)
    Barr.append(Bfield())
    phasedet=[]
    VG3comp(det[-1][0])
    VG4comp(det[-1][1])
    time.sleep(0.1)
    VG1now=VG1()
    VG1onmin(G1now-1,G1now+1,201,0)
    G1now=VG1()
    # VG2onmin(G2now-1,G2now+1,201,0)
    # G2now=VG2()
    phimin=ph1()

    G1pos.append(G1now)
    # G2pos.append(G2now)
    for i in range(0,len(det)):
        VG3comp(det[i][0])
        VG4comp(det[i][1])
        time.sleep(0.05)
        phasedet.append(ph1())
    # f= plt.figure()    
    # plt.plot(phasedet)    
    G1min.append(phimin-ph1())
    phases.append(phasedet) 
    phases_smooth.append(scipy.signal.savgol_filter( np.ravel(phasedet),11,3) )
    
    if j%10==0:
        phimin=np.min(phases_smooth[j])
        phimax=np.max(phases_smooth[j])
        argmin=np.argmin(phases_smooth[j])
        kmin=0
        kmax=0
        philim=phimin+(phimax-phimin)/2
        sigmaphi=0.05
        for k in range(0,len(det)):
            if ((phases_smooth[j][k]>=(philim-sigmaphi) and phases_smooth[0][k]<=(philim+sigmaphi)) and kmax==0):
                kmax=k
            
            #typicalFWHM is <1.5mVdef VT2onmin(initVB1,finalVB1,points,showplot):
       
        VG4comp(det[kmax][1])
        VG3comp(det[kmax][0])
        # sensor_on_interdot_sweepG4comp(-797,-800.5,301,1)
        
        
        ####pulse vs amplitude
        trigger_mode()
        ziUhf.daq.setInt('/dev2010/sigouts/1/on', 1)    
        t=np.linspace(0,6e-3,points)
        phasearray=[]
        amp=[]
        
        for i in range(0,201):
            amp.append(ampliAWG())
            ampliAWG(i*0.005)
            phasearray.append(phase_trig())
        ziUhf.daq.setInt('/dev2010/sigouts/1/on', 0)    
        
        phase=[]
        for i in range(0,201):
            phase.append(phasearray[i][0])
        
        plt.plot(phase)
        Y= amp
        X = t
        ZZ=phase
        
        
        f = plt.figure()
        plt.pcolor(X,Y,ZZ,cmap='viridis')
        # plt.clim(vmin=None,vmax=0.3)
        plt.colorbar(label='phi(deg)')
        plt.xlabel('t(s)')
        # plt.ylabel('pulse amplitude_pp (mV)')
        plt.ylabel('pulse amplitude_pp (AWG)')
        
        now=datetime.datetime.now()
        dayFolder=datetime.date.isoformat(now)
        name='TP7_pulsevspulse_amplitude_200repB_'+str(Bfield())
        plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
        np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt''',phase)
        ziUhf.daq.setInt('/dev2010/sigouts/1/on', 0)  
        continuous_acquisition()

name='detuningvsBfield_TP7_resetG1_initin11_'
f= plt.figure()    

# plt.plot(phases_smooth[0])   
plt.plot(G1pos)
# ax.x
plt.xlabel('B (A.U.)')
# plt.ylabel('pulse amplitude_pp (mV)')
plt.ylabel('G1 position(mV)')
plt.savefig(folder2+'\\'+dayFolder+'\\G1pos_Bfrom3to0T.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'G1pos_Bfrom3to0T.txt',G1pos)  

f= plt.figure()       
plt.plot(G1min)
# ax.x
plt.xlabel('B (A.U.)')
# plt.ylabel('pulse amplitude_pp (mV)')
plt.ylabel('G1 contrast(rad)')
plt.savefig(folder2+'\\'+dayFolder+'\\G1minminusmax_Bfrom3to0T.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'G1min_Bfrom3to0T.txt',G1min)  

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
 
Bfield(0) 


Z3=phases_smooth
Z3=np.reshape(Z3,(len(Y),len(X)))
Z3=removeBackground(Z3)
f = plt.figure()
plt.pcolor(X,Y,Z3,cmap='viridis')
# plt.clim(vmin=None,vmax=0.3)
plt.colorbar(label='phi(deg)')
plt.xlabel('detuning (mV)')
# plt.ylabel('pulse amplitude_pp (mV)')
plt.ylabel('B (T)')
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'_smooth.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'_smooth.txt',Z3)  

# f = plt.figure()
# plt.pcolor(X,Y,Z,cmap='viridis')
# # plt.clim(vmin=None,vmax=0.3)
# plt.colorbar(label='phi(deg)')
# plt.xlabel('detuning (mV)')
# # plt.ylabel('pulse amplitude_pp (mV)')
# plt.ylabel('B (T)')
# plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
# np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',Z3)  