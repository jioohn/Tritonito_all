# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 12:39:12 2021

@author: G-GRE-GRE050402
"""

slopeG3G2=-0.30199999999999816
slopeG4G2=-0.022000000000025464
slopeG3G5=-0.013999999999987267
slopeG4G5=-0.21200000000003455

VG4comp=  SpecialParameters.CompensateG4_double(VG4,VG5,VG2,slopeG4G5,slopeG4G2)
VG3comp=  SpecialParameters.CompensateG3_double(VG3,VG5,VG2,slopeG3G5,slopeG3G2)

# slopeG3G2=-0.18
# slopeG4G2=-0.015

# rampVG1(-1550)
# rampVG2(-1550)



# rampVG5(-1500)
# rampVG6(-1800)

# rampVG3(-750)
# rampVG4(-750)

initG4=VG4()
initG3=VG3()

Vds=-0.2
bias(Vds)

rampVG4(initG4)
rampVG3(initG3)

VG1now=VG1()
VG2now=VG2()
VG3now=VG3()
VG4now=VG4()
VG5now=VG5()

# VG1onmin_phS(VG1now-20,VG1now+20,1001,1)

# VG1onmin_phS(VG1now-4,VG1now+4,801,1)

time.sleep(1)
VG2onmin_phS(VG2now-4,VG2now+4,801,1)

VG1now=VG1()
VG2now=VG2()
VG3now=VG3()
VG4now=VG4()
VG5now=VG5()

DeltaVG4=3#mV
DeltaVG3=3#mV



smooth=1


now=datetime.datetime.now()
dayFolder= datetime.date.isoformat(now)
try:
        os.makedirs(folder2+'\\'+dayFolder)
except IOError:
        donothing=1

rampVG3(initG3)
rampVG4(initG4)


initVG2=VG2now-3
finalVG2=VG2now+2
rampVG2(initVG2)
ph2()
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
plt.ylabel('$\phi_{S}$(deg)')

now=datetime.datetime.now()
dayFolder=datetime.date.isoformat(now)
name='calibrate_G2'
plt.savefig(folder2+'\\'+dayFolder+'\\'+str(dataid)+name+'.png')



slopeG3G2=float(dVB_G3/DeltaVG3)

slopeG4G2=float(dVB_G4/DeltaVG4) 
print('alpha_G3G2='+str(slopeG3G2))
print('alpha_G4G2='+str(slopeG4G2))
print('VG2='+str(VBmin))

###################################################•
VG3comp=  SpecialParameters.CompensateG3(VG3,VG2,slopeG3G2)
VG4comp=  SpecialParameters.CompensateG4(VG4,VG2,slopeG4G2)

####################################################

#################################################################"
###########################################################################"
rampVG3(initG3)
rampVG4(initG4)

VG5now=VG5()
VG6now=VG6()
VG6onmin_phD(VG6now-30,VG6now+30,601,1)

VG5onmin_phD(VG5now-5,VG5now+5,201,1)
plt.close()

now=datetime.datetime.now()
dayFolder= datetime.date.isoformat(now)
try:
        os.makedirs(folder2+'\\'+dayFolder)
except IOError:
        donothing=1

rampVG3(initG3)
rampVG4(initG4)
# DeltaVG4=5#mV
# DeltaVG3=5 #mV
# guessVG5=VG5()
initVG5=VG5()-3
finalVG5=VG5()+2

VG5(initVG5)
ph1()
Npoints=501


a,dataid,c=sweep1D(VG5,initVG5,finalVG5,Npoints,0.01,ph1)
data_set,data_get, parameters_name =Extract_data(a)     

# phimin=np.min(data_get[0])
# argmin=np.argmin(data_get[0])
datasmooth=scipy.signal.savgol_filter(np.ravel(data_get[0]),11, 3)
phimin=np.min(datasmooth)
argmin=np.argmin(datasmooth)

# f = plt.figure()
# plt.plot(data_set,data_get[0],label='VG3='+str(VG3())+'mV, VG4='+str(VG4())+'mV')
plt.plot(data_set,datasmooth,label='VG3='+str(VG3())+'mV, VG4='+str(VG4())+'mV')


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
dVG5=0

#############################################
f = plt.figure()
plt.plot(data_set,datasmooth,label='VG3='+str(VG3())+'mV, VG4='+str(VG4())+'mV')


#############################################
###move G3 and caluculate relative displacement of G5 peak
rampVG3(VG3()+DeltaVG3)

a,dataid,c=sweep1D(VG5,initVG5,finalVG5,Npoints,0.01,ph1)
data_set,data_get, parameters_name =Extract_data(a)     


# phimin=np.min(data_get[0])
# argmin=np.argmin(data_get[0])
datasmooth=scipy.signal.savgol_filter(np.ravel(data_get[0]),11, 3)
phimin=np.min(datasmooth)
argmin=np.argmin(datasmooth)

# f = plt.figure()
# plt.plot(data_set,data_get[0],label='VG3='+str(VG3())+'mV, VG4='+str(VG4())+'mV')
plt.plot(data_set,datasmooth,label='VG3='+str(VG3())+'mV, VG4='+str(VG4())+'mV')


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
###move G4 and caluculate relative displacement of G5 peak
rampVG4(VG4()+DeltaVG4)
time.sleep(5)
a,dataid,c=sweep1D(VG5,initVG5,finalVG5,Npoints,0.01,ph1)
data_set,data_get, parameters_name =Extract_data(a)     


# phimin=np.min(data_get[0])
# argmin=np.argmin(data_get[0])
datasmooth=scipy.signal.savgol_filter(np.ravel(data_get[0]),11, 3)
phimin=np.min(datasmooth)
argmin=np.argmin(datasmooth)

# f = plt.figure()
# plt.plot(data_set,data_get[0],label='VG3='+str(VG3())+'mV, VG4='+str(VG4())+'mV')
plt.plot(data_set,datasmooth,label='VG3='+str(VG3())+'mV, VG4='+str(VG4())+'mV')


plt.legend()
plt.xlabel('VG5(mV)')
plt.ylabel('$\phi_D$(deg)')

now=datetime.datetime.now()
dayFolder=datetime.date.isoformat(now)
name='calibrate_G5'
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
dVB_G4=np.subtract(VBmin,VBold)


# slolpeG3G2=-0.2799999999999727
# slopeG4G2=0.007999999999924512
# slopeG3G5=0.06800000000009732
# slopeG4G5=0.6879999999999882

# slopeG3G5=-0.007999999999992725
# slopeG4G5=-0.14400000000000546
slopeG3G5=float(dVB_G3/DeltaVG3)
slopeG4G5=float(dVB_G4/DeltaVG4) 
print('slopeG3G2='+str(slopeG3G2))
print('slopeG4G2='+str(slopeG4G2))

print('slopeG3G5='+str(slopeG3G5))
print('slopeG4G5='+str(slopeG4G5))
print('VG5='+str(VBmin))

# VG3comp=  SpecialParameters.CompensateG3(VG3,VG5,slopeG3G5)
# VG4comp=  SpecialParameters.CompensateG4(VG4,VG5,slopeG4G5)
#for now just sit on min, fine calib after
VG5(VBmin)          

VG4comp=  SpecialParameters.CompensateG4_double(VG4,VG5,VG2,slopeG4G5,slopeG4G2)
VG3comp=  SpecialParameters.CompensateG3_double(VG3,VG5,VG2,slopeG3G5,slopeG3G2)

VG4comp(initG4)
VG3comp(initG3)

################################
VG4comp=  SpecialParameters.CompensateG4(VG4,VG5,slopeG4G5)
VG3comp=  SpecialParameters.CompensateG3(VG3,VG2,slopeG3G2)

# slopeG3G2=-0.21359999999999674
# slopeG4G2=-0.019200000000000727
# slopeG3G5=-0.08119999999998981
# slopeG4G5=-0.175


# VG3(-825)
# VG4(-825)
# VG5now=VG5()
# VG2now=VG2()
# VG6now=VG6()
# VG1now=VG1()
# VG6onmin_phD(VG6now-20,VG6now+20,801,1)
# VG5onmin_phD(VG5now-5,VG5now+5,401,1)

# VG1onmin_phS(VG1now-20,VG1now+20,801,1)
# VG2onmin_phS(VG2now-5,VG2now+5,401,1)

# name='DOUBLECOMP_G4vsG3_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
# a,dataid,c,d=sweep2D(VG3comp,-771,-774,101,0.015,VG4comp,-810,-826,161,0.015,ph2,ph1)                
# plot_by_id(dataid)
# save2plots(name,dataid)



# name='DOUBLECOMP_G4vsG3_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
# a,dataid,c,d=sweep2D(VG3comp,-774,-776,41,0.015,VG4comp,-800,-780,81,0.015,ph2,ph1)                
# plot_by_id(dataid)
# save2plots(name,dataid)
