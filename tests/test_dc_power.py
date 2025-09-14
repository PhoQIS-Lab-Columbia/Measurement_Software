import unittest
from Instruments import spectrum_analyzer_signal_hound
import pyvisa
from network_manager import NetworkManager
import time
import os
class TestDCPowerSupply(unittest.TestCase):
    def setup(self):
        nm = NetworkManager()
        atten = nm.connect_dc_power_supply()
        return atten
    
    def test_connection(self):
        rm = pyvisa.ResourceManager()
        nm = NetworkManager(rm)
        print(rm.list_resources())
        atten = nm.connect_dc_power_supply()
        self.assertIsNotNone(atten, "DC Power Supply connection failed.")
    
    def test_recall(self):
        dc = self.setup()
        dc.save("default")
        state = dc.recall("default")
        print(state)

       

    