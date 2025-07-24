import unittest
import pyvisa
from network_manager import NetworkManager
from Instruments import oscilloscope_rigol
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


    """def test_system_parameters_byte_values_change_with_parms(self):
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
test.test_system_parameters_file_write()"""