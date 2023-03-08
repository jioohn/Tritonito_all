# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 17:11:18 2020

@author: G-GRE-GRE050402
"""



# name='detuningvsBfield_TP62_reset_G1_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV__G6'+str(VG6())+'mV'

###
# detuningPoint1 = [-871.5,-784.7] 
# detuningPoint2 = [-871.7,-783.4]          # [G3(x), G4(y)]
# detuningPoint1 = [-835.6,-834.4] #TPA
# detuningPoint2 = [-836.4,-833.2]  

# detuningPoint1 = [-837.2,-816.3] 
# detuningPoint2 = [-836.1,-817.3]  #TPB

############"
continuous_acquisition()
continuous_acquisition_ch2()
########################
# detuningPoint1 = [-847.6,-832.4] 
# detuningPoint2 = [-848.2,-831]  #TPC
detuningPoint1 = [-899.5,-833]  #TPC #G3,G4
detuningPoint2 = [-898,-833.6] 



# detuningPoint1 = [-850,-828]  #TPC #G3,G4
# detuningPoint2 = [-846,-833] 
# VG3comp(detuningPoint1[0])
# VG4comp(detuningPoint1[1])
# DeltaG4G3=(detuningPoint1[0]-detuningPoint2[0])/(detuningPoint1[1]-detuningPoint2[1])


# G4detuning=  SpecialParameters.CompensateG4(VG4,VG3,DeltaG4G3)



detpoints=301
detuning = qc.combine(VG3, VG4, name = 'detuning', unit= 'points')
eps=np.sqrt((detuningPoint1[0]-detuningPoint2[0])**2 +(detuningPoint1[1]-detuningPoint2[1])**2) 
VG3comp(detuningPoint1[0])
VG4comp(detuningPoint1[1])

det=generateEpsilonAxis(detuningPoint1, detuningPoint2, detpoints)
eps=np.sqrt((detuningPoint1[0]-detuningPoint2[0])**2 +(detuningPoint1[1]-detuningPoint2[1])**2) 
epsilon=np.linspace(-eps/2,eps/2,detpoints)
VG3comp(det[0][0])
VG4comp(det[0][1])
tag='TPC_nocomp_'

phaseS=[]
phaseD=[]
amplitudeS=[]
amplitudeD=[]
Barr=[]
G1pos=[]
G2pos=[]
G1min=[]
for j in range(0,41):
    Bfield_Hon(2-0.05*j)
    print(Bfield_Hon())
    time.sleep(2)
    Barr.append(Bfield())
    phiD=[]
    phiS=[]
    amps=[]
    ampd=[]
    
    # VG3comp(det[0][0])
    # VG4comp(det[0][1])
    VG3(det[0][0])
    VG4(det[0][1])
    
    VG1now=VG1()
    time.sleep(0.5)
    G2now=VG2()

    # VG2onmin_phS(G2now-1,G2now+1,201,0)
    
    G2now=VG2()
    phimin=ph1()

    G2pos.append(G2now)
    for i in range(0,len(det)):
    #     VG3comp(det[i][0])
    #     VG4comp(det[i][1])
        VG3(det[i][0])
        VG4(det[i][1])
        time.sleep(0.02)
        phiS.append(ph2())
        phiD.append(ph1())
        # ampd.append(A1())
        # amps.append(A2())
    # G1min.append(phimin-ph1())
    phaseS.append(phiS)    
    phaseD.append(phiD)  
    # amplitudeS.append(amps)
    # amplitudeD.append(ampd)

#####CHECK
# f= plt.figure()       
# plt.plot(epsilon,phiS)

# plt.ylabel('$\phi_S(deg)$ ')
# plt.xlabel('$ \epsilon (mV)$')

# plt.savefig(folder2+'\\'+dayFolder+'\\1d_scandetuning.png')


#######

# now=datetime.datetime.now()
# dayFolder=datetime.date.isoformat(now)
# f= plt.figure()       
# plt.plot(Barr,G2pos)
# # ax.x
# plt.xlabel('B (T)')
# # plt.ylabel('pulse amplitude_pp (mV)')
# plt.ylabel('G2 position(mV)')
# plt.savefig(folder2+'\\'+dayFolder+'\\G2pos_Bfrom2to0T.png')
# np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'G2pos_Bfrom2to0T.txt',G1pos)  


# f= plt.figure()       
# plt.plot(Barr,G1pos)
# # ax.x
# plt.xlabel('B (T)')
# # plt.ylabel('pulse amplitude_pp (mV)')
# plt.ylabel('G1 position(mV)')
# plt.savefig(folder2+'\\'+dayFolder+'\\G1pos_Bfrom3to0T.png')
# np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'G1pos_Bfrom3to0T.txt',G1pos)  

# f= plt.figure()       
# plt.plot(Barr,G1min)
# # ax.x
# plt.xlabel('B (T)')
# # plt.ylabel('pulse amplitude_pp (mV)')
# plt.ylabel('G1 contrast(rad)')
# plt.savefig(folder2+'\\'+dayFolder+'\\G1minminusmax_Bfrom3o0T.png')
# np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'G1contrast_Bfrom3to0T.txt',G1min)  
name=tag+'phS___detvsField_G1__G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
Y= Barr
X = epsilon
Z1=phaseS
Z=np.reshape(Z1,(len(Y),len(X)))
def removeBackground(data,rangeMin=0, rangeMax=-1):
    for i in range(len(data)):
        data[i] = data[i] - data[i][rangeMin:rangeMax].mean() 
    return(data)

f = plt.figure()
plt.pcolor(X,Y,Z,cmap='viridis')
# plt.clim(vmin=None,vmax=0.3)
plt.colorbar(label='$\phi_S(deg)$')
plt.xlabel('detuning (mV)')
# plt.ylabel('pulse amplitude_pp (mV)')
plt.ylabel('B (T)')
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',Z)  
# 



Z2=removeBackground(Z)

f = plt.figure()
plt.pcolor(X,Y,Z2,cmap='viridis')
# plt.clim(vmin=None,vmax=0.3)
plt.colorbar(label='$\phi_S(deg)$')
plt.xlabel('detuning (mV)')
# plt.ylabel('pulse amplitude_pp (mV)')
plt.ylabel('B (T)')

# name='detuningvsBfield_TP6'
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'_Bgsub.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'_Bgsub.txt',Z2)   
###phD
name=tag+'phid_detvsField_G1____G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV__G6'+str(VG6())+'mV'
Y= Barr
X = epsilon
Z1=phaseD
Z=np.reshape(Z1,(len(Y),len(X)))
def removeBackground(data,rangeMin=0, rangeMax=-1):
    for i in range(len(data)):
        data[i] = data[i] - data[i][rangeMin:rangeMax].mean() 
    return(data)

f = plt.figure()
plt.pcolor(X,Y,Z,cmap='viridis')
# plt.clim(vmin=None,vmax=0.3)
plt.colorbar(label='$\phi_D(deg)$')
plt.xlabel('detuning (mV)')
# plt.ylabel('pulse amplitude_pp (mV)')
plt.ylabel('B (T)')
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',Z)



Z2=removeBackground(Z)

f = plt.figure()
plt.pcolor(X,Y,Z2,cmap='viridis')
# plt.clim(vmin=None,vmax=0.3)
plt.colorbar(label='$\phi_D(deg)$')
plt.xlabel('detuning (mV)')
# plt.ylabel('pulse amplitude_pp (mV)')
plt.ylabel('B (T)')

# name='detuningvsBfield_TP6'
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'_Bgsub.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'_Bgsub.txt',Z2) 


Bfield(Bfield_Hon()) 
    





####AMPS plots

name=tag+'As_detvsField_G1____G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV__G6'+str(VG6())+'mV'
Y= Barr
X = epsilon
Z1=amplitudeS
Z=np.reshape(Z1,(len(Y),len(X)))
def removeBackground(data,rangeMin=0, rangeMax=-1):
    for i in range(len(data)):
        data[i] = data[i] - data[i][rangeMin:rangeMax].mean() 
    return(data)

f = plt.figure()
plt.pcolor(X,Y,Z,cmap='viridis')
# plt.clim(vmin=None,vmax=0.3)
plt.colorbar(label='$A_S(V)$')
plt.xlabel('detuning (mV)')
# plt.ylabel('pulse amplitude_pp (mV)')
plt.ylabel('B (T)')
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',Z)



Z2=removeBackground(Z)

f = plt.figure()
plt.pcolor(X,Y,Z2,cmap='viridis')
# plt.clim(vmin=None,vmax=0.3)
plt.colorbar(label='$A_S(V)$')
plt.xlabel('detuning (mV)')
# plt.ylabel('pulse amplitude_pp (mV)')
plt.ylabel('B (T)')

# name='detuningvsBfield_TP6'
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'_Bgsub.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'_Bgsub.txt',Z2) 


name=tag+'Ad_detvsField_G1____G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV__G6'+str(VG6())+'mV'
Y= Barr
X = epsilon
Z1=amplitudeD
Z=np.reshape(Z1,(len(Y),len(X)))
def removeBackground(data,rangeMin=0, rangeMax=-1):
    for i in range(len(data)):
        data[i] = data[i] - data[i][rangeMin:rangeMax].mean() 
    return(data)

f = plt.figure()
plt.pcolor(X,Y,Z,cmap='viridis')
# plt.clim(vmin=None,vmax=0.3)
plt.colorbar(label='$A_D(V)$')
plt.xlabel('detuning (mV)')
# plt.ylabel('pulse amplitude_pp (mV)')
plt.ylabel('B (T)')
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',Z)



Z2=removeBackground(Z)

f = plt.figure()
plt.pcolor(X,Y,Z2,cmap='viridis')
# plt.clim(vmin=None,vmax=0.3)
plt.colorbar(label='$A_D(V)$')
plt.xlabel('detuning (mV)')
# plt.ylabel('pulse amplitude_pp (mV)')
plt.ylabel('B (T)')

# name='detuningvsBfield_TP6'
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'_Bgsub.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'_Bgsub.txt',Z2) 




#######################""
###########fit epsilon vs phase
# detuningPoint1 = [-872.3,-767] 
# detuningPoint2 = [-872,-768.4]          # [G3(x), G4(y)]

# detuningPoint1 = [-847.6,-830.2]  #TPC
# detuningPoint2 = [-846.4,-831.7] 

detpoints=201
detuning = qc.combine(VG3, VG4, name = 'detuning', unit= 'points')
eps=np.sqrt((detuningPoint1[0]-detuningPoint2[0])**2 +(detuningPoint1[1]-detuningPoint2[1])**2) 
VG3comp(detuningPoint1[0])
VG4comp(detuningPoint1[1])

det=generateEpsilonAxis(detuningPoint1, detuningPoint2, detpoints)
eps=np.sqrt((detuningPoint1[0]-detuningPoint2[0])**2 +(detuningPoint1[1]-detuningPoint2[1])**2) 
epsilon=np.linspace(-eps/2,eps/2,detpoints)

# name='comp_detuningvsBfield_TP54_resetG1__G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV__G6'+str(VG6())+'mV'
tag='TPC_'
phases=[]
Barr=[]
G1pos=[]
G2pos=[]
G1min=[]

phasedet=[]
for i in range(0,len(det)):
    # VG3comp(det[i][0])
    # VG4comp(det[i][1])
    VG3(det[i][0])
    VG4(det[i][1])
    time.sleep(0.04)
    phasedet.append(ph2())
    
datasmooth=scipy.signal.savgol_filter(np.ravel(phasedet),11, 3)
phimin=np.min(datasmooth)
phimax=np.max(datasmooth)
argmin=np.argmin(datasmooth)
kmin=0
kmax=0
philim=phimin+(phimax-phimin)/2
T=0.44
sigmaphi=0.005
# for k in range(0,len(data_set)):
#         if ((data_get[0][k]>=(philim-sigmaphi) and data_get[0][k]<=(philim+sigmaphi)) and kmax==0):
#             kmax=k
for k in range(0,len(epsilon)):
    if ((  datasmooth[k]>=(philim-sigmaphi) and   datasmooth[k]<=(philim+sigmaphi)) and kmax==0):
        kmax=k
        print('ok')

    
VG3comp(det[kmax][0])
VG4comp(det[kmax][1])

# xaxis=np.multiply(np.subtract(data_set,data_set[kmax]),1e-3)
xaxis=np.multiply(np.subtract(epsilon,epsilon[kmax]),1e-3)
datasmooth2=np.subtract(datasmooth,phimin)

xaxis2=np.array(xaxis,dtype=float)
datasmooth2=np.array(datasmooth2,dtype=float)


xaxis2=np.reshape(xaxis2,201)
datasmooth2=np.reshape(datasmooth2,201)

fig, ax = plt.subplots()
ax.set_xlabel('$\epsilon$ (V)',fontsize=fontSize)
ax.set_ylabel('$\phi_S $(rad)',fontsize=fontSize)

plt.title('Fit at T='+str(T)+'K')
plt.plot(xaxis,datasmooth2,'b+',label='data@'+str(T)+'K')#mV on x  
plt.legend(loc='upper right')
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
name=tag+str(dataid)+'0p438K_TPC_findalphadetunig_tnegligible_1dscan-'+str(Bfield())+'_T_'
# fig.savefig(foldername2+'0.44K_Tonly_TP9_1dscan-'+str(Bfield())+'_T_ampliAWG'+str(ampliAWG())+'.png') 
# np.savetxt(foldername2+'0.44K_Tonly_TP9_1dscan-'+str(Bfield())+'_T_ampliAWG'+str(ampliAWG())+'.txt',datasmooth2)

plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',datasmooth2)
