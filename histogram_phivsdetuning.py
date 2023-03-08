# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 15:39:58 2021

@author: G-GRE-GRE050402
"""

path=pathS
Threshold=Threshold_S

path='S:\\132-PHELIQS\\132.05-LATEQS\\132.05.01-QuantumSilicon\\Tritonito\\2021\\Feb2021_6G22_2_die103\\data\\2021-04-22\\test'



num_point=6
tc=2e-6
total_time=1
demod_S=2
demod_D=1
startG4=-977.8
stopG4=-978.8
startG3=-764.4
stopG3=-763.8
pathS=folder2+'\\'+dayFolder+'\\'+str(Bfield())+'_T_G30to1_VG3='+str(startG3)+'_mV_VG4='+str(startG4)+'mV_phS_'
path2S = pathS + f'/time_traces'
pathD=folder2+'\\'+dayFolder+'\\'+str(Bfield())+'_T_G30to1VG3='+str(startG3)+'_mV_VG4='+str(startG4)+'mV_phD_'
path2D = pathD + f'/time_traces'


# register_time_trace_interdot(daq_S,startG4,stopG4, startG3,stopG3,num_point,tc,total_time,demod_S,pathS,path2S)



def phasevsdetuning_counts_S(startG4,stopG4,startG3,stopG3,num_point,tc,total_time,path,path2) :
    
    ziUhf.daq.setDouble('/'+uhfRef+'/demods/{}/timeconstant'.format(2-1),tc)

    path2=path+'\\timetraces_counts'
    path_ex=np.array([])

    try : 
        os.mkdir(path)
    except :
        print('Dossier existant')
    try : 
        os.mkdir(path2)
    except :
        print('Dossier existant')

    G4ar=np.linspace(startG4,stopG4,num_point)
    
    G3ar=np.linspace(startG3,stopG3,num_point)
    Mx=[]
    My=[]
    bins=401
    minrange=-0.0015
    maxrange=0.001
    minrange=0.00015
    maxrange=0.00025
#     for i,j in enumerate(profondeur) :
    # for i in trange(len(G4ar)):
    #     path_register=path2+f'/vG3=%smV_vg4=%smV'%(round(VG3(),3),round(VG4(),3))
    #     if i==0 :
    #         # VG3(Vgw4+j)
    #         # VG4(Vgw5+coeff_dir*j) 
    #         VG4comp(G4ar[i])
    #         VG3comp(G3ar[i])
    #         daq_S.get_data_bin(total_time,path_register)
            
    #     else :     
    #         VG4comp(G4ar[i])
    #         VG3comp(G3ar[i])

    #         daq_S.get_data_bin(total_time,path_register,header=False,affichage=False)
            
    #     path_ex=np.append(path_ex,path_register)  
              
    for i in trange(len(G4ar)):
        path_register=path2+f'/vG3=%smV_vg4=%smV'%(round(VG3(),3),round(VG4(),3))
 
        VG4comp(G4ar[i])
        VG3comp(G3ar[i])

        daq_S.get_data_bin(total_time,path_register,header=False,affichage=False)
            
 
        
        title='TEST'
        pathtxt=path+'\\'+title+'.txt'     
        daq_S.get_data_txt(total_time,pathtxt,'x','y',affichage=False)
    
        data=np.loadtxt(pathtxt)
        file=open(pathtxt)
        read=file.read()
        file.close()
        read=read[1:read.find('\n')]
        parameters=read.split(';')
    
        for i,stringi in enumerate(parameters) :
            if parameters[i].find('x')>=0 :
                xvalues=data[:,i]
                xlabel=stringi
            if parameters[i].find('y')>=0 :
                yvalues=data[:,i]
                ylabel=stringi
    
       
        px=np.histogram(xvalues,bins,range=(minrange,maxrange))
        py=np.histogram(yvalues,bins,range=(minrange,maxrange))
        Mx.append(px[0])
    
    
    
    # plt.hist(yvalues,201)



    bins_ax=np.linspace(minrange, maxrange,len(px[1])-1)
    title=str(Bfield())+'T_phase_S_histogram2D_G5'+str(VG5())+'mV_G4'+str(VG4())+'mV_G3'+str(VG3())+'mV_'
    
    
    #Enregistrement de la figure tracée 
    len(Mx)
    Mx=np.transpose(Mx)
    fig,ax = plt.subplots()
    # plt.pcolor(t*1e6,Vreads,np.transpose(M))
    plt.pcolor(G4ar,bins_ax,Mx)
    plt.ylabel('$y(Volt)$',fontsize=18)
    plt.xlabel('$VG_4 (mV)$',fontsize=18)
    cb=plt.colorbar()
    cb.set_label('$counts_S$ ')
    
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
    np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'.txt',Mx) 






def phasevsdetuning_counts_D(startG4,stopG4,startG3,stopG3,num_point,tc,total_time,path,path2) :
    
    ziUhf.daq.setDouble('/'+uhfRef+'/demods/{}/timeconstant'.format(1-1),tc)

    path2=path+'\\timetraces_counts'
    path_ex=np.array([])

    try : 
        os.mkdir(path)
    except :
        print('Dossier existant')
    try : 
        os.mkdir(path2)
    except :
        print('Dossier existant')

    G4ar=np.linspace(startG4,stopG4,num_point)
    
    G3ar=np.linspace(startG3,stopG3,num_point)
    Mx=[]
    My=[]
    bins=401
    minrange=-0.0015
    maxrange=0.001
    minrange=0.00025
    maxrange=0.00045
#     for i,j in enumerate(profondeur) :
    # for i in trange(len(G4ar)):
    #     path_register=path2+f'/vG3=%smV_vg4=%smV'%(round(VG3(),3),round(VG4(),3))
    #     if i==0 :
    #         # VG3(Vgw4+j)
    #         # VG4(Vgw5+coeff_dir*j) 
    #         VG4comp(G4ar[i])
    #         VG3comp(G3ar[i])
    #         daq_S.get_data_bin(total_time,path_register)
            
    #     else :     
    #         VG4comp(G4ar[i])
    #         VG3comp(G3ar[i])

    #         daq_S.get_data_bin(total_time,path_register,header=False,affichage=False)
            
    #     path_ex=np.append(path_ex,path_register)  
              
    for i in trange(len(G4ar)):
        path_register=path2+f'/vG3=%smV_vg4=%smV'%(round(VG3(),3),round(VG4(),3))
 
        VG4comp(G4ar[i])
        VG3comp(G3ar[i])

        daq_D.get_data_bin(total_time,path_register,header=False,affichage=False)
            
 
        
        title='TEST'
        pathtxt=path+'\\'+title+'.txt'     
        daq_D.get_data_txt(total_time,pathtxt,'x','y',affichage=False)
    
        data=np.loadtxt(pathtxt)
        file=open(pathtxt)
        read=file.read()
        file.close()
        read=read[1:read.find('\n')]
        parameters=read.split(';')
    
        for i,stringi in enumerate(parameters) :
            if parameters[i].find('x')>=0 :
                xvalues=data[:,i]
                xlabel=stringi
            if parameters[i].find('y')>=0 :
                yvalues=data[:,i]
                ylabel=stringi
    
       
        px=np.histogram(xvalues,bins,range=(minrange,maxrange))
        py=np.histogram(yvalues,bins,range=(minrange,maxrange))
        Mx.append(px[0])
    
    
    
    # plt.hist(yvalues,201)



    bins_ax=np.linspace(minrange, maxrange,len(px[1])-1)
    title=str(Bfield())+'T_phase_D_histogram2D_G5'+str(VG5())+'mV_G4'+str(VG4())+'mV_G3'+str(VG3())+'mV_'
    
    
    #Enregistrement de la figure tracée 
    len(Mx)
    Mx=np.transpose(Mx)
    fig,ax = plt.subplots()
    # plt.pcolor(t*1e6,Vreads,np.transpose(M))
    plt.pcolor(G4ar,bins_ax,Mx)
    plt.ylabel('$y(Volt)$',fontsize=18)
    plt.xlabel('$VG_4 (mV)$',fontsize=18)
    cb=plt.colorbar()
    cb.set_label('$counts_D$ ')
    
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
    np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'.txt',Mx) 

