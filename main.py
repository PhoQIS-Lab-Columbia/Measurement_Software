from Instruments import oscilloscope_rigol
import pyvisa
import platform
from network_manager import NetworkManager
from EInstrument import EInstrument
import time
from Instruments import vector_network_analyzer_copper_mountain
from Instruments import flowmeter_keyence
from PIL import Image
from Instruments import spectrum_analyzer_signal_hound
import time
import json
import subprocess
import sys
from ctypes import *
import struct
rm = pyvisa.ResourceManager()
insturment_list = [] #types the name of the instruments you want to query 
"""resources = rm.list_resources()
print(resources)
inst = rm.open_resource('TCPIP0::localhost::5025::SOCKET')

# For SOCKET programming, we want to tell VISA to use a terminating character
#   to end a read and write operation.
inst.read_termination = '\n'
inst.write_termination = '\n'"""



# Set the measurement mode to sweep

"""inst = rm.open_resources('TCPIP0::192.168.0.215::inst0::INSTR')
print(inst.query('*IDN?'))"""
nm = NetworkManager()
rf = nm.connect_rf_switch()
"""if struct.calcsize("P") * 8 == 32:
    vnx = cdll.LoadLibrary("C:/Users/phoqi/Desktop/Measurement_Software/Instruments/digital_attenuator_vanuix/VNX_atten.dll")
elif struct.calcsize("P") * 8 == 64:
    vnx = cdll.LoadLibrary("C:/Users/phoqi/Desktop/Measurement_Software/Instruments/digital_attenuator_vanuix/VNX_atten64.dll")
else:
    raise NotImplementedError("Unsupported operating system")

vnx.fnLDA_SetTestMode(False)

devices_num = vnx.fnLDA_GetNumDevices()
        # Create an array of device ids for connected devices
DeviceIDArray = c_int * devices_num
devices_list = DeviceIDArray()

print("Device number: "+str(devices_num))
print(len(devices_list))"""
#sa = nm.connect_spectrum_analyzer()
#dc = nm.connect_dc_power_supply()
#da = nm.connect_digital_attenuator()
#print(da.get_attenuation_step())
#vna = nm.connect_vector_network_analyzer()
#TODO Change the channel names because it's bothering me
#Take classes out for ease of use (so does not do a double object)
"""vna.status.get_operation_status_event()
vna.trigger.average.enable_average()
vna.trigger.get_source()
vna.output.enable_output()

vna.calculate_channel1.get_corrected_data()"""

#Can connect to all instruments with empty list
#instruments = nm.connect_instruments([])
#instruments = nm.connect_instruments([EInstrument.OSCILLOSCOPE,EInstrument.SPECTRUM_ANALYZER])
#Or can connect to each instrument seperately
"""dc = nm.connect_dc_power_supply()
print(dc.get_id())
dc.enable_output_channel('CH3')
dc.enable_output_channel('CH2')
dc.channel2.voltage.set(15)
print(dc.channel2.voltage.get())"""
#print(dc.get_id())
#osc = nm.connect_oscilloscope()
#sa = spectrum_analyzer_signal_hound.SpectrumAnalyzer(None)
"""app = subprocess.Popen(['C:/Program Files/Signal Hound/Spike/Spike.exe'], shell=False)
time.sleep(2)
app.terminate()
sys.exit()"""
#sa.app.terminate()
#app = subprocess.Popen(['C:/VNA/S4VNA/S4VNA.exe'], shell = False)
    #Helper Functions

#time.sleep(2)
#app.terminate()
#Put your instrument ttings here
"""osc.set_waveform_format(fmt="ASCII")
print(osc.get_waveform_format())
osc.run()
time.sleep(3)
osc.stop()"""
#print(platform.system())
#Read out any data
#If you want to save the data to a file everyti
# me the function is run, leave 
#The default path for saved data is "~/Measurement_Software/Experiments/Outputs"
#osc.enable_auto_saving_data()
#img = osc.get_display_data()

#Disconnect all instruments 
#nm.disconnect(instruments)
"""sa = spectrum_analyzer_signal_hound.SpectrumAnalyzer(None)
time.sleep(9)
sa.disconnect()
print("termination")"""