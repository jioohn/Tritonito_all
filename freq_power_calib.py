# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 13:29:17 2021

@author: G-GRE-GRE050402
"""
rampVG6(-1824)

# a,b,c=sweep1D(VG6,-800,-1500,1001,0.01,ph1)
# # plot_by_id(b)

# a,b,c=sweep1D(VG6,-948,-958,301,0.01,ph1)
# plot_by_id(b)
# ziUhf.daq.setInt('/dev2226/sigouts/0/on', 0)
# ziUhf.daq.setInt('/dev2226/sigouts/1/on', 1)
# VG6onmin_phD(-1400,-1450,401,1)
# VG6onmin_phG6(-1400,-1500,1001,1)
ziUhf.daq.setInt('/dev2226/sigouts/0/on', 1)
ziUhf.daq.setInt('/dev2226/sigouts/1/on', 0)
a,b,c,d =sweep2D(rf1freq,411e6,415e6,101,0.02,VG6,-1915,-1917,81,0.02,A1,ph1)
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
plt.savefig(folder2+'\\'+dayFolder+'\\'+str(b)+name+'.png')




# a,b,c,d =sweep2D(rf1freq,411e6,413e6,51,0.02,VG6,-1412,-1414,41,0.02,A1)

# plot_by_id(b,name)


#####poxwer




a,b,c,d =sweep2D(G1power,0,-30,51,0.02,VG6,-1914,-1918,81,0.02,A1,ph1)
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
plt.ylabel('rfG6_power(dBm)')
plt.clim(vmin=None,vmax=0.3)
now=datetime.datetime.now()
dayFolder=datetime.date.isoformat(now)
name='G6vs_reflectoG6_power'
plt.savefig(folder2+'\\'+dayFolder+'\\'+str(b)+name+'.png')






a,b,c,d =sweep2D(Spower,-15,-50,51,0.02,VG6,-1914,-1918,81,0.02,A2,ph2)
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
plt.ylabel('rfS_power(dBm)')
plt.clim(vmin=None,vmax=0.3)
now=datetime.datetime.now()
dayFolder=datetime.date.isoformat(now)
name='G6vs_reflectoS_power'
plt.savefig(folder2+'\\'+dayFolder+'\\'+str(b)+name+'.png')