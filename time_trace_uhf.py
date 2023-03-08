import qcodes as qc
import numpy as np
import time
from time import sleep 
import zhinst
from qcodes.dataset.measurements import Measurement 
from qcodes.dataset.plotting import plot_by_id
from qcodes.dataset.experiment_container import new_experiment

from qcodes import Station, Measurement, Instrument
     

class DAM(qc.Parameter,qc.dataset.measurements.Measurement) :
    '''
    Class allowing to have acces with python to the Data Acquisition Module (DAM)
    
        Def get_data
            only function 
    
    '''
    def __init__(self, uhf, demod):
        '''
        Initialize the class 
        
        inputs : uhf -> (qc.instrument) Zurich instrument uhf
                 demod -> Demodulator chosen for the DAM. To be clear, demod 1 is 1 and so on. 
        '''
        self._uhf = uhf
        
        self.device=uhf.device
        
        self.demod=demod-1
        
        self._uhf.daq.flush()
        self._DAM = self._uhf.daq.dataAcquisitionModule()
        self._DAM.set('dataAcquisitionModule/device', self.device)
        self._uhf.daq.setInt('/'+self.device+'/demods/'+str(self.demod)+'/trigger', 0) #continuous
        self._DAM.set("dataAcquisitionModule/triggernode", '/'+self.device+'/demods/'+str(self.demod)+'/sample.theta')
        
        # This parameters can be changed in the class itself if one wants to change the DAM parameters 
        # To change it just call self._DAM.set('name',value)
        
        self._DAM.set("grid/mode", 4)   
        self._DAM.set("count", 1)
        

        
    def get_data(self,temps,*params) :
        
        ''' Store all *params in the data base Npoints over a duration Temps.
        
        inputs : temps -> (float) Time in second for the acquisition
                 * params -> (String [phase, amp, x,y]) if None DAM operate on the phase
        
        
        output : Dataid -> (int) Id to find data in the Database
        
        '''
                
        self.signal_path = []
        output=[]
        
        param_phase=qc.Parameter(name='Value_phase',label='Phase',unit='Rad')
        param_amp=qc.Parameter(name='Value_amp',label='Amplitude',unit='Volt')
        param_x=qc.Parameter(name='Value_x',label='X_amplitude',unit='Volt')
        param_y=qc.Parameter(name='Value_y',label='Y_amplitude',unit='Volt')
        
        dic = {'phase': ['Phase','Radians','/sample.theta',param_phase],
        'amp': ['amplitude','Volt','/sample.r',param_amp],
        'x': ['X','Volt','/sample.x',param_x],
        'y': ['Y','Volt','/sample.y',param_y]
        }
        
        
        if params == () :
            params=['phase']
        

        for param in params :
            self.signal_path.append('/'+self.device+'/demods/'+str(self.demod)+dic[param][2])
            output.append(dic[param][3])
        tc=self._uhf.daq.getDouble('/'+self.device+'/demods/'+str(self.demod)+'/timeconstant')
        sr = self._uhf.daq.getDouble('/'+self.device+'/demods/'+str(self.demod)+'/rate')
        
        points = int(temps*sr)
        self._DAM.set("grid/cols", points)
        
#        
#        print('')
#        print('***************************************************************')
#        print('************************* Tc= ' + '%.1e' %tc +  's ************************')
#        print('*********************** T_ech = ' +'%.1e' %(1/sr) +  's **********************')
#        print('***************************************************************')
#        print('')           
#        
#        if tc<(1/sr) :
#            print('')
#            print('********************************************************************************')
#            print('****************** Be Careful you may miss some events *************************')
#            print('********************************************************************************')
#            print('')           
        
#        self._DAM.set("duration", temps)
    
        for signal in self.signal_path :
            self._DAM.subscribe(signal)
        
        clockbase = float(self._uhf.daq.getInt('/'+self.device+'/clockbase'))      # Useful to convert in real time later
        data_read = self._DAM.read(True)
        progress = self._DAM.progress()[0]

        self._DAM.execute()
        self._DAM.set("forcetrigger", 1) #start now!
#        ziDAQ('set', h, 'dataAcquisitionModule/forcetrigger', 1);
        while not self._DAM.finished():
            time.sleep(0.001)
        data = self._DAM.read(True)
        self._DAM.finish()
        self._DAM.unsubscribe('*')

        samples = data[self.signal_path[0]]
        
        param1=qc.Parameter(name='Time',label='Time',unit='Sec')
        outputs=[]

        meas = Measurement()
        meas.name='Time_traces'
        meas.register_parameter(param1)
                
        for parameter in output :
            meas.register_parameter(parameter, setpoints=[param1])
            outputs.append([parameter, None])
                    
        t = (samples[0]['timestamp'][0, :] - samples[0]['timestamp'][0, 0])/clockbase
        values = samples[0]['value'][0, :]
        
        with meas.run() as datasaver:
            for i, paramt in enumerate(t):
                for j,parameter in enumerate(output) :
                    outputs[j][1] =  data[self.signal_path[j]][0]['value'][0, i]
                datasaver.add_result((param1, paramt),*outputs)
            
        dataid = datasaver.run_id  # convenient to have for plotting
#        
#        print('')
#        print('***************************************************************')
#        print('****************** Data saved in Database *********************')
#        print('***************************************************************')
#        
        return dataid
        
    def get_data_txt(self,temps,path,*params,affichage=True) :
        
        ''' Store all *params in the data base Npoints over a duration Temps.
        
        inputs : temps -> (float) Time in second for the acquisition
                 path -> a path where the time trace has to be saved
                 * params -> (String [phase, amp, x,y]) if None DAM operate on the phase
        
        
        output : Saves a time trace as a .txt file in "path"
        
        '''
                
        self.signal_path = []
        output=[]
        
        param_phase=qc.Parameter(name='Value_phase',label='Phase',unit='Rad')
        param_amp=qc.Parameter(name='Value_amp',label='Amplitude',unit='Volt')
        param_x=qc.Parameter(name='Value_x',label='X_amplitude',unit='Volt')
        param_y=qc.Parameter(name='Value_y',label='Y_amplitude',unit='Volt')
        
        dic = {'phase': ['Phase','Radians','/sample.theta',param_phase],
        'amp': ['amplitude','Volt','/sample.r',param_amp],
        'x': ['X','Volt','/sample.x',param_x],
        'y': ['Y','Volt','/sample.y',param_y]
        }
        
        
        if params == () :
            params=['phase']
        

        for param in params :
            self.signal_path.append('/'+self.device+'/demods/'+str(self.demod)+dic[param][2])
            output.append(dic[param][3])
        tc=self._uhf.daq.getDouble('/'+self.device+'/demods/'+str(self.demod)+'/timeconstant')
        sr = self._uhf.daq.getDouble('/'+self.device+'/demods/'+str(self.demod)+'/rate')
        points = int(temps*sr)
        self._DAM.set("grid/cols", points)
        
#        if affichage==True : 
#            print('')
#            print('***************************************************************')
#            print('************************* Tc= ' + '%.1e' %tc +  's ************************')
#            print('*********************** T_ech = ' +'%.1e' %(1/sr) +  's **********************')
#            print('***************************************************************')
#            print('')           
#            
#            if tc<(1/sr) :
#                print('')
#                print('********************************************************************************')
#                print('****************** Be Careful you may miss some events *************************')
#                print('********************************************************************************')
#                print('')           
#        
#        self._DAM.set("duration", temps)
    
        for signal in self.signal_path :
            self._DAM.subscribe(signal)
        
        clockbase = float(self._uhf.daq.getInt('/'+self.device+'/clockbase'))      # Useful to convert in real time later
        data_read = self._DAM.read(True)
        progress = self._DAM.progress()[0]

        self._DAM.execute()
        self._DAM.set("forcetrigger", 1) #start now!
#        ziDAQ('set', h, 'dataAcquisitionModule/forcetrigger', 1);
        while not self._DAM.finished():
            time.sleep(0.001)
        data = self._DAM.read(True)
        self._DAM.finish()
        self._DAM.unsubscribe('*')

        samples = data[self.signal_path[0]]
        
        param1=qc.Parameter(name='Time',label='Time',unit='Sec')
        outputs=[]
                   
        t = (samples[0]['timestamp'][0, :] - samples[0]['timestamp'][0, 0])/clockbase
        values = samples[0]['value'][0, :]
        
        compteur=1
        header= param1.name + ' (' + param1.unit +') ; '
        sortie=np.array(t)
        
        for j,parameter in enumerate(output) :
            compteur+=1
            datas=data[self.signal_path[j]][0]['value'][0, :]
            sortie=np.concatenate((sortie,datas))
            header=header+ parameter.name + ' (' + parameter.unit +') ; '
         
        sortie=np.reshape(sortie,(compteur,np.size(t)))
        
        np.savetxt(path,np.transpose(sortie),fmt='%.6e',header=header) 

    def get_data_bin(self,temps,path,*params,header=True,affichage=True) :
        
        ''' Store all *params in a binary file according to path. Path also contains the name of the binary file. 
        
        inputs : temps -> (float) Time in second for the acquisition
                 path -> a path where the time trace has to be saved
                 * params -> (String [phase, amp, x,y]) if None DAM operate on the phase
        
        
        output : Dataid -> (int) Id to find data in the Database
        
        '''
                
        self.signal_path = []
        output=[]
        
        param_phase=qc.Parameter(name='Value_phase',label='Phase',unit='Rad')
        param_amp=qc.Parameter(name='Value_amp',label='Amplitude',unit='Volt')
        param_x=qc.Parameter(name='Value_x',label='X_amplitude',unit='Volt')
        param_y=qc.Parameter(name='Value_y',label='Y_amplitude',unit='Volt')
        
        dic = {'phase': ['Phase','Radians','/sample.theta',param_phase],
        'amp': ['amplitude','Volt','/sample.r',param_amp],
        'x': ['X','Volt','/sample.x',param_x],
        'y': ['Y','Volt','/sample.y',param_y]
        }
        
        
        if params == () :
            params=['phase']
        

        for param in params :
            self.signal_path.append('/'+self.device+'/demods/'+str(self.demod)+dic[param][2])
            output.append(dic[param][3])
        tc=self._uhf.daq.getDouble('/'+self.device+'/demods/'+str(self.demod)+'/timeconstant')
        sr = self._uhf.daq.getDouble('/'+self.device+'/demods/'+str(self.demod)+'/rate')
        
        points = int(temps*sr)
        self._DAM.set("grid/cols", points)
        
#        if affichage == True :
#            print('')
#            print('***************************************************************')
#            print('************************* Tc= ' + '%.1e' %tc +  's ************************')
#            print('*********************** T_ech = ' +'%.1e' %(1/sr) +  's **********************')
#            print('***************************************************************')
#            print('')           
#            
#            if tc<(1/sr) :
#                print('')
#                print('********************************************************************************')
#                print('****************** Be Careful you may miss some events *************************')
#                print('********************************************************************************')
#                print('')           
#        
#        self._DAM.set("duration", temps)
    
        for signal in self.signal_path :
            self._DAM.subscribe(signal)
        
        clockbase = float(self._uhf.daq.getInt('/'+self.device+'/clockbase'))      # Useful to convert in real time later
        data_read = self._DAM.read(True)
        progress = self._DAM.progress()[0]

        self._DAM.execute()
        self._DAM.set("forcetrigger", 1) #start now!
#        ziDAQ('set', h, 'dataAcquisitionModule/forcetrigger', 1);
        while not self._DAM.finished():
            time.sleep(0.001)
        data = self._DAM.read(True)
        self._DAM.finish()
        self._DAM.unsubscribe('*')

        samples = data[self.signal_path[0]]
        
        param1=qc.Parameter(name='Time',label='Time',unit='Sec')
        outputs=[]
                   
        t = (samples[0]['timestamp'][0, :] - samples[0]['timestamp'][0, 0])/clockbase
        values = samples[0]['value'][0, :]
        
        compteur=1
        headertxt= param1.name + ' (' + param1.unit +') ; '
        sortie=np.array(t)
        
        for j,parameter in enumerate(output) :
            compteur+=1
            datas=data[self.signal_path[j]][0]['value'][0, :]
            sortie=np.concatenate((sortie,datas))
            headertxt=headertxt+ parameter.name + ' (' + parameter.unit +') ; '
         
        sortie=np.reshape(sortie,(compteur,np.size(t)))  
  
        np.save(path,np.transpose(sortie)) 
        pathtxt=path+'header.txt'
        
        if header==True :
            np.savetxt(pathtxt,[],fmt='%.6e',header=headertxt) 
        
        
class DAMTrig(qc.Parameter,qc.dataset.measurements.Measurement) :
    '''
    Class to record time traces on demand triggered with TrigIn1. Returns time and phase, no database yet.
    
        Def get_data
            only function 
    
    '''
    def __init__(self, uhf, demod):
        '''
        Initialize the class 
        
        inputs : uhf -> (qc.instrument) Zurich instrument uhf
                 demod -> Demodulator chosen for the DAM. To be clear, demod 1 is 1 and so on. 
        '''
        self._uhf = uhf
        
        self.device=uhf.device
        
        self.demod=demod-1
        
        self._uhf.daq.flush()
        self._DAM = self._uhf.daq.dataAcquisitionModule()
        self._DAM.set('dataAcquisitionModule/device', self.device)
        self._uhf.daq.setInt('/'+self.device+'/demods/'+str(self.demod)+'/trigger', 0) #continuous
        
        self._DAM.set('dataAcquisitionModule/type', 6)   ### Has to be set like this to trig on TrigIn1 signal
        self._DAM.set("dataAcquisitionModule/triggernode", '/'+self.device+'/demods/'+str(self.demod)+'/sample.TrigAWGTrig3') ### Trig on TrigIn1 signal   
        
        # This parameters can be changed in the class itself if one wants to change the DAM parameters 
        # To change it just call self._DAM.set('name',value)
        
        self._DAM.set("grid/mode", 4)   
        self._DAM.set("count", 1)
        self._DAM.set('dataAcquisitionModule/grid/repetitions', 1)
        self._DAM.set('dataAcquisitionModule/delay', 0)
        self._DAM.set('dataAcquisitionModule/holdoff/time', 0)
        
    def get_data(self,temps,*params) :
        
        ''' Returns a single time traces of one parameter.
        
        inputs : points -> (int) Number of point for the acquisition
                 temps -> (float) Time in second for the acquisition
                 * params -> (String [phase, amp, x,y]) if None DAM operate on the phase
        
        
        output : t -> a vector containing the time values
                 values: Values of the chosen parameter versus time.
        '''
                
        self.signal_path = []
        output=[]
        
        param_phase=qc.Parameter(name='Value_phase',label='Phase',unit='Rad')
        param_amp=qc.Parameter(name='Value_amp',label='Amplitude',unit='Volt')
        param_x=qc.Parameter(name='Value_x',label='X_amplitude',unit='Volt')
        param_y=qc.Parameter(name='Value_y',label='Y_amplitude',unit='Volt')
        
        dic = {'phase': ['Phase','Radians','/sample.theta',param_phase],
        'amp': ['amplitude','Volt','/sample.r',param_amp],
        'x': ['X','Volt','/sample.x',param_x],
        'y': ['Y','Volt','/sample.y',param_y]
        }
        
        
        if params == () :
            params=['phase']
        

        for param in params :
            self.signal_path.append('/'+self.device+'/demods/'+str(self.demod)+dic[param][2])
            output.append(dic[param][3])
        tc=self._uhf.daq.getDouble('/'+self.device+'/demods/'+str(self.demod)+'/timeconstant')
        sr = self._uhf.daq.getDouble('/'+self.device+'/demods/'+str(self.demod)+'/rate')
#        print(sr)
        points = int(temps*sr)
#        print(points)
        self._DAM.set("grid/cols", points)
        
        
#        self._DAM.set("duration", temps)
    
        for signal in self.signal_path :
            self._DAM.subscribe(signal)
        
        clockbase = float(self._uhf.daq.getInt('/'+self.device+'/clockbase'))      # Useful to convert in real time later
        data_read = self._DAM.read(True)
        progress = self._DAM.progress()[0]

        self._DAM.execute()
#        self._DAM.set("forcetrigger", 1) #start now!
#        ziDAQ('set', h, 'dataAcquisitionModule/forcetrigger', 1);
        while not self._DAM.finished():
            time.sleep(0.001)
        data = self._DAM.read(True)
        self._DAM.finish()
        self._DAM.unsubscribe('*')

        samples = data[self.signal_path[0]]
        
        param1=qc.Parameter(name='Time',label='Time',unit='Sec')
        outputs=[]

#        meas = Measurement()
#        meas.name='Time_traces'
#        meas.register_parameter(param1)
#                
#        for parameter in output :
#            meas.register_parameter(parameter, setpoints=[param1])
#            outputs.append([parameter, None])
                    
        t = (samples[0]['timestamp'][0, :] - samples[0]['timestamp'][0, 0])/clockbase
        values = samples[0]['value'][0, :]
        
     
        return t, values



    def get_data_pulseseq(self,temps,delay,number,*params) :
        
        ''' Returns an array from the UHF with time and values
        
        inputs : points -> (int) Number of lines to record acquisition
                 temps -> (float) Time in second for the acquisition
                 * params -> (String [phase, amp, x,y]) if None DAM operate on the phase
        
        
        output : t -> a vector containing the time values
                 values: a matrix containing the N temporal traces as rows, versus time on x axis.
        
        '''
        self._uhf.daq.setInt('/'+self.device+'/demods/'+str(self.demod)+'/trigger', 33554432) #AWG trigger2
        
        self.signal_path = []
        output=[]
        
        param_phase=qc.Parameter(name='Value_phase',label='Phase',unit='Rad')
        param_amp=qc.Parameter(name='Value_amp',label='Amplitude',unit='Volt')
        param_x=qc.Parameter(name='Value_x',label='X_amplitude',unit='Volt')
        param_y=qc.Parameter(name='Value_y',label='Y_amplitude',unit='Volt')
        
        dic = {'phase': ['Phase','Radians','/sample.theta',param_phase],
        'amp': ['amplitude','Volt','/sample.r',param_amp],
        'x': ['X','Volt','/sample.x',param_x],
        'y': ['Y','Volt','/sample.y',param_y]
        }
        
        
        if params == () :
            params=['phase']
        

        for param in params :
            self.signal_path.append('/'+self.device+'/demods/'+str(self.demod)+dic[param][2])
            output.append(dic[param][3])
        tc=self._uhf.daq.getDouble('/'+self.device+'/demods/'+str(self.demod)+'/timeconstant')
        sr = self._uhf.daq.getDouble('/'+self.device+'/demods/'+str(self.demod)+'/rate')
#        print(sr)
        points = int(temps*sr)
#        print(points)
        self._DAM.set("grid/cols", points)
        self._DAM.set("grid/rows", number)
        self._DAM.set("delay", delay)
        
#        self._DAM.set("duration", temps)
    
        for signal in self.signal_path :
            self._DAM.subscribe(signal)
        
        clockbase = float(self._uhf.daq.getInt('/'+self.device+'/clockbase'))      # Useful to convert in real time later
        data_read = self._DAM.read(True)
        progress = self._DAM.progress()[0]

        self._DAM.execute()
#        self._DAM.set("forcetrigger", 1) #start now!
#        ziDAQ('set', h, 'dataAcquisitionModule/forcetrigger', 1);
        while not self._DAM.finished():
            time.sleep(0.001)
        data = self._DAM.read(True)
        self._DAM.finish()
        self._DAM.unsubscribe('*')

        samples = data[self.signal_path[0]]
        
#        param1=qc.Parameter(name='Time',label='Time',unit='Sec')
#        outputs=[]

#        meas = Measurement()
#        meas.name='Time_traces'
#        meas.register_parameter(param1)
#                
#        for parameter in output :
#            meas.register_parameter(parameter, setpoints=[param1])
#            outputs.append([parameter, None])
                    
        t = (samples[0]['timestamp'][0, :] - samples[0]['timestamp'][0, 0])/clockbase
        values = samples[0]['value'][:, :]
        values=np.transpose(values)
     
        return t, values

