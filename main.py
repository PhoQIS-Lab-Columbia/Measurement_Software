from flowmeter_keyence import Flowmeter
from dc_power_supply_siglent import DCPowerSupply
from oscilloscope_rigol import Oscilloscope
from spectrum_analyzer_signal_hound import SpectrumAnalyzer
from vector_network_analyzer_copper_mountain import VNA
import time
from network_manager import NetworkManager
import pyvisa
from EInstrument import EInstrument
# Initialize the instruments
#There will be some pop ups
nm = NetworkManager()
rm = pyvisa.ResourceManager()
#dc = nm.connect_dc_power_supply()
port = 'TCPIP0::192.168.0.8::8249::SOCKET'
rf = rm.open_resource(port)
rf.read_termination = '\n'
rf.write_termination = '\n'
rf.write("Reset")
time.sleep(0.3)
print("Both channel status "+str(rf.write("Read_Channel_Status?")))
print(rf.write("CH1_Status?"))
time.sleep(0.3)
rf.write("CH1_1_ON")
time.sleep(0.3)
print("Both channel status "+str(rf.write("Read_Channel_Status?")))
print(rf.write("CH1_Status?"))
time.sleep(0.3)
rf.write("CH1_1_OFF")
time.sleep(0.3)
print("Both channel status "+str(rf.write("Read_Channel_Status?")))
time.sleep(0.3)
print(rf.write("CH1_Status?"))
time.sleep(0.3)
rf.write("CH1_5_ON")
time.sleep(0.3)
print("Both channel status "+str(rf.write("Read_Channel_Status?\r")))
time.sleep(0.3)
print(rf.query("CH1_Status?\r"))
time.sleep(0.3)
rf.write("CH1_5_OFF")
time.sleep(0.3)
print("Both channel status "+str(rf.query("Read_Channel_Status?")))
time.sleep(0.3)
print(rf.write("CH1_Status"))

'''rfs = nm.connect_rf_switch()
rfs.switch1.channel_5.disable()
print(rfs.switch1.get_status())
rfs.switch1.channel_1.enable()
print(rfs.switch1.get_status())
rfs.switch1.channel_1.disable()
print(rfs.switch1.get_status())
rfs.switch1.channel_5.enable()
print(rfs.switch1.get_status())'''
"""osc = nm.connect_oscilloscope()
vna = nm.connect_vector_network_analyzer()
sa = nm.connect_spectrum_analyzer()
fm = nm.connect_flowmeter()
csv1 = "20250912_021011.csv"
fm.add_csv(0,csv1) # Add the csv file path for flowmeter 1
data = fm.load_csv() # Load the csv data into a list of dictionaries
#Run an experiment here. Add any PCB board code, set timer and loops

osc.timebase.set_delay_offset(0)
osc.trigger.set_mode("'RS232'")
sa.format.get_trace_data_format()
sa.sense.pathloss1.set_enabled(True)
sa.record.trigger.zerospan.set_source("EXTERNAL")
vna.calculate_channel13.set_phase_offset(0)
avg_count = vna.trigger.get_source()
osc.channel1.set_scale(0.5)
osc.run()
sa.sense.bluetooth.set_channel_index(1)
# Data Processing
print(data)
#Disconnect all instruments and close applications
nm.disconnect([osc,vna,sa,fm])"""