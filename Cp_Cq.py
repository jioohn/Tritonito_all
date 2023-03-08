# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 16:38:52 2021

@author: G-GRE-GRE050402
"""

def from_V_to_dBm(a):
    b=10*np.log10(a*a/50*1e6*1e-3)
    return b

def from_dBm_to_V(a):
    # b=np.log10(a*a/50*1e6*1e-3)**10
    b=np.sqrt(50*10**(a/10)*1e-3)
    return b

##D
f0=296.93e6
f1=296.89e6
L=330e-9




Cp=1/(4*np.pi*np.pi*L*f0*f0)

Cq=1/(4*np.pi*np.pi*L*f1*f1)-Cp

print(str(Cp*1e18)+'aF')
print(str(Cq*1e18)+'aF')

###rifaccio in V

# Psent=12.5e-3#12.5mV
attenuation=40#dB
coupler=20#dB/25
# Pdelivered=125e-6#if att =-40dB


Pdelivered=-25-attenuation-coupler


Preflected =558e-6#mV

RTampli=+35#dB
LNF=+32#dB
Poff_dev=from_V_to_dBm(Preflected)-LNF-RTampli

Gamma=from_dBm_to_V(Poff_dev)/from_dBm_to_V(Pdelivered)

# Gamma=(Z-Z0)/(Z+Z0)=Vout/Vin
Z=50*(1+Gamma)/(1-Gamma)

# on resonance Z=R

# R=L/(Z*Cp)












##G6
f0=412.51e6
f1=412.49e6
L=270e-9



Cp=1/(4*np.pi*np.pi*L*f0*f0)

Cq=1/(4*np.pi*np.pi*L*f1*f1)-Cp

print(str(Cp*1e18)+'aF')
print(str(Cq*1e18)+'aF')

###rifaccio in V

Psent=12.5e-3#12.5mV
attenuation=40#dB
coupler=20#dB/25
Pdelivered=125e-6#if att =-40dB


Pdelivered=-15-attenuation-coupler



# Pdelivered2=12.5e-6#if att =-60dB
# Gamma=(Z-Z0)/(Z+Z0)
# Preflected=Gamma*pdelivered+32dBm

Preflected =2.722e-3#mV

RTampli=+35#dB
LNF=+32#dB
Poff_dev=from_V_to_dBm(Preflected)-32-RTampli

Gamma=from_dBm_to_V(Poff_dev)/from_dBm_to_V(Pdelivered)

# Gamma=(Z-Z0)/(Z+Z0)=Vout/Vin
Z=50*(1+Gamma)/(1-Gamma)

# on resonance Z=R

# R=L/(Z*Cp)








###
########
####
###
#simulate resonance
freq_list=np.linspace(200e6,400e6,201)
resC=1/(2*np.pi*freq_list)
resL=