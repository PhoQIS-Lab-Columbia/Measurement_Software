from Instruments import Instrument
import pyvisa
from template_helper import Helper
from template_secondary import Secondary
class Instrument(Instrument.Mandatory):

    def __init__(self, instrument):
        
        self.name = None #EInstrument
        self.instrument = instrument
        self.helper = Helper()

        #Class objects
    
    #TODO: Add SCPI functions below
