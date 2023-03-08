# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 18:45:36 2020

@author: G-GRE-GRE050402
"""
####




###
# rampVG1(-400)
# rampVG2(-400)
initG4=-900
initG3=-900

# rampVG1(0)
# rampVG2(0)
rampVG3(initG3)
rampVG4(initG4)

VG5now=VG5()
VG6now=VG6()
VG6onmin_phD(VG6now-10,VG6now+10,201,1)

VG5onmin_phD(VG5now-10,VG5now+10,201,1)
plt.close()

now=datetime.datetime.now()
dayFolder= datetime.date.isoformat(now)
try:
        os.makedirs(folder2+'\\'+dayFolder)
except IOError:
        donothing=1

rampVG3(initG3)
rampVG4(initG4)
DeltaVG4=3#mV
DeltaVG3=3 #mV
# guessVG5=VG5()
initVG5=VG5()-3
finalVG5=VG5()+2


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
plt.ylabel('$\phi_4$(deg)')

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




# slopeG3G5=-0.007999999999992725
# slopeG4G5=-0.14400000000000546
slopeG3G5=float(dVB_G3/DeltaVG3)
slopeG4G5=float(dVB_G4/DeltaVG4) 
print('alpha_G3G5='+str(slopeG3G5))
print('alpha_G4G5='+str(slopeG4G5))
print('VG5='+str(VBmin[0]))

# VG3comp=  SpecialParameters.CompensateG3(VG3,VG5,slopeG3G5)
VG4comp=  SpecialParameters.CompensateG4(VG4,VG5,slopeG4G5)
#for now just sit on min, fine calib after
VG5(VBmin[0])          

VG4comp(initG4)
VG3comp(initG3)

################################
VG3comp(-925)
VG4comp(-925)
VG5now=VG5()
VG2now=VG2()
VG6now=VG6()
VG1now=VG1()
VG6onmin_phD(VG6now-5,VG6now+5,401,1)
VG5onmin_phD(VG5now-5,VG5now+5,401,1)

VG1onmin_phS(VG1now-5,VG1now+5,401,1)
VG2onmin_phS(VG2now-5,VG2now+5,401,1)
name='DOUBLECOMP_G4vsG3_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
a,dataid,c,d=sweep2D(VG3comp,-900,-950,51,0.02,VG4comp,-900,-950,51,0.025,ph1,ph2)
# a,dataid,c,d=sweep2D(VG4comp,-960,-945,151,0.02,VG3comp,-900,-940,161,0.01,ph1)                
plot_by_id(dataid)
saveplot(name,dataid)


VG4comp=  SpecialParameters.CompensateG4_double(VG4,VG5,VG2,slopeG4G5,slopeG4G2)
VG3comp=  SpecialParameters.CompensateG3_double(VG3,VG5,VG2,slopeG3G5,slopeG3G2)




# # VG3comp(-890)
# # VG4comp(-952)
# # VG5now=VG5()
# # VG5onmin_phD(VG5now-10,VG5now+10,1001,1)
# # VG5now=VG5()
# # VG5onmin_phD(VG5now-2,VG5now+2,401,1)
# # name='G4vsG3_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
# # # a,dataid,c,d=sweep2D(VG3comp,-960,-940,81,0.02,VG4comp,-820,-780,41,0.03,ph1)
# # a,dataid,c,d=sweep2D(VG4comp,-960,-940,101,0.005,VG3comp,-1000,-900,401,0.005,ph1)                
# # plot_by_id(dataid)
# # saveplot(name,dataid)
# # VG4comp(-1000)
# # VG3comp(-920)
# # VG5(-1150)
# # VG5now=VG5()
# # VG5onmin_phD(VG5now-50,VG5now+50,801,1)
# # VG5now=VG5()
# # VG5onmin_ph1(VG5now-5,VG5now+5,501,1)

# name='G4vsG5_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
# a,dataid,c,d=sweep2D(VG4,-1000,-1200,201,0.02,VG5,-1000,-1200,201,0.002,ph1)
                     
# plot_by_id(dataid)
# saveplot(name,dataid)

