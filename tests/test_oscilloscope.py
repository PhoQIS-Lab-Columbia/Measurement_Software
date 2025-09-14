import unittest
import sys
import io
sys.path.append('../Measurement_Software')
from Instruments import oscilloscope_rigol
import pyvisa

class TestRigolOscilloscope(unittest.TestCase):

    def setup(self):
        """Set up a mock instrument and RigolOscilloscope instance before each test."""
        rm = pyvisa.ResourceManager()
        insturment_list = [] #types the name of the instruments you want to query 

        #Add auto connection
        r = rm.open_resource('USB0::0x1AB1::0x0517::DS1ZE264M00036::INSTR')
        self.scope = oscilloscope_rigol.Oscilloscope(r)
        self.instrument = self.scope.instrument
        # Redirect stdout to capture print statements
        self.held_stdout = sys.stdout
        self.mock_stdout = io.StringIO()
        sys.stdout = self.mock_stdout
        

    def tearDown(self):
        """Restore stdout after each test."""
        sys.stdout = self.held_stdout
        
    # --- Common Commands Tests ---
    def test_get_identification(self):
        self.setup()
        id = "RIGOL TECHNOLOGIES,DS1202Z-E,DS1ZE264M00036,00.06.04"
        self.assertEqual(self.scope.get_id(), id)

    def test_reset_instrument(self):
        self.setup()
        self.scope.reset_instrument()
        #TODO: Do with command in the middle

    def test_clear_status_byte(self):
        self.setup()
        self.scope.clear_event_registers()
        #TODO: Do with command in the middle

    def test_operation_complete(self):
        self.setup()
        self.assertEqual(self.scope.is_operation_complete(), 1)
        

    def test_wait_for_completion(self):
        self.setup()
        self.scope.wait_for_operation_finish()
        #TODO: Add inbetween waits

    def test_self_test(self):
        self.setup()
        self.assertEqual(self.scope.self_test(), 0)

    # --- System Commands Tests ---
    """def test_get_lan_ip_address(self):
        self.instrument.query.return_value = "192.168.1.100"
        self.assertEqual(self.scope.get_lan_ip_address(), "192.168.1.100")
        self.instrument.query.assert_called_with(":SYST:COMM:LAN:IPAD?")

    def test_get_lan_subnet_mask(self):
        self.instrument.query.return_value = "255.255.255.0"
        self.assertEqual(self.scope.get_lan_subnet_mask(), "255.255.255.0")
        self.instrument.query.assert_called_with(":SYST:COMM:LAN:SMAS?")

    def test_get_lan_gateway(self):
        self.instrument.query.return_value = "192.168.1.1"
        self.assertEqual(self.scope.get_lan_gateway(), "192.168.1.1")
        self.instrument.query.assert_called_with(":SYST:COMM:LAN:GAT?")

    def test_get_lan_mac_address(self):
        self.instrument.query.return_value = "00:11:22:33:44:55"
        self.assertEqual(self.scope.get_lan_mac_address(), "00:11:22:33:44:55")
        self.instrument.query.assert_called_with(":SYST:COMM:LAN:MAC?")

    def test_set_lan_dhcp_state(self):
        self.scope.set_lan_dhcp_state('ON')
        self.instrument.write.assert_called_with(":SYST:COMM:LAN:DHCP ON")
        self.scope.set_lan_dhcp_state(0)
        self.instrument.write.assert_called_with(":SYST:COMM:LAN:DHCP OFF")
        self.scope.set_lan_dhcp_state('INVALID')
        self.assertIn("Invalid state: 'INVALID'. Allowed values are: ['ON', 'OFF', 1, 0]", self.mock_stdout.getvalue())

    def test_get_lan_dhcp_state(self):
        self.instrument.query.return_value = "ON"
        self.assertEqual(self.scope.get_lan_dhcp_state(), "ON")
        self.instrument.query.assert_called_with(":SYST:COMM:LAN:DHCP?")

    def test_set_lan_ip_address(self):
        self.scope.set_lan_ip_address("192.168.1.200")
        self.instrument.write.assert_called_with(":SYST:COMM:LAN:IPAD '192.168.1.200'")

    def test_set_lan_subnet_mask(self):
        self.scope.set_lan_subnet_mask("255.255.255.128")
        self.instrument.write.assert_called_with(":SYST:COMM:LAN:SMAS '255.255.255.128'")

    def test_set_lan_gateway(self):
        self.scope.set_lan_gateway("192.168.1.1")
        self.instrument.write.assert_called_with(":SYST:COMM:LAN:GAT '192.168.1.1'")

    def test_set_lan_dns(self):
        self.scope.set_lan_dns("8.8.4.4")
        self.instrument.write.assert_called_with(":SYST:COMM:LAN:DNS '8.8.4.4'")

    def test_get_lan_dns(self):
        self.instrument.query.return_value = "8.8.8.8"
        self.assertEqual(self.scope.get_lan_dns(), "8.8.8.8")
        self.instrument.query.assert_called_with(":SYST:COMM:LAN:DNS?")

    def test_set_lan_port(self):
        self.scope.set_lan_port(1234)
        self.instrument.write.assert_called_with(":SYST:COMM:LAN:PORT 1234")
        with self.assertRaises(ValueError):
            self.scope.set_lan_port(0)
        with self.assertRaises(ValueError):
            self.scope.set_lan_port(65536)

    def test_get_lan_port(self):
        self.instrument.query.return_value = "5555"
        self.assertEqual(self.scope.get_lan_port(), "5555")
        self.instrument.query.assert_called_with(":SYST:COMM:LAN:PORT?")

    def test_set_lan_remote_control_state(self):
        self.scope.set_lan_remote_control_state('ON')
        self.instrument.write.assert_called_with(":SYST:COMM:LAN:REM ON")
        self.scope.set_lan_remote_control_state('INVALID')
        self.assertIn("Invalid state: 'INVALID'. Allowed values are: ['ON', 'OFF', 1, 0]", self.mock_stdout.getvalue())

    def test_get_lan_remote_control_state(self):
        self.instrument.query.return_value = "ON"
        self.assertEqual(self.scope.get_lan_remote_control_state(), "ON")
        self.instrument.query.assert_called_with(":SYST:COMM:LAN:REM?")

    def test_get_scpi_version(self):
        self.instrument.query.return_value = "1999.0"
        self.assertEqual(self.scope.get_scpi_version(), "1999.0")
        self.instrument.query.assert_called_with(":SYST:VERS?")

    def test_set_date(self):
        self.scope.set_date(2025, 7, 10)
        self.instrument.write.assert_called_with(":SYST:DATE 2025,7,10")
        with self.assertRaises(ValueError):
            self.scope.set_date(2025, 13, 10)
        with self.assertRaises(ValueError):
            self.scope.set_date(2025, 7, 32)

    def test_get_date(self):
        self.instrument.query.return_value = "2025,7,10"
        self.assertEqual(self.scope.get_date(), "2025,7,10")
        self.instrument.query.assert_called_with(":SYST:DATE?")

    def test_set_time(self):
        self.scope.set_time(10, 30, 0)
        self.instrument.write.assert_called_with(":SYST:TIME 10,30,0")
        with self.assertRaises(ValueError):
            self.scope.set_time(25, 0, 0)
        with self.assertRaises(ValueError):
            self.scope.set_time(10, 60, 0)

    def test_get_time(self):
        self.instrument.query.return_value = "10,30,0"
        self.assertEqual(self.scope.get_time(), "10,30,0")
        self.instrument.query.assert_called_with(":SYST:TIME?")

    def test_set_beeper_state(self):
        self.scope.set_beeper_state('ON')
        self.instrument.write.assert_called_with(":SYST:BEEP:STAT ON")
        self.scope.set_beeper_state('INVALID')
        self.assertIn("Invalid state: 'INVALID'. Allowed values are: ['ON', 'OFF', 1, 0]", self.mock_stdout.getvalue())

    def test_get_beeper_state(self):
        self.instrument.query.return_value = "ON"
        self.assertEqual(self.scope.get_beeper_state(), "ON")
        self.instrument.query.assert_called_with(":SYST:BEEP:STAT?")

    def test_set_beeper_volume(self):
        self.scope.set_beeper_volume(75)
        self.instrument.write.assert_called_with(":SYST:BEEP:VOL 75")
        with self.assertRaises(ValueError):
            self.scope.set_beeper_volume(101)

    def test_get_beeper_volume(self):
        self.instrument.query.return_value = "50"
        self.assertEqual(self.scope.get_beeper_volume(), "50")
        self.instrument.query.assert_called_with(":SYST:BEEP:VOL?")

    def test_set_key_lock_state(self):
        self.scope.set_key_lock_state('ON')
        self.instrument.write.assert_called_with(":SYST:KLOC ON")
        self.scope.set_key_lock_state('INVALID')
        self.assertIn("Invalid state: 'INVALID'. Allowed values are: ['ON', 'OFF', 1, 0]", self.mock_stdout.getvalue())

    def test_get_key_lock_state(self):
        self.instrument.query.return_value = "OFF"
        self.assertEqual(self.scope.get_key_lock_state(), "OFF")
        self.instrument.query.assert_called_with(":SYST:KLOC?")

    def test_go_to_local(self):
        self.scope.go_to_local()
        self.instrument.write.assert_called_with(":SYST:GTL")

    def test_set_system_lock_state(self):
        self.scope.set_system_lock_state('ON')
        self.instrument.write.assert_called_with(":SYST:LOC ON")
        self.scope.set_system_lock_state('INVALID')
        self.assertIn("Invalid state: 'INVALID'. Allowed values are: ['ON', 'OFF', 1, 0]", self.mock_stdout.getvalue())

    def test_get_system_lock_state(self):
        self.instrument.query.return_value = "OFF"
        self.assertEqual(self.scope.get_system_lock_state(), "OFF")
        self.instrument.query.assert_called_with(":SYST:LOC?")

    def test_set_language(self):
        self.scope.set_language('ENGLish')
        self.instrument.write.assert_called_with(":SYST:LANG ENGLISH")
        self.scope.set_language('INVALID')
        self.assertIn("Invalid language: 'INVALID'. Allowed values are 'CHINese' or 'ENGLish'.", self.mock_stdout.getvalue())

    def test_get_language(self):
        self.instrument.query.return_value = "ENGL"
        self.assertEqual(self.scope.get_language(), "ENGL")
        self.instrument.query.assert_called_with(":SYST:LANG?")

    def test_update_system(self):
        self.scope.update_system()
        self.instrument.write.assert_called_with(":SYST:UPD")

    def test_get_model_information(self):
        self.instrument.query.return_value = "DS1054Z"
        self.assertEqual(self.scope.get_model_information(), "DS1054Z")
        self.instrument.query.assert_called_with(":SYST:INF:MOD?")

    def test_get_serial_number(self):
        self.instrument.query.return_value = "DS1ZA123456789"
        self.assertEqual(self.scope.get_serial_number(), "DS1ZA123456789")
        self.instrument.query.assert_called_with(":SYST:INF:SER?")

    def test_get_option_information(self):
        self.instrument.query.return_value = "NONE"
        self.assertEqual(self.scope.get_option_information(), "NONE")
        self.instrument.query.assert_called_with(":SYST:INF:OPT?")

    def test_get_firmware_version(self):
        self.instrument.query.return_value = "00.04.04.00.02"
        self.assertEqual(self.scope.get_firmware_version(), "00.04.04.00.02")
        self.instrument.query.assert_called_with(":SYST:INF:VER?")

    def test_get_all_information(self):
        self.instrument.query.return_value = "ALL_INFO_STRING"
        self.assertEqual(self.scope.get_all_information(), "ALL_INFO_STRING")
        self.instrument.query.assert_called_with(":SYST:INF:ALL?")

    # --- Display Commands Tests ---
    def test_set_display_type(self):
        self.scope.set_display_type('VECTor')
        self.instrument.write.assert_called_with(":DISP:TYPE VECTOR")
        self.scope.set_display_type('INVALID')
        self.assertIn("Invalid display type: 'INVALID'. Allowed values are 'VECTor' or 'DOTs'.", self.mock_stdout.getvalue())

    def test_get_display_type(self):
        self.instrument.query.return_value = "VECT"
        self.assertEqual(self.scope.get_display_type(), "VECT")
        self.instrument.query.assert_called_with(":DISP:TYPE?")

    def test_set_grid_type(self):
        self.scope.set_grid_type('FULL')
        self.instrument.write.assert_called_with(":DISP:GRID FULL")
        self.scope.set_grid_type('INVALID')
        self.assertIn("Invalid grid type: 'INVALID'. Allowed values are 'FULL', 'NONE', 'GRATicule', or 'RULEr'.", self.mock_stdout.getvalue())

    def test_get_grid_type(self):
        self.instrument.query.return_value = "FULL"
        self.assertEqual(self.scope.get_grid_type(), "FULL")
        self.instrument.query.assert_called_with(":DISP:GRID?")

    def test_set_persistence_state(self):
        self.scope.set_persistence_state('ON')
        self.instrument.write.assert_called_with(":DISP:PERS ON")
        self.scope.set_persistence_state('INVALID')
        self.assertIn("Invalid state: 'INVALID'. Allowed values are: ['ON', 'OFF', 1, 0]", self.mock_stdout.getvalue())

    def test_get_persistence_state(self):
        self.instrument.query.return_value = "OFF"
        self.assertEqual(self.scope.get_persistence_state(), "OFF")
        self.instrument.query.assert_called_with(":DISP:PERS?")

    def test_set_persistence_time(self):
        self.scope.set_persistence_time(5.0)
        self.instrument.write.assert_called_with(":DISP:PERS:TIME 5.0")
        self.scope.set_persistence_time(100.0) # Should print warning
        self.assertIn("Warning: Persistence time out of typical range (0-60s).", self.mock_stdout.getvalue())

    def test_get_persistence_time(self):
        self.instrument.query.return_value = "1.0"
        self.assertEqual(self.scope.get_persistence_time(), "1.0")
        self.instrument.query.assert_called_with(":DISP:PERS:TIME?")

    def test_set_display_brightness(self):
        self.scope.set_display_brightness(70)
        self.instrument.write.assert_called_with(":DISP:BRIG 70")
        with self.assertRaises(ValueError):
            self.scope.set_display_brightness(101)

    def test_get_display_brightness(self):
        self.instrument.query.return_value = "50"
        self.assertEqual(self.scope.get_display_brightness(), "50")
        self.instrument.query.assert_called_with(":DISP:BRIG?")

    def test_set_acquire_intensity(self):
        self.scope.set_acquire_intensity(60)
        self.instrument.write.assert_called_with(":DISP:INT:ACQ 60")
        with self.assertRaises(ValueError):
            self.scope.set_acquire_intensity(-1)

    def test_get_acquire_intensity(self):
        self.instrument.query.return_value = "50"
        self.assertEqual(self.scope.get_acquire_intensity(), "50")
        self.instrument.query.assert_called_with(":DISP:INT:ACQ?")

    def test_set_display_intensity(self):
        self.scope.set_display_intensity(80)
        self.instrument.write.assert_called_with(":DISP:INT:DISP 80")
        with self.assertRaises(ValueError):
            self.scope.set_display_intensity(101)

    def test_get_display_intensity(self):
        self.instrument.query.return_value = "50"
        self.assertEqual(self.scope.get_display_intensity(), "50")
        self.instrument.query.assert_called_with(":DISP:INT:DISP?")

    def test_clear_display(self):
        self.scope.clear_display()
        self.instrument.write.assert_called_with(":DISP:CLE")

    def test_set_color_grade_state(self):
        self.scope.set_color_grade_state('ON')
        self.instrument.write.assert_called_with(":DISP:CGR ON")
        self.scope.set_color_grade_state('INVALID')
        self.assertIn("Invalid state: 'INVALID'. Allowed values are: ['ON', 'OFF', 1, 0]", self.mock_stdout.getvalue())

    def test_get_color_grade_state(self):
        self.instrument.query.return_value = "OFF"
        self.assertEqual(self.scope.get_color_grade_state(), "OFF")
        self.instrument.query.assert_called_with(":DISP:CGR?")

    # --- Channel Commands Tests ---
    def test_set_channel_display_state(self):
        self.scope.set_channel_display_state(1, 'ON')
        self.instrument.write.assert_called_with(":CHAN1:DISP ON")
        with self.assertRaises(ValueError):
            self.scope.set_channel_display_state(5, 'ON')
        self.scope.set_channel_display_state(1, 'INVALID')
        self.assertIn("Invalid state: 'INVALID'. Allowed values are: ['ON', 'OFF', 1, 0]", self.mock_stdout.getvalue())

    def test_get_channel_display_state(self):
        self.instrument.query.return_value = "ON"
        self.assertEqual(self.scope.get_channel_display_state(1), "ON")
        self.instrument.query.assert_called_with(":CHAN1:DISP?")
        with self.assertRaises(ValueError):
            self.scope.get_channel_display_state(0)

    def test_set_channel_scale(self):
        self.scope.set_channel_scale(1, 0.05)
        self.instrument.write.assert_called_with(":CHAN1:SCAL 0.05")
        with self.assertRaises(ValueError):
            self.scope.set_channel_scale(5, 0.01)

    def test_get_channel_scale(self):
        self.instrument.query.return_value = "0.01"
        self.assertEqual(self.scope.get_channel_scale(1), "0.01")
        self.instrument.query.assert_called_with(":CHAN1:SCAL?")

    def test_set_channel_offset(self):
        self.scope.set_channel_offset(2, 0.1)
        self.instrument.write.assert_called_with(":CHAN2:OFFS 0.1")

    def test_get_channel_offset(self):
        self.instrument.query.return_value = "0.0"
        self.assertEqual(self.scope.get_channel_offset(1), "0.0")

    def test_set_channel_coupling(self):
        self.scope.set_channel_coupling(1, 'DC')
        self.instrument.write.assert_called_with(":CHAN1:COUP DC")
        self.scope.set_channel_coupling(1, 'INVALID')
        self.assertIn("Invalid coupling type: 'INVALID'. Allowed values are 'AC', 'DC', or 'GND'.", self.mock_stdout.getvalue())

    def test_get_channel_coupling(self):
        self.instrument.query.return_value = "DC"
        self.assertEqual(self.scope.get_channel_coupling(1), "DC")

    def test_set_channel_invert_state(self):
        self.scope.set_channel_invert_state(1, 'ON')
        self.instrument.write.assert_called_with(":CHAN1:INV ON")

    def test_get_channel_invert_state(self):
        self.instrument.query.return_value = "OFF"
        self.assertEqual(self.scope.get_channel_invert_state(1), "OFF")

    def test_set_channel_probe_ratio(self):
        self.scope.set_channel_probe_ratio(1, 10.0)
        self.instrument.write.assert_called_with(":CHAN1:PROB 10.0")

    def test_get_channel_probe_ratio(self):
        self.instrument.query.return_value = "1.0"
        self.assertEqual(self.scope.get_channel_probe_ratio(1), "1.0")

    def test_set_channel_bandwidth_limit_state(self):
        self.scope.set_channel_bandwidth_limit_state(1, 'ON')
        self.instrument.write.assert_called_with(":CHAN1:BWL ON")

    def test_get_channel_bandwidth_limit_state(self):
        self.instrument.query.return_value = "OFF"
        self.assertEqual(self.scope.get_channel_bandwidth_limit_state(1), "OFF")

    def test_set_channel_delay(self):
        self.scope.set_channel_delay(1, 1.0E-6)
        self.instrument.write.assert_called_with(":CHAN1:DEL 1e-06")

    def test_get_channel_delay(self):
        self.instrument.query.return_value = "0.0"
        self.assertEqual(self.scope.get_channel_delay(1), "0.0")

    def test_set_channel_units(self):
        self.scope.set_channel_units(1, 'VOLT')
        self.instrument.write.assert_called_with(":CHAN1:UNIT VOLT")
        self.scope.set_channel_units(1, 'INVALID')
        self.assertIn("Invalid unit type: 'INVALID'. Allowed values are:", self.mock_stdout.getvalue())

    def test_get_channel_units(self):
        self.instrument.query.return_value = "VOLT"
        self.assertEqual(self.scope.get_channel_units(1), "VOLT")

    def test_set_channel_vertical_position(self):
        self.scope.set_channel_vertical_position(1, 0.05)
        self.instrument.write.assert_called_with(":CHAN1:VERT:POS 0.05")

    def test_get_channel_vertical_position(self):
        self.instrument.query.return_value = "0.0"
        self.assertEqual(self.scope.get_channel_vertical_position(1), "0.0")

    def test_set_channel_label(self):
        self.scope.set_channel_label(1, "Input Signal")
        self.instrument.write.assert_called_with(":CHAN1:LAB 'Input Signal'")

    def test_get_channel_label(self):
        self.instrument.query.return_value = "CH1_Label"
        self.assertEqual(self.scope.get_channel_label(1), "CH1_Label")

    def test_set_channel_resistance(self):
        self.scope.set_channel_resistance(1, 'FIFTy')
        self.instrument.write.assert_called_with(":CHAN1:RES FIFTY")
        self.scope.set_channel_resistance(1, 'INVALID')
        self.assertIn("Invalid resistance type: 'INVALID'. Allowed values are 'FIFTy' or 'ONEMeg'.", self.mock_stdout.getvalue())

    def test_get_channel_resistance(self):
        self.instrument.query.return_value = "ONEM"
        self.assertEqual(self.scope.get_channel_resistance(1), "ONEM")

    # --- Timebase Commands Tests ---
    def test_set_timebase_mode(self):
        self.scope.set_timebase_mode('MAIN')
        self.instrument.write.assert_called_with(":TIM:MODE MAIN")
        self.scope.set_timebase_mode('INVALID')
        self.assertIn("Invalid timebase mode: 'INVALID'. Allowed values are 'MAIN', 'XY', or 'ROLL'.", self.mock_stdout.getvalue())

    def test_get_timebase_mode(self):
        self.instrument.query.return_value = "MAIN"
        self.assertEqual(self.scope.get_timebase_mode(), "MAIN")

    def test_set_timebase_scale(self):
        self.scope.set_timebase_scale(0.002)
        self.instrument.write.assert_called_with(":TIM:SCAL 0.002")

    def test_get_timebase_scale(self):
        self.instrument.query.return_value = "0.001"
        self.assertEqual(self.scope.get_timebase_scale(), "0.001")

    def test_set_timebase_offset(self):
        self.scope.set_timebase_offset(0.001)
        self.instrument.write.assert_called_with(":TIM:OFFS 0.001")

    def test_get_timebase_offset(self):
        self.instrument.query.return_value = "0.0"
        self.assertEqual(self.scope.get_timebase_offset(), "0.0")

    def test_set_timebase_delay_enable(self):
        self.scope.set_timebase_delay_enable('ON')
        self.instrument.write.assert_called_with(":TIM:DEL:ENAB ON")

    def test_get_timebase_delay_enable(self):
        self.instrument.query.return_value = "OFF"
        self.assertEqual(self.scope.get_timebase_delay_enable(), "OFF")

    def test_set_timebase_delay_scale(self):
        self.scope.set_timebase_delay_scale(0.0002)
        self.instrument.write.assert_called_with(":TIM:DEL:SCAL 0.0002")

    def test_get_timebase_delay_scale(self):
        self.instrument.query.return_value = "0.0001"
        self.assertEqual(self.scope.get_timebase_delay_scale(), "0.0001")

    def test_set_timebase_delay_offset(self):
        self.scope.set_timebase_delay_offset(0.0001)
        self.instrument.write.assert_called_with(":TIM:DEL:OFFS 0.0001")

    def test_get_timebase_delay_offset(self):
        self.instrument.query.return_value = "0.0"
        self.assertEqual(self.scope.get_timebase_delay_offset(), "0.0")

    # --- Trigger Commands Tests ---
    def test_set_trigger_mode(self):
        self.scope.set_trigger_mode('EDGE')
        self.instrument.write.assert_called_with(":TRIG:MODE EDGE")
        self.scope.set_trigger_mode('INVALID')
        self.assertIn("Invalid trigger mode: 'INVALID'. Allowed values are:", self.mock_stdout.getvalue())

    def test_get_trigger_mode(self):
        self.instrument.query.return_value = "EDGE"
        self.assertEqual(self.scope.get_trigger_mode(), "EDGE")

    def test_set_edge_trigger_source(self):
        self.scope.set_edge_trigger_source('CHAN1')
        self.instrument.write.assert_called_with(":TRIG:EDGE:SOUR CHAN1")
        self.scope.set_edge_trigger_source('INVALID')
        self.assertIn("Invalid edge trigger source: 'INVALID'. Allowed values are 'CHANnel<n>', 'ACLine', or 'EXTernal'.", self.mock_stdout.getvalue())

    def test_get_edge_trigger_source(self):
        self.instrument.query.return_value = "CHAN1"
        self.assertEqual(self.scope.get_edge_trigger_source(), "CHAN1")

    def test_set_edge_trigger_level(self):
        self.scope.set_edge_trigger_level(0.5)
        self.instrument.write.assert_called_with(":TRIG:EDGE:LEV 0.5")

    def test_get_edge_trigger_level(self):
        self.instrument.query.return_value = "0.0"
        self.assertEqual(self.scope.get_edge_trigger_level(), "0.0")

    def test_set_edge_trigger_slope(self):
        self.scope.set_edge_trigger_slope('POSitive')
        self.instrument.write.assert_called_with(":TRIG:EDGE:SLOP POSITIVE")
        self.scope.set_edge_trigger_slope('INVALID')
        self.assertIn("Invalid edge trigger slope: 'INVALID'. Allowed values are 'POSitive', 'NEGative', or 'EITHer'.", self.mock_stdout.getvalue())

    def test_get_edge_trigger_slope(self):
        self.instrument.query.return_value = "POS"
        self.assertEqual(self.scope.get_edge_trigger_slope(), "POS")

    def test_set_edge_trigger_coupling(self):
        self.scope.set_edge_trigger_coupling('DC')
        self.instrument.write.assert_called_with(":TRIG:EDGE:COUP DC")
        self.scope.set_edge_trigger_coupling('INVALID')
        self.assertIn("Invalid edge trigger coupling: 'INVALID'. Allowed values are 'AC', 'DC', 'LFReject', or 'HFReject'.", self.mock_stdout.getvalue())

    def test_get_edge_trigger_coupling(self):
        self.instrument.query.return_value = "DC"
        self.assertEqual(self.scope.get_edge_trigger_coupling(), "DC")

    def test_set_trigger_sweep_mode(self):
        self.scope.set_trigger_sweep_mode('AUTO')
        self.instrument.write.assert_called_with(":TRIG:SWE AUTO")
        self.scope.set_trigger_sweep_mode('INVALID')
        self.assertIn("Invalid trigger sweep mode: 'INVALID'. Allowed values are 'AUTO', 'NORMal', or 'SINGle'.", self.mock_stdout.getvalue())

    def test_get_trigger_sweep_mode(self):
        self.instrument.query.return_value = "AUTO"
        self.assertEqual(self.scope.get_trigger_sweep_mode(), "AUTO")

    def test_force_trigger(self):
        self.scope.force_trigger()
        self.instrument.write.assert_called_with(":TRIG:FORC")

    def test_get_trigger_status(self):
        self.instrument.query.return_value = "TD"
        self.assertEqual(self.scope.get_trigger_status(), "TD")

    def test_set_trigger_holdoff(self):
        self.scope.set_trigger_holdoff(1.0E-5)
        self.instrument.write.assert_called_with(":TRIG:HOLD 1e-05")

    def test_get_trigger_holdoff(self):
        self.instrument.query.return_value = "1.0E-6"
        self.assertEqual(self.scope.get_trigger_holdoff(), "1.0E-6")

    # --- Nth Edge Trigger Commands Tests ---
    def test_set_nth_edge_trigger_source(self):
        self.scope.set_nth_edge_trigger_source('CHAN1')
        self.instrument.write.assert_called_with(":TRIG:NTH:SOUR CHAN1")

    def test_get_nth_edge_trigger_source(self):
        self.instrument.query.return_value = "CHAN1"
        self.assertEqual(self.scope.get_nth_edge_trigger_source(), "CHAN1")

    def test_set_nth_edge_trigger_level(self):
        self.scope.set_nth_edge_trigger_level(0.2)
        self.instrument.write.assert_called_with(":TRIG:NTH:LEV 0.2")

    def test_get_nth_edge_trigger_level(self):
        self.instrument.query.return_value = "0.0"
        self.assertEqual(self.scope.get_nth_edge_trigger_level(), "0.0")

    def test_set_nth_edge_trigger_slope(self):
        self.scope.set_nth_edge_trigger_slope('NEG')
        self.instrument.write.assert_called_with(":TRIG:NTH:SLOP NEGATIVE")

    def test_get_nth_edge_trigger_slope(self):
        self.instrument.query.return_value = "POS"
        self.assertEqual(self.scope.get_nth_edge_trigger_slope(), "POS")

    def test_set_nth_edge_trigger_coupling(self):
        self.scope.set_nth_edge_trigger_coupling('AC')
        self.instrument.write.assert_called_with(":TRIG:NTH:COUP AC")

    def test_get_nth_edge_trigger_coupling(self):
        self.instrument.query.return_value = "DC"
        self.assertEqual(self.scope.get_nth_edge_trigger_coupling(), "DC")

    def test_set_nth_edge_count(self):
        self.scope.set_nth_edge_count(3)
        self.instrument.write.assert_called_with(":TRIG:NTH:N 3")
        with self.assertRaises(ValueError):
            self.scope.set_nth_edge_count(0)

    def test_get_nth_edge_count(self):
        self.instrument.query.return_value = "1"
        self.assertEqual(self.scope.get_nth_edge_count(), "1")

    # --- Pulse Trigger Commands Tests ---
    def test_set_pulse_trigger_source(self):
        self.scope.set_pulse_trigger_source('CHAN2')
        self.instrument.write.assert_called_with(":TRIG:PULS:SOUR CHAN2")

    def test_get_pulse_trigger_source(self):
        self.instrument.query.return_value = "CHAN1"
        self.assertEqual(self.scope.get_pulse_trigger_source(), "CHAN1")

    def test_set_pulse_trigger_level(self):
        self.scope.set_pulse_trigger_level(0.3)
        self.instrument.write.assert_called_with(":TRIG:PULS:LEV 0.3")

    def test_get_pulse_trigger_level(self):
        self.instrument.query.return_value = "0.0"
        self.assertEqual(self.scope.get_pulse_trigger_level(), "0.0")

    def test_set_pulse_width(self):
        self.scope.set_pulse_width(2.0E-6)
        self.instrument.write.assert_called_with(":TRIG:PULS:WIDT 2e-06")

    def test_get_pulse_width(self):
        self.instrument.query.return_value = "1.0E-6"
        self.assertEqual(self.scope.get_pulse_width(), "1.0E-6")

    def test_set_pulse_polarity(self):
        self.scope.set_pulse_polarity('NEG')
        self.instrument.write.assert_called_with(":TRIG:PULS:POL NEGATIVE")

    def test_get_pulse_polarity(self):
        self.instrument.query.return_value = "POS"
        self.assertEqual(self.scope.get_pulse_polarity(), "POS")

    def test_set_pulse_condition(self):
        self.scope.set_pulse_condition('GREaterthan')
        self.instrument.write.assert_called_with(":TRIG:PULS:COND GREATERTHAN")

    def test_get_pulse_condition(self):
        self.instrument.query.return_value = "GREA"
        self.assertEqual(self.scope.get_pulse_condition(), "GREA")

    def test_set_pulse_coupling(self):
        self.scope.set_pulse_coupling('HFReject')
        self.instrument.write.assert_called_with(":TRIG:PULS:COUP HFREJECT")

    def test_get_pulse_coupling(self):
        self.instrument.query.return_value = "DC"
        self.assertEqual(self.scope.get_pulse_coupling(), "DC")

    # --- Video Trigger Commands Tests ---
    def test_set_video_trigger_source(self):
        self.scope.set_video_trigger_source('EXT')
        self.instrument.write.assert_called_with(":TRIG:VID:SOUR EXT")

    def test_get_video_trigger_source(self):
        self.instrument.query.return_value = "CHAN1"
        self.assertEqual(self.scope.get_video_trigger_source(), "CHAN1")

    def test_set_video_trigger_level(self):
        self.scope.set_video_trigger_level(0.7)
        self.instrument.write.assert_called_with(":TRIG:VID:LEV 0.7")

    def test_get_video_trigger_level(self):
        self.instrument.query.return_value = "0.0"
        self.assertEqual(self.scope.get_video_trigger_level(), "0.0")

    def test_set_video_polarity(self):
        self.scope.set_video_polarity('INVerted')
        self.instrument.write.assert_called_with(":TRIG:VID:POL INVERTED")

    def test_get_video_polarity(self):
        self.instrument.query.return_value = "NORM"
        self.assertEqual(self.scope.get_video_polarity(), "NORM")

    def test_set_video_standard(self):
        self.scope.set_video_standard('PAL')
        self.instrument.write.assert_called_with(":TRIG:VID:STAN PAL")

    def test_get_video_standard(self):
        self.instrument.query.return_value = "NTSC"
        self.assertEqual(self.scope.get_video_standard(), "NTSC")

    def test_set_video_sync(self):
        self.scope.set_video_sync('ODDfield')
        self.instrument.write.assert_called_with(":TRIG:VID:SYNC ODDFIELD")

    def test_get_video_sync(self):
        self.instrument.query.return_value = "ALL"
        self.assertEqual(self.scope.get_video_sync(), "ALL")

    # --- Slope Trigger Commands Tests ---
    def test_set_slope_trigger_source(self):
        self.scope.set_slope_trigger_source('CHAN3')
        self.instrument.write.assert_called_with(":TRIG:SLOP:SOUR CHAN3")

    def test_get_slope_trigger_source(self):
        self.instrument.query.return_value = "CHAN1"
        self.assertEqual(self.scope.get_slope_trigger_source(), "CHAN1")

    def test_set_slope_trigger_level1(self):
        self.scope.set_slope_trigger_level1(0.1)
        self.instrument.write.assert_called_with(":TRIG:SLOP:LEV1 0.1")

    def test_get_slope_trigger_level1(self):
        self.instrument.query.return_value = "0.1"
        self.assertEqual(self.scope.get_slope_trigger_level1(), "0.1")

    def test_set_slope_trigger_level2(self):
        self.scope.set_slope_trigger_level2(-0.1)
        self.instrument.write.assert_called_with(":TRIG:SLOP:LEV2 -0.1")

    def test_get_slope_trigger_level2(self):
        self.instrument.query.return_value = "-0.1"
        self.assertEqual(self.scope.get_slope_trigger_level2(), "-0.1")

    def test_set_slope_trigger_time(self):
        self.scope.set_slope_trigger_time(1.0E-5)
        self.instrument.write.assert_called_with(":TRIG:SLOP:TIME 1e-05")

    def test_get_slope_trigger_time(self):
        self.instrument.query.return_value = "1.0E-6"
        self.assertEqual(self.scope.get_slope_trigger_time(), "1.0E-6")

    def test_set_slope_trigger_slope(self):
        self.scope.set_slope_trigger_slope('EITHer')
        self.instrument.write.assert_called_with(":TRIG:SLOP:SLOP EITHER")

    def test_get_slope_trigger_slope(self):
        self.instrument.query.return_value = "POS"
        self.assertEqual(self.scope.get_slope_trigger_slope(), "POS")

    def test_set_slope_trigger_condition(self):
        self.scope.set_slope_trigger_condition('INRange')
        self.instrument.write.assert_called_with(":TRIG:SLOP:COND INRANGE")

    def test_get_slope_trigger_condition(self):
        self.instrument.query.return_value = "GTR"
        self.assertEqual(self.scope.get_slope_trigger_condition(), "GTR")

    def test_set_slope_trigger_coupling(self):
        self.scope.set_slope_trigger_coupling('DC')
        self.instrument.write.assert_called_with(":TRIG:SLOP:COUP DC")

    def test_get_slope_trigger_coupling(self):
        self.instrument.query.return_value = "DC"
        self.assertEqual(self.scope.get_slope_trigger_coupling(), "DC")

    # --- Over Trigger Commands Tests ---
    def test_set_over_trigger_source(self):
        self.scope.set_over_trigger_source('CHAN4')
        self.instrument.write.assert_called_with(":TRIG:OVER:SOUR CHAN4")

    def test_get_over_trigger_source(self):
        self.instrument.query.return_value = "CHAN1"
        self.assertEqual(self.scope.get_over_trigger_source(), "CHAN1")

    def test_set_over_trigger_level1(self):
        self.scope.set_over_trigger_level1(0.2)
        self.instrument.write.assert_called_with(":TRIG:OVER:LEV1 0.2")

    def test_get_over_trigger_level1(self):
        self.instrument.query.return_value = "0.1"
        self.assertEqual(self.scope.get_over_trigger_level1(), "0.1")

    def test_set_over_trigger_level2(self):
        self.scope.set_over_trigger_level2(-0.2)
        self.instrument.write.assert_called_with(":TRIG:OVER:LEV2 -0.2")

    def test_get_over_trigger_level2(self):
        self.instrument.query.return_value = "-0.1"
        self.assertEqual(self.scope.get_over_trigger_level2(), "-0.1")

    def test_set_over_trigger_condition(self):
        self.scope.set_over_trigger_condition('OUTRange')
        self.instrument.write.assert_called_with(":TRIG:OVER:COND OUTRANGE")

    def test_get_over_trigger_condition(self):
        self.instrument.query.return_value = "IN"
        self.assertEqual(self.scope.get_over_trigger_condition(), "IN")

    def test_set_over_trigger_coupling(self):
        self.scope.set_over_trigger_coupling('AC')
        self.instrument.write.assert_called_with(":TRIG:OVER:COUP AC")

    def test_get_over_trigger_coupling(self):
        self.instrument.query.return_value = "DC"
        self.assertEqual(self.scope.get_over_trigger_coupling(), "DC")

    # --- Window Trigger Commands Tests ---
    def test_set_window_trigger_source(self):
        self.scope.set_window_trigger_source('CHAN1')
        self.instrument.write.assert_called_with(":TRIG:WIND:SOUR CHAN1")

    def test_get_window_trigger_source(self):
        self.instrument.query.return_value = "CHAN1"
        self.assertEqual(self.scope.get_window_trigger_source(), "CHAN1")

    def test_set_window_trigger_level1(self):
        self.scope.set_window_trigger_level1(0.3)
        self.instrument.write.assert_called_with(":TRIG:WIND:LEV1 0.3")

    def test_get_window_trigger_level1(self):
        self.instrument.query.return_value = "0.1"
        self.assertEqual(self.scope.get_window_trigger_level1(), "0.1")

    def test_set_window_trigger_level2(self):
        self.scope.set_window_trigger_level2(-0.3)
        self.instrument.write.assert_called_with(":TRIG:WIND:LEV2 -0.3")

    def test_get_window_trigger_level2(self):
        self.instrument.query.return_value = "-0.1"
        self.assertEqual(self.scope.get_window_trigger_level2(), "-0.1")

    def test_set_window_trigger_time(self):
        self.scope.set_window_trigger_time(3.0E-6)
        self.instrument.write.assert_called_with(":TRIG:WIND:TIME 3e-06")

    def test_get_window_trigger_time(self):
        self.instrument.query.return_value = "1.0E-6"
        self.assertEqual(self.scope.get_window_trigger_time(), "1.0E-6")

    def test_set_window_trigger_condition(self):
        self.scope.set_window_trigger_condition('LESThan')
        self.instrument.write.assert_called_with(":TRIG:WIND:COND LESSTHAN")

    def test_get_window_trigger_condition(self):
        self.instrument.query.return_value = "IN"
        self.assertEqual(self.scope.get_window_trigger_condition(), "IN")

    def test_set_window_trigger_coupling(self):
        self.scope.set_window_trigger_coupling('LFReject')
        self.instrument.write.assert_called_with(":TRIG:WIND:COUP LFREJECT")

    def test_get_window_trigger_coupling(self):
        self.instrument.query.return_value = "DC"
        self.assertEqual(self.scope.get_window_trigger_coupling(), "DC")

    # --- Timeout Trigger Commands Tests ---
    def test_set_timeout_trigger_source(self):
        self.scope.set_timeout_trigger_source('CHAN2')
        self.instrument.write.assert_called_with(":TRIG:TIM:SOUR CHAN2")

    def test_get_timeout_trigger_source(self):
        self.instrument.query.return_value = "CHAN1"
        self.assertEqual(self.scope.get_timeout_trigger_source(), "CHAN1")

    def test_set_timeout_trigger_time(self):
        self.scope.set_timeout_trigger_time(5.0E-6)
        self.instrument.write.assert_called_with(":TRIG:TIM:TIME 5e-06")

    def test_get_timeout_trigger_time(self):
        self.instrument.query.return_value = "1.0E-6"
        self.assertEqual(self.scope.get_timeout_trigger_time(), "1.0E-6")

    def test_set_timeout_polarity(self):
        self.scope.set_timeout_polarity('NEG')
        self.instrument.write.assert_called_with(":TRIG:TIM:POL NEGATIVE")

    def test_get_timeout_polarity(self):
        self.instrument.query.return_value = "POS"
        self.assertEqual(self.scope.get_timeout_polarity(), "POS")

    def test_set_timeout_condition(self):
        self.scope.set_timeout_condition('GREaterthan')
        self.instrument.write.assert_called_with(":TRIG:TIM:COND GREATERTHAN")

    def test_get_timeout_condition(self):
        self.instrument.query.return_value = "GTR"
        self.assertEqual(self.scope.get_timeout_condition(), "GTR")

    def test_set_timeout_coupling(self):
        self.scope.set_timeout_coupling('HFReject')
        self.instrument.write.assert_called_with(":TRIG:TIM:COUP HFREJECT")

    def test_get_timeout_coupling(self):
        self.instrument.query.return_value = "DC"
        self.assertEqual(self.scope.get_timeout_coupling(), "DC")

    # --- RS232 Trigger Commands Tests ---
    def test_set_rs232_trigger_source(self):
        self.scope.set_rs232_trigger_source(3)
        self.instrument.write.assert_called_with(":TRIG:RS232:SOUR CHAN3")

    def test_get_rs232_trigger_source(self):
        self.instrument.query.return_value = "CHAN1"
        self.assertEqual(self.scope.get_rs232_trigger_source(), "CHAN1")

    def test_set_rs232_baud_rate(self):
        self.scope.set_rs232_baud_rate(115200)
        self.instrument.write.assert_called_with(":TRIG:RS232:BAUD 115200")
        self.scope.set_rs232_baud_rate(100) # Should print warning
        self.assertIn("Warning: Baud rate 100 might not be supported.", self.mock_stdout.getvalue())

    def test_get_rs232_baud_rate(self):
        self.instrument.query.return_value = "9600"
        self.assertEqual(self.scope.get_rs232_baud_rate(), "9600")

    def test_set_rs232_parity(self):
        self.scope.set_rs232_parity('EVEN')
        self.instrument.write.assert_called_with(":TRIG:RS232:PAR EVEN")

    def test_get_rs232_parity(self):
        self.instrument.query.return_value = "NONE"
        self.assertEqual(self.scope.get_rs232_parity(), "NONE")

    def test_set_rs232_stop_bits(self):
        self.scope.set_rs232_stop_bits('TWO')
        self.instrument.write.assert_called_with(":TRIG:RS232:STOP TWO")

    def test_get_rs232_stop_bits(self):
        self.instrument.query.return_value = "ONE"
        self.assertEqual(self.scope.get_rs232_stop_bits(), "ONE")

    def test_set_rs232_data_bits(self):
        self.scope.set_rs232_data_bits(7)
        self.instrument.write.assert_called_with(":TRIG:RS232:DATA 7")
        with self.assertRaises(ValueError):
            self.scope.set_rs232_data_bits(4)

    def test_get_rs232_data_bits(self):
        self.instrument.query.return_value = "8"
        self.assertEqual(self.scope.get_rs232_data_bits(), "8")

    def test_set_rs232_polarity(self):
        self.scope.set_rs232_polarity('IDLELow')
        self.instrument.write.assert_called_with(":TRIG:RS232:POL IDLELOW")

    def test_get_rs232_polarity(self):
        self.instrument.query.return_value = "IDLEH"
        self.assertEqual(self.scope.get_rs232_polarity(), "IDLEH")

    def test_set_rs232_display_state(self):
        self.scope.set_rs232_display_state('OFF')
        self.instrument.write.assert_called_with(":TRIG:RS232:DISP OFF")

    def test_get_rs232_display_state(self):
        self.instrument.query.return_value = "ON"
        self.assertEqual(self.scope.get_rs232_display_state(), "ON")

    def test_set_rs232_packet_data(self):
        self.scope.set_rs232_packet_data("0xBB")
        self.instrument.write.assert_called_with(":TRIG:RS232:PACK:DATA '0xBB'")

    def test_get_rs232_packet_data(self):
        self.instrument.query.return_value = "0xAA"
        self.assertEqual(self.scope.get_rs232_packet_data(), "0xAA")

    def test_set_rs232_packet_length(self):
        self.scope.set_rs232_packet_length(2)
        self.instrument.write.assert_called_with(":TRIG:RS232:PACK:LENG 2")
        with self.assertRaises(ValueError):
            self.scope.set_rs232_packet_length(0)

    def test_get_rs232_packet_length(self):
        self.instrument.query.return_value = "1"
        self.assertEqual(self.scope.get_rs232_packet_length(), "1")

    def test_set_rs232_packet_offset(self):
        self.scope.set_rs232_packet_offset(1)
        self.instrument.write.assert_called_with(":TRIG:RS232:PACK:OFFS 1")
        with self.assertRaises(ValueError):
            self.scope.set_rs232_packet_offset(-1)

    def test_get_rs232_packet_offset(self):
        self.instrument.query.return_value = "0"
        self.assertEqual(self.scope.get_rs232_packet_offset(), "0")

    def test_set_rs232_packet_type(self):
        self.scope.set_rs232_packet_type('PARity')
        self.instrument.write.assert_called_with(":TRIG:RS232:PACK:TYPE PARITY")

    def test_get_rs232_packet_type(self):
        self.instrument.query.return_value = "DATA"
        self.assertEqual(self.scope.get_rs232_packet_type(), "DATA")

    def test_set_rs232_packet_condition(self):
        self.scope.set_rs232_packet_condition('NOTEqual')
        self.instrument.write.assert_called_with(":TRIG:RS232:PACK:COND NOTEQUAL")

    def test_get_rs232_packet_condition(self):
        self.instrument.query.return_value = "EQUAL"
        self.assertEqual(self.scope.get_rs232_packet_condition(), "EQUAL")

    # --- IIC Trigger Commands Tests ---
    def test_set_iic_trigger_source(self):
        self.scope.set_iic_trigger_source(1)
        self.instrument.write.assert_called_with(":TRIG:IIC:SOUR CHAN1")

    def test_get_iic_trigger_source(self):
        self.instrument.query.return_value = "CHAN1"
        self.assertEqual(self.scope.get_iic_trigger_source(), "CHAN1")

    def test_set_iic_scl_source(self):
        self.scope.set_iic_scl_source(2)
        self.instrument.write.assert_called_with(":TRIG:IIC:SCL CHAN2")

    def test_get_iic_scl_source(self):
        self.instrument.query.return_value = "CHAN2"
        self.assertEqual(self.scope.get_iic_scl_source(), "CHAN2")

    def test_set_iic_address(self):
        self.scope.set_iic_address(0x60)
        self.instrument.write.assert_called_with(":TRIG:IIC:ADDR 96") # 0x60 is 96 in decimal

    def test_get_iic_address(self):
        self.instrument.query.return_value = "0x50"
        self.assertEqual(self.scope.get_iic_address(), "0x50")

    def test_set_iic_rw_type(self):
        self.scope.set_iic_rw_type('READ')
        self.instrument.write.assert_called_with(":TRIG:IIC:RW READ")

    def test_get_iic_rw_type(self):
        self.instrument.query.return_value = "EITH"
        self.assertEqual(self.scope.get_iic_rw_type(), "EITH")

    def test_set_iic_packet_data(self):
        self.scope.set_iic_packet_data("0x02")
        self.instrument.write.assert_called_with(":TRIG:IIC:PACK:DATA '0x02'")

    def test_get_iic_packet_data(self):
        self.instrument.query.return_value = "0x01"
        self.assertEqual(self.scope.get_iic_packet_data(), "0x01")

    def test_set_iic_packet_length(self):
        self.scope.set_iic_packet_length(3)
        self.instrument.write.assert_called_with(":TRIG:IIC:PACK:LENG 3")

    def test_get_iic_packet_length(self):
        self.instrument.query.return_value = "1"
        self.assertEqual(self.scope.get_iic_packet_length(), "1")

    def test_set_iic_packet_offset(self):
        self.scope.set_iic_packet_offset(2)
        self.instrument.write.assert_called_with(":TRIG:IIC:PACK:OFFS 2")"""