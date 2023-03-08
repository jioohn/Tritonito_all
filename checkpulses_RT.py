# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 19:27:47 2021

@author: G-GRE-GRE050402
"""

rampVG1(opengate)
# rampVG2(initgate)
rampVG3(opengate)
rampVG4(opengate)
rampVG5(opengate)

rampVG2(-550)

a,dataid,c=sweep1D(VG4,0,-1500,101,0.01,current)

name='G2scan_'
xlabel='$V_{G2}$(mV)'
ylabel='$I_d$(A)'
plot_by_id(dataid)
saveplot(name,dataid)

rampVG2(-550)
time.sleep(2)

carr=[]
tarr=[]
t0=time.time()
# tarr.append(time.time()-t0)
# carr.append(current())

for i in range(0,50):
    tarr.append(time.time()-t0)
    carr.append(current())


f = plt.figure()
plt.plot(tarr,carr)
# plt.plot(carr)
plt.ylabel('current(A)')
plt.xlabel('t(s)')
# # plt.ylabel('pulse amplitude_pp (mV)')
# plt.ylabel('pulse amplitude_pp (AWG)')   
name='G2pulsetest_100mspulses'
plt.savefig(folder2+'//'+dayFolder+'//'+name)



rampVG2(-2000)
rampVG3(-550)
time.sleep(2)
carr=[]
tarr=[]
t0=time.time()
# tarr.append(time.time()-t0)
# carr.append(current())

for i in range(0,50):
    tarr.append(time.time()-t0)
    carr.append(current())


f = plt.figure()
plt.plot(tarr,carr)
# plt.plot(carr)
plt.ylabel('current(A)')
plt.xlabel('t(s)')
# # plt.ylabel('pulse amplitude_pp (mV)')
# plt.ylabel('pulse amplitude_pp (AWG)')   
name='G3pulsetest_100mspulses'
plt.savefig(folder2+'//'+dayFolder+'//'+name)


rampVG3(-2000)
rampVG4(-600)
time.sleep(2)
carr=[]
tarr=[]
t0=time.time()
# tarr.append(time.time()-t0)
# carr.append(current())

for i in range(0,50):
    tarr.append(time.time()-t0)
    carr.append(current())


f = plt.figure()
plt.plot(tarr,carr)
# plt.plot(carr)
plt.ylabel('current(A)')
plt.xlabel('t(s)')
# # plt.ylabel('pulse amplitude_pp (mV)')
# plt.ylabel('pulse amplitude_pp (AWG)')   
name='G4pulsetest_100mspulses'
plt.savefig(folder2+'//'+dayFolder+'//'+name)




rampVG4(-2000)
rampVG5(-550)
time.sleep(2)
carr=[]
tarr=[]
t0=time.time()
# tarr.append(time.time()-t0)
# carr.append(current())

for i in range(0,50):
    tarr.append(time.time()-t0)
    carr.append(current())


f = plt.figure()
plt.plot(tarr,carr)
# plt.plot(carr)
plt.ylabel('current(A)')
plt.xlabel('t(s)')
# # plt.ylabel('pulse amplitude_pp (mV)')
# plt.ylabel('pulse amplitude_pp (AWG)')   
name='G5pulsetest_100mspulses'
plt.savefig(folder2+'//'+dayFolder+'//'+name)