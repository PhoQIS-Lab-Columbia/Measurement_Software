from Instruments.flowmeter_keyence import Flowmeter
from Instruments.dc_power_supply_siglent import DCPowerSupply
from Instruments.oscilloscope_rigol import Oscilloscope
from Instruments.spectrum_analyzer_signal_hound import SpectrumAnalyzer
from Instruments.vector_network_analyzer_copper_mountain import VNA
import time
from Instruments.network_manager import NetworkManager
import pyvisa
from Instruments.data_handler import DataHandler
# Initialize the instruments
#There will be some pop ups
nm = NetworkManager()
dh = DataHandler()

rf = nm.connect_rf_switch()
osc = nm.connect_oscilloscope()
vna = nm.connect_vector_network_analyzer()
sa = nm.connect_spectrum_analyzer()
fm = nm.connect_flowmeter()
csv1 = "20250912_021011.csv"
#fm.add_csv(0,csv1) # Add the csv file path for flowmeter 1
#data = fm.load_csv() # Load the csv data into a list of dictionaries
#Run an experiment here. Add any PCB board code, set timer and loops

osc.timebase.set_delay_offset(0)
osc.trigger.set_mode("'RS232'")
sa.format.get_trace_data_format()
sa.sense.pathloss1.set_enabled(True)
sa.record.trigger.zerospan.set_source("EXTERNAL")
vna.calculate_channel13.set_phase_offset(0)
avg_count = vna.trigger.get_source()
osc.channel_1.set_scale(0.5)
osc.run()
sa.sense.bluetooth.set_channel_index(1)
osc.stop()
# Data Processing

time.sleep(4)
#Disconnect all instruments and close applications
nm.disconnect([osc,vna,sa,fm])