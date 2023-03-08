# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 02:01:47 2021

@author: G-GRE-GRE050402
"""



# num_point=11
# Ntraces=30
num_point=41
Ntraces=300


# startG4=-975
# stopG4=-978
# startG3=-764.5
# stopG3=-763
# Ntraces=300

ampliAWG(0.05)
plot_correlations(num_point,Ntraces,startG4,stopG4,startG3,stopG3)


ampliAWG(0.1)
plot_correlations(num_point,Ntraces,startG4,stopG4,startG3,stopG3)





ampliAWG(0.15)
plot_correlations(num_point,Ntraces,startG4,stopG4,startG3,stopG3)


ampliAWG(0.1)
plot_correlations(num_point,Ntraces,startG4,stopG4,startG3,stopG3)



ampliAWG(0.05)
plot_correlations(num_point,Ntraces,startG4,stopG4,startG3,stopG3)


def plot_correlations(num_point,Ntraces,startG4,stopG4,startG3,stopG3):
    
    G4ar=np.linspace(startG4,stopG4,num_point)
    
    G3ar=np.linspace(startG3,stopG3,num_point)
    
    correlations=[]
    correlationvals=[]
    decay_S=[]
    decay_D=[]
    
    for i in range (0,len(G4ar)):
        
        VG3comp(G3ar[i])
        VG4comp(G4ar[i])
        print(VG4())
        taxis=np.linspace(0,acquisition_duration*1e6,points)
        decay02S_array=[]
        decay02D_array=[]
        correlation=[]
        correlationval=[]
        
        for k in range(0,Ntraces):
            phase_ssS,phase_ssD=phases_trig()
            phase_ssS=phase_ssS[0]
            phase_ssD=phase_ssD[0]
            # tdecay_S=step_detection(phase_ssS[20:],taxis[20:])
            # tdecay_D=step_detection(phase_ssD[20:],taxis[20:])
            tdecay_S=step_detection(phase_ssS[30:-10],taxis[30:-10])
            tdecay_D=step_detection(phase_ssD[30:-10],taxis[30:-10])
            
            decay02S_array.append(tdecay_S)
            decay02D_array.append(tdecay_D)
            if np.abs(tdecay_S-tdecay_D)<10:
             correlation.append(1)
             correlationval.append(tdecay_S)
            else :
             correlation.append(0)
             
             
        correlations.append(np.mean(correlation))
        correlationvals.append(np.mean(correlationval))
        decay_S.append(np.mean(tdecay_S))
        decay_D.append(np.mean(tdecay_D))
        
    now=datetime.datetime.now()
    dayFolder= datetime.date.isoformat(now)
    try:
        os.makedirs(folder2+'\\'+dayFolder)
    except IOError:
        donothing=1    
    
    fig,ax = plt.subplots()
    plt.plot(G4ar,correlations)
    # plt.pcolor(t*1e6,ampli_list,M)
    plt.ylabel('$correlations$',fontsize=18)
    plt.xlabel('G4 (mV)',fontsize=18)
    # cb=plt.colorbar()
    # cb.set_label('$\phi_D$ (rad)',fontsize=18)
    
    ax.tick_params(labelsize=14)
    ax.set_title('B='+str(np.round(Bfield(),3))+'ampliAWG'+str(np.round(ampliAWG(),4)),size=18)
    fig.tight_layout()
    
    title=str(Bfield())+'T_correlationvsG4_A_pp_'+str(ampliAWG()*11)+'mV__G3'+str(VG3())+'mV_G4'+str(VG4())+'mV' 
    
        
    plt.savefig(folder2+'\\'+dayFolder+'\\'+title+'.png')
    np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'.txt',correlations)
    
    
    
    fig,ax = plt.subplots()
    plt.plot(G4ar,correlationvals)
    # plt.pcolor(t*1e6,ampli_list,M)
    plt.ylabel('$average coincidence time($\mu s$)$',fontsize=18)
    plt.xlabel('G4 (mV)',fontsize=18)
    # cb=plt.colorbar()
    # cb.set_label('$\phi_D$ (rad)',fontsize=18)
    
    ax.tick_params(labelsize=14)
    ax.set_title('B='+str(np.round(Bfield(),3))+'ampliAWG'+str(np.round(ampliAWG(),4)),size=18)
    fig.tight_layout()
    
    title=str(Bfield())+'T_correlationtimevsG4_A_pp_'+str(ampliAWG()*11)+'mV__G3'+str(VG3())+'mV_G4'+str(VG4())+'mV' 
    
        
    plt.savefig(folder2+'\\'+dayFolder+'\\'+title+'.png')
    np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'.txt',correlationvals)
    
    
    
    
    fig,ax = plt.subplots()
    plt.plot(G4ar,correlationvals,label='correlation time')
    plt.plot(G4ar,decay_S,label='G3 jump time')
    plt.plot(G4ar,decay_D,label='G4 jump time')
    # plt.pcolor(t*1e6,ampli_list,M)
    # plt.ylabel('$average coincidence time($\mu s$)$',fontsize=18)
    plt.xlabel('G4 (mV)',fontsize=18)
    # cb=plt.colorbar()
    # cb.set_label('$\phi_D$ (rad)',fontsize=18)
    
    ax.tick_params(labelsize=14)
    ax.set_title('B='+str(np.round(Bfield(),3))+'ampliAWG'+str(np.round(ampliAWG(),4)),size=18)
    fig.tight_layout()
    
    title=str(Bfield())+'T_alltimesvsG4_A_pp_'+str(ampliAWG()*11)+'mV__G3'+str(VG3())+'mV_G4'+str(VG4())+'mV' 
    plt.legend()
        
    plt.savefig(folder2+'\\'+dayFolder+'\\'+title+'.png')
    # np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'.txt',correlationvals,decay_S,decay_D)
