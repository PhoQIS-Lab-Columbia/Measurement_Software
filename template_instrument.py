from Instruments import Instrument
from EInstrument import EInstrument
import pyvisa

class Instrument(Instrument.Instrument):

    def __init__(self, instrument, name, saved_files_path=None):
        super().__init__(instrument, EInstrument.Name, saved_files_path)
        
        #Class objects
    
    #TODO: Add SCPI functions below
