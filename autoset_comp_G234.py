# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 23:16:20 2020

@author: G-GRE-GRE050402
"""


rampVG1(-1730)
rampVG2(-1610)
rampVG5(-1680)
rampVG6(-1840)

initG4=-900
initG3=-900

VG1now=VG1()
VG2now=VG2()
Vds=-0.2

bias(Vds)

rampVG2(VG2now)
rampVG4(initG4)
rampVG3(initG3)

VG1now=VG1()
VG2now=VG2()
VG3now=VG3()
VG4now=VG4()
VG5now=VG5()

VG1onmin_phS(VG1now-10,VG1now+10,1001,1)

# VG1onmin_phS(VG1now-4,VG1now+4,801,1)

time.sleep(1)
VG2onmin_phS(VG2now-4,VG2now+4,801,1)







smooth=1


now=datetime.datetime.now()
dayFolder= datetime.date.isoformat(now)
try:
        os.makedirs(folder2+'\\'+dayFolder)
except IOError:
        donothing=1

rampVG3(initG3)
rampVG4(initG4)
DeltaVG4=3#mV
DeltaVG3=3#mV

initVG2=VG2now-3
finalVG2=VG2now+3


Npoints=501


a,dataid,c=sweep1D(VG2,initVG2,finalVG2,Npoints,0.02,ph2)
data_set,data_get, parameters_name =Extract_data(a)     

phimin=np.min(data_get[0])
argmin=np.argmin(data_get[0])
if smooth==1:
    datasmooth=scipy.signal.savgol_filter(np.ravel(data_get[0]),11, 3)
    phimin=np.min(datasmooth)
    argmin=np.argmin(datasmooth)
# if(phimin>-0.005):
#     print('ERROR!!! peak not found or too small')
# for k in range(0,len(data_get[0])):
#     #typicalFWHM is <1.5mV
#     #take 1 mV distance from min to avoid undesiderd peaks
#     if(data_get[k]<phimin/2 and np.abs(argmin-k)<20):
#         kmax=k
#         if kmin==0:
#             kmin=k

VBmin=data_set[argmin]        
dVG2=0

#############################################
f = plt.figure()
if smooth==1:
    plt.plot(data_set,datasmooth,label='VG3='+str(VG3())+'mV, VG4='+str(VG4())+'mV')
else:
    plt.plot(data_set,data_get[0],label='VG3='+str(VG3())+'mV, VG4='+str(VG4())+'mV')


#############################################
###move G3 and caluculate relative displacement of G2 peak
rampVG3(VG3()+DeltaVG3)

a,dataid,c=sweep1D(VG2,initVG2,finalVG2,Npoints,0.02,ph2)
data_set,data_get, parameters_name =Extract_data(a)     



phimin=np.min(data_get[0])
argmin=np.argmin(data_get[0])
if smooth==1:
    datasmooth=scipy.signal.savgol_filter(np.ravel(data_get[0]),11, 3)
    phimin=np.min(datasmooth)
    argmin=np.argmin(datasmooth)

if smooth==1:
    plt.plot(data_set,datasmooth,label='VG3='+str(VG3())+'mV, VG4='+str(VG4())+'mV')
else:
    plt.plot(data_set,data_get[0],label='VG3='+str(VG3())+'mV, VG4='+str(VG4())+'mV')
kmin=0
kmax=0
# if(phimin>-0.005):
#     print('ERROR!!! peak not found or too small')
# for k in range(0,len(data_get[0])):
#     #typicalFWHM is <1.5mV
#     #take 1 mV distance from min to avoid undesiderd peaks
#     if(data_get[k]<phimin/2 and np.abs(argmin-k)<20):
#         kmax=k
#         if kmin==0:
#             kmin=k
VBold=VBmin
VBmin=data_set[argmin]        
dVB_G3=np.subtract(VBmin,VBold)


###################################
#############################################
###move G4 and caluculate relative displacement of G2 peak
rampVG4(VG4()+DeltaVG4)
time.sleep(5)
a,dataid,c=sweep1D(VG2,initVG2,finalVG2,Npoints,0.02,ph2)
data_set,data_get, parameters_name =Extract_data(a)     






phimin=np.min(data_get[0])
argmin=np.argmin(data_get[0])
if smooth==1:
    datasmooth=scipy.signal.savgol_filter(np.ravel(data_get[0]),11, 3)
    phimin=np.min(datasmooth)
    argmin=np.argmin(datasmooth)
    

if smooth==1:
    plt.plot(data_set,datasmooth,label='VG3='+str(VG3())+'mV, VG4='+str(VG4())+'mV')
else:
    plt.plot(data_set,data_get[0],label='VG3='+str(VG3())+'mV, VG4='+str(VG4())+'mV')
    
kmin=0
kmax=0
# if(phimin>-0.005):
#     print('ERROR!!! peak not found or too small')
# for k in range(0,len(data_get[0])):
#     #typicalFWHM is <1.5mV
#     #take 1 mV distance from min to avoid undesiderd peaks
#     if(data_get[k]<phimin/2 and np.abs(argmin-k)<20):
#         kmax=k
#         if kmin==0:
#             kmin=k
VBold=VBmin
VBmin=data_set[argmin]        
dVB_G4=np.subtract(VBmin,VBold)

#define axis
plt.legend()
plt.xlabel('VG2(mV)')
plt.ylabel('$\phi_{G2}$(deg)')

now=datetime.datetime.now()
dayFolder=datetime.date.isoformat(now)
name='calibrate_G2'
plt.savefig(folder2+'\\'+dayFolder+'\\'+str(dataid)+name+'.png')



slopeG3G2=float(dVB_G3/DeltaVG3)

slopeG4G2=float(dVB_G4/DeltaVG4) 
print('alpha_G3G2='+str(slopeG3G2))
print('alpha_G4G2='+str(slopeG4G2))
print('VG2='+str(VBmin[0]))

VG3comp=  SpecialParameters.CompensateG3(VG3,VG2,slopeG3G2)
VG4comp=  SpecialParameters.CompensateG4(VG4,VG2,slopeG4G2)
#for now just sit on min, fine calib after
VG2(VBmin[0])          
# slopeG4B=-0.6
# slopeG3B= -0.156
VG4comp(initG4)
VG3comp(initG3)



