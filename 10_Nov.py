# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 19:16:27 2020

@author: G-GRE-GRE050402
"""

##calib in four corners reverse scan
for i in range(0,4):
    if i==0:
       initG4=-810
       initG3=-900
    if i==1:
       initG4=-810
       initG3=-910
    if i==2:
       initG4=-820
       initG3=-900
    if i==3:
       initG4=-820
       initG3=-910
       
    if i==4:
       initG4=-825
       initG3=-885
    if i==5:
       initG4=-820
       initG3=-885
       
       
    VG4comp(initG4)
    VG3comp(initG3)
    VG1now=VG1()
    VG2now=VG2()
    Vds=-0.2
    # finalgate=-1000
    # initgate=0
    # opengate=-1000
    # closegate=-200
    # # opengate=0
    bias(Vds)
    
    
    rampVG5(0)
    
    VG1onmin(VG1now-50,VG1now+50,1001,1)
    VG1now=VG1()
    VG1onmin(VG1now-4,VG1now+4,801,1)
    VG1now=VG1()
    
    # VG2onmin(VG2now-10,VG2now+10,101,1)
    VG2now=VG2()
    ph1()
    time.sleep(1)
    VG2onmin(VG2now-5,VG2now+5,801,1)
    VG2now=VG2()
    
    G2now=VG2()
    G3now=VG3()
    G4now=VG4()
    G5now=VG5()
    
    name='G3compvsG4_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
    a,dataid,c,d=sweep2D(VG3comp,-900,-910,101,0.01,VG4comp,-810,-820,101,0.01,ph1)
    plot_by_id(dataid)
    saveplot(name,dataid)
    
#####################

    initG4=-820
    initG3=-900
    VG4comp(initG4)
    VG3comp(initG3)
    VG1now=VG1()
    VG2now=VG2()
    Vds=-0.2
    # finalgate=-1000
    # initgate=0
    # opengate=-1000
    # closegate=-200
    # # opengate=0
    bias(Vds)
    
    
    rampVG5(0)
    
    VG1onmin(VG1now-20,VG1now+20,1001,1)
    VG1now=VG1()
    VG1onmin(VG1now-4,VG1now+4,801,1)
    VG1now=VG1()
    
    # VG2onmin(VG2now-10,VG2now+10,101,1)
    VG2now=VG2()
    ph1()
    time.sleep(1)
    VG2onmin(VG2now-5,VG2now+5,801,1)
    VG2now=VG2()
    
    G2now=VG2()
    G3now=VG3()
    G4now=VG4()
    G5now=VG5()
    
    name='G3compvsG4_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
    a,dataid,c,d=sweep2D(VG3comp,-890,-910,101,0.01,VG4comp,-810,-830,201,0.01,ph1)
    plot_by_id(dataid)
    saveplot(name,dataid)
    
    # name='G4compvsG3_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
    # a,dataid,c,d=sweep2D(VG4comp,-810,-820,201,0.01,VG3comp,-890,-910,101,0.01,ph1)
    # plot_by_id(dataid)
    # saveplot(name,dataid)
    

#1521

a,dataid,c,d=sweep2D(VG3comp,-904,-910,121,0.05,VG4comp,-814,-818,81,0.05,ph1)
plot_by_id(dataid)
saveplot(name,dataid)

name='TP_G4compvsG3_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
a,dataid,c,d=sweep2D(VG4comp,-814,-818,81,0.05,VG3comp,-904,-910,121,0.05,ph1)
plot_by_id(dataid)
saveplot(name,dataid)