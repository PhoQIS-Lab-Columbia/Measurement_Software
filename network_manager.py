import json
import pyvisa
from Instruments.oscilloscope_rigol import Oscilloscope
from Instruments.spectrum_analyzer_signal_hound import SpectrumAnalyzer
from Instruments.vector_network_analyzer_copper_mountain import VNA
from EInstrument import EInstrument

class NetworkManager:
    def __init__(self, rm = pyvisa.ResourceManager()):
        self.rm = rm


    def create_instrument(self, name, instrument):
        """Create new instrument object based on the name using the selected port.
        params: name: EInstrument - name of the instrument
                instrument_ports: string 
            Returns: Instrument object"""
        
        
        if name == EInstrument.OSCILLOSCOPE.value or name == EInstrument.OSCILLOSCOPE:
            return Oscilloscope(instrument)
        elif name== EInstrument.SPECTRUM_ANALYZER.value or name== EInstrument.SPECTRUM_ANALYZER:
            return SpectrumAnalyzer(instrument)
            '''MODIFY WHEN ADDING A NEW INSTRUMENT TYPE'''
        elif name== EInstrument.VECTOR_NETWORK_ANALYZER.value or name== EInstrument.VECTOR_NETWORK_ANALYZER:
            return VNA(instrument)
        else:
            raise ValueError(f"Instrument {name} is not recognized.")

    
    def connect_instruments(self, instrument_list = []):
        """Connects and creates instrument objects from list of names. If no list is provided, then connects 
        and creates instrument for all detected instruments.
        params: instrument_list: list - list of instrument Enum names to connect to.
        Returns: list of instrument objects"""

        resources = self.rm.list_resources()
        
        with open('noninstrumentPorts.json', 'r') as f:
            data = json.load(f) 
        
        #Remove ports that are known to not be instruments
        unknown_resources = [x for x in resources if x not in data.keys()]
        instruments = []
        print(unknown_resources)

        with open('instrumentPorts.json', 'r') as f:
            instrumentPorts = json.load(f) 
        for port in unknown_resources:
            #print("Port: "+str(port))
            inst = self.rm.open_resource(port, read_termination = '\n')
            id = inst.query('*IDN?')
            
            if id in instrumentPorts.keys() and (instrument_list == [] or EInstrument(instrumentPorts[id]) in instrument_list):
                print("To create instrument: "+ str(instrumentPorts[id]))
                instruments.append(self.create_instrument(instrumentPorts[id],inst))
        return instruments

    def connect_oscilloscope(self) -> Oscilloscope:
        '''MODIFY WHEN ADDING A NEW INSTRUMENT TYPE'''
        return self.connect_instruments([EInstrument.OSCILLOSCOPE])[0]
            
    def connect_spectrum_analyzer(self) -> SpectrumAnalyzer:
        return self.connect_instruments([EInstrument.SPECTRUM_ANALYZER])
    
    def connect_vector_network_analyzer(self) -> VNA:
        return self.connect_instruments([EInstrument.VECTOR_NETWORK_ANALYZER])
            
           
    def disconnect(self, instruments):
        
        if type(instruments) is not list:
            instruments = [instruments]
        for i in instruments:
            i.disconnect()
        
        #cleans up all instrument objects from memory
        del instruments
        self.rm.close()
            