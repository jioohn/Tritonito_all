

Tempty=30e-6
Tload=20e-6
Tread=200e-6

# Tempty=0e-6
# Tload=100e-6
# Tread=100e-6
namefile='C:\\Users\\g-gre-gre050402\\Documents\\Zurich Instruments\\LabOne\\WebServer\\awg\\src\\diagonal_pulse.seqc'    


changetempty(namefile, Tempty) 
changetload(namefile, Tload) 
changetread(namefile, Tread) 

# run_seq('dev2010','pulse_triggerdata_transfer.seqc')   
# ziUhf.daq.setInt('/dev2010/demods/1/enable', 1)
# ziUhf.daq.setInt('/dev2010/demods/0/enable', 1)

# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 15:38:14 2021

@author: G-GRE-GRE050402
"""

# acquisition_duration = Tempty+Tload+Tread  # length of time to record (s)
# delay=0
delay=Tempty+Tload
acquisition_duration =50e-6 # length of time to record (s)


# repetitions = 1000           # number of repetitions for the averaging
# points = 71# number of points in the acquisition window (min=2)
#efftc=acquisition_duration/10
efftc=1.25e-6
ziUhf.daq.setDouble('/dev2010/demods/1/rate', 800e3)
# efftc=5e-6
# ziUhf.daq.setDouble('/dev2010/demods/1/rate', 200e3)
# such that the effective Tc is 100ms 
# repetitions=tc/efftc/5
# Nmeasure=1
repetitions=10000

ziUhf.daq.setInt('/dev2010/demods/1/trigger', 33554432) # demodulator trigger set on AWGtrigger2 High
# ziUhf.daq.setDouble('/dev2010/demods/0/rate', 800e3)
# ziUhf.daq.setDouble('/dev2010/demods/1/rate', 800e3)
# ziUhf.daq.setDouble('/dev2010/demods/0/rate', 2e6)
# ziUhf.daq.setDouble('/dev2010/demods/1/rate', 800e3)
# ziUhf.daq.setDouble('/dev2010/demods/0/rate', 800e3)
ziUhf.daq.setInt('/dev2010/demods/1/order', 1)

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
                   ['dataAcquisitionModule/delay', delay], #0                                       # trigger delay (s)
                   ##
                   ['dataAcquisitionModule/endless', 0]]                                            # endless disabled = 0


grid_setting =    [['dataAcquisitionModule/grid/mode', 2],                          # mode. 2 = Linear interpolation 
                   ['dataAcquisitionModule/grid/cols', points],                     # number of points in the acquisition window
                   ['dataAcquisitionModule/duration', acquisition_duration],        # length of time to record (s)
                   ['dataAcquisitionModule/grid/rows', 1],                        # rows
                   ['dataAcquisitionModule/grid/direction', 0],                     # scan direction. 0 = forwardphase_pulsed = SpecialParameters.Pulsed_readout(ziUhf, repetitions, returnOnePoint=False)
                   ['dataAcquisitionModule/grid/repetitions', repetitions],         # number of repetitions for the averaging
                   ['dataAcquisitionModule/awgcontrol', 1],                         # set the AWG control
                   ['dataAcquisitionModule/save/fileformat', 1]]                    # 1 = CSV format 

phase_trigS= SpecialParameters.Pulsed_readout_S(ziUhf, repetitions, returnOnePoint=False)
phase_trigD= SpecialParameters.Pulsed_readout_D(ziUhf, repetitions, returnOnePoint=False)

phase_trigS.setSettings(trigger_setting, grid_setting)
phase_trigD.setSettings(trigger_setting, grid_setting)

ziUhf.daq.setInt('/dev2010/sigouts/0/enables/5', 1)


# Readlevel=Read_level(ziUhf)
# DAM.get_data_txt(timetot,pathtxt,'x','y',affichage=False)
amplimV=-0.55


Readlevel(-0.71)

# acquisition_duration=70e-6
# delay=220e-6

# acquisition_duration=Tread+5e-6
# delay=Tempty+Tload-5e-6

# acquisition_duration=140e-6
# delay=0



Ntraces=10000
# taxis=np.linspace(delay,acquisition_duration+delay,points)
# c=daqtrig.get_data(acquisition_duration)



c,d=daqtrig.get_data_pulseseq(acquisition_duration,delay,Ntraces)
traceavg=[]
threshold=-0.1#rad

for i in range(0,len(d)):
    traceavg.append(np.nanmean(d[i]))

Pup=0
singletraces=np.transpose(d)    
for i in range(0,len(singletraces)):
    if np.min(singletraces[i])<threshold:
        Pup+=1

Pupnorm=Pup/len(singletraces)
# len(singletraces)


taxis=np.linspace(delay,acquisition_duration+delay,len(singletraces[0]))

plt.figure()
plt.plot(taxis*1e6,traceavg, label='average'+str(Ntraces)+' traces, readlevel='+str(Readlevel())+'mV')

# plt.plot(taxis,phase_trigD()[0])
title=str(data_id)+'_sstraces'+str(Ntraces)+'_10us_load-'+str(Readlevel())+'ampliread_'
# plt.plot(taxis*1e6,singletraces[4],label='spin down ')
# plt.plot(taxis*1e6,singletraces[9],label='spin up')
plt.xlabel('$t(\mu s)$')
plt.ylabel('$\phi(rad)$')
plt.legend()
plt.savefig(folder2+'\\'+dayFolder+'\\'+title+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'.txt',d)

# plt.plot(taxis*1e6,singletraces[8],label='spin up')


M=singletraces
title=str(Bfield())+'all_SS_40usacq_readlevel='+str(Readlevel())+'_Tempty'+str(Tempty)+'Tload'+str(Tload)+'Tread'+str(Tread)+'G5'+str(VG5())+'mV'

# np.save(pathelzou+f'/El_Zeerman_data'+str(round(Field,2)),M) 
# np.save(pathelzou+f'/El_Zeerman_times'+str(round(Field,2)),t)
# np.save(pathelzou+f'/El_Zeerman_Vread'+str(round(Field,2)),Vreads)
t=np.linspace(delay,acquisition_duration+delay,len(singletraces[0]))

ntr=np.linspace(1,len(singletraces),len(singletraces))
#Enregistrement de la figure tracée 
fig,ax = plt.subplots()

plt.pcolor(t*1e6,ntr,M)

plt.ylabel('Ntraces(mV)',fontsize=18)
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





















# multiple points
plt.figure()
for j in range(0,4):
    Vread=-0.6-j*0.05
    Readlevel(Vread)
    
    # acquisition_duration=70e-6
    # delay=220e-6
    
    # acquisition_duration=Tread+5e-6
    # delay=Tempty+Tload-5e-6
    
    # acquisition_duration=100e-6
    # delay=40e-6
    
    
    
    Ntraces=10000
    # taxis=np.linspace(delay,acquisition_duration+delay,points)
    # c=daqtrig.get_data(acquisition_duration)
    
    
    
    c,d=daqtrig.get_data_pulseseq(acquisition_duration,delay,Ntraces)
    traceavg=[]
    threshold=-0.15#rad
    
    for i in range(0,len(d)):
        traceavg.append(np.nanmean(d[i]))
    
    Pup=0
    singletraces=np.transpose(d)    
    for i in range(0,len(singletraces)):
        if np.min(singletraces[i])<threshold:
            Pup+=1
    
    Pupnorm=Pup/len(singletraces)
    # len(singletraces)
    
    
    taxis=np.linspace(delay,acquisition_duration+delay,len(singletraces[0]))
    

    plt.plot(taxis*1e6,traceavg, label='average'+str(Ntraces)+' traces, readlevel='+str(Readlevel())+'mV')
    
    # plt.plot(taxis,phase_trigD()[0])
title=str(data_id)+'_sstraces'+str(Ntraces)+'_10us_load-'+str(Readlevel())+'ampliread_'
# plt.plot(taxis*1e6,singletraces[4],label='spin down ')
# plt.plot(taxis*1e6,singletraces[28],label='spin up')
plt.xlabel('$t(\mu s)$')
plt.ylabel('$\phi(rad)$')
plt.legend()
plt.savefig(folder2+'\\'+dayFolder+'\\'+title+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'.txt',d)



M=singletraces
title=str(Bfield())+'Ntracesvstime_Tempty'+str(Tempty)+'Tload'+str(Tload)+'Tread'+str(Tread)+'G5'+str(VG5())+'mV'

# np.save(pathelzou+f'/El_Zeerman_data'+str(round(Field,2)),M) 
# np.save(pathelzou+f'/El_Zeerman_times'+str(round(Field,2)),t)
# np.save(pathelzou+f'/El_Zeerman_Vread'+str(round(Field,2)),Vreads)
t=np.linspace(delay,acquisition_duration+delay,len(singletraces[0]))
#Enregistrement de la figure tracée 
ntr=np.linspace(1,len(singletraces),len(singletraces))
fig,ax = plt.subplots()
# plt.pcolor(t*1e6,Vreads,np.transpose(M))
plt.pcolor(t*1e6,ntr,M)

plt.ylabel('Ntraces$',fontsize=18)
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












path=folder2+'\\'+dayFolder+'\\'
path2=register_SS_traces(daq,4e-6,1.5,1,path)
analyze_SS_traces(Threshold,path2)

total_time=1#s


# ziUhf.daq.setDouble('/'+uhfRef+'/demods/0/timeconstant',1e-6)

# j = profondeur[i]
path_register=path+'vg4f=%smV_vg5f=%smV'%(round(VG4(),3),round(VG5(),3))
p=daq.get_data(total_time)

###
p=daqtrig.getdatapulse_seq(total_time)


# p=daqtrig.get_data(1)
# DAM.get_data_bin(total_time,path_register)

path2=path_register

data = np.load(path2+'.npy')


def register_SS_traces(DAM,tc,total_time,demod,path) :
    
    ziUhf.daq.setDouble('/'+uhfRef+'/demods/{}/timeconstant'.format(demod-1),tc)

    # j = profondeur[i]
    path_register=path+'vg4f=%smV_vg5f=%smV'%(round(VG4(),3),round(VG5(),3))
    
    
    # try : 
    #     os.mkdir(path)
    # except :
    #     print('Dossier existant')


#     for i,j in enumerate(profondeur) :
    DAM.get_data_bin(total_time,path_register)
            
            
    # path_ex=np.append(path_ex,path_register)  
               
    # text_file = open(path+'\\path_SS.txt', "w")
    # for i in path_ex : 
    #     text_file.write(i + f';')
    # text_file.close()   
    return path_register
        
def analyse_SS_traces(path2,threshold) :


    data = np.load(path2+'.npy')
    P_up,P_down,T_up,T_down = Occupations_and_times(data,Threshold, Do_plot = False)
    
    Ps_up.append(P_up)
    Ps_down.append(P_down)
    Ts_up.append(T_up)
    Ts_down.append(T_down)

    # Vg = np.linspace(-0.3,0.3,len(Ps_up))    


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


