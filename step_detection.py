# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 18:04:10 2021

@author: G-GRE-GRE050402
"""
# pulses correlation function
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
    
    step_indx = np.argmax(dary_step)  # yes, cleaner than np.where(dary_step == dary_step.max())[0][0]
    
    # # plots
    # fig, ax = plt.subplots()
    # plt.plot(taxis,dary)
    
    # plt.plot(taxis,dary_step[0:-1]/10)
    
    # plt.plot((taxis[step_indx], taxis[step_indx]), (dary_step[step_indx]/10, 0), 'r')
    # ax.set_ylabel('$\phi$(rad)',fontsize=fontSize)
    # ax.set_xlabel('time ($\mu$s) ',fontsize=fontSize)
    # plt.savefig(folder2+'\\'+dayFolder+'\\stepdetection.png')
    return(taxis[step_indx-1])




acquisition_duration=200e-6
efftc=5e-6
delay=0e-6
# such that the effective Tc is 100ms 
# repetitions=tc/efftc/5

repetitions=1

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
phases_trig= Pulsed_readout_both(ziUhf, repetitions, returnOnePoint=False)
phases_trig.setSettings(trigger_setting, grid_setting)
# Duration of the time trace to record:


# Vreads = np.arange(-0.3,0.015,0.0005)

# Vread = Vreads[i]      
t=np.linspace(0,acquisition_duration,points)

phaseDarray=[]
phaseSarray=[]


taxis=np.linspace(0,acquisition_duration*1e6,points)
decay02S_array=[]
decay02D_array=[]
correlation=[]
for k in range(0,10):
    phase_ssS,phase_ssD=phases_trig()
    phase_ssS=phase_ssS[0]
    phase_ssD=phase_ssD[0]
    # tdecay_S=step_detection(phase_ssS[20:],taxis[20:])
    # tdecay_D=step_detection(phase_ssD[20:],taxis[20:])
    tdecay_S=step_detection(phase_ssS[40:],taxis[40:])
    tdecay_D=step_detection(phase_ssD[40:],taxis[40:])
    
    decay02S_array.append(tdecay_S)
    decay02D_array.append(tdecay_D)
    if np.abs(tdecay_S-tdecay_D)<10:
     correlation.append(1)
    else :
     correlation.append(0)
     
     
correlations=np.mean(correlation)
# phase_ssS,phase_ssD=phases_trig()
# phase_ssS=phase_ssS[0]
# phase_ssD=phase_ssD[0]

# # phase_ssS,phase_ssD=phases_trig()
# fig, ax = plt.subplots()
# plt.plot(taxis,phase_ssS)
# plt.plot(taxis,phase_ssD)

  



 
fig, ax = plt.subplots()
ax.set_xlabel(r'$\tau(\mu s)$',fontsize=fontSize)
ax.set_ylabel('$counts_S$ ',fontsize=fontSize)


# counts_hist02=np.histogram(decay02S_array,bins=110)[0]
# t_hist02=np.histogram(decay02S_array,bins=110)[1]

plt.hist(decay02S_array,bins=110)


name=str(Bfield())+'T_decay_distribution_phS_tc5us_histogram_'+str(len(decay02S_array))+'counts_A_pp_'+str(ampliAWG()*11)+'mV_G3'+str(VG3())+'mV_G4'+str(VG4()) +'mV'
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',decay02S_array)       


fig, ax = plt.subplots()
ax.set_xlabel(r'$\tau(\mu s)$',fontsize=fontSize)
ax.set_ylabel('$counts_D$ ',fontsize=fontSize)


# counts_hist02=np.histogram(decay02D_array,bins=110)[0]
# t_hist02=np.histogram(decay02D_array,bins=110)[1]

plt.hist(decay02D_array,bins=110)


name=str(Bfield())+'T_decay_distribution_phD_tc5us_histogram_'+str(len(decay02D_array))+'counts_A_pp_'+str(ampliAWG()*11)+'mV__G3'+str(VG3())+'mV_G4'+str(VG4())+'mV' 
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',decay02D_array) 



#correlations vs detuning

ampliAWG(0.2)


num_point=41
tc=2e-6
total_time=1
demod_S=2
demod_D=1
startG4=-975
stopG4=-978
startG3=-764.5
stopG3=-763
G4ar=np.linspace(startG4,stopG4,num_point)

G3ar=np.linspace(startG3,stopG3,num_point)

correlations=[]
correlationvals=[]

for i in range (0,len(G4ar)):
    
    VG3comp(G3ar[i])
    VG4comp(G4ar[i])
    print(VG4())
    taxis=np.linspace(0,acquisition_duration*1e6,points)
    decay02S_array=[]
    decay02D_array=[]
    correlation=[]
    correlationval=[]
    
    for k in range(0,300):
        phase_ssS,phase_ssD=phases_trig()
        phase_ssS=phase_ssS[0]
        phase_ssD=phase_ssD[0]
        # tdecay_S=step_detection(phase_ssS[20:],taxis[20:])
        # tdecay_D=step_detection(phase_ssD[20:],taxis[20:])
        tdecay_S=step_detection(phase_ssS[40:-10],taxis[40:-10])
        tdecay_D=step_detection(phase_ssD[40:-10],taxis[40:-10])
        
        # decay02S_array.append(tdecay_S)
        # decay02D_array.append(tdecay_D)
        if np.abs(tdecay_S-tdecay_D)<10:
         correlation.append(1)
         correlationval.append(tdecay_S)
        else :
         correlation.append(0)
         
         
    correlations.append(np.mean(correlation))
    correlationvals.append(np.mean(correlationval))
    
    
now=datetime.datetime.now()
dayFolder= datetime.date.isoformat(now)
try:
    os.makedirs(folder2+'\\'+dayFolder)
except IOError:
    donothing=1    

fig,ax = plt.subplots()
plt.plot(G4ar,correlations)
# plt.pcolor(t*1e6,ampli_list,M)
plt.ylabel('$correlations$',fontsize=18)
plt.xlabel('G4 (mV)',fontsize=18)
# cb=plt.colorbar()
# cb.set_label('$\phi_D$ (rad)',fontsize=18)

ax.tick_params(labelsize=14)
ax.set_title('B='+str(Bfield()),size=18)
fig.tight_layout()

title=str(Bfield())+'T_correlationvsG4_A_pp_'+str(ampliAWG()*11)+'mV__G3'+str(VG3())+'mV_G4'+str(VG4())+'mV' 

    
plt.savefig(folder2+'\\'+dayFolder+'\\'+title+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'.txt',correlations)





####detuning vs phase while pulsing
ampliAWG(0.2)
now=datetime.datetime.now()
dayFolder= datetime.date.isoformat(now)
try:
    os.makedirs(folder2+'\\'+dayFolder)
except IOError:
    donothing=1
    
plt.savefig(folder2+'\\'+dayFolder+'\\'+title+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'.txt',M)


M=phaseD


title=str(Bfield())+'T_phD_detuningvstime_ampliAWG0p2_200us__G5'+str(VG5())+'mV_G4'+str(VG4())+'mV_G3'+str(VG3())+'mV_____'



fig,ax = plt.subplots()

plt.pcolor(t*1e6,G4ar,M)
plt.ylabel('$G4(mV)$',fontsize=18)
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