# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 16:12:10 2019

@author: G-GRE-GRE050402
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
x = []
y = []
z=[]
xdata=[]
ydata=[]
zdata=[]
xsimm=[]


folder= r'Z:\110-PHELIQS\110.05-LATEQS\110.05.01-QuantumSilicon\Tritonito\data\2019-10-04'
name=r'\TP12_1dscan_51averages.txt'
with open(folder+name,'r') as f:
     lines = f.readlines()
      #remove commas from datafile!!!
     y= np.array([line.split()[0] for line in lines],dtype='float64')
     
          

  
#y=-y
#smoothing    
#y=savgol_filter(y, 51, 3)    

detuningPoint1 = [466,556] # [B2=x,T2=y]
detuningPoint2 = [467.2,554.2]  
#eps7=np.sqrt((detuningPoint1[0]-detuningPoint2[0])**2 +(detuningPoint1[1]-detuningPoint2[1])**2) 
x=np.linspace(723,727,81) 
#x0=np.argmin(y)
#deltax=x[x0]-x[len(x)-1]/2
#xsimm=linspace(-x[len(x)-1]/2,x[len(x)-1]/2, len(x))
#xsimm=(xsimm-deltax)/1000#in mV

x=x/1000
x=x*alpha
#offset substraction
xsimm=x-0.7256*alpha
#cut bad points
y=y[6:]   
xsimm=xsimm[6:]
#


ydata=y
#plot.add_to_plot(x=xdata, y=ydata, xlabel='detuning(mV)', ylabel='phiB1(mrad)',title='TP7vsfield_450mK')
fig, ax = plt.subplots()
ax.set_xlabel('$\epsilon$ (V)',fontsize=fontSize)
ax.set_ylabel('$\phi $(mrad)',fontsize=fontSize)
#    plt.plot(xsimm,guessT/max(guessT))
plt.title('Fit at T='+str(T)+'K')
plt.plot(xsimm,y,'b+',label='data@'+str(T)+'K')#mV on x  
plt.show()


normalizey=y/min(y)+min(y)


def interdotfit_chargesensor_simple(x,*p):
#
##Sground
#    energysingletground=-0.5*((2*p[0])**2+ (alpha*x+p[3])**2)**0.5
##Sex
#    energysingletexc= +0.5*((2*p[0])**2+ (alpha*x+p[3])**2)**0.5 
##T0
#    energyT0=-alpha*x/2
##T-
#    energyTup=-alpha*x/2 -2*bohr*B
##T+
#    energyTdown=-alpha*x/2 +2*bohr*B
#    
#    #exponential
#    expsingletground=exp(-energysingletground*beta)
#    expsingletexc=exp(-energysingletexc*beta)
#  
##    expT0 =exp(-energyT0*p[4])
##    expTup=exp(-energyTup*p[4])
##    expTdown=exp(-energyTdown*p[4])
#
#    Z=expsingletground+expsingletexc+expT0+expTup+expTdown
#    BoltzmannSground=expsingletground/Z
#    BoltzmannSexc=expsingletexc/Z
#    dE=x
    
#   return( p[2]+p[1]*(x*alpha/dE*tanh(dE/(2*kB*p[3]))))
    return( p[2]+p[1]*(np.tanh(x/(2*kb*p[0])))) 
   
   
const=+0.06
offset=-0.006
popt,pcov = curve_fit(interdotfit_chargesensor_simple,xsimm,y,p0=[T,offset,const],maxfev=3000)    
plt.plot(xsimm,interdotfit_chargesensor_simple(xsimm,*popt),'r',label='fit@'+str(T)+', alpha='+str(alpha)) 
    

Teff=popt[0]
Teff_error=pcov[0]/h*1e-9
er=np.sqrt(np.diag(pcov))
errort=er[0]/h*1e-9
