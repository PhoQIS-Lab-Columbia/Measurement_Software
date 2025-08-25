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
import subprocess
import sys
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
sa = nm.connect_spectrum_analyzer()
sa.display.show()
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