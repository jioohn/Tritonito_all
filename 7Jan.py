# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 15:20:45 2021

@author: G-GRE-GRE050402
"""
rampVG1(-1600)
rampVG2(-500)
rampVG3(0)
rampVG4(0)
rampVG5(00)
bias(0)
continuous_acquisition()

ziUhf.daq.setInt('/dev2010/sigouts/1/on', 0)

Bfield(0)
continuous_acquisition()
name=str(Bfield())+'G4vsG3_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
# a,dataid,c,d=sweep2D(VG3,-500,-900,401,0.02,VG2,-500,-900,401,0.02,ph1)
plot_by_id(dataid)
saveplot(name,dataid)



rampVG1(-1700)
rampVG2(-600)
rampVG3(-500)
rampVG4(0)
rampVG5(00)
continuous_acquisition()
name=str(Bfield())+'G1vsG2_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
a,dataid,c,d=sweep2D(VG1,-1700,-1500,201,0.02,VG2,-600,-900,401,0.02,ph1)
plot_by_id(dataid)
saveplot(name,dataid)



VG1(-1700)
VG1onmin(-1710,-1690,201,1)
continuous_acquisition()
name=str(Bfield())+'G2vsG3_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
a,dataid,c,d=sweep2D(VG2,-600,-1000,301,0.02,VG3,-600,-1000,301,0.02,ph1)
plot_by_id(dataid)
saveplot(name,dataid)

VG1(-1540)
# VG1onmin(-1710,-1690,201,1)
continuous_acquisition()
name=str(Bfield())+'G2vsG3_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
a,dataid,c,d=sweep2D(VG2,-1100,-1120,101,0.02,VG3,-900,-1000,201,0.02,ph1)
plot_by_id(dataid)
saveplot(name,dataid)


VG1(-1540)
VG3(-900)
# VG1onmin(-1710,-1690,201,1)
continuous_acquisition()
name=str(Bfield())+'G2vsG4_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
a,dataid,c,d=sweep2D(VG2,-1115,-1105,101,0.02,VG4,-1000,-1100,201,0.02,ph1)
plot_by_id(dataid)
saveplot(name,dataid)



VG1(-1540)
VG2(-1150)
VG3(-1050)
VG4(-850)
VG1onmin(-1530,-1550,201,1)
# VG1onmin(-1710,-1690,201,1)
continuous_acquisition()
name=str(Bfield())+'G3vsG4_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
a,dataid,c,d=sweep2D(VG3,-1050,-900,201,0.02,VG4,-850,-1000,201,0.02,ph1)
plot_by_id(dataid)
saveplot(name,dataid)




slopeG3G2=-0.14
slopeG4G2=-0.015
VG3comp=  SpecialParameters.CompensateG3(VG3,VG2,slopeG3G2)
VG4comp=  SpecialParameters.CompensateG4(VG4,VG2,slopeG4G2)


# VG1(-1540)
# VG2(-1150)
# VG3(-960)
# VG4(-920)
# VG1onmin(-1530,-1550,201,1)
# # VG1onmin(-1710,-1690,201,1)
# continuous_acquisition()
# name=str(Bfield())+'G3vsG4_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
# a,dataid,c,d=sweep2D(VG3comp,-900,-1000,201,0.02,VG4comp,-850,-1000,201,0.02,ph1)
# plot_by_id(dataid)
# saveplot(name,dataid)


#47
VG1(-1540)
VG2(-1150)
VG3(-946)
VG4(-920)
VG1onmin(-1530,-1550,201,1)
VG1now=VG1()
VG1onmin(VG1now-4,VG1now+4,201,1)

continuous_acquisition()
name=str(Bfield())+'G3vsG4_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
a,dataid,c,d=sweep2D(VG3comp,-940,-950,101,0.02,VG4comp,-880,-980,361,0.01,ph1)
plot_by_id(dataid)
saveplot(name,dataid)


#56
VG1(-1540)
VG2(-1150)
VG3(-946)
VG4(-920)

ziUhf.daq.setInt('/dev2010/sigouts/1/on', 0)
G1now=VG1()
G2now=VG2()
G3now=VG3()
G4now=VG4()
G5now=VG5()
VG3comp()
VG4comp()
VG1onmin(G1now-10,G1now+10,801,1)
G1now=VG1()
VG1onmin(G1now-4,G1now+4,801,1)
G1now=VG1()
VG2onmin(G2now-4,G2now+4,801,1)
G2now=VG2()
# VG5onmin_ph2(G5now-10,G5now+10,801,1)
G5now=VG5()

continuous_acquisition()
name=str(Bfield())+'G3vsG4_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
a,dataid,c,d=sweep2D(VG3comp,-960,-980,101,0.02,VG4comp,-880,-980,361,0.01,ph1)
plot_by_id(dataid)
saveplot(name,dataid)

#60
VG1(-1570)
VG2(-1150)
VG3(-971.5)
VG4(-904)

ziUhf.daq.setInt('/dev2010/sigouts/1/on', 0)
G1now=VG1()
G2now=VG2()
G3now=VG3()
G4now=VG4()
G5now=VG5()
VG3comp()
VG4comp()
VG1onmin(G1now-10,G1now+10,801,1)
G1now=VG1()
VG1onmin(G1now-4,G1now+4,801,1)
G1now=VG1()
VG2onmin(G2now-4,G2now+4,801,1)
G2now=VG2()
# VG5onmin_ph2(G5now-10,G5now+10,801,1)
G5now=VG5()

continuous_acquisition()
name=str(Bfield())+'G3vsG4_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
a,dataid,c,d=sweep2D(VG3comp,-972,-969,61,0.02,VG4comp,-903,-930,161,0.01,ph1)
plot_by_id(dataid)
saveplot(name,dataid)
##oldcomp
# slopeG3G2=-0.22
# slopeG4G2=-0.04
# VG3comp=  SpecialParameters.CompensateG3(VG3,VG2,slopeG3G2)
# VG4comp=  SpecialParameters.CompensateG4(VG4,VG2,slopeG4G2)


# VG1(-1540)
# VG2(-1150)
# VG3(-960)
# VG4(-920)
# VG1onmin(-1530,-1550,201,1)
# # VG1onmin(-1710,-1690,201,1)
# continuous_acquisition()
# name=str(Bfield())+'G3vsG4_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
# a,dataid,c,d=sweep2D(VG3comp,-900,-1050,201,0.02,VG4comp,-850,-1000,201,0.02,ph1)
# plot_by_id(dataid)
# saveplot(name,dataid)