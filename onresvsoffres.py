# -*- coding: utf-8 -*-
"""
Created on Mon Jul  5 16:53:37 2021

@author: G-GRE-GRE050402

"""







points=401

initG1=-10+-550
finalG1=-10+-570




VG1(initG1)
a,b,c=sweep1D(G1freq,451e6,454e6,points,0.02,ph1)

# name='G5scan_'+T
xlabel='$f_{rf}$(MHz)'
ylabel='$\phi_{G1}$(deg)'
# plot_by_id(b)
# saveplot(name,b)
data_set,data_get,parameters_name=Extract_data(a)


plt.figure()
plt.plot(data_set*1e-6 ,np.unwrap(data_get[0]),label='off resonance VG1='+str(VG1())+'mV')
# plt.title('Id vs $V_{g}$')


######
VG1onmin_f(initG1,finalG1,401,0,fS)
########

a,b,c=sweep1D(G1freq,451e6,454e6,points,0.02,ph1)
data_set,data_get,parameters_name=Extract_data(a)
plt.plot(data_set*1e-6 ,np.unwrap(data_get[0]),label='on resonance VG1='+str(VG1())+'mV')

name=str(b)+'_G1res_freqscan_phase_rfpower_'+str(np.round(ziUhf.daq.getDouble('/dev2226/sigouts/0/amplitudes/3')*1e3,3))+'mV'
plt.xlabel(xlabel,fontsize=16)
plt.ylabel(ylabel,fontsize=16)  
plt.legend()
plt.savefig(folder2+'\\'+dayFolder+'\\' +name+'.png')
#####################


VG1(initG1)
a,b,c=sweep1D(G1freq,451e6,454e6,points,0.02,A1)

# name='G5scan_'+T
xlabel='$f_{rf}$(MHz)'
ylabel='$A_{G1}$(deg)'
# plot_by_id(b)
# saveplot(name,b)
data_set,data_get,parameters_name=Extract_data(a)


plt.figure()
plt.plot(data_set*1e-6 ,np.unwrap(data_get[0]),label='off resonance VG1='+str(VG1())+'mV')
# plt.title('Id vs $V_{g}$')
plt.xlabel(xlabel,fontsize=16)
plt.ylabel(ylabel,fontsize=16)  


VG1onmin_f(initG1,finalG1,401,0,fS)


a,b,c=sweep1D(G1freq,451e6,454e6,points,0.02,A1)
data_set,data_get,parameters_name=Extract_data(a)
plt.plot(data_set*1e-6 ,np.unwrap(data_get[0]),label='on resonance VG1='+str(VG1())+'mV')
#####################


plt.xlabel(xlabel,fontsize=16)
plt.ylabel(ylabel,fontsize=16)  
plt.legend()
name=str(b)+'_G1res_freqscan_Amplitude_rfpower_'+str(np.round(ziUhf.daq.getDouble('/dev2226/sigouts/0/amplitudes/3')*1e3,3))+'mV'
plt.savefig(folder2+'\\'+dayFolder+'\\' +name+'.png')








#same but close to resonances of S
VG1(initG1)
a,b,c=sweep1D(G1freq,373e6,376e6,points,0.02,ph1)

# name='G5scan_'+T
xlabel='$f_{rf}$(MHz)'
ylabel='$\phi_{S}$(deg)'
# plot_by_id(b)
# saveplot(name,b)
data_set,data_get,parameters_name=Extract_data(a)


plt.figure()
plt.plot(data_set*1e-6 ,np.unwrap(data_get[0]),label='off resonance VG1='+str(VG1())+'mV')
# plt.title('Id vs $V_{g}$')
plt.xlabel(xlabel,fontsize=16)
plt.ylabel(ylabel,fontsize=16)  


VG1onmin_f(initG1,finalG1,401,0,fS)

a,b,c=sweep1D(G1freq,373e6,376e6,points,0.02,ph1)
data_set,data_get,parameters_name=Extract_data(a)
plt.plot(data_set*1e-6 ,np.unwrap(data_get[0]),label='on resonance VG1='+str(VG1())+'mV')
#####################



plt.xlabel(xlabel,fontsize=16)
plt.ylabel(ylabel,fontsize=16)  
plt.legend()
name=str(b)+'_S_res_freqscan_phi_gateopenvsgateclosed_rfpower_'+str(np.round(ziUhf.daq.getDouble('/dev2226/sigouts/0/amplitudes/3')*1e3,3))+'mV'
plt.savefig(folder2+'\\'+dayFolder+'\\' +name+'.png')
  

######same for amplitude
VG1(initG1)
a,b,c=sweep1D(G1freq,373e6,376e6,points,0.02,A1)

# name='G5scan_'+T
xlabel='$f_{rf}$(MHz)'
ylabel='$A_{S}$(V)'
# plot_by_id(b)
# saveplot(name,b)
data_set,data_get,parameters_name=Extract_data(a)


plt.figure()
plt.plot(data_set*1e-6 ,np.unwrap(data_get[0]),label='off resonance VG1='+str(VG1())+'mV')
# plt.title('Id vs $V_{g}$')
plt.xlabel(xlabel,fontsize=16)
plt.ylabel(ylabel,fontsize=16)  


VG1onmin_f(initG1,finalG1,401,0,fS)

a,b,c=sweep1D(G1freq,373e6,376e6,points,0.02,A1)
data_set,data_get,parameters_name=Extract_data(a)
plt.plot(data_set*1e-6 ,np.unwrap(data_get[0]),label='on resonance VG1='+str(VG1())+'mV')
#####################


plt.xlabel(xlabel,fontsize=16)
plt.ylabel(ylabel,fontsize=16)  
plt.legend()
name=str(b)+'_S_res_freqscan_Amplitude_rfpower_'+str(np.round(ziUhf.daq.getDouble('/dev2226/sigouts/0/amplitudes/3')*1e3,3))+'mV'
plt.savefig(folder2+'\\'+dayFolder+'\\' +name+'.png')







