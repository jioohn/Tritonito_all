# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 17:06:36 2021

@author: G-GRE-GRE050402
"""


startG4=-811.5
stopG4=-812.6
startG3=-865
stopG3=-863
DeltaG3=np.abs(startG3-stopG3)
DeltaG4=np.abs(startG4-stopG4)

cr=DeltaG3/DeltaG4

ziUhf.daq.setDouble('/dev2010/auxouts/0/scale', 0.15*cr)
ziUhf.daq.setDouble('/dev2010/auxouts/1/scale', 0.15)
ziUhf.daq.setDouble('/dev2010/auxouts/2/scale', -0.03*cr)
ziUhf.daq.setDouble('/dev2010/auxouts/3/scale', -0.03)
VG4comp(startG4)
VG3comp(startG3)


ziUhf.daq.setDouble('/dev2010/auxouts/1/scale', 0.15)
ziUhf.daq.setDouble('/dev2010/auxouts/3/scale', -0.03)

ziUhf.daq.setDouble('/dev2010/auxouts/0/scale', 0.15)
ziUhf.daq.setDouble('/dev2010/auxouts/2/scale', -0.03)


# Bfield(2)
ziUhf.daq.setDouble('/dev2010/auxouts/1/scale', 0.15)
ziUhf.daq.setDouble('/dev2010/auxouts/3/scale', -0.03)

ziUhf.daq.setDouble('/dev2010/auxouts/0/scale', 0.15/2)
ziUhf.daq.setDouble('/dev2010/auxouts/2/scale', -0.03/2)



acquisition_duration=400e-6
efftc=4e-6
delay=0e-6
# such that the effective Tc is 100ms 
# repetitions=tc/efftc/5

repetitions=500

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


# Duration of the time trace to record:


# Vreads = np.arange(-0.3,0.015,0.0005)

# Vread = Vreads[i]      
t=np.linspace(0,acquisition_duration,points)

phaseDarray=[]
phaseSarray=[]
amp=[]
Npoints=51

# Vreads=np.linspace(start,stop,Npoints)##real amplitudes in mV on G4

ampli_list=np.linspace(0,1,Npoints)
# ampliAWG(0.2)

for i in range(0,Npoints):
    ampliAWG(ampli_list[i])
    print(ampliAWG())
    phaseSarray.append(phase_trigS())
    phaseDarray.append(phase_trigD())
# ziUhf.daq.setInt('/dev2010/sigouts/1/on', 0)    

phaseS=[]
for i in range(0,Npoints):
    phaseS.append(phaseSarray[i][0])
    
phaseD=[]
for i in range(0,Npoints):
    phaseD.append(phaseDarray[i][0])
    
    
    
ampli_list=ampli_list*4.55
t=np.linspace(0,acquisition_duration,points)



M=phaseS

title=str(Bfield())+'T_phS_DIAG_sitinterdot_200usampliAWGvstime_G3overG4ampli'+str(np.round(ziUhf.daq.getDouble('/dev2010/auxouts/0/scale')/ziUhf.daq.getDouble('/dev2010/auxouts/1/scale'),3))+'_G4'+str(VG4())+'mV_G3'+str(VG3())+'mV'


#Create and save plot

fig,ax = plt.subplots()
# plt.pcolor(t*1e6,Vreads,np.transpose(M))
plt.pcolor(t*1e6,ampli_list,M)
plt.ylabel('$A(mV)$',fontsize=18)
plt.xlabel('t ($\mu$s)',fontsize=18)
cb=plt.colorbar()
cb.set_label('$\phi_S$ (rad)',fontsize=18)

ax.tick_params(labelsize=14)
ax.set_title('B='+str(Bfield()),size=18)
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


title=str(Bfield())+'T_phD_DIAG_sitinterdot_200us_ampliAWGvstime_G3overG4ampli'+str(np.round(ziUhf.daq.getDouble('/dev2010/auxouts/0/scale')/ziUhf.daq.getDouble('/dev2010/auxouts/1/scale'),3))+'_G4'+str(VG4())+'mV_G3'+str(VG3())+'mV'



fig,ax = plt.subplots()

plt.pcolor(t*1e6,ampli_list,M)
plt.ylabel('$A(mV)$',fontsize=18)
plt.xlabel('t ($\mu$s)',fontsize=18)
cb=plt.colorbar()
cb.set_label('$\phi_D$ (rad)',fontsize=18)

ax.tick_params(labelsize=14)
ax.set_title('B='+str(Bfield()),size=18)
fig.tight_layout()


now=datetime.datetime.now()
dayFolder= datetime.date.isoformat(now)
try:
    os.makedirs(folder2+'\\'+dayFolder)
except IOError:
    donothing=1
    
plt.savefig(folder2+'\\'+dayFolder+'\\'+title+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'.txt',M)


