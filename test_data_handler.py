import unittest
import pyvisa
from network_manager import NetworkManager
from Instruments import oscilloscope_rigol
from Instruments import spectrum_analyzer_signal_hound
from data_handler import DataHandler
from EFileType import EFileType
#TODO: Fix import path issues and dafult save path issues
#How to give access to computer file system
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
        self.sa = nm.connect_spectrum_analyzer()
        
    
        self.metrics = ["metric1", "metric2"]

    # 1. fetch_am
    def test_fetch_am_returns_dict(self):
        result = self.sa.sense.ADEMod.Fetch.fetch_am(self.metrics)
        self.assertIsInstance(result, dict)

    def test_fetch_am_write_and_read_file(self):
        data = self.sa.sense.ADEMod.Fetch.fetch_am(self.metrics)
        self.dh.write_to_file("test_fetch_am", data, file_type=EFileType.JSON)
        loaded = self.dh.read_file("test_fetch_am", EFileType.JSON)
        self.assertEqual(data, loaded)

    def test_fetch_am_set_parameters(self):
        data = self.sa.sense.ADEMod.Fetch.fetch_am(self.metrics)
        self.sa.sense.ADEMod.Fetch.set_am(data)
        # Assuming set_am sets internal state, check state or call get_am
        self.assertEqual(self.sa.sense.ADEMod.Fetch.get_am(), data)

    # 2. fetch_fm
    def test_fetch_fm_returns_dict(self):
        result = self.sa.sense.ADEMod.Fetch.fetch_fm(self.metrics)
        self.assertIsInstance(result, dict)

    def test_fetch_fm_write_and_read_file(self):
        data = self.sa.sense.ADEMod.Fetch.fetch_fm(self.metrics)
        self.dh.write_to_file("test_fetch_fm", data, file_type=EFileType.JSON)
        loaded = self.dh.read_file("test_fetch_fm", EFileType.JSON)
        self.assertEqual(data, loaded)

    def test_fetch_fm_set_parameters(self):
        data = self.sa.sense.ADEMod.Fetch.fetch_fm(self.metrics)
        self.sa.sense.ADEMod.Fetch.set_fm(data)
        self.assertEqual(self.sa.sense.ADEMod.Fetch.get_fm(), data)

    # 3. IQ get_data
    def test_iq_get_data_returns_list(self):
        result = self.sa.sense.DDEMod.Custom.IQ.get_data()
        self.assertIsInstance(result, list)

    def test_iq_get_data_write_and_read_file(self):
        data = self.sa.sense.DDEMod.Custom.IQ.get_data()
        self.dh.write_to_file("test_iq_data", data, file_type=EFileType.JSON)
        loaded = self.dh.read_file("test_iq_data", EFileType.JSON)
        self.assertEqual(data, loaded)

    def test_iq_get_data_set_parameters(self):
        data = self.sa.sense.DDEMod.Custom.IQ.get_data()
        self.sa.sense.DDEMod.Custom.IQ.set_data(data)
        self.assertEqual(self.sa.sense.DDEMod.Custom.IQ.get_data(), data)

    # 4. Trace Sweep get_data
    def test_trace_sweep_get_data_returns_list(self):
        result = self.sa.sense.DDEMod.Trace.Sweep.get_data()
        self.assertIsInstance(result, list)

    def test_trace_sweep_get_data_write_and_read_file(self):
        data = self.sa.sense.DDEMod.Trace.Sweep.get_data()
        self.dh.write_to_file("test_trace_sweep", data, file_type=EFileType.JSON)
        loaded = self.dh.read_file("test_trace_sweep", EFileType.JSON)
        self.assertEqual(data, loaded)

    def test_trace_sweep_get_data_set_parameters(self):
        data = self.sa.sense.DDEMod.Trace.Sweep.get_data()
        self.sa.sense.DDEMod.Trace.Sweep.set_data(data)
        self.assertEqual(self.sa.sense.DDEMod.Trace.Sweep.get_data(), data)

    # 5. DDEMod Fetch fetch
    def test_ddemod_fetch_returns_dict(self):
        result = self.sa.sense.DDEMod.Fetch.fetch(self.metrics)
        self.assertIsInstance(result, dict)

    def test_ddemod_fetch_write_and_read_file(self):
        data = self.sa.sense.DDEMod.Fetch.fetch(self.metrics)
        self.dh.write_to_file("test_ddemod_fetch", data, file_type=EFileType.JSON)
        loaded = self.dh.read_file("test_ddemod_fetch", EFileType.JSON)
        self.assertEqual(data, loaded)

    def test_ddemod_fetch_set_parameters(self):
        data = self.sa.sense.DDEMod.Fetch.fetch(self.metrics)
        self.sa.sense.DDEMod.Fetch.set_fetch(data)
        self.assertEqual(self.sa.sense.DDEMod.Fetch.get_fetch(), data)

    # 6. LTE Fetch fetch
    def test_lte_fetch_returns_dict(self):
        result = self.sa.sense.LTE.Fetch.fetch(self.metrics)
        self.assertIsInstance(result, dict)

    def test_lte_fetch_write_and_read_file(self):
        data = self.sa.sense.LTE.Fetch.fetch(self.metrics)
        self.dh.write_to_file("test_lte_fetch", data, file_type=EFileType.JSON)
        loaded = self.dh.read_file("test_lte_fetch", EFileType.JSON)
        self.assertEqual(data, loaded)

    def test_lte_fetch_set_parameters(self):
        data = self.sa.sense.LTE.Fetch.fetch(self.metrics)
        self.sa.sense.LTE.Fetch.set_fetch(data)
        self.assertEqual(self.sa.sense.LTE.Fetch.get_fetch(), data)

    # 7. nfigure Fetch get_nfigure
    def test_nfigure_get_nfigure_returns_float(self):
        result = self.sa.sense.nfigure.Fetch.get_nfigure()
        self.assertIsInstance(result, float)

    def test_nfigure_get_nfigure_write_and_read_file(self):
        data = self.sa.sense.nfigure.Fetch.get_nfigure()
        self.dh.write_to_file("test_nfigure", [data], file_type=EFileType.CSV)
        loaded = self.dh.read_file("test_nfigure.csv", EFileType.CSV)
        self.assertEqual(float(loaded[1][0]), data)

    def test_nfigure_get_nfigure_set_parameters(self):
        data = self.sa.sense.nfigure.Fetch.get_nfigure()
        self.sa.sense.nfigure.Fetch.set_nfigure(data)
        self.assertEqual(self.sa.sense.nfigure.Fetch.get_nfigure(), data)

    # 8. nfigure Fetch get_gain
    def test_nfigure_get_gain_returns_float(self):
        result = self.sa.sense.nfigure.Fetch.get_gain()
        self.assertIsInstance(result, float)

    def test_nfigure_get_gain_write_and_read_file(self):
        data = self.sa.sense.nfigure.Fetch.get_gain()
        self.dh.write_to_file("test_nfigure_gain", [data], file_type=EFileType.CSV)
        loaded = self.dh.read_file("test_nfigure_gain.csv", EFileType.CSV)
        self.assertEqual(float(loaded[1][0]), data)

    def test_nfigure_get_gain_set_parameters(self):
        data = self.sa.sense.nfigure.Fetch.get_gain()
        self.sa.sense.nfigure.Fetch.set_gain(data)
        self.assertEqual(self.sa.sense.nfigure.Fetch.get_gain(), data)

    # 9. Bluetooth Fetch fetch
    def test_bluetooth_fetch_returns_dict(self):
        result = self.sa.sense.Bluetooth.Fetch.fetch(self.metrics)
        self.assertIsInstance(result, dict)

    def test_bluetooth_fetch_write_and_read_file(self):
        data = self.sa.sense.Bluetooth.Fetch.fetch(self.metrics)
        self.dh.write_to_file("test_bluetooth_fetch", data, file_type=EFileType.JSON)
        loaded = self.dh.read_file("test_bluetooth_fetch", EFileType.JSON)
        self.assertEqual(data, loaded)

    def test_bluetooth_fetch_set_parameters(self):
        data = self.sa.sense.Bluetooth.Fetch.fetch(self.metrics)
        self.sa.sense.Bluetooth.Fetch.set_fetch(data)
        self.assertEqual(self.sa.sense.Bluetooth.Fetch.get_fetch(), data)

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
        result = self.sa.sense.Pathloss.get_data()
        self.assertIsInstance(result, list)

    def test_pathloss_get_data_write_and_read_file(self):
        data = self.sa.sense.Pathloss.get_data()
        self.dh.write_to_file("test_pathloss", data, file_type=EFileType.JSON)
        loaded = self.dh.read_file("test_pathloss", EFileType.JSON)
        self.assertEqual(data, loaded)

    def test_pathloss_get_data_set_parameters(self):
        data = self.sa.sense.Pathloss.get_data()
        self.sa.sense.Pathloss.set_data(data)
        self.assertEqual(self.sa.sense.Pathloss.get_data(), data)

    # 12. SEMask Offset get_offset_parameters
    def test_semask_offset_get_offset_parameters_returns_dict(self):
        result = self.sa.sense.SEMask.Offset.get_offset_parameters()
        self.assertIsInstance(result, dict)

    def test_semask_offset_get_offset_parameters_write_and_read_file(self):
        data = self.sa.sense.SEMask.Offset.get_offset_parameters()
        self.dh.write_to_file("test_semask_offset", data, file_type=EFileType.JSON)
        loaded = self.dh.read_file("test_semask_offset", EFileType.JSON)
        self.assertEqual(data, loaded)

    def test_semask_offset_get_offset_parameters_set_parameters(self):
        data = self.sa.sense.SEMask.Offset.get_offset_parameters()
        self.sa.sense.SEMask.Offset.set_offset_parameters(data)
        self.assertEqual(self.sa.sense.SEMask.Offset.get_offset_parameters(), data)

    # 13. nfigure correction enr_table get_data
    def test_nfigure_enr_table_get_data_returns_list(self):
        result = self.sa.sense.nfigure.correction.enr_table.get_data()
        self.assertIsInstance(result, list)

    def test_nfigure_enr_table_get_data_write_and_read_file(self):
        data = self.sa.sense.nfigure.correction.enr_table.get_data()
        self.dh.write_to_file("test_enr_table", data, file_type=EFileType.JSON)
        loaded = self.dh.read_file("test_enr_table", EFileType.JSON)
        self.assertEqual(data, loaded)

    def test_nfigure_enr_table_get_data_set_parameters(self):
        data = self.sa.sense.nfigure.correction.enr_table.get_data()
        self.sa.sense.nfigure.correction.enr_table.set_data(data)
        self.assertEqual(self.sa.sense.nfigure.correction.enr_table.get_data(), data)




class TestOscilloscopeData(unittest.TestCase):
    def osc_setup(self):
        nm = NetworkManager()
        return nm.connect_oscilloscope()
        
    def test_system_parameters_byte_values_change_with_parms(self):
            osc = self.osc_setup()
            #osc.auto_save = False
            data1 = osc.system.get_setup()
            print("Initial Data "+str(data1))
            #print("Check tmc header"+str(osc.instrument.query_binary_values(":SYST:SETup?", datatype='B', container=bytes)))
            osc.acquisition.set_mode("NORMAL")
            osc.channel1.set_units("WATT")
        
            data2 = osc.system.get_setup()
            #print("After Data "+str(data2))
            print(data1)
            self.assertNotEqual(data1, data2,"Bytes did not change even with parameter changes.")

    def test_load_parameters_(self):
        osc = self.osc_setup()
        #osc.auto_save = False
        
        #osc.enable_system_autoscale_key(True)
        osc.system.set_pon("LAT")
        osc.system.data_handler.enable_auto_saving_data()
        data1 = osc.system.get_setup()

        osc.system.set_pon("DEF")
        
        osc.system.set_setup(str(data1))
        #self.assertTrue(osc.is_system_autoscale_key_enabled())
        self.assertEqual(osc.system.get_pon(),"DEF")
       
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
