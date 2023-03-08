# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 13:20:02 2017

@author: TronitoTeam
"""
from __future__ import print_function
import qcodes as qc
import time
import numpy as np
#from scipy import optimize
import os
import zhinst.utils





class DetuningG4(qc.Parameter):
    def __init__(self, gate1, gate2,slope):
        super().__init__(name='Detuning', label='$\epsilon$', vals=qc.validators.Numbers(-2500, 2500), unit='mV')
        self._gate1 = gate1
        self._gate2 = gate2
        self._slope = slope
        
    def get_raw(self):

     return self._gate1(),self._gate2()
        
    def set_raw(self, val):
        #first record old values and change relative values
        init1=self._gate1()
        init2=self._gate2()
        dx=val-init1
        dy=dx*self._slope
        self._gate1(val)
        time.sleep(0.01)
        self._gate2(init2+dy)

class Compensate(qc.Parameter):
    def __init__(self, gate1, gate2,slope , name = 'compV'):
        self.name = name
        super().__init__(name=name, label=name, vals=qc.validators.Numbers(-2500, 2500), unit='mV')
        self._gate1 = gate1
        self._gate2 = gate2
        self._slope = slope
        
    def get_raw(self):

     return self._gate1(),self._gate2()
        
    def set_raw(self, val):
        #first record old values and change relative values
        init1=self._gate1()
        init2=self._gate2()
        dx=val-init1
        dy=dx*self._slope
        self._gate1(val)
        self._gate2(init2+dy)


class CompensateB2(qc.Parameter):
    def __init__(self, gate1, gate2,slope):
        super().__init__(name='CompensatedB2', label='CompensatedB2', vals=qc.validators.Numbers(-2500, 2500), unit='mV')
        self._gate1 = gate1
        self._gate2 = gate2
        self._slope = slope
        
    def get_raw(self):

     return self._gate1(),self._gate2()
        
    def set_raw(self, val):
        #first record old values and change relative values
        init1=self._gate1()
        init2=self._gate2()
        dx=val-init1
        dy=dx*self._slope
        self._gate1(val)
        self._gate2(init2+dy)
        
class CompensateB1(qc.Parameter):
    def __init__(self, gate1, gate2,slope):
        super().__init__(name='CompensatedB1', label='CompensatedB1', vals=qc.validators.Numbers(-2500, 2500), unit='mV')
        self._gate1 = gate1
        self._gate2 = gate2
        self._slope = slope
        
    def get_raw(self):

     return self._gate1(),self._gate2()
        
    def set_raw(self, val):
        #first record old values and change relative values
        init1=self._gate1()
        init2=self._gate2()
        dx=val-init1
        dy=dx*self._slope
        self._gate1(val)
        self._gate2(init2+dy)
        
    
class Calibrated_Fmw(qc.Parameter):
    
    '''  - frequency is the asked frequency
         - power will be adapted based on the calibration function
         - Calib is a 1d interp function of the calibration curve (dB vs Frequency)
         - F is a vector of frequencies used to interpolate the calibration curve, start and stop values must match the calibration curve ones'''
   
    def __init__(self, frequency, power, Calib, F,P0 ):
        super().__init__(name='Calibreatd_Fmw', label='Calibreatd_Fmw', unit='Hz')
        self._frequency = frequency
        self._power = power
        self._Calib = Calib
        self._F = F
        self._P0 = P0
        
    def get_raw(self):

     return self._frequency(),self._power()
        
    def set_raw(self, val):
        #first record old values and change relative values
        initF=self._frequency()
        initP=self._power()
        p = np.abs(self._F - initF).argmin() 
        Power = float(self._Calib(self._F[p]))
        self._frequency(val)
        self._power(Power+self._P0)
                
        
class CompensateT1(qc.Parameter):
    def __init__(self, gate1, gate2,slope):
        super().__init__(name='CompensatedT1', label='CompensatedT1', vals=qc.validators.Numbers(-2000, 2000), unit='mV')
        self._gate1 = gate1
        self._gate2 = gate2
        self._slope = slope
        
    def get_raw(self):

     return self._gate1(),self._gate2()
        
    def set_raw(self, val):
        #first record old values and change relative values
        init1=self._gate1()
        init2=self._gate2()
        dx=val-init1
        dy=dx*self._slope
        self._gate1(val)
        self._gate2(init2+dy)        
        
class Reflecto_frequency(qc.Parameter):
    def __init__(self, name, UHF, outsignal):
        super().__init__(name, label='frequency', vals=qc.validators.Numbers(), unit='Hz', docstring='UHF_oscillator1_frequency')
        self._daq = UHF.daq
        self._outsignal=outsignal
        
class CompensateT2(qc.Parameter):
    def __init__(self, gate1, gate2,slope):
        super().__init__(name='CompensatedT2', label='CompensatedT2', vals=qc.validators.Numbers(-2000, 2000), unit='mV')
        self._gate1 = gate1
        self._gate2 = gate2
        self._slope = slope
        
    def get_raw(self):

     return self._gate1(),self._gate2()
        
    def set_raw(self, val):
        #first record old values and change relative values
        init1=self._gate1()
        init2=self._gate2()
        dx=val-init1
        dy=dx*self._slope
        self._gate1(val)
        self._gate2(init2+dy)
    
class AllGates(qc.Parameter):
    def __init__(self, gate1, gate2,gate3,gate4):
        super().__init__(name='AllGates', label='AllGates', vals=qc.validators.Numbers(-2000, 2000), unit='mV')
        self._gate1 = gate1
        self._gate2 = gate2
        self._gate3 = gate3
        self._gate4 = gate4
        
    def get_raw(self):

     return self._gate1(),self._gate2(),self._gate3(),self._gate4()
        
    def set_raw(self, val):
        #first record old values and change relative values
        self._gate1(val)
        self._gate2(val)
        self._gate3(val)          
        self._gate4(val)  
    
class Reflecto_frequency(qc.Parameter):
    def __init__(self, name, UHF, outsignal):
        super().__init__(name, label='frequency', vals=qc.validators.Numbers(), unit='Hz', docstring='UHF_oscillator1_frequency')
        self._daq = UHF.daq
        self._outsignal=outsignal       
    def get_raw(self):
        f =  self._daq.getDouble('/dev2226/oscs/'+str(self._outsignal)+'/freq')#in Hz
#        power= d*d/50 #W
#        power=power*1000#mW
#        powerdBm=10*np.log10(power)
        return f
    
    def set_raw(self,val):
#        valV=50*np.sqrt((10**((val-14)/10))/1000) #conversion dBm to V
        cmd= '/dev2226/oscs/' +str(self._outsignal)+'/freq'
        self._daq.setDouble(cmd, val)#in Hz

class Reflecto_power(qc.Parameter):
    def __init__(self, name, UHF, outsignal, outchannel):
        super().__init__(name, label='power', vals=qc.validators.Numbers(), unit='dBm', docstring='UHF output power')
        self._daq = UHF.daq
        self._outsignal=outsignal
        self._outchannel=outchannel
        
    def get_raw(self):
        d =  self._daq.getDouble('/dev2226/sigouts/'+str(self._outsignal)+'/amplitudes/'+str(self._outchannel))#in Vpk
        power= d*d/50 #W
        power=power*1000#mW
        powerdBm=10*np.log10(power)
        return powerdBm
    
    def set_raw(self,val):
        valV=50*np.sqrt((10**((val-14)/10))/1000) #conversion dBm to V
        cmd= '/dev2226/sigouts/' +str(self._outsignal)+'/amplitudes/'+str(self._outchannel)
        self._daq.setDouble(cmd, valV)#in Vpk
        
class Reflecto_powerB3(qc.Parameter):
    def __init__(self, name, UHF, outsignal, outchannel):
        super().__init__(name, label='power', vals=qc.validators.Numbers(), unit='dBm', docstring='UHF output power')
        self._daq = UHF.daq
        self._outsignal=outsignal
        self._outchannel=outchannel
        
    def get_raw(self):
        d =  self._daq.getDouble('/dev2226/sigouts/'+str(self._outsignal)+'/amplitudes/'+str(self._outchannel))#in Vpk
        power= d*d/50 #W
        power=power*1000#mW
        powerdBm=10*np.log10(power)
        return powerdBm
    
    def set_raw(self,val):
        valV=50*np.sqrt((10**((val-14)/10))/1000) #conversion dBm to V
        cmd= '/dev2226/sigouts/' +str(self._outsignal)+'/amplitudes/'+str(self._outchannel)
        self._daq.setDouble(cmd, valV)#in Vpk


class ParameterPhase0_T2(qc.Parameter):
    def __init__(self, UHF, param, phase, name='phase0Param'):
        super().__init__(name=param.name + 'Phase0', label=param.label + ' Phase0', vals=qc.validators.Numbers(), unit=param.unit)

        self._daq = UHF.daq
        self._param = param
        self._phase = phase

    # you must provide a get method, a set method, or both
    def get_raw(self):
        return self._param.get()
        
    
    def set_raw(self, val):
        for i in range(0,2):
            self._param.set(val)
            tc = self._daq.getDouble('/dev2226/demods/1/timeconstant')
    #        time.sleep(1)
    #        self._daq.setDouble('/dev2365/demods/1/phaseshift', 0)
            time.sleep(5*tc)
            meanphase = 0
            numAverages = 10
            for i in range(numAverages):
                meanphase += np.rad2deg(self._phase.get())/numAverages
            self._daq.setDouble('/dev2226/demods/1/phaseshift', self._daq.getDouble('/dev2226/demods/1/phaseshift') + meanphase)
            time.sleep(5*tc)
            
            
class ParameterPhase0_B3(qc.Parameter):
    def __init__(self, UHF, param, phaseB3, name='phase0Param'):
        super().__init__(name=param.name + 'Phase0', label=param.label + ' Phase0', vals=qc.validators.Numbers(), unit=param.unit)

        self._daq = UHF.daq
        self._param = param
        self._phaseB3 = phaseB3
    # you must provide a get method, a set method, or both
    def get_raw(self):
        return self._param.get()
    def set_raw(self,val):
        meanphase = 0
        numAverages = 10
        self._param.set(val)
        tc = self._daq.getDouble('/dev2226/demods/5/timeconstant')
        time.sleep(5*tc)
        
        for i in range(numAverages):
            meanphase += np.rad2deg(self._phaseB3.get())
        meanphase=meanphase/numAverages
        print(meanphase)
        self._daq.setDouble('/dev2226/demods/5/phaseshift', self._daq.getDouble('/dev2226/demods/5/phaseshift') - meanphase)
        time.sleep(5*tc)   
            
#        daq.setInt('/dev2226/demods/5/phaseadjust', 1)
        
class ParameterPhase0(qc.Parameter):     
    def __init__(self, UHF, param, demod, name='phase0Param'):
        super().__init__(name=param.name + 'Phase0', label=param.label + ' Phase0', vals=qc.validators.Numbers(), unit=param.unit)

        self._daq = UHF.daq
        self._param = param
        self._demod = demod
        
        # you must provide a get method, a set method, or both
    def get_raw(self):
        return self._param.get()
    def set_raw(self,val):
        self._param.set(val) 
        time.sleep(0.5)   
        command='/dev2226/demods/' + str(self._demod) + '/phaseadjust'
        self._daq.setInt(command, 1)
        time.sleep(0.5)   
        
        
        
class ZField(qc.Parameter):
    def __init__(self, magnet):
        # only name is required
        super().__init__(name='zField',
                             label='Field along z axis',
#                         vals=qc.validators.Numbers(-6, 6),
                         docstring='Field along z axis')
        self._magnet = magnet

    # you must provide a get method, a set method, or both
    def get_raw(self):
#        return self._magnet.z_setpoint.get()
        return self._magnet.z_fld.get()

    def set_raw(self, val):
        # StandardParameter handles validation automatically, Parameter doesn't
#        self._vals.validate(val)
#        self._magnet.z_setpointC.set(val)
        self._magnet.z_setpoint.set(val)
        self._magnet.z_setpoint.set(val)
        #heater on
        self._magnet.ask_raw('SET:DEV:GRPZ:PSU:SIG:SWHT:ON')
        time.sleep(20)
        self._magnet.rtos()
        
        while self._magnet.z_ACTN.get() != ":HOLD":
            time.sleep(0.001)
            ##
            if self._magnet.z_setpoint.get()==self._magnet.z_fld.get():
                self._magnet.z_ACTN("HOLD")
                #heater off
        self._magnet.ask_raw('SET:DEV:GRPZ:PSU:SIG:SWHT:OFF')    
        
class ZField_Hon(qc.Parameter):
    def __init__(self, magnet):
        # only name is required
        super().__init__(name='zField',
                             label='Field along z axis',
#                         vals=qc.validators.Numbers(-6, 6),
                         docstring='Field along z axis')
        self._magnet = magnet

    # you must provide a get method, a set method, or both
    def get_raw(self):
#        return self._magnet.z_setpoint.get()
        return self._magnet.z_fld.get()

    def set_raw(self, val):
        # StandardParameter handles validation automatically, Parameter doesn't
#        self._vals.validate(val)
#        self._magnet.z_setpointC.set(val)
        self._magnet.z_setpoint.set(val)
        self._magnet.z_setpoint.set(val)
        self._magnet.ask_raw('SET:DEV:GRPZ:PSU:SIG:SWHT:ON')
        time.sleep(1)
        self._magnet.rtos()
        
        while self._magnet.z_ACTN.get() != ":HOLD":
            time.sleep(0.001)
            ##
            if self._magnet.z_setpoint.get()==self._magnet.z_fld.get():
                self._magnet.z_ACTN("HOLD")       

class Fres(qc.Parameter):
    def __init__(self, sweep, estimatedLorentianHeight, estimatedLorentianCenter, estimatedLorentianWidth, estimatedLorentianYOffset):
        # only name is required
        super().__init__(label='Resonance frequency',
                         vals=qc.validators.Numbers(),
                         docstring='Resonance frequency')
        self._sweep = sweep
        self._estimatedLorentianHeight  = estimatedLorentianHeight
        self._estimatedLorentianCenter  = estimatedLorentianCenter
        self._estimatedLorentianWidth   = estimatedLorentianWidth
        self._estimatedLorentianYOffset = estimatedLorentianYOffset

    # you must provide a get method, a set method, or both
    def get_raw(self):
        sweepdata = qc.Measure(self._sweep).run(name='blabla')
        dPhi = np.gradient(np.unwrap(sweepdata.ZIUHFLI_phase), 1 / len(sweepdata.ZIUHFLI_phase))
        fitfunc = lambda p, x: p[0] / (1 + ((x - p[1])/p[2])**2) + p[3] # Target function
        errfunc = lambda p, x, y: fitfunc(p, x) - y # Distance to the target function
        p0 = [self._estimatedLorentianHeight, self._estimatedLorentianCenter, self._estimatedLorentianWidth, self._estimatedLorentianYOffset] # Initial guess for the parameters
        p1, success = optimize.leastsq(errfunc, p0[:], args=(sweepdata.Hz_set, dPhi))
        return p1[1]

    def set_raw(self, val):
        time.sleep(0.001)
        
    
class Phi(qc.Parameter):
    def __init__(self, name, UHF, demodulator):
        super().__init__(name, label='phase', vals=qc.validators.Numbers(), unit='rad', docstring='UHF demodulator phase')
        self._daq = UHF.daq
#        self._daq.unsubscribe('*')
        self._daq.flush()
        self._sampleKey = '/dev2226/demods/'+str(demodulator)+'/sample'
        self._rateKey = '/dev2226/demods/'+str(demodulator)+'/rate'
        self._daq.subscribe(self._sampleKey)
        
    # you must provide a get method, a set_raw method, or both
    def get_raw(self):
        #self._daq.flush()
        notFound = True
        while notFound:
            d = self._daq.poll(1.5/self._daq.getDouble(self._rateKey),10,1, True)
#            d = self._daq.poll(1e-6,10,1, True)
            if self._sampleKey in d:
                x = d[self._sampleKey]['x']
                y = d[self._sampleKey]['y']
#                phi = d[self._sampleKey]['phi']
                notFound = False
            
#        return np.arctan2(np.mean(y),np.mean(x)) #np.arctan2(y[-1],x[-1])
       # print(len(x))
        #print(np.arctan2(y,x))
        self._daq.flush()
        return np.arctan2(y[-1],x[-1])
#                return phi[-1]
    
    def set_raw(self, val):
        time.sleep(0.001)    
        
class Module(qc.Parameter):
    def __init__(self, name, UHF, demodulator):
        super().__init__(name, label='Power attenuation', vals=qc.validators.Numbers(), unit='dB',
       docstring='Power attenuation between the injected signal and the reflected one demodulated by the UHF')
        self._uhf = UHF
#        self._uhf.daq.unsubscribe('*')
        self._uhf.daq.flush()
        self._sampleKey = '/dev2226/demods/'+str(demodulator)+'/sample'
        self._rateKey = '/dev2226/demods/'+str(demodulator)+'/rate'
        self._uhf.daq.subscribe(self._sampleKey)
        
    # you must provide a get method, a set method, or both
    def get_raw(self):
        self._uhf.daq.flush()
        notFound = True
        while notFound:
            d = self._uhf.daq.poll(1.5/self._uhf.daq.getDouble(self._rateKey),10,1, True)
            if self._sampleKey in d:
                x = d[self._sampleKey]['x']
                y = d[self._sampleKey]['y']
#                R = [self._sampleKey]['R']
                notFound = False
        return 20 * np.log10(np.sqrt(2) * np.sqrt(x[-1]**2+y[-1]**2)/self._uhf.signal_output1_amplitude.get())        
#        return 20 * np.log10(np.sqrt(2) * np.sqrt((x**2).mean()+(y**2).mean())/self._uhf.signal_output1_amplitude.get())
#                return R[-1]
                       
    def set_raw(self, val):
       time.sleep(1e-3)
     

class Ics(qc.Parameter):
    def __init__(self, name, UHF, demodulator):
        super().__init__(name, label='X', vals=qc.validators.Numbers(), unit='mV', docstring='UHF demodulator inphase component')
        self._daq = UHF.daq
        self._daq.flush()
        self._sampleKey = '/dev2226/demods/'+str(demodulator)+'/sample'
        self._rateKey = '/dev2226/demods/'+str(demodulator)+'/rate'
        self._daq.subscribe(self._sampleKey)
        
    # you must provide a get method, a set method, or both
    def get_raw(self):
        notFound = True
        while notFound:
            d = self._daq.poll(1.5/self._daq.getDouble(self._rateKey),10,1, True)
#            d = self._daq.poll(1e-6,10,1, True)
            if self._sampleKey in d:
                x = d[self._sampleKey]['x']
                notFound = False
            
        self._daq.flush()
        return x[-1]
    
    def set_raw(self, val):
        time.sleep(0.001)    

# **************  Classes for AWH UHF Zurich  **************************************************************************************

class Twait(qc.Parameter):
    def __init__(self, uhf, name='t_wait'):
        super().__init__(name, label='waiting time', vals=qc.validators.Numbers(150e-9, 1),#validator was previously 100e-9 and correction 50ns, depends on how many wait there are on AWG code
              unit='s', docstring='waiting time')
        self._uhf = uhf
        self._sequencerClockFreq = 225e6 # in Hz

    def set_raw(self, t_wait_sec):
        val = (t_wait_sec - 150e-9) * self._sequencerClockFreq
        self._uhf.daq.setDouble('/dev2226/awgs/0/userregs/0', val)

    def get_raw(self):
        return (self._uhf.daq.getDouble('/dev2226/awgs/0/userregs/0')/self._sequencerClockFreq)+150e-9


class Tpulse(qc.Parameter):
    def __init__(self, uhf, name='t_pulse'):
        super().__init__(name, label='pulsing time', vals=qc.validators.Numbers(),
              unit='s', docstring='pulsing time')
        self._uhf = uhf
        self._AWGClockFreq = 1.8e9 # in Hz

    def set_raw(self, t_pulse_sec):
        val = t_pulse_sec*self._AWGClockFreq
        self._uhf.daq.setDouble('/dev2226/awgs/0/userregs/1', val)

    def get_raw(self):
        return self._uhf.daq.getDouble('/dev2226/awgs/0/userregs/1')/self._AWGClockFreq


def change_tpulse(filename,t):
    lines=open(filename).read().splitlines()
    with open(filename,'r+') as f:
         f.truncate(0)
         lines[16]='const pulse_sec =' +str(t)+';'
#         lines[4]='const f_s =' + str()
         for i in range(len(lines)):
    
             f.write(lines[i]+'\n')
             
             #f.writelines()
    f.close()

def change_read(filename,A):
    lines=open(filename).read().splitlines()
    with open(filename,'r+') as f:
         f.truncate(0)
         lines[10]='const amplitude_read_scaled=' +str(A)+';'
         for i in range(len(lines)):
    
             f.write(lines[i]+'\n')
             
             #f.writelines()
    f.close()
    



#this time is expressed in terms of sequencer points    
class Tcompensation(qc.Parameter):
    def __init__(self, uhf, name='t_pulse'):
        super().__init__(name, label='pulsing time', vals=qc.validators.Numbers(),
              unit='s', docstring='pulsing time')
        self._uhf = uhf
        self._seqclock = 225e6 # in Hz

    def set_raw(self, t_pulse_sec):
        val = t_pulse_sec*self._seqclock
        self._uhf.daq.setDouble('/dev2226/awgs/0/userregs/2', val)

    def get_raw(self):
        return self._uhf.daq.getDouble('/dev2226/awgs/0/userregs/2')/self._seqclock


class TdoubleuserReg(qc.Parameter):
    def __init__(self, uhf, name='t_pulse'):
        super().__init__(name, label='pulsing time', vals=qc.validators.Numbers(),
              unit='s', docstring='pulsing time')
        self._uhf = uhf
        self._seqclock = 225e6 # in Hz
        self._AWGClockFreq = 1.8e9 # in Hz

    def set_raw(self, t_pulse_sec):
        val1 = t_pulse_sec*self._AWGClockFreq
        val2 = t_pulse_sec*self._seqclock-9 # in Hz 40ns wait correction
        self._uhf.daq.setDouble('/dev2226/awgs/0/userregs/1', val1)
        self._uhf.daq.setDouble('/dev2226/awgs/0/userregs/2', val2)

    def get_raw(self):
        return self._uhf.daq.getDouble('/dev2226/awgs/0/userregs/2')/self._seqclock

#distance between start of data transfer trigger and start of data acquisition 
class Ttrigger(qc.Parameter):
    def __init__(self, uhf, name='DAQ_delay'):
        super().__init__(name, label='daq_delay', vals=qc.validators.Numbers(),
              unit='s', docstring='daq_delay')
        self._uhf = uhf
        self._seqclock = 225e6 # in Hz

    def set_raw(self, t_pulse_sec):
        val = t_pulse_sec*self._seqclock
        self._uhf.daq.setDouble('/dev2226/awgs/0/userregs/3', val)

    def get_raw(self):
        return self._uhf.daq.getDouble('/dev2226/awgs/0/userregs/3')/self._seqclock
    
    
    
class AmpliPulseOutput1(qc.Parameter):
    def __init__(self, uhf, name='pulseAmplitude_B2'):
        super().__init__(name, label='pulse amplitude', vals=qc.validators.Numbers(-1,1),
              unit='fraction', docstring='pulse amplitude')
        self._uhf = uhf

    def set_raw(self, val):
        self._uhf.daq.setDouble('/dev2226/awgs/0/outputs/0/amplitude', val)

    def get_raw(self):
        return self._uhf.daq.getDouble('/dev2226/awgs/0/outputs/0/amplitude')
       
class AmpliPulseOutput2(qc.Parameter):
    def __init__(self, uhf, name='pulseAmplitude_T3'):
        super().__init__(name, label='pulse amplitude', vals=qc.validators.Numbers(-1,1),
              unit='fraction', docstring='pulse amplitude')
        self._uhf = uhf

    def set_raw(self, val):
        self._uhf.daq.setDouble('/dev2226/awgs/0/outputs/1/amplitude', val)

    def get_raw(self):
        return self._uhf.daq.getDouble('/dev2226/awgs/0/outputs/1/amplitude')       
    

    
class Pulsed_readout(qc.Parameter):
    def __init__(self, uhf, repetitions, returnOnePoint=True, treat_backgnd=False, name='phase_pulse'):
        super().__init__(name, label='phase triggered', vals=qc.validators.Numbers(),
              unit='rad', docstring='triggered readout of the phase')
        self._uhf = uhf
        self._uhf.daq.flush()
        self._dAM = self._uhf.daq.dataAcquisitionModule()
        self._repetitions = repetitions
        self._returnOnePoint = returnOnePoint
        self._dAM.set_raw('dataAcquisitionModule/device', 'dev2226')
        self._treat_backgnd = treat_backgnd
        
    def setSettings(self,  trigger_setting, grid_setting):
        self._dAM.set(trigger_setting)
        self._dAM.set(grid_setting)

        
    def get_raw(self):
        self._uhf.daq.flush()
        signal_path = '/dev2226/demods/1/sample.theta' 
        
        if self._repetitions > 1:
            signal_path += '.avg'  
                    
        self._dAM.subscribe(signal_path)
                
        self._dAM.execute()
        while not self._dAM.finished():
            time.sleep(0.0001)
#             time.sleep(5e-7)
            
        data = self._dAM.read(True)
        
        self._dAM.finish()
        
        self._dAM.unsubscribe('*')
        
        samples = data[signal_path]
        data_vector = samples[0]['value'] 
        
        if not self._returnOnePoint: 
            return data_vector
           
        else:
            if not self._treat_backgnd:
                return np.mean(data_vector[0][1:-1])
            else:
                signal = data_vector[0][240:340]#140-190uv,352 points grid
#                background = data_vector[0][150:len(data_vector[0])]
                background = data_vector[0][120:160]#70-90uV
                delta_signal = np.mean(signal) - np.mean(background)
                return delta_signal
        
    def closeModule(self):
        self._dAM.clear()       # Stop the Module's thread and clear the memory    
        
class Pulsed_readout_B3(qc.Parameter):
    def __init__(self, uhf, repetitions, returnOnePoint=True, treat_backgnd=False, name='phase_pulse_B3'):
        super().__init__(name, label='phase triggered_B3', vals=qc.validators.Numbers(),
              unit='rad', docstring='triggered readout of the phase')
        self._uhf = uhf
        self._uhf.daq.flush()
        self._dAM = self._uhf.daq.dataAcquisitionModule()
        self._repetitions = repetitions
        self._returnOnePoint = returnOnePoint
        self._dAM.set('dataAcquisitionModule/device', 'dev2226')
        self._treat_backgnd = treat_backgnd
        
    def setSettings(self,  trigger_setting, grid_setting):
        self._dAM.set(trigger_setting)
        self._dAM.set(grid_setting)

        
    def get_raw(self):
        self._uhf.daq.flush()
        signal_path = '/dev2226/demods/2/sample.theta' 
        
        if self._repetitions > 1:
            signal_path += '.avg'  
                    
        self._dAM.subscribe(signal_path)
                
        self._dAM.execute()
        while not self._dAM.finished():
            time.sleep(0.0001)
#             time.sleep(5e-7)
            
        data = self._dAM.read(True)
        
        self._dAM.finish()
        
        self._dAM.unsubscribe('*')
        
        samples = data[signal_path]
        data_vector = samples[0]['value'] 
        
        if not self._returnOnePoint: 
            return data_vector
           
        else:
            if not self._treat_backgnd:
                return np.mean(data_vector[0][1:-1])
            else:
                signal = data_vector[0][240:340]#140-190uv,352 points grid
#                background = data_vector[0][150:len(data_vector[0])]
                background = data_vector[0][120:160]#70-90uV
                delta_signal = np.mean(signal) - np.mean(background)
                return delta_signal
        
    def closeModule(self):
        self._dAM.clear()       # Stop the Module's thread and clear the memory    
        
        
class Pulsed_readout_S(qc.Parameter):
    def __init__(self, uhf, repetitions, returnOnePoint=True, treat_backgnd=False, name='phiS'):
        super().__init__(name, label='phaseS triggered', vals=qc.validators.Numbers(),
              unit='rad', docstring='triggered readout of the phaseS')
        self._uhf = uhf
        self._uhf.daq.flush()
        self._dAM = self._uhf.daq.dataAcquisitionModule()
        self._repetitions = repetitions
        self._returnOnePoint = returnOnePoint
        self._dAM.set('dataAcquisitionModule/device', 'dev2226')
        self._treat_backgnd = treat_backgnd
        
    def setSettings(self,  trigger_setting, grid_setting):
        self._dAM.set(trigger_setting)
        self._dAM.set(grid_setting)

        
    def get_raw(self):
        self._uhf.daq.flush()
        signal_path = '/dev2226/demods/1/sample.theta' 
        
        if self._repetitions > 1:
            signal_path += '.avg'  
                    
        self._dAM.subscribe(signal_path)
                
        self._dAM.execute()
        while not self._dAM.finished():
            time.sleep(0.0001)
#             time.sleep(5e-7)
            
        data = self._dAM.read(True)
        
        self._dAM.finish()
        
        self._dAM.unsubscribe('*')
        
        samples = data[signal_path]
        data_vector = samples[0]['value'] 
        
        if not self._returnOnePoint: 
            return data_vector
           
        else:
            if not self._treat_backgnd:
                return np.mean(data_vector[0][1:-1])
            else:
                signal = data_vector[0][240:340]#140-190uv,352 points grid
#                background = data_vector[0][150:len(data_vector[0])]
                background = data_vector[0][120:160]#70-90uV
                delta_signal = np.mean(signal) - np.mean(background)
                return delta_signal
        
    def closeModule(self):
        self._dAM.clear()       # Stop        

class Pulsed_readout_D(qc.Parameter):
    def __init__(self, uhf, repetitions, returnOnePoint=True, treat_backgnd=False, name='phiD'):
        super().__init__(name, label='phaseD triggered', vals=qc.validators.Numbers(),
              unit='rad', docstring='triggered readout of the phaseD')
        self._uhf = uhf
        self._uhf.daq.flush()
        self._dAM = self._uhf.daq.dataAcquisitionModule()
        self._repetitions = repetitions
        self._returnOnePoint = returnOnePoint
        self._dAM.set('dataAcquisitionModule/device', 'dev2226')
        self._treat_backgnd = treat_backgnd
        
    def setSettings(self,  trigger_setting, grid_setting):
        self._dAM.set(trigger_setting)
        self._dAM.set(grid_setting)

        
    def get_raw(self):
        self._uhf.daq.flush()
        signal_path = '/dev2226/demods/0/sample.theta' 
        
        if self._repetitions > 1:
            signal_path += '.avg'  
                    
        self._dAM.subscribe(signal_path)
                
        self._dAM.execute()
        while not self._dAM.finished():
            time.sleep(0.0001)
#             time.sleep(5e-7)
            
        data = self._dAM.read(True)
        
        self._dAM.finish()
        
        self._dAM.unsubscribe('*')
        
        samples = data[signal_path]
        data_vector = samples[0]['value'] 
        
        if not self._returnOnePoint: 
            return data_vector
           
        else:
            if not self._treat_backgnd:
                return np.mean(data_vector[0][1:-1])
            else:
                signal = data_vector[0][240:340]#140-190uv,352 points grid
#                background = data_vector[0][150:len(data_vector[0])]
                background = data_vector[0][120:160]#70-90uV
                delta_signal = np.mean(signal) - np.mean(background)
                return delta_signal
        
    def closeModule(self):
        self._dAM.clear()       # Stop        
        
        
class Pulsed_readout_amp(qc.Parameter):
    def __init__(self, uhf, repetitions, returnOnePoint=True, treat_backgnd=False, name='amp_pulse'):
        super().__init__(name, label='amplitude triggered', vals=qc.validators.Numbers(),
              unit='rad', docstring='triggered readout of the amplitude')
        self._uhf = uhf
        self._uhf.daq.flush()
        self._dAM = self._uhf.daq.dataAcquisitionModule()
        self._repetitions = repetitions
        self._returnOnePoint = returnOnePoint
        self._dAM.set('dataAcquisitionModule/device', 'dev2226')
        self._treat_backgnd = treat_backgnd
        
    def setSettings(self,  trigger_setting, grid_setting):
        self._dAM.set(trigger_setting)
        self._dAM.set(grid_setting)

        
    def get_raw(self):
        self._uhf.daq.flush()
        signal_path = '/dev2226/demods/1/sample.R' 
        
        if self._repetitions > 1:
            signal_path += '.avg'  
                    
        self._dAM.subscribe(signal_path)
                
        self._dAM.execute()
        while not self._dAM.finished():
            time.sleep(0.0001)
#             time.sleep(5e-7)
            
        data = self._dAM.read(True)
        
        self._dAM.finish()
        
        self._dAM.unsubscribe('*')
        
        samples = data[signal_path]
        data_vector = samples[0]['value'] 
        
        if not self._returnOnePoint: 
            return data_vector
           
        else:
            if not self._treat_backgnd:
                return np.mean(data_vector[0][1:-1])
            else:
                signal = data_vector[0][240:340]#140-190uv,352 points grid
#                background = data_vector[0][150:len(data_vector[0])]
                background = data_vector[0][120:160]#70-90uV
                delta_signal = np.mean(signal) - np.mean(background)
                return delta_signal
        
    def closeModule(self):
        self._dAM.clear()       # Stop the Module's thread and clear the memory         
        
def run_seq(device_id, awg_sourcefile=None):
    
        # Settings
        apilevel_example = 6  # The API level supported by this example.
        err_msg = "This example can only be ran on either a UHFAWG or a UHF with the AWG option enabled."
        # Call a zhinst utility function that returns:
        # - an API session `daq` in order to communicate with devices via the data server.
        # - the device ID string that specifies the device branch in the server's node hierarchy.
        # - the device's discovery properties.
        (daq, device, props) = zhinst.utils.create_api_session(device_id, apilevel_example, required_devtype='UHF',
                                                               required_options=['AWG'], required_err_msg=err_msg)
        zhinst.utils.api_server_version_check(daq)
    
    #I removed this , I can put daq settings I want for triggering
        # Create a base instrument configuration: disable all outputs, demods and scopes.
#        general_setting = [['/%s/demods/*/enable' % device, 0],
#                           ['/%s/demods/*/trigger' % device, 0],
#                           ['/%s/sigouts/*/enables/*' % device, 0],
#                           ['/%s/scopes/*/enable' % device, 0]]
#        if 'IA' in props['options']:
#            general_setting.append(['/%s/imps/*/enable' % device, 0])
#        daq.set(general_setting)
#        
        ####
        # Perform a global synchronisation between the device and the data server:
        # Ensure that the settings have taken effect on the device before continuing.
        daq.sync()
    
        print("Disabling AWG.")
        daq.setInt('/' + device + '/awgs/0/enable', 1)
        daq.sync()
    
        # Create an instance of the AWG Module
        awgModule = daq.awgModule()
        awgModule.set('awgModule/device', device)
        awgModule.execute()
    
        # Get the LabOne user data directory.
        data_dir = awgModule.getString('awgModule/directory')
        # The AWG Tab in the LabOne UI also uses this directory for AWG segc files.
        src_dir = os.path.join(data_dir, "awg", "src")
        if not os.path.isdir(src_dir):
            # The data directory is created by the AWG module and should always exist. If this exception is raised,
            # something might be wrong with the file system.
            raise Exception("AWG module wave directory {} does not exist or is not a directory".format(src_dir))
    
        # Note, the AWG source file must be located in the AWG source directory of the user's LabOne data directory.
        if awg_sourcefile is None:
            # Write an AWG source file to disk that we can compile in this example.
            awg_sourcefile = "ziPython_example_awg_sourcefile.seqc"
            with open(os.path.join(src_dir, awg_sourcefile), "w") as f:
                f.write(source)
        else:
            if not os.path.exists(os.path.join(src_dir, awg_sourcefile)):
                raise Exception("The file {} does not exist, this must be specified via an "
                                "absolute or relative path.".format(awg_sourcefile))
    
        print("Will compile and load", awg_sourcefile, "from", src_dir)
    
        # Transfer the AWG sequence program. Compilation starts automatically.
        awgModule.set('awgModule/compiler/sourcefile', awg_sourcefile)
        # Note: when using an AWG program from a source file (and only then), the compiler needs to
        # be started explicitly:
        awgModule.set('awgModule/compiler/start', 1)
        timeout = 20
        t0 = time.time()
        while awgModule.get('awgModule/compiler/status')['compiler']['status'][0] == -1:
            time.sleep(0.1)
            if time.time() - t0 > timeout:
                Exception("Timeout")
    
        if awgModule.get('awgModule/compiler/status')['compiler']['status'][0] == 1:
            # compilation failed, raise an exception
            raise Exception(awgModule.get('awgModule/compiler/statusstring')['compiler']['statusstring'][0])
        else:
            if awgModule.get('awgModule/compiler/status')['compiler']['status'][0] == 0:
                print("Compilation successful with no warnings, will upload the program to the instrument.")
            if awgModule.get('awgModule/compiler/status')['compiler']['status'][0] == 2:
                print("Compilation successful with warnings, will upload the program to the instrument.")
                print("Compiler warning: " +
                      awgModule.get('awgModule/compiler/statusstring')['compilelsr']['statusstring'][0])
            # Wait for the waveform upload to finish
            time.sleep(0.2)
            i = 0
            while awgModule.get('awgModule/progress')['progress'][0] < 1.0:
                print("{} progress: {}".format(i, awgModule.get('awgModule/progress')['progress'][0]))
                time.sleep(0.5)
                i += 1
    
        print('Success. Enabling the AWG.')
        daq.setInt('/' + device + '/awgs/0/enable', 1)

#correction for high sampling rate    
class Symmetricpulse(qc.Parameter):
    def __init__(self, uhf ,name='t_pulse_and_wait'):
        super().__init__(name, label='semiperiod_duty50', vals=qc.validators.Numbers(150e-9, 1),#validator was previously 100e-9 and correction 50ns, depends on how many wait there are on AWG code
              unit='s', docstring='waiting time')
        self._uhf = uhf
        self._sequencerClockFreq = 225e6 # in Hz
#        folder =r'C:\Users\g-gre-gre050402\Documents\Zurich Instruments\LabOne\WebServer\awg\src\negativepulse_fixpulsevarywait_triggered.seqc'
#        folder='C:\\Users\\g-gre-gre050402\\Documents\\Zurich Instruments\\LabOne\\WebServer\\awg\\src\\negativepulse_fixpulsevarywait_triggered.seqc'

    
    
    def set_raw(self, t_wait_sec):
#        if(t_wait_sec<36.4e-6):
        val = (t_wait_sec - 150e-9) * self._sequencerClockFreq
        self._uhf.daq.setDouble('/dev2226/awgs/0/userregs/0', val)
#        else :
#         val = (t_wait_sec - 150e-9-6e-6) * self._sequencerClockFreq
#         self._uhf.daq.setDouble('/dev2226/awgs/0/userregs/0', val)  
         
        changetpulse('C:\\Users\\g-gre-gre050402\\Documents\\Zurich Instruments\\LabOne\\WebServer\\awg\\src\\negativepulse_fixpulsevarywait_triggered.seqc', t_wait_sec)    
        run_seq('dev2226','negativepulse_fixpulsevarywait_triggered.seqc')

    def get_raw(self):
        return (self._uhf.daq.getDouble('/dev2226/awgs/0/userregs/0')/self._sequencerClockFreq)+150e-9        
 

class Symmetricpulse_ramp(qc.Parameter):
    def __init__(self, uhf ,name='t_pulse_and_wait'):
        super().__init__(name, label='semiperiod_duty50', vals=qc.validators.Numbers(150e-9, 1),#validator was previously 100e-9 and correction 50ns, depends on how many wait there are on AWG code
              unit='s', docstring='waiting time')
        self._uhf = uhf
        self._sequencerClockFreq = 225e6 # in Hz
#        folder =r'C:\Users\g-gre-gre050402\Documents\Zurich Instruments\LabOne\WebServer\awg\src\negativepulse_fixpulsevarywait_triggered.seqc'
#        folder='C:\\Users\\g-gre-gre050402\\Documents\\Zurich Instruments\\LabOne\\WebServer\\awg\\src\\negativepulse_fixpulsevarywait_triggered.seqc'

    
    
    def set_raw(self, t_wait_sec):
#        if(t_wait_sec<36.4e-6):
        val = (t_wait_sec - 150e-9) * self._sequencerClockFreq
        self._uhf.daq.setDouble('/dev2226/awgs/0/userregs/0', val)
#        else :
#         val = (t_wait_sec - 150e-9-6e-6) * self._sequencerClockFreq
#         self._uhf.daq.setDouble('/dev2226/awgs/0/userregs/0', val)  
         
        changetpulse('C:\\Users\\g-gre-gre050402\\Documents\\Zurich Instruments\\LabOne\\WebServer\\awg\\src\\negativepulse_fixpulsevarywait_triggered.seqc', t_wait_sec)    
        run_seq('dev2226','negativepulse_fixpulsevarywait_triggered.seqc')

    def get_raw(self):
        return (self._uhf.daq.getDouble('/dev2226/awgs/0/userregs/0')/self._sequencerClockFreq)+150e-9      
    
class pulsetime(qc.Parameter):
    def __init__(self, uhf ,name='t_pulse_and_wait'):
        super().__init__(name, label='semiperiod_duty50', vals=qc.validators.Numbers(150e-9, 1),#validator was previously 100e-9 and correction 50ns, depends on how many wait there are on AWG code
              unit='s', docstring='waiting time')
        self._uhf = uhf
        self._sequencerClockFreq = 225e6 # in Hz
#        folder =r'C:\Users\g-gre-gre050402\Documents\Zurich Instruments\LabOne\WebServer\awg\src\negativepulse_fixpulsevarywait_triggered.seqc'
#        folder='C:\\Users\\g-gre-gre050402\\Documents\\Zurich Instruments\\LabOne\\WebServer\\awg\\src\\negativepulse_fixpulsevarywait_triggered.seqc'

    
    
    def set_raw(self, t_wait_sec):
#        if(t_wait_sec<36.4e-6):
        val = (t_wait_sec - 150e-9) * self._sequencerClockFreq
        self._uhf.daq.setDouble('/dev2226/awgs/0/userregs/0', val)
#        else :
#         val = (t_wait_sec - 150e-9-6e-6) * self._sequencerClockFreq
#         self._uhf.daq.setDouble('/dev2226/awgs/0/userregs/0', val)  
         
        changetpulse('C:\\Users\\g-gre-gre050402\\Documents\\Zurich Instruments\\LabOne\\WebServer\\awg\\src\\Morello_Tritonito.seqc', t_wait_sec)    
        run_seq('dev2226','Morello_Tritonito.seqc')

    def get_raw(self):
        return (self._uhf.daq.getDouble('/dev2226/awgs/0/userregs/0')/self._sequencerClockFreq)+150e-9       
    
    
    
    
class Read_level(qc.Parameter):
    def __init__(self, uhf ,name='read_amplitude'):
        super().__init__(name, label='read_ampli', vals=qc.validators.Numbers(-1, 1),#amplitude of read is fraction of total amplitude
              unit='mV', docstring='read_level')
        self._uhf = uhf
        self._sequencerClockFreq = 225e6 # in Hz

    def set_raw(self, readlevel):
        amplimV=readlevel
        A=amplimV/ampliAWG()/5.5 #renormalize in AWG units
        changeAread('C:\\Users\\g-gre-gre050402\\Documents\\Zurich Instruments\\LabOne\\WebServer\\awg\\src\\diagonal_pulse.seqc', A)    
        run_seq('dev2226','diagonal_pulse.seqc')
        ziUhf.daq.setInt('/dev2226/demods/1/enable', 1)
        ziUhf.daq.setInt('/dev2226/demods/0/enable', 1)
        ziUhf.daq.setInt('/dev2226/sigouts/0/enables/4', 1)
        ziUhf.daq.setInt('/dev2226/demods/0/trigger', 33554432)
        

class Pulse_duration(qc.Parameter):
    def __init__(self, uhf ,name='pulse_duration'):
        super().__init__(name, label='read_ampli', vals=qc.validators.Numbers(0, 1),
              unit='s', docstring='pulse_duration')
        self._uhf = uhf
        self._sequencerClockFreq = 225e6 # in Hz

    def set_raw(self, duration):
        change_tpulse('C:\\Users\\g-gre-gre050402\\Documents\\Zurich Instruments\\LabOne\\WebServer\\awg\\src\\morello_Tritonito.seqc', duration)    
        run_seq('dev2226','Morello_Tritonito.seqc')


# **************  Classes for AWH UHF Zurich  -  end  **************************************************************************************




# ************************************************************
class SNR(qc.Parameter):
    def __init__(self, UHF, name='SNR'):
        super().__init__(name, label='Signal to Noise Ratio', vals=qc.validators.Numbers(),
              unit='dB', docstring='The height of the sidebands in respect to the noise floor')
        self._uhf = UHF
        
    def get_raw(self):
        demod_index = 0
        return_flat_data_dict = True
        # Create an instance of the Spectrum Analyser Module (ziDAQZoomFFT class).
        zoomfft = self._uhf.daq.zoomFFT()
        # Set the device that will be used for the spectrum analyser - this parameter must be set.
        zoomfft.set('zoomFFT/device', self._uhf.device)
        # Spectrum mode FFT(x+iy) = 0, FFT(r) = 1, FFT(theta) = 2, FFT(freq) = 3, FFT(dtheta/dt)/2pi = 4
        zoomfft.set('zoomFFT/mode', 2)
        # Disable overlap mode.
        zoomfft.set('zoomFFT/overlap', 0)
        # Use a Hann windowing function in the FFT:
        # 0=Rectangular, 1=Hann, 2=Hamming, 3=Blackman Harris.
        zoomfft.set('zoomFFT/window', 1)
        # Return absolute frequencies instead of relative to 0.
        zoomfft.set('zoomFFT/absolute', 0)
        # The number of lines is 2**bits.
        zoomfft.set('zoomFFT/bit', 14)
        # The number of zoomFFT's to perform.
        loopcount = 1
        zoomfft.set('zoomFFT/loopcount', loopcount)
        # The Spectrum Analyzer Module needs to subscribe to the nodes it will return data for.
        path = '/%s/demods/%d/sample' % (self._uhf.device, demod_index)
        zoomfft.subscribe(path)
        # Start the zoomFFT.
        zoomfft.execute()
        # Wait until the FFT is done
        while not zoomfft.finished():
            time.sleep(0.001)
        # Read the zoomFFT data.
        data = zoomfft.read(return_flat_data_dict)
        # Unsubscribe from the data nodes
        zoomfft.unsubscribe(path)
        # Stop the module's thread and clear the memory.
        zoomfft.clear()
        
        assert data, "FFT returned an empty data dictionary!"
        assert path in data, "data dictionary has no key '%s'" % path
        
        return data[path]
    
    
    
class Phicomp(qc.Parameter):
    def __init__(self, name, UHF, demodulator,VB3,phaseref):
        super().__init__(name, label='phaseB3comp', vals=qc.validators.Numbers(), unit='rad', docstring='UHF demodulator phase')
        self._daq = UHF.daq
#        self._daq.unsubscribe('*')
        self._daq.flush()
        self._sampleKey = '/dev2226/demods/'+str(demodulator)+'/sample'
        self._rateKey = '/dev2226/demods/'+str(demodulator)+'/rate'
        self._daq.subscribe(self._sampleKey)
        
        self._VB3get=VB3.get
        self._VB3set=VB3.set
        self._phi0=phaseref        
    # you must provide a get method, a set method, or both
    def get_raw(self):
        #self._daq.flush()
        notFound = True
        while notFound:
            d = self._daq.poll(1.5/self._daq.getDouble(self._rateKey),10,1, True)
#            d = self._daq.poll(1e-6,10,1, True)
            if self._sampleKey in d:
                x = d[self._sampleKey]['x']
                y = d[self._sampleKey]['y']
#                phi = d[self._sampleKey]['phi']
                notFound = False
            
#        return np.arctan2(np.mean(y),np.mean(x)) #np.arctan2(y[-1],x[-1])
       # print(len(x))
        #print(np.arctan2(y,x))
        self._daq.flush()
        
        m=-0.014 #rad/mV
#        m=-0.01428 #rad/mV

        phasenow=np.arctan2(y[-1],x[-1])
        dphi=phasenow-self._phi0
        B3val=self._VB3get()-dphi/m
        self._VB3set(B3val)
#
#        while notFound:
#            d = self._daq.poll(1.5/self._daq.getDouble(self._rateKey),10,1, True)
##            d = self._daq.poll(1e-6,10,1, True)
#            if self._sampleKey in d:
#                x = d[self._sampleKey]['x']
#                y = d[self._sampleKey]['y']
##                phi = d[self._sampleKey]['phi']
#                notFound = False
#        self._daq.flush()
        
        return np.arctan2(y[-1],x[-1])
    
    
    
######parameters created after 15/10/2020


class CompensateG3(qc.Parameter):
    def __init__(self, gate1, gate2,slope):
        super().__init__(name='CompensatedG3', label='CompensatedG3', vals=qc.validators.Numbers(-2500, 2500), unit='mV')
        self._gate1 = gate1
        self._gate2 = gate2
        self._slope = slope
        
    def get_raw(self):

     return self._gate1(),self._gate2()
        
    def set_raw(self, val):
        #first record old values and change relative values
        init1=self._gate1()
        init2=self._gate2()
        dx=val-init1
        dy=dx*self._slope
        self._gate1(val)
        time.sleep(0.01)
        self._gate2(init2+dy)
        

class CompensateG2(qc.Parameter):
    def __init__(self, gate1, gate2,slope):
        super().__init__(name='CompensatedG2', label='CompensatedG2', vals=qc.validators.Numbers(-2500, 2500), unit='mV')
        self._gate1 = gate1
        self._gate2 = gate2
        self._slope = slope
        
    def get_raw(self):

     return self._gate1(),self._gate2()
        
    def set_raw(self, val):
        #first record old values and change relative values
        init1=self._gate1()
        init2=self._gate2()
        dx=val-init1
        dy=dx*self._slope
        self._gate1(val)
        # send volt XXX
        # send syst:err?
        # wait for reply
        # send volt YYY

        time.sleep(0.01)
        self._gate2(init2+dy)

class CompensateG4(qc.Parameter):
    def __init__(self, gate1, gate2,slope):
        super().__init__(name='CompensatedG4', label='CompensatedG4', vals=qc.validators.Numbers(-2500, 2500), unit='mV')
        self._gate1 = gate1
        self._gate2 = gate2
        self._slope = slope
        
    def get_raw(self):

     return self._gate1(),self._gate2()
        
    def set_raw(self, val):
        #first record old values and change relative values
        init1=self._gate1()
        init2=self._gate2()
        dx=val-init1
        dy=dx*self._slope
        self._gate1(val)
        time.sleep(0.01)
        self._gate2(init2+dy)
        
        
class CompensateG4_double(qc.Parameter):
    def __init__(self, gate1, gate2,gate3,slope,slope2):
        super().__init__(name='CompensatedG4', label='CompensatedG4', vals=qc.validators.Numbers(-2500, 2500), unit='mV')
        self._gate1 = gate1
        self._gate2 = gate2
        self._gate3 = gate3
        self._slope = slope
        self._slope2 = slope2
        
    def get_raw(self):

     return self._gate1(),self._gate2(),self._gate3()
        
    def set_raw(self, val):
        #first record old values and change relative values
        init1=self._gate1()
        init2=self._gate2()
        init3=self._gate3()
        
        dx=val-init1
        dy=dx*self._slope
        dz=dx*self._slope2
        self._gate1(val)
        time.sleep(0.012)
        self._gate2(init2+dy)
        time.sleep(0.012)
        self._gate3(init3+dz)
        
        
class CompensateG3_double(qc.Parameter):
    def __init__(self, gate1, gate2,gate3,slope,slope2):
        super().__init__(name='CompensatedG3', label='CompensatedG3', vals=qc.validators.Numbers(-2500, 2500), unit='mV')
        self._gate1 = gate1
        self._gate2 = gate2
        self._gate3 = gate3
        self._slope = slope
        self._slope2 = slope2
        
    def get_raw(self):

     return self._gate1(),self._gate2(),self._gate3()
        
    def set_raw(self, val):
        #first record old values and change relative values
        init1=self._gate1()
        init2=self._gate2()
        init3=self._gate3()
        
        dx=val-init1
        dy=dx*self._slope
        dz=dx*self._slope2
        self._gate1(val)
        time.sleep(0.012)
        self._gate2(init2+dy)
        time.sleep(0.012)
        self._gate3(init3+dz)
        
        

    
# class Pulsed_readout_both(qc.Parameter):
#     # def __init__(self, uhf, repetitions, returnOnePoint=True, treat_backgnd=False, name='phase_pulse'):
#     #     super().__init__(name, label='phase triggered', vals=qc.validators.Numbers(),
#     #           unit='rad', docstring='triggered readout of the phase')
#     #     self._uhf = uhf
#     #     self._uhf.daq.flush()
#     #     self._dAM = self._uhf.daq.dataAcquisitionModule()
#     #     # self._dAMD = self._uhf.daq.dataAcquisitionModule()
#     #     self._repetitions = repetitions
#     #     self._returnOnePoint = returnOnePoint
#     #     self._dAM.set_raw('dataAcquisitionModule/device', 'dev2226')
#     #     # self._dAMD.set_raw('dataAcquisitionModule/device', 'dev2226')
#     #     self._treat_backgnd = treat_backgnd
#     def __init__(self, uhf, repetitions, returnOnePoint=True, treat_backgnd=False, name='phase_pulse'):
#         super().__init__(name, label='phase triggered', vals=qc.validators.Numbers(),
#               unit='rad', docstring='triggered readout of the phase')
#         self._uhf = uhf
#         self._uhf.daq.flush()
#         self._dAM = self._uhf.daq.dataAcquisitionModule()
#         self._repetitions = repetitions
#         self._returnOnePoint = returnOnePoint
#         self._dAM.set_raw('dataAcquisitionModule/device', 'dev2226')
#         self._treat_backgnd = treat_backgnd
#     def setSettings(self,  trigger_setting, grid_setting):
#         self._dAM.set(trigger_setting)
#         # self._dAMD.set(trigger_setting)
#         self._dAM.set(grid_setting)
#         # self._dAMD.set(grid_setting)
        
#     def get_raw(self):
#         self._uhf.daq.flush()
#         signal_pathS = '/dev2226/demods/1/sample.theta' 
#         signal_pathD = '/dev2226/demods/0/sample.theta' 
        
#         if self._repetitions > 1:
#             signal_path += '.avg'  
                    
#         self._dAM.subscribe(signal_pathS)
#         self._dAM.subscribe(signal_pathD)  
        
        
#         self._dAM.execute()
#         while not self._dAM.finished():
#             time.sleep(0.0001)
# #             time.sleep(5e-7)
            
#         dataS = self._dAM.read(True)
#         dataD = self._dAM.read(True)
#         self._dAM.finish()
        
#         self._dAM.unsubscribe('*')
        
#         samplesS,samplesD = dataS[signal_pathS],dataD[signal_pathD]
#         data_vectorS,data_vectorD = samplesS[0]['value'] , samplesD[0]['value']
        
#         if not self._returnOnePoint: 
#             return data_vectorS,data_vectorD
        
           
#         else:
#             if not self._treat_backgnd:
#                 return np.mean(data_vectorS[0][1:-1]), np.mean(data_vectorD[0][1:-1])
#             else:
#                 signal = data_vector[0][240:340]#140-190uv,352 points grid
# #                background = data_vector[0][150:len(data_vector[0])]
#                 background = data_vector[0][120:160]#70-90uV
#                 delta_signal = np.mean(signal) - np.mean(background)
#                 return delta_signal
            
            
            

    

class Pulsed_readout_both(qc.Parameter):
    def __init__(self, uhf, repetitions, returnOnePoint=True, treat_backgnd=False, name='phiS'):
        super().__init__(name, label='phaseS triggered', vals=qc.validators.Numbers(),
              unit='rad', docstring='triggered readout of the phaseS')
        self._uhf = uhf
        self._uhf.daq.flush()
        self._dAM = self._uhf.daq.dataAcquisitionModule()
        self._repetitions = repetitions
        self._returnOnePoint = returnOnePoint
        self._dAM.set('dataAcquisitionModule/device', 'dev2226')
        self._treat_backgnd = treat_backgnd
        
    def setSettings(self,  trigger_setting, grid_setting):
        self._dAM.set(trigger_setting)
        self._dAM.set(grid_setting)

        
    def get_raw(self):
        self._uhf.daq.flush()
        signal_path = '/dev2226/demods/1/sample.theta' 
        signal_pathD = '/dev2226/demods/0/sample.theta' 
        
        if self._repetitions > 1:
            signal_path += '.avg'  
            signal_pathD += '.avg'  
                    
        self._dAM.subscribe(signal_path)
        self._dAM.subscribe(signal_pathD)
                
        self._dAM.execute()
        while not self._dAM.finished():
            time.sleep(0.0001)
#             time.sleep(5e-7)
            
        data= self._dAM.read(True)
        
        self._dAM.finish()
        
        self._dAM.unsubscribe('*')
        
        samples,samplesD = data[signal_path],data[signal_pathD]
        data_vector = samples[0]['value'] 
        data_vectorD = samplesD[0]['value'] 
        if not self._returnOnePoint: 
            return data_vector, data_vectorD
           
        else:
            if not self._treat_backgnd:
                return np.mean(data_vector[0][1:-1])
            else:
                signal = data_vector[0][240:340]#140-190uv,352 points grid
#                background = data_vector[0][150:len(data_vector[0])]
                background = data_vector[0][120:160]#70-90uV
                delta_signal = np.mean(signal) - np.mean(background)
                return delta_signal
        
    def closeModule(self):
        self._dAM.clear()       # Stop        