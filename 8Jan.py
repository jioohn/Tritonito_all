# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 10:36:42 2021

@author: G-GRE-GRE050402
"""


# class Phi(qc.Parameter):
#     def __init__(self, name, UHF, demodulator):
#         super().__init__(name, label='phase', vals=qc.validators.Numbers(), unit='rad', docstring='UHF demodulator phase')
#         self._daq = UHF.daq
# #        self._daq.unsubscribe('*')
#         self._daq.flush()
#         self._sampleKey = '/dev2010/demods/'+str(demodulator)+'/sample'
#         self._rateKey = '/dev2010/demods/'+str(demodulator)+'/rate'
#         self._daq.subscribe(self._sampleKey)
        
#     # you must provide a get method, a set_raw method, or both
#     def get_raw(self):
#         #self._daq.flush()
#         notFound = True
#         while notFound:
#             d = self._daq.poll(1.5/self._daq.getDouble(self._rateKey),10,1, True)
# #            d = self._daq.poll(1e-6,10,1, True)
#             if self._sampleKey in d:
#                 x = d[self._sampleKey]['x']
#                 y = d[self._sampleKey]['y']
# #                phi = d[self._sampleKey]['phi']
#                 notFound = False
            
# #        return np.arctan2(np.mean(y),np.mean(x)) #np.arctan2(y[-1],x[-1])
#        # print(len(x))
#         #print(np.arctan2(y,x))
#         self._daq.flush()
#         phase=np.arctan2(y[-1],x[-1])
#         if phase>0:
#             phase=phase-2*np.pi
#         return phase
# #                return phi[-1]
#     def set_raw(self, val):
#         time.sleep(0.001)    

ph1 = SpecialParameters.PhiD('phiD', ziUhf, 0)
#test ph unwrap
VG3(-825)
VG4(-825)
VG5now=VG5()
VG2now=VG2()
VG6now=VG6()
VG1now=VG1()
a,b,c=sweep1D(VG6,VG6now-100,VG6now+100,801,0.02,ph1)
plot_by_id(b)




VG3(-825)
VG4(-825)
VG5now=VG5()
VG2now=VG2()
VG6now=VG6()
VG1now=VG1()
a,b,c=sweep1D(VG6,VG6now-50,VG6now+50,801,0.02,ph1)


VG6onmin_phD(VG6now-20,VG6now+20,801,1)
VG5onmin_phD(VG5now-5,VG5now+5,401,1)

VG1onmin_phS(VG1now-20,VG1now+20,801,1)
VG2onmin_phS(VG2now-5,VG2now+5,401,1)


rampVG1(-1800)
rampVG2(-1400)
rampVG5(-1400)
rampVG6(-1800)

for i in range(0,4):
    for j in range(0,4):
        rampVG3(-760-20*i)
        rampVG4(-760-20*j)
        VG5now=VG5()
        VG2now=VG2()
        VG6now=VG6()
        VG1now=VG1()

        VG6onmin_phD(VG6now-20,VG6now+20,801,1)
        VG5onmin_phD(VG5now-5,VG5now+5,401,1)
        
        VG1onmin_phS(VG1now-20,VG1now+20,801,1)
        VG2onmin_phS(VG2now-5,VG2now+5,401,1)
    
        name='G3vsG4_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
        a,dataid,c,d=sweep2D(VG3comp,-750-20*i,-770-20*i,51,0.02,VG4comp,-750-20*j,-770-20*j,51,0.02,ph1,ph2)
        plot_by_id(dataid)
        saveplot(name,dataid)
        
        
name='G2vsG3_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG5())+'mV'
a,dataid,c,d=sweep2D(VG2,-1420,-1430,51,0.02,VG3,-800,-900,201,0.015,ph2)
plot_by_id(dataid)
saveplot(name,dataid)

VG3(-700)

name='G5vsG6_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG5())+'mV'
a,dataid,c,d=sweep2D(VG5,-1360,-1370,51,0.02,VG4,-600,-700,201,0.015,ph1)
plot_by_id(dataid)
saveplot(name,dataid)


rampVG3(-775)
rampVG4(-815)
VG5now=VG5()
VG2now=VG2()
VG6now=VG6()
VG1now=VG1()

VG6onmin_phD(VG6now-30,VG6now+30,801,1)
VG5onmin_phD(VG5now-5,VG5now+5,401,1)

VG1onmin_phS(VG1now-30,VG1now+30,801,1)
VG2onmin_phS(VG2now-5,VG2now+5,401,1)

name='G3vsG4_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
a,dataid,c,d=sweep2D(VG3comp,-760,-790,201,0.02,VG4comp,-800,-830,201,0.015,ph1,ph2)
plot_by_id(dataid)
save2plots(name,dataid)


for i in range(0,3):
    for j in range(0,3):
        rampVG3(-760-20*i)
        rampVG4(-760-20*j)
        VG5now=VG5()
        VG2now=VG2()
        VG6now=VG6()
        VG1now=VG1()

        VG6onmin_phD(VG6now-20,VG6now+20,801,1)
        VG5onmin_phD(VG5now-5,VG5now+5,401,1)
        
        VG1onmin_phS(VG1now-20,VG1now+20,801,1)
        VG2onmin_phS(VG2now-5,VG2now+5,401,1)
    
        name='G3vsG4_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
        a,dataid,c,d=sweep2D(VG3comp,-750-20*i,-770-20*i,51,0.02,VG4comp,-750-20*j,-770-20*j,51,0.015,ph1,ph2)
        plot_by_id(dataid)
        saveplot(name,dataid)



VG3(-700)
VG4(-700)
name='G1vsG2_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
a,dataid,c,d=sweep2D(VG1,-1100,-1600,501,0.015,VG2,-1100,-1600,501,0.015,ph2)                
plot_by_id(dataid)
save3plots(name,dataid)


VG3(-700)
VG4(-700)
name='G6vsG5_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
a,dataid,c,d=sweep2D(VG6,-1100,-1600,501,0.015,VG5,-1100,-1600,501,0.012,ph1)                
plot_by_id(dataid)
save3plots(name,dataid)     



bias(3)
VG3(-700)
VG4(-700)
name='G3vsG4_3mVbias__G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
a,dataid,c,d=sweep2D(VG3,-700,-900,401,0.015,VG4,-700,-900,401,0.012,ph1,ph2,current)                
plot_by_id(dataid)
save2plots(name,dataid)     
        





VG3(-700)
VG4(-700)
name='G1vsG2_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
a,dataid,c,d=sweep2D(VG1,-1600,-1610,51,0.015,VG2,-1450,-1460,51,0.015,ph2)                
plot_by_id(dataid)
save3plots(name,dataid)


VG3(-700)
VG4(-700)
name='G6vsG5_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
a,dataid,c,d=sweep2D(VG6,-1800,-1810,51,0.015,VG5,-1600,-1610,51,0.012,ph1)                
plot_by_id(dataid)
saveplot(name,dataid)     

a,dataid,c=sweep1D(VG1,-1200,-1800,1201,0.012,ph2)                
plot_by_id(dataid)
a,dataid,c=sweep1D(VG2,-1200,-1800,1201,0.012,ph2)                
plot_by_id(dataid)       

VG6(-1800)
VG5(-1500)
VG1(-1500)
VG2(-1500)


