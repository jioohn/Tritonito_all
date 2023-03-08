# -*- coding: utf-8 -*-
"""
Created on Thu May  6 11:35:50 2021

@author: G-GRE-GRE050402
"""





VG4comp(-807)
VG3comp(-864)
VG6now=VG6()
VG5now=VG5()
VG2now=VG2()
VG1now=VG1()


continuous_acquisition()
continuous_acquisition_ch2()


VG1onmin_phS(VG1now-5,VG1now+5,501,1)

VG6onmin_phD(VG6now-5,VG6now+5,501,1)
phiS=[]
phiD=[]
for i in range (0,50):
   
    phiS.append(ph2())
    phiD.append(ph1())

sigma_S=np.std(phiS)
sigma_D=np.std(phiD)



# VG4comp(-803)
# VG3comp(-863)
VG6now=VG6()
VG5now=VG5()
VG2now=VG2()
VG1now=VG1()


continuous_acquisition()
continuous_acquisition_ch2()

ks=0
kd=0
first_time=0

while ks==0 or kd==0:
    if ks==0:
        VG1now=VG1()-20*first_time
        rampVG2(VG2()-20*first_time)
        VG1onmin_phS(VG1now-10,VG1now+10,801,1)
    if kd==0:
        VG6now=VG6()-20*first_time
        rampVG5(VG5()-20*first_time)
        VG6onmin_phD(VG6now-10,VG6now+10,801,1)

    phiS=[]
    phiD=[]
    for i in range (0,50):
        time.sleep(10)
        phiS.append(ph2())
        phiD.append(ph1())
        
    phiSmax=np.max(phiS)
    phiSmin=np.min(phiS)
    
    
    phiDmax=np.max(phiD)
    phiDmin=np.min(phiD)
    
    
    if np.abs(phiSmax-phiSmin)>4*sigma_S:
        print('phiS is drifting')
        ks=0
        first_time=1
    else:
            print('phiS is stable')
            ks=1
            first_time=0
    if np.abs(phiDmax-phiDmin)>4*sigma_D:
        print('phiD is drifting')
        kd=0
        first_time=1
    else:
            print('phiD is stable')
            kd=1
            first_time=0