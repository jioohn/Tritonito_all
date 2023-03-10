# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 18:47:45 2020

@author: G-GRE-GRE050402
"""

# bias(-0.2)
# rampVG1(-1500)
# rampVG2(-1500)
# rampVG3(-1000)
# rampVG4(-1000)
# rampVG5(-1000)
# G2now=VG2()
# G3now=VG3()
# G4now=VG4()
# G5now=VG5()
# VG1onmin(-1495,-1505,201,1)
# G1now=VG1()
# VG1onmin(G1now-3,G1now+3,601,1)
# G1now=VG1()
# # VG2onmin(-1090,-1110,501,1)
# # VG3onmin(-700,-950,1001,1)
# # VG4onmin(-700,-1000,1001,1)
# # VG5onmin(-200,+200,1001,1)
# VG2onmin(G2now-3,G2now+3,501,1)
# # VG2onmin(G2now-10,G2now+10,501,1)
# # VG3onmin(G3now-150,G3now+150,1001,1)
# VG3onmin(G3now-50,G3now+50,1001,1)
# # VG4onmin(G4now-200,G4now+200,2001,1)
# VG4onmin(G4now-100,G4now+100,1001,1)
# VG5onmin(G5now-250,G5now+250,1001,1)
# a,b,c,d =sweep2D(rf1freq,377.3e6,377.8e6,51,0.02,VG1,-1498.5,-1500.5,201,0.005,ph1,A1)

# rf1freq(377.6e6)

# a,b,c,d =sweep2D(rf1power,-15,-45,31,0.02,VG1,-1498.5,-1500.5,201,0.005,ph1,A1)
# rf1power(-25)

# rf1freq(376.9e6)

# a,b,c,d =sweep2D(rf1power,-15,-45,31,0.02,VG1,-1498.5,-1500.5,201,0.005,ph1,A1)
# rf1power(-25)

bias(-0.2)
rampVG1(-1500)
rampVG2(-1500)
rampVG3(-1000)
rampVG4(-1000)
rampVG5(0)
G2now=VG2()
G3now=VG3()
G4now=VG4()
G5now=VG5()
VG1onmin(-1495,-1505,201,1)
G1now=VG1()
VG1onmin(G1now-3,G1now+3,601,1)
G1now=VG1()
# VG2onmin(-1090,-1110,501,1)
# VG3onmin(-700,-950,1001,1)
# VG4onmin(-700,-1000,1001,1)
# VG5onmin(-200,+200,1001,1)
VG2onmin(G2now-3,G2now+3,501,1)
# VG2onmin(G2now-10,G2now+10,501,1)
# VG3onmin(G3now-150,G3now+150,1001,1)
VG3onmin(G3now-5,G3now+5,1001,1)
# VG4onmin(G4now-200,G4now+200,2001,1)
VG4onmin(G4now-5,G4now+5,1001,1)
# VG5onmin(G5now-250,G5now+250,1001,1)

name='G1vsG2_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
# a,dataid,c,d=sweep2D(VG3,G3now-100,G3now+100,801,0.02,VG4,G4now-20,G4now+20,401,0.01,ph1)
# plot_by_id(dataid)
# saveplot(name,dataid)
G2now=VG2()
G3now=VG3()
G4now=VG4()
G5now=VG5()
#626
a,dataid,c,d=sweep2D(VG1,-1300,-1600,301,0.02,VG2,-1300,-1600,301,0.005,ph1)
plot_by_id(dataid)
saveplot(name,dataid)



bias(-0.2)
rampVG1(-1500)
rampVG2(-1500)
rampVG3(-1000)
rampVG4(-1000)
rampVG5(0)
G2now=VG2()
G3now=VG3()
G4now=VG4()
G5now=VG5()
VG1onmin(-1495,-1505,201,1)
G1now=VG1()
VG1onmin(G1now-3,G1now+3,601,1)
G1now=VG1()
# VG2onmin(-1090,-1110,501,1)
# VG3onmin(-700,-950,1001,1)
# VG4onmin(-700,-1000,1001,1)
# VG5onmin(-200,+200,1001,1)
VG2onmin(G2now-3,G2now+3,501,1)
# VG2onmin(G2now-10,G2now+10,501,1)
# VG3onmin(G3now-150,G3now+150,1001,1)
VG3onmin(G3now-5,G3now+5,1001,1)
# VG4onmin(G4now-200,G4now+200,2001,1)
VG4onmin(G4now-5,G4now+5,1001,1)
# VG5onmin(G5now-250,G5now+250,1001,1)

name='G2vsG3_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
# a,dataid,c,d=sweep2D(VG3,G3now-100,G3now+100,801,0.02,VG4,G4now-20,G4now+20,401,0.01,ph1)
# plot_by_id(dataid)
# saveplot(name,dataid)
G2now=VG2()
G3now=VG3()
G4now=VG4()
G5now=VG5()
#626
a,dataid,c,d=sweep2D(VG2,-1600,-1300,301,0.02,VG3,-600,-1000,401,0.005,ph1)
plot_by_id(dataid)
saveplot(name,dataid)



bias(-0.2)
rampVG1(-1500)
rampVG2(-1500)
rampVG3(-1000)
rampVG4(-1000)
rampVG5(0)
G2now=VG2()
G3now=VG3()
G4now=VG4()
G5now=VG5()
VG1onmin(-1495,-1505,201,1)
G1now=VG1()
VG1onmin(G1now-3,G1now+3,601,1)
G1now=VG1()
# VG2onmin(-1090,-1110,501,1)
# VG3onmin(-700,-950,1001,1)
# VG4onmin(-700,-1000,1001,1)
# VG5onmin(-200,+200,1001,1)
VG2onmin(G2now-3,G2now+3,501,1)
# VG2onmin(G2now-10,G2now+10,501,1)
# VG3onmin(G3now-150,G3now+150,1001,1)
VG3onmin(G3now-5,G3now+5,1001,1)
# VG4onmin(G4now-200,G4now+200,2001,1)
VG4onmin(G4now-5,G4now+5,1001,1)
VG5onmin(G5now-250,G5now+250,1001,1)


# a,dataid,c,d=sweep2D(VG3,G3now-100,G3now+100,801,0.02,VG4,G4now-20,G4now+20,401,0.01,ph1)
# plot_by_id(dataid)
# saveplot(name,dataid)
G2now=VG2()
G3now=VG3()
G4now=VG4()
G5now=VG5()
#626
name='G3vsG4_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G5'+str(VG5())+'mV'
a,dataid,c,d=sweep2D(VG3,-600,-1000,401,0.02,VG4,-600,-1000,401,0.005,ph1,A1)
plot_by_id(dataid)
saveplot(name,dataid)



for i in range(4,9):
    bias(-0.2)
    # rampVG1(-1500)
    rampVG2(-1200)
    rampVG3(-1000)
    rampVG4(-1020+40*i)
    rampVG5(0)
    G1now=VG1()
    G2now=VG2()
    G3now=VG3()
    G4now=VG4()
    G5now=VG5()
    VG1onmin(G1now-20,G1now+20,201,1)
    G1now=VG1()
    VG1onmin(G1now-3,G1now+3,601,1)
    G1now=VG1()
    # VG2onmin(-1090,-1110,501,1)
    # VG3onmin(-700,-950,1001,1)
    # VG4onmin(-700,-1000,1001,1)
    # VG5onmin(-200,+200,1001,1)
    VG2onmin(G2now-3,G2now+3,501,1)
    # VG2onmin(G2now-10,G2now+10,501,1)
    # VG3onmin(G3now-150,G3now+150,1001,1)
    # VG3onmin(G3now-5,G3now+5,1001,1)
    # VG4onmin(G4now-200,G4now+200,2001,1)
    # VG4onmin(G4now-5,G4now+5,1001,1)
    # VG5onmin(G5now-250,G5now+250,1001,1)
    
    G2now=VG2()
    G3now=VG3()
    G4now=VG4()
    G5now=VG5()
    #626
    name='G3vsG4_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
    a,dataid,c,d=sweep2D(VG3,-1010,-990,81,0.02,VG4,-1000+40*i,-1040+40*i,81,0.005,ph1)
    plot_by_id(dataid)
    saveplot(name,dataid)