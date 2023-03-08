# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 22:49:05 2021

@author: G-GRE-GRE050402
"""
# time.sleep(3600)
rampVG4(-1500)
rampVG1(-300)
rampVG3(-825)
rampVG2(-775)
rampVG2(-1950)
VG1now=VG1()
VG2now=VG2()
VG3now=VG3()
VG4now=VG4()
VG5now=VG5()
VG5onmin_ph2(VG5now-50,VG5now+50,1001,1)
VG4onmin_ph2(VG4now-50,VG4now+50,1001,1)
VG1now=VG1()
# VG1onmin(VG1now-4,VG1now+4,801,1)
VG1now=VG1()
VG4now=VG4()
VG5now=VG5()
# VG5onmin_ph2(VG5now-3,VG5now+50,1001,1)
VG4onmin_ph2(VG4now-3,VG4now+3,601,1)


for i in range (0,3):
    for j in range(0,3):
        VG3comp(-825-50*i)
        VG2comp(-775-50*j)
        VG4now=VG4()
        VG4onmin_ph2(VG4now-5,VG4now+5,1001,1)
        name=str(Bfield())+'T_G2vsG3_Vmet'+str(dac.dac17())+'V_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
        a,dataid,c,d=sweep2D(VG3comp,-800-50*i,-850-50*i,201,0.1,VG2comp,-750-50*j,-800-50*j,201,0.012,ph2)
        plot_by_id(dataid)
        saveplot(name,dataid)
        
################  
dac.dac17(20)
time.sleep(3600)
dac.dac17(-30)
time.sleep(7200)
###############
rampVG4(-1500)
rampVG1(-300)
rampVG3(-825)
rampVG2(-775)
rampVG2(-1950)
VG1now=VG1()
VG2now=VG2()
VG3now=VG3()
VG4now=VG4()
VG5now=VG5()
VG5onmin_ph2(VG5now-50,VG5now+50,1001,1)
VG4onmin_ph2(VG4now-50,VG4now+50,1001,1)
VG1now=VG1()
# VG1onmin(VG1now-4,VG1now+4,801,1)
VG1now=VG1()
VG4now=VG4()
VG5now=VG5()
# VG5onmin_ph2(VG5now-3,VG5now+50,1001,1)
VG4onmin_ph2(VG4now-3,VG4now+3,601,1)


for i in range (0,3):
    for j in range(0,3):
        VG3comp(-825-50*i)
        VG2comp(-775-50*j)
        VG4now=VG4()
        VG4onmin_ph2(VG4now-10,VG4now+10,1001,1)
        name=str(Bfield())+'T_G2vsG3_Vmet'+str(dac.dac17())+'V_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
        a,dataid,c,d=sweep2D(VG3comp,-800-50*i,-850-50*i,201,0.1,VG2comp,-750-50*j,-800-50*j,201,0.012,ph2)
        plot_by_id(dataid)
        saveplot(name,dataid)
        
rampVG1(-300)
rampVG2(-700)    
rampVG3(-700) 
name=str(Bfield())+'T_G2vsG3_Vmet'+str(dac.dac17())+'V_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'        
a,dataid,c,d=sweep2D(VG5,-1800,-1900,501,0.1,VG4,-1400,-1500,101,0.012,ph2)
plot_by_id(dataid)
saveplot(name,dataid)




# VG5onmin_ph2(-2000,-1700,601,1)
# VG4onmin_ph2(-1600,-1200,801,1)

# slopeG3G4=-0.4299999999999879
# slopeG2G4=-0.03333333333337881
slopeG3G4=-0.3833333
slopeG2G4=-0.053333
VG3comp=  SpecialParameters.CompensateG3(VG3,VG4,slopeG3G4)
VG2comp=  SpecialParameters.CompensateG2(VG2,VG4,slopeG2G4)

rampVG1(-300)
rampVG2(-700)
rampVG3(-700)
rampVG4(-1522)
rampVG5(-1804)




Bfield(3)
VG2comp(-725)
VG3comp(-725)
VG5now=VG5()
VG5onmin_ph2(VG5now-50,VG5now+50,501,1)
VG4now=VG4()
VG4onmin_ph2(VG4now-5,VG4now+5,1001,1)
name=str(Bfield())+'T_G2vsG3_Vmet'+str(dac.dac17())+'V_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
a,dataid,c,d=sweep2D(VG2comp,-700,-750,51,0.012,VG3comp,-750,-700,51,0.012,ph2)
plot_by_id(dataid)
saveplot(name,dataid)

VG4now=VG4()
VG5now=VG5()
VG5onmin_ph2(VG5now-50,VG5now+50,501,1)
VG4now=VG4()
VG4onmin_ph2(VG4now-5,VG4now+5,1001,1)
name=str(Bfield())+'T_G5vstime_Vmet'+str(dac.dac17())+'V_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
a,dataid,c,d=sweep2D(dac.dac16,0,0.1,100,1,VG5,VG5now-100,VG5now+100,401,0.02,ph2)
plot_by_id(dataid)
saveplot(name,dataid)
# VG3comp(-625)

# VG2comp(-625)
# VG5onmin_ph2(-2000,-1700,601,1)
# VG4onmin_ph2(-1600,-1700,801,1)

VG5now=VG5()
VG5onmin_ph2(VG5now-50,VG5now+50,1001,1)
VG4now=VG4()
VG4onmin_ph2(VG4now-20,VG4now+20,1001,1)

for i in range (0,3):
    for j in range(0,3):
        VG3comp(-775-50*i)
        VG2comp(-775-50*j)
        VG4now=VG4()
        VG4onmin_ph2(VG4now-10,VG4now+10,1001,1)
        name=str(Bfield())+'T_G2vsG3_Vmet'+str(dac.dac17())+'V_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
        a,dataid,c,d=sweep2D(VG3comp,-750-50*i,-800-50*i,101,0.1,VG2comp,-750-50*j,-800-50*j,101,0.012,ph2)
        plot_by_id(dataid)
        saveplot(name,dataid)
        

VG3comp(-831.5)
VG2comp(-845)
VG4now=VG4()
VG4onmin_ph2(VG4now-10,VG4now+10,1001,1)
name=str(Bfield())+'T_G2vsG3_Vmet'+str(dac.dac17())+'V_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
a,dataid,c,d=sweep2D(VG3comp,-837,-847,51,0.1,VG2comp,-829,-839,51,0.014,ph2)
plot_by_id(dataid)
saveplot(name,dataid)


VG3comp(-831.5)

VG4now=VG4()
VG4onmin_ph2(VG4now-10,VG4now+10,1001,1)

name=str(Bfield())+'T_G2vsG3_Vmet'+str(dac.dac17())+'V_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
a,dataid,c,d=sweep2D(Bfield,3,1,61,0.1,VG2comp,-831,-836,51,0.014,ph2,ph1)
plot_by_id(dataid)
saveplot(name,dataid)

