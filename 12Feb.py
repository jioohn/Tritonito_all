# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 15:38:48 2021

@author: G-GRE-GRE050402
"""

slolpeG3G2=-0.1043999999999869
slopeG4G2=-0.008400000000006003
slopeG3G5=-0.00420000000001437
slopeG4G5=-0.09659999999998944
VG4comp=  SpecialParameters.CompensateG4_double(VG4,VG5,VG2,slopeG4G5,slopeG4G2)
VG3comp=  SpecialParameters.CompensateG3_double(VG3,VG5,VG2,slopeG3G5,slopeG3G2)

VG4comp=  SpecialParameters.CompensateG4(VG4,VG5,slopeG4G5)
VG3comp=  SpecialParameters.CompensateG3(VG3,VG2,slopeG3G2)


rampVG1(-1600)
rampVG2(-1700)
# rampVG3(-750)
# rampVG4(-890)
rampVG5(-1700)
rampVG6(-1600)
bias(0)

#G1-1634.01mV_G2-1336.1208mV_G3-1025.0mV_G4-790.0mV_G5-1630.6681mV_G6-1780.1mV
# 1022_7DOUBLECOMP_G4vsG3_G1-1633.4599999999998mV_G2-1342.0918mV_G3-1025.0mV_G4-850.0mV_G5-1654.6081mV_G6-1793.6499999999999mV2
# 967_6DOUBLECOMP_G4vsG3_G1-1636.26mV_G2-1369.7438mV_G3-1025.0mV_G4-1070.0mV_G5-1688.2131mV_G6-1788.75mV2 - Copie

VG6onmin_phD(VG6now-50,VG6now+50,1001,1)
VG5onmin_phD(VG5now-50,VG5now+50,1001,1)
VG2onmin_phS(VG2now-50,VG2now+50,1001,1)
VG1onmin_phS(VG1now-50,VG1now+50,1001,1)


rampVG3(-1102)
rampVG4(-1168)

VG5now=VG5()
VG2now=VG2()
VG6now=VG6()
VG1now=VG1()
VG6onmin_phD(VG6now-30,VG6now+30,401,1)
VG5onmin_phD(VG5now-5,VG5now+5,401,1)

VG1onmin_phS(VG1now-30,VG1now+30,401,1)
VG5onmin_phD(VG5now-5,VG5now+5,401,1)
VG2onmin_phS(VG2now-5,VG2now+5,401,1)

name=str(Bfield())+'T_DOUBLECOMP__G4vsG3_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
a,dataid,c,d=sweep2D(VG3comp,-1103.5,-1105.5,41,0.015,VG4comp,-1164,-1161.5,41,0.012,ph2,ph1)#A2,A1,ph1,ph2)
             
plot_by_id(dataid)
saveplot(name,dataid)
# save2plots(name,dataid)


VG3comp(-1104.4)
VG4comp(-1167.9)


















rampVG1(-1750)
rampVG2(-1500)
# rampVG3(-750)
# rampVG4(-890)
rampVG5(-1600)
rampVG6(-1850)
bias(-0)





rampVG3(-1102)
rampVG4(-1105)
VG5now=VG5()
VG2now=VG2()
VG6now=VG6()
VG1now=VG1()
VG6onmin_phD(VG6now-10,VG6now+10,401,1)
VG5onmin_phD(VG5now-5,VG5now+5,401,1)

VG1onmin_phS(VG1now-10,VG1now+10,401,1)
VG2onmin_phS(VG2now-5,VG2now+5,401,1)

name='DOUBLECOMP_G4vsG3_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
a,dataid,c,d=sweep2D(VG3comp,-1104,-1102,21,0.015,VG4comp,-1104,-1105,11,0.03,ph2)
              
plot_by_id(dataid)
save2plots(name,dataid)



VG4comp=  SpecialParameters.CompensateG4(VG4,VG5,slopeG4G5)
VG3comp=  SpecialParameters.CompensateG3(VG3,VG2,slopeG3G2)
VGonmin_phD(VGnow-50,VGnow+50,1001,1)
VG5onmin_phD(VG5now-50,VG5now+50,1001,1)
# VG1onmin_phS(VG1now-100,VG1now+100,1001,1)
# VG2onmin_phS(VG2now-100,VG2now+100,1001,1)

for i in range(0,11):
    VG3(-790+20*i)
    VG4(-895)
    VG5now=VG5()
    VG2now=VG2()
    VG6now=VG6()
    VG1now=VG1()
    VG6onmin_phD(VG6now-20,VG6now+20,801,1)
    VG5onmin_phD(VG5now-5,VG5now+5,401,1)
    
    VG1onmin_phS(VG1now-20,VG1now+20,801,1)
    VG2onmin_phS(VG2now-5,VG2now+5,401,1)
    
    name=str(i)+'DOUBLECOMP_G4vsG3_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
    a,dataid,c,d=sweep2D(VG3comp,-800+20*i,-780+20*i,201,0.015,VG4comp,-1106-900,101,0.03,ph2,ph1)
    # a,dataid,c,d=sweep2D(VG4comp,-960,-945,151,0.02,VG3comp,-900,-940,161,0.01,ph1)                
    plot_by_id(dataid)
    save2plots(name,dataid)


name='G1vs2_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
a,dataid,c,d=sweep2D(VG1,-1800,-1820,41,0.015,VG2,-1450,-1470,41,0.015,ph2)
      
plot_by_id(dataid)
saveplot(name,dataid)

name='G5vsG6_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
a,dataid,c,d=sweep2D(VG6,-1790,-1820,41,0.015,VG5,-1530,-1550,41,0.015,ph1)
      
plot_by_id(dataid)
saveplot(name,dataid)
