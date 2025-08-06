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
        atten = nm.connect_digital_attenuator()
        self.assertIsNotNone(atten, "Data Attenuator connection failed.")

    def test_get_device_status(self):
        attenuator = self.setup()
        
        status = attenuator.get_device_status()
        print(status)
        self.assertIsNotNone(status, "Device status fetch failed.")
        self.assertIn("", status, "Device status should contain 'ATTENUATOR'.")
       

    