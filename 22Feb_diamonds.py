# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 12:55:38 2021

@author: G-GRE-GRE050402
"""



bias(2)
opengate=-1600
opengateL=-1900
initgate=-800
finalgate=-1200
#################################
rampVG1(initgate)
rampVG2(initgate)
rampVG3(opengate)
rampVG4(opengate)

rampVG5(opengate)
rampVG6(opengateL)

continuous_acquisition()
name='G1vsG2_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
a,dataid,c,d=sweep2D(VG1,-800,-1000,201,0.02,VG2,-800,-1000,201,0.012,current,ph1,ph2)
plot_by_id(dataid)
saveplot(name,dataid)
save3plots(name,dataid)



rampVG1(opengateL)
rampVG2(initgate)
rampVG3(initgate)
rampVG4(opengate)
rampVG5(opengate)
rampVG6(opengateL)

continuous_acquisition()
name='_G2vsG3_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
a,dataid,c,d=sweep2D(VG2,-800,-1000,201,0.02,VG3,-800,-1000,201,0.012,current,ph1,ph2)
plot_by_id(dataid)
saveplot(name,dataid)

rampVG1(opengateL)
rampVG2(opengate)
rampVG3(initgate)
rampVG4(initgate)
rampVG5(opengate)
rampVG6(opengateL)


continuous_acquisition()
name='_G3vsG4_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
a,dataid,c,d=sweep2D(VG3,-700,-1000,201,0.02,VG4,-700,-1000,201,0.012,current,ph1,ph2,ph3,ph4)
plot_by_id(dataid)
saveplot(name,dataid)



rampVG1(opengateL)
rampVG2(opengate)
rampVG3(opengate)
rampVG4(initgate)
rampVG5(initgate)
rampVG6(opengateL)


continuous_acquisition()
name='_G4vsG5_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
a,dataid,c,d=sweep2D(VG4,-800,-1000,201,0.02,VG5,-800,-1000,201,0.012,current,ph1,ph2)
plot_by_id(dataid)
saveplot(name,dataid)

rampVG1(opengateL)
rampVG2(opengate)
rampVG3(opengate)
rampVG4(opengate)
rampVG5(initgate)
rampVG6(initgate)


continuous_acquisition()
name='_G5vsG6_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
a,dataid,c,d=sweep2D(VG5,-800,-1000,201,0.02,VG6,-800,-1000,201,0.012,current,ph1,ph2)
plot_by_id(dataid)
saveplot(name,dataid)

# rampVG1(-1100)
# rampVG2(-1100)
# rampVG3(-1600)
# rampVG4(-1600)

# rampVG5(-1600)
# rampVG6(-1600)

# continuous_acquisition()
# name=str(Bfield())+'_G3vsG4_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
# a,dataid,c,d=sweep2D(VG1,-1100,-1200,201,0.02,VG2,-1100,-1200,201,0.012,current,ph1,ph2)
# plot_by_id(dataid)
# saveplot(name,dataid)




###########DIAMONDS (6hours)
#check saturation of ampli before
rampVG1(-650)
rampVG2(opengate)
rampVG3(opengate)
rampVG4(opengate)
rampVG5(opengate)
rampVG6(opengateL)


continuous_acquisition()
name='_G1DIAMONDS_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
a,dataid,c,d=sweep2D(bias,-5,5,101,0.02,VG1,-650,-950,601,0.02,current,ph1,ph2)
plot_by_id(dataid)
saveplot(name,dataid)



rampVG1(opengateL)
rampVG2(-650)
rampVG3(opengate)
rampVG4(opengate)
rampVG5(opengate)
rampVG6(opengateL)

# VG2onmin_phS(-1480,-1520,401,1)
# VG5onmin_phD(-1480,-1520,401,1)



continuous_acquisition()
name='_G2DIAMONDS_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
a,dataid,c,d=sweep2D(bias,-5,5,101,0.02,VG2,-650,-950,601,0.02,current,ph1,ph2)
plot_by_id(dataid)
saveplot(name,dataid)


rampVG1(opengateL)
rampVG2(opengate)
rampVG3(-650)
rampVG4(opengate)
rampVG5(opengate)
rampVG6(opengateL)
# VG2onmin_phS(-1480,-1520,401,1)
# VG5onmin_phD(-1480,-1520,401,1)



continuous_acquisition()
name='_G3DIAMONDS_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
a,dataid,c,d=sweep2D(bias,-5,5,201,0.02,VG3,-650,-950,601,0.02,current,ph1,ph2)
plot_by_id(dataid)
saveplot(name,dataid)



rampVG1(opengateL)
rampVG2(opengate)
rampVG3(opengate)
rampVG4(-650)
rampVG5(opengate)
rampVG6(opengateL)
# VG2onmin_phS(-1480,-1520,401,1)
# VG5onmin_phD(-1480,-1520,401,1)



continuous_acquisition()
name='_G4DIAMONDS_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
a,dataid,c,d=sweep2D(bias,-5,5,101,0.02,VG4,-650,-950,601,0.02,current)#,ph1,ph2)
plot_by_id(dataid)
saveplot(name,dataid)



rampVG1(opengateL)
rampVG2(opengate)
rampVG3(opengate)
rampVG4(opengate)
rampVG5(-650)
rampVG6(opengateL)

# VG2onmin_phS(-1480,-1520,401,1)
# VG5onmin_phD(-1480,-1520,401,1)



continuous_acquisition()
name='_G5DIAMONDS_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
a,dataid,c,d=sweep2D(bias,-5,5,101,0.02,VG5,-650,-950,601,0.02,current,ph1,ph2)
plot_by_id(dataid)
saveplot(name,dataid)

rampVG1(opengate)
rampVG2(opengate)
rampVG3(opengate)
rampVG4(opengate)
rampVG5(opengate)
rampVG6(-650)

# VG2onmin_phS(-1480,-1520,401,1)
# VG5onmin_phD(-1480,-1520,401,1)



continuous_acquisition()
name='_G6DIAMONDS_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
a,dataid,c,d=sweep2D(bias,-5,5,101,0.02,VG6,-650,-950,601,0.02,current,ph1,ph2)
plot_by_id(dataid)
saveplot(name,dataid)


