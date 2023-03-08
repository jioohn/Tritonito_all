# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 16:34:40 2021

@author: G-GRE-GRE050402
"""


rampVG1(-1000)
rampVG2(-400)
rampVG3(-800)
rampVG4(-800)
rampVG5(00)
# bias(0)
continuous_acquisition()

name=str(Bfield())+'G1scan'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
a,dataid,c=sweep1D(VG1,-000,-1500,1601,0.02,ph1)
plot_by_id(dataid)
saveplot(name,dataid)

continuous_acquisition()

name=str(Bfield())+'G5scan'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
a,dataid,c=sweep1D(VG5,0,-1500,1501,0.02,ph2)
plot_by_id(dataid)
saveplot(name,dataid)

name=str(Bfield())+'G5scan'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
a,dataid,c=sweep1D(VG5,-2300,-1000,2001,0.02,ph2)
plot_by_id(dataid)
saveplot(name,dataid)

name=str(Bfield())+'G1scan'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
a,dataid,c=sweep1D(VG1,-825,-835,801,0.02,ph1)
plot_by_id(dataid)
saveplot(name,dataid)

ziUhf.daq.setInt('/dev2010/sigouts/1/on', 0)

# Bfield(0)
# time.sleep(3600)
rampVG1(-1300)
rampVG2(-500)
rampVG3(-800)
rampVG4(-500)
rampVG5(-1000)
time.sleep(30)
# time.sleep(30)

continuous_acquisition()
name=str(Bfield())+'config1_G1vsG2_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
a,dataid,c,d=sweep2D(VG1,-1300,-1000,201,0.02,VG2,-500,-1000,601,0.02,ph1)
plot_by_id(dataid)
saveplot(name,dataid)


rampVG1(-1100)
rampVG2(-500)
rampVG3(-800)
rampVG4(-500)
rampVG5(-1000)


continuous_acquisition()
name=str(Bfield())+'config1_G1vsG3_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
a,dataid,c,d=sweep2D(VG1,-1080,-1100,101,0.02,VG3,-500,-900,601,0.02,ph1,ph2)
plot_by_id(dataid)
saveplot(name,dataid)




rampVG1(-1000)
rampVG2(-500)
rampVG3(-800)
rampVG4(-500)
rampVG5(-1000)


continuous_acquisition()
name=str(Bfield())+'config2_G4vsG5_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
a,dataid,c,d=sweep2D(VG5,-1300,-1100,201,0.02,VG4,-900,-1200,301,0.02,ph1,ph2)
plot_by_id(dataid)
saveplot(name,dataid)


rampVG1(-1100)
rampVG2(-500)
rampVG3(-800)
rampVG4(-500)
rampVG5(-1000)
time.sleep(30)

continuous_acquisition()
name=str(Bfield())+'config2_G5vsG3_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
a,dataid,c,d=sweep2D(VG5,-1300,-1280,101,0.02,VG3,-600,-900,301,0.02,ph1,ph2)
plot_by_id(dataid)
saveplot(name,dataid)







rampVG1(-1300)
rampVG2(-500)
rampVG3(-800)
rampVG4(-500)
rampVG5(-1000)
time.sleep(30)
# time.sleep(30)

continuous_acquisition()
name=str(Bfield())+'config1_G1vsG2_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
a,dataid,c,d=sweep2D(VG1,-1050,-1000,101,0.02,VG2,-500,-0,601,0.02,ph1)
plot_by_id(dataid)
saveplot(name,dataid)




VG3comp(-870)
VG4comp(-770)
VG1now=VG1()
VG2now=VG2()

VG1onmin(VG1now-10,VG1now+10,1001,1)
VG1now=VG1()
VG1onmin(VG1now-4,VG1now+4,801,1)
VG1now=VG1()
continuous_acquisition()
name=str(Bfield())+'G4vsG3_Vmet'+str(dac.dac17())+'V_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'

# a,dataid,c,d=sweep2D(VG3comp,-859,-851,81,0.1,VG4comp,-750,-820,141,0.005,ph1,ph2)
# a,dataid,c,d=sweep2D(VG3comp,-870,-900,101,0.1,VG4comp,-750,-800,201,0.005,ph1,ph2)
a,dataid,c,d=sweep2D(VG3comp,-800,-900,201,0.1,VG4comp,-700,-800,201,0.02,ph1)
# a,dataid,c,d=sweep2D(VG3comp,-880,-780,181,0.1,VG4comp,-850,-800,121,0.01,ph1)
plot_by_id(dataid)
saveplot(name,dataid)



VG3comp(-750)
VG4comp(-750)
VG1now=VG1()
VG2now=VG2()


VG1onmin(VG1now-10,VG1now+10,1001,1)
VG1now=VG1()
VG1onmin(VG1now-4,VG1now+4,801,1)
VG1now=VG1()
continuous_acquisition()
name=str(Bfield())+'G4vsG3_Vmet'+str(dac.dac17())+'V_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'

# a,dataid,c,d=sweep2D(VG3comp,-859,-851,81,0.1,VG4comp,-750,-820,141,0.005,ph1,ph2)
# a,dataid,c,d=sweep2D(VG3comp,-870,-900,101,0.1,VG4comp,-750,-800,201,0.005,ph1,ph2)
a,dataid,c,d=sweep2D(VG3comp,-700,-800,201,0.1,VG4comp,-700,-800,201,0.02,ph1)
# a,dataid,c,d=sweep2D(VG3comp,-880,-780,181,0.1,VG4comp,-850,-800,121,0.01,ph1)
plot_by_id(dataid)
saveplot(name,dataid)



# VG3comp(-882)
# VG4comp(-741)
VG3comp(-881)
VG4comp(-746)
VG1now=VG1()
VG2now=VG2()


VG1onmin(VG1now-10,VG1now+10,1001,1)
VG1now=VG1()
VG1onmin(VG1now-4,VG1now+4,801,1)
VG1now=VG1()
continuous_acquisition()
name=str(Bfield())+'G4vsG3_Vmet'+str(dac.dac17())+'V_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'

# a,dataid,c,d=sweep2D(VG3comp,-859,-851,81,0.1,VG4comp,-750,-820,141,0.005,ph1,ph2)
# a,dataid,c,d=sweep2D(VG3comp,-870,-900,101,0.1,VG4comp,-750,-800,201,0.005,ph1,ph2)
a,dataid,c,d=sweep2D(VG3comp,-878,-885,71,0.1,VG4comp,-740,-747,71,0.02,ph1)
# a,dataid,c,d=sweep2D(VG3comp,-880,-780,181,0.1,VG4comp,-850,-800,121,0.01,ph1)
plot_by_id(dataid)
saveplot(name,dataid)


continuous_acquisition()
VG3comp(-882.1)
sensor_on_interdot_sweepG4comp(-742,-745.5,201,1)

tc=0.10
acquisition_duration =600e-6  # length of time to record (s)
repetitions = 10            # number of repetitions for the averaging
points = 132 # number of points in the acquisition window (min=2)

#efftc=acquisition_duration/10
efftc=5e-6

# such that the effective Tc is 100ms 
# repetitions=tc/efftc/5

repetitions=300

ziUhf.daq.setInt('/dev2010/demods/0/trigger', 33554432) # demodulator trigger set on AWGtrigger2 High
ziUhf.daq.setDouble('/dev2010/demods/0/rate', 200e3)
ziUhf.daq.setInt('/dev2010/demods/0/order', 1)
ziUhf.daq.setDouble('/dev2010/demods/0/timeconstant', efftc)
#ziUhf.daq.setInt('/dev2365/awgs/0/enable', 1)      # 1 = enable;   0 = disabled
ziUhf.daq.sync()

#Trigger type used. Some parameters are only valid for special trigger types.
    #0 = trigger off
    #1 = analog edge trigger on source
    #2 = digital trigger mode on DIO source
    #3 = analog pulse trigger on source
    #4 = analog tracking trigger on source
    #5 = change trigger
    #6 = hardware trigger on trigger line source
    #7 = tracking edge trigger on source
    #8 = event count trigger on counter source
    
ziUhf.daq.sync()
trigger_setting = [['dataAcquisitionModule/triggernode', '/dev2010/demods/0/sample.TrigAWGTrig3'],  # trigger node is AWG trigger number 3 
#                   ['dataAcquisitionModule/type', 2],      
                   ['dataAcquisitionModule/type', 6],                                          # this setting is related to the AWG trigger
                   ['dataAcquisitionModule/edge', 1],                                               # trigger on the positive edge. 1 = positive, 2=negative
                   ['dataAcquisitionModule/count', 1],                                              # number of trigger events to count
                   ['dataAcquisitionModule/holdoff/time', 0],                                       # hold off time
                   ['dataAcquisitionModule/holdoff/count', 0],                                      # hold off count
                   ##careful
                   ['dataAcquisitionModule/delay', -5e-6], #0                                       # trigger delay (s)
                   #7
                   ['dataAcquisitionModule/endless', 0]]                                            # endless disabled = 0


grid_setting =    [['dataAcquisitionModule/grid/mode', 2],                          # mode. 2 = Linear interpolation 
                   ['dataAcquisitionModule/grid/cols', points],                     # number of points in the acquisition window
                   ['dataAcquisitionModule/duration', acquisition_duration],        # length of time to record (s)
                   ['dataAcquisitionModule/grid/rows', 1],                          # rows
                   ['dataAcquisitionModule/grid/direction', 0],                     # scan direction. 0 = forwardphase_pulsed = SpecialParameters.Pulsed_readout(ziUhf, repetitions, returnOnePoint=False)
                   ['dataAcquisitionModule/grid/repetitions', repetitions],         # number of repetitions for the averaging
                   ['dataAcquisitionModule/awgcontrol', 1],                         # set the AWG control
                   ['dataAcquisitionModule/save/fileformat', 1]]                    # 1 = CSV format 

phase_trig= SpecialParameters.Pulsed_readout_G1(ziUhf, repetitions, returnOnePoint=False)
#phase_pulsed_B3= Pulsed_readout_B3(ziUhf, repetitions, returnOnePoint=True)
phase_trig.setSettings(trigger_setting, grid_setting)



trigger_mode()
ziUhf.daq.setInt('/dev2010/sigouts/1/on', 1)    
t=np.linspace(0,acquisition_duration,points)
phasearray=[]
amp=[]


for i in range(0,51):
    ampliAWG(+i*0.01)
    amp.append(ampliAWG())
    phasearray.append(phase_trig())
ziUhf.daq.setInt('/dev2010/sigouts/1/on', 0)    

phase=[]
for i in range(0,51):
    phase.append(phasearray[i][0])

plt.plot(phase)
Y= amp
X = t
Z1=phase


f = plt.figure()
plt.pcolor(X,Y,Z1,cmap='viridis')
# plt.clim(vmin=None,vmax=0.3)
plt.colorbar(label='phi(deg)')
plt.xlabel('t(s)')
# plt.ylabel('pulse amplitude_pp (mV)')
plt.ylabel('pulse amplitude_pp (AWG)')

now=datetime.datetime.now()
dayFolder=datetime.date.isoformat(now)
name=str(Bfield())+'T_TPa_pulsevspulse_amplitude_300rep_B'+str(Bfield())+'T_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV'
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',phase)






########################################################################"
VG3comp(-881)
# sensor_on_interdot_sweepG4comp(-742,-745.5,201,1)
continuous_acquisition()
name=str(Bfield())+'BvsG4_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
a,dataid,c,d=sweep2D(Bfield_Hon,4,1,31,1,VG4,-742,-745.5,201,0.02,ph1)
plot_by_id(dataid)
saveplot(name,dataid)

Bfield(1)





VG3comp(-845)
VG4comp(-750)
VG1now=VG1()
VG2now=VG2()

VG1onmin(VG1now-10,VG1now+10,1001,1)
VG1now=VG1()
VG1onmin(VG1now-4,VG1now+4,801,1)
VG1now=VG1()
continuous_acquisition()
name=str(Bfield())+'G4vsG3_Vmet'+str(dac.dac17())+'V_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'

# a,dataid,c,d=sweep2D(VG3comp,-859,-851,81,0.1,VG4comp,-750,-820,141,0.005,ph1,ph2)
# a,dataid,c,d=sweep2D(VG3comp,-870,-900,101,0.1,VG4comp,-750,-800,201,0.005,ph1,ph2)
a,dataid,c,d=sweep2D(VG3comp,-850,-825,101,0.1,VG4comp,-750,-800,101,0.02,ph1)
# a,dataid,c,d=sweep2D(VG3comp,-880,-780,181,0.1,VG4comp,-850,-800,121,0.01,ph1)
plot_by_id(dataid)
saveplot(name,dataid)


VG3comp(-840)
VG4comp(-793)
VG1now=VG1()
VG2now=VG2()

VG1onmin(VG1now-10,VG1now+10,1001,1)
VG1now=VG1()
VG1onmin(VG1now-4,VG1now+4,801,1)
VG1now=VG1()
continuous_acquisition()
name=str(Bfield())+'G4vsG3_Vmet'+str(dac.dac17())+'V_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'

# a,dataid,c,d=sweep2D(VG3comp,-859,-851,81,0.1,VG4comp,-750,-820,141,0.005,ph1,ph2)
# a,dataid,c,d=sweep2D(VG3comp,-870,-900,101,0.1,VG4comp,-750,-800,201,0.005,ph1,ph2)
a,dataid,c,d=sweep2D(VG3comp,-836,-844,101,0.1,VG4comp,-792,-800,101,0.02,ph1)
# a,dataid,c,d=sweep2D(VG3comp,-880,-780,181,0.1,VG4comp,-850,-800,121,0.01,ph1)
plot_by_id(dataid)
saveplot(name,dataid)



VG3comp(-870)
VG4comp(-790)
VG1now=VG1()
VG2now=VG2()

VG1onmin(VG1now-10,VG1now+10,1001,1)
VG1now=VG1()
VG1onmin(VG1now-4,VG1now+4,801,1)
VG1now=VG1()
continuous_acquisition()
name=str(Bfield())+'G4vsG3_Vmet'+str(dac.dac17())+'V_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'

# a,dataid,c,d=sweep2D(VG3comp,-859,-851,81,0.1,VG4comp,-750,-820,141,0.005,ph1,ph2)
# a,dataid,c,d=sweep2D(VG3comp,-870,-900,101,0.1,VG4comp,-750,-800,201,0.005,ph1,ph2)
a,dataid,c,d=sweep2D(VG3comp,-870,-882,101,0.1,VG4comp,-770,-790,201,0.04,ph1)
# a,dataid,c,d=sweep2D(VG3comp,-880,-780,181,0.1,VG4comp,-850,-800,121,0.01,ph1)
plot_by_id(dataid)
saveplot(name,dataid)


Bfield(0)

VG3comp(-870)
VG4comp(-790)
VG1now=VG1()
VG2now=VG2()

VG1onmin(VG1now-10,VG1now+10,1001,1)
VG1now=VG1()
VG1onmin(VG1now-4,VG1now+4,801,1)
VG1now=VG1()
continuous_acquisition()
name=str(Bfield())+'G4vsG3_Vmet'+str(dac.dac17())+'V_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'

# a,dataid,c,d=sweep2D(VG3comp,-859,-851,81,0.1,VG4comp,-750,-820,141,0.005,ph1,ph2)
# a,dataid,c,d=sweep2D(VG3comp,-870,-900,101,0.1,VG4comp,-750,-800,201,0.005,ph1,ph2)
a,dataid,c,d=sweep2D(VG3comp,-870,-882,101,0.1,VG4comp,-770,-790,201,0.04,ph1)
# a,dataid,c,d=sweep2D(VG3comp,-880,-780,181,0.1,VG4comp,-850,-800,121,0.01,ph1)
plot_by_id(dataid)
saveplot(name,dataid)





VG3comp(-825)
VG4comp(-775)
VG1now=VG1()
VG2now=VG2()

VG1onmin(VG1now-10,VG1now+10,1001,1)
VG1now=VG1()
VG1onmin(VG1now-4,VG1now+4,801,1)
VG1now=VG1()
continuous_acquisition()
continuous_acquisition()
name=str(Bfield())+'G4vsG3_Vmet'+str(dac.dac17())+'V_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'

# a,dataid,c,d=sweep2D(VG3comp,-859,-851,81,0.1,VG4comp,-750,-820,141,0.005,ph1,ph2)
# a,dataid,c,d=sweep2D(VG3comp,-870,-900,101,0.1,VG4comp,-750,-800,201,0.005,ph1,ph2)
a,dataid,c,d=sweep2D(VG3comp,-850,-820,51,0.1,VG4comp,-780,-800,201,0.02,ph1)
# a,dataid,c,d=sweep2D(VG3comp,-880,-780,181,0.1,VG4comp,-850,-800,121,0.01,ph1)
plot_by_id(dataid)
saveplot(name,dataid)


for i in range(0,2):
    for j in range(0,2):
        VG3comp(-825-50*i)
        VG4comp(-725-50*j)
        VG1now=VG1()
        VG2now=VG2()
        
        VG1onmin(VG1now-10,VG1now+10,1001,1)
        VG1now=VG1()
        VG1onmin(VG1now-4,VG1now+4,801,1)
        VG1now=VG1()
        continuous_acquisition()
        continuous_acquisition()
        name=str(Bfield())+'G4vsG3_Vmet'+str(dac.dac17())+'V_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
        
        # a,dataid,c,d=sweep2D(VG3comp,-859,-851,81,0.1,VG4comp,-750,-820,141,0.005,ph1,ph2)
        # a,dataid,c,d=sweep2D(VG3comp,-870,-900,101,0.1,VG4comp,-750,-800,201,0.005,ph1,ph2)
        a,dataid,c,d=sweep2D(VG3comp,-800-50*i,-850-50*i,101,0.1,VG4comp,-700-50*j,-750-50*j,101,0.02,ph1)
        # a,dataid,c,d=sweep2D(VG3comp,-880,-780,181,0.1,VG4comp,-850,-800,121,0.01,ph1)
        plot_by_id(dataid)
        saveplot(name,dataid)


VG1(-1130)
rampVG5(-1800)
VG3comp(-775)
VG4comp(-675)
time.sleep(120)
VG1now=VG1()
VG2now=VG2()

Bfield(0)
VG1onmin(VG1now-50,VG1now+50,1001,1)
VG1now=VG1()
VG1onmin(VG1now-4,VG1now+4,801,1)
VG1now=VG1()
continuous_acquisition()


for i in range(0,3):
    for j in range(0,3):
        VG3comp(-775-50*i)
        VG4comp(-725-50*j)
        VG1now=VG1()
        VG2now=VG2()
        VG5now=VG5()
        VG5now=VG5()
        VG1now=VG1()
        VG1onmin(VG1now-4,VG1now+4,801,1)
        VG2onmin(VG2now-5,VG2now+10,1001,1)

        VG1now=VG1()
        continuous_acquisition()

        name=str(Bfield())+'G4vsG3_Vmet'+str(dac.dac17())+'V_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
        
        # a,dataid,c,d=sweep2D(VG3comp,-859,-851,81,0.1,VG4comp,-750,-820,141,0.005,ph1,ph2)
        # a,dataid,c,d=sweep2D(VG3comp,-870,-900,101,0.1,VG4comp,-750,-800,201,0.005,ph1,ph2)
        a,dataid,c,d=sweep2D(VG3comp,-750-50*i,-800-50*i,101,0.1,VG4comp,-700-50*j,-750-50*j,101,0.02,ph1)
        # a,dataid,c,d=sweep2D(VG3comp,-880,-780,181,0.1,VG4comp,-850,-800,121,0.01,ph1)
        plot_by_id(dataid)
        saveplot(name,dataid)


VG1(-1130)
rampVG5(-1800)
VG3comp(-740)
VG4comp(-675)
time.sleep(120)
VG1now=VG1()
VG2now=VG2()

VG1onmin(VG1now-20,VG1now+20,1001,1)
VG1now=VG1()
VG1onmin(VG1now-4,VG1now+4,801,1)
VG1now=VG1()
continuous_acquisition()


for i in range(0,3):
    for j in range(0,3):
        VG3comp(-775-50*i)
        VG4comp(-675-50*j)
        VG1now=VG1()
        VG2now=VG2()
        VG5now=VG5()
        VG5now=VG5()
        VG5onmin_ph2(VG5now-10,VG5now+10,1001,1)
        VG1now=VG1()
        VG1onmin(VG1now-4,VG1now+4,801,1)
        VG1now=VG1()
        continuous_acquisition()

        name=str(Bfield())+'G3vsG4_Vmet'+str(dac.dac17())+'V_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
        
        # a,dataid,c,d=sweep2D(VG3comp,-859,-851,81,0.1,VG4comp,-750,-820,141,0.005,ph1,ph2)
        # a,dataid,c,d=sweep2D(VG3comp,-870,-900,101,0.1,VG4comp,-750,-800,201,0.005,ph1,ph2)
        a,dataid,c,d=sweep2D(VG4comp,-650-50*j,-700-50*j,101,0.1,VG3comp,-750-50*i,-800-50*i,101,0.02,ph1,ph2)
        # a,dataid,c,d=sweep2D(VG3comp,-880,-780,181,0.1,VG4comp,-850,-800,121,0.01,ph1)
        plot_by_id(dataid)
        save2plots(name,dataid)


VG3comp(-805.5)
VG4comp(-756)
VG1now=VG1()
VG2now=VG2()

VG1onmin(VG1now-20,VG1now+20,1001,1)
VG1now=VG1()
VG1onmin(VG1now-4,VG1now+4,801,1)
VG1now=VG1()

continuous_acquisition()
name=str(Bfield())+'G4vsG3_Vmet'+str(dac.dac17())+'V_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'

# a,dataid,c,d=sweep2D(VG3comp,-859,-851,81,0.1,VG4comp,-750,-820,141,0.005,ph1,ph2)
# a,dataid,c,d=sweep2D(VG3comp,-870,-900,101,0.1,VG4comp,-750,-800,201,0.005,ph1,ph2)
a,dataid,c,d=sweep2D(VG3comp,-804,-808,41,0.1,VG4comp,-750,-758,41,0.02,ph1,ph2)
# a,dataid,c,d=sweep2D(VG3comp,-880,-780,181,0.1,VG4comp,-850,-800,121,0.01,ph1)
plot_by_id(dataid)
save2plots(name,dataid)

sensor_on_interdot_sweepG4comp()

rampVG1(-300)
VG3comp(-805.5)
VG4comp(-756)
VG1now=VG1()
VG2now=VG2()

VG1onmin(VG1now-20,VG1now+20,1001,1)
VG1now=VG1()
VG1onmin(VG1now-4,VG1now+4,801,1)
VG1now=VG1()

continuous_acquisition()
name=str(Bfield())+'G4vsG3_Vmet'+str(dac.dac17())+'V_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'

# a,dataid,c,d=sweep2D(VG3comp,-859,-851,81,0.1,VG4comp,-750,-820,141,0.005,ph1,ph2)
# a,dataid,c,d=sweep2D(VG3comp,-870,-900,101,0.1,VG4comp,-750,-800,201,0.005,ph1,ph2)
a,dataid,c,d=sweep2D(VG3comp,-804,-808,41,0.1,VG4comp,-750,-758,41,0.02,ph1,ph2)
# a,dataid,c,d=sweep2D(VG3comp,-880,-780,181,0.1,VG4comp,-850,-800,121,0.01,ph1)
plot_by_id(dataid)
save2plots(name,dataid)

sensor_on_interdot_sweepG4comp()
