from Instruments import Instrument
import time
from EInstrument import EInstrument
class SpectrumAnalyzer(Instrument.Instrument):
    def __init__(self, device):
       #TODO Add in 
       self.instrument = device
       self.name = EInstrument.SPECTRUM_ANALYZER
       

    #Helper Functions
    def _validate_line_num(self, line_num):
        """Helper to validate if line_num is within the allowed range (1-6)."""
        if not 1 <= line_num <= 6:
            raise ValueError("Limit line number must be an integer between 1 and 6.")
    def _validate_pathloss_table_num(self, table_num):
        """Helper to validate if path loss table number is within the allowed range (1-8)."""
        if not 1 <= table_num <= 8:
            raise ValueError("Path loss table number must be an integer between 1 and 8.")
    #Display
    class Display:
        """
        The Display commands are used to control display-related settings.
        """
        def __init__(self, instrument):
            self.instrument = instrument

        def hide(self, state):
            """
            Parameter:
                state (int): 1 to hide, 0 to show.
            Return:
                None
            """
            if state not in [0, 1]:
                raise ValueError("state must be 0 or 1")
            self.instrument.write(f":DISP:HIDE {state}")

        def is_hidden(self):
            """
            Parameter:
                None
            Return:
                bool: True if display is hidden, False otherwise.
            """
            resp = self.instrument.query(":DISP:HIDE?")
            return resp.strip() == 1

        def set_title(self, title):
            """
            Parameter:
                title (str): The measurement title. Empty string to clear.
            Return:
                None
            """
            self.instrument.write(f':DISP:ANN:TITLE "{title}"')

        def get_title(self):
            """
            Parameter:
                None
            Return:
                str: The current measurement title.
            """
            return self.instrument.query(":DISP:ANN:TITLE?")

        def clear_title(self):
            """
            Parameter:
                None
            Return:
                None
            """
            self.instrument.write(":DISP:ANN:CLEAR")

    class Format:
        """
        The Format commands are used to set/query trace and IQ data formats.
        """
        def __init__(self, instrument):
            self.instrument = instrument

        def set_trace_data_format(self, fmt):
            """
            Parameter:
                fmt (str): 'ASCII' or 'REAL'
            Return:
                None
            """
            allowed = {"ASCII", "REAL"}
            if fmt.upper() not in allowed:
                raise ValueError("fmt must be 'ASCII' or 'REAL'")
            self.instrument.write(f":FORM:TRAC {fmt.upper()}")

        def get_trace_data_format(self):
            """
            Parameter:
                None
            Return:
                str: The current trace data format.
            """
            return self.instrument.query(":FORM:TRAC?")

        def set_iq_data_format(self, fmt):
            """
            Parameter:
                fmt (str): 'ASCII' or 'BIN'
            Return:
                None
            """
            allowed = {"ASCII", "BIN"}
            if fmt.upper() not in allowed:
                raise ValueError("fmt must be 'ASCII' or 'BIN'")
            self.instrument.write(f":FORM:IQ {fmt.upper()}")

        def get_iq_data_format(self):
            """
            Parameter:
                None
            Return:
                str: The current IQ data format.
            """
            return self.instrument.query(":FORM:IQ?")

    class System:
        """
        The System commands are used to perform system level software actions and query information about the system.
        """
        def __init__(self, instrument):
            self.instrument = instrument

        def close(self):
            """
            Parameter:
                None
            Return:
                None
            """
            self.instrument.write(":SYSTem:CLOSe")

        def preset(self):
            """
            Parameter:
                None
            Return:
                None
            """
            self.instrument.write(":SYSTem:PRESet")

        def is_preset(self):
            """
            Parameter:
                None
            Return:
                bool: True if system is preset, False otherwise.
            """
            resp = self.instrument.query(":SYSTem:PRESet?")
            return resp.strip() == 1
        def save_user_preset(self, filename):
            """
            Parameter:
            filename (str): The file name to save the preset. Should have extension ".ini".
            Return:
            None
            """
            if not filename.lower().endswith(".ini"):
                raise ValueError("filename must have extension '.ini'")
            self.instrument.write(f':SYSTem:PRESet:USER:SAVE "{filename}"')

        def load_user_preset(self, filename):
            """
            Parameter:
            filename (str): The file name to load the preset. Should have extension ".ini".
            Return:
            None
            """
            if not filename.lower().endswith(".ini"):
                raise ValueError("filename must have extension '.ini'")
            self.instrument.write(f':SYSTem:PRESet:USER:LOAD "{filename}"')

        def get_version(self):
            """
            Parameter:
            None
            Return:
            str: The Spike software version number.
            """
            return self.instrument.query(":SYSTem:VERsion?")

        def goto_local(self):
            """
            Parameter:
            None
            Return:
            None
            """
            self.instrument.write(":SYSTem:COMMunicate:GTLocal")

        def save_image(self, filename):
            """
            Parameter:
            filename (str): The file name to save the image.
            Return:
            None
            """
            self.instrument.write(f':SYSTem:IMAGe:SAVe "{filename}"')

        def quick_save_image(self):
            """
            Parameter:
            None
            Return:
            None
            """
            self.instrument.write(":SYSTem:IMAGe:SAVe:QUICk")

        def print_image(self):
            """
            Parameter:
            None
            Return:
            None
            """
            self.instrument.write(":SYSTem:PRINt")

        def get_temperature(self):
            """
            Parameter:
            None
            Return:
            float: The current internal temperature of the active device, in degrees Celsius.
            """
            return float(self.instrument.query(":SYSTem:TEMPerature?"))

        def get_voltage(self):
            """
            Parameter:
            None
            Return:
            float: The measured voltage of the active device, in volts.
            """
            return float(self.instrument.query(":SYSTem:VOLTage?"))

        def get_current(self):
            """
            Parameter:
            None
            Return:
            float: The measured current of the active device, in amps.
            """
            return float(self.instrument.query(":SYSTem:CURRent?"))

        class Device:
            """
            The Device commands allow you to remotely manage the active device in the Spike software.
            """
            def __init__(self, instrument):
                self.instrument = instrument

            def is_active(self):
                """
                Parameter:
                None
                Return:
                bool: True if a device is currently connected and active, False otherwise.
                """
                resp = self.instrument.query(":SYSTem:DEVice:ACTive?")
                return resp.strip() == 1

            def get_count(self):
                """
                Parameter:
                None
                Return:
                int: The number of devices connected to the PC.
                """
                return int(self.instrument.query(":SYSTem:DEVice:COUNt?"))

            def get_list(self):
                """
                Parameter:
                None
                Return:
                str: The list of connected devices.
                """
                return self.instrument.query(":SYSTem:DEVice:LIST?")

            def get_current(self):
                """
                Parameter:
                None
                Return:
                str: The currently active device.
                """
                return self.instrument.query(":SYSTem:DEVice:CURRent?")

            def connect(self, device_index):
                """
                Parameter:
                device_index (int): The index of the device to connect.
                Return:
                None
                """
                if not isinstance(device_index, int) or device_index < 0:
                    raise ValueError("device_index must be a non-negative integer")
                self.instrument.write(f":SYSTem:DEVice:CONnect? {device_index}")

            def disconnect(self):
                """
                Parameter:
                None
                Return:
                None
                """
                self.instrument.write(":SYSTem:DEVice:DISConnect?")
    class Error:
        """
        The Error commands allow you to query and clear system errors.
        """
        def __init__(self, instrument):
            self.instrument = instrument

        def get_count(self):
            """
            Parameter:
            None
            Return:
            int: The number of errors in the error queue.
            """
            return int(self.instrument.query(":SYSTem:ERRor:COUNt?"))

        def get_next(self):
            """
            Parameter:
            None
            Return:
            str: The next error in the queue, removing it from the queue.
            """
            return self.instrument.query(":SYSTem:ERRor:NEXT?")

        def clear(self):
            """
            Parameter:
            None
            Return:
            None
            """
            self.instrument.write(":SYSTem:ERRor:CLEar")

    class InstrumentMode:
        """
        The InstrumentMode commands control the measurement mode of the Spike software.
        """
        def __init__(self, instrument):
            self.instrument = instrument

        def select(self, mode):
            """
            Parameter:
            mode (str): One of 'SA', 'RTSA', 'ZS', 'HARMONICS', 'NA', 'PNOISE', 'DDEMOD', 'EMI', 'ADEMOD', 'IH', 'SEMASK', 'NFIGURE', 'WLAN', 'BLE', 'LTE'.
            Return:
            None
            """
            allowed = {
                "SA", "RTSA", "ZS", "HARMONICS", "NA", "PNOISE", "DDEMOD",
                "EMI", "ADEMOD", "IH", "SEMASK", "NFIGURE", "WLAN", "BLE", "LTE"
            }
            if mode.upper() not in allowed:
                raise ValueError("mode must be one of: " + ", ".join(allowed))
            self.instrument.write(f":INSTrument:SELect {mode.upper()}")

        def get_selected(self):
            """
            Parameter:
            None
            Return:
            str: The current measurement mode.
            """
            return self.instrument.query(":INSTrument:SELect?")

        def recalibrate(self):
            """
            Parameter:
            None
            Return:
            None
            """
            self.instrument.write(":INSTrument:RECALibrate")
    class Initiate:
        """
        The Initiate commands control when measurements are performed in the application.
        """
        def __init__(self, instrument):
            self.instrument = instrument

        def set_continuous(self, state):
            """
            Parameter:
            state (int or str): 1/0 or 'ON'/'OFF' to enable/disable continuous measurement.
            Return:
            None
            """
            if isinstance(state, str):
                state = state.upper()
                if state not in {"ON", "OFF"}:
                    raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
            elif state not in [0, 1]:
                raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
            self.instrument.write(f":INITiate:CONTinuous {state}")

        def is_continuous_enabled(self):
            """
            Parameter:
            None
            Return:
            bool: True if continuous measurement is enabled, False otherwise.
            """
            resp = self.instrument.query(":INITiate:CONTinuous?")
            return resp.strip() in {1, "ON"}

        def immediate(self):
            """
            Parameter:
            None
            Return:
            None
            """
            self.instrument.write(":INITiate:IMMediate")

    class Calculate:
        """
        The Calculate commands control the limit lines in measurement modes.
        """
        def __init__(self, instrument):
            self.instrument = instrument
        class Marker:
            """
            The Marker commands control the sweep markers.
            """
            def __init__(self, instrument):
                self.instrument = instrument

            def select(self, marker_num):
                """
                Parameter:
                marker_num (int): Marker index.
                Return:
                None
                """
                self.instrument.write(f":CALCulate:MARKer:SELect {marker_num}")

            def get_selected(self):
                """
                Parameter:
                None
                Return:
                int: The currently selected marker index.
                """
                return int(self.instrument.query(":CALCulate:MARKer:SELect?"))

            def set_state(self, state):
                """
                Parameter:
                state (int or str): 1/0 or 'ON'/'OFF' to enable/disable marker.
                Return:
                None
                """
                if isinstance(state, str):
                    state = state.upper()
                if state not in {"ON", "OFF"}:
                    raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                    state = 1 if state == "ON" else 0
                elif state not in [0, 1]:
                    raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                self.instrument.write(f":CALCulate:MARKer:STATe {state}")

            def is_enabled(self):
                """
                Parameter:
                None
                Return:
                bool: True if marker is enabled, False otherwise.
                """
                resp = self.instrument.query(":CALCulate:MARKer:STATe?")
                return int(resp.strip()) == 1

            def set_trace(self, trace_num):
                """
                Parameter:
                trace_num (int): Trace index to place marker on.
                Return:
                None
                """
                self.instrument.write(f":CALCulate:MARKer:TRACe {trace_num}")

            def get_trace(self):
                """
                Parameter:
                None
                Return:
                int: The trace index the marker is placed on.
                """
                return int(self.instrument.query(":CALCulate:MARKer:TRACe?"))

            def set_mode(self, mode):
                """
                Parameter:
                mode (str): 'POSITION', 'NOISE', 'CHPOWER', or 'NDB'.
                Return:
                None
                """
                allowed = {"POSITION", "NOISE", "CHPOWER", "NDB"}
                if not isinstance(mode, str) or mode.upper() not in allowed:
                    raise ValueError("mode must be one of 'POSITION', 'NOISE', 'CHPOWER', or 'NDB'")
                self.instrument.write(f":CALCulate:MARKer:MODE {mode.upper()}")

            def get_mode(self):
                """
                Parameter:
                None
                Return:
                str: The current marker mode.
                """
                return self.instrument.query(":CALCulate:MARKer:MODE?")

            def set_update(self, state):
                """
                Parameter:
                state (int or str): 1/0 or 'ON'/'OFF' to enable/disable marker update.
                Return:
                None
                """
                if isinstance(state, str):
                    state = state.upper()
                if state not in {"ON", "OFF"}:
                    raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                    state = 1 if state == "ON" else 0
                elif state not in [0, 1]:
                    raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                self.instrument.write(f":CALCulate:MARKer:UPDate {state}")

            def is_update_enabled(self):
                """
                Parameter:
                None
                Return:
                bool: True if marker update is enabled, False otherwise.
                """
                resp = self.instrument.query(":CALCulate:MARKer:UPDate?")
                return int(resp.strip()) == 1

            def set_delta(self, state):
                """
                Parameter:
                state (int or str): 1/0 or 'ON'/'OFF' to enable/disable delta mode.
                Return:
                None
                """
                if isinstance(state, str):
                    state = state.upper()
                if state not in {"ON", "OFF"}:
                    raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                    state = 1 if state == "ON" else 0
                elif state not in [0, 1]:
                    raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                self.instrument.write(f":CALCulate:MARKer:DELTa {state}")

            def is_delta_enabled(self):
                """
                Parameter:
                None
                Return:
                bool: True if delta mode is enabled, False otherwise.
                """
                resp = self.instrument.query(":CALCulate:MARKer:DELTa?")
                return int(resp.strip()) == 1

            def set_peak_track(self, state):
                """
                Parameter:
                state (int or str): 1/0 or 'ON'/'OFF' to enable/disable peak tracking.
                Return:
                None
                """
                if isinstance(state, str):
                    state = state.upper()
                if state not in {"ON", "OFF"}:
                    raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                    state = 1 if state == "ON" else 0
                elif state not in [0, 1]:
                    raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                self.instrument.write(f":CALCulate:MARKer:PKTRack {state}")

            def is_peak_track_enabled(self):
                """
                Parameter:
                None
                Return:
                bool: True if peak tracking is enabled, False otherwise.
                """
                resp = self.instrument.query(":CALCulate:MARKer:PKTRack?")
                return int(resp.strip()) == 1

            def set_x(self, freq):
                """
                Parameter:
                freq (float): Frequency to move marker to (Hz).
                Return:
                None
                """
                self.instrument.write(f":CALCulate:MARKer:X {freq}")

            def get_x(self):
                """
                Parameter:
                None
                Return:
                float: The marker position frequency (Hz).
                """
                return float(self.instrument.query(":CALCulate:MARKer:X?"))

            def get_y(self):
                """
                Parameter:
                None
                Return:
                float: The marker position amplitude.
                """
                return float(self.instrument.query(":CALCulate:MARKer:Y?"))

            def maximum(self):
                """
                Parameter:
                None
                Return:
                None
                """
                self.instrument.write(":CALCulate:MARKer:MAXimum")

            def maximum_next(self):
                """
                Parameter:
                None
                Return:
                None
                """
                self.instrument.write(":CALCulate:MARKer:MAXimum:NEXT")

            def maximum_left(self):
                """
                Parameter:
                None
                Return:
                None
                """
                self.instrument.write(":CALCulate:MARKer:MAXimum:LEFT")

            def maximum_right(self):
                """
                Parameter:
                None
                Return:
                None
                """
                self.instrument.write(":CALCulate:MARKer:MAXimum:RIGHt")

            def minimum(self):
                """
                Parameter:
                None
                Return:
                None
                """
                self.instrument.write(":CALCulate:MARKer:MINimum")

            def set_peak_excursion(self, value):
                """
                Parameter:
                value (float): Peak excursion in dB.
                Return:
                None
                """
                self.instrument.write(f":CALCulate:MARKer:PEAK:EXCursion {value}")

            def get_peak_excursion(self):
                """
                Parameter:
                None
                Return:
                float: The current peak excursion in dB.
                """
                return float(self.instrument.query(":CALCulate:MARKer:PEAK:EXCursion?"))

            def set_peak_threshold(self, value):
                """
                Parameter:
                value (float): Peak threshold in dBm.
                Return:
                None
                """
                self.instrument.write(f":CALCulate:MARKer:PEAK:THReshold {value}")

            def get_peak_threshold(self):
                """
                Parameter:
                None
                Return:
                float: The current peak threshold in dBm.
                """
                return float(self.instrument.query(":CALCulate:MARKer:PEAK:THReshold?"))

            def set_chpower_width(self, freq):
                """
                Parameter:
                freq (float): Channel power marker width (Hz).
                Return:
                None
                """
                self.instrument.write(f":CALCulate:MARKer:CHPower:WIDth {freq}")

            def get_chpower_width(self):
                """
                Parameter:
                None
                Return:
                float: The channel power marker width (Hz).
                """
                return float(self.instrument.query(":CALCulate:MARKer:CHPower:WIDth?"))

            def set_ndb_offset(self, value):
                """
                Parameter:
                value (float): N dB marker offset (dB).
                Return:
                None
                """
                self.instrument.write(f":CALCulate:MARKer:NDB:OFFset {value}")

            def get_ndb_offset(self):
                """
                Parameter:
                None
                Return:
                float: The N dB marker offset (dB).
                """
                return float(self.instrument.query(":CALCulate:MARKer:NDB:OFFset?"))

            def get_ndb_bandwidth(self):
                """
                Parameter:
                None
                Return:
                float: The width of the N dB band (Hz).
                """
                return float(self.instrument.query(":CALCulate:MARKer:NDB:BANDwidth?"))

            def get_ndb_rleft(self):
                """
                Parameter:
                None
                Return:
                float: The left edge frequency of the N dB band (Hz).
                """
                return float(self.instrument.query(":CALCulate:MARKer:NDB:RLEFt?"))

            def get_ndb_rright(self):
                """
                Parameter:
                None
                Return:
                float: The right edge frequency of the N dB band (Hz).
                """
                return float(self.instrument.query(":CALCulate:MARKer:NDB:RRIGht?"))

            def set_center(self):
                """
                Parameter:
                None
                Return:
                None
                """
                self.instrument.write(":CALCulate:MARKer:SET:CENTer")

            def set_rlevel(self):
                """
                Parameter:
                None
                Return:
                None
                """
                self.instrument.write(":CALCulate:MARKer:SET:RLEVel")

            def disable_all(self):
                """
                Parameter:
                None
                Return:
                None
                """
                self.instrument.write(":CALCulate:MARKer:AOFF")

        class Math:
            """
            The CalculateMath commands control trace math functions.
            """
        def __init__(self, instrument):
            self.instrument = instrument

        def set_state(self, state):
            """
            Parameter:
            state (int or str): 1/0 or 'ON'/'OFF' to enable/disable trace math.
            Return:
            None
            """
            if isinstance(state, str):
                state = state.upper()
            if state not in {"ON", "OFF"}:
                raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                state = 1 if state == "ON" else 0
            elif state not in [0, 1]:
                raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
            self.instrument.write(f":CALCulate:MATH:STATe {state}")

        def is_enabled(self):
            """
            Parameter:
            None
            Return:
            bool: True if trace math is enabled, False otherwise.
            """
            resp = self.instrument.query(":CALCulate:MATH:STATe?")
            return int(resp.strip()) == 1

        def set_first(self, trace_num):
            """
            Parameter:
            trace_num (int): First operand trace [1,6].
            Return:
            None
            """
            if not isinstance(trace_num, int) or not (1 <= trace_num <= 6):
                raise ValueError("trace_num must be an integer between 1 and 6")
            self.instrument.write(f":CALCulate:MATH:FIRST {trace_num}")

        def get_first(self):
            """
            Parameter:
            None
            Return:
            int: The first operand trace.
            """
            return int(self.instrument.query(":CALCulate:MATH:FIRST?"))

        def set_second(self, trace_num):
            """
            Parameter:
            trace_num (int): Second operand trace [1,6].
            Return:
            None
            """
            if not isinstance(trace_num, int) or not (1 <= trace_num <= 6):
                raise ValueError("trace_num must be an integer between 1 and 6")
            self.instrument.write(f":CALCulate:MATH:SECond {trace_num}")

        def get_second(self):
            """
            Parameter:
            None
            Return:
            int: The second operand trace.
            """
            return int(self.instrument.query(":CALCulate:MATH:SECond?"))

        def set_result(self, trace_num):
            """
            Parameter:
            trace_num (int): Result trace [1,6].
            Return:
            None
            """
            if not isinstance(trace_num, int) or not (1 <= trace_num <= 6):
                raise ValueError("trace_num must be an integer between 1 and 6")
            self.instrument.write(f":CALCulate:MATH:RESult {trace_num}")

        def get_result(self):
            """
            Parameter:
            None
            Return:
            int: The result trace.
            """
            return int(self.instrument.query(":CALCulate:MATH:RESult?"))

        def set_operation(self, op):
            """
            Parameter:
            op (str): 'PDIFF', 'PSUM', 'LOFFSET', or 'LDIFF'.
            Return:
            None
            """
            allowed = {"PDIFF", "PSUM", "LOFFSET", "LDIFF"}
            if not isinstance(op, str) or op.upper() not in allowed:
                raise ValueError("op must be one of 'PDIFF', 'PSUM', 'LOFFSET', or 'LDIFF'")
            self.instrument.write(f":CALCulate:MATH:OP {op.upper()}")

        def get_operation(self):
            """
            Parameter:
            None
            Return:
            str: The current trace math operation.
            """
            return self.instrument.query(":CALCulate:MATH:OP?")

        def set_offset(self, value):
            """
            Parameter:
            value (float): Offset for logarithm trace math functions.
            Return:
            None
            """
            self.instrument.write(f":CALCulate:MATH:OFFSet {value}")

        def get_offset(self):
            """
            Parameter:
            None
            Return:
            float: The current offset for logarithm trace math functions.
            """
            return float(self.instrument.query(":CALCulate:MATH:OFFSet?"))
        class LimitLine:
            """
            LimitLine commands for a specific limit line number (1-6).
            """
            def __init__(self, instrument, line_num):
                self.instrument = instrument
                if not 1 <= line_num <= 6:
                    raise ValueError("Limit line number must be between 1 and 6.")
                self.line_num = line_num

            def set_state(self, state):
                """
                Parameter:
                state (int or str): 1/0 or 'ON'/'OFF' to enable/disable testing of this limit line.
                Return:
                None
                """
                if isinstance(state, str):
                    state = state.upper()
                    if state not in {"ON", "OFF"}:
                        raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                elif state not in [0, 1]:
                    raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                self.instrument.write(f":CALCulate:LLINe{self.line_num}:STATe {state}")

            def is_enabled(self):
                """
                Parameter:
                None
                Return:
                bool: True if limit line testing is enabled, False otherwise.
                """
                resp = self.instrument.query(f":CALCulate:LLINe{self.line_num}:STATe?")
                return resp.strip() in {1, "ON"}

            def set_title(self, title):
                """
                Parameter:
                title (str): The name of the limit line.
                Return:
                None
                """
                self.instrument.write(f':CALCulate:LLINe{self.line_num}:TITLe "{title}"')

            def get_title(self):
                """
                Parameter:
                None
                Return:
                str: The current name of the limit line.
                """
                return self.instrument.query(f":CALCulate:LLINe{self.line_num}:TITLe?")

            def set_trace(self, trace_num):
                """
                Parameter:
                trace_num (int): The trace number to test against this limit line.
                Return:
                None
                """
                if not isinstance(trace_num, int):
                    raise ValueError("trace_num must be an integer")
                self.instrument.write(f":CALCulate:LLINe{self.line_num}:TRACe {trace_num}")

            def get_trace(self):
                """
                Parameter:
                None
                Return:
                int: The trace number tested against this limit line.
                """
                return int(self.instrument.query(f":CALCulate:LLINe{self.line_num}:TRACe?"))

            def set_type(self, typ):
                """
                Parameter:
                typ (str): 'UPPER' or 'LOWER'
                Return:
                None
                """
                allowed = {"UPPER", "LOWER"}
                if typ.upper() not in allowed:
                    raise ValueError("typ must be 'UPPER' or 'LOWER'")
                self.instrument.write(f":CALCulate:LLINe{self.line_num}:TYPE {typ.upper()}")

            def get_type(self):
                """
                Parameter:
                None
                Return:
                str: The type of the limit line ('UPPER' or 'LOWER').
                """
                return self.instrument.query(f":CALCulate:LLINe{self.line_num}:TYPE?")

            def set_reference(self, ref):
                """
                Parameter:
                ref (str): 'FIXED' or 'RELATIVE'
                Return:
                None
                """
                allowed = {"FIXED", "RELATIVE"}
                if ref.upper() not in allowed:
                    raise ValueError("ref must be 'FIXED' or 'RELATIVE'")
                self.instrument.write(f":CALCulate:LLINe{self.line_num}:REFerence {ref.upper()}")

            def get_reference(self):
                """
                Parameter:
                None
                Return:
                str: The reference type of the limit line.
                """
                return self.instrument.query(f":CALCulate:LLINe{self.line_num}:REFerence?")

            def transform_reference(self):
                """
                Parameter:
                None
                Return:
                None
                """
                self.instrument.write(f":CALCulate:LLINe{self.line_num}:REFerence:TRANsform")

            def set_interpolate(self, interp):
                """
                Parameter:
                interp (str): 'LINEAR' or 'LOGARITHMIC'
                Return:
                None
                """
                allowed = {"LINEAR", "LOGARITHMIC"}
                if interp.upper() not in allowed:
                    raise ValueError("interp must be 'LINEAR' or 'LOGARITHMIC'")
                self.instrument.write(f":CALCulate:LLINe{self.line_num}:INTerpolate {interp.upper()}")

            def get_interpolate(self):
                """
                Parameter:
                None
                Return:
                str: The interpolation type of the limit line.
                """
                return self.instrument.query(f":CALCulate:LLINe{self.line_num}:INTerpolate?")

            def set_pause_state(self, state):
                """
                Parameter:
                state (int or str): 1/0 or 'ON'/'OFF' to enable/disable pause on failure.
                Return:
                None
                """
                if isinstance(state, str):
                    state = state.upper()
                    if state not in {"ON", "OFF"}:
                        raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                elif state not in [0, 1]:
                    raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                self.instrument.write(f":CALCulate:LLINe{self.line_num}:PAUSe:STATe {state}")

            def is_pause_enabled(self):
                """
                Parameter:
                None
                Return:
                bool: True if pause on failure is enabled, False otherwise.
                """
                resp = self.instrument.query(f":CALCulate:LLINe{self.line_num}:PAUSe:STATe?")
                return resp.strip() in {1, "ON"}

            def set_display_line(self, state):
                """
                Parameter:
                state (int or str): 1/0 or 'ON'/'OFF' to enable/disable line display.
                Return:
                None
                """
                if isinstance(state, str):
                    state = state.upper()
                    if state not in {"ON", "OFF"}:
                        raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                elif state not in [0, 1]:
                    raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                self.instrument.write(f":CALCulate:LLINe{self.line_num}:DISPlay:LINE:STATe {state}")

            def is_display_line_enabled(self):
                """
                Parameter:
                None
                Return:
                bool: True if line display is enabled, False otherwise.
                """
                resp = self.instrument.query(f":CALCulate:LLINe{self.line_num}:DISPlay:LINE:STATe?")
                return resp.strip() in {1, "ON"}

            def set_display_result(self, state):
                """
                Parameter:
                state (int or str): 1/0 or 'ON'/'OFF' to enable/disable result display.
                Return:
                None
                """
                if isinstance(state, str):
                    state = state.upper()
                    if state not in {"ON", "OFF"}:
                        raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                elif state not in [0, 1]:
                    raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                self.instrument.write(f":CALCulate:LLINe{self.line_num}:DISPlay:RESult:STATe {state}")

            def is_display_result_enabled(self):
                """
                Parameter:
                None
                Return:
                bool: True if result display is enabled, False otherwise.
                """
                resp = self.instrument.query(f":CALCulate:LLINe{self.line_num}:DISPlay:RESult:STATe?")
                return resp.strip() in {1, "ON"}

            def set_offset_y(self, offset):
                """
                Parameter:
                offset (float): dB offset to the limit line.
                Return:
                None
                """
                self.instrument.write(f":CALCulate:LLINe{self.line_num}:OFFSet:Y {offset}")

            def get_offset_y(self):
                """
                Parameter:
                None
                Return:
                float: The dB offset of the limit line.
                """
                return float(self.instrument.query(f":CALCulate:LLINe{self.line_num}:OFFSet:Y?"))

            def set_build_points(self, num_points):
                """
                Parameter:
                num_points (int): Number of points to use when building limit line from trace.
                Return:
                None
                """
                if not isinstance(num_points, int):
                    raise ValueError("num_points must be an integer")
                self.instrument.write(f":CALCulate:LLINe{self.line_num}:BUILD:POINts {num_points}")

            def get_build_points(self):
                """
                Parameter:
                None
                Return:
                int: Number of points used when building limit line from trace.
                """
                return int(self.instrument.query(f":CALCulate:LLINe{self.line_num}:BUILD:POINts?"))

            def build(self):
                """
                Parameter:
                None
                Return:
                None
                """
                self.instrument.write(f":CALCulate:LLINe{self.line_num}:BUILD")

            def get_points_count(self):
                """
                Parameter:
                None
                Return:
                int: Number of points in the limit line.
                """
                return int(self.instrument.query(f":CALCulate:LLINe{self.line_num}:POINts?"))

            def set_data(self, points):
                """
                Parameter:
                points (list of tuple): List of (freq, ampl) pairs.
                Return:
                None
                """
                if not isinstance(points, list) or not all(isinstance(p, tuple) and len(p) == 2 for p in points):
                    raise ValueError("points must be a list of (freq, ampl) tuples")
                data_str = ", ".join(f"{freq},{ampl}" for freq, ampl in points)
                self.instrument.write(f":CALCulate:LLINe{self.line_num}:DATA {data_str}")

            def get_data(self):
                """
                Parameter:
                None
                Return:
                str: The points in the limit line as freq/ampl pairs.
                """
                return self.instrument.query(f":CALCulate:LLINe{self.line_num}:DATA?")

            def is_failed(self):
                """
                Parameter:
                None
                Return:
                bool: True if the limit test has failed, False otherwise.
                """
                resp = self.instrument.query(f":CALCulate:LLINe{self.line_num}:FAIL?")
                return resp.strip() == 1

            def clear(self):
                """
                Parameter:
                None
                Return:
                None
                """
                self.instrument.write(f":CALCulate:LLINe{self.line_num}:CLEAr")

            def clear_all_limit_lines(self):
                """
                Parameter:
                None
                Return:
                None
                """
                self.instrument.write(":CALCulate:LLINe:ALL:CLEAr")
    def set_reference_oscillator_source(self, source):
        """
        Parameter:
            source (str): 'INTERNAL', 'EXTERNAL', or 'OUT'.
        Return:
            None
        """
        allowed = {"INTERNAL", "EXTERNAL", "OUT"}
        if not isinstance(source, str) or source.upper() not in allowed:
            raise ValueError("source must be one of 'INTERNAL', 'EXTERNAL', or 'OUT'")
        self.instrument.write(f":SENSe:ROSCillator:SOURce {source.upper()}")

    def get_reference_oscillator_source(self):
        """
        Parameter:
            None
        Return:
            str: The current reference oscillator source.
        """
        return self.instrument.query(":SENSe:ROSCillator:SOURce?")
    class Sense:
        def __init__(self, instrument):
            self.instrument = instrument
        class Sweep_Configuration:
                    """
        The Sweep Configuration commands control the sweep configuration in scalar network analysis mode.
        """
        def __init__(self, instrument):
            self.instrument = instrument

        def set_points(self, num_points):
            """
            Parameter:
                num_points (int): Suggested sweep size.
            Return:
                None
            """
            if not isinstance(num_points, int):
                raise ValueError("num_points must be an integer")
            self.instrument.write(f":SENSe:NA:SWEep:POINts {num_points}")

        def get_points(self):
            """
            Parameter:
                None
            Return:
                int: The suggested sweep size.
            """
            return int(self.instrument.query(":SENSe:NA:SWEep:POINts?"))

        def set_type(self, typ):
            """
            Parameter:
                typ (str): 'PASSive' or 'ACTive'.
            Return:
                None
            """
            allowed = {"PASSive", "ACTive"}
            if not isinstance(typ, str) or typ.upper() not in allowed:
                raise ValueError("typ must be 'PASSive' or 'ACTive'")
            self.instrument.write(f":SENSe:NA:SWEep:TYPE {typ.upper()}")

        def get_type(self):
            """
            Parameter:
                None
            Return:
                str: The sweep type.
            """
            return self.instrument.query(":SENSe:NA:SWEep:TYPE?")

        def set_hrange(self, state):
            """
            Parameter:
                state (int or str): 1/0 or 'ON'/'OFF' to enable/disable high range.
            Return:
                None
            """
            if isinstance(state, str):
                state = state.upper()
                if state not in {"ON", "OFF"}:
                    raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                state = 1 if state == "ON" else 0
            elif state not in [0, 1]:
                raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
            self.instrument.write(f":SENSe:NA:SWEep:HRANge {state}")

        def is_hrange_enabled(self):
            """
            Parameter:
                None
            Return:
                bool: True if high range is enabled, False otherwise.
            """
            resp = self.instrument.query(":SENSe:NA:SWEep:HRANge?")
            return int(resp.strip()) == 1
        class NA:
            """
            The Scalar Network and Analysis Mode commands
            """
            class View():
                """NAView commands control the view settings in scalar network analysis mode."""
                def __init__(self, instrument):
                    self.instrument = instrument

                def set_scale(self, scale):
                    """
                    Parameter:
                        scale (str): 'LOG' or 'VSWR'.
                    Return:
                        None
                    """
                    allowed = {"LOG", "VSWR"}
                    if not isinstance(scale, str) or scale.upper() not in allowed:
                        raise ValueError("scale must be 'LOG' or 'VSWR'")
                    self.instrument.write(f":SENSe:NA:VIEW:SCALe {scale.upper()}")

                def get_scale(self):
                    """
                    Parameter:
                        None
                    Return:
                        str: The plot scale.
                    """
                    return self.instrument.query(":SENSe:NA:VIEW:SCALe?")

                def set_rlevel(self, amplitude):
                    """
                    Parameter:
                        amplitude (float): Reference level in dBm (LOG) or SWR (VSWR).
                    Return:
                        None
                    """
                    self.instrument.write(f":SENSe:NA:VIEW:RLEVel {amplitude}")

                def get_rlevel(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: The reference level.
                    """
                    return float(self.instrument.query(":SENSe:NA:VIEW:RLEVel?"))

                def set_div(self, division):
                    """
                    Parameter:
                        division (float): Plot vertical scale as dB (LOG) or SWR (VSWR).
                    Return:
                        None
                    """
                    self.instrument.write(f":SENSe:NA:VIEW:DIV {division}")

                def get_div(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: The plot vertical scale.
                    """
                    return float(self.instrument.query(":SENSe:NA:VIEW:DIV?"))
            class Correction:
                """
                The NACorrection commands control the correction settings in scalar network analysis mode.
                """
                def __init__(self, instrument):
                    self.instrument = instrument

                def store_thru(self):
                    """
                    Parameter:
                        None
                    Return:
                        None
                    """
                    self.instrument.write(":SENSe:CORRection:NA:STORe:THRU")

                def store_thru_high(self):
                    """
                    Parameter:
                        None
                    Return:
                        None
                    """
                    self.instrument.write(":SENSe:CORRection:NA:STORe:THRU:HIGH")

                def is_thru_active(self):
                    """
                    Parameter:
                        None
                    Return:
                        bool: True if a calibration is active, False otherwise.
                    """
                    resp = self.instrument.query(":SENSe:CORRection:NA:STORe:THRU:ACTive?")
                    return resp.strip() == '1'
        
        class PNoise:
            """
            The PNoise commands control the phase noise measurement mode.
            """
            def __init__(self, instrument):
                self.instrument = instrument

            def set_peak_track(self, state):
                """
                Parameter:
                    state (int or str): 1/0 or 'ON'/'OFF' to enable/disable peak tracking.
                Return:
                    None
                """
                if isinstance(state, str):
                    state = state.upper()
                    if state not in {"ON", "OFF"}:
                        raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                    state = 1 if state == "ON" else 0
                elif state not in [0, 1]:
                    raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                self.instrument.write(f":SENSe:PNoise:PKTRack {state}")

            def is_peak_track_enabled(self):
                """
                Parameter:
                    None
                Return:
                    bool: True if peak tracking is enabled, False otherwise.
                """
                resp = self.instrument.query(":SENSe:PNoise:PKTRack?")
                return int(resp.strip()) == 1

            def set_type(self, typ):
                """
                Parameter:
                    typ (str): 'PN', 'PNPAM', or 'AM'.
                Return:
                    None
                """
                allowed = {"PN", "PNPAM", "AM"}
                if not isinstance(typ, str) or typ.upper() not in allowed:
                    raise ValueError("typ must be 'PN', 'PNPAM', or 'AM'")
                self.instrument.write(f":SENSe:PNoise:TYPE {typ.upper()}")

            def get_type(self):
                """
                Parameter:
                    None
                Return:
                    str: The measurement type.
                """
                return self.instrument.query(":SENSe:PNoise:TYPE?")
            class Carrier:
                """
                The Carrier commands control the carrier search settings in phase noise measurement mode.
                """
                def __init__(self, instrument):
                    self.instrument = instrument

                def set_search_state(self, state):
                    """
                    Parameter:
                        state (int or str): 1/0 or 'ON'/'OFF' to enable/disable signal search.
                    Return:
                        None
                    """
                    if isinstance(state, str):
                        state = state.upper()
                        if state not in {"ON", "OFF"}:
                            raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                        state = 1 if state == "ON" else 0
                    elif state not in [0, 1]:
                        raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                    self.instrument.write(f":SENSe:PNoise:CARRier:SEARch:STATe {state}")

                def is_search_enabled(self):
                    """
                    Parameter:
                        None
                    Return:
                        bool: True if signal search is enabled, False otherwise.
                    """
                    resp = self.instrument.query(":SENSe:PNoise:CARRier:SEARch:STATe?")
                    return int(resp.strip()) == 1

                def set_search_start(self, freq):
                    """
                    Parameter:
                        freq (float): Start frequency of the signal search range in Hz.
                    Return:
                        None
                    """
                    self.instrument.write(f":SENSe:PNoise:CARRier:SEARch:STARt {freq}")

                def get_search_start(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: The start frequency of the signal search range in Hz.
                    """
                    return float(self.instrument.query(":SENSe:PNoise:CARRier:SEARch:STARt?"))

                def set_search_stop(self, freq):
                    """
                    Parameter:
                        freq (float): Stop frequency of the signal search range in Hz.
                    Return:
                        None
                    """
                    self.instrument.write(f":SENSe:PNoise:CARRier:SEARch:STOP {freq}")

                def get_search_stop(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: The stop frequency of the signal search range in Hz.
                    """
                    return float(self.instrument.query(":SENSe:PNoise:CARRier:SEARch:STOP?"))

                def perform_search(self):
                    """
                    Parameter:
                        None
                    Return:
                        None
                    """
                    self.instrument.write(":SENSe:PNoise:CARRier:SEARch:PERForm")

                def set_threshold_minimum(self, amplitude):
                    """
                    Parameter:
                        amplitude (float): Minimum amplitude required for signal detection in dBm.
                    Return:
                        None
                    """
                    self.instrument.write(f":SENSe:PNoise:CARRier:THReshold:MINimum {amplitude}")

                def get_threshold_minimum(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: The minimum amplitude required for signal detection in dBm.
                    """
                    return float(self.instrument.query(":SENSe:PNoise:CARRier:THReshold:MINimum?"))

                def get_threshold_minimum(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: The minimum amplitude required for signal detection in dBm.
                    """
                    return float(self.instrument.query(":SENSe:PNoise:CARRier:THReshold:MINimum?"))

                def is_valid(self):
                    """
                    Parameter:
                        None
                    Return:
                        bool: True if a carrier was detected, False otherwise.
                    """
                    resp = self.instrument.query(":SENSe:PNoise:CARRier:VALid?")
                    return resp.strip() == '1'

                def get_frequency(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: The detected frequency of the carrier in Hz.
                    """
                    return float(self.instrument.query(":SENSe:PNoise:CARRier:FREQuency?"))

                def get_amplitude(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: The detected amplitude of the carrier as dBm.
                    """
                    return float(self.instrument.query(":SENSe:PNoise:CARRier:AMPLitude?"))
            class View:
                """
                The View commands control the plot view settings in phase noise measurement mode.
                """
                def __init__(self, instrument):
                    self.instrument = instrument

                def set_rlevel(self, amplitude):
                    """
                    Parameter:
                        amplitude (float): Plot reference level as dBc/Hz.
                    Return:
                        None
                    """
                    self.instrument.write(f":SENSe:PNoise:VIEW:RLEVel {amplitude}")

                def get_rlevel(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: The plot reference level as dBc/Hz.
                    """
                    return float(self.instrument.query(":SENSe:PNoise:VIEW:RLEVel?"))

                def set_pdivision(self, division):
                    """
                    Parameter:
                        division (float): Plot division height as a floating point value.
                    Return:
                        None
                    """
                    self.instrument.write(f":SENSe:PNoise:VIEW:PDIVision {division}")

                def get_pdivision(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: The plot division height as a floating point value.
                    """
                    return float(self.instrument.query(":SENSe:PNoise:VIEW:PDIVision?"))

                def set_pnumdivisions(self, num_divisions):
                    """
                    Parameter:
                        num_divisions (int): Number of divisions on the phase noise plot.
                    Return:
                        None
                    """
                    if not isinstance(num_divisions, int):
                        raise ValueError("num_divisions must be an integer")
                    self.instrument.write(f":SENSe:PNoise:VIEW:PNUMDIVisions {num_divisions}")

                def get_pnumdivisions(self):
                    """
                    Parameter:
                        None
                    Return:
                        int: The number of divisions on the phase noise plot.
                    """
                    return int(self.instrument.query(":SENSe:PNoise:VIEW:PNUMDIVisions?"))
            
            class Frequency:
                """
                The PNoiseFrequency commands control the frequency settings in phase noise measurement mode.
                """
                def __init__(self, instrument):
                    self.instrument = instrument

                def set_center(self, freq):
                    """
                    Parameter:
                        freq (float): Carrier search frequency window in Hz.
                    Return:
                        None
                    """
                    self.instrument.write(f":SENSe:PNoise:FREQuency:CENTer {freq}")

                def get_center(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: The carrier search frequency window in Hz.
                    """
                    return float(self.instrument.query(":SENSe:PNoise:FREQuency:CENTer?"))

                def set_offset_start(self, freq):
                    """
                    Parameter:
                        freq (float): Start frequency of the phase noise sweep as an offset from the detected carrier center frequency in Hz.
                    Return:
                        None
                    """
                    self.instrument.write(f":SENSe:PNoise:FREQuency:OFFSet:STARt {freq}")

                def get_offset_start(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: The start frequency of the phase noise sweep as an offset from the detected carrier center frequency in Hz.
                    """
                    return float(self.instrument.query(":SENSe:PNoise:FREQuency:OFFSet:STARt?"))

                def set_offset_stop(self, freq):
                    """
                    Parameter:
                        freq (float): Stop frequency of the phase noise sweep as an offset from the detected carrier center frequency in Hz.
                    Return:
                        None
                    """
                    self.instrument.write(f":SENSe:PNoise:FREQuency:OFFSet:STOP {freq}")

                def get_offset_stop(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: The stop frequency of the phase noise sweep as an offset from the detected carrier center frequency in Hz.
                    """
                    return float(self.instrument.query(":SENSe:PNoise:FREQuency:OFFSet:STOP?"))
            class XCORr:
                """
                The PNoiseXCORr commands control the cross correlation settings in phase noise measurement mode.
                """
                def __init__(self, instrument):
                    self.instrument = instrument

                class Device:
                    """
                    The Device commands control the cross correlation device settings in phase noise measurement mode.
                    """
                    def __init__(self, instrument):
                        self.instrument = instrument

                    def is_active(self):
                        """
                        Parameter:
                        None
                        Return:
                        bool: True if a device is currently connected and active, False otherwise.
                        """
                        resp = self.instrument.query(":SENSe:PNoise:XCORr:DEVice:ACTive?")
                        return resp.strip() == '1'

                    def get_count(self):
                        """
                        Parameter:
                        None
                        Return:
                        int: The number of devices connected to the PC.
                        """
                        return int(self.instrument.query(":SENSe:PNoise:XCORr:DEVice:COUNt?"))

                    def get_list(self):
                        """
                        Parameter:
                        None
                        Return:
                        str: The list of connected devices.
                        """
                        return self.instrument.query(":SENSe:PNoise:XCORr:DEVice:LIST?")

                    def get_current(self):
                        """
                        Parameter:
                        None
                        Return:
                        str: The currently active device.
                        """
                        return self.instrument.query(":SENSe:PNoise:XCORr:DEVice:CURRent?")

                    def connect(self, device_index):
                        """
                        Parameter:
                        device_index (int): The index of the device to connect.
                        Return:
                        None
                        """
                        if not isinstance(device_index, int) or device_index < 0:
                            raise ValueError("device_index must be a non-negative integer")
                        self.instrument.write(f":SENSe:PNoise:XCORr:DEVice:CONnect? {device_index}")

                    def disconnect(self):
                        """
                        Parameter:
                        None
                        Return:
                        None
                        """
                        self.instrument.write(":SENSe:PNoise:XCORr:DEVice:DISConnect?")

                def set_state(self, state):
                    """
                    Parameter:
                        state (int or str): 1/0 or 'ON'/'OFF' to enable/disable cross correlation.
                    Return:
                        None
                    """
                    if isinstance(state, str):
                        state = state.upper()
                        if state not in {"ON", "OFF"}:
                            raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                        state = 1 if state == "ON" else 0
                    elif state not in [0, 1]:
                        raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                    self.instrument.write(f":SENSe:PNoise:XCORr:STATe {state}")

                def is_enabled(self):
                    """
                    Parameter:
                        None
                    Return:
                        bool: True if cross correlation is enabled, False otherwise.
                    """
                    resp = self.instrument.query(":SENSe:PNoise:XCORr:STATe?")
                    return int(resp.strip()) == 1
        class PeakTable:
                """
                The PeakTable commands control the Peak Table display panel in Swept Analysis mode.
                """
                def __init__(self, instrument):
                    self.instrument = instrument

                def set_state(self, state):
                    """
                    Parameter:
                        state (int or str): 1/0 or 'ON'/'OFF' to enable/disable the Peak Table panel.
                    Return:
                        None
                    """
                    if isinstance(state, str):
                        state = state.upper()
                        if state not in {"ON", "OFF"}:
                            raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                        state = 1 if state == "ON" else 0
                    elif state not in [0, 1]:
                        raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                    self.instrument.write(f":SENSe:PEAK:TABLe:STATe {state}")

                def is_enabled(self):
                    """
                    Parameter:
                        None
                    Return:
                        bool: True if Peak Table panel is enabled, False otherwise.
                    """
                    resp = self.instrument.query(":SENSe:PEAK:TABLe:STATe?")
                    return int(resp.strip()) == 1

                def set_trace(self, trace_num):
                    """
                    Parameter:
                        trace_num (int): Trace index.
                    Return:
                        None
                    """
                    self.instrument.write(f":SENSe:PEAK:TABLe:TRACe {trace_num}")

                def get_trace(self):
                    """
                    Parameter:
                        None
                    Return:
                        int: The trace index used for peak measurement.
                    """
                    return int(self.instrument.query(":SENSe:PEAK:TABLe:TRACe?"))

                def set_threshold(self, value):
                    """
                    Parameter:
                        value (float): Peak threshold in dBm.
                    Return:
                        None
                    """
                    self.instrument.write(f":SENSe:PEAK:TABLe:THReshold {value}")

                def get_threshold(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: The current peak threshold in dBm.
                    """
                    return float(self.instrument.query(":SENSe:PEAK:TABLe:THReshold?"))

                def set_excursion(self, value):
                    """
                    Parameter:
                        value (float): Peak excursion in dB.
                    Return:
                        None
                    """
                    self.instrument.write(f":SENSe:PEAK:TABLe:EXCursion {value}")

                def get_excursion(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: The current peak excursion in dB.
                    """
                    return float(self.instrument.query(":SENSe:PEAK:TABLe:EXCursion?"))

                def set_sort(self, order):
                    """
                    Parameter:
                        order (str): 'FREQUENCY' or 'AMPLITUDE'.
                    Return:
                        None
                    """
                    allowed = {"FREQUENCY", "AMPLITUDE"}
                    if not isinstance(order, str) or order.upper() not in allowed:
                        raise ValueError("order must be 'FREQUENCY' or 'AMPLITUDE'")
                    self.instrument.write(f":SENSe:PEAK:TABLe:SORT {order.upper()}")

                def get_sort(self):
                    """
                    Parameter:
                        None
                    Return:
                        str: The current sort order.
                    """
                    return self.instrument.query(":SENSe:PEAK:TABLe:SORT?")

                def get_count(self):
                    """
                    Parameter:
                        None
                    Return:
                        int: The number of peaks in the table.
                    """
                    return int(self.instrument.query(":SENSe:PEAK:TABLe:COUNt?"))

                def set_max(self, value):
                    """
                    Parameter:
                        value (int): Maximum number of peaks [0,99].
                    Return:
                        None
                    """
                    if not isinstance(value, int) or not (0 <= value <= 99):
                        raise ValueError("value must be an integer between 0 and 99")
                    self.instrument.write(f":SENSe:PEAK:TABLe:MAX {value}")

                def get_max(self):
                    """
                    Parameter:
                        None
                    Return:
                        int: The maximum number of peaks.
                    """
                    return int(self.instrument.query(":SENSe:PEAK:TABLe:MAX?"))

                def get_frequency(self, peak_num):
                    """
                    Parameter:
                        peak_num (int): Peak index [1,16].
                    Return:
                        float: Frequency of the specified peak.
                    """
                    return float(self.instrument.query(f":SENSe:PEAK:TABLe:FREQuency? {peak_num}"))

                def get_amplitude(self, peak_num):
                    """
                    Parameter:
                        peak_num (int): Peak index [1,16].
                    Return:
                        float: Amplitude of the specified peak.
                    """
                    return float(self.instrument.query(f":SENSe:PEAK:TABLe:AMPLitude? {peak_num}"))

                def get_frequency_delta(self, peak_num):
                    """
                    Parameter:
                        peak_num (int): Peak index [1,16].
                    Return:
                        float: Frequency difference between the specified peak and the first peak.
                    """
                    return float(self.instrument.query(f":SENSe:PEAK:TABLe:FREQuency:DELTa? {peak_num}"))

                def get_amplitude_delta(self, peak_num):
                    """
                    Parameter:
                        peak_num (int): Peak index [1,16].
                    Return:
                        float: Amplitude difference between the specified peak and the first peak.
                    """
                    return float(self.instrument.query(f":SENSe:PEAK:TABLe:AMPLitude:DELTa? {peak_num}"))

        class ChPower:
            """
            The SenseChPower commands control the channel power measurement.
            """
            def __init__(self, instrument):
                self.instrument = instrument

            def set_state(self, state):
                """
                Parameter:
                state (int or str): 1/0 or 'ON'/'OFF' to enable/disable channel power measurement.
                Return:
                None
                """
                if isinstance(state, str):
                    state = state.upper()
                if state not in {"ON", "OFF"}:
                    raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                    state = 1 if state == "ON" else 0
                elif state not in [0, 1]:
                    raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                self.instrument.write(f":SENSe:CHPower:STATe {state}")

            def is_enabled(self):
                """
                Parameter:
                None
                Return:
                bool: True if channel power measurement is enabled, False otherwise.
                """
                resp = self.instrument.query(":SENSe:CHPower:STATe?")
                return int(resp.strip()) == 1

            def set_trace(self, trace_num):
                """
                Parameter:
                trace_num (int): Trace index.
                Return:
                None
                """
                self.instrument.write(f":SENSe:CHPower:TRACe {trace_num}")

            def get_trace(self):
                """
                Parameter:
                None
                Return:
                int: The trace index used for channel power measurement.
                """
                return int(self.instrument.query(":SENSe:CHPower:TRACe?"))

            def set_width(self, freq):
                """
                Parameter:
                freq (float): Width of the main channel (Hz).
                Return:
                None
                """
                self.instrument.write(f":SENSe:CHPower:WIDth {freq}")

            def get_width(self):
                """
                Parameter:
                None
                Return:
                float: The width of the main channel (Hz).
                """
                return float(self.instrument.query(":SENSe:CHPower:WIDth?"))

            def set_channel_state(self, channel_num, state):
                """
                Parameter:
                channel_num (int): Channel index.
                state (int or str): 1/0 or 'ON'/'OFF' to enable/disable adjacent channel.
                Return:
                None
                """
                if isinstance(state, str):
                    state = state.upper()
                if state not in {"ON", "OFF"}:
                    raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                    state = 1 if state == "ON" else 0
                elif state not in [0, 1]:
                    raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                self.instrument.write(f":SENSe:CHPower:CHANnel:STATe {channel_num},{state}")

            def get_channel_state(self, channel_num):
                """
                Parameter:
                channel_num (int): Channel index.
                Return:
                bool: True if adjacent channel is enabled, False otherwise.
                """
                resp = self.instrument.query(f":SENSe:CHPower:CHANnel:STATe? {channel_num}")
                return int(resp.strip()) == 1

            def set_channel_offset(self, channel_num, freq):
                """
                Parameter:
                channel_num (int): Channel index.
                freq (float): Offset from center (Hz).
                Return:
                None
                """
                self.instrument.write(f":SENSe:CHPower:CHANnel:OFFSet {channel_num},{freq}")

            def get_channel_offset(self, channel_num):
                """
                Parameter:
                channel_num (int): Channel index.
                Return:
                float: Offset from center (Hz).
                """
                return float(self.instrument.query(f":SENSe:CHPower:CHANnel:OFFSet? {channel_num}"))

            def set_channel_width(self, channel_num, freq):
                """
                Parameter:
                channel_num (int): Channel index.
                freq (float): Channel width (Hz).
                Return:
                None
                """
                self.instrument.write(f":SENSe:CHPower:CHANnel:WIDth {channel_num},{freq}")

            def get_channel_width(self, channel_num):
                """
                Parameter:
                channel_num (int): Channel index.
                Return:
                float: Channel width (Hz).
                """
                return float(self.instrument.query(f":SENSe:CHPower:CHANnel:WIDth? {channel_num}"))

            def get_chpower(self):
                """
                Parameter:
                None
                Return:
                float: Channel power of the main channel.
                """
                return float(self.instrument.query(":SENSe:CHPower:CHPower?"))

            def get_chpower_lower(self, channel_num):
                """
                Parameter:
                channel_num (int): Channel index.
                Return:
                float: Lower channel power of adjacent channel (dBm).
                """
                return float(self.instrument.query(f":SENSe:CHPower:CHPower:LOWer? {channel_num}"))

            def get_chpower_upper(self, channel_num):
                """
                Parameter:
                channel_num (int): Channel index.
                Return:
                float: Upper channel power of adjacent channel (dBm).
                """
                return float(self.instrument.query(f":SENSe:CHPower:CHPower:UPPer? {channel_num}"))

            def get_acpower_lower(self, channel_num):
                """
                Parameter:
                channel_num (int): Channel index.
                Return:
                float: Lower adjacent power of adjacent channel (dBc).
                """
                return float(self.instrument.query(f":SENSe:CHPower:ACPower:LOWer? {channel_num}"))

            def get_acpower_upper(self, channel_num):
                """
                Parameter:
                channel_num (int): Channel index.
                Return:
                float: Upper adjacent power of adjacent channel (dBc).
                """
                return float(self.instrument.query(f":SENSe:CHPower:ACPower:UPPer? {channel_num}"))
        class Pathloss:
            """
            The Pathloss commands control the path loss tables.
            """
            def __init__(self, instrument, table_num=1):
                self.instrument = instrument
                if not 1 <= table_num <= 8:
                    raise ValueError("Path loss table number must be between 1 and 8.")
                self.table_num = table_num

            def set_enabled(self, state):
                """
                Parameter:
                    state (int or str): 1/0 or 'ON'/'OFF' to enable/disable this path loss table.
                Return:
                    None
                """
                if isinstance(state, str):
                    state = state.upper()
                    if state not in {"ON", "OFF"}:
                        raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                    state = 1 if state == "ON" else 0
                elif state not in [0, 1]:
                    raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                self.instrument.write(f":SENSe:CORRection:PATHloss{self.table_num}:STATe {state}")

            def is_enabled(self):
                """
                Parameter:
                    None
                Return:
                    bool: True if this path loss table is enabled, False otherwise.
                """
                resp = self.instrument.query(f":SENSe:CORRection:PATHloss{self.table_num}:STATe?")
                return resp.strip() == 1

            def set_description(self, desc):
                """
                Parameter:
                    desc (str): The name/description of this path loss table.
                Return:
                    None
                """
                self.instrument.write(f':SENSe:CORRection:PATHloss{self.table_num}:DESCription "{desc}"')

            def get_description(self):
                """
                Parameter:
                    None
                Return:
                    str: The name/description of this path loss table.
                """
                return self.instrument.query(f":SENSe:CORRection:PATHloss{self.table_num}:DESCription?")

            def get_points_count(self):
                """
                Parameter:
                    None
                Return:
                    int: Number of points in the path loss table.
                """
                return int(self.instrument.query(f":SENSe:CORRection:PATHloss{self.table_num}:POINts?"))

            def set_data(self, points):
                """
                Parameter:
                    points (list of tuple): List of (freq, offset) pairs.
                Return:
                    None
                """
                if not isinstance(points, list) or not all(isinstance(p, tuple) and len(p) == 2 for p in points):
                    raise ValueError("points must be a list of (freq, offset) tuples")
                data_str = ", ".join(f"{freq},{offset}" for freq, offset in points)
                self.instrument.write(f":SENSe:CORRection:PATHloss{self.table_num}:DATA {data_str}")

            def get_data(self):
                """
                Parameter:
                    None
                Return:
                    str: The points in the path loss table as freq/offset pairs.
                """
                return self.instrument.query(f":SENSe:CORRection:PATHloss{self.table_num}:DATA?")

            def clear(self):
                """
                Parameter:
                    None
                Return:
                    None
                """
                self.instrument.write(f":SENSe:CORRection:PATHloss{self.table_num}:CLEAr")

            @staticmethod
            def clear_all(instrument):
                """
                Parameter:
                    instrument: The instrument instance.
                Return:
                    None
                """
                instrument.write(":SENSe:CORRection:PATHloss:ALL:CLEAr")
        
        class Frequency:
            """
            The Frequency commands control the frequency range and step of the sweep in swept analysis mode.
            """
            def __init__(self, instrument):
                self.instrument = instrument

            def set_center(self, freq):
                """
                Parameter:
                    freq (float or str): Center frequency in Hz, or 'UP', or 'DOWN'.
                Return:
                    None
                """
                if isinstance(freq, str):
                    if freq.upper() not in {"UP", "DOWN"}:
                        raise ValueError("freq must be a float or one of 'UP', 'DOWN'")
                    freq_str = freq.upper()
                else:
                    freq_str = str(freq)
                self.instrument.write(f":SENSe:FREQuency:CENTer {freq_str}")

            def get_center(self, bound=None):
                """
                Parameter:
                    bound (str, optional): 'MIN' or 'MAX' to query frequency limits, or None for current center.
                Return:
                    float: The center frequency in Hz, or the min/max limit.
                """
                if bound is not None:
                    bound = bound.upper()
                    if bound not in {"MIN", "MAX"}:
                        raise ValueError("bound must be 'MIN' or 'MAX'")
                    resp = self.instrument.query(f":SENSe:FREQuency:CENTer? {bound}")
                else:
                    resp = self.instrument.query(":SENSe:FREQuency:CENTer?")
                return float(resp)

            def set_start(self, freq):
                """
                Parameter:
                    freq (float): Start frequency in Hz.
                Return:
                    None
                """
                self.instrument.write(f":SENSe:FREQuency:STARt {freq}")

            def get_start(self):
                """
                Parameter:
                    None
                Return:
                    float: The current measurement start frequency in Hz.
                """
                return float(self.instrument.query(":SENSe:FREQuency:STARt?"))

            def set_stop(self, freq):
                """
                Parameter:
                    freq (float): Stop frequency in Hz.
                Return:
                    None
                """
                self.instrument.write(f":SENSe:FREQuency:STOP {freq}")

            def get_stop(self):
                """
                Parameter:
                    None
                Return:
                    float: The current measurement stop frequency in Hz.
                """
                return float(self.instrument.query(":SENSe:FREQuency:STOP?"))

            def set_center_step(self, freq):
                """
                Parameter:
                    freq (float): Step amount for center frequency changes in Hz.
                Return:
                    None
                """
                self.instrument.write(f":SENSe:FREQuency:CENTer:STEP {freq}")

            def get_center_step(self):
                """
                Parameter:
                    None
                Return:
                    float: The center frequency step size in Hz.
                """
                return float(self.instrument.query(":SENSe:FREQuency:CENTer:STEP?"))

            def set_span(self, span):
                """
                Parameter:
                    span (float or str): Span in Hz, or 'UP', or 'DOWN'.
                Return:
                    None
                """
                if isinstance(span, str):
                    if span.upper() not in {"UP", "DOWN"}:
                        raise ValueError("span must be a float or one of 'UP', 'DOWN'")
                    span_str = span.upper()
                else:
                    span_str = str(span)
                self.instrument.write(f":SENSe:FREQuency:SPAN {span_str}")

            def get_span(self):
                """
                Parameter:
                    None
                Return:
                    float: The span in Hz.
                """
                return float(self.instrument.query(":SENSe:FREQuency:SPAN?"))

    
        class Power:
            """
            The Power commands affect the RF front end of the device.
            """
            def __init__(self, instrument):
                self.instrument = instrument

            def set_reference_level(self, amplitude):
                """
                Parameter:
                    amplitude (float or str): Reference level in dBm or 'UP'/'DOWN'.
                Return:
                    None
                """
                if isinstance(amplitude, str):
                    if amplitude.upper() not in {"UP", "DOWN"}:
                        raise ValueError("amplitude must be a float or one of 'UP', 'DOWN'")
                    amp_str = amplitude.upper()
                else:
                    amp_str = str(amplitude)
                self.instrument.write(f":SENSe:POWer:RF:RLEVel {amp_str}")

            def get_reference_level(self):
                """
                Parameter:
                    None
                Return:
                    float: The current reference level as dBm.
                """
                return float(self.instrument.query(":SENSe:POWer:RF:RLEVel?"))

            def get_reference_level_unit(self):
                """
                Parameter:
                    None
                Return:
                    str: The current amplitude unit used to express reference level.
                """
                return self.instrument.query(":SENSe:POWer:RF:RLEVel:UNIT?")

            def set_reference_level_offset(self, offset):
                """
                Parameter:
                    offset (float): Reference level offset in dB.
                Return:
                    None
                """
                self.instrument.write(f":SENSe:POWer:RF:RLEVel:OFFSet {offset}")

            def get_reference_level_offset(self):
                """
                Parameter:
                    None
                Return:
                    float: The reference level offset in dB.
                """
                return float(self.instrument.query(":SENSe:POWer:RF:RLEVel:OFFSet?"))

            def set_plot_vertical_division(self, division):
                """
                Parameter:
                    division (float): Plot vertical division in dB.
                Return:
                    None
                """
                self.instrument.write(f":SENSe:POWer:RF:PDIVision {division}")

            def get_plot_vertical_division(self):
                """
                Parameter:
                    None
                Return:
                    float: The plot vertical division in dB.
                """
                return float(self.instrument.query(":SENSe:POWer:RF:PDIVision?"))

            def set_attenuation(self, value):
                """
                Parameter:
                    value (int): Attenuation index.
                Return:
                    None
                """
                if not isinstance(value, int):
                    raise ValueError("value must be an integer")
                self.instrument.write(f":SENSe:POWer:RF:ATTenuation {value}")

            def get_attenuation(self):
                """
                Parameter:
                    None
                Return:
                    int: The attenuation index.
                """
                return int(self.instrument.query(":SENSe:POWer:RF:ATTenuation?"))

            def set_attenuation_auto(self, state):
                """
                Parameter:
                    state (int or str): 1/0 or 'ON'/'OFF' to enable/disable auto attenuation.
                Return:
                    None
                """
                if isinstance(state, str):
                    state = state.upper()
                    if state not in {"ON", "OFF"}:
                        raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                    state = 1 if state == "ON" else 0
                elif state not in [0, 1]:
                    raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                self.instrument.write(f":SENSe:POWer:RF:ATTenuation:AUTO {state}")

            def is_attenuation_auto(self):
                """
                Parameter:
                    None
                Return:
                    bool: True if auto attenuation is enabled, False otherwise.
                """
                resp = self.instrument.query(":SENSe:POWer:RF:ATTenuation:AUTO?")
                return resp.strip() == 1

            def set_gain(self, value):
                """
                Parameter:
                    value (int): Gain index.
                Return:
                    None
                """
                if not isinstance(value, int):
                    raise ValueError("value must be an integer")
                self.instrument.write(f":SENSe:POWer:RF:GAIN {value}")

            def get_gain(self):
                """
                Parameter:
                    None
                Return:
                    int: The gain index.
                """
                return int(self.instrument.query(":SENSe:POWer:RF:GAIN?"))

            def set_gain_auto(self, state):
                """
                Parameter:
                    state (int or str): 1/0 or 'ON'/'OFF' to enable/disable auto gain.
                Return:
                    None
                """
                if isinstance(state, str):
                    state = state.upper()
                    if state not in {"ON", "OFF"}:
                        raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                    state = 1 if state == "ON" else 0
                elif state not in [0, 1]:
                    raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                self.instrument.write(f":SENSe:POWer:RF:GAIN:AUTO {state}")

            def is_gain_auto(self):
                """
                Parameter:
                    None
                Return:
                    bool: True if auto gain is enabled, False otherwise.
                """
                resp = self.instrument.query(":SENSe:POWer:RF:GAIN:AUTO?")
                return resp.strip() == 1

            def set_preamp(self, value):
                """
                Parameter:
                    value (int): Preamp state (typically 0 or 1).
                Return:
                    None
                """
                if value not in [0, 1]:
                    raise ValueError("value must be 0 or 1")
                self.instrument.write(f":SENSe:POWer:RF:PREAMP {value}")

            def get_preamp(self):
                """
                Parameter:
                    None
                Return:
                    int: The preamp state (0 or 1).
                """
                return int(self.instrument.query(":SENSe:POWer:RF:PREAMP?"))

            def set_preamp_auto(self, state):
                """
                Parameter:
                    state (int or str): 1/0 or 'ON'/'OFF' to enable/disable auto preamp.
                Return:
                    None
                """
                if isinstance(state, str):
                    state = state.upper()
                    if state not in {"ON", "OFF"}:
                        raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                    state = 1 if state == "ON" else 0
                elif state not in [0, 1]:
                    raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                self.instrument.write(f":SENSe:POWer:RF:PREAMP:AUTO {state}")

            def is_preamp_auto(self):
                """
                Parameter:
                    None
                Return:
                    bool: True if auto preamp is enabled, False otherwise.
                """
                resp = self.instrument.query(":SENSe:POWer:RF:PREAMP:AUTO?")
                return resp.strip() == 1

            def set_preselector_state(self, state):
                """
                Parameter:
                    state (int or str): 1/0 or 'ON'/'OFF' to enable/disable preselector (SM200A only).
                Return:
                    None
                """
                if isinstance(state, str):
                    state = state.upper()
                    if state not in {"ON", "OFF"}:
                        raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                    state = 1 if state == "ON" else 0
                elif state not in [0, 1]:
                    raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                self.instrument.write(f":SENSe:POWer:RF:MW:PRESelector:STATe {state}")

            def is_preselector_enabled(self):
                """
                Parameter:
                    None
                Return:
                    bool: True if preselector is enabled, False otherwise.
                """
                resp = self.instrument.query(":SENSe:POWer:RF:MW:PRESelector:STATe?")
                return resp.strip() == 1

            def set_spur_reject(self, state):
                """
                Parameter:
                    state (int or str): 1/0 or 'ON'/'OFF' to enable/disable spur reject.
                Return:
                    None
                """
                if isinstance(state, str):
                    state = state.upper()
                    if state not in {"ON", "OFF"}:
                        raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                    state = 1 if state == "ON" else 0
                elif state not in [0, 1]:
                    raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                self.instrument.write(f":SENSe:POWer:RF:SPURReject {state}")

            def is_spur_reject_enabled(self):
                """
                Parameter:
                    None
                Return:
                    bool: True if spur reject is enabled, False otherwise.
                """
                resp = self.instrument.query(":SENSe:POWer:RF:SPURReject?")
                return resp.strip() == 1
        class Bandwidth:
            """
            The Bandwidth commands control the FFT processing for the receivers.
            """
            def __init__(self, instrument):
                self.instrument = instrument

            def set_resolution(self, freq):
                """
                Parameter:
                    freq (float or str): RBW in Hz, or 'UP', or 'DOWN'.
                Return:
                    None
                """
                if isinstance(freq, str):
                    if freq.upper() not in {"UP", "DOWN"}:
                        raise ValueError("freq must be a float or one of 'UP', 'DOWN'")
                    freq_str = freq.upper()
                else:
                    freq_str = str(freq)
                self.instrument.write(f":SENSe:BANDwidth:RESolution {freq_str}")

            def get_resolution(self):
                """
                Parameter:
                    None
                Return:
                    float: The current RBW in Hz.
                """
                return float(self.instrument.query(":SENSe:BANDwidth:RESolution?"))

            def set_resolution_auto(self, state):
                """
                Parameter:
                    state (int or str): 1/0 or 'ON'/'OFF' to enable/disable auto RBW.
                Return:
                    None
                """
                if isinstance(state, str):
                    state = state.upper()
                    if state not in {"ON", "OFF"}:
                        raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                    state = 1 if state == "ON" else 0
                elif state not in [0, 1]:
                    raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                self.instrument.write(f":SENSe:BANDwidth:RESolution:AUTO {state}")

            def is_resolution_auto(self):
                """
                Parameter:
                    None
                Return:
                    bool: True if auto RBW is enabled, False otherwise.
                """
                resp = self.instrument.query(":SENSe:BANDwidth:RESolution:AUTO?")
                return resp.strip() == 1

            def set_video(self, freq):
                """
                Parameter:
                    freq (float or str): VBW in Hz, or 'UP', or 'DOWN'.
                Return:
                    None
                """
                if isinstance(freq, str):
                    if freq.upper() not in {"UP", "DOWN"}:
                        raise ValueError("freq must be a float or one of 'UP', 'DOWN'")
                    freq_str = freq.upper()
                else:
                    freq_str = str(freq)
                self.instrument.write(f":SENSe:BANDwidth:VIDeo {freq_str}")

            def get_video(self):
                """
                Parameter:
                    None
                Return:
                    float: The current VBW in Hz.
                """
                return float(self.instrument.query(":SENSe:BANDwidth:VIDeo?"))

            def set_video_auto(self, state):
                """
                Parameter:
                    state (int or str): 1/0 or 'ON'/'OFF' to enable/disable auto VBW.
                Return:
                    None
                """
                if isinstance(state, str):
                    state = state.upper()
                    if state not in {"ON", "OFF"}:
                        raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                    state = 1 if state == "ON" else 0
                elif state not in [0, 1]:
                    raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                self.instrument.write(f":SENSe:BANDwidth:VIDeo:AUTO {state}")

            def is_video_auto(self):
                """
                Parameter:
                    None
                Return:
                    bool: True if auto VBW is enabled, False otherwise.
                """
                resp = self.instrument.query(":SENSe:BANDwidth:VIDeo:AUTO?")
                return resp.strip() == 1

            def set_shape(self, shape):
                """
                Parameter:
                    shape (str): 'FLATTOP', 'NUTTALL', or 'GAUSSIAN'.
                Return:
                    None
                """
                allowed = {"FLATTOP", "NUTTALL", "GAUSSIAN"}
                if not isinstance(shape, str) or shape.upper() not in allowed:
                    raise ValueError("shape must be one of 'FLATTOP', 'NUTTALL', or 'GAUSSIAN'")
                self.instrument.write(f":SENSe:BANDwidth:SHAPe {shape.upper()}")

            def get_shape(self):
                """
                Parameter:
                    None
                Return:
                    str: The current FFT window function.
                """
                return self.instrument.query(":SENSe:BANDwidth:SHAPe?")
        class Sweep:
            """
            The Sweep commands control additional FFT settings of the receiver.
            """
            def __init__(self, instrument):
                self.instrument = instrument

            def set_time(self, value):
                """
                Parameter:
                    value (float): Sweep time in seconds.
                Return:
                    None
                """
                self.instrument.write(f":SENSe:SWEep:TIME {value}")

            def get_time(self):
                """
                Parameter:
                    None
                Return:
                    float: The current sweep time in seconds.
                """
                return float(self.instrument.query(":SENSe:SWEep:TIME?"))

            class Detector:
                """
                The Detector commands control how the VBW processing is performed.
                """
                def __init__(self, instrument):
                    self.instrument = instrument

                def set_function(self, func):
                    """
                    Parameter:
                        func (str): 'AVERAGE', 'MINMAX', 'MIN', or 'MAX'.
                    Return:
                        None
                    """
                    allowed = {"AVERAGE", "MINMAX", "MIN", "MAX"}
                    if not isinstance(func, str) or func.upper() not in allowed:
                        raise ValueError("func must be one of 'AVERAGE', 'MINMAX', 'MIN', or 'MAX'")
                    self.instrument.write(f":SENSe:SWEep:DETector:FUNCtion {func.upper()}")

                def get_function(self):
                    """
                    Parameter:
                        None
                    Return:
                        str: The current detector function.
                    """
                    return self.instrument.query(":SENSe:SWEep:DETector:FUNCtion?")

                def set_units(self, units):
                    """
                    Parameter:
                        units (str): 'POWER', 'SAMPLE', 'VOLTAGE', or 'LOG'.
                    Return:
                        None
                    """
                    allowed = {"POWER", "SAMPLE", "VOLTAGE", "LOG"}
                    if not isinstance(units, str) or units.upper() not in allowed:
                        raise ValueError("units must be one of 'POWER', 'SAMPLE', 'VOLTAGE', or 'LOG'")
                    self.instrument.write(f":SENSe:SWEep:DETector:UNITs {units.upper()}")

                def get_units(self):
                    """
                    Parameter:
                        None
                    Return:
                        str: The current detector units.
                    """
                    return self.instrument.query(":SENSe:SWEep:DETector:UNITs?")
    class Trace:
        """
        The Trace commands control the user configurable traces for sweep mode.
        """
        def __init__(self, instrument):
            self.instrument = instrument

        def select(self, trace_num):
            """
            Parameter:
                trace_num (int): Trace index [1,6].
            Return:
                None
            """
            if not isinstance(trace_num, int) or not (1 <= trace_num <= 6):
                raise ValueError("trace_num must be an integer between 1 and 6")
            self.instrument.write(f":TRACe:SELect {trace_num}")

        def get_selected(self):
            """
            Parameter:
                None
            Return:
                int: The currently selected trace index.
            """
            return int(self.instrument.query(":TRACe:SELect?"))

        def set_type(self, typ):
            """
            Parameter:
                typ (str): 'OFF', 'WRITE', 'AVERAGE', 'MAXHOLD', 'MINHOLD', or 'MINMAX'.
            Return:
                None
            """
            allowed = {"OFF", "WRITE", "AVERAGE", "MAXHOLD", "MINHOLD", "MINMAX"}
            if not isinstance(typ, str) or typ.upper() not in allowed:
                raise ValueError("typ must be one of 'OFF', 'WRITE', 'AVERAGE', 'MAXHOLD', 'MINHOLD', or 'MINMAX'")
            self.instrument.write(f":TRACe:TYPE {typ.upper()}")

        def get_type(self):
            """
            Parameter:
                None
            Return:
                str: The current trace type.
            """
            return self.instrument.query(":TRACe:TYPE?")

        def set_average_count(self, count):
            """
            Parameter:
                count (int): Number of traces to average together.
            Return:
                None
            """
            if not isinstance(count, int) or count < 1:
                raise ValueError("count must be a positive integer")
            self.instrument.write(f":TRACe:AVERage:COUNt {count}")

        def get_average_count(self):
            """
            Parameter:
                None
            Return:
                int: The number of traces averaged together.
            """
            return int(self.instrument.query(":TRACe:AVERage:COUNt?"))

        def get_average_current(self):
            """
            Parameter:
                None
            Return:
                int: The current number of traces averaged together.
            """
            return int(self.instrument.query(":TRACe:AVERage:CURRent?"))

        def copy(self, dest_trace_num):
            """
            Parameter:
                dest_trace_num (int): Destination trace index [1,6], not equal to current.
            Return:
                None
            """
            if not isinstance(dest_trace_num, int) or not (1 <= dest_trace_num <= 6):
                raise ValueError("dest_trace_num must be an integer between 1 and 6")
            self.instrument.write(f":TRACe:COPY {dest_trace_num}")

        def set_update_state(self, state):
            """
            Parameter:
                state (int or str): 1/0 or 'ON'/'OFF' to enable/disable trace update.
            Return:
                None
            """
            if isinstance(state, str):
                state = state.upper()
                if state not in {"ON", "OFF"}:
                    raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                state = 1 if state == "ON" else 0
            elif state not in [0, 1]:
                raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
            self.instrument.write(f":TRACe:UPDate:STATe {state}")

        def is_update_enabled(self):
            """
            Parameter:
                None
            Return:
                bool: True if trace update is enabled, False otherwise.
            """
            resp = self.instrument.query(":TRACe:UPDate:STATe?")
            return int(resp.strip()) == 1

        def set_display_state(self, state):
            """
            Parameter:
                state (int or str): 1/0 or 'ON'/'OFF' to show/hide the trace.
            Return:
                None
            """
            if isinstance(state, str):
                state = state.upper()
                if state not in {"ON", "OFF"}:
                    raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                state = 1 if state == "ON" else 0
            elif state not in [0, 1]:
                raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
            self.instrument.write(f":TRACe:DISPlay:STATe {state}")

        def is_displayed(self):
            """
            Parameter:
                None
            Return:
                bool: True if trace is displayed, False otherwise.
            """
            resp = self.instrument.query(":TRACe:DISPlay:STATe?")
            return int(resp.strip()) == 1

        def clear(self):
            """
            Parameter:
                None
            Return:
                None
            """
            self.instrument.write(":TRACe:CLEar")

        def clear_all(self):
            """
            Parameter:
                None
            Return:
                None
            """
            self.instrument.write(":TRACe:CLEar:ALL")

        def get_xstart(self):
            """
            Parameter:
                None
            Return:
                float: Frequency of the first point in the sweep (Hz).
            """
            return float(self.instrument.query(":TRACe:XSTARt?"))

        def get_xincrement(self):
            """
            Parameter:
                None
            Return:
                float: Frequency step between two points in the trace data (Hz).
            """
            return float(self.instrument.query(":TRACe:XINCrement?"))

        def get_points_count(self):
            """
            Parameter:
                None
            Return:
                int: Number of points in the trace data.
            """
            return int(self.instrument.query(":TRACe:POINts?"))

        def get_data(self):
            """
            Parameter:
                None
            Return:
                str: The trace data as comma separated ascii floating point values.
            """
            return self.instrument.query(":TRACe:DATA?")
            
    class Record:
        """
        The Record commands control the Sweep Recording control panel in Swept Analysis mode.
        """
        def __init__(self, instrument):
            self.instrument = instrument

        class Sweep:
            def __init__(self, instrument):
                self.instrument = instrument

            class Decimate:
                def __init__(self, instrument):
                    self.instrument = instrument

                def set_type(self, typ):
                    """
                    Parameter:
                        typ (str): 'TIME' or 'COUNT'.
                    Return:
                        None
                    """
                    allowed = {"TIME", "COUNT"}
                    if not isinstance(typ, str) or typ.upper() not in allowed:
                        raise ValueError("typ must be 'TIME' or 'COUNT'")
                    self.instrument.write(f":RECord:SWEep:DECimate:TYPE {typ.upper()}")

                def get_type(self):
                    """
                    Parameter:
                        None
                    Return:
                        str: The current decimation type.
                    """
                    return self.instrument.query(":RECord:SWEep:DECimate:TYPE?")

                def set_time(self, value):
                    """
                    Parameter:
                        value (float): Decimation time.
                    Return:
                        None
                    """
                    self.instrument.write(f":RECord:SWEep:DECimate:TIME {value}")

                def get_time(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: The decimation time.
                    """
                    return float(self.instrument.query(":RECord:SWEep:DECimate:TIME?"))

                def set_count(self, value):
                    """
                    Parameter:
                        value (int): Number of sweeps by which to decimate.
                    Return:
                        None
                    """
                    if not isinstance(value, int):
                        raise ValueError("value must be an integer")
                    self.instrument.write(f":RECord:SWEep:DECimate:COUNt {value}")

                def get_count(self):
                    """
                    Parameter:
                        None
                    Return:
                        int: The decimation count.
                    """
                    return int(self.instrument.query(":RECord:SWEep:DECimate:COUNt?"))

                def set_detector(self, det):
                    """
                    Parameter:
                        det (str): 'AVERAGE' or 'MAX'.
                    Return:
                        None
                    """
                    allowed = {"AVERAGE", "MAX"}
                    if not isinstance(det, str) or det.upper() not in allowed:
                        raise ValueError("det must be 'AVERAGE' or 'MAX'")
                    self.instrument.write(f":RECord:SWEep:DECimate:DETector {det.upper()}")

                def get_detector(self):
                    """
                    Parameter:
                        None
                    Return:
                        str: The decimation detector.
                    """
                    return self.instrument.query(":RECord:SWEep:DECimate:DETector?")

            class Channelizer:
                def __init__(self, instrument):
                    self.instrument = instrument

                def set_state(self, state):
                    """
                    Parameter:
                        state (int or str): 1/0 or 'ON'/'OFF' to enable/disable channelizer.
                    Return:
                        None
                    """
                    if isinstance(state, str):
                        state = state.upper()
                        if state not in {"ON", "OFF"}:
                            raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                        state = 1 if state == "ON" else 0
                    elif state not in [0, 1]:
                        raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                    self.instrument.write(f":RECord:SWEep:CHANnelizer:STATe {state}")

                def is_enabled(self):
                    """
                    Parameter:
                        None
                    Return:
                        bool: True if channelizer is enabled, False otherwise.
                    """
                    resp = self.instrument.query(":RECord:SWEep:CHANnelizer:STATe?")
                    return int(resp.strip()) == 1

                def set_center(self, freq):
                    """
                    Parameter:
                        freq (float): Center frequency (Hz).
                    Return:
                        None
                    """
                    self.instrument.write(f":RECord:SWEep:CHANnelizer:CENTer {freq}")

                def get_center(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: The center frequency (Hz).
                    """
                    return float(self.instrument.query(":RECord:SWEep:CHANnelizer:CENTer?"))

                def set_spacing(self, freq):
                    """
                    Parameter:
                        freq (float): Channel spacing (Hz).
                    Return:
                        None
                    """
                    self.instrument.write(f":RECord:SWEep:CHANnelizer:SPACing {freq}")

                def get_spacing(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: The channel spacing (Hz).
                    """
                    return float(self.instrument.query(":RECord:SWEep:CHANnelizer:SPACing?"))

                def set_units(self, units):
                    """
                    Parameter:
                        units (str): 'DBM' or 'DBMHZ'.
                    Return:
                        None
                    """
                    allowed = {"DBM", "DBMHZ"}
                    if not isinstance(units, str) or units.upper() not in allowed:
                        raise ValueError("units must be 'DBM' or 'DBMHZ'")
                    self.instrument.write(f":RECord:SWEep:CHANnelizer:UNITs {units.upper()}")

                def get_units(self):
                    """
                    Parameter:
                        None
                    Return:
                        str: The output units.
                    """
                    return self.instrument.query(":RECord:SWEep:CHANnelizer:UNITs?")

            def get_progress(self):
                """
                Parameter:
                    None
                Return:
                    float: The progress of the current decimation in percent.
                """
                return float(self.instrument.query(":RECord:SWEep:PROGress?"))

            def get_count(self):
                """
                Parameter:
                    None
                Return:
                    int: The number of sweeps saved so far.
                """
                return int(self.instrument.query(":RECord:SWEep:COUNt?"))

            def get_file_size(self):
                """
                Parameter:
                    None
                Return:
                    float: The size of the file in bytes.
                """
                return float(self.instrument.query(":RECord:SWEep:FILE:SIZE?"))

            def set_file_prefix(self, prefix):
                """
                Parameter:
                    prefix (str): File prefix.
                Return:
                    None
                """
                self.instrument.write(f':RECord:SWEep:FILE:PREfix "{prefix}"')

            def get_file_prefix(self):
                """
                Parameter:
                    None
                Return:
                    str: The file prefix.
                """
                return self.instrument.query(":RECord:SWEep:FILE:PREfix?")

            def set_directory(self, directory):
                """
                Parameter:
                    directory (str): Directory path.
                Return:
                    None
                """
                self.instrument.write(f':RECord:SWEep:FILE:DIRectory "{directory}"')

            def get_directory(self):
                """
                Parameter:
                    None
                Return:
                    str: The directory path.
                """
                return self.instrument.query(":RECord:SWEep:FILE:DIRectory?")

            def start(self):
                """
                Parameter:
                    None
                Return:
                    None
                """
                self.instrument.write(":RECord:SWEep:STARt")

            def stop(self):
                """
                Parameter:
                    None
                Return:
                    None
                """
                self.instrument.write(":RECord:SWEep:STOP")

            def is_recording(self):
                """
                Parameter:
                    None
                Return:
                    bool: True if actively recording, False otherwise.
                """
                resp = self.instrument.query(":RECord:SWEep:STATus?")
                return int(resp.strip()) == 1

            class ZeroSpan:
                """
                The ZeroSpan commands control the receiver configuration in zero-span mode.
                """
                def __init__(self, instrument):
                    self.instrument = instrument

                class Capture:
                    def __init__(self, instrument):
                        self.instrument = instrument

                    def set_rlevel(self, amplitude):
                        """
                        Parameter:
                            amplitude (float): Reference level in dBm.
                        Return:
                            None
                        """
                        self.instrument.write(f":SENSe:ZS:CAPture:RLEVel {amplitude}")

                    def get_rlevel(self):
                        """
                        Parameter:
                            None
                        Return:
                            float: The current reference level as dBm.
                        """
                        return float(self.instrument.query(":SENSe:ZS:CAPture:RLEVel?"))

                    def set_center(self, freq):
                        """
                        Parameter:
                            freq (float or str): Center frequency in Hz, or 'UP', or 'DOWN'.
                        Return:
                            None
                        """
                        if isinstance(freq, str):
                            if freq.upper() not in {"UP", "DOWN"}:
                                raise ValueError("freq must be a float or one of 'UP', 'DOWN'")
                            freq_str = freq.upper()
                        else:
                            freq_str = str(freq)
                        self.instrument.write(f":SENSe:ZS:CAPture:CENTer {freq_str}")

                    def get_center(self, bound=None):
                        """
                        Parameter:
                            bound (str, optional): 'MIN' or 'MAX' to query frequency limits, or None for current center.
                        Return:
                            float: The center frequency in Hz, or the min/max limit.
                        """
                        if bound is not None:
                            bound = bound.upper()
                            if bound not in {"MIN", "MAX"}:
                                raise ValueError("bound must be 'MIN' or 'MAX'")
                            resp = self.instrument.query(f":SENSe:ZS:CAPture:CENTer? {bound}")
                        else:
                            resp = self.instrument.query(":SENSe:ZS:CAPture:CENTer?")
                        return float(resp)

                    def set_center_step(self, freq):
                        """
                        Parameter:
                            freq (float): Step amount for center frequency changes in Hz.
                        Return:
                            None
                        """
                        self.instrument.write(f":SENSe:ZS:CAPture:CENTer:STEP {freq}")

                    def get_center_step(self):
                        """
                        Parameter:
                            None
                        Return:
                            float: The center frequency step size in Hz.
                        """
                        return float(self.instrument.query(":SENSe:ZS:CAPture:CENTer:STEP?"))

                    def set_srate(self, freq):
                        """
                        Parameter:
                            freq (float): Sample rate in Hz.
                        Return:
                            None
                        """
                        self.instrument.write(f":SENSe:ZS:CAPture:SRATe {freq}")

                    def get_srate(self):
                        """
                        Parameter:
                            None
                        Return:
                            float: The sample rate in Hz.
                        """
                        return float(self.instrument.query(":SENSe:ZS:CAPture:SRATe?"))

                    def set_ifbwidth(self, freq):
                        """
                        Parameter:
                            freq (float): IF bandwidth in Hz.
                        Return:
                            None
                        """
                        self.instrument.write(f":SENSe:ZS:CAPture:IFBWidth {freq}")

                    def get_ifbwidth(self):
                        """
                        Parameter:
                            None
                        Return:
                            float: The IF bandwidth in Hz.
                        """
                        return float(self.instrument.query(":SENSe:ZS:CAPture:IFBWidth?"))

                    def set_ifbwidth_auto(self, state):
                        """
                        Parameter:
                            state (int or str): 1/0 or 'ON'/'OFF' to enable/disable auto IF bandwidth.
                        Return:
                            None
                        """
                        if isinstance(state, str):
                            state = state.upper()
                            if state not in {"ON", "OFF"}:
                                raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                            state = 1 if state == "ON" else 0
                        elif state not in [0, 1]:
                            raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                        self.instrument.write(f":SENSe:ZS:CAPture:IFBWidth:AUTO {state}")

                    def is_ifbwidth_auto(self):
                        """
                        Parameter:
                            None
                        Return:
                            bool: True if auto IF bandwidth is enabled, False otherwise.
                        """
                        resp = self.instrument.query(":SENSe:ZS:CAPture:IFBWidth:AUTO?")
                        return int(resp.strip()) == 1

                    def set_sweep_time(self, value):
                        """
                        Parameter:
                            value (float): Sweep time in seconds.
                        Return:
                            None
                        """
                        self.instrument.write(f":SENSe:ZS:CAPture:SWEep:TIME {value}")

                    def get_sweep_time(self):
                        """
                        Parameter:
                            None
                        Return:
                            float: The sweep time in seconds.
                        """
                        return float(self.instrument.query(":SENSe:ZS:CAPture:SWEep:TIME?"))

                class Trigger:
                    def __init__(self, instrument):
                        self.instrument = instrument

                    def set_source(self, source):
                        """
                        Parameter:
                            source (str): 'IMMEDIATE', 'IF', 'EXTERNAL', or 'FMT'.
                        Return:
                            None
                        """
                        allowed = {"IMMEDIATE", "IF", "EXTERNAL", "FMT"}
                        if not isinstance(source, str) or source.upper() not in allowed:
                            raise ValueError("source must be one of 'IMMEDIATE', 'IF', 'EXTERNAL', or 'FMT'")
                        self.instrument.write(f":TRIGger:ZS:SOURce {source.upper()}")

                    def get_source(self):
                        """
                        Parameter:
                            None
                        Return:
                            str: The trigger type.
                        """
                        return self.instrument.query(":TRIGger:ZS:SOURce?")

                    def set_slope(self, slope):
                        """
                        Parameter:
                            slope (str): 'POSITIVE' or 'NEGATIVE'.
                        Return:
                            None
                        """
                        allowed = {"POSITIVE", "NEGATIVE"}
                        if not isinstance(slope, str) or slope.upper() not in allowed:
                            raise ValueError("slope must be 'POSITIVE' or 'NEGATIVE'")
                        self.instrument.write(f":TRIGger:ZS:SLOPe {slope.upper()}")

                    def get_slope(self):
                        """
                        Parameter:
                            None
                        Return:
                            str: The trigger edge.
                        """
                        return self.instrument.query(":TRIGger:ZS:SLOPe?")

                    def set_if_level(self, amplitude):
                        """
                        Parameter:
                            amplitude (float): Trigger level of the IF trigger.
                        Return:
                            None
                        """
                        self.instrument.write(f":TRIGger:ZS:IF:LEVel {amplitude}")

                    def get_if_level(self):
                        """
                        Parameter:
                            None
                        Return:
                            float: The trigger level of the IF trigger.
                        """
                        return float(self.instrument.query(":TRIGger:ZS:IF:LEVel?"))

                    def set_position(self, value):
                        """
                        Parameter:
                            value (float): Trigger delay as percent of samples before trigger.
                        Return:
                            None
                        """
                        self.instrument.write(f":TRIGger:ZS:POSition {value}")

                    def get_position(self):
                        """
                        Parameter:
                            None
                        Return:
                            float: The trigger delay as percent of samples before trigger.
                        """
                        return float(self.instrument.query(":TRIGger:ZS:POSition?"))

            class Fetch:
                """
                The Fetch commands are used to retrieve measurement results in zero-span mode.
                """
                def __init__(self, instrument):
                    self.instrument = instrument

                def get_zs(self, param):
                    """
                    Parameter:
                        param (int): 1 for I/Q data, 2 for length, 10 for average power.
                    Return:
                        str or float: I/Q data (str), length (int), or average power (float).
                    """
                    if param == 1:
                        return self.instrument.query(":FETCh:ZS? 1")
                    elif param == 2:
                        return int(self.instrument.query(":FETCh:ZS? 2"))
                    elif param == 10:
                        return float(self.instrument.query(":FETCh:ZS? 10"))
                    else:
                        raise ValueError("param must be 1 (I/Q data), 2 (length), or 10 (average power)")
                    
                    
           