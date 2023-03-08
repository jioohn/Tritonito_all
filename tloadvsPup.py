# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 20:26:51 2021

@author: G-GRE-GRE050402
"""

amplimV=-0.29
namefile='C:\\Users\\g-gre-gre050402\\Documents\\Zurich Instruments\\LabOne\\WebServer\\awg\\src\\diagonal_pulse.seqc'    
def changetload(filename,A):
    lines=open(filename).read().splitlines()
    with open(filename,'r+') as f:
         f.truncate(0)
         lines[31]='const pulseManip_sec =' +str(A)+';'
         for i in range(len(lines)):
             f.write(lines[i]+'\n')   
             #f.writelines()
             
    f.close()   
    
A=amplimV/ampliAWG()/5.5 #renormalize in AWG units

changeAread(namefile, A) 



Npoints=101
tload=np.linspace(5e-6,1000e-6,Npoints)##real amplitudes in mV on G4
Par=[]
    # ampliAWG(0.2)
threshold=-0.1#rad   

phaseD=[]

namefile='C:\\Users\\g-gre-gre050402\\Documents\\Zurich Instruments\\LabOne\\WebServer\\awg\\src\\diagonal_pulse.seqc' 

for i in range(0,Npoints):
    
    print(i)

    changetload(namefile, tload[i]) 
    run_seq('dev2010','diagonal_pulse.seqc')   
    ziUhf.daq.setInt('/dev2010/demods/1/enable', 1)
    ziUhf.daq.setInt('/dev2010/demods/0/enable', 1)
    ziUhf.daq.setInt('/dev2010/sigouts/0/enables/5', 1)
    ziUhf.daq.setInt('/dev2010/demods/1/trigger', 33554432)




    
    
    
    # run_seq('dev2010','pulse_triggerdata_transfer.seqc')   
    # ziUhf.daq.setInt('/dev2010/demods/1/enable', 1)
    # ziUhf.daq.setInt('/dev2010/demods/0/enable', 1)
    
    
    

    delay=Tempty+tload[i]
    # acquisition_duration = Tread # length of time to record (s)cha
    # acquisition_duration = 70e-6 # length of time to record (s)
    
    Ntraces=1000
    
    
    # taxis=np.linspace(delay,acquisition_duration+delay,points)
    # c=daqtrig.get_data(acquisition_duration)
    
    
    
    c,d=daqtrig.get_data_pulseseq(acquisition_duration,delay,Ntraces)
    traceavg=[]

    
    for i in range(0,len(d)):
        traceavg.append(np.mean(d[i]))
            
    phaseD.append(traceavg)
    Pup=0
    singletraces=np.transpose(d)    
    for i in range(0,len(singletraces)):
        if np.min(singletraces[i])<threshold:
            Pup+=1
    
    Pupnorm=Pup/len(singletraces)
    # error=np.std(singletraces[i])
    Par.append(Pupnorm)

plt.figure()
plt.plot(tload*1e6,Par)

# plt.plot(taxis,phase_trigD()[0])
title=str(data_id)+'Pupvstload4_amplimV-'+str(Readlevel())

plt.xlabel('$t_{load} (\mu s)$',fontsize=18)
plt.ylabel('$Pup $',fontsize=18)
# plt.legend()
plt.savefig(folder2+'\\'+dayFolder+'\\'+title+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'Pup.txt',Par)
np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'tload.txt',tload)

np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'rawtraces.txt',singletraces)

###
M=phaseD
#Enregistrement des datas dans un sous dossier convenablement nommé 


title=str(Bfield())+'tloadvsPup--Tempty'+str(Tempty)+'Tload'+str(Tload)+'Tread'+str(Tread)+'G5'+str(VG5())+'mV'

# np.save(pathelzou+f'/El_Zeerman_data'+str(round(Field,2)),M) 
# np.save(pathelzou+f'/El_Zeerman_times'+str(round(Field,2)),t)
# np.save(pathelzou+f'/El_Zeerman_Vread'+str(round(Field,2)),Vreads)
t=np.linspace(delay,acquisition_duration+delay,len(singletraces[0]))
#Enregistrement de la figure tracée 

fig,ax = plt.subplots()
# plt.pcolor(t*1e6,Vreads,np.transpose(M))
plt.pcolor(t*1e6,tload,M)
plt.ylabel('$t_{load}(us)$',fontsize=18)
plt.xlabel('t ($\mu$s)',fontsize=18)
cb=plt.colorbar()
cb.set_label('$\phi_D$ (rad)',fontsize=18)

# ax.tick_params(labelsize=14)
ax.set_title('B='+str(Bfield()),size=18)
fig.tight_layout()


now=datetime.datetime.now()
dayFolder= datetime.date.isoformat(now)
try:
    os.makedirs(folder2+'\\'+dayFolder)
except IOError:
    donothing=1
    
plt.savefig(folder2+'\\'+dayFolder+'\\'+title+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'.txt',M)















Tempty=30e-6
Tload=20e-6
Tread=100e-6

namefile='C:\\Users\\g-gre-gre050402\\Documents\\Zurich Instruments\\LabOne\\WebServer\\awg\\src\\diagonal_pulse.seqc'    


changetempty(namefile, Tempty) 
changetload(namefile, Tload) 
changetread(namefile, Tread) 
#run_seq before!!!

amplimV=-0.6


A=amplimV/ampliAWG()/5.5 #renormalize in AWG units

changeAread(namefile, A) 

run_seq('dev2010','diagonal_pulse.seqc')   
ziUhf.daq.setInt('/dev2010/demods/1/enable', 1)
ziUhf.daq.setInt('/dev2010/demods/0/enable', 1)
ziUhf.daq.setInt('/dev2010/sigouts/0/enables/4', 1)

ziUhf.daq.setInt('/dev2010/demods/0/trigger', 33554432)


#setmw
tburst=15e-6
##set mw gen
mwgen.trigpulses(1)
mwgen.power(5)
mwgen.trigdelay(Tempty+Tload-tburst)
mwgen.burstwidth(tburst) 
mwgen.frequency(16e6)
mwgen.on()





phaseD=[]

amp=[]
Npoints=5001

# Vreads=np.linspace(start,stop,Npoints)##real amplitudes in mV on G4

freq_list=np.linspace(16e9,30e9,Npoints)
# ampliAWG(0.2)
mwgen.on()
mwgen.power(0)
Par=[]


acquisition_duration = Tread +20e-6# length of time to record (s)
delay=Tload+Tempty-20e-6
threshold=0.1

for i in range(0,Npoints):
    mwgen.frequency(freq_list[i])
    # ziUhf.daq.setInt('/dev2010/sigouts/0/enables/5', 1)
    print(i)
    
    
    Ntraces=400
    
    
    # taxis=np.linspace(delay,acquisition_duration+delay,points)
    # c=daqtrig.get_data(acquisition_duration)
    
    
    
    c,d=daqtrig.get_data_pulseseq(acquisition_duration,delay,Ntraces)
    traceavg=[]

    
    for j in range(0,len(d)):
        traceavg.append(np.mean(d[j]))
        
    phaseD.append(traceavg)
    
    Pup=0
    singletraces=np.transpose(d)    
    for k in range(0,len(singletraces)):
        if np.min(singletraces[k])<threshold:
            Pup+=1
    
    Pupnorm=Pup/len(singletraces)
    # error=np.std(singletraces[i])
    Par.append(Pupnorm)
    


M=phaseD
#Enregistrement des datas dans un sous dossier convenablement nommé 


title=str(Bfield())+'try_ampli--0p35_EDSR_'+str(mwgen.power())+'dBm on sample_garound1p4_9usburstonload_Tempty'+str(Tempty)+'Tload'+str(Tload)+'Tread'+str(Tread)+'G5'+str(VG5())+'mV'

# np.save(pathelzou+f'/El_Zeerman_data'+str(round(Field,2)),M) 
# np.save(pathelzou+f'/El_Zeerman_times'+str(round(Field,2)),t)
# np.save(pathelzou+f'/El_Zeerman_Vread'+str(round(Field,2)),Vreads)
t=np.linspace(delay,acquisition_duration+delay,len(singletraces[0]))
#Enregistrement de la figure tracée 

fig,ax = plt.subplots()
# plt.pcolor(t*1e6,Vreads,np.transpose(M))
plt.pcolor(t*1e6,freq_list*1e-9,M)
plt.ylabel('$f (GHz)$',fontsize=18)
plt.xlabel('t ($\mu$s)',fontsize=18)
cb=plt.colorbar()
cb.set_label('$\phi_D$ (Rad)')

ax.tick_params(labelsize=14)
ax.set_title('B='+str(Bfield()),size=18)
fig.tight_layout()


now=datetime.datetime.now()
dayFolder= datetime.date.isoformat(now)
try:
    os.makedirs(folder2+'\\'+dayFolder)
except IOError:
    donothing=1
    
plt.savefig(folder2+'\\'+dayFolder+'\\'+title+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'.txt',M)





plt.figure()
plt.plot(freq_list[0:len(Par)]*1e-9,Par)

# plt.plot(taxis,phase_trigD()[0])
title=str(data_id)+'Pup_-vsfrequency_'

plt.xlabel('$f(GHz)$')
plt.ylabel('$Pup $')
# plt.legend()
plt.savefig(folder2+'\\'+dayFolder+'\\'+title+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'Pup.txt',Par)
np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'Vread.txt',Vreads)

np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'rawtraces.txt',singletraces)