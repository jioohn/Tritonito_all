# -*- coding: utf-8 -*-
"""
Created on Mon May 17 01:36:09 2021

@author: G-GRE-GRE050402
"""
Vds=0.5
finalgate=-2000
initgate=0
opengate=-2000
# opengate=0
Npoints=501
folder2=r'S:\132-PHELIQS\132.05-LATEQS\132.05.01-QuantumSilicon\Tritonito\2021\Feb2021_6G22_2_die103\data'


def func(): 
	return dmm.volt.get() * 1e-8

current = qc.Parameter('current', instrument=dmm, get_cmd=func,get_parser=float)


###measurements routine for 6G devices


# opengate5=-2000
#here write temp, device and bias

# T='5G23_2-_T__440mK__Vmet'+str(int(dac.dac17()))+'V_'+str(int(bias()*1000))+'uVbias_gates_'+str(opengate)+'mV_G5'+str(opengate5)+'mV_'

#change this line to choose directory where you save stuff


now=datetime.datetime.now()
dayFolder= datetime.date.isoformat(now)
try:
    os.makedirs(folder2+'\\'+dayFolder)
except IOError:
    donothing=1


bias(Vds)
# T='6G22_2_-400mK_Vmet'+str(int(dac.dac17()))+'_Vbias'+str(int(bias()*1000))+'uVbias_gates_'+str(opengate)+'mV_allphi'
T='6G22_2__--440mK_Vmet'+str(int(dac.dac17()))+'_Vbias'+str(int(bias()*1000))+'uVbias_gates_'+str(opengate)+'mV'
#measure
#scanG1

Npoints=1501
rampVG1(initgate)
rampVG2(opengate)
rampVG3(opengate)
rampVG4(opengate)
rampVG5(opengate)
rampVG6(opengate)

a,b,c=sweep1D(VG1,initgate,finalgate,Npoints,0.01,current)

name='G1scan_'+T
plot_by_id(b)
saveplot(name,b)


#measure
#scanG2
rampVG1(opengate)
rampVG2(initgate)
rampVG3(opengate)
rampVG4(opengate)
rampVG5(opengate)
rampVG6(opengate)
# time.sleep(20)#for capa
a,b,c=sweep1D(VG2,initgate,finalgate,Npoints,0.01,current)

name='G2scan_'+T
xlabel='$V_{G2}$(mV)'
ylabel='$I_d$(A)'
plot_by_id(b)
saveplot(name,b)


#measure
#scanG3
rampVG1(opengate)
rampVG2(opengate)
rampVG3(initgate)
rampVG4(opengate)
rampVG5(opengate)
rampVG6(opengate)

time.sleep(5)
a,b,c=sweep1D(VG3,initgate,finalgate,Npoints,0.01,current)

name='G3scan_'+T
xlabel='$V_{G3}$(mV)'
ylabel='$I_d$(A)'
plot_by_id(b)
saveplot(name,b)



#measure
#scanG4
rampVG1(opengate)
rampVG2(opengate)
rampVG3(opengate)
rampVG4(initgate)
rampVG5(opengate)
rampVG6(opengate)
a,b,c=sweep1D(VG4,initgate,finalgate,Npoints,0.01,current)

name='G4scan'+T
xlabel='$V_{G4}$(mV)'
ylabel='$I_d$(A)'
plot_by_id(b)
saveplot(name,b)

#measure
#scanG5
rampVG1(opengate)
rampVG2(opengate)
rampVG3(opengate)
rampVG4(opengate)
rampVG5(initgate)
rampVG6(opengate)

a,b,c=sweep1D(VG5,initgate,finalgate,Npoints,0.01,current)

name='G5scan_'+T
xlabel='$V_{G5}$(mV)'
ylabel='$I_d$(A)'
plot_by_id(b)
saveplot(name,b)

rampVG1(opengate)
rampVG2(opengate)
rampVG3(opengate)
rampVG4(opengate)
rampVG5(opengate)
rampVG6(initgate)
a,b,c=sweep1D(VG6,initgate,finalgate,Npoints,0.01,current)


name='G6scan_'+T
xlabel='$V_{G6}$(mV)'
ylabel='$I_d$(A)'
plot_by_id(b)
saveplot(name,b)

bias(-0.22)
dac.set_dacs_zero()
