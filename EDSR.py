# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 01:38:46 2021

@author: G-GRE-GRE050402
"""





Tempty=40e-6
Tload=150-6
Tread=200e-6

namefile='C:\\Users\\g-gre-gre050402\\Documents\\Zurich Instruments\\LabOne\\WebServer\\awg\\src\\diagonal_pulse.seqc'    



changetempty(namefile, Tempty) 
changetload(namefile, Tload) 
changetread(namefile, Tread) 

run_seq('dev2010','diagonal_pulse.seqc')
ziUhf.daq.setInt('/dev2010/demods/1/enable', 1)
# ziUhf.daq.setInt('/dev2010/demods/0/enable', 1)
ziUhf.daq.setInt('/dev2010/sigouts/0/enables/5', 1)
ziUhf.daq.setInt('/dev2010/demods/1/trigger', 33554432)
        


#run_seq before!!!

# delay=Tload+Tempty
# acquisition_duration=50e-6

Readlevel(-0.65)


tburst=10-6
##set mw gen
mwgen.trigpulses(1)
mwgen.power(5)
mwgen.trigdelay(Tempty+Tload-tburst-1e-6)
mwgen.burstwidth(tburst) 
# mwgen.frequency(16e6)
mwgen.on()




# Bfield(1.33)
phaseD=[]

amp=[]
Npoints=81

# Vreads=np.linspace(start,stop,Npoints)##real amplitudes in mV on G4

freq_list=np.linspace(25.1e9,25.5e9,Npoints)
# ampliAWG(0.2)
mwgen.on()
# mwgen.power(-5)
Par=[]


# acquisition_duration = Tread +20e-6# length of time to record (s)
# delay=Tload+Tempty-20e-6
threshold=-0.1

for i in range(0,Npoints):
    mwgen.frequency(freq_list[i])
    # ziUhf.daq.setInt('/dev2010/sigouts/0/enables/5', 1)
    print(i)
    
    
    Ntraces=5000
    
    
    # taxis=np.linspace(delay,acquisition_duration+delay,points)
    # c=daqtrig.get_data(acquisition_duration)
    
    
    
    c,d=daqtrig.get_data_pulseseq(acquisition_duration,delay,Ntraces)
    traceavg=[]

    
    for j in range(0,len(d)):
        traceavg.append(np.nanmean(d[j]))
        
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


title=str(Bfield())+'_ampli____'+str(Readlevel())+'__EDSR_'+str(mwgen.power())+'dBmurstonload' +str(tburst)+'_Tempty'+str(Tempty)+'Tload'+str(Tload)+'Tread'+str(Tread)+'G5'+str(VG5())+'mV'

# np.save(pathelzou+f'/El_Zeerman_data'+str(round(Field,2)),M) 
# np.save(pathelzou+f'/El_Zeerman_times'+str(round(Field,2)),t)
# np.save(pathelzou+f'/El_Zeerman_Vread'+str(round(Field,2)),Vreads)
t=np.linspace(delay,acquisition_duration+delay,len(singletraces[0]))
#Enregistrement de la figure tracée 

fig,ax = plt.subplots()
# plt.pcolor(t*1e6,Vreads,np.transpose(M))
plt.pcolor(t*1e6,freq_list[0:len(phaseD)]*1e-9,M)
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
plt.plot(freq_list[0:len(phaseD)]*1e-9,Par)

# plt.plot(taxis,phase_trigD()[0])
title=str(Bfield())+'_Pupvs_freq_'+str(Readlevel())+'__EDSR_'+str(mwgen.power())+'dBmurstonload' +str(tburst)+'_Tempty'+str(Tempty)+'Tload'+str(Tload)+'Tread'+str(Tread)+'G5'+str(VG5())+'mV'

plt.xlabel('$f(GHz)$')
plt.ylabel('$Pup $')
# plt.legend()
plt.savefig(folder2+'\\'+dayFolder+'\\'+title+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'Pup.txt',Par)
# np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'Vread.txt',Vreads)

np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'rawtraces.txt',singletraces)

mwgen.off()



