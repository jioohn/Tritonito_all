# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 23:39:06 2021

@author: G-GRE-GRE050402
"""

# num_point=201

startG4=-973.5
stopG4=-976
startG3=-766.8
stopG3=-766
DeltaG3=np.abs(startG3-stopG3)
DeltaG4=np.abs(startG4-stopG4)

cr=DeltaG3/DeltaG4

ziUhf.daq.setDouble('/dev2010/auxouts/0/scale', 0.15*cr)
ziUhf.daq.setDouble('/dev2010/auxouts/1/scale', 0.15)
ziUhf.daq.setDouble('/dev2010/auxouts/2/scale', -0.03*cr)
ziUhf.daq.setDouble('/dev2010/auxouts/3/scale', -0.03)




ampliAWG(0.05)

acquisition_duration=400e-6
efftc=3e-6
delay=0e-6
# such that the effective Tc is 100ms 
# repetitions=tc/efftc/5

repetitions=1000

ziUhf.daq.setInt('/dev2010/demods/0/trigger', 33554432) # demodulator trigger set on AWGtrigger2 High
ziUhf.daq.setDouble('/dev2010/demods/0/rate', 400e3)
ziUhf.daq.setDouble('/dev2010/demods/1/rate', 400e3)

# ziUhf.daq.setDouble('/dev2010/demods/1/rate', 2e6)
# ziUhf.daq.setDouble('/dev2010/demods/0/rate', 2e6)
ziUhf.daq.setInt('/dev2010/demods/0/order', 1)
ziUhf.daq.setInt('/dev2010/demods/1/order', 1)

points=int(acquisition_duration*ziUhf.daq.getDouble('/dev2010/demods/0/rate'))


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

# phases_trig= SpecialParameters.Pulsed_readout_both(ziUhf, repetitions, returnOnePoint=False)
phases_trig= SpecialParameters.Pulsed_readout_both(ziUhf, repetitions, returnOnePoint=False)
phases_trig.setSettings(trigger_setting, grid_setting)
# Duration of the time trace to record:


# Vreads = np.arange(-0.3,0.015,0.0005)



Npoints=101
# tc=2e-6
# total_time=1
# demod_S=2
# demod_D=1
# startG4=-975
# stopG4=-978
# startG3=-764.5
# stopG3=-763

G4ar=np.linspace(startG4,stopG4,Npoints)

G3ar=np.linspace(startG3,stopG3,Npoints)



# Vread = Vreads[i]      
t=np.linspace(0,acquisition_duration,points)

phaseDarray=[]
phaseSarray=[]



for i in range(0,Npoints):
    VG4comp(G4ar[i])
    VG3comp(G3ar[i])
    print(VG4())
    s,d=phases_trig()
    phaseSarray.append(s)
    phaseDarray.append(d)
# ziUhf.daq.setInt('/dev2010/sigouts/1/on', 0)    

phaseS=[]
for i in range(0,Npoints):
    phaseS.append(phaseSarray[i][0])
    
phaseD=[]
for i in range(0,Npoints):
    phaseD.append(phaseDarray[i][0])
    
    
    
# ampli_list=ampli_list*4.55
t=np.linspace(0,acquisition_duration,points)



M=phaseS

title=str(Bfield())+'T_phS_DIAG_detuningvstime_ampliAWG'+str(np.round(ampliAWG(),3))+'mV_G5'+str(VG5())+'mV_G4'+str(VG4())+'mV_G3'+str(VG3())+'mV_____'


#Create and save plot

fig,ax = plt.subplots()
# plt.pcolor(t*1e6,Vreads,np.transpose(M))
plt.pcolor(t*1e6,G4ar,M)
plt.ylabel('$G4(mV)$',fontsize=18)
plt.xlabel('t ($\mu$s)',fontsize=18)
cb=plt.colorbar()
cb.set_label('$\phi_S$ (rad)',fontsize=18)

ax.tick_params(labelsize=14)
ax.set_title('B='+str(Bfield())+'T_ampliAWG'+str(np.round(ampliAWG(),3)),size=18)
fig.tight_layout()


now=datetime.datetime.now()
dayFolder= datetime.date.isoformat(now)
try:
    os.makedirs(folder2+'\\'+dayFolder)
except IOError:
    donothing=1
    
plt.savefig(folder2+'\\'+dayFolder+'\\'+title+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'.txt',M)


M=phaseD


title=str(Bfield())+'T_phD_detuningvstime_ampliAWG'+str(np.round(ampliAWG(),3))+'_100us__G5'+str(VG5())+'mV_G4'+str(VG4())+'mV_G3'+str(VG3())+'mV_____'



plt.ylabel('$G4(mV)$',fontsize=18)
fig,ax = plt.subplots()

plt.pcolor(t*1e6,G4ar,M)
plt.xlabel('t ($\mu$s)',fontsize=18)
cb=plt.colorbar()
cb.set_label('$\phi_D$ (rad)',fontsize=18)

ax.tick_params(labelsize=14)
ax.set_title('B='+str(Bfield())+'T_ampliAWG'+str(np.round(ampliAWG(),3))+'',size=18)
fig.tight_layout()


now=datetime.datetime.now()
dayFolder= datetime.date.isoformat(now)
try:
    os.makedirs(folder2+'\\'+dayFolder)
except IOError:
    donothing=1
    
plt.savefig(folder2+'\\'+dayFolder+'\\'+title+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'.txt',M)


ampliAWG(-0.05)
t=np.linspace(0,acquisition_duration,points)

phaseDarray=[]
phaseSarray=[]



for i in range(0,Npoints):
    VG4comp(G4ar[i])
    VG3comp(G3ar[i])
    print(VG4())
    s,d=phases_trig()
    phaseSarray.append(s)
    phaseDarray.append(d)
# ziUhf.daq.setInt('/dev2010/sigouts/1/on', 0)    

phaseS=[]
for i in range(0,Npoints):
    phaseS.append(phaseSarray[i][0])
    
phaseD=[]
for i in range(0,Npoints):
    phaseD.append(phaseDarray[i][0])
    
    
    
# ampli_list=ampli_list*4.55
t=np.linspace(0,acquisition_duration,points)



M=phaseS

title=str(Bfield())+'T_phS_DIAG_detuningvstime_ampliAWG'+str(np.round(ampliAWG(),3))+'mV_G5'+str(VG5())+'mV_G4'+str(VG4())+'mV_G3'+str(VG3())+'mV_____'


#Create and save plot

fig,ax = plt.subplots()
# plt.pcolor(t*1e6,Vreads,np.transpose(M))
plt.pcolor(t*1e6,G4ar,M)
plt.ylabel('$G4(mV)$',fontsize=18)
plt.xlabel('t ($\mu$s)',fontsize=18)
cb=plt.colorbar()
cb.set_label('$\phi_S$ (rad)',fontsize=18)

ax.tick_params(labelsize=14)
ax.set_title('B='+str(Bfield())+'T_ampliAWG'+str(np.round(ampliAWG(),3)),size=18)
fig.tight_layout()


now=datetime.datetime.now()
dayFolder= datetime.date.isoformat(now)
try:
    os.makedirs(folder2+'\\'+dayFolder)
except IOError:
    donothing=1
    
plt.savefig(folder2+'\\'+dayFolder+'\\'+title+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'.txt',M)


M=phaseD


title=str(Bfield())+'T_phD_detuningvstime_ampliAWG'+str(np.round(ampliAWG(),3))+'_100us__G5'+str(VG5())+'mV_G4'+str(VG4())+'mV_G3'+str(VG3())+'mV_____'



plt.ylabel('$G4(mV)$',fontsize=18)
fig,ax = plt.subplots()

plt.pcolor(t*1e6,G4ar,M)
plt.xlabel('t ($\mu$s)',fontsize=18)
cb=plt.colorbar()
cb.set_label('$\phi_D$ (rad)',fontsize=18)

ax.tick_params(labelsize=14)
ax.set_title('B='+str(Bfield())+'T_ampliAWG'+str(np.round(ampliAWG(),3))+'',size=18)
fig.tight_layout()


now=datetime.datetime.now()
dayFolder= datetime.date.isoformat(now)
try:
    os.makedirs(folder2+'\\'+dayFolder)
except IOError:
    donothing=1
    
plt.savefig(folder2+'\\'+dayFolder+'\\'+title+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'.txt',M)



ampliAWG(0.1)

t=np.linspace(0,acquisition_duration,points)

phaseDarray=[]
phaseSarray=[]



for i in range(0,Npoints):
    VG4comp(G4ar[i])
    VG3comp(G3ar[i])
    print(VG4())
    s,d=phases_trig()
    phaseSarray.append(s)
    phaseDarray.append(d)
# ziUhf.daq.setInt('/dev2010/sigouts/1/on', 0)    

phaseS=[]
for i in range(0,Npoints):
    phaseS.append(phaseSarray[i][0])
    
phaseD=[]
for i in range(0,Npoints):
    phaseD.append(phaseDarray[i][0])
    
    
    
# ampli_list=ampli_list*4.55
t=np.linspace(0,acquisition_duration,points)



M=phaseS

title=str(Bfield())+'T_phS_DIAG_detuningvstime_ampliAWG'+str(np.round(ampliAWG(),3))+'mV_G5'+str(VG5())+'mV_G4'+str(VG4())+'mV_G3'+str(VG3())+'mV_____'


#Create and save plot

fig,ax = plt.subplots()
# plt.pcolor(t*1e6,Vreads,np.transpose(M))
plt.pcolor(t*1e6,G4ar,M)
plt.ylabel('$G4(mV)$',fontsize=18)
plt.xlabel('t ($\mu$s)',fontsize=18)
cb=plt.colorbar()
cb.set_label('$\phi_S$ (rad)',fontsize=18)

ax.tick_params(labelsize=14)
ax.set_title('B='+str(Bfield())+'T_ampliAWG'+str(np.round(ampliAWG(),3)),size=18)
fig.tight_layout()


now=datetime.datetime.now()
dayFolder= datetime.date.isoformat(now)
try:
    os.makedirs(folder2+'\\'+dayFolder)
except IOError:
    donothing=1
    
plt.savefig(folder2+'\\'+dayFolder+'\\'+title+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'.txt',M)


M=phaseD


title=str(Bfield())+'T_phD_detuningvstime_ampliAWG'+str(np.round(ampliAWG(),3))+'_100us__G5'+str(VG5())+'mV_G4'+str(VG4())+'mV_G3'+str(VG3())+'mV_____'



plt.ylabel('$G4(mV)$',fontsize=18)
fig,ax = plt.subplots()

plt.pcolor(t*1e6,G4ar,M)
plt.xlabel('t ($\mu$s)',fontsize=18)
cb=plt.colorbar()
cb.set_label('$\phi_D$ (rad)',fontsize=18)

ax.tick_params(labelsize=14)
ax.set_title('B='+str(Bfield())+'T_ampliAWG'+str(np.round(ampliAWG(),3))+'',size=18)
fig.tight_layout()


now=datetime.datetime.now()
dayFolder= datetime.date.isoformat(now)
try:
    os.makedirs(folder2+'\\'+dayFolder)
except IOError:
    donothing=1
    
plt.savefig(folder2+'\\'+dayFolder+'\\'+title+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'.txt',M)



ampliAWG(0.2)

t=np.linspace(0,acquisition_duration,points)

phaseDarray=[]
phaseSarray=[]



for i in range(0,Npoints):
    VG4comp(G4ar[i])
    VG3comp(G3ar[i])
    print(VG4())
    s,d=phases_trig()
    phaseSarray.append(s)
    phaseDarray.append(d)
# ziUhf.daq.setInt('/dev2010/sigouts/1/on', 0)    

phaseS=[]
for i in range(0,Npoints):
    phaseS.append(phaseSarray[i][0])
    
phaseD=[]
for i in range(0,Npoints):
    phaseD.append(phaseDarray[i][0])
    
    
    
# ampli_list=ampli_list*4.55
t=np.linspace(0,acquisition_duration,points)



M=phaseS

title=str(Bfield())+'T_phS_DIAG_detuningvstime_ampliAWG'+str(np.round(ampliAWG(),3))+'mV_G5'+str(VG5())+'mV_G4'+str(VG4())+'mV_G3'+str(VG3())+'mV_____'


#Create and save plot

fig,ax = plt.subplots()
# plt.pcolor(t*1e6,Vreads,np.transpose(M))
plt.pcolor(t*1e6,G4ar,M)
plt.ylabel('$G4(mV)$',fontsize=18)
plt.xlabel('t ($\mu$s)',fontsize=18)
cb=plt.colorbar()
cb.set_label('$\phi_S$ (rad)',fontsize=18)

ax.tick_params(labelsize=14)
ax.set_title('B='+str(Bfield())+'T_ampliAWG'+str(np.round(ampliAWG(),3)),size=18)
fig.tight_layout()


now=datetime.datetime.now()
dayFolder= datetime.date.isoformat(now)
try:
    os.makedirs(folder2+'\\'+dayFolder)
except IOError:
    donothing=1
    
plt.savefig(folder2+'\\'+dayFolder+'\\'+title+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'.txt',M)


M=phaseD


title=str(Bfield())+'T_phD_detuningvstime_ampliAWG'+str(np.round(ampliAWG(),3))+'_100us__G5'+str(VG5())+'mV_G4'+str(VG4())+'mV_G3'+str(VG3())+'mV_____'



plt.ylabel('$G4(mV)$',fontsize=18)
fig,ax = plt.subplots()

plt.pcolor(t*1e6,G4ar,M)
plt.xlabel('t ($\mu$s)',fontsize=18)
cb=plt.colorbar()
cb.set_label('$\phi_D$ (rad)',fontsize=18)

ax.tick_params(labelsize=14)
ax.set_title('B='+str(Bfield())+'T_ampliAWG'+str(np.round(ampliAWG(),3))+'',size=18)
fig.tight_layout()


now=datetime.datetime.now()
dayFolder= datetime.date.isoformat(now)
try:
    os.makedirs(folder2+'\\'+dayFolder)
except IOError:
    donothing=1
    
plt.savefig(folder2+'\\'+dayFolder+'\\'+title+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'.txt',M)