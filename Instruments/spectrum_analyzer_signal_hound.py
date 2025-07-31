from Instruments import Instrument
import time
from EFileType import EFileType
from EInstrument import EInstrument
class SpectrumAnalyzer(Instrument.Instrument):
    def __init__(self, device):
       
       self.instrument = device
       self.name = EInstrument.SPECTRUM_ANALYZER
       self.display = SpectrumAnalyzer.Display(self.instrument, self.data_handler)
       self.format = SpectrumAnalyzer.Format(self.instrument, self.data_handler)
       self.system = SpectrumAnalyzer.System(self.instrument, self.data_handler)
       self.sense = SpectrumAnalyzer.Sense(self.instrument, self.data_handler)
       self.initiate = SpectrumAnalyzer.Initiate(self.instrument, self.data_handler)
       self.calculate = SpectrumAnalyzer.Calculate(self.instrument, self.data_handler)
       self.trace = SpectrumAnalyzer.Trace(self.instrument, self.data_handler)
       self.wlan = SpectrumAnalyzer.WLAN(self.instrument, self.data_handler)
       

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
        def __init__(self, instrument,data_handler):
            self.instrument = instrument
            self.data_handler = data_handler

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
        def __init__(self, instrument,data_handler):
            self.instrument = instrument
            self.data_handler = data_handler

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
        def __init__(self, instrument,data_handler):
            self.instrument = instrument
            self.data_handler = data_handler
            self.device = SpectrumAnalyzer.System.Device(self.instrument)
            self.error = SpectrumAnalyzer.System.Error(self.instrument)
            self.instrumentmode = SpectrumAnalyzer.System.InstrumentMode(self.instrument)

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
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler

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
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler

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
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler

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
        def __init__(self, instrument,data_handler):
            self.instrument = instrument
            self.data_handler = data_handler

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
        def __init__(self, instrument,data_handler):
            self.instrument = instrument
            self.data_handler = data_handler
            self.pnoise = SpectrumAnalyzer.Calculate.PNoise(self.instrument)
            self.marker = SpectrumAnalyzer.Calculate.Marker(self.instrument)
            self.math = SpectrumAnalyzer.Calculate.Math(self.instrument)
            self.limitline1 = SpectrumAnalyzer.Calculate.LimitLine(self.instrument,1)
            self.limitline2 = SpectrumAnalyzer.Calculate.LimitLine(self.instrument,2)
            self.limitline3 = SpectrumAnalyzer.Calculate.LimitLine(self.instrument,3)
            self.limitline4 = SpectrumAnalyzer.Calculate.LimitLine(self.instrument,4)
            self.limitline5 = SpectrumAnalyzer.Calculate.LimitLine(self.instrument,5)
            self.limitline6 = SpectrumAnalyzer.Calculate.LimitLine(self.instrument,6)
        class PNoise:
            """
            The PNoise commands control phase noise marker and jitter configuration.
            """
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler
                self.marker = SpectrumAnalyzer.Calculate.PNoise.Marker(self.instrument)
                self.jitter = SpectrumAnalyzer.Calculate.PNoise.Jitter(self.instrument)

            class Marker:
                """
                The Marker commands control the phase noise markers.
                """
                def __init__(self, instrument,data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler

                def select(self, marker_num):
                    """
                    Parameter:
                    marker_num (int): Marker index [1-6].
                    Return:
                    None
                    """
                    if not isinstance(marker_num, int) or not (1 <= marker_num <= 6):
                        raise ValueError("marker_num must be an integer between 1 and 6")
                    self.instrument.write(f":CALCulate:PNoise:MARKer:SELect {marker_num}")

                def get_selected(self):
                    """
                    Parameter:
                    None
                    Return:
                    int: The currently selected marker index.
                    """
                    return int(self.instrument.query(":CALCulate:PNoise:MARKer:SELect?"))

                def set_state(self, state):
                    """
                    Parameter:
                    state (int or str): 1/0 or 'ON'/'OFF' to enable/disable the marker.
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
                    self.instrument.write(f":CALCulate:PNoise:MARKer:STATe {state}")

                def is_enabled(self):
                    """
                    Parameter:
                    None
                    Return:
                    bool: True if marker is enabled, False otherwise.
                    """
                    resp = self.instrument.query(":CALCulate:PNoise:MARKer:STATe?")
                    return int(resp.strip()) == 1

                def set_trace(self, trace_num):
                    """
                    Parameter:
                    trace_num (int): Trace index [1-3].
                    Return:
                    None
                    """
                    if not isinstance(trace_num, int) or not (1 <= trace_num <= 3):
                        raise ValueError("trace_num must be an integer between 1 and 3")
                    self.instrument.write(f":CALCulate:PNoise:MARKer:TRACe {trace_num}")

                def get_trace(self):
                    """
                    Parameter:
                    None
                    Return:
                    int: The trace index the marker is placed on.
                    """
                    return int(self.instrument.query(":CALCulate:PNoise:MARKer:TRACe?"))

                def set_delta(self, state):
                    """
                    Parameter:
                    state (int or str): 1/0 or 'ON'/'OFF' to enable/disable delta marker.
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
                    self.instrument.write(f":CALCulate:PNoise:MARKer:DELTa {state}")

                def is_delta_enabled(self):
                    """
                    Parameter:
                    None
                    Return:
                    bool: True if delta marker is enabled, False otherwise.
                    """
                    resp = self.instrument.query(":CALCulate:PNoise:MARKer:DELTa?")
                    return int(resp.strip()) == 1

                def set_x(self, freq):
                    """
                    Parameter:
                    freq (float): Marker frequency offset from carrier (Hz).
                    Return:
                    None
                    """
                    self.instrument.write(f":CALCulate:PNoise:MARKer:X {freq}")

                def get_x(self):
                    """
                    Parameter:
                    None
                    Return:
                    float: The marker frequency offset from carrier (Hz).
                    """
                    return float(self.instrument.query(":CALCulate:PNoise:MARKer:X?"))

                def get_y(self):
                    """
                    Parameter:
                    None
                    Return:
                    float: The marker amplitude as dBc/Hz.
                    """
                    return float(self.instrument.query(":CALCulate:PNoise:MARKer:Y?"))

            class Jitter:
                """
                The Jitter commands control the jitter measurement configuration.
                """
                def __init__(self, instrument,data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler

                def set_state(self, state):
                    """
                    Parameter:
                    state (int or str): 1/0 or 'ON'/'OFF' to enable/disable jitter measurement.
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
                    self.instrument.write(f":CALCulate:PNoise:JITTer:STATe {state}")

                def is_enabled(self):
                    """
                    Parameter:
                    None
                    Return:
                    bool: True if jitter measurement is enabled, False otherwise.
                    """
                    resp = self.instrument.query(":CALCulate:PNoise:JITTer:STATe?")
                    return int(resp.strip()) == 1

                def set_trace(self, trace_num):
                    """
                    Parameter:
                    trace_num (int): Trace index [1-3].
                    Return:
                    None
                    """
                    if not isinstance(trace_num, int) or not (1 <= trace_num <= 3):
                        raise ValueError("trace_num must be an integer between 1 and 3")
                    self.instrument.write(f":CALCulate:PNoise:JITTer:TRACe {trace_num}")

                def get_trace(self):
                    """
                    Parameter:
                    None
                    Return:
                    int: The trace index used for jitter measurement.
                    """
                    return int(self.instrument.query(":CALCulate:PNoise:JITTer:TRACe?"))

                def set_start(self, freq):
                    """
                    Parameter:
                    freq (float): Start frequency offset from carrier (Hz).
                    Return:
                    None
                    """
                    self.instrument.write(f":CALCulate:PNoise:JITTer:STARt {freq}")

                def get_start(self):
                    """
                    Parameter:
                    None
                    Return:
                    float: Start frequency offset from carrier (Hz).
                    """
                    return float(self.instrument.query(":CALCulate:PNoise:JITTer:STARt?"))

                def set_stop(self, freq):
                    """
                    Parameter:
                    freq (float): Stop frequency offset from carrier (Hz).
                    Return:
                    None
                    """
                    self.instrument.write(f":CALCulate:PNoise:JITTer:STOP {freq}")

                def get_stop(self):
                    """
                    Parameter:
                    None
                    Return:
                    float: Stop frequency offset from carrier (Hz).
                    """
                    return float(self.instrument.query(":CALCulate:PNoise:JITTer:STOP?"))

                def get_rms(self):
                    """
                    Parameter:
                    None
                    Return:
                    float: RMS jitter in seconds.
                    """
                    return float(self.instrument.query(":CALCulate:PNoise:JITTer:RMS?"))

                def get_phase(self):
                    """
                    Parameter:
                    None
                    Return:
                    float: Phase jitter in radians.
                    """
                    return float(self.instrument.query(":CALCulate:PNoise:JITTer:PHASe?"))

        class Marker:
            """
            The Marker commands control the sweep markers.
            """
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler

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
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler

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
            def __init__(self, instrument,data_handler, line_num):
                self.instrument = instrument
                self.data_handler = data_handler
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
        def __init__(self, instrument,data_handler):
            self.instrument = instrument
            self.data_handler = data_handler
            self.harmonics = SpectrumAnalyzer.Sense.Harmonics(self.instrument)
            self.ademod = SpectrumAnalyzer.Sense.ADEMod(self.instrument)
            self.ddemod = SpectrumAnalyzer.Sense.DDEMod(self.instrument)
            self.sweep_configuration = SpectrumAnalyzer.Sense.Sweep_Configuration(self.instrument)
            self.na = SpectrumAnalyzer.Sense.NA(self.instrument)
            self.vco = SpectrumAnalyzer.Sense.VCO(self.instrument)
            self.audio = SpectrumAnalyzer.Sense.Audio(self.instrument)
            self.pnoise = SpectrumAnalyzer.Sense.PNoise(self.instrument)
            self.peaktable = SpectrumAnalyzer.Sense.PeakTable(self.instrument)
            self.chpower = SpectrumAnalyzer.Sense.ChPower(self.instrument)
            self.pathloss1 = SpectrumAnalyzer.Sense.Pathloss(self.instrument, 1)
            self.pathloss2 = SpectrumAnalyzer.Sense.Pathloss(self.instrument, 2)
            self.pathloss3 = SpectrumAnalyzer.Sense.Pathloss(self.instrument, 3)
            self.pathloss4 = SpectrumAnalyzer.Sense.Pathloss(self.instrument, 4)
            self.pathloss5 = SpectrumAnalyzer.Sense.Pathloss(self.instrument, 5)
            self.pathloss6 = SpectrumAnalyzer.Sense.Pathloss(self.instrument, 6)
            self.pathloss7 = SpectrumAnalyzer.Sense.Pathloss(self.instrument, 7)
            self.pathloss8 = SpectrumAnalyzer.Sense.Pathloss(self.instrument, 8)
            self.frequency = SpectrumAnalyzer.Sense.Frequency(self.instrument)
            self.power = SpectrumAnalyzer.Sense.Power(self.instrument)
            self.bandwidth = SpectrumAnalyzer.Sense.Bandwidth(self.instrument)
            self.sweep = SpectrumAnalyzer.Sense.Sweep(self.instrument)
            self.semask = SpectrumAnalyzer.Sense.SEMask(self.instrument)
            self.nfigure = SpectrumAnalyzer.Sense.NFIGure(self.instrument)
            self.bluetooth = SpectrumAnalyzer.Sense.Bluetooth(self.instrument)
            self.lte = SpectrumAnalyzer.Sense.LTE(self.instrument)
        class Harmonics:
            """
            The Sense:Harmonics commands configure harmonic measurements.
            """
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler

            def set_number(self, num):
                """
                Parameter:
                    num (int): Number of harmonics to measure and display.
                Return:
                    None
                """
                if not isinstance(num, int):
                    raise ValueError("num must be an integer")
                self.instrument.write(f":SENSe:HARMonics:NUMBer {num}")

            def get_number(self):
                """
                Parameter:
                    None
                Return:
                    int: Number of harmonics measured and displayed.
                """
                return int(self.instrument.query(":SENSe:HARMonics:NUMBer?"))

            def set_tracking_state(self, state):
                """
                Parameter:
                    state (int or str): 1/0 or 'ON'/'OFF' to enable/disable fundamental tracking.
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
                self.instrument.write(f":SENSe:HARMonics:TRACKing:STATe {state}")

            def is_tracking_enabled(self):
                """
                Parameter:
                    None
                Return:
                    bool: True if fundamental tracking is enabled, False otherwise.
                """
                resp = self.instrument.query(":SENSe:HARMonics:TRACKing:STATe?")
                return int(resp.strip()) == 1

            def set_mode(self, mode):
                """
                Parameter:
                    mode (str): 'PEAK' or 'CHPOWER'.
                Return:
                    None
                """
                allowed = {"PEAK", "CHPOWER"}
                if not isinstance(mode, str) or mode.upper() not in allowed:
                    raise ValueError("mode must be 'PEAK' or 'CHPOWER'")
                self.instrument.write(f":SENSe:HARMonics:MODE {mode.upper()}")

            def get_mode(self):
                """
                Parameter:
                    None
                Return:
                    str: The current harmonic measurement mode.
                """
                return self.instrument.query(":SENSe:HARMonics:MODE?")

            def set_fundamental(self, freq):
                """
                Parameter:
                    freq (float or str): Center frequency of the 1st harmonic (Hz), or 'UP', or 'DOWN'.
                Return:
                    None
                """
                if isinstance(freq, str):
                    if freq.upper() not in {"UP", "DOWN"}:
                        raise ValueError("freq must be a float or one of 'UP', 'DOWN'")
                    freq_str = freq.upper()
                else:
                    freq_str = str(freq)
                self.instrument.write(f":SENSe:HARMonics:FREQuency:FUNDamental {freq_str}")

            def get_fundamental(self):
                """
                Parameter:
                    None
                Return:
                    float: Center frequency of the 1st harmonic (Hz).
                """
                return float(self.instrument.query(":SENSe:HARMonics:FREQuency:FUNDamental?"))

            def set_step_increment(self, freq):
                """
                Parameter:
                    freq (float): Step frequency for fundamental (Hz).
                Return:
                    None
                """
                self.instrument.write(f":SENSe:HARMonics:FREQuency:STEP:INCRement {freq}")

            def get_step_increment(self):
                """
                Parameter:
                    None
                Return:
                    float: Step frequency for fundamental (Hz).
                """
                return float(self.instrument.query(":SENSe:HARMonics:FREQuency:STEP:INCRement?"))

            def set_span(self, freq):
                """
                Parameter:
                    freq (float): Span of each measurement window at each harmonic (Hz).
                Return:
                    None
                """
                self.instrument.write(f":SENSe:HARMonics:FREQuency:SPAN {freq}")

            def get_span(self):
                """
                Parameter:
                    None
                Return:
                    float: Span of each measurement window at each harmonic (Hz).
                """
                return float(self.instrument.query(":SENSe:HARMonics:FREQuency:SPAN?"))

            def set_bandwidth_resolution(self, freq):
                """
                Parameter:
                    freq (float): RBW at each harmonic (Hz).
                Return:
                    None
                """
                self.instrument.write(f":SENSe:HARMonics:BANDwidth:RESolution {freq}")

            def get_bandwidth_resolution(self):
                """
                Parameter:
                    None
                Return:
                    float: RBW at each harmonic (Hz).
                """
                return float(self.instrument.query(":SENSe:HARMonics:BANDwidth:RESolution?"))

            def set_bandwidth_video(self, freq):
                """
                Parameter:
                    freq (float): VBW at each harmonic (Hz).
                Return:
                    None
                """
                self.instrument.write(f":SENSe:HARMonics:BANDwidth:VIDeo {freq}")

            def get_bandwidth_video(self):
                """
                Parameter:
                    None
                Return:
                    float: VBW at each harmonic (Hz).
                """
                return float(self.instrument.query(":SENSe:HARMonics:BANDwidth:VIDeo?"))

            def set_power_rf_rlevel(self, value):
                """
                Parameter:
                    value (float): Measurement reference level as dBm.
                Return:
                    None
                """
                self.instrument.write(f":SENSe:HARMonics:POWer:RF:RLEVel {value}")

            def get_power_rf_rlevel(self):
                """
                Parameter:
                    None
                Return:
                    float: Measurement reference level as dBm.
                """
                return float(self.instrument.query(":SENSe:HARMonics:POWer:RF:RLEVel?"))

            def set_view_rlevel(self, value):
                """
                Parameter:
                    value (float): Plot reference level as dBm.
                Return:
                    None
                """
                self.instrument.write(f":SENSe:HARMonics:VIEW:RLEVel {value}")

            def get_view_rlevel(self):
                """
                Parameter:
                    None
                Return:
                    float: Plot reference level as dBm.
                """
                return float(self.instrument.query(":SENSe:HARMonics:VIEW:RLEVel?"))

            def set_view_pdivision(self, value):
                """
                Parameter:
                    value (float): Plot division height in dB.
                Return:
                    None
                """
                self.instrument.write(f":SENSe:HARMonics:VIEW:PDIVision {value}")

            def get_view_pdivision(self):
                """
                Parameter:
                    None
                Return:
                    float: Plot division height in dB.
                """
                return float(self.instrument.query(":SENSe:HARMonics:VIEW:PDIVision?"))

            def set_trace_type(self, typ):
                """
                Parameter:
                    typ (str): 'WRITE' or 'MAXHOLD'.
                Return:
                    None
                """
                allowed = {"WRITE", "MAXHOLD"}
                if not isinstance(typ, str) or typ.upper() not in allowed:
                    raise ValueError("typ must be 'WRITE' or 'MAXHOLD'")
                self.instrument.write(f":SENSe:HARMonics:TRACe:TYPE {typ.upper()}")

            def get_trace_type(self):
                """
                Parameter:
                    None
                Return:
                    str: The trace behavior type.
                """
                return self.instrument.query(":SENSe:HARMonics:TRACe:TYPE?")
            def fetch_frequency(self, harmonic_num):
                """
                Parameter:
                    harmonic_num (int): The harmonic number to fetch frequency for.
                Return:
                    float: The specified harmonic's peak frequency in Hz.
                """
                if not isinstance(harmonic_num, int) or harmonic_num < 1:
                    raise ValueError("harmonic_num must be a positive integer")
                return float(self.instrument.query(f":SENSe:FETCh:HARMonics:FREQuency? {harmonic_num}"))

            def fetch_amplitude(self, harmonic_num):
                """
                Parameter:
                    harmonic_num (int): The harmonic number to fetch amplitude for.
                Return:
                    float: The specified harmonic's amplitude in dBm.
                """
                if not isinstance(harmonic_num, int) or harmonic_num < 1:
                    raise ValueError("harmonic_num must be a positive integer")
                return float(self.instrument.query(f":SENSe:FETCh:HARMonics:AMPLitude? {harmonic_num}"))

            def fetch_distortion(self):
                """
                Parameter:
                    None
                Return:
                    float: The measured total harmonic distortion in percent.
                """
                return float(self.instrument.query(":SENSe:FETCh:HARMonics:DISTortion?"))
        class ADEMod:
            """
            The Sense:ADEMod commands configure analog demodulation measurements.
            """
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler
                self.fetch = SpectrumAnalyzer.Sense.ADEMod.Fetch(self.instrument)
            def set_center_frequency(self, freq):
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
                self.instrument.write(f":SENSe:ADEMod:FREQuency:CENTer {freq_str}")

            def get_center_frequency(self):
                """
                Parameter:
                    None
                Return:
                    float: The measurement center frequency in Hz.
                """
                return float(self.instrument.query(":SENSe:ADEMod:FREQuency:CENTer?"))

            def set_center_step(self, freq):
                """
                Parameter:
                    freq (float): Step amount for center frequency changes in Hz.
                Return:
                    None
                """
                self.instrument.write(f":SENSe:ADEMod:FREQuency:CENTer:STEP {freq}")

            def get_center_step(self):
                """
                Parameter:
                    None
                Return:
                    float: The center frequency step size in Hz.
                """
                return float(self.instrument.query(":SENSe:ADEMod:FREQuency:CENTer:STEP?"))

            def set_reference_level(self, amplitude):
                """
                Parameter:
                    amplitude (float): Reference level in dBm.
                Return:
                    None
                """
                self.instrument.write(f":SENSe:ADEMod:POWer:RF:RLEVel {amplitude}")

            def get_reference_level(self):
                """
                Parameter:
                    None
                Return:
                    float: The measurement reference level in dBm.
                """
                return float(self.instrument.query(":SENSe:ADEMod:POWer:RF:RLEVel?"))

            def set_lpfilter(self, freq):
                """
                Parameter:
                    freq (float): Analog low pass filter cutoff frequency in Hz.
                Return:
                    None
                """
                self.instrument.write(f":SENSe:ADEMod:LPFilter {freq}")

            def get_lpfilter(self):
                """
                Parameter:
                    None
                Return:
                    float: The analog low pass filter cutoff frequency in Hz.
                """
                return float(self.instrument.query(":SENSe:ADEMod:LPFilter?"))

            class Fetch:
                """
                The Fetch commands retrieve analog demodulation measurement results.
                """
                def __init__(self, instrument,data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler

                def fetch_am(self, metrics):
                    """
                    Parameter:
                    metrics (int or list of int): Metric(s) to retrieve for AM demodulation.
                    Return:
                    str: Comma separated list of metric values in order requested.
                    """
                    if isinstance(metrics, int):
                        metrics_str = str(metrics)
                    elif isinstance(metrics, (list, tuple)) and all(isinstance(m, int) for m in metrics):
                        metrics_str = ",".join(str(m) for m in metrics)
                    else:
                        raise ValueError("metrics must be an int or list/tuple of ints")
                    response = self.instrument.query(f":FETCh:ADEMod:AM? {metrics_str}")
                    if self.data_handler.is_auto_saving_data_enabled():
                        self.data_handler.write_to_file(self, "ADEMod_AM", response, file_type = EFileType.CSV, headers = metrics_str)
                    return response

                def fetch_fm(self, metrics):
                    """
                    Parameter:
                    metrics (int or list of int): Metric(s) to retrieve for FM demodulation.
                    Return:
                    str: Comma separated list of metric values in order requested.
                    """
                    if isinstance(metrics, int):
                        metrics_str = str(metrics)
                    elif isinstance(metrics, (list, tuple)) and all(isinstance(m, int) for m in metrics):
                        metrics_str = ",".join(str(m) for m in metrics)
                    else:
                        raise ValueError("metrics must be an int or list/tuple of ints")
                    response = self.instrument.query(f":FETCh:ADEMod:FM? {metrics_str}")
                    if self.data_handler.is_auto_saving_data_enabled():
                        self.data_handler.write_to_file(self, "ADEMod_FM", response, file_type = EFileType.CSV, headers = metrics_str)
                    return response
        class DDEMod:
            """
            The Sense:DDEMod commands configure digital demodulation measurements.
            """
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler
                self.custom = SpectrumAnalyzer.Sense.DDEMod.Custom(self.instrument)
                self.trigger = SpectrumAnalyzer.Sense.DDEMod.Trigger(self.instrument)
                self.sync = SpectrumAnalyzer.Sense.DDEMod.Sync(self.instrument)
                self.compensate = SpectrumAnalyzer.Sense.DDEMod.Compensate(self.instrument)
                self.equalization = SpectrumAnalyzer.Sense.DDEMod.Equalization(self.instrument)
                self.trace = SpectrumAnalyzer.Sense.DDEMod.Trace(self.instrument)
                self.fetch = SpectrumAnalyzer.Sense.DDEMod.Fetch(self.instrument)
            def set_center_frequency(self, freq):
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
                self.instrument.write(f":SENSe:DDEMod:FREQuency:CENTer {freq_str}")

            def get_center_frequency(self):
                """
                Parameter:
                    None
                Return:
                    float: The measurement center frequency in Hz.
                """
                return float(self.instrument.query(":SENSe:DDEMod:FREQuency:CENTer?"))

            def set_center_step(self, freq):
                """
                Parameter:
                    freq (float): Step amount for center frequency changes in Hz.
                Return:
                    None
                """
                self.instrument.write(f":SENSe:DDEMod:FREQuency:CENTer:STEP {freq}")

            def get_center_step(self):
                """
                Parameter:
                    None
                Return:
                    float: The center frequency step size in Hz.
                """
                return float(self.instrument.query(":SENSe:DDEMod:FREQuency:CENTer:STEP?"))

            def set_reference_level(self, amplitude):
                """
                Parameter:
                    amplitude (float): Reference level in dBm.
                Return:
                    None
                """
                self.instrument.write(f":SENSe:DDEMod:POWer:RF:RLEVel {amplitude}")

            def get_reference_level(self):
                """
                Parameter:
                    None
                Return:
                    float: The measurement reference level in dBm.
                """
                return float(self.instrument.query(":SENSe:DDEMod:POWer:RF:RLEVel?"))

            def set_srate(self, freq):
                """
                Parameter:
                    freq (float): Symbol rate in Hz.
                Return:
                    None
                """
                self.instrument.write(f":SENSe:DDEMod:SRATe {freq}")

            def get_srate(self):
                """
                Parameter:
                    None
                Return:
                    float: The symbol rate in Hz.
                """
                return float(self.instrument.query(":SENSe:DDEMod:SRATe?"))

            def set_modulation(self, mod):
                """
                Parameter:
                    mod (str): Modulation type.
                Return:
                    None
                """
                allowed = {
                    "BPSK", "DBPSK", "QPSK", "DQPSK", "OQPSK", "PI4QPSK", "8PSK", "D8PSK",
                    "QAM16", "QAM32", "QAM64", "QAM256", "QAM1024", "FSK2", "FSK4", "FSK8",
                    "FSK16", "ASK2", "CUSTOM"
                }
                if not isinstance(mod, str) or mod.upper() not in allowed:
                    raise ValueError("mod must be a valid modulation type")
                self.instrument.write(f":SENSe:DDEMod:MODulation {mod.upper()}")

            def get_modulation(self):
                """
                Parameter:
                    None
                Return:
                    str: The current modulation type.
                """
                return self.instrument.query(":SENSe:DDEMod:MODulation?")

            def set_rlength(self, value):
                """
                Parameter:
                    value (int): Result length.
                Return:
                    None
                """
                if not isinstance(value, int):
                    raise ValueError("value must be an integer")
                self.instrument.write(f":SENSe:DDEMod:RLENgth {value}")

            def get_rlength(self):
                """
                Parameter:
                    None
                Return:
                    int: The result length.
                """
                return int(self.instrument.query(":SENSe:DDEMod:RLENgth?"))

            def set_filter(self, filt):
                """
                Parameter:
                    filt (str): Filter type ('NYQUIST', 'RNYQUIST', 'GAUSSIAN', 'RECTANGLE').
                Return:
                    None
                """
                allowed = {"NYQUIST", "RNYQUIST", "GAUSSIAN", "RECTANGLE"}
                if not isinstance(filt, str) or filt.upper() not in allowed:
                    raise ValueError("filt must be one of 'NYQUIST', 'RNYQUIST', 'GAUSSIAN', or 'RECTANGLE'")
                self.instrument.write(f":SENSe:DDEMod:FILTer {filt.upper()}")

            def get_filter(self):
                """
                Parameter:
                    None
                Return:
                    str: The current filter type.
                """
                return self.instrument.query(":SENSe:DDEMod:FILTer?")

            def set_filter_abt(self, value):
                """
                Parameter:
                    value (float): Filter alpha/beta/BT value.
                Return:
                    None
                """
                self.instrument.write(f":SENSe:DDEMod:FILTer:ABT {value}")

            def get_filter_abt(self):
                """
                Parameter:
                    None
                Return:
                    float: The filter alpha/beta/BT value.
                """
                return float(self.instrument.query(":SENSe:DDEMod:FILTer:ABT?"))
            def set_ifbwidth_auto(self, state):
                """
                Parameter:
                    state (int or str): 1/0 or 'ON'/'OFF' to enable/disable automatic IF bandwidth selection.
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
                self.instrument.write(f":SENSe:DDEMod:IFBWidth:AUTO {state}")

            def is_ifbwidth_auto(self):
                """
                Parameter:
                    None
                Return:
                    bool: True if automatic IF bandwidth is enabled, False otherwise.
                """
                resp = self.instrument.query(":SENSe:DDEMod:IFBWidth:AUTO?")
                return int(resp.strip()) == 1

            def set_ifbwidth(self, freq):
                """
                Parameter:
                    freq (float): IF bandwidth in Hz.
                Return:
                    None
                """
                self.instrument.write(f":SENSe:DDEMod:IFBWidth {freq}")

            def get_ifbwidth(self):
                """
                Parameter:
                    None
                Return:
                    float: The IF bandwidth in Hz.
                """
                return float(self.instrument.query(":SENSe:DDEMod:IFBWidth?"))

            def set_average_state(self, state):
                """
                Parameter:
                    state (int or str): 1/0 or 'ON'/'OFF' to enable/disable measurement averaging.
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
                self.instrument.write(f":SENSe:DDEMod:AVERage:STATe {state}")

            def is_average_enabled(self):
                """
                Parameter:
                    None
                Return:
                    bool: True if measurement averaging is enabled, False otherwise.
                """
                resp = self.instrument.query(":SENSe:DDEMod:AVERage:STATe?")
                return int(resp.strip()) == 1

            def set_average_count(self, count):
                """
                Parameter:
                    count (int): Number of averages.
                Return:
                    None
                """
                if not isinstance(count, int):
                    raise ValueError("count must be an integer")
                self.instrument.write(f":SENSe:DDEMod:AVERage:COUNt {count}")

            def get_average_count(self):
                """
                Parameter:
                    None
                Return:
                    int: The number of averages.
                """
                return int(self.instrument.query(":SENSe:DDEMod:AVERage:COUNt?"))

            def set_wce_state(self, state):
                """
                Parameter:
                    state (int or str): 1/0 or 'ON'/'OFF' to enable/disable wide carrier estimation.
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
                self.instrument.write(f":SENSe:DDEMod:WCE:STATe {state}")

            def is_wce_enabled(self):
                """
                Parameter:
                    None
                Return:
                    bool: True if wide carrier estimation is enabled, False otherwise.
                """
                resp = self.instrument.query(":SENSe:DDEMod:WCE:STATe?")
                return int(resp.strip()) == 1

            def set_wce_range(self, freq):
                """
                Parameter:
                    freq (float): Wide carrier estimation range in Hz.
                Return:
                    None
                """
                self.instrument.write(f":SENSe:DDEMod:WCE:RANge {freq}")

            def get_wce_range(self):
                """
                Parameter:
                    None
                Return:
                    float: The wide carrier estimation range in Hz.
                """
                return float(self.instrument.query(":SENSe:DDEMod:WCE:RANge?"))
            class Custom:
                """
                The Custom commands configure custom IQ constellations for digital demodulation.
                """
                def __init__(self, instrument,data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler
                    self.iq = SpectrumAnalyzer.Sense.DDEMod.Custom.IQ(self.instrument)

                class IQ:
                    """
                    The IQ commands configure and query custom IQ constellation data.
                    """
                    def __init__(self, instrument,data_handler):
                        self.instrument = instrument
                        self.data_handler = data_handler

                    def is_valid(self):
                        """
                        Parameter:
                            None
                        Return:
                            bool: True if the custom constellation is valid, False otherwise.
                        """
                        resp = self.instrument.query(":SENSe:DDEMod:CUSTom:IQ:VALid?")
                        return int(resp.strip()) == 1

                    def get_length(self):
                        """
                        Parameter:
                            None
                        Return:
                            int: The number of symbols in the custom constellation.
                        """
                        return int(self.instrument.query(":SENSe:DDEMod:CUSTom:IQ:LENGth?"))

                    def set_data(self, iq_values):
                        """
                        Parameter:
                            iq_values (list or tuple): List of real numbers, alternating I/Q values.
                        Return:
                            None
                        """
                        if not isinstance(iq_values, (list, tuple)) or not all(isinstance(x, (int, float)) for x in iq_values):
                            raise ValueError("iq_values must be a list or tuple of real numbers")
                        data_str = ",".join(str(x) for x in iq_values)
                        self.instrument.write(f":SENSe:DDEMod:CUSTom:IQ:DATA {data_str}")

                    def get_data(self):
                        """
                        Parameter:
                            None
                        Return:
                            str: The constellation symbols as a comma separated list of alternating IQ values.
                        """
                        response = self.instrument.query(":SENSe:DDEMod:CUSTom:IQ:DATA?")
                        if self.data_handler.is_auto_saving_data_enabled():
                            self.data_handler.write_to_file(self, "DDEMOD_IQ", response, file_type = EFileType.CSV, headers = None)
                        return response
            class Trigger:
                """
                The DDEMod:Trigger commands configure triggering for digital demodulation.
                """
                def __init__(self, instrument,data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler

                def set_source(self, source):
                    """
                    Parameter:
                        source (str): 'IMMEDIATE', 'IF', or 'EXTERNAL'
                    Return:
                        None
                    """
                    allowed = {"IMMEDIATE", "IF", "EXTERNAL"}
                    if not isinstance(source, str) or source.upper() not in allowed:
                        raise ValueError("source must be one of 'IMMEDIATE', 'IF', or 'EXTERNAL'")
                    self.instrument.write(f":TRIGger:DDEMod:SOURce {source.upper()}")

                def get_source(self):
                    """
                    Parameter:
                        None
                    Return:
                        str: The trigger type.
                    """
                    return self.instrument.query(":TRIGger:DDEMod:SOURce?")

                def set_if_level(self, amplitude):
                    """
                    Parameter:
                        amplitude (float): Trigger level of the IF trigger.
                    Return:
                        None
                    """
                    self.instrument.write(f":TRIGger:DDEMod:IF:LEVel {amplitude}")

                def get_if_level(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: The trigger level of the IF trigger.
                    """
                    return float(self.instrument.query(":TRIGger:DDEMod:IF:LEVel?"))

                def set_delay(self, value):
                    """
                    Parameter:
                        value (int): Trigger delay (number of symbols after trigger to start measurement).
                    Return:
                        None
                    """
                    if not isinstance(value, int):
                        raise ValueError("value must be an integer")
                    self.instrument.write(f":TRIGger:DDEMod:DELay {value}")

                def get_delay(self):
                    """
                    Parameter:
                        None
                    Return:
                        int: The trigger delay (number of symbols after trigger).
                    """
                    return int(self.instrument.query(":TRIGger:DDEMod:DELay?"))

            class Sync:
                """
                The DDEMod:Sync commands configure sync pattern search for digital demodulation.
                """
                def __init__(self, instrument,data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler
                    self.sword = SpectrumAnalyzer.Sense.DDEMod.Sync.Sword(self.instrument)
                def set_state(self, state):
                    """
                    Parameter:
                        state (int or str): 1/0 or 'ON'/'OFF' to enable/disable sync search.
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
                    self.instrument.write(f":SENSe:DDEMod:SYNC:STATe {state}")

                def is_enabled(self):
                    """
                    Parameter:
                        None
                    Return:
                        bool: True if sync search is enabled, False otherwise.
                    """
                    resp = self.instrument.query(":SENSe:DDEMod:SYNC:STATe?")
                    return int(resp.strip()) == 1

                class Sword:
                    """
                    The SWord commands configure the sync pattern and length.
                    """
                    def __init__(self, instrument,data_handler):
                        self.instrument = instrument
                        self.data_handler = data_handler

                    def set_pattern(self, hex_string):
                        """
                        Parameter:
                            hex_string (str): The pattern to trigger on (hex string).
                        Return:
                            None
                        """
                        if not isinstance(hex_string, str):
                            raise ValueError("hex_string must be a string")
                        self.instrument.write(f":SENSe:DDEMod:SYNC:SWORd:PATTern {hex_string}")

                    def get_pattern(self):
                        """
                        Parameter:
                            None
                        Return:
                            str: The current sync pattern (hex string).
                        """
                        return self.instrument.query(":SENSe:DDEMod:SYNC:SWORd:PATTern?")

                    def set_length(self, value):
                        """
                        Parameter:
                            value (int): The length in symbols of the pattern trigger.
                        Return:
                            None
                        """
                        if not isinstance(value, int):
                            raise ValueError("value must be an integer")
                        self.instrument.write(f":SENSe:DDEMod:SYNC:SWORd:LENGth {value}")

                    def get_length(self):
                        """
                        Parameter:
                            None
                        Return:
                            int: The length in symbols of the pattern trigger.
                        """
                        return int(self.instrument.query(":SENSe:DDEMod:SYNC:SWORd:LENGth?"))

                def set_slength(self, value):
                    """
                    Parameter:
                        value (int): Search length for the pattern trigger.
                    Return:
                        None
                    """
                    if not isinstance(value, int):
                        raise ValueError("value must be an integer")
                    self.instrument.write(f":SENSe:DDEMod:SYNC:SLENgth {value}")

                def get_slength(self):
                    """
                    Parameter:
                        None
                    Return:
                        int: Search length for the pattern trigger.
                    """
                    return int(self.instrument.query(":SENSe:DDEMod:SYNC:SLENgth?"))

                def set_offset(self, value):
                    """
                    Parameter:
                        value (int): Offset from the beginning of a successful sync search (can be negative).
                    Return:
                        None
                    """
                    if not isinstance(value, int):
                        raise ValueError("value must be an integer")
                    self.instrument.write(f":SENSe:DDEMod:SYNC:OFFSet {value}")

                def get_offset(self):
                    """
                    Parameter:
                        None
                    Return:
                        int: Offset from the beginning of a successful sync search.
                    """
                    return int(self.instrument.query(":SENSe:DDEMod:SYNC:OFFSet?"))

            class Compensate:
                """
                The DDEMod:Compensate commands configure compensation settings for digital demodulation.
                """
                def __init__(self, instrument,data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler

                def set_iqinversion_state(self, state):
                    """
                    Parameter:
                        state (int or str): 1/0 or 'ON'/'OFF' to enable/disable IQ swap.
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
                    self.instrument.write(f":SENSe:DDEMod:COMPensate:IQINVersion:STATe {state}")

                def is_iqinversion_enabled(self):
                    """
                    Parameter:
                        None
                    Return:
                        bool: True if IQ swap is enabled, False otherwise.
                    """
                    resp = self.instrument.query(":SENSe:DDEMod:COMPensate:IQINVersion:STATe?")
                    return int(resp.strip()) == 1

                def set_iqoffset_state(self, state):
                    """
                    Parameter:
                        state (int or str): 1/0 or 'ON'/'OFF' to enable/disable IQ offset removal.
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
                    self.instrument.write(f":SENSe:DDEMod:COMPensate:IQOFFset:STATe {state}")

                def is_iqoffset_enabled(self):
                    """
                    Parameter:
                        None
                    Return:
                        bool: True if IQ offset removal is enabled, False otherwise.
                    """
                    resp = self.instrument.query(":SENSe:DDEMod:COMPensate:IQOFFset:STATe?")
                    return int(resp.strip()) == 1

                def set_adroop_state(self, state):
                    """
                    Parameter:
                        state (int or str): 1/0 or 'ON'/'OFF' to enable/disable amplitude droop compensation.
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
                    self.instrument.write(f":SENSe:DDEMod:COMPensate:ADRoop:STATe {state}")

                def is_adroop_enabled(self):
                    """
                    Parameter:
                        None
                    Return:
                        bool: True if amplitude droop compensation is enabled, False otherwise.
                    """
                    resp = self.instrument.query(":SENSe:DDEMod:COMPensate:ADRoop:STATe?")
                    return int(resp.strip()) == 1

            class Equalization:
                """
                The DDEMod:Equalization commands configure adaptive equalizer settings.
                """
                def __init__(self, instrument,data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler

                def set_state(self, state):
                    """
                    Parameter:
                        state (int or str): 1/0 or 'ON'/'OFF' to enable/disable equalization.
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
                    self.instrument.write(f":SENSe:DDEMod:EQUalization:STATe {state}")

                def is_enabled(self):
                    """
                    Parameter:
                        None
                    Return:
                        bool: True if equalization is enabled, False otherwise.
                    """
                    resp = self.instrument.query(":SENSe:DDEMod:EQUalization:STATe?")
                    return int(resp.strip()) == 1

                def set_length(self, value):
                    """
                    Parameter:
                        value (int): Length of the equalization filter in symbols (must be odd).
                    Return:
                        None
                    """
                    if not isinstance(value, int) or value % 2 != 1:
                        raise ValueError("value must be an odd integer")
                    self.instrument.write(f":SENSe:DDEMod:EQUalization:LENGth {value}")

                def get_length(self):
                    """
                    Parameter:
                        None
                    Return:
                        int: Length of the equalization filter in symbols.
                    """
                    return int(self.instrument.query(":SENSe:DDEMod:EQUalization:LENGth?"))

                def set_convergence(self, value):
                    """
                    Parameter:
                        value (float): Adaptive rate (convergence).
                    Return:
                        None
                    """
                    self.instrument.write(f":SENSe:DDEMod:EQUalization:CONVergence {value}")

                def get_convergence(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: Adaptive rate (convergence).
                    """
                    return float(self.instrument.query(":SENSe:DDEMod:EQUalization:CONVergence?"))

                def set_hold_state(self, state):
                    """
                    Parameter:
                        state (int or str): 1/0 or 'ON'/'OFF' to enable/disable hold (bypass adaptation).
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
                    self.instrument.write(f":SENSe:DDEMod:EQUalization:HOLD:STATe {state}")

                def is_hold_enabled(self):
                    """
                    Parameter:
                        None
                    Return:
                        bool: True if hold is enabled, False otherwise.
                    """
                    resp = self.instrument.query(":SENSe:DDEMod:EQUalization:HOLD:STATe?")
                    return int(resp.strip()) == 1

                def reset(self):
                    """
                    Parameter:
                        None
                    Return:
                        None
                    """
                    self.instrument.write(":SENSe:DDEMod:EQUalization:RESet")

            class Trace:
                """
                The DDEMod:Trace commands retrieve spectrum data from digital demodulation measurement mode.
                """
                def __init__(self, instrument,data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler
                    self.sweep = SpectrumAnalyzer.Sense.DDEMod.Trace.Sweep(self.instrument)
                class Sweep:
                    """
                    The DDEMod:Trace:Sweep commands retrieve sweep data.
                    """
                    def __init__(self, instrument,data_handler):
                        self.instrument = instrument
                        self.data_handler = data_handler

                    def get_xstart(self):
                        """
                        Parameter:
                            None
                        Return:
                            float: Frequency value associated with the first sample in the returned data.
                        """
                        return float(self.instrument.query(":SENSe:DDEMod:TRACe:SWEep:XSTARt?"))

                    def get_xincrement(self):
                        """
                        Parameter:
                            None
                        Return:
                            float: Frequency spacing for the samples in the returned data.
                        """
                        return float(self.instrument.query(":SENSe:DDEMod:TRACe:SWEep:XINCrement?"))

                    def get_points(self):
                        """
                        Parameter:
                            None
                        Return:
                            int: Number of points returned by the DATA function.
                        """
                        return int(self.instrument.query(":SENSe:DDEMod:TRACe:SWEep:POINts?"))

                    def get_data(self):
                        """
                        Parameter:
                            None
                        Return:
                            str: The spectrum trace as a comma separated list.
                        """
                        response = self.instrument.query(":SENSe:DDEMod:TRACe:SWEep:DATA?")
                        if self.data_handler.is_auto_saving_data_enabled():
                            self.data_handler.write_to_file(self, "TRACE_SWEEP", response, file_type = EFileType.CSV, headers = None)
                        return response

            class Fetch:
                """
                The DDEMod:Fetch commands retrieve measurement results for digital demodulation.
                """
                def __init__(self, instrument,data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler

                def fetch(self, metrics):
                    """
                    Parameter:
                        metrics (int or list/tuple of int): Metric(s) to retrieve.
                    Return:
                        str: Comma separated list of metric values in order requested.
                    """
                    if isinstance(metrics, int):
                        metrics_str = str(metrics)
                    elif isinstance(metrics, (list, tuple)) and all(isinstance(m, int) for m in metrics):
                        metrics_str = ",".join(str(m) for m in metrics)
                    else:
                        raise ValueError("metrics must be an int or list/tuple of ints")
                    response = self.instrument.query(f":FETCh:DDEMod? {metrics_str}")
                    if self.data_handler.is_auto_saving_data_enabled():
                        self.data_handler.write_to_file(self, "DDEMOD_METRICS", response, file_type = EFileType.CSV, headers = None)
                    return response
        class Sweep_Configuration:
            """
            The Sweep Configuration commands control the sweep configuration in scalar network analysis mode.
            """
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler

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
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler
                self.view = SpectrumAnalyzer.Sense.NA.View(self.instrument)
                self.correction = SpectrumAnalyzer.Sense.NA.Correction(self.instrument)
            
            class View():
                """View commands control the view settings in scalar network analysis mode."""
                def __init__(self, instrument,data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler

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
                The Correction commands control the correction settings in scalar network analysis mode.
                """
                def __init__(self, instrument,data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler

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
        class VCO:
            """
            The VCO commands control the configuration of the measurement in VCO Characterization mode.
            """
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler
                self.sweep = SpectrumAnalyzer.Sense.VCO.Sweep(self.instrument)
                self.source = SpectrumAnalyzer.Sense.VCO.Source(self.instrument)
            class Sweep:
                """
                The Sweep commands control the sweep configuration in VCO Characterization mode.
                """
                def __init__(self, instrument,data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler

                def get_source(self):
                    """
                    Parameter:
                        None
                    Return:
                        str: The sweep source.
                    """
                    return self.instrument.query(":SENSe:VCO:SWEep:SOURce?")

                def set_start(self, value):
                    """
                    Parameter:
                        value (float): Starting voltage for the sweep in volts.
                    Return:
                        None
                    """
                    self.instrument.write(f":SENSe:VCO:SWEep:STARt {value}")

                def get_start(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: Starting voltage for the sweep in volts.
                    """
                    return float(self.instrument.query(":SENSe:VCO:SWEep:STARt?"))

                def set_stop(self, value):
                    """
                    Parameter:
                        value (float): Stopping voltage for the sweep in volts.
                    Return:
                        None
                    """
                    self.instrument.write(f":SENSe:VCO:SWEep:STOP {value}")

                def get_stop(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: Stopping voltage for the sweep in volts.
                    """
                    return float(self.instrument.query(":SENSe:VCO:SWEep:STOP?"))

                def set_points(self, num_points):
                    """
                    Parameter:
                        num_points (int): Number of points to measure.
                    Return:
                        None
                    """
                    if not isinstance(num_points, int):
                        raise ValueError("num_points must be an integer")
                    self.instrument.write(f":SENSe:VCO:SWEep:POINts {num_points}")

                def get_points(self):
                    """
                    Parameter:
                        None
                    Return:
                        int: Number of points to measure.
                    """
                    return int(self.instrument.query(":SENSe:VCO:SWEep:POINts?"))

                def set_rf_rlevel(self, value):
                    """
                    Parameter:
                        value (float): Reference level as dBm.
                    Return:
                        None
                    """
                    self.instrument.write(f":SENSe:VCO:SWEep:RF:RLEVel {value}")

                def get_rf_rlevel(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: Reference level as dBm.
                    """
                    return float(self.instrument.query(":SENSe:VCO:SWEep:RF:RLEVel?"))

                def set_band_auto(self, state):
                    """
                    Parameter:
                        state (int or str): 1/0 or 'ON'/'OFF' to enable/disable automatic frequency band search.
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
                    self.instrument.write(f":SENSe:VCO:SWEep:FREQuency:BAND:AUTO {state}")

                def is_band_auto(self):
                    """
                    Parameter:
                        None
                    Return:
                        bool: True if automatic frequency band search is enabled, False otherwise.
                    """
                    resp = self.instrument.query(":SENSe:VCO:SWEep:FREQuency:BAND:AUTO?")
                    return int(resp.strip()) == 1

                def set_band_start(self, freq):
                    """
                    Parameter:
                        freq (float): Start frequency of the search range.
                    Return:
                        None
                    """
                    self.instrument.write(f":SENSe:VCO:SWEep:FREQuency:BAND:STARt {freq}")

                def get_band_start(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: Start frequency of the search range.
                    """
                    return float(self.instrument.query(":SENSe:VCO:SWEep:FREQuency:BAND:STARt?"))

                def set_band_stop(self, freq):
                    """
                    Parameter:
                        freq (float): Stop frequency of the search range.
                    Return:
                        None
                    """
                    self.instrument.write(f":SENSe:VCO:SWEep:FREQuency:BAND:STOP {freq}")

                def get_band_stop(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: Stop frequency of the search range.
                    """
                    return float(self.instrument.query(":SENSe:VCO:SWEep:FREQuency:BAND:STOP?"))

                def set_fcounter_resolution(self, freq):
                    """
                    Parameter:
                        freq (float): Frequency resolution of each measurement (RBW).
                    Return:
                        None
                    """
                    self.instrument.write(f":SENSe:VCO:SWEep:FCOunter:RESolution {freq}")

                def get_fcounter_resolution(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: Frequency resolution of each measurement (RBW).
                    """
                    return float(self.instrument.query(":SENSe:VCO:SWEep:FCOunter:RESolution?"))

                def set_chpower_width(self, freq):
                    """
                    Parameter:
                        freq (float): Width of the channel for power and harmonics measurements.
                    Return:
                        None
                    """
                    self.instrument.write(f":SENSe:VCO:SWEep:CHPower:WIDth {freq}")

                def get_chpower_width(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: Width of the channel for power and harmonics measurements.
                    """
                    return float(self.instrument.query(":SENSe:VCO:SWEep:CHPower:WIDth?"))

                def set_delay(self, value):
                    """
                    Parameter:
                        value (float): Dwell time for each measurement (pause between setting voltage and measuring).
                    Return:
                        None
                    """
                    self.instrument.write(f":SENSe:VCO:SWEep:DELay {value}")

                def get_delay(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: Dwell time for each measurement.
                    """
                    return float(self.instrument.query(":SENSe:VCO:SWEep:DELay?"))

            class Source:
                """
                The Source commands control the DC source configuration in VCO Characterization mode.
                """
                def __init__(self, instrument,data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler

                def set_voltage_state(self, state):
                    """
                    Parameter:
                        state (int or str): 1/0 or 'ON'/'OFF' to enable/disable overall DC power.
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
                    self.instrument.write(f":SENSe:VCO:SOURce:VOLTage:STATe {state}")

                def is_voltage_enabled(self):
                    """
                    Parameter:
                        None
                    Return:
                        bool: True if DC power is enabled, False otherwise.
                    """
                    resp = self.instrument.query(":SENSe:VCO:SOURce:VOLTage:STATe?")
                    return int(resp.strip()) == 1

                def set_fixed_level(self, value):
                    """
                    Parameter:
                        value (float): Output level of the fixed power source in volts.
                    Return:
                        None
                    """
                    self.instrument.write(f":SENSe:VCO:SOURce:VOLTage:FIXed:LEVel {value}")

                def get_fixed_level(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: Output level of the fixed power source in volts.
                    """
                    return float(self.instrument.query(":SENSe:VCO:SOURce:VOLTage:FIXed:LEVel?"))

                def set_vtune_limit_low(self, value):
                    """
                    Parameter:
                        value (float): Minimum output level of the V Tune port in volts.
                    Return:
                        None
                    """
                    self.instrument.write(f":SENSe:VCO:SOURce:VOLTage:VTUNe:LEVel:LIMit:LOW {value}")

                def get_vtune_limit_low(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: Minimum output level of the V Tune port in volts.
                    """
                    return float(self.instrument.query(":SENSe:VCO:SOURce:VOLTage:VTUNe:LEVel:LIMit:LOW?"))

                def set_vtune_limit_high(self, value):
                    """
                    Parameter:
                        value (float): Maximum output level of the V Tune port in volts.
                    Return:
                        None
                    """
                    self.instrument.write(f":SENSe:VCO:SOURce:VOLTage:VTUNe:LEVel:LIMit:HIGH {value}")

                def get_vtune_limit_high(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: Maximum output level of the V Tune port in volts.
                    """
                    return float(self.instrument.query(":SENSe:VCO:SOURce:VOLTage:VTUNe:LEVel:LIMit:HIGH?"))

                def set_vsup_limit_low(self, value):
                    """
                    Parameter:
                        value (float): Minimum output level of the V Supply port in volts.
                    Return:
                        None
                    """
                    self.instrument.write(f":SENSe:VCO:SOURce:VOLTage:VSUPply:LEVel:LIMit:LOW {value}")

                def get_vsup_limit_low(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: Minimum output level of the V Supply port in volts.
                    """
                    return float(self.instrument.query(":SENSe:VCO:SOURce:VOLTage:VSUPply:LEVel:LIMit:LOW?"))

                def set_vsup_limit_high(self, value):
                    """
                    Parameter:
                        value (float): Maximum output level of the V Supply port in volts.
                    Return:
                        None
                    """
                    self.instrument.write(f":SENSe:VCO:SOURce:VOLTage:VSUPply:LEVel:LIMit:HIGH {value}")

                def get_vsup_limit_high(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: Maximum output level of the V Supply port in volts.
                    """
                    return float(self.instrument.query(":SENSe:VCO:SOURce:VOLTage:VSUPply:LEVel:LIMit:HIGH?"))
        class Audio:
            """
            The Audio commands control the audio player utility in Spike.
            """
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler

            def start(self):
                """
                Parameter:
                    None
                Return:
                    None
                """
                self.instrument.write(":SENSe:AUDio:STARt")

            def stop(self):
                """
                Parameter:
                    None
                Return:
                    None
                """
                self.instrument.write(":SENSe:AUDio:STOP")

            def set_center_frequency(self, freq):
                """
                Parameter:
                    freq (float): Center frequency of the audio player (Hz).
                Return:
                    None
                """
                self.instrument.write(f":SENSe:AUDio:FREQuency:CENTer {freq}")

            def get_center_frequency(self):
                """
                Parameter:
                    None
                Return:
                    float: The center frequency of the audio player (Hz).
                """
                return float(self.instrument.query(":SENSe:AUDio:FREQuency:CENTer?"))

            def set_modulation(self, mod):
                """
                Parameter:
                    mod (str): 'AM', 'FM', 'LSB', 'USB', or 'CW'.
                Return:
                    None
                """
                allowed = {"AM", "FM", "LSB", "USB", "CW"}
                if not isinstance(mod, str) or mod.upper() not in allowed:
                    raise ValueError("mod must be one of 'AM', 'FM', 'LSB', 'USB', or 'CW'")
                self.instrument.write(f":SENSe:AUDio:MOD {mod.upper()}")

            def get_modulation(self):
                """
                Parameter:
                    None
                Return:
                    str: The audio demodulation type.
                """
                return self.instrument.query(":SENSe:AUDio:MOD?")

            def set_if_bandwidth(self, freq):
                """
                Parameter:
                    freq (float): IF bandwidth of the audio player (Hz).
                Return:
                    None
                """
                self.instrument.write(f":SENSe:AUDio:BANDwidth:IF {freq}")

            def get_if_bandwidth(self):
                """
                Parameter:
                    None
                Return:
                    float: The IF bandwidth of the audio player (Hz).
                """
                return float(self.instrument.query(":SENSe:AUDio:BANDwidth:IF?"))

            def set_lowpass_bandwidth(self, freq):
                """
                Parameter:
                    freq (float): Audio low pass filter cutoff (Hz).
                Return:
                    None
                """
                self.instrument.write(f":SENSe:AUDio:BANDwidth:LOW {freq}")

            def get_lowpass_bandwidth(self):
                """
                Parameter:
                    None
                Return:
                    float: The audio low pass filter cutoff (Hz).
                """
                return float(self.instrument.query(":SENSe:AUDio:BANDwidth:LOW?"))

            def set_highpass_bandwidth(self, freq):
                """
                Parameter:
                    freq (float): Audio high pass filter cutoff (Hz).
                Return:
                    None
                """
                self.instrument.write(f":SENSe:AUDio:BANDwidth:HIGH {freq}")

            def get_highpass_bandwidth(self):
                """
                Parameter:
                    None
                Return:
                    float: The audio high pass filter cutoff (Hz).
                """
                return float(self.instrument.query(":SENSe:AUDio:BANDwidth:HIGH?"))

            def set_fm_deemphasis(self, value):
                """
                Parameter:
                    value (float): FM deemphasis in microseconds.
                Return:
                    None
                """
                self.instrument.write(f":SENSe:AUDio:FM:DEEMphasis {value}")

            def get_fm_deemphasis(self):
                """
                Parameter:
                    None
                Return:
                    float: The FM deemphasis in microseconds.
                """
                return float(self.instrument.query(":SENSe:AUDio:FM:DEEMphasis?"))
        class PNoise:
            """
            The PNoise commands control the phase noise measurement mode.
            """
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler
                self.carrier = SpectrumAnalyzer.Sense.PNoise.Carrier(self.instrument)
                self.view = SpectrumAnalyzer.Sense.PNoise.View(self.instrument)
                self.frequency = SpectrumAnalyzer.Sense.PNoise.Frequency(self.instrument)
                self.xcorr = SpectrumAnalyzer.Sense.PNoise.XCORr(self.instrument)
                self.vco = SpectrumAnalyzer.Sense.PNoise.VCO(self.instrument)

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
                def __init__(self, instrument,data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler

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
                def __init__(self, instrument,data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler

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
                def __init__(self, instrument,data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler

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
                def __init__(self, instrument,data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler
                    self.device = SpectrumAnalyzer.Sense.PNoise.XCORr.Device(self.instrument)

                class Device:
                    """
                    The Device commands control the cross correlation device settings in phase noise measurement mode.
                    """
                    def __init__(self, instrument,data_handler):
                        self.instrument = instrument
                        self.data_handler = data_handler

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
                
            class VCO:
                """
                The VCO commands control the VCO settings in phase noise measurement mode.
                """
                def __init__(self, instrument,data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler

                
                def is_active(self):
                    """
                    Parameter:
                        None
                    Return:
                        bool: True if the PN400 is connected in the software, False otherwise.
                    """
                    resp = self.instrument.query(":SENSe:PNoise:VCO:ACTive?")
                    return resp.strip() == '1'

                def connect(self):
                    """
                    Parameter:
                        None
                    Return:
                        bool: True if PN400 is connected successfully, False otherwise.
                    """
                    resp = self.instrument.query(":SENSe:PNoise:VCO:CONnect?")
                    return resp.strip() == '1'

                def set_voltage_state(self, state):
                    """
                    Parameter:
                        state (int or str): 1/0 or 'ON'/'OFF' to enable/disable the supply and tune output voltages.
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
                    self.instrument.write(f":SENSe:PNoise:VCO:VOLTage:STATe {state}")

                def is_voltage_enabled(self):
                    """
                    Parameter:
                        None
                    Return:
                        bool: True if supply and tune output voltages are enabled, False otherwise.
                    """
                    resp = self.instrument.query(":SENSe:PNoise:VCO:VOLTage:STATe?")
                    return int(resp.strip()) == 1

                def set_supply_min(self, value):
                    """
                    Parameter:
                        value (float): Minimum supply voltage.
                    Return:
                        None
                    """
                    self.instrument.write(f":SENSe:PNoise:VCO:VOLTage:SUPply:MIN {value}")

                def get_supply_min(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: Minimum supply voltage.
                    """
                    return float(self.instrument.query(":SENSe:PNoise:VCO:VOLTage:SUPply:MIN?"))

                def set_supply_max(self, value):
                    """
                    Parameter:
                        value (float): Maximum supply voltage.
                    Return:
                        None
                    """
                    self.instrument.write(f":SENSe:PNoise:VCO:VOLTage:SUPply:MAX {value}")

                def get_supply_max(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: Maximum supply voltage.
                    """
                    return float(self.instrument.query(":SENSe:PNoise:VCO:VOLTage:SUPply:MAX?"))

                def set_supply(self, value):
                    """
                    Parameter:
                        value (float): Supply voltage.
                    Return:
                        None
                    """
                    self.instrument.write(f":SENSe:PNoise:VCO:VOLTage:SUPply {value}")

                def get_supply(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: Supply voltage.
                    """
                    return float(self.instrument.query(":SENSe:PNoise:VCO:VOLTage:SUPply?"))

                def set_tune_min(self, value):
                    """
                    Parameter:
                        value (float): Minimum tune voltage.
                    Return:
                        None
                    """
                    self.instrument.write(f":SENSe:PNoise:VCO:VOLTage:TUNE:MIN {value}")

                def get_tune_min(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: Minimum tune voltage.
                    """
                    return float(self.instrument.query(":SENSe:PNoise:VCO:VOLTage:TUNE:MIN?"))

                def set_tune_max(self, value):
                    """
                    Parameter:
                        value (float): Maximum tune voltage.
                    Return:
                        None
                    """
                    self.instrument.write(f":SENSe:PNoise:VCO:VOLTage:TUNE:MAX {value}")

                def get_tune_max(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: Maximum tune voltage.
                    """
                    return float(self.instrument.query(":SENSe:PNoise:VCO:VOLTage:TUNE:MAX?"))

                def set_tune(self, value):
                    """
                    Parameter:
                        value (float): Tune voltage.
                    Return:
                        None
                    """
                    self.instrument.write(f":SENSe:PNoise:VCO:VOLTage:TUNE {value}")

                def get_tune(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: Tune voltage.
                    """
                    return float(self.instrument.query(":SENSe:PNoise:VCO:VOLTage:TUNE?"))
        class PeakTable:
                """
                The PeakTable commands control the Peak Table display panel in Swept Analysis mode.
                """
                def __init__(self, instrument,data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler

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
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler

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
            def __init__(self, instrument,data_handler, table_num):
                self.instrument = instrument
                self.data_handler = data_handler
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
                response = self.instrument.query(f":SENSe:CORRection:PATHloss{self.table_num}:DATA?")
                if self.data_handler.is_auto_saving_data_enabled():
                    self.data_handler.write_to_file(self, "CORR_PATHLOSS", response, file_type = EFileType.CSV, headers = None)
                return response

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
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler

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
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler

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
            def set_rf_division(self, division):
                """
                Parameter:
                division (float): Plot vertical division (1/10th of the plot height) as dB.
                Return:
                None
                """
                self.instrument.write(f":SENSe:POWer:RF:PDIVision {division}")

            def get_rf_division(self):
                """
                Parameter:
                None
                Return:
                float: The plot vertical division as dB.
                """
                return float(self.instrument.query(":SENSe:POWer:RF:PDIVision?"))

            def get_rlevel(self):
                """
                Parameter:
                None
                Return:
                float: The current reference level as dBm.
                """
                return float(self.instrument.query(":SENSe:POWer:RF:RLEVel?"))
        class Bandwidth:
            """
            The Bandwidth commands control the FFT processing for the receivers.
            """
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler

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
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler
                self.detector = SpectrumAnalyzer.Sense.Sweep.Detector(self.instrument)
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
                def __init__(self, instrument,data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler

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
        class SEMask:
            """
            The SEMask commands control the spectrum emission mask mode.
            """
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler
                self.frequency = SpectrumAnalyzer.Sense.SEMask.Frequency(self.instrument)
                self.bandwidth = SpectrumAnalyzer.Sense.SEMask.Bandwidth(self.instrument)
                self.sweep = SpectrumAnalyzer.Sense.SEMask.Sweep(self.instrument)
                self.reference = SpectrumAnalyzer.Sense.SEMask.Reference(self.instrument)
                self.offset = SpectrumAnalyzer.Sense.SEMask.Offset(self.instrument)
                self.marker = SpectrumAnalyzer.Sense.SEMask.Marker(self.instrument)
            class Frequency:
                """
                The SEMask:Frequency commands control the frequency range of the sweeps in spectrum emission mask mode.
                """
                def __init__(self, instrument,data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler

                def set_center(self, value):
                    """
                    Parameter:
                        value (float or str): Center frequency in Hz, or 'UP', or 'DOWN'.
                    Return:
                        None
                    """
                    if isinstance(value, str):
                        if value.upper() not in {"UP", "DOWN"}:
                            raise ValueError("value must be a float or one of 'UP', 'DOWN'")
                        val_str = value.upper()
                    else:
                        val_str = str(value)
                    self.instrument.write(f":SENSe:SEMask:FREQuency:CENTer {val_str}")

                def get_center(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: The center frequency in Hz.
                    """
                    return float(self.instrument.query(":SENSe:SEMask:FREQuency:CENTer?"))

                def set_center_step(self, value):
                    """
                    Parameter:
                        value (float): Step amount for center frequency changes in Hz.
                    Return:
                        None
                    """
                    self.instrument.write(f":SENSe:SEMask:FREQuency:CENTer:STEP {value}")

                def get_center_step(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: The center frequency step size in Hz.
                    """
                    return float(self.instrument.query(":SENSe:SEMask:FREQuency:CENTer:STEP?"))

                def set_span(self, value):
                    """
                    Parameter:
                        value (float): Span in Hz.
                    Return:
                        None
                    """
                    self.instrument.write(f":SENSe:SEMask:FREQuency:SPAN {value}")

                def get_span(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: The span in Hz.
                    """
                    return float(self.instrument.query(":SENSe:SEMask:FREQuency:SPAN?"))

            class Bandwidth:
                """
                The SEMask:Bandwidth commands control the FFT processing for the receivers in SEM mode.
                """
                def __init__(self, instrument,data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler

                def set_resolution(self, value):
                    """
                    Parameter:
                        value (float or str): RBW in Hz, or 'UP', or 'DOWN'.
                    Return:
                        None
                    """
                    if isinstance(value, str):
                        if value.upper() not in {"UP", "DOWN"}:
                            raise ValueError("value must be a float or one of 'UP', 'DOWN'")
                        val_str = value.upper()
                    else:
                        val_str = str(value)
                    self.instrument.write(f":SENSe:SEMask:BANDwidth:RESolution {val_str}")

                def get_resolution(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: The current RBW in Hz.
                    """
                    return float(self.instrument.query(":SENSe:SEMask:BANDwidth:RESolution?"))

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
                    self.instrument.write(f":SENSe:SEMask:BANDwidth:RESolution:AUTO {state}")

                def is_resolution_auto(self):
                    """
                    Parameter:
                        None
                    Return:
                        bool: True if auto RBW is enabled, False otherwise.
                    """
                    resp = self.instrument.query(":SENSe:SEMask:BANDwidth:RESolution:AUTO?")
                    return int(resp.strip()) == 1

                def set_video(self, value):
                    """
                    Parameter:
                        value (float or str): VBW in Hz, or 'UP', or 'DOWN'.
                    Return:
                        None
                    """
                    if isinstance(value, str):
                        if value.upper() not in {"UP", "DOWN"}:
                            raise ValueError("value must be a float or one of 'UP', 'DOWN'")
                        val_str = value.upper()
                    else:
                        val_str = str(value)
                    self.instrument.write(f":SENSe:SEMask:BANDwidth:VIDeo {val_str}")

                def get_video(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: The current VBW in Hz.
                    """
                    return float(self.instrument.query(":SENSe:SEMask:BANDwidth:VIDeo?"))

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
                    self.instrument.write(f":SENSe:SEMask:BANDwidth:VIDeo:AUTO {state}")

                def is_video_auto(self):
                    """
                    Parameter:
                        None
                    Return:
                        bool: True if auto VBW is enabled, False otherwise.
                    """
                    resp = self.instrument.query(":SENSe:SEMask:BANDwidth:VIDeo:AUTO?")
                    return int(resp.strip()) == 1
            class Sweep:
                """
                The Sweep commands control the detector and trace settings of the receiver in SEM mode.
                """
                def __init__(self, instrument,data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler
                    self.detector = SpectrumAnalyzer.Sense.SEMask.Sweep.Detector(self.instrument)
                class Detector:
                    """
                    The Detector commands control the detector function and units in SEM mode.
                    """
                    def __init__(self, instrument,data_handler):
                        self.instrument = instrument
                        self.data_handler = data_handler

                    def set_function(self, func):
                        """
                        Parameter:
                            func (str): 'AVERAGE' or 'MINMAX'
                        Return:
                            None
                        """
                        allowed = {"AVERAGE", "MINMAX"}
                        if not isinstance(func, str) or func.upper() not in allowed:
                            raise ValueError("func must be 'AVERAGE' or 'MINMAX'")
                        self.instrument.write(f":SENSe:SEMask:SWEep:DETector:FUNCtion {func.upper()}")

                    def get_function(self):
                        """
                        Parameter:
                            None
                        Return:
                            str: The current detector function.
                        """
                        return self.instrument.query(":SENSe:SEMask:SWEep:DETector:FUNCtion?")

                    def set_units(self, units):
                        """
                        Parameter:
                            units (str): 'POWER', 'SAMPLE', 'VOLTAGE', or 'LOG'
                        Return:
                            None
                        """
                        allowed = {"POWER", "SAMPLE", "VOLTAGE", "LOG"}
                        if not isinstance(units, str) or units.upper() not in allowed:
                            raise ValueError("units must be one of 'POWER', 'SAMPLE', 'VOLTAGE', or 'LOG'")
                        self.instrument.write(f":SENSe:SEMask:SWEep:DETector:UNITs {units.upper()}")

                    def get_units(self):
                        """
                        Parameter:
                            None
                        Return:
                            str: The current detector units.
                        """
                        return self.instrument.query(":SENSe:SEMask:SWEep:DETector:UNITs?")
            class Reference():
                """The Reference commands control the reference measurement settings in SEM mode."""
                def __init__(self, instrument,data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler
                def set_trace_type(self, typ):
                    """
                    Parameter:
                        typ (str): 'WRITE' or 'MAXHOLD'
                    Return:
                        None
                    """
                    allowed = {"WRITE", "MAXHOLD"}
                    if not isinstance(typ, str) or typ.upper() not in allowed:
                        raise ValueError("typ must be 'WRITE' or 'MAXHOLD'")
                    self.instrument.write(f":TRACe:SEMask:REF:TYPE {typ.upper()}")

                def get_trace_type(self):
                    """
                    Parameter:
                        None
                    Return:
                        str: The current trace type.
                    """
                    return self.instrument.query(":TRACe:SEMask:REF:TYPE?")
               
                def get_type(self):
                    """
                    Parameter:
                        None
                    Return:
                        str: The current reference measurement type.
                    """
                    return self.instrument.query(":SENSe:SEMask:REF:TYPE?")

                def set_bandwidth_mode(self, mode):
                    """
                    Parameter:
                        mode (str): 'AUTO' or 'MANUAL'
                    Return:
                        None
                    """
                    allowed = {"AUTO", "MANUAL"}
                    if not isinstance(mode, str) or mode.upper() not in allowed:
                        raise ValueError("mode must be 'AUTO' or 'MANUAL'")
                    self.instrument.write(f":SENSe:SEMask:REF:BANDwidth:MODE {mode.upper()}")

                def get_bandwidth_mode(self):
                    """
                    Parameter:
                        None
                    Return:
                        str: The current bandwidth mode.
                    """
                    return self.instrument.query(":SENSe:SEMask:REF:BANDwidth:MODE?")

                def set_bandwidth(self, freq):
                    """
                    Parameter:
                        freq (float): The width of the measurement band in Hz.
                    Return:
                        None
                    """
                    self.instrument.write(f":SENSe:SEMask:REF:BANDwidth {freq}")

                def get_bandwidth(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: The width of the measurement band in Hz.
                    """
                    return float(self.instrument.query(":SENSe:SEMask:REF:BANDwidth?"))

                def set_level(self, amplitude):
                    """
                    Parameter:
                        amplitude (float): Reference amplitude level in dBm.
                    Return:
                        None
                    """
                    self.instrument.write(f":SENSe:SEMask:REF:LEVEL {amplitude}")

                def get_level(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: The reference amplitude level in dBm.
                    """
                    return float(self.instrument.query(":SENSe:SEMask:REF:LEVEL?"))
            class Offset:
                """
                The Offset commands control the offset settings for the spectrum emission mask."""
                def __init__(self, instrument,data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler
                def set_offset_parameters(self, offsets):
                    """
                    Parameter:
                        offsets (list of tuple): List of tuples, each containing (enabled, startFreq, stopFreq, startLimit, stopLimit, mode).
                            enabled: 'ON', 'OFF', 1, or 0
                            startFreq: float (Hz)
                            stopFreq: float (Hz)
                            startLimit: float
                            stopLimit: float
                            mode: 'RELATIVE' or 'ABSOLUTE'
                    Return:
                        None
                    """
                    allowed_enabled = {"ON", "OFF", 1, 0}
                    allowed_mode = {"RELATIVE", "ABSOLUTE"}
                    if not isinstance(offsets, list) or not all(isinstance(o, tuple) and len(o) == 6 for o in offsets):
                        raise ValueError("offsets must be a list of 6-element tuples")
                    parts = []
                    for enabled, startFreq, stopFreq, startLimit, stopLimit, mode in offsets:
                        if isinstance(enabled, str):
                            enabled_val = enabled.upper()
                            if enabled_val not in allowed_enabled:
                                raise ValueError("enabled must be 'ON', 'OFF', 1, or 0")
                        elif enabled in [1, 0]:
                            enabled_val = enabled
                        else:
                            raise ValueError("enabled must be 'ON', 'OFF', 1, or 0")
                        if not isinstance(mode, str) or mode.upper() not in allowed_mode:
                            raise ValueError("mode must be 'RELATIVE' or 'ABSOLUTE'")
                        parts.append(f"{enabled_val},{startFreq},{stopFreq},{startLimit},{stopLimit},{mode.upper()}")
                    data_str = ", ".join(parts)
                    self.instrument.write(f":SENSe:SEMask:OFFSet:DATA {data_str}")

                def get_offset_parameters(self):
                    """
                    Parameter:
                        None
                    Return:
                        str: The current offset table as a comma separated list.
                    """
                    response = self.instrument.query(":SENSe:SEMask:OFFSet:DATA?")
                    if self.data_handler.is_auto_saving_data_enabled():
                        self.data_handler.write_to_file(self, "SEMASK_OFFSET", response, file_type = EFileType.CSV, headers = None)
                    return response

                def is_fail(self):
                    """
                    Parameter:
                        None
                    Return:
                        bool: True if mask fails, False otherwise.
                    """
                    resp = self.instrument.query(":SENSe:SEMask:OFFSet:FAIL?")
                    return int(resp.strip()) == 1

                def is_offset_fail(self, offset_num):
                    """
                    Parameter:
                        offset_num (int): Offset index [1-16].
                    Return:
                        bool: True if specified offset fails, False otherwise.
                    """
                    if not isinstance(offset_num, int) or not (1 <= offset_num <= 16):
                        raise ValueError("offset_num must be an integer between 1 and 16")
                    resp = self.instrument.query(f":SENSe:SEMask:OFFSet{offset_num}:FAIL?")
                    return int(resp.strip()) == 1

                def is_lower_fail(self, offset_num):
                    """
                    Parameter:
                        offset_num (int): Offset index [1-16].
                    Return:
                        bool: True if lower range of specified offset fails, False otherwise.
                    """
                    if not isinstance(offset_num, int) or not (1 <= offset_num <= 16):
                        raise ValueError("offset_num must be an integer between 1 and 16")
                    resp = self.instrument.query(f":SENSe:SEMask:OFFSet{offset_num}:LOWer:FAIL?")
                    return int(resp.strip()) == 1

                def is_upper_fail(self, offset_num):
                    """
                    Parameter:
                        offset_num (int): Offset index [1-16].
                    Return:
                        bool: True if upper range of specified offset fails, False otherwise.
                    """
                    if not isinstance(offset_num, int) or not (1 <= offset_num <= 16):
                        raise ValueError("offset_num must be an integer between 1 and 16")
                    resp = self.instrument.query(f":SENSe:SEMask:OFFSet{offset_num}:UPper:FAIL?")
                    return int(resp.strip()) == 1

                def get_margin(self, offset_num):
                    """
                    Parameter:
                        offset_num (int): Offset index [1-16].
                    Return:
                        float: Worst margin (limit - peak) of specified offset.
                    """
                    if not isinstance(offset_num, int) or not (1 <= offset_num <= 16):
                        raise ValueError("offset_num must be an integer between 1 and 16")
                    return float(self.instrument.query(f":SENSe:SEMask:OFFSet{offset_num}:MARgin?"))

                def get_margin_lower(self, offset_num):
                    """
                    Parameter:
                        offset_num (int): Offset index [1-16].
                    Return:
                        float: Margin (limit - peak) of lower range of specified offset.
                    """
                    if not isinstance(offset_num, int) or not (1 <= offset_num <= 16):
                        raise ValueError("offset_num must be an integer between 1 and 16")
                    return float(self.instrument.query(f":SENSe:SEMask:OFFSet{offset_num}:MARgin:LOWer?"))

                def get_margin_upper(self, offset_num):
                    """
                    Parameter:
                        offset_num (int): Offset index [1-16].
                    Return:
                        float: Margin (limit - peak) of upper range of specified offset.
                    """
                    if not isinstance(offset_num, int) or not (1 <= offset_num <= 16):
                        raise ValueError("offset_num must be an integer between 1 and 16")
                    return float(self.instrument.query(f":SENSe:SEMask:OFFSet{offset_num}:MARgin:UPper?"))

                def get_peak_level_lower(self, offset_num):
                    """
                    Parameter:
                        offset_num (int): Offset index [1-16].
                    Return:
                        float: Peak level of lower range of specified offset.
                    """
                    if not isinstance(offset_num, int) or not (1 <= offset_num <= 16):
                        raise ValueError("offset_num must be an integer between 1 and 16")
                    return float(self.instrument.query(f":SENSe:SEMask:OFFSet{offset_num}:PEAK:LEVel:LOWer?"))

                def get_peak_level_upper(self, offset_num):
                    """
                    Parameter:
                        offset_num (int): Offset index [1-16].
                    Return:
                        float: Peak level of upper range of specified offset.
                    """
                    if not isinstance(offset_num, int) or not (1 <= offset_num <= 16):
                        raise ValueError("offset_num must be an integer between 1 and 16")
                    return float(self.instrument.query(f":SENSe:SEMask:OFFSet{offset_num}:PEAK:LEVel:UPper?"))

                def get_peak_frequency_lower(self, offset_num):
                    """
                    Parameter:
                        offset_num (int): Offset index [1-16].
                    Return:
                        float: Frequency at peak of lower range of specified offset.
                    """
                    if not isinstance(offset_num, int) or not (1 <= offset_num <= 16):
                        raise ValueError("offset_num must be an integer between 1 and 16")
                    return float(self.instrument.query(f":SENSe:SEMask:OFFSet{offset_num}:PEAK:FREQuency:LOWer?"))

                def get_peak_frequency_upper(self, offset_num):
                    """
                    Parameter:
                        offset_num (int): Offset index [1-16].
                    Return:
                        float: Frequency at peak of upper range of specified offset.
                    """
                    if not isinstance(offset_num, int) or not (1 <= offset_num <= 16):
                        raise ValueError("offset_num must be an integer between 1 and 16")
                    return float(self.instrument.query(f":SENSe:SEMask:OFFSet{offset_num}:PEAK:FREQuency:UPper?"))

            class Marker:
                """
                The Marker commands control the marker in spectrum emission mask mode.
                """
                def __init__(self, instrument,data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler

                def enable(self, state):
                    """
                    Parameter:
                        state (int or str): 1/0 or 'ON'/'OFF' to enable/disable the marker.
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
                    self.instrument.write(f":CALCulate:SEMask:MARKer:STATe {state}")

                def is_enabled(self):
                    """
                    Parameter:
                        None
                    Return:
                        bool: True if marker is enabled, False otherwise.
                    """
                    resp = self.instrument.query(":CALCulate:SEMask:MARKer:STATe?")
                    return int(resp.strip()) == 1

                def set_delta(self, state):
                    """
                    Parameter:
                        state (int or str): 1/0 or 'ON'/'OFF' to enable/disable delta marker.
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
                    self.instrument.write(f":CALCulate:SEMask:MARKer:DELTa {state}")

                def is_delta_enabled(self):
                    """
                    Parameter:
                        None
                    Return:
                        bool: True if delta marker is enabled, False otherwise.
                    """
                    resp = self.instrument.query(":CALCulate:SEMask:MARKer:DELTa?")
                    return int(resp.strip()) == 1

                def set_x(self, freq):
                    """
                    Parameter:
                        freq (float): Frequency to move marker to (Hz).
                    Return:
                        None
                    """
                    self.instrument.write(f":CALCulate:SEMask:MARKer:X {freq}")

                def get_x(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: The marker position frequency (Hz).
                    """
                    return float(self.instrument.query(":CALCulate:SEMask:MARKer:X?"))

                def get_y(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: The marker position amplitude.
                    """
                    return float(self.instrument.query(":CALCulate:SEMask:MARKer:Y?"))

                def maximum(self):
                    """
                    Parameter:
                        None
                    Return:
                        None
                    """
                    self.instrument.write(":CALCulate:SEMask:MARKer:MAXimum")

                def minimum(self):
                    """
                    Parameter:
                        None
                    Return:
                        None
                    """
                    self.instrument.write(":CALCulate:SEMask:MARKer:MINimum")

                def next(self):
                    """
                    Parameter:
                        None
                    Return:
                        None
                    """
                    self.instrument.write(":CALCulate:SEMask:MARKer:NEXT")

                def previous(self):
                    """
                    Parameter:
                        None
                    Return:
                        None
                    """
                    self.instrument.write(":CALCulate:SEMask:MARKer:PREVious")
        class NFIGure:
            """
            The NFIGure commands control the Noise Figure measurement mode.
            """
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler
                self.frequency = SpectrumAnalyzer.Sense.NFIGure.Frequency(self.instrument)
                self.bandwidth = SpectrumAnalyzer.Sense.NFIGure.Bandwidth(self.instrument)
                self.correction = SpectrumAnalyzer.Sense.NFIGure.Correction(self.instrument)
                self.fetch = SpectrumAnalyzer.Sense.NFIGure.Fetch(self.instrument)
            class Frequency:
                """
                The NFIGure:Frequency commands control the list of frequency points for noise figure measurements.
                """
                def __init__(self, instrument,data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler

                def set_mode(self, mode):
                    """
                    Parameter:
                    mode (str): 'SWEPt' or 'FIXed'
                    Return:
                    None
                    """
                    allowed = {"SWEPT", "FIXED"}
                    if not isinstance(mode, str) or mode.upper() not in allowed:
                        raise ValueError("mode must be 'SWEPt' or 'FIXed'")
                    self.instrument.write(f":SENSe:NFIGure:FREQuency:MODE {mode.upper()}")

                def get_mode(self):
                    """
                    Parameter:
                    None
                    Return:
                    str: The current frequency list mode.
                    """
                    return self.instrument.query(":SENSe:NFIGure:FREQuency:MODE?")

                def set_start(self, freq):
                    """
                    Parameter:
                    freq (float): Start frequency in Hz.
                    Return:
                    None
                    """
                    self.instrument.write(f":SENSe:NFIGure:FREQuency:STARt {freq}")

                def get_start(self):
                    """
                    Parameter:
                    None
                    Return:
                    float: The current start frequency in Hz.
                    """
                    return float(self.instrument.query(":SENSe:NFIGure:FREQuency:STARt?"))

                def set_stop(self, freq):
                    """
                    Parameter:
                    freq (float): Stop frequency in Hz.
                    Return:
                    None
                    """
                    self.instrument.write(f":SENSe:NFIGure:FREQuency:STOP {freq}")

                def get_stop(self):
                    """
                    Parameter:
                    None
                    Return:
                    float: The current stop frequency in Hz.
                    """
                    return float(self.instrument.query(":SENSe:NFIGure:FREQuency:STOP?"))

                def set_center(self, freq):
                    """
                    Parameter:
                    freq (float): Center frequency in Hz.
                    Return:
                    None
                    """
                    self.instrument.write(f":SENSe:NFIGure:FREQuency:CENTer {freq}")

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
                        #raise ValueError("bound must be 'MIN' or 'MAX'")
                        resp = self.instrument.query(f":SENSe:NFIGure:FREQuency:CENTer? {bound}")
                    else:
                        resp = self.instrument.query(":SENSe:NFIGure:FREQuency:CENTer?")
                    return float(resp)

                def set_span(self, span):
                    """
                    Parameter:
                    span (float): Span in Hz.
                    Return:
                    None
                    """
                    self.instrument.write(f":SENSe:NFIGure:FREQuency:SPAN {span}")

                def get_span(self):
                    """
                    Parameter:
                    None
                    Return:
                    float: The span in Hz.
                    """
                    return float(self.instrument.query(":SENSe:NFIGure:FREQuency:SPAN?"))

                def set_points(self, num_points):
                    """
                    Parameter:
                    num_points (int): Number of measurement points.
                    Return:
                    None
                    """
                    if not isinstance(num_points, int):
                        raise ValueError("num_points must be an integer")
                    self.instrument.write(f":SENSe:NFIGure:FREQuency:POINts {num_points}")

                def get_points(self):
                    """
                    Parameter:
                    None
                    Return:
                    int: The number of measurement points.
                    """
                    return int(self.instrument.query(":SENSe:NFIGure:FREQuency:POINts?"))

                def set_fixed(self, freq):
                    """
                    Parameter:
                    freq (float): Fixed frequency in Hz.
                    Return:
                    None
                    """
                    self.instrument.write(f":SENSe:NFIGure:FREQuency:FIXed {freq}")

                def get_fixed(self):
                    """
                    Parameter:
                    None
                    Return:
                    float: The fixed frequency in Hz.
                    """
                    return float(self.instrument.query(":SENSe:NFIGure:FREQuency:FIXed?"))

                def get_list_data(self):
                    """
                    Parameter:
                    None
                    Return:
                    str: The list of measurement frequencies in Hz (comma separated).
                    """
                    return self.instrument.query(":SENSe:NFIGure:FREQuency:LIST:DATA?")
            class Bandwidth:
                """
                The NFIGure:Bandwidth commands control the bandwidth settings for noise figure measurements.
                """
                def __init__(self, instrument,data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler

                def set_resolution(self, value):
                    """
                    Parameter:
                        value (float or str): RBW in Hz, or 'UP', or 'DOWN'.
                    Return:
                        None
                    """
                    if isinstance(value, str):
                        if value.upper() not in {"UP", "DOWN"}:
                            raise ValueError("value must be a float or one of 'UP', 'DOWN'")
                        val_str = value.upper()
                    else:
                        val_str = str(value)
                    self.instrument.write(f":SENSe:NFIGure:BANDwidth:RESolution {val_str}")

                def get_resolution(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: The current RBW in Hz.
                    """
                    return float(self.instrument.query(":SENSe:NFIGure:BANDwidth:RESolution?"))

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
                    self.instrument.write(f":SENSe:NFIGure:BANDwidth:RESolution:AUTO {state}")

                def is_resolution_auto(self):
                    """
                    Parameter:
                        None
                    Return:
                        bool: True if auto RBW is enabled, False otherwise.
                    """
                    resp = self.instrument.query(":SENSe:NFIGure:BANDwidth:RESolution:AUTO?")
                    return int(resp.strip()) == 1

                def set_video(self, value):
                    """
                    Parameter:
                        value (float or str): VBW in Hz, or 'UP', or 'DOWN'.
                    Return:
                        None
                    """
                    if isinstance(value, str):
                        if value.upper() not in {"UP", "DOWN"}:
                            raise ValueError("value must be a float or one of 'UP', 'DOWN'")
                        val_str = value.upper()
                    else:
                        val_str = str(value)
                    self.instrument.write(f":SENSe:NFIGure:BANDwidth:VIDeo {val_str}")

                def get_video(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: The current VBW in Hz.
                    """
                    return float(self.instrument.query(":SENSe:NFIGure:BANDwidth:VIDeo?"))

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
                    self.instrument.write(f":SENSe:NFIGure:BANDwidth:VIDeo:AUTO {state}")

                def is_video_auto(self):
                    """
                    Parameter:
                        None
                    Return:
                        bool: True if auto VBW is enabled, False otherwise.
                    """
                    resp = self.instrument.query(":SENSe:NFIGure:BANDwidth:VIDeo:AUTO?")
                    return int(resp.strip()) == 1

                def set_power_rf_rlevel(self, value):
                    """
                    Parameter:
                    value (float): Reference level of the measurement in dBm.
                    Return:
                    None
                    """
                    self.instrument.write(f":SENSe:NFIGure:POWer:RF:RLEVel {value}")

                def get_power_rf_rlevel(self):
                    """
                    Parameter:
                    None
                    Return:
                    float: The reference level of the measurement in dBm.
                    """
                    return float(self.instrument.query(":SENSe:NFIGure:POWer:RF:RLEVel?"))

                def set_meas_span(self, value):
                    """
                    Parameter:
                    value (float): Span of each sweep in Hz.
                    Return:
                    None
                    """
                    self.instrument.write(f":SENSe:NFIGure:MEAS:SPAN {value}")

                def get_meas_span(self):
                    """
                    Parameter:
                    None
                    Return:
                    float: The span of each sweep in Hz.
                    """
                    return float(self.instrument.query(":SENSe:NFIGure:MEAS:SPAN?"))

                def set_average_state(self, state):
                    """
                    Parameter:
                    state (int or str): 1/0 or 'ON'/'OFF' to enable/disable averaging.
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
                    self.instrument.write(f":SENSe:NFIGure:AVERage:STATe {state}")

                def is_average_enabled(self):
                    """
                    Parameter:
                    None
                    Return:
                    bool: True if averaging is enabled, False otherwise.
                    """
                    resp = self.instrument.query(":SENSe:NFIGure:AVERage:STATe?")
                    return int(resp.strip()) == 1

                def set_average_count(self, count):
                    """
                    Parameter:
                    count (int): Number of sweeps to average together.
                    Return:
                    None
                    """
                    if not isinstance(count, int):
                        raise ValueError("count must be an integer")
                    self.instrument.write(f":SENSe:NFIGure:AVERage:COUNt {count}")

                def get_average_count(self):
                    """
                    Parameter:
                    None
                    Return:
                    int: The number of sweeps averaged together.
                    """
                    return int(self.instrument.query(":SENSe:NFIGure:AVERage:COUNt?"))

                def set_tcold_value(self, value):
                    """
                    Parameter:
                    value (float): Room temperature in Kelvin.
                    Return:
                    None
                    """
                    self.instrument.write(f":SENSe:NFIGure:CORRection:TCOLd:VALue {value}")

                def get_tcold_value(self):
                    """
                    Parameter:
                    None
                    Return:
                    float: Room temperature in Kelvin.
                    """
                    return float(self.instrument.query(":SENSe:NFIGure:CORRection:TCOLd:VALue?"))

                def set_alert_state(self, state):
                    """
                    Parameter:
                    state (int or str): 1/0 or 'ON'/'OFF' to enable/disable alert on sweep completion.
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
                    self.instrument.write(f":SENSe:NFIGure:ALERt:STATe {state}")

                def is_alert_enabled(self):
                    """
                    Parameter:
                    None
                    Return:
                    bool: True if alert is enabled, False otherwise.
                    """
                    resp = self.instrument.query(":SENSe:NFIGure:ALERt:STATe?")
                    return int(resp.strip()) == 1
                

            class Correction:
                """
                The NFIGure:Correction commands control ENR tables and calibration settings for noise figure measurements.
                """
                def __init__(self, instrument,data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler
                    self.enr_table = SpectrumAnalyzer.Sense.NFIGure.Correction.ENRTable(self.instrument)
                class ENRTable:
                    """
                    The ENRTable commands manage ENR tables for noise sources.
                    """
                    def __init__(self, instrument,data_handler):
                        self.instrument = instrument
                        self.data_handler = data_handler

                    def get_count(self):
                        """
                        Parameter:
                        None
                        Return:
                        int: The count of ENR tables.
                        """
                        return int(self.instrument.query(":SENSe:NFIGure:CORRection:ENR:TABLe:COUNt?"))

                    def new(self):
                        """
                        Parameter:
                        None
                        Return:
                        None
                        """
                        self.instrument.write(":SENSe:NFIGure:CORRection:ENR:TABLe:NEW")

                    def load(self, table_id):
                        """
                        Parameter:
                        table_id (int): ENR table ID to load.
                        Return:
                        None
                        """
                        if not isinstance(table_id, int):
                            raise ValueError("table_id must be an integer")
                        self.instrument.write(f":SENSe:NFIGure:CORRection:ENR:TABLe:LOAD {table_id}")

                    def get_current(self):
                        """
                        Parameter:
                        None
                        Return:
                        str: The ID of the currently loaded ENR table.
                        """
                        return self.instrument.query(":SENSe:NFIGure:CORRection:ENR:TABLe?")

                    def set_title(self, title):
                        """
                        Parameter:
                        title (str): Title of the ENR table.
                        Return:
                        None
                        """
                        self.instrument.write(f':SENSe:NFIGure:CORRection:ENR:TABLe:TITLe "{title}"')

                    def get_title(self):
                        """
                        Parameter:
                        None
                        Return:
                        str: The title of the loaded ENR table.
                        """
                        return self.instrument.query(":SENSe:NFIGure:CORRection:ENR:TABLe:TITLe?")

                    def get_points_count(self):
                        """
                        Parameter:
                        None
                        Return:
                        int: Number of points in the loaded ENR table.
                        """
                        return int(self.instrument.query(":SENSe:NFIGure:CORRection:ENR:TABLe:POINts?"))

                    def set_data(self, points):
                        """
                        Parameter:
                        points (list of tuple): List of (freq, enr) pairs.
                        Return:
                        None
                        """
                        if not isinstance(points, list) or not all(isinstance(p, tuple) and len(p) == 2 for p in points):
                            raise ValueError("points must be a list of (freq, enr) tuples")
                        data_str = ", ".join(f"{freq},{enr}" for freq, enr in points)
                        self.instrument.write(f":SENSe:NFIGure:CORRection:ENR:TABLe:DATA {data_str}")

                    def get_data(self):
                        """
                        Parameter:
                        None
                        Return:
                        str: The list of points in the loaded ENR table.
                        """
                        response = self.instrument.query(":SENSe:NFIGure:CORRection:ENR:TABLe:DATA?")
                        if self.data_handler.is_auto_saving_data_enabled():
                            self.data_handler.write_to_file(self, "CORR_ENR", response, file_type = EFileType.CSV, headers = None)
                        return response

                    def set_calibration_table(self, table_id):
                        """
                        Parameter:
                            table_id (int): ENR table ID to use for calibration.
                        Return:
                            None
                        """
                        if not isinstance(table_id, int):
                            raise ValueError("table_id must be an integer")
                        self.instrument.write(f":SENSe:NFIGure:CORRection:ENR:CALibration:TABLe {table_id}")
                        
                    def get_calibration_table(self):
                        """
                        Parameter:
                            None
                        Return:
                            str: The calibration ENR table.
                        """
                        return self.instrument.query(":SENSe:NFIGure:CORRection:ENR:CALibration:TABLe?")

                    def set_measurement_table(self, table_id):
                        """
                        Parameter:
                            table_id (int): ENR table ID to use for measurement.
                        Return:
                            None
                        """
                        if not isinstance(table_id, int):
                            raise ValueError("table_id must be an integer")
                        self.instrument.write(f":SENSe:NFIGure:CORRection:ENR:MEASurement:TABLe {table_id}")

                def get_measurement_table(self):
                    """
                    Parameter:
                        None
                    Return:
                        str: The measurement ENR table.
                    """
                    return self.instrument.query(":SENSe:NFIGure:CORRection:ENR:MEASurement:TABLe?")

            def get_calibration_state(self):
                """
                Parameter:
                None
                Return:
                str: The current calibration state ('uncal', 'semical', or 'cal').
                """
                return self.instrument.query(":SENSe:NFIGure:CALibration:STATe?")

            def initiate_calibration(self):
                """
                Parameter:
                None
                Return:
                None
                """
                self.instrument.write(":SENSe:NFIGure:CALibration:INITiate")

            def initiate_measurement(self):
                """
                Parameter:
                None
                Return:
                None
                """
                self.instrument.write(":SENSe:NFIGure:MEASurement:INITiate")

            def continue_process(self):
                """
                Parameter:
                None
                Return:
                None
                """
                self.instrument.write(":SENSe:NFIGure:CONTinue")

            def abort(self):
                """
                Parameter:
                None
                Return:
                None
                """
                self.instrument.write(":SENSe:NFIGure:ABORt")

            def get_next_action(self):
                """
                Parameter:
                None
                Return:
                str: The next action user needs to take before continuing measurement.
                """
                return self.instrument.query(":STATus:NFIGure:NEXT?")

            def get_progress(self):
                """
                Parameter:
                None
                Return:
                float: The percentage progress of the current sweep.
                """
                return float(self.instrument.query(":STATus:NFIGure:PROGress?"))

            class Fetch:
                """
                The Fetch commands retrieve noise figure and gain measurement results.
                """
                def __init__(self, instrument,data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler

                def get_nfigure(self):
                    """
                    Parameter:
                        None
                    Return:
                        str: List of noise figure measurements for each point in the frequency list.
                    """
                    response = self.instrument.query(":FETCh:NFIGure?")
                    if self.data_handler.is_auto_saving_data_enabled():
                        self.data_handler.write_to_file(self, "NFIGURE_FETCH", response, file_type = EFileType.CSV, headers = None)
                    return response

                def get_gain(self):
                    """
                    Parameter:
                        None
                    Return:
                        str: List of gain measurements for each point in the frequency list.
                    """
                    response = self.instrument.query(":FETCh:NFIGure:GAIN?")
                    if self.data_handler.is_auto_saving_data_enabled():
                        self.data_handler.write_to_file(self, "NFIG_FETCH", response, file_type = EFileType.CSV, headers = None)
                    return response
        class Bluetooth:
            """
            The Bluetooth commands control the Bluetooth Low Energy measurement mode.
            """
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler
                self.measurement = SpectrumAnalyzer.Sense.Bluetooth.Measurement(self.instrument)
                self.trigger = SpectrumAnalyzer.Sense.Bluetooth.Trigger(self.instrument)
            class Measurement:
                """
                The Measurement commands configure Bluetooth measurement mode.
                """
                def __init__(self, instrument,data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler

                def set_meas(self, meas_type):
                    """
                    Parameter:
                    meas_type (str): 'DEMOD' or 'IBE'
                    Return:
                    None
                    """
                    allowed = {"DEMOD", "IBE"}
                    if not isinstance(meas_type, str) or meas_type.upper() not in allowed:
                        raise ValueError("meas_type must be 'DEMOD' or 'IBE'")
                    self.instrument.write(f":SENSe:BLE:MEAS {meas_type.upper()}")

                def get_meas(self):
                    """
                    Parameter:
                    None
                    Return:
                    str: The current Bluetooth measurement type.
                    """
                    return self.instrument.query(":SENSe:BLE:MEAS?")

                def set_center_frequency(self, freq):
                    """
                    Parameter:
                    freq (float): Center frequency in Hz.
                    Return:
                    None
                    """
                    self.instrument.write(f":SENSe:BLE:FREQuency:CENTer {freq}")

                def get_center_frequency(self):
                    """
                    Parameter:
                    None
                    Return:
                    float: The center frequency in Hz.
                    """
                    return float(self.instrument.query(":SENSe:BLE:FREQuency:CENTer?"))

                def set_center_step(self, freq):
                    """
                    Parameter:
                    freq (float): Center frequency step size in Hz.
                    Return:
                    None
                    """
                    self.instrument.write(f":SENSe:BLE:FREQuency:CENTer:STEP {freq}")

                def get_center_step(self):
                    """
                    Parameter:
                    None
                    Return:
                    float: The center frequency step size in Hz.
                    """
                    return float(self.instrument.query(":SENSe:BLE:FREQuency:CENTer:STEP?"))

                def set_ifbw(self, freq):
                    """
                    Parameter:
                    freq (float): Measurement bandwidth for demodulation in Hz.
                    Return:
                    None
                    """
                    self.instrument.write(f":SENSe:BLE:IFBW {freq}")

                def get_ifbw(self):
                    """
                    Parameter:
                    None
                    Return:
                    float: The measurement bandwidth for demodulation in Hz.
                    """
                    return float(self.instrument.query(":SENSe:BLE:IFBW?"))

            def set_channel_index(self, index):
                """
                Parameter:
                index (int): Channel index.
                Return:
                None
                """
                if not isinstance(index, int):
                    raise ValueError("index must be an integer")
                self.instrument.write(f":SENSe:BLE:CHANnel:INDex {index}")

            def get_channel_index(self):
                """
                Parameter:
                None
                Return:
                int: The channel index.
                """
                return int(self.instrument.query(":SENSe:BLE:CHANnel:INDex?"))

            def set_channel_auto(self, state):
                """
                Parameter:
                state (int or str): 1/0 or 'ON'/'OFF' to enable/disable auto channel index.
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
                self.instrument.write(f":SENSe:BLE:CHANnel:AUTO {state}")

            def is_channel_auto(self):
                """
                Parameter:
                None
                Return:
                bool: True if auto channel index is enabled, False otherwise.
                """
                resp = self.instrument.query(":SENSe:BLE:CHANnel:AUTO?")
                return int(resp.strip()) == 1

            def set_reference_level(self, value):
                """
                Parameter:
                value (float): Reference level in dBm.
                Return:
                None
                """
                self.instrument.write(f":SENSe:BLE:POWer:RF:RLEVel {value}")

            def get_reference_level(self):
                """
                Parameter:
                None
                Return:
                float: The reference level in dBm.
                """
                return float(self.instrument.query(":SENSe:BLE:POWer:RF:RLEVel?"))

            class Trigger:
                """
                The Trigger commands control the Bluetooth Low Energy trigger settings.
                """
                def __init__(self, instrument,data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler

                def set_slength(self, value):
                    """
                    Parameter:
                    value (float): Measurement capture length in seconds.
                    Return:
                    None
                    """
                    self.instrument.write(f":TRIGger:BLE:SLENgth {value}")

                def get_slength(self):
                    """
                    Parameter:
                    None
                    Return:
                    float: The measurement capture length in seconds.
                    """
                    return float(self.instrument.query(":TRIGger:BLE:SLENgth?"))

                class Fetch:
                    """
                    The Fetch commands retrieve Bluetooth Low Energy demodulation metrics.
                    """
                    def __init__(self, instrument,data_handler):
                        self.instrument = instrument
                        self.data_handler = data_handler

                    def fetch(self, metrics):
                        """
                        Parameter:
                        metrics (int or list/tuple of int): Metric(s) to retrieve.
                        Return:
                        str: Comma separated list of metric values in order requested.
                        """
                        if isinstance(metrics, int):
                            metrics_str = str(metrics)
                        elif isinstance(metrics, (list, tuple)) and all(isinstance(m, int) for m in metrics):
                            metrics_str = ",".join(str(m) for m in metrics)
                        else:
                            raise ValueError("metrics must be an int or list/tuple of ints")
                        response = self.instrument.query(f":FETCh:BLE? {metrics_str}")
                        if self.data_handler.is_auto_saving_data_enabled():
                            self.data_handler.write_to_file(self, "BLUETOOTH_FETCH", response, file_type = EFileType.CSV, headers = None)
                        return response
        class LTE:
            """
            The LTE commands control the receiver and measurement configuration in the LTE measurement mode.
            """
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler
                self.measurement = SpectrumAnalyzer.Sense.LTE.Measurement(self.instrument)
                self.scan = SpectrumAnalyzer.Sense.LTE.Scan(self.instrument)
                self.fetch = SpectrumAnalyzer.Sense.LTE.Fetch(self.instrument)
                self.trigger = SpectrumAnalyzer.Sense.LTE.Trigger(self.instrument)
            class Measurement:
                """
                The Measurement commands configure LTE measurement mode.
                """
                def __init__(self, instrument,data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler

                def set_standard(self, standard):
                    """
                    Parameter:
                        standard (str): 'FDD', 'TDD', or 'NB'
                    Return:
                        None
                    """
                    allowed = {"FDD", "TDD", "NB"}
                    if not isinstance(standard, str) or standard.upper() not in allowed:
                        raise ValueError("standard must be one of 'FDD', 'TDD', or 'NB'")
                    self.instrument.write(f":SENSe:LTE:STANdard {standard.upper()}")

                def get_standard(self):
                    """
                    Parameter:
                        None
                    Return:
                        str: The current LTE standard.
                    """
                    return self.instrument.query(":SENSe:LTE:STANdard?")

                def set_bandwidth(self, bw):
                    """
                    Parameter:
                        bw (str): '1.4', '3', '5', '10', '15', or '20' (MHz as string)
                    Return:
                        None
                    """
                    allowed = {"1.4", "3", "5", "10", "15", "20"}
                    if not isinstance(bw, str) or bw not in allowed:
                        raise ValueError("bw must be one of '1.4', '3', '5', '10', '15', or '20'")
                    self.instrument.write(f":SENSe:LTE:BANDwidth {bw}")

                def get_bandwidth(self):
                    """
                    Parameter:
                        None
                    Return:
                        str: The current LTE bandwidth in MHz.
                    """
                    return self.instrument.query(":SENSe:LTE:BANDwidth?")

                def set_center_frequency(self, freq):
                    """
                    Parameter:
                        freq (float): Center frequency in Hz.
                    Return:
                        None
                    """
                    self.instrument.write(f":SENSe:LTE:FREQuency:CENTer {freq}")

                def get_center_frequency(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: Center frequency in Hz.
                    """
                    return float(self.instrument.query(":SENSe:LTE:FREQuency:CENTer?"))

                def set_reference_level(self, value):
                    """
                    Parameter:
                        value (float): Reference level in dBm.
                    Return:
                        None
                    """
                    self.instrument.write(f":SENSe:LTE:POWer:RF:RLEVel {value}")

                def get_reference_level(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: Reference level in dBm.
                    """
                    return float(self.instrument.query(":SENSe:LTE:POWer:RF:RLEVel?"))
            
                def set_include(self, state):
                    """
                    Parameter:
                        state (int or str): 1/0 or 'ON'/'OFF' to include single frequency measurements in cell search results.
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
                    self.instrument.write(f":SENSe:LTE:MEAS:INClude {state}")

                def is_include_enabled(self):
                    """
                    Parameter:
                        None
                    Return:
                        bool: True if single frequency measurements are included in cell search results, False otherwise.
                    """
                    resp = self.instrument.query(":SENSe:LTE:MEAS:INClude?")
                    return int(resp.strip()) == 1

            class Scan:
                """
                The Scan commands control LTE cell search and scan results.
                """
                def __init__(self, instrument,data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler

                def set_type(self, scan_type):
                    """
                    Parameter:
                        scan_type (str): 'SINGLE' or 'CONTINUOUS'
                    Return:
                        None
                    """
                    allowed = {"SINGLE", "CONTINUOUS"}
                    if not isinstance(scan_type, str) or scan_type.upper() not in allowed:
                        raise ValueError("scan_type must be 'SINGLE' or 'CONTINUOUS'")
                    self.instrument.write(f":SENSe:LTE:SCAN:TYPE {scan_type.upper()}")

                def get_type(self):
                    """
                    Parameter:
                        None
                    Return:
                        str: The current scan type.
                    """
                    return self.instrument.query(":SENSe:LTE:SCAN:TYPE?")

                def set_results_sort(self, sort):
                    """
                    Parameter:
                        sort (str): 'RSSI', 'FREQUENCY', or 'TIME'
                    Return:
                        None
                    """
                    allowed = {"RSSI", "FREQUENCY", "TIME"}
                    if not isinstance(sort, str) or sort.upper() not in allowed:
                        raise ValueError("sort must be 'RSSI', 'FREQUENCY', or 'TIME'")
                    self.instrument.write(f":SENSe:LTE:SCAN:RESults:SORT {sort.upper()}")

                def get_results_sort(self):
                    """
                    Parameter:
                        None
                    Return:
                        str: The current sort order for scan results.
                    """
                    return self.instrument.query(":SENSe:LTE:SCAN:RESults:SORT?")

                def set_results_keep(self, keep):
                    """
                    Parameter:
                        keep (str): 'LAST' or 'PEAK'
                    Return:
                        None
                    """
                    allowed = {"LAST", "PEAK"}
                    if not isinstance(keep, str) or keep.upper() not in allowed:
                        raise ValueError("keep must be 'LAST' or 'PEAK'")
                    self.instrument.write(f":SENSe:LTE:SCAN:RESults:KEEP {keep.upper()}")

                def get_results_keep(self):
                    """
                    Parameter:
                        None
                    Return:
                        str: The current keep setting for grouped scan results.
                    """
                    return self.instrument.query(":SENSe:LTE:SCAN:RESults:KEEP?")

                def set_results_group(self, state):
                    """
                    Parameter:
                        state (int or str): 1/0 or 'ON'/'OFF' to enable/disable grouping of scan results.
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
                    self.instrument.write(f":SENSe:LTE:SCAN:RESults:GROUP {state}")

                def is_results_group_enabled(self):
                    """
                    Parameter:
                        None
                    Return:
                        bool: True if grouping of scan results is enabled, False otherwise.
                    """
                    resp = self.instrument.query(":SENSe:LTE:SCAN:RESults:GROUP?")
                    return int(resp.strip()) == 1

                def set_results_max(self, value):
                    """
                    Parameter:
                        value (int): Maximum number of entries in scan results.
                    Return:
                        None
                    """
                    if not isinstance(value, int):
                        raise ValueError("value must be an integer")
                    self.instrument.write(f":SENSe:LTE:SCAN:RESults:MAX {value}")

                def get_results_max(self):
                    """
                    Parameter:
                        None
                    Return:
                        int: Maximum number of entries in scan results.
                    """
                    return int(self.instrument.query(":SENSe:LTE:SCAN:RESults:MAX?"))

                def start(self):
                    """
                    Parameter:
                        None
                    Return:
                        int: 1 if scan started.
                    """
                    return int(self.instrument.query(":SENSe:LTE:SCAN:STARt?"))

                def is_active(self):
                    """
                    Parameter:
                        None
                    Return:
                        bool: True if scan is active, False otherwise.
                    """
                    resp = self.instrument.query(":SENSe:LTE:SCAN:ACTive?")
                    return int(resp.strip()) == 1

                def stop(self):
                    """
                    Parameter:
                        None
                    Return:
                        int: 1 when scan is stopped.
                    """
                    return int(self.instrument.query(":SENSe:LTE:SCAN:STOP?"))

                def get_results_count(self):
                    """
                    Parameter:
                        None
                    Return:
                        int: Number of rows in the cell scan results table.
                    """
                    return int(self.instrument.query(":SENSe:LTE:SCAN:RESults:COUNt?"))

                def set_results_index(self, index):
                    """
                    Parameter:
                        index (int): Index into the cell scan results table.
                    Return:
                        None
                    """
                    if not isinstance(index, int):
                        raise ValueError("index must be an integer")
                    self.instrument.write(f":SENSe:LTE:SCAN:RESults:INDEX {index}")

                def get_results_index(self):
                    """
                    Parameter:
                        None
                    Return:
                        int: The current index into the cell scan results table.
                    """
                    return int(self.instrument.query(":SENSe:LTE:SCAN:RESults:INDEX?"))

                def clear_results(self):
                    """
                    Parameter:
                        None
                    Return:
                        None
                    """
                    self.instrument.write(":SENSe:LTE:SCAN:RESults:CLEar")

            class Fetch:
                """
                The Fetch commands retrieve LTE measurement results.
                """
                def __init__(self, instrument,data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler

                def fetch(self, metrics):
                    """
                    Parameter:
                        metrics (int or list/tuple of int): Metric(s) to retrieve. See documentation for valid values.
                    Return:
                        str: Comma separated list of metric values in order requested.
                    """
                    if isinstance(metrics, int):
                        metrics_str = str(metrics)
                    elif isinstance(metrics, (list, tuple)) and all(isinstance(m, int) for m in metrics):
                        metrics_str = ",".join(str(m) for m in metrics)
                    else:
                        raise ValueError("metrics must be an int or list/tuple of ints")
                    return self.instrument.query(f":FETCh:LTE? {metrics_str}")

            class Trigger:
                """
                The Trigger commands control the LTE trigger settings.
                """
                def __init__(self, instrument,data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler

                def set_slength(self, value):
                    """
                    Parameter:
                        value (float): Measurement capture length in seconds.
                    Return:
                        None
                    """
                    self.instrument.write(f":TRIGger:LTE:SLENgth {value}")

                def get_slength(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: Measurement capture length in seconds.
                    """
                    return float(self.instrument.query(":TRIGger:LTE:SLENgth?"))

                def set_if_level(self, value):
                    """
                    Parameter:
                        value (float): Trigger level in dBm.
                    Return:
                        None
                    """
                    self.instrument.write(f":TRIGger:LTE:IF:LEVel {value}")

                def get_if_level(self):
                    """
                    Parameter:
                        None
                    Return:
                        float: Trigger level in dBm.
                    """
                    return float(self.instrument.query(":TRIGger:LTE:IF:LEVel?"))

            class Fetch:
                """
                The Fetch commands retrieve LTE demodulation metrics.
                """
                def __init__(self, instrument,data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler

                def fetch(self, metrics):
                    """
                    Parameter:
                        metrics (int or list/tuple of int): Metric(s) to retrieve.
                    Return:
                        str: Comma separated list of metric values in order requested.
                    """
                    if isinstance(metrics, int):
                        metrics_str = str(metrics)
                    elif isinstance(metrics, (list, tuple)) and all(isinstance(m, int) for m in metrics):
                        metrics_str = ",".join(str(m) for m in metrics)
                    else:
                        raise ValueError("metrics must be an int or list/tuple of ints")
                    response = self.instrument.query(f":FETCh:LTE? {metrics_str}")
                    if self.data_handler.is_auto_saving_data_enabled():
                        self.data_handler.write_to_file(self, "FETCH_LTE", response, file_type = EFileType.CSV, headers = None)
                    return response
    class WLAN:
        """
        The WLAN commands control the receiver and measurement configuration in the WLAN measurement mode.
        """
        def __init__(self, instrument,data_handler):
            self.instrument = instrument
            self.data_handler = data_handler
            self.measurement = SpectrumAnalyzer.WLAN.Measurement(self.instrument)
            self.trigger = SpectrumAnalyzer.WLAN.Trigger(self.instrument)
            self.fetch = SpectrumAnalyzer.WLAN.Fetch(self.instrument)
                
        class Measurement:
            """
            The Measurement commands configure WLAN measurement mode.
            """
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler

            def set_standard(self, standard):
                """
                Parameter:
                standard (str): 'BG', 'AG', 'N20', 'N40', 'AC20', 'AC40', or 'AH'
                Return:
                None
                """
                allowed = {"BG", "AG", "N20", "N40", "AC20", "AC40", "AH"}
                if not isinstance(standard, str) or standard.upper() not in allowed:
                    raise ValueError("standard must be one of 'BG', 'AG', 'N20', 'N40', 'AC20', 'AC40', or 'AH'")
                self.instrument.write(f":SENSe:WLAN:STANdard {standard.upper()}")

            def get_standard(self):
                """
                Parameter:
                None
                Return:
                str: The current WLAN modulation standard.
                """
                return self.instrument.query(":SENSe:WLAN:STANdard?")

            def set_dsss_symbols(self, num):
                """
                Parameter:
                num (int): Number of DSSS symbols to demodulate/decode.
                Return:
                None
                """
                if not isinstance(num, int):
                    raise ValueError("num must be an integer")
                self.instrument.write(f":SENSe:WLAN:SYMbols:DSSS {num}")

            def get_dsss_symbols(self):
                """
                Parameter:
                None
                Return:
                int: Number of DSSS symbols to demodulate/decode.
                """
                return int(self.instrument.query(":SENSe:WLAN:SYMbols:DSSS?"))

            def set_psdu_decode(self, state):
                """
                Parameter:
                state (int or str): 1/0 or 'ON'/'OFF' to enable/disable OFDM PSDU decoding.
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
                self.instrument.write(f":SENSe:WLAN:PSDU:DECode {state}")

            def is_psdu_decode_enabled(self):
                """
                Parameter:
                None
                Return:
                bool: True if OFDM PSDU decoding is enabled, False otherwise.
                """
                resp = self.instrument.query(":SENSe:WLAN:PSDU:DECode?")
                return int(resp.strip()) == 1

            def set_symbol_offset(self, value):
                """
                Parameter:
                value (float): GI timing offset between -100 and 0 (%)
                Return:
                None
                """
                self.instrument.write(f":SENSe:WLAN:SYMBol:OFFSet {value}")

            def get_symbol_offset(self):
                """
                Parameter:
                None
                Return:
                float: GI timing offset between -100 and 0 (%)
                """
                return float(self.instrument.query(":SENSe:WLAN:SYMBol:OFFSet?"))

            def set_center_frequency(self, freq):
                """
                Parameter:
                freq (float): Center frequency in Hz.
                Return:
                None
                """
                self.instrument.write(f":SENSe:WLAN:FREQuency:CENTer {freq}")

            def get_center_frequency(self):
                """
                Parameter:
                None
                Return:
                float: Center frequency in Hz.
                """
                return float(self.instrument.query(":SENSe:WLAN:FREQuency:CENTer?"))

            def set_center_step(self, freq):
                """
                Parameter:
                freq (float): Center frequency step size in Hz.
                Return:
                None
                """
                self.instrument.write(f":SENSe:WLAN:FREQuency:CENTer:STEP {freq}")

            def get_center_step(self):
                """
                Parameter:
                None
                Return:
                float: Center frequency step size in Hz.
                """
                return float(self.instrument.query(":SENSe:WLAN:FREQuency:CENTer:STEP?"))

            def set_ifbw(self, freq):
                """
                Parameter:
                freq (float): IF bandwidth in Hz.
                Return:
                None
                """
                self.instrument.write(f":SENSe:WLAN:IFBW {freq}")

            def get_ifbw(self):
                """
                Parameter:
                None
                Return:
                float: IF bandwidth in Hz.
                """
                return float(self.instrument.query(":SENSe:WLAN:IFBW?"))

            def set_reference_level(self, value):
                """
                Parameter:
                value (float): Reference level in dBm.
                Return:
                None
                """
                self.instrument.write(f":SENSe:WLAN:POWer:RF:RLEVel {value}")

            def get_reference_level(self):
                """
                Parameter:
                None
                Return:
                float: Reference level in dBm.
                """
                return float(self.instrument.query(":SENSe:WLAN:POWer:RF:RLEVel?"))

        class Trigger:
            """
            The Trigger commands control the WLAN trigger settings.
            """
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler

            def set_slength(self, value):
                """
                Parameter:
                value (float): Measurement capture length in seconds.
                Return:
                None
                """
                self.instrument.write(f":TRIGger:WLAN:SLENgth {value}")

            def get_slength(self):
                """
                Parameter:
                None
                Return:
                float: Measurement capture length in seconds.
                """
                return float(self.instrument.query(":TRIGger:WLAN:SLENgth?"))

            def set_if_threshold(self, value):
                """
                Parameter:
                value (float): OFDM trigger threshold in dB.
                Return:
                None
                """
                self.instrument.write(f":TRIGger:WLAN:IF:THRESHold {value}")

            def get_if_threshold(self):
                """
                Parameter:
                None
                Return:
                float: OFDM trigger threshold in dB.
                """
                return float(self.instrument.query(":TRIGger:WLAN:IF:THRESHold?"))

            def set_if_level(self, value):
                """
                Parameter:
                value (float): DSSS video trigger level in dBm.
                Return:
                None
                """
                self.instrument.write(f":TRIGger:WLAN:IF:LEVel {value}")

            def get_if_level(self):
                """
                Parameter:
                None
                Return:
                float: DSSS video trigger level in dBm.
                """
                return float(self.instrument.query(":TRIGger:WLAN:IF:LEVel?"))

        class Fetch:
            """
            The Fetch commands retrieve WLAN demodulation metrics.
            """
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler

            def fetch(self, metrics):
                """
                Parameter:
                metrics (int or list/tuple of int): Metric(s) to retrieve.
                Return:
                str: Comma separated list of metric values in order requested.
                """
                if isinstance(metrics, int):
                    metrics_str = str(metrics)
                elif isinstance(metrics, (list, tuple)) and all(isinstance(m, int) for m in metrics):
                    metrics_str = ",".join(str(m) for m in metrics)
                else:
                    raise ValueError("metrics must be an int or list/tuple of ints")
                return self.instrument.query(f":FETCh:WLAN? {metrics_str}")
    class Trace:
        """
        The Trace commands control the user configurable traces for sweep mode.
        """
        def __init__(self, instrument,data_handler):
            self.instrument = instrument
            self.data_handler = data_handler
            self.pnoise = SpectrumAnalyzer.Trace.PNoise(self.instrument)
        class PNoise:
            """
            The PNoise commands control the user configurable traces for phase noise measurements.
            """
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler

            def select(self, trace_num):
                """
                Parameter:
                    trace_num (int): Trace index [1,6].
                Return:
                    None
                """
                if not isinstance(trace_num, int) or not (1 <= trace_num <= 6):
                    raise ValueError("trace_num must be an integer between 1 and 6")
                self.instrument.write(f":TRACe:PNoise:SELect {trace_num}")

            def get_selected(self):
                """
                Parameter:
                    None
                Return:
                    int: The currently selected trace index.
                """
                return int(self.instrument.query(":TRACe:PNoise:SELect?"))

            def set_type(self, typ):
                """
                Parameter:
                    typ (str): 'OFF', 'NORMal', 'AVERage', 'REFerence', 'MINHold', or 'MAXHold'.
                Return:
                    None
                """
                allowed = {"OFF", "NORMal", "AVERage", "REFerence", "MINHold", "MAXHold"}
                if not isinstance(typ, str) or typ.upper() not in allowed:
                    raise ValueError("typ must be one of 'OFF', 'NORMal', 'AVERage', 'REFerence', 'MINHold', or 'MAXHold'")
                self.instrument.write(f":TRACe:PNoise:TYPE {typ.upper()}")

            def get_type(self):
                """
                Parameter:
                    None
                Return:
                    str: The current trace type.
                """
                return self.instrument.query(":TRACe:PNoise:TYPE?")

            def set_average_count(self, count):
                """
                Parameter:
                    count (int): Number of traces to average together.
                Return:
                    None
                """
                if not isinstance(count, int) or count < 1:
                    raise ValueError("count must be a positive integer")
                self.instrument.write(f":TRACe:PNoise:AVERage:COUNt {count}")

            def get_average_count(self):
                """
                Parameter:
                    None
                Return:
                    int: The number of traces averaged together.
                """
                return int(self.instrument.query(":TRACe:PNoise:AVERage:COUNt?"))

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
                self.instrument.write(f":TRACe:PNoise:UPDate:STATe {state}")

            def is_update_enabled(self):
                """
                Parameter:
                    None
                Return:
                    bool: True if trace update is enabled, False otherwise.
                """
                resp = self.instrument.query(":TRACe:PNoise:UPDate:STATe?")
                return int(resp.strip()) == 1

            def set_hide_state(self, state):
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
                self.instrument.write(f":TRACe:PNoise:HIDE:STATe {state}")

            def is_hidden(self):
                """
                Parameter:
                    None
                Return:
                    bool: True if trace is hidden, False otherwise.
                """
                resp = self.instrument.query(":TRACe:PNoise:HIDE:STATe?")
                return int(resp.strip()) == 1
            
            def set_smoothing_state(self, state):
                """
                Parameter:
                    state (int or str): 1/0 or 'ON'/'OFF' to enable/disable trace smoothing.
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
                self.instrument.write(f":TRACe:PNoise:SMOothing:STATe {state}")

            def is_smoothing_enabled(self):
                """
                Parameter:
                    None
                Return:
                    bool: True if trace smoothing is enabled, False otherwise.
                """
                resp = self.instrument.query(":TRACe:PNoise:SMOothing:STATe?")
                return int(resp.strip()) == 1

            def set_smoothing_aperture(self, aperture):
                """
                Parameter:
                    aperture (float): Smoothing aperture value.
                Return:
                    None
                """
                self.instrument.write(f":TRACe:PNoise:SMOothing:APERture {aperture}")

            def get_smoothing_aperture(self):
                """
                Parameter:
                    None
                Return:
                    float: The smoothing aperture value.
                """
                return float(self.instrument.query(":TRACe:PNoise:SMOothing:APERture?"))

            def set_spur_reject_state(self, state):
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
                self.instrument.write(f":TRACe:PNoise:SPURReject:STATe {state}")

            def is_spur_reject_enabled(self):
                """
                Parameter:
                    None
                Return:
                    bool: True if spur reject is enabled, False otherwise.
                """
                resp = self.instrument.query(":TRACe:PNoise:SPURReject:STATe?")
                return int(resp.strip()) == 1
            def set_spur_reject_threshold(self, value):
                """
                Parameter:
                    value (float): Spur reject threshold in dB.
                Return:
                    None
                """
                self.instrument.write(f":TRACe:PNoise:SPURReject:THRESHold {value}")

            def get_spur_reject_threshold(self):
                """
                Parameter:
                    None
                Return:
                    float: The current spur reject threshold in dB.
                """
                return float(self.instrument.query(":TRACe:PNoise:SPURReject:THRESHold?"))
            def set_offset(self, value):
                """
                Parameter:
                    value (float): Offset in dB to immediately apply to the trace.
                Return:
                    None
                """
                self.instrument.write(f":TRACe:PNoise:OFFSet {value}")

            def get_offset(self):
                """
                Parameter:
                    None
                Return:
                    float: The current offset in dB applied to the trace.
                """
                return float(self.instrument.query(":TRACe:PNoise:OFFSet?"))

            def to(self, trace_num):
                """
                Parameter:
                    trace_num (int): Trace index [1,6] to move the current trace to.
                Return:
                    None
                """
                if not isinstance(trace_num, int) or not (1 <= trace_num <= 6):
                    raise ValueError("trace_num must be an integer between 1 and 6")
                self.instrument.write(f":TRACe:PNoise:TO {trace_num}")

            def clear(self):
                """
                Parameter:
                    None
                Return:
                    None
                """
                self.instrument.write(":TRACe:PNoise:CLEar")

            def get_data_y(self):
                """
                Parameter:
                    None
                Return:
                    str: The trace data amplitudes as comma separated values.
                """
                response = self.instrument.query(":TRACe:PNoise:DATA:Y?")
                if self.data_handler.is_auto_saving_data_enabled():
                    self.data_handler.write_to_file(self, "PNOISE_Y", response, file_type = EFileType.CSV, headers = None)
                return response

            def get_data_x(self):
                """
                Parameter:
                    None
                Return:
                    str: The trace data frequencies as comma separated values.
                """
                response = self.instrument.query(":TRACe:PNoise:DATA:X?")
                if self.data_handler.is_auto_saving_data_enabled():
                    self.data_handler.write_to_file(self, "PNOISE_X", response, file_type = EFileType.CSV, headers = None)
                return response

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
            response = self.instrument.query(":TRACe:DATA?")
            if self.data_handler.is_auto_saving_data_enabled():
                self.data_handler.write_to_file(self, "TRACE_DATA", response, file_type = EFileType.CSV, headers = None)
            return response
            
    class Record:
        """
        The Record commands control the Sweep Recording control panel in Swept Analysis mode.
        """
        def __init__(self, instrument,data_handler):
            self.instrument = instrument
            self.data_handler = data_handler
            self.sweep = SpectrumAnalyzer.Record.Sweep(self.instrument)
            self.trigger = SpectrumAnalyzer.Record.Trigger(self.instrument)
        class Sweep:
            def __init__(self, instrument):
                self.instrument = instrument
                self.decimate = SpectrumAnalyzer.Record.Sweep.Decimate(self.instrument)
                self.channelizer = SpectrumAnalyzer.Record.Sweep.Channelizer(self.instrument)
                self.zero_span = SpectrumAnalyzer.Record.Sweep.ZeroSpan(self.instrument)
            class Decimate:
                def __init__(self, instrument,data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler

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
                def __init__(self, instrument,data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler

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
                def __init__(self, instrument,data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler
                    self.capture = SpectrumAnalyzer.Record.Sweep.ZeroSpan.Capture(self.instrument)
                class Capture:
                    def __init__(self, instrument,data_handler):
                        self.instrument = instrument
                        self.data_handler = data_handler

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
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler
                self.zerospan = SpectrumAnalyzer.Record.Trigger.ZS(self.instrument)
            class ZS:
                """The ZS commands control the trigger configuration in zero-span mode."""
                def __init__(self, instrument,data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler
                    self.fetch = SpectrumAnalyzer.Record.Trigger.ZS.Fetch(self.instrument)
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
                    def __init__(self, instrument,data_handler):
                        self.instrument = instrument
                        self.data_handler = data_handler

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
                            
                            