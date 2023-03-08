# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 17:42:50 2021

@author: G-GRE-GRE050402
"""



Tempty=30e-6
Tload=200e-6
Tread=200e-6

namefile='C:\\Users\\g-gre-gre050402\\Documents\\Zurich Instruments\\LabOne\\WebServer\\awg\\src\\diagonal_pulse.seqc'    


changetempty(namefile, Tempty) 
changetload(namefile, Tload) 
changetread(namefile, Tread) 
#run_seq before!!!

Readlevel()

# Bfield(1.32)


# Bfield(1.33)
phaseD=[]


Npoints=601

# Vreads=np.linspace(start,stop,Npoints)##real amplitudes in mV on G4


# ampliAWG(0.2)
mwgen.on()
mwgen.power(0)
##
mwgen.frequency(27.1485e9)
###
Par=[]


# acquisition_duration = Tread +20e-6# length of time to record (s)
# delay=Tload+Tempty-20e-6
threshold=-0.1
tburstar=np.linspace(0e-6,6e-6,Npoints)


for i in range (0,len(tburstar)):
# tburst=6-6
##set mw gen
    mwgen.trigpulses(1)

    mwgen.trigdelay(Tempty+Tload-tburstar[i])
    mwgen.burstwidth(tburstar[i]) 

    mwgen.on()

   
    print(i)
    
    
    Ntraces=10000
    
    
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


title=str(Bfield())+'_bursttimevstime__'+str(Readlevel())+'__EDSR_'+str(mwgen.power())+'dBmurstonload' +str(tburst)+'_Tempty'+str(Tempty)+'Tload'+str(Tload)+'Tread'+str(Tread)+'G5'+str(VG5())+'mV'

# np.save(pathelzou+f'/El_Zeerman_data'+str(round(Field,2)),M) 
# np.save(pathelzou+f'/El_Zeerman_times'+str(round(Field,2)),t)
# np.save(pathelzou+f'/El_Zeerman_Vread'+str(round(Field,2)),Vreads)
t=np.linspace(delay,acquisition_duration+delay,len(singletraces[0]))
#Enregistrement de la figure tracée 

fig,ax = plt.subplots()
# plt.pcolor(t*1e6,Vreads,np.transpose(M))
plt.pcolor(t*1e6,tburstar*1e6,M)
plt.ylabel('$t_{burst} (GHz)$',fontsize=18)
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
plt.plot(tburstar*1e6,Par)

# plt.plot(taxis,phase_trigD()[0])
title=str(Bfield())+'_Pupvstburst__'+str(Readlevel())+'__EDSR_'+str(mwgen.power())+'dBmurstonload' +str(tburst)+'_Tempty'+str(Tempty)+'Tload'+str(Tload)+'Tread'+str(Tread)+'G5'+str(VG5())+'mV'

plt.xlabel(r'$ \tau_{burst}$ $ (\mu s)$',fontsize=18)
plt.ylabel('$Pup $',fontsize=18)
# plt.legend()
plt.savefig(folder2+'\\'+dayFolder+'\\'+title+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'Pup.txt',Par)
np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'Vread.txt',Vreads)

np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'rawtraces.txt',singletraces)

mwgen.off()



