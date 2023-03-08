# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 11:44:51 2021

@author: G-GRE-GRE050402
"""
250_-0.0T_G3vsG4_G1-1670.095mV_G2-1055.2522mV_G3-763.5mV_G4-979.0mV_G5-1344.2537000000002mV_G6-1862.8mV
def config250():
    rampVG1(-1670)
    rampVG2(-1055)
    rampVG3(-763)
    rampVG4(-979)
    rampVG5(-1344)
    rampVG6(-1863)
    bias(-0.2)
G1-1694.945mV_G2-1057.3429999999998mV_G3-821.0mV_G4-845.0mV_G5-1368.6309999999999mV_G6-1865.385mV2

def config1537():
    rampVG1(-1694)
    rampVG2(-1055)
    rampVG3(-821)
    rampVG4(-945)
    rampVG5(-1368)
    rampVG6(-1863)
    bias(-0.2)
##################

continuous_acquisition()
continuous_acquisition_ch2()
VG3comp(-764)
VG4comp(-976)
VG5now=VG5()
VG2now=VG2()
VG6now=VG6()
VG1now=VG1()

# # VG6onmin_phD(VG6now-10,VG6now+10,401,1)
VG6onmin_phD(VG6now-3,VG6now+3,401,1)

VG1onmin_phS(VG1now-3,VG1now+3,401,1)
# VG1onmin_phS(VG1now-30,VG1now+30,401,1)

# VG5onmin_phD(VG5now-10,VG5now+10,401,1)

# # VG1onmin_phS(VG1now-10,VG1now+10,401,1)
# VG2onmin_phS(VG2now-10,VG2now+10,401,1)

continuous_acquisition()
continuous_acquisition_ch2()

name=str(Bfield())+'T_CALIB_G3vsG4_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
# a,dataid,c,d=sweep2D(VG3comp,-762,-766,41,0.02,VG4comp,-976,-982,61,0.014,ph1,ph2)
a,dataid,c,d=sweep2D(VG3comp,-766,-762,41,0.02,VG4comp,-973,-978,41,0.014,ph1,ph2)
plot_by_id(dataid)
save2plots(name,dataid)


# save2plots(name,dataid)


daq_S =DAM(ziUhf, 2)
daqtrig_S= DAMTrig(ziUhf,2)
daq_D =DAM(ziUhf, 1)
daqtrig_D= DAMTrig(ziUhf,1)

####################""


num_point=201
tc=2e-6
total_time=1
demod_S=2
demod_D=1
startG4=-975
stopG4=-976.2
startG3=-764.6
stopG3=-764
pathS=folder2+'\\'+dayFolder+'\\'+str(Bfield())+'_T_G30to1_VG3='+str(startG3)+'_mV_VG4='+str(startG4)+'mV_phS_'
path2S = pathS + f'/time_traces'
pathD=folder2+'\\'+dayFolder+'\\'+str(Bfield())+'_T_G30to1VG3='+str(startG3)+'_mV_VG4='+str(startG4)+'mV_phD_'
path2D = pathD + f'/time_traces'

continuous_acquisition()
continuous_acquisition_ch2()
Threshold_S,Threshold_D=fit_interdot(startG4,stopG4,startG3,stopG3)#plot, fit and sit on interdot

Threshold_S=Threshold_S*np.pi/180
Threshold_D=Threshold_D*np.pi/180

G3now=VG3()
G4now=VG4()
#bubbles SNR on interdot for phiS
title='IQ_On_interdot_tc'+str(tc)
VG3comp(G3now)
VG4comp(G4now)
blopIQ_interdot(daq_S,tc,total_time,demod_S,pathS,title=title)

VG3comp(startG3)
VG4comp(startG4)
title='IQ_in11_tc'+str(tc)


blopIQ_interdot(daq_S,tc,total_time,demod_S,pathS,title='IQ_in11_tc'+str(tc))

VG3comp(stopG3)
VG4comp(stopG4)
title='IQ_in02_tc'+str(tc)


blopIQ_interdot(daq_S,tc,total_time,demod_S,pathS,title='IQ_in02_tc'+str(tc))

path_dbb=[pathS + '\\IQ_in11_tc'+str(tc)+'.txt',pathS + '\\IQ_in02_tc'+str(tc)+'.txt']


draw_multiple_bbl_interdot(path_dbb,pathS)

#bubbles SNR on interdot for phiD
VG3comp(G3now)
VG4comp(G4now)
title='IQ_On_interdot_tc'+str(tc)

blopIQ_interdot(daq_D,tc,total_time,demod_D,pathD,title=title)

VG3comp(startG3)
VG4comp(startG4)
title='IQ_in11_tc'+str(tc)


blopIQ_interdot(daq_D,tc,total_time,demod_D,pathD,title='IQ_in11_tc'+str(tc))

VG3comp(stopG3)
VG4comp(stopG4)
title='IQ_in02_tc'+str(tc)


blopIQ_interdot(daq_D,tc,total_time,demod_D,pathD,title='IQ_in02_tc'+str(tc))

path_dbb=[pathD + '\\IQ_in11_tc'+str(tc)+'.txt',pathD + '\\IQ_in02_tc'+str(tc)+'.txt']


draw_multiple_bbl_interdot(path_dbb,pathD)


######analysis of occupation probabilities and tunnel rate
    
register_time_trace_interdot(daq_S,startG4,stopG4, startG3,stopG3,num_point,tc,total_time,demod_S,pathS,path2S)

gammarate=analyse_time_traces_interdot(pathS,startG4,stopG4,startG3,stopG3,Threshold_S)
  


register_time_trace_interdot(daq_D,startG4,stopG4, startG3,stopG3,num_point,tc,total_time,demod_D,pathD,path2D)

gammarate=analyse_time_traces_interdot(pathD,startG4,stopG4,startG3,stopG3,Threshold_D)
  

####2dmap phase distribution vs detuning


#I can use same data as ones used to extract tunnel coupling-->2d histogram of phase

def analyse_time_traces_interdot(path,start,stop,startG3,stopG3,Threshold) :
    
    print(path)
    file = path+'\\paths.txt'
    with open(file) as f:
        for line in f:
                paths = line.split(";")
#     Name = re.sub('../../exploration','',path)       
    Ps_up = []
    Ps_down = []
    Ts_up = []
    Ts_down = []
    for i in trange(len(paths)-1):
        path1 = paths[i]
        data = np.load(path1+'.npy')
        P_up,P_down,T_up,T_down = Occupations_and_times(data,Threshold, Do_plot = False)
        Ps_up.append(P_up)
        Ps_down.append(P_down)
        Ts_up.append(T_up)
        Ts_down.append(T_down)

    # Vg = np.linspace(-0.3,0.3,len(Ps_up))   
    
    eps=np.sqrt((start-stop)**2 +(startG3-stopG3)**2) 
    
    Vg = np.linspace(0,eps,len(Ps_up))    

    ## Plot the occupations up/down:
    fig,ax = plt.subplots()
    plt.plot(Vg,Ps_up)
    plt.plot(Vg,Ps_down)
    plt.xlabel('$\epsilon$ (mV)',fontsize=18)
    plt.ylabel('$P_{11},P_{02}$',fontsize=18)
    ax.tick_params(labelsize=14)
    ax.set_title('Occupations'+str(Bfield())+'T',size=18)
    fig.tight_layout()
    plt.savefig(path+'\\'+str(Bfield())+'T_Occupation.png')

    ## Plot the tunnel rates:
    gamma_up = 1/np.array(Ts_up)
    gamma_down = 1/np.array(Ts_down)

    gamma_up[gamma_up>1e300]=0  
    gamma_down[gamma_down>1e300]=0  
    
    fig,ax = plt.subplots()
    
    plt.plot(Vg,gamma_up*1e-3,'+',label='$\Gamma_{out}$')
    plt.plot(Vg,gamma_down*1e-3,'+',label='$\Gamma_{in}$')
    


    if np.max(gamma_up)>100e3 or np.max(gamma_down)>100e3:
        plt.ylim(0,100)
        
    plt.xlabel('$\epsilon$ (mV)',fontsize=18)
    plt.ylabel('$\Gamma_{in},\Gamma_{out}$ (kHz)',fontsize=18)
    ax.tick_params(labelsize=14)
    ax.set_title('Rates '+str(Bfield())+'T',size=18)
    fig.tight_layout()
    plt.legend()
    plt.savefig(path+'//'+str(Bfield())+'T_Rates.png')

    # title='gamma_rates'
    
    # try : 
    #     os.mkdir(path_register)
    # except :
    #     print('Dossier existant')

    # fig.savefig(path+'\\'+title,dpi=600)
    
    crossing=np.argmin(np.abs(gamma_up-gamma_down))

    
    return gamma_up[crossing] #, Vg[crossing]     
        
def register_time_trace_interdot(DAM,startG4,stopG4,startG3,stopG3,num_point,tc,total_time,demod,path,path2) :
    
    ziUhf.daq.setDouble('/'+uhfRef+'/demods/{}/timeconstant'.format(demod-1),tc)
    ziUhf.daq.setDouble('/'+uhfRef+'/demods/{}/rate'.format(demod-1),1/tc)
    
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
#     for i,j in enumerate(profondeur) :
    for i in trange(len(G4ar)):
        path_register=path2+f'/vG3=%smV_vg4=%smV'%(round(VG3(),3),round(VG4(),3))
        if i==0 :
            # VG3(Vgw4+j)
            # VG4(Vgw5+coeff_dir*j) 
            VG4comp(G4ar[i])
            VG3comp(G3ar[i])
            DAM.get_data_bin(total_time,path_register)
            
        else :     
            VG4comp(G4ar[i])
            VG3comp(G3ar[i])

            DAM.get_data_bin(total_time,path_register,header=False,affichage=False)
            
        path_ex=np.append(path_ex,path_register)  
               
    text_file = open(path+f'\paths.txt', "w")
    for i in path_ex : 
        text_file.write(i + f';')
    text_file.close()   
        
    return(path_ex)    



def Occupations_and_times(array,Threshold, Do_plot = False):
#     import time
    '''
    #### Function that takes as input an array, corresponding to a phase versus time trace ###

    array: must be an array of the time trace. First column = Time, Second column = phase 
    Threshold: value of the signal chosen to separate the two detected states
    
    returns the normlaized probablities of begin up or down, as well as the average times spent up and down in seconds

    '''
   
    T = array[:,0]
    PH = array[:,1]
    tstep = T[1]-T[0]
    Ttot = len(T)*tstep
    
    if Do_plot == True:
        f = plt.figure()
        f = plt.plot(T,PH)
    Ts_up = [0]
    Ts_down = [0]
#     t0 = time.time()
    j = 0
    for i,ph in enumerate(PH):
        if ph > Threshold:
            if i > 1 and PH[i-1] < Threshold:
                Ts_up.append(1)
                j = j+1
            elif i > 1 and PH[i-1] > Threshold:
                Ts_up[j] = Ts_up[j] + 1

    j = 0
    for i,ph in enumerate(PH):
        if ph < Threshold:
            if i > 1 and PH[i-1] < Threshold:
                Ts_down[j] = Ts_down[j] + 1  
            elif i > 1 and PH[i-1] > Threshold:
                Ts_down.append(1)
                j = j+1
    
    P_up = sum(Ts_up)/len(PH)
    P_down = sum(Ts_down)/len(PH)
    T_up = np.mean(Ts_up)*tstep    # time spent in the two different states
    T_down = np.mean(Ts_down)*tstep 
#     t1 = time.time()
#     print('Done in', t1-t0 , 's')
    return P_up,P_down,T_up,T_down


# pathh,-0.2,0.2,Threshold,str(round(j,3)),str(round(i,3))





        





def fit_interdot(startG4,stopG4,startG3,stopG3):
    
    detuningPoint1 = [startG3,startG4]  #TPC #G3,G4
    detuningPoint2 = [stopG3,stopG4] 
    
    detpoints=201
    detuning = qc.combine(VG3, VG4, name = 'detuning', unit= 'points')
    eps=np.sqrt((detuningPoint1[0]-detuningPoint2[0])**2 +(detuningPoint1[1]-detuningPoint2[1])**2) 
    VG3comp(detuningPoint1[0])
    VG4comp(detuningPoint1[1])
    
    det=generateEpsilonAxis(detuningPoint1, detuningPoint2, detpoints)
    eps=np.sqrt((detuningPoint1[0]-detuningPoint2[0])**2 +(detuningPoint1[1]-detuningPoint2[1])**2) 
    epsilon=np.linspace(-eps/2,eps/2,detpoints)
    
    
    tag='TP0_'
    phases=[]
    
    
    
    phasedet_D=[]
    phasedet_S=[]
    for i in range(0,len(det)):
    
        VG3comp(det[i][0])
        VG4comp(det[i][1])
        time.sleep(0.02)
        phasedet_S.append(ph2())
        phasedet_D.append(ph1())
        
    datasmooth_S=scipy.signal.savgol_filter(np.ravel(phasedet_S),11, 3)
    phimin=np.min(datasmooth_S)
    phimax=np.max(datasmooth_S)
    argmin=np.argmin(datasmooth_S)
    kmin=0
    kmax=0
    
    philim_S=phimin+(phimax-phimin)/2
    T=0.44
    sigmaphi=0.5#deg
    # for k in range(0,len(data_set)):
    #         if ((data_get[0][k]>=(philim-sigmaphi) and data_get[0][k]<=(philim+sigmaphi)) and kmax==0):
    #             kmax=k
    for k in range(0,len(epsilon)):
        if ((  datasmooth_S[k]>=(philim_S-sigmaphi) and   datasmooth_S[k]<=(philim_S+sigmaphi)) and kmax==0):
            kmax=k
            print('ok')
    
        
    # VG3comp(det[kmax][0])
    # VG4comp(det[kmax][1])
    # VG3comp(det[kmax][0])
    # VG4comp(det[kmax][1])
    
    # xaxis=np.multiply(np.subtract(data_set,data_set[kmax]),1e-3)
    xaxis=np.multiply(np.subtract(epsilon,epsilon[kmax]),1e-3)
    datasmooth2=np.subtract(datasmooth_S,phimin)
    
    xaxis2=np.array(xaxis,dtype=float)
    datasmooth2=np.array(datasmooth2,dtype=float)
    
    
    xaxis2=np.reshape(xaxis2,201)
    datasmooth2=np.reshape(datasmooth2,201)
    
    fig, ax = plt.subplots()
    ax.set_xlabel('$\epsilon$ (V)',fontsize=fontSize)
    ax.set_ylabel('$\phi_S $(rad)',fontsize=fontSize)
    
    plt.title('Fit at T='+str(T)+'K')
    plt.plot(xaxis,datasmooth2,'b+',label='data@'+str(T)+'K')#mV on x  
    plt.legend(loc='upper right')
    plt.show()
    
    
    
    alpha=0.4
    const=phimin
    offset=phimin+(phimax-phimin)
    
     
    popt,pcov = curve_fit(interdotfit_chargesensor,xaxis2,datasmooth2,p0=[alpha,0,1],maxfev=10000) 
    plt.plot(xaxis2,interdotfit_chargesensor(xaxis2,*popt))    
    
    
    alpha=popt[0] 
    
    er=np.sqrt(np.diag(pcov))
    erroralpha=er[0]
    # errortunnel=er[3]
    # print('Teff='+str(Teff))
    # Tarray.append(Teff)
    # errorTarray.append(errortemp)
    
    # tunnelarray.append(tunnel)
    # tunnelarrayerr.append(errortunnel)
    
    # errortunnel=errortunnel/h*10e-9#conv to Ghz
    plt.plot(xaxis,interdotfit_chargesensor(xaxis2,*popt),'r',label='alpha='+str( round(alpha,2)) +'$\pm$'+str( round(erroralpha,2))+'_eV/V')#,t='+str( round(tunnel,3))+'$\pm$'+str(round(errortunnel,3))+'_GHz, alpha='+str(alpha))
    #    plt.plot(xaxis,interdotfit_chargesensor(xaxis,*popt),'r',label='Teff='+str( round(Teff,2)) +'$\pm$'+str( round(errortemp,2))+'_K,t='+str( round(tunnel,3))+'$\pm$'+str(round(errortunnel,3))+'_GHz, alpha='+str(alpha))
    plt.legend(loc='upper right')
    plt.show()
    name=tag+str(dataid)+'phi_S_0p44K_findalphadetunig_tnegligible__G4init'+str(startG4)+'mV_1dscan-'+str(Bfield())+'_T_'
    # fig.savefig(foldername2+'0.44K_Tonly_TP9_1dscan-'+str(Bfield())+'_T_ampliAWG'+str(ampliAWG())+'.png') 
    # np.savetxt(foldername2+'0.44K_Tonly_TP9_1dscan-'+str(Bfield())+'_T_ampliAWG'+str(ampliAWG())+'.txt',datasmooth2)
    
    plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
    np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',datasmooth2)
    
    #############################################
    
    datasmooth_D=scipy.signal.savgol_filter(np.ravel(phasedet_D),11, 3)
    phimin=np.min(datasmooth_D)
    phimax=np.max(datasmooth_D)
    argmin=np.argmin(datasmooth_D)
    kmin=0
    kmax=0
    
    philim_D=phimin+(phimax-phimin)/2
    T=0.44
    sigmaphi=0.5#deg
    # for k in range(0,len(data_Det)):
    #         if ((data_get[0][k]>=(philim-sigmaphi) and data_get[0][k]<=(philim+sigmaphi)) and kmax==0):
    #             kmax=k
    for k in range(0,len(epsilon)):
        if ((  datasmooth_D[k]>=(philim_D-sigmaphi) and   datasmooth_D[k]<=(philim_D+sigmaphi)) and kmax==0):
            kmax=k
            print('ok')
    
        
    VG3comp(det[kmax][0])
    VG4comp(det[kmax][1])
    VG3comp(det[kmax][0])
    VG4comp(det[kmax][1])
    
    # xaxis=np.multiply(np.subtract(data_Det,data_Det[kmax]),1e-3)
    xaxis=np.multiply(np.subtract(epsilon,epsilon[kmax]),1e-3)
    datasmooth2=np.subtract(datasmooth_D,phimin)
    
    xaxis2=np.array(xaxis,dtype=float)
    datasmooth2=np.array(datasmooth2,dtype=float)
    
    
    xaxis2=np.reshape(xaxis2,201)
    datasmooth2=np.reshape(datasmooth2,201)
    
    fig, ax = plt.subplots()
    ax.set_xlabel('$\epsilon$ (V)',fontsize=fontSize)
    ax.set_ylabel('$\phi_D $(rad)',fontsize=fontSize)
    
    plt.title('Fit at T='+str(T)+'K')
    plt.plot(xaxis,datasmooth2,'b+',label='data@'+str(T)+'K')#mV on x  
    plt.legend(loc='upper right')
    plt.show()
    
    
    
    alpha=0.55
    const=phimin
    offset=phimin+(phimax-phimin)
    
     
    popt,pcov = curve_fit(interdotfit_chargesensor,xaxis2,datasmooth2,p0=[alpha,0,1],maxfev=10000) 
    plt.plot(xaxis2,interdotfit_chargesensor(xaxis2,*popt))    
    
    
    alpha=popt[0] 
    
    er=np.sqrt(np.diag(pcov))
    erroralpha=er[0]
    # errortunnel=er[3]
    # print('Teff='+str(Teff))
    # Tarray.append(Teff)
    # errorTarray.append(errortemp)
    
    # tunnelarray.append(tunnel)
    # tunnelarrayerr.append(errortunnel)
    
    # errortunnel=errortunnel/h*10e-9#conv to Ghz
    plt.plot(xaxis,interdotfit_chargesensor(xaxis2,*popt),'r',label='alpha='+str( round(alpha,2)) +'$\pm$'+str( round(erroralpha,2))+'_eV/V')#,t='+str( round(tunnel,3))+'$\pm$'+str(round(errortunnel,3))+'_GHz, alpha='+str(alpha))
    #    plt.plot(xaxis,interdotfit_chargesensor(xaxis,*popt),'r',label='Teff='+str( round(Teff,2)) +'$\pm$'+str( round(errortemp,2))+'_K,t='+str( round(tunnel,3))+'$\pm$'+str(round(errortunnel,3))+'_GHz, alpha='+str(alpha))
    plt.legend(loc='upper right')
    plt.show()
    name=tag+str(dataid)+'phiD_0p44K_findalphadetunig_tnegligible_G4init'+str(startG4)+'mV_1dscan-'+str(Bfield())+'_T_'
    # fig.savefig(foldername2+'0.44K_Tonly_TP9_1dscan-'+str(Bfield())+'_T_ampliAWG'+str(ampliAWG())+'.png') 
    # np.savetxt(foldername2+'0.44K_Tonly_TP9_1dscan-'+str(Bfield())+'_T_ampliAWG'+str(ampliAWG())+'.txt',datasmooth2)
    
    plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
    np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',datasmooth2)

    return philim_S,philim_D


def blopIQ_interdot(DAM,tc,timetot,demod,path,title='I/Q measure') :
    
    try : 
        os.mkdir(path)
    except :
        print('Dossier existant')
    # try : 
    #     os.mkdir(path2)
    # except :
    #     print('Dossier existant')
    ziUhf.daq.setDouble('/'+uhfRef+'/demods/{}/timeconstant'.format(demod-1),tc)
    ziUhf.daq.setDouble('/'+uhfRef+'/demods/{}/rate'.format(demod-1),1/tc)
    
    pathtxt=path+'\\'+title+'.txt'

    DAM.get_data_txt(timetot,pathtxt,'x','y',affichage=False)

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

    fig = plt.figure(figsize=(10, 10))
    grid = plt.GridSpec(4, 4, hspace=0.3, wspace=0.3)
    
    size = 14
    
    main_ax = fig.add_subplot(grid[:-1, 1:])
    main_ax.set_title('I/Q measure',size=size)
    main_ax.ticklabel_format(axis='both',style='sci',scilimits=[-6,-6])
#     main_ax.set_aspect('equal')

    y_hist = fig.add_subplot(grid[:-1, 0], xticklabels=[], sharey=main_ax)
    y_hist.ticklabel_format(axis='y',style='sci',scilimits=[-6,-6])
    y_hist.set_ylabel(ylabel,fontsize=size)

    x_hist = fig.add_subplot(grid[-1, 1:], yticklabels=[], sharex=main_ax)
    x_hist.ticklabel_format(axis='x',style='sci',scilimits=[-6,-6])
    x_hist.set_xlabel(xlabel,fontsize=size)

    color='darkorange'
    alpha=0.8
    # scatter points on the main axes
    main_ax.plot(xvalues, yvalues, 'ok', markersize=3, alpha=0.2,color=color)
    main_ax.set_aspect('equal')

    # histogram on the attached axes
    x_hist.hist(xvalues, 200,
                orientation='vertical', color=color,alpha=alpha)
    x_hist.invert_yaxis()

    y_hist.hist(yvalues, 200,
                orientation='horizontal', color=color,alpha=alpha)
    y_hist.invert_xaxis()
    
    main_ax.tick_params(labelsize=14)
    x_hist.tick_params(labelsize=14)
    y_hist.tick_params(labelsize=14)

    fig.tight_layout()

    
    fig.savefig(path+'\\'+title+'.png',dpi=600)
    
    



def draw_multiple_bbl_interdot(path,path_register) :

    fig = plt.figure(figsize=(10, 10))
    grid = plt.GridSpec(4, 4, hspace=0.3, wspace=0.3)
    size = 14
    main_ax = fig.add_subplot(grid[:-1, 1:])
    main_ax.set_title('I/Q measure',size=size)
    main_ax.ticklabel_format(axis='both',style='sci',scilimits=[-6,-6])

    y_hist = fig.add_subplot(grid[:-1, 0], xticklabels=[], sharey=main_ax)
    y_hist.ticklabel_format(axis='y',style='sci',scilimits=[-6,-6])

    x_hist = fig.add_subplot(grid[-1, 1:], yticklabels=[], sharex=main_ax)
    x_hist.ticklabel_format(axis='x',style='sci',scilimits=[-6,-6])
    
    color_all=['darkorange','tomato','blue','green','black']
    
    for j,pathh in enumerate(path) :
        data=np.loadtxt(pathh)
        file=open(pathh)
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

        color=color_all[j]
        alpha=0.8
        # scatter points on the main axes
        main_ax.plot(xvalues, yvalues, 'ok', markersize=3, alpha=0.2,color=color)

        # histogram on the attached axes
        x_hist.hist(xvalues, 200,
                    orientation='vertical', color=color,alpha=alpha)
        x_hist.invert_yaxis()

        y_hist.hist(yvalues, 200,
                    orientation='horizontal', color=color,alpha=alpha)
        y_hist.invert_xaxis()
        
    y_hist.set_ylabel(ylabel,fontsize=size)
    x_hist.set_xlabel(xlabel,fontsize=size)
    main_ax.tick_params(labelsize=14)
    x_hist.tick_params(labelsize=14)
    y_hist.tick_params(labelsize=14)
    
    title='\\IQ_double_bbl_tc'+str(tc)
    
    fig.savefig(path_register+f'/'+title,dpi=600)
    
    # patth = f'..\exploration/1-all_Bubbles'

    fig.savefig(path_register+title,dpi=600)

    fig.tight_layout()
