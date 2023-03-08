# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 18:02:39 2021

@author: G-GRE-GRE050402
"""

# rampVG1(-1000)
# rampVG2(-800)

# rampVG3(-800)
# rampVG4(-800)

initG2=-1000
initG3=-850
# rampVG5()

VG3comp(initG3)
VG2comp(initG2)

VG4now=VG4()
VG4onmin_ph2(VG4now-10,VG4now+10,101,1)
plt.close()

now=datetime.datetime.now()
dayFolder= datetime.date.isoformat(now)
try:
        os.makedirs(folder2+'\\'+dayFolder)
except IOError:
        donothing=1

rampVG3(initG3)
rampVG2(initG2)
DeltaVG2=3#mV
DeltaVG3=3 #mV
# guessVG4=VG4()
initVG4=VG4()-3
finalVG4=VG4()+2


Npoints=501


a,dataid,c=sweep1D(VG4,initVG4,finalVG4,Npoints,0.01,ph2)
data_set,data_get, parameters_name =Extract_data(a)     

# phimin=np.min(data_get[0])
# argmin=np.argmin(data_get[0])
datasmooth=scipy.signal.savgol_filter(np.ravel(data_get[0]),11, 3)
phimin=np.min(datasmooth)
argmin=np.argmin(datasmooth)

# f = plt.figure()
# plt.plot(data_set,data_get[0],label='VG3='+str(VG3())+'mV, VG2='+str(VG2())+'mV')
plt.plot(data_set,datasmooth,label='VG3='+str(VG3())+'mV, VG2='+str(VG2())+'mV')


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
dVG4=0

#############################################
f = plt.figure()
plt.plot(data_set,datasmooth,label='VG3='+str(VG3())+'mV, VG2='+str(VG2())+'mV')


#############################################
###move G3 and caluculate relative displacement of G4 peak
rampVG3(VG3()+DeltaVG3)

a,dataid,c=sweep1D(VG4,initVG4,finalVG4,Npoints,0.01,ph2)
data_set,data_get, parameters_name =Extract_data(a)     


# phimin=np.min(data_get[0])
# argmin=np.argmin(data_get[0])
datasmooth=scipy.signal.savgol_filter(np.ravel(data_get[0]),11, 3)
phimin=np.min(datasmooth)
argmin=np.argmin(datasmooth)

# f = plt.figure()
# plt.plot(data_set,data_get[0],label='VG3='+str(VG3())+'mV, VG2='+str(VG2())+'mV')
plt.plot(data_set,datasmooth,label='VG3='+str(VG3())+'mV, VG2='+str(VG2())+'mV')


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
###move G2 and caluculate relative displacement of G4 peak
rampVG2(VG2()+DeltaVG2)
time.sleep(5)
a,dataid,c=sweep1D(VG4,initVG4,finalVG4,Npoints,0.01,ph2)
data_set,data_get, parameters_name =Extract_data(a)     


# phimin=np.min(data_get[0])
# argmin=np.argmin(data_get[0])
datasmooth=scipy.signal.savgol_filter(np.ravel(data_get[0]),11, 3)
phimin=np.min(datasmooth)
argmin=np.argmin(datasmooth)

# f = plt.figure()
# plt.plot(data_set,data_get[0],label='VG3='+str(VG3())+'mV, VG2='+str(VG2())+'mV')
plt.plot(data_set,datasmooth,label='VG3='+str(VG3())+'mV, VG2='+str(VG2())+'mV')


plt.legend()
plt.xlabel('VG4(mV)')
plt.ylabel('$\phi_4$(deg)')

now=datetime.datetime.now()
dayFolder=datetime.date.isoformat(now)
name='calibrate_G4'
plt.savefig(folder2+'\\'+dayFolder+'\\'+str(dataid)+name+'.png')




# phimin=np.min(data_get[0])
# argmin=np.argmin(data_get[0])
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
dVB_G2=np.subtract(VBmin,VBold)




# slopeG3G4=-0.007999999999992725
# slopeG2G4=-0.14400000000000546
slopeG3G4=float(dVB_G3/DeltaVG3)
slopeG2G4=float(dVB_G2/DeltaVG2) 
print('alpha_G3G4='+str(slopeG3G4))
print('alpha_G2G4='+str(slopeG2G4))
print('VG4='+str(VBmin[0]))

VG3comp=  SpecialParameters.CompensateG3(VG3,VG4,slopeG3G4)
VG2comp=  SpecialParameters.CompensateG2(VG2,VG4,slopeG2G4)
#for now just sit on min, fine calib after
VG4(VBmin[0])          

VG2comp(initG2)
VG3comp(initG3)

# VG3comp(-800)
# VG4comp(-800)
# VG4now=VG4()
# VG4onmin_ph2(VG4now-5,VG4now+5,401,1)
# name='G4vsG3_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
# a,dataid,c,d=sweep2D(VG2comp,-825,-900,301,0.02,VG3comp,-775,-825,201,0.03,ph2)
# # a,dataid,c,d=sweep2D(VG4comp,-960,-945,151,0.02,VG3comp,-900,-940,161,0.01,ph2)                
# plot_by_id(dataid)
# saveplot(name,dataid)