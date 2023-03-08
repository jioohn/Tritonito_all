# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 18:14:50 2020

@author: AA255540
"""

import matplotlib.pyplot as plt
import numpy as np
from numpy import exp, linspace, random
from scipy.optimize import curve_fit
from scipy import asarray as ar,exp
from scipy.signal import savgol_filter
import math
import qcodes as qc

kb=8.617333262*1e-5#(eV/K)
T=0.36
beta=1/(kb*T)
alpha=0.23
bohr=5.7883818e-5#eV*T
fontSize=16
h=4.135667*1e-15


location = r'C:\Users\AA255540\Desktop\dati e figurepaper\TP7/#088_TP7_detuningscanT350mK_0T_17-32-13'
loadedData = qc.load_data(location)
ycs=loadedData.phiB3
yrf=loadedData.phi
det=loadedData.detuning_set
detlen=np.sqrt((np.max(loadedData.B2)-np.min(loadedData.B2))**2+(np.max(loadedData.T2)-np.min(loadedData.T2))**2)
detstep=detlen/len(det)
detuningax=det*detstep


alpha=0.28#check again

argmin=np.argmin(scipy.signal.savgol_filter(loadedData.phi,21, 9))
argmin=np.argmin(loadedData.phi)
x0= detuningax[argmin]

xaxis=(detuningax-x0)*alpha/1000-1e-6#V
# xum= xaxis*1e6

def interdotfit_chargesensor_simple(x,*p):

#    dE=x
    
#   return( p[2]+p[1]*(x*alpha/dE*tanh(dE/(2*kB*p[3]))))
    return( p[2]+p[1]*(np.tanh(x/(2*kb*p[0])))) 
def interdotfit_chargesensor_simple(x,*p):

#    dE=x
    
#   return( p[2]+p[1]*(x*alpha/dE*tanh(dE/(2*kB*p[3]))))
    return( p[2]+p[1]*(np.tanh(x/(2*kb*p[0])))) 

offset=-0.07
tcoupling=500e6*h
# T=0.355
xum= xaxis*1e6

popt,pcov = curve_fit(interdotfit_chargesensor_simple,xaxis,ycs,p0=[T,offset,-0.007],maxfev=30000) 
err=er=np.sqrt(np.diag(pcov))
# plt.plot(xaxis,interdotfit_chargesensor_simple(xaxis,*popt),'r',label='fit:$T=$'+str(np.round(popt[0],3))+'$\pm$'+str(np.round(err[0],3))+'K')
fig, ax = plt.subplots()
plt.plot(xum,ycs,'+',label='data')
plt.plot(xum,interdotfit_chargesensor_simple(xaxis,*popt),'r',label='fit:$T=$'+str(np.round(popt[0],3))+'$\pm$'+str(np.round(err[0],3))+'K')
ax.set_xlabel('$\epsilon$ ($\mu eV$)',fontsize=fontSize)
ax.set_ylabel('$\phi_{CS} $(rad)',fontsize=fontSize)    
plt.legend()
plt.savefig('fitT')


T=popt[0]
def interdotfit_chargesensor_alpha_Tfix(x,*p):

# #    dE=x
# #       return( p[2]+p[1]*(x*alpha/dE*np.tanh(x/(2*kb*p[0]))))
    return( p[1]+p[2]*x/np.sqrt(x**2+(2*p[0])**2)*(np.tanh(np.sqrt(x**2+(2*p[0])**2)/(2*kb*T)))) 

xaxis=(detuningax-x0)*alpha/1000#+10e-6#V
xum= xaxis*1e6
offset=-0.007
tcoupling=5e9*h
# T=0.355
parameter_bounds=([1e9*h,-8e-3,-8e-3],[8e9*h,-6e-3,-6e-3])
popt,pcov = curve_fit(interdotfit_chargesensor_alpha_Tfix,xaxis,ycs,p0=[tcoupling,-7.25e-3,-0.0069],bounds=parameter_bounds,maxfev=10000) #,bounds=parameter_bounds
tunnel=popt[0]/h*1e-9
er=np.sqrt(np.diag(pcov))
terr=er[0]/h*1e-9


fig, ax = plt.subplots()
plt.plot(xum,ycs,'+',label='data')

plt.plot(xum,interdotfit_chargesensor_alpha_Tfix(xaxis,*popt),'r',label='fit: $t=$'+str(np.abs(np.round(tunnel,1)))+'$\pm$'+str(np.round(terr,1)) +'GHz')
ax.set_xlabel('$\epsilon$ ($\mu eV$)',fontsize=fontSize)
ax.set_ylabel('$\phi_{CS}$ (rad)',fontsize=fontSize)    
plt.legend()
# plt.plot(xum,yrf,'+',label='data')
plt.savefig('chargesensingfit_findtunnel2_T'+str(T)+'.png')




# tcoupling=popt[2]/h*1e-9
# print(tcoupling)
#

x0= detuningax[argmin]

xaxis=(detuningax-x0)*alpha/1000-1e-6#V-
xum= xaxis*1e6


beta=1/(kb*T)
B=0
def interdotfit_alphafix(x,*p):

#Sground
    energysingletground=-0.5*((2*p[0])**2+ (alpha*x)**2)**0.5
#Sex
    energysingletexc= +0.5*((2*p[0])**2+ (alpha*x)**2)**0.5 
#T0
    energyT0=-alpha*x/2
#T-
    energyTup=-alpha*x/2 -2*bohr*B
#T+
    energyTdown=-alpha*x/2 +2*bohr*B
    #exponential
    expsingletground=exp(-energysingletground*beta)
    expsingletexc=exp(-energysingletexc*beta)
  
    expT0 =exp(-energyT0*beta)
    expTup=exp(-energyTup*beta)
    expTdown=exp(-energyTdown*beta)

    Z=expsingletground+expsingletexc+expT0+expTup+expTdown
    BoltzmannSground=expsingletground/Z
    BoltzmannSexc=expsingletexc/Z
#p[0]-->t
#p[1]-->const
#    return (2*t)**2 / ( (2*t)**2+ x**2)**1.5*exp(-E/(kb*T))*const
    # return p[2]+ p[1]*(2*p[0])**2 / ( (2*p[0])**2+ (x-p[3])**2)**1.5 *(-BoltzmannSground+BoltzmannSexc)

    return p[2]+ p[1]*(2*p[0])**2 / ( (2*p[0])**2+ (x)**2)**1.5 *(-BoltzmannSground+BoltzmannSexc)

offset=0.007
tcoupling=5e9*h

popt,pcov = curve_fit(interdotfit_alphafix,xaxis,yrf,p0=[tcoupling,offset,0],maxfev=3000) 

tcoupling=popt[0]/h*1e-9
er=np.sqrt(np.diag(pcov))
terr=er[0]/h*1e-9
fig, ax = plt.subplots()
plt.plot(xum,yrf,'+',label='data')
plt.plot(xum,interdotfit_alphafix(xaxis,*popt),'r',label='fit: $t=$'+str(np.round(tcoupling,1))+'$\pm$'+str(np.round(terr,1)) +'GHz')
ax.set_xlabel('$\epsilon$ ($\mu eV$)',fontsize=fontSize)
ax.set_ylabel('$\phi_{rf}$ (rad)',fontsize=fontSize)      
plt.legend()

plt.savefig('interdotfit_tunnel_argmin_T'+str(T)+'.png')


# beta=1/(kb*T)
# B=0
# t=tcoupling*h*1e9
# #doesn't work
# def interdotfit_alphafix_tfix(x,*p):
#     beta=1/(kb*p[0])
# #Sground
#     energysingletground=-0.5*((2*t)**2+ (alpha*x)**2)**0.5
# #Sex
#     energysingletexc= +0.5*((2*t)**2+ (alpha*x)**2)**0.5 
# #T0
#     energyT0=-alpha*x/2
# #T-
#     energyTup=-alpha*x/2 -2*bohr*B
# #T+
#     energyTdown=-alpha*x/2 +2*bohr*B
#     #exponential
#     expsingletground=exp(-energysingletground*beta)
#     expsingletexc=exp(-energysingletexc*beta)
  
#     expT0 =exp(-energyT0*beta)
#     expTup=exp(-energyTup*beta)
#     expTdown=exp(-energyTdown*beta)

#     Z=expsingletground+expsingletexc+expT0+expTup+expTdown
#     BoltzmannSground=expsingletground/Z
#     BoltzmannSexc=expsingletexc/Z
# #p[0]-->t
# #p[1]-->const
# #    return (2*t)**2 / ( (2*t)**2+ x**2)**1.5*exp(-E/(kb*T))*const
#     return p[2]+ p[1]*(2*t)**2 / ( (2*t)**2+ (x)**2)**1.5 *(-BoltzmannSground+BoltzmannSexc)


# popt,pcov = curve_fit(interdotfit_alphafix_tfix,xaxis,ycs,p0=[T,offset,-0.007],maxfev=30000) 
# err=er=np.sqrt(np.diag(pcov))
# fig, ax = plt.subplots()
# plt.plot(xum,yrf,'+',label='data')
# plt.plot(xum,interdotfit_alphafix_tfix(xaxis,*popt),'r',label='fit:$T=$'+str(np.round(popt[0],3))+'$\pm$'+str(np.round(err[0],3))+'K')
# ax.set_xlabel('$\epsilon$ ($\mu eV$)',fontsize=fontSize)
# ax.set_ylabel('$\phi_{CS} $(rad)',fontsize=fontSize)    
# plt.legend()
# plt.savefig('fit_rfinterdot_T')
