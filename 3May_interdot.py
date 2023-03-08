# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 13:38:50 2021

@author: G-GRE-GRE050402
"""
def config1537():
    rampVG1(-1694)
    rampVG2(-1055)
    rampVG3(-821)
    rampVG4(-845)
    rampVG5(-1368)
    rampVG6(-1863)
    bias(-0.2)
    


VG6now=VG6()
VG5now=VG5()
VG2now=VG2()
VG1now=VG1()


continuous_acquisition()
continuous_acquisition_ch2()

VG4comp(-812)
VG3comp(-862.5)
VG6now=VG6()
VG5now=VG5()
VG2now=VG2()
VG1now=VG1()


# VG6onmin_phD(VG6now-30,VG6now+30,1201,1)
VG6onmin_phD(VG6now-3,VG6now+3,401,1)
# VG5onmin_phD(VG5now-3,VG5now+3,401,1)
VG1onmin_phS(VG1now-3,VG1now+3,401,1)
# VG1onmin_phS(VG1now-30,VG1now+30,1201,1)

# VG5onmin_phD(VG5now-10,VG5now+10,401,1)

# # # VG1onmin_phS(VG1now-10,VG1now+10,401,1)
# VG2onmin_phS(VG2now-10,VG2now+10,401,1)

continuous_acquisition()
continuous_acquisition_ch2()

name=str(Bfield())+'T_CALIB_G3vsG4_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'

# a,dataid,c,d=sweep2D(VG3comp,-864,-860,41,0.02,VG4comp,-812,-808,41,0.014,ph1,ph2)
a,dataid,c,d=sweep2D(VG3comp,-862.5,-864.5,41,0.02,VG4comp,-812,-810,41,0.014,ph2,ph1)
plot_by_id(dataid)
save2plots(name,dataid)




num_point=201
tc=2e-6
total_time=1
demod_S=2
demod_D=1
startG4=-809.4
stopG4=-810.6
startG3=-864.2
stopG3=-863.2

pathS=folder2+'\\'+dayFolder+'\\'+str(Bfield())+'_T_G_VG3'+str(startG3)+'_mV_VG4='+str(startG4)+'mV_phS_'
path2S = pathS + f'/time_traces'
pathD=folder2+'\\'+dayFolder+'\\'+str(Bfield())+'_T_G30to1VG3='+str(startG3)+'_mV_VG4='+str(startG4)+'mV_phD_'
path2D = pathD + f'/time_traces'

continuous_acquisition()
continuous_acquisition_ch2()
Threshold_S,Threshold_D=fit_interdot(startG4,stopG4,startG3,stopG3)#plot, fit and sit on interdot

Threshold_S=Threshold_S*np.pi/180
Threshold_D=Threshold_D*np.pi/180



G3now=VG3()
G4now=VG4()
#bubbles SNR on interdot for phiS
title='IQ_On_interdot_tc'+str(tc)
VG3comp(G3now)
VG4comp(G4now)
blopIQ_interdot(daq_S,tc,total_time,demod_S,pathS,title=title)

VG3comp(startG3)
VG4comp(startG4)
title='IQ_in11_tc'+str(tc)


blopIQ_interdot(daq_S,tc,total_time,demod_S,pathS,title='IQ_in11_tc'+str(tc))

VG3comp(stopG3)
VG4comp(stopG4)
title='IQ_in02_tc'+str(tc)


blopIQ_interdot(daq_S,tc,total_time,demod_S,pathS,title='IQ_in02_tc'+str(tc))

path_dbb=[pathS + '\\IQ_in11_tc'+str(tc)+'.txt',pathS + '\\IQ_in02_tc'+str(tc)+'.txt']


draw_multiple_bbl_interdot(path_dbb,pathS)

#bubbles SNR on interdot for phiD
VG3comp(G3now)
VG4comp(G4now)
title='IQ_On_interdot_tc'+str(tc)

blopIQ_interdot(daq_D,tc,total_time,demod_D,pathD,title=title)

VG3comp(startG3)
VG4comp(startG4)
title='IQ_in11_tc'+str(tc)


blopIQ_interdot(daq_D,tc,total_time,demod_D,pathD,title='IQ_in11_tc'+str(tc))

VG3comp(stopG3)
VG4comp(stopG4)
title='IQ_in02_tc'+str(tc)


blopIQ_interdot(daq_D,tc,total_time,demod_D,pathD,title='IQ_in02_tc'+str(tc))

path_dbb=[pathD + '\\IQ_in11_tc'+str(tc)+'.txt',pathD + '\\IQ_in02_tc'+str(tc)+'.txt']


draw_multiple_bbl_interdot(path_dbb,pathD)


######analysis of occupation probabilities and tunnel rate
    
register_time_trace_interdot(daq_S,startG4,stopG4, startG3,stopG3,num_point,tc,total_time,demod_S,pathS,path2S)

gammarate=analyse_time_traces_interdot(pathS,startG4,stopG4,startG3,stopG3,Threshold_S)
  


register_time_trace_interdot(daq_D,startG4,stopG4, startG3,stopG3,num_point,tc,total_time,demod_D,pathD,path2D)

gammarate=analyse_time_traces_interdot(pathD,startG4,stopG4,startG3,stopG3,Threshold_D)
  


# Bfield(0)
# VG3comp(G3now)
# VG4comp(G4now)


acquisition_duration=400e-6
efftc=2e-6
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


ziUhf.daq.setInt('/dev2010/awgs/0/enable', 1)
# Duration of the time trace to record:


# Vreads = np.arange(-0.3,0.015,0.0005)

# Vread = Vreads[i]      
t=np.linspace(0,acquisition_duration,points)

phaseDarray=[]
phaseSarray=[]
amp=[]
Npoints=101

# Vreads=np.linspace(start,stop,Npoints)##real amplitudes in mV on G4

ampli_list=np.linspace(-0.05,0.5,Npoints)
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

title=str(Bfield())+'T_phS_G3overG4ampli'+str(np.round(ziUhf.daq.getDouble('/dev2010/auxouts/0/scale')/0.15,3))+'_200usampliAWGvstime_G4'+str(VG4())+'mV_G3'+str(VG3())+'mV'


#Create and save plot

fig,ax = plt.subplots()
# plt.pcolor(t*1e6,Vreads,np.transpose(M))
plt.pcolor(t*1e6,ampli_list,M)
plt.ylabel('$A(mV)$',fontsize=18)
plt.xlabel('t ($\mu$s)',fontsize=18)
cb=plt.colorbar()
cb.set_label('$\phi_S$ (rad)',fontsize=18)

ax.tick_params(labelsize=14)
ax.set_title('B='+str(Bfield())+'G3/G4ampli'+str(np.round(ziUhf.daq.getDouble('/dev2010/auxouts/0/scale')/0.15,3)),size=18)
# plt.title('AWG-'+str(np.round(ampliAWG()*11,3))+'mV G3/G4 ampli'+str(np.round(ziUhf.daq.getDouble('/dev2010/auxouts/0/scale')/0.15,3)))
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


title=str(Bfield())+'T_phD_G3overG4ampli'+str(np.round(ziUhf.daq.getDouble('/dev2010/auxouts/0/scale')/0.15,3))+'_200usampliAWGvstime_G4'+str(VG4())+'mV_G3'+str(VG3())+'mV_'



fig,ax = plt.subplots()

plt.pcolor(t*1e6,ampli_list,M)
plt.ylabel('$A(mV)$',fontsize=18)
plt.xlabel('t ($\mu$s)',fontsize=18)
cb=plt.colorbar()
cb.set_label('$\phi_D$ (rad)',fontsize=18)

ax.tick_params(labelsize=14)
ax.set_title('B='+str(Bfield())+'G3/G4 ampli'+str(np.round(ziUhf.daq.getDouble('/dev2010/auxouts/0/scale')/0.15,3)),size=18)

fig.tight_layout()


now=datetime.datetime.now()
dayFolder= datetime.date.isoformat(now)
try:
    os.makedirs(folder2+'\\'+dayFolder)
except IOError:
    donothing=1
    
plt.savefig(folder2+'\\'+dayFolder+'\\'+title+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'.txt',M)
