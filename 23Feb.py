# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 17:32:47 2021

@author: G-GRE-GRE050402
"""

rampVG1(-500)
rampVG2(0)

rampVG3(0)
rampVG4(0)

rampVG5(0)
rampVG6(0)



name='G1scan_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
a,dataid,c=sweep1D(VG1,-500,-1500,1001,0.02,ph2,ph1,ph3,ph4)
plot_by_id(dataid)
save4plots(name,dataid)


rampVG1(-500)
rampVG2(0)

rampVG3(0)
rampVG4(0)

rampVG5(0)
rampVG6(0)



name='G6scan_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
a,dataid,c=sweep1D(VG6,-500,-1500,1001,0.02,ph2,ph1,ph3,ph4)
plot_by_id(dataid)
save4plots(name,dataid)



rampVG1(-1800)
rampVG2(-800)
rampVG3(-800)
rampVG4(-800)
rampVG5(-1800)
rampVG6(-1800)



name='G2scan_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
a,dataid,c=sweep1D(VG2,-800,-1800,1001,0.02,ph2,ph1,current)
plot_by_id(dataid)
save3plots(name,dataid)





rampVG1(-1800)
rampVG2(-1700)
rampVG3(-1000)
rampVG4(-1000)
rampVG5(-1700)
rampVG6(-1800)

name='G1scan_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
a,dataid,c=sweep1D(VG6,-1000,-2000,1001,0.02,ph2,ph1,current)
plot_by_id(dataid)
save3plots(name,dataid)



rampVG1(-1800)
rampVG2(-1700)

rampVG3(-1000)
rampVG4(-1000)

rampVG5(-1700)
rampVG6(-1800)



name='G1scan_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
a,dataid,c=sweep1D(VG6,-1000,-2000,1001,0.02,ph2,ph1,current)
plot_by_id(dataid)
save3plots(name,dataid)




# opengate=-1600
# opengateL=-1900
# initgate=-800
# finalgate=-1200
#################################
rampVG1(-1800)
rampVG2(-1400)
rampVG3(-700)
rampVG4(-700)

rampVG5(-1400)
rampVG6(-1800)

continuous_acquisition()
name='G1vsG2_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
a,dataid,c,d=sweep2D(VG1,-1800,-1850,101,0.02,VG2,-1400,-1450,101,0.012,ph2,ph4)
plot_by_id(dataid)
# saveplot(name,dataid)
save2plots(name,dataid)


rampVG1(-1800)
rampVG2(-1400)
rampVG3(-700)
rampVG4(-700)

rampVG5(-1400)
rampVG6(-1800)

continuous_acquisition()
name='G6vsG5_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
a,dataid,c,d=sweep2D(VG6,-1800,-1850,101,0.02,VG5,-1400,-1450,101,0.012,ph1,ph3)
plot_by_id(dataid)
# saveplot(name,dataid)
save2plots(name,dataid)


#####comp map