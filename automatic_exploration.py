# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 19:52:57 2021

@author: G-GRE-GRE050402
"""
# continuous_acquisition()
# # continuous_acquisition_ch2()
# # VG5(-1100)
# # VG4(-800)
# VG3(-1100)
# VG6onmin_phD(-1500,-1600,1601,1)

# name=str(Bfield())+'T_G4vsG5_N4to5_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
# # a,dataid,c,d=sweep2D(VG5,-1000,-1200,801,0.05,VG4,-760,-860,401,0.01,ph1)
# # plot_by_id(dataid)
# # saveplot(name,dataid)
# VG3(-1100)
# VG6onmin_phD(-1500,-1600,1601,1)
# a,dataid,c,d=sweep2D(VG5,-1200,-1250,201,0.05,VG4,-700,-800,201,0.01,ph1)
# plot_by_id(dataid)
# saveplot(name,dataid)

def changeAread(filename,A):
    lines=open(filename).read().splitlines()
    with open(filename,'r+') as f:
         f.truncate(0)
         lines[16]='const amplitude11_scaled=' +str(A)+';'
         for i in range(len(lines)):
    
             f.write(lines[i]+'\n')
             
             #f.writelines()
    f.close()
    
def changetempty(filename,A):
    lines=open(filename).read().splitlines()
    with open(filename,'r+') as f:
         f.truncate(0)
         lines[30]='const pulseInit_sec =' +str(A)+';'
         for i in range(len(lines)):
             f.write(lines[i]+'\n')   
             #f.writelines()
    f.close()   
    
def changetload(filename,A):
    lines=open(filename).read().splitlines()
    with open(filename,'r+') as f:
         f.truncate(0)
         lines[31]='const pulseManip_sec =' +str(A)+';'
         for i in range(len(lines)):
             f.write(lines[i]+'\n')   
             #f.writelines()
    f.close()   
    
def changetread(filename,A):
    lines=open(filename).read().splitlines()
    with open(filename,'r+') as f:
         f.truncate(0)
         lines[34]='const pulseRead_sec =' +str(A)+';'
         for i in range(len(lines)):
             f.write(lines[i]+'\n')   
             #f.writelines()
    f.close()         


def find_working_point_by_id_inv(data_id,G2f,G3f,Plot = True, savefig = True):
# Function aimed to find the point at which the interdot breaks, starting from the id a of a small plot centered on a G2 transition

    data = qc.load_by_id(data_id)
    VarX=data.get_parameters()[0].unit
    nameX=data.get_parameters()[0].name
    VarY=data.get_parameters()[1].unit
    nameY=data.get_parameters()[1].name
    Varmap=data.get_parameters()[2].unit
    namemap=data.get_parameters()[2].name

    data_list = data.get_parameter_data()
    P = data.parameters
    p = P.split(',')
    X = data_list[p[2]][p[0]]
    Y = data_list[p[2]][p[1]]
    x = (np.unique(X))
    y = np.unique(Y)

    Vg3 = x
    Vg2 = y
    #Z1(Vg2,Vg3)!!!

    z1 = data_list[p[2]][p[2]]
    Z1 = np.transpose(z1.reshape((np.size(np.unique(X)),np.size(np.unique(Y)))))
    
# find maximum along the dot-lead
    ind1 = np.argmax(Z1[0,:])
    V1 = Vg3[ind1]
    Vpk = np.zeros(len(Vg2))
    for i in range(len(Vg2)):
        ind1 = np.argmin(Z1[i,:])
        Vpk[i] = Vg3[ind1]
# fit this maximum with a linear approx, only from the upper part of the plot:

    Ncut = int(len(Vg2)*0.4)  # number of points to take from upper of the scan 
    a,b = np.polyfit(Vg2[-Ncut:],Vpk[-Ncut:], 1)                   #linear fit to extract alpha

    # Extract profile along line:
    profile = np.zeros(len(Vg2))
    Eps = np.zeros(len(Vg2))
    V3 = a*Vg2+b
    delta = abs(Vg3[1]-Vg3[0])
#     delta = 0.015

    for i,V in enumerate(Vg2):
        indVg3 = np.where( (Vg3 > V3[i] - delta) & (Vg3 < V3[i] + delta))
        ind = indVg3[0][0]
        profile[i] = Z1[i,ind]

    # Find Vg2 corresponding to the middle of the jump
    mi = np.max(profile)
    ma = np.min(profile)
    av = (mi+ma)/2
    

    arg=np.argmin(np.abs(scipy.signal.savgol_filter(profile,11, 3)-av))
    

        
        #typicalFWHM is <1.5mVdef VT2onmin(initVB1,finalVB1,points,showplot):
   
    
    
    
    # diff = np.diff(profile)
    # arg = np.where(abs(diff) == np.max(abs(diff)))
    
##################
    V2p = Vg2[arg]
    # Find the corresponding Vg3:
    V3p = a*V2p+b   

#     print(V2p,V3p)
    if Plot == True:
        fig,ax=plt.subplots()
        X,Y = np.meshgrid(x,y)
        f = plt.pcolor(X,Y,Z1)    # 2D plot  
        plt.colorbar(label='$\phi_D(deg)$')
        ax.set_xlabel(nameX+ ' (' + VarX+')')
        ax.set_ylabel(nameY+ ' (' + VarY+')')

        f = plt.plot(Vpk[-Ncut:],Vg2[-Ncut:],color=(0,0,1))     # Plot of the max
        f = plt.plot(a*Vg2+b,Vg2, '--',color = (1,0,0),linewidth = 0.5)     # Plot of the linear fit
        f = plt.scatter(V3p,V2p,color = (1,0,1),marker = 'x',s =150)
        db_name=data.path_to_db[data.path_to_db.find('data')+5:]
        ax.title.set_text('database {} \n data_id {} \n '.format(db_name,data_id))
        plt.tight_layout()
        if savefig == True:
                        
            
#             plt.savefig('../analysis/Triple_points/Vg2='+str(round(V3p*1000)/1000)+'Vg2='+str(round(V2p*1000)/1000)+'.png')
            
                        
            path = f'..\exploration\g4=%s_g5=%s'%(G2f,G3f)

            try : 
                os.mkdir(path)
            except :
                print('Dossier existant')
            Field = Bfield_Hon()
            plt.savefig(path+f'/interdot_working_point_B='+str(round(Field,3))+'T.png',dpi=600)
        
#             plt.savefig(path+f'/interdot_working_point',dpi=600)
        
            path = f'..\exploration/0-all_interdot'

            try : 
                os.mkdir(path)
            except :
                print('Dossier existant')

            plt.savefig(path+f'\g4=%s_g5=%s_working_point'%(str(int(float(G2f))),str(int(float(G3f)))),dpi=600)

    # plot profile:    
    # f = plt.subplot(1,2,2)
    if Plot == True:
        f = plt.figure()
        f = plt.plot(Vg2,profile,color=(0,0,1))
        f = plt.vlines(V2p,mi,ma,color = (1,0,1),linestyles='dashed')
        plt.title('Slice along the transition')
        plt.xlabel('$VG_4$ (mV)')
        plt.ylabel('Phase (deg)')
        plt.tight_layout()
        if savefig == True:
#             plt.savefig('../analysis/Triple_points/Vg2='+str(round(V3p*1000)/1000)+'Vg2='+str(round(V2p*1000)/1000)+'_profile.png')

            path = f'..\exploration\g4=%s_g5=%s'%(G2f,G3f)

            plt.savefig(path+f'\interdot_working_slice',dpi=600)

            path = f'..\exploration/0-all_interdot'

            plt.savefig(path+f'\g4=%s_g5=%s_working_slice'%(str(int(float(G2f))),str(int(float(G3f)))),dpi=600)            
            
    return V2p,V3p,a,b, av



#######################################
def blopIQ(DAM,tc,timetot,demod,path,G2f,G3f,title='I/Q measure') :
    ziUhf.daq.setDouble('/'+uhfRef+'/demods/{}/timeconstant'.format(demod-1),tc)
    ziUhf.daq.setDouble('/'+uhfRef+'/demods/{}/rate'.format(demod-1),1/tc)
    
    pathtxt=path+'.txt'

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

    
    fig.savefig(path,dpi=600)
    
    path = f'..\exploration/1-all_Bubbles'
    
    try : 
        os.mkdir(path)
    except :
        print('Dossier existant')

    fig.savefig(path+f'\g4=%s_g5=%s '%(str(int(float(G2f))),str(int(float(G3f))))+title,dpi=600)

# path=[f'..\exploration\Saving_process\g2=-638.475_g3=-949.55/IQ_on_signal.txt',f'..\exploration\Saving_process\g2=-638.475_g3=-949.55/IQ_out_of_signal.txt']


#######################
def draw_multiple_bbl(path,path_register,G2f,G3f) :

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
    
    title=f'IQ_double_bbl'
    
    fig.savefig(path_register+f'/'+title,dpi=600)
    
    patth = f'..\exploration/1-all_Bubbles'

    fig.savefig(patth+f'\g5=%s_g4=%s '%(str(int(float(G2f))),str(int(float(G3f))))+title,dpi=600)

    fig.tight_layout()


def register_time_trace(DAM,start,stop,num_point,tc,total_time,demod,path,coeff_dir) :
    
    ziUhf.daq.setDouble('/'+uhfRef+'/demods/{}/timeconstant'.format(demod-1),tc)
    ziUhf.daq.setDouble('/'+uhfRef+'/demods/{}/rate'.format(demod-1),1/tc)
    
    path_ex=np.array([])
    
    try : 
        os.mkdir(path)
    except :
        print('Dossier existant')

    profondeur=np.linspace(start,stop,num_point)

#     for i,j in enumerate(profondeur) :
    for i in trange(len(profondeur)):
        j = profondeur[i]
        path_register=path+f'/vg4f=%smV_vg5f=%smV'%(round(j,3),round(coeff_dir*j,3))
        if i==0 :
            VG4(Vgw4+j)
            VG5(Vgw5+coeff_dir*j) 
            DAM.get_data_bin(total_time,path_register)
            
        else :     
            VG4(Vgw4+j)
            VG5(Vgw5+coeff_dir*j) 
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

def analyse_time_traces(path,start,stop,Threshold,G2f,G3f) :
    
    print(path)
    file = path+f'/time_traces/paths.txt'
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
    Vg = np.linspace(start,stop,len(Ps_up))    

    ## Plot the occupations up/down:
    fig,ax = plt.subplots()
    plt.plot(Vg,Ps_up)
    plt.plot(Vg,Ps_down)
    plt.xlabel('$VG_4$ (mV)',fontsize=18)
    plt.ylabel('$P_{in},P_{out}$',fontsize=18)
    ax.tick_params(labelsize=14)
    ax.set_title('Occupations up/down',size=18)
    fig.tight_layout()
    plt.savefig(path+f'/Occupation.png')

    ## Plot the tunnel rates:
    gamma_up = 1/np.array(Ts_up)
    gamma_down = 1/np.array(Ts_down)

    gamma_up[gamma_up>1e300]=0  
    gamma_down[gamma_down>1e300]=0  
    
    fig,ax = plt.subplots()
    
    plt.plot(Vg,gamma_up*1e-3,'+',label='$\Gamma_{out}$')
    plt.plot(Vg,gamma_down*1e-3,'+',label='$\Gamma_{in}$')
    


    # if np.max(gamma_up)>50e3 or np.max(gamma_down)>50e3:
    #     plt.ylim(0.0,30)
        
    plt.xlabel('$V_{G4}$ (mV)',fontsize=18)
    plt.ylabel('$\Gamma_{in},\Gamma_{out}$ (kHz)',fontsize=18)
    ax.tick_params(labelsize=14)
    ax.set_title('Rates up/down',size=18)
    fig.tight_layout()
    plt.legend()
    plt.savefig(path+f'/Rates.png')
    
    path_register = f'..\exploration/2-all_Rates'
    title=f'gamma_rates'
    
    try : 
        os.mkdir(path_register)
    except :
        print('Dossier existant')

    fig.savefig(path_register+f'\g4=%s_g5=%s '%(str(int(float(G2f))),str(int(float(G3f))))+title,dpi=600)
    
    crossing=np.argmin(np.abs(gamma_up-gamma_down))
    
    return gamma_up[crossing] #, Vg[crossing]




def Elzouzou_fast(path,start,stop,G2f,G3f,average,Npoints, Tempty,Tload, Tread,Vload=-0.1,Vread=0,Vempty=0.1) :
    # Number of averages to perform at each read level:
   
    namefile='C:\\Users\\g-gre-gre050402\\Documents\\Zurich Instruments\\LabOne\\WebServer\\awg\\src\\diagonal_pulse.seqc'    
    
    
    changetempty(namefile, Tempty) 
    changetload(namefile, Tload) 
    changetread(namefile, Tread) 
    
    # run_seq('dev2010','pulse_triggerdata_transfer.seqc')   
    # ziUhf.daq.setInt('/dev2010/demods/1/enable', 1)
    # ziUhf.daq.setInt('/dev2010/demods/0/enable', 1)
    
    
    
    acquisition_duration = Tempty+Tload+Tread  # length of time to record (s)
    
    
    
    
    # repetitions = 1000           # number of repetitions for the averaging
    # points = 71# number of points in the acquisition window (min=2)
    #efftc=acquisition_duration/10
    efftc=1/800e3
    
    # such that the effective Tc is 100ms 
    # repetitions=tc/efftc/5
    
    repetitions=average
    # daq_module.set('holdoff/time', 0)
    ziUhf.daq.setInt('/dev2010/demods/0/trigger', 33554432) # demodulator trigger set on AWGtrigger2 High
    # ziUhf.daq.setDouble('/dev2010/demods/0/rate', 800e3)
    # ziUhf.daq.setDouble('/dev2010/demods/1/rate', 800e3)
    # ziUhf.daq.setDouble('/dev2010/demods/0/rate', 2e6)
    # ziUhf.daq.setDouble('/dev2010/demods/1/rate', 800e3)
    ziUhf.daq.setDouble('/dev2010/demods/0/rate', 800e3)
    ziUhf.daq.setInt('/dev2010/demods/0/order', 1)
    
    points=int(acquisition_duration*ziUhf.daq.getDouble('/dev2010/demods/0/rate'))
    
    
    ziUhf.daq.setDouble('/dev2010/demods/0/timeconstant', efftc)
    ziUhf.daq.setDouble('/dev2010/demods/1/timeconstant', efftc)
    #ziUhf.daq.setInt('/dev2365/awgs/0/enable', 1)      # 1 = enable;   0 = disabled
    #add also check if meas start, otherwise restart AWG
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
    trigger_setting = [['dataAcquisitionModule/triggernode', '/dev2010/demods/0/sample.TrigAWGTrig3'],  # trigger node is AWG trigger number 3 
    #                   ['dataAcquisitionModule/type', 2],      
                       ['dataAcquisitionModule/type', 6],                                          # this setting is related to the AWG trigger
                       ['dataAcquisitionModule/edge', 1],                                               # trigger on the positive edge. 1 = positive, 2=negative
                       ['dataAcquisitionModule/count', 1],                                              # number of trigger events to count
                       ['dataAcquisitionModule/holdoff/time', 0],                                       # hold off time
                       ['dataAcquisitionModule/holdoff/count', 0],                                      # hold off count
                       ##careful
                       ['dataAcquisitionModule/delay', 0e-6], #0                                       # trigger delay (s)
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
    
    phase_trigS= SpecialParameters.Pulsed_readout_S(ziUhf, repetitions, returnOnePoint=False)
    phase_trigD= SpecialParameters.Pulsed_readout_D(ziUhf, repetitions, returnOnePoint=False)
    
    phase_trigS.setSettings(trigger_setting, grid_setting)
    phase_trigD.setSettings(trigger_setting, grid_setting)
    
    
    # Duration of the time trace to record:
    

    # Vreads = np.arange(-0.3,0.015,0.0005)

    # Vread = Vreads[i]      
    t=np.linspace(0,acquisition_duration,points)
    
    phaseDarray=[]
    phaseSarray=[]
    amp=[]
    # Npoints=101

    Vreads=np.linspace(start,stop,Npoints)##real amplitudes in mV on G4
    
    # ampliAWG(0.2)
    
    for i in range(0,Npoints):
    
        amplimV=Vreads[i]
    
        
        A=amplimV/ampliAWG()/5.5 #renormalize in AWG units
    
        changeAread(namefile, A) 
        # changet11(namefile, t11) 
        # changet11(namefile, tramp) 
        # run_seq('dev2010','pulse_triggerdata_transfer.seqc')   
        run_seq('dev2010','diagonal_pulse.seqc')   
        ziUhf.daq.setInt('/dev2010/demods/1/enable', 1)
        ziUhf.daq.setInt('/dev2010/demods/0/enable', 1)
        ziUhf.daq.setInt('/dev2010/sigouts/0/enables/4', 1)
        ziUhf.daq.setInt('/dev2010/demods/0/trigger', 33554432)

        # ziUhf.daq.setInt('/dev2010/sigouts/0/enables/5', 1)
    
        # phaseSarray.append(phase_trigS())
        phaseDarray.append(phase_trigD())
    # ziUhf.daq.setInt('/dev2010/sigouts/1/on', 0)    
    
    # phaseS=[]
    # for i in range(0,Npoints):
    #     phaseS.append(phaseSarray[i][0])
        
    phaseD=[]
    for i in range(0,Npoints):
        phaseD.append(phaseDarray[i][0])
        


    M=phaseD
    #Enregistrement des datas dans un sous dossier convenablement nommé 
    Field = Bfield_Hon()
    pathelzou=path + f'/El_Zeerman'
    
    try : 
        os.mkdir(pathelzou)
    except :
        print('Dossier existant')
    
    np.save(pathelzou+f'/El_Zeerman_data'+str(round(Field,2)),M) 
    np.save(pathelzou+f'/El_Zeerman_times'+str(round(Field,2)),t)
    np.save(pathelzou+f'/El_Zeerman_Vread'+str(round(Field,2)),Vreads)
    
    title=str(Bfield())+'Elzermanseq_Tempty'+str(Tempty)+'Tload'+str(Tload)+'Tread'+str(Tread)+'G5'+str(VG5())+'mV'
    
    pathtxt=pathelzou+'//'+title+'.txt'
    
    Headertxt=f'Tload=%s ; Tread=%s ; Tempty=%s ; Vload=%s ; Vread=%s ; Vempty=%s ; ' %(Tload,Tread,Tempty,Vload,Vread,Vempty)
    Headertxt=Headertxt + f'\n' 
    Headertxt=f'awg.ch1.awg_amplitude=%s Volt' %(ampliAWG())
    Headertxt=Headertxt + f'\n' 
    Headertxt=Headertxt + 'X -> Time (sec) ; Y -> Phase (Rad)'
    
    np.savetxt(pathtxt,[],fmt='%.6e',header=Headertxt) 
    
    #Enregistrement de la figure tracée 
    
    fig,ax = plt.subplots()
    # plt.pcolor(t*1e6,Vreads,np.transpose(M))
    plt.pcolor(t*1e6,Vreads,M)
    plt.ylabel('$V_{read}(mV)$',fontsize=18)
    plt.xlabel('t ($\mu$s)',fontsize=18)
    cb=plt.colorbar()
    cb.set_label('$\phi_D$ (Rad)')
    
    ax.tick_params(labelsize=14)
    ax.set_title('B='+str(Bfield())+'G5='+str(np.round(VG5(),3))+'mV Aawg'+str(np.round(ampliAWG(),3)),size=18)
    fig.tight_layout()

    now=datetime.datetime.now()
    dayFolder= datetime.date.isoformat(now)
    try:
        os.makedirs(folder2+'\\'+dayFolder)
    except IOError:
        donothing=1
        
    plt.savefig(folder2+'\\'+dayFolder+'\\'+title+'.png')
    np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'.txt',M)
    
    print(path)
    
    fig.savefig(path+'\\'+title+'.png',dpi=600)
       
    path_register = f'..\exploration/3-all_Elzouzous'

    
    try : 
        os.mkdir(path_register)
    except :
        print('Dossier existant')


    fig.savefig(path_register+'\\g4='+str(VG4())+'_g5='+str(VG5())+'_'+title+'.png')











# Give the coordinates of the triple points to study:


# G5 = [-1207,-1213,-1218,-1223,-1229,-1234,-1239,-1244,-1249,-1254,-1259,-1265,-1261,-1276,-1281,-1286,-1291,-1296,-1301,-1306,-1311,-1317,-1322,-1327,-1332,-1337,-1342,-1347,-1352,-1357,-1362,-1367,-1377,-1382,-1387,-1392,-1397,-1402,-1407]
# G4 = [ -748, -748, -746, -746, -746, -745,  -745,-745 ,-744, -744,  -744, -743,-743,  -743,-742 ,-742 ,-742,-741  ,-741,  -740,-740 ,-739,-739   ,-739,-738,-738   ,-738,-737,-737   ,-737,-736,-736   ,-735,-735,  -734,-734, -733, -733, -733]
# G4=np.add(G4,3)



# G5=np.linspace(-1351,-1447,20)
# G4=np.linspace(-736.11,-729.71,20)
# G5=G5[13:]
# G4=G4[13:]



# G5=np.linspace(-1407,-1607,41)
# G4=np.linspace(-732,-720,41)


# G5=np.linspace(-1333,-1433,21)
# G4=np.linspace(-779,-773,21)
# Then launch the script that will eventually (if each step is chosen as "True", but can be avoided by putting "false"):
# •Replace on the triple point by doing a 2D scan,
# •Replace more accuratley by sweeping the fine gates
# •Study the tunnel rates for each triple point
# •Record the "Bubbles" in the IQ plane for both states of the charge sensor
# •Try Elzermann's readout on the triple point
# G4=[-727]
# G5=[-1482]
# G5=[-1300]
# G4=[-741]
# G5=[-1303.11]
# G4=[-781.11]

# G5=[-1240.16]
# G4=[-735.16]
# G5=np.linspace(-1250,-1450,6)
# G4=np.linspace(-735,-728,6)
# 284_1.7T_G4vsG5_N0to1_G1-1823.3500000000001mV_G2-1410.769mV_G3-813.0mV_G4-731.1mV_G5-1444.1999999999998mV_G6-1569.4375mV
# G5=np.linspace(-1402,-1501,21)
# G4=np.linspace(-743,-735,21)
# VG6onmin_phD(-2000,-2100,2001,1)



continuous_acquisition()
VG6onmin_phD(-1544,-1538,501,1)

G5=[-1462.03]
G4=[-729.53]


Gamma=[]
compteur = 0
Scan2d = True
# Fine_Pos = True
time_traces = True
bubbles =True
# time_traces = False
# bubbles =False

elzouzou = True 

for i,j in zip(G5,G4):

    if Scan2d == True:
        VG4(j)
        VG5(i)
        continuous_acquisition()
        ziUhf.daq.setInt('/dev2010/awgs/0/enable', 0)
        tc=10e-3
        ziUhf.daq.setDouble('/'+uhfRef+'/demods/0/timeconstant',tc/2)
        ziUhf.daq.setDouble('/'+uhfRef+'/demods/0/rate',2e3) 
        ziUhf.daq.setDouble('/'+uhfRef+'/demods/0/order',3) 
        # ziUhf.daq.setInt('/dev2010/demods/2/enable', 1)
        ziUhf.daq.setInt('/dev2010/demods/0/enable', 1)

        # ziUhf.daq.setInt('/dev2010/sigouts/0/enables/6', 1)
        name=str(Bfield())+'T_G4vsG5_N0to1_increasedG3__G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
        # c1,data_id,c2,c3=sweep2D(VG5,i-3,i+3,121,tc,VG4,j-4,j+4,161,tc,ph1)
        c1,data_id,c2,c3=sweep2D(VG5,i-3,i+3,81,tc,VG4,j-4,j+4,81,tc,ph1)

        
        
        
        
        G4f=str(round(j,3))
        G5f= str(round(i,3))
        
    # Enregistrement du scan précédent sous forme 
        plot_by_id(data_id)
        # save2plots(name,data_id)
        saveplot(name,data_id)
        
        Field = Bfield_Hon()
        pathh= f'..\exploration\G4=%s_G5=%s'%(str(round(j,3)),str(round(i,3)))
        
        Vgw4,Vgw5,a,b,Threshold=find_working_point_by_id_inv(data_id,str(round(j,3)),str(round(i,3)))
        
        
        Threshold=Threshold*np.pi/180#into rad
        # Vgw4,Vgw5=Vgw4[0],Vgw5[0]
        
        ##correct position
        # Vgw5=Vgw5+0.1
        # # print('working_point_G4'+str(VG4())+'_G5'+str(VG5()))
        
        # VG4(Vgw4)
        # VG5(Vgw5)
        
        # print('working_point_G4'+str(VG4())+'_G5'+str(VG5()))
        
        
# Sous code permettant d'obtenir les IQ bubbles dans le signal et en dehors du signal pour calculer a la fois le SNR et
# s'assurer qu'il n'y a pas un système a deux niveau qui traine dans le coin. 
    if bubbles == True:    
        #On regarde sur le signal lié à la transition 3->4 resonnante à une profondeur de n(mV) par rapport au cut 
        profondeur=1
        VG4(Vgw4+profondeur)
        VG5(Vgw5+a*profondeur)   
        
        # tc=2e-6
        tc=5e-6
        totaltime=0.5
        demod=1
        path2 = pathh + f'\IQ_on_signal'#+str(tc*1e6)+'us'
        blopIQ(daq,tc,totaltime,demod,path2,str(round(j,3)),str(round(i,3)),title='IQ_On_Signal')
        
        #On regarde en epsilon=0 ! 
        profondeur=0
        VG4(Vgw4+profondeur)
        VG5(Vgw5+a*profondeur)   
        
        path2 = pathh + f'\IQ_epsilon=0'#+str(tc*1e6)+'us'
        blopIQ(daq,tc,totaltime,demod,path2,str(round(j,3)),str(round(i,3)),title='IQ_Epsilon=0')
        
        #On regarde en dehors de tout signal ! 
        profondeur=-1
        VG4(Vgw4+profondeur)
        VG5(Vgw5+a*profondeur)   
        
        path2 = pathh + f'\IQ_out_of_signal'#+str(tc*1e6)+'us'
        blopIQ(daq,tc,totaltime,demod,path2,str(round(j,3)),str(round(i,3)),title='IQ_Out_Of_Signal')
        
        #Trace la double bubble pour voir les superpositions, le SNR etc...
        path_dbb=[pathh + f'\IQ_on_signal.txt',pathh + f'\IQ_out_of_signal.txt']
        draw_multiple_bbl(path_dbb,pathh,str(round(j,3)),str(round(i,3)))
    
    if time_traces == True:
        #Enregistre les times traces dans un sous dossier time_traces qui seront a post traité dans la partie suivante     
        path3 = pathh + f'/time_traces'
        #pas de 2microVolt donc haute résolution 
        nb_elements=51
        # def register_time_trace(DAM,start,stop,num_point,tc,total_time,demod,path,coeff_dir)
        
        # path_ex=register_time_trace(daq,-0.2,0.2,nb_elements,1e-5,3,1,path3,a)#300k repetitions like this
        
        path_ex=register_time_trace(daq,-0.6,0.6,nb_elements,1e-5,4,1,path3,a)
        
     #Post traitement des gammas rates et de la probabilité d'occupation dans le dot 
    # Threshold2=5
        gammarate=analyse_time_traces(pathh,-0.6,0.6,Threshold,str(round(j,3)),str(round(i,3)))
      
        Gamma.append(gammarate)
    # On tente le Elzouzou ici


    
    if elzouzou==True :
        # tc_zouzou=500e-9
        VG4(Vgw4)
        VG5(Vgw5) 


        Elzouzou_fast(pathh,-0,-0.5,Vgw4,Vgw5,1000,41, 50e-6, 10e-6,100e-6)
        # Elzouzou_fast(pathh,0.6,-0.6,Vgw4,Vgw5,1000,101, 50e-6, 50e-6,150e-6)
        # Elzouzou_fast(pathh,0.6,-0.6,Vgw4,Vgw5,1000,101, 50e-6, 200e-6,150e-6)

        # Bfield(1.2)
        # Elzouzou_fast(pathh,-0,-0.6,Vgw4,Vgw5,500,101, 50e-6, 20e-6,500e-6)
        # Bfield(2)
        
#before        
#         : VG4()
# Out[334]: -732.3

# VG5()
# Out[335]: -1443.7076



#Définition de la séquence Init
print('Done')

name= 'GammavsG5_'
f = plt.figure()
plt.plot(G5[:len(Gamma)],Gamma,'+')
plt.xlabel('$V_{G5}$ (mV')
plt.ylabel('$\Gamma$ (Hz)')

plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'_.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'_.txt',Gamma)