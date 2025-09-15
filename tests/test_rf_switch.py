import unittest
from Instruments import spectrum_analyzer_signal_hound
import pyvisa
from Instruments.network_manager import NetworkManager
import time
import os
class TestRFSwitch(unittest.TestCase):
    def setup(self):
        nm = NetworkManager()
        rf = nm.connect_rf_switch()
        return rf
    
    def test_connection(self):
        rm = pyvisa.ResourceManager()
        nm = NetworkManager(rm)
        print(rm.list_resources())
        rf = nm.connect_rf_switch()
        self.assertIsNotNone(rf, "Lock In Amp connection failed.")
    def test_get_status(self):
        rf = self.setup()
        status = rf.switch1.get_status()
        print(status)
        self.assertIsNotNone(status, "RF Switch status fetch failed.")
        self.assertIn("RF_SWITCH", status, "RF Switch status should contain 'RF_SWITCH'.")

    