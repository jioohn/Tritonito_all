# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 14:56:16 2021

@author: G-GRE-GRE050402
"""

# detuningPoint1 = [-877.5,-824] #G3,G2
# detuningPoint2 = [-880.5,-820.5]  
detuningPoint1 = [-842.62,-832.8]  
detuningPoint2 = [-842.64,-831.33] #G3,G2

detpoints=301
detuning = qc.combine(VG3, VG2, name = 'detuning', unit= 'points')
eps=np.sqrt((detuningPoint1[0]-detuningPoint2[0])**2 +(detuningPoint1[1]-detuningPoint2[1])**2) 
VG3comp(detuningPoint1[0])
VG2comp(detuningPoint1[1])

det=generateEpsilonAxis(detuningPoint1, detuningPoint2, detpoints)
eps=np.sqrt((detuningPoint1[0]-detuningPoint2[0])**2 +(detuningPoint1[1]-detuningPoint2[1])**2) 
epsilon=np.linspace(-eps/2,eps/2,detpoints)

name='detuningvsfield_TPc3_resetG4__G4'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G2'+str(VG4())+'mV_G5'+str(VG5())+'mV'

phases=[]
Barr=[]
G4pos=[]
G2pos=[]
G4min=[]
for j in range(0,21):
    Bfield_Hon(3-0.1*j)
    print(Bfield())
    time.sleep(2)
    Barr.append(Bfield())
    phasedet=[]
    VG3comp(det[0][0])
    VG2comp(det[0][1])
    VG4now=VG4()
    time.sleep(0.3)
    G4now=VG4()
    VG4onmin_ph2(G4now-1,G4now+1,201,0)
    G4now=VG4()
    # VG2onmin(G2now-1,G2now+1,201,0)
    # G2now=VG2()
    phimin=ph2()
    # G4min.append(ph2())
    G4pos.append(G4now)
    # G2pos.append(G2now)
    for i in range(0,len(det)):
        VG3comp(det[i][0])
        VG2comp(det[i][1])
        time.sleep(0.1)
        phasedet.append(ph2())
    G4min.append(phimin-ph2())
    print(G4min[j])
    phases.append(phasedet)    



  


f= plt.figure()       
plt.plot(Barr,G4pos)
# ax.x
plt.xlabel('B (T)')
# plt.ylabel('pulse amplitude_pp (mV)')
plt.ylabel('G4 position(mV)')
plt.savefig(folder2+'\\'+dayFolder+'\\G4pos_Bfrom2p5to0T.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'G4pos_Bfrom3to0T.txt',G4pos)  

f= plt.figure()       
plt.plot(Barr,G4min)
# ax.x
plt.xlabel('B (T)')
# plt.ylabel('pulse amplitude_pp (mV)')
plt.ylabel('G4 contrast(rad)')
plt.savefig(folder2+'\\'+dayFolder+'\\G4contrast_Bfrom3to0T.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'G4contrast_Bfrom3to0T.txt',G4min)  

Y= Barr
X = epsilon
Z1=phases
Z=np.reshape(Z1,(len(Y),len(X)))
def removeBackground(data,rangeMin=0, rangeMax=-1):
    for i in range(len(data)):
        data[i] = data[i] - data[i][rangeMin:rangeMax].mean() 
    return(data)

f = plt.figure()
plt.pcolor(X,Y,Z,cmap='viridis')
# plt.clim(vmin=None,vmax=0.3)
plt.colorbar(label='phi(deg)')
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
plt.colorbar(label='phi(deg)')
plt.xlabel('detuning (mV)')
# plt.ylabel('pulse amplitude_pp (mV)')
plt.ylabel('B (T)')

# name='detuningvsBfield_TP6'
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'_Bgsub.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'_Bgsub.txt',Z2)   
     
Bfield(Bfield_Hon()) 





###########fit epsilon vs phase
# detuningPoint1 = [-872.3,-767] 
# detuningPoint2 = [-872,-768.4]          # [G3(x), G2(y)]


detpoints=201
detuning = qc.combine(VG3, VG2, name = 'detuning', unit= 'points')
eps=np.sqrt((detuningPoint1[0]-detuningPoint2[0])**2 +(detuningPoint1[1]-detuningPoint2[1])**2) 
VG3comp(detuningPoint1[0])
VG2comp(detuningPoint1[1])

det=generateEpsilonAxis(detuningPoint1, detuningPoint2, detpoints)
eps=np.sqrt((detuningPoint1[0]-detuningPoint2[0])**2 +(detuningPoint1[1]-detuningPoint2[1])**2) 
epsilon=np.linspace(-eps/2,eps/2,detpoints)

name='detuningvsBfield_TP54_resetG4__G4'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'

phases=[]
Barr=[]
G4pos=[]
G2pos=[]
G4min=[]

phasedet=[]
for i in range(0,len(det)):
    VG3comp(det[i][0])
    VG2comp(det[i][1])
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
sigmaphi=0.05
# for k in range(0,len(data_set)):
#         if ((data_get[0][k]>=(philim-sigmaphi) and data_get[0][k]<=(philim+sigmaphi)) and kmax==0):
#             kmax=k
for k in range(0,len(epsilon)):
    if ((  datasmooth[k]>=(philim-sigmaphi) and   datasmooth[k]<=(philim+sigmaphi)) and kmax==0):
        kmax=k
        print('ok')

    
VG3comp(det[kmax][0])
VG2comp(det[kmax][1])

# xaxis=np.multiply(np.subtract(data_set,data_set[kmax]),1e-3)
xaxis=np.multiply(np.subtract(epsilon,epsilon[kmax]),1e-3)
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
name='0p44K_TPc2findalpha_tnegligible_TP52_1dscan-'+str(Bfield())+'_T_'
# fig.savefig(foldername2+'0.44K_Tonly_TP9_1dscan-'+str(Bfield())+'_T_ampliAWG'+str(ampliAWG())+'.png') 
# np.savetxt(foldername2+'0.44K_Tonly_TP9_1dscan-'+str(Bfield())+'_T_ampliAWG'+str(ampliAWG())+'.txt',datasmooth2)

plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',datasmooth2)