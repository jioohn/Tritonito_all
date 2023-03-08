# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 11:39:38 2020

@author: G-GRE-GRE050402
"""

Bfield(0)
# M=np.zeros((Bpoints,points)) #y,x
M=[]
ydata=[]
tempty=[]
# tguessarray=[]
# tguessarray2=[]
# tguessgoodarray=[]

temptyfitarray=[]
# temptyfitarray2=[]
temptyfitarray_nodelay=[]
temptyerrorfitarray_nodelay=[]
Tarray=[]
# foldername="O:\\132-PHELIQS\\132.05-LATEQS\\132.05.01-QuantumSilicon\\Tritonito\\data\\2019-11-05\\"
errorTarray=[]
tunnelarray=[]
tunnelarrayerr=[]
T=0.37

taxis=np.linspace(0,200e-6,88)
t=time.time()
for i in range(0,100):
    # print('field='+str(Bfield()))
#    Bfield(Binit+Bfinal/(Bpoints-1)*i)
    # Bfield_Hon(Binit+dB*i)
    # time.sleep(30)
#    tguessarray2.append(tguess2)
    ydata.append(time.time()-t)
    ampliAWG(0.2)
    # continuous_acquisition()
    # VG4comp(-799)
    # VG3comp(-936.7)
    # ziUhf.daq.setInt('/dev2010/sigouts/1/on', 0)
    # sensor_on_interdot_sweepG4comp(-802,-797,201,0)
    # G4val.append(VG4())
    trigger_mode()
    ziUhf.daq.setInt('/dev2010/sigouts/1/on', 1)
    ziUhf.daq.setDouble('/dev2010/demods/0/rate', 400e3)
    ziUhf.daq.setDouble('/dev2010/demods/0/timeconstant', 1e-6)
    phase=phase_trig()
    phase=phase[0]
    M.append(phase)
    
    
    # fig, ax = plt.subplots()
    # ax.set_xlabel('time(s)',fontsize=fontSize)
    # ax.set_ylabel('$\phi $(rad)',fontsize=fontSize)
    # plt.plot(taxis,phase,'b+',label='data')

    #check@1mV

    def fit_exponential(x,*p):
     return p[1]*np.exp(-x/p[0]+ p[3]) +p[2]#phimax-phimin)*np.exp(-x/p[0])+phimin  
 
    
    
    def fit_exponential2(x,*p):
        phimin=-0.012
        return p[1]*np.exp(-x/p[0]) +phimin#phimax-phimin)*np.exp(-x/p[0])+phimin    
    
    def fit_exponential_nodelay(x,*p):
        return p[1]*np.exp(-x/p[0]) +p[2]  
    
    
    phimax=np.max(phase)
    phimin=np.min(phase)
    popt,pcov = curve_fit(fit_exponential_nodelay,taxis,M[i],p0=[1e-6,phimax-phimin,phimin],maxfev=10000)    
    
    er=np.sqrt(np.diag(pcov))
    tempty_nodelay=popt[0]
    errortempty_nodelay=er[0]
    temptyfitarray_nodelay.append(tempty_nodelay)
    temptyerrorfitarray_nodelay.append(errortempty_nodelay)
    # plt.plot(taxis,fit_exponential_nodelay(taxis,*popt),'r',label='tempty='+str( round(tempty_nodelay*1000000,3)) +'$\pm$'+str( round(errortempty_nodelay*1000000,3))+'_us')#',phimin='+str(round(popt[2]*1000,3))+'mrad_phimax='+str(round((popt[1]+popt[2])*1000,3))+'mrad')
        
  
 
    # plt.legend(loc='upper right')
    # plt.show()
    # name='TP7__decayfitin02_amplitude_pp_'+str(ampliAWG()*11)+'mV_1000rep_B'+str(Bfield())+'T_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV'+str(VG5())+'mV'
    # # name='TP7__decayfitin11_amplitude_pp_'+str(ampliAWG()*11)+'mV_1000rep_B'+str(Bfield())+'T_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV'+str(VG5())+'mV'
    # try:
    #     plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
    #     np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',phase)
    # except FileNotFoundError:
    #     print('BUG, file not saved, name too long probably')
        
    # print('tau_empty_nodelay='+str(tempty_nodelay*1000)+'ms')
    # print('phimin_nodelay='+str(popt[2]*1000)+'mrad')
    # print('phimax_nodelay='+str( (popt[1]+popt[2])*1000)+'mrad')
    


# ydata=np.linspace(Binit,Bfinal,Bpoints)
# Brange='2to0T'

# #2dmap of signalvsfield
# fig, ax = plt.subplots()
# ax.set_xlabel('time(s)',fontsize=fontSize)
# ax.set_ylabel('$B$ (T)',fontsize=fontSize)
# name='TP7____timevsfield_amplitude_pp_'+str(ampliAWG()*11)+'mV_1000rep_B'+str(Bfield())+'T_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
# # name='TP7____timein11sfield_amplitude_pp_'+str(np.round(ampliAWG()*11,4))+'mV_1000rep_B'+str(Bfield())+'T_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV'

# def removeBackground(data,rangeMin=0, rangeMax=-1):
#     for i in range(len(data)):
#         data[i] = data[i] - data[i][rangeMin:rangeMax].mean() 
#     return(data)

# Z=removeBackground(M)


# plt.pcolor(taxis,ydata,Z,cmap='viridis')
# # plt.clim(vmin=None,vmax=0.3)
# plt.colorbar(label='phi(rad)')
# plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
# np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',Z)


tempty=np.multiply(temptyfitarray_nodelay,1e6)#convert in us
terror=np.multiply(temptyerrorfitarray_nodelay,1e6)
#extracted_decay_vsfield
fig, ax = plt.subplots()
ax.set_xlabel('time(s)',fontsize=fontSize)
ax.set_ylabel(r'$\tau$ ($\mu$s)',fontsize=fontSize)

name='TP7__decaytimevstime_amplitude_pp_'+str(ampliAWG()*11)+'mV_1000rep_B'+str(Bfield())+'T_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV'
# name='TP7____decaytimein11sfield_amplitude_pp_'+str(np.round(ampliAWG()*11,4))+'mV_1000rep_B'+str(Bfield())+'T_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV'
# plt.plot(ydata,tempty,'b+',label='data')
plt.errorbar(ydata,tempty,yerr=terror,fmt='b+')
# plt.clim(vmin=None,vmax=0.3)
# plt.colorbar(label='phi(rad)')
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',tempty)
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'errors.txt',terror)