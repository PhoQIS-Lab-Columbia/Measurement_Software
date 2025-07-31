from Instruments import Instrument
from EInstrument import EInstrument
import pyvisa

class Instrument(Instrument.Instrument):

    def __init__(self, instrument, name):
        super().__init__(instrument, EInstrument.Name)
        
        #Class objects
    
    #TODO: Add SCPI functions below
