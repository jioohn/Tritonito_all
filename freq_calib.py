# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 18:42:41 2020

@author: G-GRE-GRE050402
"""
Vds=-0.2
bias(0.5)
rampVG1(-1015)
rampVG2(opengate)
rampVG3(opengate)
rampVG4(opengate)

rampVG5(opengate)
rampVG6(opengateL)

# a,b,c=sweep1D(VG1,-1016,-1022,301,0.01,ph2)
# plot_by_id(b)
# #calibG1 reflecto

a,b,c,d =sweep2D(rf2freq,373.5e6,374.5e6,101,0.02,VG1,-1683,-1687,101,0.02,ph2)
the_data = load_by_id(b)
data_list = the_data.get_parameter_data()
P = the_data.parameters
p = P.split(',')
Y= data_list[p[2]][p[0]]#freq
X = data_list[p[2]][p[1]]#gate
x = np.unique(X)
y = np.unique(Y)
z1 = data_list[p[2]][p[2]]
Z1 = z1.reshape((np.size(np.unique(Y)),np.size(np.unique(X))))
X,Y = np.meshgrid(x,y)
# #Boris remove bckgnd
# S = np.shape(Z1)
# Ph2 = np.zeros(S)

# for i in range(S[1]):
#     for j in range(S[0]):
#         Ph2[j,i] = Z1[j,i] -  np.mean(Z1[:,i])
def removeBackground(data,rangeMin=0, rangeMax=-1):
    for i in range(len(data)):
        data[i] = data[i] - data[i][rangeMin:rangeMax].mean() 
    return(data)

Z1=removeBackground(Z1)
f = plt.figure()
plt.pcolor(X,Y,Z1)
plt.xlabel(p[0])
plt.ylabel(p[1])
plt.colorbar()
plt.xlabel('G1(mV)')
plt.ylabel('rfS(Hz)')
plt.clim(vmin=None,vmax=0.3)
now=datetime.datetime.now()
dayFolder=datetime.date.isoformat(now)
name='G1vs_reflectoS_freq'
plt.savefig(folder2+'\\'+dayFolder+'\\'+str(dataid)+name+'.png')
            



a,b,c,d =sweep2D(rf1freq,296e6,297.5e6,101,0.02,VG6,-1871,-1875,101,0.02,ph1)
the_data = load_by_id(b)
data_list = the_data.get_parameter_data()
P = the_data.parameters
p = P.split(',')
Y= data_list[p[2]][p[0]]#freq
X = data_list[p[2]][p[1]]#gate
x = np.unique(X)
y = np.unique(Y)
z1 = data_list[p[2]][p[2]]
Z1 = z1.reshape((np.size(np.unique(Y)),np.size(np.unique(X))))
X,Y = np.meshgrid(x,y)
# #Boris remove bckgnd
# S = np.shape(Z1)
# Ph2 = np.zeros(S)

# for i in range(S[1]):
#     for j in range(S[0]):
#         Ph2[j,i] = Z1[j,i] -  np.mean(Z1[:,i])
def removeBackground(data,rangeMin=0, rangeMax=-1):
    for i in range(len(data)):
        data[i] = data[i] - data[i][rangeMin:rangeMax].mean() 
    return(data)

Z1=removeBackground(Z1)
f = plt.figure()
plt.pcolor(X,Y,Z1)
plt.xlabel(p[0])
plt.ylabel(p[1])
plt.colorbar()
plt.xlabel('G6(mV)')
plt.ylabel('rf_D(Hz)')
plt.clim(vmin=None,vmax=0.3)
now=datetime.datetime.now()
dayFolder=datetime.date.isoformat(now)
name='G6vs_reflectoD_freq'
plt.savefig(folder2+'\\'+dayFolder+'\\'+str(dataid)+name+'.png')




######otherside

rampVG1(opengateL)
rampVG2(opengate)
rampVG3(opengate)
rampVG4(opengate)

rampVG5(opengate)
rampVG6(-946)

# a,b,c=sweep1D(VG6,-800,-1500,1001,0.01,ph1)
# # plot_by_id(b)

# a,b,c=sweep1D(VG6,-948,-958,301,0.01,ph1)
# plot_by_id(b)


a,b,c,d =sweep2D(rf1freq,291e6,300e6,101,0.02,VG6,-946,-956,201,0.02,ph1,A1)
the_data = load_by_id(b)
data_list = the_data.get_parameter_data()
P = the_data.parameters
p = P.split(',')
Y= data_list[p[2]][p[0]]#freq
X = data_list[p[2]][p[1]]#gate
x = np.unique(X)
y = np.unique(Y)
z1 = data_list[p[2]][p[2]]
Z1 = z1.reshape((np.size(np.unique(Y)),np.size(np.unique(X))))
X,Y = np.meshgrid(x,y)
# #Boris remove bckgnd
# S = np.shape(Z1)
# Ph2 = np.zeros(S)

# for i in range(S[1]):
#     for j in range(S[0]):
#         Ph2[j,i] = Z1[j,i] -  np.mean(Z1[:,i])
def removeBackground(data,rangeMin=0, rangeMax=-1):
    for i in range(len(data)):
        data[i] = data[i] - data[i][rangeMin:rangeMax].mean() 
    return(data)

Z1=removeBackground(Z1)
f = plt.figure()
plt.pcolor(X,Y,Z1)
plt.xlabel(p[0])
plt.ylabel(p[1])
plt.colorbar()
plt.xlabel('G6(mV)')
plt.ylabel('rfD(Hz)')
plt.clim(vmin=None,vmax=0.3)
now=datetime.datetime.now()
dayFolder=datetime.date.isoformat(now)
name='G6vs_reflectoD_freq'
plt.savefig(folder2+'\\'+dayFolder+'\\'+str(dataid)+name+'.png')


a,b,c,d =sweep2D(rf3freq,405e6,417e6,101,0.02,VG6,-946,-956,201,0.02,ph3,A3)
the_data = load_by_id(b)
data_list = the_data.get_parameter_data()
P = the_data.parameters
p = P.split(',')
Y= data_list[p[2]][p[0]]#freq
X = data_list[p[2]][p[1]]#gate
x = np.unique(X)
y = np.unique(Y)
z1 = data_list[p[2]][p[2]]
Z1 = z1.reshape((np.size(np.unique(Y)),np.size(np.unique(X))))
X,Y = np.meshgrid(x,y)
# #Boris remove bckgnd
# S = np.shape(Z1)
# Ph2 = np.zeros(S)

# for i in range(S[1]):
#     for j in range(S[0]):
#         Ph2[j,i] = Z1[j,i] -  np.mean(Z1[:,i])
def removeBackground(data,rangeMin=0, rangeMax=-1):
    for i in range(len(data)):
        data[i] = data[i] - data[i][rangeMin:rangeMax].mean() 
    return(data)

Z1=removeBackground(Z1)
f = plt.figure()
plt.pcolor(X,Y,Z1)
plt.xlabel(p[0])
plt.ylabel(p[1])
plt.colorbar()
plt.xlabel('G6(mV)')
plt.ylabel('rfG6(Hz)')
plt.clim(vmin=None,vmax=0.3)
now=datetime.datetime.now()
dayFolder=datetime.date.isoformat(now)
name='G6vs_reflectoG6_freq'
plt.savefig(folder2+'\\'+dayFolder+'\\'+str(dataid)+name+'.png')
            
            
            
    







#POWER CALIBRATI
a,b,c,d =sweep2D(rf2power,-10,-40,61,0.02,VG1,-1121,-1125.5,81,0.02,ph2,A2)

the_data = load_by_id(b)
data_list = the_data.get_parameter_data()
P = the_data.parameters
p = P.split(',')
Y= data_list[p[2]][p[0]]#freq
X = data_list[p[2]][p[1]]#gate
x = np.unique(X)
y = np.unique(Y)
z1 = data_list[p[2]][p[2]]
Z1 = z1.reshape((np.size(np.unique(Y)),np.size(np.unique(X))))
X,Y = np.meshgrid(x,y)

def removeBackground(data,rangeMin=0, rangeMax=-1):
    for i in range(len(data)):
        data[i] = data[i] - data[i][rangeMin:rangeMax].mean() 
    return(data)

Z1=removeBackground(Z1)
f = plt.figure()
plt.pcolor(X,Y,Z1)
plt.xlabel(p[0])
plt.ylabel(p[1])
plt.colorbar()
plt.xlabel('G1(mV)')
plt.ylabel('rf1_power(dBm)')
# plt.clim(vmin=None,vmax=0.3)
now=datetime.datetime.now()
dayFolder=datetime.date.isoformat(now)
name='G1vs_reflectoS_power'
plt.savefig(folder2+'\\'+dayFolder+'\\'+str(dataid)+name+'.png')
            
            







