import json
import pyvisa
import os
from ctypes import *
import ctypes
import struct
import subprocess
import importlib.resources
from Instruments.oscilloscope_rigol import Oscilloscope
from Instruments.spectrum_analyzer_signal_hound import SpectrumAnalyzer
from Instruments.vector_network_analyzer_copper_mountain import VNA
from Instruments.EInstrument import EInstrument
from Instruments.digital_attenuator_vanuix import digital_attenuator

from Instruments.rf_switch import RF_Switch
from Instruments.dc_power_supply_siglent import DCPowerSupply
from Instruments.flowmeter_keyence import Flowmeter
import time
import psutil

class NetworkManager:
    def __init__(self, non_default_program_path = None, non_default_instrument_ports=None,rm = pyvisa.ResourceManager()):
        '''Initialize the NetworkManager with a VISA Resource Manager.
        params: non_default_program_path: string - path to a json file containing non-default program paths for instruments.
            If None, internal default will be used
            non_default_instrument_ports: string - path to a json file containing non-default instrument ports.
            If None, internal default will be used
            rm: pyvisa.ResourceManager - Resource manager to use for instrument connections.
            If None, a new resource manager will be created.
        '''
        self.rm = rm
        if non_default_program_path is None:
            self.program_path = 'program_paths.json'
        else:
            self.program_path = non_default_program_path

        if non_default_instrument_ports is None:
            self.instrument_ports = 'instrumentPorts.json'
        else:
            self.instrument_ports = non_default_instrument_ports
        

    def process_exists(self, process_name): 
        pieces = process_name.split('/')
        process_name = pieces[len(pieces)-1]
        call = 'TASKLIST', '/FI', f'imagename eq {process_name}'
        output = subprocess.check_output(call).decode()
        last_line = output.strip().split('\r\n')[-1]
        return last_line.lower().startswith(process_name.lower())
    
    def get_process_by_name(self,process_name):
        """Return the first psutil.Process object matching the process name."""
        
        pieces = process_name.split('/')
        name = pieces[len(pieces)-1]
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] and proc.info['name'].lower() == name.lower():
                return proc  # This is a psutil.Process object
        return None
    
    def create_instrument(self, name, instrument,saved_files_path):
        """Create new instrument object based on the name using the selected port.
        params: name: EInstrument - name of the instrument
                instrument_ports: string 
            Returns: Instrument object"""
        
        if name == EInstrument.OSCILLOSCOPE.value or name == EInstrument.OSCILLOSCOPE:
            return Oscilloscope(instrument,saved_files_path)
        elif name== EInstrument.SPECTRUM_ANALYZER.value or name== EInstrument.SPECTRUM_ANALYZER:
            return self.connect_spectrum_analyzer(saved_files_path)
        elif name== EInstrument.VECTOR_NETWORK_ANALYZER.value or name== EInstrument.VECTOR_NETWORK_ANALYZER:
            return self.connect_vector_network_analyzer(saved_files_path)
        elif name == EInstrument.DIGITAL_ATTENUATOR.value or name == EInstrument.DIGITAL_ATTENUATOR:
            return self.connect_digital_attenuators(saved_files_path)
        elif name == EInstrument.RF_SWITCH.value or name == EInstrument.RF_SWITCH:
            return RF_Switch(instrument, saved_files_path)
        elif name == EInstrument.DC_POWER_SUPPLY.value or name == EInstrument.DC_POWER_SUPPLY:
            return DCPowerSupply(instrument, saved_files_path)
        elif name == EInstrument.FLOW_METER.value or name == EInstrument.FLOW_METER:
            return self.connect_flow_meter()
        else:
            raise ValueError(f"Instrument {name} is not recognized.")
    
    def connect_instruments(self, instrument_list = [], saved_files_path = None):
        """Connects and creates instrument objects from list of names. If no list is provided, then connects 
        and creates instrument for all detected instruments.
        params: instrument_list: list - list of instrument Enum names to connect to.
        Returns: list of instrument objects"""

        resources = self.rm.list_resources()
        
        with importlib.resources.open_text('Instruments.data','noninstrumentPorts.json') as f:
            data = json.load(f)
        
        #Remove ports that are known to not be instruments
        unknown_resources = [x for x in resources if x not in data.keys()]
        instruments = []
        print(unknown_resources)

        with importlib.resources.open_text('Instruments.data','instrumentPorts.json') as f:
            instrumentPorts = json.load(f) 
        for port in unknown_resources:
        #for i in range(0,1):
            #port = unknown_resources[i]
            print("Port: "+str(port))
            try:
                inst = self.rm.open_resource(port, read_termination = '\n')
                id = inst.query('*IDN?')
            except pyvisa.VisaIOError:
                print("Resource is listed but not actually present or accessible.")
                id = "None"
            print(id)
            print("Instrument list "+str(instrument_list))
            if id in instrumentPorts.keys() and (instrument_list == [] or EInstrument(instrumentPorts[id]) in instrument_list):
                print("To create instrument: "+ str(instrumentPorts[id]))
                instruments.append(self.create_instrument(instrumentPorts[id],inst,saved_files_path))
        if instrument_list == [] or EInstrument.VECTOR_NETWORK_ANALYZER in instrument_list:
            instruments.append(self.connect_vector_network_analyzer(saved_files_path))
        if instrument_list == [] or EInstrument.SPECTRUM_ANALYZER in instrument_list:
            instruments.append(self.connect_spectrum_analyzer(saved_files_path))
        if instrument_list == [] or EInstrument.DIGITAL_ATTENUATOR in instrument_list:
            instruments.append(self.connect_digital_attenuators(saved_files_path))

        print("Abount to leave connect instrument.")
        return instruments
    
    def connect_flowmeter(self, saved_files = []) -> Flowmeter:
        return Flowmeter(saved_files)
    
    def connect_oscilloscope(self,saved_files_path = None) -> Oscilloscope:
        osc = self.connect_instruments([EInstrument.OSCILLOSCOPE],saved_files_path)
        print(osc)
        if osc == None:
            raise ValueError("Oscilloscope failed to connect.")
        return osc[0]
            
    def connect_spectrum_analyzer(self,saved_files_path = None) -> SpectrumAnalyzer:
        #try: 
            
        '''with importlib.resources.open_text('Instruments.data','program_paths.json') as file:
            p = json.load(file)'''
        program_path = "C:/Program Files/Signal Hound/Spike/Spike.exe"#p[EInstrument.SPECTRUM_ANALYZER.value]
        if self.process_exists(program_path):
            app = self.get_process_by_name(program_path)
        app = subprocess.Popen([program_path], shell = False)
        time.sleep(8)
        '''with importlib.resources.open_text('Instruments.data','instrumentPorts.json') as file:
            ip = json.load(file)'''
        # Open a session to the Spike software, Spike must be running at this point
        port = "TCPIP0::localhost::5026::SOCKET"#ip[EInstrument.SPECTRUM_ANALYZER.value]
        inst = self.rm.open_resource(port)

        # For SOCKET programming, we want to tell VISA to use a terminating character
        #   to end a read and write operation.
        inst.read_termination = '\n'
        inst.write_termination = '\n'
        #except:
            #raise ValueError("Spectrum Analyzer failed to connect.")
        return SpectrumAnalyzer(inst,app, program_path,saved_files_path)
    
    def connect_vector_network_analyzer(self,saved_files_path = None) -> VNA:
        #try: 
            
        '''with importlib.resources.open_text('Instruments.data','program_paths.json') as file:
            p = json.load(file)'''
        program_path = "C:/VNA/S4VNA/S4VNA.exe"#p[EInstrument.VECTOR_NETWORK_ANALYZER.value]
        app = subprocess.Popen([program_path], shell = False)
        time.sleep(5)
        '''with importlib.resources.open_text('Instruments.data','instrumentPorts.json') as file:
            ip = json.load(file)'''
        port = "TCPIP0::localhost::5025::SOCKET"#ip[EInstrument.VECTOR_NETWORK_ANALYZER.value]
        
        # Open a session to the S4VNA software, S4VNA must be running at this point
        inst = self.rm.open_resource(port)

        # For SOCKET programming, we want to tell VISA to use a terminating character
        #   to end a read and write operation.
        inst.read_termination = '\n'
        inst.write_termination = '\n'
        #except:
            #raise ValueError("VNA failed to connect.")
        return VNA(inst,app, program_path,saved_files_path)
        
    def connect_flow_meter(self,saved_files = []) -> Flowmeter:
        return Flowmeter(saved_files)
    
    def connect_dc_power_supply(self,saved_files_path = None) -> DCPowerSupply:
        dc_power = self.connect_instruments([EInstrument.DC_POWER_SUPPLY],saved_files_path)
        if dc_power == None:
            raise ValueError("DC Power Supply failed to connect.")
        return dc_power[0]
    def connect_rf_switch(self,saved_files_path = None) -> RF_Switch:
        with importlib.resources.open_text('Instruments.data','instrumentPorts.json') as file:
            ip = json.load(file)
        port = ip[EInstrument.RF_SWITCH.value]
        inst = self.rm.open_resource(port)

        # For SOCKET programming, we want to tell VISA to use a terminating character
        #   to end a read and write operation.
        inst.read_termination = '\n'
        inst.write_termination = '\n'

        return RF_Switch(inst,saved_files_path)
    def connect_digital_attenuators(self,saved_files_path = None):
        #os.add_dll_directory(os.getcwd())
        #TODO Add an add digital attnuator and have it take device id as param, only return that one, call that function in here recursively
        if struct.calcsize("P") * 8 == 32:
            vnx = cdll.LoadLibrary("C:/Users/phoqi/Desktop/Measurement_Software/Instruments/digital_attenuator_vanuix/VNX_atten.dll")
        elif struct.calcsize("P") * 8 == 64:
            vnx = cdll.LoadLibrary("C:/Users/phoqi/Desktop/Measurement_Software/Instruments/digital_attenuator_vanuix/VNX_atten64.dll")
        else:
            raise NotImplementedError("Unsupported operating system")
        
        # Set test mode to false
        # This means that we will be using real devices
        vnx.fnLDA_SetTestMode(False)

        # Get the number of devices
        devices_num = vnx.fnLDA_GetNumDevices()
        # Create an array of device ids for connected devices
        DeviceIDArray = c_int * devices_num
        devices_list = DeviceIDArray()
        # fill the array with the ID's of connected attenuators
        vnx.fnLDA_GetDevInfo(devices_list)

        if len(devices_list) > 0:
            # Select which device to use
            devid = 0
            if len(devices_list) == 1:
                
                devid = devices_list[0]
            else:
                while not devid in devices_list:
                    print("Connected Devices:")
                    for device in devices_list:
                        print(f"\t({device}) {vnx.fnLDA_GetSerialNumber(device)}")
                    try:
                        devid = int(input("Select a device: "))
                        if not devid in devices_list:
                            print("Invalid device selection")
                    except ValueError:
                        print("Invalid device selection")
                    print()
            
            
            # Open selected device
            vnx.fnLDA_InitDevice(devid)
            
            return digital_attenuator(vnx, devid, saved_files_path)
        
            
    def disconnect(self, instruments):
        
        if type(instruments) is not list:
            instruments = [instruments]
        for i in instruments:
            i.disconnect()
        
        #cleans up all instrument objects from memory
        del instruments
        self.rm.close()
            