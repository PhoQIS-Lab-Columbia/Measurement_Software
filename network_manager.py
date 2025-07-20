import json
import pyvisa
from Instruments.oscilloscope_rigol import Oscilloscope
from Instruments.spectrum_analyzer_signal_hound import SpectrumAnalyzer
from EInstrument import EInstrument

class NetworkManager:
    def __init__(self):
        pass


    def create_instrument(self, name,instrument):
        """Create new instrument object based on the name using the selected port.
        params: name: EInstrument - name of the instrument
                instrument_ports: string 
            Returns: Instrument object"""
        
        
        if name == EInstrument.OSCILLOSCOPE.value or name == EInstrument.OSCILLOSCOPE:
            return Oscilloscope(instrument)
        elif name== EInstrument.SPECTRUM_ANALYZER.value or name== EInstrument.SPECTRUM_ANALYZER:
            return SpectrumAnalyzer(instrument)
            '''MODIFY WHEN ADDING A NEW INSTRUMENT TYPE'''
        else:
            raise ValueError(f"Instrument {name} is not recognized.")

    def add_new_instrument(self, name, unknown_ports,rm = pyvisa.ResourceManager()):
        """To add a new instrument to the registered list of connections.
            params: name:str - name of insturment
                unknown_ports: list - list of string of detected instruments lacking a label
                 rm: pyvis resource manager - include if already have one active 
                 returns: If instrument found, return new instrument object."""
        ids = []
        
        for p in unknown_ports:
            inst = rm.open_resource(p)
            id = inst.query('*IDN')
            ids.append(id)
            #Checks for instrument match
            if id.lower().contains(name):
                with open('instrumentPorts.json', 'r') as f:
                    data = json.load(f) 
                data[p] = name
                with open('instrumentPorts.json', 'w') as f:
                   json.dump(data,f) 
                return self.create_instrument(name,inst)
            inst.close()
      
        raise ValueError(f"Cannot find {name}. Ids detected {str(ids)}")
    


    def connect_instrument(self, instrument):
        """Connects and return single instrument.
            params: instrument: EInstrument or str"""
        rm = pyvisa.ResourceManager()
        resources = rm.list_resources()
        known_resources = []
        with open('instrumentPorts.json', 'r') as f:
            data = json.load(f) 

        for port in data.keys():
            known_resources.append(port)
            if data[port] == instrument or data[port] == instrument.value:
                instrument = rm.open_resource(port)
                return self.create_instrument(data[port],instrument)
            
        return self.add_new_instrument(instrument,(set(resources)^set(known_resources)),rm)
            
    def connect_instruments(self, instrument_list = []):
        """Connects and creates instrument objects from list of names. If no list is provided, then connects 
        and creates instrument for all detected instruments.
        params: instrument_list: list - list of instrument Enum names to connect to.
        Returns: list of instrument objects"""

        instruments = []
        if len(instrument_list) == 0:
            instrument_list = [x.value for x in EInstrument]

        rm = pyvisa.ResourceManager()
        resources = rm.list_resources()
        with open('instrumentPorts.json', 'r') as f:
            data = json.load(f) 

        for r in resources:
            if r in data.keys():
                if data[r] in instrument_list:
                    instrument = rm.open_resource(data[r], r)
                    instruments.append(self.create_instrument(data[r], instrument))
            else:
                if data[r] in instrument_list:
                    instruments.append(self.add_new_instrument(data[r],[r],rm))
        
        return instruments
            
           
    def disconnect(self, instruments):
        
        if type(instruments) is not list:
            instruments = [instruments]
        for i in instruments:
            i.disconnect()
        
        #cleans up all instrument objects from memory
        del instruments
            