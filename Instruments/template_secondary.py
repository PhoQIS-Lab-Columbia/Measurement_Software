from Instruments import Instrument
import pyvisa

class Instrument(Instrument.Mandatory):

    def __init__(self, instrument):
        
        self.name = None #EInstrument
        self.instrument = instrument
       
    
    #TODO: Add SCPI functions below
