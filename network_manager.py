import json
import pyvisa
import os
from ctypes import *
import ctypes
import struct
import subprocess

from Instruments.oscilloscope_rigol import Oscilloscope
from Instruments.spectrum_analyzer_signal_hound import SpectrumAnalyzer
from Instruments.vector_network_analyzer_copper_mountain import VNA
from EInstrument import EInstrument
from Instruments.digital_attenuator_vanuix import digital_attenuator
from Instruments.signal_generator_signal_core import signal_generator
from Instruments.lock_in_amp_srs import LockInAmp
from Instruments.rf_switch import RF_Switch
from Instruments.dc_power_supply_siglent import DCPowerSupply
from Instruments.flowmeter_keyence import Flowmeter
import time

class NetworkManager:
    def __init__(self, rm = pyvisa.ResourceManager()):
        self.rm = rm

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
            return self.connect_digital_attenuator(saved_files_path)
        elif name == EInstrument.SIGNAL_GENERATOR.value or name == EInstrument.SIGNAL_GENERATOR:
            return self.connect_signal_generator(saved_files_path)
        elif name == EInstrument.LOCK_IN_AMP.value or name == EInstrument.LOCK_IN_AMP:
            return LockInAmp(instrument,saved_files_path)
        elif name == EInstrument.RF_SWITCH.value or name == EInstrument.RF_SWITCH:
            return RF_Switch(instrument, saved_files_path)
        elif name == EInstrument.DC_POWER_SUPPLY.value or name == EInstrument.DC_POWER_SUPPLY:
            return DCPowerSupply(instrument, saved_files_path)
        elif name == EInstrument.FLOW_METER.value or name == EInstrument.FLOW_METER:
            return Flowmeter()
        else:
            raise ValueError(f"Instrument {name} is not recognized.")

    def connect_flow_meter(self):
        return Flowmeter(None)
    
    def connect_instruments(self, instrument_list = [], saved_files_path = None):
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
            instruments.append(self.connect_digital_attenuator(saved_files_path))
        if instrument_list == [] or EInstrument.SIGNAL_GENERATOR in instrument_list:
            instruments.append(self.connect_signal_generator(saved_files_path))
        print("Abount to leave connect instrument.")
        return instruments
    
    def connect_flowmeter(self, saved_files_path = None) -> Flowmeter:
        return Flowmeter()
    
    def connect_oscilloscope(self,saved_files_path = None) -> Oscilloscope:
        osc = self.connect_instruments([EInstrument.OSCILLOSCOPE],saved_files_path)
        print(osc)
        if osc == None:
            raise ValueError("Oscilloscope failed to connect.")
        return osc[0]
            
    def connect_spectrum_analyzer(self,saved_files_path = None) -> SpectrumAnalyzer:
        #try: 
            
        with open('program_paths.json') as file:
            p = json.load(file)
        program_path = p[EInstrument.SPECTRUM_ANALYZER.value]
        app = subprocess.Popen([program_path], shell = False)
        time.sleep(8)
        with open('instrumentPorts.json') as file:
            ip = json.load(file)
        # Open a session to the Spike software, Spike must be running at this point
        port = ip[EInstrument.SPECTRUM_ANALYZER.value]
        inst = self.rm.open_resource(port)

        # For SOCKET programming, we want to tell VISA to use a terminating character
        #   to end a read and write operation.
        inst.read_termination = '\n'
        inst.write_termination = '\n'
        #except:
            #raise ValueError("Spectrum Analyzer failed to connect.")
        return SpectrumAnalyzer(inst,app, program_path,saved_files_path)
    
    def connect_vector_network_analyzer(self,saved_files_path = None) -> VNA:
        try: 
            
            with open('program_paths.json') as file:
                p = json.load(file)
            program_path = p[EInstrument.VECTOR_NETWORK_ANALYZER.value]
            app = subprocess.Popen([program_path], shell = False)
            time.sleep(5)
            with open('instrumentPorts.json') as file:
                ip = json.load(file)
            port = ip[EInstrument.VECTOR_NETWORK_ANALYZER.value]
            
            # Open a session to the S4VNA software, S4VNA must be running at this point
            inst = self.rm.open_resource(port)

            # For SOCKET programming, we want to tell VISA to use a terminating character
            #   to end a read and write operation.
            inst.read_termination = '\n'
            inst.write_termination = '\n'
        except:
            raise ValueError("VNA failed to connect.")
        return VNA(inst,app, program_path,saved_files_path)
        
    
    def connect_lock_in_amp(self,saved_files_path = None) -> LockInAmp:
        lock_in_amp = self.connect_instruments([EInstrument.LOCK_IN_AMP],saved_files_path)
        if lock_in_amp == None:
            raise ValueError("Lock In Amplifier failed to connect.")
        return lock_in_amp[0]
    
    def connect_dc_power_supply(self,saved_files_path = None) -> DCPowerSupply:
        dc_power = self.connect_instruments([EInstrument.DC_POWER_SUPPLY],saved_files_path)
        if dc_power == None:
            raise ValueError("Lock In Amplifier failed to connect.")
        return dc_power[0]
    def connect_rf_switch(self,saved_files_path = None) -> RF_Switch:
        with open('instrumentPorts.json') as file:
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
        
    def connect_signal_generator(self,saved_files_path = None):
        """Connects to the signal generator and returns the instrument object."""
        os.add_dll_directory(os.getcwd())
        # Open the dll
        
        sg = cdll.sc5510a
        # Get the number of devices
        devices_num = sg.sc5510a_search_devices()
        # Create an array of device ids for connected devices
        

        if devices_num > 0:
            # Select which device to use
            devid = 0
            if devices_num == 1:
                devices_list = []
                #TODO: Test if id correctly returned or char array jsut give memory address
                sg.sc5510a_search_devices(devices_list,1)
                sig_gen = sg.sc5510a_open_device(devices_list[0])
            
        return signal_generator(sg, sig_gen,saved_files_path)
            
    def disconnect(self, instruments):
        
        if type(instruments) is not list:
            instruments = [instruments]
        for i in instruments:
            i.disconnect()
        
        #cleans up all instrument objects from memory
        del instruments
        self.rm.close()
            