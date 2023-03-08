# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 16:54:00 2021

@author: G-GRE-GRE050402
"""

###config
# 6_G3vsG4_G1-1694.3600000000001mV_G2-1057.3543mV_G3-821.0mV_G4-845.0mV_G5-1368.6687mV_G6-1866.3600000000001mV
VG1now=-1694
VG2now=-1057
VG3now=-821
VG4now=-845
VG5now=-1368
VG6now=-1866

rampVG1(VG1now)
rampVG2(VG2now)
rampVG3(VG3now)
rampVG4(VG4now)
rampVG5(VG5now)
rampVG6(VG6now)

#####
continuous_acquisition()
continuous_acquisition_ch2()
VG3comp(-821)
VG4comp(-845)
VG5now=VG5()
VG2now=VG2()
VG6now=VG6()
VG1now=VG1()

# VG6onmin_phD(VG6now-20,VG6now+20,401,1)
# VG1onmin_phS(VG1now-20,VG1now+20,401,1)

VG6onmin_phD(VG6now-3,VG6now+3,401,1)
VG1onmin_phS(VG1now-3,VG1now+3,401,1)
# Bfield(1.3)
name=str(Bfield())+'T_G3vsG4_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
a,dataid,c,d=sweep2D(VG3comp,-820,-825,51,0.02,VG4comp,-843,-847,51,0.02,ph1,ph2)

plot_by_id(dataid)
save2plots(name,dataid)


VG3comp(-821)
VG4comp(-845)
VG5now=VG5()
VG2now=VG2()
VG6now=VG6()
VG1now=VG1()

VG6onmin_phD(VG6now-20,VG6now+20,401,1)

# VG1onmin_phS(VG1now-10,VG1now+10,401,1)
VG1onmin_phS(VG1now-20,VG1now+20,401,1)
a,dataid,c,d=sweep2D(VG3comp,-810,-850,51,0.02,VG4comp,-810,-850,51,0.02,ph1,ph2)
plot_by_id(dataid)
save2plots(name,dataid)

VG3comp(-822)
VG4comp(-844)
VG5now=VG5()
VG2now=VG2()
VG6now=VG6()
VG1now=VG1()

VG6onmin_phD(VG6now-3,VG6now+3,401,1)


VG1onmin_phS(VG1now-3,VG1now+3,401,1)

name='G3vsG4zoom_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
a,dataid,c,d=sweep2D(VG3comp,-822,-824,21,0.02,VG4comp,-842,-844,21,0.014,ph1,ph2)
# a,dataid,c,d=sweep2D(VG3comp,-820-20*i,-840-20*i,201,0.02,VG4comp,-780-20*j,-800-20*j,201,0.012,ph1,ph2)
plot_by_id(dataid)
save2plots(name,dataid)






# repetitions = 1000           # number of repetitions for the averaging
# points = 71# number of points in the acquisition window (min=2)
#efftc=acquisition_duration/10

Bfield(2)
acquisition_duration=100e-6
efftc=500e-9

# such that the effective Tc is 100ms 
# repetitions=tc/efftc/5

repetitions=2000

ziUhf.daq.setInt('/dev2010/demods/0/trigger', 33554432) # demodulator trigger set on AWGtrigger2 High
ziUhf.daq.setDouble('/dev2010/demods/0/rate', 800e3)
ziUhf.daq.setDouble('/dev2010/demods/1/rate', 800e3)

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
Npoints=201

# Vreads=np.linspace(start,stop,Npoints)##real amplitudes in mV on G4

ampli_list=np.linspace(-0.3,0.3,Npoints)
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



M=phaseD


title=str(Bfield())+'T_phD_ampliAWGvstime_G5'+str(VG5())+'mV_G4'+str(VG4())+'mV_G3'+str(VG3())+'mV__'


#Enregistrement de la figure tracée 

fig,ax = plt.subplots()
# plt.pcolor(t*1e6,Vreads,np.transpose(M))
plt.pcolor(t*1e6,ampli_list,M)
plt.ylabel('$A(mV)$',fontsize=18)
plt.xlabel('t ($\mu$s)',fontsize=18)
cb=plt.colorbar()
cb.set_label('$\phi_D$ (Rad)')

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






M=phaseS

title=str(Bfield())+'T_phS_ampliAWGvstime_G5'+str(VG5())+'mV_G4'+str(VG4())+'mV_G3'+str(VG3())+'mV__'


#Enregistrement de la figure tracée 

fig,ax = plt.subplots()
# plt.pcolor(t*1e6,Vreads,np.transpose(M))
plt.pcolor(t*1e6,ampli_list,M)
plt.ylabel('$A(mV)$',fontsize=18)
plt.xlabel('t ($\mu$s)',fontsize=18)
cb=plt.colorbar()
cb.set_label('$\phi_D$ (Rad)')

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


################"
#3stage





Tempty=20e-6
Tload=20-6
Tread=100e-6

namefile='C:\\Users\\g-gre-gre050402\\Documents\\Zurich Instruments\\LabOne\\WebServer\\awg\\src\\diagonal_pulse.seqc'    



changetempty(namefile, Tempty) 
changetload(namefile, Tload) 
changetread(namefile, Tread) 




acquisition_duration=Tempty+Tload+Tread

efftc=1.25e-6

# such that the effective Tc is 100ms 
# repetitions=tc/efftc/5

repetitions=2000

ziUhf.daq.setInt('/dev2010/demods/0/trigger', 33554432) # demodulator trigger set on AWGtrigger2 High
# ziUhf.daq.setDouble('/dev2010/demods/0/rate', 800e3)
# ziUhf.daq.setDouble('/dev2010/demods/1/rate', 800e3)
# ziUhf.daq.setDouble('/dev2010/demods/0/rate', 2e6)
ziUhf.daq.setDouble('/dev2010/demods/1/rate', 800e3)
ziUhf.daq.setDouble('/dev2010/demods/0/rate', 800e3)
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




ampliAWG(-0.15)
Npoints=201

t=np.linspace(0,acquisition_duration,points)

phaseDarray=[]
phaseSarray=[]
amp=[]
# Npoints=101

Vreads=np.linspace(-0.5,+0.5,Npoints)##real amplitudes in mV on G3

# ampliAWG(0.2)

for i in range(0,Npoints):
    print(i)
    amplimV=Vreads[i]

    
    Readlevel(amplimV)
    ziUhf.daq.setInt('/dev2010/sigouts/0/enables/5', 1)
    ziUhf.daq.setInt('/dev2010/sigouts/0/enables/5', 1)

    # phaseSarray.append(phase_trigS())
    phaseDarray.append(phase_trigS())
# ziUhf.daq.setInt('/dev2010/sigouts/1/on', 0)    

# phaseS=[]
# for i in range(0,Npoints):
#     phaseS.append(phaseSarray[i][0])
    
phaseD=[]
for i in range(0,Npoints):
    phaseD.append(phaseDarray[i][0])
    
phaseS=[]
for i in range(0,Npoints):
    phaseS.append(phaseSarray[i][0])



now=datetime.datetime.now()
dayFolder= datetime.date.isoformat(now)
try:
    os.makedirs(folder2+'\\'+dayFolder)
except IOError:
    donothing=1


M=phaseS

title=str(Bfield())+'T_phS_amplireadvstime_awg'+str(ampliAWG())+'_G5'+str(VG5())+'mV_G4'+str(VG4())+'mV_G3'+str(VG3())+'mV'


#Enregistrement de la figure tracée 

fig,ax = plt.subplots()
# plt.pcolor(t*1e6,Vreads,np.transpose(M))
plt.pcolor(t*1e6,Vreads,M)
plt.ylabel('$A_{read} (mV)$',fontsize=18)
plt.xlabel('t ($\mu$s)',fontsize=18)
cb=plt.colorbar()
cb.set_label('$\phi_S$ (rad)')

ax.tick_params(labelsize=14)
ax.set_title('B='+str(Bfield()),size=18)
fig.tight_layout()


    
plt.savefig(folder2+'\\'+dayFolder+'\\'+title+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'.txt',M)




M=phaseD

title=str(Bfield())+'T_phD_amplireadvstime_awg'+str(ampliAWG())+'_G5'+str(VG5())+'mV_G4'+str(VG4())+'mV_G3'+str(VG3())+'mV'


#Enregistrement de la figure tracée 

fig,ax = plt.subplots()
# plt.pcolor(t*1e6,Vreads,np.transpose(M))
plt.pcolor(t*1e6,Vreads,M)
plt.ylabel('$A_{read} (mV)$',fontsize=18)
plt.xlabel('t ($\mu$s)',fontsize=18)
cb=plt.colorbar()
cb.set_label('$\phi_D$ (rad)')

ax.tick_params(labelsize=14)
ax.set_title('B='+str(Bfield()),size=18)
fig.tight_layout()


    
plt.savefig(folder2+'\\'+dayFolder+'\\'+title+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'.txt',M)




ampliAWG(+0.15)
Npoints=201

t=np.linspace(0,acquisition_duration,points)

phaseDarray=[]
phaseSarray=[]
amp=[]
# Npoints=101

Vreads=np.linspace(-0.5,+0.5,Npoints)##real amplitudes in mV on G3

# ampliAWG(0.2)

for i in range(0,Npoints):
    print(i)
    amplimV=Vreads[i]

    
    Readlevel(amplimV)
    ziUhf.daq.setInt('/dev2010/sigouts/0/enables/5', 1)
    ziUhf.daq.setInt('/dev2010/sigouts/0/enables/5', 1)

    # phaseSarray.append(phase_trigS())
    phaseDarray.append(phase_trigS())
# ziUhf.daq.setInt('/dev2010/sigouts/1/on', 0)    

# phaseS=[]
# for i in range(0,Npoints):
#     phaseS.append(phaseSarray[i][0])
    
phaseD=[]
for i in range(0,Npoints):
    phaseD.append(phaseDarray[i][0])
    
phaseS=[]
for i in range(0,Npoints):
    phaseS.append(phaseSarray[i][0])



now=datetime.datetime.now()
dayFolder= datetime.date.isoformat(now)
try:
    os.makedirs(folder2+'\\'+dayFolder)
except IOError:
    donothing=1


M=phaseS

title=str(Bfield())+'T_phS_amplireadvstime_awg'+str(ampliAWG())+'_G5'+str(VG5())+'mV_G4'+str(VG4())+'mV_G3'+str(VG3())+'mV'


#Enregistrement de la figure tracée 

fig,ax = plt.subplots()
# plt.pcolor(t*1e6,Vreads,np.transpose(M))
plt.pcolor(t*1e6,Vreads,M)
plt.ylabel('$A_{read} (mV)$',fontsize=18)
plt.xlabel('t ($\mu$s)',fontsize=18)
cb=plt.colorbar()
cb.set_label('$\phi_S$ (rad)')

ax.tick_params(labelsize=14)
ax.set_title('B='+str(Bfield()),size=18)
fig.tight_layout()


    
plt.savefig(folder2+'\\'+dayFolder+'\\'+title+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'.txt',M)




M=phaseD

title=str(Bfield())+'T_phD_amplireadvstime_awg'+str(ampliAWG())+'_G5'+str(VG5())+'mV_G4'+str(VG4())+'mV_G3'+str(VG3())+'mV'


#Enregistrement de la figure tracée 

fig,ax = plt.subplots()
# plt.pcolor(t*1e6,Vreads,np.transpose(M))
plt.pcolor(t*1e6,Vreads,M)
plt.ylabel('$A_{read} (mV)$',fontsize=18)
plt.xlabel('t ($\mu$s)',fontsize=18)
cb=plt.colorbar()
cb.set_label('$\phi_D$ (rad)')

ax.tick_params(labelsize=14)
ax.set_title('B='+str(Bfield()),size=18)
fig.tight_layout()


    
plt.savefig(folder2+'\\'+dayFolder+'\\'+title+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'.txt',M)










#########################
########################
################

name=str(Bfield())+'G3vsG4comp_trigacq_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
a,dataid,c,d=sweep2D(VG3comp,-817,-823,51,0.02,VG4comp,-838,-843,51,0.014,phase_trigS,phase_trigD)

plot_by_id(dataid)
save2plots(name,dataid)

#################
detuningPoint1 = [-821.7,-841]  #TPC #G3,G4
detuningPoint2 = [-820,-842.8] 
VG3comp(detuningPoint1[0])
VG4comp(detuningPoint1[1])
DeltaG4G3=(detuningPoint1[0]-detuningPoint2[0])/(detuningPoint1[1]-detuningPoint2[1])


G4detuning=  SpecialParameters.DetuningG4(VG4,VG3,DeltaG4G3)

name=str(Bfield())+'G4detuningscan_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
a,dataid,c=sweep1D(G4detuning,-841,-842.8,241,0.02,ph1,ph2)
plot_by_id(dataid)
save2plots(name,dataid)





