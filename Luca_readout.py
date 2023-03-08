# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 16:33:54 2021

@author: G-GRE-GRE050402
"""


slopeG3G2=-0.30199999999999816
slopeG4G2=-0.022000000000025464
slopeG3G5=-0.013999999999987267
slopeG4G5=-0.21200000000003455

VG4comp=  SpecialParameters.CompensateG4_double(VG4,VG5,VG2,slopeG4G5,slopeG4G2)
VG3comp=  SpecialParameters.CompensateG3_double(VG3,VG5,VG2,slopeG3G5,slopeG3G2)



#set trigger such that it acquires in read

continuous_acquisition()
continuous_acquisition_ch2()

# Bfield(0)

mwgen.off()
#Drain detector calib in 02
rampVG3(-846.5)
rampVG4(-832.5)
VG5now=VG5()
VG2now=VG2()
VG6now=VG6()
VG1now=VG1()
VG3now=VG3()
VG4now=VG4()
# 1089_0.899T_MWon10dB_5GHz_G3vsG4COMP_G1-1672.3mV_G2-1377.1969mV_G3-845.0mV_G4-834.0mV_G5-1471.0487mV_G6-1593.2417mV2
# VG6onmin_phD(VG6now-20,VG6now+20,801,1)
VG5onmin_phD(VG5now-5,VG5now+5,401,1)


#Source detector calib in 11
VG3comp(-848)
VG4comp(-830)
VG5now=VG5()
VG2now=VG2()
VG6now=VG6()
VG1now=VG1()
VG3now=VG3()
VG4now=VG4()
# VG1onmin_phS(VG1now-20,VG1now+20,801,1)
VG2onmin_phS(VG2now-5,VG2now+5,401,1)

# mwgen.on()
# mwgen.power(16)
name=str(Bfield())+'T_G3vsG4COMP_mWoff_nom_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
a,dataid,c,d=sweep2D(VG3comp,-849,-845,41,0.05,VG4comp,-829,-833,51,0.02,ph1,ph2)
# a,dataid,c,d=sweep2D(VG3comp,-847,-845,101,0.05,VG4comp,-831,-833,101,0.02,ph1,ph2)
plot_by_id(dataid)
save2plots(name,dataid)

plot2d_diff(dataid)

######################################
VG3comp(-847)
VG4comp(-831.4)
####################
folder=r'C:\Users\g-gre-gre050402\Documents\Zurich Instruments\LabOne\WebServer\awg\src'
#name="\\negativepulse_fixpulsevarywait_triggered.seqc"
#name='\pulse_sequence.txt'
#name='\\balancedpulsemovewindow.seqc'
name="\\diagonal_pulse.seqc"
namefile=folder+name


def changeAread(filename,A):
    lines=open(filename).read().splitlines()
    with open(filename,'r+') as f:
         f.truncate(0)
         lines[16]='const amplitude11_scaled=' +str(A)+';'
         for i in range(len(lines)):
    
             f.write(lines[i]+'\n')
             
             #f.writelines()
    f.close()

def changetramp(filename,A):
    lines=open(filename).read().splitlines()
    with open(filename,'r+') as f:
         f.truncate(0)
         lines[14]='const pulseramp_sec =' +str(A)+';'
         for i in range(len(lines)):
             f.write(lines[i]+'\n')   
             #f.writelines()
    f.close()
    
def changet11(filename,A):
    lines=open(filename).read().splitlines()
    with open(filename,'r+') as f:
         f.truncate(0)
         lines[13]='const pulse_sec =' +str(A)+';'
         for i in range(len(lines)):
             f.write(lines[i]+'\n')   
             #f.writelines()
    f.close()   
    



ampliAWG(0.2)
tramp=200e-9
t02=10e-6
t11=10e-6
tread=10e-6
burst_time=9e-6
##set mw gen
mwgen.power(-10)
mwgen.trigdelay(t02+tramp+t11-burst_time)
mwgen.burstwidth(burst_time)
# mwgen.frequency(?)

#set pulses
amplimV=0.150
A=amplimV/ampliAWG()/5.5
changeAread(namefile, A) 
changet11(namefile, t11) 
changetramp(namefile, tramp) 
run_seq('dev2010','diagonal_pulse.seqc')   
ziUhf.daq.setInt('/dev2010/demods/1/enable', 1)
ziUhf.daq.setInt('/dev2010/demods/0/enable', 1)
# ziUhf.daq.setInt('/dev2010/sigouts/0/enables/4', 1)
# ziUhf.daq.setInt('/dev2010/sigouts/0/enables/5, 1)


#set_triggeracquisition
# trigger_mode() 
tc=0.5
acquisition_duration =tread  # length of time to record (s)
# repetitions = 10            # number of repetitions for the averaging
points = 10  # number of points in the acquisition window (min=2)

#efftc=acquisition_duration/10
efftc=1e-6

# such that the effective Tc is 100ms 
# repetitions=tc/efftc/5

repetitions=100

ziUhf.daq.setInt('/dev2010/demods/0/trigger', 33554432) # demodulator trigger set on AWGtrigger2 High
ziUhf.daq.setDouble('/dev2010/demods/0/rate', 800e3)
ziUhf.daq.setDouble('/dev2010/demods/1/rate', 800e3)
ziUhf.daq.setInt('/dev2010/demods/0/order', 1)
ziUhf.daq.setDouble('/dev2010/demods/0/timeconstant', efftc)

ziUhf.daq.setInt('/dev2010/demods/1/order', 1)
ziUhf.daq.setDouble('/dev2010/demods/1/timeconstant', efftc)
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
trigger_setting_S = [['dataAcquisitionModule/triggernode', '/dev2010/demods/1/sample.TrigAWGTrig3'],  # trigger node is AWG trigger number 3 
#                   ['dataAcquisitionModule/type', 2],      
                   ['dataAcquisitionModule/type', 6],                                          # this setting is related to the AWG trigger
                   ['dataAcquisitionModule/edge', 1],                                               # trigger on the positive edge. 1 = positive, 2=negative
                   ['dataAcquisitionModule/count', 1],                                              # number of trigger events to count
                   ['dataAcquisitionModule/holdoff/time', 0],                                       # hold off time
                   ['dataAcquisitionModule/holdoff/count', 0],                                      # hold off count
                   ##careful
                   ['dataAcquisitionModule/delay', t02+tramp*2+t11], #0                                       # trigger delay (s)
                   ##
                   ['dataAcquisitionModule/endless', 0]]          
                                  # endless disabled = 0
trigger_setting_D = [['dataAcquisitionModule/triggernode', '/dev2010/demods/0/sample.TrigAWGTrig3'],  # trigger node is AWG trigger number 3 
#                   ['dataAcquisitionModule/type', 2],      
                    ['dataAcquisitionModule/type', 6],                                          # this setting is related to the AWG trigger
                    ['dataAcquisitionModule/edge', 1],                                               # trigger on the positive edge. 1 = positive, 2=negative
                    ['dataAcquisitionModule/count', 1],                                              # number of trigger events to count
                    ['dataAcquisitionModule/holdoff/time', 0],                                       # hold off time
                    ['dataAcquisitionModule/holdoff/count', 0],                                      # hold off count
                    ##careful
                    ['dataAcquisitionModule/delay', t02+tramp*2+t11], #0                                       # trigger delay (s)
                    ##
                    ['dataAcquisitionModule/endless', 0]]                                            # endless disabled = 0

grid_setting =    [['dataAcquisitionModule/grid/mode', 2],                          # mode. 2 = Linear interpolation 
                   ['dataAcquisitionModule/grid/cols', points],                     # number of points in the acquisition window
                   ['dataAcquisitionModule/duration', acquisition_duration],        # length of time to record (s)
                   ['dataAcquisitionModule/grid/rows', 1],                          # rows
                   ['dataAcquisitionModule/grid/direction', 0],                     # scan direction. 0 = forwardphase_pulsed = SpecialParameters.Pulsed_readout(ziUhf, repetitions, returnOnePoint=False)
                   ['dataAcquisitionModule/grid/repetitions', repetitions],         # number of repetitions for the averaging
                   ['dataAcquisitionModule/awgcontrol', 1],                         # set the AWG control
                   ['dataAcquisitionModule/save/fileformat', 1]]                    # 1 = CSV format 


phase_trigS= SpecialParameters.Pulsed_readout_S(ziUhf, repetitions, returnOnePoint=True)
phase_trigD= SpecialParameters.Pulsed_readout_D(ziUhf, repetitions, returnOnePoint=True)
#phase_pulsed_B3= Pulsed_readout_B3(ziUhf, repetitions, returnOnePoint=True)
phase_trigS.setSettings(trigger_setting_S, grid_setting)
phase_trigD.setSettings(trigger_setting_D, grid_setting)

ziUhf.daq.setInt('/dev2010/demods/1/trigger', 33554432)
ziUhf.daq.setInt('/dev2010/demods/0/trigger', 33554432)

ziUhf.daq.setInt('/dev2010/sigouts/0/enables/4', 1)
ziUhf.daq.setInt('/dev2010/sigouts/0/enables/5', 1)

ampliAWG(0.2)#1mV
mwgen.on()
mwgen.power(20)
# name=str(Bfield())+'T_freqvsdetuning_power-10dBm_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
# mwgen.on()
# a,dataid,c,d=sweep2D(mwgen.frequency,13e9,18e9,5000,0.01,G4detuning,-831,-832.5,201,0.01,ph1,ph2)
# plot_by_id(dataid)
# save2plots(name,dataid)

phaseS=[]
phaseD=[]
amplitudeS=[]
amplitudeD=[]
alist=np.linspace(-0.65,-0.75,11)##real amplitudes in MV

# f1=1.4*bohr*Bfield_Hon()/h
flist=np.linspace(16e9,16.5e9,251)
# epsread=[]
for j in range(0,len(alist)):
    
    amplimV=alist[j]
    phiD=[]
    phiS=[]
    amps=[]
    ampd=[]
    
    A=amplimV/ampliAWG()/5.5

    changeAread(namefile, A) 
    # changet11(namefile, t11) 
    # changet11(namefile, tramp) 
    run_seq('dev2010','diagonal_pulse.seqc')   
    ziUhf.daq.setInt('/dev2010/demods/1/enable', 1)
    ziUhf.daq.setInt('/dev2010/demods/0/enable', 1)
    ziUhf.daq.setInt('/dev2010/sigouts/0/enables/4', 1)
    ziUhf.daq.setInt('/dev2010/sigouts/0/enables/5', 1)
    
    for i in range(0,len(flist)):

        mwgen.frequency(flist[i])
        phiS.append(phase_trigS())
        phiD.append(phase_trigD())
        # ampd.append(A1())
        # amps.append(A2())
    # G1min.append(phimin-ph1())
    phaseS.append(phiS)    
    phaseD.append(phiD)  



#######
tag='seq3stage_'
name=tag+'phid_epsreadvsfreq G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV__G6'+str(VG6())+'mV'
Y= alist[0:len(phaseD)]
X = flist

Z1=phaseD
Z=np.reshape(Z1,(len(Y),len(X)))


f = plt.figure()
plt.pcolor(X,Y,Z,cmap='viridis')
# plt.clim(vmin=None,vmax=0.3)
plt.colorbar(label='$\phi_D(rad)$')
plt.ylabel('$\epsilon_R$ (mV)')
# plt.ylabel('pulse amplitude_pp (mV)')
plt.xlabel('f(Hz)')
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',Z)

################"
name=tag+'phis_epsreadvsfreq G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV__G6'+str(VG6())+'mV'
Y= alist[0:len(phaseD)]
X = flist
Z1=phaseS
Z=np.reshape(Z1,(len(Y),len(X)))
f = plt.figure()
plt.pcolor(X,Y,Z,cmap='viridis')
# plt.clim(vmin=None,vmax=0.3)
plt.colorbar(label='$\phi_S(rad)$')
plt.ylabel('$\epsilon_R$ (mV)')
# plt.ylabel('pulse amplitude_pp (mV)')
plt.xlabel('f(Hz)')
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',Z)
