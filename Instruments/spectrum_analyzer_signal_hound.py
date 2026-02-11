from Instruments.Instrument import Instrument
import time
import subprocess
from Instruments.EFileType import EFileType
from Instruments.EInstrument import EInstrument
import sys
import json
class SpectrumAnalyzer(Instrument):
    """Controls for Signal Hound Spectrum Analyzer."""
    def __init__(self, instrument, app, program_path, save_files_path=None):
       """Initialize the Spectrum Analyzer instrument.
       
       :param instrument: The pyvisa instrument instance.
       :type instrument: pyvisa.resources.Resource
       :param save_files_path: Optional path to save data files. If None, defaults to JSON format.
       :type save_files_path: str or None"""

       super().__init__(instrument, EInstrument.SPECTRUM_ANALYZER, save_files_path)

       self.display = Display(self.instrument, self.data_handler)
       self.format = Format(self.instrument, self.data_handler)
       self.system = System(self.instrument, self.data_handler)
       self.sense = Sense(self.instrument, self.data_handler)
       self.initiate = Initiate(self.instrument, self.data_handler)
       self.calculate = Calculate(self.instrument, self.data_handler)
       self.trace = Trace(self.instrument, self.data_handler)
       self.wlan = WLAN(self.instrument, self.data_handler)
       self.record = Record(self.instrument, self.data_handler)
       
       self.program_path = program_path
       self.app = app
    
    #Helper Functions
    def open_software(self):
        """Open the Signal Hound Spike software."""
        subprocess.Popen(['C:/Program Files/Signal Hound/Spike/Spike.exe'], shell = False)
    def disconnect(self):
        """Disconnect from the Spectrum Analyzer and close the Spike software."""
        self.app.terminate()
        super().disconnect()
        

    def _validate_line_num(self, line_num):
        """Helper to validate if line_num is within the allowed range (1-6).
        
        :param line_num: The limit line number to validate.
        :type line_num: int"""
        if not 1 <= line_num <= 6:
            raise ValueError("Limit line number must be an integer between 1 and 6.")
    def _validate_pathloss_table_num(self, table_num):
        """Helper to validate if path loss table number is within the allowed range (1-8).
        
        :param table_num: The path loss table number to validate.
        :type table_num: int"""
        if not 1 <= table_num <= 8:
            raise ValueError("Path loss table number must be an integer between 1 and 8.")
#Display
class Display:
    """
    The Display commands are used to control display-related settings.
    """
    def __init__(self, instrument,data_handler):
        """Initalize Display class.
        
        :param instrument: The pyvisa instrument instance.
        :type instrument: pyvisa.resources.Resource
        :param data_handler: Data handler instance.
        :type data_handler: DataHandler"""
        self.instrument = instrument
        self.data_handler = data_handler

    def hide(self):
        """
        Hide Spike's window.

        When set to true, hides the Spike application. The application will be hidden
        in the taskbar but will continue to be visible in the task manager. The SCPI lockout
        dialog, device connecting progress dialog, no device connected alert dialog and
        multiple devices connected alert dialog will be hidden, overriding related settings in
        the preferences menu.

        """
        self.instrument.write(f":DISP:HIDE 1")

    def show(self):
        """
        Show Spike's window. When set to false, shows the Spike application window.
        """
        self.instrument.write(f":DISP:HIDE 0")

    def is_hidden(self):
        """
        Query if Spike's window is hidden.

        :return: True if display is hidden, False otherwise.
        :rtype: bool
        """
        resp = self.instrument.query(":DISP:HIDE?")
        return resp.strip() == '1'

    def set_title(self, title):
        """
        Set the measurement title.

        :param title: The measurement title. Empty string to clear.
        :type title: str
        """
        self.instrument.write(f':DISP:ANN:TITLE "{title}"')

    def get_title(self):
        """
        Query the measurement title.

        :return: The current measurement title.
        :rtype: str
        """
        return self.instrument.query(":DISP:ANN:TITLE?")

    def clear_title(self):
        """
        Remove the measurement title.

        Remove the title. Has the same effect as setting the title with an empty string.
        """
        self.instrument.write(":DISP:ANN:CLEAR")

class Format:
    """
    The Format commands are used to set/query trace and IQ data formats.
    """
    def __init__(self, instrument,data_handler):
        """Initalize Format class.
        
        :param instrument: The pyvisa instrument instance.
        :type instrument: pyvisa.resources.Resource
        :param data_handler: Data handler instance.
        :type data_handler: DataHandler"""
        self.instrument = instrument
        self.data_handler = data_handler

    def set_trace_data_format(self, fmt):
        """
        Set the format of the returned trace data from the TRACe[:DATA]? command.

        :param fmt: 'ASCII' or 'REAL'
        :type fmt: str
        """
        allowed = {"ASCII", "REAL"}
        if fmt.upper() not in allowed:
            raise ValueError("fmt must be 'ASCII' or 'REAL'")
        self.instrument.write(f":FORM:TRAC {fmt.upper()}")

    def get_trace_data_format(self):
        """
        Query the format of the returned trace data from the TRACe[:DATA]? command.

        :return: The current trace data format.
        :rtype: str
        """
        return self.instrument.query(":FORM:TRAC?")

    def set_iq_data_format(self, fmt):
        """
        Specify the format of the returned IQ data from the FETCH:ZS? 1 command.

        :param fmt: 'ASCII' or 'BIN'
        :type fmt: str
        """
        allowed = {"ASCII", "BIN"}
        if fmt.upper() not in allowed:
            raise ValueError("fmt must be 'ASCII' or 'BIN'")
        self.instrument.write(f":FORM:IQ {fmt.upper()}")

    def get_iq_data_format(self):
        """
        Query the format of the returned IQ data from the FETCH:ZS? 1 command.

        
        :return: The current IQ data format.
        :rtype: str
        """
        return self.instrument.query(":FORM:IQ?")

class System:
    """
    The System commands are used to perform system level software actions and query information about the system.
    """
    def __init__(self, instrument,data_handler):
        """Initalize System class.
        
        :param instrument: The pyvisa instrument instance.
        :type instrument: pyvisa.resources.Resource
        :param data_handler: Data handler instance.
        :type data_handler: DataHandler"""

        self.instrument = instrument
        self.data_handler = data_handler
        self.device = self.Device_System(self.instrument, self.data_handler)
        self.error = self.Error(self.instrument, self.data_handler)
        self.instrumentmode = self.InstrumentMode(self.instrument,self.data_handler)

    def close(self):
        """
        Disconnect any active device and close the Spike software.

        This command disconnects any active device and closes the Spike software.
        It also terminates the socket connection with the Spike software.
        Note: There is not a way to reopen the software using SCPI commands.
        """
        self.instrument.write(":SYSTem:CLOSe")

    def preset(self):
        """
        Preset the active device.

        This command power cycles the active device and returns the software to the initial power-on state.
        The process can take between 6-20 seconds depending on the device type.
        """
        self.instrument.write(":SYSTem:PRESet")

    def is_preset(self):
        """
        Query if the active device is preset.

        This command closes and reopens the active device. The process can take between 6-20 seconds depending on the device type.
        Returns 1 for success, 0 otherwise.

        
        :return: True if system is preset, False otherwise.
        :rtype: bool
        """
        resp = self.instrument.query(":SYSTem:PRESet?")
        return resp.strip() == 1

    def save_user_preset(self, filename):
        """
        Save a user preset with the given file name.

        The file name should have extension ".ini".

        :param filename: The file name to save the preset. Should have extension ".ini".
        :type filename: str
        """
        if not filename.lower().endswith(".ini"):
            raise ValueError("filename must have extension '.ini'")
        self.instrument.write(f':SYSTem:PRESet:USER:SAVE "{filename}"')

    def load_user_preset(self, filename):
        """
        Load a user preset from the given file name.

        If the preset does not exist, nothing occurs. The file name should have extension ".ini".

        :param filename: The file name to load the preset. Should have extension ".ini".
        :type filename: str
        """
        if not filename.lower().endswith(".ini"):
            raise ValueError("filename must have extension '.ini'")
        self.instrument.write(f':SYSTem:PRESet:USER:LOAD "{filename}"')

    def get_version(self):
        """
        Query the Spike software version number.

        :return: The Spike software version number.
        :rtype: str
        """
        return self.instrument.query(":SYSTem:VERsion?")

    def goto_local(self):
        """
        Put Spike in local mode.
        """
        self.instrument.write(":SYSTem:COMMunicate:GTLocal")

    def save_image(self, filename):
        """
        Save an image with the specified filename.

        :param filename: The file name to save the image.
        :type filename: str
        """
        self.instrument.write(f':SYSTem:IMAGe:SAVe "{filename}"')

    def quick_save_image(self):
        """
        Quick save image.

        Same functionality as the Image quick save file menu option.
        """
        self.instrument.write(":SYSTem:IMAGe:SAVe:QUICk")

    def print_image(self):
        """
        Print with the default system print settings.
        """
        self.instrument.write(":SYSTem:PRINt")

    def get_temperature(self):
        """
        Query the current internal temperature of the active device.

        :return: The current internal temperature of the active device, in degrees Celsius.
        :rtype: float
        """
        return float(self.instrument.query(":SYSTem:TEMPerature?"))

    def get_voltage(self):
        """
        Query the measured voltage of the active device.

        :return: The measured voltage of the active device, in volts.
        :rtype: float
        """
        return float(self.instrument.query(":SYSTem:VOLTage?"))

    def get_current(self):
        """
        Query the measured current of the active device.

        :return: The measured current of the active device, in amps.
        :rtype: float
        """
        return float(self.instrument.query(":SYSTem:CURRent?"))
    def did_overflow(self):
        """
        Query if the system is in an overflow state.

        :return: True if overflow is present, False otherwise.
        :rtype: bool
        """
        resp = self.instrument.query(":SYSTem:OVERflow?")
        return resp.strip() == '1'
    class Device_System:
        """
        The Device commands allow you to remotely manage the active device in the Spike software.
        """
        def __init__(self, instrument,data_handler):
            """Initalize Device_System class.
            
            :param instrument: The pyvisa instrument instance.
            :type instrument: pyvisa.resources.Resource
            :param data_handler: Data handler instance.
            :type data_handler: DataHandler"""
            self.instrument = instrument
            self.data_handler = data_handler

        def is_active(self):
            """Returns whether or not a device is currently connected and active in the software. You can use the IDN? function to request information about the device.

            :return: True if a device is currently connected and active, False otherwise.
            :rtype: bool"""
            
            resp = self.instrument.query(":SYSTem:DEVice:ACTive?")
            return resp.strip() == '1'

        def get_count(self):
            """
            Returns the number of devices connected to the PC.
            Note: No device may be active when this function is called. You must call DISConnect? before calling this function.
            Any networked devices that have been configured will be counted in the returned value.

            :return: The number of devices connected to the PC.
            :rtype: int
            """
            return int(self.instrument.query(":SYSTem:DEVice:COUNt?"))

        def get_list(self):
            """
            Returns the connection strings for all devices available to connect in the Spike software.
            For USB devices, this is serial numbers returned as ASCII integers and comma separated.
            For networked devices, the format is SOCKET::IP::PORT (e.g., SOCKET::192.168.1.1::12345).
            Use the COUNt? function to determine how many devices are present.

            :return: The list of connected devices.
            :rtype: str
            """
            return self.instrument.query(":SYSTem:DEVice:LIST?")

        def get_current(self):
            """
            Returns the currently active device’s connection string.
            See LIST? for format.

            :return: The currently active device.
            :rtype: str
            """
            return self.instrument.query(":SYSTem:DEVice:CURRent?")

        def connect(self, device_index):
            """
            Connect a device in the Spike software.
            For USB devices, provide the serial number of the device to connect.
            For networked devices, send a string with format SOCKET::IP::PORT (e.g., SOCKET::192.168.1.1::12345).
            Returns 0 or 1 depending on if the device successfully opened.

            :param device_index: The index (serial number) or connection string of the device to connect.
            :type device_index: int or str
            """
            if isinstance(device_index, int):
                if device_index < 0:
                    raise ValueError("device_index must be a non-negative integer")
                self.instrument.write(f":SYSTem:DEVice:CONnect? {device_index}")
            elif isinstance(device_index, str):
                self.instrument.write(f":SYSTem:DEVice:CONnect? {device_index}")
            else:
                raise ValueError("device_index must be an integer or connection string")

        def is_disconnected(self):
            """
            Disconnects any device actively connected in Spike.

            :return: True if successfully disconnected, False otherwise.
            :rtype: bool
            """
            self.instrument.write(":SYSTem:DEVice:DISConnect?")
    class Error:
        """
        The Error commands allow you to query and clear system errors.
        """
        def __init__(self, instrument,data_handler):
            """Initalize Error class.
            
            :param instrument: The pyvisa instrument instance.
            :type instrument: pyvisa.resources.Resource
            :param data_handler: Data handler instance.
            :type data_handler: DataHandler"""
            self.instrument = instrument
            self.data_handler = data_handler

        def get_count(self):
            """ Returns the number of errors in the error queue
           
            :return: The number of errors in the error queue.
            :rtype: int
            """
            return int(self.instrument.query(":SYSTem:ERRor:COUNt?"))

        def get_next(self):
            """
            :return: The next error in the queue, removing it from the queue.
            :rtype: str
            """
            return self.instrument.query(":SYSTem:ERRor:NEXT?")

        def clear(self):
            """ Remove all errors from the queue, returns nothing.
            """
            self.instrument.write(":SYSTem:ERRor:CLEar")

    class InstrumentMode:
        """
        The InstrumentMode commands control the measurement mode of the Spike software.
        """
        def __init__(self, instrument,data_handler):
            """Initalize InstrumentMode class.
            
            :param instrument: The pyvisa instrument instance.
            :type instrument: pyvisa.resources.Resource
            :param data_handler: Data handler instance.
            :type data_handler: DataHandler"""

            self.instrument = instrument
            self.data_handler = data_handler

        def select(self, mode):
            """ Sets the current measurement mode.
            
            :param mode: One of 'SA', 'RTSA', 'ZS', 'HARMONICS', 'NA', 'PNOISE', 'DDEMOD', 'EMI', 'ADEMOD', 'IH', 'SEMASK', 'NFIGURE', 'WLAN', 'BLE', 'LTE'.
            :type mode: str
            """
            allowed = {
                "SA", "RTSA", "ZS", "HARMONICS", "NA", "PNOISE", "DDEMOD",
                "EMI", "ADEMOD", "IH", "SEMASK", "NFIGURE", "WLAN", "BLE", "LTE"
            }
            if mode.upper() not in allowed:
                raise ValueError("mode must be one of: " + ", ".join(allowed))
            self.instrument.write(f":INSTrument:SELect {mode.upper()}")

        def get_selected(self):
            """ Gets the current measurement mode.
            
            :return: The current measurement mode.
            :rtype: str
            """
            return self.instrument.query(":INSTrument:SELect?")

        def recalibrate(self):
            """Perform a device recalibration.
            """
            self.instrument.write(":INSTrument:RECALibrate")
class Initiate:
    """
    The Initiate commands control when measurements are performed in the application.
    """
    def __init__(self, instrument,data_handler):
        """Initalize Initiate class.
        
        :param instrument: The pyvisa instrument instance.
        :type instrument: pyvisa.resources.Resource
        :param data_handler: Data handler instance.
        :type data_handler: DataHandler"""
        self.instrument = instrument
        self.data_handler = data_handler

    def set_continuous(self, state):
        """
        Enable/Disable continuous measurement operation.

        This state is global and will affect all measurements. When enabled, measurements are
        automatically triggered after the previous measurement is finished. When disabled,
        measurements are triggered only on the IMMediate command.

        :param state: 1/0 or 'ON'/'OFF' to enable/disable continuous measurement.
        :type state: int or str
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
        Query if continuous measurement is enabled.

        :return: True if continuous measurement is enabled, False otherwise.
        :rtype: bool
        """
        resp = self.instrument.query(":INITiate:CONTinuous?")
        return resp.strip() in {1, "ON"}

    def immediate(self):
        """
        Trigger a measurement.
        Triggers a measurement. Has no effect if CONTinuous is enabled.
        """
        self.instrument.write(":INITiate:IMMediate")

class Calculate:
    """
    The Calculate commands control the limit lines in measurement modes.
    """
    def __init__(self, instrument,data_handler):
        """Initalize Calculate class.
        
        :param instrument: The pyvisa instrument instance.
        :type instrument: pyvisa.resources.Resource
        :param data_handler: Data handler instance.
        :type data_handler: DataHandler"""
        
        self.instrument = instrument
        self.data_handler = data_handler
        self.pnoise = self.PNoise_Calc(self.instrument, self.data_handler)
        self.marker = self.Marker_Calc(self.instrument, self.data_handler)
        self.math = self.Math_Calc(self.instrument, self.data_handler)
        self.limitline_1 = self.LimitLine(self.instrument, self.data_handler,1)
        self.limitline_2 = self.LimitLine(self.instrument, self.data_handler,2)
        self.limitline_3 = self.LimitLine(self.instrument, self.data_handler,3)
        self.limitline_4 = self.LimitLine(self.instrument, self.data_handler,4)
        self.limitline_5 = self.LimitLine(self.instrument, self.data_handler,5)
        self.limitline_6 = self.LimitLine(self.instrument, self.data_handler,6)
    class PNoise_Calc:
        """
        The PNoise commands control phase noise marker and jitter configuration.
        """
        def __init__(self, instrument,data_handler):
            """Initalize PNoise_Calc class.
            
            :param instrument: The pyvisa instrument instance.
            :type instrument: pyvisa.resources.Resource
            :param data_handler: Data handler instance.
            :type data_handler: DataHandler"""
            self.instrument = instrument
            self.data_handler = data_handler
            self.marker = self.Marker_PN(self.instrument, self.data_handler)
            self.jitter = self.Jitter(self.instrument, self.data_handler)

        class Marker_PN:
            """
            The Marker commands control the phase noise markers.
            """
            def __init__(self, instrument,data_handler):
                """Initalize Marker_PN class.
                
                :param instrument: The pyvisa instrument instance.
                :type instrument: pyvisa.resources.Resource
                :param data_handler: Data handler instance.
                :type data_handler: DataHandler"""
                self.instrument = instrument
                self.data_handler = data_handler

            def select(self, marker_num):
                """
                Specify the active marker index. All future operations will occur on this marker.

                :param marker_num: Marker index [1-6].
                :type marker_num: int

                """
                if not isinstance(marker_num, int) or not (1 <= marker_num <= 6):
                    raise ValueError("marker_num must be an integer between 1 and 6")
                self.instrument.write(f":CALCulate:PNoise:MARKer:SELect {marker_num}")

            def get_selected(self):
                """
                Query the currently selected marker index.
                
                :return: The currently selected marker index.
                :rtype: int
                """
                return int(self.instrument.query(":CALCulate:PNoise:MARKer:SELect?"))

            def set_state(self, state):
                """
                Enable or disable the marker.

                :param state: 1/0 or 'ON'/'OFF' to enable/disable the marker.
                :type state: int or str
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
                Query if marker is enabled.

                
                :return: True if marker is enabled, False otherwise.
                :rtype: bool
                """
                resp = self.instrument.query(":CALCulate:PNoise:MARKer:STATe?")
                return int(resp.strip()) == 1

            def set_trace(self, trace_num):
                """
                Select which trace the marker is placed on. The marker is updated immediately.

                :param trace_num: Trace index [1-3].
                :type trace_num: int
                """
                if not isinstance(trace_num, int) or not (1 <= trace_num <= 3):
                    raise ValueError("trace_num must be an integer between 1 and 3")
                self.instrument.write(f":CALCulate:PNoise:MARKer:TRACe {trace_num}")

            def get_trace(self):
                """
                Query the trace index the marker is placed on.

                
                :return: The trace index the marker is placed on.
                :rtype: int
                """
                return int(self.instrument.query(":CALCulate:PNoise:MARKer:TRACe?"))

            def set_delta(self, state):
                """
                Enable or disable the delta marker. A reference marker is created when enabled.
                Updating delta again updates the reference marker.

                :param state: 1/0 or 'ON'/'OFF' to enable/disable delta marker.
                :type state: int or str
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
                Query if delta marker is enabled.

                
                :return: True if delta marker is enabled, False otherwise.
                :rtype: bool
                """
                resp = self.instrument.query(":CALCulate:PNoise:MARKer:DELTa?")
                return int(resp.strip()) == 1

            def set_x(self, freq):
                """
                Set the marker frequency as an offset from the carrier frequency.

                :param freq: Marker frequency offset from carrier (Hz).
                :type freq: float
                """
                self.instrument.write(f":CALCulate:PNoise:MARKer:X {freq}")

            def get_x(self):
                """
                Query the frequency of the marker as a frequency offset from the carrier.
                If the reference marker is active, returns the difference between reference and current position.

                
                :return: The marker frequency offset from carrier (Hz).
                """
                return float(self.instrument.query(":CALCulate:PNoise:MARKer:X?"))

            def get_y(self):
                """
                Query the amplitude of the marker as dBc/Hz.
                If the reference marker is active, returns the dB difference between reference and current position.

                
                :return: The marker amplitude as dBc/Hz.
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
                Enable/disable the jitter measurement.

                :param state: 1/0 or 'ON'/'OFF' to enable/disable jitter measurement.
                :type state: int or str
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
                Query if jitter measurement is enabled.

                
                :return: True if jitter measurement is enabled, False otherwise.
                :rtype: bool
                """
                resp = self.instrument.query(":CALCulate:PNoise:JITTer:STATe?")
                return int(resp.strip()) == 1

            def set_trace(self, trace_num):
                """
                Specify the target trace of the jitter measurement.

                :param trace_num: Trace index [1-3].
                :type trace_num: int

                """
                if not isinstance(trace_num, int) or not (1 <= trace_num <= 3):
                    raise ValueError("trace_num must be an integer between 1 and 3")
                self.instrument.write(f":CALCulate:PNoise:JITTer:TRACe {trace_num}")

            def get_trace(self):
                """
                Query the trace index used for jitter measurement.

                
                :return: The trace index used for jitter measurement.
                :rtype: int
                """
                return int(self.instrument.query(":CALCulate:PNoise:JITTer:TRACe?"))

            def set_start(self, freq):
                """
                Specify the start frequency of the jitter measurement as an offset from the carrier frequency.

                :param freq: Start frequency offset from carrier (Hz).
                :type freq: float

                """
                self.instrument.write(f":CALCulate:PNoise:JITTer:STARt {freq}")

            def get_start(self):
                """
                Query the start frequency offset from carrier for jitter measurement.

                
                :return: Start frequency offset from carrier (Hz).
                :rtype: float
                """
                return float(self.instrument.query(":CALCulate:PNoise:JITTer:STARt?"))

            def set_stop(self, freq):
                """
                Specify the stop frequency of the jitter measurement as an offset from the carrier frequency.

                :param freq: Stop frequency offset from carrier (Hz).
                :type freq: float

                """
                self.instrument.write(f":CALCulate:PNoise:JITTer:STOP {freq}")

            def get_stop(self):
                """
                Query the stop frequency offset from carrier for jitter measurement.

                
                :return: Stop frequency offset from carrier (Hz).
                :rtype: float
                """
                return float(self.instrument.query(":CALCulate:PNoise:JITTer:STOP?"))

            def get_rms(self):
                """
                Query the RMS Jitter of the measurement in seconds.

                
                :return: RMS jitter in seconds.
                :rtype: float
                """
                return float(self.instrument.query(":CALCulate:PNoise:JITTer:RMS?"))

            def get_phase(self):
                """
                Query the Phase Jitter of the measurement in radians.

                
                :return: Phase jitter in radians.
                :rtype: float
                """
                return float(self.instrument.query(":CALCulate:PNoise:JITTer:PHASe?"))

    class Marker_Calc:
        """
        The Marker commands control the sweep markers.
        """
        def __init__(self, instrument,data_handler):
            """Initalize Marker_Calc class.
            
            :param instrument: The pyvisa instrument instance.
            :type instrument: pyvisa.resources.Resource
            :param data_handler: Data handler instance.
            :type data_handler: DataHandler"""
            self.instrument = instrument
            self.data_handler = data_handler

        def select(self, marker_num):
            """
            Select the active marker.

            :param marker_num: Marker index.
            :type marker_num: int
            """
            self.instrument.write(f":CALCulate:MARKer:SELect {marker_num}")

        def get_selected(self):
            """
            Query the currently selected marker index.

            
            :return: The currently selected marker index.
            :rtype: int
            """
            return int(self.instrument.query(":CALCulate:MARKer:SELect?"))

        def set_state(self, state):
            """
            Turn the marker on/off.

            :param state: 1/0 or 'ON'/'OFF' to enable/disable marker.
            :type state: int or str

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
            Query if marker is enabled.

            
            :return: True if marker is enabled, False otherwise.
            :rtype: bool
            """
            resp = self.instrument.query(":CALCulate:MARKer:STATe?")
            return int(resp.strip()) == 1

        def set_trace(self, trace_num):
            """
            Specify which trace to place the marker on. The trace must also be active to retrieve marker measurements.

            :param trace_num: Trace index to place marker on.
            :type trace_num: int

            """
            self.instrument.write(f":CALCulate:MARKer:TRACe {trace_num}")

        def get_trace(self):
            """
            Query the trace index the marker is placed on.

            
            :return: The trace index the marker is placed on.
            :rtype: int
            """
            return int(self.instrument.query(":CALCulate:MARKer:TRACe?"))

        def set_mode(self, mode):
            """
            Switch between positional and noise marker.

            :param mode: 'POSITION', 'NOISE', 'CHPOWER', or 'NDB'.
            :type mode: str

            """
            allowed = {"POSITION", "NOISE", "CHPOWER", "NDB"}
            if not isinstance(mode, str) or mode.upper() not in allowed:
                raise ValueError("mode must be one of 'POSITION', 'NOISE', 'CHPOWER', or 'NDB'")
            self.instrument.write(f":CALCulate:MARKer:MODE {mode.upper()}")

        def get_mode(self):
            """
            Query the current marker mode.

            
            :return: The current marker mode.
            :rtype: str
            """
            return self.instrument.query(":CALCulate:MARKer:MODE?")

        def set_update(self, state):
            """
            When update is disabled, the marker will hold its current position and will not update on future sweep updates.

            :param state: 1/0 or 'ON'/'OFF' to enable/disable marker update.
            :type state: int or str

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
            Query if marker update is enabled.

            
            :return: True if marker update is enabled, False otherwise.
            :rtype: bool
            """
            resp = self.instrument.query(":CALCulate:MARKer:UPDate?")
            return int(resp.strip()) == 1

        def set_delta(self, state):
            """
            When delta is enabled, the delta reference takes the current marker position and the marker measurement returns the delta frequency and amplitude between the current marker position and the delta reference.

            :param state: 1/0 or 'ON'/'OFF' to enable/disable delta mode.
            :type state: int or str

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
            Query if delta mode is enabled.

            
            :return: True if delta mode is enabled, False otherwise.
            :rtype: bool
            """
            resp = self.instrument.query(":CALCulate:MARKer:DELTa?")
            return int(resp.strip()) == 1

        def set_peak_track(self, state):
            """
            When enabled, the marker performs a peak search on each new trace update.

            :param state: 1/0 or 'ON'/'OFF' to enable/disable peak tracking.
            :type state: int or str

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
            Query if peak tracking is enabled.

            
            :return: True if peak tracking is enabled, False otherwise.
            :rtype: bool
            """
            resp = self.instrument.query(":CALCulate:MARKer:PKTRack?")
            return int(resp.strip()) == 1

        def set_x(self, freq):
            """
            Move the marker position to the specified frequency.

            :param freq: Frequency to move marker to (Hz).
            :type freq: float

            """
            self.instrument.write(f":CALCulate:MARKer:X {freq}")

        def get_x(self):
            """
            Retrieve the marker position frequency as Hz.

            
            :return: The marker position frequency (Hz).
            :rtype: float
            """
            return float(self.instrument.query(":CALCulate:MARKer:X?"))

        def get_y(self):
            """
            Retrieve the marker position amplitude according to marker type. Position and channel power markers return dBm, and noise markers return dBm/Hz. N dB markers also return the amplitude at their position in dBm.

            
            :return: The marker position amplitude.
            :rtype: float
            """
            return float(self.instrument.query(":CALCulate:MARKer:Y?"))

        def maximum(self):
            """
            Perform a peak search.
            """
            self.instrument.write(":CALCulate:MARKer:MAXimum")

        def maximum_next(self):
            """
            Move the marker to the next highest peak. Only peaks that meet the peak criteria are considered.
            """
            self.instrument.write(":CALCulate:MARKer:MAXimum:NEXT")

        def maximum_left(self):
            """
            Move the marker to the next peak to the left of its current position. Only peaks that meet the peak criteria are considered.
            """
            self.instrument.write(":CALCulate:MARKer:MAXimum:LEFT")

        def maximum_right(self):
            """
            Move the marker to the next peak to the right of its current position (higher frequency). Only peaks that meet the peak criteria are considered.

            

            """
            self.instrument.write(":CALCulate:MARKer:MAXimum:RIGHt")

        def minimum(self):
            """
            Perform a minimum peak search.

            

            """
            self.instrument.write(":CALCulate:MARKer:MINimum")

        def set_peak_excursion(self, value):
            """
            Specify the peak excursion in dB. How many dB above surrounding points the point must be before being considered a peak.

            :param value: Peak excursion in dB.
            :type value: float

            """
            self.instrument.write(f":CALCulate:MARKer:PEAK:EXCursion {value}")

        def get_peak_excursion(self):
            """
            Query the current peak excursion in dB.

            
            :return: The current peak excursion in dB.
            :rtype: float
            """
            return float(self.instrument.query(":CALCulate:MARKer:PEAK:EXCursion?"))

        def set_peak_threshold(self, value):
            """
            Specify the peak threshold. A point must exceed this amount before being considered as a peak. Once the threshold test is met, then the excursion test is ran. If it meets both, then a point is considered a peak.

            :param value: Peak threshold in dBm.
            :type value: float

            """
            self.instrument.write(f":CALCulate:MARKer:PEAK:THReshold {value}")

        def get_peak_threshold(self):
            """
            Returns the current threshold as dBm.

            
            :return: The current peak threshold in dBm.
            :rtype: float
            """
            return float(self.instrument.query(":CALCulate:MARKer:PEAK:THReshold?"))

        def set_chpower_width(self, freq):
            """
            Specify the width of the channel power marker measurement as a frequency.

            :param freq: Channel power marker width (Hz).
            :type freq: float

            """
            self.instrument.write(f":CALCulate:MARKer:CHPower:WIDth {freq}")

        def get_chpower_width(self):
            """
            Query the channel power marker width.

            
            :return: The channel power marker width (Hz).
            :rtype: float
            """
            return float(self.instrument.query(":CALCulate:MARKer:CHPower:WIDth?"))

        def set_ndb_offset(self, value):
            """
            Specify the offset of the N dB marker measurement in dB.

            :param value: N dB marker offset (dB).
            :type value: float

            """
            self.instrument.write(f":CALCulate:MARKer:NDB:OFFset {value}")

        def get_ndb_offset(self):
            """
            Query the N dB marker offset.

            
            :return: The N dB marker offset (dB).
            :rtype: float
            """
            return float(self.instrument.query(":CALCulate:MARKer:NDB:OFFset?"))

        def get_ndb_bandwidth(self):
            """
            Retrieve the width of the N dB band.

            
            :return: The width of the N dB band (Hz).
            :rtype: float
            """
            return float(self.instrument.query(":CALCulate:MARKer:NDB:BANDwidth?"))

        def get_ndb_rleft(self):
            """
            Retrieve the left edge frequency of the N dB band.

            
            :return: The left edge frequency of the N dB band (Hz).
            :rtype: float
            """
            return float(self.instrument.query(":CALCulate:MARKer:NDB:RLEFt?"))

        def get_ndb_rright(self):
            """
            Retrieve the right edge frequency of the N dB band.

            
            :return: The right edge frequency of the N dB band (Hz).
            :rtype: float
            """
            return float(self.instrument.query(":CALCulate:MARKer:NDB:RRIGht?"))

        def set_center(self):
            """
            Set the sweep center frequency to the current marker frequency.

            """
            self.instrument.write(":CALCulate:MARKer:SET:CENTer")

        def set_rlevel(self):
            """
            Set the sweep reference level to the current marker amplitude.

            """
            self.instrument.write(":CALCulate:MARKer:SET:RLEVel")

        def disable_all(self):
            """
            Disables all markers. All other configuration parameters of the markers remain the same.

            """
            self.instrument.write(":CALCulate:MARKer:AOFF")

    class Math_Calc:
        """
        The CalculateMath commands control trace math functions.
        """
        def __init__(self, instrument,data_handler):
            self.instrument = instrument
            self.data_handler = data_handler

        def set_state(self, state):
            """
            Enable or disable the trace math function.

            :param state: 1/0 or 'ON'/'OFF' to enable/disable trace math.

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
            Query if trace math is enabled.

            
            :return: True if trace math is enabled, False otherwise.
            """
            resp = self.instrument.query(":CALCulate:MATH:STATe?")
            return int(resp.strip()) == 1

        def set_first(self, trace_num):
            """
            Specify the first operand trace in the selected trace math function.
            Valid values are [1,6].

            :param trace_num: First operand trace [1,6].

            """
            if not isinstance(trace_num, int) or not (1 <= trace_num <= 6):
                raise ValueError("trace_num must be an integer between 1 and 6")
            self.instrument.write(f":CALCulate:MATH:FIRST {trace_num}")

        def get_first(self):
            """
            Query the first operand trace in the selected trace math function.

            
            :return: The first operand trace.
            """
            return int(self.instrument.query(":CALCulate:MATH:FIRST?"))

        def set_second(self, trace_num):
            """
            Specify the second operand trace in the selected trace math function.
            Valid values are [1,6].

            :param trace_num: Second operand trace [1,6].

            """
            if not isinstance(trace_num, int) or not (1 <= trace_num <= 6):
                raise ValueError("trace_num must be an integer between 1 and 6")
            self.instrument.write(f":CALCulate:MATH:SECond {trace_num}")

        def get_second(self):
            """
            Query the second operand trace in the selected trace math function.

            
            :return: The second operand trace.
            """
            return int(self.instrument.query(":CALCulate:MATH:SECond?"))

        def set_result(self, trace_num):
            """
            Specify the result trace in the selected trace math function.
            Valid values are [1,6].

            :param trace_num: Result trace [1,6].

            """
            if not isinstance(trace_num, int) or not (1 <= trace_num <= 6):
                raise ValueError("trace_num must be an integer between 1 and 6")
            self.instrument.write(f":CALCulate:MATH:RESult {trace_num}")

        def get_result(self):
            """
            Query the result trace in the selected trace math function.

            
            :return: The result trace.
            """
            return int(self.instrument.query(":CALCulate:MATH:RESult?"))

        def set_operation(self, op):
            """
            Specify the trace math function.

            :param op: 'PDIFF', 'PSUM', 'LOFFSET', or 'LDIFF'.

            """
            allowed = {"PDIFF", "PSUM", "LOFFSET", "LDIFF"}
            if not isinstance(op, str) or op.upper() not in allowed:
                raise ValueError("op must be one of 'PDIFF', 'PSUM', 'LOFFSET', or 'LDIFF'")
            self.instrument.write(f":CALCulate:MATH:OP {op.upper()}")

        def get_operation(self):
            """
            Query the current trace math operation.

            
            :return: The current trace math operation.
            """
            return self.instrument.query(":CALCulate:MATH:OP?")

        def set_offset(self, value):
            """
            Specify the offset to use in the logarithm trace math functions.

            :param value: Offset for logarithm trace math functions.

            """
            self.instrument.write(f":CALCulate:MATH:OFFSet {value}")

        def get_offset(self):
            """
            Query the current offset for logarithm trace math functions.

            
            :return: The current offset for logarithm trace math functions.
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

        def enable_testing(self, state):
            """
            Enable testing of this limit line. If there are not at least 2 points in
            the limit line, testing doesn’t occur despite being enabled.


            """

            self.instrument.write(f":CALCulate:LLINe{self.line_num}:STATe ON")
        def disable_testing(self, state):
            """
            Disable testing of this limit line. If there are not at least 2 points in
            the limit line, testing doesn’t occur despite being enabled.


            """

            self.instrument.write(f":CALCulate:LLINe{self.line_num}:STATe OFF")
        def is_enabled(self):
            """
            Query if limit line testing is enabled.

            
            :return: True if limit line testing is enabled, False otherwise.
            """
            resp = self.instrument.query(f":CALCulate:LLINe{self.line_num}:STATe?")
            return resp.strip() in {1, "ON"}

        def set_title(self, title):
            """
            Specify the name of the limit line.

            :param title: The name of the limit line.

            """
            self.instrument.write(f':CALCulate:LLINe{self.line_num}:TITLe "{title}"')

        def get_title(self):
            """
            Query the current name of the limit line.

            
            :return: The current name of the limit line.
            """
            return self.instrument.query(f":CALCulate:LLINe{self.line_num}:TITLe?")

        def set_trace(self, trace_num):
            """
            Specify which trace is tested against this limit line.

            :param trace_num: The trace number to test against this limit line.

            """
            if not isinstance(trace_num, int):
                raise ValueError("trace_num must be an integer")
            self.instrument.write(f":CALCulate:LLINe{self.line_num}:TRACe {trace_num}")

        def get_trace(self):
            """
            Query the trace number tested against this limit line.

            
            :return: The trace number tested against this limit line.
            """
            return int(self.instrument.query(f":CALCulate:LLINe{self.line_num}:TRACe?"))

        def set_type(self, typ):
            """
            Specify whether the limit line is tested as an upper bound or lower bound.

            :param typ: 'UPPER' or 'LOWER'

            """
            allowed = {"UPPER", "LOWER"}
            if typ.upper() not in allowed:
                raise ValueError("typ must be 'UPPER' or 'LOWER'")
            self.instrument.write(f":CALCulate:LLINe{self.line_num}:TYPE {typ.upper()}")

        def get_type(self):
            """
            Query the type of the limit line ('UPPER' or 'LOWER').

            
            :return: The type of the limit line ('UPPER' or 'LOWER').
            """
            return self.instrument.query(f":CALCulate:LLINe{self.line_num}:TYPE?")

        def set_reference(self, ref):
            """
            Specify whether the limit line values are fixed/absolute or relative to the
            center frequency and ref level.

            :param ref: 'FIXED' or 'RELATIVE'

            """
            allowed = {"FIXED", "RELATIVE"}
            if ref.upper() not in allowed:
                raise ValueError("ref must be 'FIXED' or 'RELATIVE'")
            self.instrument.write(f":CALCulate:LLINe{self.line_num}:REFerence {ref.upper()}")

        def get_reference(self):
            """
            Query the reference type of the limit line.

            
            :return: The reference type of the limit line.
            """
            return self.instrument.query(f":CALCulate:LLINe{self.line_num}:REFerence?")

        def transform_reference(self):
            """
            Convert the limit line reference type between fixed and
            relative by recalculating points based on the current configuration.

            

            """
            self.instrument.write(f":CALCulate:LLINe{self.line_num}:REFerence:TRANsform")

        def set_interpolate(self, interp):
            """
            Specify whether the limit line uses linear or logarithmic interpolation.

            :param interp: 'LINEAR' or 'LOGARITHMIC'

            """
            allowed = {"LINEAR", "LOGARITHMIC"}
            if interp.upper() not in allowed:
                raise ValueError("interp must be 'LINEAR' or 'LOGARITHMIC'")
            self.instrument.write(f":CALCulate:LLINe{self.line_num}:INTerpolate {interp.upper()}")

        def get_interpolate(self):
            """
            Query the interpolation type of the limit line.

            
            :return: The interpolation type of the limit line.
            """
            return self.instrument.query(f":CALCulate:LLINe{self.line_num}:INTerpolate?")

        def enable_pause(self):
            """
            When enabled, a failure of this limit will pause the sweep update.


            """
            
            self.instrument.write(f":CALCulate:LLINe{self.line_num}:PAUSe:STATe ON")
        def disable_pause(self):
            """
            When enabled, a failure of this limit will pause the sweep update.


            """
            
            self.instrument.write(f":CALCulate:LLINe{self.line_num}:PAUSe:STATe OFF")
        def is_pause_enabled(self):
            """
            Query if pause on failure is enabled.

            
            :return: True if pause on failure is enabled, False otherwise.
            """
            resp = self.instrument.query(f":CALCulate:LLINe{self.line_num}:PAUSe:STATe?")
            return resp.strip() in {1, "ON"}

        def _display_line(self, state):
            """
            When enabled, the limit line will be visible on the graticule.

            :param state: 1/0 or 'ON'/'OFF' to enable/disable line display.

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
            Query if line display is enabled.

            
            :return: True if line display is enabled, False otherwise.
            """
            resp = self.instrument.query(f":CALCulate:LLINe{self.line_num}:DISPlay:LINE:STATe?")
            return resp.strip() in {1, "ON"}

        def enable_display_result(self):
            """
            When enabled, the limit line pass/fail result will be
            visible on the graticule.


            """

            self.instrument.write(f":CALCulate:LLINe{self.line_num}:DISPlay:RESult:STATe ON")
        def disable_display_result(self):
            """
            When disabled, the limit line pass/fail result will not be
            visible on the graticule.


            """

            self.instrument.write(f":CALCulate:LLINe{self.line_num}:DISPlay:RESult:STATe OFF")
        def is_display_result_enabled(self):
            """
            Query if result display is enabled.

            
            :return: True if result display is enabled, False otherwise.
            """
            resp = self.instrument.query(f":CALCulate:LLINe{self.line_num}:DISPlay:RESult:STATe?")
            return resp.strip() in {1, "ON"}

        def set_offset_y(self, offset):
            """
            Specify a dB offset to the limit line.

            :param offset: dB offset to the limit line.

            """
            self.instrument.write(f":CALCulate:LLINe{self.line_num}:OFFSet:Y {offset}")

        def get_offset_y(self):
            """
            Query the dB offset of the limit line.

            
            :return: The dB offset of the limit line.
            """
            return float(self.instrument.query(f":CALCulate:LLINe{self.line_num}:OFFSet:Y?"))

        def set_build_points(self, num_points):
            """
            Specify how many points to use when building limit line from trace.

            :param num_points: Number of points to use when building limit line from trace.

            """
            if not isinstance(num_points, int):
                raise ValueError("num_points must be an integer")
            self.instrument.write(f":CALCulate:LLINe{self.line_num}:BUILD:POINts {num_points}")

        def get_build_points(self):
            """
            Query the number of points used when building limit line from trace.

            
            :return: Number of points used when building limit line from trace.
            """
            return int(self.instrument.query(f":CALCulate:LLINe{self.line_num}:BUILD:POINts?"))

        def build(self):
            """
            Build limit line points from trace, max holding across frequency sections.

            

            """
            self.instrument.write(f":CALCulate:LLINe{self.line_num}:BUILD")

        def get_points_count(self):
            """
            Returns the number of points in the limit line as an integer.

            
            :return: Number of points in the limit line.
            """
            return int(self.instrument.query(f":CALCulate:LLINe{self.line_num}:POINts?"))

        def set_data(self, points):
            """
            Specify the points in the limit line, will override any existing points. Points are
            specified as freq/amplitude pairs where the amplitude is specified as dBm.

            :param points: List of (freq, ampl) pairs.

            """
            if not isinstance(points, list) or not all(isinstance(p, tuple) and len(p) == 2 for p in points):
                raise ValueError("points must be a list of (freq, ampl) tuples")
            data_str = ", ".join(f"{freq},{ampl}" for freq, ampl in points)
            self.instrument.write(f":CALCulate:LLINe{self.line_num}:DATA {data_str}")

        def get_data(self):
            """
            Returns the points in the limit line. Points are returned as freq/amplitude
            pairs where the frequencies are specified as Hz and the amplitudes as dBm.

            
            :return: The points in the limit line as freq/ampl pairs.
            """
            return self.instrument.query(f":CALCulate:LLINe{self.line_num}:DATA?")

        def is_failed(self):
            """
            Returns 1 when the limit test has failed, 0 if passed.

            
            :return: True if the limit test has failed, False otherwise.
            """
            resp = self.instrument.query(f":CALCulate:LLINe{self.line_num}:FAIL?")
            return resp.strip() == 1

        def clear(self):
            """
            Resets the selected limit line. Removes all points stored.

            

            """
            self.instrument.write(f":CALCulate:LLINe{self.line_num}:CLEAr")

        def clear_all_limit_lines(self):
            """
            Resets all limit lines. Removes all points stored.

            

            """
            self.instrument.write(":CALCulate:LLINe:ALL:CLEAr")

class Sense:
    def __init__(self, instrument,data_handler):
        self.instrument = instrument
        self.data_handler = data_handler
        self.harmonics = self.Harmonics(self.instrument, self.data_handler)
        self.ademod = self.ADEMod(self.instrument, self.data_handler)
        self.ddemod = self.DDEMod(self.instrument, self.data_handler)
        self.sweep_configuration = self.Sweep_Configuration(self.instrument, self.data_handler)
        self.na = self.NA(self.instrument, self.data_handler)
        self.vco = self.VCO_Sense(self.instrument, self.data_handler)
        self.audio = self.Audio(self.instrument, self.data_handler)
        self.pnoise = self.PNoise_Sense(self.instrument, self.data_handler)
        self.peaktable = self.PeakTable(self.instrument, self.data_handler)
        self.chpower = self.ChPower(self.instrument, self.data_handler)
        self.pathloss_1 = self.Pathloss(self.instrument, self.data_handler, 1)
        self.pathloss_2 = self.Pathloss(self.instrument, self.data_handler, 2)
        self.pathloss_3 = self.Pathloss(self.instrument, self.data_handler, 3)
        self.pathloss_4 = self.Pathloss(self.instrument, self.data_handler, 4)
        self.pathloss_5 = self.Pathloss(self.instrument, self.data_handler, 5)
        self.pathloss_6 = self.Pathloss(self.instrument, self.data_handler, 6)
        self.pathloss_7 = self.Pathloss(self.instrument, self.data_handler, 7)
        self.pathloss_8 = self.Pathloss(self.instrument, self.data_handler, 8)
        self.frequency = self.Frequency_Sense(self.instrument, self.data_handler)
        self.power = self.Power(self.instrument, self.data_handler)
        self.bandwidth = self.Bandwidth_Sense(self.instrument, self.data_handler)
        self.sweep = self.Sweep_Sense(self.instrument, self.data_handler)
        self.semask = self.SEMask(self.instrument, self.data_handler)
        self.nfigure = self.NFIGure(self.instrument, self.data_handler)
        self.bluetooth = self.Bluetooth(self.instrument, self.data_handler)
        self.lte = self.LTE(self.instrument, self.data_handler)
        self.occupied_bandwidth = self.Occupied_Bandwidth(self.instrument, self.data_handler)
        self.intermodulation_distort = self.IntermodulationDistortion(self.instrument, self.data_handler)
    def set_reference_oscillator_source(self, source):
        """
        :param source: 'INTERNAL', 'EXTERNAL', or 'OUT'.

        """
        allowed = {"INTERNAL", "EXTERNAL", "OUT"}
        if not isinstance(source, str) or source.upper() not in allowed:
            raise ValueError("source must be one of 'INTERNAL', 'EXTERNAL', or 'OUT'")
        self.instrument.write(f":SENSe:ROSCillator:SOURce {source.upper()}")

    def get_reference_oscillator_source(self):
        """
        
        :return: The current reference oscillator source.
        """
        return self.instrument.query(":SENSe:ROSCillator:SOURce?")
    class IntermodulationDistortion:
        """
        The Intermodulation Distortion (IMD) commands control the IMD measurement mode.
        """
        def __init__(self, instrument, data_handler):
            self.instrument = instrument
            self.data_handler = data_handler

        def enable(self):
            """
            Enable the intermodulation distortion measurement.

        

            """

            self.instrument.write(f":SENSe:IMD:STATe ON")
        def disable(self):
            """
            Disable the intermodulation distortion measurement.

            """
            self.instrument.write(f":SENSe:IMD:STATe OFF")
        def is_enabled(self):
            """
            Query if IMD measurement is enabled.

            :return:  True if enabled, False otherwise.
            """
            resp = self.instrument.query(":SENSe:IMD:STATe?")
            return int(resp.strip()) == 1

        def get_frequency(self, product):
            """
            Returns the frequency of the specified intermodulation product.

            :param product: 'F1', 'F2', 'IM3L', or 'IM3U'
            :return: Frequency in Hz.
            """
            allowed = {"F1", "F2", "IM3L", "IM3U"}
            if not isinstance(product, str) or product.upper() not in allowed:
                raise ValueError("product must be one of 'F1', 'F2', 'IM3L', or 'IM3U'")
            return float(self.instrument.query(f":SENSe:IMD:FREQuency? {product.upper()}"))

        def get_tonal_power(self, product):
            """
            Returns the tonal power in dBm of the specified intermodulation product.

            :param product: 'F1', 'F2', 'IM3L', or 'IM3U'
            :return: Power in dBm.
            """
            allowed = {"F1", "F2", "IM3L", "IM3U"}
            if not isinstance(product, str) or product.upper() not in allowed:
                raise ValueError("product must be one of 'F1', 'F2', 'IM3L', or 'IM3U'")
            return float(self.instrument.query(f":SENSe:IMD:TPOWer? {product.upper()}"))

        def get_tonal_power_diff(self, product):
            """
            Returns the tonal power difference in dBc between the specified third order product and its corresponding first order product.

            :param product: 'IM3L' or 'IM3U'
            :return: Power difference in dBc.
            """
            allowed = {"IM3L", "IM3U"}
            if not isinstance(product, str) or product.upper() not in allowed:
                raise ValueError("product must be 'IM3L' or 'IM3U'")
            return float(self.instrument.query(f":SENSe:IMD:TPOWer:DIFF? {product.upper()}"))

        def get_toi(self, product):
            """
            Returns the third-order intercept in dBm of the specified third order product.

            :param product: 'IM3L' or 'IM3U'
            :return: Third-order intercept in dBm.
            """
            allowed = {"IM3L", "IM3U"}
            if not isinstance(product, str) or product.upper() not in allowed:
                raise ValueError("product must be 'IM3L' or 'IM3U'")
            return float(self.instrument.query(f":SENSe:IMD:TOI? {product.upper()}"))
    class Occupied_Bandwidth:
        """
        The Occupied Bandwidth commands control the occupied bandwidth measurement.
        """
        def __init__(self, instrument, data_handler):
            self.instrument = instrument
            self.data_handler = data_handler

        def enable(self):
            """
            Enable the occupied bandwidth measurement.


            """
            
            self.instrument.write(f":SENSe:OBWidth:STATe ON")
        def disable(self):
            """
            Disable the occupied bandwidth measurement.


            """
            
            self.instrument.write(f":SENSe:OBWidth:STATe ON")
        def is_enabled(self):
            """
            Query if occupied bandwidth measurement is enabled.

            :return:  True if enabled, False otherwise.
            """
            resp = self.instrument.query(":SENSe:OBWidth:STATe?")
            return int(resp.strip()) == 1

        def set_trace(self, trace_num):
            """
            Specify which trace the occupied bandwidth measurement is performed on.

            :param trace_num: Trace index.

            """
            if not isinstance(trace_num, int):
                raise ValueError("trace_num must be an integer")
            self.instrument.write(f":SENSe:OBWidth:TRACe {trace_num}")

        def get_trace(self):
            """
            Query which trace is used for occupied bandwidth measurement.

            :return: The trace index.
            """
            return int(self.instrument.query(":SENSe:OBWidth:TRACe?"))

        def set_percent(self, percent):
            """
            Specify the percent of total energy for the occupied bandwidth measurement.

            :param percent: Percent value.

            """
            self.instrument.write(f":SENSe:OBWidth:PERCent {percent}")

        def get_percent(self):
            """
            Query the percent of total energy for the occupied bandwidth measurement.

            :return: Percent value.
            """
            return float(self.instrument.query(":SENSe:OBWidth:PERCent?"))

        def get_obwidth(self):
            """
            Returns the bandwidth of the occupied bandwidth measurement as Hz.

            :return: Occupied bandwidth in Hz.
            """
            return float(self.instrument.query(":SENSe:OBWidth:OBWidth?"))

        def get_center(self):
            """
            Returns the center frequency of the occupied bandwidth measurement as Hz.

            :return: Center frequency in Hz.
            """
            return float(self.instrument.query(":SENSe:OBWidth:CENTer?"))

        def get_power(self):
            """
            Returns the power of the occupied bandwidth measurement.

            :return: Power value.
            """
            return float(self.instrument.query(":SENSe:OBWidth:POWer?"))
    class Harmonics:
        """
        The Sense:Harmonics commands configure harmonic measurements.
        """
        def __init__(self, instrument,data_handler):
            self.instrument = instrument
            self.data_handler = data_handler

        def set_number(self, num):
            """
            Specify the number of harmonics to be measured and displayed on screen.

            :param num: Number of harmonics to measure and display.

            """
            if not isinstance(num, int):
                raise ValueError("num must be an integer")
            self.instrument.write(f":SENSe:HARMonics:NUMBer {num}")

        def get_number(self):
            """
            Query the number of harmonics measured and displayed.

            
            :return: Number of harmonics measured and displayed.
            """
            return int(self.instrument.query(":SENSe:HARMonics:NUMBer?"))

        def enable_tracking(self, state):
            """
            Enable fundamental tracking. When enabled, the fundamental frequency is tracked.
            In peak mode, the peak frequency is used; in channel power mode, the center of the occupied bandwidth is tracked.
            Harmonics are measured at multiples of the measured fundamental, which is always drawn centered.


            """

            self.instrument.write(f":SENSe:HARMonics:TRACKing:STATe ON")
        def disable_tracking(self):
            """
            Disable fundamental tracking."""
            self.instrument.write(f":SENSe:HARMonics:TRACKing:STATe OFF")
        def is_tracking_enabled(self):
            """
            Query if fundamental tracking is enabled.

            
            :return:  True if fundamental tracking is enabled, False otherwise.
            """
            resp = self.instrument.query(":SENSe:HARMonics:TRACKing:STATe?")
            return int(resp.strip()) == 1

        def set_mode(self, mode):
            """
            Specify the measurement mode for harmonics peak amplitude.
            'PEAK' performs a peak search algorithm on the measured span.
            'CHPOWER' measures channel power over the entire measured harmonic span.

            :param mode: 'PEAK' or 'CHPOWER'.

            """
            allowed = {"PEAK", "CHPOWER"}
            if not isinstance(mode, str) or mode.upper() not in allowed:
                raise ValueError("mode must be 'PEAK' or 'CHPOWER'")
            self.instrument.write(f":SENSe:HARMonics:MODE {mode.upper()}")

        def get_mode(self):
            """
            Query the current harmonic measurement mode.

            
            :return: The current harmonic measurement mode.
            """
            return self.instrument.query(":SENSe:HARMonics:MODE?")

        def set_fundamental(self, freq):
            """
            Specify the center frequency of the 1st harmonic (fundamental).

            :param freq: Center frequency of the 1st harmonic (Hz), or 'UP', or 'DOWN'.

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
            Query the center frequency of the 1st harmonic (fundamental).

            
            :return: Center frequency of the 1st harmonic (Hz).
            """
            return float(self.instrument.query(":SENSe:HARMonics:FREQuency:FUNDamental?"))

        def set_step_increment(self, freq):
            """
            Specify the step frequency for the fundamental frequency.

            :param freq: Step frequency for fundamental (Hz).

            """
            self.instrument.write(f":SENSe:HARMonics:FREQuency:STEP:INCRement {freq}")

        def get_step_increment(self):
            """
            Query the step frequency for the fundamental frequency.

            
            :return: Step frequency for fundamental (Hz).
            """
            return float(self.instrument.query(":SENSe:HARMonics:FREQuency:STEP:INCRement?"))

        def set_span(self, freq):
            """
            Specify the span of each measurement window at each harmonic.

            :param freq: Span of each measurement window at each harmonic (Hz).

            """
            self.instrument.write(f":SENSe:HARMonics:FREQuency:SPAN {freq}")

        def get_span(self):
            """
            Query the span of each measurement window at each harmonic.

            
            :return: Span of each measurement window at each harmonic (Hz).
            """
            return float(self.instrument.query(":SENSe:HARMonics:FREQuency:SPAN?"))

        def set_bandwidth_resolution(self, freq):
            """
            Specify the resolution bandwidth (RBW) of the measurement at each harmonic.

            :param freq: RBW at each harmonic (Hz).

            """
            self.instrument.write(f":SENSe:HARMonics:BANDwidth:RESolution {freq}")

        def get_bandwidth_resolution(self):
            """
            Query the resolution bandwidth (RBW) at each harmonic.

            
            :return: RBW at each harmonic (Hz).
            """
            return float(self.instrument.query(":SENSe:HARMonics:BANDwidth:RESolution?"))

        def set_bandwidth_video(self, freq):
            """
            Specify the video bandwidth (VBW) of the measurement at each harmonic.

            :param freq: VBW at each harmonic (Hz).

            """
            self.instrument.write(f":SENSe:HARMonics:BANDwidth:VIDeo {freq}")

        def get_bandwidth_video(self):
            """
            Query the video bandwidth (VBW) at each harmonic.

            
            :return: VBW at each harmonic (Hz).
            """
            return float(self.instrument.query(":SENSe:HARMonics:BANDwidth:VIDeo?"))

        def set_power_rf_rlevel(self, value):
            """
            Specify the measurement reference level as dBm.
            This value should be greater than the expected input power to prevent IF/ADC overload.

            :param value: Measurement reference level as dBm.

            """
            self.instrument.write(f":SENSe:HARMonics:POWer:RF:RLEVel {value}")

        def get_power_rf_rlevel(self):
            """
            Query the measurement reference level as dBm.

            
            :return: Measurement reference level as dBm.
            """
            return float(self.instrument.query(":SENSe:HARMonics:POWer:RF:RLEVel?"))

        def set_view_rlevel(self, value):
            """
            Specify the plot reference level as dBm. This affects only the plot y-axis.

            :param value: Plot reference level as dBm.

            """
            self.instrument.write(f":SENSe:HARMonics:VIEW:RLEVel {value}")

        def get_view_rlevel(self):
            """
            Query the plot reference level as dBm.

            
            :return: Plot reference level as dBm.
            """
            return float(self.instrument.query(":SENSe:HARMonics:VIEW:RLEVel?"))

        def set_view_pdivision(self, value):
            """
            Specify the division height of the plot in dB. The division height is 1/10th of the plot height.

            :param value: Plot division height in dB.

            """
            self.instrument.write(f":SENSe:HARMonics:VIEW:PDIVision {value}")

        def get_view_pdivision(self):
            """
            Query the division height of the plot in dB.

            
            :return: Plot division height in dB.
            """
            return float(self.instrument.query(":SENSe:HARMonics:VIEW:PDIVision?"))

        def set_trace_type(self, typ):
            """
            Specify the trace behavior.

            :param typ: 'WRITE' or 'MAXHOLD'.

            """
            allowed = {"WRITE", "MAXHOLD"}
            if not isinstance(typ, str) or typ.upper() not in allowed:
                raise ValueError("typ must be 'WRITE' or 'MAXHOLD'")
            self.instrument.write(f":SENSe:HARMonics:TRACe:TYPE {typ.upper()}")

        def get_trace_type(self):
            """
            Query the trace behavior type.

            
            :return: The trace behavior type.
            """
            return self.instrument.query(":SENSe:HARMonics:TRACe:TYPE?")
        def fetch_frequency(self, harmonic_num):
            """
            Fetch the specified harmonic's peak frequency in Hz.

            :param harmonic_num: The harmonic number to fetch frequency for.
            :return: The specified harmonic's peak frequency in Hz.
            """
            if not isinstance(harmonic_num, int) or harmonic_num < 1:
                raise ValueError("harmonic_num must be a positive integer")
            return float(self.instrument.query(f":SENSe:FETCh:HARMonics:FREQuency? {harmonic_num}"))

        def fetch_amplitude(self, harmonic_num):
            """
            Fetch the specified harmonic's amplitude in dBm.

            :param harmonic_num: The harmonic number to fetch amplitude for.
            :return: The specified harmonic's amplitude in dBm.
            """
            if not isinstance(harmonic_num, int) or harmonic_num < 1:
                raise ValueError("harmonic_num must be a positive integer")
            return float(self.instrument.query(f":SENSe:FETCh:HARMonics:AMPLitude? {harmonic_num}"))

        def fetch_distortion(self):
            """
            Fetch the measured total harmonic distortion in percent.

            
            :return: The measured total harmonic distortion in percent.
            """
            return float(self.instrument.query(":SENSe:FETCh:HARMonics:DISTortion?"))
    class ADEMod:
        """
        The Sense:ADEMod commands configure analog demodulation measurements.
        """
        def __init__(self, instrument,data_handler):
            self.instrument = instrument
            self.data_handler = data_handler
            self.fetch = self.Fetch_ADE(self.instrument, self.data_handler)
        def set_center_frequency(self, freq):
            """
            Specify the measurement center frequency.

            :param freq: Center frequency in Hz, or 'UP', or 'DOWN'.

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
            Query the measurement center frequency.

            
            :return: The measurement center frequency in Hz.
            """
            return float(self.instrument.query(":SENSe:ADEMod:FREQuency:CENTer?"))

        def set_center_step(self, freq):
            """
            Specify the center frequency step amount when using the UP|DOWN parameters.

            :param freq: Step amount for center frequency changes in Hz.

            """
            self.instrument.write(f":SENSe:ADEMod:FREQuency:CENTer:STEP {freq}")

        def get_center_step(self):
            """
            Query the center frequency step size.

            
            :return: The center frequency step size in Hz.
            """
            return float(self.instrument.query(":SENSe:ADEMod:FREQuency:CENTer:STEP?"))

        def set_reference_level(self, amplitude):
            """
            Specify the measurement reference level. This should be larger than the highest expected input power.

            :param amplitude: Reference level in dBm.

            """
            self.instrument.write(f":SENSe:ADEMod:POWer:RF:RLEVel {amplitude}")

        def get_reference_level(self):
            """
            Query the measurement reference level.

            
            :return: The measurement reference level in dBm.
            """
            return float(self.instrument.query(":SENSe:ADEMod:POWer:RF:RLEVel?"))

        def set_lpfilter(self, freq):
            """
            Specify the analog low pass filter cutoff frequency.

            :param freq: Analog low pass filter cutoff frequency in Hz.

            """
            self.instrument.write(f":SENSe:ADEMod:LPFilter {freq}")

        def get_lpfilter(self):
            """
            Query the analog low pass filter cutoff frequency.

            
            :return: The analog low pass filter cutoff frequency in Hz.
            """
            return float(self.instrument.query(":SENSe:ADEMod:LPFilter?"))

        class Fetch_ADE:
            """
            The Fetch commands retrieve analog demodulation measurement results.
            """
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler

            def am(self, metrics):
                """
                Fetch AM demodulation metrics.

                AM? returns AM demodulation metrics. The integer parameter specifies the metric to retrieve.
                Possible integer values:
                1. Carrier frequency in Hz
                2. Carrier power in dBm
                3. AM modulation rate in Hz
                4. AM Depth (RMS) as %
                5. AM Depth (Peak+) as %
                6. AM Depth (Peak-) as %
                7. AM SINAD as dB
                8. AM THD as %
                Can specify a list of metrics to request as a comma separated list. The metrics will be returned as a comma separated list in the order they were requested.

                :param metrics: Metric(s) to retrieve for AM demodulation.
                :type metrics: int or list of int
                :return: Comma separated list of metric values in order requested.
                :rtype: str
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

            def fm(self, metrics):
                """
                Fetch FM demodulation metrics.

                FM? returns FM demodulation metrics. The integer parameter specifies the metric to retrieve.
                Possible integer values:
                1. Carrier frequency in Hz
                2. Carrier power in dBm
                3. FM modulation rate in Hz
                4. FM Depth (RMS) in Hz
                5. FM Depth (Peak+) in Hz
                6. FM Depth (Peak-) in Hz
                7. FM SINAD as dB
                Can specify a list of metrics to request as a comma separated list. The metrics will be returned as a comma separated list in the order they were requested.

                :param metrics: Metric(s) to retrieve for FM demodulation.
                :type metrics: int or list of int
                :return: Comma separated list of metric values in order requested.
                :rtype: str
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
            self.custom = self.Custom(self.instrument, self.data_handler)
            self.trigger = self.Trigger_DDE(self.instrument, self.data_handler)
            self.sync = self.Sync(self.instrument, self.data_handler)
            self.compensate = self.Compensate(self.instrument, self.data_handler)
            self.equalization = self.Equalization(self.instrument, self.data_handler)
            self.trace = self.Trace_DDE(self.instrument, self.data_handler)
            self.fetch = self.Fetch_DDE(self.instrument, self.data_handler)
        def set_center_frequency(self, freq):
            """
            Set the center frequency of the measurement.

            :param freq: Center frequency in Hz, or 'UP', or 'DOWN'.

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
            Query the center frequency of the measurement.

            
            :return: The measurement center frequency in Hz.
            """
            return float(self.instrument.query(":SENSe:DDEMod:FREQuency:CENTer?"))

        def set_center_step(self, freq):
            """
            Set the center frequency step amount.

            :param freq: Step amount for center frequency changes in Hz.

            """
            self.instrument.write(f":SENSe:DDEMod:FREQuency:CENTer:STEP {freq}")

        def get_center_step(self):
            """
            Query the center frequency step size.

            
            :return: The center frequency step size in Hz.
            """
            return float(self.instrument.query(":SENSe:DDEMod:FREQuency:CENTer:STEP?"))

        def set_reference_level(self, amplitude):
            """
            Set the reference level of the measurement. This value should be higher than
            the expected peak power of the input signal. Setting it closer to the actual peak input
            will optimize for dynamic range.

            :param amplitude: Reference level in dBm.

            """
            self.instrument.write(f":SENSe:DDEMod:POWer:RF:RLEVel {amplitude}")

        def get_reference_level(self):
            """
            Query the reference level of the measurement.

            
            :return: The measurement reference level in dBm.
            """
            return float(self.instrument.query(":SENSe:DDEMod:POWer:RF:RLEVel?"))

        def set_srate(self, freq):
            """
            Specify the sample rate of the input modulated signal.

            :param freq: Symbol rate in Hz.

            """
            self.instrument.write(f":SENSe:DDEMod:SRATe {freq}")

        def get_srate(self):
            """
            Query the sample rate of the input modulated signal.

            
            :return: The symbol rate in Hz.
            """
            return float(self.instrument.query(":SENSe:DDEMod:SRATe?"))

        def set_modulation(self, mod):
            """
            Specify the modulation type of the input signal.

            :param mod: Modulation type.

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
            Query the modulation type of the input signal.

            
            :return: The current modulation type.
            """
            return self.instrument.query(":SENSe:DDEMod:MODulation?")

        def set_rlength(self, value):
            """
            Specify the measurement window length in symbols.

            :param value: Result length.

            """
            if not isinstance(value, int):
                raise ValueError("value must be an integer")
            self.instrument.write(f":SENSe:DDEMod:RLENgth {value}")

        def get_rlength(self):
            """
            Query the measurement window length in symbols.

            
            :return: The result length.
            """
            return int(self.instrument.query(":SENSe:DDEMod:RLENgth?"))

        def set_filter(self, filt):
            """
            Specify the measurement and reference filter.

            :param filt: Filter type ('NYQUIST', 'RNYQUIST', 'GAUSSIAN', 'RECTANGLE').

            """
            allowed = {"NYQUIST", "RNYQUIST", "GAUSSIAN", "RECTANGLE"}
            if not isinstance(filt, str) or filt.upper() not in allowed:
                raise ValueError("filt must be one of 'NYQUIST', 'RNYQUIST', 'GAUSSIAN', or 'RECTANGLE'")
            self.instrument.write(f":SENSe:DDEMod:FILTer {filt.upper()}")

        def get_filter(self):
            """
            Query the measurement and reference filter.

            
            :return: The current filter type.
            """
            return self.instrument.query(":SENSe:DDEMod:FILTer?")

        def set_filter_abt(self, value):
            """
            Specify the filter alpha/beta coefficient.

            :param value: Filter alpha/beta/BT value.

            """
            self.instrument.write(f":SENSe:DDEMod:FILTer:ABT {value}")

        def get_filter_abt(self):
            """
            Query the filter alpha/beta coefficient.

            
            :return: The filter alpha/beta/BT value.
            """
            return float(self.instrument.query(":SENSe:DDEMod:FILTer:ABT?"))

        def set_ifbwidth_auto(self, state):
            """
            When enabled, the Spike software will automatically choose an
            appropriate IF bandwidth for the measurement (usually 2x the sample rate).

            :param state: 1/0 or 'ON'/'OFF' to enable/disable automatic IF bandwidth selection.

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
            Query if automatic IF bandwidth selection is enabled.

            
            :return:  True if automatic IF bandwidth is enabled, False otherwise.
            """
            resp = self.instrument.query(":SENSe:DDEMod:IFBWidth:AUTO?")
            return int(resp.strip()) == 1

        def set_ifbwidth(self, freq):
            """
            Specify the IF bandwidth, only active when AUTO is set to false.

            :param freq: IF bandwidth in Hz.

            """
            self.instrument.write(f":SENSe:DDEMod:IFBWidth {freq}")

        def get_ifbwidth(self):
            """
            Query the IF bandwidth.

            
            :return: The IF bandwidth in Hz.
            """
            return float(self.instrument.query(":SENSe:DDEMod:IFBWidth?"))

        def enable_average_state(self, state):
            """
            Enable measurement averaging.

            :param state: 1/0 or 'ON'/'OFF' to enable/disable measurement averaging.

            """

            self.instrument.write(f":SENSe:DDEMod:AVERage:STATe ON")
        def disable_average(self):
            """
            Disable measurement averaging."""
            self.instrument.write(f":SENSe:DDEMod:AVERage:STATe OFF")
        def is_average_enabled(self):
            """
            Query if measurement averaging is enabled.

            
            :return:  True if measurement averaging is enabled, False otherwise.
            """
            resp = self.instrument.query(":SENSe:DDEMod:AVERage:STATe?")
            return int(resp.strip()) == 1

        def set_average_count(self, count):
            """
            Specify the average count.

            :param count: Number of averages.

            """
            if not isinstance(count, int):
                raise ValueError("count must be an integer")
            self.instrument.write(f":SENSe:DDEMod:AVERage:COUNt {count}")

        def get_average_count(self):
            """
            Query the average count.

            
            :return: The number of averages.
            """
            return int(self.instrument.query(":SENSe:DDEMod:AVERage:COUNt?"))

        def enable_wide_carrier_est(self, state):
            """
            Enable wide carrier estimation.

            :param state: 1/0 or 'ON'/'OFF' to enable/disable wide carrier estimation.

            """

            self.instrument.write(f":SENSe:DDEMod:WCE:STATe ON")
        def disable_wce(self):
            """
            Disable wide carrier estimation."""
            self.instrument.write(f":SENSe:DDEMod:WCE:STATe OFF")
        def is_wce_enabled(self):
            """
            Query if wide carrier estimation is enabled.

            
            :return:  True if wide carrier estimation is enabled, False otherwise.
            """
            resp = self.instrument.query(":SENSe:DDEMod:WCE:STATe?")
            return int(resp.strip()) == 1

        def set_wce_range(self, freq):
            """
            Set the wide carrier estimation range.

            :param freq: Wide carrier estimation range in Hz.

            """
            self.instrument.write(f":SENSe:DDEMod:WCE:RANge {freq}")

        def get_wce_range(self):
            """
            Query the wide carrier estimation range.

            
            :return: The wide carrier estimation range in Hz.
            """
            return float(self.instrument.query(":SENSe:DDEMod:WCE:RANge?"))
        class Custom:
            """
            The Custom commands configure custom IQ constellations for digital demodulation.
            """
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler
                self.iq = self.IQ(self.instrument, self.data_handler)

            class IQ:
                """
                The IQ commands configure and query custom IQ constellation data.
                """
                def __init__(self, instrument,data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler

                def is_valid(self):
                    """
                    Returns 1 when the custom constellation is valid.

                    
                    :return:  True if the custom constellation is valid, False otherwise.
                    """
                    resp = self.instrument.query(":SENSe:DDEMod:CUSTom:IQ:VALid?")
                    return int(resp.strip()) == 1

                def get_length(self):
                    """
                    Returns the number of symbols in the custom constellation.

                    
                    :return: The number of symbols in the custom constellation.
                    """
                    return int(self.instrument.query(":SENSe:DDEMod:CUSTom:IQ:LENGth?"))

                def set_data(self, iq_values):
                    """
                    Specify the constellation symbols as IQ values. IQ values are specified as
                    comma separated real numbers, alternating IQ values. If an odd number of real
                    values are provided the last value is ignored. If any value is an invalid real number,
                    the command fails and throws a system error. While not strictly necessary, it is
                    suggested to scale the constellation so that the maximum symbol magnitude is 1.

                    :param iq_values (list or tuple): List of real numbers, alternating I/Q values.

                    """
                    if not isinstance(iq_values, (list, tuple)) or not all(isinstance(x, (int, float)) for x in iq_values):
                        raise ValueError("iq_values must be a list or tuple of real numbers")
                    data_str = ",".join(str(x) for x in iq_values)
                    self.instrument.write(f":SENSe:DDEMod:CUSTom:IQ:DATA {data_str}")

                def get_data(self):
                    """
                    Returns the constellation symbols as a comma separated list of alternating
                    IQ values.

                    
                    :return: The constellation symbols as a comma separated list of alternating IQ values.
                    """
                    response = self.instrument.query(":SENSe:DDEMod:CUSTom:IQ:DATA?")
                    if self.data_handler.is_auto_saving_data_enabled():
                        self.data_handler.write_to_file(self, "DDEMOD_IQ", response, file_type = EFileType.CSV, headers = None)
                    return response
        class Trigger_DDE:
            """
            The DDEMod:Trigger commands configure triggering for digital demodulation.
            """
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler

            def set_source(self, source):
                """
                Specify the trigger type.

                :param source: 'IMMEDIATE', 'IF', or 'EXTERNAL'

                """
                allowed = {"IMMEDIATE", "IF", "EXTERNAL"}
                if not isinstance(source, str) or source.upper() not in allowed:
                    raise ValueError("source must be one of 'IMMEDIATE', 'IF', or 'EXTERNAL'")
                self.instrument.write(f":TRIGger:DDEMod:SOURce {source.upper()}")

            def get_source(self):
                """
                Query the trigger type.

                
                :return: The trigger type.
                """
                return self.instrument.query(":TRIGger:DDEMod:SOURce?")

            def set_if_level(self, amplitude):
                """
                Specify the trigger level of the IF trigger.

                :param amplitude: Trigger level of the IF trigger.

                """
                self.instrument.write(f":TRIGger:DDEMod:IF:LEVel {amplitude}")

            def get_if_level(self):
                """
                Query the trigger level of the IF trigger.

                
                :return: The trigger level of the IF trigger.
                """
                return float(self.instrument.query(":TRIGger:DDEMod:IF:LEVel?"))

            def set_delay(self, value):
                """
                Specify the trigger delay of the IF or ext trigger, the number of symbols after
                the trigger to start the measurement.

                :param value: Trigger delay (number of symbols after trigger to start measurement).

                """
                if not isinstance(value, int):
                    raise ValueError("value must be an integer")
                self.instrument.write(f":TRIGger:DDEMod:DELay {value}")

            def get_delay(self):
                """
                Query the trigger delay (number of symbols after trigger).

                
                :return: The trigger delay (number of symbols after trigger).
                """
                return int(self.instrument.query(":TRIGger:DDEMod:DELay?"))

        class Sync:
            """
            The DDEMod:Sync commands configure sync pattern search for digital demodulation.
            """
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler
                self.sword = self.Sword(self.instrument, self.data_handler)
            def enable_sync_search(self):
                """Enable sync search.
            

                """
                self.instrument.write(f":SENSe:DDEMod:SYNC:STATe ON")
            
            def disable_sync_search(self):
                """Disable sync search.
                """
                self.instrument.write(f":SENSe:DDEMod:SYNC:STATe OFF")
            def is_enabled(self):
                """ Check if sync search is enabled.
                
                :return:  True if sync search is enabled, False otherwise.
                """
                resp = self.instrument.query(":SENSe:DDEMod:SYNC:STATe?")
                return int(resp.strip()) == 1
            def set_slength(self, value):
                """
                Set the search length for the pattern trigger.

                :param value: Search length for the pattern trigger.

                """
                if not isinstance(value, int):
                    raise ValueError("value must be an integer")
                self.instrument.write(f":SENSe:DDEMod:SYNC:SLENgth {value}")

            def get_slength(self):
                """
                Get the search length for the pattern trigger.

                
                :return: Search length for the pattern trigger.
                """
                return int(self.instrument.query(":SENSe:DDEMod:SYNC:SLENgth?"))

            def set_offset(self, value):
                """
                Offset the measurement from the beginning of a successful sync search.
                Can be negative.

                :param value: Offset from the beginning of a successful sync search (can be negative).

                """
                if not isinstance(value, int):
                    raise ValueError("value must be an integer")
                self.instrument.write(f":SENSe:DDEMod:SYNC:OFFSet {value}")

            def get_offset(self):
                """
                Get the offset from the beginning of a successful sync search.
                Can be negative.

                
                :return: Offset from the beginning of a successful sync search.
                """
                return int(self.instrument.query(":SENSe:DDEMod:SYNC:OFFSet?"))
            class Sword:
                """
                The SWord commands configure the sync pattern and length.
                """
                def __init__(self, instrument,data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler

                def set_pattern(self, hex_string):
                    """
                    Set the pattern to trigger on for the trigger pattern.

                    The pattern will be converted to uppercase when provided otherwise.

                    :param hex_string: The pattern to trigger on (hex string).

                    """
                    if not isinstance(hex_string, str):
                        raise ValueError("hex_string must be a string")
                    self.instrument.write(f":SENSe:DDEMod:SYNC:SWORd:PATTern {hex_string}")

                def get_pattern(self):
                    """
                    Query the current sync pattern.

                    
                    :return: The current sync pattern (hex string).
                    """
                    return self.instrument.query(":SENSe:DDEMod:SYNC:SWORd:PATTern?")

                def set_length(self, value):
                    """
                    Set the length in symbols of the pattern trigger.

                    The pattern length is not necessarily the same length as the pattern itself.
                    A shorter length uses only a portion of the pattern and a longer length pads the pattern with 'zeros'.

                    :param value: The length in symbols of the pattern trigger.

                    """
                    if not isinstance(value, int):
                        raise ValueError("value must be an integer")
                    self.instrument.write(f":SENSe:DDEMod:SYNC:SWORd:LENGth {value}")

                def get_length(self):
                    """
                    Query the length in symbols of the pattern trigger.

                    
                    :return: The length in symbols of the pattern trigger.
                    """
                    return int(self.instrument.query(":SENSe:DDEMod:SYNC:SWORd:LENGth?"))

        class Compensate:
            """
            The DDEMod:Compensate commands configure compensation settings for digital demodulation.
            """
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler

            def enable_iqinversion(self):
                """
                Enable IQ swap compensation.

                When enabled, the I and Q channels are swapped in the signal.


                """
                self.instrument.write(f":SENSe:DDEMod:COMPensate:IQINVersion:STATe ON")

            def disable_iqinversion(self):
                """
                Disable IQ swap compensation.

                When disabled, the I and Q channels are not swapped.


                """
                self.instrument.write(f":SENSe:DDEMod:COMPensate:IQINVersion:STATe OFF")

            def is_iqinversion_enabled(self):
                """
                Query if IQ swap compensation is enabled.

                
                :return:  True if IQ swap is enabled, False otherwise.
                """
                resp = self.instrument.query(":SENSe:DDEMod:COMPensate:IQINVersion:STATe?")
                return int(resp.strip()) == 1

            def enable_iqoffset(self):
                """
                Enable IQ offset removal.

                When enabled, IQ offset is removed from the signal.


                """
                self.instrument.write(f":SENSe:DDEMod:COMPensate:IQOFFset:STATe ON")

            def disable_iqoffset(self):
                """
                Disable IQ offset removal.

                When disabled, IQ offset is not removed from the signal.


                """
                self.instrument.write(f":SENSe:DDEMod:COMPensate:IQOFFset:STATe OFF")

            def is_iqoffset_enabled(self):
                """
                Query if IQ offset removal is enabled.

                
                :return:  True if IQ offset removal is enabled, False otherwise.
                """
                resp = self.instrument.query(":SENSe:DDEMod:COMPensate:IQOFFset:STATe?")
                return int(resp.strip()) == 1

            def enable_linear_amp_error_correction(self):
                """
                Enable linear amplitude error correction (ADRoop).

                When enabled, linear amplitude errors are corrected for in the signal.


                """
                self.instrument.write(f":SENSe:DDEMod:COMPensate:ADRoop:STATe ON")

            def disable_linear_amp_error_correction(self):
                """
                Disable linear amplitude error correction (ADRoop).

                When disabled, linear amplitude errors are not corrected.


                """
                self.instrument.write(f":SENSe:DDEMod:COMPensate:ADRoop:STATe OFF")

            def is_linear_amp_error_correction_enabled(self):
                """
                Query if linear amplitude error correction (ADRoop) is enabled.

                
                :return:  True if amplitude droop compensation is enabled, False otherwise.
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

            def enable(self):
                """
                Enable equalization.

                Enables the equalization filter in digital demodulation mode.


                """
                self.instrument.write(f":SENSe:DDEMod:EQUalization:STATe ON")

            def disable(self):
                """
                Disable equalization.

                Disables the equalization filter in digital demodulation mode.


                """
                self.instrument.write(f":SENSe:DDEMod:EQUalization:STATe OFF")

            def is_enabled(self):
                """
                Query if equalization is enabled.

                
                :return:  True if equalization is enabled, False otherwise.
                """
                resp = self.instrument.query(":SENSe:DDEMod:EQUalization:STATe?")
                return int(resp.strip()) == 1

            def set_length(self, value):
                """
                Set the length of the equalization filter in symbols.

                The length must be an odd integer.

                :param value: Length of the equalization filter in symbols (must be odd).

                """
                if not isinstance(value, int) or value % 2 != 1:
                    raise ValueError("value must be an odd integer")
                self.instrument.write(f":SENSe:DDEMod:EQUalization:LENGth {value}")

            def get_length(self):
                """
                Query the length of the equalization filter in symbols.

                
                :return: Length of the equalization filter in symbols.
                """
                return int(self.instrument.query(":SENSe:DDEMod:EQUalization:LENGth?"))

            def set_convergence(self, value):
                """
                Set the adaptive rate (convergence) of the equalizer.

                Higher values adapt faster but are more unstable.

                :param value: Adaptive rate (convergence).

                """
                self.instrument.write(f":SENSe:DDEMod:EQUalization:CONVergence {value}")

            def get_convergence(self):
                """
                Query the adaptive rate (convergence) of the equalizer.

                
                :return: Adaptive rate (convergence).
                """
                return float(self.instrument.query(":SENSe:DDEMod:EQUalization:CONVergence?"))

            def set_hold_state(self, state):
                """
                Enable or disable hold (bypass adaptation).

                When enabled, adaptation step is bypassed but equalization is still applied.

                :param state: 1/0 or 'ON'/'OFF' to enable/disable hold (bypass adaptation).

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
                Query if hold (bypass adaptation) is enabled.

                
                :return:  True if hold is enabled, False otherwise.
                """
                resp = self.instrument.query(":SENSe:DDEMod:EQUalization:HOLD:STATe?")
                return int(resp.strip()) == 1

            def reset(self):
                """
                Reset the equalization filter.

                Resets the equalization filter to the unit impulse response (pass through).

                

                """
                self.instrument.write(":SENSe:DDEMod:EQUalization:RESet")

        class Trace_DDE:
            """
            The DDEMod:Trace commands retrieve spectrum data from digital demodulation measurement mode.
            """
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler
                self.sweep = self.Sweep_Tr_DDE(self.instrument, self.data_handler)
            class Sweep_Tr_DDE:
                """
                The DDEMod:Trace:Sweep commands retrieve sweep data.
                """
                def __init__(self, instrument,data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler

                def get_xstart(self):
                    """
                    Get the frequency value associated with the first sample in the returned data.

                    
                    :return: Frequency value associated with the first sample in the returned data.
                    """
                    return float(self.instrument.query(":SENSe:DDEMod:TRACe:SWEep:XSTARt?"))

                def get_xincrement(self):
                    """
                    Get the frequency spacing for the samples in the returned data.

                    
                    :return: Frequency spacing for the samples in the returned data.
                    """
                    return float(self.instrument.query(":SENSe:DDEMod:TRACe:SWEep:XINCrement?"))

                def get_points(self):
                    """
                    Get the number of points returned by the DATA function.

                    
                    :return: Number of points returned by the DATA function.
                    """
                    return int(self.instrument.query(":SENSe:DDEMod:TRACe:SWEep:POINts?"))

                def get_data(self):
                    """
                    Get the spectrum trace.

                    
                    :return: The spectrum trace as a comma separated list.
                    """
                    response = self.instrument.query(":SENSe:DDEMod:TRACe:SWEep:DATA?")
                    if self.data_handler.is_auto_saving_data_enabled():
                        self.data_handler.write_to_file(self, "TRACE_SWEEP", response, file_type = EFileType.CSV, headers = None)
                    return response


        class Fetch_DDE:
            """
            The DDEMod:Fetch commands retrieve measurement results for digital demodulation.
            """
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler

            def fetch(self, metrics):
                """ Fetch digital demodulation metrics. The integer parameter specifies the
                metric to retrieve. Possible integer values can be printed with function print_fetch_options(). Can specify a list of metrics to
                request as comma separated list. The metrics will be returned as a comma
                separated list in the order they were requested.
                
                :param metrics: Metric(s) to retrieve.
                :return: Comma separated list of metric values in order requested.
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
            def print_fetch_options(self):
                """ Print available fetch options for digital demodulation metrics.
                    
                    :return table: List of (ID, Description) tuples for available metrics.
                    """
                table = [
                    (1,  "RMS EVM average as %"),
                    (2,  "RMS EVM peak as %"),
                    (3,  "RMS mag error average as %"),
                    (4,  "RMS mag error peak as %"),
                    (5,  "RMS phase error average as %"),
                    (6,  "RMS phase error peak as %"),
                    (7,  "IQ offset average as dB"),
                    (8,  "IQ offset peak as dB"),
                    (9,  "Frequency error average as Hz"),
                    (10, "Frequency error peak as Hz"),
                    (11, "RF power average as dBm"),
                    (12, "RF power peak as dBm"),
                    (13, "SNR average as dB"),
                    (14, "SNR peak as dB"),
                    (15, "RMS FSK error average as %"),
                    (16, "RMS FSK error peak as %"),
                    (17, "FSK deviation avg as Hz"),
                    (18, "FSK deviation peak as Hz"),
                    (29, "Current average count"),
                    (30, "Demod bits as binary string"),
                    (40, "Constellation result length (see 41)"),
                    (41, "Constellation results (see docstring for details)"),
                ]
                print("{:<4} {}".format("ID", "Description"))
                print("-" * 50)
                for id, desc in table:
                    print("{:<4} {}".format(id, desc))
                return table
    class Sweep_Configuration:
        """
        The Sweep Configuration commands control the sweep configuration in scalar network analysis mode.
        """
        def __init__(self, instrument,data_handler):
            self.instrument = instrument
            self.data_handler = data_handler

        def set_points(self, num_points):
            """
            Specify a suggested sweep size.

            The final sweep size takes this setting into consideration as well as hardware limitations when determining the final sweep size.

            :param num_points: Suggested sweep size.

            """
            if not isinstance(num_points, int):
                raise ValueError("num_points must be an integer")
            self.instrument.write(f":SENSe:NA:SWEep:POINts {num_points}")

        def get_points(self):
            """
            Query the suggested sweep size.

            The final sweep size may differ due to hardware limitations.

            
            :return: The suggested sweep size.
            """
            return int(self.instrument.query(":SENSe:NA:SWEep:POINts?"))

        def set_type(self, typ):
            """
            Specify whether an active or passive device is being measured.

            This will affect the attenuation and gain used during the sweep. Failure to properly set this value may result in reduced dynamic range or IF overload.

            :param typ: 'PASSive' or 'ACTive'.

            """
            allowed = {"PASSive", "ACTive"}
            if not isinstance(typ, str) or typ.upper() not in allowed:
                raise ValueError("typ must be 'PASSive' or 'ACTive'")
            self.instrument.write(f":SENSe:NA:SWEep:TYPE {typ.upper()}")

        def get_type(self):
            """
            Query the sweep type.

            Indicates whether an active or passive device is being measured.

            
            :return: The sweep type.
            """
            return self.instrument.query(":SENSe:NA:SWEep:TYPE?")

        def set_hrange(self, state):
            """
            Enable or disable high range.

            If high range is enabled, the software will optimize the sweep for dynamic range when a 20dB pad store through is performed. Sweep speed will decrease when selected.

            :param state: 1/0 or 'ON'/'OFF' to enable/disable high range.

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
            Query if high range is enabled.

            When enabled, sweep is optimized for dynamic range with a 20dB pad store through, but sweep speed will decrease.

            
            :return:  True if high range is enabled, False otherwise.
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
            self.view = self.View_NA(self.instrument, self.data_handler)
            self.correction = self.Correction_NA(self.instrument, self.data_handler)
        
        class View_NA:
            """View commands control the view settings in scalar network analysis mode."""
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler

            def set_scale(self, scale):
                """
                Specify whether the plot is in log or VSWR units. A unique reference
                level and div are stored for both scale types.

                :param scale: 'LOG' or 'VSWR'.

                """
                allowed = {"LOG", "VSWR"}
                if not isinstance(scale, str) or scale.upper() not in allowed:
                    raise ValueError("scale must be 'LOG' or 'VSWR'")
                self.instrument.write(f":SENSe:NA:VIEW:SCALe {scale.upper()}")

            def get_scale(self):
                """
                Query whether the plot is in log or VSWR units.

                
                :return: The plot scale.
                """
                return self.instrument.query(":SENSe:NA:VIEW:SCALe?")

            def set_rlevel(self, amplitude):
                """
                Specify the reference level. When log scale is selected, the rlevel is
                specified as dBm, when VSWR is selected, rlevel is specified as SWR directly.
                Do not specify units.

                :param amplitude: Reference level in dBm (LOG) or SWR (VSWR).

                """
                self.instrument.write(f":SENSe:NA:VIEW:RLEVel {amplitude}")

            def get_rlevel(self):
                """
                Query the reference level. When log scale is selected, the rlevel is
                specified as dBm, when VSWR is selected, rlevel is specified as SWR directly.

                
                :return: The reference level.
                """
                return float(self.instrument.query(":SENSe:NA:VIEW:RLEVel?"))

            def set_div(self, division):
                """
                Specify the plot vertical scale as either dB or SWR (depending on what
                scale is currently selected). Do not specify units. In each case, the div is 1/10th the
                vertical scale of the plot.

                :param division: Plot vertical scale as dB (LOG) or SWR (VSWR).

                """
                self.instrument.write(f":SENSe:NA:VIEW:DIV {division}")

            def get_div(self):
                """
                Query the plot vertical scale as either dB or SWR (depending on what
                scale is currently selected). In each case, the div is 1/10th the vertical scale of the plot.

                
                :return: The plot vertical scale.
                """
                return float(self.instrument.query(":SENSe:NA:VIEW:DIV?"))
        class Correction_NA:
            """
            The Correction commands control the correction settings in scalar network analysis mode.
            """
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler

            def store_thru(self):
                """
                Perform a store through calibration.

                

                """
                self.instrument.write(":SENSe:CORRection:NA:STORe:THRU")

            def store_thru_high(self):
                """
                Perform a store through high range calibration.

                

                """
                self.instrument.write(":SENSe:CORRection:NA:STORe:THRU:HIGH")

            def is_thru_active(self):
                """
                Returns true when a calibration is active (the store through has been performed for the current sweep settings).

                
                :return:  True if a calibration is active, False otherwise.
                """
                resp = self.instrument.query(":SENSe:CORRection:NA:STORe:THRU:ACTive?")
                return resp.strip() == '1'
    class VCO_Sense:
        """
        The VCO commands control the configuration of the measurement in VCO Characterization mode.
        """
        def __init__(self, instrument,data_handler):
            self.instrument = instrument
            self.data_handler = data_handler
            self.sweep = self.Sweep_VCO(self.instrument, self.data_handler)
            self.source = self.Source_VCO(self.instrument, self.data_handler)
            self.fetch = self.Fetch_VCO(self.instrument, self.data_handler)
        class Sweep_VCO:
            """
            The Sweep commands control the sweep configuration in VCO Characterization mode.
            """
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler

            def get_source(self):
                """
                
                :return: The sweep source.
                """
                return self.instrument.query(":SENSe:VCO:SWEep:SOURce?")

            def set_start(self, value):
                """
                Set the starting voltage for the sweep in volts.

                :param value: Starting voltage for the sweep in volts.

                """
                self.instrument.write(f":SENSe:VCO:SWEep:STARt {value}")

            def get_start(self):
                """
                Get the starting voltage for the sweep in volts.

                
                :return: Starting voltage for the sweep in volts.
                """
                return float(self.instrument.query(":SENSe:VCO:SWEep:STARt?"))

            def set_stop(self, value):
                """
                Set the stopping voltage for the sweep in volts.

                :param value: Stopping voltage for the sweep in volts.

                """
                self.instrument.write(f":SENSe:VCO:SWEep:STOP {value}")

            def get_stop(self):
                """
                Get the stopping voltage for the sweep in volts.

                
                :return: Stopping voltage for the sweep in volts.
                """
                return float(self.instrument.query(":SENSe:VCO:SWEep:STOP?"))

            def set_points(self, num_points):
                """
                Set the number of points to measure.

                :param num_points: Number of points to measure.

                """
                if not isinstance(num_points, int):
                    raise ValueError("num_points must be an integer")
                self.instrument.write(f":SENSe:VCO:SWEep:POINts {num_points}")

            def get_points(self):
                """
                Get the number of points to measure.

                
                :return: Number of points to measure.
                """
                return int(self.instrument.query(":SENSe:VCO:SWEep:POINts?"))

            def set_rf_rlevel(self, value):
                """
                Set the reference level as dBm.

                :param value: Reference level as dBm.

                """
                self.instrument.write(f":SENSe:VCO:SWEep:RF:RLEVel {value}")

            def get_rf_rlevel(self):
                """
                Get the reference level as dBm.

                
                :return: Reference level as dBm.
                """
                return float(self.instrument.query(":SENSe:VCO:SWEep:RF:RLEVel?"))

            def set_band_auto(self, state):
                """
                Set whether the frequency band search range is automatically configured.

                :param state: 1/0 or 'ON'/'OFF' to enable/disable automatic frequency band search.

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
                Query if automatic frequency band search is enabled.

                
                :return:  True if automatic frequency band search is enabled, False otherwise.
                """
                resp = self.instrument.query(":SENSe:VCO:SWEep:FREQuency:BAND:AUTO?")
                return int(resp.strip()) == 1

            def set_band_start(self, freq):
                """
                Set the start frequency of the search range.

                :param freq: Start frequency of the search range.

                """
                self.instrument.write(f":SENSe:VCO:SWEep:FREQuency:BAND:STARt {freq}")

            def get_band_start(self):
                """
                Get the start frequency of the search range.

                
                :return: Start frequency of the search range.
                """
                return float(self.instrument.query(":SENSe:VCO:SWEep:FREQuency:BAND:STARt?"))

            def set_band_stop(self, freq):
                """
                Set the stop frequency of the search range.

                :param freq: Stop frequency of the search range.

                """
                self.instrument.write(f":SENSe:VCO:SWEep:FREQuency:BAND:STOP {freq}")

            def get_band_stop(self):
                """
                Get the stop frequency of the search range.

                
                :return: Stop frequency of the search range.
                """
                return float(self.instrument.query(":SENSe:VCO:SWEep:FREQuency:BAND:STOP?"))

            def set_fcounter_resolution(self, freq):
                """
                Set the frequency resolution of each measurement. This is effectively the RBW of the measurement sweep performed at each point.

                :param freq: Frequency resolution of each measurement (RBW).

                """
                self.instrument.write(f":SENSe:VCO:SWEep:FCOunter:RESolution {freq}")

            def get_fcounter_resolution(self):
                """
                Get the frequency resolution of each measurement (RBW).

                
                :return: Frequency resolution of each measurement (RBW).
                """
                return float(self.instrument.query(":SENSe:VCO:SWEep:FCOunter:RESolution?"))

            def set_chpower_width(self, freq):
                """
                Set the width of the channel for power and harmonics measurements.

                :param freq: Width of the channel for power and harmonics measurements.

                """
                self.instrument.write(f":SENSe:VCO:SWEep:CHPower:WIDth {freq}")

            def get_chpower_width(self):
                """
                Get the width of the channel for power and harmonics measurements.

                
                :return: Width of the channel for power and harmonics measurements.
                """
                return float(self.instrument.query(":SENSe:VCO:SWEep:CHPower:WIDth?"))

            def set_delay(self, value):
                """
                Set the dwell time for each measurement, or the pause between setting PN400 voltage and measuring VCO output.

                :param value: Dwell time for each measurement (pause between setting voltage and measuring).

                """
                self.instrument.write(f":SENSe:VCO:SWEep:DELay {value}")

            def get_delay(self):
                """
                Get the dwell time for each measurement.

                
                :return: Dwell time for each measurement.
                """
                return float(self.instrument.query(":SENSe:VCO:SWEep:DELay?"))

        class Source_VCO:
            """
            The Source commands control the DC source configuration in VCO Characterization mode.
            """
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler

            def set_voltage_state(self, state):
                """
                Enable or disable overall DC power.

                :param state: 1/0 or 'ON'/'OFF' to enable/disable overall DC power.

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
                Query if overall DC power is enabled.

                
                :return:  True if DC power is enabled, False otherwise.
                """
                resp = self.instrument.query(":SENSe:VCO:SOURce:VOLTage:STATe?")
                return int(resp.strip()) == 1

            def set_fixed_level(self, value):
                """
                Set the output level of the fixed power source in volts.

                :param value: Output level of the fixed power source in volts.

                """
                self.instrument.write(f":SENSe:VCO:SOURce:VOLTage:FIXed:LEVel {value}")

            def get_fixed_level(self):
                """
                Query the output level of the fixed power source in volts.

                
                :return: Output level of the fixed power source in volts.
                """
                return float(self.instrument.query(":SENSe:VCO:SOURce:VOLTage:FIXed:LEVel?"))

            def set_vtune_limit_low(self, value):
                """
                Set the minimum output level of the V Tune port in volts.

                :param value: Minimum output level of the V Tune port in volts.

                """
                self.instrument.write(f":SENSe:VCO:SOURce:VOLTage:VTUNe:LEVel:LIMit:LOW {value}")

            def get_vtune_limit_low(self):
                """
                Query the minimum output level of the V Tune port in volts.

                
                :return: Minimum output level of the V Tune port in volts.
                """
                return float(self.instrument.query(":SENSe:VCO:SOURce:VOLTage:VTUNe:LEVel:LIMit:LOW?"))

            def set_vtune_limit_high(self, value):
                """
                Set the maximum output level of the V Tune port in volts.

                :param value: Maximum output level of the V Tune port in volts.

                """
                self.instrument.write(f":SENSe:VCO:SOURce:VOLTage:VTUNe:LEVel:LIMit:HIGH {value}")

            def get_vtune_limit_high(self):
                """
                Query the maximum output level of the V Tune port in volts.

                
                :return: Maximum output level of the V Tune port in volts.
                """
                return float(self.instrument.query(":SENSe:VCO:SOURce:VOLTage:VTUNe:LEVel:LIMit:HIGH?"))

            def set_vsup_limit_low(self, value):
                """
                Set the minimum output level of the V Supply port in volts.

                :param value: Minimum output level of the V Supply port in volts.

                """
                self.instrument.write(f":SENSe:VCO:SOURce:VOLTage:VSUPply:LEVel:LIMit:LOW {value}")

            def get_vsup_limit_low(self):
                """
                Query the minimum output level of the V Supply port in volts.

                
                :return: Minimum output level of the V Supply port in volts.
                """
                return float(self.instrument.query(":SENSe:VCO:SOURce:VOLTage:VSUPply:LEVel:LIMit:LOW?"))

            def set_vsup_limit_high(self, value):
                """
                Set the maximum output level of the V Supply port in volts.

                :param value: Maximum output level of the V Supply port in volts.

                """
                self.instrument.write(f":SENSe:VCO:SOURce:VOLTage:VSUPply:LEVel:LIMit:HIGH {value}")

            def get_vsup_limit_high(self):
                """
                Query the maximum output level of the V Supply port in volts.

                
                :return: Maximum output level of the V Supply port in volts.
                """
                return float(self.instrument.query(":SENSe:VCO:SOURce:VOLTage:VSUPply:LEVel:LIMit:HIGH?"))
        class Fetch_VCO:
            """
            The Fetch commands retrieve VCO characterization measurement results.
            """
            def __init__(self, instrument, data_handler):
                self.instrument = instrument
                self.data_handler = data_handler

            def get_frequency(self):
                """
                Fetch the frequency vs. voltage measurement data.

                :return: Frequency vs. voltage data as a comma separated list.
                """
                response = self.instrument.query(":FETCh:VCO:FREQuency?")
                if self.data_handler.is_auto_saving_data_enabled():
                    self.data_handler.write_to_file(self, "VCO_FREQUENCY", response, file_type=EFileType.CSV, headers=None)
                return response

            def get_sensitivity(self):
                """
                Fetch the frequency delta vs. voltage delta measurement data.

                :return: Sensitivity data as a comma separated list.
                """
                response = self.instrument.query(":FETCh:VCO:SENSitivity?")
                if self.data_handler.is_auto_saving_data_enabled():
                    self.data_handler.write_to_file(self, "VCO_SENSITIVITY", response, file_type=EFileType.CSV, headers=None)
                return response

            def get_power(self):
                """
                Fetch the amplitude vs. voltage measurement data.

                :return: Power data as a comma separated list.
                """
                response = self.instrument.query(":FETCh:VCO:POWer?")
                if self.data_handler.is_auto_saving_data_enabled():
                    self.data_handler.write_to_file(self, "VCO_POWER", response, file_type=EFileType.CSV, headers=None)
                return response

            def get_current(self):
                """
                Fetch the current vs. voltage measurement data.

                :return: Current data as a comma separated list.
                """
                response = self.instrument.query(":FETCh:VCO:CURRent?")
                if self.data_handler.is_auto_saving_data_enabled():
                    self.data_handler.write_to_file(self, "VCO_CURRENT", response, file_type=EFileType.CSV, headers=None)
                return response

            def get_harmonics(self, harmonic_num):
                """
                Fetch the harmonic amplitude vs. voltage measurement data.

                Args:
                    harmonic_num: Harmonic number to retrieve [1-6].

                :return: Harmonic amplitude vs. voltage data as a comma separated list.
                """
                if not isinstance(harmonic_num, int) or not (1 <= harmonic_num <= 6):
                    raise ValueError("harmonic_num must be an integer between 1 and 6")
                response = self.instrument.query(f":FETCh:VCO:HARMonics? {harmonic_num}")
                if self.data_handler.is_auto_saving_data_enabled():
                    self.data_handler.write_to_file(self, f"VCO_HARMONICS_{harmonic_num}", response, file_type=EFileType.CSV, headers=None)
                return response
    class Audio:
        """
        The Audio commands control the audio player utility in Spike.
        """
        def __init__(self, instrument,data_handler):
            self.instrument = instrument
            self.data_handler = data_handler

        def start(self):
            """
            Open the audio player.

            Opens the audio player. If the audio player is already open, does nothing.

            

            """
            self.instrument.write(":SENSe:AUDio:STARt")

        def stop(self):
            """
            Close the audio player.

            Closes the audio player. If the audio player is already closed, does nothing.

            

            """
            self.instrument.write(":SENSe:AUDio:STOP")

        def set_center_frequency(self, freq):
            """
            Set the center frequency of the audio player.

            :param freq: Center frequency of the audio player (Hz).

            """
            self.instrument.write(f":SENSe:AUDio:FREQuency:CENTer {freq}")

        def get_center_frequency(self):
            """
            Query the center frequency of the audio player.

            
            :return: The center frequency of the audio player (Hz).
            """
            return float(self.instrument.query(":SENSe:AUDio:FREQuency:CENTer?"))

        def set_modulation(self, mod):
            """
            Set the audio demodulation type.

            :param mod: 'AM', 'FM', 'LSB', 'USB', or 'CW'.

            """
            allowed = {"AM", "FM", "LSB", "USB", "CW"}
            if not isinstance(mod, str) or mod.upper() not in allowed:
                raise ValueError("mod must be one of 'AM', 'FM', 'LSB', 'USB', or 'CW'")
            self.instrument.write(f":SENSe:AUDio:MOD {mod.upper()}")

        def get_modulation(self):
            """
            Query the audio demodulation type.

            
            :return: The audio demodulation type.
            """
            return self.instrument.query(":SENSe:AUDio:MOD?")

        def set_if_bandwidth(self, freq):
            """
            Set the IF bandwidth of the audio player.

            Sets the IF bandwidth of the audio player. This is the filter applied before audio demodulation.

            :param freq: IF bandwidth of the audio player (Hz).

            """
            self.instrument.write(f":SENSe:AUDio:BANDwidth:IF {freq}")

        def get_if_bandwidth(self):
            """
            Query the IF bandwidth of the audio player.

            
            :return: The IF bandwidth of the audio player (Hz).
            """
            return float(self.instrument.query(":SENSe:AUDio:BANDwidth:IF?"))

        def set_lowpass_bandwidth(self, freq):
            """
            Set the audio low pass filter.

            Sets the audio low pass filter cutoff frequency.

            :param freq: Audio low pass filter cutoff (Hz).

            """
            self.instrument.write(f":SENSe:AUDio:BANDwidth:LOW {freq}")

        def get_lowpass_bandwidth(self):
            """
            Query the audio low pass filter cutoff.

            
            :return: The audio low pass filter cutoff (Hz).
            """
            return float(self.instrument.query(":SENSe:AUDio:BANDwidth:LOW?"))

        def set_highpass_bandwidth(self, freq):
            """
            Set the audio high pass filter.

            Sets the audio high pass filter cutoff frequency.

            :param freq: Audio high pass filter cutoff (Hz).

            """
            self.instrument.write(f":SENSe:AUDio:BANDwidth:HIGH {freq}")

        def get_highpass_bandwidth(self):
            """
            Query the audio high pass filter cutoff.

            
            :return: The audio high pass filter cutoff (Hz).
            """
            return float(self.instrument.query(":SENSe:AUDio:BANDwidth:HIGH?"))

        def set_fm_deemphasis(self, value):
            """
            Set the FM deemphasis.

            Sets the FM deemphasis in microseconds.

            :param value: FM deemphasis in microseconds.

            """
            self.instrument.write(f":SENSe:AUDio:FM:DEEMphasis {value}")

        def get_fm_deemphasis(self):
            """
            Query the FM deemphasis.

            
            :return: The FM deemphasis in microseconds.
            """
            return float(self.instrument.query(":SENSe:AUDio:FM:DEEMphasis?"))
    class PNoise_Sense:
        """
        The PNoise commands control the phase noise measurement mode.
        """
        def __init__(self, instrument,data_handler):
            self.instrument = instrument
            self.data_handler = data_handler
            self.carrier = self.Carrier(self.instrument, self.data_handler)
            self.view = self.View_PN(self.instrument, self.data_handler)
            self.frequency = self.Frequency_PN(self.instrument, self.data_handler)
            self.xcorr = self.XCORr(self.instrument, self.data_handler)
            self.vco = self.VCO_PN(self.instrument, self.data_handler)

        def set_peak_track(self, state):
            """
            Enable or disable peak tracking in phase noise measurement mode.

            When enabled, the marker performs a peak search on each new trace update.

            :param state: 1/0 or 'ON'/'OFF' to enable/disable peak tracking.

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
            Query if peak tracking is enabled in phase noise measurement mode.


            
            :return:  True if peak tracking is enabled, False otherwise.
            """
            resp = self.instrument.query(":SENSe:PNoise:PKTRack?")
            return int(resp.strip()) == 1

        def set_type(self, typ):
            """
            Set the measurement type in phase noise measurement mode.

            Select between AM noise, Phase noise, or both.

            :param typ: 'PN', 'PNPAM', or 'AM'.

            """
            allowed = {"PN", "PNPAM", "AM"}
            if not isinstance(typ, str) or typ.upper() not in allowed:
                raise ValueError("typ must be 'PN', 'PNPAM', or 'AM'")
            self.instrument.write(f":SENSe:PNoise:TYPE {typ.upper()}")

        def get_type(self):
            """
            Query the measurement type in phase noise measurement mode.

            Returns the current measurement type.

            
            :return: The measurement type.
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
                Enable or disable the signal search functionality.

                :param state: 1/0 or 'ON'/'OFF' to enable/disable signal search.

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
                Query if signal search functionality is enabled.

                
                :return:  True if signal search is enabled, False otherwise.
                """
                resp = self.instrument.query(":SENSe:PNoise:CARRier:SEARch:STATe?")
                return int(resp.strip()) == 1

            def set_search_start(self, freq):
                """
                Set the start frequency of the signal search range.

                :param freq: Start frequency of the signal search range in Hz.

                """
                self.instrument.write(f":SENSe:PNoise:CARRier:SEARch:STARt {freq}")

            def get_search_start(self):
                """
                Query the start frequency of the signal search range.

                
                :return: The start frequency of the signal search range in Hz.
                """
                return float(self.instrument.query(":SENSe:PNoise:CARRier:SEARch:STARt?"))

            def set_search_stop(self, freq):
                """
                Set the stop frequency of the signal search range.

                :param freq: Stop frequency of the signal search range in Hz.

                """
                self.instrument.write(f":SENSe:PNoise:CARRier:SEARch:STOP {freq}")

            def get_search_stop(self):
                """
                Query the stop frequency of the signal search range.

                
                :return: The stop frequency of the signal search range in Hz.
                """
                return float(self.instrument.query(":SENSe:PNoise:CARRier:SEARch:STOP?"))

            def perform_search(self):
                """
                Force a new signal search.

                

                """
                self.instrument.write(":SENSe:PNoise:CARRier:SEARch:PERForm")

            def set_threshold_minimum(self, amplitude):
                """
                Specify the minimum amplitude required (dBm, do not include units) for a signal to be detected as a carrier.

                :param amplitude: Minimum amplitude required for signal detection in dBm.

                """
                self.instrument.write(f":SENSe:PNoise:CARRier:THReshold:MINimum {amplitude}")

            def get_threshold_minimum(self):
                """
                Query the minimum amplitude required for signal detection.

                
                :return: The minimum amplitude required for signal detection in dBm.
                """
                return float(self.instrument.query(":SENSe:PNoise:CARRier:THReshold:MINimum?"))

            def is_valid(self):
                """
                Returns whether a carrier was detected.

                
                :return:  True if a carrier was detected, False otherwise.
                """
                resp = self.instrument.query(":SENSe:PNoise:CARRier:VALid?")
                return resp.strip() == '1'

            def get_frequency(self):
                """
                Returns the detected frequency of the carrier in Hz.

                
                :return: The detected frequency of the carrier in Hz.
                """
                return float(self.instrument.query(":SENSe:PNoise:CARRier:FREQuency?"))

            def get_amplitude(self):
                """
                Returns the detected amplitude of the carrier as dBm.

                
                :return: The detected amplitude of the carrier as dBm.
                """
                return float(self.instrument.query(":SENSe:PNoise:CARRier:AMPLitude?"))
        class View_PN:
            """
            The View commands control the plot view settings in phase noise measurement mode.
            """
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler

            def set_rlevel(self, amplitude):
                """
                Specify the plot reference level as dBc/Hz.

                :param amplitude: Plot reference level as dBc/Hz.

                """
                self.instrument.write(f":SENSe:PNoise:VIEW:RLEVel {amplitude}")

            def get_rlevel(self):
                """
                Query the plot reference level as dBc/Hz.

                
                :return: The plot reference level as dBc/Hz.
                """
                return float(self.instrument.query(":SENSe:PNoise:VIEW:RLEVel?"))

            def set_pdivision(self, division):
                """
                Specify the plot division height as a floating point value.

                :param division: Plot division height as a floating point value.

                """
                self.instrument.write(f":SENSe:PNoise:VIEW:PDIVision {division}")

            def get_pdivision(self):
                """
                Query the plot division height as a floating point value.

                
                :return: The plot division height as a floating point value.
                """
                return float(self.instrument.query(":SENSe:PNoise:VIEW:PDIVision?"))

            def set_pnumdivisions(self, num_divisions):
                """
                Specify the number of divisions on the phase noise plot.

                :param num_divisions: Number of divisions on the phase noise plot.

                """
                if not isinstance(num_divisions, int):
                    raise ValueError("num_divisions must be an integer")
                self.instrument.write(f":SENSe:PNoise:VIEW:PNUMDIVisions {num_divisions}")

            def get_pnumdivisions(self):
                """
                Query the number of divisions on the phase noise plot.

                
                :return: The number of divisions on the phase noise plot.
                """
                return int(self.instrument.query(":SENSe:PNoise:VIEW:PNUMDIVisions?"))

        class Frequency_PN:
            """
            The PNoiseFrequency commands control the frequency settings in phase noise measurement mode.
            """
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler

            def set_center(self, freq):
                """
                Specify the carrier search frequency window.

                A search window with 200kHz span centered at the specified frequency is used for detecting a carrier.

                :param freq: Carrier search frequency window in Hz.

                """
                self.instrument.write(f":SENSe:PNoise:FREQuency:CENTer {freq}")

            def get_center(self):
                """
                Query the carrier search frequency window.

                Returns the center frequency of the carrier search window in Hz.

                
                :return: The carrier search frequency window in Hz.
                """
                return float(self.instrument.query(":SENSe:PNoise:FREQuency:CENTer?"))

            def set_offset_start(self, freq):
                """
                Specify the start frequency of the phase noise sweep as an offset from the detected carrier center frequency.

                Values must be between 10Hz and 10kHz and will be clamped to the closest value from the list [10Hz, 100Hz, 1kHz, 10kHz].

                :param freq: Start frequency of the phase noise sweep as an offset from the detected carrier center frequency in Hz.

                """
                self.instrument.write(f":SENSe:PNoise:FREQuency:OFFSet:STARt {freq}")

            def get_offset_start(self):
                """
                Query the start frequency of the phase noise sweep as an offset from the detected carrier center frequency.

                
                :return: The start frequency of the phase noise sweep as an offset from the detected carrier center frequency in Hz.
                """
                return float(self.instrument.query(":SENSe:PNoise:FREQuency:OFFSet:STARt?"))

            def set_offset_stop(self, freq):
                """
                Specify the stop frequency of the phase noise sweep as an offset from the detected carrier center frequency.

                Values must be between 1kHz and 10MHz and will be clamped to the closest value from the list [1kHz, 10kHz, 100kHz, 1MHz, 10MHz].

                :param freq: Stop frequency of the phase noise sweep as an offset from the detected carrier center frequency in Hz.

                """
                self.instrument.write(f":SENSe:PNoise:FREQuency:OFFSet:STOP {freq}")

            def get_offset_stop(self):
                """
                Query the stop frequency of the phase noise sweep as an offset from the detected carrier center frequency.

                
                :return: The stop frequency of the phase noise sweep as an offset from the detected carrier center frequency in Hz.
                """
                return float(self.instrument.query(":SENSe:PNoise:FREQuency:OFFSet:STOP?"))
        class XCORr:
            """
            The PNoiseXCORr commands control the cross correlation settings in phase noise measurement mode.
            """
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler
                self.device = self.Device(self.instrument, self.data_handler)
            def set_state(self, state):
                """
                :param state: 1/0 or 'ON'/'OFF' to enable/disable cross correlation.

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
                
                :return:  True if cross correlation is enabled, False otherwise.
                """
                resp = self.instrument.query(":SENSe:PNoise:XCORr:STATe?")
                return int(resp.strip()) == 1
            def set_reference(self, reference):
                """
                Set the timebase reference of the cross correlation measurement system.

                :param reference: 'INTERNAL', 'EXTERNAL', or 'RF'

                """
                allowed = {"INTERNAL", "EXTERNAL", "RF"}
                if not isinstance(reference, str) or reference.upper() not in allowed:
                    raise ValueError("reference must be 'INTERNAL', 'EXTERNAL', or 'RF'")
                self.instrument.write(f":SENSe:PNoise:XCORr:REFerence {reference.upper()}")

            def get_reference(self):
                """
                Query the timebase reference of the cross correlation measurement system.

                :return: The current reference type.
                """
                return self.instrument.query(":SENSe:PNoise:XCORr:REFerence?")

            def set_factor(self, factor):
                """
                Set the cross correlation factor.

                :param factor: Cross correlation factor.

                """
                if not isinstance(factor, int) or factor < 1:
                    raise ValueError("factor must be a positive integer")
                self.instrument.write(f":SENSe:PNoise:XCORr:FACTor {factor}")

            def get_factor(self):
                """
                Query the cross correlation factor.

                :return: The cross correlation factor.
                """
                return int(self.instrument.query(":SENSe:PNoise:XCORr:FACTor?"))

            def set_gain_indicator_state(self, state):
                """
                Show/hide the gain indicator.

                :param state: 1/0 or 'ON'/'OFF' to show/hide the gain indicator.

                """
                if isinstance(state, str):
                    state = state.upper()
                    if state not in {"ON", "OFF"}:
                        raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                    state = 1 if state == "ON" else 0
                elif state not in [0, 1]:
                    raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                self.instrument.write(f":DISPlay:PNoise:XCORr:GINdicator:STATe {state}")

            def is_gain_indicator_enabled(self):
                """
                Query if gain indicator is shown.

                :return:  True if gain indicator is shown, False otherwise.
                """
                resp = self.instrument.query(":DISPlay:PNoise:XCORr:GINdicator:STATe?")
                return int(resp.strip()) == 1

            def set_count_state(self, state):
                """
                Show/hide the cross correlation counts.

                :param state: 1/0 or 'ON'/'OFF' to show/hide the counts.

                """
                if isinstance(state, str):
                    state = state.upper()
                    if state not in {"ON", "OFF"}:
                        raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                    state = 1 if state == "ON" else 0
                elif state not in [0, 1]:
                    raise ValueError("state must be 1, 0, 'ON', or 'OFF'")
                self.instrument.write(f":DISPlay:PNoise:XCORr:COUNt:STATe {state}")

            def is_count_enabled(self):
                """
                Query if cross correlation counts are shown.

                :return:  True if counts are shown, False otherwise.
                """
                resp = self.instrument.query(":DISPlay:PNoise:XCORr:COUNt:STATe?")
                return int(resp.strip()) == 1

            def restart_measurement(self):
                """
                Restart a cross correlation measurement.


                """
                self.instrument.write(":SENSe:PNoise:XCORr:MEAS:RESTart")

            def get_measurement_progress(self):
                """
                Track the progress of the cross correlation measurement.

                :return: Progress value between [0, XCorr factor], or -1 if not enabled.
                """
                return int(self.instrument.query(":SENSe:PNoise:XCORr:MEAS:PROGress?"))
            class Device:
                """
                The Device commands control the cross correlation device settings in phase noise measurement mode.
                """
                def __init__(self, instrument,data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler

                def is_active(self):
                    """
                    Returns true if second SM device is connected.

                    
                    :return: True if a device is currently connected and active, False otherwise.
                    """
                    resp = self.instrument.query(":SENSe:PNoise:XCORr:DEVice:ACTive?")
                    return resp.strip() == '1'

                def get_count(self):
                    """
                    Returns the number of devices connected to the PC.

                    
                    Return:
                    int: The number of devices connected to the PC.
                    """
                    return int(self.instrument.query(":SENSe:PNoise:XCORr:DEVice:COUNt?"))

                def get_list(self):
                    """
                    Returns a list of all SM devices that can be used as the second analyzer for cross correlation measurements.

                    
                    Return:
                    str: The list of connected devices.
                    """
                    return self.instrument.query(":SENSe:PNoise:XCORr:DEVice:LIST?")

                def get_current(self):
                    """
                    Returns the name of the second analyzer, if active.

                    
                    Return:
                    str: The currently active device.
                    """
                    return self.instrument.query(":SENSe:PNoise:XCORr:DEVice:CURRent?")

                def connect(self, device_index):
                    """
                    Connects the second analyzer. Must be one of the names returned from the LIST? command.

                    :param device_index: The index of the device to connect.
                    """
                    if not isinstance(device_index, int) or device_index < 0:
                        raise ValueError("device_index must be a non-negative integer")
                    self.instrument.write(f":SENSe:PNoise:XCORr:DEVice:CONnect? {device_index}")

                def disconnect(self):
                    """
                    Disconnects the second analyzer.

                    
                    
                    """
                    self.instrument.write(":SENSe:PNoise:XCORr:DEVice:DISConnect?")

        class VCO_PN:
            """
            The VCO commands control the VCO settings in phase noise measurement mode.
            """
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler

            def is_active(self):
                """
                Returns whether the PN400 is connected in the software.

                
                :return:  True if the PN400 is connected in the software, False otherwise.
                """
                resp = self.instrument.query(":SENSe:PNoise:VCO:ACTive?")
                return resp.strip() == '1'

            def connect(self):
                """
                Connects the PN400 and returns true if successful. If the PN400 is
                already connected, then returns true immediately.

                
                :return:  True if PN400 is connected successfully, False otherwise.
                """
                resp = self.instrument.query(":SENSe:PNoise:VCO:CONnect?")
                return resp.strip() == '1'

            def set_voltage_state(self, state):
                """
                Enable/disable the supply and tune output voltages.

                :param state: 1/0 or 'ON'/'OFF' to enable/disable the supply and tune output voltages.

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
                Query if supply and tune output voltages are enabled.

                
                :return:  True if supply and tune output voltages are enabled, False otherwise.
                """
                resp = self.instrument.query(":SENSe:PNoise:VCO:VOLTage:STATe?")
                return int(resp.strip()) == 1

            def set_supply_min(self, value):
                """
                :param value: Minimum supply voltage.

                """
                self.instrument.write(f":SENSe:PNoise:VCO:VOLTage:SUPply:MIN {value}")

            def get_supply_min(self):
                """
                
                :return: Minimum supply voltage.
                """
                return float(self.instrument.query(":SENSe:PNoise:VCO:VOLTage:SUPply:MIN?"))

            def set_supply_max(self, value):
                """
                :param value: Maximum supply voltage.

                """
                self.instrument.write(f":SENSe:PNoise:VCO:VOLTage:SUPply:MAX {value}")

            def get_supply_max(self):
                """
                
                :return: Maximum supply voltage.
                """
                return float(self.instrument.query(":SENSe:PNoise:VCO:VOLTage:SUPply:MAX?"))

            def set_supply(self, value):
                """
                :param value: Supply voltage.

                """
                self.instrument.write(f":SENSe:PNoise:VCO:VOLTage:SUPply {value}")

            def get_supply(self):
                """
                
                :return: Supply voltage.
                """
                return float(self.instrument.query(":SENSe:PNoise:VCO:VOLTage:SUPply?"))

            def set_tune_min(self, value):
                """
                :param value: Minimum tune voltage.

                """
                self.instrument.write(f":SENSe:PNoise:VCO:VOLTage:TUNE:MIN {value}")

            def get_tune_min(self):
                """
                
                :return: Minimum tune voltage.
                """
                return float(self.instrument.query(":SENSe:PNoise:VCO:VOLTage:TUNE:MIN?"))

            def set_tune_max(self, value):
                """
                :param value: Maximum tune voltage.

                """
                self.instrument.write(f":SENSe:PNoise:VCO:VOLTage:TUNE:MAX {value}")

            def get_tune_max(self):
                """
                
                :return: Maximum tune voltage.
                """
                return float(self.instrument.query(":SENSe:PNoise:VCO:VOLTage:TUNE:MAX?"))

            def set_tune(self, value):
                """
                :param value: Tune voltage.

                """
                self.instrument.write(f":SENSe:PNoise:VCO:VOLTage:TUNE {value}")

            def get_tune(self):
                """
                
                :return: Tune voltage.
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
            :param state: 1/0 or 'ON'/'OFF' to enable/disable the Peak Table panel.

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
            Enables/disables the Peak Table panel.

            
            :return:  True if Peak Table panel is enabled, False otherwise.
            """
            resp = self.instrument.query(":SENSe:PEAK:TABLe:STATe?")
            return int(resp.strip()) == 1

        def set_trace(self, trace_num):
            """
            Selects which trace the peak measurements are performed on.

            :param trace_num: Trace index.

            """
            self.instrument.write(f":SENSe:PEAK:TABLe:TRACe {trace_num}")

        def get_trace(self):
            """
            Queries which trace is used for peak measurement.

            
            :return: The trace index used for peak measurement.
            """
            return int(self.instrument.query(":SENSe:PEAK:TABLe:TRACe?"))

        def set_threshold(self, value):
            """
            Specify the peak threshold in dBm. A point must exceed this amount
            before being considered as a peak. Once the threshold test is met, then the
            excursion test is ran. If it meets both, then a point is considered a peak.

            :param value: Peak threshold in dBm.

            """
            self.instrument.write(f":SENSe:PEAK:TABLe:THReshold {value}")

        def get_threshold(self):
            """
            Queries the current peak threshold in dBm.

            
            :return: The current peak threshold in dBm.
            """
            return float(self.instrument.query(":SENSe:PEAK:TABLe:THReshold?"))

        def set_excursion(self, value):
            """
            Specify the peak excursion in dB. How many dB above surrounding
            points the point must be before being considered a peak.

            :param value: Peak excursion in dB.

            """
            self.instrument.write(f":SENSe:PEAK:TABLe:EXCursion {value}")

        def get_excursion(self):
            """
            Queries the current peak excursion in dB.

            
            :return: The current peak excursion in dB.
            """
            return float(self.instrument.query(":SENSe:PEAK:TABLe:EXCursion?"))

        def set_sort(self, order):
            """
            Specifies the sort order of the table. Peaks can be sorted by frequency or
            amplitude. Frequency is ascending; amplitude is descending.

            :param order: 'FREQUENCY' or 'AMPLITUDE'.

            """
            allowed = {"FREQUENCY", "AMPLITUDE"}
            if not isinstance(order, str) or order.upper() not in allowed:
                raise ValueError("order must be 'FREQUENCY' or 'AMPLITUDE'")
            self.instrument.write(f":SENSe:PEAK:TABLe:SORT {order.upper()}")

        def get_sort(self):
            """
            Queries the current sort order.

            
            :return: The current sort order.
            """
            return self.instrument.query(":SENSe:PEAK:TABLe:SORT?")

        def get_count(self):
            """
            Returns the number of peaks in the table. This is the number of peaks that
            have met the criteria specified. This value can change after each sweep.

            
            :return: The number of peaks in the table.
            """
            return int(self.instrument.query(":SENSe:PEAK:TABLe:COUNt?"))

        def set_max(self, value):
            """
            Specify the maximum number of peaks that can appear in the table. This value
            must be between [0, 99].

            :param value: Maximum number of peaks [0,99].

            """
            if not isinstance(value, int) or not (0 <= value <= 99):
                raise ValueError("value must be an integer between 0 and 99")
            self.instrument.write(f":SENSe:PEAK:TABLe:MAX {value}")

        def get_max(self):
            """
            Queries the maximum number of peaks.

            
            :return: The maximum number of peaks.
            """
            return int(self.instrument.query(":SENSe:PEAK:TABLe:MAX?"))

        def get_frequency(self, peak_num):
            """
            Returns the frequency of the specified peak.

            :param peak_num: Peak index [1,16].
            :return: Frequency of the specified peak.
            """
            return float(self.instrument.query(f":SENSe:PEAK:TABLe:FREQuency? {peak_num}"))

        def get_amplitude(self, peak_num):
            """
            Returns the amplitude of the specified peak.

            :param peak_num: Peak index [1,16].
            :return: Amplitude of the specified peak.
            """
            return float(self.instrument.query(f":SENSe:PEAK:TABLe:AMPLitude? {peak_num}"))

        def get_frequency_delta(self, peak_num):
            """
            Returns the frequency difference between the specified peak
            and the first peak in the list.

            :param peak_num: Peak index [1,16].
            :return: Frequency difference between the specified peak and the first peak.
            """
            return float(self.instrument.query(f":SENSe:PEAK:TABLe:FREQuency:DELTa? {peak_num}"))

        def get_amplitude_delta(self, peak_num):
            """
            Returns the amplitude difference between the specified peak
            and the first peak in the list.

            :param peak_num: Peak index [1,16].
            :return: Amplitude difference between the specified peak and the first peak.
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
            Enables/disables the channel power measurement.

            :param state: 1/0 or 'ON'/'OFF' to enable/disable channel power measurement.

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
            Queries if channel power measurement is enabled.

            
            :return: True if channel power measurement is enabled, False otherwise.
            """
            resp = self.instrument.query(":SENSe:CHPower:STATe?")
            return int(resp.strip()) == 1

        def set_trace(self, trace_num):
            """
            Selects which trace the channel power measurement is performed on.

            :param trace_num: Trace index.

            """
            self.instrument.write(f":SENSe:CHPower:TRACe {trace_num}")

        def get_trace(self):
            """
            Queries which trace is used for channel power measurement.

            
            :return: The trace index used for channel power measurement.
            """
            return int(self.instrument.query(":SENSe:CHPower:TRACe?"))

        def set_width(self, freq):
            """
            Specifies the width of the main channel power measurement as a frequency.

            :param freq: Width of the main channel (Hz).

            """
            self.instrument.write(f":SENSe:CHPower:WIDth {freq}")

        def get_width(self):
            """
            Queries the width of the main channel power measurement.

            
            :return: The width of the main channel (Hz).
            """
            return float(self.instrument.query(":SENSe:CHPower:WIDth?"))

        def set_channel_state(self, channel_num, state):
            """
            Enables/disables the measurement of an adjacent channel.

            :param channel_num: Channel index.
            :param state: 1/0 or 'ON'/'OFF' to enable/disable adjacent channel.

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
            Queries if measurement of an adjacent channel is enabled.

            :param channel_num: Channel index.
            :return: True if adjacent channel is enabled, False otherwise.
            """
            resp = self.instrument.query(f":SENSe:CHPower:CHANnel:STATe? {channel_num}")
            return int(resp.strip()) == 1

        def set_channel_offset(self, channel_num, freq):
            """
            Specifies the offset from center of an adjacent channel.

            :param channel_num: Channel index.
            :param freq: Offset from center (Hz).

            """
            self.instrument.write(f":SENSe:CHPower:CHANnel:OFFSet {channel_num},{freq}")

        def get_channel_offset(self, channel_num):
            """
            Queries the offset from center of an adjacent channel.

            :param channel_num: Channel index.
            :return: Offset from center (Hz).
            """
            return float(self.instrument.query(f":SENSe:CHPower:CHANnel:OFFSet? {channel_num}"))

        def set_channel_width(self, channel_num, freq):
            """
            Specifies the width of an adjacent channel.

            :param channel_num: Channel index.
            :param freq: Channel width (Hz).

            """
            self.instrument.write(f":SENSe:CHPower:CHANnel:WIDth {channel_num},{freq}")

        def get_channel_width(self, channel_num):
            """
            Queries the width of an adjacent channel.

            :param channel_num: Channel index.
            :return: Channel width (Hz).
            """
            return float(self.instrument.query(f":SENSe:CHPower:CHANnel:WIDth? {channel_num}"))

        def get_chpower(self):
            """
            Returns the channel power of the main channel. The value has units equal to the units currently selected in reference level.

            
            :return: Channel power of the main channel.
            """
            return float(self.instrument.query(":SENSe:CHPower:CHPower?"))

        def get_chpower_lower(self, channel_num):
            """
            Returns the lower channel power of an adjacent channel as dBm.

            :param channel_num: Channel index.
            :return: Lower channel power of adjacent channel (dBm).
            """
            return float(self.instrument.query(f":SENSe:CHPower:CHPower:LOWer? {channel_num}"))

        def get_chpower_upper(self, channel_num):
            """
            Returns the upper channel power of an adjacent channel as dBm.

            :param channel_num: Channel index.
            :return: Upper channel power of adjacent channel (dBm).
            """
            return float(self.instrument.query(f":SENSe:CHPower:CHPower:UPPer? {channel_num}"))

        def get_acpower_lower(self, channel_num):
            """
            Returns the lower adjacent power of an adjacent channel as dBc.

            :param channel_num: Channel index.
            :return: Lower adjacent power of adjacent channel (dBc).
            """
            return float(self.instrument.query(f":SENSe:CHPower:ACPower:LOWer? {channel_num}"))

        def get_acpower_upper(self, channel_num):
            """
            Returns the upper adjacent power of an adjacent channel as dBc.

            :param channel_num: Channel index.
            :return: Upper adjacent power of adjacent channel (dBc).
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
            Enable or disable application of this path loss table.

            :param state: 1/0 or 'ON'/'OFF' to enable/disable this path loss table.

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
            Query if application of this path loss table is enabled.

            
            :return:  True if this path loss table is enabled, False otherwise.
            """
            resp = self.instrument.query(f":SENSe:CORRection:PATHloss{self.table_num}:STATe?")
            return resp.strip() == 1

        def set_description(self, desc):
            """
            Specify the name/description of this path loss table.

            :param desc: The name/description of this path loss table.

            """
            self.instrument.write(f':SENSe:CORRection:PATHloss{self.table_num}:DESCription "{desc}"')

        def get_description(self):
            """
            Query the name/description of this path loss table.

            
            :return: The name/description of this path loss table.
            """
            return self.instrument.query(f":SENSe:CORRection:PATHloss{self.table_num}:DESCription?")

        def get_points_count(self):
            """
            Returns the number of points in the path loss table as an integer.

            
            :return: Number of points in the path loss table.
            """
            return int(self.instrument.query(f":SENSe:CORRection:PATHloss{self.table_num}:POINts?"))

        def set_data(self, points):
            """
            Specify the points in the path loss table, will override any existing points.
            Points are specified as freq/offset pairs where the offset is specified as dB.

            :param points: List of (freq, offset) pairs.

            """
            if not isinstance(points, list) or not all(isinstance(p, tuple) and len(p) == 2 for p in points):
                raise ValueError("points must be a list of (freq, offset) tuples")
            data_str = ", ".join(f"{freq},{offset}" for freq, offset in points)
            self.instrument.write(f":SENSe:CORRection:PATHloss{self.table_num}:DATA {data_str}")

        def get_data(self):
            """
            Returns the points in the path loss table. Points are returned as freq/offset
            pairs where the frequencies are specified as Hz and the offsets as dB.

            
            :return: The points in the path loss table as freq/offset pairs.
            """
            response = self.instrument.query(f":SENSe:CORRection:PATHloss{self.table_num}:DATA?")
            if self.data_handler.is_auto_saving_data_enabled():
                self.data_handler.write_to_file(self, "CORR_PATHLOSS", response, file_type = EFileType.CSV, headers = None)
            return response

        def clear(self):
            """
            Resets the selected path loss table. Removes all points stored.

            

            """
            self.instrument.write(f":SENSe:CORRection:PATHloss{self.table_num}:CLEAr")

        @staticmethod
        def clear_all(instrument):
            """
            Resets all path loss tables.

            :param instrument: The instrument instance.

            """
            instrument.write(":SENSe:CORRection:PATHloss:ALL:CLEAr")

    class Frequency_Sense:
        """
        The Frequency commands control the frequency range and step of the sweep in swept analysis mode.
        """
        def __init__(self, instrument,data_handler):
            self.instrument = instrument
            self.data_handler = data_handler

        def set_center(self, freq):
            """
            Set the measurement center frequency.

            This can cause the start or stop frequency to change if the device is unable to maintain the current span with the new center frequency.
            This can have the side effect of changing the span/start/stop frequencies.

            :param freq: Center frequency in Hz, or 'UP', or 'DOWN'.

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
            Query the current center frequency.

            Returned as Hz. By passing the MIN or MAX arguments, the user can query the upper and lower frequency limits for a sweep.

            :param bound: 'MIN' or 'MAX' to query frequency limits, or None for current center.
            :return: The center frequency in Hz, or the min/max limit.
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
            Change the sweep start frequency.

            The lower bound for the start frequency is determined with the CENT? MIN command.

            :param freq: Start frequency in Hz.

            """
            self.instrument.write(f":SENSe:FREQuency:STARt {freq}")

        def get_start(self):
            """
            Query the current measurement start frequency in Hz.

            
            :return: The current measurement start frequency in Hz.
            """
            return float(self.instrument.query(":SENSe:FREQuency:STARt?"))

        def set_stop(self, freq):
            """
            Set the sweep stop frequency.

            The upper bound for the stop frequency is determined with the CENT? MAX command.

            :param freq: Stop frequency in Hz.

            """
            self.instrument.write(f":SENSe:FREQuency:STOP {freq}")

        def get_stop(self):
            """
            Query the current measurement stop frequency in Hz.

            
            :return: The current measurement stop frequency in Hz.
            """
            return float(self.instrument.query(":SENSe:FREQuency:STOP?"))

        def set_center_step(self, freq):
            """
            Set the step amount the center frequency changes by when using the UP or DOWN parameters on the CENTer command.

            :param freq: Step amount for center frequency changes in Hz.

            """
            self.instrument.write(f":SENSe:FREQuency:CENTer:STEP {freq}")

        def get_center_step(self):
            """
            Query the center frequency step size in Hz.

            
            :return: The center frequency step size in Hz.
            """
            return float(self.instrument.query(":SENSe:FREQuency:CENTer:STEP?"))

        def set_span(self, span):
            """
            Set the sweep span.

            This will change the start/stop and potentially center frequency of the sweep in attempt to meet the span requested.

            :param span: Span in Hz, or 'UP', or 'DOWN'.

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
            Query the span in Hz.

            
            :return: The span in Hz.
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
            Set the reference level. If UP or DOWN is specified, the reference level is
            increased or decreased by the div amount (when reference level is a logarithmic unit).

            :param amplitude: Reference level in dBm or 'UP'/'DOWN'.

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
            Return the current reference level as dBm.

            
            :return: The current reference level as dBm.
            """
            return float(self.instrument.query(":SENSe:POWer:RF:RLEVel?"))

        def get_reference_level_unit(self):
            """
            Return the current amplitude unit used to express reference level.

            
            :return: The current amplitude unit used to express reference level.
            """
            return self.instrument.query(":SENSe:POWer:RF:RLEVel:UNIT?")

        def set_reference_level_offset(self, offset):
            """
            Set the reference level offset in dB.

            :param offset: Reference level offset in dB.

            """
            self.instrument.write(f":SENSe:POWer:RF:RLEVel:OFFSet {offset}")

        def get_reference_level_offset(self):
            """
            Return the reference level offset in dB.

            
            :return: The reference level offset in dB.
            """
            return float(self.instrument.query(":SENSe:POWer:RF:RLEVel:OFFSet?"))

        def set_plot_vertical_division(self, division):
            """
            Specify the plot vertical division (1/10th of the plot height) as dB.
            Logarithmic scale only.

            :param division: Plot vertical division in dB.

            """
            self.instrument.write(f":SENSe:POWer:RF:PDIVision {division}")

        def get_plot_vertical_division(self):
            """
            Return the plot vertical division in dB.

            
            :return: The plot vertical division in dB.
            """
            return float(self.instrument.query(":SENSe:POWer:RF:PDIVision?"))

        def set_attenuation(self, value):
            """
            Specify the attenuation index. It is recommended to leave attenuation set to auto
            and set the reference level instead.

            :param value: Attenuation index.

            """
            if not isinstance(value, int):
                raise ValueError("value must be an integer")
            self.instrument.write(f":SENSe:POWer:RF:ATTenuation {value}")

        def get_attenuation(self):
            """
            Return the attenuation index.

            
            :return: The attenuation index.
            """
            return int(self.instrument.query(":SENSe:POWer:RF:ATTenuation?"))

        def set_attenuation_auto(self, state):
            """
            Enable/disable auto attenuation.

            :param state: 1/0 or 'ON'/'OFF' to enable/disable auto attenuation.

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
            Query if auto attenuation is enabled.

            
            :return:  True if auto attenuation is enabled, False otherwise.
            """
            resp = self.instrument.query(":SENSe:POWer:RF:ATTenuation:AUTO?")
            return resp.strip() == 1

        def set_gain(self, value):
            """
            Specify the gain index. It is recommended to leave gain set to auto and set
            the reference level instead.

            :param value: Gain index.

            """
            if not isinstance(value, int):
                raise ValueError("value must be an integer")
            self.instrument.write(f":SENSe:POWer:RF:GAIN {value}")

        def get_gain(self):
            """
            Return the gain index.

            
            :return: The gain index.
            """
            return int(self.instrument.query(":SENSe:POWer:RF:GAIN?"))

        def set_gain_auto(self, state):
            """
            Enable/disable auto gain.

            :param state: 1/0 or 'ON'/'OFF' to enable/disable auto gain.

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
            Query if auto gain is enabled.

            
            :return:  True if auto gain is enabled, False otherwise.
            """
            resp = self.instrument.query(":SENSe:POWer:RF:GAIN:AUTO?")
            return resp.strip() == 1

        def set_preamp(self, value):
            """
            Specify whether the preamp is on/off. Only valid for the SA devices.
            It is recommended to leave preamp set to auto and set the reference level instead.

            :param value: Preamp state (typically 0 or 1).

            """
            if value not in [0, 1]:
                raise ValueError("value must be 0 or 1")
            self.instrument.write(f":SENSe:POWer:RF:PREAMP {value}")

        def get_preamp(self):
            """
            Return the preamp state (0 or 1).

            
            :return: The preamp state (0 or 1).
            """
            return int(self.instrument.query(":SENSe:POWer:RF:PREAMP?"))

        def set_preamp_auto(self, state):
            """
            Enable/disable auto preamp.

            :param state: 1/0 or 'ON'/'OFF' to enable/disable auto preamp.

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
            Query if auto preamp is enabled.

            
            :return:  True if auto preamp is enabled, False otherwise.
            """
            resp = self.instrument.query(":SENSe:POWer:RF:PREAMP:AUTO?")
            return resp.strip() == 1

        def set_preselector_state(self, state):
            """
            SM200A only. Set the preselector state on or off. The preselector filters affected by this setting are below 650MHz.

            :param state: 1/0 or 'ON'/'OFF' to enable/disable preselector (SM200A only).

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
            Query if preselector is enabled.

            
            :return:  True if preselector is enabled, False otherwise.
            """
            resp = self.instrument.query(":SENSe:POWer:RF:MW:PRESelector:STATe?")
            return resp.strip() == 1

        def set_spur_reject(self, state):
            """
            Enable/Disable the software spur reject algorithm.

            :param state: 1/0 or 'ON'/'OFF' to enable/disable spur reject.

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
            Query if spur reject is enabled.

            
            :return:  True if spur reject is enabled, False otherwise.
            """
            resp = self.instrument.query(":SENSe:POWer:RF:SPURReject?")
            return resp.strip() == 1

        def set_rf_division(self, division):
            """
            Specify the plot vertical division (1/10th of the plot height) as dB.

            :param division: Plot vertical division (1/10th of the plot height) as dB.

            """
            self.instrument.write(f":SENSe:POWer:RF:PDIVision {division}")

        def get_rf_division(self):
            """
            Return the plot vertical division as dB.

            
            :return: The plot vertical division as dB.
            """
            return float(self.instrument.query(":SENSe:POWer:RF:PDIVision?"))

        def get_rlevel(self):
            """
            Return the current reference level as dBm.

            
            :return: The current reference level as dBm.
            """
            return float(self.instrument.query(":SENSe:POWer:RF:RLEVel?"))
    class Bandwidth_Sense:
        """
        The Bandwidth commands control the FFT processing for the receivers.
        """
        def __init__(self, instrument,data_handler):
            self.instrument = instrument
            self.data_handler = data_handler

        def set_resolution(self, freq):
            """
            Specify the resolution bandwidth (RBW). If UP or DOWN is specified, the RBW is stepped in a 1/3/10 sequence.

            :param freq: RBW in Hz, or 'UP', or 'DOWN'.

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
            Query the current resolution bandwidth (RBW) in Hz.

            
            :return: The current RBW in Hz.
            """
            return float(self.instrument.query(":SENSe:BANDwidth:RESolution?"))

        def set_resolution_auto(self, state):
            """
            Enable or disable automatic RBW selection.

            :param state: 1/0 or 'ON'/'OFF' to enable/disable auto RBW.

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
            Query if automatic RBW selection is enabled.

            
            :return:  True if auto RBW is enabled, False otherwise.
            """
            resp = self.instrument.query(":SENSe:BANDwidth:RESolution:AUTO?")
            return resp.strip() == 1

        def set_video(self, freq):
            """
            Specify the video bandwidth (VBW). If UP or DOWN is specified, the VBW is stepped in a 1/3/10 sequence.

            :param freq: VBW in Hz, or 'UP', or 'DOWN'.

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
            Query the current video bandwidth (VBW) in Hz.

            
            :return: The current VBW in Hz.
            """
            return float(self.instrument.query(":SENSe:BANDwidth:VIDeo?"))

        def set_video_auto(self, state):
            """
            Enable or disable automatic VBW selection.

            :param state: 1/0 or 'ON'/'OFF' to enable/disable auto VBW.

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
            Query if automatic VBW selection is enabled.

            
            :return:  True if auto VBW is enabled, False otherwise.
            """
            resp = self.instrument.query(":SENSe:BANDwidth:VIDeo:AUTO?")
            return resp.strip() == 1

        def set_shape(self, shape):
            """
            Specify the FFT window function.

            :param shape: 'FLATTOP', 'NUTTALL', or 'GAUSSIAN'.

            """
            allowed = {"FLATTOP", "NUTTALL", "GAUSSIAN"}
            if not isinstance(shape, str) or shape.upper() not in allowed:
                raise ValueError("shape must be one of 'FLATTOP', 'NUTTALL', or 'GAUSSIAN'")
            self.instrument.write(f":SENSe:BANDwidth:SHAPe {shape.upper()}")

        def get_shape(self):
            """
            Query the current FFT window function.

            
            :return: The current FFT window function.
            """
            return self.instrument.query(":SENSe:BANDwidth:SHAPe?")
    class Sweep_Sense:
        """
        The Sweep commands control additional FFT settings of the receiver.
        """
        def __init__(self, instrument,data_handler):
            self.instrument = instrument
            self.data_handler = data_handler
            self.detector = self.Detector_Sweep_Sense(self.instrument, self.data_handler)
        def set_time(self, value):
            """
            Set the overall acquisition length for the sweep.

            If the sweep time is smaller than needed for the current RBW/VBW settings, sweep time is ignored.
            If sweep time is longer than necessary for the current RBW/VBW settings, VBW is lowered internally to meet the requested sweep time.
            The VBW is lowered internally and won’t be represented in the VBW settings.

            :param value: Sweep time in seconds.

            """
            self.instrument.write(f":SENSe:SWEep:TIME {value}")

        def get_time(self):
            """
            Query the overall acquisition length for the sweep.

            If the sweep time is smaller than needed for the current RBW/VBW settings, sweep time is ignored.
            If sweep time is longer than necessary for the current RBW/VBW settings, VBW is lowered internally to meet the requested sweep time.
            The VBW is lowered internally and won’t be represented in the VBW settings.

            
            :return: The current sweep time in seconds.
            """
            return float(self.instrument.query(":SENSe:SWEep:TIME?"))

        class Detector_Sweep_Sense:
            """
            The Detector commands control how the VBW processing is performed.
            """
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler

            def set_function(self, func):
                """
                Controls how the VBW processing is performed.
                If 'AVERAGE', overlapping FFTs are averaged together.
                If 'MINMAX', overlapping FFTs are min/max held.
                'MIN' or 'MAX' returns only one of the resulting arrays.

                :param func: 'AVERAGE', 'MINMAX', 'MIN', or 'MAX'.

                """
                allowed = {"AVERAGE", "MINMAX", "MIN", "MAX"}
                if not isinstance(func, str) or func.upper() not in allowed:
                    raise ValueError("func must be one of 'AVERAGE', 'MINMAX', 'MIN', or 'MAX'")
                self.instrument.write(f":SENSe:SWEep:DETector:FUNCtion {func.upper()}")

            def get_function(self):
                """
                Controls how the VBW processing is performed.
                If 'AVERAGE', overlapping FFTs are averaged together.
                If 'MINMAX', overlapping FFTs are min/max held.
                'MIN' or 'MAX' returns only one of the resulting arrays.

                
                :return: The current detector function.
                """
                return self.instrument.query(":SENSe:SWEep:DETector:FUNCtion?")

            def set_units(self, units):
                """
                Controls the units in which the detector function is performed in.

                :param units: 'POWER', 'SAMPLE', 'VOLTAGE', or 'LOG'.

                """
                allowed = {"POWER", "SAMPLE", "VOLTAGE", "LOG"}
                if not isinstance(units, str) or units.upper() not in allowed:
                    raise ValueError("units must be one of 'POWER', 'SAMPLE', 'VOLTAGE', or 'LOG'")
                self.instrument.write(f":SENSe:SWEep:DETector:UNITs {units.upper()}")

            def get_units(self):
                """
                Controls the units in which the detector function is performed in.

                
                :return: The current detector units.
                """
                return self.instrument.query(":SENSe:SWEep:DETector:UNITs?")
    class SEMask:
        """
        The SEMask commands control the spectrum emission mask mode.
        """
        def __init__(self, instrument,data_handler):
            self.instrument = instrument
            self.data_handler = data_handler
            self.frequency = self.SEMask_Frequency(self.instrument, self.data_handler)
            self.bandwidth = self.SEMask_Bandwidth(self.instrument, self.data_handler)
            self.sweep = self.SEMask_Sweep(self.instrument, self.data_handler)
            self.reference = self.SEMask_Reference(self.instrument, self.data_handler)
            self.offset = self.SEMask_Offset(self.instrument, self.data_handler)
            self.marker = self.SEMask_Marker(self.instrument, self.data_handler)
        class SEMask_Frequency:
            """
            The SEMask:Frequency commands control the frequency range of the sweeps in spectrum emission mask mode.
            """
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler

            def set_center(self, value):
                """
                :param value: Center frequency in Hz, or 'UP', or 'DOWN'.

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
                Query the center frequency of the measurement.

                
                :return: The center frequency in Hz.
                """
                return float(self.instrument.query(":SENSe:SEMask:FREQuency:CENTer?"))

            def set_center_step(self, value):
                """
                Set the center frequency step amount.

                :param value: Step amount for center frequency changes in Hz.
                
                """
                self.instrument.write(f":SENSe:SEMask:FREQuency:CENTer:STEP {value}")

            def get_center_step(self):
                """
                Query the center frequency step size in Hz.

                
                :return: The center frequency step size in Hz.
                """
                return float(self.instrument.query(":SENSe:SEMask:FREQuency:CENTer:STEP?"))

            def set_span(self, value):
                """
                Set the sweep span.

                :param value: Span in Hz.
                
                """
                self.instrument.write(f":SENSe:SEMask:FREQuency:SPAN {value}")

            def get_span(self):
                """
                Query the sweep span in Hz.

                
                :return: The span in Hz.
                """
                return float(self.instrument.query(":SENSe:SEMask:FREQuency:SPAN?"))


        class SEMask_Bandwidth:
            """
            The SEMask:Bandwidth commands control the FFT processing for the receivers in SEM mode.
            """
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler

            def set_resolution(self, value):
                """
                Specify the resolution bandwidth (RBW). If UP or DOWN is specified, the RBW is stepped in a 1/3/10 sequence.

                :param value: RBW in Hz, or 'UP', or 'DOWN'.

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
                Query the current resolution bandwidth (RBW) in Hz.

                
                :return: The current RBW in Hz.
                """
                return float(self.instrument.query(":SENSe:SEMask:BANDwidth:RESolution?"))

            def set_resolution_auto(self, state):
                """
                Enable or disable automatic RBW selection.

                :param state: 1/0 or 'ON'/'OFF' to enable/disable auto RBW.

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
                Query if automatic RBW selection is enabled.

                
                :return:  True if auto RBW is enabled, False otherwise.
                """
                resp = self.instrument.query(":SENSe:SEMask:BANDwidth:RESolution:AUTO?")
                return int(resp.strip()) == 1

            def set_video(self, value):
                """
                Specify the video bandwidth (VBW). If UP or DOWN is specified, the VBW is stepped in a 1/3/10 sequence.

                :param value: VBW in Hz, or 'UP', or 'DOWN'.

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
                Query the current video bandwidth (VBW) in Hz.

                
                :return: The current VBW in Hz.
                """
                return float(self.instrument.query(":SENSe:SEMask:BANDwidth:VIDeo?"))

            def set_video_auto(self, state):
                """
                Enable or disable automatic VBW selection.

                :param state: 1/0 or 'ON'/'OFF' to enable/disable auto VBW.

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
                Query if automatic VBW selection is enabled.

                
                :return:  True if auto VBW is enabled, False otherwise.
                """
                resp = self.instrument.query(":SENSe:SEMask:BANDwidth:VIDeo:AUTO?")
                return int(resp.strip()) == 1
        class SEMask_Sweep:
            """
            The Sweep commands control the detector and trace settings of the receiver in SEM mode.
            """
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler
                self.detector = self.Detector(self.instrument, self.data_handler)
            class Detector:
                """
                The Detector commands control the detector function and units in SEM mode.
                """
                def __init__(self, instrument,data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler

                def set_function(self, func):
                    """
                    Controls how the VBW processing is performed.
                    If 'AVERAGE', overlapping FFTs are averaged together.
                    If 'MINMAX', overlapping FFTs are min/max held.

                    :param func: 'AVERAGE' or 'MINMAX'
            
                    """
                    allowed = {"AVERAGE", "MINMAX"}
                    if not isinstance(func, str) or func.upper() not in allowed:
                        raise ValueError("func must be 'AVERAGE' or 'MINMAX'")
                    self.instrument.write(f":SENSe:SEMask:SWEep:DETector:FUNCtion {func.upper()}")

                def get_function(self):
                    """
                    Query how the VBW processing is performed.
                    Returns the current detector function: 'AVERAGE' or 'MINMAX'.

                    
                    :return: The current detector function.
                    """
                    return self.instrument.query(":SENSe:SEMask:SWEep:DETector:FUNCtion?")

                def set_units(self, units):
                    """
                    Controls the units in which the detector function is performed.

                    :param units: 'POWER', 'SAMPLE', 'VOLTAGE', or 'LOG'
            
                    """
                    allowed = {"POWER", "SAMPLE", "VOLTAGE", "LOG"}
                    if not isinstance(units, str) or units.upper() not in allowed:
                        raise ValueError("units must be one of 'POWER', 'SAMPLE', 'VOLTAGE', or 'LOG'")
                    self.instrument.write(f":SENSe:SEMask:SWEep:DETector:UNITs {units.upper()}")

                def get_units(self):
                    """
                    Query the units in which the detector function is performed.

                    
                    :return: The current detector units.
                    """
                    return self.instrument.query(":SENSe:SEMask:SWEep:DETector:UNITs?")
        class SEMask_Reference:
            """The Reference commands control the reference measurement settings in SEM mode."""
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler
            def set_trace_type(self, typ):
                """
                Controls how the reference measurement is taken.

                PSD performs a channel power computation, PEAK does a peak search, and DIRECT uses the amplitude value set directly by user.

                :param typ: 'WRITE' or 'MAXHOLD'

                """
                allowed = {"WRITE", "MAXHOLD"}
                if not isinstance(typ, str) or typ.upper() not in allowed:
                    raise ValueError("typ must be 'WRITE' or 'MAXHOLD'")
                self.instrument.write(f":TRACe:SEMask:REF:TYPE {typ.upper()}")

            def get_trace_type(self):
                """
                Controls how the reference measurement is taken.

                PSD performs a channel power computation, PEAK does a peak search, and DIRECT uses the amplitude value set directly by user.

                
                :return: The current trace type.
                """
                return self.instrument.query(":TRACe:SEMask:REF:TYPE?")
            
            def get_type(self):
                """
                Controls how the reference measurement is taken.

                PSD performs a channel power computation, PEAK does a peak search, and DIRECT uses the amplitude value set directly by user.

                
                :return: The current reference measurement type.
                """
                return self.instrument.query(":SENSe:SEMask:REF:TYPE?")

            def set_bandwidth_mode(self, mode):
                """
                Controls the mode of setting the width of the measurement band.

                AUTO chooses a value automatically, MANUAL uses a width entered by user.

                :param mode: 'AUTO' or 'MANUAL'

                """
                allowed = {"AUTO", "MANUAL"}
                if not isinstance(mode, str) or mode.upper() not in allowed:
                    raise ValueError("mode must be 'AUTO' or 'MANUAL'")
                self.instrument.write(f":SENSe:SEMask:REF:BANDwidth:MODE {mode.upper()}")

            def get_bandwidth_mode(self):
                """
                Controls the mode of setting the width of the measurement band.

                AUTO chooses a value automatically, MANUAL uses a width entered by user.

                
                :return: The current bandwidth mode.
                """
                return self.instrument.query(":SENSe:SEMask:REF:BANDwidth:MODE?")

            def set_bandwidth(self, freq):
                """
                Controls the width of the measurement band in manual mode.

                :param freq: The width of the measurement band in Hz.

                """
                self.instrument.write(f":SENSe:SEMask:REF:BANDwidth {freq}")

            def get_bandwidth(self):
                """
                Controls the width of the measurement band in manual mode.

                
                :return: The width of the measurement band in Hz.
                """
                return float(self.instrument.query(":SENSe:SEMask:REF:BANDwidth?"))

            def set_level(self, amplitude):
                """
                Controls the reference amplitude level in direct set mode.

                :param amplitude: Reference amplitude level in dBm.

                """
                self.instrument.write(f":SENSe:SEMask:REF:LEVEL {amplitude}")

            def get_level(self):
                """
                Controls the reference amplitude level in direct set mode.

                
                :return: The reference amplitude level in dBm.
                """
                return float(self.instrument.query(":SENSe:SEMask:REF:LEVEL?"))
        class SEMask_Offset:
            """
            The Offset commands control the offset settings for the spectrum emission mask."""
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler
            def set_offset_parameters(self, offsets):
                """
                :param offsets: List of tuples, each containing (enabled, startFreq, stopFreq, startLimit, stopLimit, mode).
                :param enabled: 'ON', 'OFF', 1, or 0
                :param startFreq: float (Hz)
                :param stopFreq: float (Hz)
                :param startLimit: float
                :param stopLimit: float
                :param mode: 'RELATIVE' or 'ABSOLUTE'

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
                
                :return: The current offset table as a comma separated list.
                """
                response = self.instrument.query(":SENSe:SEMask:OFFSet:DATA?")
                if self.data_handler.is_auto_saving_data_enabled():
                    self.data_handler.write_to_file(self, "SEMASK_OFFSET", response, file_type = EFileType.CSV, headers = None)
                return response

            def is_fail(self):
                """
                Returns 1 if mask fails, 0 if passes.

                
                :return:  True if mask fails, False otherwise.
                """
                resp = self.instrument.query(":SENSe:SEMask:OFFSet:FAIL?")
                return int(resp.strip()) == 1

            def is_offset_fail(self, offset_num):
                """
                Returns 1 if specified offset fails, 0 if it passes.

                :param offset_num: Offset index [1-16].
                :return:  True if specified offset fails, False otherwise.
                """
                if not isinstance(offset_num, int) or not (1 <= offset_num <= 16):
                    raise ValueError("offset_num must be an integer between 1 and 16")
                resp = self.instrument.query(f":SENSe:SEMask:OFFSet{offset_num}:FAIL?")
                return int(resp.strip()) == 1

            def is_lower_fail(self, offset_num):
                """
                Returns 1 if lower range of specified offset fails, 0 if it passes.

                :param offset_num: Offset index [1-16].
                :return:  True if lower range of specified offset fails, False otherwise.
                """
                if not isinstance(offset_num, int) or not (1 <= offset_num <= 16):
                    raise ValueError("offset_num must be an integer between 1 and 16")
                resp = self.instrument.query(f":SENSe:SEMask:OFFSet{offset_num}:LOWer:FAIL?")
                return int(resp.strip()) == 1

            def is_upper_fail(self, offset_num):
                """
                Returns 1 if upper range of specified offset fails, 0 if it passes.

                :param offset_num: Offset index [1-16].
                :return:  True if upper range of specified offset fails, False otherwise.
                """
                if not isinstance(offset_num, int) or not (1 <= offset_num <= 16):
                    raise ValueError("offset_num must be an integer between 1 and 16")
                resp = self.instrument.query(f":SENSe:SEMask:OFFSet{offset_num}:UPper:FAIL?")
                return int(resp.strip()) == 1

            def get_margin(self, offset_num):
                """
                Around peak of specified offset.

                :param offset_num: Offset index [1-16].
                :return: of specified offset.
                """
                if not isinstance(offset_num, int) or not (1 <= offset_num <= 16):
                    raise ValueError("offset_num must be an integer between 1 and 16")
                return float(self.instrument.query(f":SENSe:SEMask:OFFSet{offset_num}:MARgin?"))

            def get_margin_lower(self, offset_num):
                """
                Lower range of specified offset.

                :param offset_num: Offset index [1-16].
                :return: Lower range of specified offset.
                """
                if not isinstance(offset_num, int) or not (1 <= offset_num <= 16):
                    raise ValueError("offset_num must be an integer between 1 and 16")
                return float(self.instrument.query(f":SENSe:SEMask:OFFSet{offset_num}:MARgin:LOWer?"))

            def get_margin_upper(self, offset_num):
                """
                peak) of upper range of specified offset.

                :param offset_num: Offset index [1-16].
                :return: upper range of specified offset.
                """
                if not isinstance(offset_num, int) or not (1 <= offset_num <= 16):
                    raise ValueError("offset_num must be an integer between 1 and 16")
                return float(self.instrument.query(f":SENSe:SEMask:OFFSet{offset_num}:MARgin:UPper?"))

            def get_peak_level_lower(self, offset_num):
                """
                Retrieves peak level of lower range of specified offset.

                :param offset_num: Offset index [1-16].
                :return: Peak level of lower range of specified offset.
                """
                if not isinstance(offset_num, int) or not (1 <= offset_num <= 16):
                    raise ValueError("offset_num must be an integer between 1 and 16")
                return float(self.instrument.query(f":SENSe:SEMask:OFFSet{offset_num}:PEAK:LEVel:LOWer?"))

            def get_peak_level_upper(self, offset_num):
                """
                Retrieves peak level of upper range of specified offset.

                :param offset_num: Offset index [1-16].
                :return: Peak level of upper range of specified offset.
                """
                if not isinstance(offset_num, int) or not (1 <= offset_num <= 16):
                    raise ValueError("offset_num must be an integer between 1 and 16")
                return float(self.instrument.query(f":SENSe:SEMask:OFFSet{offset_num}:PEAK:LEVel:UPper?"))

            def get_peak_frequency_lower(self, offset_num):
                """
                Retrieves frequency at peak of lower range of specified offset.

                :param offset_num: Offset index [1-16].
                :return: Frequency at peak of lower range of specified offset.
                """
                if not isinstance(offset_num, int) or not (1 <= offset_num <= 16):
                    raise ValueError("offset_num must be an integer between 1 and 16")
                return float(self.instrument.query(f":SENSe:SEMask:OFFSet{offset_num}:PEAK:FREQuency:LOWer?"))

            def get_peak_frequency_upper(self, offset_num):
                """
                Retrieves frequency at peak of upper range of specified offset.

                :param offset_num: Offset index [1-16].
                :return: Frequency at peak of upper range of specified offset.
                """
                if not isinstance(offset_num, int) or not (1 <= offset_num <= 16):
                    raise ValueError("offset_num must be an integer between 1 and 16")
                return float(self.instrument.query(f":SENSe:SEMask:OFFSet{offset_num}:PEAK:FREQuency:UPper?"))

        class SEMask_Marker:
            """
            The Marker commands control the marker in spectrum emission mask mode.
            """
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler

            def enable(self, state):
                """
                Turn the marker on/off.

                :param state: 1/0 or 'ON'/'OFF' to enable/disable the marker.

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
                Query if marker is enabled.

                
                :return:  True if marker is enabled, False otherwise.
                """
                resp = self.instrument.query(":CALCulate:SEMask:MARKer:STATe?")
                return int(resp.strip()) == 1

            def set_delta(self, state):
                """
                When delta is enabled, the delta reference takes the current marker position
                and the marker measurement returns the delta frequency and amplitude between
                the current marker position and the delta reference.

                :param state: 1/0 or 'ON'/'OFF' to enable/disable delta marker.

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
                Query if delta marker is enabled.

                
                :return:  True if delta marker is enabled, False otherwise.
                """
                resp = self.instrument.query(":CALCulate:SEMask:MARKer:DELTa?")
                return int(resp.strip()) == 1

            def set_x(self, freq):
                """
                Move the marker position to the specified frequency.

                :param freq: Frequency to move marker to (Hz).

                """
                self.instrument.write(f":CALCulate:SEMask:MARKer:X {freq}")

            def get_x(self):
                """
                Retrieve the marker position frequency as Hz.

                
                :return: The marker position frequency (Hz).
                """
                return float(self.instrument.query(":CALCulate:SEMask:MARKer:X?"))

            def get_y(self):
                """
                Retrieve the marker position amplitude.

                
                :return: The marker position amplitude.
                """
                return float(self.instrument.query(":CALCulate:SEMask:MARKer:Y?"))

            def maximum(self):
                """
                Perform a peak search.

                

                """
                self.instrument.write(":CALCulate:SEMask:MARKer:MAXimum")

            def minimum(self):
                """
                Perform a minimum search.

                

                """
                self.instrument.write(":CALCulate:SEMask:MARKer:MINimum")

            def next(self):
                """
                Move marker to next graph on plot.

                

                """
                self.instrument.write(":CALCulate:SEMask:MARKer:NEXT")

            def previous(self):
                """
                Move marker to previous graph on plot.

                

                """
                self.instrument.write(":CALCulate:SEMask:MARKer:PREVious")
    class NFIGure:
        """
        The NFIGure commands control the Noise Figure measurement mode.
        """
        def __init__(self, instrument,data_handler):
            self.instrument = instrument
            self.data_handler = data_handler
            self.frequency = self.NFIGure_Frequency(self.instrument, self.data_handler)
            self.bandwidth = self.NFIGure_Bandwidth(self.instrument, self.data_handler)
            self.correction = self.NFIGure_Correction(self.instrument, self.data_handler)
            self.fetch = self.NFIGure_Fetch(self.instrument, self.data_handler)
        def get_calibration_state(self):
            """
            Returns the current calibration state for noise figure measurements.

            Possible values:
            - 'uncal': No valid calibration stored. High measurement error is likely unless the DUT has at least 30 dB gain.
            - 'semical': A valid calibration is stored, but measurement accuracy is reduced due to configuration changes since last calibration.
            - 'cal': A valid calibration is stored and settings are identical to the current configuration.

            
            :return: The current calibration state ('uncal', 'semical', or 'cal').
            """
            return self.instrument.query(":SENSe:NFIGure:CALibration:STATe?")

        def initiate_calibration(self):
            """
            Begin the calibration process for noise figure measurements.

            

            """
            self.instrument.write(":SENSe:NFIGure:CALibration:INITiate")

        def initiate_measurement(self):
            """
            Begin the measurement process for noise figure measurements.

            

            """
            self.instrument.write(":SENSe:NFIGure:MEASurement:INITiate")

        def continue_process(self):
            """
            Continue the calibration or measurement process after the required next action has been taken.

            

            """
            self.instrument.write(":SENSe:NFIGure:CONTinue")

        def abort(self):
            """
            Abort any calibration or measurement in progress. Corresponding data is not retained.

            

            """
            self.instrument.write(":SENSe:NFIGure:ABORt")

        def get_next_action(self):
            """
            Query the next action the user needs to take before continuing calibration or measurement.

            
            :return: The next action user needs to take before continuing measurement.
            """
            return self.instrument.query(":STATus:NFIGure:NEXT?")

        def get_progress(self):
            """
            Query the percentage progress of the current sweep. Returns 100% if no sweep is in progress.

            
            :return: The percentage progress of the current sweep.
            """
            return float(self.instrument.query(":STATus:NFIGure:PROGress?"))

        class NFIGure_Frequency:
            """
            The NFIGure:Frequency commands control the list of frequency points for noise figure measurements.
            """
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler

            def set_mode(self, mode):
                """
                Set how the list of measurement frequencies is determined.

                In SWEPt mode, the points are linearly distributed between the Start and Stop frequencies, with Points determining the number of points.
                In FIXed mode, a single frequency is measured, specified by Fixed Freq.

                :param mode: 'SWEPt' or 'FIXed'

                """
                allowed = {"SWEPT", "FIXED"}
                if not isinstance(mode, str) or mode.upper() not in allowed:
                    raise ValueError("mode must be 'SWEPt' or 'FIXed'")
                self.instrument.write(f":SENSe:NFIGure:FREQuency:MODE {mode.upper()}")

            def get_mode(self):
                """
                Query how the list of measurement frequencies is determined.

                
                :return: The current frequency list mode.
                """
                return self.instrument.query(":SENSe:NFIGure:FREQuency:MODE?")

            def set_start(self, freq):
                """
                Change the measurement list start frequency in Swept mode.

                The lower bound for the start frequency is determined with the CENT? MIN command.

                :param freq: Start frequency in Hz.

                """
                self.instrument.write(f":SENSe:NFIGure:FREQuency:STARt {freq}")

            def get_start(self):
                """
                Query the current measurement list start frequency in Hz.

                
                :return: The current start frequency in Hz.
                """
                return float(self.instrument.query(":SENSe:NFIGure:FREQuency:STARt?"))

            def set_stop(self, freq):
                """
                Set the measurement list stop frequency in Swept mode.

                The upper bound for the stop frequency is determined with the CENT? MAX command.

                :param freq: Stop frequency in Hz.

                """
                self.instrument.write(f":SENSe:NFIGure:FREQuency:STOP {freq}")

            def get_stop(self):
                """
                Query the current measurement list stop frequency in Hz.

                
                :return: The current stop frequency in Hz.
                """
                return float(self.instrument.query(":SENSe:NFIGure:FREQuency:STOP?"))

            def set_center(self, freq):
                """
                Set the measurement list center frequency in Swept mode.

                :param freq: Center frequency in Hz.

                """
                self.instrument.write(f":SENSe:NFIGure:FREQuency:CENTer {freq}")

            def get_center(self, bound=None):
                """
                Query the current measurement list center frequency in Hz.

                By passing the MIN or MAX arguments, the user can query the upper and lower frequency limits for a measurement.

                :param bound: 'MIN' or 'MAX' to query frequency limits, or None for current center.
                :return: The center frequency in Hz, or the min/max limit.
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
                Set the measurement list span in Swept mode.

                This will change the start/stop and potentially center frequency of the measurement list in attempt to meet the span requested.

                :param span: Span in Hz.

                """
                self.instrument.write(f":SENSe:NFIGure:FREQuency:SPAN {span}")

            def get_span(self):
                """
                Query the measurement list span in Hz.

                
                :return: The span in Hz.
                """
                return float(self.instrument.query(":SENSe:NFIGure:FREQuency:SPAN?"))

            def set_points(self, num_points):
                """
                Set the number of measurement points distributed across the Span in Swept mode.

                :param num_points: Number of measurement points.

                """
                if not isinstance(num_points, int):
                    raise ValueError("num_points must be an integer")
                self.instrument.write(f":SENSe:NFIGure:FREQuency:POINts {num_points}")

            def get_points(self):
                """
                Query the number of measurement points.

                
                :return: The number of measurement points.
                """
                return int(self.instrument.query(":SENSe:NFIGure:FREQuency:POINts?"))

            def set_fixed(self, freq):
                """
                Set the frequency of the measurement in Fixed mode.

                :param freq: Fixed frequency in Hz.

                """
                self.instrument.write(f":SENSe:NFIGure:FREQuency:FIXed {freq}")

            def get_fixed(self):
                """
                Query the frequency of the measurement in Hz.

                
                :return: The fixed frequency in Hz.
                """
                return float(self.instrument.query(":SENSe:NFIGure:FREQuency:FIXed?"))

            def get_list_data(self):
                """
                Get the list of measurement frequencies in Hz.

                
                :return: The list of measurement frequencies in Hz (comma separated).
                """
                return self.instrument.query(":SENSe:NFIGure:FREQuency:LIST:DATA?")
        class NFIGure_Bandwidth:
            """
            The NFIGure:Bandwidth commands control the bandwidth settings for noise figure measurements.
            """
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler

            def set_resolution(self, value):
                """
                Specify the resolution bandwidth (RBW). If UP or DOWN is specified, the RBW is stepped in a 1/3/10 sequence.

                :param value: RBW in Hz, or 'UP', or 'DOWN'.

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
                Query the current resolution bandwidth (RBW) in Hz.

                
                :return: The current RBW in Hz.
                """
                return float(self.instrument.query(":SENSe:NFIGure:BANDwidth:RESolution?"))

            def set_resolution_auto(self, state):
                """
                Automatically choose the RBW.

                :param state: 1/0 or 'ON'/'OFF' to enable/disable auto RBW.

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
                Query if automatic RBW selection is enabled.

                
                :return:  True if auto RBW is enabled, False otherwise.
                """
                resp = self.instrument.query(":SENSe:NFIGure:BANDwidth:RESolution:AUTO?")
                return int(resp.strip()) == 1

            def set_video(self, value):
                """
                Specify the video bandwidth (VBW). If UP or DOWN is specified, the VBW is stepped in a 1/3/10 sequence.

                :param value: VBW in Hz, or 'UP', or 'DOWN'.

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
                Query the current video bandwidth (VBW) in Hz.

                
                :return: The current VBW in Hz.
                """
                return float(self.instrument.query(":SENSe:NFIGure:BANDwidth:VIDeo?"))

            def set_video_auto(self, state):
                """
                Automatically choose the VBW.

                :param state: 1/0 or 'ON'/'OFF' to enable/disable auto VBW.

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
                Query if automatic VBW selection is enabled.

                
                :return:  True if auto VBW is enabled, False otherwise.
                """
                resp = self.instrument.query(":SENSe:NFIGure:BANDwidth:VIDeo:AUTO?")
                return int(resp.strip()) == 1

            def set_power_rf_rlevel(self, value):
                """
                Specify the reference level of the measurement in dBm.

                :param value: Reference level of the measurement in dBm.

                """
                self.instrument.write(f":SENSe:NFIGure:POWer:RF:RLEVel {value}")

            def get_power_rf_rlevel(self):
                """
                Query the reference level for the noise figure measurement.

                
                :return: The reference level of the measurement in dBm.
                """
                return float(self.instrument.query(":SENSe:NFIGure:POWer:RF:RLEVel?"))

            def set_meas_span(self, value):
                """
                Specify the span of each sweep.

                :param value: Span of each sweep in Hz.

                """
                self.instrument.write(f":SENSe:NFIGure:MEAS:SPAN {value}")

            def get_meas_span(self):
                """
                Query the span of each sweep.

                
                :return: The span of each sweep in Hz.
                """
                return float(self.instrument.query(":SENSe:NFIGure:MEAS:SPAN?"))

            def set_average_state(self, state):
                """
                Specify whether multiple sweeps are averaged together.

                :param state: 1/0 or 'ON'/'OFF' to enable/disable averaging.

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
                Query if averaging is enabled.

                
                :return: True if averaging is enabled, False otherwise.
                """
                resp = self.instrument.query(":SENSe:NFIGure:AVERage:STATe?")
                return int(resp.strip()) == 1

            def set_average_count(self, count):
                """
                Specify the number of sweeps that are averaged together.

                :param count: Number of sweeps to average together.

                """
                if not isinstance(count, int):
                    raise ValueError("count must be an integer")
                self.instrument.write(f":SENSe:NFIGure:AVERage:COUNt {count}")

            def get_average_count(self):
                """
                Query the number of sweeps that are averaged together.

                
                :return: The number of sweeps averaged together.
                """
                return int(self.instrument.query(":SENSe:NFIGure:AVERage:COUNt?"))

            def set_tcold_value(self, value):
                """
                Specify room temperature in Kelvin.

                :param value: Room temperature in Kelvin.

                """
                self.instrument.write(f":SENSe:NFIGure:CORRection:TCOLd:VALue {value}")

            def get_tcold_value(self):
                """
                Query room temperature in Kelvin.

                
                :return: Room temperature in Kelvin.
                """
                return float(self.instrument.query(":SENSe:NFIGure:CORRection:TCOLd:VALue?"))

            def set_alert_state(self, state):
                """
                Specify whether a series of beeps will play when a sweep has finished.

                :param state: 1/0 or 'ON'/'OFF' to enable/disable alert on sweep completion.

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
                Query whether an alert will play on sweep completion.

                
                :return: True if alert is enabled, False otherwise.
                """
                resp = self.instrument.query(":SENSe:NFIGure:ALERt:STATe?")
                return int(resp.strip()) == 1
            

        class NFIGure_Correction:
            """
            The NFIGure:Correction commands control ENR tables and calibration settings for noise figure measurements.
            """
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler
                self.enr_table = self.Corr_ENRTable(self.instrument, self.data_handler)
            class Corr_ENRTable:
                """
                The ENRTable commands manage ENR tables for noise sources.
                """
                def __init__(self, instrument,data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler

                def get_count(self):
                    """
                    Query the count of ENR tables, corresponding to noise sources.

                    
                    :return: The count of ENR tables.
                    """
                    return int(self.instrument.query(":SENSe:NFIGure:CORRection:ENR:TABLe:COUNt?"))

                def new(self):
                    """
                    Create a new ENR table.

                    

                    """
                    self.instrument.write(":SENSe:NFIGure:CORRection:ENR:TABLe:NEW")

                def load(self, table_id):
                    """
                    Load an ENR table by ID for programmatic access.

                    :param table_id: ENR table ID to load.

                    """
                    if not isinstance(table_id, int):
                        raise ValueError("table_id must be an integer")
                    self.instrument.write(f":SENSe:NFIGure:CORRection:ENR:TABLe:LOAD {table_id}")

                def get_current(self):
                    """
                    Query the ID of the currently loaded ENR table.

                    
                    :return: The ID of the currently loaded ENR table.
                    """
                    return self.instrument.query(":SENSe:NFIGure:CORRection:ENR:TABLe?")

                def set_title(self, title):
                    """
                    Set the title of the currently loaded ENR table.

                    :param title: Title of the ENR table.

                    """
                    self.instrument.write(f':SENSe:NFIGure:CORRection:ENR:TABLe:TITLe "{title}"')

                def get_title(self):
                    """
                    Query the title of the loaded ENR table.

                    
                    :return: The title of the loaded ENR table.
                    """
                    return self.instrument.query(":SENSe:NFIGure:CORRection:ENR:TABLe:TITLe?")

                def get_points_count(self):
                    """
                    Query the number of points in the loaded ENR table.

                    
                    :return: Number of points in the loaded ENR table.
                    """
                    return int(self.instrument.query(":SENSe:NFIGure:CORRection:ENR:TABLe:POINts?"))

                def set_data(self, points):
                    """
                    Set the (frequency, enr) points in the loaded ENR table.

                    :param points: List of (freq, enr) pairs.

                    """
                    if not isinstance(points, list) or not all(isinstance(p, tuple) and len(p) == 2 for p in points):
                        raise ValueError("points must be a list of (freq, enr) tuples")
                    data_str = ", ".join(f"{freq},{enr}" for freq, enr in points)
                    self.instrument.write(f":SENSe:NFIGure:CORRection:ENR:TABLe:DATA {data_str}")

                def get_data(self):
                    """
                    Get the list of points in the loaded ENR table.

                    
                    :return: The list of points in the loaded ENR table.
                    """
                    response = self.instrument.query(":SENSe:NFIGure:CORRection:ENR:TABLe:DATA?")
                    if self.data_handler.is_auto_saving_data_enabled():
                        self.data_handler.write_to_file(self, "CORR_ENR", response, file_type = EFileType.CSV, headers = None)
                    return response

                def set_calibration_table(self, table_id):
                    """
                    Specify which ENR table will be used for calibration.

                    :param table_id: ENR table ID to use for calibration.

                    """
                    if not isinstance(table_id, int):
                        raise ValueError("table_id must be an integer")
                    self.instrument.write(f":SENSe:NFIGure:CORRection:ENR:CALibration:TABLe {table_id}")
                    
                def get_calibration_table(self):
                    """
                    Query the calibration ENR table.

                    
                    :return: The calibration ENR table.
                    """
                    return self.instrument.query(":SENSe:NFIGure:CORRection:ENR:CALibration:TABLe?")

                def set_measurement_table(self, table_id):
                    """
                    Specify which ENR table will be used for measurement.

                    :param table_id: ENR table ID to use for measurement.

                    """
                    if not isinstance(table_id, int):
                        raise ValueError("table_id must be an integer")
                    self.instrument.write(f":SENSe:NFIGure:CORRection:ENR:MEASurement:TABLe {table_id}")

                def get_measurement_table(self):
                    """
                    Query the measurement ENR table.

                    
                    :return: The measurement ENR table.
                    """
                    return self.instrument.query(":SENSe:NFIGure:CORRection:ENR:MEASurement:TABLe?")

                
        class NFIGure_Fetch:
            """
            The Fetch commands retrieve noise figure and gain measurement results.
            """
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler

            def get_nfigure(self):
                """
                
                :return: List of noise figure measurements for each point in the frequency list.
                """
                response = self.instrument.query(":FETCh:NFIGure?")
                if self.data_handler.is_auto_saving_data_enabled():
                    self.data_handler.write_to_file(self, "NFIGURE_FETCH", response, file_type = EFileType.CSV, headers = None)
                return response

            def get_gain(self):
                """
                
                :return: List of gain measurements for each point in the frequency list.
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
            self.measurement = self.Measurement(self.instrument, self.data_handler)
            self.trigger = self.Trigger(self.instrument, self.data_handler)
        class Measurement:
            """
            The Measurement commands configure Bluetooth measurement mode.
            """
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler

            def set_meas(self, meas_type):
                """
                Specify the active Bluetooth measurement type.

                Select between demodulation and in-band emission (IBE) testing.

                :param meas_type: 'DEMOD' or 'IBE'
        
                """
                allowed = {"DEMOD", "IBE"}
                if not isinstance(meas_type, str) or meas_type.upper() not in allowed:
                    raise ValueError("meas_type must be 'DEMOD' or 'IBE'")
                self.instrument.write(f":SENSe:BLE:MEAS {meas_type.upper()}")

            def get_meas(self):
                """
                Query the active Bluetooth measurement type.

                Returns the current measurement type: demodulation or in-band emission (IBE).

                
                :return: The current Bluetooth measurement type.
                """
                return self.instrument.query(":SENSe:BLE:MEAS?")

            def set_center_frequency(self, freq):
                """
                Specify the center frequency of the demodulation measurements.

                :param freq: Center frequency in Hz.
        
                """
                self.instrument.write(f":SENSe:BLE:FREQuency:CENTer {freq}")

            def get_center_frequency(self):
                """
                Query the center frequency of the demodulation measurements.

                
                :return: The center frequency in Hz.
                """
                return float(self.instrument.query(":SENSe:BLE:FREQuency:CENTer?"))

            def set_center_step(self, freq):
                """
                Specify the center frequency step size for demodulation measurements.

                :param freq: Center frequency step size in Hz.
        
                """
                self.instrument.write(f":SENSe:BLE:FREQuency:CENTer:STEP {freq}")

            def get_center_step(self):
                """
                Query the center frequency step size for demodulation measurements.

                
                :return: The center frequency step size in Hz.
                """
                return float(self.instrument.query(":SENSe:BLE:FREQuency:CENTer:STEP?"))

            def set_ifbw(self, freq):
                """
                Specify the measurement bandwidth for demodulation measurements.

                :param freq: Measurement bandwidth for demodulation in Hz.
        
                """
                self.instrument.write(f":SENSe:BLE:IFBW {freq}")

            def get_ifbw(self):
                """
                Query the measurement bandwidth for demodulation measurements.

                
                :return: The measurement bandwidth for demodulation in Hz.
                """
                return float(self.instrument.query(":SENSe:BLE:IFBW?"))

            def set_channel_index(self, index):
                """
                Specify the channel index for Bluetooth measurements.

                When auto channel index is disabled, this value seeds the PDU dewhitening.

                :param index: Channel index.
        
                """
                if not isinstance(index, int):
                    raise ValueError("index must be an integer")
                self.instrument.write(f":SENSe:BLE:CHANnel:INDex {index}")

            def get_channel_index(self):
                """
                Query the channel index used for Bluetooth measurements.

                
                :return: The channel index.
                """
                return int(self.instrument.query(":SENSe:BLE:CHANnel:INDex?"))

            def set_channel_auto(self, state):
                """
                Enable or disable automatic channel index selection.

                When enabled, the channel index is inferred from the center frequency.

                :param state: 1/0 or 'ON'/'OFF' to enable/disable auto channel index.
        
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
                Query if automatic channel index selection is enabled.

                Returns True if channel index is inferred from the center frequency.

                
                :return:  True if auto channel index is enabled, False otherwise.
                """
                resp = self.instrument.query(":SENSe:BLE:CHANnel:AUTO?")
                return int(resp.strip()) == 1

            def set_reference_level(self, value):
                """
                Specify the reference level of the Bluetooth measurement in dBm.

                :param value: Reference level in dBm.
        
                """
                self.instrument.write(f":SENSe:BLE:POWer:RF:RLEVel {value}")

            def get_reference_level(self):
                """
                Query the reference level of the Bluetooth measurement in dBm.

                
                :return: The reference level in dBm.
                """
                return float(self.instrument.query(":SENSe:BLE:POWer:RF:RLEVel?"))

        class Trigger:
            """
            The Trigger commands control the Bluetooth Low Energy trigger settings.
            """
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler
                self.fetch = self.Fetch(self.instrument,data_handler)
            def set_slength(self, value):
                """
                :param value: Measurement capture length in seconds.
        
                """
                self.instrument.write(f":TRIGger:BLE:SLENgth {value}")

            def get_slength(self):
                """
                
                :return: The measurement capture length in seconds.
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
                    :param metrics: Metric(s) to retrieve.
                    :return: Comma separated list of metric values in order requested.
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
            self.measurement = self.Measurement(self.instrument, self.data_handler)
            self.scan = self.Scan(self.instrument, self.data_handler)
            self.fetch = self.Fetch(self.instrument, self.data_handler)
            self.trigger = self.Trigger(self.instrument, self.data_handler)
        class Measurement:
            """
            The Measurement commands configure LTE measurement mode.
            """
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler

            def set_standard(self, standard):
                """
                Select the LTE standard.

                :param standard: 'FDD', 'TDD', or 'NB'
        
                """
                allowed = {"FDD", "TDD", "NB"}
                if not isinstance(standard, str) or standard.upper() not in allowed:
                    raise ValueError("standard must be one of 'FDD', 'TDD', or 'NB'")
                self.instrument.write(f":SENSe:LTE:STANdard {standard.upper()}")

            def get_standard(self):
                """
                Query the current LTE standard.

                
                :return: The current LTE standard.
                """
                return self.instrument.query(":SENSe:LTE:STANdard?")

            def set_bandwidth(self, bw):
                """
                Set the LTE bandwidth in MHz.

                :param bw: '1.4', '3', '5', '10', '15', or '20' (MHz as string)
        
                """
                allowed = {"1.4", "3", "5", "10", "15", "20"}
                if not isinstance(bw, str) or bw not in allowed:
                    raise ValueError("bw must be one of '1.4', '3', '5', '10', '15', or '20'")
                self.instrument.write(f":SENSe:LTE:BANDwidth {bw}")

            def get_bandwidth(self):
                """
                Query the current LTE bandwidth in MHz.

                
                :return: The current LTE bandwidth in MHz.
                """
                return self.instrument.query(":SENSe:LTE:BANDwidth?")

            def set_center_frequency(self, freq):
                """
                Set the center frequency of the single frequency LTE measurement.

                :param freq: Center frequency in Hz.
        
                """
                self.instrument.write(f":SENSe:LTE:FREQuency:CENTer {freq}")

            def get_center_frequency(self):
                """
                Query the center frequency of the single frequency LTE measurement.

                
                :return: Center frequency in Hz.
                """
                return float(self.instrument.query(":SENSe:LTE:FREQuency:CENTer?"))

            def set_reference_level(self, value):
                """
                Set the reference level (in dBm) for the single frequency LTE measurement.

                :param value: Reference level in dBm.
        
                """
                self.instrument.write(f":SENSe:LTE:POWer:RF:RLEVel {value}")

            def get_reference_level(self):
                """
                Query the reference level (in dBm) for the single frequency LTE measurement.

                
                :return: Reference level in dBm.
                """
                return float(self.instrument.query(":SENSe:LTE:POWer:RF:RLEVel?"))
            
            def set_include(self, state):
                """
                When enabled, single frequency measurements are included in the cell search results.

                :param state: 1/0 or 'ON'/'OFF' to include single frequency measurements in cell search results.
        
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
                Query if single frequency measurements are included in the cell search results.

                
                :return:  True if single frequency measurements are included in cell search results, False otherwise.
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
                Set whether the configured scan occurs once or continuously per “start scan”.

                :param scan_type: 'SINGLE' or 'CONTINUOUS'
        
                """
                allowed = {"SINGLE", "CONTINUOUS"}
                if not isinstance(scan_type, str) or scan_type.upper() not in allowed:
                    raise ValueError("scan_type must be 'SINGLE' or 'CONTINUOUS'")
                self.instrument.write(f":SENSe:LTE:SCAN:TYPE {scan_type.upper()}")

            def get_type(self):
                """
                Query whether the configured scan occurs once or continuously per “start scan”.

                
                :return: The current scan type.
                """
                return self.instrument.query(":SENSe:LTE:SCAN:TYPE?")

            def set_results_sort(self, sort):
                """
                Determines how the cell search result entries are sorted.

                :param sort: 'RSSI', 'FREQUENCY', or 'TIME'
        
                """
                allowed = {"RSSI", "FREQUENCY", "TIME"}
                if not isinstance(sort, str) or sort.upper() not in allowed:
                    raise ValueError("sort must be 'RSSI', 'FREQUENCY', or 'TIME'")
                self.instrument.write(f":SENSe:LTE:SCAN:RESults:SORT {sort.upper()}")

            def get_results_sort(self):
                """
                Query how the cell search result entries are sorted.

                
                :return: The current sort order for scan results.
                """
                return self.instrument.query(":SENSe:LTE:SCAN:RESults:SORT?")

            def set_results_keep(self, keep):
                """
                When cell search results are grouped, determines which measurement is displayed for that given grouping.

                :param keep: 'LAST' or 'PEAK'
        
                """
                allowed = {"LAST", "PEAK"}
                if not isinstance(keep, str) or keep.upper() not in allowed:
                    raise ValueError("keep must be 'LAST' or 'PEAK'")
                self.instrument.write(f":SENSe:LTE:SCAN:RESults:KEEP {keep.upper()}")

            def get_results_keep(self):
                """
                Query which measurement is displayed for a given grouping when cell search results are grouped.

                
                :return: The current keep setting for grouped scan results.
                """
                return self.instrument.query(":SENSe:LTE:SCAN:RESults:KEEP?")

            def set_results_group(self, state):
                """
                Enables or disables cell search result grouping.

                :param state: 1/0 or 'ON'/'OFF' to enable/disable grouping of scan results.
        
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
                Query if grouping of scan results is enabled.

                
                :return:  True if grouping of scan results is enabled, False otherwise.
                """
                resp = self.instrument.query(":SENSe:LTE:SCAN:RESults:GROUP?")
                return int(resp.strip()) == 1

            def set_results_max(self, value):
                """
                Determines the maximum number of entries visible in the cell search results window.

                :param value: Maximum number of entries in scan results.
        
                """
                if not isinstance(value, int):
                    raise ValueError("value must be an integer")
                self.instrument.write(f":SENSe:LTE:SCAN:RESults:MAX {value}")

            def get_results_max(self):
                """
                Query the maximum number of entries visible in the cell search results window.

                
                :return: Maximum number of entries in scan results.
                """
                return int(self.instrument.query(":SENSe:LTE:SCAN:RESults:MAX?"))

            def start(self):
                """
                Starts the scan, returns 1 once the scan has been started.

                
                :return: 1 if scan started.
                """
                return int(self.instrument.query(":SENSe:LTE:SCAN:STARt?"))

            def is_active(self):
                """
                Returns 1 if the scan is active.

                
                :return:  True if scan is active, False otherwise.
                """
                resp = self.instrument.query(":SENSe:LTE:SCAN:ACTive?")
                return int(resp.strip()) == 1

            def stop(self):
                """
                Stops the scan. Returns 1 when complete.

                
                :return: 1 when scan is stopped.
                """
                return int(self.instrument.query(":SENSe:LTE:SCAN:STOP?"))

            def get_results_count(self):
                """
            Returns the number of rows in the cell scan results table.

                
                :return: Number of rows in the cell scan results table.
                """
                return int(self.instrument.query(":SENSe:LTE:SCAN:RESults:COUNt?"))

            def set_results_index(self, index):
                """
            Set the index into the cell scan results table to be used with the FETCH command.

                :param index: Index into the cell scan results table.
        
                """
                if not isinstance(index, int):
                    raise ValueError("index must be an integer")
                self.instrument.write(f":SENSe:LTE:SCAN:RESults:INDEX {index}")

            def get_results_index(self):
                """
            Query the current index into the cell scan results table.

                
                :return: The current index into the cell scan results table.
                """
                return int(self.instrument.query(":SENSe:LTE:SCAN:RESults:INDEX?"))

            def clear_results(self):
                """
            Clears the cell search results table.

                
        
                """
                self.instrument.write(":SENSe:LTE:SCAN:RESults:CLEar")

        class Trigger:
            """
            The Trigger commands control the LTE trigger settings.
            """
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler

            def set_slength(self, value):
                """
                :param value: Measurement capture length in seconds.
                
                """
                self.instrument.write(f":TRIGger:LTE:SLENgth {value}")

            def get_slength(self):
                """
                
                :return: Measurement capture length in seconds.
                """
                return float(self.instrument.query(":TRIGger:LTE:SLENgth?"))

            def set_if_level(self, value):
                """
                :param value: Trigger level in dBm.
                
                """
                self.instrument.write(f":TRIGger:LTE:IF:LEVel {value}")

            def get_if_level(self):
                """
                
                :return: Trigger level in dBm.
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
                :param metrics: Metric(s) to retrieve.
                :return: Comma separated list of metric values in order requested.
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
        self.measurement = self.Measurement(self.instrument, self.data_handler)
        self.trigger = self.Trigger(self.instrument, self.data_handler)
        self.fetch = self.Fetch(self.instrument, self.data_handler)
            
    class Measurement:
        """
        The Measurement commands configure WLAN measurement mode.
        """
        def __init__(self, instrument,data_handler):
            self.instrument = instrument
            self.data_handler = data_handler

        def set_standard(self, standard):
            """
            Select the WLAN modulation standard.

            :param standard: 'BG', 'AG', 'N20', 'N40', 'AC20', 'AC40', or 'AH'
    
            """
            allowed = {"BG", "AG", "N20", "N40", "AC20", "AC40", "AH"}
            if not isinstance(standard, str) or standard.upper() not in allowed:
                raise ValueError("standard must be one of 'BG', 'AG', 'N20', 'N40', 'AC20', 'AC40', or 'AH'")
            self.instrument.write(f":SENSe:WLAN:STANdard {standard.upper()}")

        def get_standard(self):
            """
            Query the WLAN modulation standard.

            
            :return: The current WLAN modulation standard.
            """
            return self.instrument.query(":SENSe:WLAN:STANdard?")

        def set_dsss_symbols(self, num):
            """
            Specify how many DSSS symbols to demodulate/decode.

            :param num: Number of DSSS symbols to demodulate/decode.
    
            """
            if not isinstance(num, int):
                raise ValueError("num must be an integer")
            self.instrument.write(f":SENSe:WLAN:SYMbols:DSSS {num}")

        def get_dsss_symbols(self):
            """
            Query how many DSSS symbols to demodulate/decode.

            
            :return: Number of DSSS symbols to demodulate/decode.
            """
            return int(self.instrument.query(":SENSe:WLAN:SYMbols:DSSS?"))

        def set_psdu_decode(self, state):
            """
            Enable OFDM PSDU decoding for BCC encoded waveforms.

            :param state: 1/0 or 'ON'/'OFF' to enable/disable OFDM PSDU decoding.
    
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
            Query if OFDM PSDU decoding is enabled.

            
            :return:  True if OFDM PSDU decoding is enabled, False otherwise.
            """
            resp = self.instrument.query(":SENSe:WLAN:PSDU:DECode?")
            return int(resp.strip()) == 1

        def set_symbol_offset(self, value):
            """
            Specify a GI timing offset between -100 and 0 (%).

            :param value: GI timing offset between -100 and 0 (%)
    
            """
            self.instrument.write(f":SENSe:WLAN:SYMBol:OFFSet {value}")

        def get_symbol_offset(self):
            """
            Query the GI timing offset.

            
            :return: GI timing offset between -100 and 0 (%)
            """
            return float(self.instrument.query(":SENSe:WLAN:SYMBol:OFFSet?"))

        def set_center_frequency(self, freq):
            """
            Specify the center frequency of the WLAN measurement.

            :param freq: Center frequency in Hz.
    
            """
            self.instrument.write(f":SENSe:WLAN:FREQuency:CENTer {freq}")

        def get_center_frequency(self):
            """
            Query the center frequency of the WLAN measurement.

            
            :return: Center frequency in Hz.
            """
            return float(self.instrument.query(":SENSe:WLAN:FREQuency:CENTer?"))

        def set_center_step(self, freq):
            """
            Specify the center frequency step size.

            :param freq: Center frequency step size in Hz.
    
            """
            self.instrument.write(f":SENSe:WLAN:FREQuency:CENTer:STEP {freq}")

        def get_center_step(self):
            """
            Query the center frequency step size.

            
            :return: Center frequency step size in Hz.
            """
            return float(self.instrument.query(":SENSe:WLAN:FREQuency:CENTer:STEP?"))

        def set_ifbw(self, freq):
            """
            Specify the IF bandwidth of the measurement. This is applied as a low pass filter before the WLAN demodulation occurs.

            :param freq: IF bandwidth in Hz.
    
            """
            self.instrument.write(f":SENSe:WLAN:IFBW {freq}")

        def get_ifbw(self):
            """
            Query the IF bandwidth of the measurement.

            
            :return: IF bandwidth in Hz.
            """
            return float(self.instrument.query(":SENSe:WLAN:IFBW?"))

        def set_reference_level(self, value):
            """
            Specify the reference level of the measurement in dBm. This controls the sensitivity of the measurement.

            :param value: Reference level in dBm.
    
            """
            self.instrument.write(f":SENSe:WLAN:POWer:RF:RLEVel {value}")

        def get_reference_level(self):
            """
            Query the reference level of the measurement in dBm.

            
            :return: Reference level in dBm.
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
        Specify the measurement capture length.

            :param value: Measurement capture length in seconds.
    
            """
            self.instrument.write(f":TRIGger:WLAN:SLENgth {value}")

        def get_slength(self):
            """
        Query the measurement capture length.

            
            :return: Measurement capture length in seconds.
            """
            return float(self.instrument.query(":TRIGger:WLAN:SLENgth?"))

        def set_if_threshold(self, value):
            """
        Specify the OFDM trigger threshold in dB.

            :param value: OFDM trigger threshold in dB.
    
            """
            self.instrument.write(f":TRIGger:WLAN:IF:THRESHold {value}")

        def get_if_threshold(self):
            """
        Query the OFDM trigger threshold in dB.

            
            :return: OFDM trigger threshold in dB.
            """
            return float(self.instrument.query(":TRIGger:WLAN:IF:THRESHold?"))

        def set_if_level(self, value):
            """
        Specify the DSSS video trigger level in dBm.

            :param value: DSSS video trigger level in dBm.
    
            """
            self.instrument.write(f":TRIGger:WLAN:IF:LEVel {value}")

        def get_if_level(self):
            """
        Query the DSSS video trigger level in dBm.

            
            :return: DSSS video trigger level in dBm.
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
            """ Fetch WLAN demodulation metrics. The integer parameter specifies
            the metric to retrieve. Possible integer values can be printed with print_fetch_WLAN. Can specify a list of metrics
            to request as comma separated list. The metrics will be returned as a comma
            separated list in the order they were requested.

            :param metrics: Metric(s) to retrieve.
            :return: Comma separated list of metric values in order requested.
            """
            if isinstance(metrics, int):
                metrics_str = str(metrics)
            elif isinstance(metrics, (list, tuple)) and all(isinstance(m, int) for m in metrics):
                metrics_str = ",".join(str(m) for m in metrics)
            else:
                raise ValueError("metrics must be an int or list/tuple of ints")
            return self.instrument.query(f":FETCh:WLAN? {metrics_str}")
    def print_fetch_WLAN(self):
        """
        Print the list of available WLAN fetch metrics.
            
        
        """
        print("WLAN 802.11 a/n/ac/ah fetch metrics:")
        print("{:<3} {}".format("ID", "Description"))
        print("-" * 50)
        wlan_anacah_metrics = [
            (1, "Modulation as text"),
            (2, "Modulation encoding as text"),
            (3, "Guard interval as text"),
            (4, "Frequency error as Hz"),
            (5, "EVM as %"),
            (6, "EVM as dB"),
            (7, "Avg Power as dBm"),
            (8, "Peak Power as dBm"),
            (9, "Crest factor"),
            (10, "Initial scrambler state"),
            (11, "Symbol count"),
            (12, "Payload bit count"),
            (13, "Sample rate error as ppm"),
            (14, "Bandwidth as MHz (detected BW for WLAN-AH)"),
        ]
        for id, desc in wlan_anacah_metrics:
            print("{:<3} {}".format(id, desc))

        print("\nWLAN 802.11 b fetch metrics:")
        print("{:<3} {}".format("ID", "Description"))
        print("-" * 50)
        wlan_b_metrics = [
            (1, "Modulation as text"),
            (2, "Preamble as text"),
            (3, "Payload bit count"),
            (4, "EVM as %"),
            (5, "EVM as dB"),
            (6, "Freq error as Hz"),
            (7, "Avg power as dBm"),
            (8, "Peak power as dBm"),
            (9, "Crest factor"),
        ]
        for id, desc in wlan_b_metrics:
            print("{:<3} {}".format(id, desc))
class Trace:
    """
    The Trace commands control the user configurable traces for sweep mode.
    """
    def __init__(self, instrument,data_handler):
        self.instrument = instrument
        self.data_handler = data_handler
        self.pnoise = self.Trace_PNoise(self.instrument, self.data_handler)
    def select(self, trace_num):
        """
        Specify a trace index [1,6]. All future operations occur on this trace.

        :param trace_num: Trace index [1,6].

        """
        if not isinstance(trace_num, int) or not (1 <= trace_num <= 6):
            raise ValueError("trace_num must be an integer between 1 and 6")
        self.instrument.write(f":TRACe:SELect {trace_num}")

    def get_selected(self):
        """
        Retrieve the currently selected trace index.

        
        :return: The currently selected trace index.
        """
        return int(self.instrument.query(":TRACe:SELect?"))

    def set_type(self, typ):
        """
        Specify the behavior of the trace.

        :param typ: 'OFF', 'WRITE', 'AVERAGE', 'MAXHOLD', 'MINHOLD', or 'MINMAX'.

        """
        allowed = {"OFF", "WRITE", "AVERAGE", "MAXHOLD", "MINHOLD", "MINMAX"}
        if not isinstance(typ, str) or typ.upper() not in allowed:
            raise ValueError("typ must be one of 'OFF', 'WRITE', 'AVERAGE', 'MAXHOLD', 'MINHOLD', or 'MINMAX'")
        self.instrument.write(f":TRACe:TYPE {typ.upper()}")

    def get_type(self):
        """
        Retrieve the current trace type.

        
        :return: The current trace type.
        """
        return self.instrument.query(":TRACe:TYPE?")

    def set_average_count(self, count):
        """
        Specify the number of traces that are averaged together to create the final sweep.

        :param count: Number of traces to average together.

        """
        if not isinstance(count, int) or count < 1:
            raise ValueError("count must be a positive integer")
        self.instrument.write(f":TRACe:AVERage:COUNt {count}")

    def get_average_count(self):
        """
        Retrieve the number of traces averaged together.

        
        :return: The number of traces averaged together.
        """
        return int(self.instrument.query(":TRACe:AVERage:COUNt?"))

    def get_average_current(self):
        """
        Retrieve the current number of traces that have been averaged together to create the final sweep.

        
        :return: The current number of traces averaged together.
        """
        return int(self.instrument.query(":TRACe:AVERage:CURRent?"))

    def copy(self, dest_trace_num):
        """
        Copy the currently selected trace to the trace specified by the supplied parameter.
        The supplied parameter should be between [1,6] and not equal to the currently selected trace.
        If the destination trace type is off, the trace type is set to clear and write. Update is set to off and display is set to on for the destination trace.

        :param dest_trace_num: Destination trace index [1,6], not equal to current.

        """
        if not isinstance(dest_trace_num, int) or not (1 <= dest_trace_num <= 6):
            raise ValueError("dest_trace_num must be an integer between 1 and 6")
        self.instrument.write(f":TRACe:COPY {dest_trace_num}")

    def set_update_state(self, state):
        """
        Specify if the trace updates when a new sweep is acquired from the device.

        :param state: 1/0 or 'ON'/'OFF' to enable/disable trace update.

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
        Query if trace update is enabled.

        
        :return:  True if trace update is enabled, False otherwise.
        """
        resp = self.instrument.query(":TRACe:UPDate:STATe?")
        return int(resp.strip()) == 1

    def set_display_state(self, state):
        """
        Specify if the trace is hidden.

        :param state: 1/0 or 'ON'/'OFF' to show/hide the trace.

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
        Query if trace is displayed.

        
        :return:  True if trace is displayed, False otherwise.
        """
        resp = self.instrument.query(":TRACe:DISPlay:STATe?")
        return int(resp.strip()) == 1

    def clear(self):
        """
        Clear the selected trace. For example, if the current sweep is a max hold sweep and is cleared, the trace will be replaced with the next sweep from the device.

        

        """
        self.instrument.write(":TRACe:CLEar")

    def clear_all(self):
        """
        Clear all the traces.

        

        """
        self.instrument.write(":TRACe:CLEar:ALL")

    def get_xstart(self):
        """
        Retrieve the frequency of the first point in the sweep as Hz.
        Useful for calculating the frequency of each point in the trace data returned from the :TRACe:DATA? command.

        
        :return: Frequency of the first point in the sweep (Hz).
        """
        return float(self.instrument.query(":TRACe:XSTARt?"))

    def get_xincrement(self):
        """
        Retrieve the frequency step between two points in the trace data as Hz.
        Useful for calculating the frequency of each point in the trace data.

        
        :return: Frequency step between two points in the trace data (Hz).
        """
        return float(self.instrument.query(":TRACe:XINCrement?"))

    def get_points_count(self):
        """
        Returns the number of points in the trace data.

        
        :return: Number of points in the trace data.
        """
        return int(self.instrument.query(":TRACe:POINts?"))

    def get_data(self):
        """
        Returns the trace data.

        
        :return: The trace data as comma separated ascii floating point values.
        """
        response = self.instrument.query(":TRACe:DATA?")
        if self.data_handler.is_auto_saving_data_enabled():
            self.data_handler.write_to_file(self, "TRACE_DATA", response, file_type = EFileType.CSV, headers = None)
        return response
    class Trace_PNoise:
        """
        The PNoise commands control the user configurable traces for phase noise measurements.
        """
        def __init__(self, instrument,data_handler):
            self.instrument = instrument
            self.data_handler = data_handler

        def select(self, trace_num):
            """
            Specify the active trace index. All future operations will occur on this trace.

            :param trace_num: Trace index [1,6].

            """
            if not isinstance(trace_num, int) or not (1 <= trace_num <= 6):
                raise ValueError("trace_num must be an integer between 1 and 6")
            self.instrument.write(f":TRACe:PNoise:SELect {trace_num}")

        def get_selected(self):
            """
            Query the currently selected trace index.

            
            :return: The currently selected trace index.
            """
            return int(self.instrument.query(":TRACe:PNoise:SELect?"))

        def set_type(self, typ):
            """
            Specify the trace type. AVERage:COUNt sweeps and REFerence stops the trace from updating (effectively holding the current values).

            :param typ: 'OFF', 'NORMal', 'AVERage', 'REFerence', 'MINHold', or 'MAXHold'.

            """
            allowed = {"OFF", "NORMal", "AVERage", "REFerence", "MINHold", "MAXHold"}
            if not isinstance(typ, str) or typ.upper() not in allowed:
                raise ValueError("typ must be one of 'OFF', 'NORMal', 'AVERage', 'REFerence', 'MINHold', or 'MAXHold'")
            self.instrument.write(f":TRACe:PNoise:TYPE {typ.upper()}")

        def get_type(self):
            """
            Query the current trace type.

            
            :return: The current trace type.
            """
            return self.instrument.query(":TRACe:PNoise:TYPE?")

        def set_average_count(self, count):
            """
            Specify the number of sweeps that will be averaged together when trace is set to average type.

            :param count: Number of traces to average together.

            """
            if not isinstance(count, int) or count < 1:
                raise ValueError("count must be a positive integer")
            self.instrument.write(f":TRACe:PNoise:AVERage:COUNt {count}")

        def get_average_count(self):
            """
            Query the number of sweeps that will be averaged together.

            
            :return: The number of traces averaged together.
            """
            return int(self.instrument.query(":TRACe:PNoise:AVERage:COUNt?"))

        def set_update_state(self, state):
            """
            Specify if the trace updates when a new sweep is acquired from the device.

            :param state: 1/0 or 'ON'/'OFF' to enable/disable trace update.

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
            Query if trace update is enabled.

            
            :return:  True if trace update is enabled, False otherwise.
            """
            resp = self.instrument.query(":TRACe:PNoise:UPDate:STATe?")
            return int(resp.strip()) == 1

        def set_hide_state(self, state):
            """
            Hide or show the trace.

            :param state: 1/0 or 'ON'/'OFF' to show/hide the trace.

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
            Query if trace is hidden.

            
            :return:  True if trace is hidden, False otherwise.
            """
            resp = self.instrument.query(":TRACe:PNoise:HIDE:STATe?")
            return int(resp.strip()) == 1
        
        def set_smoothing_state(self, state):
            """
            Enable or disable smoothing.

            :param state: 1/0 or 'ON'/'OFF' to enable/disable trace smoothing.

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
            Query if smoothing is enabled.

            
            :return:  True if trace smoothing is enabled, False otherwise.
            """
            resp = self.instrument.query(":TRACe:PNoise:SMOothing:STATe?")
            return int(resp.strip()) == 1

        def set_smoothing_aperture(self, aperture):
            """
            Specify the trace smoothing aperture as a percentage.

            :param aperture: Smoothing aperture value.

            """
            self.instrument.write(f":TRACe:PNoise:SMOothing:APERture {aperture}")

        def get_smoothing_aperture(self):
            """
            Query the trace smoothing aperture as a percentage.

            
            :return: The smoothing aperture value.
            """
            return float(self.instrument.query(":TRACe:PNoise:SMOothing:APERture?"))

        def set_spur_reject_state(self, state):
            """
            Enable or disable trace spur rejection.

            :param state: 1/0 or 'ON'/'OFF' to enable/disable spur reject.

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
            Query if trace spur rejection is enabled.

            
            :return:  True if spur reject is enabled, False otherwise.
            """
            resp = self.instrument.query(":TRACe:PNoise:SPURReject:STATe?")
            return int(resp.strip()) == 1

        def set_spur_reject_threshold(self, value):
            """
            Specify the spur reject threshold in dB.

            :param value: Spur reject threshold in dB.

            """
            self.instrument.write(f":TRACe:PNoise:SPURReject:THRESHold {value}")

        def get_spur_reject_threshold(self):
            """
            Query the current spur reject threshold in dB.

            
            :return: The current spur reject threshold in dB.
            """
            return float(self.instrument.query(":TRACe:PNoise:SPURReject:THRESHold?"))

        def set_offset(self, value):
            """
            Specify an offset in dB. Immediately applies to the trace.

            :param value: Offset in dB to immediately apply to the trace.

            """
            self.instrument.write(f":TRACe:PNoise:OFFSet {value}")

        def get_offset(self):
            """
            Query the current offset in dB applied to the trace.

            
            :return: The current offset in dB applied to the trace.
            """
            return float(self.instrument.query(":TRACe:PNoise:OFFSet?"))

        def to(self, trace_num):
            """
            Move the current trace to the selected trace. The selected trace type will be set to reference.

            :param trace_num: Trace index [1,6] to move the current trace to.

            """
            if not isinstance(trace_num, int) or not (1 <= trace_num <= 6):
                raise ValueError("trace_num must be an integer between 1 and 6")
            self.instrument.write(f":TRACe:PNoise:TO {trace_num}")

        def clear(self):
            """
            Clear the current average accumulation.

            

            """
            self.instrument.write(":TRACe:PNoise:CLEar")

        def get_data_y(self):
            """
            Returns the trace data amplitudes. The number of values returned is the number of decades in the sweep times 100.

            
            :return: The trace data amplitudes as comma separated values.
            """
            response = self.instrument.query(":TRACe:PNoise:DATA:Y?")
            if self.data_handler.is_auto_saving_data_enabled():
                self.data_handler.write_to_file(self, "PNOISE_Y", response, file_type = EFileType.CSV, headers = None)
            return response

        def get_data_x(self):
            """
            Returns the trace data frequencies. The number of values returned is the number of decades in the sweep times 100.

            
            :return: The trace data frequencies as comma separated values.
            """
            response = self.instrument.query(":TRACe:PNoise:DATA:X?")
            if self.data_handler.is_auto_saving_data_enabled():
                self.data_handler.write_to_file(self, "PNOISE_X", response, file_type = EFileType.CSV, headers = None)
            return response

    
class Record:
    """
    The Record commands control the Sweep Recording control panel in Swept Analysis mode.
    """
    def __init__(self, instrument,data_handler):
        self.instrument = instrument
        self.data_handler = data_handler
        self.sweep = self.Record_Sweep(self.instrument, self.data_handler)
        self.trigger = self.Record_Trigger(self.instrument, self.data_handler)
    class Record_Sweep:
        def __init__(self, instrument, data_handler):
            self.instrument = instrument
            self.data_handler = data_handler
            self.decimate = self.Record_Sweep_Decimate(self.instrument, self.data_handler)
            self.channelizer = self.Record_Sweep_Channelizer(self.instrument, self.data_handler)
            self.zero_span = self.Record_Sweep_ZeroSpan(self.instrument, self.data_handler)
        def get_progress(self):
            """
            Returns the progress of the current decimation in time as a floating
            point percentage between 0 and 100.

            
            :return: The progress of the current decimation in percent.
            """
            return float(self.instrument.query(":RECord:SWEep:PROGress?"))

        def get_count(self):
            """
            Returns the integer number of sweeps saved so far.

            
            :return: The number of sweeps saved so far.
            """
            return int(self.instrument.query(":RECord:SWEep:COUNt?"))

        def get_file_size(self):
            """
            Returns the size of the file in bytes as a floating point number.

            
            :return: The size of the file in bytes.
            """
            return float(self.instrument.query(":RECord:SWEep:FILE:SIZE?"))

        def set_file_prefix(self, prefix):
            """
            Specifies the file prefix.

            :param prefix: File prefix.

            """
            self.instrument.write(f':RECord:SWEep:FILE:PREfix "{prefix}"')

        def get_file_prefix(self):
            """
            Queries the file prefix.

            
            :return: The file prefix.
            """
            return self.instrument.query(":RECord:SWEep:FILE:PREfix?")

        def set_directory(self, directory):
            """
            Specifies the directory in which to save recordings. If the
            specified directory does not exist, then no change is made.

            :param directory: Directory path.

            """
            self.instrument.write(f':RECord:SWEep:FILE:DIRectory "{directory}"')

        def get_directory(self):
            """
            Queries the directory in which recordings are saved.

            
            :return: The directory path.
            """
            return self.instrument.query(":RECord:SWEep:FILE:DIRectory?")

        def start(self):
            """
            Start recording.

            

            """
            self.instrument.write(":RECord:SWEep:STARt")

        def stop(self):
            """
            Stop recording.

            

            """
            self.instrument.write(":RECord:SWEep:STOP")

        def is_recording(self):
            """
            Returns true if actively recording.

            
            :return:  True if actively recording, False otherwise.
            """
            resp = self.instrument.query(":RECord:SWEep:STATus?")
            return int(resp.strip()) == 1

        class Record_Sweep_Decimate:
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler

            def set_type(self, typ):
                """
                Selects the decimation type.

                :param typ: 'TIME' or 'COUNT'.

                """
                allowed = {"TIME", "COUNT"}
                if not isinstance(typ, str) or typ.upper() not in allowed:
                    raise ValueError("typ must be 'TIME' or 'COUNT'")
                self.instrument.write(f":RECord:SWEep:DECimate:TYPE {typ.upper()}")

            def get_type(self):
                """
                Queries the current decimation type.

                
                :return: The current decimation type.
                """
                return self.instrument.query(":RECord:SWEep:DECimate:TYPE?")

            def set_time(self, value):
                """
                Specifies the amount of time by which to decimate.

                :param value: Decimation time.

                """
                self.instrument.write(f":RECord:SWEep:DECimate:TIME {value}")

            def get_time(self):
                """
                Queries the decimation time.

                
                :return: The decimation time.
                """
                return float(self.instrument.query(":RECord:SWEep:DECimate:TIME?"))

            def set_count(self, value):
                """
                Specifies the number of sweeps by which to decimate.

                :param value: Number of sweeps by which to decimate.

                """
                if not isinstance(value, int):
                    raise ValueError("value must be an integer")
                self.instrument.write(f":RECord:SWEep:DECimate:COUNt {value}")

            def get_count(self):
                """
                Queries the decimation count.

                
                :return: The decimation count.
                """
                return int(self.instrument.query(":RECord:SWEep:DECimate:COUNt?"))

            def set_detector(self, det):
                """
                Selects the decimation detector.

                :param det: 'AVERAGE' or 'MAX'.

                """
                allowed = {"AVERAGE", "MAX"}
                if not isinstance(det, str) or det.upper() not in allowed:
                    raise ValueError("det must be 'AVERAGE' or 'MAX'")
                self.instrument.write(f":RECord:SWEep:DECimate:DETector {det.upper()}")

            def get_detector(self):
                """
                Queries the decimation detector.

                
                :return: The decimation detector.
                """
                return self.instrument.query(":RECord:SWEep:DECimate:DETector?")

        class Record_Sweep_Channelizer:
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler

            def set_state(self, state):
                """
                Toggles decimation in frequency with the channelizer.

                :param state: 1/0 or 'ON'/'OFF' to enable/disable channelizer.

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
                Query if channelizer decimation is enabled.

                
                :return:  True if channelizer is enabled, False otherwise.
                """
                resp = self.instrument.query(":RECord:SWEep:CHANnelizer:STATe?")
                return int(resp.strip()) == 1

            def set_center(self, freq):
                """
                Specifies the center frequency of the channel.

                :param freq: Center frequency (Hz).

                """
                self.instrument.write(f":RECord:SWEep:CHANnelizer:CENTer {freq}")

            def get_center(self):
                """
                Query the center frequency of the channel.

                
                :return: The center frequency (Hz).
                """
                return float(self.instrument.query(":RECord:SWEep:CHANnelizer:CENTer?"))

            def set_spacing(self, freq):
                """
                Specifies the channel width.

                :param freq: Channel spacing (Hz).

                """
                self.instrument.write(f":RECord:SWEep:CHANnelizer:SPACing {freq}")

            def get_spacing(self):
                """
                Query the channel width.

                
                :return: The channel spacing (Hz).
                """
                return float(self.instrument.query(":RECord:SWEep:CHANnelizer:SPACing?"))

            def set_units(self, units):
                """
                Selects the output units of the channel power measurement.

                :param units: 'DBM' or 'DBMHZ'.

                """
                allowed = {"DBM", "DBMHZ"}
                if not isinstance(units, str) or units.upper() not in allowed:
                    raise ValueError("units must be 'DBM' or 'DBMHZ'")
                self.instrument.write(f":RECord:SWEep:CHANnelizer:UNITs {units.upper()}")

            def get_units(self):
                """
                Query the output units of the channel power measurement.

                
                :return: The output units.
                """
                return self.instrument.query(":RECord:SWEep:CHANnelizer:UNITs?")
        class Record_Sweep_ZeroSpan:
            """
            The ZeroSpan commands control the receiver configuration in zero-span mode.
            """
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler
                self.capture = self.Capture(self.instrument, self.data_handler)
            class Capture:
                def __init__(self, instrument,data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler

                def set_rlevel(self, amplitude):
                    """
                    Set the reference level for the capture.

                    :param amplitude: Reference level in dBm.

                    """
                    self.instrument.write(f":SENSe:ZS:CAPture:RLEVel {amplitude}")

                def get_rlevel(self):
                    """
                    Query the current reference level for the capture.

                    
                    :return: The current reference level as dBm.
                    """
                    return float(self.instrument.query(":SENSe:ZS:CAPture:RLEVel?"))

                def set_center(self, freq):
                    """
                    Set the measurement center frequency for the capture.

                    :param freq: Center frequency in Hz, or 'UP', or 'DOWN'.

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
                    Query the current center frequency for the capture.
                    Returned as Hz. By passing the MIN or MAX arguments, the user can query the upper and lower frequency limits for a capture.

                    :param bound: 'MIN' or 'MAX' to query frequency limits, or None for current center.
                    :return: The center frequency in Hz, or the min/max limit.
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
                    Set the step amount the center frequency changes by when using the UP or DOWN parameters on the CENTer command.

                    :param freq: Step amount for center frequency changes in Hz.
                    
                    """
                    self.instrument.write(f":SENSe:ZS:CAPture:CENTer:STEP {freq}")

                def get_center_step(self):
                    """
                    Query the center frequency step size in Hz.

                    
                    :return: The center frequency step size in Hz.
                    """
                    return float(self.instrument.query(":SENSe:ZS:CAPture:CENTer:STEP?"))

                def set_srate(self, freq):
                    """
                    Specify the sample rate of the capture. This determines how much decimation will be applied to the full signal.

                    :param freq: Sample rate in Hz.

                    """
                    self.instrument.write(f":SENSe:ZS:CAPture:SRATe {freq}")

                def get_srate(self):
                    """
                    Query the sample rate of the capture.

                    
                    :return: The sample rate in Hz.
                    """
                    return float(self.instrument.query(":SENSe:ZS:CAPture:SRATe?"))

                def set_ifbwidth(self, freq):
                    """
                    Specify the IF bandwidth for the capture. Only active when AUTO is set to false.

                    :param freq: IF bandwidth in Hz.

                    """
                    self.instrument.write(f":SENSe:ZS:CAPture:IFBWidth {freq}")

                def get_ifbwidth(self):
                    """
                    Query the IF bandwidth for the capture.

                    
                    :return: The IF bandwidth in Hz.
                    """
                    return float(self.instrument.query(":SENSe:ZS:CAPture:IFBWidth?"))

                def set_ifbwidth_auto(self, state):
                    """
                    Enable or disable automatic IF bandwidth selection for the capture.
                    When enabled, the Spike software will automatically choose an appropriate IF bandwidth for the measurement.

                    :param state: 1/0 or 'ON'/'OFF' to enable/disable auto IF bandwidth.

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
                    Query if automatic IF bandwidth selection is enabled for the capture.

                    
                    :return:  True if auto IF bandwidth is enabled, False otherwise.
                    """
                    resp = self.instrument.query(":SENSe:ZS:CAPture:IFBWidth:AUTO?")
                    return int(resp.strip()) == 1

                def set_sweep_time(self, value):
                    """
                    Set the overall acquisition length of the capture in seconds.

                    :param value: Sweep time in seconds.

                    """
                    self.instrument.write(f":SENSe:ZS:CAPture:SWEep:TIME {value}")

                def get_sweep_time(self):
                    """
                    Query the overall acquisition length of the capture in seconds.

                    
                    :return: The sweep time in seconds.
                    """
                    return float(self.instrument.query(":SENSe:ZS:CAPture:SWEep:TIME?"))

    class Record_Trigger:
        def __init__(self, instrument,data_handler):
            self.instrument = instrument
            self.data_handler = data_handler
            self.zerospan = self.ZS(self.instrument, self.data_handler)
        class ZS:
            """The ZS commands control the trigger configuration in zero-span mode."""
            def __init__(self, instrument,data_handler):
                self.instrument = instrument
                self.data_handler = data_handler
                self.fetch = self.ZS_Fetch(self.instrument, self.data_handler)
            def set_source(self, source):
                """
                Specify the trigger type.

                :param source: 'IMMEDIATE', 'IF', 'EXTERNAL', or 'FMT'.

                """
                allowed = {"IMMEDIATE", "IF", "EXTERNAL", "FMT"}
                if not isinstance(source, str) or source.upper() not in allowed:
                    raise ValueError("source must be one of 'IMMEDIATE', 'IF', 'EXTERNAL', or 'FMT'")
                self.instrument.write(f":TRIGger:ZS:SOURce {source.upper()}")

            def get_source(self):
                """
                Query the trigger type.

                
                :return: The trigger type.
                """
                return self.instrument.query(":TRIGger:ZS:SOURce?")

            def set_slope(self, slope):
                """
                Specify rising edge (positive) or falling edge.

                :param slope: 'POSITIVE' or 'NEGATIVE'.

                """
                allowed = {"POSITIVE", "NEGATIVE"}
                if not isinstance(slope, str) or slope.upper() not in allowed:
                    raise ValueError("slope must be 'POSITIVE' or 'NEGATIVE'")
                self.instrument.write(f":TRIGger:ZS:SLOPe {slope.upper()}")

            def get_slope(self):
                """
                Query the trigger edge.

                
                :return: The trigger edge.
                """
                return self.instrument.query(":TRIGger:ZS:SLOPe?")

            def set_if_level(self, amplitude):
                """
                Specify the trigger level of the IF trigger.

                :param amplitude: Trigger level of the IF trigger.

                """
                self.instrument.write(f":TRIGger:ZS:IF:LEVel {amplitude}")

            def get_if_level(self):
                """
                Query the trigger level of the IF trigger.

                
                :return: The trigger level of the IF trigger.
                """
                return float(self.instrument.query(":TRIGger:ZS:IF:LEVel?"))

            def set_position(self, value):
                """
                Specify the trigger delay of the IF or ext trigger, the percentage of
                samples of the capture displayed before the trigger.

                :param value: Trigger delay as percent of samples before trigger.

                """
                self.instrument.write(f":TRIGger:ZS:POSition {value}")

            def get_position(self):
                """
                Query the trigger delay as percent of samples before trigger.

                
                :return: The trigger delay as percent of samples before trigger.
                """
                return float(self.instrument.query(":TRIGger:ZS:POSition?"))

            class ZS_Fetch:
                """
                The Fetch commands are used to retrieve measurement results in zero-span mode.
                """
                def __init__(self, instrument,data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler

                def get_zs(self, param):
                    """  Fetch I/Q data and other measurement parameters. The integer parameter
                    specifies which to retrieve.
                    1. I/Q data in ASCII or binary format (see “I/Q Data” section above)
                    2. Length of I/Q data. This is the number of complex I/Q data points (eg. (I1, Q1) is a
                    single point).
                    10. Average power as reported on the AM vs Time plot. Returned as dBm.

                    :param param: 1 for I/Q data, 2 for length, 10 for average power.
                    :return: I/Q data (str), length (int), or average power (float).
                    """
                    if param == 1:
                        return self.instrument.query(":FETCh:ZS? 1")
                    elif param == 2:
                        return int(self.instrument.query(":FETCh:ZS? 2"))
                    elif param == 10:
                        return float(self.instrument.query(":FETCh:ZS? 10"))
                    else:
                        raise ValueError("param must be 1 (I/Q data), 2 (length), or 10 (average power)")
                                        
                                    