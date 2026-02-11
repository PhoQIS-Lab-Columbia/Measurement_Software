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
from Instruments.digital_attenuator_vanuix import DigitalAttenuator

from Instruments.rf_switch import RF_Switch
from Instruments.dc_power_supply_siglent import DCPowerSupply
from Instruments.flowmeter_keyence import Flowmeter
import time
import psutil

class NetworkManager:
    def __init__(self, rm = pyvisa.ResourceManager()):
        """Initialize the NetworkManager to handle setting up instruments and establishing VISA connections.
            
            :param rm: pyvisa.ResourceManager - Resource manager to use for instrument connections. If None, a new resource manager will be created.
            :type rm: pyvisa.ResourceManager"""
        
        self.rm = rm
        

    def process_exists(self, process_name): 
        """Check if there is any running process that contains the given name process_name.
        
        :param process_name: Name of the process to check.
        :type process_name: str
        :return: True if the process is running, False otherwise.
        :rtype: bool"""
        
        pieces = process_name.split('/')
        process_name = pieces[len(pieces)-1]
        call = 'TASKLIST', '/FI', f'imagename eq {process_name}'
        output = subprocess.check_output(call).decode()
        last_line = output.strip().split('\r\n')[-1]
        return last_line.lower().startswith(process_name.lower())
    
    def get_process_by_name(self,process_name):
        """Return the first psutil. Process object matching the process name.
        
        :param process_name: Name of the process to find.
        :type process_name: str
        :return: psutil.Process object if found, None otherwise.
        :rtype: psutil.Process or None"""
        
        pieces = process_name.split('/')
        name = pieces[len(pieces)-1]
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] and proc.info['name'].lower() == name.lower():
                return proc  # This is a psutil.Process object
        return None
    
    def create_instrument(self, name, instrument, saved_files_path):
        """Create new instrument object based on the name using the selected port.
        
        :param name: name of the instrument
        :type name: EInstrument
        :param instrument: the instrument to create
        :type instrument: pyvisa.Resource
        :param saved_files_path: path to the saved files
        :type saved_files_path: str
        :return: created instrument
        :rtype: Instrument"""
        
        if name == EInstrument.OSCILLOSCOPE.value or name == EInstrument.OSCILLOSCOPE:
            return Oscilloscope(instrument,saved_files_path)
        elif name== EInstrument.SPECTRUM_ANALYZER.value or name== EInstrument.SPECTRUM_ANALYZER:
            return self.connect_spectrum_analyzer(instrument,saved_files_path)
        elif name== EInstrument.VECTOR_NETWORK_ANALYZER.value or name== EInstrument.VECTOR_NETWORK_ANALYZER:
            return self.connect_vector_network_analyzer(instrument,saved_files_path)
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

        :param instrument_list: list of instrument Enum names to connect to.
        :type instrument_list: list of EInstrument
        :param saved_files_path: path to save files for the instruments.
        :type saved_files_path: str
        :return: list of instrument objects
        :rtype: list of Instrument"""

        resources = self.rm.list_resources()
        
        with importlib.resources.open_text('Instruments.data','noninstrumentPorts.json') as f:
            data = json.load(f)
        
        #Remove ports that are known to not be instruments
        unknown_resources = [x for x in resources if x not in data.keys()]
        instruments = []

        instrumentPorts = {"RIGOL TECHNOLOGIES,DS1202Z-E,DS1ZE264M00036,00.06.04":"oscilloscope",
"Siglent Technologies,SPD3303C,SPD3EGGD802587,1.02.01.02.02R3,V2.0":"dc power supply",
"spectrum analyzer":"TCPIP0::localhost::5026::SOCKET",
"vector network analyzer":"TCPIP0::localhost::5025::SOCKET",
"rf switch":"TCPIP0::192.168.0.8::8249::SOCKET"}
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
            instruments.append(self.connect_vector_network_analyzer(instrumentPorts["vector network analyzer"],saved_files_path))
        if instrument_list == [] or EInstrument.SPECTRUM_ANALYZER in instrument_list:
            instruments.append(self.connect_spectrum_analyzer(instrumentPorts["spectrum analyzer"],saved_files_path))
        if instrument_list == [] or EInstrument.DIGITAL_ATTENUATOR in instrument_list:
            instruments.append(self.connect_digital_attenuators(saved_files_path))

        print("About to leave connect instrument.")
        return instruments
    
    def connect_flowmeter(self, saved_files = []) -> Flowmeter:
        """Connect to the Keyence NQ Sensor Monitor software and return a Flowmeter object.
        
        :param saved_files: List of CSV file paths for the flowmeter data.
        :type saved_files: list of str
        :return: Flowmeter object connected to the NQ Sensor Monitor software.
        :rtype: Flowmeter"""

        return Flowmeter(saved_files)
    
    def connect_oscilloscope(self,port = None,saved_files_path = None) -> Oscilloscope:
        """Connect to the Rigol Oscilloscope and return an Oscilloscope object.
        
        :param saved_files_path: Path to save files for the Oscilloscope.
        :type saved_files_path: str
        :return: Oscilloscope object connected to the Rigol Oscilloscope.
        :rtype: Oscilloscope"""
        if port == None:
            port = "RIGOL TECHNOLOGIES,DS1202Z-E,DS1ZE264M00036,00.06.04"
        inst = self.rm.open_resource(port, read_termination = '\n')
        osc = Oscilloscope(inst,saved_files_path)
        if osc == None:
            raise ValueError("Oscilloscope failed to connect.")
        return osc
            
    def connect_spectrum_analyzer(self,port = None, saved_files_path = None) -> SpectrumAnalyzer:
        #try: 
        """Connect to the Signal Hound Spike software and return a SpectrumAnalyzer object.

        :param saved_files_path: Path to save files for the Spectrum Analyzer.
        :type saved_files_path: str
        :return: SpectrumAnalyzer object connected to the Spike software.
        :rtype: SpectrumAnalyzer"""
        
        program_path = "C:/Program Files/Signal Hound/Spike/Spike.exe"#p[EInstrument.SPECTRUM_ANALYZER.value]
        if self.process_exists(program_path):
            app = self.get_process_by_name(program_path)
        app = subprocess.Popen([program_path], shell = False)
        time.sleep(8)
        
        # Open a session to the Spike software, Spike must be running at this point
        if port == None:
            port = "TCPIP0::localhost::5026::SOCKET"#ip[EInstrument.SPECTRUM_ANALYZER.value]
        inst = self.rm.open_resource(port)

        # For SOCKET programming, we want to tell VISA to use a terminating character
        #   to end a read and write operation.
        inst.read_termination = '\n'
        inst.write_termination = '\n'
        #except:
            #raise ValueError("Spectrum Analyzer failed to connect.")
        return SpectrumAnalyzer(inst,app, program_path,saved_files_path)
    
    def connect_vector_network_analyzer(self,port = None, saved_files_path = None) -> VNA:
        #try: 
        """
        Connect to the Copper Mountain Technologies S4VNA software and return a VNA object.
        
        :param saved_files_path: Path to save files for the VNA.
        :type saved_files_path: str
        :return: VNA object connected to the S4VNA software.
        :rtype: VNA"""
        
        program_path = "C:/VNA/S4VNA/S4VNA.exe"#p[EInstrument.VECTOR_NETWORK_ANALYZER.value]
        app = subprocess.Popen([program_path], shell = False)
        time.sleep(5)
    
        if port == None:
            port = "TCPIP0::localhost::5025::SOCKET"
        
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
        """Connect to the Keyence NQ Sensor Monitor software and return a Flowmeter object.
        
        :param saved_files: List of CSV file paths for the flowmeter data.
        :type saved_files: list of str
        :return: Flowmeter object connected to the NQ Sensor Monitor software.
        :rtype: Flowmeter"""

        return Flowmeter(saved_files)
    
    def connect_dc_power_supply(self,port = None,saved_files_path = None) -> DCPowerSupply:
        """Connect to the DC Power Supply and return a DCPowerSupply object.
        
        :param saved_files_path: Path to save files for the DC Power Supply.
        :type saved_files_path: str
        :return: DCPowerSupply object connected to the DC Power Supply.
        :rtype: DCPowerSupply"""
        if port == None:
            port = "Siglent Technologies,SPD3303C,SPD3EGGD802587,1.02.01.02.02R3,V2.0"
        inst = self.rm.open_resource(port, read_termination = '\n')
        dc_power = DCPowerSupply(inst, saved_files_path)
        if dc_power == None:
            raise ValueError("DC Power Supply failed to connect.")
        
        return dc_power
    
    def connect_rf_switch(self,port,saved_files_path = None) -> RF_Switch:
        """Connect to the RF Switch and return a RF_Switch object.
        
        :param saved_files_path: Path to save files for the RF Switch.
        :type saved_files_path: str
        :return: RF_Switch object connected to the RF Switch.
        :rtype: RF_Switch"""

        if port == None:
            port = "TCPIP0::192.168.0.8::8249::SOCKET"
        
        inst = self.rm.open_resource(port)

        # For SOCKET programming, we want to tell VISA to use a terminating character
        #   to end a read and write operation.
        inst.read_termination = '\n'
        inst.write_termination = '\n'

        return RF_Switch(inst,saved_files_path)
    def connect_digital_attenuators(self,saved_files_path = None):
        """Connect to the Vanuix Digital Attenuator and return a DigitalAttenuator object.
        
        :param saved_files_path: Path to save files for the Digital Attenuator.
        :type saved_files_path: str
        :return: DigitalAttenuator object connected to the Vanuix Digital Attenuator.
        :rtype: DigitalAttenuator"""

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
            
            return DigitalAttenuator(vnx, devid, saved_files_path)
        
            
    def disconnect(self, instruments):
        """Disconnects and cleans up all instrument objects from memory.
        
        :param instruments: Instrument object or list of Instrument objects to disconnect.
        :type instruments: Instrument or list of Instrument"""

        if type(instruments) is not list:
            instruments = [instruments]
        for i in instruments:
            i.disconnect()
        
        #cleans up all instrument objects from memory
        del instruments
        self.rm.close()
            