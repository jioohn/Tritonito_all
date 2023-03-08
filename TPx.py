# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 15:04:27 2021

@author: G-GRE-GRE050402
"""

continuous_acquisition()
bias()
for i in range(0,4):
    if i%2==0:
        dac.dac17(-20)
    else:   
       dac.dac17(0) 
    time.sleep(3600)
    
    VG3comp(-925)
    VG4comp(-800)
    rampVG1(-1490.1)
    rampVG2(-1160.2)
    rampVG5(500)
    # VG1(-1490)
    # VG2(-1135)
    
    continuous_acquisition()
    
    ziUhf.daq.setInt('/dev2010/sigouts/1/on', 0)
    G1now=VG1()
    G2now=VG2()
    G3now=VG3()
    G4now=VG4()
    G5now=VG5()
    VG3comp()
    VG4comp()
    # VG2onmin(G2now-30,G2now+30,801,1)
    G2now=VG2()
    VG1onmin(G1now-20,G1now+20,801,1)
    G1now=VG1()
    VG1onmin(G1now-4,G1now+4,801,1)
    G1now=VG1()
    VG2onmin(G2now-10,G2now+10,801,1)
    G2now=VG2()
    # VG5onmin_ph2(G5now-10,G5now+10,801,1)
    G5now=VG5()
    
    continuous_acquisition()
    name=str(Bfield())+'G4vsG3_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
    a,dataid,c,d=sweep2D(VG3comp,-950,-900,251,0.02,VG4comp,-750,-850,301,0.02,ph1)
    # a,dataid,c,d=sweep2D(VG3comp,-917,-911,61,0.02,VG4comp,-785,-793,81,0.02,ph1)
    plot_by_id(dataid)
    saveplot(name,dataid)








VG3comp(-932.45)
sensor_on_interdot_sweepG4comp(-779,-782,201,1)

tc=0.10
acquisition_duration =600e-6  # length of time to record (s)
repetitions = 10            # number of repetitions for the averaging
points = 132 # number of points in the acquisition window (min=2)

#efftc=acquisition_duration/10
efftc=5e-6

# such that the effective Tc is 100ms 
# repetitions=tc/efftc/5

repetitions=1000

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


for i in range(0,101):
    ampliAWG(-1+i*0.02)
    amp.append(ampliAWG())
    phasearray.append(phase_trig())
ziUhf.daq.setInt('/dev2010/sigouts/1/on', 0)    

phase=[]
for i in range(0,101):
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
name=str(Bfield())+'T_TP5x_pulsevspulse_amplitude_500rep_B'+str(Bfield())+'T_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV'
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',phase)