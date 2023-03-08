# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 11:59:17 2020

@author: G-GRE-GRE050402
"""
continuous_acquisition()
VG3comp(-899.665)
sensor_on_interdot_sweepG4comp(-914.5,-916.5,201,1)



folder=r'C:\Users\g-gre-gre050402\Documents\Zurich Instruments\LabOne\WebServer\awg\src'
#name="\\negativepulse_fixpulsevarywait_triggered.seqc"
#name='\pulse_sequence.txt'
#name='\\balancedpulsemovewindow.seqc'
name="\\pulsing.seqc"
namefile=folder+name

def changetpulse(filename,t):
    lines=open(filename).read().splitlines()
    with open(filename,'r+') as f:
         f.truncate(0)
         lines[16]='const pulse_sec =' +str(t)+';'
         for i in range(len(lines)):
    
             f.write(lines[i]+'\n')
             
             #f.writelines()
    f.close()
def changeApulse11(filename,A):
    lines=open(filename).read().splitlines()
    with open(filename,'r+') as f:
         f.truncate(0)
         lines[18]='const amplitude11_scaled=' +str(A)+';'
         for i in range(len(lines)):
    
             f.write(lines[i]+'\n')
             
             #f.writelines()
    f.close()    
    
    
def pulsetime(t):
    changetpulse(namefile,t)
    run_seq('dev2010','pulsing.seqc')
    ziUhf.daq.setInt('/dev2010/sigouts/0/enables/0', 1)
    ziUhf.daq.setInt('/dev2010/demods/0/enable', 1)
    ziUhf.daq.setInt('/dev2010/sigouts/1/on', 1)
    
def ampli11(t):
    changeApulse11(namefile,t)
    run_seq('dev2010','pulsing.seqc')
    ziUhf.daq.setInt('/dev2010/sigouts/0/enables/0', 1)
    ziUhf.daq.setInt('/dev2010/demods/0/enable', 1)
    ziUhf.daq.setInt('/dev2010/sigouts/1/on', 1)

changeApulse11(namefile,0.1)


###fit decayvsB
tc=0.10
acquisition_duration =800e-6  # length of time to record (s)
repetitions = 10            # number of repetitions for the averaging
points = 176 # number of points in the acquisition window (min=2)

# acquisition_duration =200e-6
# points = 44


efftc=5e-6

repetitions=400

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
                   ['dataAcquisitionModule/delay', -6e-6], #0                                       # trigger delay (s)
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

# ampli11(0.1)
Bfield(0)
ampliAWG(1)
ziUhf.daq.setInt('/dev2010/sigouts/1/on', 1)   
alpha=0.65

t=np.linspace(0,800e-6,points)
phasearray=[]
amp=[]

for i in range(0,501):
    A=0.001*i
    ampli11(A)
    amp.append(A*ampliAWG()*11/2)
    
    phasearray.append(phase_trig())
ziUhf.daq.setInt('/dev2010/sigouts/1/on', 0)    

phase=[]
for i in range(0,501):
    phase.append(phasearray[i][0])

plt.plot(phase)
Y= amp
X = t
Z1=phase


f = plt.figure()
plt.pcolor(X,Y,Z1,cmap='viridis')
# plt.clim(vmin=None,vmax=0.3)
plt.colorbar(label='phi(deg)')
plt.xlabel('t(s)',fontsize=fontSize)
# plt.ylabel('pulse amplitude_pp (mV)')
plt.ylabel('$\epsilon_{11}$(mV)',fontsize=fontSize)
#draw horizontal line the fixed voltage is @ampliAWG/10
plt.plot((min(X), max(X)), (ampliAWG()*11/6, ampliAWG()*11/6), 'r')
now=datetime.datetime.now()
dayFolder=datetime.date.isoformat(now)
name=str(Bfield())+'T_TP5__timevspulse_amplitudein11_fixedAWGampli'+str(ampliAWG()*1.1)+'_500rep_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',phase)










for j in range(0,6):
Bfield(j*0.1)
ampliAWG(0.650)
ziUhf.daq.setInt('/dev2010/sigouts/1/on', 1)   
alpha=0.55

t=np.linspace(0,800e-6,points)
phasearray=[]
amp=[]

for i in range(0,101):
    A=0.01*i
    ampli11(A)
    amp.append(A*11*ampliAWG()*alpha)
    
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
plt.xlabel('t(s)',fontsize=fontSize)
# plt.ylabel('pulse amplitude_pp (mV)')
plt.ylabel('$\epsilon_{11}$(eV)',fontsize=fontSize)

now=datetime.datetime.now()
dayFolder=datetime.date.isoformat(now)
name=str(Bfield())+'T_TP5_timevspulse_amplitudein11_200ns_in11_totnAWGampli'+str(ampliAWG()*11)+'_500rep_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',phase)
