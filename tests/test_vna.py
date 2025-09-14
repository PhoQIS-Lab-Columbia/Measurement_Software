import unittest
from Instruments import spectrum_analyzer_signal_hound
import pyvisa
from network_manager import NetworkManager
import time
import os
class TestVNA(unittest.TestCase):
    def setup(self):
        nm = NetworkManager()
        vna = nm.connect_vector_network_analyzer()
        return vna
    
    def test_connection(self):
        rm = pyvisa.ResourceManager()
        nm = NetworkManager(rm)
        print(rm.list_resources())
        vna = nm.connect_vector_network_analyzer()
        self.assertIsNotNone(vna, "Vector Network Analyzer connection failed.")

    
    # --- Data Tests ---
    def test_get_analysis_result_data(self):
        vna = self.setup()
        vna.data_handler.enable_auto_saving_data()
        data = vna.calculate_channel1.trace_analysis.get_analysis_result_data()
        self.assertIsNotNone(data, "Analysis result data fetch failed.")
        self.assertGreater(len(data), 0, "Analysis result data should not be empty.")
        expected_file = os.path.join(vna.data_handler.file_path, "ANALYSIS_RESULT_DATA.csv")
        self.assertTrue(os.path.exists(expected_file), "ANALYSIS_RESULT_DATA data file should exist after fetch.")

    def test_get_limit_line_table(self):
        vna = self.setup()
        vna.data_handler.enable_auto_saving_data()
        result = vna.calculate_channel1.limit.get_limit_line_table()
        self.assertIsInstance(result, str, "Limit line table should be a string.")
        self.assertGreater(len(result), 0, "Limit line table string should not be empty.")

    def test_get_all_marker_data(self):
        vna = self.setup()
        vna.data_handler.enable_auto_saving_data()
        data = vna.calculate_channel1.marker.get_all_marker_data()
        self.assertIsNotNone(data, "All marker data fetch failed.")
        self.assertGreater(len(data), 0, "All marker data should not be empty.")
        expected_file = os.path.join(vna.data_handler.file_path, "ALL_MARKER_DATA.csv")
        self.assertTrue(os.path.exists(expected_file), "ALL_MARKER_DATA data file should exist after fetch.")

    def test_get_bandwidth_search_result(self):
        vna = self.setup()
        vna.data_handler.enable_auto_saving_data()
        marker = 1
        data = vna.calculate_channel1.marker.get_bandwidth_search_result(marker)
        self.assertIsNotNone(data, "Bandwidth search result fetch failed.")
        self.assertGreater(len(data), 0, "Bandwidth search result should not be empty.")
        expected_file = os.path.join(vna.data_handler.file_path, f"BANDWIDTH_SEARCH_RESULT_MARKER{marker}.csv")
        self.assertTrue(os.path.exists(expected_file), f"BANDWIDTH_SEARCH_RESULT_MARKER{marker} data file should exist after fetch.")

    def test_get_formatted_data(self):
        vna = self.setup()
        vna.data_handler.enable_auto_saving_data()
        data = vna.calculate_channel1.get_formatted_data()
        self.assertIsNotNone(data, "Formatted data fetch failed.")
        self.assertGreater(len(data), 0, "Formatted data should not be empty.")
        expected_file = os.path.join(vna.data_handler.file_path, "FORMATTED_DATA.csv")
        self.assertTrue(os.path.exists(expected_file), "FORMATTED_DATA data file should exist after fetch.")

    def test_get_formatted_memory(self):
        vna = self.setup()
        vna.data_handler.enable_auto_saving_data()
        data = vna.calculate_channel1.get_formatted_memory()
        self.assertIsNotNone(data, "Formatted memory fetch failed.")
        self.assertGreater(len(data), 0, "Formatted memory should not be empty.")
        expected_file = os.path.join(vna.data_handler.file_path, "FORMATTED_MEMORY.csv")
        self.assertTrue(os.path.exists(expected_file), "FORMATTED_MEMORY data file should exist after fetch.")

    def test_get_corrected_data(self):
        vna = self.setup()
        vna.data_handler.enable_auto_saving_data()
        data = vna.sense_channel1.data.get_corrected_data()
        self.assertIsNotNone(data, "Corrected data fetch failed.")
        self.assertGreater(len(data), 0, "Corrected data should not be empty.")
        expected_file = os.path.join(vna.data_handler.file_path, "CORRECTED_DATA.csv")
        self.assertTrue(os.path.exists(expected_file), "CORRECTED_DATA data file should exist after fetch.")

    def test_get_corrected_memory(self):
        vna = self.setup()
        vna.data_handler.enable_auto_saving_data()
        data = vna.calculate_channel1.get_corrected_memory()
        self.assertIsNotNone(data, "Corrected memory fetch failed.")
        self.assertGreater(len(data), 0, "Corrected memory should not be empty.")
        expected_file = os.path.join(vna.data_handler.file_path, "CORRECTED_MEMORY.csv")
        self.assertTrue(os.path.exists(expected_file), "CORRECTED_MEMORY data file should exist after fetch.")

    def test_get_x_axis(self):
        vna = self.setup()
        vna.data_handler.enable_auto_saving_data()
        data = vna.calculate_channel1.get_x_axis()
        self.assertIsNotNone(data, "X-axis data fetch failed.")
        self.assertGreater(len(data), 0, "X-axis data should not be empty.")
        expected_file = os.path.join(vna.data_handler.file_path, "X_AXIS.csv")
        self.assertTrue(os.path.exists(expected_file), "X_AXIS data file should exist after fetch.")


    
    
    