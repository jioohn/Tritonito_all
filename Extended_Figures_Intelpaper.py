# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 09:33:34 2020

@author: Tobias
"""
# For this analysis PycQED has to be installed, see the readme file for further instructions

import sys
import os
dirname = os.path.dirname(__file__)
parent_folder = os.path.abspath(__file__+'/../../')
sys.path.append('C:/Users/Tobias/Documents/GitHub/PycQED_py3') # Folder where PycQED is installed

from pycqed.analysis import measurement_analysis
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np
import scipy
import matplotlib
import qcodes
from matplotlib import cm
import scipy.optimize as optimize
import pandas as pd

mm_to_inch=0.0393701

plt.rcParams.update({'axes.labelsize': 7,'xtick.labelsize': 7,'ytick.labelsize': 7,
                    'legend.fontsize': 7,'lines.markersize': 3,'font.size': 7,
                    'font.family': u'sans-serif','font.sans-serif': ['Arial'],'text.usetex': False})


#%% basic functions

def fermi(x,a,b,c,d,e):
    return a*(1/(np.exp(b*(x-c)) +1)) + d*x + e

def ExpDampOscFunc(t, tau, frequency, phase, amplitude,
                   oscillation_offset, exponential_offset):
    return amplitude * np.exp(-(t / tau) ** 2) * (np.cos(
        2 * np.pi * frequency * t + phase) + oscillation_offset) + exponential_offset

def ExpDampOscFunc_v2(t, tau, frequency, amplitude, exponential_offset):
    return amplitude * np.exp(-(t / tau) ** 2) * (np.cos(
        2 * np.pi * frequency * t + np.pi)) + exponential_offset

def ExpDampOscFunc_v3(t, tau, frequency, phase, amplitude, exponent,
                   oscillation_offset, exponential_offset):
    return amplitude * np.exp(-(t / tau) ** exponent) * (np.cos(
        2 * np.pi * frequency * t + phase) + oscillation_offset) + exponential_offset

def ExpDampOscFunc_v4(t, tau, frequency, phase, amplitude,
                   oscillation_offset, exponential_offset):
    return amplitude * np.exp(-(t / tau)) * (np.cos(
        2 * np.pi * frequency * t + phase) + oscillation_offset) + exponential_offset

def Rabi_Decay(t, tau, frequency, amplitude, offset):
    return amplitude * np.exp(-(t / tau) ** 2) * np.cos(2 * np.pi * frequency * t + np.pi) + offset

def Sin(phase, a, b, phi):
    return a*np.sin((phase+phi)*np.pi/180) + b

def lin(x,a):
    return a*x

def lin2(x,a, b):
    return a*x +b

def extracted_amplitude(x, ydata,  tau, frequency, phase, amplitude,
                   oscillation_offset, exponential_offset):
    return (ydata-exponential_offset)/(amplitude * (np.cos(
        2 * np.pi * frequency * x + phase) + oscillation_offset))

def expected_amplitude(x,  tau, frequency, phase, amplitude,
                   oscillation_offset, exponential_offset):
    return np.exp(-(x / tau) ** 2)
    
def oscillation_part(x,  tau, frequency, phase, amplitude,
                   oscillation_offset, exponential_offset):
    return abs(np.cos(2 * np.pi * frequency * x + phase) + oscillation_offset)
    
def Noise_PSD(f, amplitude, exponent):
    return amplitude/f**exponent

def oneoverf(f, amplitude):
    return amplitude/(f**1.1)

def T2_fit(x, a, c):
    return a * np.array(x)**(c/(c+1))

def fit_and_plot_ext(MA, num=None):
    x = MA.sweep_points
    y = MA.sweep_points_2D
    z = MA.measured_values[0]

    xdata = 1*x[:]
    ydata = []
    idxs = []
    
    # filtering values based on if the calibration points for the pi pulse go above a certain value
    for i in range(z.shape[1]):
        if np.mean(z[len(x)-2:len(x),i])>50:
            idxs.append(i)
    number_of_meas_per_trace = 200 # 200 reps for each y value.
    ydata = np.mean(z[:,idxs],1)/number_of_meas_per_trace
    
    popt, pcov = curve_fit(ExpDampOscFunc, xdata[0:-4], ydata[0:-4], p0 = [1000e-6, 5/x[-1], np.pi/2, np.max(ydata)- np.min(ydata), np.mean(ydata), 0 ])
    test_x = np.linspace(0, np.max(xdata[0:-4]), 200)
        
    fig = plt.figure(num = num, figsize=(57.5*mm_to_inch,48*mm_to_inch),constrained_layout=True)
    plt.plot(test_x *1e3, ExpDampOscFunc(test_x , *popt), color=cm.magma(200),linewidth=1)
    plt.plot(x[0:-4]*1e3,ydata[0:-4], 'o', color=cm.magma(70),markersize=2)
    plt.xlabel('Evolution time [ms]', labelpad=2)
    plt.ylabel('Spin-up probability', labelpad=2)
    
    return fig, popt, pcov

def fit(MA):
    x = MA.sweep_points
    y = MA.sweep_points_2D
    z = MA.measured_values[0]

    xdata = 1*x[:]
    ydata = []
    idxs = []
    
    # filtering values based on if the calibration points for the pi pulse go above a certain value
    for i in range(z.shape[1]):
        if np.mean(z[len(x)-2:len(x),i])>50:
            idxs.append(i)
    number_of_meas_per_trace = 200 # 200 reps for each y value.
    ydata = np.mean(z[:,idxs],1)/number_of_meas_per_trace
    
    popt, pcov = curve_fit(ExpDampOscFunc, xdata[0:-4], ydata[0:-4], p0 = [1000e-6, 5/x[-1], np.pi/2, np.max(ydata)- np.min(ydata), np.mean(ydata), 0 ])
    return popt, pcov

def exp(x,a,b,c,d):
    return a*np.exp(-(x-c)/b)+d

def gauss(x, a, b, c,d):
    return a* np.exp( -(x-b)**2/(2*c**2)) + d

def Dephasing_time(sensitivity, PSD_freqs, PSD_values, N=0, T1 = None, t_guess = 5e-8):

    '''
    Returns the 1/e echo time given a sensitivity and a noise PSD
    sensitivity (float): Sensitivity of the qubit to the noise process
    PSD_Freqs (array): Frequencies at which the PSD values are given
    PSD_values (array): Noise PSD values
    N: Number of refocussing pulses (N=0 is Ramsey, N=1 is Echo, ...)
    T1: additional exponential decay constant (to incorporate T1 effect)
    t_guess: guess of the approximate time to improve reliability - make sure it's smaller than expected value
    '''

    if T1 != None:
        helpfunc = lambda t : (np.exp(-1/2*phase_noise(t,sensitivity, PSD_freqs, PSD_values, N))*np.exp(-t/(2*T1))-1/np.e)       

    else:
        helpfunc = lambda t : (np.exp(-1/2*phase_noise(t,sensitivity, PSD_freqs, PSD_values, N))-1/np.e)

    res = scipy.optimize.fsolve(helpfunc,t_guess)[0]
    return res

def Ramsey_filter(t, f):
    return np.sin(np.pi*f*t)**2/(np.pi*f)**2

def Martinis_Echo_filter(t, f, N):
    return np.tan(np.pi*f*t/(2*N))**2*np.sin(np.pi*f*t)**2/(np.pi*f)**2

def phase_noise(t, sensitivity, PSD_freqs, PSD_values, N):
    
    if N==0:
        filter_vals = Ramsey_filter(t,PSD_freqs)
    else:
        filter_vals = Martinis_Echo_filter(t,PSD_freqs, N)
        
    integral_val = scipy.integrate.trapz(PSD_values*filter_vals,PSD_freqs)
    return (2*np.pi*sensitivity)**2*integral_val

def Spin_analysis_1D(data_traces, cut1 = 21, cut2 = -1, threshold = 0.09, no_floor_average = 5, rel=True, up = True):
    '''
    Spin readout analyzer for a 1D data set
    
    
    '''
    Result=[]
    if rel:
    
        for n in np.arange(data_traces.shape[0]):
            time_data = data_traces[n]
            
            Prob = spin_prob_rel(time_data,cut1,cut2,threshold,no_floor_average)
            
            Result.append(Prob)
            
    else:
        Result=[]
        
        for n in np.arange(data_traces.shape[0]):
            time_data = data_traces[n]
            
            Prob = spin_prob_abs(time_data,cut1,cut2,threshold,up=up)
            
            Result.append(Prob)
            
    return Result        

def Spin_analysis_2D(data_traces, cut1 = 21, cut2 = -1, threshold = 0.09, no_floor_average = 5, rel=True, up = True):  
    '''
    Spin readout analyzer for a 2D data set
    
    
    '''    
    Result=[]
    
    for n in np.arange(data_traces.shape[0]):
        
        Line_Result = Spin_analysis_1D(data_traces[n], cut1, cut2, threshold, no_floor_average, rel=rel, up=up)
        
        Result.append(Line_Result)
        
    return Result

def spin_readout_rel(data_trace, cut1=0, cut2=-1, threshold = 0.09, no_floor_average = 5):
    '''
    Takes time traces and thresholds them, assigning 0 or 1 to corresponding single-shot, the threshold is added
    to the noise floor determined by the no_floor_average largest or smallest points of the trace
    
    Input:
        load_time_trace (NxM-array): data array with M averages of the time trace for a specific loading time.
        cut1 (int): front cutting index - only data after this index is taken into account for the analysis.
        cut2 (int): back cutting index - only data before this index is taken into account for the analysis.
        threshold (float): threshold value. Positive threshold will look for upward blips, negative threshold
            for dips
        no_floor_average (int): the x minimum/maximum values that are taken and averaged to determine the floor on
                                which the threshold is added.
    Returns:
        outcome (0 or 1): Readout of single trace
    '''
    
    analysis_data = data_trace[cut1:cut2]
    
    if threshold > 0:
        min_vals = min_x_entries(data_trace, no_floor_average)
        mean_floor = np.mean(min_vals)
        
        if max(analysis_data) >= mean_floor + threshold:
            outcome = 1
            
        else:
            outcome = 0        
        
    else:
        max_vals = max_x_entries(data_trace, no_floor_average)
        mean_floor = np.mean(max_vals)
        
        if min(analysis_data) <= mean_floor + threshold:
            outcome = 1
        else:
            outcome = 0   


    return outcome

def spin_readout_abs(data_trace, cut1=0, cut2=-1, threshold = 0.09,up=True):
    
    
    
    analysis_data = data_trace[cut1:cut2]
    
    if up:
        if max(analysis_data) >= threshold:
            outcome = 1
        else:
            outcome = 0
    else:
        if min(analysis_data) <= threshold:
            outcome = 1
        else:
            outcome = 0
    return outcome
    

def spin_prob_rel(data_traces, cut1, cut2, threshold = 0.09, no_floor_average = 5):
    '''
    This function takes a number of traces, taken at the same load time, cuts the traces 
    to the desired readout part and thresholds the trace. The threshold is determined as 
    a threshold added to the the average of the x min values of the trace. If the trace 
    crossed the threshold, a 1 is asdsigned to the trace, otherwise, a 0 is assigned.
    The average of the 0s and 1s of all the traces =for a given loading time, gives the spin
    up probability (in Si, or spin down probability in GaAs).
    
    Input:
        data_traces (NxM-array): data array with M averages of the time trace for a specific loading time.
        cut1 (int): front cutting index - only data after this index is taken into account for the analysis.
        cut2 (int): back cutting index - only data before this index is taken into account for the analysis.
        threshold (float): threshold value.
        no_floor_average (int): the x minimum values that are taken and averaged to determine the floor on
                                which the threshold is added.
    
    Returns:
        spin_prob (float): probability of spin up taken from all the data traces averaged.
    '''
    outcome_list = []
    for m, data in enumerate(data_traces):
        
        result = spin_readout_rel(data,cut1,cut2,threshold,no_floor_average)
        outcome_list.append(result)
        
    spin_prob = np.mean(outcome_list)
    return spin_prob

def spin_prob_abs(data_traces, cut1, cut2, threshold = 0.09, up = True):
    '''
    This function takes a number of traces, cuts the traces 
    to the desired readout part and thresholds the trace. The threshold is given as an absolute. if the max (min for up=False)
    of the trace is above (below for up=False) the threshold a spin up (1) is assigned otherwise a spin down (0)
    
    Input:
        data_traces (NxM-array): data array with M averages of the time trace for a specific loading time.
        cut1 (int): front cutting index - only data after this index is taken into account for the analysis.
        cut2 (int): back cutting index - only data before this index is taken into account for the analysis.
        threshold (float): threshold value.
        up (bool): if True then blip upwards are detected if False then dips downwards dips are detected
    
    Returns:
        spin_prob (float): probability of spin up taken from all the data traces averaged.
    '''
    outcome_list = []
    for m, data in enumerate(data_traces):
        
        result = spin_readout_abs(data,cut1,cut2,threshold,up=up)
        outcome_list.append(result)
        
    spin_prob = np.mean(outcome_list)
    return spin_prob

def min_x_entries(array, x):
    '''
    This function takes an array and returns the x smallest entries of the array
    Input:
        array (array) - the array that you want the min values from
        x (int) - the function returns the x min values of the array
    Return:
        min_values (list) - list with the x min values in the array
    '''
    A = np.array(array)
    min_ind = np.argpartition(A, x)
    
    min_vals = array[min_ind[:x]]
    return min_vals   

def max_x_entries(array, x):
    '''
    This function takes an array and returns the x largest entries of the array
    Input:
        array (array) - the array that you want the max values from
        x (int) - the function returns the x max values of the array
    Return:
        max_values (list) - list with the x max values in the array
    '''
    sorted_array = np.sort(array)
    
    max_vals = sorted_array[-x:len(sorted_array)]
    return max_vals  

#%% Do the plots

save = True # Bolean to save the figure panels in the figures folder
format_string = 'pdf' # specify the format of the saved figures, e.g. pdf, eps, jpg, etc.


#%% EF3 Uniformity maps
data_ef3 = pd.read_excel (os.path.join(dirname, r'data\uniformity_data.xlsx'), engine='openpyxl')

x_ef3=np.array(data_ef3.X)
y_ef3=np.array(data_ef3.Y)
S1_ef3=np.array(data_ef3.L1_VT_SPREAD)
S2_ef3=np.array(data_ef3.L2_VT_SPREAD)
M1_ef3=np.array(data_ef3.L1_VT_MEDIAN)
M2_ef3=np.array(data_ef3.L2_VT_MEDIAN)
colors = cm.get_cmap('magma', 256)


ext_fig_3a = plt.figure(num='Extended Figure 3a',figsize=(65.5*mm_to_inch,68*mm_to_inch),constrained_layout=True)
newcolors_3a = colors(np.linspace(0.2,1,8))
newcmp_3a = matplotlib.colors.ListedColormap(newcolors_3a)
plt.scatter(x_ef3, y_ef3, c=M1_ef3, s=163, marker='s', cmap=newcmp_3a,vmin=0.5,vmax=0.9)
plt.plot(x_ef3, y_ef3,'o',color=[0,0,0],markersize=2)
cb=plt.colorbar(shrink=0.75,panchor=(1,0), anchor=(0,0),aspect=15,location='right')
cb.ax.set_title(r'M$_{VT1}$ [V]',fontsize=7,loc='left')
cb.set_ticks([0.5,0.6,0.7,0.8,0.9])
cb.set_ticklabels(['$\leq 0.5$','$0.6$','$0.7$','$0.8$','$\geq 0.9$'])
plt.xlabel('Column X', labelpad=-0)
plt.ylabel('Row Y', labelpad=-0)

if save:
    ext_fig_3a.savefig(os.path.join(dirname, r'figures\Ext_Fig3_a.'+format_string), format=format_string, dpi = 600)


ext_fig_3b = plt.figure(num='Extended Figure 3b',figsize=(65.5*mm_to_inch,68*mm_to_inch),constrained_layout=True)
newcolors_3b = colors(np.linspace(0.2,1,8))
newcmp_3b = matplotlib.colors.ListedColormap(newcolors_3b)
plt.scatter(x_ef3, y_ef3, c=M2_ef3, s=163, marker='s', cmap=newcmp_3b,vmin=0.5,vmax=0.9)
plt.plot(x_ef3, y_ef3,'o',color=[0,0,0],markersize=2)
cb=plt.colorbar(shrink=0.75,panchor=(1,0), anchor=(0,0),aspect=15,location='right')
cb.ax.set_title(r'M$_{VT2}$ [V]',fontsize=7,loc='left')
cb.set_ticks([0.5,0.6,0.7,0.8,0.9])
cb.set_ticklabels(['$\leq 0.5$','$0.6$','$0.7$','$0.8$','$\geq 0.9$'])
plt.xlabel('Column X', labelpad=-0)
plt.ylabel('Row Y', labelpad=-0)

if save:
    ext_fig_3b.savefig(os.path.join(dirname, r'figures\Ext_Fig3_b.'+format_string), format=format_string, dpi = 600)


ext_fig_3c = plt.figure(num='Extended Figure 3c',figsize=(65.5*mm_to_inch,68*mm_to_inch),constrained_layout=True)

newcolors_3c = colors(np.linspace(0.2,1,6))
newcmp_3c = matplotlib.colors.ListedColormap(newcolors_3c)
plt.scatter(x_ef3, y_ef3, c=S1_ef3, s=163, marker='s', cmap=newcmp_3c,vmin=0.00,vmax=0.3)
plt.plot(x_ef3, y_ef3,'o',color=[0,0,0],markersize=2)
cb=plt.colorbar(shrink=0.75,panchor=(1,0), anchor=(0,0),aspect=15,location='right')
cb.ax.set_title(r'$\Delta$ VT1 [V]',fontsize=7,loc='left')
cb.set_ticks([0.0,0.1,0.2,0.3])
cb.set_ticklabels(['$0$','$0.1$','$0.2$','$\geq 0.3$'])

plt.xlabel('Column X', labelpad=-0)
plt.ylabel('Row Y', labelpad=-0)

if save:
    ext_fig_3c.savefig(os.path.join(dirname, r'figures\Ext_Fig3_c.'+format_string), format=format_string, dpi = 600)
    
    
ext_fig_3d = plt.figure(num='Extended Figure 3d',figsize=(65.5*mm_to_inch,68*mm_to_inch),constrained_layout=True)
newcolors_3d = colors(np.linspace(0.2,1,6))
newcmp_3d = matplotlib.colors.ListedColormap(newcolors_3d)
plt.scatter(x_ef3, y_ef3, c=S2_ef3, s=163, marker='s', cmap=newcmp_3d,vmin=0.0,vmax=0.3)
plt.plot(x_ef3, y_ef3,'o',color=[0,0,0],markersize=2)
cb=plt.colorbar(shrink=0.75,panchor=(1,0), anchor=(0,0),aspect=15,location='right')
cb.ax.set_title(r'$\Delta$ VT2 [V]',fontsize=7,loc='left')
cb.set_ticks([0,0.1,0.2,0.3])
cb.set_ticklabels(['$0$','$0.1$','$0.2$','$\geq 0.3$'])
plt.xlabel('Column X', labelpad=-0)
plt.ylabel('Row Y', labelpad=-0)

if save:
    ext_fig_3d.savefig(os.path.join(dirname, r'figures\Ext_Fig3_d.'+format_string), format=format_string, dpi = 600)
    
    
#%% EF4 Coulomb diamond

dir_ef4 = os.path.join(dirname, r'data\10-58-53_qtt_scan2D')
ds_ef4 = qcodes.load_data(dir_ef4)


x_data_ef4 = ds_ef4.B1
y_data_ef4 = 0.1*np.array(ds_ef4.S1[1,:])
z_data_ef4 = np.transpose(1e9*np.array(ds_ef4.Idc1))

ext_fig_4 = plt.figure(num = 'Extended Figure 4', figsize=(98*mm_to_inch,55*mm_to_inch),constrained_layout=True)
plot = plt.pcolormesh(x_data_ef4,y_data_ef4,z_data_ef4,shading='auto',rasterized=True)
plt.set_cmap('magma_r')

cb=plt.colorbar(shrink=0.75,panchor=(1,0), anchor=(0,0),aspect=15,location='right')
cb.ax.set_title(r'$I_{QD}$ [nA]')
plt.clim(-2, 2)
plt.ylabel('V$_{SD}$ [mV]', labelpad=-0)
plt.xlabel('G3 [mV]', labelpad=-0)

if save:
    ext_fig_4.savefig(os.path.join(dirname, r'figures\Ext_Fig4.'+format_string), format=format_string, dpi = 600)
    
#%% EF5 large stability diagram

dir_ef5 = os.path.join(dirname, r'data\pycqed\20200726')

zdata = []
xdata = []
ydata = []
zdiffx = []
zdiffy = []
for fold in os.listdir(dir_ef5):

    MA = measurement_analysis.MeasurementAnalysis(folder =  os.path.join(dir_ef5, fold), TwoD = True, show = False, auto=False)
    MA.run_default_analysis(TwoD = True,  auto=False, close_fig = True)
    zdata.append(MA.measured_values[0])
    xdata.append(MA.sweep_points)
    ydata.append(MA.sweep_points_2D)
    zdiffx.append(np.gradient(MA.measured_values[0], axis=0))
    zdiffy.append(np.gradient(MA.measured_values[0], axis=1))

ext_fig_5 = plt.figure(num = 'Extended Figure 5',figsize=(160*mm_to_inch,90*mm_to_inch),constrained_layout=True)
plt.set_cmap('magma_r')
ax_ef5=ext_fig_5.gca()
for i,te in enumerate(zdata):
    mapable = ax_ef5.pcolormesh(xdata[i], ydata[i],np.transpose(zdiffx[i]),shading='auto', vmin= -0.004, vmax = 0.004,rasterized=True)
    
ax_ef5.plot(924,980,'o',markersize=16,color=([1,1,1]))
ax_ef5.plot(941,1287,'o',markersize=16,color=([1,1,1]))
ax_ef5.text(920,969,'2',fontsize=7)
ax_ef5.text(938,1277,'1',fontsize=7)

plt.ylabel('G3 [mV]', labelpad=2)
plt.xlabel('G2 [mV]', labelpad=0)
cb=plt.colorbar(mappable = mapable, shrink=0.75,panchor=(1,0), anchor=(0,0),aspect=20,location='right')
cb.ax.set_title(r'$\frac{dI_{Sens}}{dV_{G_2}}$ [a.u.]',loc='left')

if save:
    ext_fig_5.savefig(os.path.join(dirname, r'figures\Ext_Fig5.'+format_string), format=format_string, dpi = 300)
    
    
#%% EF6 Resonance frequency shift with MW drive

MA = measurement_analysis.MeasurementAnalysis(folder = os.path.join(dirname, r'data\pycqed\20200728\160038_Rabi_with_off_resonance'), TwoD = True, show = False, auto=False)
MA.run_default_analysis(TwoD = True,  auto=False, close_fig = True)

x= MA.sweep_points
y = MA.sweep_points_2D
signal= MA.measured_values[0]

ext_fig_6a = plt.figure(num='Extended Figure 6a',figsize=(65.5*mm_to_inch,48*mm_to_inch),constrained_layout=True)
plot = plt.pcolormesh(x/1e6,y,np.transpose(signal),shading='auto',rasterized=True)
plt.xlabel('Modulation frequency [MHz]', labelpad=-0)
plt.ylabel('I/Q amplitude [V]', labelpad=-0)
plt.ylim([0,0.3])
plt.set_cmap('magma')

if save:
    ext_fig_6a.savefig(os.path.join(dirname, r'figures\Ext_Fig6a.'+format_string), format=format_string, dpi = 600)

MA = measurement_analysis.MeasurementAnalysis(folder = os.path.join(dirname, r'data\pycqed\20200730\074957_Rabi_with_off_resonance'), TwoD = True, show = False, auto=False)
MA.run_default_analysis(TwoD = True,  auto=False, close_fig = True)

x= MA.sweep_points
y = MA.sweep_points_2D
signal= MA.measured_values[0]

ext_fig_6b = plt.figure(num='Extended Figure 6b',figsize=(65.5*mm_to_inch,48*mm_to_inch),constrained_layout=True)
plot = plt.pcolormesh(x/1e6,y,np.transpose(signal),shading='auto',rasterized=True)

plt.xlabel('Modulation frequency [MHz]', labelpad=-0)
plt.ylabel('I/Q amplitude [V]', labelpad=-0)
plt.ylim([0,0.3])
plt.set_cmap('magma')

if save:
    ext_fig_6b.savefig(os.path.join(dirname, r'figures\Ext_Fig6b.'+format_string), format=format_string, dpi = 600)


#%% EF7 Relaxation and saturation behaviour of the prepulse

MA = measurement_analysis.MeasurementAnalysis(folder =os.path.join(dirname, r'data\pycqed\20200706\113549_Rabi_with_off_resonance'), TwoD = True, show = False, auto=False)
MA.run_default_analysis(TwoD = True,  auto=False, close_fig = True)

x= MA.sweep_points
y = MA.sweep_points_2D
signal= MA.measured_values[0]

freqs1 = []

for i in range(signal.shape[1]):
    z = signal[:,i]
    b = x[np.argmax(z,0)]
    d = np.min(z)
    a = np.max(z)-np.min(z)
    popt, pcov = curve_fit(gauss, x, z, p0 = [a,b,0.1e6,d])
    freqs1.append(popt[1])
    x1 = np.linspace(np.min(x), np.max(x), 1000)
freqs1 = np.array(freqs1)    
popt1, pcov1 = curve_fit(exp, y, freqs1/1e6, p0 = [1,1e-4, 1e-4,-0.4])
y_int = np.linspace(np.min(y), np.max(y), 1000)


ext_fig_7a = plt.figure(num='Extended Figure 7a',figsize=(65.5*mm_to_inch,48*mm_to_inch),constrained_layout=True)

plt.plot(y_int*1000, exp(y_int, *popt1),color=cm.magma(200),linewidth=1)  
plt.plot(y*1000, freqs1/1e6,'o',color=cm.magma(70),markersize=2)

plt.xlabel('Off-resonant burst duration [ms]')
plt.ylabel('Resonance - LO frequency [MHz]')
plt.text(0.05,0.6,'decay time = {:.1f} $\mu$s'.format(popt1[1]*1e6))
if save:
    ext_fig_7a.savefig(os.path.join(dirname, r'figures\Ext_Fig7a.'+format_string), format=format_string, dpi = 600)


MA = measurement_analysis.MeasurementAnalysis(folder = os.path.join(dirname, r'data\pycqed\20200706\111832_Rabi_with_off_resonance'), TwoD = True, show = False, auto=False)
MA.run_default_analysis(TwoD = True,  auto=False, close_fig = True)

x2= MA.sweep_points
y2 = MA.sweep_points_2D
signal2= MA.measured_values[0]

freqs2 = []

for i in range(signal2.shape[1]):
    z = signal2[:,i]
    b = x2[np.argmax(z,0)]
    d = np.min(z)
    a = np.max(z)-np.min(z)
    popt, pcov = curve_fit(gauss, x2, z, p0 = [a,b,0.1e6,d])
    freqs2.append(popt[1])
    x1 = np.linspace(np.min(x2), np.max(x2), 1000)
freqs2 = np.array(freqs2)    
popt2, pcov2 = curve_fit(exp, y2, freqs2/1e6, p0 = [-1,1e-4,8e-4,0.8])
y2_int = np.linspace(np.min(y2), np.max(y2), 1000)

ext_fig_7b = plt.figure(num='Extended Figure 7b',figsize=(65.5*mm_to_inch,48*mm_to_inch),constrained_layout=True)

plt.plot(y2_int*1000, exp(y2_int, *popt2),color=cm.magma(200),linewidth=1)  
plt.plot(y2*1000, freqs2/1e6,'o',color=cm.magma(70),markersize=2)
plt.xlabel('Time between off and on-resonant burst [ms]')
plt.ylabel('Resonance - LO frequency [MHz]')

plt.text(0.05,0,'decay time = {:.1f} $\mu$s'.format(popt2[1]*1e6))
if save:
    ext_fig_7b.savefig(os.path.join(dirname, r'figures\Ext_Fig7b.'+format_string), format=format_string, dpi = 600)

#%% EF8 Ramsey measurement analyis

MA = measurement_analysis.MeasurementAnalysis(folder = os.path.join(parent_folder, r'Figure_4\data\pycqed\20200803\084731_Ramsey_vary_offresonant_freq'), TwoD = True, show = False, auto=False)
MA.run_default_analysis(TwoD = True, show = True, auto=False, close_fig = True)
x = MA.sweep_points
y = MA.sweep_points_2D
z = MA.measured_values[0]/200 # normalized to probability; 200 singl-shots per point

length = x
fit_length = np.linspace(0,length.max(),1000)

# First we take the FFT of the Ramsey decay to see the frequency jumps over time
z1 = z[:,0]
N = x.shape[0]
T = x[1]-x[0]
xf = np.linspace(0.0, 1.0/(2.0*T), N//2)

data_fft = np.zeros([xf.shape[0], y.shape[0]])

for i in range(y.shape[0]):
    yf = scipy.fft(z[:,i])
    data_fft[:,i] = 2.0/N * np.abs(yf[0:N//2])
    
Ramsey_fft = np.transpose(data_fft[1:,:])

# plot the result:
ext_fig_8a=plt.figure(num='Extended Figure 8a',figsize=(57.5*mm_to_inch,48*mm_to_inch),constrained_layout=True)
plt.pcolormesh(xf[1:]/1000, y, Ramsey_fft)
plt.xlabel('FFT Ramsey Oscillations [kHz]')
plt.ylabel('Total repetition number')
plt.set_cmap('magma')
plt.clim([-0.01,0.15])

if save:
    ext_fig_8a.savefig(os.path.join(dirname, r'figures\Ext_Fig8a.'+format_string), format=format_string, dpi = 600)

# Extract the frequency of the Ramsey oscillation from the FFT; for starting fit parameters
freqs=[]
for i in range(len(y)):
    line_fft = Ramsey_fft[i,:]
    freqs.append(xf[np.argmax(line_fft)]) # get the frequency value of the max per line of the FFT data

# Evaluate Ramsey experiment of Q2
T2s = []
MSE = []
Res_freq = []

for i in range(len(y)): # iterate over the repetition numbers
    data_trace = z[:,i]
    try:
        popt, pcov = curve_fit(ExpDampOscFunc, length,  data_trace, p0 = [30e-6, freqs[i], 0.2, 0.1, 0., 0.5]) # Due to freq jumps we take the starting parameter from the fft
        T2s.append(abs(popt[0])) # extracted T2 from the fit
        Res_freq.append(popt[1])
        residuals = data_trace-ExpDampOscFunc(length,*popt) # calculate fitting error
        mse = np.sum([z**2 for z in residuals])/len(residuals)/(data_trace.max()-data_trace.min()) # mean square error, normalized to visibilty of ramsey
        MSE.append(mse)
    except:
        print('{} failed'.format(i)) # print lines that failed fitting
        
# Some fits give an unreasonable T2 result, due to bad data quality. select traces according to their fitting error:
MSE_selected = []
T2s_selected = []
index = []
for i in range(len(T2s)): # only take traces into account if the MSE is lower than a threshold
    if MSE[i]<0.0035:
        T2s_selected.append(T2s[i])
        MSE_selected.append(MSE[i])
        index.append(i)
        
# plotting the T2* of the traces which were selected according to their fit
times = np.arange(len(T2s_selected))
T2_ave = np.mean(T2s_selected)
T2_std = np.std(T2s_selected)

ext_fig_8b = plt.figure(num='Extended Figure 8b',figsize=(57.5*mm_to_inch,48*mm_to_inch),constrained_layout=True)
plt.plot(times+1, [1e6*T2_ave]*len(times), color=cm.magma(200), label='$T_2^*$ average is = {:.0f} $\pm$ {:.0f} $\mu$s'.format(1e6*T2_ave,1e6*T2_std))
plt.plot(times+1, [1e6*z for z in T2s_selected],'o', color=cm.magma(70))
plt.legend()
plt.xlabel('Selected repetition number')
plt.ylabel('$T_2^*$ [$\mu$s]')
plt.ylim([2,37])

if save:
    ext_fig_8b.savefig(os.path.join(dirname, r'figures\Ext_Fig8b.'+format_string), format=format_string, dpi = 600)


data_select=MA.measured_values[0][:,index]
z_selected = np.sum(data_select,1)/(200*data_select.shape[1])
popt, pcov = curve_fit(ExpDampOscFunc, length,  z_selected, p0 = [ 15e-6, 0.2e6, 0, 0.07, 0,0])
ext_fig_8c = plt.figure(num='Extended Figure 8c',figsize=(57.5*mm_to_inch,48*mm_to_inch),constrained_layout=True)
times=np.linspace(0,length.max(),200)
plt.plot(1e6*times, ExpDampOscFunc(times, *popt), color=cm.magma(200),linewidth = 1)
plt.plot(1e6*length, z_selected, 'o', color=cm.magma(70),markersize=2)
plt.xlabel('Evolution time [$\mu$s]')
plt.ylabel('Spin-up prob.')
T2 = 1e6*np.abs(popt[0])
Std = 1e6*np.sqrt(pcov[0][0])
plt.text(15,0.525,'T$_2^*$ = {:.0f} $\pm$ {:.0f} $\mu$s'.format(T2,Std))
if save:
    ext_fig_8c.savefig(os.path.join(dirname, r'figures\Ext_Fig8c.'+format_string), format=format_string, dpi = 600)


data_select=MA.measured_values[0][:,:]
z_selected = np.sum(data_select,1)/(200*data_select.shape[1])
popt, pcov = curve_fit(ExpDampOscFunc, length,  z_selected, p0 = [ 11e-6, 0.2e6, -0.2, 0.05, -0.1,0.4])
ext_fig_8d = plt.figure(num = 'Extended Figure 8d', figsize=(57.5*mm_to_inch,48*mm_to_inch),constrained_layout=True)
times=np.linspace(0,length.max(),200)
plt.plot(1e6*times, ExpDampOscFunc(times, *popt), color=cm.magma(200),linewidth = 1)
plt.plot(1e6*length, z_selected, 'o', color=cm.magma(70),markersize=2)
plt.xlabel('Evolution time [$\mu$s]')
plt.ylabel('Spin-up prob.')
T2 = 1e6*np.abs(popt[0])
Std = 1e6*np.sqrt(pcov[0][0])
plt.text(15,0.485,'T$_2^*$ = {:.0f} $\pm$ {:.0f} $\mu$s'.format(T2,Std))
if save:
    ext_fig_8d.savefig(os.path.join(dirname, r'figures\Ext_Fig8d.'+format_string), format=format_string, dpi = 600)

#%% EF9 CPMG Noise analysis

ext_fig_9a = plt.figure(num = 'Extended Figure 9a', figsize=(57.5*mm_to_inch,48*mm_to_inch),constrained_layout=True)
ax_ef9a = ext_fig_9a.gca()
ext_fig_9b = plt.figure(num = 'Extended Figure 9b',figsize=(57.5*mm_to_inch,48*mm_to_inch),constrained_layout=True)
ax_ef9b = ext_fig_9b.gca()

datasets = [
            r'Figure_4\data\pycqed\20200802\204041_CPMG1',
            r'Figure_4\data\pycqed\20200802\183140_CPMG5',
            r'Figure_4\data\pycqed\20200802\181003_CPMG10',
            r'Figure_4\data\pycqed\20200802\172753_CPMG15',
            r'Figure_4\data\pycqed\20200802\192719_CPMG30',
            r'Figure_4\data\pycqed\20200803\073854_CPMG50',
        ]

color=plt.cm.magma(np.linspace(0.2,0.9,len(datasets)))
Noise_tot = []
freq_tot = []

CPMGorder_Q2 = []
T2s_Q2 = []
T2s_Q2_ms = []

for ind, ds in enumerate(datasets): #analyse one dataset after the other

    MA = measurement_analysis.MeasurementAnalysis(folder = os.path.join(parent_folder,  ds), TwoD = True, show = False, auto=False) # load data
    MA.run_default_analysis(TwoD = True, show = True, auto=False, close_fig = True)
    
    x = MA.sweep_points
    y = MA.sweep_points_2D
    z = MA.measured_values[0]
    
    xdata = 1*x[0:-4]
    ydata = []
    idxs = []
    
    # filtering values based on if the calibration points for the pi pulse go above a certain value
    for i in range(z.shape[1]):
        if np.mean(z[len(x)-2:len(x),i])>50:
            idxs.append(i)
    number_of_meas_per_trace = 200 # 200 reps for each y value.
    ydata = np.mean(z[0:-4,idxs],1)/number_of_meas_per_trace # ydata is the cpmg decay curve
    
    popt, pcov = curve_fit(ExpDampOscFunc, xdata, ydata, p0 = [1000e-6, 5/x[-1], 0, np.max(ydata)- np.min(ydata), np.mean(ydata), 0 ]) #fitting
    
    CPMGorder_Q2.append(np.float(ds[41:]))
    T2s_Q2.append(abs(popt[0]))
    T2s_Q2_ms.append(1e3*abs(popt[0]))
    x_final=[]
    extracted=[]
    noise_line=[]
    freq_line=[]
    for l in range(len(ydata)): #analyse each point in the CPMG decay individiually
        if ((oscillation_part(xdata[l],*popt)>0.4) and (expected_amplitude(xdata[l],*popt)>0.0)): #Due to the oscillation we have to get rid of some points
            extr = extracted_amplitude(xdata[l], ydata[l], *popt)
            exp = expected_amplitude(xdata[l], *popt)
            x_final.append(xdata[l]) # xaxis of the selected datapoints
            extracted.append(extr) # extracted amplitude from the oscillating datapoints
            if ((exp>0.15) and (exp<0.85) and (extr>0) and (ds[41:] != '1')): #compute Noise PSD from CPMG amplitudes exclude CPMG 1
                noise_point = -np.log(extr)/(2*np.pi**2*xdata[l])
                noise_line.append(noise_point)
                freq_line.append(np.float(ds[41:])/(2*xdata[l]))
    
    xfit = np.linspace(0,10e-3,400) # x-axis for the fit plot to make it smooth
    ax_ef9a.loglog(freq_line,noise_line,'o',color = color[ind],zorder=10+ind) # plot Noise points in seperate figure
    #collect data for fitting the PSD:
    freq_tot = freq_tot + freq_line
    Noise_tot = Noise_tot + noise_line
    
# Fitting the Noise PSD
popt, pcov = curve_fit(Noise_PSD, freq_tot, Noise_tot, p0=[1000,1])#, sigma = [1/a for a in freq_tot])

freq_fit = np.linspace(1e3,2e4,1000)
ax_ef9a.plot(freq_fit, Noise_PSD(freq_fit, *popt),color=cm.magma(70), linewidth = 1, zorder=1)
ax_ef9a.set_xlabel('Frequency [Hz]', labelpad=2)
ax_ef9a.set_ylabel('Noise spectral density [Hz$^2$/Hz]', labelpad=2)





popt1, pcov1 = curve_fit(T2_fit, CPMGorder_Q2[1:], T2s_Q2_ms[1:], p0 = [1, 1])
test_x = np.linspace(0, np.max(CPMGorder_Q2), 200)


for ind, ds in enumerate(datasets):
    ax_ef9b.plot(CPMGorder_Q2[ind], T2s_Q2_ms[ind], 'o', color = color[ind],markersize=2,zorder=20)
ax_ef9b.set_xlabel('Number of $\pi$-pulses n', labelpad=2)
ax_ef9b.set_ylabel('T$_2^\mathrm{CPMG}$ [ms]', labelpad=2)


sqrtA_guess_eV = 29.86e-6 # charge noise in eV at 1 Hz
ac_leverarm = 0.032 # eV/AWG_V
sensitivity = 900e3/ac_leverarm # Sensitivity in Hz/eV
alpha = 1.0664

# Run the calculation

Ns = np.linspace(0, 50, 51)  # Pulse numbers to simulate
simulation_freqs = np.logspace(1,9,10001)  # Frequencies at which the integral should be evaluated
simulation_PSD = sqrtA_guess_eV**2/(simulation_freqs**alpha)  # Simulated power spectral density, just A/f
Refocussing_times = []  # Array with the simulated 1/e time for each pulse number

for N in Ns:

    Refocussing_times.append(np.abs(Dephasing_time(sensitivity=sensitivity, PSD_freqs=simulation_freqs,
                                            PSD_values=simulation_PSD,
                                            N=N, T1 = None, t_guess = 0.5e-7)))
    
Refocussing_times = np.array(Refocussing_times)

ax_ef9b.plot(Ns, Refocussing_times*1e3,'-', color = cm.magma(200))

if save:
    ext_fig_9a.savefig(os.path.join(dirname, r'figures\Ext_Fig9a.'+format_string), format=format_string, dpi = 600)
    ext_fig_9b.savefig(os.path.join(dirname, r'figures\Ext_Fig9b.'+format_string), format=format_string, dpi = 600)

#%% EF10 AllXY and RB

# Q1 allXY 

MA = measurement_analysis.MeasurementAnalysis(folder =os.path.join(parent_folder, r'Figure_4\data\pycqed\20200731\180426_AllXY_with_cal'), TwoD = True, show = False, auto=False)
MA.run_default_analysis(TwoD = True,  auto=False, close_fig = True)
x = MA.sweep_points
y = MA.sweep_points_2D
z = MA.measured_values[0]/200 #100 is is number of reps per lin
allxy_result = np.mean(z,1)
low = np.mean(allxy_result[0:5])
high = np.mean(allxy_result[-4:])
mid = (low + high)/2

ext_fig_10a = plt.figure(num = 'Extended Figure 10a',figsize=(57.5*mm_to_inch,48*mm_to_inch),constrained_layout=True)

plt.plot([0,4,5,16,17,20], [low,low,mid,mid,high,high],'-',color=cm.magma(200),linewidth=1)
plt.plot(x, allxy_result,'o',color=cm.magma(70),markersize=2)
plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
           ['$I I$','$X^2X^2$','$Y^2Y^2$','$X^2Y^2$','$Y^2X^2$','$X I$', '$Y I$',
            '$XY$', '$YX$', '$XY^2$', '$YX^2$', '$X^2Y$', '$Y^2X$', '$XX^2$',
            '$X^2X$', '$YY^2$', '$Y^2Y$', '$X^2I$', '$Y^2I$', '$XX$', '$YY$'], rotation='vertical', fontsize =6)

plt.ylabel('Spin-up prob.', labelpad=0)
plt.xlabel('AllXY sequence', labelpad=0)

if save:
    ext_fig_10a.savefig(os.path.join(dirname, r'figures\Ext_Fig10a.'+format_string), format=format_string, dpi = 600)


# Q1 RB

MA = measurement_analysis.MeasurementAnalysis(folder =os.path.join(parent_folder, r'Figure_4\data\pycqed\20200731\192822_RB_with_cal'), TwoD = True, show = False, auto=False)

MA.run_default_analysis(TwoD = True,  auto=False, close_fig = True)
data_hdf5 = MA.load_hdf5data()

data = np.array(data_hdf5['Experimental Data']['Data'])

x_values = 24
y_values  =20  # 5 seeds per y value, new randomization per y value ->100 randomizations -clifford group constructed like in Xiao Xue et al
x = np.zeros([x_values])
y = np.zeros([y_values])
z = np.zeros([x_values, y_values])
for j in range(y_values):
    for i in range(x_values):
        z[i,j] = data[x_values*j + i,2]
        x[i] = data[i,0]
        y[j]= data[x_values*j , 1]

signal_sum = np.sum(z,1)
up_cal =np.mean( signal_sum[x_values-1:x_values])
down_cal =np.mean( signal_sum[x_values-3:x_values-2])
signal_norm = (signal_sum - down_cal)/( up_cal - down_cal)

act_data = signal_norm[:22-4]
act_x = x[:22-4]
act_x = act_x[::2]
RB_down = act_data[::2]
RB_up = act_data[1::2]

def power(m, a,p):
    return a*(p**m)


popt, pcov = curve_fit(power,act_x, RB_up-RB_down, p0 = [1, 1])
test_x = np.linspace(np.min(act_x), np.max(act_x), 200)


ext_fig_10b = plt.figure(num = 'Extended Figure 10b',figsize=(57.5*mm_to_inch,48*mm_to_inch),constrained_layout=True)

plt.plot(act_x, RB_up,'o', color=cm.magma(200),markersize=2)
plt.plot(act_x, RB_down,'o', color=cm.magma(70),markersize=2)

plt.xlabel('Number of Clifford operations', labelpad=0)
plt.ylabel('Spin up probability', labelpad=0)
plt.legend(['return to up', 'return to down'])

if save:
    ext_fig_10b.savefig(os.path.join(dirname, r'figures\Ext_Fig10b.'+format_string), format=format_string, dpi = 600)

ext_fig_10c = plt.figure(num = 'Extended Figure 10c',figsize=(57.5*mm_to_inch,48*mm_to_inch),constrained_layout=True)

plt.plot(test_x, power(test_x, *popt), color=cm.magma(200),markersize=2)
plt.plot(act_x, RB_up-RB_down,'o', color=cm.magma(70),markersize=2)
plt.yscale('log')
plt.ylim([1.e-1, 0.9])
fidelity = 100*(1-(1-popt[1])/2/1.875)
uncertainty = 100*np.sqrt(pcov[0][0])/2/1.875
plt.text(10,0.7,'Gate fidelity = {:.1f} $\pm$ {:.1f} %'.format(fidelity,uncertainty))
plt.xlabel('Number of Clifford operations', labelpad=0)
plt.ylabel('Pup - Pdown', labelpad=0)
plt.yticks([0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8],[0.1,0.2,'',0.4,'',0.6,'',0.8])

if save:
    ext_fig_10c.savefig(os.path.join(dirname, r'figures\Ext_Fig10c.'+format_string), format=format_string, dpi = 600)
    
# Q2 AllXY

MA = measurement_analysis.MeasurementAnalysis(folder =os.path.join(parent_folder, r'Figure_4\data\pycqed\20200703\092107_AllXY_with_cal'), TwoD = True, show = False, auto=False)

MA.run_default_analysis(TwoD = True,  auto=False, close_fig = True)
x = MA.sweep_points
y = MA.sweep_points_2D
z = MA.measured_values[0]/100 #100 is is number of reps per lin
allxy_result = np.mean(z,1)
low = np.mean(allxy_result[0:5])
high = np.mean(allxy_result[-4:])
mid = (low + high)/2

ext_fig_10d = plt.figure(num='Extended Figure 10d', figsize=(57.5*mm_to_inch,48*mm_to_inch),constrained_layout=True)

plt.plot([0,4,5,16,17,20], [low,low,mid,mid,high,high],'-',color=cm.magma(200),linewidth=1)
plt.plot(x, allxy_result,'o',color=cm.magma(70),markersize=2)
plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
           ['$I I$','$X^2X^2$','$Y^2Y^2$','$X^2Y^2$','$Y^2X^2$','$X I$', '$Y I$',
            '$XY$', '$YX$', '$XY^2$', '$YX^2$', '$X^2Y$', '$Y^2X$', '$XX^2$',
            '$X^2X$', '$YY^2$', '$Y^2Y$', '$X^2I$', '$Y^2I$', '$XX$', '$YY$'], rotation='vertical', fontsize =6)

plt.ylabel('Spin-up prob.', labelpad=0)
plt.xlabel('AllXY sequence', labelpad=0)

if save:
    ext_fig_10d.savefig(os.path.join(dirname, r'figures\Ext_Fig10d.'+format_string), format=format_string, dpi = 600)



# Q2 RB
#  900ns Pi time, 10us off-resonant prepulse due to freqeuncy shift, 
MA = measurement_analysis.MeasurementAnalysis(folder =os.path.join(parent_folder, r'Figure_4\data\pycqed\20200703\173846_RB_with_cal'), TwoD = True, show = False, auto=False)

MA.run_default_analysis(TwoD = True,  auto=False, close_fig = True)
data_hdf5 = MA.load_hdf5data()

data = np.array(data_hdf5['Experimental Data']['Data'])

x_values = 22
y_values  =20 


x = np.zeros([x_values])
y = np.zeros([y_values])
z = np.zeros([x_values, y_values])
for j in range(y_values):
    for i in range(x_values):
        z[i,j] = data[x_values*j + i,2]
        x[i] = data[i,0]
        y[j]= data[x_values*j , 1]

signal_sum = np.sum(z,1)

up_cal =np.mean( signal_sum[x_values-1:x_values])
down_cal =np.mean( signal_sum[x_values-3:x_values-2])
signal_norm = (signal_sum - down_cal)/( up_cal - down_cal)

act_data = signal_norm[:22-4]
act_x = x[:22-4]
act_x = act_x[::2]
RB_down = act_data[::2]
RB_up = act_data[1::2]

def power(m, a,p):
    return a*(p**m)


popt, pcov = curve_fit(power,act_x, RB_up-RB_down, p0 = [1, 1])
test_x = np.linspace(np.min(act_x), np.max(act_x), 200)


ext_fig_10e = plt.figure(num='Extended Figure 10e', figsize=(57.5*mm_to_inch,48*mm_to_inch),constrained_layout=True)

plt.plot(act_x, RB_up,'o', color=cm.magma(200),markersize=2)
plt.plot(act_x, RB_down,'o', color=cm.magma(70),markersize=2)

plt.xlabel('Number of Clifford operations', labelpad=0)
plt.ylabel('Spin up probability', labelpad=0)
plt.legend(['return to up', 'return to down'])

if save:
    ext_fig_10e.savefig(os.path.join(dirname, r'figures\Ext_Fig10e.'+format_string), format=format_string, dpi = 600)


ext_fig_10f = plt.figure(num='Extended Figure 10f', figsize=(57.5*mm_to_inch,48*mm_to_inch),constrained_layout=True)

plt.plot(act_x, power(act_x, *popt), color=cm.magma(200),linewidth=1)
plt.plot(act_x, RB_up-RB_down,'o', color=cm.magma(70),markersize=2)
plt.yscale('log')
plt.ylim([1.5e-1, 0.9])
plt.xlabel('Number of Clifford operations', labelpad=0)
plt.ylabel('Pup - Pdown', labelpad=0)

fidelity = 100*(1-(1-popt[1])/2/1.875)
uncertainty = 100*np.sqrt(pcov[0][0])/2/1.875
plt.text(10,0.7,'Gate fidelity = {:.1f} $\pm$ {:.1f} %'.format(fidelity,uncertainty))
plt.yticks([0.2,0.3,0.4,0.5,0.6,0.7,0.8],[0.2,'',0.4,'',0.6,'',0.8])

if save:
    ext_fig_10f.savefig(os.path.join(dirname, r'figures\Ext_Fig10f.'+format_string), format=format_string, dpi = 600)

#%% EF11 Q2 Rabi
powers = []
rabi_freqs = []

# power = 1dB
number_of_reps =400 #unfortunately not stored in metadata for these types of plots
MA = measurement_analysis.MeasurementAnalysis(folder =os.path.join(parent_folder, r'Figure_4\data\pycqed\20200701\151717_Rabi_vary_dur_n1_Q1'), TwoD = False, show = False, auto=False)
MA.run_default_analysis(TwoD = False,  auto=False, close_fig = True)
# last 4 points are calibration points 0pi and pi
length= MA.sweep_points[:-4]
signal= MA.measured_values[0][:-4]/number_of_reps

popt, pcov = curve_fit(Rabi_Decay, length,  signal, p0 = [ 50e-6, .2e6, 0.3, 0.2])

ext_fig_11a = plt.figure(num='Extended Figure 11a', figsize=(57.5*mm_to_inch,48*mm_to_inch),constrained_layout=True)

test_x = np.linspace(0, np.max(length), 200)
plt.plot(test_x *1e6, Rabi_Decay(test_x , *popt),color=cm.magma(200),linewidth=1)
plt.plot(length*1e6, signal, 'o',color=cm.magma(70),markersize=2)

plt.ylabel('Spin-up prob.', labelpad=0)
plt.xlabel('Microwave burst duration [$\mu$s]', labelpad=0)
plt.text(11.5, 0.32, 'P = 1 dBm', fontsize=7,fontstyle='italic')

if save:
    ext_fig_11a.savefig(os.path.join(dirname, r'figures\Ext_Fig11a.'+format_string), format=format_string, dpi = 600)

data_hdf5 = MA.load_hdf5data()
power = (data_hdf5['Snapshot']['instruments']['MW1']['parameters']['power'].attrs['raw_value'])
rabi_freq = int(popt[1]/1e3)/1e3
powers.append(power)
rabi_freqs.append(rabi_freq)

# power = 7dBm
MA = measurement_analysis.MeasurementAnalysis(folder =os.path.join(parent_folder, r'Figure_4\data\pycqed\20200702\175338_Rabi_over_time'), TwoD = True, show = False, auto=False)
MA.run_default_analysis(TwoD = True,  auto=False, close_fig = True)

length= MA.sweep_points[1:-5]
y = MA.sweep_points_2D
signal= MA.measured_values[0][:,0:5]

ydata = np.sum(signal[1:-5,:],1)/(100*len(y))
popt, pcov = curve_fit(ExpDampOscFunc, length,  ydata, p0 = [10e-6, .31e6, np.pi/2, 0.13, 0.1 ,0.1 ])
test_x = np.linspace(0, np.max(length), 200)

ext_fig_11b = plt.figure(num='Extended Figure 11b',figsize=(57.5*mm_to_inch,48*mm_to_inch),constrained_layout=True)

test_x = np.linspace(0, np.max(length), 200)
plt.plot(test_x *1e6, ExpDampOscFunc(test_x , *popt),color=cm.magma(200),linewidth=1)
plt.plot(length*1e6, ydata, 'o',color=cm.magma(70),markersize=2)

plt.ylabel('Spin-up prob.', labelpad=0)
plt.xlabel('Microwave burst duration [$\mu$s]', labelpad=0)
plt.text(11.5, 0.05, 'P = 7 dBm', fontsize=7,fontstyle='italic')

if save:
    ext_fig_11b.savefig(os.path.join(dirname, r'figures\Ext_Fig11b.'+format_string), format=format_string, dpi = 600)

data_hdf5 = MA.load_hdf5data()
power = (data_hdf5['Snapshot']['instruments']['MW1']['parameters']['power'].attrs['raw_value'])
rabi_freq = int(popt[1]/1e3)/1e3
powers.append(power)
rabi_freqs.append(rabi_freq)

# power = 13dBm


MA = measurement_analysis.MeasurementAnalysis(folder =os.path.join(parent_folder, r'Figure_4\data\pycqed\20200703\080715_Rabi_over_time'), TwoD = True, show = False, auto=False)
MA.run_default_analysis(TwoD = True,  auto=False, close_fig = True)

length= MA.sweep_points[:-4]
y = MA.sweep_points_2D
signal= MA.measured_values[0]
ydata = np.sum(signal[:-4,:],1)/(100*len(y))
popt, pcov = curve_fit(Rabi_Decay, length,  ydata, p0 = [ 20e-6, .5e6, 0.25, 0.4])
test_x = np.linspace(0, np.max(length), 100)

ext_fig_11c = plt.figure(num='Extended Figure 11c',figsize=(57.5*mm_to_inch,48*mm_to_inch),constrained_layout=True)

test_x = np.linspace(0, np.max(length), 200)
plt.plot(test_x *1e6, Rabi_Decay(test_x , *popt),color=cm.magma(200),linewidth=1)
plt.plot(length*1e6, ydata, 'o',color=cm.magma(70),markersize=2)

plt.ylabel('Spin-up prob.', labelpad=0)
plt.xlabel('Microwave burst duration [$\mu$s]', labelpad=0)
plt.text(6, 0.14, 'P = 13 dBm', fontsize=7,fontstyle='italic')

if save:
    ext_fig_11c.savefig(os.path.join(dirname, r'figures\Ext_Fig11c.'+format_string), format=format_string, dpi = 600)


data_hdf5 = MA.load_hdf5data()
power = (data_hdf5['Snapshot']['instruments']['MW1']['parameters']['power'].attrs['raw_value'])
rabi_freq = int(popt[1]/1e3)/1e3
powers.append(power)
rabi_freqs.append(rabi_freq)

# power = 18dBm 
number_of_reps =400 #unfortunately not stored in metadata for these types of plots

MA = measurement_analysis.MeasurementAnalysis(folder =os.path.join(parent_folder, r'Figure_4\data\pycqed\20200705\133037_Rabi_vary_dur_n1_Q1'), TwoD = False, show = False, auto=False)
#%
MA.run_default_analysis(TwoD = False,  auto=False, close_fig = True)
# last 4 points are calibration points 0pi and pi
length= MA.sweep_points[:-4]
signal= MA.measured_values[0][:-4]/number_of_reps

popt, pcov = curve_fit(Rabi_Decay, length,  signal, p0 = [ 20e-6, 0.9e6, 0.25, 0.4])
test_x = np.linspace(0, np.max(length), 200)

ext_fig_11d = plt.figure(num='Extended Figure 11d',figsize=(57.5*mm_to_inch,48*mm_to_inch),constrained_layout=True)

test_x = np.linspace(0, np.max(length), 200)
plt.plot(test_x *1e6, Rabi_Decay(test_x , *popt),color=cm.magma(200),linewidth=1)
plt.plot(length*1e6, signal, 'o',color=cm.magma(70),markersize=2)

plt.ylabel('Spin-up prob.', labelpad=0)
plt.xlabel('Microwave burst duration [$\mu$s]', labelpad=0)
plt.text(5, 0.1, 'P = 18 dBm', fontsize=7,fontstyle='italic')

if save:
    ext_fig_11d.savefig(os.path.join(dirname, r'figures\Ext_Fig11d.'+format_string), format=format_string, dpi = 600)

data_hdf5 = MA.load_hdf5data()
power = (data_hdf5['Snapshot']['instruments']['MW1']['parameters']['power'].attrs['raw_value'])
rabi_freq = int(popt[1]/1e3)/1e3
powers.append(power)
rabi_freqs.append(rabi_freq)

powers = np.array(powers)
rabi_freqs = np.array(rabi_freqs)

# Rabi freq vs. power

power__watts = 10**(np.array(powers)/10)/1000

h = 4.135e-15
ub = 5.788e-5

B1 = h*rabi_freqs*1e6/(4*5.788e-5)
xdata = power__watts**.5
ydata = rabi_freqs
popt, pcov = curve_fit(lin2, xdata,  ydata)#, p0 = [ 50e-6, .6e6, np.pi/2, 0.5, 0.2,0 ])
test_x = np.linspace(0, np.max(xdata), 100)


ext_fig_11e = plt.figure(num = 'Extended Figure 11e', figsize=(57.5*mm_to_inch,48*mm_to_inch),constrained_layout=True)

plt.plot(xdata, lin2(xdata , *popt),color=cm.magma(200),linewidth=1)
plt.plot(power__watts**.5, rabi_freqs, 'o',color=cm.magma(70),markersize=2)
plt.xlabel('Power [W$^{1/2}$]', labelpad=0)
plt.ylabel('Rabi frequency [MHz]', labelpad=0)

if save:
    ext_fig_11e.savefig(os.path.join(dirname, r'figures\Ext_Fig11e.'+format_string), format=format_string, dpi = 600)

#%% EF12 Q2 CPMG


MA = measurement_analysis.MeasurementAnalysis(folder =os.path.join(parent_folder, r'Figure_4\data\pycqed\20200627\144624_CPMG20'), TwoD = True, show = False, auto=False)
MA.run_default_analysis(TwoD = True, show = True, auto=False, close_fig = True)

ext_fig_12a, popt, pcov = fit_and_plot_ext(MA, 'Extended Figure 12a')

if save:
    ext_fig_12a.savefig(os.path.join(dirname, r'figures\Ext_Fig12a.'+format_string), format=format_string, dpi = 600)



ext_fig_12b = plt.figure(num ='Extended Figure 12b', figsize=(57.5*mm_to_inch,48*mm_to_inch),constrained_layout=True)
ax_ef12b = ext_fig_12b.gca()
ext_fig_12c = plt.figure(num ='Extended Figure 12c', figsize=(57.5*mm_to_inch,48*mm_to_inch),constrained_layout=True)
ax_ef12c = ext_fig_12c.gca()

datasets = [
            r'Figure_4\data\pycqed\20200624\120755_Hahn',
            r'Figure_4\data\pycqed\20200629\180912_CPMG3',
            r'Figure_4\data\pycqed\20200629\173131_CPMG5',
            r'Figure_4\data\pycqed\20200629\140724_CPMG10',
            r'Figure_4\data\pycqed\20200629\201245_CPMG15',
            r'Figure_4\data\pycqed\20200627\144624_CPMG20',
        ]

number = np.ones(len(datasets))

for ind, ds in enumerate(datasets[1:]):
    number[ind+1] = ds[41:]

color=plt.cm.magma(np.linspace(0.2,0.9,len(datasets)))
Noise_tot = []
freq_tot = []

CPMGorder_Q2 = []
T2s_Q2 = []
T2s_Q2_ms = []

for ind, ds in enumerate(datasets):

    MA = measurement_analysis.MeasurementAnalysis(folder = os.path.join(parent_folder,  ds), TwoD = True, show = False, auto=False)
    MA.run_default_analysis(TwoD = True, show = True, auto=False, close_fig = True)
    
    x = MA.sweep_points
    y = MA.sweep_points_2D
    z = MA.measured_values[0]
    
    xdata = 1*x[0:-4]
    ydata = []
    idxs = []
    
    # filtering values based on if the calibration points for the pi pulse go above a certain value
    for i in range(z.shape[1]):
        if np.mean(z[len(x)-2:len(x),i])>50:
            idxs.append(i)
    number_of_meas_per_trace = 200 # 200 reps for each y value.
    ydata = np.mean(z[0:-4,idxs],1)/number_of_meas_per_trace
    
    popt, pcov = curve_fit(ExpDampOscFunc, xdata, ydata, p0 = [1000e-6, 5/x[-1], np.pi/2, np.max(ydata)- np.min(ydata), np.mean(ydata), 0 ])
    CPMGorder_Q2.append(np.float(number[ind]))
    T2s_Q2.append(abs(popt[0]))
    T2s_Q2_ms.append(1e3*abs(popt[0]))
    x_final=[]
    extracted=[]
    for l in range(len(ydata)):
        if ((oscillation_part(xdata[l],*popt)>0.5) and (expected_amplitude(xdata[l],*popt)>0.0)):
            extr = extracted_amplitude(xdata[l], ydata[l], *popt)
            exp = expected_amplitude(xdata[l], *popt)
            x_final.append(xdata[l])
            extracted.append(extr)
    xfit = np.linspace(0,3e-3,400)
    ax_ef12b.plot([1e3*x for x in x_final],extracted,'o',color = color[ind],label = 'n: %s'%(int(number[ind])),zorder=30-ind,markersize=2)
    ax_ef12b.plot(1e3*xfit,expected_amplitude(xfit,*popt), color = color[ind], linewidth = 1,zorder=10-ind)
ax_ef12b.set_xlim([3e-3,4])
ax_ef12b.set_ylim([-0.2,1.35])
ax_ef12b.set_xscale('log')
ax_ef12b.minorticks_off()
ax_ef12b.set_xticks([0.1,1])
ax_ef12b.set_xticklabels([0.1,1])
ax_ef12b.set_xlabel('Evolution time [ms]', labelpad=2)
ax_ef12b.set_ylabel('CPMG amplitude [norm.]', labelpad=2)
ax_ef12b.legend(fontsize=7, labelspacing=0.0,handlelength=0.75,handletextpad=0.3)

popt1, pcov1 = curve_fit(T2_fit, CPMGorder_Q2[2:], T2s_Q2_ms[2:], p0 = [1, 1])
test_x = np.linspace(0, np.max(CPMGorder_Q2), 200)

ax_ef12c.plot(test_x, T2_fit(test_x, *popt1),color=cm.magma(200),linewidth=1)

for ind, ds in enumerate(datasets):
    ax_ef12c.plot(CPMGorder_Q2[ind], T2s_Q2_ms[ind], 'o', color = color[ind],markersize=2)

ax_ef12c.set_xlabel('Number of $\pi$-pulses n', labelpad=2)
ax_ef12c.set_ylabel('T$_2^\mathrm{CPMG}$ [ms]')
ax_ef12c.set_ylim([-0.1, 1.3])
ax_ef12c.set_xlim([-1,21])

if save:
    ext_fig_12b.savefig(os.path.join(dirname, r'figures\Ext_Fig12b.'+format_string), format=format_string, dpi = 600)
    ext_fig_12c.savefig(os.path.join(dirname, r'figures\Ext_Fig12c.'+format_string), format=format_string, dpi = 600)

#%% EF13 Q3 Results

dir_ef13a = os.path.join(dirname, r'data\18-56-13_qtt_pulse_train_1D')
ds_ef13a = qcodes.load_data(dir_ef13a)

ext_fig_13a = plt.figure(num='Extended Figure 13a',figsize=(57.5*mm_to_inch,48*mm_to_inch),constrained_layout=True)

length = np.array(ds_ef13a.Time_train)
signal = np.array(Spin_analysis_1D(ds_ef13a.digitizer_dig_1,threshold = 0.3))

popt, pcov = curve_fit(Rabi_Decay, length,  signal, p0 = [ 3e-6, 1.4e6, 0.15, 0.5 ])
test_x = np.linspace(0, np.max(length), 200)

plt.plot(test_x *1e6, Rabi_Decay(test_x , *popt),color=cm.magma(200),linewidth=1)
plt.plot(length*1e6, signal, 'o',color=cm.magma(70),markersize=2)

plt.ylabel('Spin-up probability', labelpad=2)
plt.xlabel('Microwave burst duration [$\mu$s]    ', labelpad=2)

if save:
    ext_fig_13a.savefig(os.path.join(dirname, r'figures\Ext_Fig13a.'+format_string), format=format_string, dpi = 600)
    

dir_ef13b = os.path.join(dirname, r'data\12-26-35_sweep2D_manip_mw_bp0_onvsfrequency')
ds_ef13b = qcodes.load_data(dir_ef13b)

x_data_2 = np.array(ds_ef13b.manip_mw_bp0_on_set[1])*1e6
y_data_2 = np.array(ds_ef13b.vector_source_frequency_set)/1e9
z_data_2 = Spin_analysis_2D(ds_ef13b.digitizer_dig_1,threshold = 0.2)

ext_fig_13b = plt.figure(num='Extended Figure 13b', figsize=(65.5*mm_to_inch,48*mm_to_inch),constrained_layout=True)
ax_ef13b = plt.gca()
plot = plt.pcolormesh(x_data_2,y_data_2,z_data_2)
plt.xticks([0, 2,4,6])

plt.ylabel('Microwave Frequency [GHz]', labelpad=-0)
plt.xlabel('Microwave burst duration [$\mu$s]', labelpad=-0)

plt.set_cmap('magma')
plt.clim(0.1, 0.8)
cbaxes = ext_fig_13b.add_axes([0.615, 0.86, 0.35, 0.05])
cb = plt.colorbar(cax=cbaxes, orientation='horizontal')
cb.set_ticks([0.1,0.3,0.5,0.7])
cbaxes.set_title('Spin up prob.',pad = -2,fontsize=7)

rect = matplotlib.patches.Rectangle((3.35,18.59),100,100,color=(1,1,1))
ax_ef13b.add_patch(rect)

if save:
    ext_fig_13b.savefig(os.path.join(dirname, r'figures\Ext_Fig13b.'+format_string), format=format_string, dpi = 600)
    
