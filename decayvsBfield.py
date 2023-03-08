# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 11:54:57 2020

@author: G-GRE-GRE050402
"""
####decaytimevsfield
tc=0.10
acquisition_duration =300e-6  # length of time to record (s)
repetitions = 10            # number of repetitions for the averaging
points = 66  # number of points in the acquisition window (min=2)

#efftc=acquisition_duration/10
efftc=5e-6

# such that the effective Tc is 100ms 
# repetitions=tc/efftc/5

repetitions=500

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
trigger_setting02 = [['dataAcquisitionModule/triggernode', '/dev2010/demods/0/sample.TrigAWGTrig3'],  # trigger node is AWG trigger number 3 
#                   ['dataAcquisitionModule/type', 2],      
                   ['dataAcquisitionModule/type', 6],                                          # this setting is related to the AWG trigger
                   ['dataAcquisitionModule/edge', 1],                                               # trigger on the positive edge. 1 = positive, 2=negative
                   ['dataAcquisitionModule/count', 1],                                              # number of trigger events to count
                   ['dataAcquisitionModule/holdoff/time', 0],                                       # hold off time
                   ['dataAcquisitionModule/holdoff/count', 0],                                      # hold off count
                   ##careful
                   ['dataAcquisitionModule/delay', 295e-6], #0                                       # trigger delay (s)
                   #7
                   ['dataAcquisitionModule/endless', 0]]                                            # endless disabled = 0
trigger_setting11 = [['dataAcquisitionModule/triggernode', '/dev2010/demods/0/sample.TrigAWGTrig3'],  # trigger node is AWG trigger number 3 
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
phase_trig.setSettings(trigger_setting02, grid_setting)

phase_trig11= SpecialParameters.Pulsed_readout_G1(ziUhf, repetitions, returnOnePoint=False)
phase_trig11.setSettings(trigger_setting11, grid_setting)


################
G4val=[]
G1val=[]
Binit=2.5
Bfinal=+0
Bpoints=101
dB=(Bfinal-Binit)/(Bpoints-1)
# M=np.zeros((Bpoints,points)) #y,x
M=[]
ydata=np.linspace(Binit,Bfinal,Bpoints)
tempty=[]


temptyfitarray_nodelay=[]
temptyerrorfitarray_nodelay=[]

alpha_array=[]

error_alpha_array=[]

# tunnelarray=[]
# tunnelarrayerr=[]
T=0.44

taxis=np.linspace(0,acquisition_duration,points)
M2=[]
tempty11_nodelay=[]
errortempty11_nodelay=[]
temptyfitarray11_nodelay=[]
temptyerrorfitarray11_nodelay=[]

for i in range(0,Bpoints):
    print('field='+str(Bfield()))
#    Bfield(Binit+Bfinal/(Bpoints-1)*i)
    Bfield_Hon(Binit+dB*i)
    if i==(Bpoints-1):
        Bfield(Bfinal)
    # time.sleep(30)
#    tguessarray2.append(tguess2)
    ##turnoff pulsesbefore
    # if i==0:
    continuous_acquisition()
    ziUhf.daq.setInt('/dev2010/sigouts/1/on', 0)

    # G1now=VG1()
    # VG1onmin(G1now-0.5,G1now+0.5,101,0)
    # G1now=VG1()
    # while VG4()<-916:
    VG3comp(-932.45)
    # sensor_on_interdot_sweepG4comp(-779,-782,201,1)
    #####################check sensorsignal
    a,b,c=sweep1D(VG4comp,-779,-782,201,0.02,ph1)
    xlabel='$V_{G4}$(mV)'
    ylabel='$\phi_{G1}$(deg)'
    data_set,data_get,parameters_name=Extract_data(a)
    datasmooth=scipy.signal.savgol_filter(np.ravel(data_get[0]),11, 3)
    phimin=np.min(datasmooth)
    phimax=np.max(datasmooth)
    argmin=np.argmin(datasmooth)
    kmin=0
    kmax=0
    philim=phimin+(phimax-phimin)/2
    T=0.44
    sigmaphi=0.05
    for k in range(0,len(data_set)):
            if ((data_get[0][k]>=(philim-sigmaphi) and data_get[0][k]<=(philim+sigmaphi)) and kmax==0):
                kmax=k

    
    VG4comp(data_set[kmax][0])
    
    xaxis=np.multiply(np.subtract(data_set,data_set[kmax]),1e-3)
    datasmooth2=np.subtract(datasmooth,phimin)
    
    xaxis2=np.array(xaxis,dtype=float)
    datasmooth2=np.array(datasmooth2,dtype=float)
    
    
    xaxis2=np.reshape(xaxis2,201)
    datasmooth2=np.reshape(datasmooth2,201)
    
    fig, ax = plt.subplots()
    ax.set_xlabel('$\epsilon$ (V)',fontsize=fontSize)
    ax.set_ylabel('$\phi $(rad)',fontsize=fontSize)
    
    plt.title('Fit at T='+str(T)+'K')
    plt.plot(xaxis,datasmooth2,'b+',label='data@'+str(T)+'K')#mV on x  
    plt.legend(loc='upper left')
    plt.show()
    
    
    
    alpha=0.55
    const=phimin
    offset=phimin+(phimax-phimin)
    
      
    popt,pcov = curve_fit(interdotfit_chargesensor,xaxis2,datasmooth2,p0=[alpha,0,1],maxfev=10000) 
    plt.plot(xaxis2,interdotfit_chargesensor(xaxis2,*popt))    
    
    
    alpha=popt[0] 
    
    er=np.sqrt(np.diag(pcov))
    erroralpha=er[0]
    # errortunnel=er[3]
    # print('Teff='+str(Teff))
    # Tarray.append(Teff)
    # errorTarray.append(errortemp)
    
    # tunnelarray.append(tunnel)
    # tunnelarrayerr.append(errortunnel)
    
    # errortunnel=errortunnel/h*10e-9#conv to Ghz
    plt.plot(xaxis,interdotfit_chargesensor(xaxis2,*popt),'r',label='alpha='+str( round(alpha,2)) +'$\pm$'+str( round(erroralpha,2))+'_eV/V')#,t='+str( round(tunnel,3))+'$\pm$'+str(round(errortunnel,3))+'_GHz, alpha='+str(alpha))
    #    plt.plot(xaxis,interdotfit_chargesensor(xaxis,*popt),'r',label='Teff='+str( round(Teff,2)) +'$\pm$'+str( round(errortemp,2))+'_K,t='+str( round(tunnel,3))+'$\pm$'+str(round(errortunnel,3))+'_GHz, alpha='+str(alpha))
    plt.legend(loc='upper left')
    plt.show()
    name='0p44K_findalpha_tnegligible_TP9_1dscan-'+str(Bfield())+'_T_'
    # fig.savefig(foldername2+'0.44K_Tonly_TP9_1dscan-'+str(Bfield())+'_T_ampliAWG'+str(ampliAWG())+'.png') 
    # np.savetxt(foldername2+'0.44K_Tonly_TP9_1dscan-'+str(Bfield())+'_T_ampliAWG'+str(ampliAWG())+'.txt',datasmooth2)
    
    # plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
    # np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',datasmooth2)
    
    
    
    
    
    alpha_array.append(alpha)

    error_alpha_array.append(erroralpha)
    
    
    
    
    
    
    
    #########################
    G4val.append(VG4())
    G1val.append(VG1())
    ampliAWG(0.1)
    # continuous_acquisition()
    # VG4comp(-799)
    # VG3comp(-936.7)
    # ziUhf.daq.setInt('/dev2010/sigouts/1/on', 0)
    # sensor_on_interdot_sweepG4comp(-802,-797,201,0)
    # G4val.append(VG4())
    trigger_mode()
    ziUhf.daq.setInt('/dev2010/sigouts/1/on', 1)
    ziUhf.daq.setDouble('/dev2010/demods/0/rate', 200e3)
    ziUhf.daq.setDouble('/dev2010/demods/0/timeconstant', 5e-6)
    
    phase=phase_trig()[0]
    M.append(phase)
    
    
    fig, ax = plt.subplots()
    ax.set_xlabel('time(s)',fontsize=fontSize)
    ax.set_ylabel('$\phi $(rad)',fontsize=fontSize)
    plt.plot(taxis,phase,'b+',label='data')

    #check@1mV

    
    def fit_exponential_nodelay(x,*p):
        return p[1]*np.exp(-x/p[0]) +p[2]  
    
    
    phimax=np.max(phase)
    phimin=np.min(phase)
    popt,pcov = curve_fit(fit_exponential_nodelay,taxis,M[i],p0=[100e-6,phimax-phimin,phimin],maxfev=10000)    
    
    er=np.sqrt(np.diag(pcov))
    tempty_nodelay=popt[0]
    errortempty_nodelay=er[0]
    temptyfitarray_nodelay.append(tempty_nodelay)
    temptyerrorfitarray_nodelay.append(errortempty_nodelay)
    plt.plot(taxis,fit_exponential_nodelay(taxis,*popt),'r',label='tempty='+str( round(tempty_nodelay*1000000,3)) +'$\pm$'+str( round(errortempty_nodelay*1000000,3))+'_us')#',phimin='+str(round(popt[2]*1000,3))+'mrad_phimax='+str(round((popt[1]+popt[2])*1000,3))+'mrad')
        
  
 
    plt.legend(loc='upper right')
    plt.show()
    name='TP52_decayfitin02_amplitude_pp_'+str(ampliAWG()*11)+'mV_1000rep_B'+str(Bfield())+'T_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV'+str(VG5())+'mV'
    # name='TP7__decayfitin11_amplitude_pp_'+str(ampliAWG()*11)+'mV_1000rep_B'+str(Bfield())+'T_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV'+str(VG5())+'mV'
    try:
        plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
        np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',phase)
    except FileNotFoundError:
        print('BUG, file not saved, name too long probably')
        
    print('tau_empty_nodelay='+str(tempty_nodelay*1000)+'ms')
    print('phimin_nodelay='+str(popt[2]*1000)+'mrad')
    print('phimax_nodelay='+str( (popt[1]+popt[2])*1000)+'mrad')
    
    #either define 2 phase_trig or reverse pulse amplitude
    # ampliAWG(-0.055)
    
    # continuous_acquisition()
    # VG4comp(-799)
    # VG3comp(-936.7)
    # ziUhf.daq.setInt('/dev2010/sigouts/1/on', 0)
    # sensor_on_interdot_sweepG4comp(-802,-797,201,0)
    # G4val.append(VG4())
    trigger_mode()
    ziUhf.daq.setInt('/dev2010/sigouts/1/on', 1)
    ziUhf.daq.setDouble('/dev2010/demods/0/rate', 200e3)
    ziUhf.daq.setDouble('/dev2010/demods/0/timeconstant', 5e-6)
    
    phase=phase_trig11()[0]
    M2.append(phase)
    
    
    fig, ax = plt.subplots()
    ax.set_xlabel('time(s)',fontsize=fontSize)
    ax.set_ylabel('$\phi $(rad)',fontsize=fontSize)
    plt.plot(taxis,phase,'b+',label='data')

    #check@1mV

    
    def fit_exponential_nodelay(x,*p):
        return p[1]*np.exp(-x/p[0]) +p[2]  
    
    
    phimax=np.max(phase)
    phimin=np.min(phase)
    popt,pcov = curve_fit(fit_exponential_nodelay,taxis,M2[i],p0=[10e-6,phimax-phimin,phimin],maxfev=10000)    
    
    tempty11_nodelay=popt[0]
    errortempty11_nodelay=er[0]
    temptyfitarray11_nodelay.append(tempty11_nodelay)
    temptyerrorfitarray11_nodelay.append(errortempty11_nodelay)
    plt.plot(taxis,fit_exponential_nodelay(taxis,*popt),'r',label='tempty='+str( round(tempty11_nodelay*1000000,3)) +'$\pm$'+str( round(errortempty11_nodelay*1000000,3))+'_us')#',phimin='+str(round(popt[2]*1000,3))+'mrad_phimax='+str(round((popt[1]+popt[2])*1000,3))+'mrad')
        
  
 
    plt.legend(loc='upper right')
    plt.show()
    name='TPxx_decayfitin11_amplitude_pp_'+str(ampliAWG()*11)+'mV_500rep_B'+str(Bfield())+'T_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV'+str(VG5())+'mV'

ydata=np.linspace(Binit,Bfinal,Bpoints)
# Brange='2to0T'

#2dmap of signalvsfield
fig, ax = plt.subplots()
ax.set_xlabel('time(s)',fontsize=fontSize)
ax.set_ylabel('$B$ (T)',fontsize=fontSize)
name='TPxx__timevsfield_amplitude_pp_'+str(ampliAWG()*11)+'mV_'+str(repetitions)+'_B'+str(Bfield())+'T_G1'+str(VG1())+'_G2'+str(VG2())+'_G3'+str(VG3())+'_G4'+str(VG4())+'mV_G5'+str(VG5())
# name='TP7____timein11sfield_amplitude_pp_'+str(np.round(ampliAWG()*11,4))+'mV_1000rep_B'+str(Bfield())+'T_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV'

def removeBackground(data,rangeMin=0, rangeMax=-1):
    for i in range(len(data)):
        data[i] = data[i] - data[i][rangeMin:rangeMax].mean() 
    return(data)

Z=removeBackground(M)


plt.pcolor(taxis,ydata,Z,cmap='viridis')
# plt.clim(vmin=None,vmax=0.3)
plt.colorbar(label='phi(rad)')
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',Z)
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'raw.txt',M)
##################

fig, ax = plt.subplots()
ax.set_xlabel('time(s)',fontsize=fontSize)
ax.set_ylabel('$B$ (T)',fontsize=fontSize)
name='TPxx__timevsfield_in11_amplitude_pp_'+str(ampliAWG()*11)+'mV_'+str(repetitions)+'rep_B'+str(Bfield())+'T_G1'+str(VG1())+'_G2'+str(VG2())+'_G3'+str(VG3())+'_G4'+str(VG4())+'G5'+str(VG5())
# name='TP7____timein11sfield_amplitude_pp_'+str(np.round(ampliAWG()*11,4))+'mV_1000rep_B'+str(Bfield())+'T_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV'


Z2=removeBackground(M2)


plt.pcolor(taxis,ydata,Z2,cmap='viridis')
# plt.clim(vmin=None,vmax=0.3)
plt.colorbar(label='phi(rad)')
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',Z2)
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'raw.txt',M2)

##############
tempty=np.multiply(temptyfitarray_nodelay,1e6)#convert in us
terror=np.multiply(temptyerrorfitarray_nodelay,1e6)
#extracted_decay_vsfield

#########################
fig, ax = plt.subplots()
ax.set_xlabel('B(T)',fontsize=fontSize)
ax.set_ylabel(r'$\tau_{02}$ ($\mu$s)',fontsize=fontSize)

name='TPxx__decaytimevsfield_amplitude_pp_'+str(ampliAWG()*11)+'mV_'+str(repetitions)+'rep_B'+str(Bfield())+'T_G1'+str(VG1())+'_G2'+str(VG2())+'_G3'+str(VG3())+'_G4'+str(VG4())+'G5'+str(VG5())
# name='TP7____decaytimein11sfield_amplitude_pp_'+str(np.round(ampliAWG()*11,4))+'mV_1000rep_B'+str(Bfield())+'T_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV'
# plt.plot(ydata,tempty,'b+',label='data')
plt.errorbar(ydata,tempty,yerr=terror,fmt='b+')
# plt.clim(vmin=None,vmax=0.3)
# plt.colorbar(label='phi(rad)')
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',tempty)
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'errors.txt',terror)
##########################
##############
tempty11=np.multiply(temptyfitarray11_nodelay,1e6)#convert in us
terror11=np.multiply(temptyerrorfitarray11_nodelay,1e6)
#extracted_decay_vsfield

#########################
fig, ax = plt.subplots()
ax.set_xlabel('B(T)',fontsize=fontSize)
ax.set_ylabel(r'$\tau_{11}$ ($\mu$s)',fontsize=fontSize)

name='TP52__decaytime11vsfield_amplitude_pp_'+str(ampliAWG()*11)+'mV_'+str(repetitions)+'rep_B'+str(Bfield())+'T_G1'+str(VG1())+'_G2'+str(VG2())+'_G3'+str(VG3())+'G4'+str(VG4())+'G5'+str(VG5())
# name='TP7____decaytimein11sfield_amplitude_pp_'+str(np.round(ampliAWG()*11,4))+'mV_1000rep_B'+str(Bfield())+'T_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV'
# plt.plot(ydata,tempty,'b+',label='data')
plt.errorbar(ydata,tempty11,yerr=terror11,fmt='b+')
# plt.ylim(5,15)
# plt.clim(vmin=None,vmax=0.3)
# plt.colorbar(label='phi(rad)')
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',tempty11)
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'errors.txt',terror11)
##############
# tempty11=np.multiply(temptyfitarray_nodelay11,1e6)#convert in us
# terror11=np.multiply(temptyerrorfitarray_nodelay11,1e6)
# #extracted_decay_vsfield












fig, ax = plt.subplots()
ax.set_xlabel('B(T)',fontsize=fontSize)
ax.set_ylabel('alpha(eV/V)',fontsize=fontSize)

name='TPxx_alphavsfield_amplitude_pp_'+str(ampliAWG()*11)+'mV_500rep_B'+str(Bfield())+'T_G1'+str(VG1())+'_G2'+str(VG2())+'_G3'+str(VG3())+'G4'+str(VG4())+'G5'+str(VG5())
# name='TP7____decaytimein11sfield_amplitude_pp_'+str(np.round(ampliAWG()*11,4))+'mV_1000rep_B'+str(Bfield())+'T_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV'
# plt.plot(ydata,tempty,'b+',label='data')
plt.errorbar(ydata,alpha_array,yerr=error_alpha_array,fmt='b+')
# plt.clim(vmin=None,vmax=0.3)
# plt.colorbar(label='phi(rad)')
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',alpha_array)
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'errors.txt',error_alpha_array)












######

fig, ax = plt.subplots()
ax.set_xlabel('B(T)',fontsize=fontSize)
ax.set_ylabel('G4(mV)',fontsize=fontSize)

name='TP52__G4vsfield_amplitude_pp_'+str(ampliAWG()*11)+'mV_500rep_B'+str(Bfield())+'T_G1'+str(VG1())+'_G2'+str(VG2())+'_G3'+str(VG3())+'G4'+str(VG4())+'G5'+str(VG5())
# name='TP7____decaytimein11sfield_amplitude_pp_'+str(np.round(ampliAWG()*11,4))+'mV_1000rep_B'+str(Bfield())+'T_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV'
plt.plot(ydata,G4val)
# plt.errorbar(ydata,tempty,yerr=terror,fmt='b+')
# plt.clim(vmin=None,vmax=0.3)
# plt.colorbar(label='phi(rad)')
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'G1.txt',G4val)

###################
fig, ax = plt.subplots()
ax.set_xlabel('B(T)',fontsize=fontSize)
ax.set_ylabel('G1(mV)',fontsize=fontSize)

name='TP52__G1vsfield_amplitude_pp_'+str(ampliAWG()*11)+'mV_500rep_B'+str(Bfield())+'T_G1'+str(VG1())+'_G2'+str(VG2())+'_G3'+str(VG3())+'G4'+str(VG4())+'G5'+str(VG5())
# name='TP7____decaytimein11sfield_amplitude_pp_'+str(np.round(ampliAWG()*11,4))+'mV_1000rep_B'+str(Bfield())+'T_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV'
plt.plot(ydata,G1val)
# plt.errorbar(ydata,tempty,yerr=terror,fmt='b+')
# plt.clim(vmin=None,vmax=0.3)
# plt.colorbar(label='phi(rad)')
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',G1val)
Bfield(Bfinal)
