# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 16:40:22 2020

@author: G-GRE-GRE050402
"""





rampVG1(-1100)
rampVG2(-1000)
VG1now=VG1()
VG1onmin(VG1now-10,VG1now+10,201,1)
# rampVG3(-800)
# rampVG4(-800)

initG4=-800
initG3=-800

smooth=1


now=datetime.datetime.now()
dayFolder= datetime.date.isoformat(now)
try:
        os.makedirs(folder2+'\\'+dayFolder)
except IOError:
        donothing=1

rampVG3(initG3)
rampVG4(initG4)
DeltaVG4=-5#mV
DeltaVG3=-5 #mV
guessVG1=0
initVG1=-825
finalVG1=-835


Npoints=1001


a,dataid,c=sweep1D(VG1,initVG1,finalVG1,Npoints,0.02,ph1)
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
dVG1=0

#############################################
f = plt.figure()
if smooth==1:
    plt.plot(data_set,datasmooth,label='VG3='+str(VG3())+'mV, VG4='+str(VG4())+'mV')
else:
    plt.plot(data_set,data_get[0],label='VG3='+str(VG3())+'mV, VG4='+str(VG4())+'mV')


#############################################
###move G3 and caluculate relative displacement of G1 peak
rampVG3(VG3()+DeltaVG3)

a,dataid,c=sweep1D(VG1,initVG1,finalVG1,Npoints,0.02,ph1)
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
###move G4 and caluculate relative displacement of G1 peak
rampVG4(VG4()+DeltaVG4)
time.sleep(5)
a,dataid,c=sweep1D(VG1,initVG1,finalVG1,Npoints,0.02,ph1)
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
plt.xlabel('VG1(mV)')
plt.ylabel('$\phi_{G1}$(deg)')

now=datetime.datetime.now()
dayFolder=datetime.date.isoformat(now)
name='calibrate_G1'
plt.savefig(folder2+'\\'+dayFolder+'\\'+str(dataid)+name+'.png')



slopeG3G1=float(dVB_G3/DeltaVG3)

slopeG4G1=float(dVB_G4/DeltaVG4) 
print('alpha_G3G1='+str(slopeG3G1))
print('alpha_G4G1='+str(slopeG4G1))
print('VG1='+str(VBmin[0]))

VG3comp=  SpecialParameters.CompensateG3(VG3,VG1,slopeG3G1)
VG4comp=  SpecialParameters.CompensateG4(VG4,VG1,slopeG4G1)
#for now just sit on min, fine calib after
VG1(VBmin[0])          
# slopeG4B=-0.6
# slopeG3B= -0.156
VG4comp(initG4)
VG3comp(initG3)

# ###########################
# bias(Vds)
# rampVG1(-120)
# rampVG2(-200)
# rampVG3(-1000)
# rampVG4(-1000)
# rampVG5(-200)

# VG1onmin(-120,-140,1001,1)
# ###################
# a,dataid,c,d=sweep2D(VG3comp,-1000,-1050,51,0.1,VG4comp,-1000,-1050,51,0.01,ph1,A1)
# name='G3compvsG4_gates_'+str(opengate)+'mV'
# plot_by_id(dataid)
# saveplot(name,dataid)

# VG1onmin(VG1()-20,VG1()+20,1001,1)
# ###################
# a,dataid,c,d=sweep2D(VG3comp,-1050,-1100,26,0.1,VG4comp,-1050,-1100,26,0.01,ph1,A1)
# name='G3compvsG4_gates_'+str(opengate)+'mV'
# plot_by_id(dataid)
# saveplot(name,dataid)

# VG1onmin(VG1()-20,VG1()+20,1001,1)
# ###################
# a,dataid,c,d=sweep2D(VG3comp,-1100,-1150,26,0.1,VG4comp,-1100,-1150,26,0.01,ph1,A1)
# name='G3compvsG4_gates_'+str(opengate)+'mV'
# plot_by_id(dataid)
# saveplot(name,dataid)

# VG1onmin(VG1()-20,VG1()+20,1001,1)
# ###################
# a,dataid,c,d=sweep2D(VG3comp,-1150,-1200,26,0.1,VG4comp,-1150,-1200,26,0.01,ph1,A1)
# name='G3compvsG4_gates_'+str(opengate)+'mV'
# plot_by_id(dataid)
# saveplot(name,dataid)




# VG1onmin(VG1()-20,VG1()+20,1001,1)
# ###################
# a,dataid,c,d=sweep2D(VG3comp,-1200,-1300,51,0.1,VG4comp,-1200,-1300,51,0.01,ph1,A1)
# name='G3compvsG4_gates_'+str(opengate)+'mV'
# plot_by_id(dataid)
# saveplot(name,dataid)

# VG1onmin(VG1()-20,VG1()+20,1001,1)
# ###################
# a,dataid,c,d=sweep2D(VG3comp,-1300,-1400,51,0.1,VG4comp,-1300,-1400,51,0.01,ph1,A1)
# name='G3compvsG4_gates_'+str(opengate)+'mV'
# plot_by_id(dataid)
# saveplot(name,dataid)

# VG1onmin(VG1()-20,VG1()+20,1001,1)
# ###################
# a,dataid,c,d=sweep2D(VG3comp,-1400,-1500,51,0.1,VG4comp,-1400,-1500,51,0.01,ph1,A1)
# name='G3compvsG4_gates_'+str(opengate)+'mV'
# plot_by_id(dataid)
# saveplot(name,dataid)

# VG1onmin(VG1()-20,VG1()+20,1001,1)
# ###################
# a,dataid,c,d=sweep2D(VG3comp,-1500,-1600,51,0.1,VG4comp,-1500,-1600,51,0.01,ph1,A1)
# name='G3compvsG4_gates_'+str(opengate)+'mV'
# plot_by_id(dataid)
# saveplot(name,dataid)