# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 12:55:35 2021

@author: G-GRE-GRE050402
"""





for i in range(0,3):
    for j in range(0,3):
        rampVG3(-760-20*i)
        rampVG4(-760-20*j)
        VG5now=VG5()
        VG2now=VG2()
        VG6now=VG6()
        VG1now=VG1()

        VG6onmin_phD(VG6now-20,VG6now+20,801,1)
        VG5onmin_phD(VG5now-5,VG5now+5,401,1)
        
        VG1onmin_phS(VG1now-20,VG1now+20,801,1)
        VG2onmin_phS(VG2now-5,VG2now+5,401,1)
    
        name='G3vsG4_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV'
        a,dataid,c,d=sweep2D(VG3comp,-750-20*i,-770-20*i,51,0.02,VG4comp,-750-20*j,-770-20*j,51,0.012,ph1,ph2)
        plot_by_id(dataid)
        save2plots(name,dataid)
        
        
rampVG3(-720)
rampVG4(-720)
VG5now=VG5()
VG2now=VG2()
VG6now=VG6()
VG1now=VG1()

VG6onmin_phD(VG6now-20,VG6now+20,801,1)
VG5onmin_phD(VG5now-5,VG5now+5,401,1)

VG1onmin_phS(VG1now-20,VG1now+20,801,1)
VG2onmin_phS(VG2now-5,VG2now+5,401,1)

name='G3vsG4_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
a,dataid,c,d=sweep2D(VG3comp,-750,-680,71,0.05,VG4comp,-750,-680,71,0.012,ph1,ph2)
plot_by_id(dataid)
save2plots(name,dataid)


for i in range(0,4):
    for j in range(0,4):
        rampVG3(-800-20*i)
        rampVG4(-810-20*j)
        VG5now=VG5()
        VG2now=VG2()
        VG6now=VG6()
        VG1now=VG1()

        VG6onmin_phD(VG6now-20,VG6now+20,801,1)
        VG5onmin_phD(VG5now-5,VG5now+5,401,1)
        
        VG1onmin_phS(VG1now-20,VG1now+20,801,1)
        VG2onmin_phS(VG2now-5,VG2now+5,401,1)
    
        name='G3vsG4_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
        a,dataid,c,d=sweep2D(VG3comp,-790-20*i,-810-20*i,101,0.05,VG4comp,-800-20*j,-820-20*j,101,0.015,ph1,ph2,A1,A2,ph3,ph4)
        plot_by_id(dataid)
        save2plots(name,dataid)



        
        
rampVG3(-837)
rampVG4(-815.5)
VG5now=VG5()
VG2now=VG2()
VG6now=VG6()
VG1now=VG1()

VG6onmin_phD(VG6now-20,VG6now+20,801,1)
VG5onmin_phD(VG5now-5,VG5now+5,401,1)

VG1onmin_phS(VG1now-20,VG1now+20,801,1)
VG2onmin_phS(VG2now-5,VG2now+5,401,1)
name='G3vsG4_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
a,dataid,c,d=sweep2D(VG3comp,-835,-837,41,0.05,VG4comp,-815,-817,41,0.012,ph1,ph2)
plot_by_id(dataid)
save2plots(name,dataid)

#################
#NIGHT MEAS

for i in range(0,4):
    Bfield(2-0.5*i)
    name=str(Bfield)+'T_G3vsG4_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
    a,dataid,c,d=sweep2D(VG3comp,-835,-838,201,0.05,VG4comp,-815,-818,201,0.012,ph1,ph2)
    plot_by_id(dataid)
    save2plots(name,dataid)


VG1(-2000)
VG2(-1800)
for i in range(0,4):
    for j in range(0,4):
        rampVG3(-800-20*i)
        rampVG4(-810-20*j)
        VG5now=VG5()
        VG2now=VG2()
        VG6now=VG6()
        VG1now=VG1()

        VG6onmin_phD(VG6now-20,VG6now+20,801,1)
        VG5onmin_phD(VG5now-5,VG5now+5,401,1)
        
        VG1onmin_phS(VG1now-20,VG1now+20,801,1)
        VG2onmin_phS(VG2now-5,VG2now+5,401,1)
    
        name='G3vsG4_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
        a,dataid,c,d=sweep2D(VG3comp,-790-20*i,-810-20*i,101,0.05,VG4comp,-800-20*j,-820-20*j,101,0.015,ph1,ph2)
        plot_by_id(dataid)
        save2plots(name,dataid)
        

      
dataid_init=dataid-40
    
f = plt.figure()
for i in range (0,9):
    
    # f = plt.figure()
    dataid=dataid_init+5*i
    the_data = load_by_id(dataid)
    data_list = the_data.get_parameter_data()
    P = the_data.parameters
    p = P.split(',')
    Y= data_list[p[2]][p[0]]#gate4
    X = data_list[p[2]][p[1]]#gate3
    x = np.unique(X)
    y = np.unique(Y)
    z1 = data_list[p[2]][p[2]]
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
name='BIGMAP_collage_G3vsG4_phD_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
plt.savefig(folder2+'\\'+dayFolder+'\\'+str(dataid)+name+'.png')

###same for phiS
      

f = plt.figure()
for i in range (0,9):
    
    # f = plt.figure()
    dataid=dataid_init+5*i
    the_data = load_by_id(dataid)
    data_list = the_data.get_parameter_data()
    P = the_data.parameters
    p = P.split(',')
    Y= data_list[p[2]][p[0]]#gate4
    X = data_list[p[2]][p[1]]#gate3
    x = np.unique(X)
    y = np.unique(Y)
    z1 = data_list[p[3]][p[3]]
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
name='BIGMAP_collage_G3vsG4_phS_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
plt.savefig(folder2+'\\'+dayFolder+'\\'+str(dataid)+name+'.png')
        



VG5(-2000)
VG6(-1800)
for i in range(0,4):
    for j in range(0,4):
        rampVG3(-800-20*i)
        rampVG4(-810-20*j)
        VG5now=VG5()
        VG2now=VG2()
        VG6now=VG6()
        VG1now=VG1()

        VG6onmin_phD(VG6now-20,VG6now+20,801,1)
        VG5onmin_phD(VG5now-5,VG5now+5,401,1)
        
        VG1onmin_phS(VG1now-20,VG1now+20,801,1)
        VG2onmin_phS(VG2now-5,VG2now+5,401,1)
    
        name='G3vsG4_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
        a,dataid,c,d=sweep2D(VG3comp,-790-20*i,-810-20*i,101,0.05,VG4comp,-800-20*j,-820-20*j,101,0.015,ph1,ph2,A1,A2,ph3,ph4)
        plot_by_id(dataid)
        save2plots(name,dataid)
        

      
dataid_init=dataid-40
    
f = plt.figure()
for i in range (0,9):
    
    # f = plt.figure()
    dataid=dataid_init+5*i
    the_data = load_by_id(dataid)
    data_list = the_data.get_parameter_data()
    P = the_data.parameters
    p = P.split(',')
    Y= data_list[p[2]][p[0]]#gate4
    X = data_list[p[2]][p[1]]#gate3
    x = np.unique(X)
    y = np.unique(Y)
    z1 = data_list[p[2]][p[2]]
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
name='BIGMAP_collage_G3vsG4_phD_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
plt.savefig(folder2+'\\'+dayFolder+'\\'+str(dataid)+name+'.png')

###same for phiS
      

f = plt.figure()
for i in range (0,9):
    
    # f = plt.figure()
    dataid=dataid_init+5*i
    the_data = load_by_id(dataid)
    data_list = the_data.get_parameter_data()
    P = the_data.parameters
    p = P.split(',')
    Y= data_list[p[2]][p[0]]#gate4
    X = data_list[p[2]][p[1]]#gate3
    x = np.unique(X)
    y = np.unique(Y)
    z1 = data_list[p[3]][p[3]]
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
name='BIGMAP_collage_G3vsG4_phS_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
plt.savefig(folder2+'\\'+dayFolder+'\\'+str(dataid)+name+'.png')







VG1(-1700)
VG2(-1400)
VG3comp(-800)
VG4comp(-810)
VG5now=VG5()
VG2now=VG2()
VG6now=VG6()
VG1now=VG1()

VG6onmin_phD(VG6now-50,VG6now+50,1001,1)
VG5onmin_phD(VG5now-5,VG5now+5,401,1)

VG1onmin_phS(VG1now-50,VG1now+50,1001,1)
VG2onmin_phS(VG2now-5,VG2now+5,401,1)

for i in range(0,3):
    for j in range(0,3):
        rampVG3(-800-20*i)
        rampVG4(-800-20*j)
        VG5now=VG5()
        VG2now=VG2()
        VG6now=VG6()
        VG1now=VG1()

        VG6onmin_phD(VG6now-10,VG6now+10,401,1)
        VG5onmin_phD(VG5now-5,VG5now+5,201,1)
        
        VG1onmin_phS(VG1now-10,VG1now+10,401,1)
        VG2onmin_phS(VG2now-5,VG2now+5,201,1)
    
        name='G3vsG4_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
        a,dataid,c,d=sweep2D(VG3comp,-790-20*i,-810-20*i,41,0.05,VG4comp,-790-20*j,-810-20*j,41,0.015,ph1,ph2)
        plot_by_id(dataid)
        save2plots(name,dataid)


      
dataid_init=dataid-40
    
f = plt.figure()
for i in range (0,9):
    
    # f = plt.figure()
    dataid=dataid_init+5*i
    the_data = load_by_id(dataid)
    data_list = the_data.get_parameter_data()
    P = the_data.parameters
    p = P.split(',')
    Y= data_list[p[2]][p[0]]#gate4
    X = data_list[p[2]][p[1]]#gate3
    x = np.unique(X)
    y = np.unique(Y)
    z1 = data_list[p[2]][p[2]]
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
name='BIGMAP_collage_G3vsG4_phD_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
plt.savefig(folder2+'\\'+dayFolder+'\\'+str(dataid)+name+'.png')

###same for phiS
      

f = plt.figure()
for i in range (0,9):
    
    # f = plt.figure()
    dataid=dataid_init+5*i
    the_data = load_by_id(dataid)
    data_list = the_data.get_parameter_data()
    P = the_data.parameters
    p = P.split(',')
    Y= data_list[p[2]][p[0]]#gate4
    X = data_list[p[2]][p[1]]#gate3
    x = np.unique(X)
    y = np.unique(Y)
    z1 = data_list[p[3]][p[3]]
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
name='BIGMAP_collage_G3vsG4_phS_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'
plt.savefig(folder2+'\\'+dayFolder+'\\'+str(dataid)+name+'.png')