# -*- coding: utf-8 -*-
"""
Created on Tue May 18 17:56:36 2021

@author: G-GRE-GRE050402
"""

import matplotlib.colors as colors
X2=[]
Y2=[]
# Z2=np.zeros((122,183))

Z2=np.zeros((183,122))


Y2=np.linspace(-740,-800,183)
X2=np.linspace(-740,-780,122)

# f = plt.figure()
for i in range (0,6):
    
    # f = plt.figure()
    if i==0:
        dataid=321
        the_data = load_by_id(dataid)
    elif i==1:
        dataid=324
        the_data = load_by_id(dataid)
    elif i==2:
        dataid=327
        the_data = load_by_id(dataid)
    elif i==3:
        dataid=339
        the_data = load_by_id(dataid)

    elif i==4:
        dataid=342
        the_data = load_by_id(dataid)

    elif i==5:
        dataid=345
        the_data = load_by_id(dataid)

        
    
    data_list = the_data.get_parameter_data()
    P = the_data.parameters
    p = P.split(',')
    Y= data_list[p[2]][p[0]]#gate4
    X = data_list[p[2]][p[1]]#gate3+5
    
    x = np.unique(X)
    y = np.unique(Y)
    # if i>=16:
    #     y=np.add(y,3.5)
    z1 = data_list[p[3]][p[3]]#phS
    if i>=3:
        z1=np.subtract(z1,13)
    Z = z1.reshape((np.size(np.unique(Y)),np.size(np.unique(X))))
    X,Y = np.meshgrid(x,y)
    # Z=np.transpose(Z)
    Z=np.flip(Z)
    # X2.append(X)
    # Y2.append(Y)
    if i==0:
        Z2[0:len(Z),0:len(Z)]=np.flip(np.transpose(Z))
    elif i==1:
        Z2[len(Z):2*len(Z),0:len(Z),]=np.flip(np.transpose(Z))
    elif i==2:
        Z2[2*len(Z):3*len(Z),0:len(Z)]=np.flip(np.transpose(Z))
    elif i==3:
        Z2[0:len(Z),len(Z):2*len(Z)]=np.flip(np.transpose(Z))

    elif i==4:
        Z2[len(Z):2*len(Z),len(Z):2*len(Z)]=np.flip(np.transpose(Z))

    elif i==5:
        Z2[2*len(Z):3*len(Z),len(Z):2*len(Z)]=np.flip(np.transpose(Z))
    # plt.pcolor(Y,X,Z)

Z2=np.abs(Z2)
f = plt.figure()
plt.pcolor(X2,Y2,Z2,norm=colors.LogNorm(vmin=Z2.min(),vmax=Z2.max()))
plt.xlabel(p[0])
plt.ylabel(p[1])
plt.colorbar(label='$\phi_S(rad)$')
plt.xlabel('G3(mV)')
plt.ylabel('G4(mV)')
# plt.clim(vmin=None,vmax=0.3)
now=datetime.datetime.now()
dayFolder=datetime.date.isoformat(now)
name='BIGMAP_collage-corr_G3vsG4_LOG_phS_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
plt.savefig(folder2+'\\'+dayFolder+'\\'+str(dataid)+name+'.png')