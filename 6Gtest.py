# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 17:58:04 2020

@author: G-GRE-GRE050402
"""




###define gate intervals  (Leti performed RT measurements with gates not swept at -1 and -2V)
Vds=5
finalgate=-1500
initgate=0
opengate=-1500
# opengate=0
Npoints=501
folder2=r'S:\132-PHELIQS\132.05-LATEQS\132.05.01-QuantumSilicon\Tritonito\2021\Feb2021_6G22_2_die103\data'


def func(): 
	return dmm.volt.get() * 1e-8

current = qc.Parameter('current', instrument=dmm, get_cmd=func,get_parser=float)

# VG1 = qc.ScaledParameter(dac.dac1, gain=1000, name='G1', label='$V_{G1}$', unit='mV')
# VG2 = qc.ScaledParameter(dac.dac2, gain=1000, name='G2', label='$V_{G2}$', unit='mV')

# VG3= qc.ScaledParameter(dac.dac3, gain=1000, name='G3', label='$V_{G3}$', unit='mV')
# VG4= qc.ScaledParameter(dac.dac4, gain=1000, name='G4', label='$V_{G4}$', unit='mV')
# VG5= qc.ScaledParameter(dac.dac5, gain=1000, name='G5', label='$V_{G5}$', unit='mV')
# bias = qc.ScaledParameter(dac.dac6, gain=1000, name='S', label='$V_{SD}$', unit='mV')


# rampVG1 = qc.ScaledParameter(dac.rampdac1, gain=1000, name='G1', label='VG1', unit='mV')
# rampVG2 = qc.ScaledParameter(dac.rampdac2, gain=1000, name='G2', label='VG2', unit='mV')

# rampVG3= qc.ScaledParameter(dac.rampdac3, gain=1000, name='G3', label='VG3', unit='mV')
# rampVG4= qc.ScaledParameter(dac.rampdac4, gain=1000, name='G4', label='VG4', unit='mV')

# rampVG5= qc.ScaledParameter(dac.rampdac5, gain=1000, name='G5', label='VG5', unit='mV')

#extract data and parameters name as lists
def Extract_data(a):
#extract parameters name
    parameters_name=[]
    c1=0
    for i in range(0, len(a.parameters)):
        # print(i)
        # print(a.parameters)
        if i==(len(a.parameters)-1): 
            parameters_name.append(a.parameters[c1:])
    
        if a.parameters[i]!=',':
           c2=i+1
        elif a.parameters[i]==',':
             parameters_name.append(a.parameters[c1:c2])
             c1=i+1
    
    data_set=[]
    data_get=[]
    
    #parameter_swept_fixed length
    data_x=a.get_parameter_data(parameters_name[0])
    x=data_x[parameters_name[0]]
    x=x[parameters_name[0]] 
    data_set=x  
    
    
    #parameter_acquired may have variable length
    #update data .get
    for i in range(1,len(parameters_name)):
        print(i)
        data_y=a.get_parameter_data(parameters_name[i])
        y=data_y[parameters_name[i]]
        y=y[parameters_name[i]] 
    
        data_get.append(y)
    
    
    lendata_set=len(data_set)
    lendata_get=len(data_get[0])
    
    # #clean set parameters that are registered multiple times in sweep function
    # i=0
    # while i <(len(data_set)-1):
    #     # if i%(int(lendata_set/lendata_get)) !=0:
    #         if data_set[i]==data_set[i+1]:
    #             del data_set[i]
    #         else:
    #             i+=1    
    data_set=np.unique(data_set)

    return data_set,data_get, parameters_name   

#plot and save data  in csv format  
def plot_savecsv(data_set,xlabel,data_get,ylabel,parameters_name,folder,name):
    for i in range(0,len(data_get)):
        plt.figure()
        plt.plot(data_set ,data_get[i]) 
        # plt.title('Id vs $V_{g}$')
        plt.xlabel(xlabel,fontsize=16)
        plt.ylabel(ylabel,fontsize=16)  
        plt.savefig(folder+'\\'+name+'_'+parameters_name[i+1])
        plt.show()
        filename=folder+'\\'+name+'_'+parameters_name[i+1]+'.csv'
        # datas=list(zip(data_get[0],data_set))
        # np.savetxt(filename,datas,delimiter=',',header="A,B")
        # np.savetxt(filename,data_get[0])
        f=open(filename,"w")
        f.write("{};{};{};{};{}\n".format(ylabel,xlabel,'lot T18S0062A','DIE 241','WAFER23'))
        for x in zip(data_get[0],data_set):
            f.write("{};{} \n".format(str(x[0])[1:-1],str(x[1])[1:-1]))
        f.close()



###measurements routine for 6G devices


# opengate5=-2000
#here write temp, device and bias

# T='5G23_2-_T__440mK__Vmet'+str(int(dac.dac17()))+'V_'+str(int(bias()*1000))+'uVbias_gates_'+str(opengate)+'mV_G5'+str(opengate5)+'mV_'

#change this line to choose directory where you save stuff


now=datetime.datetime.now()
dayFolder= datetime.date.isoformat(now)
try:
    os.makedirs(folder2+'\\'+dayFolder)
except IOError:
    donothing=1


bias(Vds)
# T='6G22_2_-400mK_Vmet'+str(int(dac.dac17()))+'_Vbias'+str(int(bias()*1000))+'uVbias_gates_'+str(opengate)+'mV_allphi'
T='6G22_2_--440mK_Vmet'+str(int(dac.dac17()))+'_Vbias'+str(int(bias()*1000))+'uVbias_gates_'+str(opengate)+'mV'
#measure
#scanG1

Npoints=1001
rampVG1(initgate)
rampVG2(opengate)
rampVG3(opengate)
rampVG4(opengate)
rampVG5(opengate)
rampVG6(opengate)

a,b,c=sweep1D(VG1,initgate,finalgate,Npoints,0.01,current)

name='G1scan_'+T
xlabel='$V_{G1}$(mV)'
ylabel='$I_d$(A)'
data_set,data_get,parameters_name=Extract_data(a)
plot_savecsv(data_set,xlabel,data_get,ylabel,parameters_name,folder2,dayFolder+'\\' +name)


#measure
#scanG2
rampVG1(opengate)
rampVG2(initgate)
rampVG3(opengate)
rampVG4(opengate)
rampVG5(opengate)
rampVG6(opengate)
# time.sleep(20)#for capa
a,b,c=sweep1D(VG2,initgate,finalgate,Npoints,0.01,current)

name='G2scan_'+T
xlabel='$V_{G2}$(mV)'
ylabel='$I_d$(A)'
data_set,data_get,parameters_name=Extract_data(a)
plot_savecsv(data_set,xlabel,data_get,ylabel,parameters_name,folder2,dayFolder+'\\' +name)



#measure
#scanG3
rampVG1(opengate)
rampVG2(opengate)
rampVG3(initgate)
rampVG4(opengate)
rampVG5(opengate)
rampVG6(opengate)

time.sleep(5)
a,b,c=sweep1D(VG3,initgate,finalgate,Npoints,0.01,current)

name='G3scan_'+T
xlabel='$V_{G3}$(mV)'
ylabel='$I_d$(A)'
data_set,data_get,parameters_name=Extract_data(a)
plot_savecsv(data_set,xlabel,data_get,ylabel,parameters_name,folder2,dayFolder+'\\' +name)



#measure
#scanG4
rampVG1(opengate)
rampVG2(opengate)
rampVG3(opengate)
rampVG4(initgate)
rampVG5(opengate)
rampVG6(opengate)
a,b,c=sweep1D(VG4,initgate,finalgate,Npoints,0.01,current)

name='G4scan'+T
xlabel='$V_{G4}$(mV)'
ylabel='$I_d$(A)'
data_set,data_get,parameters_name=Extract_data(a)
plot_savecsv(data_set,xlabel,data_get,ylabel,parameters_name,folder2,dayFolder+'\\' +name)

#measure
#scanG5
rampVG1(opengate)
rampVG2(opengate)
rampVG3(opengate)
rampVG4(opengate)
rampVG5(initgate)
rampVG6(opengate)

a,b,c=sweep1D(VG5,initgate,finalgate,Npoints,0.01,current)

name='G5scan_'+T
xlabel='$V_{G5}$(mV)'
ylabel='$I_d$(A)'
data_set,data_get,parameters_name=Extract_data(a)
plot_savecsv(data_set,xlabel,data_get,ylabel,parameters_name,folder2,dayFolder+'\\' +name)

rampVG1(opengate)
rampVG2(opengate)
rampVG3(opengate)
rampVG4(opengate)
rampVG5(opengate)
rampVG6(initgate)
a,b,c=sweep1D(VG6,initgate,finalgate,Npoints,0.01,current)
plot_by_id(b)

name='G6scan_'+T
xlabel='$V_{G6}$(mV)'
ylabel='$I_d$(A)'
data_set,data_get,parameters_name=Extract_data(a)
plot_savecsv(data_set,xlabel,data_get,ylabel,parameters_name,folder2,dayFolder+'\\' +name)









dac.set_dacs_zero()
bias(-0.2)
########################
test6gate(initgate,finalgate,opengate,Vds)
test6gate_log(initgate,finalgate,opengate,Vds)

# name='fakegatevsG3'
# a,dataid,c,d=sweep2D(dac.dac9,-0,0.1,1001,0.1,VG3,-600,-900,1201,0.03,ph1,current)

# plot_by_id(dataid)
# saveplot(name,dataid)


bias(-0.2)
# dac.dac9(-30)



###singleplot for all, nocsv
# Npoints=1001
# bias(Vds)
# rampVG1(initgate)
# rampVG2(opengate)
# rampVG3(opengate)
# rampVG4(opengate)
# rampVG5(opengate)

# a,b,c=sweep1D(VG1,initgate,finalgate,Npoints,0.01,current)
# data_set,data_get,parameters_name=Extract_data(a)

# xlabel='$V_{G}$(mV)'
# ylabel='$I_d$(A)'

# plt.figure()
# plt.plot(data_set ,data_get[0],label='$V_{G1}') 
# # plt.title('Id vs $V_{g}$')
# plt.xlabel(xlabel,fontsize=16)
# plt.ylabel(ylabel,fontsize=16)  


# #measure
# #scanG2
# rampVG1(opengate)
# rampVG2(initgate)
# rampVG3(opengate)
# rampVG4(opengate)
# rampVG5(opengate)
# # time.sleep(20)#for capa
# a,b,c=sweep1D(VG2,initgate,finalgate,Npoints,0.01,current)

# data_set,data_get,parameters_name=Extract_data(a)
# plt.plot(data_set ,data_get[0],label='$V_{G2}') 



# #measure
# #scanG3
# rampVG1(opengate)
# rampVG2(opengate)
# rampVG3(initgate)
# rampVG4(opengate)
# rampVG5(opengate)
# time.sleep(2)
# a,b,c=sweep1D(VG3,initgate,finalgate,Npoints,0.01,current)
# data_set,data_get,parameters_name=Extract_data(a)
# plt.plot(data_set ,data_get[0],label='$V_{G3}') 





# #measure
# #scanG4
# rampVG1(opengate)
# rampVG2(opengate)
# rampVG3(opengate)
# rampVG4(initgate)
# rampVG5(opengate)
# a,b,c=sweep1D(VG4,initgate,finalgate,Npoints,0.01,current)
# data_set,data_get,parameters_name=Extract_data(a)
# plt.plot(data_set ,data_get[0],label='$V_{G4}') 



# #measure
# #scanG5
# rampVG1(opengate)
# rampVG2(opengate)
# rampVG3(opengate)
# rampVG4(opengate)
# rampVG5(initgate)

# a,b,c=sweep1D(VG5,initgate,finalgate,Npoints,0.01,current)
# data_set,data_get,parameters_name=Extract_data(a)
# plt.plot(data_set ,data_get[0],label='$V_{G5}') 

# plt.legend()
# name=str(dataid)+'_5Gtest'
# plt.savefig(folder2+'\\'+dayFolder+'\\' +name)


# test5gate(initgate,finalgate,opengate,Vds)
bias(-0.2)