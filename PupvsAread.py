# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 18:34:25 2021

@author: G-GRE-GRE050402
"""

Npoints=21
Vreads=np.linspace(-0.2,-0.8,Npoints)##real amplitudes in mV on G4
Par=[]
    # ampliAWG(0.2)
threshold=-0.1#rad   
phaseD=[]
for i in range(0,Npoints):
    
    amplimV=Vreads[i]
    print(i)
    
    Readlevel(amplimV)




    
    
    Ntraces=2000
    
    

    # c=daqtrig.get_data(acquisition_duration)
    
    
    
    c,d=daqtrig.get_data_pulseseq(acquisition_duration,delay,Ntraces)
    traceavg=[]

    
    for j in range(0,len(d)):
        traceavg.append(np.mean(d[j]))
    phaseD.append(traceavg)
    Pup=0
    singletraces=np.transpose(d)    
    for i in range(0,len(singletraces)):
        # np.min(scipy.signal.savgol_filter(singletraces[i],3,1))
        if np.min(singletraces[i])<threshold:
            Pup+=1
    
    Pupnorm=Pup/len(singletraces)

    Par.append(Pupnorm)


plt.figure()
plt.plot(Vreads,Par)

# plt.plot(taxis,phase_trigD()[0])
title=str(data_id)+'Pup-vsVread__'

plt.xlabel('$V_{read} (mV)$',size=fontSize)
plt.ylabel('$Pup $',size=fontSize)
# plt.legend()
plt.savefig(folder2+'\\'+dayFolder+'\\'+title+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'Pup.txt',Par)
np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'Vread.txt',Vreads)

np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'rawtraces.txt',singletraces)



taxis=np.linspace(delay,acquisition_duration+delay,len(singletraces[0]))
plt.figure()
plt.plot(taxis*1e6,traceavg, label='average 10000 traces')

# plt.plot(taxis,phase_trigD()[0])
title=str(data_id)+'sstraces'
plt.plot(taxis*1e6,singletraces[1],label='spin down ')
plt.plot(taxis*1e6,singletraces[121],label='spin up')
plt.plot(taxis*1e6,scipy.signal.savgol_filter(singletraces[0],3,1))
         
         
plt.xlabel('$t(\mu s)$',size=fontSize)
plt.ylabel('$\phi(rad)$',size=fontSize)
plt.legend()
plt.savefig(folder2+'\\'+dayFolder+'\\'+title+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'.txt',d)






M=phaseD
title=str(Bfield())+'ampli_readvssignal_Tempty'+str(Tempty)+'Tload'+str(Tload)+'Tread'+str(Tread)+'G5'+str(VG5())+'mV'

# np.save(pathelzou+f'/El_Zeerman_data'+str(round(Field,2)),M) 
# np.save(pathelzou+f'/El_Zeerman_times'+str(round(Field,2)),t)
# np.save(pathelzou+f'/El_Zeerman_Vread'+str(round(Field,2)),Vreads)
t=np.linspace(delay,acquisition_duration+delay,len(singletraces[0]))
#Enregistrement de la figure tracée 

fig,ax = plt.subplots()
# plt.pcolor(t*1e6,Vreads,np.transpose(M))
plt.pcolor(t*1e6,Vreads,M)
plt.ylabel('$A_{read} (mV)$',fontsize=18)
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



