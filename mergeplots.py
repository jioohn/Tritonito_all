# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 11:43:44 2021

@author: G-GRE-GRE050402
"""


# VG4(-820)
# # VG1onmin_phS(-1500,-1800,2001,1)

# name=str(Bfield())+'T_G2vsG3_G4filled__G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'

# a,dataid,c,d=sweep2D(VG2,-1000,-1100,201,0.013,VG3,-760,-860,201,0.01,ph2)
# plot_by_id(dataid)
# saveplot(name,dataid)


# # VG6onmin_phD(-1500,-1800,2001,1)

# VG3(-860)
# name=str(Bfield())+'T_G4vsG5_G3filled_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'

# a,dataid,c,d=sweep2D(VG5,-1300,-1400,201,0.013,VG4,-720,-820,201,0.01,ph1)
# plot_by_id(dataid)
# saveplot(name,dataid)


rampVG1(-0)
rampVG2(-0)
rampVG3(-0)
rampVG4(-0)
rampVG5(-0)
rampVG6(-0)





# slopeG3G2=-0.20199999999999816
# slopeG4G2=-0.022000000000025464
# slopeG3G5=-0.013999999999987267
# slopeG4G5=-0.21200000000003455
slopeG3G2=-0.25
slopeG4G2=-0.022000000000025464
slopeG3G5=-0.013999999999987267
slopeG4G5=-0.25

slopeG3G2=-0.3
# slopeG4G2=-0.022000000000025464
# slopeG3G5=-0.013999999999987267
slopeG4G5=-0.3

VG4comp=  SpecialParameters.CompensateG4(VG4,VG5,slopeG4G5)
VG3comp=  SpecialParameters.CompensateG3(VG3,VG2,slopeG3G2)



rampVG1(-1610)
rampVG2(-1450)
rampVG3(-700)
rampVG4(-700)
rampVG5(-1633)
rampVG6(-1698)


rampVG3(-730)
rampVG4(-690)
VG5now=VG5()
VG2now=VG2()
VG6now=VG6()
VG1now=VG1()

VG6onmin_phD(VG6now-10,VG6now+10,401,1)
# VG5onmin_phD(VG5now-20,VG5now+20,401,1)

VG1onmin_phS(VG1now-10,VG1now+10,401,1)
# VG2onmin_phS(VG2now-20,VG2now+20,401,1)

VG5now=VG5()
VG2now=VG2()
VG6now=VG6()
VG1now=VG1()

VG6onmin_phD(VG6now-5,VG6now+5,401,1)
# VG5onmin_phD(VG5now-20,VG5now+20,401,1)

VG1onmin_phS(VG1now-5,VG1now+5,401,1)
# VG2onmin_phS(VG2now-20,VG2now+20,401,1)


continuous_acquisition()
continuous_acquisition_ch2()

name=str(Bfield())+'T_CALIB_G3vsG4_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
# a,dataid,c,d=sweep2D(VG3comp,-762,-766,41,0.02,VG4comp,-976,-982,61,0.014,ph1,ph2)
a,dataid,c,d=sweep2D(VG3comp,-720,-740,41,0.02,VG4comp,-680,-700,41,0.012,ph1,ph2)
plot_by_id(dataid)
save2plots(name,dataid)


for i in range(0,6):
    for j in range(0,6):
        rampVG3(-730-20*i)
        rampVG4(-690-20*j)

        VG5now=VG5()
        VG2now=VG2()
        VG6now=VG6()
        VG1now=VG1()

        VG6onmin_phD(VG6now-5,VG6now+5,401,1)
        # VG5onmin_phD(VG5now-3,VG5now+3,401,1)
        
        VG1onmin_phS(VG1now-5,VG1now+5,401,1)
        # VG2onmin_phS(VG2now-3,VG2now+3,401,1)
    
        name=str(Bfield())+'T_G3vsG4_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
        # a,dataid,c,d=sweep2D(VG3comp,-760-20*i,-780-20*i,51,0.02,VG4comp,-800-20*j,-820-20*j,51,0.014,ph1,ph2)
        a,dataid,c,d=sweep2D(VG3comp,-720-20*i,-740-20*i,51,0.02,VG4comp,-680-20*j,-700-20*j,51,0.016,ph1,ph2)
        
        plot_by_id(dataid)
        save2plots(name,dataid)
        
        
        
        
# data_id=dataid
        
# dataid_init=data_id-3*(i)*(j)  +3     
      
dataid_init=429
# dataid_init=[595,598,599]
f = plt.figure()
for i in range (0,36):
    
    # f = plt.figure()
    dataid=dataid_init+3*i
    
    # dataid=dataid_init[i]
    the_data = load_by_id(dataid)
    data_list = the_data.get_parameter_data()
    P = the_data.parameters
    p = P.split(',')
    Y= data_list[p[2]][p[0]]#gate4
    X = data_list[p[2]][p[1]]#gate3
    x = np.unique(X)
    y = np.unique(Y)
    # if i>=16:
    #     y=np.add(y,3.5)
    z1 = data_list[p[2]][p[2]]#phD
    Z = z1.reshape((np.size(np.unique(Y)),np.size(np.unique(X))))
    X,Y = np.meshgrid(x,y)
    # Z=np.transpose(Z)
    Z=np.flip(Z)
    plt.pcolor(Y,X,Z)




plt.xlabel(p[0])
plt.ylabel(p[1])
plt.colorbar(label='$\phi_D(rad)$')
plt.xlabel('G3(mV)')
plt.ylabel('G4(mV)')
# plt.clim(vmin=None,vmax=0.3)
now=datetime.datetime.now()
dayFolder=datetime.date.isoformat(now)
name='BIGMAP_collage_corr_G3vsG4_phD_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
plt.savefig(folder2+'\\'+dayFolder+'\\'+str(dataid)+name+'.png')

###same for phiS
f = plt.figure()
for i in range (0,36):
    
    # f = plt.figure()
    dataid=dataid_init+3*i
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
    Z = z1.reshape((np.size(np.unique(Y)),np.size(np.unique(X))))
    X,Y = np.meshgrid(x,y)
    # Z=np.transpose(Z)
    Z=np.flip(Z)
    plt.pcolor(Y,X,Z)




plt.xlabel(p[0])
plt.ylabel(p[1])
plt.colorbar(label='$\phi_S(rad)$')
plt.xlabel('G3(mV)')
plt.ylabel('G4(mV)')
# plt.clim(vmin=None,vmax=0.3)
now=datetime.datetime.now()
dayFolder=datetime.date.isoformat(now)
name='BIGMAP_collage-corr_G3vsG4_phS_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
plt.savefig(folder2+'\\'+dayFolder+'\\'+str(dataid)+name+'.png')



