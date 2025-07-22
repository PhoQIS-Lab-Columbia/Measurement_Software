import unittest
import pyvisa
from network_manager import NetworkManager
from Instruments import oscilloscope_rigol
from data_handler import DataHandler
class TestDataHandler(unittest.TestCase):
    def setup(self):
       nm = NetworkManager()
       osc = nm.connect_oscilloscope()
       return osc
    
    def test_system_parameters_byte_values_change_with_parms(self):
        osc = self.setup()
        osc.auto_save = False
        data1 = osc.get_system_parameters()
        #print("Initial Data "+str(data1))
        osc.set_acquistion_mode("NORMAL")
        osc.set_channel_units(1,"WATT")
    
        data2 = osc.get_system_parameters()
        #print("After Data "+str(data2))
        self.assertNotEqual(data1, data2,"Bytes did not change even with parameter changes.")

    def test_load_parameters_(self):
        osc = self.setup()
        osc.auto_save = False
        
        osc.enable_system_autoscale_key(True)
        osc.set_system_power_on_recall("LAT")
        data1 = osc.get_system_parameters()

        osc.enable_system_autoscale_key(False)
        osc.set_system_power_on_recall("DEF")

        osc.set_system_parameters(data1)
        self.assertTrue(osc.is_system_autoscale_key_enabled())
        self.assertEqual(osc.get_system_power_on_recall(),"LAT")
       
    def test_system_parameters_file_write(self):
        osc = self.setup()
        osc.auto_save = True
        data1 = osc.get_system_parameters()

    def test_waveform(self):
        osc = self.setup()
        osc.auto_save = False
        #data = osc.get_waveform_data()
        #print(data)
    #get_waveform_data
    #get_display_data
    #get_event_table_data
    #get_system_setup
    #set_system_setup
test = TestDataHandler()
test.test_system_parameters_file_write()