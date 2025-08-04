import unittest
from Instruments import spectrum_analyzer_signal_hound

class TestSpectrumAnalyzer(unittest.TestCase):
    
    def setup(self):
        #TODO insert connection
        self.sa = spectrum_analyzer_signal_hound.SpectrumAnalyzer(None)
    # --- Display Tests ---
    """def test_is_spike_hidden(self):
        self.mock_instrument.query.return_value = '1'
        self.assertTrue(self.sa.is_spike_hidden())
        self.mock_instrument.query.assert_called_with(":DISP:HIDE?")

        self.mock_instrument.query.return_value = '0'
        self.assertFalse(self.sa.is_spike_hidden())

        self.mock_instrument.query.return_value = 'INVALID'
        self.assertIsNone(self.sa.is_spike_hidden())
        self.assertIn("Invalid response received: INVALID", self.mock_stdout.getvalue())

    def test_hide_spike(self):
        self.sa.hide_spike('ON')
        self.mock_instrument.write.assert_called_with(":DISP:HIDE ON")
        self.sa.hide_spike(0)
        self.mock_instrument.write.assert_called_with(":DISP:HIDE OFF")

        self.sa.hide_spike('INVALID')
        self.assertIn("Invalid format. Allowed values are: ['ON', 'OFF', 1, 0]", self.mock_stdout.getvalue())

    def test_get_measurement_title(self):
        self.mock_instrument.query.return_value = "My Title"
        self.assertEqual(self.sa.get_measurement_title(), "My Title")
        self.mock_instrument.query.assert_called_with(":DISP:ANN:TITL?")

    def test_set_measurement_title(self):
        self.sa.set_measurement_title("New Title")
        self.mock_instrument.write.assert_called_with(":DISP:ANN:TITL 'New Title'")

        self.sa.set_measurement_title(123)
        self.assertIn("Invalid type. Title must be a string.", self.mock_stdout.getvalue())

    def test_clear_measurement_title(self):
        self.sa.clear_measurement_title()
        self.mock_instrument.write.assert_called_with(":DISP:ANN:CLE")

    # --- Format Trace Controls Tests ---
    def test_get_trace_format(self):
        self.mock_instrument.query.return_value = "ASC"
        self.assertEqual(self.sa.get_trace_format(), "ASC")
        self.mock_instrument.query.assert_called_with(":FORM:TRAC?")

    def test_set_trace_format(self):
        self.sa.set_trace_format("ASCII")
        self.mock_instrument.write.assert_called_with(":FORM:TRAC ASCII")
        self.sa.set_trace_format("REAL")
        self.mock_instrument.write.assert_called_with(":FORM:TRAC REAL")

        self.sa.set_trace_format("INVALID")
        self.assertIn("Invalid format. Allowed values are: ['ASCII', 'REAL', 'ASC']", self.mock_stdout.getvalue())

    def test_get_iq_format(self):
        self.mock_instrument.query.return_value = "BIN"
        self.assertEqual(self.sa.get_iq_format(), "BIN")
        self.mock_instrument.query.assert_called_with(":FORM:IQ?")

    def test_set_iq_format(self):
        self.sa.set_iq_format("BINARY")
        self.mock_instrument.write.assert_called_with(":FORM:IQ BINARY")
        self.sa.set_iq_format("ASC")
        self.mock_instrument.write.assert_called_with(":FORM:IQ ASC")

        self.sa.set_iq_format("INVALID")
        self.assertIn("Invalid format. Allowed values are: ['ASCII', 'BINARY', 'BIN', 'ASC']", self.mock_stdout.getvalue())

    # --- System Controls Tests ---
    def test_close_system(self):
        self.sa.close_system()
        self.mock_instrument.write.assert_called_with(":SYST:CLOS")
        self.assertIn("System close command sent. Socket connection terminated.", self.mock_stdout.getvalue())

    def test_preset_system(self):
        self.sa.preset_system()
        self.mock_instrument.write.assert_called_with(":SYST:PRES")

    def test_is_preset_successful(self):
        self.mock_instrument.query.return_value = '1'
        self.assertTrue(self.sa.is_preset_successful())
        self.mock_instrument.query.assert_called_with(":SYST:PRES?")

        self.mock_instrument.query.return_value = '0'
        self.assertFalse(self.sa.is_preset_successful())

        self.mock_instrument.query.return_value = 'ERROR'
        self.assertIsNone(self.sa.is_preset_successful())
        self.assertIn("Invalid response for preset status: ERROR", self.mock_stdout.getvalue())

    def test_save_image(self):
        self.sa.save_image("my_screenshot")
        self.mock_instrument.write.assert_called_with(":SYST:IMAG:SAVE 'my_screenshot.ini'")
        self.sa.save_image("another_image.ini")
        self.mock_instrument.write.assert_called_with(":SYST:IMAG:SAVE 'another_image.ini'")

    def test_save_image_quick(self):
        self.sa.save_image_quick()
        self.mock_instrument.write.assert_called_with(":SYST:IMAG:SAVE:QUIC")

    def test_load_user_preset(self):
        self.sa.load_user_preset("my_preset")
        self.mock_instrument.write.assert_called_with(":SYST:PRES:USER:LOAD 'my_preset.ini'")

    def test_save_user_preset(self):
        self.sa.save_user_preset("new_preset")
        self.mock_instrument.write.assert_called_with(":SYST:PRES:USER:SAVE 'new_preset.ini'")

    def test_communicate_gtlocal(self):
        self.sa.communicate_gtlocal()
        self.mock_instrument.write.assert_called_with(":SYST:COMM:GTL")

    def test_print_system(self):
        self.sa.print_system()
        self.mock_instrument.write.assert_called_with(":SYST:PRIN")

    def test_get_temperature(self):
        self.mock_instrument.query.return_value = "25.5"
        self.assertEqual(self.sa.get_temperature(), 25.5)
        self.mock_instrument.query.assert_called_with(":SYST:TEMP?")

        self.mock_instrument.query.return_value = "N/A"
        self.assertIsNone(self.sa.get_temperature())
        self.assertIn("Invalid response for temperature: N/A", self.mock_stdout.getvalue())

    def test_get_voltage(self):
        self.mock_instrument.query.return_value = "5.123"
        self.assertEqual(self.sa.get_voltage(), 5.123)
        self.mock_instrument.query.assert_called_with(":SYST:VOLT?")

        self.mock_instrument.query.return_value = "BAD"
        self.assertIsNone(self.sa.get_voltage())
        self.assertIn("Invalid response for voltage: BAD", self.mock_stdout.getvalue())

    def test_get_current(self):
        self.mock_instrument.query.return_value = "0.05"
        self.assertEqual(self.sa.get_current(), 0.05)
        self.mock_instrument.query.assert_called_with(":SYST:CURR?")

        self.mock_instrument.query.return_value = "ZERO"
        self.assertIsNone(self.sa.get_current())
        self.assertIn("Invalid response for current: ZERO", self.mock_stdout.getvalue())

    # --- Device Management Controls Tests ---
    def test_get_device_active_status(self):
        self.mock_instrument.query.return_value = '1'
        self.assertTrue(self.sa.get_device_active_status())
        self.mock_instrument.query.assert_called_with(":SYST:DEV:ACT?")

        self.mock_instrument.query.return_value = '0'
        self.assertFalse(self.sa.get_device_active_status())

        self.mock_instrument.query.return_value = 'FAIL'
        self.assertIsNone(self.sa.get_device_active_status())
        self.assertIn("Invalid response for device active status: FAIL", self.mock_stdout.getvalue())

    def test_get_device_count(self):
        self.mock_instrument.query.return_value = '3'
        self.assertEqual(self.sa.get_device_count(), 3)
        self.mock_instrument.query.assert_called_with(":SYST:DEV:COUN?")

        self.mock_instrument.query.return_value = 'NONE'
        self.assertIsNone(self.sa.get_device_count())
        self.assertIn("Invalid response for device count: NONE", self.mock_stdout.getvalue())

    def test_get_device_list(self):
        self.mock_instrument.query.return_value = "USB0::123,SOCKET::192.168.1.1::5025"
        expected_list = ["USB0::123", "SOCKET::192.168.1.1::5025"]
        self.assertEqual(self.sa.get_device_list(), expected_list)
        self.mock_instrument.query.assert_called_with(":SYST:DEV:LIST?")

    def test_get_current_device_connection_string(self):
        self.mock_instrument.query.return_value = "USB0::DEVICE_SN"
        self.assertEqual(self.sa.get_current_device_connection_string(), "USB0::DEVICE_SN")
        self.mock_instrument.query.assert_called_with(":SYST:DEV:CURR?")

    def test_connect_device(self):
        self.sa.connect_device("USB0::12345")
        self.mock_instrument.write.assert_called_with(":SYST:DEV:CON 'USB0::12345'")

    def test_disconnect_device(self):
        self.mock_instrument.query.return_value = '1'
        self.assertTrue(self.sa.disconnect_device())
        self.mock_instrument.query.assert_called_with(":SYST:DEV:DISC")

        self.mock_instrument.query.return_value = '0'
        self.assertFalse(self.sa.disconnect_device())

        self.mock_instrument.query.return_value = 'ERROR'
        self.assertIsNone(self.sa.disconnect_device())
        self.assertIn("Invalid response for disconnect status: ERROR", self.mock_stdout.getvalue())

    # --- Error Controls Tests ---
    def test_clear_all_errors(self):
        self.sa.clear_all_errors()
        self.mock_instrument.write.assert_called_with(":SYST:ERR:CLE")

    # --- Measurement Mode Controls Tests ---
    def test_set_mode(self):
        self.sa.set_mode("SA")
        self.mock_instrument.write.assert_called_with(":INST:SEL SA")
        self.sa.set_mode("RTSA")
        self.mock_instrument.write.assert_called_with(":INST:SEL RTSA")

        self.sa.set_mode("INVALID_MODE")
        self.assertIn("Invalid mode: 'INVALID_MODE'. Allowed modes are:", self.mock_stdout.getvalue())

    def test_get_mode(self):
        self.mock_instrument.query.return_value = "SA"
        self.assertEqual(self.sa.get_mode(), "SA")
        self.mock_instrument.query.assert_called_with(":INST:SEL?")

    def test_recalibrate_device(self):
        self.sa.recalibrate_device()
        self.mock_instrument.write.assert_called_with(":INST:REC")

    # --- Initiate Commands Tests ---
    def test_enable_continous_measurement(self):
        self.sa.enable_continous_measurement('ON')
        self.mock_instrument.write.assert_called_with(":INIT:CONT ON")
        self.sa.enable_continous_measurement(0)
        self.mock_instrument.write.assert_called_with(":INIT:CONT OFF")

    def test_is_continuous_measurement_enabled(self):
        self.mock_instrument.query.return_value = '1'
        self.assertTrue(self.sa.is_continuous_measurement_enabled())
        self.mock_instrument.query.assert_called_with(":INIT:CONT?")

        self.mock_instrument.query.return_value = '0'
        self.assertFalse(self.sa.is_continuous_measurement_enabled())

    def test_trigger_immediate_measurement(self):
        self.sa.trigger_immediate_measurement()
        self.mock_instrument.write.assert_called_with(":INIT:IMM")

    # --- Limit Lines Tests ---
    def test_enable_limit_line_testing(self):
        self.sa.enable_limit_line_testing(1, 'ON')
        self.mock_instrument.write.assert_called_with(":CALC:LLINE1:STAT ON")
        self.sa.enable_limit_line_testing(6, 0)
        self.mock_instrument.write.assert_called_with(":CALC:LLINE6:STAT OFF")

        with self.assertRaises(ValueError):
            self.sa.enable_limit_line_testing(0, 'ON')
        with self.assertRaises(ValueError):
            self.sa.enable_limit_line_testing(7, 'ON')

    def test_is_limit_line_testing_enabled(self):
        self.mock_instrument.query.return_value = '1'
        self.assertTrue(self.sa.is_limit_line_testing_enabled(1))
        self.mock_instrument.query.assert_called_with(":CALC:LLINE1:STAT?")

        self.mock_instrument.query.return_value = '0'
        self.assertFalse(self.sa.is_limit_line_testing_enabled(6))

        with self.assertRaises(ValueError):
            self.sa.is_limit_line_testing_enabled(0)

    def test_set_limit_line_state(self):
        self.sa.set_limit_line_state(1, 'ON')
        self.mock_instrument.write.assert_called_with(":CALC:LLINE1:STAT ON")
        self.sa.set_limit_line_state(2, 0)
        self.mock_instrument.write.assert_called_with(":CALC:LLINE2:STAT OFF")

        self.sa.set_limit_line_state(1, 'INVALID')
        self.assertIn("Invalid state: 'INVALID'. Allowed values are: ['ON', 'OFF', 1, 0]", self.mock_stdout.getvalue())

    def test_set_limit_line_title(self):
        self.sa.set_limit_line_title(1, "My Limit Line")
        self.mock_instrument.write.assert_called_with(":CALC:LLINE1:TITL 'My Limit Line'")

        with self.assertRaises(ValueError):
            self.sa.set_limit_line_title(0, "Title")

    def test_get_limit_line_title(self):
        self.mock_instrument.query.return_value = "Test Title"
        self.assertEqual(self.sa.get_limit_line_title(1), "Test Title")
        self.mock_instrument.query.assert_called_with(":CALC:LLINE1:TITL?")

    def test_set_limit_line_trace(self):
        self.sa.set_limit_line_trace(1, 1)
        self.mock_instrument.write.assert_called_with(":CALC:LLINE1:TRAC 1")

    def test_get_limit_lines_trace(self):
        self.mock_instrument.query.return_value = "2"
        self.assertEqual(self.sa.get_limit_lines_trace(1), "2")
        self.mock_instrument.query.assert_called_with(":CALC:LLINE1:TRAC?")

    def test_set_limit_line_type(self):
        self.sa.set_limit_line_type(1, "UPPer")
        self.mock_instrument.write.assert_called_with(":CALC:LLINE1:TYPE UPPER")
        self.sa.set_limit_line_type(2, "LOWer")
        self.mock_instrument.write.assert_called_with(":CALC:LLINE2:TYPE LOWER")

        self.sa.set_limit_line_type(1, "INVALID")
        self.assertIn("Invalid limit line type: 'INVALID'. Allowed values are 'UPPer' or 'LOWer'.", self.mock_stdout.getvalue())

    def test_get_limit_line_type(self):
        self.mock_instrument.query.return_value = "UPPER"
        self.assertEqual(self.sa.get_limit_line_type(1), "UPPER")
        self.mock_instrument.query.assert_called_with(":CALC:LLINE1:TYPE?")

    def test_set_limit_line_reference(self):
        self.sa.set_limit_line_reference(1, "FIXed")
        self.mock_instrument.write.assert_called_with(":CALC:LLINE1:REF FIXED")

        self.sa.set_limit_line_reference(1, "INVALID")
        self.assertIn("Invalid reference type: 'INVALID'. Allowed values are 'FIXed' or 'RELative'.", self.mock_stdout.getvalue())

    def test_get_limit_line_reference(self):
        self.mock_instrument.query.return_value = "FIXED"
        self.assertEqual(self.sa.get_limit_line_reference(1), "FIXED")
        self.mock_instrument.query.assert_called_with(":CALC:LLINE1:REF?")

    def test_transform_limit_line_reference(self):
        self.sa.transform_limit_line_reference(1)
        self.mock_instrument.write.assert_called_with(":CALC:LLINE1:REF:TRAN")

    def test_set_limit_line_interpolation(self):
        self.sa.set_limit_line_interpolation(1, "LINear")
        self.mock_instrument.write.assert_called_with(":CALC:LLINE1:INT LINEAR")

        self.sa.set_limit_line_interpolation(1, "INVALID")
        self.assertIn("Invalid interpolation type: 'INVALID'. Allowed values are 'LINear' or 'LOGarithmic'.", self.mock_stdout.getvalue())

    def test_get_limit_line_interpolation(self):
        self.mock_instrument.query.return_value = "LINEAR"
        self.assertEqual(self.sa.get_limit_line_interpolation(1), "LINEAR")
        self.mock_instrument.query.assert_called_with(":CALC:LLINE1:INT?")

    def test_set_limit_line_pause_state(self):
        self.sa.set_limit_line_pause_state(1, 'ON')
        self.mock_instrument.write.assert_called_with(":CALC:LLINE1:PAUS:STAT ON")

        self.sa.set_limit_line_pause_state(1, 'INVALID')
        self.assertIn("Invalid state: 'INVALID'. Allowed values are: ['ON', 'OFF', 1, 0]", self.mock_stdout.getvalue())

    def test_get_limit_line_pause_state(self):
        self.mock_instrument.query.return_value = '1'
        self.assertEqual(self.sa.get_limit_line_pause_state(1), '1')
        self.mock_instrument.query.assert_called_with(":CALC:LLINE1:PAUS:STAT?")

    def test_set_limit_line_display_visibility(self):
        self.sa.set_limit_line_display_visibility(1, 'ON')
        self.mock_instrument.write.assert_called_with(":CALC:LLINE1:DISP:STAT ON")

        self.sa.set_limit_line_display_visibility(1, 'INVALID')
        self.assertIn("Invalid state: 'INVALID'. Allowed values are: ['ON', 'OFF', 1, 0]", self.mock_stdout.getvalue())

    def test_is_limit_line_display_visible(self):
        self.mock_instrument.query.return_value = '1'
        self.assertTrue(self.sa.is_limit_line_display_visible(1))
        self.mock_instrument.query.assert_called_with(":CALC:LLINE1:DISP:STAT?")

    def test_change_limit_line_result_visibility(self):
        self.sa.change_limit_line_result_visibility(1, 'ON')
        self.mock_instrument.write.assert_called_with(":CALC:LLINE1:DISP:RES:STAT ON")

        self.sa.change_limit_line_result_visibility(1, 'INVALID')
        self.assertIn("Invalid state: 'INVALID'. Allowed values are: ['ON', 'OFF', 1, 0]", self.mock_stdout.getvalue())

    def test_is_limit_line_result_visible(self):
        self.mock_instrument.query.return_value = '1'
        self.assertTrue(self.sa.is_limit_line_result_visible(1))
        self.mock_instrument.query.assert_called_with(":CALC:LLINE1:DISP:RES:STAT?")

    def test_set_limit_line_offset_y(self):
        self.sa.set_limit_line_offset_y(1, 10.5)
        self.mock_instrument.write.assert_called_with(":CALC:LLINE1:OFFS:Y 10.5")

    def test_get_limit_line_offset_y(self):
        self.mock_instrument.query.return_value = "5.0"
        self.assertEqual(self.sa.get_limit_line_offset_y(1), "5.0")
        self.mock_instrument.query.assert_called_with(":CALC:LLINE1:OFFS:Y?")

    def test_build_limit_line(self):
        self.sa.build_limit_line(1)
        self.mock_instrument.write.assert_called_with(":CALC:LLINE1:BUIL")

    def test_get_limit_line_build_points(self):
        self.mock_instrument.query.return_value = "100"
        self.assertEqual(self.sa.get_limit_line_build_points(1), 100)
        self.mock_instrument.query.assert_called_with(":CALC:LLINE1:BUIL:POIN?")

        self.mock_instrument.query.return_value = "ABC"
        self.assertIsNone(self.sa.get_limit_line_build_points(1))
        self.assertIn("Invalid response for limit line build points: ABC", self.mock_stdout.getvalue())

    def test_save_limit_line_points(self):
        self.sa.save_limit_line_points(1)
        self.mock_instrument.write.assert_called_with(":CALC:LLINE1:SAVE")

    def test_get_limit_line_data(self):
        self.mock_instrument.query.return_value = "1000,0.1,2000,0.2"
        self.assertEqual(self.sa.get_limit_line_data(1), "1000,0.1,2000,0.2")
        self.mock_instrument.query.assert_called_with(":CALC:LLINE1:DATA?")

    def test_get_limit_line_fail_status(self):
        self.mock_instrument.query.return_value = '0' # 0 means passed in SCPI, which the original code maps to True
        self.assertTrue(self.sa.get_limit_line_fail_status(1))
        self.mock_instrument.query.assert_called_with(":CALC:LLINE1:FAIL?")

        self.mock_instrument.query.return_value = '1' # 1 means failed in SCPI, which the original code maps to False
        self.assertFalse(self.sa.get_limit_line_fail_status(1))

    def test_clear_all_limit_lines(self):
        self.sa.clear_all_limit_lines()
        self.mock_instrument.write.assert_called_with(":CALC:LLINE:ALL:CLE")

    # --- Path Loss Tables Tests ---
    def test_set_path_loss_table_state(self):
        self.sa.set_path_loss_table_state(1, 'ON')
        self.mock_instrument.write.assert_called_with(":SENS:CORR:PATH1:STAT ON")
        self.sa.set_path_loss_table_state(8, 0)
        self.mock_instrument.write.assert_called_with(":SENS:CORR:PATH8:STAT OFF")

        with self.assertRaises(ValueError):
            self.sa.set_path_loss_table_state(0, 'ON')
        with self.assertRaises(ValueError):
            self.sa.set_path_loss_table_state(9, 'ON')

        self.sa.set_path_loss_table_state(1, 'INVALID')
        self.assertIn("Invalid state: 'INVALID'. Allowed values are: ['ON', 'OFF', 1, 0]", self.mock_stdout.getvalue())

    def test_get_path_loss_table_state(self):
        self.mock_instrument.query.return_value = '1'
        self.assertTrue(self.sa.get_path_loss_table_state(1))
        self.mock_instrument.query.assert_called_with(":SENS:CORR:PATH1:STAT?")

        self.mock_instrument.query.return_value = '0'
        self.assertFalse(self.sa.get_path_loss_table_state(8))

    def test_set_path_loss_table_description(self):
        self.sa.set_path_loss_table_description(1, "My Path Loss Table")
        self.mock_instrument.write.assert_called_with(":SENS:CORR:PATH1:DESC 'My Path Loss Table'")

    def test_get_path_loss_table_description(self):
        self.mock_instrument.query.return_value = "Test Description"
        self.assertEqual(self.sa.get_path_loss_table_description(1), "Test Description")
        self.mock_instrument.query.assert_called_with(":SENS:CORR:PATH1:DESC?")

    def test_set_path_loss_table_points(self):
        self.sa.set_path_loss_table_points(1, "1000,0.5,2000,1.0")
        self.mock_instrument.write.assert_called_with(":SENS:CORR:PATH1:DATA 1000,0.5,2000,1.0")

    def test_get_path_loss_table_points_count(self):
        self.mock_instrument.query.return_value = "2"
        self.assertEqual(self.sa.get_path_loss_table_points_count(1), 2)
        self.mock_instrument.query.assert_called_with(":SENS:CORR:PATH1:POIN?")

        self.mock_instrument.query.return_value = "XYZ"
        self.assertIsNone(self.sa.get_path_loss_table_points_count(1))
        self.assertIn("Invalid response for path loss table points count: XYZ", self.mock_stdout.getvalue())

    def test_get_path_loss_table_data(self):
        self.mock_instrument.query.return_value = "1000,0.5,2000,1.0"
        self.assertEqual(self.sa.get_path_loss_table_data(1), "1000,0.5,2000,1.0")
        self.mock_instrument.query.assert_called_with(":SENS:CORR:PATH1:DATA?")

    def test_clear_path_loss_table(self):
        self.sa.clear_path_loss_table(1)
        self.mock_instrument.write.assert_called_with(":SENS:CORR:PATH1:CLE")

    def test_clear_all_path_loss_tables(self):
        self.sa.clear_all_path_loss_tables()
        self.mock_instrument.write.assert_called_with(":SENS:CORR:PATH:ALL:CLE")"""
