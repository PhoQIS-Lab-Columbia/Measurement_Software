from Instruments import oscilloscope_rigol
import pyvisa

from network_manager import NetworkManager
from EInstrument import EInstrument
import time
from PIL import Image
rm = pyvisa.ResourceManager()
insturment_list = [] #types the name of the instruments you want to query 
resources = rm.list_resources()
print(resources)
#id = inst.query('*IDN?')
nm = NetworkManager()
#Can connect to all instruments with empty list
#instruments = nm.connect_instruments([])
#instruments = nm.connect_instruments([EInstrument.OSCILLOSCOPE,EInstrument.SPECTRUM_ANALYZER])
#Or can connect to each instrument seperately
#osc = nm.connect_oscilloscope()

#Put your instrument settings here
"""osc.set_waveform_format(fmt="ASCII")
print(osc.get_waveform_format())
osc.run()
time.sleep(3)
osc.stop()"""

#Read out any data
#If you want to save the data to a file everytime the function is run, leave 
#The default path for saved data is "~/Measurement_Software/Experiments/Outputs"
#osc.enable_auto_saving_data()
#img = osc.get_display_data()

#Disconnect all instruments 
#nm.disconnect(instruments)