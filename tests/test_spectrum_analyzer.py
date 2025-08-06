import unittest
from Instruments import spectrum_analyzer_signal_hound
import pyvisa
from network_manager import NetworkManager
import time
import os
class TestSpectrumAnalyzer(unittest.TestCase):
    def setup(self):
        nm = NetworkManager()
        spec_ana = nm.connect_spectrum_analyzer()
        return spec_ana
    
    def test_connection(self):
        rm = pyvisa.ResourceManager()
        nm = NetworkManager(rm)
        print(rm.list_resources())
        spec_ana = nm.connect_spectrum_analyzer()
        self.assertIsNotNone(spec_ana, "Spectrum Analyzer connection failed.")

    
    # --- Display Tests ---
    def test_is_spike_hidden(self):
        spec = self.setup()

        h = spec.display.is_hidden()
        self.assertFalse(h, "Spike window should not be hidden by default.")

    def test_hide_spike(self):
        #Open spike window, start with visible
        spec = self.setup()
        spec.display.hide()
        #See if his window
        
        self.assertTrue(spec.display.is_hidden(), "Spike window should be hidden.")
        time.sleep(2)
        spec.display.show()
        self.assertFalse(spec.display.is_hidden(), "Spike window should be visible after showing it.")

    #Test data writing
    def test_fetch_am(self):
        spec = self.setup()
        data = spec.sense.ademod.fetch.am()
        spec.data_handler.enable_auto_saving_data()
        self.assertIsNotNone(data, "AM data fetch failed.")
        self.assertGreater(len(data), 0, "AM data should not be empty.")
        self.assertTrue(os.path.exists(spec.data_handler.file_path+"ADEMod_AM.csv"), "AM data file should exist after fetch.")
    
    def test_fetch_fm(self):
        spec = self.setup()
        spec.data_handler.enable_auto_saving_data()
        data = spec.sense.ademod.fetch.fm()
        self.assertIsNotNone(data, "FM data fetch failed.")
        self.assertGreater(len(data), 0, "FM data should not be empty.")
        self.assertTrue(os.path.exists(spec.data_handler.file_path+"ADEMod_FM.csv"), "AM data file should exist after fetch.")
    
    def test_get_ddemod_iq_data(self):
        spec = self.setup()
        # Enable auto saving to test file writing
        spec.data_handler.enable_auto_saving_data()
        # Mock the instrument query response if needed, or call directly if hardware is available
        # Here we assume the instrument returns a non-empty string of IQ data
        data = spec.sense.ddemod.custom.iq.get_data()
        self.assertIsNotNone(data, "DDEMod IQ data fetch failed.")
        self.assertGreater(len(data), 0, "DDEMod IQ data should not be empty.")
        # Check if file was written
        expected_file = os.path.join(spec.data_handler.file_path, "DDEMOD_IQ.csv")
        self.assertTrue(os.path.exists(expected_file), "DDEMod IQ data file should exist after fetch.")
    
    def test_get_ddemod_trace_sweep_data(self):
        spec = self.setup()
        # Enable auto saving to test file writing
        spec.data_handler.enable_auto_saving_data()
        # Fetch the trace sweep data
        data = spec.sense.ddemod.trace.sweep.get_data()
        self.assertIsNotNone(data, "DDEMod trace sweep data fetch failed.")
        self.assertGreater(len(data), 0, "DDEMod trace sweep data should not be empty.")
        # Check if file was written
        expected_file = os.path.join(spec.data_handler.file_path, "TRACE_SWEEP.csv")
        self.assertTrue(os.path.exists(expected_file), "DDEMod trace sweep data file should exist after fetch.")
    
    def test_fetch_metrics_single(self):
        spec = self.setup()
        # Mock instrument query and data handler if needed
        metrics = 1
        # Assume instrument.query returns a string of values
        response, = spec.sense.ddemod.fetch(metrics)
        self.assertIsInstance(response, str, "Fetch should return a string response for single metric.")
        self.assertGreater(len(response), 0, "Fetch response should not be empty for single metric.")
        expected_file = os.path.join(spec.data_handler.file_path, "DDEMOD_METRICS.csv")
        self.assertTrue(os.path.exists(expected_file), "DDEMOD_METRICS data file should exist after fetch.")

    def test_fetch_metrics_multiple(self):
        spec = self.setup()
        metrics = [1, 2, 3]
        response, = spec.sense.ddemod.fetch(metrics)
        self.assertIsInstance(response, str, "Fetch should return a string response for multiple metrics.")
        self.assertGreater(len(response), 0, "Fetch response should not be empty for multiple metrics.")
        expected_file = os.path.join(spec.data_handler.file_path, "DDEMOD_METRICS.csv")
        self.assertTrue(os.path.exists(expected_file), "DDEMOD_METRICS data file should exist after fetch.")


    def test_get_pathloss_data(self):
        spec = self.setup()
        # Assume spec.sense.correction.pathloss[0] exists and is configured
        pathloss = spec.sense.correction.pathloss[0]
        response = pathloss.get_data()
        self.assertIsInstance(response, str, "get_data should return a string response.")
        self.assertGreater(len(response), 0, "Pathloss data should not be empty.")
        expected_file = os.path.join(spec.data_handler.file_path, "CORR_PATHLOSS.csv")
        self.assertTrue(os.path.exists(expected_file), "CORR_PATHLOSS data file should exist after get_data.")

    def test_get_offset_parameters(self):
        spec = self.setup()
        response = spec.sense.semask.get_offset_parameters()
        self.assertIsInstance(response, str, "get_offset_parameters should return a string response.")
        self.assertGreater(len(response), 0, "Offset parameters should not be empty.")
        expected_file = os.path.join(spec.data_handler.file_path, "SEMASK_OFFSET.csv")
        self.assertTrue(os.path.exists(expected_file), "SEMASK_OFFSET data file should exist after get_offset_parameters.")
    
    def test_get_enr_table_data(self):
        spec = self.setup()
        # Enable auto saving to test file writing
        spec.data_handler.enable_auto_saving_data()
        # Assume spec.sense.correction.enr exists and is configured
        enr = spec.sense.nfigure.correction.enr_table
        response, = enr.get_data()
        self.assertIsInstance(response, str, "get_data should return a string response for ENR table.")
        self.assertGreater(len(response), 0, "ENR table data should not be empty.")
        expected_file = os.path.join(spec.data_handler.file_path, "CORR_ENR.csv")
        self.assertTrue(os.path.exists(expected_file), "CORR_ENR data file should exist after get_data.")

    def test_get_noise_figure(self):
        spec = self.setup()
        # Enable auto saving to test file writing
        spec.data_handler.enable_auto_saving_data()
        # Assume spec.sense.nfigure exists and is configured
        nfigure = spec.sense.nfigure.fetch
        response, = nfigure.get_nfigure()
        self.assertIsInstance(response, str, "get_nfigure should return a string response for noise figure.")
        self.assertGreater(len(response), 0, "Noise figure data should not be empty.")
        expected_file = os.path.join(spec.data_handler.file_path, "NFIGURE_FETCH.csv")
        self.assertTrue(os.path.exists(expected_file), "NFIGURE_FETCH data file should exist after get_nfigure.")

    def test_get_gain(self):
        spec = self.setup()
        # Enable auto saving to test file writing
        spec.data_handler.enable_auto_saving_data()
        # Assume spec.sense.nfigure exists and is configured
        nfigure = spec.sense.nfigure.fetch
        response, = nfigure.get_gain()
        self.assertIsInstance(response, str, "get_gain should return a string response for gain.")
        self.assertGreater(len(response), 0, "Gain data should not be empty.")
        expected_file = os.path.join(spec.data_handler.file_path, "NFIG_FETCH.csv")
        self.assertTrue(os.path.exists(expected_file), "NFIG_FETCH data file should exist after get_gain.")

    def test_fetch_bluetooth_metrics_single(self):
        spec = self.setup()
        # Enable auto saving to test file writing
        spec.data_handler.enable_auto_saving_data()
        # Assume spec.sense.bluetooth exists and is configured
        bluetooth = spec.sense.bluetooth
        metrics = 1
        response = bluetooth.trigger.fetch(metrics)
        self.assertIsInstance(response, str, "fetch should return a string response for single Bluetooth metric.")
        self.assertGreater(len(response), 0, "Bluetooth fetch response should not be empty for single metric.")
        expected_file = os.path.join(spec.data_handler.file_path, "BLUETOOTH_FETCH.csv")
        self.assertTrue(os.path.exists(expected_file), "BLUETOOTH_FETCH data file should exist after fetch.")

    def test_fetch_bluetooth_metrics_multiple(self):
        spec = self.setup()
        # Enable auto saving to test file writing
        spec.data_handler.enable_auto_saving_data()
        # Assume spec.sense.bluetooth exists and is configured
        bluetooth = spec.sense.bluetooth
        metrics = [1, 2, 3]
        response, = bluetooth.trigger.fetch(metrics)
        self.assertIsInstance(response, str, "fetch should return a string response for multiple Bluetooth metrics.")
        self.assertGreater(len(response), 0, "Bluetooth fetch response should not be empty for multiple metrics.")
        expected_file = os.path.join(spec.data_handler.file_path, "BLUETOOTH_FETCH.csv")
        self.assertTrue(os.path.exists(expected_file), "BLUETOOTH_FETCH data file should exist after fetch.")
    
    def test_fetch_lte_single_metric(self):
        spec = self.setup()
        # Enable auto saving to test file writing
        spec.data_handler.enable_auto_saving_data()
        metrics = 5
        response = spec.sense.lte.fetch(metrics)
        self.assertIsInstance(response, str, "Fetch should return a string response for single LTE metric.")
        self.assertGreater(len(response), 0, "Fetch response should not be empty for single LTE metric.")
        expected_file = os.path.join(spec.data_handler.file_path, "FETCH_LTE.csv")
        self.assertTrue(os.path.exists(expected_file), "FETCH_LTE data file should exist after fetch.")

    def test_fetch_lte_multiple_metrics(self):
        spec = self.setup()
        # Enable auto saving to test file writing
        spec.data_handler.enable_auto_saving_data()
        metrics = [1, 2, 3]
        response = spec.sense.lte.fetch(metrics)
        self.assertIsInstance(response, str, "Fetch should return a string response for multiple LTE metrics.")
        self.assertGreater(len(response), 0, "Fetch response should not be empty for multiple LTE metrics.")
        expected_file = os.path.join(spec.data_handler.file_path, "FETCH_LTE.csv")
        self.assertTrue(os.path.exists(expected_file), "FETCH_LTE data file should exist after fetch.")


    def test_get_data_y(self):
        spec = self.setup()
        spec.data_handler.enable_auto_saving_data()
        response = spec.trace.pnoise.get_data_y()
        self.assertIsInstance(response, str, "get_data_y should return a string response.")
        self.assertGreater(len(response), 0, "get_data_y response should not be empty.")
        expected_file = os.path.join(spec.data_handler.file_path, "PNOISE_Y.csv")
        self.assertTrue(os.path.exists(expected_file), "PNOISE_Y data file should exist after get_data_y.")

    def test_get_data_x(self):
        spec = self.setup()
        spec.data_handler.enable_auto_saving_data()
        response = spec.trace.pnoise.get_data_x()
        self.assertIsInstance(response, str, "get_data_x should return a string response.")
        self.assertGreater(len(response), 0, "get_data_x response should not be empty.")
        expected_file = os.path.join(spec.data_handler.file_path, "PNOISE_X.csv")
        self.assertTrue(os.path.exists(expected_file), "PNOISE_X data file should exist after get_data_x.")

    def test_get_trace_data(self):
        spec = self.setup()
        spec.data_handler.enable_auto_saving_data()
        response = spec.trace.get_data()
        self.assertIsInstance(response, str, "get_data should return a string response for trace data.")
        self.assertGreater(len(response), 0, "Trace data response should not be empty.")
        expected_file = os.path.join(spec.data_handler.file_path, "TRACE_DATA.csv")
        self.assertTrue(os.path.exists(expected_file), "TRACE_DATA data file should exist after get_data.")