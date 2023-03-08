# -*- coding: utf-8 -*-
"""
Created on Mon Jul  5 15:14:28 2021

@author: G-GRE-GRE050402
"""
dac.set_dacs_zero()
finalgate=-2000
initgate=0
opengate=-2000

#########
a,b,c=sweep1D(G1freq,200e6,500e6,3001,0.02,ph1)

# name='G5scan_'+T
xlabel='$f_{rf}$(MHz)'
ylabel='$\phi$(deg)'
# plot_by_id(b)
# saveplot(name,b)
data_set,data_get,parameters_name=Extract_data(a)



plt.figure()
plt.plot(data_set*1e-6 ,np.unwrap(data_get[0]),label='all gates closed') 
# plt.title('Id vs $V_{g}$')
plt.xlabel(xlabel,fontsize=16)
plt.ylabel(ylabel,fontsize=16)  


bias(0.5)
rampVG1(opengate)
rampVG2(opengate)
rampVG3(opengate)
rampVG4(opengate)
rampVG5(opengate)
rampVG6(opengate)
a,b,c=sweep1D(G1freq,200e6,500e6,3001,0.02,ph1)
data_set,data_get,parameters_name=Extract_data(a)
plt.plot(data_set*1e-6 ,np.unwrap(data_get[0]),label='all gates open at -2V') 


#####################



plt.xlabel(xlabel,fontsize=16)
plt.ylabel(ylabel,fontsize=16)  
plt.legend()
name=str(b)+'freqscan_phi_gateopenvsgateclosed_rfpower_'+str(np.round(ziUhf.daq.getDouble('/dev2226/sigouts/0/amplitudes/3')*1e3,3))+'mV'
plt.savefig(folder2+'\\'+dayFolder+'\\' +name+'.png')
  

######same for amplitude
dac.set_dacs_zero()


a,b,c=sweep1D(G1freq,200e6,500e6,3001,0.02,A1)

# name='G5scan_'+T
xlabel='$f_{rf}$(MHz)'
ylabel='$A$(V)'
# plot_by_id(b)
# saveplot(name,b)
data_set,data_get,parameters_name=Extract_data(a)



plt.figure()
plt.plot(data_set*1e-6 ,data_get[0],label='all gates closed') 
# plt.title('Id vs $V_{g}$')
plt.xlabel(xlabel,fontsize=16)
plt.ylabel(ylabel,fontsize=16)  


bias(0.5)
rampVG1(opengate)
rampVG2(opengate)
rampVG3(opengate)
rampVG4(opengate)
rampVG5(opengate)
rampVG6(opengate)
a,b,c=sweep1D(G1freq,200e6,500e6,3001,0.02,A1)
data_set,data_get,parameters_name=Extract_data(a)
plt.plot(data_set*1e-6 ,data_get[0],label='all gates open at -2V') 
#####################


plt.xlabel(xlabel,fontsize=16)
plt.ylabel(ylabel,fontsize=16)  
plt.legend()
name=str(b)+'freqscan_Amplitude_gateopenvsgateclosed_rfpower_'+str(np.round(ziUhf.daq.getDouble('/dev2226/sigouts/0/amplitudes/3')*1e3,3))+'mV'
plt.savefig(folder2+'\\'+dayFolder+'\\' +name+'.png')








####################################################################
##################################
##################################
#same but close to resonances of G1
dac.set_dacs_zero()
a,b,c=sweep1D(G1freq,451e6,454e6,601,0.02,ph1)

# name='G5scan_'+T
xlabel='$f_{rf}$(MHz)'
ylabel='$\phi_{G1}$(deg)'
# plot_by_id(b)
# saveplot(name,b)
data_set,data_get,parameters_name=Extract_data(a)



plt.figure()
plt.plot(data_set*1e-6 ,np.unwrap(data_get[0]),label='all gates closed') 
# plt.title('Id vs $V_{g}$')
plt.xlabel(xlabel,fontsize=16)
plt.ylabel(ylabel,fontsize=16)  


bias(0.5)
rampVG1(opengate)
rampVG2(opengate)
rampVG3(opengate)
rampVG4(opengate)
rampVG5(opengate)
rampVG6(opengate)
a,b,c=sweep1D(G1freq,451e6,454e6,601,0.02,ph1)
data_set,data_get,parameters_name=Extract_data(a)
plt.plot(data_set*1e-6 ,np.unwrap(data_get[0]),label='all gates open at -2V') 


#####################



plt.xlabel(xlabel,fontsize=16)
plt.ylabel(ylabel,fontsize=16)  
plt.legend()
name=str(b)+'G1res_freqscan_phi_gateopenvsgateclosed_rfpower_'+str(np.round(ziUhf.daq.getDouble('/dev2226/sigouts/0/amplitudes/3')*1e3,3))+'mV'
plt.savefig(folder2+'\\'+dayFolder+'\\' +name+'.png')
  

######same for amplitude
dac.set_dacs_zero()


a,b,c=sweep1D(G1freq,451e6,454e6,601,0.02,A1)

# name=str(b)+'G5scan_'+T
xlabel='$f_{rf}$(MHz)'
ylabel='$A_{G1}$(V)'
# plot_by_id(b)
# saveplot(name,b)
data_set,data_get,parameters_name=Extract_data(a)



plt.figure()
plt.plot(data_set*1e-6 ,data_get[0],label='all gates closed') 
# plt.title('Id vs $V_{g}$')
plt.xlabel(xlabel,fontsize=16)
plt.ylabel(ylabel,fontsize=16)  


bias(0.5)
rampVG1(opengate)
rampVG2(opengate)
rampVG3(opengate)
rampVG4(opengate)
rampVG5(opengate)
rampVG6(opengate)
a,b,c=sweep1D(G1freq,451e6,454e6,601,0.02,A1)
data_set,data_get,parameters_name=Extract_data(a)
plt.plot(data_set*1e-6 ,data_get[0],label='all gates open at -2V') 
#####################


plt.xlabel(xlabel,fontsize=16)
plt.ylabel(ylabel,fontsize=16)  
plt.legend()
name=str(b)+'_G1res_freqscan_Amplitude_rfpower_'+str(np.round(ziUhf.daq.getDouble('/dev2226/sigouts/0/amplitudes/3')*1e3,3))+'mV'
plt.savefig(folder2+'\\'+dayFolder+'\\' +name+'.png')








#same but close to resonances of S
dac.set_dacs_zero()
a,b,c=sweep1D(G1freq,373e6,376e6,601,0.02,ph1)

# name='G5scan_'+T
xlabel='$f_{rf}$(MHz)'
ylabel='$\phi_S$(deg)'
# plot_by_id(b)
# saveplot(name,b)
data_set,data_get,parameters_name=Extract_data(a)



plt.figure()
plt.plot(data_set*1e-6 ,np.unwrap(data_get[0]),label='all gates closed') 
# plt.title('Id vs $V_{g}$')
plt.xlabel(xlabel,fontsize=16)
plt.ylabel(ylabel,fontsize=16)  


bias(0.5)
rampVG1(opengate)
rampVG2(opengate)
rampVG3(opengate)
rampVG4(opengate)
rampVG5(opengate)
rampVG6(opengate)
a,b,c=sweep1D(G1freq,373e6,376e6,601,0.02,ph1)
data_set,data_get,parameters_name=Extract_data(a)
plt.plot(data_set*1e-6 ,np.unwrap(data_get[0]),label='all gates open at -2V') 


#####################



plt.xlabel(xlabel,fontsize=16)
plt.ylabel(ylabel,fontsize=16)  
plt.legend()
name=str(b)+'_S_res_freqscan_phi_gateopenvsgateclosed_rfpower_'+str(np.round(ziUhf.daq.getDouble('/dev2226/sigouts/0/amplitudes/3')*1e3,3))+'mV'
plt.savefig(folder2+'\\'+dayFolder+'\\' +name+'.png')
  

######same for amplitude
dac.set_dacs_zero()


a,b,c=sweep1D(G1freq,373e6,376e6,601,0.02,A1)

# name=str(b)+'G5scan_'+T
xlabel='$f_{rf}$(MHz)'
ylabel='$A_S$(V)'
# plot_by_id(b)
# saveplot(name,b)
data_set,data_get,parameters_name=Extract_data(a)



plt.figure()
plt.plot(data_set*1e-6 ,data_get[0],label='all gates closed') 
# plt.title('Id vs $V_{g}$')
plt.xlabel(xlabel,fontsize=16)
plt.ylabel(ylabel,fontsize=16)  


bias(0.5)
rampVG1(opengate)
rampVG2(opengate)
rampVG3(opengate)
rampVG4(opengate)
rampVG5(opengate)
rampVG6(opengate)
a,b,c=sweep1D(G1freq,373e6,376e6,601,0.02,A1)
data_set,data_get,parameters_name=Extract_data(a)
plt.plot(data_set*1e-6 ,data_get[0],label='all gates open at -2V') 
#####################


plt.xlabel(xlabel,fontsize=16)
plt.ylabel(ylabel,fontsize=16)  
plt.legend()
name=str(b)+'_S_res_freqscan_Amplitude_rfpower_'+str(np.round(ziUhf.daq.getDouble('/dev2226/sigouts/0/amplitudes/3')*1e3,3))+'mV'
plt.savefig(folder2+'\\'+dayFolder+'\\' +name+'.png')























def VG1onmin_f(initVT2,finalVT2,points,showplot,f):
    #include correction for axis direction
    rampVG1(initVT2)
    time.sleep(0.1)
    fG1=452.55e6
    fS=374.42e6
    
    # G1freq(fG1)
    # Sfreq(fS)

    if f==fG1:
        G1freq(fG1)
        a,dataid,c=sweep1D(rampVG1, initVT2,finalVT2,points,0.01,ph1)
    if f==fS:
        G1freq(fS)
        a,dataid,c=sweep1D(rampVG1, initVT2,finalVT2,points,0.01,ph1)
    
    now=datetime.datetime.now()
    dayFolder= datetime.date.isoformat(now)
    try:
        os.makedirs(folder2+'\\'+dayFolder)
    except IOError:
        donothing=1

    folder=r'S:\132-PHELIQS\132.05-LATEQS\132.05.01-QuantumSilicon\Tritonito\2021\Feb2021_6G22_2_die103\\data'
    name=str(dataid)+'_G1scan_calibrate_cs'
    xlabel='$V_{G1}$(mV)'
    ylabel='$\phi_{S}$(deg)'
    data_set,data_get,parameters_name=Extract_data(a)
    if showplot==1:
     # plot_by_id(b)
     # plt.close()
     plot_savetxt(data_set,xlabel,data_get,ylabel,parameters_name,folder+'\\'+dayFolder,name)


    datasmooth=scipy.signal.savgol_filter(np.ravel(data_get[0]),11, 3)
    phimin=np.min(datasmooth)
    argmin=np.argmin(datasmooth)

   
    rampVG1(data_set[argmin])
    print('minpeak_VG1='+str(VG1()))





####### resonance vs off resonance
dac.set_dacs_zero()
bias(-0.22)
rampVG1(-500)
rampVG2(0)
rampVG3(0)
rampVG4(0)
rampVG5(0)
rampVG6(0)
fG1=452.55e6
fS=374.42e6

G1freq(452.55e6)
Sfreq(374.42e6)

####check maximum phase for real 

#work on phi1
VG1onmin_f(-550,-570,501,1,fS)






