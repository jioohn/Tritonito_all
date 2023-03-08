# -*- coding: utf-8 -*-
"""
Created on Sun May  9 20:40:29 2021

@author: G-GRE-GRE050402
"""




VG3comp(-765)
VG4comp(-975)
VG5now=VG5()
VG2now=VG2()
VG6now=VG6()
VG1now=VG1()

# VG6onmin_phD(VG6now-10,VG6now+10,401,1)


# VG1onmin_phS(VG1now-10,VG1now+10,401,1)


# VG5onmin_phD(VG5now-10,VG5now+10,401,1)
# VG2onmin_phS(VG2now-10,VG2now+10,201,1)

continuous_acquisition()
continuous_acquisition_ch2()
VG6now=VG6()
VG1now=VG1()
# VG6onmin_phD(VG6now-30,VG6now+10,2001,1)
# VG5onmin_phD(VG5now-10,VG5now+10,201,1)
VG6onmin_phD(VG6now-5,VG6now+5,201,1)
VG1onmin_phS(VG1now-5,VG1now+5,201,1)
# VG6onmin_phD(VG6now-3,VG6now+3,201,1)


# VG2onmin_phS(VG2now-30,VG2now+30,+201,1)

continuous_acquisition()
continuous_acquisition_ch2()

name=str(Bfield())+'T_G3vsG4_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'

a,dataid,c,d=sweep2D(VG3comp,-767,-765,31,0.02,VG4comp,-975,-973,31,0.013,ph1,ph2)
# a,dataid,c,d=sweep2D(VG3comp,-768,-772,31,0.02,VG4comp,-876,-879,31,0.013,ph1,ph2)
# a,dataid,c,d=sweep2D(VG3comp,-765,-780,41,0.02,VG4comp,-875,-885,41,0.013,ph1,ph2)
plot_by_id(dataid)
save2plots(name,dataid)
plt.close()
plot_by_id(dataid)

VG3comp(-766)
VG4comp(-974.27)


ampliAWG(0.2)

acquisition_duration=400e-6
efftc=5e-6
delay=0e-6
# such that the effective Tc is 100ms 
# repetitions=tc/efftc/5

repetitions=1

ziUhf.daq.setInt('/dev2010/demods/0/trigger', 33554432) # demodulator trigger set on AWGtrigger2 High
ziUhf.daq.setDouble('/dev2010/demods/0/rate', 200e3)
ziUhf.daq.setDouble('/dev2010/demods/1/rate', 200e3)

# ziUhf.daq.setDouble('/dev2010/demods/1/rate', 2e6)
# ziUhf.daq.setDouble('/dev2010/demods/0/rate', 2e6)
ziUhf.daq.setInt('/dev2010/demods/0/order', 1)
ziUhf.daq.setInt('/dev2010/demods/1/order', 1)

points=int(acquisition_duration*ziUhf.daq.getDouble('/dev2010/demods/0/rate'))


ziUhf.daq.setDouble('/dev2010/demods/0/timeconstant', efftc)
ziUhf.daq.setDouble('/dev2010/demods/1/timeconstant', efftc)
#ziUhf.daq.setInt('/dev2365/awgs/0/enable', 1)      # 1 = enable;   0 = disabled


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
ziUhf.daq.setInt('/dev2010/awgs/0/enable', 1)    






Tload=1e-6
Tempty=100e-6

Tread=0e-6

namefile='C:\\Users\\g-gre-gre050402\\Documents\\Zurich Instruments\\LabOne\\WebServer\\awg\\src\\diagonal_pulse.seqc'    
changetempty(namefile, Tload) 
changetload(namefile, Tempty) 


# changetread(namefile, Tread) 
#run_seq before!!!

amplimV=0.05


A=amplimV/ampliAWG()/5.5 #renormalize in AWG units

# changeAread(namefile, A) 

run_seq('dev2010','diagonal_pulse.seqc')   
ziUhf.daq.setInt('/dev2010/demods/1/enable', 1)
ziUhf.daq.setInt('/dev2010/demods/0/enable', 1)
ziUhf.daq.setInt('/dev2010/sigouts/0/enables/4', 1)
ziUhf.daq.setInt('/dev2010/sigouts/0/enables/5', 1)
ziUhf.daq.setInt('/dev2010/demods/0/trigger', 33554432)
ziUhf.daq.setInt('/dev2010/demods/1/trigger', 33554432)


Npoints =21
tload=np.linspace(0e-9,10e-6,Npoints)

traceavgS=[]
traceavgD=[]
for i in range(0,Npoints):
    
    print(i)

    changetempty(namefile, tload[i]) 
    run_seq('dev2010','diagonal_pulse.seqc')   
    ziUhf.daq.setInt('/dev2010/demods/1/enable', 1)
    ziUhf.daq.setInt('/dev2010/demods/0/enable', 1)
    ziUhf.daq.setInt('/dev2010/sigouts/0/enables/4', 1)
    ziUhf.daq.setInt('/dev2010/sigouts/0/enables/5', 1)
    ziUhf.daq.setInt('/dev2010/demods/0/trigger', 33554432)
    ziUhf.daq.setInt('/dev2010/demods/1/trigger', 33554432)


    delay=tload[i]
    # acquisition_duration = Tread # length of time to record (s)cha
    # acquisition_duration = 70e-6 # length of time to record (s)
    acquisition_duration=100e-6
    efftc=1e-6
    # delay=0e-6
    # such that the effective Tc is 100ms 
    # repetitions=tc/efftc/5
    
    repetitions=1000
    
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
    
    # phase_trigS= SpecialParameters.Pulsed_readout_S(ziUhf, repetitions, returnOnePoint=False)
    # phase_trigD= SpecialParameters.Pulsed_readout_D(ziUhf, repetitions, returnOnePoint=False)
    
    # phase_trigS.setSettings(trigger_setting, grid_setting)
    # phase_trigD.setSettings(trigger_setting, grid_setting)
    
    # phases_trig= SpecialParameters.Pulsed_readout_both(ziUhf, repetitions, returnOnePoint=False)
    phases_trig= SpecialParameters.Pulsed_readout_both(ziUhf, repetitions, returnOnePoint=False)
    phases_trig.setSettings(trigger_setting, grid_setting)
    ziUhf.daq.setInt('/dev2010/awgs/0/enable', 1)    


    # Ntraces=100

    d,s=phases_trig()
    traceavg=[]

    traceavgS.append(s[0])
    traceavgD.append(d[0])
        # traceavgD.append(np.mean(d[i]))
        # traceavgD.append(np.mean(d[i]))  
    # phaseD.append(traceavgS
    # Pup=0
    # singletraces=np.transpose(d)    
    # for i in range(0,len(singletraces)):
    #     if np.min(singletraces[i])<threshold:
    #         Pup+=1
    
    # Pupnorm=Pup/len(singletraces)
    # # error=np.std(singletraces[i])
    # Par.append(Pupnorm)




###
M=traceavgS
#Enregistrement des datas dans un sous dossier convenablement nommé 


title=str(dataid)+'phS_tcharge_vstime_G4'+str(VG4())+'mV_G3'+str(VG3())+'mV_AWG'+str(ampliAWG())


t=np.linspace(0,acquisition_duration,points)

fig,ax = plt.subplots()
# plt.pcolor(t*1e6,Vreads,np.transpose(M))
plt.pcolor(t*1e6,tload,M)
plt.ylabel('$t_{load}(us)$',fontsize=18)
plt.xlabel('t ($\mu$s)',fontsize=18)
cb=plt.colorbar()
cb.set_label('$\phi_S$ (rad)',fontsize=18)

# ax.tick_params(labelsize=14)
ax.set_title('B='+str(Bfield())+'T_ampliAWG'+str(np.round(ampliAWG(),3)),size=18)
fig.tight_layout()
plt.savefig(folder2+'\\'+dayFolder+'\\'+title+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'.txt',M)


###
M=traceavgD
#Enregistrement des datas dans un sous dossier convenablement nommé 


title=str(dataid)+'phD_tcharge_vstime_G4'+str(VG4())+'mV_G3'+str(VG3())+'mV_AWG'+str(ampliAWG())


# t=np.linspace(delay,acquisition_duration+delay,len(singletraces[0]))

fig,ax = plt.subplots()
# plt.pcolor(t*1e6,Vreads,np.transpose(M))
plt.pcolor(t*1e6,tload,M)
plt.ylabel('$t_{load}(us)$',fontsize=18)
plt.xlabel('t ($\mu$s)',fontsize=18)
cb=plt.colorbar()
cb.set_label('$\phi_D$ (rad)',fontsize=18)

# ax.tick_params(labelsize=14)
ax.set_title('B='+str(Bfield())+'T_ampliAWG'+str(np.round(ampliAWG(),3)),size=18)
fig.tight_layout()
plt.savefig(folder2+'\\'+dayFolder+'\\'+title+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'.txt',M)