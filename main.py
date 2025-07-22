from Instruments import oscilloscope_rigol
import pyvisa

from network_manager import NetworkManager

rm = pyvisa.ResourceManager()
insturment_list = [] #types the name of the instruments you want to query 
print(rm.list_resources())
print(rm)
#inst = rm.open_resource("TCPIP0::128.59.65.98::INSTR")
nm = NetworkManager()
#nm.add_new_instrument("fake", rm.list_resources(),rm)
#Add auto connection
#r = rm.open_resource('USB0::0x1AB1::0x0517::DS1ZE264M00036::INSTR')
#ro = oscilloscope_rigol.Oscilloscope(r)
#inst = rm.open_resource('TCPIP0::128.59.65.98::INSTR')
#id = inst.ask('*IDN')
