# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 18:24:49 2021

@author: G-GRE-GRE050402
"""
# Bfield(0.8)

continuous_acquisition()
continuous_acquisition_ch2()




mwgen.off()
rampVG3(-848.7)
rampVG4(-830.7)
VG5now=VG5()
VG2now=VG2()
VG6now=VG6()
VG1now=VG1()
# 1089_0.899T_MWon10dB_5GHz_G3vsG4COMP_G1-1672.3mV_G2-1377.1969mV_G3-845.0mV_G4-834.0mV_G5-1471.0487mV_G6-1593.2417mV2
# VG6onmin_phD(VG6now-20,VG6now+20,801,1)
VG5onmin_phD(VG5now-5,VG5now+5,401,1)

# VG1onmin_phS(VG1now-20,VG1now+20,801,1)
VG2onmin_phS(VG2now-5,VG2now+5,401,1)

name=str(Bfield())+'T_G3vsG4COMP_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
a,dataid,c,d=sweep2D(VG3,-847.3,-846,41,0.05,VG4,-831,-831.6,41,0.02,ph1,ph2)
# a,dataid,c,d=sweep2D(VG3comp,-850,-845,51,0.05,VG4comp,-829,-834,51,0.012,ph1,ph2)
plot_by_id(dataid)
save2plots(name,dataid)
plt.close()
plot_by_id(dataid)

plot2d_diff(dataid)









#########################################################################




continuous_acquisition()
continuous_acquisition_ch2()

detuningPoint1 = [-847.7,-830.5]  #TPC #G3,G4
detuningPoint2 = [-847.2,-831.7] 
VG3comp(detuningPoint1[0])
VG4comp(detuningPoint1[1])
DeltaG4G3=(detuningPoint1[0]-detuningPoint2[0])/(detuningPoint1[1]-detuningPoint2[1])


G4detuning=  SpecialParameters.DetuningG4(VG4,VG3,DeltaG4G3)
# G4detuning=  SpecialParameters.CompensateG4(VG4comp,VG3comp,DeltaG4G3)

mwgen.off()
#test detuning
name=str(Bfield())+'T_detuningscan_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
a,dataid,c=sweep1D(G4detuning,-830.5,-832.5,101,0.012,ph1,ph2)
plot_by_id(dataid)
saveplot(name,dataid)
plt.show()
#################################




#testrf
mwgen.on()
mwgen.power(3)

name=str(Bfield())+'T_freq_scan_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
a,dataid,c=sweep1D(mwgen.frequency,3e9,20e9,501,0.012,ph2)
plot_by_id(dataid)
saveplot(name,dataid)
#calibrate rf power
mwgen.on()
mwgen.power(10)
mwgen.frequency(12e9)
name=str(Bfield())+'T_power_scan_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
a,dataid,c=sweep1D(mwgen.power,-10,30,401,0.012,ph1)
plot_by_id(dataid)
saveplot(name,dataid)
#calibrate rf power



mwgen.on()
mwgen.power(20)
name=str(Bfield())+'T_freqvsdetuning_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
mwgen.on()
a,dataid,c,d=sweep2D(G4detuning,-832.5,-831,51,0.05,mwgen.frequency,9e9,19e9,1000,0.01,ph2,ph1)
plot_by_id(dataid)
saveplot(name,dataid)

save2plots(name,dataid)

############
# VG3comp(-846.85)
# VG4comp(-832.8)
Bfield(0.2)
mwgen.on()
mwgen.power(-10)
name=str(Bfield())+'T_freqvsdetuning_power-10dBm_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
mwgen.on()
a,dataid,c,d=sweep2D(mwgen.frequency,3e9,10e9,700,0.01,G4detuning,-830.5,-831.7,81,0.01,ph1,ph2)
plot_by_id(dataid)
save2plots(name,dataid)


##########################

VG3comp(-850)
VG4comp(-829)
VG5onmin_phD(VG5now-5,VG5now+5,401,1)
VG2onmin_phS(VG2now-5,VG2now+5,401,1)
mwgen.on()
name=str(Bfield())+'T_freqvspower_offICT_pulseonG4__45dBatt_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
a,dataid,c,d=sweep2D(mwgen.frequency,3e9,20e9,341,0.01,mwgen.power,30,-10,81,0.05,ph2,ph1)
plot_by_id(dataid)
save2plots(name,dataid)
# save4plots(name,dataid)

# data_set,data_get,parameters_name=Extract_data(a)

the_data = load_by_id(dataid)
data_list = the_data.get_parameter_data()
P = the_data.parameters
p = P.split(',')
Y= data_list[p[2]][p[0]]#freq
X = data_list[p[2]][p[1]]#gate
x = np.unique(X)
y = np.unique(Y)
z1 = data_list[p[2]][p[2]]#phS
Z1 = z1.reshape((np.size(np.unique(Y)),np.size(np.unique(X))))
X,Y = np.meshgrid(x,y)



Z1 = z1.reshape((np.size(np.unique(Y)),np.size(np.unique(X))))
par=x
far=y
threshold=-4.1
calib=[]
for i in range(0,len(y)):
    previousmin=10
    for j in range(0,len(x)):
     # Z1[i]=scipy.signal.savgol_filter(Z1[i], 11, 3)
         if np.abs(Z1[i][j]-threshold)<previousmin:
             previousmin= np.abs(Z1[i][j]-threshold)
             argmin=j
    calib.append(x[argmin])


mwfreq_calib=SpecialParameters.Calibrated_Fmw(mwgen.frequency,mwgen.power,calib,far,-5)  

np.savetxt(folder2+'\\'+dayFolder+'\\'+str(dataid)+'calibfile.txt',calib)  

VG3comp(-846.75)
VG4comp(-831.25)


G4detuning(-831)

mwgen.on()
mwgen.power(16)
name=str(Bfield())+'T_fvsdet_P'+str(mwgen.power()-65)+'dBG1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
a,dataid,c,d=sweep2D(mwgen.frequency,10e9,15e9,5001,0.01,G4detuning,-831,-832,81,0.01,ph1,ph2)
plot_by_id(dataid)
save2plots(name,dataid)


VG3comp(-846.75)
VG4comp(-831.25)
G4detuning(-831.75)

Bfield(0.4)
mwgen.on()
mwgen.power(10)
ziUhf.daq.setInt('/dev2010/awgs/0/enable', 1)
ampliAWG(0.1)

name=str(Bfield())+'T_fvsdet_pulsing_P'+str(mwgen.power()-65)+'dBG1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
a,dataid,c,d=sweep2D(Bfield_Hon,0.7,0.8,21,1,mwgen.frequency,12e9,18e9,3000,0.005,ph1,ph2)
plot_by_id(dataid)
save2plots(name,dataid)





Bfield(0.4)
mwgen.on()
mwgen.power(10)
ziUhf.daq.setInt('/dev2010/awgs/0/enable', 1)
ampliAWG(0.1)
name=str(Bfield())+'T_freq_scan_pulsing_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
a,dataid,c=sweep1D(mwgen.frequency,6.5e9,9e9,25001,0.012,ph2,ph1)
plot_by_id(dataid)
saveplot(name,dataid)
# P0=0
# calib=np.subtract(calib,P0)
# val=3e9
# initF=mwgen.frequency()
# initP=mwgen.power()
# p = np.argmin(np.abs(far-val))
# Power = float(calib[p])
# mwgen.frequency(val)
# mwgen.power(Power+P0)