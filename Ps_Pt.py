# -*- coding: utf-8 -*-
"""
Created on Tue May 11 18:52:52 2021

@author: G-GRE-GRE050402
"""
        t=np.linspace(0,acquisition_duration,points)
        taxis=np.linspace(0,acquisition_duration,points)

        plt.figure()
        s,d=phases_trig()
        plt.plot(taxis*1e6,s[0],label='$\phi_{G3}$')
        plt.plot(taxis*1e6,d[0],label='$\phi_{G4}$')
        plt.legend()
        Ps_s=0
        Ps_d=0
        Ps_s2=0
        Ps_d2=0
        Ps_d3 =0
        Ps_s3 =0
        if np.mean(s[0][0:9])<phi_thS and np.mean(s[0][10:20])>phi_thS:
                Ps_s2+=1
        if np.mean(d[0][0:9])>phi_thD and np.mean(d[0][10:20])<phi_thD:
                Ps_d2+=1
                
        if np.mean(s[0][0:9])<phi_thS3 and np.mean(s[0][10:20])>phi_thS3:
                Ps_s3 +=1
        if np.mean(d[0][0:9])>phi_thD3 and np.mean(d[0][10:20])<phi_thD3:
                Ps_d3 +=1

        print(Ps_s2)
        print(Ps_d2)
        print(Ps_d3) 
        print(Ps_s3)


        
        
        
T02=200e-6
T11=50e-6
Tramp=2e-6


acquisition_duration=200e-6
efftc=5e-6
# delay=T02+Tramp+T11
delay=130e-6

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
                   ['dataAcquisitionModule/delay', delay], #0                                       # trigger delay (s)
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
phases_trig= SpecialParameters.Pulsed_readout_both(ziUhf, repetitions, returnOnePoint=False)
phases_trig.setSettings(trigger_setting, grid_setting)
ziUhf.daq.setInt('/dev2010/awgs/0/enable', 1)    

# t=np.linspace(delay,acquisition_duration+delay,points)
# taxis=np.linspace(delay,acquisition_duration+delay,points)

t=np.linspace(0,acquisition_duration,points)
taxis=np.linspace(0,acquisition_duration,points)

amp=[]
Npoints=51

# Vreads=np.linspace(start,stop,Npoints)##real amplitudes in mV on G4

ampli_list=np.linspace(-0,0.3,Npoints)
# ampliAWG(0.2)
traceavgS=[]
traceavgD=[]

t_threshold=40e-6
Psinglet_S=[]
Psinglet_D=[]

Psinglet_D2=[]
Psinglet_S2=[]

Psinglet_D3=[]
Psinglet_S3=[]
NSS=201
phi_thS=0.05
phi_thD=0.15
phi_thS3=0.1
phi_thD3=0.1
for i in range(0,Npoints):
    ampliAWG(ampli_list[i])
    print(ampliAWG())
    s,d=phases_trig()

    traceavgS.append(s[0])
    traceavgD.append(d[0])
    
    decay02S_array=[]
    decay02D_array=[]
    Ps_s=0
    Ps_d=0
    Ps_s2=0
    Ps_d2=0
    Ps_d3 =0
    Ps_s3 =0
    for j in range(0,NSS):
        
        s,d=phases_trig()
        tdecay_S=step_detection(s[0],taxis)
        tdecay_D=step_detection(-d[0],taxis)
        
        # plt.figure()
        # s,d=phases_trig()
        # plt.plot(taxis*1e6,s[0],label='$\phi_{G3}$')
        # plt.plot(taxis*1e6,d[0],label='$\phi_{G4}$')
        # plt.legend()
        
        decay02S_array.append(tdecay_S)
        decay02D_array.append(tdecay_D)
        if tdecay_S<t_threshold and not tdecay_S>180e-6:
                Ps_s+=1
        if tdecay_D<t_threshold and not tdecay_S>180e-6:
                Ps_d+=1
        if np.mean(s[0][0:9])<phi_thS and np.mean(s[0][10:20])>phi_thS:
                Ps_s2+=1
        if np.mean(d[0][0:9])>phi_thD and np.mean(d[0][10:20])<phi_thD:
                Ps_d2+=1
                
        if np.mean(s[0][0:9])<phi_thS3 and np.mean(s[0][10:20])>phi_thS3:
                Ps_s3 +=1
        if np.mean(d[0][0:9])>phi_thD3 and np.mean(d[0][10:20])<phi_thD3:
                Ps_d3 +=1


    Psinglet_D.append(Ps_d/NSS)    
    Psinglet_S.append(Ps_s/NSS)   
    
    Psinglet_D2.append(Ps_d2/NSS)    
    Psinglet_S2.append(Ps_s2/NSS)
    
    Psinglet_D3.append(Ps_d3/NSS)    
    Psinglet_S3.append(Ps_s3/NSS)


ampli_list=ampli_list*5.5

plt.figure()

plt.plot(ampli_list,Psinglet_S,label='$P_{singlet} (G3)$')
plt.xlabel('$\epsilon(mV)$')
plt.ylabel('$P_{singlet} (G3)$')
plt.legend()
# plt.title('AWG-'+str(np.round(ampliAWG()*11,3))+'mV G3/G4 ampli'+str(np.round(ziUhf.daq.getDouble('/dev2010/auxouts/0/scale')/0.15,3)))
title=str(Bfield())+'T_Sphase_Psingletvsdetuning_'+str(Ntraces)+'_SSvsaverages_AWG-'+str(np.round(ampliAWG(),3))+'G3ampli'+str(np.round(ziUhf.daq.getDouble('/dev2010/auxouts/0/scale'),3))+'VG3_'+str(VG3())+'mV'
plt.savefig(folder2+'\\'+dayFolder+'\\'+title+'.png')
plt.show()
np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'.txt',Psinglet_S)



plt.figure()

plt.plot(ampli_list,Psinglet_D,label='$P_{singlet} (G4)$')
plt.xlabel('$\epsilon(mV)$')
plt.ylabel('$P_{singlet} (G4)$')
plt.legend()
# plt.title('AWG-'+str(np.round(ampliAWG()*11,3))+'mV G3/G4 ampli'+str(np.round(ziUhf.daq.getDouble('/dev2010/auxouts/0/scale')/0.15,3)))
title=str(Bfield())+'T_Dphase_Psingletvsdetuning_'+str(Ntraces)+'_SSvsaverages_AWG-'+str(np.round(ampliAWG(),3))+'G3ampli'+str(np.round(ziUhf.daq.getDouble('/dev2010/auxouts/0/scale'),3))+'VG3_'+str(VG3())+'mV'
plt.savefig(folder2+'\\'+dayFolder+'\\'+title+'.png')
plt.show()
np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'.txt',Psinglet_D)


####
plt.figure()

plt.plot(ampli_list,Psinglet_S2,label='$P_{singlet} (G3)$')
plt.xlabel('$\epsilon(mV)$')
plt.ylabel('$P_{singlet} (G3)$')
plt.legend()
# plt.title('AWG-'+str(np.round(ampliAWG()*11,3))+'mV G3/G4 ampli'+str(np.round(ziUhf.daq.getDouble('/dev2010/auxouts/0/scale')/0.15,3)))
title=str(Bfield())+'T_Sphase2_Psingletvsdetuning_'+str(Ntraces)+'_SSvsaverages_AWG-'+str(np.round(ampliAWG(),3))+'G3ampli'+str(np.round(ziUhf.daq.getDouble('/dev2010/auxouts/0/scale'),3))+'VG3_'+str(VG3())+'mV'
plt.savefig(folder2+'\\'+dayFolder+'\\'+title+'.png')
plt.show()
np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'.txt',Psinglet_S2)



plt.figure()

plt.plot(ampli_list,Psinglet_D2,label='$P_{singlet} (G4)$')
plt.xlabel('$\epsilon(mV)$')
plt.ylabel('$P_{singlet} (G4)$')
plt.legend()
# plt.title('AWG-'+str(np.round(ampliAWG()*11,3))+'mV G3/G4 ampli'+str(np.round(ziUhf.daq.getDouble('/dev2010/auxouts/0/scale')/0.15,3)))
title=str(Bfield())+'T_Dphase2_Psingletvsdetuning_G3ampli'+str(np.round(ziUhf.daq.getDouble('/dev2010/auxouts/0/scale'),3))+'VG3_'+str(VG3())+'mV'
plt.savefig(folder2+'\\'+dayFolder+'\\'+title+'.png')
plt.show()
np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'.txt',Psinglet_D2)



lt.figure()

plt.plot(ampli_list,Psinglet_S3,label='$P_{singlet} (G3)$')
plt.xlabel('$\epsilon(mV)$')
plt.ylabel('$P_{singlet} (G3)$')
plt.legend()
# plt.title('AWG-'+str(np.round(ampliAWG()*11,3))+'mV G3/G4 ampli'+str(np.round(ziUhf.daq.getDouble('/dev2010/auxouts/0/scale')/0.15,3)))
title=str(Bfield())+'T_Sphase3_Psingletvsdetuning_'+str(Ntraces)+'_SSvsaverages_AWG-'+str(np.round(ampliAWG(),3))+'G3ampli'+str(np.round(ziUhf.daq.getDouble('/dev2010/auxouts/0/scale'),3))+'VG3_'+str(VG3())+'mV'
plt.savefig(folder2+'\\'+dayFolder+'\\'+title+'.png')
plt.show()
np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'.txt',Psinglet_S3)



plt.figure()

plt.plot(ampli_list,Psinglet_D3,label='$P_{singlet} (G4)$')
plt.xlabel('$\epsilon(mV)$')
plt.ylabel('$P_{singlet} (G4)$')
plt.legend()
# plt.title('AWG-'+str(np.round(ampliAWG()*11,3))+'mV G3/G4 ampli'+str(np.round(ziUhf.daq.getDouble('/dev2010/auxouts/0/scale')/0.15,3)))
title=str(Bfield())+'T_Dphase3_Psingletvsdetuning_G3ampli'+str(np.round(ziUhf.daq.getDouble('/dev2010/auxouts/0/scale'),3))+'VG3_'+str(VG3())+'mV'
plt.savefig(folder2+'\\'+dayFolder+'\\'+title+'.png')
plt.show()
np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'.txt',Psinglet_D3)
















     
    # fig, ax = plt.subplots()
    # ax.set_xlabel(r'$\tau(\mu s)$',fontsize=fontSize)
    # ax.set_ylabel('$counts_S$ ',fontsize=fontSize)
    
    
    # # counts_hist02=np.histogram(decay02S_array,bins=110)[0]
    # # t_hist02=np.histogram(decay02S_array,bins=110)[1]
    
    # plt.hist(decay02S_array,bins=110)
    
    
    # name=str(Bfield())+'T_decay_distribution_phS_tc4us_histogram_'+str(len(decay02S_array))+'counts_A_pp_'+str(ampliAWG()*5.5)+'mV_G3'+str(VG3())+'mV_G4'+str(VG4()) +'mV'
    # plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
    # np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',decay02S_array)       
    
    
    # fig, ax = plt.subplots()
    # ax.set_xlabel(r'$\tau(\mu s)$',fontsize=fontSize)
    # ax.set_ylabel('$counts_D$ ',fontsize=fontSize)
    
    
    # # counts_hist02=np.histogram(decay02D_array,bins=110)[0]
    # # t_hist02=np.histogram(decay02D_array,bins=110)[1]
    
    # plt.hist(decay02D_array,bins=110)
    
    
    # name=str(Bfield())+'T_decay_distribution_phD_tc5us_histogram_'+str(len(decay02D_array))+'counts_A_pp_'+str(ampliAWG()*5.5)+'mV__G3'+str(VG3())+'mV_G4'+str(VG4())+'mV' 
    # plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
    # np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',decay02D_array) 
# phaseS=[]
# for i in range(0,Npoints):
#     phaseS.append(traceavgS[i])    
    
# phaseD=[]
# for i in range(0,Npoints):
#     phaseD.append(traceavgD[i])        
    






















ampliAWG(0.2)



Ntraces=100
c,data=daqtrig_S.get_data_pulseseq(acquisition_duration,delay,Ntraces)
traceavgS=[]
threshold=-0.1#rad

for i in range(0,len(data)):
    traceavgS.append(np.nanmean(data[i]))
    
Ntraces=100
c,data=daqtrig_D.get_data_pulseseq(acquisition_duration,delay,Ntraces)
traceavgD=[]
# threshold=-0.1#rad

for i in range(0,len(data)):
    traceavgD.append(np.nanmean(data[i]))
    
 
    



taxis=np.linspace(delay,acquisition_duration+delay,points)


plt.figure()

plt.plot(taxis*1e6,traceavgS, label='$\phi_{G3}$ averaged '+str(Ntraces)+' times' )
plt.plot(taxis*1e6,traceavgD, label='$\phi_{G4}$ averaged '+str(Ntraces)+' times' )

# plt.plot(taxis,phase_trigD()[0])
s,d=phases_trig()
plt.plot(taxis*1e6,s[0],label='$\phi_{G3}$')
plt.plot(taxis*1e6,d[0],label='$\phi_{G4}$')
plt.xlabel('$t(\mu s)$')
plt.ylabel('$\phi(rad)$')
plt.legend()
plt.title('AWG-'+str(np.round(ampliAWG()*11,3))+'mV G3/G4 ampli'+str(np.round(ziUhf.daq.getDouble('/dev2010/auxouts/0/scale')/0.15,3)))
title=str(dataid)+'_sstraces_3stagepulse_'+str(Ntraces)+'_SSvsaverages_AWG-'+str(np.round(ampliAWG(),3))+'G3ampli'+str(np.round(ziUhf.daq.getDouble('/dev2010/auxouts/0/scale'),3))+'VG3_'+str(VG3())+'mV'
plt.savefig(folder2+'\\'+dayFolder+'\\'+title+'.png')
plt.show()
np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'.txt',traceavgS)























def plot_correlations(num_point,Ntraces,startG4,stopG4,startG3,stopG3):
    
    G4ar=np.linspace(startG4,stopG4,num_point)
    
    G3ar=np.linspace(startG3,stopG3,num_point)
    
    correlations=[]
    correlationvals=[]
    decay_S=[]
    decay_D=[]
    
    for i in range (0,len(G4ar)):
        
        VG3comp(G3ar[i])
        VG4comp(G4ar[i])
        print(VG4())
        taxis=np.linspace(0,acquisition_duration*1e6,points)
        decay02S_array=[]
        decay02D_array=[]
        correlation=[]
        correlationval=[]
        
        for k in range(0,Ntraces):
            phase_ssS,phase_ssD=phases_trig()
            phase_ssS=phase_ssS[0]
            phase_ssD=phase_ssD[0]
            # tdecay_S=step_detection(phase_ssS[20:],taxis[20:])
            # tdecay_D=step_detection(phase_ssD[20:],taxis[20:])
            tdecay_S=step_detection(phase_ssS[30:-10],taxis[30:-10])
            tdecay_D=step_detection(phase_ssD[30:-10],taxis[30:-10])
            
            decay02S_array.append(tdecay_S)
            decay02D_array.append(tdecay_D)
            if np.abs(tdecay_S-tdecay_D)<10:
             correlation.append(1)
             correlationval.append(tdecay_S)
            else :
             correlation.append(0)
             
             
        correlations.append(np.mean(correlation))
        correlationvals.append(np.mean(correlationval))
        decay_S.append(np.mean(tdecay_S))
        decay_D.append(np.mean(tdecay_D))
        
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
    ax.set_title('B='+str(np.round(Bfield(),3))+'ampliAWG'+str(np.round(ampliAWG(),4)),size=18)
    fig.tight_layout()
    
    title=str(Bfield())+'T_correlationvsG4_A_pp_'+str(ampliAWG()*11)+'mV__G3'+str(VG3())+'mV_G4'+str(VG4())+'mV' 
    
        
    plt.savefig(folder2+'\\'+dayFolder+'\\'+title+'.png')
    np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'.txt',correlations)
    
    
    
    fig,ax = plt.subplots()
    plt.plot(G4ar,correlationvals)
    # plt.pcolor(t*1e6,ampli_list,M)
    plt.ylabel('$average coincidence time($\mu s$)$',fontsize=18)
    plt.xlabel('G4 (mV)',fontsize=18)
    # cb=plt.colorbar()
    # cb.set_label('$\phi_D$ (rad)',fontsize=18)
    
    ax.tick_params(labelsize=14)
    ax.set_title('B='+str(np.round(Bfield(),3))+'ampliAWG'+str(np.round(ampliAWG(),4)),size=18)
    fig.tight_layout()
    
    title=str(Bfield())+'T_correlationtimevsG4_A_pp_'+str(ampliAWG()*11)+'mV__G3'+str(VG3())+'mV_G4'+str(VG4())+'mV' 
    
        
    plt.savefig(folder2+'\\'+dayFolder+'\\'+title+'.png')
    np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'.txt',correlationvals)
    
    
    
    
    fig,ax = plt.subplots()
    plt.plot(G4ar,correlationvals,label='correlation time')
    plt.plot(G4ar,decay_S,label='G3 jump time')
    plt.plot(G4ar,decay_D,label='G4 jump time')
    # plt.pcolor(t*1e6,ampli_list,M)
    # plt.ylabel('$average coincidence time($\mu s$)$',fontsize=18)
    plt.xlabel('G4 (mV)',fontsize=18)
    # cb=plt.colorbar()
    # cb.set_label('$\phi_D$ (rad)',fontsize=18)
    
    ax.tick_params(labelsize=14)
    ax.set_title('B='+str(np.round(Bfield(),3))+'ampliAWG'+str(np.round(ampliAWG(),4)),size=18)
    fig.tight_layout()
    
    title=str(Bfield())+'T_alltimesvsG4_A_pp_'+str(ampliAWG()*11)+'mV__G3'+str(VG3())+'mV_G4'+str(VG4())+'mV' 
    plt.legend()
        
    plt.savefig(folder2+'\\'+dayFolder+'\\'+title+'.png')
    # np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'.txt',correlationvals,decay_S,decay_D)



