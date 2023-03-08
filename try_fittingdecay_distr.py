# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 13:27:47 2020

@author: G-GRE-GRE050402
"""

def rayleigh(t_hist02, *p):
    return ( (np.subtract(t_hist02,p[0]))/(p[1])*np.exp((-1*(np.subtract(t_hist02,p[0])**2)/(2*p[1]))))

popt,pcov = curve_fit(rayleigh,t_hist02[0:-1],counts_hist02,p0=[20,100],maxfev=10000) 
plt.plot(t_hist02[0:-1],rayleigh(t_hist02[0:-1],*popt))    

fig, ax = plt.subplots()
ax.set_xlabel(r'$\tau_{02}(\mu s)$',fontsize=fontSize)
ax.set_ylabel('$counts$ ',fontsize=fontSize)


counts_hist02=np.histogram(decay02_array,bins=100)[0]#,range(min(phase11,max(phase11))))[0]
t_hist02=np.histogram(decay02_array,bins=100)[1]

plt.hist(decay02_array,bins=100)


name=str(Bfield())+'T_decay_distr_tc5us_histogram_'+str(len(decay02_array))+'counts_A_pp_'+str(ampliAWG()*11)+'mV_G1'+str(VG1())+'mV_G2'+str(VG2())+'mV_G3'+str(VG3())+'mV_G4'+str(VG4()) 
plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',decay02_array)


from lmfit.models import SkewedGaussianModel

xvals, yvals = t_hist02[0:-1],counts_hist02

model = SkewedGaussianModel()

# set initial parameter values
params = model.make_params(amplitude=10, center=0, sigma=1, gamma=0)

# adjust parameters  to best fit data.
result = model.fit(yvals, params, x=xvals)

print(result.fit_report())
pylab.plot(xvals, yvals)
plt.plot(xvals, result.best_fit) 
