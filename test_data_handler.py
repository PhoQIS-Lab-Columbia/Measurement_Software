import unittest
import pyvisa
from network_manager import NetworkManager
from Instruments import oscilloscope_rigol
from Instruments import spectrum_analyzer_signal_hound
from data_handler import DataHandler
from EFileType import EFileType

class TestDataHandler(unittest.TestCase):
    def setup(self):
       nm = NetworkManager()
       osc = nm.connect_oscilloscope()
       return osc
    def test_read_file_csv(self):
        dh = DataHandler()
        file_path = "Experiments/Outputs/test.csv"
        data = dh.read_file(file_path, EFileType.CSV)
        print(data)
        self.assertIsInstance(data, list, "Data read from CSV is not a list.")
        self.assertGreater(len(data), 0, "No data read from CSV file.")
    def test_write_file_csv(self):
        dh = DataHandler()
        headers = ["p1", "p2", "p3","p4","p5"]
        dummy_data = [1,2,3,4,5]
        dh.write_to_file("Experiments/Outputs/test2", dummy_data, file_type=EFileType.CSV, headers=headers)
        data = dh.read_file("Experiments/Outputs/test2.csv", EFileType.CSV)
        print(data)
        self.assertEqual(data[0], headers, "Headers do not match written data.")
        self.assertEqual(data[1], dummy_data, "Data does not match written data.")
        #self.assertEqual(len(data), 2, "Data length does not match expected length of 2 rows.")

    def test_add_to_file_csv(self):
        dh = DataHandler()
        headers = ["p1", "p2", "p3","p4","p5"]
        dummy_data = [1,2,3,4,5]
        dh.write_to_file("Experiments/Outputs/test", dummy_data, file_type=EFileType.CSV, headers=headers)
        data = dh.read_file("Experiments/Outputs/test.csv", EFileType.CSV)
        print(data)
        self.assertEqual(data[0], headers, "Headers do not match written data.")
        self.assertEqual(data[1], dummy_data, "Data does not match written data.")
        #self.assertEqual(len(data), 3, "Data length does not match expected length of 2 rows.")
    
    

    def test_write_file_dict_json(self):
        dh = DataHandler()
        dummy_data = {"p1":1,"p2":2,"p3":3,"p4":4,"p5":5}
        dh.write_to_file("Experiments/Outputs/test", dummy_data, file_type=EFileType.JSON)
        data = dh.read_file("Experiments/Outputs/test", EFileType.JSON)
        print(data)

        self.assertEqual(data, dummy_data, "Data does not match written data.")
        self.assertEqual(len(data), 5, "Data length does not match expected length of 2 rows.")

    def test_read_file_json(self):
        dh = DataHandler()
        file_path = "Experiments/Outputs/test"
        data = dh.read_file(file_path, EFileType.JSON)
        print(data)
        self.assertIsInstance(data, dict, "Data read from Json is not a list.")
        self.assertGreater(len(data), 0, "No data read from Json file.")

    def test_add_to_file_json(self):
        dh = DataHandler()
        dummy_data = {"p6":6,"p7":2,"p8":3,"p9":4,"p10":5}
        dh.write_to_file("Experiments/Outputs/test2", dummy_data, file_type=EFileType.JSON)
        data = dh.read_file("Experiments/Outputs/test2", EFileType.JSON)
        print(data)
        self.assertEqual(len(data), 10, "Data length does not match expected length of 2 rows.")
        #self.assertEqual(data, {"p1":1,"p2":2,"p3":3,"p4":4,"p5":5,"p6":6,"p7":2,"p8":3,"p9":4,"p10":5}, "Data does not match written data.")

class TestSpectrumAnalyzerSignalHound(unittest.TestCase):
    def setUp(self):
        nm = NetworkManager()
        inst = nm.connect_spectrum_analyzer()
        self.sa = spectrum_analyzer_signal_hound.SpectrumAnalyzer(inst)
    
        self.metrics = ["metric1", "metric2"]

    # 1. fetch_am
    def test_fetch_am_returns_dict(self):
        result = self.sa.Sense.ADEMod.Fetch.fetch_am(self.metrics)
        self.assertIsInstance(result, dict)

    def test_fetch_am_write_and_read_file(self):
        data = self.sa.Sense.ADEMod.Fetch.fetch_am(self.metrics)
        self.dh.write_to_file("test_fetch_am", data, file_type=EFileType.JSON)
        loaded = self.dh.read_file("test_fetch_am", EFileType.JSON)
        self.assertEqual(data, loaded)

    def test_fetch_am_set_parameters(self):
        data = self.sa.Sense.ADEMod.Fetch.fetch_am(self.metrics)
        self.sa.Sense.ADEMod.Fetch.set_am(data)
        # Assuming set_am sets internal state, check state or call get_am
        self.assertEqual(self.sa.Sense.ADEMod.Fetch.get_am(), data)

    # 2. fetch_fm
    def test_fetch_fm_returns_dict(self):
        result = self.sa.Sense.ADEMod.Fetch.fetch_fm(self.metrics)
        self.assertIsInstance(result, dict)

    def test_fetch_fm_write_and_read_file(self):
        data = self.sa.Sense.ADEMod.Fetch.fetch_fm(self.metrics)
        self.dh.write_to_file("test_fetch_fm", data, file_type=EFileType.JSON)
        loaded = self.dh.read_file("test_fetch_fm", EFileType.JSON)
        self.assertEqual(data, loaded)

    def test_fetch_fm_set_parameters(self):
        data = self.sa.Sense.ADEMod.Fetch.fetch_fm(self.metrics)
        self.sa.Sense.ADEMod.Fetch.set_fm(data)
        self.assertEqual(self.sa.Sense.ADEMod.Fetch.get_fm(), data)

    # 3. IQ get_data
    def test_iq_get_data_returns_list(self):
        result = self.sa.Sense.DDEMod.Custom.IQ.get_data()
        self.assertIsInstance(result, list)

    def test_iq_get_data_write_and_read_file(self):
        data = self.sa.Sense.DDEMod.Custom.IQ.get_data()
        self.dh.write_to_file("test_iq_data", data, file_type=EFileType.JSON)
        loaded = self.dh.read_file("test_iq_data", EFileType.JSON)
        self.assertEqual(data, loaded)

    def test_iq_get_data_set_parameters(self):
        data = self.sa.Sense.DDEMod.Custom.IQ.get_data()
        self.sa.Sense.DDEMod.Custom.IQ.set_data(data)
        self.assertEqual(self.sa.Sense.DDEMod.Custom.IQ.get_data(), data)

    # 4. Trace Sweep get_data
    def test_trace_sweep_get_data_returns_list(self):
        result = self.sa.Sense.DDEMod.Trace.Sweep.get_data()
        self.assertIsInstance(result, list)

    def test_trace_sweep_get_data_write_and_read_file(self):
        data = self.sa.Sense.DDEMod.Trace.Sweep.get_data()
        self.dh.write_to_file("test_trace_sweep", data, file_type=EFileType.JSON)
        loaded = self.dh.read_file("test_trace_sweep", EFileType.JSON)
        self.assertEqual(data, loaded)

    def test_trace_sweep_get_data_set_parameters(self):
        data = self.sa.Sense.DDEMod.Trace.Sweep.get_data()
        self.sa.Sense.DDEMod.Trace.Sweep.set_data(data)
        self.assertEqual(self.sa.Sense.DDEMod.Trace.Sweep.get_data(), data)

    # 5. DDEMod Fetch fetch
    def test_ddemod_fetch_returns_dict(self):
        result = self.sa.Sense.DDEMod.Fetch.fetch(self.metrics)
        self.assertIsInstance(result, dict)

    def test_ddemod_fetch_write_and_read_file(self):
        data = self.sa.Sense.DDEMod.Fetch.fetch(self.metrics)
        self.dh.write_to_file("test_ddemod_fetch", data, file_type=EFileType.JSON)
        loaded = self.dh.read_file("test_ddemod_fetch", EFileType.JSON)
        self.assertEqual(data, loaded)

    def test_ddemod_fetch_set_parameters(self):
        data = self.sa.Sense.DDEMod.Fetch.fetch(self.metrics)
        self.sa.Sense.DDEMod.Fetch.set_fetch(data)
        self.assertEqual(self.sa.Sense.DDEMod.Fetch.get_fetch(), data)

    # 6. LTE Fetch fetch
    def test_lte_fetch_returns_dict(self):
        result = self.sa.Sense.LTE.Fetch.fetch(self.metrics)
        self.assertIsInstance(result, dict)

    def test_lte_fetch_write_and_read_file(self):
        data = self.sa.Sense.LTE.Fetch.fetch(self.metrics)
        self.dh.write_to_file("test_lte_fetch", data, file_type=EFileType.JSON)
        loaded = self.dh.read_file("test_lte_fetch", EFileType.JSON)
        self.assertEqual(data, loaded)

    def test_lte_fetch_set_parameters(self):
        data = self.sa.Sense.LTE.Fetch.fetch(self.metrics)
        self.sa.Sense.LTE.Fetch.set_fetch(data)
        self.assertEqual(self.sa.Sense.LTE.Fetch.get_fetch(), data)

    # 7. NFIGure Fetch get_nfigure
    def test_nfigure_get_nfigure_returns_float(self):
        result = self.sa.Sense.NFIGure.Fetch.get_nfigure()
        self.assertIsInstance(result, float)

    def test_nfigure_get_nfigure_write_and_read_file(self):
        data = self.sa.Sense.NFIGure.Fetch.get_nfigure()
        self.dh.write_to_file("test_nfigure", [data], file_type=EFileType.CSV)
        loaded = self.dh.read_file("test_nfigure.csv", EFileType.CSV)
        self.assertEqual(float(loaded[1][0]), data)

    def test_nfigure_get_nfigure_set_parameters(self):
        data = self.sa.Sense.NFIGure.Fetch.get_nfigure()
        self.sa.Sense.NFIGure.Fetch.set_nfigure(data)
        self.assertEqual(self.sa.Sense.NFIGure.Fetch.get_nfigure(), data)

    # 8. NFIGure Fetch get_gain
    def test_nfigure_get_gain_returns_float(self):
        result = self.sa.Sense.NFIGure.Fetch.get_gain()
        self.assertIsInstance(result, float)

    def test_nfigure_get_gain_write_and_read_file(self):
        data = self.sa.Sense.NFIGure.Fetch.get_gain()
        self.dh.write_to_file("test_nfigure_gain", [data], file_type=EFileType.CSV)
        loaded = self.dh.read_file("test_nfigure_gain.csv", EFileType.CSV)
        self.assertEqual(float(loaded[1][0]), data)

    def test_nfigure_get_gain_set_parameters(self):
        data = self.sa.Sense.NFIGure.Fetch.get_gain()
        self.sa.Sense.NFIGure.Fetch.set_gain(data)
        self.assertEqual(self.sa.Sense.NFIGure.Fetch.get_gain(), data)

    # 9. Bluetooth Fetch fetch
    def test_bluetooth_fetch_returns_dict(self):
        result = self.sa.Sense.Bluetooth.Fetch.fetch(self.metrics)
        self.assertIsInstance(result, dict)

    def test_bluetooth_fetch_write_and_read_file(self):
        data = self.sa.Sense.Bluetooth.Fetch.fetch(self.metrics)
        self.dh.write_to_file("test_bluetooth_fetch", data, file_type=EFileType.JSON)
        loaded = self.dh.read_file("test_bluetooth_fetch", EFileType.JSON)
        self.assertEqual(data, loaded)

    def test_bluetooth_fetch_set_parameters(self):
        data = self.sa.Sense.Bluetooth.Fetch.fetch(self.metrics)
        self.sa.Sense.Bluetooth.Fetch.set_fetch(data)
        self.assertEqual(self.sa.Sense.Bluetooth.Fetch.get_fetch(), data)

    # 10. Calculate LimitLine get_data
    def test_limitline_get_data_returns_list(self):
        result = self.sa.Calculate.LimitLine.get_data()
        self.assertIsInstance(result, list)

    def test_limitline_get_data_write_and_read_file(self):
        data = self.sa.Calculate.LimitLine.get_data()
        self.dh.write_to_file("test_limitline", data, file_type=EFileType.JSON)
        loaded = self.dh.read_file("test_limitline", EFileType.JSON)
        self.assertEqual(data, loaded)

    def test_limitline_get_data_set_parameters(self):
        data = self.sa.Calculate.LimitLine.get_data()
        self.sa.Calculate.LimitLine.set_data(data)
        self.assertEqual(self.sa.Calculate.LimitLine.get_data(), data)

    # 11. Pathloss get_data
    def test_pathloss_get_data_returns_list(self):
        result = self.sa.Sense.Pathloss.get_data()
        self.assertIsInstance(result, list)

    def test_pathloss_get_data_write_and_read_file(self):
        data = self.sa.Sense.Pathloss.get_data()
        self.dh.write_to_file("test_pathloss", data, file_type=EFileType.JSON)
        loaded = self.dh.read_file("test_pathloss", EFileType.JSON)
        self.assertEqual(data, loaded)

    def test_pathloss_get_data_set_parameters(self):
        data = self.sa.Sense.Pathloss.get_data()
        self.sa.Sense.Pathloss.set_data(data)
        self.assertEqual(self.sa.Sense.Pathloss.get_data(), data)

    # 12. SEMask Offset get_offset_parameters
    def test_semask_offset_get_offset_parameters_returns_dict(self):
        result = self.sa.Sense.SEMask.Offset.get_offset_parameters()
        self.assertIsInstance(result, dict)

    def test_semask_offset_get_offset_parameters_write_and_read_file(self):
        data = self.sa.Sense.SEMask.Offset.get_offset_parameters()
        self.dh.write_to_file("test_semask_offset", data, file_type=EFileType.JSON)
        loaded = self.dh.read_file("test_semask_offset", EFileType.JSON)
        self.assertEqual(data, loaded)

    def test_semask_offset_get_offset_parameters_set_parameters(self):
        data = self.sa.Sense.SEMask.Offset.get_offset_parameters()
        self.sa.Sense.SEMask.Offset.set_offset_parameters(data)
        self.assertEqual(self.sa.Sense.SEMask.Offset.get_offset_parameters(), data)

    # 13. NFIGure Correction ENRTable get_data
    def test_nfigure_enrtable_get_data_returns_list(self):
        result = self.sa.Sense.NFIGure.Correction.ENRTable.get_data()
        self.assertIsInstance(result, list)

    def test_nfigure_enrtable_get_data_write_and_read_file(self):
        data = self.sa.Sense.NFIGure.Correction.ENRTable.get_data()
        self.dh.write_to_file("test_enrtable", data, file_type=EFileType.JSON)
        loaded = self.dh.read_file("test_enrtable", EFileType.JSON)
        self.assertEqual(data, loaded)

    def test_nfigure_enrtable_get_data_set_parameters(self):
        data = self.sa.Sense.NFIGure.Correction.ENRTable.get_data()
        self.sa.Sense.NFIGure.Correction.ENRTable.set_data(data)
        self.assertEqual(self.sa.Sense.NFIGure.Correction.ENRTable.get_data(), data)

if __name__ == "__main__":
    unittest.main()

class TestOscilloscopeData(unittest.Testcase):
    def setUp(self):
        nm = NetworkManager()
        inst = nm.connect_oscilloscope()
        
        return oscilloscope_rigol.Oscilloscope(inst)
        
        self.metrics = ["metric1", "metric2"]
    def test_system_parameters_byte_values_change_with_parms(self):
            osc = self.setup()
            osc.auto_save = False
            data1 = osc.get_system_parameters()
            #print("Initial Data "+str(data1))
            osc.set_acquistion_mode("NORMAL")
            osc.set_channel_units(1,"WATT")
        
            data2 = osc.get_system_parameters()
            #print("After Data "+str(data2))
            print(data1)
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
       
    """def test_system_parameters_file_write(self):
        osc = self.setup()
        osc.auto_save = True
        data1 = osc.get_system_parameters()

    def test_waveform(self):
        osc = self.setup()
        osc.auto_save = False
        #data = osc.get_waveform_data()
        #print(data)"""
    #get_waveform_data
    #get_display_data
    #get_event_table_data
    #get_system_setup
    #set_system_setup
