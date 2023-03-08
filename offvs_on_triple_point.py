# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 15:46:43 2021

@author: G-GRE-GRE050402
"""
f1=412.5e6

f2=296.922e6

G1freq(f1)
Sfreq(f2)



zerophase=False



points=201
initfD=296.8e6
finalfD=297.2e6

initfG=412.3e6
finalfG=412.7e6

#from lower to higher
#more negative to less negative
initG6=-1502
finalG6=-1499.65
initG5=-1400
finalG5=-1404.1


rampVG6(initG6)
rampVG5(initG5)

ziUhf.daq.setInt('/dev2226/sigouts/0/on', 1)
ziUhf.daq.setInt('/dev2226/sigouts/1/on', 0)

ziUhf.daq.setDouble('/dev2226/demods/0/timeconstant', 0.1)

G1freq(initfG)
time.sleep(0.5)
#####
# rampVG6(initG6)
# ziUhf.daq.setInt('/dev2226/demods/0/phaseadjust', 1)
# ziUhf.daq.setInt('/dev2226/demods/0/phaseadjust', 1)
a,b,c=sweep1D(G1freq,initfG,finalfG,points,0.2,A1)

# name='G5scan_'+T
xlabel='$f_{rf}$(MHz)'
ylabel='$A_{G6}$(V)'
# plot_by_id(b)
# saveplot(name,b)
data_set,data_get,parameters_name=Extract_data(a)
f0_off=data_set[np.argmin(scipy.signal.savgol_filter(data_get[0],11,3))]
# f0_off=data_set[np.argmin(data_get[0])]

plt.figure(figsize=(7.5,5))
plt.plot(data_set*1e-6 ,data_get[0],label='off resonanceVG6='+str(np.round(VG6(),4))+'mV f0='+str(np.round(f0_off*1e-6,5))+'MHz')
# plt.plot(data_set*1e-6 ,scipy.signal.savgol_filter(data_get[0],11,3),label='off resonanceVG6='+str(np.round(VG6(),4))+'mV f0='+str(np.round(f0_off*1e-6,5))+'MHz')
# plt.title('Id vs $V_{g}$')
plt.xlabel(xlabel,fontsize=16)
plt.ylabel(ylabel,fontsize=16)  

G1freq(f1)
Sfreq(f2)
#####sit on interdot
rampVG6(finalG6)
rampVG5(finalG5)
######
ziUhf.daq.setInt('/dev2226/sigouts/0/on', 1)
ziUhf.daq.setInt('/dev2226/sigouts/1/on', 0)
# G1freq(initfG)
# ziUhf.daq.setInt('/dev2226/demods/0/phaseadjust', 1)
# ziUhf.daq.setInt('/dev2226/demods/0/phaseadjust', 1)
a,b,c=sweep1D(G1freq,initfG,finalfG,points,0.2,A1)
data_set,data_get,parameters_name=Extract_data(a)
f0_on=data_set[np.argmin(scipy.signal.savgol_filter(data_get[0],11,3))]
# f0_on=data_set[np.argmin(data_get[0])]
plt.plot(data_set*1e-6 ,data_get[0],label='on interdot VG6='+str(np.round(VG6(),4))+'mV f0='+str(np.round(f0_on*1e-6,5))+'MHz')
# plt.plot(data_set*1e-6 ,scipy.signal.savgol_filter(data_get[0],11,3),label='on interdot VG6='+str(np.round(VG6(),4))+'mV f0='+str(np.round(f0_on*1e-6,5))+'MHz')


# plt.plot(data_set*1e-6 ,scipy.signal.savgol_filter(data_get[0],51,3),label='on interdot VG6='+str(np.round(VG6(),4))+'mV f0='+str(np.round(f0_on*1e-6,5))+'MHz')

#####################


plt.xlabel(xlabel,fontsize=16)
plt.ylabel(ylabel,fontsize=16)  
plt.legend()
name=str(b)+'_G6_'+str(VG6())+'mv_G5'+str(VG5())+'mV'+'_G6res_freqscan_Amplitude_rfpower_'+str(np.round(ziUhf.daq.getDouble('/dev2226/sigouts/0/amplitudes/3')*1e3,3))+'mV'
plt.title(str(b)+'_G6_'+str(VG6())+'mv_G5'+str(VG5())+'mV')
plt.savefig(folder2+'\\'+dayFolder+'\\' +name+'.png')

#################""""
ziUhf.daq.setDouble('/dev2226/demods/0/timeconstant', 0.02)







########
rampVG6(initG6)
rampVG5(initG5)
#####
ziUhf.daq.setInt('/dev2226/sigouts/0/on', 0)
ziUhf.daq.setInt('/dev2226/sigouts/1/on', 1)
# rampVG6(initG6)
Sfreq(initfD)
time.sleep(0.5)
# ziUhf.daq.setInt('/dev2226/demods/0/phaseadjust', 1)
# ziUhf.daq.setInt('/dev2226/demods/0/phaseadjust', 1)
a,b,c=sweep1D(Sfreq,initfD,finalfD,points,0.05,A2)

# name='G5scan_'+T
xlabel='$f_{rf}$(MHz)'
ylabel='$A_{D}$ (V)'
# plot_by_id(b)
# saveplot(name,b)
data_set,data_get,parameters_name=Extract_data(a)

f0_off=data_set[np.argmin(scipy.signal.savgol_filter(data_get[0],11,3))]

plt.figure(figsize=(7.5,5))
plt.plot(data_set*1e-6 ,data_get[0],label='off resonance VG6='+str(np.round(VG6(),4))+'mV f0='+str(np.round(f0_off*1e-6,5))+'MHz')
# plt.title('Id vs $V_{g}$')
plt.xlabel(xlabel,fontsize=16)
plt.ylabel(ylabel,fontsize=16)  

G1freq(f1)
Sfreq(f2)

#####sit on interdot
rampVG6(finalG6)
rampVG5(finalG5)
######
# ziUhf.daq.setInt('/dev2226/demods/0/phaseadjust', 1)
# ziUhf.daq.setInt('/dev2226/demods/0/phaseadjust', 1)
a,b,c=sweep1D(Sfreq,initfD,finalfD,points,0.05,A2)
data_set,data_get,parameters_name=Extract_data(a)
f0_on=data_set[np.argmin(scipy.signal.savgol_filter(data_get[0],11,3))]
# f0_on=data_set[np.argmin(data_get[0])]
plt.plot(data_set*1e-6 ,data_get[0],label='on interdot VG6='+str(np.round(VG6(),4))+'mV f0='+str(np.round(f0_on*1e-6,5))+'MHz')
#####################


plt.xlabel(xlabel,fontsize=16)
plt.ylabel(ylabel,fontsize=16)  
plt.legend()
plt.title(str(b)+'_G6_'+str(VG6())+'mv_G5'+str(VG5())+'mV')
name=str(b)+'_G6_'+str(VG6())+'mv_G5'+str(VG5())+'mV'+'_S_res_freqscan_Amplitude_rfpower_'+str(np.round(ziUhf.daq.getDouble('/dev2226/sigouts/0/amplitudes/3')*1e3,3))+'mV'
plt.savefig(folder2+'\\'+dayFolder+'\\' +name+'.png')






# a,b,c,d =sweep2D(Sfreq,290e6,310e6,201,0.05,VG6,-1914,-1918,121,0.05,A2,ph2)
# the_data = load_by_id(b)
# data_list = the_data.get_parameter_data()
# P = the_data.parameters
# p = P.split(',')
# Y= data_list[p[2]][p[0]]#freq
# X = data_list[p[2]][p[1]]#gate
# x = np.unique(X)
# y = np.unique(Y)
# z1 = data_list[p[2]][p[2]]
# Z1 = z1.reshape((np.size(np.unique(Y)),np.size(np.unique(X)))
# X,Y = np.meshgrid(x,y)
# # #Boris remove bckgnd
# # S = np.shape(Z1)
# # Ph2 = np.zeros(S)

# # for i in range(S[1]):
# #     for j in range(S[0]):
# #         Ph2[j,i] = Z1[j,i] -  np.mean(Z1[:,i]) 
# def removeBackground(data,rangeMin=0, rangeMax=-1):
#     for i in range(len(data)):
#         data[i] = data[i] - data[i][rangeMin:rangeMax].mean() 
#     return(data)

# Z1=removeBackground(Z1)
# f = plt.figure()
# plt.pcolor(X,Y,Z1)
# plt.xlabel(p[0])
# plt.ylabel(p[1])
# plt.colorbar()
# plt.xlabel('G6(mV)')
# plt.ylabel('$rf_S$(Hz)')
# plt.clim(vmin=None,vmax=0.3)
# now=datetime.datetime.now()
# dayFolder=datetime.date.isoformat(now)
# name='G6vs_reflectoS_freq'
# plt.savefig(folder2+'\\'+dayFolder+'\\'+str(b)+name+'.png')







# a,b,c,d =sweep2D(G1freq,400e6,420e6,201,0.05,VG6,-1914,-1918,121,0.05,A1,ph1)
# the_data = load_by_id(b)
# data_list = the_data.get_parameter_data()
# P = the_data.parameters
# p = P.split(',')
# Y= data_list[p[2]][p[0]]#freq
# X = data_list[p[2]][p[1]]#gate
# x = np.unique(X)
# y = np.unique(Y)
# z1 = data_list[p[2]][p[2]]
# Z1 = z1.reshape((np.size(np.unique(Y)),np.size(np.unique(X)))
# X,Y = np.meshgrid(x,y)
# # #Boris remove bckgnd
# # S = np.shape(Z1)
# # Ph2 = np.zeros(S)

# # for i in range(S[1]):
# #     for j in range(S[0]):
# #         Ph2[j,i] = Z1[j,i] -  np.mean(Z1[:,i]) 
# def removeBackground(data,rangeMin=0, rangeMax=-1):
#     for i in range(len(data)):
#         data[i] = data[i] - data[i][rangeMin:rangeMax].mean() 
#     return(data)

# Z1=removeBackground(Z1)
# f = plt.figure()
# plt.pcolor(X,Y,Z1)
# plt.xlabel(p[0])
# plt.ylabel(p[1])
# plt.colorbar()
# plt.xlabel('G6(mV)')
# plt.ylabel('$rf_{G6}$ (Hz)')
# plt.clim(vmin=None,vmax=0.3)
# now=datetime.datetime.now()
# dayFolder=datetime.date.isoformat(now)
# name='G6vs_reflectoG6_freq'
# plt.savefig(folder2+'\\'+dayFolder+'\\'+str(b)+name+'.png')







####phi comparison


# zerophase=False


# points=101
# initfD=295e6
# finalfD=300e6

# initfG=412e6
# finalfG=417e6

# #from lower to higher
# #more negative to less negative
# initG6=-1918
# finalG6=-1914

# VG6onmin_phD(initG6,finalG6,201,1)
# VG5onmin_phD(-1400,-1500,801,1)


########
rampVG6(initG6)
rampVG5(initG5)
#####

ziUhf.daq.setInt('/dev2226/sigouts/0/on', 1)
ziUhf.daq.setInt('/dev2226/sigouts/1/on', 0)

# rampVG6(initG6)
G1freq(initfG)
time.sleep(0.5)
if zerophase:
    time.sleep(0.5)
    ziUhf.daq.setInt('/dev2226/demods/0/phaseadjust', 1)
    time.sleep(0.5)
    ziUhf.daq.setInt('/dev2226/demods/0/phaseadjust', 1)
a,b,c=sweep1D(G1freq,initfG,finalfG,points,0.05,ph1)

# name='G5scan_'+T
xlabel='$f_{rf}$(MHz)'
ylabel='$\phi_{G6}$(deg)'
# plot_by_id(b)
# saveplot(name,b)
data_set,data_get,parameters_name=Extract_data(a)



plt.figure(figsize=(7.5,5))

dphi_off=np.gradient(scipy.signal.savgol_filter(np.ravel(data_get[0]*np.pi/180),11, 6),data_set)
f0_off=data_set[np.argmin(dphi_off)]
Q_off=dphi_off[np.argmin(dphi_off)]/4*f0_off

plt.plot(data_set*1e-6 ,np.unwrap(data_get[0]),label='off resonance VG6='+str(np.round(VG6(),4))+'mV f0='+str(np.round(f0_off*1e-6,5))+'MHz')



# plt.title('Id vs $V_{g}$')


#sitonres
G1freq(f1)
Sfreq(f2)



########
rampVG6(finalG6)
rampVG5(finalG5)
#####

########
G1freq(initfG)
time.sleep(0.5)
if zerophase:
    time.sleep(0.5)
    ziUhf.daq.setInt('/dev2226/demods/0/phaseadjust', 1)
    time.sleep(0.5)
    ziUhf.daq.setInt('/dev2226/demods/0/phaseadjust', 1)
a,b,c=sweep1D(G1freq,initfG,finalfG,points,0.05,ph1)
data_set,data_get,parameters_name=Extract_data(a)


dphi_on=np.gradient(scipy.signal.savgol_filter(np.ravel(data_get[0]*np.pi/180),11, 6),data_set)
f0_on=data_set[np.argmin(dphi_on)]
Q_on=dphi_on[np.argmin(dphi_on)]/4*f0_on
plt.plot(data_set*1e-6 ,np.unwrap(data_get[0]),label='on interdot VG6='+str(np.round(VG6(),4))+'mV f0='+str(np.round(f0_on*1e-6,5))+'MHz')

    
    
    
name=str(b)+'_G6_'+str(VG6())+'mv_G5'+str(VG5())+'mV'+'_G6_'+str(VG6())+'mv_G5'+str(VG5())+'mV'+'_G6res_freqscan_phase_rfpower_'+str(np.round(ziUhf.daq.getDouble('/dev2226/sigouts/0/amplitudes/3')*1e3,3))+'mV'
plt.xlabel(xlabel,fontsize=16)
plt.ylabel(ylabel,fontsize=16)  
plt.legend()
plt.title(str(b)+'_G6_'+str(VG6())+'mv_G5'+str(VG5())+'mV')
plt.savefig(folder2+'\\'+dayFolder+'\\' +name+'.png')


plt.figure(figsize=(8,5))
plt.plot(data_set*1e-6 ,dphi_off,label='off resonance VG6='+str(initG6)+'mV Q='+str(np.round(Q_off,4)))
plt.plot(data_set*1e-6 ,dphi_on,label='on interdot VG6='+str(Vres)+'mV Q=' +str(np.round(Q_on,4)))
# plt.title('Id vs $V_{g}$')
plt.xlabel(xlabel,fontsize=16)
plt.ylabel('$d \phi_{G6} /df$ (rad/Hz)',fontsize=16)  
name=str(b)+'_G6_'+str(VG6())+'mv_G5'+str(VG5())+'mV'+'_G6_res_derivative comparison_gateopenvsgateclosed_rfpower_'+str(np.round(ziUhf.daq.getDouble('/dev2226/sigouts/0/amplitudes/3')*1e3,3))+'mV'
plt.legend(loc='upper right')
plt.savefig(folder2+'\\'+dayFolder+'\\' +name+'.png')









#################on D




ziUhf.daq.setInt('/dev2226/sigouts/0/on', 0)
ziUhf.daq.setInt('/dev2226/sigouts/1/on', 1)

########
rampVG6(initG6)
rampVG5(initG5)
#####

Sfreq(initfD)
time.sleep(0.5)
if zerophase:
    time.sleep(0.5)
    ziUhf.daq.setInt('/dev2226/demods/4/phaseadjust', 1)
    time.sleep(0.5)
    ziUhf.daq.setInt('/dev2226/demods/4/phaseadjust', 1)
a,b,c=sweep1D(Sfreq,initfD,finalfD,points,0.05,ph2)

# name='G5scan_'+T
xlabel='$f_{rf}$(MHz)'
ylabel='$\phi_{D}$(deg)'
# plot_by_id(b)
# saveplot(name,b)
data_set,data_get,parameters_name=Extract_data(a)


plt.figure(figsize=(7.5,5))
plt.plot(data_set*1e-6 ,np.unwrap(data_get[0]),label='off resonance VG6='+str(VG6())+'mV')

dphi_off=np.gradient(scipy.signal.savgol_filter(np.ravel(data_get[0]*np.pi/180),11, 6),data_set)
f0=data_set[np.argmin(dphi_off)]
Q_off=dphi_off[np.argmin(dphi_off)]/4*f0

# plt.title('Id vs $V_{g}$')
plt.xlabel(xlabel,fontsize=16)
plt.ylabel(ylabel,fontsize=16)  

G1freq(f1)
Sfreq(f2)

########
rampVG6(finalG6)
rampVG5(finalG5)
#####

Vres=VG6()
Sfreq(initfD)
time.sleep(0.5)
if zerophase:
    time.sleep(0.5)
    ziUhf.daq.setInt('/dev2226/demods/4/phaseadjust', 1)
    time.sleep(0.5)
    ziUhf.daq.setInt('/dev2226/demods/4/phaseadjust', 1)
    
a,b,c=sweep1D(Sfreq,initfD,finalfD,points,0.05,ph2)
data_set,data_get,parameters_name=Extract_data(a)
plt.plot(data_set*1e-6 ,np.unwrap(data_get[0]),label='on interdot VG6='+str(VG6())+'mV')
dphi_on=np.gradient(scipy.signal.savgol_filter(np.ravel(data_get[0]*np.pi/180),11, 6),data_set)
f0_on=data_set[np.argmin(dphi_on)]
Q_on=dphi_on[np.argmin(dphi_on)]/4*f0_on
#####################



plt.xlabel(xlabel,fontsize=16)
plt.ylabel(ylabel,fontsize=16)  
plt.legend()
name=str(b)+'_G6_'+str(VG6())+'mv_G5'+str(VG5())+'mV'+'_S_res_freqscan_phi_gateopenvsgateclosed_rfpower_'+str(np.round(ziUhf.daq.getDouble('/dev2226/sigouts/1/amplitudes/7')*1e3,3))+'mV'
plt.title(str(b)+'_G6_'+str(VG6())+'mv_G5'+str(VG5())+'mV')
plt.savefig(folder2+'\\'+dayFolder+'\\' +name+'.png')




plt.figure(figsize=(8,5))
plt.plot(data_set*1e-6 ,dphi_off,label='off resonance VG6='+str(initG6)+'mV Q='+str(Q_off))
plt.plot(data_set*1e-6 ,dphi_on,label='on interdot VG6='+str(Vres)+'mV Q='+str(Q_on))
# plt.title('Id vs $V_{g}$')
plt.xlabel(xlabel,fontsize=16)
plt.ylabel('$d \phi_D /df$ (rad/Hz)',fontsize=16)  
name=str(b)+'_G6_'+str(VG6())+'mv_G5'+str(VG5())+'mV'+'_S_res_derivative comparison_gateopenvsgateclosed_rfpower_'+str(np.round(ziUhf.daq.getDouble('/dev2226/sigouts/0/amplitudes/3')*1e3,3))+'mV'
plt.legend(loc='upper right')
plt.savefig(folder2+'\\'+dayFolder+'\\' +name+'.png')


# G1freq(f1)
# Sfreq(f2)

# ziUhf.daq.setInt('/dev2226/sigouts/0/on', 1)
# ziUhf.daq.setInt('/dev2226/sigouts/1/on', 0)
# a,b,c=sweep1D(VG6,finalG6-1,finalG6+1,points,0.02,A1,ph1)
# plot_by_id(b)
# name='_G6_'+str(VG6())+'mv_G5'+str(VG5())+'mV'+'_G6resonance'
# # plt.rcParams["figure.figsize"]=(12,9)
# # plt.rcParams["label.labelsize"]=16
# save2plots(name,b)


# ziUhf.daq.setInt('/dev2226/sigouts/0/on', 0)
# ziUhf.daq.setInt('/dev2226/sigouts/1/on', 1)
# a,b,c=sweep1D(VG6,finalG6-1,finalG6+1,points,0.02,A2,ph2)
# plot_by_id(b)
# name='_G6_'+str(VG6())+'mv_G5'+str(VG5())+'mV'+'_Sresonance'
# # plt.rcParams["figure.figsize"]=(12,9)
# # plt.rcParams["label.labelsize"]=16
# save2plots(name,b)
