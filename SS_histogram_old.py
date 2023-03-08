# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 16:20:15 2020

@author: AA255540
"""

folder=r'C:/Users/AA255540/Desktop/dati e figurepaper/'
nome1=r'histogram_11Fidelity_phaseafter6ms_in_02_B-0.0T_ampliAWG_0.10000000149011612_counts_1000_-T1_-0.300V-T2_0.439V-T3_-0.400V-B1_-0.400V-B2_0.820V-B3_0.869V-bias_0.000V'
nome2=r'histogram_02Fidelity_phaseafter6ms_in_02_B-0.0001T_ampliAWG_0.10000000149011612_counts_1000_-T1_-0.300V-T2_0.439V-T3_-0.400V-B1_-0.400V-B2_0.820V-B3_0.869V-bias_0.000V'
nome3=r'histogram_02Fidelity_phaseafter6ms_in_02_B-0.0T_ampliAWG_0.05999999865889549_counts_1000_-T1_-0.300V-T2_0.439V-T3_-0.400V-B1_-0.400V-B2_0.820V-B3_0.869V-bias_0.000V'
###code I used in the measurement
# for j in range(0,5):
#     ampliAWG(0.06+0.02*j)    
#     Ntraces=1000
# #    Ntraces=2
# #    points=1125#5ms
#     phase_init=[]
#     phase_readout=[]
#     phase=[]
#     phase_readout2=[]
#     countaxis=np.linspace(1,Ntraces,Ntraces)
#     for i in range(0,Ntraces):
#         print(i)
#         phase.append(phase_pulsed_B3()[0])
#         phase_init.append(phase[i][5])#after 25us
#         phase_readout.append(phase[i][200])#after900us
#         phase_readout2.append(phase[i][1300])#after6ms
        
#     hist, bin_edges=np.histogram(phase_init,bins=101,range= (-0.021,0.007))
#     hist_read, bin_edges_read=np.histogram(phase_readout,bins=101,range= (-0.021,0.007))
#     hist_read2, bin_edges_read2=np.histogram(phase_readout2,bins=101,range= (-0.021,0.007))
    # plot.add_to_plot(x=bin_edges_read2[0:len(hist)],y=hist_read2,xlabel='phase',ylabel='counts',title='histogram_'+titolo)

###################    
nbin=101
phimin=-0.021
phimax=0.007
xax=np.linspace(phimin,phimax,nbin)

with open(folder+nome1+'.txt', 'r') as f:
    lines = f.read().splitlines()
c11=[]
for i in range(0,len(x)):
  c11.append(float(lines[i]))  

xax2=np.linspace(phimax,phimin,nbin)
with open(folder+nome2+'.txt', 'r') as f:
    lines = f.read().splitlines()
c02=[]
for i in range(0,len(x)):
  c02.append(float(lines[i]))  
  
  
with open(folder+nome3+'.txt', 'r') as f:
    lines = f.read().splitlines()
c02=[]
for i in range(0,len(x)):
  c02.append(float(lines[i]))   
