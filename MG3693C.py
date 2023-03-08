from numpy import pi

from qcodes import VisaInstrument, validators as vals





class MG3693C(VisaInstrument):
    '''
xxxxx
    '''
    def __init__(self, name, address, step_attenuator=False, **kwargs):
        super().__init__(name, address, **kwargs)

        self.add_parameter(name='frequency',
                           label='Frequency',
                           unit='Hz',
                           get_cmd='FREQ:CW?',
                           set_cmd='FREQ:CW' + ' {:.4f}',
                           get_parser=float,
                           set_parser=float,
                           vals=vals.Numbers(10e6, 31.8e9))

        self.add_parameter(name='power',
                           label='Power',
                           unit='dBm',
                           get_cmd='POW:AMPL?',
                           set_cmd='POW:AMPL' + ' {:.4f}',
                           get_parser=float,
                           set_parser=float,
                           vals=vals.Numbers(-10, 30))
        
        self.add_parameter('status',
                           get_cmd=':OUTP?',
                           set_cmd='OUTP {}',
                           get_parser=self.parse_on_off,
                           # Only listed most common spellings idealy want a
                           # .upper val for Enum or string
                           vals=vals.Enum('on', 'On', 'ON',
                                          'off', 'Off', 'OFF'))
        self.add_parameter('trigdelay',
                           get_cmd='PULS:DEL?',
                           set_cmd='PULS:DEL'+  ' {}',
                           get_parser=float,
                           set_parser=float)
                           
        self.add_parameter('burstwidth',
                           get_cmd='PULS:WIDTH?',
                           set_cmd='PULS:WIDTH'+' {}',##space before{} is crucial
                           get_parser=float,
                           set_parser=float)
        self.add_parameter('trigpulses',
                           get_cmd='SOUR:PULM:STAT ?',
                           set_cmd='SOUR:PULM:STAT'+' {}',##space before{} is crucial
                           get_parser=float,
                           set_parser=float)                  

        self.connect_message()

    # Note it would be useful to have functions like this in some module instad
    # of repeated in every instrument driver

    def parse_on_off(self, stat):
        if stat.startswith('0'):
            stat = 'Off'
        elif stat.startswith('1'):
            stat = 'On'
        return stat

    def on(self):
        self.set('status', 'on')

    def off(self):
        self.set('status', 'off')
