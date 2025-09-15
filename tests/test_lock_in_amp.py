import unittest
from Instruments import spectrum_analyzer_signal_hound
import pyvisa
from Instruments.network_manager import NetworkManager
import time
import os
class TestLockInAmp(unittest.TestCase):
    def setup(self):
        nm = NetworkManager()
        lockinamp = nm.connect_lock_in_amp()
        return lockinamp
    
    def test_connection(self):
        rm = pyvisa.ResourceManager()
        nm = NetworkManager(rm)
        print(rm.list_resources())
        lockinamp = nm.connect_lock_in_amp()
        self.assertIsNotNone(lockinamp, "Lock In Amp connection failed.")

    def test_get_detection_frequency(self):
        lockinamp = self.setup()
        
        freq = lockinamp.reference.frequency.get_detection_frequency()
        print(freq)
        
    def test_get_screenshot_image(self):
        lockinamp = self.setup()
        
        image = lockinamp.display.get_screenshot_image()
        self.assertIsNotNone(image, "Screenshot image fetch failed.")
        self.assertTrue(os.path.exists(image), "Screenshot image file should exist after fetch.")
        print(f"Screenshot saved at: {image}")

        
       

