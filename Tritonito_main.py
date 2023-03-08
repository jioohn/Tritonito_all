# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 12:07:56 2018

@author: G-GRE-GRE050402
"""

from qcodes.dataset.measurements import Measurement 
from qcodes.dataset.plotting import plot_by_id
from qcodes import initialise_or_create_database_at
from qcodes.dataset.experiment_container import new_experiment
import datetime
#####################################################
# import init
import plottr
# import matplotlib
import sys
import os
import zhinst.utils
import matplotlib.pyplot as plt
# import qcodes.instrument_drivers.Anritsu.MG3693C as MG3693C ## this is the driver provided by qcodes, I modified it to be able to change tburst and burstwidth

#DAC.CLOSE() !!!!!!
import time
import SpecialParameters 
# import SpecialParameters_Tritonito as SpecialParameters 
import numpy as np
from InstrumentsHandler import InstrumentsHandler
import qcodes as qc
import scipy.signal
import MG3693C
# import qcodes_contrib_drivers.drivers.Bilt.iTest as Bilt

# import  qcodes.instrument_drivers.Bilt.iTest as iTest

import iTest 

# from qcodes.instrument_drivers.agilent import Agilent_E8527D_Lateqs
import qcodes.instrument_drivers.Keysight.Keysight_34465A_submodules as Keysight
# from qcodes.instrument_drivers.Keysight import Keysight_34465A 
# import qcodes.instrument_drivers.agilent.Agilent_E8527D_Lateqs as E8527D


import mercuryiPS#careful, it's the one in Tzirkle folder

from qcodes.instrument_drivers.ZI.ZIUHFLI import ZIUHFLI

##driver used previously

# import qcodes.instrument_drivers.oxford.mercuryiPS as mercuryiPS
# import mercuryiPS 
import scipy
from scipy.optimize import curve_fit
# import Agilent_E8527D_Lateqs
from time import sleep
import scipy.signal
# import qcodes
from qcodes import Station, load_or_create_experiment,initialise_database, Measurement, Instrument, VisaInstrument, ManualParameter, MultiParameter, validators as vals
from qcodes.dataset.plotting import plot_by_id, plot_dataset
from qcodes.dataset.data_set import new_data_set
from qcodes.dataset.data_set import load_by_id

# from qcodes_gre.measurements.time_trace_uhf import DAM
# from qcodes_gre.measurements.time_trace_uhf import DAMTrig

from tqdm.notebook import tqdm, trange

from time_trace_uhf import DAM
from time_trace_uhf import DAMTrig

# from qcodes_gre.measurements.time_trace_uhf import DAM
# from time_trace_uhf import DAM
# from time_trace_uhf import DAMTrig

# initialise_or_create_database_at('../data/2021_09_08_2S13_3.db')
# initialise_or_create_database_at('S:/132-PHELIQS/132.05-LATEQS/132.05.01-QuantumSilicon/Tritonito/2021/Feb2021_6G22_2_die103/data/2021_05_07_6G22_2.db')
initialise_or_create_database_at('C:\Users\AA255540\Desktop\Tritonito2021_alldata\Feb2021_6G22_2_die103\data\2021_12_03_6G22_2.db')
qc.config.core.db_location
# exp = qc.load_or_create_experiment(experiment_name='ABM', sample_name="4G11_1" )
exp = qc.load_or_create_experiment(experiment_name='reflecto_reservoir_vs_gate', sample_name="6G22_2" )
folder2=r'S:\132-PHELIQS\132.05-LATEQS\132.05.01-QuantumSilicon\Tritonito\2021\Feb2021_6G22_2_die103\data'
now=datetime.datetime.now()
dayFolder= datetime.date.isoformat(now)
try:
        os.makedirs(folder2+'\\'+dayFolder)
except IOError:
        donothing=1

#add
################################

sample_name = '6G22_2'


#dac.close()
# ih = InstrumentsHandler('InstrumentsConfig.yaml')
# ih.loadConfigFile()

# dmm=Agilent.Agilent_34400A(name='dmm',address='TCPIP0::192.168.150.4::inst0::INSTR')

dmm=Keysight.Keysight_34465A(name='dmm',address='TCPIP0::192.168.150.4::inst0::INSTR')
def func(): 
	return dmm.volt.get() * 1e-8

current = qc.Parameter('current', instrument=dmm, get_cmd=func,get_parser=float)
# dac=iTest.ITest(name='dac',address='TCPIP0::192.168.150.115::5025::SOCKET')#ethernet
dac=iTest.ITest(name='dac',address='ASRL5')#USB, does not disconnect
mwgen=MG3693C.MG3693C(name='mwgen',address = 'GPIB0::6::INSTR')#Anritsu

###magnet load
magnet = mercuryiPS.MercuryiPS(name = 'magnet', address = '192.168.150.3')#,axes='Z')

Bfield=SpecialParameters.ZField(magnet)#keep heater off after changing field
Bfield_Hon=SpecialParameters.ZField_Hon(magnet)#keep heater on after changing field


# dmm=ih.loadInstrument('dmm')
#dac=ih.loadInstrument('dac')
#mwgen      = ih.loadInstrument('mwgen')
# magnet      = ih.loadInstrument('magnet') 
# ziUhf= ih.loadInstrument('uhf')

uhfRef='dev2226'
ziUhf = ZIUHFLI('ZIUHFLI', uhfRef)

#1 is really 1
daq =DAM(ziUhf, 2)
daqtrig= DAMTrig(ziUhf,2)

daq_S =DAM(ziUhf, 2)
daqtrig_S= DAMTrig(ziUhf,2)
daq_D =DAM(ziUhf, 1)
daqtrig_D= DAMTrig(ziUhf,1)

station = qc.Station(dac,ziUhf,dmm,magnet)#,mwgen)
                     
VG1 = qc.ScaledParameter(dac.dac1, gain=1000, name='G1', label='$V_{G1}$', unit='mV')
VG2 = qc.ScaledParameter(dac.dac2, gain=1000, name='G2', label='$V_{G2}$', unit='mV')

VG3= qc.ScaledParameter(dac.dac3, gain=1000, name='G3', label='$V_{G3}$', unit='mV')
VG4= qc.ScaledParameter(dac.dac4, gain=1000, name='G4', label='$V_{G4}$', unit='mV')
VG5= qc.ScaledParameter(dac.dac5, gain=1000, name='G5', label='$V_{G5}$', unit='mV')
VG6= qc.ScaledParameter(dac.dac6, gain=1000, name='G6', label='$V_{G6}$', unit='mV')


VGfake= qc.ScaledParameter(dac.dac8, gain=1000, name='timegate', label='$time$', unit='A.U.')

bias = qc.ScaledParameter(dac.dac7, gain=1000, name='VDS', label='$V_{DS}$', unit='mV')

Top_gate= qc.ScaledParameter(dac.dac17, gain=1000, name='VTG', label='$V_{TG}$', unit='mV')

rampVG1 = qc.ScaledParameter(dac.rampdac1, gain=1000, name='G1', label='VG1', unit='mV')
rampVG2 = qc.ScaledParameter(dac.rampdac2, gain=1000, name='G2', label='VG2', unit='mV')

rampVG3= qc.ScaledParameter(dac.rampdac3, gain=1000, name='G3', label='VG3', unit='mV')
rampVG4= qc.ScaledParameter(dac.rampdac4, gain=1000, name='G4', label='VG4', unit='mV')

rampVG5= qc.ScaledParameter(dac.rampdac5, gain=1000, name='G5', label='VG5', unit='mV')

rampVG6= qc.ScaledParameter(dac.rampdac6, gain=1000, name='G6', label='VG6', unit='mV')

#useful numbers
h=4.135667662e-15 #eV*s
bohr=5.7883818e-5#eV*
fontSize=16
kb=8.61733e-5#eV/K
#
#
#

A1 = ziUhf.demod1_R
A2 = ziUhf.demod2_R
A3 = ziUhf.demod3_R
A4 = ziUhf.demod4_R
ph1 = ziUhf.demod1_phi
# ph2 = ziUhf.demod8_phi
ph3 = ziUhf.demod3_phi
ph4 = ziUhf.demod4_phi


##############
ph2 = ziUhf.demod5_phi
A2 = ziUhf.demod5_R
#######################


# att = SpecialParameters.Module('attenuation', ziUhf,0) #T2
# phase = SpecialParameters.Phi('phi', ziUhf, 0) #T2

# attB3 = SpecialParameters.Module('attenuationB3', ziUhf,5)
# ph1 = SpecialParameters.PhiD('phiD', ziUhf, 0)
# ph2 = SpecialParameters.PhiD('phiS', ziUhf, 1)
# ph3 = SpecialParameters.Phi('phiG6', ziUhf, 2)
# ph4 = SpecialParameters.Phi('phiG1', ziUhf, 3)

# ics = SpecialParameters.Ics('X', ziUhf, 1)
twait = SpecialParameters.Twait(ziUhf)#user Reg0
#tpulse = SpecialParameters.Tpulse(ziUhf)#userreg1
tcomp = SpecialParameters.Tcompensation(ziUhf)#userreg2 # in terms of f_seq
tpulse = SpecialParameters.TdoubleuserReg(ziUhf)#userreg1 & userreg2 same number in different point units compensation of twait(add wait to keep it constant)
t_trigger= SpecialParameters.Ttrigger(ziUhf)

period=SpecialParameters.Symmetricpulse(ziUhf)



ampliAWG=SpecialParameters.AmpliPulseOutput1(ziUhf)
ampliAWG_B2=SpecialParameters.AmpliPulseOutput1(ziUhf)
ampliAWG_T3=SpecialParameters.AmpliPulseOutput2(ziUhf)

rf1power= SpecialParameters.Reflecto_power('rf1_power', ziUhf, 0,4)#out1_amp1 #the get is wrong, set is fine
rf2power= SpecialParameters.Reflecto_power('rf2_power', ziUhf, 0,5)#out1_amp2
rf3power= SpecialParameters.Reflecto_power('rf3_power', ziUhf, 0,2)#out1_amp3
rf4power= SpecialParameters.Reflecto_power('rf4_power', ziUhf, 0,3)#out1_amp4

G1power= SpecialParameters.Reflecto_power('rf3_power', ziUhf, 0,3)#out1_amp3
Spower= SpecialParameters.Reflecto_power('rf4_power', ziUhf, 1,7)#out1_amp4

G1freq= SpecialParameters.Reflecto_frequency('G1_frequency', ziUhf, 0)
Sfreq= SpecialParameters.Reflecto_frequency('Source_frequency', ziUhf, 1)
rf3freq= SpecialParameters.Reflecto_frequency('rf3frequency', ziUhf, 2)
rf4freq= SpecialParameters.Reflecto_frequency('rf4frequency', ziUhf, 3)

rf1freq= SpecialParameters.Reflecto_frequency('rf3frequency', ziUhf, 0)
rf2freq= SpecialParameters.Reflecto_frequency('rf4frequency', ziUhf, 1)




   


#define phase 0 for all parameters
#VT1S = SpecialParameters.ParameterPhase0both(ziUhf, VT2, phase,phaseT2)
# VT1S = SpecialParameters.ParameterPhase0(ziUhf, VT1, 1)
# VT2S = SpecialParameters.ParameterPhase0(ziUhf, VT2, 1)
# VB1S = SpecialParameters.ParameterPhase0(ziUhf, VB, 1)
# VB2S = SpecialParameters.ParameterPhase0(ziUhf, VB2, 1)

biasS = SpecialParameters.ParameterPhase0(ziUhf, bias, 5)

# rf1freqS= SpecialParameters.ParameterPhase0(ziUhf,rf1freq,  1)
# rf2freqS= SpecialParameters.ParameterPhase0(ziUhf,rf2freq,  5)

# rf3freqS= SpecialParameters.ParameterPhase0(ziUhf,rf1freq,  1)
# rf4freqS= SpecialParameters.ParameterPhase0(ziUhf,rf2freq,  5)

# rfpowerS= SpecialParameters.ParameterPhase0(ziUhf, rfpower, 1)
# rfpower2S= SpecialParameters.ParameterPhase0(ziUhf, rfpower2, 1)
#mwpowerS= SpecialParameters.ParameterPhase0(ziUhf, mwgen.power, 5)
#mwfrequencyS= SpecialParameters.ParameterPhase0(ziUhf, mwgen.frequency, 1)

rfpower=ziUhf.daq.getDouble('/dev2226/sigouts/0/amplitudes/3')

tpulseS= SpecialParameters.ParameterPhase0(ziUhf,tpulse, 1)
twaitS = SpecialParameters.ParameterPhase0(ziUhf,twait, 1)
t_triggerS=SpecialParameters.ParameterPhase0(ziUhf,t_trigger, 1)

ampliAWGS=SpecialParameters.ParameterPhase0(ziUhf,ampliAWG, 1)
ampliAWGS_T3=SpecialParameters.ParameterPhase0(ziUhf,ampliAWG_T3, 1)
print('Till here OK')
def changeAread(filename,A):
    lines=open(filename).read().splitlines()
    with open(filename,'r+') as f:
         f.truncate(0)
         lines[16]='const amplitude11_scaled=' +str(A)+';'
         for i in range(len(lines)):
    
             f.write(lines[i]+'\n')
             
             #f.writelines()
    f.close()
class Read_level(qc.Parameter):
    def __init__(self, uhf ,name='read_amplitude'):
        super().__init__(name, label='read_ampli', vals=qc.validators.Numbers(-2, 2),#amplitude of read is fraction of total amplitude
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
        ziUhf.daq.setInt('/dev2226/sigouts/0/enables/5', 1)
        ziUhf.daq.setInt('/dev2226/demods/0/trigger', 33554432)
        
Readlevel=Read_level(ziUhf)
#CAREFUL!!!!!! Dac.dacx is in Volt
#define gates and rampgate in mV HERE!

#dac,VT1,VT2,VT3,VB1,VB2,VB3,bias,Vmet,VBG,testgate9,testgate10  = revitalizedac()

# slopeG3G2=-0.20199999999999816
# slopeG4G2=-0.022000000000025464
# slopeG3G5=-0.013999999999987267
# slopeG4G5=-0.21200000000003455

# VG4comp=  SpecialParameters.CompensateG4_double(VG4,VG5,VG2,slopeG4G5,slopeG4G2)
# VG3comp=  SpecialParameters.CompensateG3_double(VG3,VG5,VG2,slopeG3G5,slopeG3G2)


slopeG3G2=-0.25
slopeG4G2=-0.022000000000025464
slopeG3G5=-0.013999999999987267
slopeG4G5=-0.25

VG4comp=  SpecialParameters.CompensateG4(VG4,VG5,slopeG4G5)
VG3comp=  SpecialParameters.CompensateG3(VG3,VG2,slopeG3G2)




def saveSequence(SequenceFileName):     # it saves the sequence of the Zurich's sequencer in the same folder of the measurement

    import os
    import datetime
    
    now=datetime.datetime.now()
    dayFolder=datetime.date.isoformat(now)
    folderPath=os.path.join(r's:\132-PHELIQS\110.05-LATEQS\110.05.01-QuantumSilicon\Tritonito\data', dayFolder)
    culo=os.listdir(folderPath)
    
    numeri=[]
    for i in range(len(culo)): 
        if culo[i][0] == '#':
            numeri.append(culo[i][1:4])
    
    last=max(numeri)
    
    for i in range(len(culo)): 
        if culo[i].startswith('#'+last) and culo[i][-4:] != '.png':
               lastmeasureFolder = culo[i]
    
    sequenceName = SequenceFileName
    sequencePath = sequenceName + '.seqc'
    
    sequence=open(os.path.join(r'C:\Users\g-gre-gre050402\Documents\Zurich Instruments\LabOne\WebServer\awg\src', sequencePath)).read().splitlines()
    
    folderPathData=os.path.join(folderPath, lastmeasureFolder)
    sequenceLabel = 'AWGsequence.txt'
    filenameTOT = os.path.join(folderPathData, sequenceLabel)
    
    print(sequence, file=open(filenameTOT, 'w+'))


def generateEpsilonAxis(startPoint,endPoint,numPts):
	
	#1D scan with combined parameters
	detuningX = []
	detuningY = []
	
	print('Start point x1 = {0}, y1 = {1}'.format(startPoint[0],startPoint[1]))
	print('End point x2 = {0}, y2 = {1}'.format(endPoint[0],endPoint[1]))	    
	
	a = (endPoint[1] - startPoint[1]) / (endPoint[0] - startPoint[0])
	b = startPoint[1] - a*startPoint[0]
	
	for x in np.linspace(startPoint[0], endPoint[0], num=numPts):
	    detuningX.append(x)
	    detuningY.append(a*x+b)
	
	sweepValues = np.transpose(np.array([detuningX,detuningY]))
	
	return sweepValues



def phaseZero():  
    #if both on and activated
    if (ziUhf.daq.getInt('/dev2226/demods/5/enable') == 1 & ziUhf.daq.getInt('/dev2226/sigouts/1/on') == 1 &ziUhf.daq.getInt('/dev2226/demods/1/enable') == 1 & ziUhf.daq.getInt('/dev2226/sigouts/0/on') == 1):
       for j in range(0,2):  
        tc = ziUhf.daq.getDouble('/dev2226/demods/5/timeconstant')
        time.sleep(5*tc)
        meanphase = 0
        numAverages = 10
        for i in range(numAverages):
            meanphase += np.rad2deg(ph1.get())/numAverages
            
        ziUhf.daq.setDouble('/dev2226/demods/5/phaseshift', ziUhf.daq.getDouble('/dev2226/demods/5/phaseshift') + meanphase)
        time.sleep(5*tc)
        
        tc = ziUhf.daq.getDouble('/dev2226/demods/1/timeconstant')
        time.sleep(5*tc)
        meanphase = 0
        numAverages = 10
        for i in range(numAverages):
            meanphase += np.rad2deg(ph1.get())/numAverages
            
        ziUhf.daq.setDouble('/dev2226/demods/1/phaseshift', ziUhf.daq.getDouble('/dev2226/demods/1/phaseshift') + meanphase)
        time.sleep(5*tc)  
        
    elif ziUhf.daq.getInt('/dev2226/demods/5/enable') == 1 & ziUhf.daq.getInt('/dev2226/sigouts/1/on') == 1:
       for j in range(0,2):  
        tc = ziUhf.daq.getDouble('/dev2226/demods/5/timeconstant')
        time.sleep(5*tc)
        meanphase = 0
        numAverages = 10
        for i in range(numAverages):
            meanphase += np.rad2deg(phaseB3.get())/numAverages
            
        ziUhf.daq.setDouble('/dev2226/demods/5/phaseshift', ziUhf.daq.getDouble('/dev2226/demods/5/phaseshift') + meanphase)
        time.sleep(5*tc)
        
    elif ziUhf.daq.getDouble('/dev2226/demods/1/enable') == 1:
       for j in range(0,2): 
        tc = ziUhf.daq.getDouble('/dev2226/demods/1/timeconstant')
        time.sleep(5*tc)
        meanphase = 0
        numAverages = 10
        for i in range(numAverages):
            meanphase += np.rad2deg(phase.get())/numAverages
            
        ziUhf.daq.setDouble('/dev2226/demods/1/phaseshift', ziUhf.daq.getDouble('/dev2226/demods/1/phaseshift') + meanphase)
        time.sleep(5*tc)  
        
    
        
    else:
        print("Select Demodulator 1 and/or 5")
        
        
def phaseZero_B3():  
    
   for j in range(0,2):  

    if ziUhf.daq.getInt('/dev2226/demods/5/enable') == 1 & ziUhf.daq.getInt('/dev2226/sigouts/0/on') == 1:
       for j in range(0,2):  
        tc = ziUhf.daq.getDouble('/dev2226/demods/5/timeconstant')
        time.sleep(5*tc)
        meanphase = 0
        numAverages = 10
        for i in range(numAverages):
            meanphase += np.rad2deg(phaseB3.get())/numAverages
            
        ziUhf.daq.setDouble('/dev2226/demods/5/phaseshift', ziUhf.daq.getDouble('/dev2226/demods/5/phaseshift') + meanphase)
        time.sleep(5*tc)
        
def phaseZero_T2():  

    
   for j in range(0,2):  

    if ziUhf.daq.getInt('/dev2226/demods/1/enable') == 1 & ziUhf.daq.getInt('/dev2226/sigouts/1/on') == 1:
       for j in range(0,2):  
        tc = ziUhf.daq.getDouble('/dev2226/demods/5/timeconstant')
        time.sleep(5*tc)
        meanphase = 0
        numAverages = 10
        for i in range(numAverages):
            meanphase += np.rad2deg(phaseB3.get())/numAverages
            
        ziUhf.daq.setDouble('/dev2226/demods/5/phaseshift', ziUhf.daq.getDouble('/dev2226/demods/5/phaseshift') + meanphase)
        time.sleep(5*tc)

def videomode_off():
    
    ziUhf.daq.setDouble('/dev2226/demods/5/rate', 2000)
    ziUhf.daq.setDouble('/dev2226/demods/5/timeconstant', 0.017777)
#    h=ziUhf.daq.awgModule()
#    
#    ziUhf.daq.set('/module/c0p1t10p1cf0/awgModule/awg/enable', 0)
    


    
def dacnames():
#    dacname=loop.sweep_values.name
#    if dacname=='T1Phase0'or dacname=='T1' :
#        Namedacvalues='-T2_%.2fV-B1_%.4fV-B2_%.4fV-Vbias_%.3fV' % (dac.dac2(),dac.dac3(), dac.dac4(),dac.dac5())
#    elif dacname=='T2Phase0'or dacname=='T2' :
#        Namedacvalues='-T1_%.2fV-B1_%.4fV-B2_%.4fV-Vbias_%.3fV' % (dac.dac1(),dac.dac3(), dac.dac4(),dac.dac5())
#    elif dacname=='B1Phase0'or dacname=='B1' :
#        Namedacvalues='-T1_%.2fV-T2_%.4fV-B2_%.4fV-Vbias_%.3fV' % (dac.dac1(),dac.dac2(), dac.dac4(),dac.dac5())
#    elif dacname=='B2Phase0'or dacname=='B2':
#        Namedacvalues='-T1_%.2fV-T2_%.2fV-B1_%.4fV-Vbias_%.3fV' % (dac.dac1(),dac.dac2(), dac.dac3(),dac.dac5())
#    else:
#        Namedacvalues='-T1_%.2fV-T2_%.2fV-B1_%.3fV-B2_%.2fV' % (dac.dac1(),dac.dac2(), dac.dac3(),dac.dac4())
    Namedacvalues='-T1_%.3fV-T2_%.3fV-B1_%.3fV-B2_%.3fV-bias_%.6fV' % (dac.dac1(),dac.dac2(), dac.dac3(),dac.dac4(),dac.dac5())
    return str(Namedacvalues)




def removeBackground_B3(rangeMin=0, rangeMax=-1):
    for i in range(len(data.phiB3)):
        data.phiB3[i] = data.phiB3[i] - data.phiB3[i][rangeMin:rangeMax].mean() 


def removeMeanFromEachLine(rangeMin=0, rangeMax=-1):
    for i in range(len(loadedData.phi)):
        loadedData.phi[i] = loadedData.phi[i] - loadedData.phi[i][rangeMin:rangeMax].mean() 
        
def removeMeanFromEachLine_T3(rangeMin=0, rangeMax=-1):
    for i in range(len(loadedData.phiB3)):
        loadedData.phiB3[i] = loadedData.phiB3[i] - loadedData.phiB3[i][rangeMin:rangeMax].mean() 
#########################################
# dacs labels legend:
#    dac1=T1
#    dac2=T2
#    dac3=T3        
#    dac4=B1
#    dac5=B2
#    dac6=B3        
#    dac7=Vds
#########################################



def run_seq(device_id, awg_sourcefile=None):
    """
    Connect to a Zurich Instruments UHF Lock-in Amplifier or UHFAWG, compile,
    upload and run an AWG sequence program.

    Requirements:

      UHFAWG or UHFLI with UHF-AWG Arbitrary Waveform Generator Option.

    Arguments:

      device_id (str): The ID of the device to run the example with. For
        example, `dev2006` or `uhf-dev2006`.

      awg_sourcefile (str, optional): Specify an AWG sequencer file to compile
        and upload. This file must exist in the AWG source sub-folder of your
        LabOne data directory (this location is provided by the
        awgModule/directory parameter). The source folder must not be included;
        specify the filename only with extension.

    Raises:

      Exception: AWG functionality is not available.

      RuntimeError: If the device is not "discoverable" from the API.

    See the "LabOne Programing Manual" for further help, available:
      - On Windows via the Start-Menu:
        Programs -> Zurich Instruments -> Documentation
      - On Linux in the LabOne .tar.gz archive in the "Documentation"
        sub-folder.
    """

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

    # Create a base instrument configuration: disable all outputs, demods and scopes.
    general_setting = [['/%s/demods/*/enable' % device, 0],
                       ['/%s/demods/*/trigger' % device, 0],
                       ['/%s/sigouts/*/enables/*' % device, 0],
                       ['/%s/scopes/*/enable' % device, 0]]
    if 'IA' in props['options']:
        general_setting.append(['/%s/imps/*/enable' % device, 0])
    daq.set(general_setting)
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
#    timeout = 20
    timeout = 100
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
            print("Compiler warning: " +awgModule.get('awgModule/compiler/statusstring')['compiler']['statusstring'][0])
        # Wait for the waveform upload to finish
        time.sleep(0.2)
        i = 0
        while awgModule.get('awgModule/progress')['progress'][0] < 1.0:
            print("{} progress: {}".format(i, awgModule.get('awgModule/progress')['progress'][0]))
            time.sleep(0.5)
            i += 1

    print('Success. Enabling the AWG.')
    daq.setInt('/' + device + '/awgs/0/enable', 1)
    time.sleep(1)
    


#ziUhf.daq.setInt('/dev2226/demods/*/enable', 0)
#ziUhf.daq.setInt('/dev2226/awgs/0/enable', 0)

 


folder=r'C:\Users\g-gre-gre050402\Documents\Zurich Instruments\LabOne\WebServer\awg\src'
#name="\\negativepulse_fixpulsevarywait_triggered.seqc"
#name='\pulse_sequence.txt'
#name='\\balancedpulsemovewindow.seqc'
name="\\pulse_symm.seqc"
namefile=folder+name

def changetpulse(filename,t):
    lines=open(filename).read().splitlines()
    with open(filename,'r+') as f:
         f.truncate(0)
         lines[16]='const pulse_sec =' +str(t)+';'
         for i in range(len(lines)):
    
             f.write(lines[i]+'\n')
             
             #f.writelines()
    f.close()
    
def pulsetime(t):
    changetpulse(namefile,t)
    run_seq('dev2226','Morello_Tritonito.seqc')
    ziUhf.daq.setInt('/dev2226/sigouts/1/enables/3', 1)
    ziUhf.daq.setInt('/dev2226/demods/1/enable', 1)
    ziUhf.daq.setInt('/dev2226/sigouts/0/on', 1)
   
#full path for the file
#for runseq it is sufficient just filename   
def changetramp(filename,tpulse,tramp,twait):
    lines=open(filename).read().splitlines()
    with open(filename,'r+') as f:
         f.truncate(0)
         lines[8]='const pulse_sec =' +str(tpulse)+';'
         lines[14]='const wait_sec =' +str(twait)+';'
         lines[18]='const ramp_sec =' +str(tramp)+';'
         for i in range(len(lines)):
    
             f.write(lines[i]+'\n')
             
             #f.writelines()
    f.close()  
 
    
class Span(qc.Parameter):
    
    def __init__(self, x, y, a, b, name='span'):
        super().__init__(name=name,
                         label='span',
                         unit=x.unit)
        #y = ax + b     <==>    B = a*f + b
        self._x = x
        self._y = y
        self._a = a
        self._b = b
        
    def set(self, value):
        self._x.set(value + (self._y.get() - self._b)/self._a)    



    
  #calculate pek position for negative amplitude
  #factor 1000/88 to convert awg amplitude on sample (in mV)
#tr=tramp
#tp=tpulse
#tw=twait 
  
#calibrated for internalAWG amplitude=100mV*ampliAWG()
def peakpos(ampliAWG,VB2nopulse,tr,tp,tw):
    A=ampliAWG/88*1000
    
    DC_offset=1/(tp+tw+tr)*(-tr/2-tp)*A
    pulsepos=VB2nopulse+(DC_offset)
    return pulsepos   

def continuous_acquisition():
    ziUhf.daq.setInt('/dev2226/demods/0/trigger', 0) # demodulator trigger off
    ziUhf.daq.setDouble('/dev2226/demods/0/timeconstant', 10e-3)
    ziUhf.daq.setInt('/dev2226/demods/0/order', 3)
    ziUhf.daq.setDouble('/dev2226/demods/0/rate', 2e3)
    ziUhf.daq.setInt('/dev2226/awgs/0/enable', 0)
    ziUhf.daq.setInt('/dev2226/sigouts/0/enables/4', 1)
    
def continuous_acquisition_ch2():
    ziUhf.daq.setInt('/dev2226/demods/1/trigger', 0) # demodulator trigger off
    ziUhf.daq.setDouble('/dev2226/demods/1/timeconstant', 10e-3)
    ziUhf.daq.setInt('/dev2226/demods/1/order', 3)
    ziUhf.daq.setDouble('/dev2226/demods/1/rate', 2e3)
    ziUhf.daq.setInt('/dev2226/awgs/0/enable',0)
    ziUhf.daq.setInt('/dev2226/sigouts/0/enables/5', 1)
    
def continuous_acquisition_B3():
    ziUhf.daq.setInt('/dev2226/demods/5/trigger', 0) # demodulator trigger off
    ziUhf.daq.setDouble('/dev2226/demods/5/timeconstant', 0.1)
    ziUhf.daq.setInt('/dev2226/demods/5/order', 3)
    ziUhf.daq.setDouble('/dev2226/demods/5/rate', 2e3)    
    
    
def trigger_mode():
    ziUhf.daq.setInt('/dev2226/demods/0/trigger', 33554432) # demodulator trigger set on AWGtrigger2 High
    ziUhf.daq.setDouble('/dev2226/demods/0/rate', 200e3)
    ziUhf.daq.setInt('/dev2226/demods/0/order', 1)
    ziUhf.daq.setDouble('/dev2226/demods/0/timeconstant',5e-6)
    ziUhf.daq.sync()
    
def trigger_mode_ch2():
    ziUhf.daq.setInt('/dev2226/demods/1/trigger', 33554432) # demodulator trigger set on AWGtrigger2 High
    ziUhf.daq.setDouble('/dev2226/demods/1/rate', 200e3)
    ziUhf.daq.setInt('/dev2226/demods/1/order', 1)
    ziUhf.daq.setDouble('/dev2226/demods/1/timeconstant',5e-6)
    ziUhf.daq.sync()
    

def trigger_mode_B3():
    ziUhf.daq.setInt('/dev2226/demods/5/trigger', 33554432) # demodulator trigger set on AWGtrigger2 High
    ziUhf.daq.setDouble('/dev2226/demods/5/rate', 200e3)
    ziUhf.daq.setInt('/dev2226/demods/5/order', 1)
    ziUhf.daq.setDouble('/dev2226/demods/5/timeconstant', 5e-6)
    ziUhf.daq.sync()    
    
    
def phaseZerotrig():
    continuous_acquisition()    
    ziUhf.daq.setInt('/dev2226/awgs/0/enable', 0)    
    phaseZero()
    ziUhf.daq.setInt('/dev2226/awgs/0/enable', 1)
    trigger_mode()       
   
    
    
def define_grid_settings(points,acquisition_duration,repetitions):    
 trigger_setting = [['dataAcquisitionModule/triggernode', '/dev2226/demods/1/sample.TrigAWGTrig3'],  # trigger node is AWG trigger number 3 
#                   ['dataAcquisitionModule/type', 2],      
                   ['dataAcquisitionModule/type', 6],                                          # this setting is related to the AWG trigger
                   ['dataAcquisitionModule/edge', 1],                                               # trigger on the positive edge. 1 = positive, 2=negative
                   ['dataAcquisitionModule/count', 1],                                              # number of trigger events to count
                   ['dataAcquisitionModule/holdoff/time', 0],                                       # hold off time
                   ['dataAcquisitionModule/holdoff/count', 0],                                      # hold off count
                   ['dataAcquisitionModule/delay', 0], #0                                       # trigger delay (s)
                   ['dataAcquisitionModule/endless', 0]]                                            # endless disabled = 0


 grid_setting =    [['dataAcquisitionModule/grid/mode', 2],                          # mode. 2 = Linear interpolation 
                   ['dataAcquisitionModule/grid/cols', points],                     # number of points in the acquisition window
                   ['dataAcquisitionModule/duration', acquisition_duration],        # length of time to record (s)
                   ['dataAcquisitionModule/grid/rows', 1],                          # rows
                   ['dataAcquisitionModule/grid/direction', 0],                     # scan direction. 0 = forward
                   ['dataAcquisitionModule/grid/repetitions', repetitions],         # number of repetitions for the averaging
                   ['dataAcquisitionModule/awgcontrol', 1],                         # set the AWG control
                   ['dataAcquisitionModule/save/fileformat', 1]]                    # 1 = CSV format 

#############
# slopeG3G2= -0.22933333333336728
# slopeG4G2=-0.026666666666642413
# VG3comp=  SpecialParameters.CompensateG3(VG3,VG2,slopeG3G2)
# VG4comp=  SpecialParameters.CompensateG4(VG4,VG2,slopeG4G2)



def sensor_on_interdot(initVT2,finalVT2,points,showplot):
    VG4(initVT2)
    ph1()
    time.sleep(0.1)
    ph1()
    a,dataid,c=sweep1D(VG4, initVT2,finalVT2,points,0.01,ph1)
    # a,dataid,c=sweep1D(VG4,-1093,-1094.5,401,0.005,ph1)
    now=datetime.datetime.now()
    dayFolder= datetime.date.isoformat(now)
    try:
        os.makedirs(folder2+'\\'+dayFolder)
    except IOError:
        donothing=1

    folder=r'S:\132-PHELIQS\132.05-LATEQS\132.05.01-QuantumSilicon\Tritonito\2021\Feb2021_6G22_2_die103\\data'
    name=str(dataid)+'_G4scan_calibrate_cs'
    xlabel='$V_{G4}$(mV)'
    ylabel='$\phi_{G1}$(deg)'
    data_set,data_get,parameters_name=Extract_data(a)
    if showplot==1:
     # plot_by_id(b)
     # plt.close()
     plot_savetxt(data_set,xlabel,data_get,ylabel,parameters_name,folder+'\\'+dayFolder,name)


    datasmooth=scipy.signal.savgol_filter(np.ravel(data_get[0]),11, 3)
    phimin=np.min(datasmooth)
    phimax=np.max(datasmooth)
    argmin=np.argmin(datasmooth)
    kmin=0
    kmax=0
    philim=phimin+(phimax-phimin)/2
    sigmaphi=0.05
    for k in range(0,len(data_set)):
        if ((data_get[0][k]>=(philim-sigmaphi) and data_get[0][k]<=(philim+sigmaphi)) and kmax==0):
            kmax=k
        
        #typicalFWHM is <1.5mVdef VT2onmin(initVB1,finalVB1,points,showplot):
   
    VG4(data_set[kmax])
    print('minpeak_VG4='+str(VG4()))   

    # kmin_init=kmin

def interdotfit_chargesensor(x,*p):
     T=0.44
     return( p[2]+p[1]*(np.tanh(x*p[0]/(2*kb*T))) ) 
 
    
def sensor_on_interdot_sweepG4comp_phD(initVT2,finalVT2,points,showplot):
    VG4comp(initVT2)
    ph1()
    time.sleep(0.1)
    ph1()
    a,dataid,c=sweep1D(VG4comp, initVT2,finalVT2,points,0.01,ph1)
    # a,dataid,c=sweep1D(VG4,-1093,-1094.5,401,0.005,ph1)
    now=datetime.datetime.now()
    dayFolder= datetime.date.isoformat(now)
    try:
        os.makedirs(folder2+'\\'+dayFolder)
    except IOError:
        donothing=1

    folder=r'S:\132-PHELIQS\132.05-LATEQS\132.05.01-QuantumSilicon\Tritonito\2021\Feb2021_6G22_2_die103\\data'
    name=str(dataid)+'_G4scan_calibrate_cs'
    xlabel='$V_{G4comp}$(mV)'
    ylabel='$\phi_{D}$(rad)'
    data_set,data_get,parameters_name=Extract_data(a)
    if showplot==1:
     # plot_by_id(b)
     # plt.close()
     plot_savetxt(data_set,xlabel,data_get,ylabel,parameters_name,folder+'\\'+dayFolder,name)


    datasmooth=scipy.signal.savgol_filter(np.ravel(data_get[0]),11, 3)
    phimin=np.min(datasmooth)
    phimax=np.max(datasmooth)
    argmin=np.argmin(datasmooth)
    kmin=0
    kmax=0
    philim=phimin+(phimax-phimin)/2
    sigmaphi=0.05
    for k in range(0,len(data_set)):
        if ((data_get[0][k]>=(philim-sigmaphi) and data_get[0][k]<=(philim+sigmaphi)) and kmax==0):
            kmax=k
        
        #typicalFWHM is <1.5mVdef VT2onmin(initVB1,finalVB1,points,showplot):
   
    VG4comp(data_set[kmax])
    print('minpeak_VG4='+str(VG4()))    
    
    
def sensor_on_interdot_sweepG4comp_phS(initVT2,finalVT2,points,showplot):
    VG4comp(initVT2)
    ph1()
    time.sleep(0.1)
    ph1()
    a,dataid,c=sweep1D(VG4comp, initVT2,finalVT2,points,0.01,ph2)
    # a,dataid,c=sweep1D(VG4,-1093,-1094.5,401,0.005,ph1)
    now=datetime.datetime.now()
    dayFolder= datetime.date.isoformat(now)
    try:
        os.makedirs(folder2+'\\'+dayFolder)
    except IOError:
        donothing=1

    folder=r'S:\132-PHELIQS\132.05-LATEQS\132.05.01-QuantumSilicon\Tritonito\2021\Feb2021_6G22_2_die103\\data'
    name=str(dataid)+'_G4scan_calibrate_cs'
    xlabel='$V_{G4comp}$(mV)'
    ylabel='$\phi_{S}$(deg)'
    data_set,data_get,parameters_name=Extract_data(a)
    if showplot==1:
     # plot_by_id(b)
     # plt.close()
     plot_savetxt(data_set,xlabel,data_get,ylabel,parameters_name,folder+'\\'+dayFolder,name)


    datasmooth=scipy.signal.savgol_filter(np.ravel(data_get[0]),11, 3)
    phimin=np.min(datasmooth)
    phimax=np.max(datasmooth)
    argmin=np.argmin(datasmooth)
    kmin=0
    kmax=0
    philim=phimin+(phimax-phimin)/2
    sigmaphi=0.05
    for k in range(0,len(data_set)):
        if ((data_get[0][k]>=(philim-sigmaphi) and data_get[0][k]<=(philim+sigmaphi)) and kmax==0):
            kmax=k
        
        #typicalFWHM is <1.5mVdef VT2onmin(initVB1,finalVB1,points,showplot):
   
    VG4comp(data_set[kmax])
    print('minpeak_VG4='+str(VG4()))  





     
def sensor_on_interdot_sweepG4_phS(initVT2,finalVT2,points,showplot):
    VG4comp(initVT2)
    ph1()
    time.sleep(0.1)
    ph1()
    a,dataid,c=sweep1D(VG4, initVT2,finalVT2,points,0.01,ph2)
    # a,dataid,c=sweep1D(VG4,-1093,-1094.5,401,0.005,ph1)
    now=datetime.datetime.now()
    dayFolder= datetime.date.isoformat(now)
    try:
        os.makedirs(folder2+'\\'+dayFolder)
    except IOError:
        donothing=1

    folder=r'S:\132-PHELIQS\132.05-LATEQS\132.05.01-QuantumSilicon\Tritonito\2021\Feb2021_6G22_2_die103\\data'
    name=str(dataid)+'_G4scan_calibrate_cs'
    xlabel='$V_{G4}$(mV)'
    ylabel='$\phi_{S}$(deg)'
    data_set,data_get,parameters_name=Extract_data(a)
    if showplot==1:
     # plot_by_id(b)
     # plt.close()
     plot_savetxt(data_set,xlabel,data_get,ylabel,parameters_name,folder+'\\'+dayFolder,name)


    datasmooth=scipy.signal.savgol_filter(np.ravel(data_get[0]),11, 3)
    phimin=np.min(datasmooth)
    phimax=np.max(datasmooth)
    argmin=np.argmin(datasmooth)
    kmin=0
    kmax=0
    philim=phimin+(phimax-phimin)/2
    sigmaphi=0.05
    for k in range(0,len(data_set)):
        if ((data_get[0][k]>=(philim-sigmaphi) and data_get[0][k]<=(philim+sigmaphi)) and kmax==0):
            kmax=k
        
        #typicalFWHM is <1.5mVdef VT2onmin(initVB1,finalVB1,points,showplot):
   
    VG4(data_set[kmax])
    print('minpeak_VG4='+str(VG4()))    
    
def sensor_on_interdot_sweepG4_phD(initVT2,finalVT2,points,showplot):
    VG4comp(initVT2)
    ph1()
    time.sleep(0.1)
    ph1()
    a,dataid,c=sweep1D(VG4, initVT2,finalVT2,points,0.01,ph1)
    # a,dataid,c=sweep1D(VG4,-1093,-1094.5,401,0.005,ph1)
    now=datetime.datetime.now()
    dayFolder= datetime.date.isoformat(now)
    try:
        os.makedirs(folder2+'\\'+dayFolder)
    except IOError:
        donothing=1

    folder=r'S:\132-PHELIQS\132.05-LATEQS\132.05.01-QuantumSilicon\Tritonito\2021\Feb2021_6G22_2_die103\\data'
    name=str(dataid)+'_G4scan_calibrate_cs'
    xlabel='$V_{G4}$(mV)'
    ylabel='$\phi_{D}$(deg)'
    data_set,data_get,parameters_name=Extract_data(a)
    if showplot==1:
     # plot_by_id(b)
     # plt.close()
     plot_savetxt(data_set,xlabel,data_get,ylabel,parameters_name,folder+'\\'+dayFolder,name)


    datasmooth=scipy.signal.savgol_filter(np.ravel(data_get[0]),11, 3)
    phimin=np.min(datasmooth)
    phimax=np.max(datasmooth)
    argmin=np.argmin(datasmooth)
    kmin=0
    kmax=0
    philim=phimin+(phimax-phimin)/2
    sigmaphi=(phimax-phimin)/points*4
    for k in range(0,len(data_set)):
        if ((data_get[0][k]>=(philim-sigmaphi) and data_get[0][k]<=(philim+sigmaphi)) and kmax==0):
            kmax=k
        
        #typicalFWHM is <1.5mVdef VT2onmin(initVB1,finalVB1,points,showplot):
   
    VG4(data_set[kmax])
    print('minpeak_VG4='+str(VG4()))     
    
    
    
    
def sensor_on_interdot_sweepG3comp(initVT2,finalVT2,points,showplot):
    VG3comp(initVT2)
    ph1()
    time.sleep(0.1)
    ph1()
    a,dataid,c=sweep1D(VG3comp, initVT2,finalVT2,points,0.01,ph1)
    # a,dataid,c=sweep1D(VG4,-1093,-1094.5,401,0.005,ph1)
    now=datetime.datetime.now()
    dayFolder= datetime.date.isoformat(now)
    try:
        os.makedirs(folder2+'\\'+dayFolder)
    except IOError:
        donothing=1

    folder=r'S:\132-PHELIQS\132.05-LATEQS\132.05.01-QuantumSilicon\Tritonito\2021\Feb2021_6G22_2_die103\\data'
    name=str(dataid)+'_G3scan_calibrate_cs'
    xlabel='$V_{G3comp}$(mV)'
    ylabel='$\phi_{G1}$(deg)'
    data_set,data_get,parameters_name=Extract_data(a)
    if showplot==1:
     # plot_by_id(b)
     # plt.close()
     plot_savetxt(data_set,xlabel,data_get,ylabel,parameters_name,folder+'\\'+dayFolder,name)


    datasmooth=scipy.signal.savgol_filter(np.ravel(data_get[0]),11, 3)
    phimin=np.min(datasmooth)
    phimax=np.max(datasmooth)
    argmin=np.argmin(datasmooth)
    kmin=0
    kmax=0
    philim=phimin+(phimax-phimin)/2
    sigmaphi=0.05
    for k in range(0,len(data_set)):
        if ((data_get[0][k]>=(philim-sigmaphi) and data_get[0][k]<=(philim+sigmaphi)) and kmax==0):
            kmax=k
        
        #typicalFWHM is <1.5mVdef VT2onmin(initVB1,finalVB1,points,showplot):
   
    VG3comp(data_set[kmax])
    print('minpeak_VG3='+str(VG3()))        
 
    
 
def VG2onrightside(initVT2,finalVT2,points,showplot):
    a,dataid,c=sweep1D(VG2, initVT2,finalVT2,points,0.01,ph1)
    now=datetime.datetime.now()
    dayFolder= datetime.date.isoformat(now)
    try:
        os.makedirs(folder2+'\\'+dayFolder)
    except IOError:
        donothing=1

    folder=r'S:\132-PHELIQS\132.05-LATEQS\132.05.01-QuantumSilicon\Tritonito\2021\Feb2021_6G22_2_die103\\data'
    name=str(dataid)+'_G2scan_calibrate_cs'
    xlabel='$V_{G2}$(mV)'
    ylabel='$\phi_{G1}$(deg)'
    data_set,data_get,parameters_name=Extract_data(a)
    if showplot==1:
     # plot_by_id(b)
     # plt.close()
     plot_savetxt(data_set,xlabel,data_get,ylabel,parameters_name,folder+'\\'+dayFolder,name)


    datasmooth=scipy.signal.savgol_filter(np.ravel(data_get[0]),11, 3)
    phimin=np.min(datasmooth)
    phimax=np.max(datasmooth)
    argmin=np.argmin(datasmooth)
    kmin=0
    kmax=0
    
    for k in range(argmin,len(data_set)):
        if data_get[0][argmin+k]>(phimin+(phimax-phimin)/2) and kmax==0:
            kmax=k
        
        #typicalFWHM is <1.5mVdef VT2onmin(initVB1,finalVB1,points,showplot):
   
    VG2(data_set[argmin+kmax][0])
    print('minpeak_VG2='+str(VG2()))   

def VG2onleftside(initVT2,finalVT2,points,showplot):
    a,dataid,c=sweep1D(VG2, initVT2,finalVT2,points,0.01,ph1)
    now=datetime.datetime.now()
    dayFolder= datetime.date.isoformat(now)
    try:
        os.makedirs(folder2+'\\'+dayFolder)
    except IOError:
        donothing=1

    folder=r'S:\132-PHELIQS\132.05-LATEQS\132.05.01-QuantumSilicon\Tritonito\2021\Feb2021_6G22_2_die103\\data'
    name=str(dataid)+'G2scan_calibrate_cs'
    xlabel='$V_{G2}$(mV)'
    ylabel='$\phi_{G1}$(deg)'
    data_set,data_get,parameters_name=Extract_data(a)
    if showplot==1:
     # plot_by_id(b)
     # plt.close()
     plot_savetxt(data_set,xlabel,data_get,ylabel,parameters_name,folder+'\\'+dayFolder,name)


    datasmooth=scipy.signal.savgol_filter(np.ravel(data_get[0]),11, 3)
    phimin=np.min(datasmooth)
    phimax=np.max(datasmooth)
    argmin=np.argmin(datasmooth)
    kmin=0
    kmax=0
    
    for k in range(argmin,len(data_set)):
        if data_get[0][argmin-k]>(phimin+(phimax-phimin)/2) and kmax==0:
            kmax=k
        
        #typicalFWHM is <1.5mVdef VT2onmin(initVB1,finalVB1,points,showplot):
   
    VG2(data_set[argmin-kmax][0])
    print('minpeak_VG2='+str(VG2()))  
    

        
    
def VG1onmin(initVT2,finalVT2,points,showplot):
    rampVG1(initVT2)
    time.sleep(0.1)
    a,dataid,c=sweep1D(rampVG1, initVT2,finalVT2,points,0.01,ph2)
    now=datetime.datetime.now()
    dayFolder= datetime.date.isoformat(now)
    try:
        os.makedirs(folder2+'\\'+dayFolder)
    except IOError:
        donothing=1

    folder=r'S:\132-PHELIQS\132.05-LATEQS\132.05.01-QuantumSilicon\Tritonito\2021\Feb2021_6G22_2_die103\\data'
    name=str(dataid)+'_G1scan_calibrate_cs'
    xlabel='$V_{G1}$(mV)'
    ylabel='$\phi_{G1}$(deg)'
    data_set,data_get,parameters_name=Extract_data(a)
    if showplot==1:
     # plot_by_id(b)
     # plt.close()
     plot_savetxt(data_set,xlabel,data_get,ylabel,parameters_name,folder+'\\'+dayFolder,name)


    datasmooth=scipy.signal.savgol_filter(np.ravel(data_get[0]),11, 3)
    phimin=np.min(datasmooth)
    argmin=np.argmin(datasmooth)

   
    rampVG1(data_set[argmin])
    print('minpeak_VG1='+str(VG1()))

def VG2onmin(initVT2,finalVT2,points,showplot):
    rampVG2(initVT2)
    time.sleep(0.1)
    a,dataid,c=sweep1D(VG2, initVT2,finalVT2,points,0.01,ph2)
    now=datetime.datetime.now()
    dayFolder= datetime.date.isoformat(now)
    try:
        os.makedirs(folder2+'\\'+dayFolder)
    except IOError:
        donothing=1

    folder=r'S:\132-PHELIQS\132.05-LATEQS\132.05.01-QuantumSilicon\Tritonito\2021\Feb2021_6G22_2_die103\\data'
    name=str(dataid)+'_G2scan_calibrate_cs'
    xlabel='$V_{G2}$(mV)'
    ylabel='$\phi_{G1}$(deg)'
    data_set,data_get,parameters_name=Extract_data(a)
    if showplot==1:
     # plot_by_id(b)
     # plt.close()
     plot_savetxt(data_set,xlabel,data_get,ylabel,parameters_name,folder+'\\'+dayFolder,name)


    datasmooth=scipy.signal.savgol_filter(np.ravel(data_get[0]),11, 3)
    phimin=np.min(datasmooth)
    argmin=np.argmin(datasmooth)

   
    VG2(data_set[argmin])
    print('minpeak_VG2='+str(VG2()))  
    
       
    
def VG1onmin_phS(initVT2,finalVT2,points,showplot):
    VG1(initVT2)
    time.sleep(0.1)
    a,dataid,c=sweep1D(VG1, initVT2,finalVT2,points,0.01,ph2)
    now=datetime.datetime.now()
    dayFolder= datetime.date.isoformat(now)
    try:
        os.makedirs(folder2+'\\'+dayFolder)
    except IOError:
        donothing=1

    folder=r'S:\132-PHELIQS\132.05-LATEQS\132.05.01-QuantumSilicon\Tritonito\2021\Feb2021_6G22_2_die103\\data'
    name=str(dataid)+'_G1scan_calibrate_minphiS'
    xlabel='$V_{G1}$(mV)'
    ylabel='$\phi_{S}$(deg)'
    data_set,data_get,parameters_name=Extract_data(a)
    if showplot==1:
     # plot_by_id(b)
     # plt.close()
     plot_savetxt(data_set,xlabel,data_get,ylabel,parameters_name,folder+'\\'+dayFolder,name)


    datasmooth=scipy.signal.savgol_filter(np.ravel(data_get[0]),11, 3)
    phimin=np.min(datasmooth)
    argmin=np.argmin(datasmooth)

   
    VG1(data_set[argmin])
    print('minpeak_VG1='+str(VG1()))   
    
    
def VG2onmin_phS(initVT2,finalVT2,points,showplot):
    rampVG2(initVT2)
    time.sleep(0.1)
    a,dataid,c=sweep1D(VG2, initVT2,finalVT2,points,0.01,ph2)
    now=datetime.datetime.now()
    dayFolder= datetime.date.isoformat(now)
    try:
        os.makedirs(folder2+'\\'+dayFolder)
    except IOError:
        donothing=1

    folder=r'S:\132-PHELIQS\132.05-LATEQS\132.05.01-QuantumSilicon\Tritonito\2021\Feb2021_6G22_2_die103\\data'
    name=str(dataid)+'_G2scan_minphiS'
    xlabel='$V_{G2}$(mV)'
    ylabel='$\phi_{S}$(deg)'
    data_set,data_get,parameters_name=Extract_data(a)
    if showplot==1:
     # plot_by_id(b)
     # plt.close()
     plot_savetxt(data_set,xlabel,data_get,ylabel,parameters_name,folder+'\\'+dayFolder,name)


    datasmooth=scipy.signal.savgol_filter(np.ravel(data_get[0]),11, 3)
    phimin=np.min(datasmooth)
    argmin=np.argmin(datasmooth)

   
    VG2(data_set[argmin])
    print('minpeak_VG2='+str(VG2()))  
    
    
    
def VG4onmin_phD(initVT2,finalVT2,points,showplot):
    rampVG4(initVT2)
    time.sleep(0.1)
    a,dataid,c=sweep1D(VG4, initVT2,finalVT2,points,0.01,ph1)
    now=datetime.datetime.now()
    dayFolder= datetime.date.isoformat(now)
    try:
        os.makedirs(folder2+'\\'+dayFolder)
    except IOError:
        donothing=1

    folder=r'S:\132-PHELIQS\132.05-LATEQS\132.05.01-QuantumSilicon\Tritonito\2021\Feb2021_6G22_2_die103\\data'
    name=str(dataid)+'_G4scan_calibrate_cs'
    xlabel='$V_{G4}$(mV)'
    ylabel='$\phi_{D}$(deg)'
    data_set,data_get,parameters_name=Extract_data(a)
    if showplot==1:
     # plot_by_id(b)
     # plt.close()
     plot_savetxt(data_set,xlabel,data_get,ylabel,parameters_name,folder+'\\'+dayFolder,name)


    datasmooth=scipy.signal.savgol_filter(np.ravel(data_get[0]),11, 3)
    phimin=np.min(datasmooth)
    argmin=np.argmin(datasmooth)

   
    VG4(data_set[argmin])
    print('minpeak_VG4='+str(VG4()))  
    
def VG5onmin_phD(initVT2,finalVT2,points,showplot):
    rampVG5(initVT2)
    time.sleep(0.1)
    a,dataid,c=sweep1D(VG5, initVT2,finalVT2,points,0.02,ph1)
    now=datetime.datetime.now()
    dayFolder= datetime.date.isoformat(now)
    try:
        os.makedirs(folder2+'\\'+dayFolder)
    except IOError:
        donothing=1

    folder=r'S:\132-PHELIQS\132.05-LATEQS\132.05.01-QuantumSilicon\Tritonito\2021\Feb2021_6G22_2_die103\\data'
    name=str(dataid)+'_G5scan_calibrate_cs_D'
    xlabel='$V_{G5}$(mV)'
    ylabel='$\phi_{D}$(deg)'
    data_set,data_get,parameters_name=Extract_data(a)
    if showplot==1:
     # plot_by_id(b)
     # plt.close()
     plot_savetxt(data_set,xlabel,data_get,ylabel,parameters_name,folder+'\\'+dayFolder,name)


    datasmooth=scipy.signal.savgol_filter(np.ravel(data_get[0]),11, 3)
    phimin=np.min(datasmooth)
    argmin=np.argmin(datasmooth)

   
    VG5(data_set[argmin])
    print('minpeak_VG5='+str(VG5()))  
    
def VG6onmin_phD(initVT2,finalVT2,points,showplot):
    rampVG6(initVT2)
    time.sleep(0.1)
    a,dataid,c=sweep1D(VG6, initVT2,finalVT2,points,0.01,ph1)
    now=datetime.datetime.now()
    dayFolder= datetime.date.isoformat(now)
    try:
        os.makedirs(folder2+'\\'+dayFolder)
    except IOError:
        donothing=1

    folder=r'S:\132-PHELIQS\132.05-LATEQS\132.05.01-QuantumSilicon\Tritonito\2021\Feb2021_6G22_2_die103\\data'
    name=str(dataid)+'_G6scan_calibrate_cs_D'
    xlabel='$V_{G6}$(mV)'
    ylabel='$\phi_{D}$(deg)'
    data_set,data_get,parameters_name=Extract_data(a)
    if showplot==1:
     # plot_by_id(b)
     # plt.close()
     plot_savetxt(data_set,xlabel,data_get,ylabel,parameters_name,folder+'\\'+dayFolder,name)


    datasmooth=scipy.signal.savgol_filter(np.ravel(data_get[0]),11, 3)
    phimin=np.min(datasmooth)
    argmin=np.argmin(datasmooth)

   
    VG6(data_set[argmin])
    print('minpeak_VG6='+str(VG6()))  
    
    
def VG6onmin(initVT2,finalVT2,points,showplot):
    rampVG6(initVT2)
    time.sleep(0.1)
    a,dataid,c=sweep1D(rampVG6, initVT2,finalVT2,points,0.01,ph1)
    now=datetime.datetime.now()
    dayFolder= datetime.date.isoformat(now)
    try:
        os.makedirs(folder2+'\\'+dayFolder)
    except IOError:
        donothing=1

    folder=r'S:\132-PHELIQS\132.05-LATEQS\132.05.01-QuantumSilicon\Tritonito\2021\Feb2021_6G22_2_die103\\data'
    name=str(dataid)+'_G6scan_calibrate_cs_D'
    xlabel='$V_{G6}$(mV)'
    ylabel='$\phi_{D}$(deg)'
    data_set,data_get,parameters_name=Extract_data(a)
    if showplot==1:
     # plot_by_id(b)
     # plt.close()
     plot_savetxt(data_set,xlabel,data_get,ylabel,parameters_name,folder+'\\'+dayFolder,name)


    datasmooth=scipy.signal.savgol_filter(np.ravel(data_get[0]),11, 3)
    phimin=np.min(datasmooth)
    argmin=np.argmin(datasmooth)

   
    rampVG6(data_set[argmin])
    print('minpeak_VG6='+str(VG6()))      
    

def VG3comp_onmin(initVT2,finalVT2,points,showplot):
    rampVG3(initVT2)
    time.sleep(0.1)
    a,dataid,c=sweep1D(VG3comp, initVT2,finalVT2,points,0.01,ph1)
    now=datetime.datetime.now()
    dayFolder= datetime.date.isoformat(now)
    try:
        os.makedirs(folder2+'\\'+dayFolder)
    except IOError:
        donothing=1

    folder=r'S:\132-PHELIQS\132.05-LATEQS\132.05.01-QuantumSilicon\Tritonito\2021\Feb2021_6G22_2_die103\\data'
    name=str(dataid)+'_G3compscan_calibrate_cs'
    xlabel='$V_{G3}$(mV)'
    ylabel='$\phi_{G1}$(deg)'
    data_set,data_get,parameters_name=Extract_data(a)
    if showplot==1:
     # plot_by_id(b)
     # plt.close()
     plot_savetxt(data_set,xlabel,data_get,ylabel,parameters_name,folder+'\\'+dayFolder,name)


    datasmooth=scipy.signal.savgol_filter(np.ravel(data_get[0]),11, 3)
    phimin=np.min(datasmooth)
    argmin=np.argmin(datasmooth)

   
    VG3comp(data_set[argmin])
    print('minpeak_VG3comp='+str(VG3comp()))  
    
def VG4comp_onmin(initVT2,finalVT2,points,showplot):
    rampVG3(initVT2)
    time.sleep(0.1)
    a,dataid,c=sweep1D(VG4comp, initVT2,finalVT2,points,0.01,ph1)
    now=datetime.datetime.now()
    dayFolder= datetime.date.isoformat(now)
    try:
        os.makedirs(folder2+'\\'+dayFolder)
    except IOError:
        donothing=1

    folder=r'S:\132-PHELIQS\132.05-LATEQS\132.05.01-QuantumSilicon\Tritonito\2021\Feb2021_6G22_2_die103\\data'
    name=str(dataid)+'_G4compscan_calibrate_cs'
    xlabel='$V_{G4}$(mV)'
    ylabel='$\phi_{G1}$(deg)'
    data_set,data_get,parameters_name=Extract_data(a)
    if showplot==1:
     # plot_by_id(b)
     # plt.close()
     plot_savetxt(data_set,xlabel,data_get,ylabel,parameters_name,folder+'\\'+dayFolder,name)


    datasmooth=scipy.signal.savgol_filter(np.ravel(data_get[0]),11, 3)
    phimin=np.min(datasmooth)
    argmin=np.argmin(datasmooth)

   
    VG4comp(data_set[argmin])
    print('minpeak_VG4comp='+str(VG4comp())) 
    
    
def VG3onmin(initVT2,finalVT2,points,showplot):
    rampVG3(initVT2)
    time.sleep(0.1)
    a,dataid,c=sweep1D(VG3, initVT2,finalVT2,points,0.01,ph1)
    now=datetime.datetime.now()
    dayFolder= datetime.date.isoformat(now)
    try:
        os.makedirs(folder2+'\\'+dayFolder)
    except IOError:
        donothing=1

    folder=r'S:\132-PHELIQS\132.05-LATEQS\132.05.01-QuantumSilicon\Tritonito\2021\Feb2021_6G22_2_die103\\data'
    name=str(dataid)+'_G3scan_calibrate_cs'
    xlabel='$V_{G3}$(mV)'
    ylabel='$\phi_{G1}$(deg)'
    data_set,data_get,parameters_name=Extract_data(a)
    if showplot==1:
     # plot_by_id(b)
     # plt.close()
     plot_savetxt(data_set,xlabel,data_get,ylabel,parameters_name,folder+'\\'+dayFolder,name)


    datasmooth=scipy.signal.savgol_filter(np.ravel(data_get[0]),11, 3)
    phimin=np.min(datasmooth)
    argmin=np.argmin(datasmooth)

   
    VG3(data_set[argmin])
    print('minpeak_VG3='+str(VG3()))  
    
def VG3componmin(initVT2,finalVT2,points,showplot):
    VG3comp(initVT2)
    time.sleep(0.1)
    a,dataid,c=sweep1D(VG3comp, initVT2,finalVT2,points,0.01,ph1)
    now=datetime.datetime.now()
    dayFolder= datetime.date.isoformat(now)
    try:
        os.makedirs(folder2+'\\'+dayFolder)
    except IOError:
        donothing=1

    folder=r'S:\132-PHELIQS\132.05-LATEQS\132.05.01-QuantumSilicon\Tritonito\2021\Feb2021_6G22_2_die103\\data'
    name=str(dataid)+'_G3scan_calibrate_cs'
    xlabel='$Vc_{G3}$(mV)'
    ylabel='$\phi_{G1}$(deg)'
    data_set,data_get,parameters_name=Extract_data(a)
    if showplot==1:
     # plot_by_id(b)
     # plt.close()
     plot_savetxt(data_set,xlabel,data_get,ylabel,parameters_name,folder+'\\'+dayFolder,name)


    datasmooth=scipy.signal.savgol_filter(np.ravel(data_get[0]),11, 3)
    phimin=np.min(datasmooth)
    argmin=np.argmin(datasmooth)

   
    VG3comp(data_set[argmin])
    print('minpeak_VG3='+str(VG3()))  

def VG4componmin(initVT2,finalVT2,points,showplot):
    VG4comp(initVT2)
    time.sleep(0.05)
    a,dataid,c=sweep1D(VG4comp, initVT2,finalVT2,points,0.01,ph1)
    now=datetime.datetime.now()
    dayFolder= datetime.date.isoformat(now)
    try:
        os.makedirs(folder2+'\\'+dayFolder)
    except IOError:
        donothing=1

    folder=r'S:\132-PHELIQS\132.05-LATEQS\132.05.01-QuantumSilicon\Tritonito\2021\Feb2021_6G22_2_die103\\data'
    name=str(dataid)+'_G4scan_calibrate_cs'
    xlabel='$Vc_{G4}$(mV)'
    ylabel='$\phi_{G1}$(deg)'
    data_set,data_get,parameters_name=Extract_data(a)
    if showplot==1:
     # plot_by_id(b)
     # plt.close()
     plot_savetxt(data_set,xlabel,data_get,ylabel,parameters_name,folder+'\\'+dayFolder,name)


    datasmooth=scipy.signal.savgol_filter(np.ravel(data_get[0]),11, 3)
    phimin=np.min(datasmooth)
    argmin=np.argmin(datasmooth)

   
    VG4(data_set[argmin])
    print('minpeak_VG4='+str(VG4()))  
    
def VG4onmin(initVT2,finalVT2,points,showplot):
    rampVG4(initVT2)
    time.sleep(0.1)
    a,dataid,c=sweep1D(VG4, initVT2,finalVT2,points,0.01,ph1)
    now=datetime.datetime.now()
    dayFolder= datetime.date.isoformat(now)
    try:
        os.makedirs(folder2+'\\'+dayFolder)
    except IOError:
        donothing=1

    folder=r'S:\132-PHELIQS\132.05-LATEQS\132.05.01-QuantumSilicon\Tritonito\2021\Feb2021_6G22_2_die103\\data'
    name=str(dataid)+'_G4scan_calibrate_cs'
    xlabel='$V_{G4}$(mV)'
    ylabel='$\phi_{G1}$(deg)'
    data_set,data_get,parameters_name=Extract_data(a)
    if showplot==1:
     # plot_by_id(b)
     # plt.close()
     plot_savetxt(data_set,xlabel,data_get,ylabel,parameters_name,folder+'\\'+dayFolder,name)


    datasmooth=scipy.signal.savgol_filter(np.ravel(data_get[0]),11, 3)
    phimin=np.min(datasmooth)
    argmin=np.argmin(datasmooth)

   
    VG4(data_set[argmin])
    print('minpeak_VG4='+str(VG4()))  

def VG5onmin(initVT2,finalVT2,points,showplot):
    rampVG5(initVT2)
    time.sleep(0.1)
    a,dataid,c=sweep1D(VG5, initVT2,finalVT2,points,0.01,ph1)
    now=datetime.datetime.now()
    dayFolder= datetime.date.isoformat(now)
    try:
        os.makedirs(folder2+'\\'+dayFolder)
    except IOError:
        donothing=1

    folder=r'S:\132-PHELIQS\132.05-LATEQS\132.05.01-QuantumSilicon\Tritonito\2021\Feb2021_6G22_2_die103\\data'
    name=str(dataid)+'_G5scan_calibrate_cs'
    xlabel='$V_{G5}$(mV)'
    ylabel='$\phi_{G1}$(deg)'
    data_set,data_get,parameters_name=Extract_data(a)
    if showplot==1:
     # plot_by_id(b)
     # plt.close()
     plot_savetxt(data_set,xlabel,data_get,ylabel,parameters_name,folder+'\\'+dayFolder,name)


    datasmooth=scipy.signal.savgol_filter(np.ravel(data_get[0]),11, 3)
    phimin=np.min(datasmooth)
    argmin=np.argmin(datasmooth)

   
    VG5(data_set[argmin])
    print('minpeak_VG5='+str(VG5()))  
    
def VG5onmin_ph2(initVT2,finalVT2,points,showplot):
    rampVG5(initVT2)
    time.sleep(0.1)
    a,dataid,c=sweep1D(VG5, initVT2,finalVT2,points,0.017777,ph2)
    now=datetime.datetime.now()
    dayFolder= datetime.date.isoformat(now)
    try:
        os.makedirs(folder2+'\\'+dayFolder)
    except IOError:
        donothing=1

    folder=r'S:\132-PHELIQS\132.05-LATEQS\132.05.01-QuantumSilicon\Tritonito\2021\Feb2021_6G22_2_die103\\data'
    name=str(dataid)+'_G5scan_calibrate_cs'
    xlabel='$V_{G5}$(mV)'
    ylabel='$\phi_{D}$(deg)'
    data_set,data_get,parameters_name=Extract_data(a)
    if showplot==1:
     # plot_by_id(b)
     # plt.close()
     plot_savetxt(data_set,xlabel,data_get,ylabel,parameters_name,folder+'\\'+dayFolder,name)


    datasmooth=scipy.signal.savgol_filter(np.ravel(data_get[0]),11, 3)
    phimin=np.min(datasmooth)
    argmin=np.argmin(datasmooth)

   
    VG5(data_set[argmin])
    print('minpeak_VG5='+str(VG5()))   
    
def VG1onmin_ph2(initVT2,finalVT2,points,showplot):
    rampVG1(initVT2)
    time.sleep(0.1)
    a,dataid,c=sweep1D(VG1, initVT2,finalVT2,points,0.01,ph2)
    now=datetime.datetime.now()
    dayFolder= datetime.date.isoformat(now)
    try:
        os.makedirs(folder2+'\\'+dayFolder)
    except IOError:
        donothing=1

    folder=r'S:\132-PHELIQS\132.05-LATEQS\132.05.01-QuantumSilicon\Tritonito\2021\Feb2021_6G22_2_die103\\data'
    name=str(dataid)+'_G1scan_calibrate_cs'
    xlabel='$V_{G1}$(mV)'
    ylabel='$\phi_{D}$(deg)'
    data_set,data_get,parameters_name=Extract_data(a)
    if showplot==1:
     # plot_by_id(b)
     # plt.close()
     plot_savetxt(data_set,xlabel,data_get,ylabel,parameters_name,folder+'\\'+dayFolder,name)


    datasmooth=scipy.signal.savgol_filter(np.ravel(data_get[0]),11, 3)
    phimin=np.min(datasmooth)
    argmin=np.argmin(datasmooth)

   
    VG1(data_set[argmin])
    print('minpeak_VG1='+str(VG1()))  
            
def VG2onmin_ph2(initVT2,finalVT2,points,showplot):
    rampVG2(initVT2)
    time.sleep(0.1)
    a,dataid,c=sweep1D(VG2, initVT2,finalVT2,points,0.01,ph2)
    now=datetime.datetime.now()
    dayFolder= datetime.date.isoformat(now)
    try:
        os.makedirs(folder2+'\\'+dayFolder)
    except IOError:
        donothing=1

    folder=r'S:\132-PHELIQS\132.05-LATEQS\132.05.01-QuantumSilicon\Tritonito\2021\Feb2021_6G22_2_die103\\data'
    name=str(dataid)+'_G2scan_calibrate_cs'
    xlabel='$V_{G2}$(mV)'
    ylabel='$\phi_{D}$(deg)'
    data_set,data_get,parameters_name=Extract_data(a)
    if showplot==1:
     # plot_by_id(b)
     # plt.close()
     plot_savetxt(data_set,xlabel,data_get,ylabel,parameters_name,folder+'\\'+dayFolder,name)


    datasmooth=scipy.signal.savgol_filter(np.ravel(data_get[0]),11, 3)
    phimin=np.min(datasmooth)
    argmin=np.argmin(datasmooth)

   
    VG2(data_set[argmin])
    print('minpeak_VG2='+str(VG2()))  
        
def VG3onmin_ph2(initVT2,finalVT2,points,showplot):
    rampVG3(initVT2)
    time.sleep(0.1)
    a,dataid,c=sweep1D(VG3, initVT2,finalVT2,points,0.01,ph2)
    now=datetime.datetime.now()
    dayFolder= datetime.date.isoformat(now)
    try:
        os.makedirs(folder2+'\\'+dayFolder)
    except IOError:
        donothing=1

    folder=r'S:\132-PHELIQS\132.05-LATEQS\132.05.01-QuantumSilicon\Tritonito\2021\Feb2021_6G22_2_die103\\data'
    name=str(dataid)+'_G3scan_calibrate_cs'
    xlabel='$V_{G3}$(mV)'
    ylabel='$\phi_{D}$(deg)'
    data_set,data_get,parameters_name=Extract_data(a)
    if showplot==1:
     # plot_by_id(b)
     # plt.close()
     plot_savetxt(data_set,xlabel,data_get,ylabel,parameters_name,folder+'\\'+dayFolder,name)


    datasmooth=scipy.signal.savgol_filter(np.ravel(data_get[0]),11, 3)
    phimin=np.min(datasmooth)
    argmin=np.argmin(datasmooth)

   
    VG3(data_set[argmin])
    print('minpeak_VG3='+str(VG3()))  
    
def VG4onmin_ph2(initVT2,finalVT2,points,showplot):
    rampVG4(initVT2)
    time.sleep(0.1)
    a,dataid,c=sweep1D(VG4, initVT2,finalVT2,points,0.01,ph2)
    now=datetime.datetime.now()
    dayFolder= datetime.date.isoformat(now)
    try:
        os.makedirs(folder2+'\\'+dayFolder)
    except IOError:
        donothing=1

    folder=r'S:\132-PHELIQS\132.05-LATEQS\132.05.01-QuantumSilicon\Tritonito\2021\Feb2021_6G22_2_die103\\data'
    name=str(dataid)+'_G4scan_calibrate_cs'
    xlabel='$V_{G4}$(mV)'
    ylabel='$\phi_{D}$(deg)'
    data_set,data_get,parameters_name=Extract_data(a)
    if showplot==1:
     # plot_by_id(b)
     # plt.close()
     plot_savetxt(data_set,xlabel,data_get,ylabel,parameters_name,folder+'\\'+dayFolder,name)


    datasmooth=scipy.signal.savgol_filter(np.ravel(data_get[0]),11, 3)
    phimin=np.min(datasmooth)
    argmin=np.argmin(datasmooth)

   
    VG4(data_set[argmin])
    print('minpeak_VG4='+str(VG4()))  
     
def VB3onrightside(initVB3,finalVB3,stepVB3,showplot):
    rampVB3(initVB3)
    phaseZero_B3()
    phaseZero_B3()
    time.sleep(1)
    loop = qc.Loop(VB3.sweep(initVB3,finalVB3,stepVB3),delay=0.1).each(phaseB3)
    data = loop.get_data_set(name='VB3test_init'+dacnames()) 
    if showplot==1:
     plot = qc.QtPlot()
     plot.add(data.phiB3)
     _= loop.with_bg_task(plot.update, plot.save).run()
    else: 
     _ = loop.run()
    
    phimin=np.min(data.phiB3)
    argmin=np.argmin(data.phiB3)
    kmin=0
    kmax=0
    if phimin>-0.005:
        print('CAREFULL!! you selected the wrong peak')
    for k in range(0,len(data.phiB3)):
        #typicalFWHM is <1.5mV
        #take 1 mV distance from min to avoid undesiderd peaks
        if(data.phiB3[k]<phimin/2 and np.abs(argmin-k)<20):
            kmax=k
            if kmin==0:
                kmin=k
                
    #sit on the left side of peak  
    
    #VB3(data.B3_set[kmin])            
    #sit on the right side of peak      
    #VB3(data.B3_set[kmax])
       #sit on the center of peak      
    VB3(data.B3_set[kmax])
    print('rightpeak_VB3='+str(VB3()))
    kmin_init=kmin

#autoset slope for compensation and sit on left side of sensor peak
def autosetting_sensor(DeltaVB2,DeltaVT2,initVB1,finalVB1,stepVB1):
    rampVB3(initVB3)
    phaseZero()
    phaseZero()
    time.sleep(2)
    a,b,c= sweep1D(VB1,initVB1,finalVB1,stepVB1,0.01,ph4)
    data_set,data_get,parameters_name=Extract_data(a)
    phimin=np.min(data_get)
    argmin=np.argmin(data_get)
    kmin=0
    kmax=0
    initVB2=VB2()
    initVT2=VT2()
    if phimin>-0.005:
        print('CAREFULL!! you selected the wrong peak')
    for k in range(0,len(data.phiB3)):
        #typicalFWHM is <1.5mV
        #take 1 mV distance from min to avoid undesiderd peaks
        if(data.phiB3[k]<phimin/2 and np.abs(argmin-k)<20):
            kmax=k
            if kmin==0:
                kmin=k
                
    #sit on the left side of peak  
    
    #VB3(data.B3_set[kmin])            
    #sit on the right side of peak      
    #VB3(data.B3_set[kmax])
       #sit on the center of peak      
    VB3(data.B3_set[argmin])
    kmin_init=kmin
    
    #change VB2 and find   new VB3*
    rampVB2(VB2()+DeltaVB2)
    
    rampVB3(initVB3)
    phaseZero()
    phaseZero()
    time.sleep(2)
    loop = qc.Loop(VB3.sweep(initVB3,finalVB3,stepVB3),delay=0.1).each(phaseB3)
    data = loop.get_data_set(name='VB3test_B2shift'+dacnames())   
    #plot = qc.QtPlot()
    plot.add(data.phiB3)
    _ = loop.with_bg_task(plot.update, plot.save).run()
    
    
    phimin=np.min(data.phiB3)
    argmin=np.argmin(data.phiB3)
    kmin=0
    kmax=0
    for k in range(0,len(data.phiB3)):
        #typicalFWHM is <1.5mV
        #take 1 mV distance from min to avoid undesiderd peaks
        if(data.phiB3[k]<phimin/2 and np.abs(argmin-k)<20):
            kmax=k
            if kmin==0:
                kmin=k
    kmin_dB2=kmin            
    dVB3=(kmin_dB2-kmin_init)*stepVB3
    
    
#    print('oldslope_B2B3=',slopeB2B3)
    slopeB2B3=dVB3/DeltaVB2
    print('newslope_B2B3=',slopeB2B3)
    
    
    #change VT2 and find  new VB3*
    rampVT2(VT2()+DeltaVT2)
    rampVB3(initVB3)
    phaseZero()
    phaseZero()
    time.sleep(2)
    loop = qc.Loop(VB3.sweep(initVB3,finalVB3,stepVB3),delay=0.1).each(phaseB3)
    data = loop.get_data_set(name='VB3test_T2shift'+dacnames())   
    #plot = qc.QtPlot()
    plot.add(data.phiB3)
    _ = loop.with_bg_task(plot.update, plot.save).run()
    
    phimin=np.min(data.phiB3)
    argmin=np.argmin(data.phiB3)
    kmin=0
    kmax=0
    for k in range(0,len(data.phiB3)):
        #typicalFWHM is <1.5mV
        #take 1 mV distance from min to avoid undesiderd peaks
        
        #20points=1mV
        if(data.phiB3[k]<phimin/2 and np.abs(argmin-k)<20):#points
            kmax=k
            if kmin==0:
                kmin=k
                
    kmin_dT2=kmin            
    dVB3=(kmin_dT2-kmin_dB2)*stepVB3
    
#    print('oldslope_T2B3=',slopeT2B3)
    slopeT2B3=dVB3/DeltaVT2  
    print('newslope_T2B3=',slopeT2B3)
    #setB3 on leftside of peak
    VB3(data.B3_set[kmin])            
    #sit on the right side of peak      
    #VB3(data.B3_set[kmax])
    
    
    VB2comp=  SpecialParameters.CompensateB2(VB2,VB3,slopeB2B3)
    VT2comp=  SpecialParameters.CompensateT2(VT2,VB3,slopeT2B3)
    print('VB2fin=',VB2())
    print('VT2fin=',VT2())
    #return topeak for initial values
    VB2comp(initVB2)
    VT2comp(initVT2)
    
def set_readout(T2):
    ziUhf.daq.setInt('/dev2226/sigouts/1/on', 0)
    continuous_acquisition_B3()
    VB2comp(808)
#    VT2comp(438.5)
    VT2comp(T2)
    VB3(850)
    ziUhf.daq.setInt('/dev2226/demods/5/phaseadjust', 1)
    time.sleep(1)
    ziUhf.daq.setInt('/dev2226/demods/5/phaseadjust', 1)

    phaseB3()
#    VB3onmin(881,887,0.0177775,1)#VT3=-450
    VB1onmin(850,860,0.0177775,1)#VT3=-350
    VB1(VB1()-0.25)
    print( str(VB1()) )
    
    #test
    VB2comp(810)
    VT2comp(T2)
    
    loop = qc.Loop(VB2comp.sweep(809,819,0.017777),delay=0.1).each(phaseB3)
    data = loop.get_data_set(name='TP12_1dscanslow-'+str(Bfield())+'_T_ampliAWG'+str(ampliAWG())+'_VT3_'+str(VT3())+'mV')#pulsed_pulsingB2_10us
    plot = qc.QtPlot()
    plot.add(data.phiB3)
    _ = loop.with_bg_task(plot.update, plot.save).run()
    
    
    #set at half 

    phimin=np.min(data.phiB3[5:])
    phimax=np.max(data.phiB3)
    phiset=(phimax-phimin)/2+phimin
    argmin=np.argmin(data.phiB3)
    kmin=0
    kmax=0
    
    for k in range(0,len(data.phiB3)):
        #typicalFWHM is <1.5mV
        #take 1 mV distance from min to avoid undesiderd peaks
        if(data.phiB3[k]<phiset+0.001 and data.phiB3[k]>phiset-0.001):
            kset=k
         


    VB2comp(data.CompensatedB2_set[kset]) 
    print(str(VB2()))
    
    
h=4.135667662e-15 #eV*s
bohr=5.7883818e-5#eV*
fontSize=16
kb=8.61733e-5#eV/K

# 
h=4.135667662e-15 #eV*s
bohr=5.7883818e-5#eV*
fontSize=16
kb=8.61733e-5#eV/K

def removeBackground_B3(rangeMin=0, rangeMax=-1):
        for i in range(len(data.phiB3)):
            data.phiB3[i] = data.phiB3[i] - data.phiB3[i][rangeMin:rangeMax].mean() 


def removeMeanFromEachLine2(rangeMin=0, rangeMax=-1):
    for i in range(len(z)):
       z[i] = z[i] - z[i][rangeMin:rangeMax].mean() 
def removeMeanFromEachLine(rangeMin=0, rangeMax=-1):
    for i in range(len(loadedData.phi)):
        loadedData.phi[i] = loadedData.phi[i] - loadedData.phi[i][rangeMin:rangeMax].mean() 
# def removeMeanFromEachLine_amplitude(rangeMin=0, rangeMax=-1):
#     for i in range(len(loadedData.attenuation)):
#         loadedData.attenuation[i] = loadedData.attenuation[i] - loadedData.attenuation[i][rangeMin:rangeMax].mean()   
        
def removeMeanFromEachLine_phasepulse(rangeMin=0, rangeMax=-1):
    for i in range(len(loadedData.phase_pulse)):
        loadedData.phase_pulse[i] = loadedData.phase_pulse[i] - loadedData.phase_pulse[i][0:10].mean() 

def removeMeanFromEachLine_firstpoints(rangeMin=0, rangeMax=-1):
    for i in range(len(loadedData.phi)):
        loadedData.phi[i] = loadedData.phi[i] - loadedData.phi[i][0:30].mean()         
        
def removeMeanFromEachLine_B3(rangeMin=0, rangeMax=-1):
    for i in range(len(loadedData.phiB3)):
        loadedData.phiB3[i] = loadedData.phiB3[i] - loadedData.phiB3[i][rangeMin:rangeMax].mean() 
        
def reverseaxis():
   for j in range(len(loadedData.zFieldPhase0_set)): 
    for i in range(int(len(loadedData.detuning_set[j])/2)):
        z = loadedData.phi[j][len(loadedData.detuning_set[j])-i-1] 
        loadedData.phi[j][len(loadedData.detuning_set[j])-i-1]= loadedData.phi[j][i]
        loadedData.phi[j][i]=z
        
def reverseaxis_B3():
   for j in range(len(loadedData.CompensatedT2_set)): 
    for i in range(int(len(loadedData.CompensatedB2_set)/2)):
        z = loadedData.phiB3[j][len(loadedData.CompensatedB2_set)-i-1] 
        loadedData.phiB3[j][len(loadedData.CompensatedB2_set)-i-1]= loadedData.phiB3[j][i]
        loadedData.phiB3[j][i]=z       
    
        
    #defined like this sweep parameter 2 first
def sweep2D(param_set1, start1, stop1, num_points1, delay1, 
         param_set2, start2, stop2, num_points2, delay2,
         *param_meas):
    # And then run an experiment
    
    meas = Measurement()
    meas.register_parameter(param_set1)
    param_set1.post_delay = delay1
    meas.register_parameter(param_set2)
    param_set2.post_delay = delay2
    output = [] 
    
    
    for parameter in param_meas:
        meas.register_parameter(parameter, setpoints=(param_set1,param_set2))
        output.append([parameter, None])

    t1=time.time()
    
    with meas.run() as datasaver:
        for set_point1 in np.linspace(start1, stop1, num_points1):
            param_set1.set(set_point1)
            for set_point2 in np.linspace(start2, stop2, num_points2):
                param_set2.set(set_point2)
                for i, parameter in enumerate(param_meas):
                    output[i][1] = parameter.get()
                datasaver.add_result((param_set1, set_point1),
                                     (param_set2, set_point2),
                                     *output)
    dataid = datasaver.run_id  # convenient to have for plotting
    
    t2=time.time()
    t=t2-t1 
    t=round(t,3)
    print('')
    print('')
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print ("Measurement time=", t, "secondes" )    
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print('')
    print('')
    
    # param_set1(0)
    # param_set2(0)
    
    return datasaver.dataset, dataid,num_points1,num_points2


def sweep1D(param_set1, start1, stop1, num_points1, delay1, *param_meas):
    # And then run an experiment
    t0=time.time()
    meas = Measurement()
    meas.register_parameter(param_set1)
    param_set1.post_delay = delay1
    output = [] 
    
    for parameter in param_meas:
        meas.register_parameter(parameter, setpoints=(param_set1,))
        output.append([parameter, None])

    with meas.run() as datasaver:
        for set_point1 in np.linspace(start1, stop1, num_points1):
            param_set1.set(set_point1)
            # for i, parameter in enumerate(param_meas):
            #         output[i][1] = parameter.get()
            for i, parameter in enumerate(param_meas):
                    output[i][1] = parameter.get()
                    
            datasaver.add_result((param_set1, set_point1), *output)
              
    dataid = datasaver.run_id  # convenient to have for plotting
    # a=datasaver.dataset.get_data('')
    
    t1=time.time()

    t=t1-t0
    t=round(t,3)
    print('')
    print('')
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print ("Measurement time=", t, "secondes" )    
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print('')
    print('')

    # param_set1(0)
    # param_set2(0)
    
    return datasaver.dataset,dataid,num_points1




def Extract_data(a):
#extract parameters name
    parameters_name=[]
    c1=0
    for i in range(0, len(a.parameters)):
        # print(i)
        # print(a.parameters)
        if i==(len(a.parameters)-1): 
            parameters_name.append(a.parameters[c1:])
    
        if a.parameters[i]!=',':
           c2=i+1
        elif a.parameters[i]==',':
             parameters_name.append(a.parameters[c1:c2])
             c1=i+1
    
    data_set=[]
    data_get=[]
    
    #parameter_swept_fixed length
    data_x=a.get_parameter_data(parameters_name[0])
    x=data_x[parameters_name[0]]
    x=x[parameters_name[0]] 
    data_set=x  
    
    
    #parameter_acquired may have variable length
    #update data .get
    for i in range(1,len(parameters_name)):
        print(i)
        data_y=a.get_parameter_data(parameters_name[i])
        y=data_y[parameters_name[i]]
        y=y[parameters_name[i]] 
    
        data_get.append(y)
    
    
    lendata_set=len(data_set)
    lendata_get=len(data_get[0])
    
    # #clean set parameters that are registered multiple times in sweep function
    # i=0
    # while i <(len(data_set)-1):
    #     # if i%(int(lendata_set/lendata_get)) !=0:
    #         if data_set[i]==data_set[i+1]:
    #             del data_set[i]
    #         else:
    #             i+=1    
    data_set=np.unique(data_set)

    return data_set,data_get, parameters_name   


def Extract_data_2d(a):
#extract parameters name
    parameters_name=[]
    c1=0
    for i in range(0, len(a.parameters)):
        print(i)
        print(a.parameters)
        if i==(len(a.parameters)-1): 
            parameters_name.append(a.parameters[c1:])
    
        if a.parameters[i]!=',':
           c2=i+1
        elif a.parameters[i]==',':
             parameters_name.append(a.parameters[c1:c2])
             c1=i+1
    
    data_set=[]
    data_get=[]
    
    #parameter_swept_fixed length
    data_set.append(a.get_data(parameters_name[0]))
    data_set.append(a.get_data(parameters_name[1]))
    #parameter_acquired may have variable length
    #update data .get
    for i in range(2,len(parameters_name)):
        print(i)
        data_get.append(a.get_values(parameters_name[i]))

    
    lendata_set=len(data_set)
    lendata_get=len(data_get[0])
    
    #clean set parameters that are registered multiple times in sweep function
    for j in range(0,2):
        i=0
        while i <(len(data_set[j])-1):
            # if i%(int(lendata_set/lendata_get)) !=0:
                if data_set[j][i]==data_set[j][i+1]:
                    del data_set[j][i]
                else:
                    i+=1    
    return data_set,data_get, parameters_name   

    
def plot_savetxt(data_set,xlabel,data_get,ylabel,parameters_name,folder,name):
    for i in range(0,len(data_get)):
        plt.figure()
        plt.plot(data_set ,data_get[i]) 
        # plt.title('Id vs $V_{g}$')
        plt.xlabel(xlabel,fontsize=16)
        plt.ylabel(ylabel,fontsize=16)  
        plt.savefig(folder+'\\'+name+'_'+parameters_name[i+1])
        plt.show()
        
        text_file = open(folder+'\\'+name+'_'+parameters_name[i+1]+'.txt', "w")
        
        text_file.write(str((data_get[i])))
        
        text_file.close()

# def plot_savecsv(data_set,xlabel,data_get,ylabel,parameters_name,folder,name):
#     for i in range(0,len(data_get)):
#         plt.figure()
#         plt.plot(data_set ,data_get[i]) 
#         # plt.title('Id vs $V_{g}$')
#         plt.xlabel(xlabel,fontsize=16)
#         plt.ylabel(ylabel,fontsize=16)  
#         plt.savefig(folder+'\\'+name+'_'+parameters_name[i+1])
#         plt.show()
#         filename=folder+'\\'+name+'_'+parameters_name[i+1]+'.csv'
#         # datas=list(zip(data_get[0],data_set))
#         # np.savetxt(filename,datas,delimiter=',',header="A,B")
#         # np.savetxt(filename,data_get[0])
#         f=open(filename,"w")
#         f.write("{};{}\n".format(ylabel,xlabel))
#         for x in zip(data_get[0],data_set):
#             f.write("{};{} \n".format(str(x[0])[1:-1],str(x[1])[1:-1]))
#         f.close()

def plot_savecsv(data_set,xlabel,data_get,ylabel,parameters_name,folder,name):
    for i in range(0,len(data_get)):
        plt.figure()
        plt.plot(data_set ,data_get[i]) 
        # plt.title('Id vs $V_{g}$')
        plt.xlabel(xlabel,fontsize=16)
        plt.ylabel(ylabel,fontsize=16)  
        plt.savefig(folder+'\\'+name+'_'+parameters_name[i+1])
        plt.show()
        filename=folder+'\\'+name+'_'+parameters_name[i+1]+'.csv'
        # datas=list(zip(data_get[0],data_set))
        # np.savetxt(filename,datas,delimiter=',',header="A,B")
        # np.savetxt(filename,data_get[0])
        f=open(filename,"w")
        f.write("{};{};{};{};{}\n".format(ylabel,xlabel,'lot T18S0062A','DIE 241','WAFER23'))
        for x in zip(data_get[0],data_set):
            f.write("{};{} \n".format(str(x[0])[1:-1],str(x[1])[1:-1]))
        f.close()


    
def saveplot(name,dataid):
    folder2=r'S:\132-PHELIQS\132.05-LATEQS\132.05.01-QuantumSilicon\Tritonito\2021\Feb2021_6G22_2_die103\data'
    now=datetime.datetime.now()
    dayFolder=datetime.date.isoformat(now)
    try:
        os.makedirs(folder2+'\\'+dayFolder)
    except IOError:
        donothing=1
    plt.savefig(folder2+'\\'+dayFolder+'\\'+str(dataid)+'_'+name+'.png')#add time as in old qcodes
    
    
def savetxt(name,dataid,data,dataname):
    folder2=r'S:\132-PHELIQS\132.05-LATEQS\132.05.01-QuantumSilicon\Tritonito\2021\Feb2021_6G22_2_die103\\data'
    now=datetime.datetime.now()
    dayFolder=datetime.date.isoformat(now)
    try:
        os.makedirs(folder2+'\\'+dayFolder)
    except IOError:
        donothing=1
    text_file = open(folder2+'\\'+dayFolder+'\\'+str(dataid)+'_'+name+'.txt', "w")
    text_file.write(dataname+'\n')
    text_file.write(data)

    text_file.close()

def transforminto_oldQCformat(dataid):
    the_data = load_by_id(dataid)
    data_list = the_data.get_parameter_data()
    P = the_data.parameters
    p = P.split(',')
    Y= data_list[p[2]][p[0]]#freq
    X = data_list[p[2]][p[1]]#gate
    x = np.unique(X)
    y = np.unique(Y)
    z1 = data_list[p[2]][p[2]]
    Z1 = z1.reshape((np.size(np.unique(Y)),np.size(np.unique(X))))
    X,Y = np.meshgrid(x,y)
    return x,y,Z1

# def transforminto_oldQCformat_sweep_on_y(dataid):
#     the_data = load_by_id(dataid)
#     data_list = the_data.get_parameter_data()
#     P = the_data.parameters
#     p = P.split(',')
#     X= data_list[p[2]][p[0]]#freq
#     Y = data_list[p[2]][p[1]]#gate
#     x = np.unique(X)
#     y = np.unique(Y)
#     z1 = data_list[p[2]][p[2]]
#     Z1 = z1.reshape((np.size(np.unique(Y)),np.size(np.unique(X))))
#     X,Y = np.meshgrid(x,y)
#     return x,y,Z1


def removeBackground(data,rangeMin=0, rangeMax=-1):
    for i in range(len(data)):
        data[i] = data[i] - data[i][rangeMin:rangeMax].mean() 
    return(data)

def extractParameters():
    # C=W/Lg
    # linear=0#if linear=0 plot in log
    
    #plot in semilog and analyse
    x=[]
    y=[]
    # for i in range (0,len(calibs)):
    #     x.append(calibs[i][0])
    #     y.append(calibs[i][1])
    y=data_get[0]
    currentoffset=np.mean(y[10:20])#with 10mVstep is -900:-800
    y=np.add(y,currentoffset)    
    x=np.divide(data_set,1000)#in V
    y=scipy.signal.savgol_filter(np.transpose(y),11,3)
    x=np.transpose(x)

    dydx=np.transpose(np.divide(np.diff(y),np.diff(x)))#I loose 1 point
    # dydx=np.gradient(y, step)#,axis=None,edge_order=1)#it was working with old python
   
    xax=x[0][1:]
    yax=y[0][1:]
    plt.plot(xax,yax) 

    threshold=np.argmin(dydx)
    y0=yax[threshold]
    C=y0-dydx[threshold]*xax[threshold]
    # y=scipy.signal.savgol_filter(dydx,51,3)
    yy=dydx[threshold]*xax +C
    plt.plot(xax,yy)
    # plt.title(nome+'VT_extraction')
    # plt.savefig(folder2+'\\'+nome+'_VTextraction'+"bias"+str(int(bias/10))+"mV"+"_T_"+Temp+'_'+giorno)
    # plt.close()
    for j in range (0,len(yy)):
        if yy[j]<0:
            threshold=j
    VTg1=xax[threshold]
    print(VTg1)

    halfvolt=int(0.5/step)
    #        x[threshold-halfvolt]#minus sign because I am scanning backwards
    IonVg1=yax[threshold+halfvolt]
    
    #extract Ion, slope and resistance
    #evaluated at Vt+0.5V, where device is not yet on saturation...
             

    
    #SS slope
    dx=step
    dx=dx*1000
    
    dy= np.log10(yax[threshold-1])-np.log10(yax[threshold-2])#VT-100mV, VT-300mV
    
    SSg1=np.round(dx/dy,1) 
    
    IoffVg1=y[0]
    # R300K=np.round(biasV/IonVg1,1)
    # #save
    # infoline0='device;W(nm);Lg(nm); VT;SS(mV/dB);Ion(Vt+500mV);Ioff(-1V);R(300K)'
    # infoline=nome+';'+str(W)+';'+str(Lg)+';'+str(VTg1)+';'+str(SSg1)+';'+str(IonVg1)+';'+str(IoffVg1)+';'+str(R300K)
    
    
    # text_file = open(folder2+'\\'+nome+"bias"+str(int(bias/10))+"mV"+"_T_"+Temp+'_'+giorno+".txt", "w")
    
    # text_file.write(infoline0 +'\n'+infoline)
    
    # text_file.close()
    
    return VTg1, SSg1

def calibrate_detector(G3,G4):    
    bias(-0.2)
    rampVG1(-1455)
    rampVG2(-1280)
    ############
    rampVG3(G3)
    rampVG4(G4)
    rampVG5(-500)
    
    ##################
    G2now=VG2()
    G3now=VG3()
    G4now=VG4()
    G5now=VG5()
    # VG1onmin(-1550,-1450,501,1)
    G1now=VG1()
    VG1onmin(G1now-4,G1now+4,601,1)
    G1now=VG1()
    VG2onmin(G2now-3,G2now+3,601,1)
    
# def step_detection(phase_ss,taxis):
#     # https://stackoverflow.com/questions/48000663/step-detection-in-one-dimensional-data
    
#     ####understand this stepfunction
#     step=2
#     ###
#     dary = np.array(phase_ss)
    
#     dary -= np.average(dary)
    
#     step = np.hstack((np.ones(len(dary)), -1*np.ones(len(dary))))
    
#     dary_step = np.convolve(dary, step, mode='valid')
    
#     # get the peak of the convolution, its index
    
#     step_indx = np.argmax(dary_step)  # yes, cleaner than np.where(dary_step == dary_step.max())[0][0]
    
#     # # plots
#     # fig, ax = plt.subplots()
#     # plt.plot(taxis,dary)
    
#     # plt.plot(taxis,dary_step[0:-1]/10)
    
#     # plt.plot((taxis[step_indx], taxis[step_indx]), (dary_step[step_indx]/10, 0), 'r')
#     # ax.set_ylabel('$\phi$(rad)',fontsize=fontSize)
#     # ax.set_xlabel('time ($\mu$s) ',fontsize=fontSize)
#     # plt.savefig(folder2+'\\'+dayFolder+'\\stepdetection.png')
#     return(taxis[step_indx])
def step_detection(phase_ss,taxis):
    # https://stackoverflow.com/questions/48000663/step-detection-in-one-dimensional-data
    
    ####understand this stepfunction
    step=2
    ###
    dary = np.array(phase_ss)
    
    dary -= np.average(dary)
    
    step = np.hstack((np.ones(len(dary)), -1*np.ones(len(dary))))
    
    dary_step = np.convolve(dary, step, mode='valid')
    
    # get the peak of the convolution, its index
    
    step_indx = np.argmax(dary_step)  # yes, cleaner than np.where(dary_step == dary_step.max())[0][0]
    
    return(taxis[step_indx-1])



    
def save2plots(name,dataid):
    folder2=r'S:\132-PHELIQS\132.05-LATEQS\132.05.01-QuantumSilicon\Tritonito\2021\Feb2021_6G22_2_die103\data'
    now=datetime.datetime.now()
    dayFolder=datetime.date.isoformat(now)
    try:
        os.makedirs(folder2+'\\'+dayFolder)
    except IOError:
        donothing=1
    plt.savefig(folder2+'\\'+dayFolder+'\\'+str(dataid)+'_'+name+'.png')#add time as in old qcodes
    plt.close()
    plt.savefig(folder2+'\\'+dayFolder+'\\'+str(dataid)+'_'+name+'2.png')#add time as in old qcodes
    
    

    
def save3plots(name,dataid):
    folder2=r'S:\132-PHELIQS\132.05-LATEQS\132.05.01-QuantumSilicon\Tritonito\2021\Feb2021_6G22_2_die103\data'
    now=datetime.datetime.now()
    dayFolder=datetime.date.isoformat(now)
    try:
        os.makedirs(folder2+'\\'+dayFolder)
    except IOError:
        donothing=1
    plt.savefig(folder2+'\\'+dayFolder+'\\'+str(dataid)+'_'+name+'.png')#add time as in old qcodes
    plt.close()
    plt.savefig(folder2+'\\'+dayFolder+'\\'+str(dataid)+'_'+name+'2.png')
    plt.close()
    plt.savefig(folder2+'\\'+dayFolder+'\\'+str(dataid)+'_'+name+'3.png')#add time as in old qcodes

def save4plots(name,dataid):
    folder2=r'S:\132-PHELIQS\132.05-LATEQS\132.05.01-QuantumSilicon\Tritonito\2021\Feb2021_6G22_2_die103\data'
    now=datetime.datetime.now()
    dayFolder=datetime.date.isoformat(now)
    try:
        os.makedirs(folder2+'\\'+dayFolder)
    except IOError:
        donothing=1
    plt.savefig(folder2+'\\'+dayFolder+'\\'+str(dataid)+'_'+name+'.png')#add time as in old qcodes
    plt.close()
    plt.savefig(folder2+'\\'+dayFolder+'\\'+str(dataid)+'_'+name+'2.png')
    plt.close()
    plt.savefig(folder2+'\\'+dayFolder+'\\'+str(dataid)+'_'+name+'3.png')#add time as in old qcodes
    plt.close()
    plt.savefig(folder2+'\\'+dayFolder+'\\'+str(dataid)+'_'+name+'4.png')#add time as in old qcodes
    
    
def sensor_on_interdot_sweepG2comp_ph2(initVT2,finalVT2,points,showplot):
    VG2comp(initVT2)
    ph1()
    time.sleep(0.02)
    ph1()
    a,dataid,c=sweep1D(VG2comp, initVT2,finalVT2,points,0.01,ph2)
    # a,dataid,c=sweep1D(VG4,-1093,-1094.5,401,0.005,ph1)
    now=datetime.datetime.now()
    dayFolder= datetime.date.isoformat(now)
    try:
        os.makedirs(folder2+'\\'+dayFolder)
    except IOError:
        donothing=1

    folder=r'S:\132-PHELIQS\132.05-LATEQS\132.05.01-QuantumSilicon\Tritonito\2021\Feb2021_6G22_2_die103\\data'
    name=str(dataid)+'_G4scan_calibrate_cs'
    xlabel='$V_{G2comp}$(mV)'
    ylabel='$\phi_{D}$(deg)'
    data_set,data_get,parameters_name=Extract_data(a)
    if showplot==1:
     # plot_by_id(b)
     # plt.close()
     plot_savetxt(data_set,xlabel,data_get,ylabel,parameters_name,folder+'\\'+dayFolder,name)


    datasmooth=scipy.signal.savgol_filter(np.ravel(data_get[0]),11, 3)
    phimin=np.min(datasmooth)
    phimax=np.max(datasmooth)
    argmin=np.argmin(datasmooth)
    kmin=0
    kmax=0
    philim=phimin+(phimax-phimin)/2
    sigmaphi=0.05
    for k in range(0,len(data_set)):
        if ((data_get[0][k]>=(philim-sigmaphi) and data_get[0][k]<=(philim+sigmaphi)) and kmax==0):
            kmax=k
        
        #typicalFWHM is <1.5mVdef VT2onmin(initVB1,finalVB1,points,showplot):
   
    VG2comp(data_set[kmax])
    print('minpeak_VG2='+str(VG2()))        
    
def test6gate(initgate,finalgate,opengate,Vds):
    Npoints=501
    bias(Vds)
    rampVG1(initgate)
    rampVG2(opengate)
    rampVG3(opengate)
    rampVG4(opengate)
    rampVG5(opengate)
    rampVG6(opengate)
    
    a,b,c=sweep1D(VG1,initgate,finalgate,Npoints,0.01,current)
    data_set,data_get,parameters_name=Extract_data(a)
    
    xlabel='$V_{G}$(mV)'
    ylabel='$I_d$(A)'
    
    plt.figure()
    plt.plot(data_set ,data_get[0],label='$V_{G1}$') 
    # plt.title('Id vs $V_{g}$')
    plt.xlabel(xlabel,fontsize=16)
    plt.ylabel(ylabel,fontsize=16)  
    
    
    #measure
    #scanG2
    rampVG1(opengate)
    rampVG2(initgate)
    rampVG3(opengate)
    rampVG4(opengate)
    rampVG5(opengate)
    rampVG6(opengate)
    # time.sleep(20)#for capa
    a,b,c=sweep1D(VG2,initgate,finalgate,Npoints,0.01,current)
    
    data_set,data_get,parameters_name=Extract_data(a)
    plt.plot(data_set ,data_get[0],label='$V_{G2}$') 
    
    
    
    #measure
    #scanG3
    rampVG1(opengate)
    rampVG2(opengate)
    rampVG3(initgate)
    rampVG4(opengate)
    rampVG5(opengate)
    rampVG6(opengate)
    
    time.sleep(5)
    a,b,c=sweep1D(VG3,initgate,finalgate,Npoints,0.01,current)
    data_set,data_get,parameters_name=Extract_data(a)
    plt.plot(data_set ,data_get[0],label='$V_{G3}$') 
    
    
    
    
    
    #measure
    #scanG4
    rampVG1(opengate)
    rampVG2(opengate)
    rampVG3(opengate)
    rampVG4(initgate)
    rampVG5(opengate)
    rampVG6(opengate)
    a,b,c=sweep1D(VG4,initgate,finalgate,Npoints,0.01,current)
    data_set,data_get,parameters_name=Extract_data(a)
    plt.plot(data_set ,data_get[0],label='$V_{G4}$') 
    
    
    
    #measure
    #scanG5
    rampVG1(opengate)
    rampVG2(opengate)
    rampVG3(opengate)
    rampVG4(opengate)
    rampVG5(initgate)
    rampVG6(opengate)
    
    a,dataid,c=sweep1D(VG5,initgate,finalgate,Npoints,0.01,current)
    data_set,data_get,parameters_name=Extract_data(a)
    plt.plot(data_set ,data_get[0],label='$V_{G5}$') 
    
    #measure
    #scanG6
    rampVG1(opengate)
    rampVG2(opengate)
    rampVG3(opengate)
    rampVG4(opengate)
    rampVG5(opengate)
    rampVG6(initgate)
    
    a,dataid,c=sweep1D(VG6,initgate,finalgate,Npoints,0.01,current)
    data_set,data_get,parameters_name=Extract_data(a)
    plt.plot(data_set ,data_get[0],label='$V_{G6}$') 
    
    plt.legend()
    name=str(dataid)+'_LIN_6Gtest_bias'+str(int(bias()*1000))+'uVbias_gates_'+str(opengate)+'mV'
    plt.savefig(folder2+'\\'+dayFolder+'\\' +name)
  
    
def test6gate_log(initgate,finalgate,opengate,Vds):
    Npoints=1001
    bias(Vds)
    rampVG1(initgate)
    rampVG2(opengate)
    rampVG3(opengate)
    rampVG4(opengate)
    rampVG5(opengate)
    rampVG6(opengate)
    
    a,b,c=sweep1D(VG1,initgate,finalgate,Npoints,0.01,current)
    data_set,data_get,parameters_name=Extract_data(a)
    
    xlabel='$V_{G}$(mV)'
    ylabel='$I_d$(A)'
    
    plt.figure()
    plt.semilogy(data_set ,data_get[0],label='$V_{G1}$')
    # plt.title('Id vs $V_{g}$')
    plt.xlabel(xlabel,fontsize=16)
    plt.ylabel(ylabel,fontsize=16)  
    
    
    #measure
    #scanG2
    rampVG1(opengate)
    rampVG2(initgate)
    rampVG3(opengate)
    rampVG4(opengate)
    rampVG5(opengate)
    rampVG6(opengate)
    # time.sleep(20)#for capa
    a,b,c=sweep1D(VG2,initgate,finalgate,Npoints,0.01,current)
    
    data_set,data_get,parameters_name=Extract_data(a)
    plt.semilogy(data_set ,data_get[0],label='$V_{G2}$')
    
    
    
    #measure
    #scanG3
    rampVG1(opengate)
    rampVG2(opengate)
    rampVG3(initgate)
    rampVG4(opengate)
    rampVG5(opengate)
    rampVG6(opengate)
    
    time.sleep(5)
    a,b,c=sweep1D(VG3,initgate,finalgate,Npoints,0.01,current)
    data_set,data_get,parameters_name=Extract_data(a)
    plt.semilogy(data_set ,data_get[0],label='$V_{G3}$')
    
    
    
    
    #measure
    #scanG4
    rampVG1(opengate)
    rampVG2(opengate)
    rampVG3(opengate)
    rampVG4(initgate)
    rampVG5(opengate)
    rampVG6(opengate)
    a,b,c=sweep1D(VG4,initgate,finalgate,Npoints,0.01,current)
    data_set,data_get,parameters_name=Extract_data(a)
    plt.semilogy(data_set ,data_get[0],label='$V_{G4}$')
    
    
    
    #measure
    #scanG5
    rampVG1(opengate)
    rampVG2(opengate)
    rampVG3(opengate)
    rampVG4(opengate)
    rampVG5(initgate)
    rampVG6(opengate)
    
    a,dataid,c=sweep1D(VG5,initgate,finalgate,Npoints,0.01,current)
    data_set,data_get,parameters_name=Extract_data(a)
    plt.semilogy(data_set ,data_get[0],label='$V_{G5}$')
    
    #measure
    #scanG6
    rampVG1(opengate)
    rampVG2(opengate)
    rampVG3(opengate)
    rampVG4(opengate)
    rampVG5(opengate)
    rampVG6(initgate)
    
    a,dataid,c=sweep1D(VG6,initgate,finalgate,Npoints,0.01,current)
    data_set,data_get,parameters_name=Extract_data(a)
    plt.semilogy(data_set ,data_get[0],label='$V_{G6}$')
    
    plt.legend()
    name=str(dataid)+'_LOG_6Gtest_bias'+str(int(bias()*1000))+'uVbias_gates_'+str(opengate)+'mV'
    plt.savefig(folder2+'\\'+dayFolder+'\\' +name)

def plot2d_diff(dataid):
    the_data = load_by_id(dataid)
    data_list = the_data.get_parameter_data()
    P = the_data.parameters
    p = P.split(',')
    X= data_list[p[2]][p[0]]#freq
    Y= data_list[p[2]][p[1]]#gate
    x = np.unique(X)
    y = np.unique(Y)
    z1 = data_list[p[2]][p[2]]#phD
    z2= data_list[p[3]][p[3]]#phS
    z=z1-z2
   
    X,Y = np.meshgrid(y,x)
    
    Z1 = z.reshape((np.size(np.unique(Y)),np.size(np.unique(X))))
    
    Z1=np.flip(Z1)
    Z1=np.flipud(Z1)
    
    f = plt.figure()
    plt.pcolor(Y,X,Z1)
    
    
    plt.xlabel(p[0])
    plt.ylabel(p[1])
    plt.colorbar(label='$\phi_D-\phi_S$(deg)')
    plt.xlabel('G3(mV)')
    plt.ylabel('G4(mV)')
    # plt.clim(vmin=None,vmax=0.3)
    now=datetime.datetime.now()
    dayFolder=datetime.date.isoformat(now)
    name='G3G4_phD-phS_Dphi'
    plt.savefig(folder2+'\\'+dayFolder+'\\'+str(dataid)+name+'.png')

# import SpecialParameters 
def changeAread(filename,A):
    lines=open(filename).read().splitlines()
    with open(filename,'r+') as f:
         f.truncate(0)
         lines[16]='const amplitude11_scaled=' +str(A)+';'
         for i in range(len(lines)):
    
             f.write(lines[i]+'\n')
             
             #f.writelines()
    f.close()
    
def changetempty(filename,A):
    lines=open(filename).read().splitlines()
    with open(filename,'r+') as f:
         f.truncate(0)
         lines[30]='const pulseInit_sec =' +str(A)+';'
         for i in range(len(lines)):
             f.write(lines[i]+'\n')   
             #f.writelines()
    f.close()   
    
def changetload(filename,A):
    lines=open(filename).read().splitlines()
    with open(filename,'r+') as f:
         f.truncate(0)
         lines[31]='const pulseManip_sec =' +str(A)+';'
         for i in range(len(lines)):
             f.write(lines[i]+'\n')   
             #f.writelines()
    f.close()   
    
def changetread(filename,A):
    lines=open(filename).read().splitlines()
    with open(filename,'r+') as f:
         f.truncate(0)
         lines[34]='const pulseRead_sec =' +str(A)+';'
         for i in range(len(lines)):
             f.write(lines[i]+'\n')   
             #f.writelines()
    f.close()         


def find_working_point_by_id_inv(data_id,G2f,G3f,Plot = True, savefig = True):
# Function aimed to find the point at which the interdot breaks, starting from the id a of a small plot centered on a G2 transition

    data = qc.load_by_id(data_id)
    VarX=data.get_parameters()[0].unit
    nameX=data.get_parameters()[0].name
    VarY=data.get_parameters()[1].unit
    nameY=data.get_parameters()[1].name
    Varmap=data.get_parameters()[2].unit
    namemap=data.get_parameters()[2].name

    data_list = data.get_parameter_data()
    P = data.parameters
    p = P.split(',')
    X = data_list[p[2]][p[0]]
    Y = data_list[p[2]][p[1]]
    x = (np.unique(X))
    y = np.unique(Y)

    Vg3 = x
    Vg2 = y
    #Z1(Vg2,Vg3)!!!

    z1 = data_list[p[2]][p[2]]
    Z1 = np.transpose(z1.reshape((np.size(np.unique(X)),np.size(np.unique(Y)))))
    
# find maximum along the dot-lead
    ind1 = np.argmax(Z1[0,:])
    V1 = Vg3[ind1]
    Vpk = np.zeros(len(Vg2))
    for i in range(len(Vg2)):
        ind1 = np.argmin(Z1[i,:])
        Vpk[i] = Vg3[ind1]
# fit this maximum with a linear approx, only from the upper part of the plot:

    Ncut = int(len(Vg2)*0.4)  # number of points to take from upper of the scan 
    a,b = np.polyfit(Vg2[-Ncut:],Vpk[-Ncut:], 1)                   #linear fit to extract alpha

    # Extract profile along line:
    profile = np.zeros(len(Vg2))
    Eps = np.zeros(len(Vg2))
    V3 = a*Vg2+b
    delta = abs(Vg3[1]-Vg3[0])
#     delta = 0.015

    for i,V in enumerate(Vg2):
        indVg3 = np.where( (Vg3 > V3[i] - delta) & (Vg3 < V3[i] + delta))
        ind = indVg3[0][0]
        profile[i] = Z1[i,ind]

    # Find Vg2 corresponding to the middle of the jump
    mi = np.max(profile)
    ma = np.min(profile)
    av = (mi+ma)/2
    

    arg=np.argmin(np.abs(scipy.signal.savgol_filter(profile,11, 3)-av))
    

        
        #typicalFWHM is <1.5mVdef VT2onmin(initVB1,finalVB1,points,showplot):
   
    
    
    
    # diff = np.diff(profile)
    # arg = np.where(abs(diff) == np.max(abs(diff)))
    
##################
    V2p = Vg2[arg]
    # Find the corresponding Vg3:
    V3p = a*V2p+b   

#     print(V2p,V3p)
    if Plot == True:
        fig,ax=plt.subplots()
        X,Y = np.meshgrid(x,y)
        f = plt.pcolor(X,Y,Z1)    # 2D plot  
        plt.colorbar(label='$\phi_S(deg)$')
        ax.set_xlabel(nameX+ ' (' + VarX+')')
        ax.set_ylabel(nameY+ ' (' + VarY+')')

        f = plt.plot(Vpk[-Ncut:],Vg2[-Ncut:],color=(0,0,1))     # Plot of the max
        f = plt.plot(a*Vg2+b,Vg2, '--',color = (1,0,0),linewidth = 0.5)     # Plot of the linear fit
        f = plt.scatter(V3p,V2p,color = (1,0,1),marker = 'x',s =150)
        db_name=data.path_to_db[data.path_to_db.find('data')+5:]
        ax.title.set_text('database {} \n data_id {} \n '.format(db_name,data_id))
        plt.tight_layout()
        if savefig == True:
                        
            
#             plt.savefig('../analysis/Triple_points/Vg2='+str(round(V3p*1000)/1000)+'Vg2='+str(round(V2p*1000)/1000)+'.png')
            
                        
            path = f'..\exploration\G3=%s_g2=%s'%(G2f,G3f)

            try : 
                os.mkdir(path)
            except :
                print('Dossier existant')
            Field = Bfield_Hon()
            plt.savefig(path+f'/interdot_working_point_B='+str(round(Field,3))+'T.png',dpi=600)
        
#             plt.savefig(path+f'/interdot_working_point',dpi=600)
        
            path = f'..\exploration/0-all_interdot'

            try : 
                os.mkdir(path)
            except :
                print('Dossier existant')

            plt.savefig(path+f'\G3=%s_g2=%s_working_point'%(str(int(float(G2f))),str(int(float(G3f)))),dpi=600)

    # plot profile:    
    # f = plt.subplot(1,2,2)
    if Plot == True:
        f = plt.figure()
        f = plt.plot(Vg2,profile,color=(0,0,1))
        f = plt.vlines(V2p,mi,ma,color = (1,0,1),linestyles='dashed')
        plt.title('Slice along the transition')
        plt.xlabel('$Vg_3$ (mV)')
        plt.ylabel('Phase (deg)')
        plt.tight_layout()
        if savefig == True:
#             plt.savefig('../analysis/Triple_points/Vg2='+str(round(V3p*1000)/1000)+'Vg2='+str(round(V2p*1000)/1000)+'_profile.png')

            path = f'..\exploration\G3=%s_g2=%s'%(G2f,G3f)

            plt.savefig(path+f'\interdot_working_slice',dpi=600)

            path = f'..\exploration/0-all_interdot'

            plt.savefig(path+f'\G3=%s_g2=%s_working_slice'%(str(int(float(G2f))),str(int(float(G3f)))),dpi=600)            
            
    return V2p,V3p,a,b, av



#######################################
def blopIQ(DAM,tc,timetot,demod,path,G2f,G3f,title='I/Q measure') :
    ziUhf.daq.setDouble('/'+uhfRef+'/demods/{}/timeconstant'.format(demod-1),tc)
    ziUhf.daq.setDouble('/'+uhfRef+'/demods/{}/rate'.format(demod-1),1/tc)
    
    pathtxt=path+'.txt'

    DAM.get_data_txt(timetot,pathtxt,'x','y',affichage=False)

    data=np.loadtxt(pathtxt)
    file=open(pathtxt)
    read=file.read()
    file.close()
    read=read[1:read.find('\n')]
    parameters=read.split(';')

    for i,stringi in enumerate(parameters) :
        if parameters[i].find('x')>=0 :
            xvalues=data[:,i]
            xlabel=stringi
        if parameters[i].find('y')>=0 :
            yvalues=data[:,i]
            ylabel=stringi

    fig = plt.figure(figsize=(10, 10))
    grid = plt.GridSpec(4, 4, hspace=0.3, wspace=0.3)
    
    size = 14
    
    main_ax = fig.add_subplot(grid[:-1, 1:])
    main_ax.set_title('I/Q measure',size=size)
    main_ax.ticklabel_format(axis='both',style='sci',scilimits=[-6,-6])
#     main_ax.set_aspect('equal')

    y_hist = fig.add_subplot(grid[:-1, 0], xticklabels=[], sharey=main_ax)
    y_hist.ticklabel_format(axis='y',style='sci',scilimits=[-6,-6])
    y_hist.set_ylabel(ylabel,fontsize=size)

    x_hist = fig.add_subplot(grid[-1, 1:], yticklabels=[], sharex=main_ax)
    x_hist.ticklabel_format(axis='x',style='sci',scilimits=[-6,-6])
    x_hist.set_xlabel(xlabel,fontsize=size)

    color='darkorange'
    alpha=0.8
    # scatter points on the main axes
    main_ax.plot(xvalues, yvalues, 'ok', markersize=3, alpha=0.2,color=color)
    main_ax.set_aspect('equal')

    # histogram on the attached axes
    x_hist.hist(xvalues, 200,
                orientation='vertical', color=color,alpha=alpha)
    x_hist.invert_yaxis()

    y_hist.hist(yvalues, 200,
                orientation='horizontal', color=color,alpha=alpha)
    y_hist.invert_xaxis()
    
    main_ax.tick_params(labelsize=14)
    x_hist.tick_params(labelsize=14)
    y_hist.tick_params(labelsize=14)

    fig.tight_layout()

    
    fig.savefig(path,dpi=600)
    
    path = f'..\exploration/1-all_Bubbles'
    
    try : 
        os.mkdir(path)
    except :
        print('Dossier existant')

    fig.savefig(path+f'\G3=%s_g2=%s '%(str(int(float(G2f))),str(int(float(G3f))))+title,dpi=600)

# path=[f'..\exploration\Saving_process\g2=-638.475_g3=-949.55/IQ_on_signal.txt',f'..\exploration\Saving_process\g2=-638.475_g3=-949.55/IQ_out_of_signal.txt']


#######################
def draw_multiple_bbl(path,path_register,G2f,G3f) :

    fig = plt.figure(figsize=(10, 10))
    grid = plt.GridSpec(4, 4, hspace=0.3, wspace=0.3)
    size = 14
    main_ax = fig.add_subplot(grid[:-1, 1:])
    main_ax.set_title('I/Q measure',size=size)
    main_ax.ticklabel_format(axis='both',style='sci',scilimits=[-6,-6])

    y_hist = fig.add_subplot(grid[:-1, 0], xticklabels=[], sharey=main_ax)
    y_hist.ticklabel_format(axis='y',style='sci',scilimits=[-6,-6])

    x_hist = fig.add_subplot(grid[-1, 1:], yticklabels=[], sharex=main_ax)
    x_hist.ticklabel_format(axis='x',style='sci',scilimits=[-6,-6])
    
    color_all=['darkorange','tomato','blue','green','black']
    
    for j,pathh in enumerate(path) :
        data=np.loadtxt(pathh)
        file=open(pathh)
        read=file.read()
        file.close()
        read=read[1:read.find('\n')]
        parameters=read.split(';')

        for i,stringi in enumerate(parameters) :
            if parameters[i].find('x')>=0 :
                xvalues=data[:,i]
                xlabel=stringi
            if parameters[i].find('y')>=0 :
                yvalues=data[:,i]
                ylabel=stringi

        color=color_all[j]
        alpha=0.8
        # scatter points on the main axes
        main_ax.plot(xvalues, yvalues, 'ok', markersize=3, alpha=0.2,color=color)

        # histogram on the attached axes
        x_hist.hist(xvalues, 200,
                    orientation='vertical', color=color,alpha=alpha)
        x_hist.invert_yaxis()

        y_hist.hist(yvalues, 200,
                    orientation='horizontal', color=color,alpha=alpha)
        y_hist.invert_xaxis()
        
    y_hist.set_ylabel(ylabel,fontsize=size)
    x_hist.set_xlabel(xlabel,fontsize=size)
    main_ax.tick_params(labelsize=14)
    x_hist.tick_params(labelsize=14)
    y_hist.tick_params(labelsize=14)
    
    title=f'IQ_double_bbl'
    
    fig.savefig(path_register+f'/'+title,dpi=600)
    
    patth = f'..\exploration/1-all_Bubbles'

    fig.savefig(patth+f'\g2=%s_G3=%s '%(str(int(float(G2f))),str(int(float(G3f))))+title,dpi=600)

    fig.tight_layout()


def register_time_trace(DAM,start,stop,num_point,tc,total_time,demod,path,coeff_dir) :
    
    ziUhf.daq.setDouble('/'+uhfRef+'/demods/{}/timeconstant'.format(demod-1),tc)
    ziUhf.daq.setDouble('/'+uhfRef+'/demods/{}/rate'.format(demod-1),1/tc)
    
    path_ex=np.array([])
    
    try : 
        os.mkdir(path)
    except :
        print('Dossier existant')

    profondeur=np.linspace(start,stop,num_point)

#     for i,j in enumerate(profondeur) :
    for i in trange(len(profondeur)):
        j = profondeur[i]
        path_register=path+f'/vG3f=%smV_vg2f=%smV'%(round(j,3),round(coeff_dir*j,3))
        if i==0 :
            VG3(Vgw4+j)
            VG2(Vgw5+coeff_dir*j) 
            DAM.get_data_bin(total_time,path_register)
            
        else :     
            VG3(Vgw4+j)
            VG2(Vgw5+coeff_dir*j) 
            DAM.get_data_bin(total_time,path_register,header=False,affichage=False)
            
        path_ex=np.append(path_ex,path_register)  
               
    text_file = open(path+f'\paths.txt', "w")
    for i in path_ex : 
        text_file.write(i + f';')
    text_file.close()   
        
    return(path_ex)    



def Occupations_and_times(array,Threshold, Do_plot = False):
#     import time
    '''
    #### Function that takes as input an array, corresponding to a phase versus time trace ###

    array: must be an array of the time trace. First column = Time, Second column = phase 
    Threshold: value of the signal chosen to separate the two detected states
    
    returns the normlaized probablities of begin up or down, as well as the average times spent up and down in seconds

    '''
   
    T = array[:,0]
    PH = array[:,1]
    tstep = T[1]-T[0]
    Ttot = len(T)*tstep
    
    if Do_plot == True:
        f = plt.figure()
        f = plt.plot(T,PH)
    Ts_up = [0]
    Ts_down = [0]
#     t0 = time.time()
    j = 0
    for i,ph in enumerate(PH):
        if ph > Threshold:
            if i > 1 and PH[i-1] < Threshold:
                Ts_up.append(1)
                j = j+1
            elif i > 1 and PH[i-1] > Threshold:
                Ts_up[j] = Ts_up[j] + 1

    j = 0
    for i,ph in enumerate(PH):
        if ph < Threshold:
            if i > 1 and PH[i-1] < Threshold:
                Ts_down[j] = Ts_down[j] + 1  
            elif i > 1 and PH[i-1] > Threshold:
                Ts_down.append(1)
                j = j+1
    
    P_up = sum(Ts_up)/len(PH)
    P_down = sum(Ts_down)/len(PH)
    T_up = np.mean(Ts_up)*tstep    # time spent in the two different states
    T_down = np.mean(Ts_down)*tstep 
#     t1 = time.time()
#     print('Done in', t1-t0 , 's')
    return P_up,P_down,T_up,T_down


# pathh,-0.2,0.2,Threshold,str(round(j,3)),str(round(i,3))

def analyse_time_traces(path,start,stop,Threshold,G2f,G3f) :
    
    print(path)
    file = path+f'/time_traces/paths.txt'
    with open(file) as f:
        for line in f:
                paths = line.split(";")
#     Name = re.sub('../../exploration','',path)       
    Ps_up = []
    Ps_down = []
    Ts_up = []
    Ts_down = []
    for i in trange(len(paths)-1):
        path1 = paths[i]
        data = np.load(path1+'.npy')
        P_up,P_down,T_up,T_down = Occupations_and_times(data,Threshold, Do_plot = False)
        Ps_up.append(P_up)
        Ps_down.append(P_down)
        Ts_up.append(T_up)
        Ts_down.append(T_down)

    # Vg = np.linspace(-0.3,0.3,len(Ps_up))    
    Vg = np.linspace(start,stop,len(Ps_up))    

    ## Plot the occupations up/down:
    fig,ax = plt.subplots()
    plt.plot(Vg,Ps_up)
    plt.plot(Vg,Ps_down)
    plt.xlabel('$Vg_3$ (mV)',fontsize=18)
    plt.ylabel('$P_{in},P_{out}$',fontsize=18)
    ax.tick_params(labelsize=14)
    ax.set_title('Occupations up/down',size=18)
    fig.tight_layout()
    plt.savefig(path+f'/Occupation.png')

    ## Plot the tunnel rates:
    gamma_up = 1/np.array(Ts_up)
    gamma_down = 1/np.array(Ts_down)

    gamma_up[gamma_up>1e300]=0  
    gamma_down[gamma_down>1e300]=0  
    
    fig,ax = plt.subplots()
    
    plt.plot(Vg,gamma_up*1e-3,'+',label='$\Gamma_{out}$')
    plt.plot(Vg,gamma_down*1e-3,'+',label='$\Gamma_{in}$')
    


    if np.max(gamma_up)>50e3 or np.max(gamma_down)>50e3:
        plt.ylim(0,40)
        
    plt.xlabel('$V_{G3}$ (mV)',fontsize=18)
    plt.ylabel('$\Gamma_{in},\Gamma_{out}$ (kHz)',fontsize=18)
    ax.tick_params(labelsize=14)
    ax.set_title('Rates up/down',size=18)
    fig.tight_layout()
    plt.legend()
    plt.savefig(path+f'/Rates.png')
    
    path_register = f'..\exploration/2-all_Rates'
    title=f'gamma_rates'
    
    try : 
        os.mkdir(path_register)
    except :
        print('Dossier existant')

    fig.savefig(path_register+f'\G3=%s_G2=%s '%(str(int(float(G2f))),str(int(float(G3f))))+title,dpi=600)
    
    crossing=np.argmin(np.abs(gamma_up-gamma_down))
    
    return gamma_up[crossing] #, Vg[crossing]




def Elzouzou_left(path,start,stop,G2f,G3f,average,Npoints, Tempty,Tload, Tread,Vload=-0.1,Vread=0,Vempty=0.1) :
    # Number of averages to perform at each read level:
   
    namefile='C:\\Users\\g-gre-gre050402\\Documents\\Zurich Instruments\\LabOne\\WebServer\\awg\\src\\diagonal_pulse.seqc'    
    
    
    changetempty(namefile, Tempty) 
    changetload(namefile, Tload) 
    changetread(namefile, Tread) 
    
    # run_seq('dev2226','pulse_triggerdata_transfer.seqc')   
    # ziUhf.daq.setInt('/dev2226/demods/1/enable', 1)
    # ziUhf.daq.setInt('/dev2226/demods/0/enable', 1)
    
    
    
    acquisition_duration = Tempty+Tload+Tread  # length of time to record (s)
    
    
    
    
    # repetitions = 1000           # number of repetitions for the averaging
    # points = 71# number of points in the acquisition window (min=2)
    #efftc=acquisition_duration/10
    efftc=1/800e3
    
    # such that the effective Tc is 100ms 
    # repetitions=tc/efftc/5
    
    repetitions=average
    # daq_module.set('holdoff/time', 0)
    ziUhf.daq.setInt('/dev2226/demods/1/trigger', 33554432) # demodulator trigger set on AWGtrigger2 High
    # ziUhf.daq.setInt('/dev2226/demods/0/trigger', 33554432)


    # ziUhf.daq.setDouble('/dev2226/demods/0/rate', 800e3)
    # ziUhf.daq.setDouble('/dev2226/demods/1/rate', 800e3)
    # ziUhf.daq.setDouble('/dev2226/demods/0/rate', 2e6)
    # ziUhf.daq.setDouble('/dev2226/demods/1/rate', 800e3)
    ziUhf.daq.setDouble('/dev2226/demods/1/rate', 800e3)
    ziUhf.daq.setInt('/dev2226/demods/1/order', 1)
    
    points=int(acquisition_duration*ziUhf.daq.getDouble('/dev2226/demods/1/rate'))
    
    
    ziUhf.daq.setDouble('/dev2226/demods/1/timeconstant', efftc)
    ziUhf.daq.setDouble('/dev2226/demods/1/timeconstant', efftc)
    ziUhf.daq.setInt('/dev2226/awgs/0/enable', 1)      # 1 = enable;   0 = disabled
    #add also check if meas start, otherwise restart AWG
    ziUhf.daq.sync()
    
    #Trigger type used. Some parameters are only valid for special trigger types.
        #0 = trigger off
        #1 = analog edge trigger on source
        #2 = digital trigger mode on DIO source
        #3 = analog pulse trigger on source
        #4 = analog tracking trigger on source
        #5 = change trigger
        #6 = hardware trigger on trigger line source
        #7 = tracking edge trigger on source
        #8 = event count trigger on counter source
        
    ziUhf.daq.sync()
    trigger_setting = [['dataAcquisitionModule/triggernode', '/dev2226/demods/1/sample.TrigAWGTrig3'],  # trigger node is AWG trigger number 3 
    #                   ['dataAcquisitionModule/type', 2],      
                       ['dataAcquisitionModule/type', 6],                                          # this setting is related to the AWG trigger
                       ['dataAcquisitionModule/edge', 1],                                               # trigger on the positive edge. 1 = positive, 2=negative
                       ['dataAcquisitionModule/count', 1],                                              # number of trigger events to count
                       ['dataAcquisitionModule/holdoff/time', 0],                                       # hold off time
                       ['dataAcquisitionModule/holdoff/count', 0],                                      # hold off count
                       ##careful
                       ['dataAcquisitionModule/delay', 0e-6], #0                                       # trigger delay (s)
                       ##
                       ['dataAcquisitionModule/endless', 0]]                                            # endless disabled = 0
    
    
    grid_setting =    [['dataAcquisitionModule/grid/mode', 2],                          # mode. 2 = Linear interpolation 
                       ['dataAcquisitionModule/grid/cols', points],                     # number of points in the acquisition window
                       ['dataAcquisitionModule/duration', acquisition_duration],        # length of time to record (s)
                       ['dataAcquisitionModule/grid/rows', 1],                          # rows
                       ['dataAcquisitionModule/grid/direction', 0],                     # scan direction. 0 = forwardphase_pulsed = SpecialParameters.Pulsed_readout(ziUhf, repetitions, returnOnePoint=False)
                       ['dataAcquisitionModule/grid/repetitions', repetitions],         # number of repetitions for the averaging
                       ['dataAcquisitionModule/awgcontrol', 1],                         # set the AWG control
                       ['dataAcquisitionModule/save/fileformat', 1]]                    # 1 = CSV format 
    
    phase_trigS= SpecialParameters.Pulsed_readout_S(ziUhf, repetitions, returnOnePoint=False)
    phase_trigD= SpecialParameters.Pulsed_readout_D(ziUhf, repetitions, returnOnePoint=False)
    
    phase_trigS.setSettings(trigger_setting, grid_setting)
    phase_trigD.setSettings(trigger_setting, grid_setting)
    
    
    # Duration of the time trace to record:
    

    # Vreads = np.arange(-0.3,0.015,0.0005)

    # Vread = Vreads[i]      
    t=np.linspace(0,acquisition_duration,points)
    
    phaseDarray=[]
    phaseSarray=[]
    amp=[]
    # Npoints=101

    Vreads=np.linspace(start,stop,Npoints)##real amplitudes in mV on G3
    
    # ampliAWG(0.2)
    
    for i in range(0,Npoints):
        print(i)
        amplimV=Vreads[i]
    
        
        Readlevel(amplimV)
        ziUhf.daq.setInt('/dev2226/sigouts/0/enables/5', 1)
        ziUhf.daq.setInt('/dev2226/sigouts/0/enables/5', 1)
    
        # phaseSarray.append(phase_trigS())
        phaseDarray.append(phase_trigS())
    # ziUhf.daq.setInt('/dev2226/sigouts/1/on', 0)    
    
    # phaseS=[]
    # for i in range(0,Npoints):
    #     phaseS.append(phaseSarray[i][0])
        
    phaseD=[]
    for i in range(0,Npoints):
        phaseD.append(phaseDarray[i][0])
        


    M=phaseD
    #Enregistrement des datas dans un sous dossier convenablement nommé 
    Field = Bfield_Hon()
    pathelzou=path + f'/El_Zeerman'
    
    try : 
        os.mkdir(pathelzou)
    except :
        print('Dossier existant')
    
    np.save(pathelzou+f'/El_Zeerman_data'+str(round(Field,2)),M) 
    np.save(pathelzou+f'/El_Zeerman_times'+str(round(Field,2)),t)
    np.save(pathelzou+f'/El_Zeerman_Vread'+str(round(Field,2)),Vreads)
    
    title=str(np.round(Bfield(),3))+'Elzermanseq_ampliAWG'+str(np.round(ampliAWG(),2))+'_Tempty'+str(Tempty)+'Tload'+str(Tload)+'Tread'+str(Tread)+'g2'+str(VG2())+'mV'
    
    pathtxt=pathelzou+'//'+title+'.txt'
    
    Headertxt=f'Tload=%s ; Tread=%s ; Tempty=%s ; Vload=%s ; Vread=%s ; Vempty=%s ; ' %(Tload,Tread,Tempty,Vload,Vread,Vempty)
    Headertxt=Headertxt + f'\n' 
    Headertxt=f'awg.ch1.awg_amplitude=%s Volt' %(ampliAWG())
    Headertxt=Headertxt + f'\n' 
    Headertxt=Headertxt + 'X -> Time (sec) ; Y -> Phase (Rad)'
    
    np.savetxt(pathtxt,[],fmt='%.6e',header=Headertxt) 
    
    #Enregistrement de la figure tracée 
    
    fig,ax = plt.subplots()
    # plt.pcolor(t*1e6,Vreads,np.transpose(M))
    plt.pcolor(t*1e6,Vreads,M)
    plt.ylabel('$V_{read}(mV)$',fontsize=18)
    plt.xlabel('t ($\mu$s)',fontsize=18)
    cb=plt.colorbar()
    cb.set_label('$\phi_S$ (rad)')
    
    ax.tick_params(labelsize=14)
    ax.set_title('B='+str(Bfield())+'g2='+str(np.round(VG2(),3))+'mV Aawg'+str(np.round(ampliAWG(),3)),size=18)
    fig.tight_layout()

    now=datetime.datetime.now()
    dayFolder= datetime.date.isoformat(now)
    try:
        os.makedirs(folder2+'\\'+dayFolder)
    except IOError:
        donothing=1
        
    plt.savefig(folder2+'\\'+dayFolder+'\\'+title+'.png')
    np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'.txt',M)
    
    print(path)
    
    fig.savefig(path+'\\'+title+'.png',dpi=600)
       
    path_register = f'..\exploration/3-all_Elzouzous'

    
    try : 
        os.mkdir(path_register)
    except :
        print('Dossier existant')


    fig.savefig(path_register+'\\G3='+str(np.round(VG3(),3))+'_g2='+str(np.round(VG2(),3))+'_'+title+'.png')

def plotmeta():    
    acquisition_duration =40e-6  # length of time to record (s)
    repetitions = 1000         # number of repetitions for the averaging
    delay=200e-6
    
    efftc=4e-6
    ziUhf.daq.setDouble('/dev2226/demods/1/rate', 400e3)
    ziUhf.daq.setDouble('/dev2226/demods/0/rate', 400e3)
    # ziUhf.daq.setDouble('/dev2226/demods/1/rate', 1e6)
    # ziUhf.daq.setDouble('/dev2226/demods/0/rate', 1e6)
    
    
    repetitions=200
    
    ziUhf.daq.setInt('/dev2226/demods/1/trigger', 33554432) # demodulator trigger set on AWGtrigger2 High
    ziUhf.daq.setInt('/dev2226/demods/0/trigger', 33554432) # demodulator trigger set on AWGtrigger2 High
    
    ziUhf.daq.setInt('/dev2226/demods/1/order', 1)
    ziUhf.daq.setInt('/dev2226/demods/0/order', 1)
    points=int(acquisition_duration*ziUhf.daq.getDouble('/dev2226/demods/0/rate'))
    # points=3
    
    ziUhf.daq.setDouble('/dev2226/demods/0/timeconstant', efftc)
    ziUhf.daq.setDouble('/dev2226/demods/1/timeconstant', efftc)
    #ziUhf.daq.setInt('/dev2365/awgs/0/enable', 1)      # 1 = enable;   0 = disabled
    #add also check if meas start, otherwise restart AWG
    ziUhf.daq.sync()
    
    #Trigger type used. Some parameters are only valid for special trigger types.
        #0 = trigger off
        #1 = analog edge trigger on source
        #2 = digital trigger mode on DIO source
        #3 = analog pulse trigger on source
        #4 = analog tracking trigger on source
        #5 = change trigger
        #6 = hardware trigger on trigger line source
        #7 = tracking edge trigger on source
        #8 = event count trigger on counter source
        
    ziUhf.daq.sync()
    trigger_setting = [['dataAcquisitionModule/triggernode', '/dev2226/demods/0/sample.TrigAWGTrig3'],  # trigger node is AWG trigger number 3 
    #                   ['dataAcquisitionModule/type', 2],      
                       ['dataAcquisitionModule/type', 6],                                          # this setting is related to the AWG trigger
                       ['dataAcquisitionModule/edge', 1],                                               # trigger on the positive edge. 1 = positive, 2=negative
                       ['dataAcquisitionModule/count', 1],                                              # number of trigger events to count
                       ['dataAcquisitionModule/holdoff/time', 0],                                       # hold off time
                       ['dataAcquisitionModule/holdoff/count', 0],                                      # hold off count
                       ##careful
                       ['dataAcquisitionModule/delay', delay], #0                                       # trigger delay (s)
                       ##
                       ['dataAcquisitionModule/endless', 0]]                                            # endless disabled = 0
    
    
    grid_setting =    [['dataAcquisitionModule/grid/mode', 2],                          # mode. 2 = Linear interpolation 
                       ['dataAcquisitionModule/grid/cols', points],                     # number of points in the acquisition window
                       ['dataAcquisitionModule/duration', acquisition_duration],        # length of time to record (s)
                       ['dataAcquisitionModule/grid/rows', 1],                        # rows
                       ['dataAcquisitionModule/grid/direction', 0],                     # scan direction. 0 = forwardphase_pulsed = SpecialParameters.Pulsed_readout(ziUhf, repetitions, returnOnePoint=False)
                       ['dataAcquisitionModule/grid/repetitions', repetitions],         # number of repetitions for the averaging
                       ['dataAcquisitionModule/awgcontrol', 1],                         # set the AWG control
                       ['dataAcquisitionModule/save/fileformat', 1]]                    # 1 = CSV format 
    
    phase_trigS= SpecialParameters.Pulsed_readout_S(ziUhf, repetitions, returnOnePoint=True)
    phase_trigD= SpecialParameters.Pulsed_readout_D(ziUhf, repetitions, returnOnePoint=True)
    
    phase_trigS.setSettings(trigger_setting, grid_setting)
    phase_trigD.setSettings(trigger_setting, grid_setting)
    
    ziUhf.daq.setInt('/dev2226/sigouts/0/enables/5', 1)
    ziUhf.daq.setInt('/dev2226/sigouts/0/enables/4', 1)
    
    
    
    print('tc='+str(efftc)+'  rep='+str(repetitions))
    #for symmetric pulses
    #print('timeperpoint='+str(repetitions*twait()*2))
    print('timeperpoint='+str(repetitions*acquisition_duration))
    
    # ziUhf.daq.setInt('/dev2226/sigouts/1/on', 0)    
    ziUhf.daq.setInt('/dev2226/sigouts/0/enables/4', 1)
    ziUhf.daq.setInt('/dev2226/sigouts/0/enables/5', 1)
    # ziUhf.daq.setInt('/dev2226/sigouts/0/on', 0)    
    # ziUhf.daq.set('/module/c0p1t10p1cf0/awgModule/awg/enable', 0)
    ziUhf.daq.setInt('/dev2226/awgs/0/enable', 1)
    # ziUhf.daq.setInt('/dev2226/awgs/0/enable', 0)
    
    
    
    
    
    name=str(Bfield())+'T_phiS_METASTABLE_30degpulse_acquire50usin02_delay'+str(delay)+'_G3vsG4comp_AWG'+str(ampliAWG())+'_VG3'+str(VG3())+'mV_G4'+str(VG4())+'mV'
    a,dataid,c,d=sweep2D(VG3comp,-866,-861,51,0.02,VG4comp,-813,-808,51,0.02,phase_trigS,phase_trigD)
    
    plot_by_id(dataid)
    save2plots(name,dataid)
    
    
    
def analyse_time_traces_interdot(path,start,stop,startG3,stopG3,Threshold) :
    
    print(path)
    file = path+'\\paths.txt'
    with open(file) as f:
        for line in f:
                paths = line.split(";")
#     Name = re.sub('../../exploration','',path)       
    Ps_up = []
    Ps_down = []
    Ts_up = []
    Ts_down = []
    for i in trange(len(paths)-1):
        path1 = paths[i]
        data = np.load(path1+'.npy')
        P_up,P_down,T_up,T_down = Occupations_and_times(data,Threshold, Do_plot = False)
        Ps_up.append(P_up)
        Ps_down.append(P_down)
        Ts_up.append(T_up)
        Ts_down.append(T_down)

    # Vg = np.linspace(-0.3,0.3,len(Ps_up))   
    
    eps=np.sqrt((start-stop)**2 +(startG3-stopG3)**2) 
    
    Vg = np.linspace(0,eps,len(Ps_up))    

    ## Plot the occupations up/down:
    fig,ax = plt.subplots()
    plt.plot(Vg,Ps_up)
    plt.plot(Vg,Ps_down)
    plt.xlabel('$\epsilon$ (mV)',fontsize=18)
    plt.ylabel('$P_{11},P_{02}$',fontsize=18)
    ax.tick_params(labelsize=14)
    ax.set_title('Occupations'+str(Bfield())+'T',size=18)
    fig.tight_layout()
    plt.savefig(path+'\\'+str(Bfield())+'T_Occupation.png')

    ## Plot the tunnel rates:
    gamma_up = 1/np.array(Ts_up)
    gamma_down = 1/np.array(Ts_down)


    crossing=np.argmin(np.abs(gamma_up-gamma_down))
    gamma_up[gamma_up>1e6]=0  
    gamma_down[gamma_down>1e6]=0  
    
    fig,ax = plt.subplots()
    
    plt.plot(Vg,gamma_up*1e-3,'+',label='$\Gamma_{out}$')
    plt.plot(Vg,gamma_down*1e-3,'+',label='$\Gamma_{in}$')
    


    if np.max(gamma_up)>200e3 or np.max(gamma_down)>200e3:
        plt.ylim(0,200)
        
    plt.xlabel('$\epsilon$ (mV)',fontsize=18)
    plt.ylabel('$\Gamma_{in},\Gamma_{out}$ (kHz)',fontsize=18)
    ax.tick_params(labelsize=14)
    ax.set_title('Rates '+str(Bfield())+'T',size=18)
    fig.tight_layout()
    plt.legend()
    plt.savefig(path+'//'+str(Bfield())+'T_Rates.png')

    # title='gamma_rates'
    
    # try : 
    #     os.mkdir(path_register)
    # except :
    #     print('Dossier existant')

    # fig.savefig(path+'\\'+title,dpi=600)
    
    
    # if gamma_up[crossing]<2:
    #     for i in range (0,len(gamma_up)):
    #         if gamma_up[i]==0:
    #             gamma_up[i]= float("NaN")
    # crossing=np.argmin(np.abs(gamma_up-gamma_down))
        

    
    return gamma_up[crossing] #, Vg[crossing]     
        
def register_time_trace_interdot(DAM,startG4,stopG4,startG3,stopG3,num_point,tc,total_time,demod,path,path2) :
    
    ziUhf.daq.setDouble('/'+uhfRef+'/demods/{}/timeconstant'.format(demod-1),tc)
    ziUhf.daq.setDouble('/'+uhfRef+'/demods/{}/rate'.format(demod-1),1/tc)
    
    path_ex=np.array([])
    
    try : 
        os.mkdir(path)
    except :
        print('Dossier existant')
    try : 
        os.mkdir(path2)
    except :
        print('Dossier existant')

    G4ar=np.linspace(startG4,stopG4,num_point)
    
    G3ar=np.linspace(startG3,stopG3,num_point)
#     for i,j in enumerate(profondeur) :
    for i in trange(len(G4ar)):
        path_register=path2+f'/vG3=%smV_vg4=%smV'%(round(VG3(),3),round(VG4(),3))
        if i==0 :
            # VG3(Vgw4+j)
            # VG4(Vgw5+coeff_dir*j) 
            VG4comp(G4ar[i])
            VG3comp(G3ar[i])
            DAM.get_data_bin(total_time,path_register)
            
        else :     
            VG4comp(G4ar[i])
            VG3comp(G3ar[i])

            DAM.get_data_bin(total_time,path_register,header=False,affichage=False)
            
        path_ex=np.append(path_ex,path_register)  
               
    text_file = open(path+f'\paths.txt', "w")
    for i in path_ex : 
        text_file.write(i + f';')
    text_file.close()   
        
    return(path_ex)    



def Occupations_and_times(array,Threshold, Do_plot = False):
#     import time
    '''
    #### Function that takes as input an array, corresponding to a phase versus time trace ###

    array: must be an array of the time trace. First column = Time, Second column = phase 
    Threshold: value of the signal chosen to separate the two detected states
    
    returns the normlaized probablities of begin up or down, as well as the average times spent up and down in seconds

    '''
   
    T = array[:,0]
    PH = array[:,1]
    tstep = T[1]-T[0]
    Ttot = len(T)*tstep
    
    if Do_plot == True:
        f = plt.figure()
        f = plt.plot(T,PH)
    Ts_up = [0]
    Ts_down = [0]
#     t0 = time.time()
    j = 0
    for i,ph in enumerate(PH):
        if ph > Threshold:
            if i > 1 and PH[i-1] < Threshold:
                Ts_up.append(1)
                j = j+1
            elif i > 1 and PH[i-1] > Threshold:
                Ts_up[j] = Ts_up[j] + 1

    j = 0
    for i,ph in enumerate(PH):
        if ph < Threshold:
            if i > 1 and PH[i-1] < Threshold:
                Ts_down[j] = Ts_down[j] + 1  
            elif i > 1 and PH[i-1] > Threshold:
                Ts_down.append(1)
                j = j+1
    
    P_up = sum(Ts_up)/len(PH)
    P_down = sum(Ts_down)/len(PH)
    T_up = np.mean(Ts_up)*tstep    # time spent in the two different states
    T_down = np.mean(Ts_down)*tstep 
#     t1 = time.time()
#     print('Done in', t1-t0 , 's')
    return P_up,P_down,T_up,T_down


# pathh,-0.2,0.2,Threshold,str(round(j,3)),str(round(i,3))





        





def fit_interdot(startG4,stopG4,startG3,stopG3):
    
    detuningPoint1 = [startG3,startG4]  #TPC #G3,G4
    detuningPoint2 = [stopG3,stopG4] 
    
    detpoints=201
    detuning = qc.combine(VG3, VG4, name = 'detuning', unit= 'points')
    eps=np.sqrt((detuningPoint1[0]-detuningPoint2[0])**2 +(detuningPoint1[1]-detuningPoint2[1])**2) 
    VG3comp(detuningPoint1[0])
    VG4comp(detuningPoint1[1])
    
    det=generateEpsilonAxis(detuningPoint1, detuningPoint2, detpoints)
    eps=np.sqrt((detuningPoint1[0]-detuningPoint2[0])**2 +(detuningPoint1[1]-detuningPoint2[1])**2) 
    epsilon=np.linspace(-eps/2,eps/2,detpoints)
    
    now=datetime.datetime.now()
    dayFolder= datetime.date.isoformat(now)
    try:
            os.makedirs(folder2+'\\'+dayFolder)
    except IOError:
            donothing=1
    
    tag='TP0_'
    phases=[]
    
    
    
    phasedet_D=[]
    phasedet_S=[]
    for i in range(0,len(det)):
    
        VG3comp(det[i][0])
        VG4comp(det[i][1])
        time.sleep(0.02)
        phasedet_S.append(ph2())
        phasedet_D.append(ph1())
        
    datasmooth_S=scipy.signal.savgol_filter(np.ravel(phasedet_S),11, 3)
    phimin=np.min(datasmooth_S)
    phimax=np.max(datasmooth_S)
    argmin=np.argmin(datasmooth_S)
    kmin=0
    kmax=0
    
    philim_S=phimin+(phimax-phimin)/2
    T=0.44
    sigmaphi=0.5#deg
    # for k in range(0,len(data_set)):
    #         if ((data_get[0][k]>=(philim-sigmaphi) and data_get[0][k]<=(philim+sigmaphi)) and kmax==0):
    #             kmax=k
    for k in range(0,len(epsilon)):
        if ((  datasmooth_S[k]>=(philim_S-sigmaphi) and   datasmooth_S[k]<=(philim_S+sigmaphi)) and kmax==0):
            kmax=k
            print('ok')
    
        
    # VG3comp(det[kmax][0])
    # VG4comp(det[kmax][1])
    # VG3comp(det[kmax][0])
    # VG4comp(det[kmax][1])
    
    # xaxis=np.multiply(np.subtract(data_set,data_set[kmax]),1e-3)
    xaxis=np.multiply(np.subtract(epsilon,epsilon[kmax]),1e-3)
    datasmooth2=np.subtract(datasmooth_S,phimin)
    
    xaxis2=np.array(xaxis,dtype=float)
    datasmooth2=np.array(datasmooth2,dtype=float)
    
    
    xaxis2=np.reshape(xaxis2,201)
    datasmooth2=np.reshape(datasmooth2,201)
    
    fig, ax = plt.subplots()
    ax.set_xlabel('$\epsilon$ (V)',fontsize=fontSize)
    ax.set_ylabel('$\phi_S $(rad)',fontsize=fontSize)
    
    plt.title('Fit at T='+str(T)+'K')
    plt.plot(xaxis,datasmooth2,'b+',label='data@'+str(T)+'K')#mV on x  
    plt.legend(loc='upper right')
    plt.show()
    
    
    
    alpha=0.4
    const=phimin
    offset=phimin+(phimax-phimin)
    
     
    popt,pcov = curve_fit(interdotfit_chargesensor,xaxis2,datasmooth2,p0=[alpha,0,1],maxfev=10000) 
    plt.plot(xaxis2,interdotfit_chargesensor(xaxis2,*popt))    
    
    
    alpha=popt[0] 
    
    er=np.sqrt(np.diag(pcov))
    erroralpha=er[0]
    # errortunnel=er[3]
    # print('Teff='+str(Teff))
    # Tarray.append(Teff)
    # errorTarray.append(errortemp)
    
    # tunnelarray.append(tunnel)
    # tunnelarrayerr.append(errortunnel)
    
    # errortunnel=errortunnel/h*10e-9#conv to Ghz
    plt.plot(xaxis,interdotfit_chargesensor(xaxis2,*popt),'r',label='alpha='+str( round(alpha,2)) +'$\pm$'+str( round(erroralpha,2))+'_eV/V')#,t='+str( round(tunnel,3))+'$\pm$'+str(round(errortunnel,3))+'_GHz, alpha='+str(alpha))
    #    plt.plot(xaxis,interdotfit_chargesensor(xaxis,*popt),'r',label='Teff='+str( round(Teff,2)) +'$\pm$'+str( round(errortemp,2))+'_K,t='+str( round(tunnel,3))+'$\pm$'+str(round(errortunnel,3))+'_GHz, alpha='+str(alpha))
    plt.legend(loc='upper right')
    plt.show()
    name='phi_S_0p44K_findalphadetunig_tnegligible__G4init'+str(startG4)+'mV_1dscan-'+str(Bfield())+'_T_'
    # fig.savefig(foldername2+'0.44K_Tonly_TP9_1dscan-'+str(Bfield())+'_T_ampliAWG'+str(ampliAWG())+'.png') 
    # np.savetxt(foldername2+'0.44K_Tonly_TP9_1dscan-'+str(Bfield())+'_T_ampliAWG'+str(ampliAWG())+'.txt',datasmooth2)
    
    plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
    np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',datasmooth2)
    
    #############################################
    
    datasmooth_D=scipy.signal.savgol_filter(np.ravel(phasedet_D),11, 3)
    phimin=np.min(datasmooth_D)
    phimax=np.max(datasmooth_D)
    argmin=np.argmin(datasmooth_D)
    kmin=0
    kmax=0
    
    philim_D=phimin+(phimax-phimin)/2
    T=0.44
    sigmaphi=0.5#deg
    # for k in range(0,len(data_Det)):
    #         if ((data_get[0][k]>=(philim-sigmaphi) and data_get[0][k]<=(philim+sigmaphi)) and kmax==0):
    #             kmax=k
    for k in range(0,len(epsilon)):
        if ((  datasmooth_D[k]>=(philim_D-sigmaphi) and   datasmooth_D[k]<=(philim_D+sigmaphi)) and kmax==0):
            kmax=k
            print('ok')
    
        
    VG3comp(det[kmax][0])
    VG4comp(det[kmax][1])
    VG3comp(det[kmax][0])
    VG4comp(det[kmax][1])
    
    # xaxis=np.multiply(np.subtract(data_Det,data_Det[kmax]),1e-3)
    xaxis=np.multiply(np.subtract(epsilon,epsilon[kmax]),1e-3)
    datasmooth2=np.subtract(datasmooth_D,phimin)
    
    xaxis2=np.array(xaxis,dtype=float)
    datasmooth2=np.array(datasmooth2,dtype=float)
    
    
    xaxis2=np.reshape(xaxis2,201)
    datasmooth2=np.reshape(datasmooth2,201)
    
    fig, ax = plt.subplots()
    ax.set_xlabel('$\epsilon$ (V)',fontsize=fontSize)
    ax.set_ylabel('$\phi_D $(rad)',fontsize=fontSize)
    
    plt.title('Fit at T='+str(T)+'K')
    plt.plot(xaxis,datasmooth2,'b+',label='data@'+str(T)+'K')#mV on x  
    plt.legend(loc='upper right')
    plt.show()
    
    
    
    alpha=0.55
    const=phimin
    offset=phimin+(phimax-phimin)
    
     
    popt,pcov = curve_fit(interdotfit_chargesensor,xaxis2,datasmooth2,p0=[alpha,0,1],maxfev=10000) 
    plt.plot(xaxis2,interdotfit_chargesensor(xaxis2,*popt))    
    
    
    alpha=popt[0] 
    
    er=np.sqrt(np.diag(pcov))
    erroralpha=er[0]
    # errortunnel=er[3]
    # print('Teff='+str(Teff))
    # Tarray.append(Teff)
    # errorTarray.append(errortemp)
    
    # tunnelarray.append(tunnel)
    # tunnelarrayerr.append(errortunnel)
    
    # errortunnel=errortunnel/h*10e-9#conv to Ghz
    plt.plot(xaxis,interdotfit_chargesensor(xaxis2,*popt),'r',label='alpha='+str( round(alpha,2)) +'$\pm$'+str( round(erroralpha,2))+'_eV/V')#,t='+str( round(tunnel,3))+'$\pm$'+str(round(errortunnel,3))+'_GHz, alpha='+str(alpha))
    #    plt.plot(xaxis,interdotfit_chargesensor(xaxis,*popt),'r',label='Teff='+str( round(Teff,2)) +'$\pm$'+str( round(errortemp,2))+'_K,t='+str( round(tunnel,3))+'$\pm$'+str(round(errortunnel,3))+'_GHz, alpha='+str(alpha))
    plt.legend(loc='upper right')
    plt.show()
    name='phiD_0p44K_findalphadetunig_tnegligible_G4init'+str(startG4)+'mV_1dscan-'+str(Bfield())+'_T_'
    # fig.savefig(foldername2+'0.44K_Tonly_TP9_1dscan-'+str(Bfield())+'_T_ampliAWG'+str(ampliAWG())+'.png') 
    # np.savetxt(foldername2+'0.44K_Tonly_TP9_1dscan-'+str(Bfield())+'_T_ampliAWG'+str(ampliAWG())+'.txt',datasmooth2)
    
    plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
    np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',datasmooth2)

    return philim_S,philim_D


def blopIQ_interdot(DAM,tc,timetot,demod,path,title='I/Q measure') :
    
    try : 
        os.mkdir(path)
    except :
        print('Dossier existant')
    # try : 
    #     os.mkdir(path2)
    # except :
    #     print('Dossier existant')
    ziUhf.daq.setDouble('/'+uhfRef+'/demods/{}/timeconstant'.format(demod-1),tc)
    ziUhf.daq.setDouble('/'+uhfRef+'/demods/{}/rate'.format(demod-1),1/tc)
    
    pathtxt=path+'\\'+title+'.txt'

    DAM.get_data_txt(timetot,pathtxt,'x','y',affichage=False)

    data=np.loadtxt(pathtxt)
    file=open(pathtxt)
    read=file.read()
    file.close()
    read=read[1:read.find('\n')]
    parameters=read.split(';')

    for i,stringi in enumerate(parameters) :
        if parameters[i].find('x')>=0 :
            xvalues=data[:,i]
            xlabel=stringi
        if parameters[i].find('y')>=0 :
            yvalues=data[:,i]
            ylabel=stringi

    fig = plt.figure(figsize=(10, 10))
    grid = plt.GridSpec(4, 4, hspace=0.3, wspace=0.3)
    
    size = 14
    
    main_ax = fig.add_subplot(grid[:-1, 1:])
    main_ax.set_title('I/Q measure',size=size)
    main_ax.ticklabel_format(axis='both',style='sci',scilimits=[-6,-6])
#     main_ax.set_aspect('equal')

    y_hist = fig.add_subplot(grid[:-1, 0], xticklabels=[], sharey=main_ax)
    y_hist.ticklabel_format(axis='y',style='sci',scilimits=[-6,-6])
    y_hist.set_ylabel(ylabel,fontsize=size)

    x_hist = fig.add_subplot(grid[-1, 1:], yticklabels=[], sharex=main_ax)
    x_hist.ticklabel_format(axis='x',style='sci',scilimits=[-6,-6])
    x_hist.set_xlabel(xlabel,fontsize=size)

    color='darkorange'
    alpha=0.8
    # scatter points on the main axes
    main_ax.plot(xvalues, yvalues, 'ok', markersize=3, alpha=0.2,color=color)
    main_ax.set_aspect('equal')

    # histogram on the attached axes
    x_hist.hist(xvalues, 200,
                orientation='vertical', color=color,alpha=alpha)
    x_hist.invert_yaxis()

    y_hist.hist(yvalues, 200,
                orientation='horizontal', color=color,alpha=alpha)
    y_hist.invert_xaxis()
    
    main_ax.tick_params(labelsize=14)
    x_hist.tick_params(labelsize=14)
    y_hist.tick_params(labelsize=14)

    fig.tight_layout()

    
    fig.savefig(path+'\\'+title+'.png',dpi=600)
    
    



def draw_multiple_bbl_interdot(path,path_register) :

    fig = plt.figure(figsize=(10, 10))
    grid = plt.GridSpec(4, 4, hspace=0.3, wspace=0.3)
    size = 14
    main_ax = fig.add_subplot(grid[:-1, 1:])
    main_ax.set_title('I/Q measure',size=size)
    main_ax.ticklabel_format(axis='both',style='sci',scilimits=[-6,-6])

    y_hist = fig.add_subplot(grid[:-1, 0], xticklabels=[], sharey=main_ax)
    y_hist.ticklabel_format(axis='y',style='sci',scilimits=[-6,-6])

    x_hist = fig.add_subplot(grid[-1, 1:], yticklabels=[], sharex=main_ax)
    x_hist.ticklabel_format(axis='x',style='sci',scilimits=[-6,-6])
    
    color_all=['darkorange','tomato','blue','green','black']
    
    for j,pathh in enumerate(path) :
        data=np.loadtxt(pathh)
        file=open(pathh)
        read=file.read()
        file.close()
        read=read[1:read.find('\n')]
        parameters=read.split(';')

        for i,stringi in enumerate(parameters) :
            if parameters[i].find('x')>=0 :
                xvalues=data[:,i]
                xlabel=stringi
            if parameters[i].find('y')>=0 :
                yvalues=data[:,i]
                ylabel=stringi

        color=color_all[j]
        alpha=0.8
        # scatter points on the main axes
        main_ax.plot(xvalues, yvalues, 'ok', markersize=3, alpha=0.2,color=color)

        # histogram on the attached axes
        x_hist.hist(xvalues, 200,
                    orientation='vertical', color=color,alpha=alpha)
        x_hist.invert_yaxis()

        y_hist.hist(yvalues, 200,
                    orientation='horizontal', color=color,alpha=alpha)
        y_hist.invert_xaxis()
        
    y_hist.set_ylabel(ylabel,fontsize=size)
    x_hist.set_xlabel(xlabel,fontsize=size)
    main_ax.tick_params(labelsize=14)
    x_hist.tick_params(labelsize=14)
    y_hist.tick_params(labelsize=14)
    
    title='\\IQ_double_bbl_tc'+str(tc)
    
    fig.savefig(path_register+f'/'+title,dpi=600)
    
    # patth = f'..\exploration/1-all_Bubbles'

    fig.savefig(path_register+title,dpi=600)

    fig.tight_layout()
    
    



def fit_interdot_G3(startG3,stopG3,startG4):
    
    stopG4=startG4
    num_point=201
    G4ar=np.linspace(startG4,stopG4,num_point)
    
    G3ar=np.linspace(startG3,stopG3,num_point)
    
    
    # eps=np.sqrt((detuningPoint1[0]-detuningPoint2[0])**2 +(detuningPoint1[1]-detuningPoint2[1])**2) 
    VG3comp(G3ar[0])
    # VG4comp(G3ar[0])
    
    # det=generateEpsilonAxis(detuningPoint1, detuningPoint2, detpoints)
    eps=np.sqrt((startG3-stopG3)**2)
    epsilon=np.linspace(-eps/2,eps/2,len(G3ar))
    
    
    tag='TP1_'
    phases=[]
    
    
    
    # phasedet_D=[]
    phasedet_S=[]
    for i in range(0,len(G3ar)):
    
        VG3comp(G3ar[i])
        # VG4comp(det[i][1])
        time.sleep(0.02)
        phasedet_S.append(ph2())
        # phasedet_D.append(ph1())
        
    datasmooth_S=scipy.signal.savgol_filter(np.ravel(phasedet_S),11, 3)
    phimin=np.min(datasmooth_S)
    phimax=np.max(datasmooth_S)
    argmin=np.argmin(datasmooth_S)
    kmin=0
    kmax=0
    
    philim_S=phimin+(phimax-phimin)/2
    T=0.44
    sigmaphi=0.5#deg
    # for k in range(0,len(data_set)):
    #         if ((data_get[0][k]>=(philim-sigmaphi) and data_get[0][k]<=(philim+sigmaphi)) and kmax==0):
    #             kmax=k
    for k in range(0,len(epsilon)):
        if ((  datasmooth_S[k]>=(philim_S-sigmaphi) and   datasmooth_S[k]<=(philim_S+sigmaphi)) and kmax==0):
            kmax=k
            print('ok')
    
        
    VG3comp(G3ar[kmax])
    # VG4comp(G3ar[kmax][1])
    # VG3comp(det[kmax][0])
    # VG4comp(det[kmax][1])
    
    # xaxis=np.multiply(np.subtract(data_set,data_set[kmax]),1e-3)
    xaxis=np.multiply(np.subtract(epsilon,epsilon[kmax]),1e-3)
    datasmooth2=np.subtract(datasmooth_S,phimin)
    
    xaxis2=np.array(xaxis,dtype=float)
    datasmooth2=np.array(datasmooth2,dtype=float)
    
    
    xaxis2=np.reshape(xaxis2,201)
    datasmooth2=np.reshape(datasmooth2,201)
    
    fig, ax = plt.subplots()
    ax.set_xlabel('$\epsilon$ (V)',fontsize=fontSize)
    ax.set_ylabel('$\phi_S $(rad)',fontsize=fontSize)
    
    plt.title('Fit at T='+str(T)+'K')
    plt.plot(xaxis,datasmooth2,'b+',label='data@'+str(T)+'K')#mV on x  
    plt.legend(loc='upper right')
    plt.show()
    
    
    
    alpha=0.4
    const=phimin
    offset=phimin+(phimax-phimin)
    
     
    popt,pcov = curve_fit(interdotfit_chargesensor,xaxis2,datasmooth2,p0=[alpha,0,1],maxfev=10000) 
    plt.plot(xaxis2,interdotfit_chargesensor(xaxis2,*popt))    
    
    
    alpha=popt[0] 
    
    er=np.sqrt(np.diag(pcov))
    erroralpha=er[0]
    # errortunnel=er[3]
    # print('Teff='+str(Teff))
    # Tarray.append(Teff)
    # errorTarray.append(errortemp)
    
    # tunnelarray.append(tunnel)
    # tunnelarrayerr.append(errortunnel)
    
    # errortunnel=errortunnel/h*10e-9#conv to Ghz
    plt.plot(xaxis,interdotfit_chargesensor(xaxis2,*popt),'r',label='alpha='+str( round(alpha,2)) +'$\pm$'+str( round(erroralpha,2))+'_eV/V')#,t='+str( round(tunnel,3))+'$\pm$'+str(round(errortunnel,3))+'_GHz, alpha='+str(alpha))
    #    plt.plot(xaxis,interdotfit_chargesensor(xaxis,*popt),'r',label='Teff='+str( round(Teff,2)) +'$\pm$'+str( round(errortemp,2))+'_K,t='+str( round(tunnel,3))+'$\pm$'+str(round(errortunnel,3))+'_GHz, alpha='+str(alpha))
    plt.legend(loc='upper right')
    plt.show()
    name=str(Bfield())+'_T_phiS_0p44K_findalpha_tnegligible_G3init'+str(startG3)+'mV__G4init'+str(startG4)+'mV'
    # fig.savefig(foldername2+'0.44K_Tonly_TP9_1dscan-'+str(Bfield())+'_T_ampliAWG'+str(ampliAWG())+'.png') 
    # np.savetxt(foldername2+'0.44K_Tonly_TP9_1dscan-'+str(Bfield())+'_T_ampliAWG'+str(ampliAWG())+'.txt',datasmooth2)
    
    plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
    np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',datasmooth2)
    
    #############################################
   

    return philim_S



def fit_interdot_G4(startG4,stopG4,startG3):
    
    stopG3=startG3
    num_point=201
    G4ar=np.linspace(startG4,stopG4,num_point)
    
    G3ar=np.linspace(startG3,stopG3,num_point)
    
    
    # eps=np.sqrt((detuningPoint1[0]-detuningPoint2[0])**2 +(detuningPoint1[1]-detuningPoint2[1])**2) 
    # VG3comp(detuningPoint1[0])
    VG4comp(G4ar[0])
    
    # det=generateEpsilonAxis(detuningPoint1, detuningPoint2, detpoints)
    eps=np.sqrt((startG4-stopG4)**2)
    epsilon=np.linspace(-eps/2,eps/2,len(G4ar))
    
    tag='TP0_'
    phases=[]
    
    
    
    phasedet_D=[]
    # phasedet_S=[]
    for i in range(0,len(G4ar)):
    
        # VG3comp(det[i][0])
        VG4comp(G4ar[i])
        time.sleep(0.02)
        # phasedet_S.append(ph2())
        phasedet_D.append(ph1())
        
   
    
    datasmooth_D=scipy.signal.savgol_filter(np.ravel(phasedet_D),11, 3)
    phimin=np.min(datasmooth_D)
    phimax=np.max(datasmooth_D)
    argmin=np.argmin(datasmooth_D)
    kmin=0
    kmax=0
    
    philim_D=phimin+(phimax-phimin)/2
    T=0.44
    sigmaphi=0.5#deg
    # for k in range(0,len(data_Det)):
    #         if ((data_get[0][k]>=(philim-sigmaphi) and data_get[0][k]<=(philim+sigmaphi)) and kmax==0):
    #             kmax=k
    for k in range(0,len(epsilon)):
        if ((  datasmooth_D[k]>=(philim_D-sigmaphi) and   datasmooth_D[k]<=(philim_D+sigmaphi)) and kmax==0):
            kmax=k
            print('ok')
    
        
    # VG3comp(G4ar[kmax][0])
    # VG4comp(G4ar[kmax][1])
    # VG3comp(G4ar[kmax][0])
    VG4comp(G4ar[kmax])
    
    # xaxis=np.multiply(np.subtract(data_Det,data_Det[kmax]),1e-3)
    xaxis=np.multiply(np.subtract(epsilon,epsilon[kmax]),1e-3)
    datasmooth2=np.subtract(datasmooth_D,phimin)
    
    xaxis2=np.array(xaxis,dtype=float)
    datasmooth2=np.array(datasmooth2,dtype=float)
    
    
    xaxis2=np.reshape(xaxis2,201)
    datasmooth2=np.reshape(datasmooth2,201)
    
    fig, ax = plt.subplots()
    ax.set_xlabel('$\epsilon$ (V)',fontsize=fontSize)
    ax.set_ylabel('$\phi_D $(rad)',fontsize=fontSize)
    
    plt.title('Fit at T='+str(T)+'K')
    plt.plot(xaxis,datasmooth2,'b+',label='data@'+str(T)+'K')#mV on x  
    plt.legend(loc='upper right')
    plt.show()
    
    
    
    alpha=0.55
    const=phimin
    offset=phimin+(phimax-phimin)
    
     
    popt,pcov = curve_fit(interdotfit_chargesensor,xaxis2,datasmooth2,p0=[alpha,0,1],maxfev=10000) 
    plt.plot(xaxis2,interdotfit_chargesensor(xaxis2,*popt))    
    
    
    alpha=popt[0] 
    
    er=np.sqrt(np.diag(pcov))
    erroralpha=er[0]
    # errortunnel=er[3]
    # print('Teff='+str(Teff))
    # Tarray.append(Teff)
    # errorTarray.append(errortemp)
    
    # tunnelarray.append(tunnel)
    # tunnelarrayerr.append(errortunnel)
    
    # errortunnel=errortunnel/h*10e-9#conv to Ghz
    plt.plot(xaxis,interdotfit_chargesensor(xaxis2,*popt),'r',label='alpha='+str( round(alpha,2)) +'$\pm$'+str( round(erroralpha,2))+'_eV/V')#,t='+str( round(tunnel,3))+'$\pm$'+str(round(errortunnel,3))+'_GHz, alpha='+str(alpha))
    #    plt.plot(xaxis,interdotfit_chargesensor(xaxis,*popt),'r',label='Teff='+str( round(Teff,2)) +'$\pm$'+str( round(errortemp,2))+'_K,t='+str( round(tunnel,3))+'$\pm$'+str(round(errortunnel,3))+'_GHz, alpha='+str(alpha))
    plt.legend(loc='upper right')
    plt.show()
    name=tag+str(Bfield())+'_T_phiD_0p44K_findalpha_tnegligible_G3init'+str(startG3)+'mV__G4init'+str(startG4)+'mV'
    # fig.savefig(foldername2+'0.44K_Tonly_TP9_1dscan-'+str(Bfield())+'_T_ampliAWG'+str(ampliAWG())+'.png') 
    # np.savetxt(foldername2+'0.44K_Tonly_TP9_1dscan-'+str(Bfield())+'_T_ampliAWG'+str(ampliAWG())+'.txt',datasmooth2)
    
    plt.savefig(folder2+'\\'+dayFolder+'\\'+name+'.png')
    np.savetxt(folder2+'\\'+dayFolder+'\\'+name+'.txt',datasmooth2)

    return philim_D


def VG3comp_onmin(initVT2,finalVT2,points,showplot):
    VG3comp(initVT2)
    time.sleep(0.05)
    continuous_acquisition_ch2()
    a,dataid,c=sweep1D(VG3comp, initVT2,finalVT2,points,0.01,ph2)
    now=datetime.datetime.now()
    dayFolder= datetime.date.isoformat(now)
    try:
        os.makedirs(folder2+'\\'+dayFolder)
    except IOError:
        donothing=1

    folder=r'S:\132-PHELIQS\132.05-LATEQS\132.05.01-QuantumSilicon\Tritonito\2021\Feb2021_6G22_2_die103\\data'
    name=str(dataid)+'_G3scan_calibrate_cs'
    xlabel='$V_{G3}$(mV)'
    ylabel='$\phi_{S}$(deg)'
    data_set,data_get,parameters_name=Extract_data(a)
    if showplot==1:
      plot_by_id(dataid)
      saveplot(name,dataid)
     # plt.close()
     # plot_savetxt(data_set,xlabel,data_get,ylabel,parameters_name,folder+'\\'+dayFolder,name)


    datasmooth=scipy.signal.savgol_filter(np.ravel(data_get[0]),11, 3)
    phimin=np.min(datasmooth)
    argmin=np.argmin(datasmooth)

   
    VG3comp(data_set[argmin])
    print('minpeak_VG3='+str(VG3()))  
    
    
    
    
def analyse_time_traces_interdot_S(path,start,stop,startG3,stopG3,Threshold) :
    
    print(path)
    file = path+'\\paths.txt'
    with open(file) as f:
        for line in f:
                paths = line.split(";")
#     Name = re.sub('../../exploration','',path)       
    Ps_up = []
    Ps_down = []
    Ts_up = []
    Ts_down = []
    for i in trange(len(paths)-1):
        path1 = paths[i]
        data = np.load(path1+'.npy')
        P_up,P_down,T_up,T_down = Occupations_and_times(data,Threshold, Do_plot = False)
        Ps_up.append(P_up)
        Ps_down.append(P_down)
        Ts_up.append(T_up)
        Ts_down.append(T_down)

    # Vg = np.linspace(-0.3,0.3,len(Ps_up))   
    
    eps=np.sqrt((start-stop)**2 +(startG3-stopG3)**2) 
    
    Vg = np.linspace(startG3,stopG3,len(Ps_up))    

    ## Plot the occupations up/down:
    fig,ax = plt.subplots()
    plt.plot(Vg,Ps_up,label='$P_{up}$')
    plt.plot(Vg,Ps_down,label='$P_{down}$')
    plt.xlabel('$V_{G3}$ (mV)',fontsize=18)
    plt.ylabel('$P_{up},P_{down}$',fontsize=18)
    ax.tick_params(labelsize=14)
    ax.set_title('Occupations'+str(Bfield())+'T',size=18)
    fig.tight_layout()
    plt.legend()
    plt.savefig(path+'\\'+str(Bfield())+'T_Occupation.png')

    ## Plot the tunnel rates:
    gamma_up = 1/np.array(Ts_up)
    gamma_down = 1/np.array(Ts_down)


    crossing=np.argmin(np.abs(gamma_up-gamma_down))
    gamma_up[gamma_up>1e6]=0  
    gamma_down[gamma_down>1e6]=0  
    
    fig,ax = plt.subplots()
    #good labelling if signal down corresponds to emptier state
    plt.plot(Vg,gamma_up*1e-3,'+',label='$\Gamma_{out}$')
    plt.plot(Vg,gamma_down*1e-3,'+',label='$\Gamma_{in}$')
    


    if np.max(gamma_up)>200e3 or np.max(gamma_down)>200e3:
        plt.ylim(0,200)
        
    plt.xlabel('$V_{G3}$ (mV)',fontsize=18)
    plt.ylabel('$\Gamma_{in},\Gamma_{out}$ (kHz)',fontsize=18)
    ax.tick_params(labelsize=14)
    ax.set_title('$V_{G4}=$'+str(VG4())+' mV',size=18)
    fig.tight_layout()
    plt.legend()
    plt.savefig(path+'//'+str(Bfield())+'T_VG4'+str(VG4())+'mv.png')


    
    return gamma_up[crossing] #, Vg[crossing]     


def analyse_time_traces_interdot_D(path,start,stop,startG3,stopG3,Threshold) :
    
    print(path)
    file = path+'\\paths.txt'
    with open(file) as f:
        for line in f:
                paths = line.split(";")
#     Name = re.sub('../../exploration','',path)       
    Ps_up = []
    Ps_down = []
    Ts_up = []
    Ts_down = []
    for i in trange(len(paths)-1):
        path1 = paths[i]
        data = np.load(path1+'.npy')
        P_up,P_down,T_up,T_down = Occupations_and_times(data,Threshold, Do_plot = False)
        Ps_up.append(P_up)
        Ps_down.append(P_down)
        Ts_up.append(T_up)
        Ts_down.append(T_down)

    # Vg = np.linspace(-0.3,0.3,len(Ps_up))   
    
    eps=np.sqrt((start-stop)**2 +(startG3-stopG3)**2) 
    
    Vg = np.linspace(start,stop,len(Ps_up))    

    ## Plot the occupations up/down:
    fig,ax = plt.subplots()
    plt.plot(Vg,Ps_up,label='$P_{up}$')
    plt.plot(Vg,Ps_down,label='$P_{down}$')
    plt.xlabel('$V_{G4}$ (mV)',fontsize=18)
    plt.ylabel('$P_{up},P_{down}$',fontsize=18)
    ax.tick_params(labelsize=14)
    ax.set_title('Occupations'+str(Bfield())+'T',size=18)
    fig.tight_layout()
    plt.legend()
    plt.savefig(path+'\\'+str(Bfield())+'T_Occupation.png')

    ## Plot the tunnel rates:
    gamma_up = 1/np.array(Ts_up)
    gamma_down = 1/np.array(Ts_down)


    crossing=np.argmin(np.abs(gamma_up-gamma_down))
    gamma_up[gamma_up>1e6]=0  
    gamma_down[gamma_down>1e6]=0  
    
    fig,ax = plt.subplots()
    ###good labelling if signal down corresponds to filled state
    plt.plot(Vg,gamma_up*1e-3,'+',label='$\Gamma_{in}$')
    plt.plot(Vg,gamma_down*1e-3,'+',label='$\Gamma_{out}$')
    


    if np.max(gamma_up)>200e3 or np.max(gamma_down)>200e3:
        plt.ylim(0,200)
        
    plt.xlabel('$V_{G4}$ (mV)',fontsize=18)
    plt.ylabel('$\Gamma_{in},\Gamma_{out}$ (kHz)',fontsize=18)
    ax.tick_params(labelsize=14)
    ax.set_title('$V_{G3}=$'+str(VG3())+' mV',size=18)
    fig.tight_layout()
    plt.legend()
    plt.savefig(path+'//'+str(Bfield())+'T_VG3'+str(VG3())+'mv.png')


    
    return gamma_up[crossing] #, Vg[crossing]  


def plot_correlations(num_point,Ntraces,startG4,stopG4,startG3,stopG3):
    #from plot_coincidences.py
    G4ar=np.linspace(startG4,stopG4,num_point)
    
    G3ar=np.linspace(startG3,stopG3,num_point)
    
    correlations=[]
    correlationvals=[]
    decay_S=[]
    decay_D=[]
    
    for i in range (0,len(G4ar)):
        
        VG3comp(G3ar[i])
        VG4comp(G4ar[i])
        print(VG4())
        taxis=np.linspace(0,acquisition_duration*1e6,points)
        decay02S_array=[]
        decay02D_array=[]
        correlation=[]
        correlationval=[]
        
        for k in range(0,Ntraces):
            phase_ssS,phase_ssD=phases_trig()
            phase_ssS=phase_ssS[0]
            phase_ssD=phase_ssD[0]
            # tdecay_S=step_detection(phase_ssS[20:],taxis[20:])
            # tdecay_D=step_detection(phase_ssD[20:],taxis[20:])
            tdecay_S=step_detection(phase_ssS[30:-10],taxis[30:-10])
            tdecay_D=step_detection(phase_ssD[30:-10],taxis[30:-10])
            
            decay02S_array.append(tdecay_S)
            decay02D_array.append(tdecay_D)
            if np.abs(tdecay_S-tdecay_D)<10:
             correlation.append(1)
             correlationval.append(tdecay_S)
            else :
             correlation.append(0)
             
             
        correlations.append(np.mean(correlation))
        correlationvals.append(np.mean(correlationval))
        decay_S.append(np.mean(tdecay_S))
        decay_D.append(np.mean(tdecay_D))
        
    now=datetime.datetime.now()
    dayFolder= datetime.date.isoformat(now)
    try:
        os.makedirs(folder2+'\\'+dayFolder)
    except IOError:
        donothing=1    
    
    fig,ax = plt.subplots()
    plt.plot(G4ar,correlations)
    # plt.pcolor(t*1e6,ampli_list,M)
    plt.ylabel('$correlations$',fontsize=18)
    plt.xlabel('G4 (mV)',fontsize=18)
    # cb=plt.colorbar()
    # cb.set_label('$\phi_D$ (rad)',fontsize=18)
    
    ax.tick_params(labelsize=14)
    ax.set_title('B='+str(np.round(Bfield(),3))+'ampliAWG'+str(np.round(ampliAWG(),4)),size=18)
    fig.tight_layout()
    
    title=str(Bfield())+'T_correlationvsG4_A_pp_'+str(ampliAWG()*11)+'mV__G3'+str(VG3())+'mV_G4'+str(VG4())+'mV' 
    
        
    plt.savefig(folder2+'\\'+dayFolder+'\\'+title+'.png')
    np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'.txt',correlations)
    
    
    
    fig,ax = plt.subplots()
    plt.plot(G4ar,correlationvals)
    # plt.pcolor(t*1e6,ampli_list,M)
    plt.ylabel('$average coincidence time($\mu s$)$',fontsize=18)
    plt.xlabel('G4 (mV)',fontsize=18)
    # cb=plt.colorbar()
    # cb.set_label('$\phi_D$ (rad)',fontsize=18)
    
    ax.tick_params(labelsize=14)
    ax.set_title('B='+str(np.round(Bfield(),3))+'ampliAWG'+str(np.round(ampliAWG(),4)),size=18)
    fig.tight_layout()
    
    title=str(Bfield())+'T_correlationtimevsG4_A_pp_'+str(ampliAWG()*11)+'mV__G3'+str(VG3())+'mV_G4'+str(VG4())+'mV' 
    
        
    plt.savefig(folder2+'\\'+dayFolder+'\\'+title+'.png')
    np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'.txt',correlationvals)
    
    
    
    
    fig,ax = plt.subplots()
    plt.plot(G4ar,correlationvals,label='correlation time')
    plt.plot(G4ar,decay_S,label='G3 jump time')
    plt.plot(G4ar,decay_D,label='G4 jump time')
    # plt.pcolor(t*1e6,ampli_list,M)
    # plt.ylabel('$average coincidence time($\mu s$)$',fontsize=18)
    plt.xlabel('G4 (mV)',fontsize=18)
    # cb=plt.colorbar()
    # cb.set_label('$\phi_D$ (rad)',fontsize=18)
    
    ax.tick_params(labelsize=14)
    ax.set_title('B='+str(np.round(Bfield(),3))+'ampliAWG'+str(np.round(ampliAWG(),4)),size=18)
    fig.tight_layout()
    
    title=str(Bfield())+'T_alltimesvsG4_A_pp_'+str(ampliAWG()*11)+'mV__G3'+str(VG3())+'mV_G4'+str(VG4())+'mV' 
    plt.legend()
        
    plt.savefig(folder2+'\\'+dayFolder+'\\'+title+'.png')
    # np.savetxt(folder2+'\\'+dayFolder+'\\'+title+'.txt',correlationvals,decay_S,decay_D)
