# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 03:13:17 2021

@author: G-GRE-GRE050402
"""

slopeG3G2=-0.16799999999996848
slopeG4G2=-0.018666666666680005
VG3comp=  SpecialParameters.CompensateG3(VG3,VG2,slopeG3G2)
VG4comp=  SpecialParameters.CompensateG4(VG4,VG2,slopeG4G2)
# rampVG5(-2000)

continuous_acquisition()
VG3comp(-865)
VG4comp(-745)
rampVG1(-1518.23)
rampVG2(-1132)
VG1now=VG1()
VG2now=VG2()
VG5now=VG5()
VG5now=VG5()
VG1now=VG1()
VG1onmin(VG1now-20,VG1now+20,801,1)
VG2onmin(VG2now-10,VG2now+10,1001,1)

VG1now=VG1()
continuous_acquisition()

name=str(Bfield())+'G4vsG3_Vmet'+str(dac.dac17())+'V_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'

# a,dataid,c,d=sweep2D(VG3comp,-859,-851,81,0.1,VG4comp,-750,-820,141,0.005,ph1,ph2)
# a,dataid,c,d=sweep2D(VG3comp,-870,-900,101,0.1,VG4comp,-750,-800,201,0.005,ph1,ph2)
a,dataid,c,d=sweep2D(VG3comp,-863,-868,51,0.1,VG4comp,-742,-747,51,0.015,ph1)
# a,dataid,c,d=sweep2D(VG3comp,-880,-780,181,0.1,VG4comp,-850,-800,121,0.01,ph1)
plot_by_id(dataid)
saveplot(name,dataid)


VG3comp(-865.4)
name=str(Bfield())+'BfieldsG3_Vmet'+str(dac.dac17())+'V_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'

# a,dataid,c,d=sweep2D(VG3comp,-859,-851,81,0.1,VG4comp,-750,-820,141,0.005,ph1,ph2)
# a,dataid,c,d=sweep2D(VG3comp,-870,-900,101,0.1,VG4comp,-750,-800,201,0.005,ph1,ph2)
a,dataid,c,d=sweep2D(Bfield_Hon,0,2,41,1,VG4comp,-742.7,-744.2,151,0.02,ph1)
# a,dataid,c,d=sweep2D(VG3comp,-880,-780,181,0.1,VG4comp,-850,-800,121,0.01,ph1)
plot_by_id(dataid)
saveplot(name,dataid)
Bfield(Bfield_Hon())


continuous_acquisition()
VG3comp(-866)
sensor_on_interdot_sweepG4comp(-743,-746,201,1)



#########################
tc=0.10
acquisition_duration =2e-3  # length of time to record (s)
repetitions = 10            # number of repetitions for the averaging
points =440 # number of points in the acquisition window (min=2)

#efftc=acquisition_duration/10
efftc=5e-6

# such that the effective Tc is 100ms 
# repetitions=tc/efftc/5

repetitions=100

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


for i in range(0,41):
    ampliAWG(i*0.01)
    amp.append(ampliAWG())
    phasearray.append(phase_trig())
ziUhf.daq.setInt('/dev2010/sigouts/1/on', 0)    

phase=[]
for i in range(0,41):
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
name=str(Bfield())+'T_TP5_pulsevspulse_amplitude__300rep_B'+str(Bfield())+'T_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV'
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',phase)

#################################
trigger_mode()
ziUhf.daq.setInt('/dev2010/sigouts/1/on', 1)    
t=np.linspace(0,acquisition_duration,points)
phasearray=[]
amp=[]

for i in range(0,41):
    ampliAWG(0.05)
    VG4(VG4()+0.02*i)
    amp.append(VG4())
    phasearray.append(phase_trig())
ziUhf.daq.setInt('/dev2010/sigouts/1/on', 0)    

phase=[]
for i in range(0,41):
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
name=str(Bfield())+'T_TP5_pulsevsG4pos_amplitude_300rep_B'+str(Bfield())+'T_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV'
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',phase)








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


VG1now=VG1()
VG1onmin(VG1now-1,VG1now+1,101,1)
# continuous_acquisition()

# for i in range(0,4):
#     VG3comp(-866)
#     sensor_on_interdot_sweepG4comp(-747,-743,201,1)
# for i in range(0,4):
#     VG3comp(-866)
#     sensor_on_interdot_sweepG4comp(-743,-747,201,1)
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


jarr=[]
for i in range(0,200):
    VG4comp(-747)
    ph1()
    a,dataid,c=sweep1D(VG4comp,-747,-743,201,0.01,ph1)
    data_set,data_get,parameters_name=Extract_data(a)
    # jpos=step_detection(data_get[0],data_set)
    # jarr.append(jpos)
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
    jarr.append(data_set[kmax])   

     
# G4axis=np.linspace(0,acquisition_duration*1e6,points)
jarr=np.array(jarr)
fig, ax = plt.subplots()
ax.set_xlabel(r'$V_ {G4}(mV)$',fontsize=fontSize)
ax.set_ylabel('$counts$ ',fontsize=fontSize)
# plt.plot(tarr,phase,'+')
counts,bins=np.histogram(jarr,bins=51,range=(-745.5,-743.5))
# plt.hist(np.array(jarr),density=True,bins=51,range=(-745.5,-743.5) )
plt.hist(np.array(jarr),bins=51)
name=str(Bfield())+'sensorjump_distribution_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',jarr)     


##############

continuous_acquisition()
VG3comp(-866)
VG4comp(-748)
rampVG1(-1518.23)
rampVG2(-1132)
rampVG5(-1500)
VG1now=VG1()
VG2now=VG2()
VG5now=VG5()
VG5now=VG5()
VG1now=VG1()
VG1onmin(VG1now-10,VG1now+10,2001,1)
VG2now=VG2()
VG2onmin(VG2now-3,VG2now+3,601,1)

VG1now=VG1()
continuous_acquisition()

name=str(Bfield())+'G4vsG3_Vmet'+str(dac.dac17())+'V_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'

# a,dataid,c,d=sweep2D(VG3comp,-859,-851,81,0.1,VG4comp,-750,-820,141,0.005,ph1,ph2)
# a,dataid,c,d=sweep2D(VG3comp,-870,-900,101,0.1,VG4comp,-750,-800,201,0.005,ph1,ph2)
a,dataid,c,d=sweep2D(VG3comp,-870,-863,51,0.1,VG4comp,-743,-749,51,0.015,ph1)
# a,dataid,c,d=sweep2D(VG3comp,-880,-780,181,0.1,VG4comp,-850,-800,121,0.01,ph1)
plot_by_id(dataid)
saveplot(name,dataid)

# a,dataid,c=sweep1D(VG3comp,-870,-863,51,0.1,






# phase=[]
# tarr=[]
# VG4comp(-743)
# time.sleep(5)
# ph1()
# t0=time.time()
# VG4comp(-745)
# tarr.append(time.time()-t0)
# phase.append(ph1())

# for i in range(0,100):
#     tarr.append(time.time()-t0)
#     phase.append(ph1())


# f = plt.figure()
# plt.plot(tarr,phase,'+')
# # plt.clim(vmin=None,vmax=0.3)
# plt.ylabel('phi(deg)')
# plt.xlabel('t(s)')
# # # plt.ylabel('pulse amplitude_pp (mV)')
# # plt.ylabel('pulse amplitude_pp (AWG)')   











VG3comp(-867)
sensor_on_interdot_sweepG4comp(-744,-749,501,1)



tarr=[]
jarr=[]
t0=time.time()
for i in range(0,500):
    VG4comp(-744)
    ph1()
    a,dataid,c=sweep1D(VG4comp,-744,-749,501,0.01,ph1)
    data_set,data_get,parameters_name=Extract_data(a)
    tarr.append(time.time()-t0)
    if i%20==0:
        name=str(Bfield())+'T_'+str(i)+'scan_onint_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())
        plot_by_id(dataid)
        saveplot(name,dataid)
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
    jarr.append(data_set[kmax])   

     
# G4axis=np.linspace(0,acquisition_duration*1e6,points)
jarr=np.array(jarr)
fig, ax = plt.subplots()
ax.set_xlabel(r'$V_ {G4}(mV)$',fontsize=fontSize)
ax.set_ylabel('$counts$ ',fontsize=fontSize)
# plt.plot(tarr,phase,'+')
counts,bins=np.histogram(jarr,bins=51,range=(-745.5,-743.5))
# plt.hist(np.array(jarr),density=True,bins=51,range=(-745.5,-743.5) )
plt.hist(np.array(jarr),bins=51)
name=str(Bfield())+'sensorjump_distribution_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',jarr)    

fig, ax = plt.subplots()
ax.set_xlabel(r'$t(s)$',fontsize=fontSize)
ax.set_ylabel('$jump pos($ ',fontsize=fontSize)
# plt.plot(tarr,phase,'+')
plt.plot(tarr,jarr)
name=str(Bfield())+'sensortime_distribution_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',jarr)    










###################""
VG2now=VG2()
VG2onmin(VG2now-4,VG2now+4,601,1)
name=str(Bfield())+'sensorintime_distribution_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())
a,dataid,c,d=sweep2D(dac.dac16,0,0.1,10000,1,VG2,VG2now-3,VG2now+3,201,0.05,ph1)

plot_by_id(dataid)
saveplot(name,dataid)

Bfield(0)

# VG3comp(-866)
# sensor_on_interdot_sweepG4comp(-744,-749,201,1)

# name=str(Bfield())+'BfieldsG3_Vmet'+str(dac.dac17())+'V_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'

# # a,dataid,c,d=sweep2D(VG3comp,-859,-851,81,0.1,VG4comp,-750,-820,141,0.005,ph1,ph2)
# # a,dataid,c,d=sweep2D(VG3comp,-870,-900,101,0.1,VG4comp,-750,-800,201,0.005,ph1,ph2)
# a,dataid,c,d=sweep2D(Bfield_Hon,2.8,1,91,1,VG4comp,-743,-747,401,0.02,ph1)
# # a,dataid,c,d=sweep2D(VG3comp,-880,-780,181,0.1,VG4comp,-850,-800,121,0.01,ph1)
# plot_by_id(dataid)
# saveplot(name,dataid)
# Bfield(Bfield_Hon())
