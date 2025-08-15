from Instruments import oscilloscope_rigol
import pyvisa
import platform
from network_manager import NetworkManager
from EInstrument import EInstrument
import time
from Instruments import vector_network_analyzer_copper_mountain
from PIL import Image
from Instruments import spectrum_analyzer_signal_hound
import time
import subprocess
import sys
rm = pyvisa.ResourceManager()
insturment_list = [] #types the name of the instruments you want to query 
#resources = rm.list_resources()
#print(resources)
#switch = rm.open_resource()
#id = inst.query('*IDN?')
#nm = NetworkManager()
#Can connect to all instruments with empty list
#instruments = nm.connect_instruments([])
#instruments = nm.connect_instruments([EInstrument.OSCILLOSCOPE,EInstrument.SPECTRUM_ANALYZER])
#Or can connect to each instrument seperately
#osc = nm.connect_oscilloscope()
#sa = spectrum_analyzer_signal_hound.SpectrumAnalyzer(None)
app = subprocess.Popen(['C:/Program Files/Signal Hound/Spike/Spike.exe'], shell=True)
time.sleep(2)
app.terminate()
sys.exit()
#sa.app.terminate()

"""vna = vector_network_analyzer_copper_mountain.VNA(None)
vna.open_software()
time.sleep(2)
vna.app.terminate()"""
#Put your instrument settings here
"""osc.set_waveform_format(fmt="ASCII")
print(osc.get_waveform_format())
osc.run()
time.sleep(3)
osc.stop()"""
#print(platform.system())
#Read out any data
#If you want to save the data to a file everytime the function is run, leave 
#The default path for saved data is "~/Measurement_Software/Experiments/Outputs"
#osc.enable_auto_saving_data()
#img = osc.get_display_data()

#Disconnect all instruments 
#nm.disconnect(instruments)