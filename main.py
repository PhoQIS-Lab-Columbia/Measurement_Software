from Instruments import oscilloscope_rigol
import pyvisa
import vxi11
from network_manager import NetworkManager
from EInstrument import EInstrument
rm = pyvisa.ResourceManager()

insturment_list = [] #types the name of the instruments you want to query 
print(rm.list_resources())
print(rm)
inst = rm.open_resource('TCPIP0::192.168.0.215::inst0::INSTR')
nm = NetworkManager()
instruments = nm.connect_instruments([EInstrument.OSCILLOSCOPE])
#nm.add_new_instrument("fake", rm.list_resources(),rm)
#Add auto connection
#r = rm.open_resource('USB0::0x1AB1::0x0517::DS1ZE264M00036::INSTR')
#ro = oscilloscope_rigol.Oscilloscope(r)
#inst = rm.open_resource('TCPIP0::128.59.65.98::INSTR')
print(instruments)
nm.disconnect(instruments)
print(rm.list_opened_resources())
