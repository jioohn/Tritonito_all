# -*- coding: utf-8 -*-
"""
Created on Mon Jul  5 19:33:43 2021

@author: G-GRE-GRE050402
"""

f1=413.14e6
f2=296.922e6

G1freq(f1)
Sfreq(f2)


# initfD=296.9e6
# finalfD=296.93e6
initfG=412e6
finalfG=414e6


initfD=296e6
finalfD=298e6

# initfG=412e6
# finalfG=413e6

points=201


def VG5onmin_phD(initVT2,finalVT2,points,showplot):
    rampVG5(initVT2)
    time.sleep(0.1)
    a,dataid,c=sweep1D(VG5, initVT2,finalVT2,points,0.02,ph2)
    now=datetime.datetime.now()
    dayFolder= datetime.date.isoformat(now)
    try:
        os.makedirs(folder2+'\\'+dayFolder)
    except IOError:
        donothing=1

    folder=r'S:\132-PHELIQS\132.05-LATEQS\132.05.01-QuantumSilicon\Tritonito\2021\Feb2021_6G22_2_die103\\data'
    name=str(dataid)+'_G5scan_calibrate_cs_D'
    xlabel='$V_{G5}$(mV)'
    ylabel='$\phi_{D}$(deg)'
    data_set,data_get,parameters_name=Extract_data(a)
    if showplot==1:
     # plot_by_id(b)
     # plt.close()
     plot_savetxt(data_set,xlabel,data_get,ylabel,parameters_name,folder+'\\'+dayFolder,name)


    datasmooth=scipy.signal.savgol_filter(np.ravel(data_get[0]),11, 3)
    phimin=np.min(datasmooth)
    argmin=np.argmin(datasmooth)

   
    VG5(data_set[argmin])
    print('minpeak_VG5='+str(VG5()))  

def VG6onmin_phD(initVT2,finalVT2,points,showplot):
    rampVG6(initVT2)
    time.sleep(0.1)
    a,dataid,c=sweep1D(VG6, initVT2,finalVT2,points,0.01,ph2)
    now=datetime.datetime.now()
    dayFolder= datetime.date.isoformat(now)
    try:
        os.makedirs(folder2+'\\'+dayFolder)
    except IOError:
        donothing=1

    folder=r'S:\132-PHELIQS\132.05-LATEQS\132.05.01-QuantumSilicon\Tritonito\2021\Feb2021_6G22_2_die103\\data'
    name=str(dataid)+'_G6scan_calibrate_cs_D'
    xlabel='$V_{G6}$(mV)'
    ylabel='$\phi_{D}$(deg)'
    data_set,data_get,parameters_name=Extract_data(a)
    if showplot==1:
     # plot_by_id(b)
     # plt.close()
     plot_savetxt(data_set,xlabel,data_get,ylabel,parameters_name,folder+'\\'+dayFolder,name)


    datasmooth=scipy.signal.savgol_filter(np.ravel(data_get[0]),11, 3)
    phimin=np.min(datasmooth)
    argmin=np.argmin(datasmooth)

   
    VG6(data_set[argmin])
    print('minpeak_VG6='+str(VG6()))  
    
    
def VG6onmin_phG6(initVT2,finalVT2,points,showplot):
    rampVG6(initVT2)
    time.sleep(0.1)
    a,dataid,c=sweep1D(VG6, initVT2,finalVT2,points,0.01,ph1)
    now=datetime.datetime.now()
    dayFolder= datetime.date.isoformat(now)
    try:
        os.makedirs(folder2+'\\'+dayFolder)
    except IOError:
        donothing=1

    folder=r'S:\132-PHELIQS\132.05-LATEQS\132.05.01-QuantumSilicon\Tritonito\2021\Feb2021_6G22_2_die103\\data'
    name=str(dataid)+'_G6scan_calibrate_cs_D'
    xlabel='$V_{G6}$(mV)'
    ylabel='$\phi_{G6}$(deg)'
    data_set,data_get,parameters_name=Extract_data(a)
    if showplot==1:
     # plot_by_id(b)
     # plt.close()
     plot_savetxt(data_set,xlabel,data_get,ylabel,parameters_name,folder+'\\'+dayFolder,name)


    datasmooth=scipy.signal.savgol_filter(np.ravel(data_get[0]),11, 3)
    phimin=np.min(datasmooth)
    argmin=np.argmin(datasmooth)

   
    VG6(data_set[argmin])
    print('minpeak_VG6='+str(VG6()))  
    
    
    
    
# initfD=290e6
# finalfD=310e6

# initfG=400e6
# finalfG=420e6
    
    
# rampVG5(-1406)



zerophase=False



points=201

#from lower to higher
#more negative to less negative
initG6=-1918
finalG6=-1914

# VG6onmin_phD(initG6,finalG6,201,1)
# VG5onmin_phD(-1400,-1500,801,1)




rampVG6(initG6)
G1freq(initfG)
if zerophase:
    time.sleep(0.5)
    ziUhf.daq.setInt('/dev2226/demods/0/phaseadjust', 1)
    time.sleep(0.5)
    ziUhf.daq.setInt('/dev2226/demods/0/phaseadjust', 1)
a,b,c=sweep1D(G1freq,initfG,finalfG,points,0.02,ph1)

# name='G5scan_'+T
xlabel='$f_{rf}$(MHz)'
ylabel='$\phi_{G6}$(deg)'
# plot_by_id(b)
# saveplot(name,b)
data_set,data_get,parameters_name=Extract_data(a)



plt.figure(figsize=(7.5,5))
plt.plot(data_set*1e-6 ,np.unwrap(data_get[0]),label='off resonance VG6='+str(VG6())+'mV')
# plt.title('Id vs $V_{g}$')




#sitonres
G1freq(f1)
Sfreq(f2)



######
G1freq(f1)
Sfreq(f2)
VG6onmin_phD(initG6,finalG6,201,0)
########
G1freq(initfG)
if zerophase:
    time.sleep(0.5)
    ziUhf.daq.setInt('/dev2226/demods/0/phaseadjust', 1)
    time.sleep(0.5)
    ziUhf.daq.setInt('/dev2226/demods/0/phaseadjust', 1)
a,b,c=sweep1D(G1freq,initfG,finalfG,points,0.02,ph1)
data_set,data_get,parameters_name=Extract_data(a)
plt.plot(data_set*1e-6 ,np.unwrap(data_get[0]),label='on resonance VG6='+str(VG6())+'mV')

name=str(b)+'_G6_'+str(VG6())+'mv_G5'+str(VG5())+'mV'+'_G6_'+str(VG6())+'mv_G5'+str(VG5())+'mV'+'_G6res_freqscan_phase_rfpower_'+str(np.round(ziUhf.daq.getDouble('/dev2226/sigouts/0/amplitudes/3')*1e3,3))+'mV'
plt.xlabel(xlabel,fontsize=16)
plt.ylabel(ylabel,fontsize=16)  
plt.legend()
plt.title(str(b)+'_G6_'+str(VG6())+'mv_G5'+str(VG5())+'mV')
plt.savefig(folder2+'\\'+dayFolder+'\\' +name+'.png')
#####################


rampVG6(initG6)
# ziUhf.daq.setInt('/dev2226/demods/0/phaseadjust', 1)
# ziUhf.daq.setInt('/dev2226/demods/0/phaseadjust', 1)
a,b,c=sweep1D(G1freq,initfG,finalfG,points,0.02,A1)

# name='G5scan_'+T
xlabel='$f_{rf}$(MHz)'
ylabel='$A_{G6}$(V)'
# plot_by_id(b)
# saveplot(name,b)
data_set,data_get,parameters_name=Extract_data(a)


plt.figure(figsize=(7.5,5))
plt.plot(data_set*1e-6 ,np.unwrap(data_get[0]),label='off resonance VG6='+str(VG6())+'mV')
# plt.title('Id vs $V_{g}$')
plt.xlabel(xlabel,fontsize=16)
plt.ylabel(ylabel,fontsize=16)  

G1freq(f1)
Sfreq(f2)
VG6onmin_phD(initG6,finalG6,101,0)
# G1freq(initfG)
# ziUhf.daq.setInt('/dev2226/demods/0/phaseadjust', 1)
# ziUhf.daq.setInt('/dev2226/demods/0/phaseadjust', 1)
a,b,c=sweep1D(G1freq,initfG,finalfG,points,0.02,A1)
data_set,data_get,parameters_name=Extract_data(a)
plt.plot(data_set*1e-6 ,np.unwrap(data_get[0]),label='on resonance VG6='+str(VG6())+'mV')
#####################


plt.xlabel(xlabel,fontsize=16)
plt.ylabel(ylabel,fontsize=16)  
plt.legend()
name=str(b)+'_G6_'+str(VG6())+'mv_G5'+str(VG5())+'mV'+'_G6res_freqscan_Amplitude_rfpower_'+str(np.round(ziUhf.daq.getDouble('/dev2226/sigouts/0/amplitudes/3')*1e3,3))+'mV'
plt.title(str(b)+'_G6_'+str(VG6())+'mv_G5'+str(VG5())+'mV')
plt.savefig(folder2+'\\'+dayFolder+'\\' +name+'.png')








#same but close to resonances of S

rampVG6(initG6)
Sfreq(initfD)
if zerophase:
    time.sleep(0.5)
    ziUhf.daq.setInt('/dev2226/demods/4/phaseadjust', 1)
    time.sleep(0.5)
    ziUhf.daq.setInt('/dev2226/demods/4/phaseadjust', 1)
a,b,c=sweep1D(Sfreq,initfD,finalfD,points,0.02,ph2)

# name='G5scan_'+T
xlabel='$f_{rf}$(MHz)'
ylabel='$\phi_{D}$(deg)'
# plot_by_id(b)
# saveplot(name,b)
data_set,data_get,parameters_name=Extract_data(a)


plt.figure(figsize=(7.5,5))
plt.plot(data_set*1e-6 ,np.unwrap(data_get[0]),label='off resonance VG6='+str(VG6())+'mV')
# plt.title('Id vs $V_{g}$')
plt.xlabel(xlabel,fontsize=16)
plt.ylabel(ylabel,fontsize=16)  

G1freq(f1)
Sfreq(f2)
VG6onmin_phD(initG6,finalG6,101,0)
Sfreq(initfD)
if zerophase:
    time.sleep(0.5)
    ziUhf.daq.setInt('/dev2226/demods/4/phaseadjust', 1)
    time.sleep(0.5)
    ziUhf.daq.setInt('/dev2226/demods/4/phaseadjust', 1)
    
a,b,c=sweep1D(Sfreq,initfD,finalfD,points,0.02,ph2)
data_set,data_get,parameters_name=Extract_data(a)
plt.plot(data_set*1e-6 ,np.unwrap(data_get[0]),label='on resonance VG6='+str(VG6())+'mV')
#####################



plt.xlabel(xlabel,fontsize=16)
plt.ylabel(ylabel,fontsize=16)  
plt.legend()
name=str(b)+'_G6_'+str(VG6())+'mv_G5'+str(VG5())+'mV'+'_S_res_freqscan_phi_gateopenvsgateclosed_rfpower_'+str(np.round(ziUhf.daq.getDouble('/dev2226/sigouts/0/amplitudes/3')*1e3,3))+'mV'
plt.title(str(b)+'_G6_'+str(VG6())+'mv_G5'+str(VG5())+'mV')
plt.savefig(folder2+'\\'+dayFolder+'\\' +name+'.png')
  

######same for amplitude
rampVG6(initG6)
Sfreq(initfD)
# ziUhf.daq.setInt('/dev2226/demods/0/phaseadjust', 1)
# ziUhf.daq.setInt('/dev2226/demods/0/phaseadjust', 1)
a,b,c=sweep1D(Sfreq,initfD,finalfD,points,0.02,A2)

# name='G5scan_'+T
xlabel='$f_{rf}$(MHz)'
ylabel='$A_{D}$ (V)'
# plot_by_id(b)
# saveplot(name,b)
data_set,data_get,parameters_name=Extract_data(a)



plt.figure(figsize=(7.5,5))
plt.plot(data_set*1e-6 ,np.unwrap(data_get[0]),label='off resonance VG6='+str(VG6())+'mV')
# plt.title('Id vs $V_{g}$')
plt.xlabel(xlabel,fontsize=16)
plt.ylabel(ylabel,fontsize=16)  

G1freq(f1)
Sfreq(f2)
VG6onmin_phD(initG6,finalG6,101,0)
# ziUhf.daq.setInt('/dev2226/demods/0/phaseadjust', 1)
# ziUhf.daq.setInt('/dev2226/demods/0/phaseadjust', 1)
a,b,c=sweep1D(Sfreq,initfD,finalfD,points,0.02,A2)
data_set,data_get,parameters_name=Extract_data(a)
plt.plot(data_set*1e-6 ,np.unwrap(data_get[0]),label='on resonance VG6='+str(VG6())+'mV')
#####################


plt.xlabel(xlabel,fontsize=16)
plt.ylabel(ylabel,fontsize=16)  
plt.legend()
plt.title(str(b)+'_G6_'+str(VG6())+'mv_G5'+str(VG5())+'mV')
name=str(b)+'_G6_'+str(VG6())+'mv_G5'+str(VG5())+'mV'+'_S_res_freqscan_Amplitude_rfpower_'+str(np.round(ziUhf.daq.getDouble('/dev2226/sigouts/0/amplitudes/3')*1e3,3))+'mV'
plt.savefig(folder2+'\\'+dayFolder+'\\' +name+'.png')



# plot_by_id(b-1)
# name=str(b-1)+'_G6_'+str(VG6())+'mv_G5'+str(VG5())+'mV'+'_drainresonance'
# saveplot(name,b-1)


G1freq(f1)
Sfreq(f2)


a,b,c=sweep1D(VG6,initG6,finalG6,points,0.02,A1,ph1)
plot_by_id(b)
name='_G6_'+str(VG6())+'mv_G5'+str(VG5())+'mV'+'_G6resonance'
# plt.rcParams["figure.figsize"]=(12,9)
# plt.rcParams["label.labelsize"]=16
save2plots(name,b)


a,b,c=sweep1D(VG6,initG6,finalG6,points,0.02,A2,ph2)
plot_by_id(b)
name='_G6_'+str(VG6())+'mv_G5'+str(VG5())+'mV'+'_G6resonance'
# plt.rcParams["figure.figsize"]=(12,9)
# plt.rcParams["label.labelsize"]=16
save2plots(name,b)
