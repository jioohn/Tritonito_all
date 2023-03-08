# -*- coding: utf-8 -*-
"""
Created on Mon May  3 23:02:41 2021

@author: G-GRE-GRE050402
"""




VG4comp(-811)
VG3comp(-867)
VG6now=VG6()
VG5now=VG5()
VG2now=VG2()
VG1now=VG1()


continuous_acquisition()
continuous_acquisition_ch2()

# VG6onmin_phD(VG6now-30,VG6now+30,1201,1)

# VG1onmin_phS(VG1now+30,VG1now-30,1201,1)
# VG5onmin_phD(VG5now-10,VG5now+10,401,1)
# VG2onmin_phS(VG2now-10,VG2now+10,401,1)
VG1onmin_phS(VG1now-8,VG1now+8,401,1)

VG6onmin_phD(VG6now-5,VG6now+5,401,1)

# # # VG1onmin_phS(VG1now-10,VG1now+10,401,1)
# VG2onmin_phS(VG2now-10,VG2now+10,401,1)

continuous_acquisition()
continuous_acquisition_ch2()

name=str(Bfield())+'T_CALIB_G3vsG4_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4())+'mV_G5'+str(VG5())+'mV_G6'+str(VG6())+'mV'

# a,dataid,c,d=sweep2D(VG3comp,-870,-850,51,0.02,VG4comp,-820,-800,51,0.014,ph1,ph2)
# a,dataid,c,d=sweep2D(VG3comp,-863,-866,31,0.02,VG4comp,-797,-794,31,0.014,ph2,ph1)
a,dataid,c,d=sweep2D(VG3comp,-867,-871,31,0.02,VG4comp,-808,-811,41,0.014,ph2,ph1)
plot_by_id(dataid)
save2plots(name,dataid)




num_point=101
tc=5e-6
total_time=1
demod_S=2
demod_D=1
startG4=-754
stopG4=-758
startG3=-749
stopG3=-748.5

pathS=folder2+'\\'+dayFolder+'\\'+str(Bfield())+'_T_interdot_VG3'+str(startG3)+'_mV_VG4='+str(startG4)+'mV_phS_3'
path2S = pathS + f'/time_traces'
pathD=folder2+'\\'+dayFolder+'\\'+str(Bfield())+'_T_interdot-VG3='+str(startG3)+'_mV_VG4='+str(startG4)+'mV_phD_3'
path2D = pathD + f'/time_traces'

continuous_acquisition()
continuous_acquisition_ch2()
Threshold_S,Threshold_D=fit_interdot(startG4,stopG4,startG3,stopG3)#plot, fit and sit on interdot

Threshold_S=Threshold_S*np.pi/180
Threshold_D=Threshold_D*np.pi/180

G3now=VG3()
G4now=VG4()

bubbles=False
# bubbles=True

if bubbles:
    G3now=VG3()
    G4now=VG4()
    #bubbles SNR on interdot for phiS
    title='IQ_On_interdot_tc'+str(tc)
    VG3comp(G3now)
    VG4comp(G4now)
    blopIQ_interdot(daq_S,tc,total_time,demod_S,pathS,title=title)
    
    VG3comp(startG3)
    VG4comp(startG4)
    title='IQ_in01_tc'+str(tc)
    
    
    blopIQ_interdot(daq_S,tc,total_time,demod_S,pathS,title='IQ_in01_tc'+str(tc))
    
    VG3comp(stopG3)
    VG4comp(stopG4)
    title='IQ_in10_tc'+str(tc)
    
    
    blopIQ_interdot(daq_S,tc,total_time,demod_S,pathS,title='IQ_in10_tc'+str(tc))
    
    path_dbb=[pathS + '\\IQ_in01_tc'+str(tc)+'.txt',pathS + '\\IQ_in10_tc'+str(tc)+'.txt']
    
    
    draw_multiple_bbl_interdot(path_dbb,pathS)
    
    #bubbles SNR on interdot for phiD
    VG3comp(G3now)
    VG4comp(G4now)
    title='IQ_On_interdot_tc'+str(tc)
    
    blopIQ_interdot(daq_D,tc,total_time,demod_D,pathD,title=title)
    
    VG3comp(startG3)
    VG4comp(startG4)
    title='IQ_in01_tc'+str(tc)
    
    
    blopIQ_interdot(daq_D,tc,total_time,demod_D,pathD,title='IQ_in01_tc'+str(tc))
    
    VG3comp(stopG3)
    VG4comp(stopG4)
    title='IQ_in10_tc'+str(tc)
    
    
    blopIQ_interdot(daq_D,tc,total_time,demod_D,pathD,title='IQ_in10_tc'+str(tc))
    
    path_dbb=[pathD + '\\IQ_in01_tc'+str(tc)+'.txt',pathD + '\\IQ_in10_tc'+str(tc)+'.txt']
    
    
    draw_multiple_bbl_interdot(path_dbb,pathD)


######analysis of occupation probabilities and tunnel rate
    
register_time_trace_interdot(daq_S,startG4,stopG4, startG3,stopG3,num_point,tc,total_time,demod_S,pathS,path2S)

gammarateinterdot_S=analyse_time_traces_interdot(pathS,startG4,stopG4,startG3,stopG3,Threshold_S)
  


register_time_trace_interdot(daq_D,startG4,stopG4, startG3,stopG3,num_point,tc,total_time,demod_D,pathD,path2D)

gammarateinterdot_D=analyse_time_traces_interdot(pathD,startG4,stopG4,startG3,stopG3,Threshold_D)
  
#################################
################"
 

#####analysis on dot lead G3 0,1-->11
num_point=101
tc=5e-6
total_time=1
demod_S=2
demod_D=1
startG4=-812.6
stopG4=-812.6
startG3=-864.8
stopG3=-863.2

pathS=folder2+'\\'+dayFolder+'\\'+str(Bfield())+'_T_DOTLEAD1_01_11_VG3'+str(startG3)+'_mV_VG4='+str(startG4)+'mV_phS_new'
path2S = pathS + f'/time_traces'

continuous_acquisition()
continuous_acquisition_ch2()
VG4comp(startG4)
VG3comp(startG3)
VG1now=VG1()

# VG1onmin_phS(VG1now-2,VG1now+2,201,1)

continuous_acquisition()
continuous_acquisition_ch2()
Threshold_S=fit_interdot_G3(startG3,stopG3,startG4)#plot, fit and sit on interdot

Threshold_S=Threshold_S*np.pi/180




#######
# Threshold_S=8*np.pi/180
###########


# a,dataid,c=sweep1D(VG3comp,startG3,stopG3,num_point,0.05,ph2)

name=str(dataid)+'_G3scan_01-11'
plot_by_id(dataid)
saveplot(name,dataid)

# Threshold_S=7*np.pi/180

G3now=VG3()
G4now=VG4()


if bubbles:
    G3now=VG3()
    G4now=VG4()
    #bubbles SNR on interdot for phiS
    title='IQ_On_dotlead01-11_tc'+str(tc)
    VG3comp(G3now)
    VG4comp(G4now)
    blopIQ_interdot(daq_S,tc,total_time,demod_S,pathS,title=title)
    
    VG3comp(startG3)
    VG4comp(startG4)
    title='IQ_in01_tc'+str(tc)
    
    
    blopIQ_interdot(daq_S,tc,total_time,demod_S,pathS,title='IQ_in01_tc'+str(tc))
    
    VG3comp(stopG3)
    VG4comp(stopG4)
    title='IQ_in11_tc'+str(tc)
    
    
    blopIQ_interdot(daq_S,tc,total_time,demod_S,pathS,title='IQ_in11_tc'+str(tc))
    
    path_dbb=[pathS + '\\IQ_in01_tc'+str(tc)+'.txt',pathS + '\\IQ_in11_tc'+str(tc)+'.txt']
    
    draw_multiple_bbl_interdot(path_dbb,pathS)



register_time_trace_interdot(daq_S,startG4,stopG4, startG3,stopG3,num_point,tc,total_time,demod_S,pathS,path2S)

gammarateS1=analyse_time_traces_interdot_S(pathS,startG4,stopG4,startG3,stopG3,Threshold_S)



#####analysis on dot lead G3 0,0-->10
num_point=101
tc=5e-6
total_time=1
demod_S=2
demod_D=1
startG4=-811.6
stopG4=-811.6
startG3=-864.8
stopG3=-863.2
pathS=folder2+'\\'+dayFolder+'\\'+str(Bfield())+'_T_DOTLEAD-00_10_VG3'+str(startG3)+'_mV_VG4='+str(startG4)+'mV_phS_new'
path2S = pathS + f'/time_traces'

continuous_acquisition()
continuous_acquisition_ch2()
VG4comp(startG4)
VG3comp(startG3)
VG1now=VG1()

# VG1onmin_phS(VG1now-2,VG1now+2,201,1)

continuous_acquisition()
continuous_acquisition_ch2()
Threshold_S=fit_interdot_G3(startG3,stopG3,startG4)#plot, fit and sit on interdot
Threshold_S=Threshold_S*np.pi/180

G3now=VG3()
G4now=VG4()
VG4comp(startG4)
# a,dataid,c=sweep1D(VG3comp,startG3,stopG3,num_point,0.015,ph2)

name=str(dataid)+'_G3scan_00-10'
plot_by_id(dataid)
saveplot(name,dataid)





# Threshold_S=7*np.pi/180



if bubbles:
    G3now=VG3()
    G4now=VG4()
    #bubbles SNR on interdot for phiS
    title='IQ_On_dotlead00-10_tc'+str(tc)
    VG3comp(G3now)
    VG4comp(G4now)
    blopIQ_interdot(daq_S,tc,total_time,demod_S,pathS,title=title)
    
    VG3comp(startG3)
    VG4comp(startG4)
    title='IQ_in00_tc'+str(tc)
    
    
    blopIQ_interdot(daq_S,tc,total_time,demod_S,pathS,title='IQ_in00_tc'+str(tc))
    
    VG3comp(stopG3)
    VG4comp(stopG4)
    title='IQ_in10_tc'+str(tc)
    
    
    blopIQ_interdot(daq_S,tc,total_time,demod_S,pathS,title='IQ_in10_tc'+str(tc))
    
    path_dbb=[pathS + '\\IQ_in00_tc'+str(tc)+'.txt',pathS + '\\IQ_in10_tc'+str(tc)+'.txt']
    
    draw_multiple_bbl_interdot(path_dbb,pathS)



register_time_trace_interdot(daq_S,startG4,stopG4, startG3,stopG3,num_point,tc,total_time,demod_S,pathS,path2S)

gammarateS2=analyse_time_traces_interdot_S(pathS,startG4,stopG4,startG3,stopG3,Threshold_S)


############################""
##analysis on dot lead G4 0,0-->0,1
num_point=101
tc=5e-6
total_time=1
demod_S=2
demod_D=1
startG4=-811.6
stopG4=-812.6
startG3=-863.2
stopG3=-863.2

continuous_acquisition()
continuous_acquisition_ch2()
VG4comp(startG4)
VG3comp(startG3)
VG6now=VG6()

# VG6onmin_phD(VG6now-2,VG6now+2,201,1)

pathD=folder2+'\\'+dayFolder+'\\'+str(Bfield())+'_T_DOTLEAD_01_00_VG3='+str(startG3)+'_mV_VG4='+str(startG4)+'mV_phD_new'
path2D = pathD + f'/time_traces'

continuous_acquisition()
continuous_acquisition_ch2()
Threshold_D=fit_interdot_G4(startG4,stopG4,startG3)#plot, fit and sit on interdot

continuous_acquisition()
continuous_acquisition_ch2()

a,dataid,c=sweep1D(VG4comp,startG4,stopG4,num_point,0.015,ph1)

name=str(dataid)+'_G4scan_calibrate_cs'
plot_by_id(dataid)
saveplot(name,dataid)

# Threshold_S=Threshold_S*np.pi/180
Threshold_D=Threshold_D*np.pi/180



G3now=VG3()
G4now=VG4()


if bubbles:
    VG3comp(G3now)
    VG4comp(G4now)
    title='IQ_On_dotlead00-01_tc'+str(tc)
    
    blopIQ_interdot(daq_D,tc,total_time,demod_D,pathD,title=title)
    
    VG3comp(startG3)
    VG4comp(startG4)
    title='IQ_in01_tc'+str(tc)
    
    
    blopIQ_interdot(daq_D,tc,total_time,demod_D,pathD,title='IQ_in01_tc'+str(tc))
    
    VG3comp(stopG3)
    VG4comp(stopG4)
    title='IQ_in00_tc'+str(tc)
    
    
    blopIQ_interdot(daq_D,tc,total_time,demod_D,pathD,title='IQ_in00_tc'+str(tc))
    
    path_dbb=[pathD + '\\IQ_in01_tc'+str(tc)+'.txt',pathD + '\\IQ_in00_tc'+str(tc)+'.txt']
    
    
    draw_multiple_bbl_interdot(path_dbb,pathD)




register_time_trace_interdot(daq_D,startG4,stopG4, startG3,stopG3,num_point,tc,total_time,demod_D,pathD,path2D)

gammarateD1=analyse_time_traces_interdot_D(pathD,startG4,stopG4,startG3,stopG3,Threshold_D)




##analysis on dot lead G4 1,1-->1,0
startG4=-811.6
stopG4=-812.6
startG3=-864.8
stopG3=-864.8


pathD=folder2+'\\'+dayFolder+'\\'+str(Bfield())+'_T_DOTLEAD_11_10_VG3='+str(startG3)+'_mV_VG4='+str(startG4)+'mV_phD_new'
path2D = pathD + f'/time_traces'


continuous_acquisition()
continuous_acquisition_ch2()
VG4comp(startG4)
VG3comp(startG3)
VG6now=VG6()

# VG6onmin_phD(VG6now-2,VG6now+2,201,1)


Threshold_D=fit_interdot_G4(startG4,stopG4,startG3)#plot, fit and sit on interdot
Threshold_D=Threshold_D*np.pi/180

continuous_acquisition()
continuous_acquisition_ch2()

a,dataid,c=sweep1D(VG4comp,startG4,stopG4,num_point,0.015,ph1)

name=str(dataid)+'_G4scan_calibrate_cs'
plot_by_id(dataid)
saveplot(name,dataid)

# Threshold_S=Threshold_S*np.pi/180


G3now=VG3()
G4now=VG4()

if bubbles:
    VG3comp(G3now)
    VG4comp(G4now)
    title='IQ_On_dotlead11-10_tc'+str(tc)
    
    blopIQ_interdot(daq_D,tc,total_time,demod_D,pathD,title=title)
    
    VG3comp(startG3)
    VG4comp(startG4)
    title='IQ_in11_tc'+str(tc)
    
    
    blopIQ_interdot(daq_D,tc,total_time,demod_D,pathD,title='IQ_in11_tc'+str(tc))
    
    VG3comp(stopG3)
    VG4comp(stopG4)
    title='IQ_in10_tc'+str(tc)
    
    
    blopIQ_interdot(daq_D,tc,total_time,demod_D,pathD,title='IQ_in10_tc'+str(tc))
    
    path_dbb=[pathD + '\\IQ_in11_tc'+str(tc)+'.txt',pathD + '\\IQ_in10_tc'+str(tc)+'.txt']
    
    
    draw_multiple_bbl_interdot(path_dbb,pathD)


######analysis of occupation probabilities and tunnel rate
  


register_time_trace_interdot(daq_D,startG4,stopG4, startG3,stopG3,num_point,tc,total_time,demod_D,pathD,path2D)

gammarateD2=analyse_time_traces_interdot_D(pathD,startG4,stopG4,startG3,stopG3,Threshold_D)

print('gamma_interdotS='+str(gammarateinterdot_S))
print('gamma_interdotD'+str(gammarateinterdot_D))
print('gamma01_00='+str(gammarateD1))
print('gamma11_10='+str(gammarateD2))
print('gamma01_11='+str(gammarateS1))
print('gamma00_10='+str(gammarateS2))
