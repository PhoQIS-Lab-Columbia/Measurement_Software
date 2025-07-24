from Instruments import Instrument
import time
from EInstrument import EInstrument
class SpectrumAnalyzer(Instrument.Instrument):
    def __init__(self, device):
       #TODO Add in 
       self.instrument = device
       self.name = EInstrument.SPECTRUM_ANALYZER
       self.valid_booleans = ['ON', 'OFF', 1, 0]

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
    #Test
    '''SPIKE pplication display controls.'''
    def is_spike_hidden(self):
        #TODO: Test that :DATA unneeded
        """ Queries if the spike application is hidden."""
        comm = ":DISP:HIDE?"
        response = self.instrument.query(comm)
        if response in ['ON', 1]:
            return True
        elif response in ['OFF', 0]:
            return False
        else:
            print("Invalid response received: " + response)
            return None

    def hide_spike(self, to_hide):
        """When set to true, hides the Spike application. The application will 
        be hidden in the taskbar but will continue to be visible in the task manager.
        The SCPI lockout dialog, device connecting progress dialog, no device 
        connected alert dialog and multiple devices connected alert dialog will be 
        hidden, overriding related settings in the preferences menu."""
    
        
        if to_hide in self.valid_booleans:
            comm = ":DISP:HIDE " + str(to_hide).upper()
            self.instrument.write(comm)
        else:
            print("Invalid format. Allowed values are: " + str(self.valid_booleans))
    
    def get_measurement_title(self):
        """ Get the measurement title."""
        comm = ":DISP:ANN:TITLE?"
        return self.instrument.query(comm)
    
    def set_measurement_title(self, title):
        """ Set the measurement title."""
        if isinstance(title, str):
            comm = ":DISP:ANN:TITLE " + title
            self.instrument.write(comm)
        else:
            print("Invalid type. Title must be a string.")
    
    def clear_measurement_title(self):
        """ Clear the measurement title."""
        comm = ":DISP:ANN:CLEar"
        self.instrument.write(comm)

    #Format Trace Controls
    def get_trace_format(self):
        #TODO: Test that :DATA unneeded
        """ Query the format the trace data is returned in."""
        comm = ":FORM:TRAC?"
        return self.instrument.query(comm)

    def set_trace_format(self, format):
        """Set the format the trace data is returned in.
        form: 'ASCii', 'REAL'"""
    
        allowed_type_values = ['ASCII', 'REAL','ASC']
        if format.upper() in allowed_type_values:
            comm = ":FORM:TRAC " + format
            self.instrument.write(comm)
        else:
            print("Invalid format. Allowed values are: " + str(allowed_type_values))
    
    def get_iq_format(self):
        #TODO: Test that :DATA unneeded
        """ Query the format the iq data is returned in."""
        comm = ":FORM:IQ?"
        return self.instrument.query(comm)

    def set_iq_format(self, format):
        """Set the format the iq data is returned in.
        form: 'ASCii', 'BINary'"""
    
        allowed_type_values = ['ASCII', 'BINARY','BIN','ASC']
        if format.upper() in allowed_type_values:
            comm = ":FORM:IQ " + format
            self.instrument.write(comm)
        else:
            print("Invalid format. Allowed values are: " + str(allowed_type_values))
    
    #System Controls
    """The following commands are used to 
    perform system level software actions and query information about the system."""
    def close_system(self):
        """
        Disconnects any active device and closes the Spike software.
        There is no way to reopen the software using SCPI commands.
        This will also terminate the socket connection with the Spike software.
        """
        comm = ":SYST:CLOS"
        self.instrument.write(comm)
        print("System close command sent. Socket connection terminated.")

    def preset_system(self):
        """
        Presets the active device. This will power cycled the active device and
        return the software to the initial power on state. This process can take
        between 6-20 seconds depending on the device type.
        """
        comm = ":SYST:PRES"
        self.instrument.write(comm)

    def is_preset_successful(self):
        """
        Queries the preset status of the active device. This will close and reopen
        the active device. This process can take between 6-20 seconds depending
        on the device type. R
        """
        comm = ":SYST:PRES?"
        response = self.instrument.query(comm)
        try:
            status = int(response)
            if status == 1:
                print("System preset successful.")
            else:
                print("System preset failed or in progress.")
            return (1==status)
        except ValueError:
            print(f"Invalid response for preset status: {response}")
            return None

    def save_image(self, filename):
        """
        Saves a screenshot with the given file name. The file will be in .ini format.
        params: filename (str): The name of the file to save the image as. Should have a '.ini' extension.
        """
        if not filename.endswith(".ini"):
            filename = filename + ".ini"
        comm = f":SYST:IMAG:SAVE {filename}"
        self.instrument.write(comm)

    def save_image_quick(self):
        """
        Saves a quick image. Same functionality as the Image quick save file menu option.
        """
        comm = ":SYST:IMAG:SAVE:QUICK"
        self.instrument.write(comm)

    def load_user_preset(self, filename):
        """
        Loads the preset given by the file name. If the preset does not exist,
        nothing occurs.
        params: filename (str): The name of the preset file to load. Should have a '.ini' extension.
        """
        if not filename.endswith(".ini"):
            filename = filename + ".ini"
        comm = f":SYST:PRES:USER:LOAD {filename}"
        self.instrument.write(comm)

    def save_user_preset(self, filename):
        """
        Saves the user preset with the given file name. The file name should have
        extension ".ini".
        params: filename (str): The name of the file to save the user preset as. Should have a '.ini' extension.
        """
        if not filename.endswith(".ini"):
            filename = filename + ".ini"
        comm = f":SYST:PRES:USER:SAVE {filename}"
        self.instrument.write(comm)

    def communicate_gtlocal(self):
        """
        Puts Spike in local mode.
        """
        comm = ":SYST:COMM:GTL"
        self.instrument.write(comm)

    def print_system(self):
        """
        Prints the default system print settings.
        """
        comm = ":SYST:PRIN"
        self.instrument.write(comm)

    def get_temperature(self):
        """
        Returns the current internal temperature of the active device, in degrees Clsius.
        """
        comm = ":SYST:TEMP?"
        temperature = self.instrument.query(comm)
        try:
            temp_float = float(temperature)
          
            return temp_float
        except ValueError:
            print(f"Invalid response for temperature: {temperature}")
            return None

    def get_voltage(self):
        """
        Returns the measured voltage of the active device, in volts.
        """
        comm = ":SYST:VOLT?"
        voltage = self.instrument.query(comm)
        try:
            volt_float = float(voltage)
            
            return volt_float
        except ValueError:
            print(f"Invalid response for voltage: {voltage}")
            return None

    def get_current(self):
        """
        Returns the measured current of the active device, in amps.
        (BB and SM series devices only. SA series devices return 0.)
        """
        comm = ":SYST:CURR?"
        current = self.instrument.query(comm)
        try:
            current_float = float(current)
         
            return current_float
        except ValueError:
            print(f"Invalid response for current: {current}")
            return None
    

    #Device Management Controls
    """The functions below allow you to remotely manage the active device 
    in the Spike software. This is useful for error recovery in the event a 
    device disconnect occurs due, or if one is managing multiple Signal Hound devices on one PC."""
    
    def get_device_active_status(self):
        """
        Returns whether or not a device is currently connected and active in the software.
        Look at the *IDN? function to request information about the device.
        """
        comm = ":SYST:DEV:ACT?"
        response = self.instrument.query(comm)
        try:
            status = int(response)
            if status == 1:
                print("Device is active.")
                return True
            else:
                print("No device is active.")
                return False
        except ValueError:
            print(f"Invalid response for device active status: {response}")
            return None

    def get_device_count(self):
        """
        Returns the number of devices connected to the PC. No device may be
        active when this function is called. IE, you must call DISConnect? before calling
        this function. Any networked device that have been configured will be counted
        in the returned value.
        """
        comm = ":SYST:DEV:COUN?"
        response = self.instrument.query(comm)
        try:
            count = int(response)
            print(f"Number of connected devices: {count}")
            return count
        except ValueError:
            print(f"Invalid response for device count: {response}")
            return None

    def get_device_list(self):
        """
        Returns the connection strings for all devices available to connect in the
        Spike software. For USB devices, this is serial numbers returned as ascii integers
        and comma separated. If any networked devices have been configured they will be
        returned in the list with the following form: SOCKET::IP::PORT example, SOCKET::192.168.1.1::12345
        This entire string can be sent to the connect function to connect to a networked device.
        """
        comm = ":SYST:DEV:LIST?"
        response = self.instrument.query(comm)
        device_list = [d.strip() for d in response.split(',')]
        print(f"Available devices: {device_list}")
        return device_list

    def get_current_device_connection_string(self):
        """
        Returns the currently active device's connection string. See LIST? for format.
        """
        comm = ":SYST:DEV:CURR?"
        response = self.instrument.query(comm)
        print(f"Current active device connection string: {response}")
        return response

    def connect_device(self, connection_string):
        """
        Connects a device in the Spike software. For USB devices, you need to
        provide the serial number of the device to connect. For networked devices,
        send a string with form: SOCKET::IP::PORT example, SOCKET::192.168.1.1::12345
        Returns 0 or 1 depending on if the device successfully opened.
        params: connection_string (str): The connection string of the device to connect.
                                         For USB, this is the serial number. For networked,
                                         it's in the format SOCKET::IP::PORT.
        """
        comm = f":SYST:DEV:CON {connection_string}"
        self.instrument.write(comm)
        # The documentation states it returns 0 or 1, but this is a 'write' command,
        # so we'd typically query a status afterward if available.
        # For now, we'll just print a message indicating the command was sent.

    def disconnect_device(self):
        """
        Disconnects any device actively connected in Spike.
        """
        comm = ":SYST:DEV:DISC"
        response = self.instrument.query(comm) # This command is a query that returns 1
        try:
            status = int(response)
            if status == 1:
                print("Device disconnected successfully.")
                return True
            else:
                print("Device disconnection failed.")
                return False
        except ValueError:
            print(f"Invalid response for disconnect status: {response}")
            return None
    
    #Error Controls
    '''These commands control the measurement mode of the Spike software.'''
        #COUNT already implemented
        #NEXT already implemented
    def clear_all_errors(self):
        """
        Remove all errors from the queue, returns nothing.
        """
        comm = ":SYST:ERR:CLE"
        self.instrument.write(comm)
        print("All errors cleared from the error queue.")
    
    #Measurement Mode Controls
    def set_mode(self, mode):
        """
        Determines the current measurement mode.
        params: mode (str): The desired measurement mode. Allowed values are:
                      'SA', 'RTSA', 'ZS', 'HARMonics', 'NA', 'PN', 'DDEMod',
                      'EMI', 'ADEMod', 'IH', 'SEMask', 'NFIGure', 'WLAN', 'BLE', 'LTE'.
        """
        if mode.upper() in self.allowed_modes:
            comm = f":INST:SEL {mode.upper()}"
            self.instrument.write(comm)
            
        else:
            print(f"Invalid mode: '{mode}'. Allowed modes are: {', '.join(self.allowed_modes)}")

    def get_mode(self):
        """
        Queries the current measurement mode.
        """
        comm = ":INST:SEL?"
        current_mode = self.instrument.query(comm)
    
        return current_mode

    def recalibrate_device(self):
        """
        Performs a device recalibration.
        """
        comm = ":INST:REC"
        self.instrument.write(comm)
       
        # Recalibration might take time, consider adding a delay or status check if available
    #Initiate Commands
    """The commands are used to control when 
    measurements are performed in the application.
    For automated measurements, it is common/recommended 
    to disable CONTinuous measurement and control when 
    the software performs the next measurement 
    (sweep/IQ acquisition/etc) with the INIT:IMM command."""
    def enable_continous_measurement(self, enable):
        """
        Enables or disables continuous measurement operation.
        params: enable (bool): True to enable continuous measurement, False to disable.
        """
        comm = ":INIT:CONT " + ('ON' if enable else 'OFF')
        self.instrument.write(comm)
    
    def is_continuous_measurement_enabled(self):
        """
        Queries the current status of continuous measurement operation.
        Returns 1 if ON, 0 if OFF.
        """
        comm = ":INIT:CONT?"
        status = self.instrument.query(comm)
        return (1 == status)

    def trigger_immediate_measurement(self):
        """
        Triggers a measurement. Has no effect if CONTINUOUS is enabled.
        """
        comm = ":INITiate:IMMediate"
        self.instrument.write(comm)
        # If continuous is enabled, this command has no effect as per documentation.
        # You might want to check get_continuous_measurement_status() before call

    #Limit Lines
    """These commands control the limit lines which are available in sweep, 
    real-time, and network analysis measurement modes. """
    def enable_limit_line_testing(self, line_num, enable):
        """
        Enables or disables limit line testing.
        params: line_num (int): The limit line number to enable/disable (1-6).
                enable (bool): True to enable limit line testing, False to disable.
        """
        comm = ":CALC:LLINE"+str(line_num)+":STAT" + ('ON' if enable else 'OFF')
        self.instrument.write(comm)

    def is_limit_line_testing_enabled(self, line_num):
        """
        Queries if limit line testing is enabled for a specific limit line.
        params: line_num (int): The limit line number to check (1-6).
        Returns 1 if enabled, 0 if disabled.
        """
        comm = ":CALC:LLINE"+str(line_num)+":STAT?"
        status = self.instrument.query(comm)
        return (status==1)
        
    
    def set_limit_line_state(self, line_num, state):
        """
        Enables or disables limit line testing. If there are not at least 2 points
        in the limit line, testing doesn't occur despite being enabled.
        params: line_num (int): The limit line number (1-6).
                state (str or int): 'ON', 'OFF', 1 (for ON), or 0 (for OFF).
        """
        self._validate_line_num(line_num)

        if state in self.valid_booleans:
            comm = f":CALC:LLINE{line_num}:STAT {state}"
            self.instrument.write(comm)
        else:
            print(f"Invalid state: '{state}'. Allowed values are: {self.valid_booleans}")


    def set_limit_line_title(self, line_num, title):
        """
        Specifies the name of the limit line.
        params: line_num (int): The limit line number (1-6).
                title (str): The name of the limit line.
        """
        self._validate_line_num(line_num)
        comm = f":CALC:LLINE{line_num}:TITL '{title}'" # SCPI strings often need quotes
        self.instrument.write(comm)

    def get_limit_line_title(self, line_num):
        """
        Queries the name of the limit line.
        params: line_num (int): The limit line number (1-6).
        Returns: str: The name of the limit line.
        """
        self._validate_line_num(line_num)
        comm = f":CALC:LLINE{line_num}:TITL?"
        title = self.instrument.query(comm)
        return title

    def set_limit_line_trace(self, line_num, trace_number):
        """
        Specifies which trace is tested against this limit line.
        params: line_num (int): The limit line number (1-6).
                trace_number (int): The trace number to test against.
        """
        self._validate_line_num(line_num)
        comm = f":CALC:LLINE{line_num}:TRAC {trace_number}"
        self.instrument.write(comm)

    def get_limit_lines_trace(self, line_num):
        """
        Queries which trace is tested against this limit line.
        params: line_num (int): The limit line number (1-6).
        Returns: str: The trace number.
        """
        self._validate_line_num(line_num)
        comm = f":CALC:LLINE{line_num}:TRAC?"
        trace = self.instrument.query(comm)
        return trace

    def set_limit_line_type(self, line_num, line_type):
        """
        Specifies whether the limit line is an upper or lower bound.
        params: line_num (int): The limit line number (1-6).
                line_type (str): 'UPPer' for upper bound, 'LOWer' for lower bound.
        """
        self._validate_line_num(line_num)
        line_type_upper = line_type.upper()
        if line_type_upper in ['UPPER', 'LOWER']:
            comm = f":CALC:LLINE{line_num}:TYPE {line_type_upper}"
            self.instrument.write(comm)
        else:
            print(f"Invalid limit line type: '{line_type}'. Allowed values are 'UPPer' or 'LOWer'.")

    def get_limit_line_type(self, line_num):
        """
        Queries whether the limit line is an upper or lower bound.
        params: line_num (int): The limit line number (1-6).
        Returns: str: 'UPPer' or 'LOWer'.
        """
        self._validate_line_num(line_num)
        comm = f":CALC:LLINE{line_num}:TYPE?"
        line_type = self.instrument.query(comm)
        return line_type

    def set_limit_line_reference(self, line_num, reference_type):
        """
        Specifies whether the limit line values are fixed/absolute or relative
        to the center frequency and ref level.
        params: line_num (int): The limit line number (1-6).
                reference_type (str): 'FIXed' for fixed/absolute, 'RELative' for relative.
        """
        self._validate_line_num(line_num)
        reference_type_upper = reference_type.upper()
        if reference_type_upper in ['FIXED', 'RELATIVE']:
            comm = f":CALC:LLINE{line_num}:REFerence {reference_type_upper}"
            self.instrument.write(comm)
        else:
            print(f"Invalid reference type: '{reference_type}'. Allowed values are 'FIXed' or 'RELative'.")

    def get_limit_line_reference(self, line_num):
        """
        Queries whether the limit line values are fixed/absolute or relative.
        params: line_num (int): The limit line number (1-6).
        Returns: str: 'FIXed' or 'RELative'.
        """
        self._validate_line_num(line_num)
        comm = f":CALC:LLINE{line_num}:REFerence?"
        reference = self.instrument.query(comm)
        return reference

    def transform_limit_line_reference(self, line_num):
        """
        Builds limit line points from trace, max holding across frequency sections.
        params: line_num (int): The limit line number (1-6).
        """
        self._validate_line_num(line_num)
        comm = f":CALC:LLINE{line_num}:REFerence:TRANsform"
        self.instrument.write(comm)

    def set_limit_line_interpolation(self, line_num, interpolation_type):
        """
        Specifies whether the limit line uses linear or logarithmic interpolation.
        params: line_num (int): The limit line number (1-6).
                interpolation_type (str): 'LINear' for linear, 'LOGarithmic' for logarithmic.
        """
        self._validate_line_num(line_num)
        interpolation_type_upper = interpolation_type.upper()
        if interpolation_type_upper in ['LINEAR', 'LOGARITHMIC']:
            comm = f":CALC:LLINE{line_num}:INTerpolate {interpolation_type_upper}"
            self.instrument.write(comm)
        else:
            print(f"Invalid interpolation type: '{interpolation_type}'. Allowed values are 'LINear' or 'LOGarithmic'.")

    def get_limit_line_interpolation(self, line_num):
        """
        Queries whether the limit line uses linear or logarithmic interpolation.
        params: line_num (int): The limit line number (1-6).
        Returns: str: 'LINear' or 'LOGarithmic'.
        """
        self._validate_line_num(line_num)
        comm = f":CALC:LLINE{line_num}:INTerpolate?"
        interpolation = self.instrument.query(comm)
        return interpolation

    def set_limit_line_pause_state(self, line_num, state):
        """
        When enabled, a failure of this limit will pause the sweep update.
        params: line_num (int): The limit line number (1-6).
                state (str or int): 'ON', 'OFF', 1 (for ON), or 0 (for OFF).
        """
        self._validate_line_num(line_num)

        if state in self.valid_booleans:
            comm = f":CALC:LLINE{line_num}:PAUSE:STATe {state}"
            self.instrument.write(comm)
        else:
            print(f"Invalid state: '{state}'. Allowed values are: {self.valid_booleans}")

    def get_limit_line_pause_state(self, line_num):
        """
        Queries if a failure of this limit will pause the sweep update.
        params: line_num (int): The limit line number (1-6).
        Returns: True is enabled, False if disabled.
        """
        self._validate_line_num(line_num)
        comm = f":CALC:LLINE{line_num}:PAUSE:STATe?"
        status = self.instrument.query(comm)
        return (1==status)

    def set_limit_line_display_visibility(self, line_num, state):
        """
        When enabled, the limit line will be visible on the graticule.
        params: line_num (int): The limit line number (1-6).
                state (str or int): 'ON', 'OFF', 1 (for ON), or 0 (for OFF).
        """
        self._validate_line_num(line_num)

        if state in self.valid_booleans:
            comm = f":CALC:LLINE{line_num}:DISP:STATe {state}"
            self.instrument.write(comm)
        else:
            print(f"Invalid state: '{state}'. Allowed values are: {self.valid_booleans}")

    def is_limit_line_display_visible(self, line_num):
        """
        Queries if the limit line is visible on the graticule.
        params: line_num (int): The limit line number (1-6).
        Returns: str: 1 if visible, 0 if hidden.
        """
        self._validate_line_num(line_num)
        comm = f":CALC:LLINE{line_num}:DISP:STATe?"
        status = self.instrument.query(comm)
        return (1==status)

    def change_limit_line_result_visibility(self, line_num, state):
        """
        When enabled, the limit line pass/fail result will be visible on the graticule.
        params: line_num (int): The limit line number (1-6).
                state (str or int): 'ON', 'OFF', 1 (for ON), or 0 (for OFF).
        """
        self._validate_line_num(line_num)

        if state in self.valid_booleans:
            comm = f":CALC:LLINE{line_num}:DISP:RES:STAT {state}"
            self.instrument.write(comm)
        else:
            print(f"Invalid state: '{state}'. Allowed values are: {self.valid_booleans}")

    def is_limit_line_result_visible(self, line_num):
        """
        Queries if the limit line pass/fail result is visible on the graticule.
        params: line_num (int): The limit line number (1-6).
        Returns: str: 1 if visible, 0 if hidden.
        """
        self._validate_line_num(line_num)
        comm = f":CALC:LLINE{line_num}:DISP:RES:STAT?"
        status = self.instrument.query(comm)
        return (status == 1)

    def set_limit_line_offset_y(self, line_num, offset_value):
        """
        Specifies a dB offset to the limit line.
        params: line_num (int): The limit line number (1-6).
                offset_value (float): The offset value in dB.
        """
        self._validate_line_num(line_num)
        comm = f":CALC:LLINE{line_num}:OFFSet:Y {offset_value}"
        self.instrument.write(comm)

    def get_limit_line_offset_y(self, line_num):
        """
        Queries the dB offset of the limit line.
        params: line_num (int): The limit line number (1-6).
        Returns: str: The offset value in dB.
        """
        self._validate_line_num(line_num)
        comm = f":CALC:LLINE{line_num}:OFFSet:Y?"
        offset = self.instrument.query(comm)
        return offset

    def build_limit_line(self, line_num):
        """
        Builds limit line points from trace, max holding across frequency sections.
        params: line_num (int): The limit line number (1-6).
        """
        self._validate_line_num(line_num)
        comm = f":CALC:LLINE{line_num}:BUILD"
        self.instrument.write(comm)

    def get_limit_line_build_points(self, line_num):
        """
        Returns the number of points in the limit line as an integer.
        params: line_num (int): The limit line number (1-6).
        Returns: int: The number of points in the limit line.
        """
        self._validate_line_num(line_num)
        comm = f":CALC:LLINE{line_num}:BUILD:POIN?"
        points = self.instrument.query(comm)
        try:
            num_points = int(points)
            return num_points
        except ValueError:
            print(f"Invalid response for limit line build points: {points}")
            return None

    def save_limit_line_points(self, line_num):
        """
        Specifies the points in the limit line will overwrite any existing points.
        Points are specified as freq/amplitude pairs where the amplitude is specified as dBm.
        This command saves the currently defined points.
        params: line_num (int): The limit line number (1-6).
        """
        self._validate_line_num(line_num)
        comm = f":CALC:LLINE{line_num}:SAVE"
        self.instrument.write(comm)

    def get_limit_line_data(self, line_num):
        """
        Returns the points in the limit line. Points are returned as freq/amplitude pairs
        where the frequencies are specified as Hz and the amplitudes as dBm.
        params: line_num (int): The limit line number (1-6).
        Returns: str: A string of comma-separated frequency and amplitude pairs (e.g., "freq1,amp1,freq2,amp2,...").
        """
        self._validate_line_num(line_num)
        comm = f":CALC:LLINE{line_num}:DATA?"
        data = self.instrument.query(comm)
        return data

    def get_limit_line_test_status(self, line_num):
        """
        Returns 1 when the limit test has failed, 0 if passed.
        params: line_num (int): The limit line number (1-6).
        Returns: True if passed.
        """
        self._validate_line_num(line_num)
        comm = f":CALC:LLINE{line_num}:FAIL?"
        status = self.instrument.query(comm)
        return (status == 0)

    def clear_all_limit_lines(self):
        """
        Resets all limit lines. Removes all points stored.
        """
        comm = ":CALC:LLINE:ALL:CLE"
        self.instrument.write(comm)
    
    #Path Loss Table Controls
    """These commands control the path loss tables which are available in sweep, 
    real-time, zero-span, harmonics, digital modulation analysis, 
    EMC precompliance, analog demod, and interference hunting measurement modes."""

    def set_path_loss_table_state(self, table_num, state):
        """
        Enables or disables application of this path loss table.
        params: table_num (int): The path loss table number (1-8).
                state (str or int): 'ON', 'OFF', 1 (for ON), or 0 (for OFF).
        """
        self._validate_pathloss_table_num(table_num)
        
        if state in self.valid_booleans:
            comm = f":SENS:CORR:PATH{table_num}:STAT {state}"
            self.instrument.write(comm)
        else:
            print(f"Invalid state: '{state}'. Allowed values are: {self.valid_booleans}")

    def get_path_loss_table_state(self, table_num):
        """
        Queries if the path loss table is enabled.
        params: table_num (int): The path loss table number (1-8).
        Returns: bool: True if enabled, False if disabled.
        """
        self._validate_pathloss_table_num(table_num)
        comm = f":SENS:CORR:PATH{table_num}:STAT?"
        status = self.instrument.query(comm)
        return (status == 1)

    def set_path_loss_table_description(self, table_num, description):
        """
        Specifies the name/description of this path loss table.
        params: table_num (int): The path loss table number (1-8).
                description (str): The name or description of the path loss table.
        """
        self._validate_pathloss_table_num(table_num)
        comm = f":SENS:CORR:PATH{table_num}:DESC '{description}'"
        self.instrument.write(comm)

    def get_path_loss_table_description(self, table_num):
        """
        Queries the name/description of this path loss table.
        params: table_num (int): The path loss table number (1-8).
        Returns: str: The name or description of the path loss table.
        """
        self._validate_pathloss_table_num(table_num)
        comm = f":SENS:CORR:PATH{table_num}:DESC?"
        description = self.instrument.query(comm)
        return description

    def set_path_loss_table_total_points(self, table_num, points_data):
        """
        Specifies the number of points in the path loss table, will overwrite any existing points.
        Points are specified as freq/offset pairs where the offset is specified as dB.
        params: table_num (int): The path loss table number (1-8).
                points_data (dict): (frequency, offset) pairs where frequency is in Hz and offset is in dB.
        """
        data = ""
        for key in points_data.keys():
            data = data + str(key) + "," + str(points_data[key]) + ","

        self._validate_pathloss_table_num(table_num)
        comm = f":SENS:CORR:PATH{table_num}:DATA {data[0:data.__len__()-1]}"
        self.instrument.write(comm)

    def get_path_loss_table_points_count(self, table_num):
        """
        Returns the number of points in the path loss table as an integer.
        params: table_num (int): The path loss table number (1-8).
        Returns: int: The number of points in the path loss table.
        """
        self._validate_pathloss_table_num(table_num)
        comm = f":SENS:CORR:PATH{table_num}:POIN?"
        points = self.instrument.query(comm)
        return int(points)

    def get_path_loss_table_data(self, table_num):
        """
        Returns the points in the path loss table. Points are returned as freq/offset
        pairs where the frequencies are specified as Hz and the offsets as dB.
        params: table_num (int): The path loss table number (1-8).
        Returns: dict : (frequency,offset) 
        """
        self._validate_pathloss_table_num(table_num)
        comm = f":SENS:CORR:PATH{table_num}:DATA?"
        data = self.instrument.query(comm)
        #TODO Test data is correct in unit test
        data_list = data.split(',')
        data_dict = {}
        for i in range(0,data_list,2):
            data_dict[data_list[i]] = data_list[i+1]

        return data_dict

    def clear_path_loss_table(self, table_num):
        """
        Resets the selected path loss table. Removes all points stored.
        params: table_num (int): The path loss table number (1-8).
        """
        self._validate_pathloss_table_num(table_num)
        comm = f":SENS:CORR:PATH{table_num}:CLE"
        self.instrument.write(comm)

    def clear_all_path_loss_tables(self):
        """
        Resets all path loss tables. Removes all points stored.
        """
        comm = ":SENS:CORR:PATH:ALL:CLE"
        self.instrument.write(comm)
#Reference Oscillscope Controls
    """These commands control the reference oscillator settings the of the spectrum analyzer."""
    def set_reference_oscillator_source(self, source):
        """
        Configures the reference oscillator source of the spectrum analyzer.
        params: source (str): The desired reference source. Allowed values are:
                              'INTERNAL', 'EXTERNAL', 'OUTPUT'.
        """
        allowed_sources = ['INTERNAL', 'EXTERNAL', 'OUTPUT', 'INT', 'EXT', 'OUT']
        source_upper = source.upper()
        if source_upper in allowed_sources:
            comm = f":SENS:ROSCILLATOR:SOURCE {source_upper}"
            self.instrument.write(comm)
        else:
            print(f"Invalid source: '{source}'. Allowed values are: {', '.join(allowed_sources)}")

    def get_reference_oscillator_source(self):
        """
        Queries the current reference oscillator source of the spectrum analyzer.
        Returns: str: The current reference source ('INTERNAL', 'EXTERNAL', 'OUTPUT').
        """
        comm = ":SENS:ROSCILLATOR:SOURCE?"
        source = self.instrument.query(comm)
        return source

#Frequency Controls
    """These commands control the frequency settings of the spectrum analyzer."""
    def set_sense_frequency_center_step(self, step_size_hz: float):
        """
        Sets the step amount the center frequency changes by when using the UP or DOWN parameters on the CENTer command.
        Parameters:
        step_size_hz: The step size in Hz (numeric value).
        """
        self.instrument.write(f"SENS:FREQ:CENT:STEP {step_size_hz}")

    def get_sense_frequency_center_step(self) -> float:
        """
        Queries the center frequency step size in Hz.
        Returns: The step size in Hz (numeric value).
        """
        response = self.instrument.query("SENS:FREQ:CENT:STEP?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for frequency center step size (not numeric): '{response}'")

#Power Controls
    """These commands affect the RF front end of the device.    
    Not all settings are available for each Signal Hound spectrum analyzer. 
    It is recommended to leave attenuation/gain/preamp set to auto and control the RF leveling with reference level."""
    
    def set_rf_reference_level(self, amplitude: float, direction: str = None):
        """
        Sets the RF reference level. If UP or DOWN is specified, the reference level is increased or decreased by the amplitude.
        Parameters:
        amplitude (float): The reference level in dBm.
        direction (str): 'UP' or 'DOWN' to adjust the reference level incrementally.
        """
        if direction:
            comm = f":SENS:POWER:RF:RLEVEL {amplitude} {direction.upper()}"
        else:
            comm = f":SENS:POWER:RF:RLEVEL {amplitude}"
        self.instrument.write(comm)

    def get_rf_reference_level(self) -> float:
        """
        Queries the current RF reference level in dBm.
        Returns: float: The reference level in dBm.
        """
        response = self.instrument.query(":SENS:POWER:RF:RLEVEL?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for RF reference level: '{response}'")

    def get_rf_reference_level_unit(self) -> str:
        """
        Queries the current amplitude unit used to express the RF reference level.
        Returns: str: The amplitude unit (e.g., 'dBm').
        """
        return self.instrument.query(":SENS:POWER:RF:RLEVEL:UNIT?").strip()

    def set_rf_reference_level_offset(self, offset: float):
        """
        Sets the RF reference level offset in dB.
        Parameters:
        offset (float): The offset value in dB.
        """
        comm = f":SENS:POWER:RF:RLEVEL:OFFSET {offset}"
        self.instrument.write(comm)

    def get_rf_reference_level_offset(self) -> float:
        """
        Queries the RF reference level offset in dB.
        Returns: float: The offset value in dB.
        """
        response = self.instrument.query(":SENS:POWER:RF:RLEVEL:OFFSET?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for RF reference level offset: '{response}'")

    def set_rf_plot_division(self, division: float):
        """
        Specifies the plot vertical division (1/10th of the plot height) as dB.
        Parameters:
        division (float): The division value in dB.
        """
        comm = f":SENS:POWER:RF:PDIVISION {division}"
        self.instrument.write(comm)

    def get_rf_plot_division(self) -> float:
        """
        Queries the plot vertical division as dB.
        Returns: float: The division value in dB.
        """
        response = self.instrument.query(":SENS:POWER:RF:PDIVISION?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for RF plot division: '{response}'")

    def set_rf_attenuation(self, attenuation: int):
        """
        Sets the RF attenuation index.
        Parameters:
        attenuation (int): The attenuation index.
        """
        comm = f":SENS:POWER:RF:ATTENUATION {attenuation}"
        self.instrument.write(comm)

    def get_rf_attenuation(self) -> int:
        """
        Queries the RF attenuation index.
        Returns: int: The attenuation index.
        """
        response = self.instrument.query(":SENS:POWER:RF:ATTENUATION?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for RF attenuation: '{response}'")

    def set_rf_attenuation_auto(self, enable: bool):
        """
        Enables or disables automatic RF attenuation.
        Parameters:
        enable (bool): True to enable automatic attenuation, False to disable.
        """
        comm = f":SENS:POWER:RF:ATTENUATION:AUTO {1 if enable else 0}"
        self.instrument.write(comm)

    def get_rf_attenuation_auto(self) -> bool:
        """
        Queries if automatic RF attenuation is enabled.
        Returns: bool: True if enabled, False if disabled.
        """
        response = self.instrument.query(":SENS:POWER:RF:ATTENUATION:AUTO?").strip()
        return response == 1

    def set_rf_gain(self, gain: int):
        """
        Sets the RF gain index.
        Parameters:
        gain (int): The gain index.
        """
        comm = f":SENS:POWER:RF:GAIN {gain}"
        self.instrument.write(comm)
    def get_rf_gain(self) -> int:
        """
        Queries the RF gain index.
        Returns: int: The gain index.
        """
        response = self.instrument.query(":SENS:POWER:RF:GAIN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for RF gain: '{response}'")

    def set_rf_gain_auto(self, enable: bool):
        """
        Enables or disables automatic RF gain.
        Parameters:
        enable (bool): True to enable automatic gain, False to disable.
        """
        comm = f":SENS:POWER:RF:GAIN:AUTO {1 if enable else 0}"
        self.instrument.write(comm)

    def get_rf_gain_auto(self) -> bool:
        """
        Queries if automatic RF gain is enabled.
        Returns: bool: True if enabled, False if disabled.
        """
        response = self.instrument.query(":SENS:POWER:RF:GAIN:AUTO?").strip()
        return response == 1

    def set_rf_preamp(self, preamp: int):
        """
        Sets the RF preamp index.
        Parameters:
        preamp (int): The preamp index.
        """
        comm = f":SENS:POWER:RF:PREAMP {preamp}"
        self.instrument.write(comm)

    def get_rf_preamp(self) -> int:
        """
        Queries the RF preamp index.
        Returns: int: The preamp index.
        """
        response = self.instrument.query(":SENS:POWER:RF:PREAMP?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for RF preamp: '{response}'")

    def set_rf_preamp_auto(self, enable: bool):
        """
        Enables or disables automatic RF preamp.
        Parameters:
        enable (bool): True to enable automatic preamp, False to disable.
        """
        comm = f":SENS:POWER:RF:PREAMP:AUTO {1 if enable else 0}"
        self.instrument.write(comm)

    def get_rf_preamp_auto(self) -> bool:
        """
        Queries if automatic RF preamp is enabled.
        Returns: bool: True if enabled, False if disabled.
        """
        response = self.instrument.query(":SENS:POWER:RF:PREAMP:AUTO?").strip()
        return response == 1

    def set_rf_spur_reject(self, enable: bool):
        """
        Enables or disables RF spur rejection.
        Parameters:
        enable (bool): True to enable spur rejection, False to disable.
        """
        comm = f":SENS:POWER:RF:SPURREJECT {1 if enable else 0}"
        self.instrument.write(comm)

    def get_rf_spur_reject(self) -> bool:
        """
        Queries if RF spur rejection is enabled.
        Returns: bool: True if enabled, False if disabled.
        """
        response = self.instrument.query(":SENS:POWER:RF:SPURREJECT?").strip()
        return response == 1
#Bandwidth
    """These commands control the FFT processing for the receivers. 
    These settings are highly coupled with the frequency range and sweep time."""
    
    def set_sense_bandwidth_shape(self, shape_type: str):
        """
        Specifies the FFT window function for bandwidth shaping.
        Parameters:
        shape_type (str): The shape type. Allowed values are 'FLATTOP', 'NUTTALL', 'GAUSSIAN'.
        """
        valid_shapes = {"FLATTOP", "NUTTALL", "GAUSSIAN", "FLAT", "NUT", "GAUS"}
        shape_upper = shape_type.upper()
        if shape_upper not in valid_shapes:
            raise ValueError(f"Invalid shape type: '{shape_type}'. Must be 'FLATTOP', 'NUTTALL', or 'GAUSSIAN'.")
        

        self.instrument.write(f"SENS:BAND:SHAP {shape_type}")

    def get_sense_bandwidth_shape(self) -> str:
        """
        Queries the FFT window function for bandwidth shaping.
        Returns:
        str: The shape type ('FLATTOP', 'NUTTALL', or 'GAUSSIAN').
        """
        response = self.instrument.query("SENS:BAND:SHAP?").strip()
        return response
#Sweep Controls
    """The sweep commands control additional FFT settings of the receiver."""
    def set_sweep_detector_function(self, function_type: str):
        """
        Controls how the VBW processing is performed.
        Parameters:
        function_type (str): Allowed values are 'AVERAGE', 'MINMAX', 'MIN', 'MAX'.
        """
        valid_functions = {"AVERAGE", "MINMAX", "MIN", "MAX", "AVER", "MINM", "MIN", "MAX"}
        function_upper = function_type.upper()
        if function_upper not in valid_functions:
            raise ValueError(f"Invalid detector function type: '{function_type}'. Must be 'AVERAGE', 'MINMAX', 'MIN', or 'MAX'.")
        

        self.instrument.write(f"SENS:SWE:DET:FUNC {function_upper}")

    def get_sweep_detector_function(self) -> str:
        """
        Queries how the VBW processing is performed.
        Returns:
        str: The detector function type ('AVERAGE', 'MINMAX', 'MIN', or 'MAX').
        """
        response = self.instrument.query("SENS:SWE:DET:FUNC?").strip().upper()
        if response.startswith("AVER"):
            return "AVERAGE"
        elif response.startswith("MINM"):
            return "MINMAX"
        elif response.startswith("MIN"):
            return "MIN"
        elif response.startswith("MAX"):
            return "MAX"
        return response

    def set_sweep_detector_units(self, units_type: str):
        """
        Controls the units in which the detector function is performed.
        Parameters:
        units_type (str): Allowed values are 'POWER', 'SAMPLE', 'VOLTAGE', 'LOG'.
        """
        valid_units = {"POWER", "SAMPLE", "VOLTAGE", "LOG", "POW", "SAMP", "VOLT", "LOG"}
        units_upper = units_type.upper()
        if units_upper not in valid_units:
            raise ValueError(f"Invalid detector units type: '{units_type}'. Must be 'POWER', 'SAMPLE', 'VOLTAGE', or 'LOG'.")
        

        self.instrument.write(f"SENS:SWE:DET:UNIT {units_upper}")

    def get_sweep_detector_units(self) -> str:
        """
        Queries the units in which the detector function is performed.
        Returns:
        str: The detector units type ('POWER', 'SAMPLE', 'VOLTAGE', or 'LOG').
        """
        response = self.instrument.query("SENS:SWE:DET:UNIT?").strip().upper()
        return response
#Trace Controls
    def select_trace(self, trace_index: int):
        """
        Specifies a trace index [1,6] for operations to occur on.
        Parameters:
        trace_index (int): The index of the trace to select (1-6).
        """
        if not (1 <= trace_index <= 6):
            raise ValueError("Invalid trace index. Must be between 1 and 6.")
        self.instrument.write(f"TRACE:SELECT {trace_index}")

    def get_trace_select(self) -> int:
        """
        Queries the currently selected trace index.
        Returns:
        int: The index of the currently selected trace (1-6).
        """
        response = self.instrument.query("TRACE:SELECT?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for TRACE:SELECT? (not numeric): '{response}'")

    def set_trace_type(self, trace_type: str):
        """
        Specifies the behavior of the trace.
        Parameters:
        trace_type (str): Allowed values are 'OFF', 'WRITE', 'AVERAGE', 'MAXHOLD', 'MINHOLD', 'MINMAX'.
        """
        valid_types = {"OFF", "WRITE", "AVERAGE", "MAXHOLD", "MINHOLD", "MINMAX"}
        trace_type_upper = trace_type.upper()
        if trace_type_upper not in valid_types:
            raise ValueError(f"Invalid trace type: '{trace_type}'. Must be one of {valid_types}.")
        self.instrument.write(f":TRAC:TYPE {trace_type_upper}")

    def set_trace_average_count(self, count: int):
        """
        Specifies the number of traces that are averaged together to create the final sweep.
        Parameters:
        count (int): The number of traces to average.
        """
        if count < 1:
            raise ValueError("Average count must be a positive integer.")
        self.instrument.write(f":TRAC:AVER:COUN {count}")

    def get_trace_average_count(self) -> int:
        """
        Queries the number of traces that are averaged together to create the final sweep.
        Returns:
        int: The number of traces averaged.
        """
        response = self.instrument.query(":TRAC:AVER:COUN?")
        return int(response)

    def get_trace_average_current(self) -> int:
        """
        Retrieves the current number of traces that have been averaged together to create the final sweep.
        Returns:
        int: The current number of averaged traces.
        """
        response = self.instrument.query(":TRAC:AVER:CURR?")
        return int(response)

    def set_trace_update_state(self, enable: bool):
        """
        Specifies if the trace updates when a new sweep is acquired from the device.
        Parameters:
        enable (bool): True to enable updates, False to disable.
        """
        self.instrument.write(f":TRAC:UPD {1 if enable else 0}")

    def get_trace_update_state(self) -> bool:
        """
        Queries if the trace updates when a new sweep is acquired from the device.
        Returns:
        bool: True if updates are enabled, False otherwise.
        """
        response = self.instrument.query(":TRAC:UPD?")
        return response == 1

    def set_trace_display_state(self, enable: bool):
        """
        Specifies if the trace is hidden or displayed.
        Parameters:
        enable (bool): True to display the trace, False to hide it.
        """
        self.instrument.write(f":TRAC:DISP {1 if enable else 0}")

    def is_trace_display_visible(self) -> bool:
        """
        Queries if the trace is hidden or displayed.
        Returns:
        bool: True if the trace is displayed, False if hidden.
        """
        response = self.instrument.query(":TRAC:DISP?")
        return response == 1

    def clear_trace(self):
        """
        Clears the selected trace. For example, if the current sweep is a max hold sweep,
        and is cleared, the trace will be replaced with the next sweep from the device.
        """
        self.instrument.write(":TRAC:CLE")

    def clear_all_traces(self):
        """
        Clears all traces.
        """
        self.instrument.write(":TRAC:CLE:ALL")

    def get_trace_xstart(self) -> float:
        """
        Retrieves the frequency of the first point in the sweep as Hz.
        Useful for calculating the frequency of each point in the trace data returned from the TRACE:DATA? command.
        Returns:
        float: The frequency of the first point in Hz.
        """
        response = self.instrument.query(":TRAC:XSTA?")
        return float(response)

    def get_trace_xincrement(self) -> float:
        """
        Retrieves the frequency step between two points in the trace data as Hz.
        Useful for calculating the frequency of each point in the trace data.
        Returns:
        float: The frequency increment in Hz.
        """
        response = self.instrument.query(":TRAC:XINC?")
        return float(response)
    
#Marker Controls
    """The marker commands control the Spike sweep markers."""
    def select_marker(self, marker_index: int):
        """
        Selects the active marker.
        Parameters:
        marker_index (int): The index of the marker to select.
        """
        self.instrument.write(f":CALC:MARK:SEL {marker_index}")

    def selected_marker_index(self) -> int:
        """
        Queries the currently selected marker index.
        Returns:
        int: The index of the currently selected marker.
        """
        response = self.instrument.query(":CALC:MARK:SEL?")
        return int(response)

    def enable_marker(self, enable: bool):
        """
        Turns the marker on or off.
        Parameters:
        enable (bool): True to turn the marker on, False to turn it off.
        """
        self.instrument.write(f":CALC:MARK:STAT {1 if enable else 0}")

    def is_marker_visible(self) -> bool:
        """
        Queries the marker state (on or off).
        Returns:
        bool: True if the marker is on, False if it is off.
        """
        response = self.instrument.query(":CALC:MARK:STAT?")
        return response == 1

    def set_marker_trace(self, trace_index: int):
        """
        Specifies which trace to place the marker on.
        Parameters:
        trace_index (int): The index of the trace to place the marker on.
        """
        self.instrument.write(f":CALC:MARK:TRAC {trace_index}")

    def get_marker_trace(self) -> int:
        """
        Queries which trace the marker is placed on.
        Returns:
        int: The index of the trace the marker is placed on.
        """
        response = self.instrument.query(":CALC:MARK:TRAC?")
        return int(response)

    def set_marker_mode(self, mode: str):
        """
        Switches between positional and noise marker modes.
        Parameters:
        mode (str): 'POSITION', 'NOISE', 'CHPOWER', 'NDB'.
        """
        valid_modes = {"POSITION", "NOISE", "POS", "CHPOWER","CHP","NDB"}
        mode_upper = mode.upper()
        if mode_upper not in valid_modes:
            raise ValueError(f"Invalid marker mode: '{mode}'. Must be 'POSITION' or 'NOISE'.")
        self.instrument.write(f":CALC:MARK:MODE {mode_upper}")

    def get_marker_mode(self) -> str:
        """
        Queries the current marker mode.
        Returns:
        str: The current marker mode ('POSITION' or 'NOISE').
        """
        response = self.instrument.query(":CALC:MARK:MODE?")
        return response.upper()

    def enable_marker_update(self, enable: bool):
        """
        Enables or disables marker updates on future sweep updates.
        Parameters:
        enable (bool): True to enable updates, False to disable.
        """
        self.instrument.write(f":CALC:MARK:UPD {1 if enable else 0}")

    def is_marker_update_enabled(self) -> bool:
        """
        Queries if marker updates are enabled on future sweep updates.
        Returns:
        bool: True if updates are enabled, False otherwise.
        """
        response = self.instrument.query(":CALC:MARK:UPD?")
        return response == 1

    def enable_marker_delta(self, enable: bool):
        """
        Enables or disables delta marker mode.
        Parameters:
        enable (bool): True to enable delta mode, False to disable.
        """
        self.instrument.write(f":CALC:MARK:DELT {1 if enable else 0}")

    def is_marker_delta_enabled(self) -> bool:
        """
        Queries if delta marker mode is enabled.
        Returns:
        bool: True if delta mode is enabled, False otherwise.
        """
        response = self.instrument.query(":CALC:MARK:DELT?")
        return response == 1

    def enable_marker_peak_track(self, enable: bool):
        """
        Enables or disables peak tracking for the marker.
        Parameters:
        enable (bool): True to enable peak tracking, False to disable.
        """
        self.instrument.write(f":CALC:MARK:PKTR {1 if enable else 0}")

    def is_marker_peak_track_enabled(self) -> bool:
        """
        Queries if peak tracking is enabled for the marker.
        Returns:
        bool: True if peak tracking is enabled, False otherwise.
        """
        response = self.instrument.query(":CALC:MARK:PKTR?")
        return response == 1

    def set_marker_position(self, frequency_hz: float):
        """
        Moves the marker position to the specified frequency.
        Parameters:
        frequency_hz (float): The frequency in Hz to move the marker to.
        """
        self.instrument.write(f":CALC:MARK:X {frequency_hz}")

    def get_marker_position_frequency(self) -> float:
        """
        Retrieves the marker position frequency in Hz.
        Returns:
        float: The marker position frequency in Hz.
        """
        response = self.instrument.query(":CALC:MARK:X?")
        return float(response)

    def get_marker_position_amplitude(self) -> float:
        """
        Retrieves the marker position amplitude according to marker type.
        Returns:
        float: The marker position amplitude in dBm or dBm/Hz.
        """
        response = self.instrument.query(":CALC:MARK:Y?")
        return float(response)

    def perform_peak_search(self):
        """
        Performs a peak search for the marker.
        """
        self.instrument.write(":CALC:MARK:MAX")

    def move_marker_to_next_peak(self):
        """
        Moves the marker to the next highest peak.
        """
        self.instrument.write(":CALC:MARK:MAX:NEXT")

    def move_marker_to_left_peak(self):
        """
        Moves the marker to the next peak to the left of its current position.
        """
        self.instrument.write(":CALC:MARK:MAX:LEFT")

    def move_marker_to_right_peak(self):
        """
        Moves the marker to the next peak to the right of its current position.
        """
        self.instrument.write(":CALC:MARK:MAX:RIGHT")

    def perform_minimum_search(self):
        """
        Performs a minimum peak search for the marker.
        """
        self.instrument.write(":CALC:MARK:MIN")

    def set_peak_excursion(self, excursion_db: float):
        """
        Specifies the peak excursion in dB.
        Parameters:
        excursion_db (float): The peak excursion in dB.
        """
        self.instrument.write(f":CALC:MARK:PEAK:EXC {excursion_db}")

    def get_peak_excursion(self) -> float:
        """
        Queries the peak excursion in dB.
        Returns:
        float: The peak excursion in dB.
        """
        response = self.instrument.query(":CALC:MARK:PEAK:EXC?")
        return float(response)

    def set_peak_threshold(self, threshold_db: float):
        """
        Specifies the peak threshold in dB.
        Parameters:
        threshold_db (float): The peak threshold in dB.
        """
        self.instrument.write(f":CALC:MARK:PEAK:THR {threshold_db}")

    def get_peak_threshold(self) -> float:
        """
        Queries the peak threshold in dB.
        Returns:
        float: The peak threshold in dB.
        """
        response = self.instrument.query(":CALC:MARK:PEAK:THR?")
        return float(response)

#Trace Math
#TODO: Add description
    def enable_trace_math(self, enable: bool):
        """
        Enables or disables the trace math function.
        Parameters:
        enable (bool): True to enable trace math, False to disable.
        """
        self.instrument.write(f":CALC:MATH:STAT {1 if enable else 0}")

    def is_trace_math_enabled(self) -> bool:
        """
        Queries if the trace math function is enabled.
        Returns:
        bool: True if enabled, False otherwise.
        """
        response = self.instrument.query(":CALC:MATH:STAT?")
        return response == 1

    def set_trace_math_first_operand(self, trace_index: int):
        """
        Specifies the first operand trace in the selected trace math function.
        Parameters:
        trace_index (int): The index of the first operand trace (1-6).
        """
        if not (1 <= trace_index <= 6):
            raise ValueError("Invalid trace index. Must be between 1 and 6.")
        self.instrument.write(f":CALC:MATH:FIRST {trace_index}")

    def get_trace_math_first_operand(self) -> int:
        """
        Queries the first operand trace in the selected trace math function.
        Returns:
        int: The index of the first operand trace (1-6).
        """
        response = self.instrument.query(":CALC:MATH:FIRST?")
        return int(response)

    def set_trace_math_second_operand(self, trace_index: int):
        """
        Specifies the second operand trace in the selected trace math function.
        Parameters:
        trace_index (int): The index of the second operand trace (1-6).
        """
        if not (1 <= trace_index <= 6):
            raise ValueError("Invalid trace index. Must be between 1 and 6.")
        self.instrument.write(f":CALC:MATH:SECOND {trace_index}")

    def get_trace_math_second_operand(self) -> int:
        """
        Queries the second operand trace in the selected trace math function.
        Returns:
        int: The index of the second operand trace (1-6).
        """
        response = self.instrument.query(":CALC:MATH:SECOND?")
        return int(response)

    def set_trace_math_result_trace(self, trace_index: int):
        """
        Specifies the result trace in the selected trace math function.
        Parameters:
        trace_index (int): The index of the result trace (1-6).
        """
        if not (1 <= trace_index <= 6):
            raise ValueError("Invalid trace index. Must be between 1 and 6.")
        self.instrument.write(f":CALC:MATH:RES {trace_index}")

    def get_trace_math_result_trace(self) -> int:
        """
        Queries the result trace in the selected trace math function.
        Returns:
        int: The index of the result trace (1-6).
        """
        response = self.instrument.query(":CALC:MATH:RES?")
        return int(response)

    def set_trace_math_operation(self, operation: str):
        """
        Specifies the trace math function.
        Parameters:
        operation (str): Allowed values are 'PDIFF', 'PSUM', 'LOFFSET', 'LDIFF'.
        """
        valid_operations = {"PDIFF", "PSUM", "LOFFSET", "LDIFF"}
        operation_upper = operation.upper()
        if operation_upper not in valid_operations:
            raise ValueError(f"Invalid operation: '{operation}'. Must be one of {valid_operations}.")
        self.instrument.write(f":CALC:MATH:OP {operation_upper}")

    def get_trace_math_operation(self) -> str:
        """
        Queries the trace math function.
        Returns:
        str: The trace math function ('PDIFF', 'PSUM', 'LOFFSET', 'LDIFF').
        """
        response = self.instrument.query(":CALC:MATH:OP?")
        return response.upper()

    def set_trace_math_offset(self, offset_value: float):
        """
        Specifies the offset to use in the logarithm trace math functions.
        Parameters:
        offset_value (float): The offset value in dB.
        """
        self.instrument.write(f":CALC:MATH:OFFS {offset_value}")

    def get_trace_math_offset(self) -> float:
        """
        Queries the offset used in the logarithm trace math functions.
        Returns:
        float: The offset value in dB.
        """
        response = self.instrument.query(":CALC:MATH:OFFS?")
        return float(response)

#Channel Power
    """These commands control the channel power measurement in the Spike software. 
    Through these commands you can configure a main channel and up to 5 adjacent 
    channels and simultaneously measure channel and adjacent channel power."""
    def enable_channel_power(self, enable: bool):
        """
        Enables or disables the channel power measurement.
        Parameters:
        enable (bool): True to enable channel power measurement, False to disable.
        """
        self.instrument.write(f":SENS:CHP:STAT {1 if enable else 0}")

    def is_channel_power_enabled(self) -> bool:
        """
        Queries if the channel power measurement is enabled.
        Returns:
        bool: True if enabled, False otherwise.
        """
        response = self.instrument.query(":SENS:CHP:STAT?")
        return response == 1

    def set_channel_power_trace(self, trace_index: int):
        """
        Selects which trace the channel power measurement is performed on.
        Parameters:
        trace_index (int): The index of the trace (1-6).
        """
        if not (1 <= trace_index <= 6):
            raise ValueError("Invalid trace index. Must be between 1 and 6.")
        self.instrument.write(f":SENS:CHP:TRAC {trace_index}")

    def get_channel_power_trace(self) -> int:
        """
        Queries which trace the channel power measurement is performed on.
        Returns:
        int: The index of the trace (1-6).
        """
        response = self.instrument.query(":SENS:CHP:TRAC?")
        return int(response)

    def set_channel_power_width(self, width_hz: float):
        """
        Specifies the width of the main channel power measurement as a frequency.
        Parameters:
        width_hz (float): The width in Hz.
        """
        self.instrument.write(f":SENS:CHP:WIDT {width_hz}")

    def get_channel_power_width(self) -> float:
        """
        Queries the width of the main channel power measurement as a frequency.
        Returns:
        float: The width in Hz.
        """
        response = self.instrument.query(":SENS:CHP:WIDT?")
        return float(response)

    def enable_adjacent_channel_power(self, channel_index: int, enable: bool):
        """
        Enables or disables the measurement of an adjacent channel.
        Parameters:
        channel_index (int): The index of the adjacent channel (1-5).
        enable (bool): True to enable measurement, False to disable.
        """
        if not (1 <= channel_index <= 5):
            raise ValueError("Invalid adjacent channel index. Must be between 1 and 5.")
        self.instrument.write(f":SENS:CHP:CHAN:STAT {channel_index},{1 if enable else 0}")

    def is_adjacent_channel_power_enabled(self, channel_index: int) -> bool:
        """
        Queries if the measurement of an adjacent channel is enabled.
        Parameters:
        channel_index (int): The index of the adjacent channel (1-5).
        Returns:
        bool: True if enabled, False otherwise.
        """
        if not (1 <= channel_index <= 5):
            raise ValueError("Invalid adjacent channel index. Must be between 1 and 5.")
        response = self.instrument.query(f":SENS:CHP:CHAN:STAT? {channel_index}")
        return response == 1

    def set_adjacent_channel_offset(self, channel_index: int, offset_hz: float):
        """
        Specifies the offset from the center of an adjacent channel.
        Parameters:
        channel_index (int): The index of the adjacent channel (1-5).
        offset_hz (float): The offset in Hz.
        """
        if not (1 <= channel_index <= 5):
            raise ValueError("Invalid adjacent channel index. Must be between 1 and 5.")
        self.instrument.write(f":SENS:CHP:CHAN:OFFS {channel_index},{offset_hz}")

    def get_adjacent_channel_offset(self, channel_index: int) -> float:
        """
        Queries the offset from the center of an adjacent channel.
        Parameters:
        channel_index (int): The index of the adjacent channel (1-5).
        Returns:
        float: The offset in Hz.
        """
        if not (1 <= channel_index <= 5):
            raise ValueError("Invalid adjacent channel index. Must be between 1 and 5.")
        response = self.instrument.query(f":SENS:CHP:CHAN:OFFS? {channel_index}")
        return float(response)

    def set_adjacent_channel_width(self, channel_index: int, width_hz: float):
        """
        Specifies the width of an adjacent channel.
        Parameters:
        channel_index (int): The index of the adjacent channel (1-5).
        width_hz (float): The width in Hz.
        """
        if not (1 <= channel_index <= 5):
            raise ValueError("Invalid adjacent channel index. Must be between 1 and 5.")
        self.instrument.write(f":SENS:CHP:CHAN:WIDT {channel_index},{width_hz}")

    def get_adjacent_channel_width(self, channel_index: int) -> float:
        """
        Queries the width of an adjacent channel.
        Parameters:
        channel_index (int): The index of the adjacent channel (1-5).
        Returns:
        float: The width in Hz.
        """
        if not (1 <= channel_index <= 5):
            raise ValueError("Invalid adjacent channel index. Must be between 1 and 5.")
        response = self.instrument.query(f":SENS:CHP:CHAN:WIDT? {channel_index}")
        return float(response)

    def get_main_channel_power(self) -> float:
        """
        Queries the channel power of the main channel.
        Returns:
        float: The channel power in dBm.
        """
        response = self.instrument.query(":SENS:CHP:CHP?")
        return float(response)

    def get_adjacent_channel_power_lower(self) -> float:
        """
        Queries the lower adjacent channel power.
        Returns:
        float: The lower adjacent channel power in dBm.
        """
        response = self.instrument.query(":SENS:CHP:CHP:LOW?")
        return float(response)

    def get_adjacent_channel_power_upper(self) -> float:
        """
        Queries the upper adjacent channel power.
        Returns:
        float: The upper adjacent channel power in dBm.
        """
        response = self.instrument.query(":SENS:CHP:CHP:UPP?")
        return float(response)

    def get_adjacent_channel_ac_power_lower(self) -> float:
        """
        Queries the lower adjacent channel AC power.
        Returns:
        float: The lower adjacent channel AC power in dBc.
        """
        response = self.instrument.query(":SENS:CHP:ACP:LOW?")
        return float(response)

    def get_adjacent_channel_ac_power_upper(self) -> float:
        """
        Queries the upper adjacent channel AC power.
        Returns:
        float: The upper adjacent channel AC power in dBc.
        """
        response = self.instrument.query(":SENS:CHP:ACP:UPP?")

        return float(response)
# Occupied Bandwidth Controls
    """These commands allow you to configure the occupied bandwidth 
    measurement in the Spike software"""
    def enable_occupied_bandwidth(self, enable: bool):
        """
        Enables or disables the occupied bandwidth measurement.
        Parameters:
        enable (bool): True to enable, False to disable.
        """
        self.instrument.write(f":SENS:OBW:STAT {1 if enable else 0}")

    def is_occupied_bandwidth_enabled(self) -> bool:
        """
        Queries if the occupied bandwidth measurement is enabled.
        Returns:
        bool: True if enabled, False otherwise.
        """
        response = self.instrument.query(":SENS:OBW:STAT?")
        return response == 1

    def set_occupied_bandwidth_trace(self, trace_index: int):
        """
        Specifies which trace the occupied bandwidth measurement is performed on.
        Parameters:
        trace_index (int): The index of the trace (1-6).
        """
        if not (1 <= trace_index <= 6):
            raise ValueError("Invalid trace index. Must be between 1 and 6.")
        self.instrument.write(f":SENS:OBW:TRAC {trace_index}")

    def get_occupied_bandwidth_trace(self) -> int:
        """
        Queries which trace the occupied bandwidth measurement is performed on.
        Returns:
        int: The index of the trace (1-6).
        """
        response = self.instrument.query(":SENS:OBW:TRAC?")
        return int(response)

    def set_occupied_bandwidth_percent(self, percent: float):
        """
        Specifies the percentage of the total energy of the sweep for the occupied bandwidth measurement.
        Parameters:
        percent (float): The percentage value.
        """
        self.instrument.write(f":SENS:OBW:PERC {percent}")

    def get_occupied_bandwidth_percent(self) -> float:
        """
        Queries the percentage of the total energy of the sweep for the occupied bandwidth measurement.
        Returns:
        float: The percentage value.
        """
        response = self.instrument.query(":SENS:OBW:PERC?")
        return float(response)

    def get_occupied_bandwidth(self) -> float:
        """
        Queries the bandwidth of the occupied bandwidth measurement as Hz.
        Returns:
        float: The bandwidth in Hz.
        """
        response = self.instrument.query(":SENS:OBW:OBW?")
        return float(response)

    def get_occupied_bandwidth_center_frequency(self) -> float:
        """
        Queries the center frequency of the occupied bandwidth measurement as Hz.
        Returns:
        float: The center frequency in Hz.
        """
        response = self.instrument.query(":SENS:OBW:CENT?")
        return float(response)

    def get_occupied_bandwidth_power(self) -> float:
        """
        Queries the power of the occupied bandwidth measurement.
        Returns:
        float: The power value.
        """
        response = self.instrument.query(":SENS:OBW:POW?")
        return float(response)

#Intermodulation Distortion (IMD) Controls
    """These commands allow you to configure the intermodulation distortion measurement in the Spike software."""
    def enable_intermodulation_distortion(self, enable: bool):
        """
        Enables or disables the intermodulation distortion measurement.
        Parameters:
        enable (bool): True to enable, False to disable.
        """
        self.instrument.write(f":SENS:IMD:STAT {1 if enable else 0}")

    def is_intermodulation_distortion_enabled(self) -> bool:
        """
        Queries if the intermodulation distortion measurement is enabled.
        Returns:
        bool: True if enabled, False otherwise.
        """
        response = self.instrument.query(":SENS:IMD:STAT?")
        return response == 1

    def get_intermodulation_frequency(self, product: str) -> float:
        """
        Returns the frequency of the specified intermodulation product.
        Parameters:
        product (str): 'F1', 'F2', 'IM3L', or 'IM3U'.
        Returns:
        float: The frequency in Hz.
        """
        response = self.instrument.query(f":SENS:IMD:FREQ? {product.upper()}")
        return float(response)

    def get_intermodulation_power(self, product: str) -> float:
        """
        Returns the tonal power in dBm of the specified intermodulation product.
        Parameters:
        product (str): 'F1', 'F2', 'IM3L', or 'IM3U'.
        Returns:
        float: The power in dBm.
        """
        response = self.instrument.query(f":SENS:IMD:TPOW? {product.upper()}")
        return float(response)

    def get_intermodulation_power_difference(self, product: str) -> float:
        """
        Returns the tonal power difference in dBc between the specified third order product and its corresponding first order product.
        Parameters:
        product (str): 'IM3L' or 'IM3U'.
        Returns:
        float: The power difference in dBc.
        """
        response = self.instrument.query(f":SENS:IMD:TPOW:DIFF? {product.upper()}")
        return float(response)

    def get_intermodulation_toi(self, product: str) -> float:
        """
        Returns the third-order intercept (TOI) in dBm of the specified third order product.
        Parameters:
        product (str): 'IM3L' or 'IM3U'.
        Returns:
        float: The TOI in dBm.
        """
        response = self.instrument.query(f":SENS:IMD:TOI? {product.upper()}")
        return float(response)
    
# Peak Table Controls
    """These commands control the Peak Table display panel in Swept Analysis mode."""
    def enable_peak_table(self, enable: bool):
        """
        Enables or disables the Peak Table panel.
        Parameters:
        enable (bool): True to enable, False to disable.
        """
        self.instrument.write(f":SENS:PEAK:TABL:STAT {1 if enable else 0}")

    def is_peak_table_enabled(self) -> bool:
        """
        Queries if the Peak Table panel is enabled.
        Returns:
        bool: True if enabled, False otherwise.
        """
        response = self.instrument.query(":SENS:PEAK:TABL:STATe?")
        return response == 1

    def set_peak_table_trace(self, trace_index: int):
        """
        Selects which trace the peak measurements are performed on.
        Parameters:
        trace_index (int): The index of the trace.
        """
        self.instrument.write(f":SENS:PEAK:TABL:TRAC {trace_index}")

    def get_peak_table_trace(self) -> int:
        """
        Queries which trace the peak measurements are performed on.
        Returns:
        int: The trace index.
        """
        response = self.instrument.query(":SENS:PEAK:TABL:TRACe?")
        return int(response)

    def set_peak_table_threshold(self, threshold_dbm: float):
        """
        Specifies the peak threshold in dBm.
        Parameters:
        threshold_dbm (float): The threshold in dBm.
        """
        self.instrument.write(f":SENS:PEAK:TABL:THR {threshold_dbm}")

    def get_peak_table_threshold(self) -> float:
        """
        Queries the peak threshold in dBm.
        Returns:
        float: The threshold in dBm.
        """
        response = self.instrument.query(":SENS:PEAK:TABL:THR?")
        return float(response)

    def set_peak_table_excursion(self, excursion_db: float):
        """
        Specifies the peak excursion in dB.
        Parameters:
        excursion_db (float): The excursion in dB.
        """
        self.instrument.write(f":SENS:PEAK:TABL:EXC {excursion_db}")

    def get_peak_table_excursion(self) -> float:
        """
        Queries the peak excursion in dB.
        Returns:
        float: The excursion in dB.
        """
        response = self.instrument.query(":SENS:PEAK:TABL:EXC?")
        return float(response)

    def set_peak_table_sort(self, sort_type: str):
        """
        Specifies the sort order of the table. Allowed values: 'FREQUENCY', 'AMPLITUDE'.
        Parameters:
        sort_type (str): The sort order.
        """
        valid_types = {"FREQUENCY", "AMPLITUDE"}
        sort_type_upper = sort_type.upper()
        if sort_type_upper not in valid_types:
            raise ValueError(f"Invalid sort type: '{sort_type}'. Must be 'FREQUENCY' or 'AMPLITUDE'.")
        self.instrument.write(f":SENS:PEAK:TABL:SORT {sort_type_upper}")

    def get_peak_table_sort(self) -> str:
        """
        Queries the sort order of the table.
        Returns:
        str: The sort order ('FREQUENCY' or 'AMPLITUDE').
        """
        response = self.instrument.query(":SENS:PEAK:TABL:SORT?")
        return response.upper()

    def get_peak_table_count(self) -> int:
        """
        Returns the number of peaks in the table.
        Returns:
        int: The number of peaks.
        """
        response = self.instrument.query(":SENS:PEAK:TABL:COUN?")
        return int(response)

    def set_peak_table_max(self, max_peaks: int):
        """
        Specifies the maximum number of peaks that can appear in the table [0, 99].
        Parameters:
        max_peaks (int): The maximum number of peaks.
        """
        self.instrument.write(f":SENS:PEAK:TABL:MAX {max_peaks}")

    def get_peak_table_max(self) -> int:
        """
        Queries the maximum number of peaks that can appear in the table.
        Returns:
        int: The maximum number of peaks.
        """
        response = self.instrument.query(":SENS:PEAK:TABL:MAX?")
        return int(response)

    def get_peak_table_frequency(self, peak_index: int) -> float:
        """
        Returns the frequency of the specified peak.
        Parameters:
        peak_index (int): The peak index.
        Returns:
        float: The frequency in Hz.
        """
        response = self.instrument.query(f":SENS:PEAK:TABL:FREQ? {peak_index}")
        return float(response)

    def get_peak_table_amplitude(self, peak_index: int) -> float:
        """
        Returns the amplitude of the specified peak.
        Parameters:
        peak_index (int): The peak index.
        Returns:
        float: The amplitude in dBm.
        """
        response = self.instrument.query(f":SENS:PEAK:TABL:AMPL? {peak_index}")
        return float(response)

    def get_peak_table_frequency_delta(self, peak_index: int) -> float:
        """
        Returns the frequency difference between the specified peak and the first peak in the list.
        Parameters:
        peak_index (int): The peak index.
        Returns:
        float: The frequency delta in Hz.
        """
        response = self.instrument.query(f":SENS:PEAK:TABL:FREQ:DELT? {peak_index}")
        return float(response)

    def get_peak_table_amplitude_delta(self, peak_index: int) -> float:
        """
        Returns the amplitude difference between the specified peak and the first peak in the list.
        Parameters:
        peak_index (int): The peak index.
        Returns:
        float: The amplitude delta in dB.
        """
        response = self.instrument.query(f":SENS:PEAK:TABL:AMPL:DELT? {peak_index}")
        return response
    
    def set_decimate_type(self, decimate_type: str):
        """
        Selects the decimation type for sweep recording using shortened SCPI.
        Parameters:
        decimate_type (str): The decimation type. Must be 'TIME' or 'COUNT'.
        """
        valid_types = {"TIME", "COUNT"}
        decimate_type_upper = decimate_type.upper()
        if decimate_type_upper not in valid_types:
            raise ValueError(f"Invalid decimation type: '{decimate_type}'. Must be 'TIME' or 'COUNT'.")
        self.instrument.write(f":SENS:REC:SWE:DEC:TYPE {decimate_type_upper}")

    def get_decimate_type(self) -> str:
        """
        Queries the decimation type for sweep recording using shortened SCPI.
        Returns:
        str: The decimation type ('TIME' or 'COUNT').
        """
        response = self.instrument.query(":SENS:REC:SWE:DEC:TYPE?")
        return response.strip().upper()

    def set_decimate_time(self, time_seconds: float):
        """
        Specifies the amount of time by which to decimate using shortened SCPI.
        Parameters:
        time_seconds (float): The decimation time in seconds.
        """
        self.instrument.write(f":SENS:REC:SWE:DEC:TIME {time_seconds}")

    def get_decimate_time(self) -> float:
        """
        Queries the decimation time for sweep recording using shortened SCPI.
        Returns:
        float: The decimation time in seconds.
        """
        response = self.instrument.query(":SENS:REC:SWE:DEC:TIME?")
        return float(response)

    def set_decimate_count(self, count: int):
        """
        Specifies the number of sweeps by which to decimate using shortened SCPI.
        Parameters:
        count (int): The number of sweeps.
        """
        self.instrument.write(f":SENS:REC:SWE:DEC:COUNt {count}")

    def get_decimate_count(self) -> int:
        """
        Queries the decimation count for sweep recording using shortened SCPI.
        Returns:
        int: The decimation count.
        """
        response = self.instrument.query(":SENS:REC:SWE:DEC:COUN?")
        return int(response)

    def set_decimate_detector(self, detector_type: str):
        """
        Selects the decimation detector using shortened SCPI.
        Parameters:
        detector_type (str): The detector type. Must be 'AVERAGE' or 'MAX'.
        """
        valid_types = {"AVERAGE", "MAX"}
        detector_type_upper = detector_type.upper()
        if detector_type_upper not in valid_types:
            raise ValueError(f"Invalid detector type: '{detector_type}'. Must be 'AVERAGE' or 'MAX'.")
        self.instrument.write(f":SENS:REC:SWE:DEC:DETector {detector_type_upper}")

    def get_decimate_detector(self) -> str:
        """
        Queries the decimation detector for sweep recording using shortened SCPI.
        Returns:
        str: The detector type ('AVERAGE' or 'MAX').
        """
        response = self.instrument.query(":SENS:REC:SWE:DEC:DET?")
        return response.strip().upper()

    def enable_channelizer(self, enable: bool):
        """
        Toggles decimation in frequency with the channelizer using shortened SCPI.
        Parameters:
        enable (bool): True to enable, False to disable.
        """
        # Use integer 1 for ON, 0 for OFF
        self.instrument.write(f":SENS:REC:SWE:CHAN:STATe {1 if enable else 0}")

    def is_channelizer_enabled(self) -> bool:
        """
        Queries if the channelizer is enabled for sweep recording using shortened SCPI.
        Returns:
        bool: True if enabled, False otherwise.
        """
        response = self.instrument.query(":SENS:REC:SWE:CHAN:STAT?")
        return int(response) == 1

    def set_channelizer_center_frequency(self, frequency_hz: float):
        """
        Specifies the center frequency of the channelizer using shortened SCPI.
        Parameters:
        frequency_hz (float): The center frequency in Hz.
        """
        self.instrument.write(f":SENS:REC:SWE:CHAN:CENTer {frequency_hz}")

    def get_channelizer_center_frequency(self) -> float:
        """
        Queries the center frequency of the channelizer using shortened SCPI.
        Returns:
        float: The center frequency in Hz.
        """
        response = self.instrument.query(":SENS:REC:SWE:CHAN:CENT?")
        return float(response)

    def set_channelizer_spacing(self, spacing_hz: float):
        """
        Specifies the channel width for the channelizer using shortened SCPI.
        Parameters:
        spacing_hz (float): The channel width in Hz.
        """
        self.instrument.write(f":SENS:REC:SWE:CHAN:SPACing {spacing_hz}")

    def get_channelizer_spacing(self) -> float:
        """
        Queries the channel width for the channelizer using shortened SCPI.
        Returns:
        float: The channel width in Hz.
        """
        response = self.instrument.query(":SENS:REC:SWE:CHAN:SPAC?")
        return float(response)

    def set_channelizer_units(self, units: str):
        """
        Selects the output units of the channel power measurement using shortened SCPI.
        Parameters:
        units (str): The units. Must be 'DBM' or 'DBMHZ'.
        """
        valid_units = {"DBM", "DBMHZ"}
        units_upper = units.upper()
        if units_upper not in valid_units:
            raise ValueError(f"Invalid units: '{units}'. Must be 'DBM' or 'DBMHZ'.")
        self.instrument.write(f":SENS:REC:SWE:CHAN:UNITS {units_upper}")

    def get_channelizer_units(self) -> str:
        """
        Queries the output units of the channel power measurement using shortened SCPI.
        Returns:
        str: The units ('DBM' or 'DBMHZ').
        """
        response = self.instrument.query(":SENS:REC:SWE:CHAN:UNITS?")
        return response.strip().upper()

    def get_recording_progress(self) -> float:
        """
        Returns the progress of the current decimation in time as a floating point
        percentage between 0 and 100 using shortened SCPI.
        Returns:
        float: The progress percentage.
        """
        response = self.instrument.query(":SENS:REC:SWE:PROG?")
        return float(response)

    def get_sweep_count(self) -> int:
        """
        Returns the integer number of sweeps saved so far using shortened SCPI.
        Returns:
        int: The number of sweeps saved.
        """
        response = self.instrument.query(":SENS:REC:SWE:COUN?")
        return int(response)

    def get_file_size(self) -> float:
        """
        Returns the size of the recording file in bytes as a floating point number using shortened SCPI.
        Returns:
        float: The file size in bytes.
        """
        response = self.instrument.query(":SENS:REC:SWE:FILE:SIZE?")
        return float(response)

    def set_file_prefix(self, prefix: str):
        """
        Specifies the file prefix for recordings using shortened SCPI.
        Parameters:
        prefix (str): The file prefix string.
        """
        self.instrument.write(f":SENS:REC:SWE:FILE:PRE '{prefix}'")

    def get_file_prefix(self) -> str:
        """
        Queries the file prefix for recordings using shortened SCPI.
        Returns:
        str: The file prefix string.
        """
        response = self.instrument.query(":SENS:REC:SWE:FILE:PRE?")
        return response.strip().strip("'") # Remove potential quotes from response

    def set_file_directory(self, directory_path: str):
        """
        Specifies the directory in which to save recordings using shortened SCPI.
        If the specified directory does not exist, then no change is made.
        Parameters:
        directory_path (str): The directory path string.
        """
        self.instrument.write(f":SENS:REC:SWE:FILE:DIR '{directory_path}'")

    def get_file_directory(self) -> str:
        """
        Queries the directory in which recordings are saved using shortened SCPI.
        Returns:
        str: The directory path string.
        """
        response = self.instrument.query(":SENS:REC:SWE:FILE:DIR?")
        return response.strip().strip("'") # Remove potential quotes from response

    def start_recording(self):
        """
        Starts sweep recording using shortened SCPI.
        """
        self.instrument.write(":SENS:REC:SWE:STAR")

    def stop_recording(self):
        """
        Stops sweep recording using shortened SCPI.
        """
        self.instrument.write(":SENS:REC:SWE:STOP")

    def is_recording_active(self) -> bool:
        """
        Queries if the instrument is actively recording using shortened SCPI.
        Returns:
        bool: True if actively recording, False otherwise.
        """
        response = self.instrument.query(":SENS:REC:SWE:STAT?")
        # The document says "Returns true if actively recording."
        # Assuming 1 for true, 0 for false based on other boolean queries.
        return int(response) == 1
    
    # --- Zero-Span Capture Settings ---

def set_zero_span_reference_level(self, amplitude_dbm: float):
    """
    Sets the reference level for zero-span capture.
    Parameters:
    amplitude_dbm (float): The reference level in dBm.
    """
    self.instrument.write(f":SENS:ZS:CAP:RLEV {amplitude_dbm}")

def get_zero_span_reference_level(self) -> float:
    """
    Queries the current reference level for zero-span capture.
    Returns:
    float: The reference level in dBm.
    """
    response = self.instrument.query(":SENS:ZS:CAP:RLEV?")
    return float(response)

def set_zero_span_center_frequency(self, frequency_hz: float):
    """
    Sets the center frequency for zero-span capture.
    Parameters:
    frequency_hz (float): The center frequency in Hz.
    """
    self.instrument.write(f":SENS:ZS:CAP:CENT {frequency_hz}")

def get_zero_span_center_frequency(self, limit: str = None) -> float:
    """
    Queries the current center frequency for zero-span capture.
    Optionally pass 'MIN' or 'MAX' to query limits.
    Parameters:
    limit (str): 'MIN' or 'MAX' (optional).
    Returns:
    float: The center frequency in Hz.
    """
    if limit:
        limit_upper = limit.upper()
        if limit_upper not in {"MIN", "MAX"}:
            raise ValueError("limit must be 'MIN' or 'MAX'")
        response = self.instrument.query(f":SENS:ZS:CAP:CENT? {limit_upper}")
    else:
        response = self.instrument.query(":SENS:ZS:CAP:CENT?")
    return float(response)

def set_zero_span_center_step(self, step_hz: float):
    """
    Sets the step amount the center frequency changes by for zero-span capture.
    Parameters:
    step_hz (float): The step size in Hz.
    """
    self.instrument.write(f":SENS:ZS:CAP:CENT:STEP {step_hz}")

def get_zero_span_center_step(self) -> float:
    """
    Queries the center frequency step size for zero-span capture.
    Returns:
    float: The step size in Hz.
    """
    response = self.instrument.query(":SENS:ZS:CAP:CENT:STEP?")
    return float(response)

def set_zero_span_sample_rate(self, sample_rate_hz: float):
    """
    Sets the sample rate for zero-span capture.
    Parameters:
    sample_rate_hz (float): The sample rate in Hz.
    """
    self.instrument.write(f":SENS:ZS:CAP:SRATE {sample_rate_hz}")

def get_zero_span_sample_rate(self) -> float:
    """
    Queries the sample rate for zero-span capture.
    Returns:
    float: The sample rate in Hz.
    """
    response = self.instrument.query(":SENS:ZS:CAP:SRATE?")
    return float(response)

def set_zero_span_if_bandwidth(self, bandwidth_hz: float):
    """
    Sets the IF bandwidth for zero-span capture.
    Parameters:
    bandwidth_hz (float): The IF bandwidth in Hz.
    """
    self.instrument.write(f":SENS:ZS:CAP:IFBW {bandwidth_hz}")

def get_zero_span_if_bandwidth(self) -> float:
    """
    Queries the IF bandwidth for zero-span capture.
    Returns:
    float: The IF bandwidth in Hz.
    """
    response = self.instrument.query(":SENS:ZS:CAP:IFBW?")
    return float(response)

def enable_zero_span_if_bandwidth_auto(self, enable: bool):
    """
    Enables or disables automatic IF bandwidth selection for zero-span capture.
    Parameters:
    enable (bool): True to enable, False to disable.
    """
    self.instrument.write(f":SENS:ZS:CAP:IFBW:AUTO {1 if enable else 0}")

def is_zero_span_if_bandwidth_auto_enabled(self) -> bool:
    """
    Queries if automatic IF bandwidth selection is enabled for zero-span capture.
    Returns:
    bool: True if enabled, False otherwise.
    """
    response = self.instrument.query(":SENS:ZS:CAP:IFBW:AUTO?")
    return int(response) == 1

def set_zero_span_sweep_time(self, sweep_time_s: float):
    """
    Sets the sweep time for zero-span capture.
    Parameters:
    sweep_time_s (float): The sweep time in seconds.
    """
    self.instrument.write(f":SENS:ZS:CAP:SWEEP:TIME {sweep_time_s}")

def get_zero_span_sweep_time(self) -> float:
    """
    Queries the sweep time for zero-span capture.
    Returns:
    float: The sweep time in seconds.
    """
    response = self.instrument.query(":SENS:ZS:CAP:SWEEP:TIME?")
    return float(response)

# --- Zero-Span Trigger Settings ---

def set_zero_span_trigger_source(self, source: str):
    """
    Sets the trigger source for zero-span mode.
    Parameters:
    source (str): Allowed values are 'IMMEDIATE', 'IF', 'EXTERNAL', 'FMT'.
    """
    valid_sources = {"IMMEDIATE", "IF", "EXTERNAL", "FMT"}
    source_upper = source.upper()
    if source_upper not in valid_sources:
        raise ValueError(f"Invalid trigger source: '{source}'. Must be one of {valid_sources}.")
    self.instrument.write(f":TRIG:ZS:SOUR {source_upper}")

def get_zero_span_trigger_source(self) -> str:
    """
    Queries the trigger source for zero-span mode.
    Returns:
    str: The trigger source.
    """
    response = self.instrument.query(":TRIG:ZS:SOUR?")
    return response.strip().upper()

def set_zero_span_trigger_slope(self, slope: str):
    """
    Sets the trigger slope for zero-span mode.
    Parameters:
    slope (str): Allowed values are 'POSITIVE', 'NEGATIVE'.
    """
    valid_slopes = {"POSITIVE", "NEGATIVE", "POS", "NEG"}
    slope_upper = slope.upper()
    if slope_upper not in valid_slopes:
        raise ValueError(f"Invalid trigger slope: '{slope}'. Must be 'POSITIVE' or 'NEGATIVE'.")
    self.instrument.write(f":TRIG:ZS:SLOP {slope_upper}")

def get_zero_span_trigger_slope(self) -> str:
    """
    Queries the trigger slope for zero-span mode.
    Returns:
    str: The trigger slope.
    """
    response = self.instrument.query(":TRIG:ZS:SLOP?")
    return response.strip().upper()

def set_zero_span_trigger_if_level(self, amplitude_dbm: float):
    """
    Sets the trigger level for IF trigger in zero-span mode.
    Parameters:
    amplitude_dbm (float): The trigger level in dBm.
    """
    self.instrument.write(f":TRIG:ZS:IF:LEV {amplitude_dbm}")

def get_zero_span_trigger_if_level(self) -> float:
    """
    Queries the trigger level for IF trigger in zero-span mode.
    Returns:
    float: The trigger level in dBm.
    """
    response = self.instrument.query(":TRIG:ZS:IF:LEV?")
    return float(response)

def set_zero_span_trigger_position(self, position_percent: float):
    """
    Sets the trigger delay (position) for zero-span mode.
    Parameters:
    position_percent (float): The percentage of samples before the trigger.
    """
    self.instrument.write(f":TRIG:ZS:POS {position_percent}")

def get_zero_span_trigger_position(self) -> float:
    """
    Queries the trigger delay (position) for zero-span mode.
    Returns:
    float: The percentage of samples before the trigger.
    """
    response = self.instrument.query(":TRIG:ZS:POS?")
    return float(response)

# --- Fetch Zero-Span Results ---

def fetch_zero_span_iq_data(self) -> str:
    """
    Fetches I/Q data from zero-span capture in ASCII or binary format.
    Returns:
    str: The I/Q data as a comma-separated string (ASCII) or binary data.
    """
    return self.instrument.query(":FETC:ZS? 1")

def fetch_zero_span_data_length(self) -> int:
    """
    Fetches the length (number of complex I/Q points) of zero-span capture data.
    Returns:
    int: The number of complex I/Q points.
    """
    response = self.instrument.query(":FETC:ZS? 2")
    return int(response)

def fetch_zero_span_average_power(self) -> float:
    """
    Fetches the average power as reported on the AM vs Time plot for zero-span capture.
    Returns:
    float: The average power in dBm.
    """
    response = self.instrument.query(":FETC:ZS? 10")
    return float(response)

# --- Scalar Network Analysis (SNA) Sweep Configuration ---

def set_sna_sweep_points(self, points: int):
    """
    Specifies the suggested sweep size for Scalar Network Analysis.
    Parameters:
    points (int): The number of sweep points.
    """
    self.instrument.write(f":SENS:NA:SWE:POIN {points}")

def get_sna_sweep_points(self) -> int:
    """
    Queries the suggested sweep size for Scalar Network Analysis.
    Returns:
    int: The number of sweep points.
    """
    response = self.instrument.query(":SENS:NA:SWE:POIN?")
    return int(response)

def set_sna_sweep_type(self, sweep_type: str):
    """
    Specifies whether an active or passive device is being measured.
    Parameters:
    sweep_type (str): Allowed values are 'PASSIVE', 'ACTIVE'.
    """
    valid_types = {"PASSIVE", "ACTIVE"}
    sweep_type_upper = sweep_type.upper()
    if sweep_type_upper not in valid_types:
        raise ValueError(f"Invalid sweep type: '{sweep_type}'. Must be 'PASSIVE' or 'ACTIVE'.")
    self.instrument.write(f":SENS:NA:SWE:TYPE {sweep_type_upper}")

def get_sna_sweep_type(self) -> str:
    """
    Queries whether an active or passive device is being measured.
    Returns:
    str: The sweep type ('PASSIVE' or 'ACTIVE').
    """
    response = self.instrument.query(":SENS:NA:SWE:TYPE?")
    return response.strip().upper()

def enable_sna_high_range(self, enable: bool):
    """
    Enables or disables high range optimization for SNA sweep.
    Parameters:
    enable (bool): True to enable, False to disable.
    """
    self.instrument.write(f":SENS:NA:SWE:HRAN {1 if enable else 0}")

def is_sna_high_range_enabled(self) -> bool:
    """
    Queries if high range optimization is enabled for SNA sweep.
    Returns:
    bool: True if enabled, False otherwise.
    """
    response = self.instrument.query(":SENS:NA:SWE:HRAN?")
    return response == 1

def set_sna_view_scale(self, scale_type: str):
    """
    Specifies the view scale for SNA. Allowed values: 'LOG', 'VSWR'.
    Parameters:
    scale_type (str): The scale type.
    """
    valid_types = {"LOG", "VSWR"}
    scale_type_upper = scale_type.upper()
    if scale_type_upper not in valid_types:
        raise ValueError(f"Invalid scale type: '{scale_type}'. Must be 'LOG' or 'VSWR'.")
    self.instrument.write(f":SENS:NA:VIEW:SCAL {scale_type_upper}")

def get_sna_view_scale(self) -> str:
    """
    Queries the view scale for SNA.
    Returns:
    str: The scale type ('LOG' or 'VSWR').
    """
    response = self.instrument.query(":SENS:NA:VIEW:SCAL?")
    return response.strip().upper()

def set_sna_view_reference_level(self, ref_level: float):
    """
    Specifies the plot reference level for SNA.
    Parameters:
    ref_level (float): The reference level as a double.
    """
    self.instrument.write(f":SENS:NA:VIEW:RLEV {ref_level}")

def get_sna_view_reference_level(self) -> float:
    """
    Queries the plot reference level for SNA.
    Returns:
    float: The reference level.
    """
    response = self.instrument.query(":SENS:NA:VIEW:RLEV?")
    return float(response)

def set_sna_view_division(self, division: float):
    """
    Specifies the plot division height for SNA.
    Parameters:
    division (float): The division height as a double.
    """
    self.instrument.write(f":SENS:NA:VIEW:DIV {division}")

def get_sna_view_division(self) -> float:
    """
    Queries the plot division height for SNA.
    Returns:
    float: The division height.
    """
    response = self.instrument.query(":SENS:NA:VIEW:DIV?")
    return float(response)

def store_sna_thru(self):
    """
    Stores the thru correction for SNA.
    """
    self.instrument.write(":SENS:CORR:NA:STOR:THRU")

def store_sna_thru_high(self):
    """
    Stores the high thru correction for SNA.
    """
    self.instrument.write(":SENS:CORR:NA:STOR:THRU:HIGH")

def is_sna_thru_active(self) -> bool:
    """
    Queries if the thru correction is active for SNA.
    Returns:
    bool: True if active, False otherwise.
    """
    response = self.instrument.query(":SENS:CORR:NA:STOR:THRU:ACT?")
    return response == 1

# --- Phase Noise Measurement Controls ---

def enable_phase_noise_carrier_search(self, enable: bool):
    """
    Enables or disables the signal search functionality for phase noise measurement.
    Parameters:
    enable (bool): True to enable, False to disable.
    """
    self.instrument.write(f":SENS:PN:CARR:SEAR:STAT {1 if enable else 0}")

def is_phase_noise_carrier_search_enabled(self) -> bool:
    """
    Queries if the signal search functionality is enabled for phase noise measurement.
    Returns:
    bool: True if enabled, False otherwise.
    """
    response = self.instrument.query(":SENS:PN:CARR:SEAR:STAT?")
    return int(response) == 1

def set_phase_noise_carrier_search_start(self, frequency_hz: float):
    """
    Sets the signal search start frequency for phase noise measurement.
    Parameters:
    frequency_hz (float): The start frequency in Hz.
    """
    self.instrument.write(f":SENS:PN:CARR:SEAR:STAR {frequency_hz}")

def get_phase_noise_carrier_search_start(self) -> float:
    """
    Queries the signal search start frequency for phase noise measurement.
    Returns:
    float: The start frequency in Hz.
    """
    response = self.instrument.query(":SENS:PN:CARR:SEAR:STAR?")
    return float(response)

def set_phase_noise_carrier_search_stop(self, frequency_hz: float):
    """
    Sets the signal search stop frequency for phase noise measurement.
    Parameters:
    frequency_hz (float): The stop frequency in Hz.
    """
    self.instrument.write(f":SENS:PN:CARR:SEAR:STOP {frequency_hz}")

def get_phase_noise_carrier_search_stop(self) -> float:
    """
    Queries the signal search stop frequency for phase noise measurement.
    Returns:
    float: The stop frequency in Hz.
    """
    response = self.instrument.query(":SENS:PN:CARR:SEAR:STOP?")
    return float(response)

def perform_phase_noise_carrier_search(self):
    """
    Forces a new signal search for phase noise measurement.
    """
    self.instrument.write(":SENS:PN:CARR:SEAR:PERF")

def set_phase_noise_carrier_threshold_min(self, amplitude_dbm: float):
    """
    Specifies the minimum amplitude required in dBm for a signal to be detected as a carrier.
    Parameters:
    amplitude_dbm (float): The minimum amplitude in dBm.
    """
    self.instrument.write(f":SENS:PN:CARR:THR:MIN {amplitude_dbm}")

def get_phase_noise_carrier_threshold_min(self) -> float:
    """
    Queries the minimum amplitude required for carrier detection.
    Returns:
    float: The minimum amplitude in dBm.
    """
    response = self.instrument.query(":SENS:PN:CARR:THR:MIN?")
    return float(response)

def is_phase_noise_carrier_valid(self) -> bool:
    """
    Returns whether a carrier was detected in phase noise measurement.
    Returns:
    bool: True if detected, False otherwise.
    """
    response = self.instrument.query(":SENS:PN:CARR:VAL?")
    return int(response) == 1

def get_phase_noise_carrier_frequency(self) -> float:
    """
    Returns the detected frequency of the carrier in Hz.
    Returns:
    float: The frequency in Hz.
    """
    response = self.instrument.query(":SENS:PN:CARR:FREQ?")
    return float(response)

def get_phase_noise_carrier_amplitude(self) -> float:
    """
    Returns the detected amplitude of the carrier as dBm.
    Returns:
    float: The amplitude in dBm.
    """
    response = self.instrument.query(":SENS:PN:CARR:AMPL?")
    return float(response)

def set_phase_noise_view_reference_level(self, ref_level: float):
    """
    Specifies the plot reference level as dBc/Hz for phase noise measurement.
    Parameters:
    ref_level (float): The reference level.
    """
    self.instrument.write(f":SENS:PN:VIEW:RLEV {ref_level}")

def get_phase_noise_view_reference_level(self) -> float:
    """
    Queries the plot reference level for phase noise measurement.
    Returns:
    float: The reference level.
    """
    response = self.instrument.query(":SENS:PN:VIEW:RLEV?")
    return float(response)

def set_phase_noise_view_division(self, division: float):
    """
    Specifies the plot division height for phase noise measurement.
    Parameters:
    division (float): The division height.
    """
    self.instrument.write(f":SENS:PN:VIEW:DIV {division}")

def get_phase_noise_view_division(self) -> float:
    """
    Queries the plot division height for phase noise measurement.
    Returns:
    float: The division height.
    """
    response = self.instrument.query(":SENS:PN:VIEW:DIV?")
    return float(response)

def set_phase_noise_view_num_divisions(self, num_divisions: int):
    """
    Specifies the number of divisions on the phase noise plot.
    Parameters:
    num_divisions (int): The number of divisions.
    """
    self.instrument.write(f":SENS:PN:VIEW:PNUMDIV {num_divisions}")

def get_phase_noise_view_num_divisions(self) -> int:
    """
    Queries the number of divisions on the phase noise plot.
    Returns:
    int: The number of divisions.
    """
    response = self.instrument.query(":SENS:PN:VIEW:PNUMDIV?")
    return int(response)

def set_phase_noise_frequency_center(self, frequency_hz: float):
    """
    Specifies the carrier search frequency window for phase noise measurement.
    Parameters:
    frequency_hz (float): The center frequency in Hz.
    """
    self.instrument.write(f":SENS:PN:FREQ:CENT {frequency_hz}")

def get_phase_noise_frequency_center(self) -> float:
    """
    Queries the carrier search frequency window for phase noise measurement.
    Returns:
    float: The center frequency in Hz.
    """
    response = self.instrument.query(":SENS:PN:FREQ:CENT?")
    return float(response)

def set_phase_noise_frequency_offset_start(self, offset_hz: float):
    """
    Specifies the start frequency of the phase noise sweep as an offset from the detected carrier center frequency.
    Parameters:
    offset_hz (float): The start offset in Hz.
    """
    self.instrument.write(f":SENS:PN:FREQ:OFFS:STAR {offset_hz}")

def get_phase_noise_frequency_offset_start(self) -> float:
    """
    Queries the start frequency offset for phase noise sweep.
    Returns:
    float: The start offset in Hz.
    """
    response = self.instrument.query(":SENS:PN:FREQ:OFFS:STAR?")
    return float(response)

def set_phase_noise_frequency_offset_stop(self, offset_hz: float):
    """
    Specifies the stop frequency of the phase noise sweep as an offset from the detected carrier center frequency.
    Parameters:
    offset_hz (float): The stop offset in Hz.
    """
    self.instrument.write(f":SENS:PN:FREQ:OFFS:STOP {offset_hz}")

def get_phase_noise_frequency_offset_stop(self) -> float:
    """
    Queries the stop frequency offset for phase noise sweep.
    Returns:
    float: The stop offset in Hz.
    """
    response = self.instrument.query(":SENS:PN:FREQ:OFFS:STOP?")
    return float(response)

def enable_phase_noise_peak_track(self, enable: bool):
    """
    Enables or disables peak tracking for phase noise measurement.
    Parameters:
    enable (bool): True to enable, False to disable.
    """
    self.instrument.write(f":SENS:PN:PKTR {1 if enable else 0}")

def is_phase_noise_peak_track_enabled(self) -> bool:
    """
    Queries if peak tracking is enabled for phase noise measurement.
    Returns:
    bool: True if enabled, False otherwise.
    """
    response = self.instrument.query(":SENS:PN:PKTR?")
    return int(response) == 1

def set_phase_noise_type(self, noise_type: str):
    """
    Sets the measurement type for phase noise: 'PN' (Phase Noise), 'PNPAM' (Phase+AM Noise), or 'AM' (AM Noise).
    Parameters:
    noise_type (str): Allowed values are 'PN', 'PNPAM', 'AM'.
    """
    valid_types = {"PN", "PNPAM", "AM"}
    noise_type_upper = noise_type.upper()
    if noise_type_upper not in valid_types:
        raise ValueError(f"Invalid phase noise type: '{noise_type}'. Must be 'PN', 'PNPAM', or 'AM'.")
    self.instrument.write(f":SENS:PN:TYPE {noise_type_upper}")

def get_phase_noise_type(self) -> str:
    """
    Queries the measurement type for phase noise.
    Returns:
    str: The measurement type ('PN', 'PNPAM', or 'AM').
    """
    response = self.instrument.query(":SENS:PN:TYPE?")
    return response.strip().upper()

# --- Phase Noise Cross Correlation Controls ---

def is_phase_noise_xcorr_active(self) -> bool:
    """
    Returns true if cross correlation is enabled.
    """
    response = self.instrument.query(":SENS:PN:XCORR:STAT?")
    return int(response) == 1

def enable_phase_noise_xcorr(self, enable: bool):
    """
    Enables or disables cross correlation.
    Parameters:
    enable (bool): True to enable, False to disable.
    """
    self.instrument.write(f":SENS:PN:XCORR:STAT {1 if enable else 0}")

def get_phase_noise_xcorr_reference(self) -> str:
    """
    Queries the timebase reference of the cross correlation measurement system.
    Returns:
    str: 'INTERNAL', 'EXTERNAL', or 'RF'
    """
    response = self.instrument.query(":SENS:PN:XCORR:REF?")
    return response.strip().upper()

def set_phase_noise_xcorr_reference(self, reference: str):
    """
    Sets the timebase reference of the cross correlation measurement system.
    Parameters:
    reference (str): Allowed values are 'INTERNAL', 'EXTERNAL', 'RF'
    """
    valid_refs = {"INTERNAL", "EXTERNAL", "RF"}
    ref_upper = reference.upper()
    if ref_upper not in valid_refs:
        raise ValueError(f"Invalid reference: '{reference}'. Must be one of {valid_refs}.")
    self.instrument.write(f":SENS:PN:XCORR:REF {ref_upper}")

def set_phase_noise_xcorr_factor(self, factor: int):
    """
    Sets the cross correlation factor.
    Parameters:
    factor (int): The cross correlation factor.
    """
    self.instrument.write(f":SENS:PN:XCORR:FACTOR {factor}")

def get_phase_noise_xcorr_factor(self) -> int:
    """
    Queries the cross correlation factor.
    Returns:
    int: The cross correlation factor.
    """
    response = self.instrument.query(":SENS:PN:XCORR:FACTOR?")
    return int(response)

def restart_phase_noise_xcorr_measurement(self):
    """
    Restarts a cross correlation measurement.
    """
    self.instrument.write(":SENS:PN:XCORR:MEAS:RESTART")

def get_phase_noise_xcorr_progress(self) -> int:
    """
    Tracks the progress of the cross correlation measurement.
    Returns:
    int: Progress value, -1 if not enabled.
    """
    response = self.instrument.query(":SENS:PN:XCORR:MEAS:PROGRESS?")
    return int(response)

def get_phase_noise_xcorr_device_list(self) -> list:
    """
    Returns a list of all SM devices that can be used as the second analyzer for cross correlation measurements.
    Returns:
    list: Device names.
    """
    response = self.instrument.query(":SENS:PN:XCORR:DEVICE:LIST?")
    return [d.strip() for d in response.split(',')]

def get_phase_noise_xcorr_device_count(self) -> int:
    """
    Returns the number of SM devices available for cross correlation.
    Returns:
    int: Device count.
    """
    response = self.instrument.query(":SENS:PN:XCORR:DEVICE:COUNT?")
    return int(response)

def get_phase_noise_xcorr_device_current(self) -> str:
    """
    Returns the name of the second analyzer, if active.
    Returns:
    str: Device name.
    """
    response = self.instrument.query(":SENS:PN:XCORR:DEVICE:CURR?")
    return response.strip()

def connect_phase_noise_xcorr_device(self, device_name: str) -> bool:
    """
    Connects the second analyzer for cross correlation.
    Parameters:
    device_name (str): The device name.
    Returns:
    bool: True if successful, False otherwise.
    """
    response = self.instrument.query(f":SENS:PN:XCORR:DEVICE:CONNECT? {device_name}")
    return int(response) == 1

def disconnect_phase_noise_xcorr_device(self) -> bool:
    """
    Disconnects the second analyzer for cross correlation.
    Returns:
    bool: True if successful, False otherwise.
    """
    response = self.instrument.query(":SENS:PN:XCORR:DEVICE:DISCONNECT?")
    return int(response) == 1

def show_phase_noise_xcorr_gain_indicator(self, enable: bool):
    """
    Show/hide the gain indicator for cross correlation.
    Parameters:
    enable (bool): True to show, False to hide.
    """
    self.instrument.write(f":DISP:PN:XCORR:GIN {1 if enable else 0}")

def is_phase_noise_xcorr_gain_indicator_visible(self) -> bool:
    """
    Queries if the gain indicator is visible for cross correlation.
    Returns:
    bool: True if visible, False otherwise.
    """
    response = self.instrument.query(":DISP:PN:XCORR:GIN?")
    return int(response) == 1

def show_phase_noise_xcorr_count(self, enable: bool):
    """
    Show/hide the cross correlation counts.
    Parameters:
    enable (bool): True to show, False to hide.
    """
    self.instrument.write(f":DISP:PN:XCORR:COUNT {1 if enable else 0}")

def is_phase_noise_xcorr_count_visible(self) -> bool:
    """
    Queries if the cross correlation counts are visible.
    Returns:
    bool: True if visible, False otherwise.
    """
    response = self.instrument.query(":DISP:PN:XCORR:COUNT?")
    return int(response) == 1

# --- Phase Noise VCO Controls ---

def is_phase_noise_vco_active(self) -> bool:
    """
    Returns whether the PN400 is connected in the software.
    Returns:
    bool: True if connected, False otherwise.
    """
    response = self.instrument.query(":SENS:PN:VCO:ACT?")
    return int(response) == 1

def connect_phase_noise_vco(self) -> bool:
    """
    Connects the PN400 and returns true if successful.
    Returns:
    bool: True if successful, False otherwise.
    """
    response = self.instrument.query(":SENS:PN:VCO:CONNECT?")
    return int(response) == 1

def enable_phase_noise_vco_voltage(self, enable: bool):
    """
    Enable/disable the supply and tune output voltages.
    Parameters:
    enable (bool): True to enable, False to disable.
    """
    self.instrument.write(f":SENS:PN:VCO:VOLT:STAT {1 if enable else 0}")

def is_phase_noise_vco_voltage_enabled(self) -> bool:
    """
    Queries if the supply and tune output voltages are enabled.
    Returns:
    bool: True if enabled, False otherwise.
    """
    response = self.instrument.query(":SENS:PN:VCO:VOLT:STAT?")
    return int(response) == 1

def set_phase_noise_vco_voltage_supply_min(self, voltage: float):
    """
    Sets the minimum supply voltage for the VCO.
    Parameters:
    voltage (float): The minimum supply voltage.
    """
    self.instrument.write(f":SENS:PN:VCO:VOLT:SUPP:MIN {voltage}")

def get_phase_noise_vco_voltage_supply_min(self) -> float:
    """
    Queries the minimum supply voltage for the VCO.
    Returns:
    float: The minimum supply voltage.
    """
    response = self.instrument.query(":SENS:PN:VCO:VOLT:SUPP:MIN?")
    return float(response)

def set_phase_noise_vco_voltage_supply_max(self, voltage: float):
    """
    Sets the maximum supply voltage for the VCO.
    Parameters:
    voltage (float): The maximum supply voltage.
    """
    self.instrument.write(f":SENS:PN:VCO:VOLT:SUPP:MAX {voltage}")

def get_phase_noise_vco_voltage_supply_max(self) -> float:
    """
    Queries the maximum supply voltage for the VCO.
    Returns:
    float: The maximum supply voltage.
    """
    response = self.instrument.query(":SENS:PN:VCO:VOLT:SUPP:MAX?")
    return float(response)

def set_phase_noise_vco_voltage_supply(self, voltage: float):
    """
    Sets the supply voltage for the VCO.
    Parameters:
    voltage (float): The supply voltage.
    """
    self.instrument.write(f":SENS:PN:VCO:VOLT:SUPP {voltage}")

def get_phase_noise_vco_voltage_supply(self) -> float:
    """
    Queries the supply voltage for the VCO.
    Returns:
    float: The supply voltage.
    """
    response = self.instrument.query(":SENS:PN:VCO:VOLT:SUPP?")
    return float(response)

def set_phase_noise_vco_voltage_tune_min(self, voltage: float):
    """
    Sets the minimum tune voltage for the VCO.
    Parameters:
    voltage (float): The minimum tune voltage.
    """
    self.instrument.write(f":SENS:PN:VCO:VOLT:TUNE:MIN {voltage}")

def get_phase_noise_vco_voltage_tune_min(self) -> float:
    """
    Queries the minimum tune voltage for the VCO.
    Returns:
    float: The minimum tune voltage.
    """
    response = self.instrument.query(":SENS:PN:VCO:VOLT:TUNE:MIN?")
    return float(response)

def set_phase_noise_vco_voltage_tune_max(self, voltage: float):
    """
    Sets the maximum tune voltage for the VCO.
    Parameters:
    voltage (float): The maximum tune voltage.
    """
    self.instrument.write(f":SENS:PN:VCO:VOLT:TUNE:MAX {voltage}")

def get_phase_noise_vco_voltage_tune_max(self) -> float:
    """
    Queries the maximum tune voltage for the VCO.
    Returns:
    float: The maximum tune voltage.
    """
    response = self.instrument.query(":SENS:PN:VCO:VOLT:TUNE:MAX?")
    return float(response)

def set_phase_noise_vco_voltage_tune(self, voltage: float):
    """
    Sets the tune voltage for the VCO.
    Parameters:
    voltage (float): The tune voltage.
    """
    self.instrument.write(f":SENS:PN:VCO:VOLT:TUNE {voltage}")

def get_phase_noise_vco_voltage_tune(self) -> float:
    """
    Queries the tune voltage for the VCO.
    Returns:
    float: The tune voltage.
    """
    response = self.instrument.query(":SENS:PN:VCO:VOLT:TUNE?")
    return float(response)

# --- Phase Noise Trace Controls ---

def select_phase_noise_trace(self, trace_index: int):
    """
    Specifies the active trace index for phase noise measurements.
    Parameters:
    trace_index (int): Trace index (1-6).
    """
    if not (1 <= trace_index <= 6):
        raise ValueError("Trace index must be between 1 and 6.")
    self.instrument.write(f":TRAC:PN:SEL {trace_index}")

def get_selected_phase_noise_trace(self) -> int:
    """
    Queries the active trace index for phase noise measurements.
    Returns:
    int: Trace index (1-6).
    """
    response = self.instrument.query(":TRAC:PN:SEL?")
    return int(response)

def set_phase_noise_trace_type(self, trace_type: str):
    """
    Specifies the trace type for phase noise measurements.
    Parameters:
    trace_type (str): Allowed values: 'OFF', 'NORMAL', 'AVERAGE', 'REFERENCE', 'MINHOLD', 'MAXHOLD'
    """
    valid_types = {"OFF", "NORMAL", "AVERAGE", "REFERENCE", "MINHOLD", "MAXHOLD"}
    trace_type_upper = trace_type.upper()
    if trace_type_upper not in valid_types:
        raise ValueError(f"Invalid trace type: '{trace_type}'. Must be one of {valid_types}.")
    self.instrument.write(f":TRAC:PN:TYPE {trace_type_upper}")

def get_phase_noise_trace_type(self) -> str:
    """
    Queries the trace type for phase noise measurements.
    Returns:
    str: Trace type.
    """
    response = self.instrument.query(":TRAC:PN:TYPE?")
    return response.strip().upper()

def set_phase_noise_trace_average_count(self, count: int):
    """
    Specifies the number of sweeps to average for phase noise trace.
    Parameters:
    count (int): Number of sweeps.
    """
    self.instrument.write(f":TRAC:PN:AVER:COUN {count}")

def get_phase_noise_trace_average_count(self) -> int:
    """
    Queries the number of sweeps averaged for phase noise trace.
    Returns:
    int: Number of sweeps.
    """
    response = self.instrument.query(":TRAC:PN:AVER:COUN?")
    return int(response)

def enable_phase_noise_trace_update(self, enable: bool):
    """
    Specifies if the trace updates when a new sweep is acquired.
    Parameters:
    enable (bool): True to enable, False to disable.
    """
    self.instrument.write(f":TRAC:PN:UPD {1 if enable else 0}")

def is_phase_noise_trace_update_enabled(self) -> bool:
    """
    Queries if the trace updates when a new sweep is acquired.
    Returns:
    bool: True if enabled, False otherwise.
    """
    response = self.instrument.query(":TRAC:PN:UPD?")
    return int(response) == 1

def enable_phase_noise_trace_hide(self, enable: bool):
    """
    Hides or shows the trace.
    Parameters:
    enable (bool): True to hide, False to show.
    """
    self.instrument.write(f":TRAC:PN:HIDE {1 if enable else 0}")

def is_phase_noise_trace_hidden(self) -> bool:
    """
    Queries if the trace is hidden.
    Returns:
    bool: True if hidden, False otherwise.
    """
    response = self.instrument.query(":TRAC:PN:HIDE?")
    return int(response) == 1

def enable_phase_noise_trace_smoothing(self, enable: bool):
    """
    Enables or disables smoothing for phase noise trace.
    Parameters:
    enable (bool): True to enable, False to disable.
    """
    self.instrument.write(f":TRAC:PN:SMOOTH {1 if enable else 0}")

def is_phase_noise_trace_smoothing_enabled(self) -> bool:
    """
    Queries if smoothing is enabled for phase noise trace.
    Returns:
    bool: True if enabled, False otherwise.
    """
    response = self.instrument.query(":TRAC:PN:SMOOTH?")
    return int(response) == 1

def set_phase_noise_trace_smoothing_aperture(self, aperture: float):
    """
    Specifies the smoothing aperture as a percentage.
    Parameters:
    aperture (float): Smoothing aperture (%).
    """
    self.instrument.write(f":TRAC:PN:SMOOTH:APER {aperture}")

def get_phase_noise_trace_smoothing_aperture(self) -> float:
    """
    Queries the smoothing aperture for phase noise trace.
    Returns:
    float: Smoothing aperture (%).
    """
    response = self.instrument.query(":TRAC:PN:SMOOTH:APER?")
    return float(response)

def enable_phase_noise_trace_spur_reject(self, enable: bool):
    """
    Enables or disables trace spur rejection.
    Parameters:
    enable (bool): True to enable, False to disable.
    """
    self.instrument.write(f":TRAC:PN:SPUR {1 if enable else 0}")

def is_phase_noise_trace_spur_reject_enabled(self) -> bool:
    """
    Queries if trace spur rejection is enabled.
    Returns:
    bool: True if enabled, False otherwise.
    """
    response = self.instrument.query(":TRAC:PN:SPUR?")
    return int(response) == 1

def set_phase_noise_trace_spur_reject_threshold(self, threshold_db: float):
    """
    Specifies the spur reject threshold in dB.
    Parameters:
    threshold_db (float): Spur reject threshold in dB.
    """
    self.instrument.write(f":TRAC:PN:SPUR:THR {threshold_db}")

def get_phase_noise_trace_spur_reject_threshold(self) -> float:
    """
    Queries the spur reject threshold in dB.
    Returns:
    float: Spur reject threshold in dB.
    """
    response = self.instrument.query(":TRAC:PN:SPUR:THR?")
    return float(response)

def set_phase_noise_trace_offset(self, offset_db: float):
    """
    Specifies an offset in dB for the trace.
    Parameters:
    offset_db (float): Offset in dB.
    """
    self.instrument.write(f":TRAC:PN:OFFS {offset_db}")

def get_phase_noise_trace_offset(self) -> float:
    """
    Queries the offset in dB for the trace.
    Returns:
    float: Offset in dB.
    """
    response = self.instrument.query(":TRAC:PN:OFFS?")
    return float(response)

def move_phase_noise_trace_to(self, trace_index: int):
    """
    Moves the current trace to the selected trace. The selected trace type will be set to reference.
    Parameters:
    trace_index (int): Trace index (1-6).
    """
    if not (1 <= trace_index <= 6):
        raise ValueError("Trace index must be between 1 and 6.")
    self.instrument.write(f":TRAC:PN:TO {trace_index}")

def clear_phase_noise_trace(self):
    """
    Clears the current average accumulation for phase noise trace.
    """
    self.instrument.write(":TRAC:PN:CLEAR")

def get_phase_noise_trace_data_y(self) -> list:
    """
    Returns the trace data amplitudes for phase noise.
    Returns:
    list: Amplitude values.
    """
    response = self.instrument.query(":TRAC:PN:DATA:Y?")
    return [float(val) for val in response.split(',') if val.strip()]

def get_phase_noise_trace_data_x(self) -> list:
    """
    Returns the trace data frequencies for phase noise.
    Returns:
    list: Frequency values.
    """
    response = self.instrument.query(":TRAC:PN:DATA:X?")
    return [float(val) for val in response.split(',') if val.strip()]

# --- Phase Noise Marker Controls ---

def select_phase_noise_marker(self, marker_index: int):
    """
    Specifies the active marker index for phase noise measurements.
    Parameters:
    marker_index (int): Marker index (1-6).
    """
    if not (1 <= marker_index <= 6):
        raise ValueError("Marker index must be between 1 and 6.")
    self.instrument.write(f":CALC:PN:MARK:SEL {marker_index}")

def get_selected_phase_noise_marker(self) -> int:
    """
    Queries the active marker index for phase noise measurements.
    Returns:
    int: Marker index (1-6).
    """
    response = self.instrument.query(":CALC:PN:MARK:SEL?")
    return int(response)

def enable_phase_noise_marker(self, enable: bool):
    """
    Enables or disables the marker for phase noise measurements.
    Parameters:
    enable (bool): True to enable, False to disable.
    """
    self.instrument.write(f":CALC:PN:MARK:STAT {1 if enable else 0}")

def is_phase_noise_marker_enabled(self) -> bool:
    """
    Queries if the marker is enabled for phase noise measurements.
    Returns:
    bool: True if enabled, False otherwise.
    """
    response = self.instrument.query(":CALC:PN:MARK:STAT?")
    return int(response) == 1

def set_phase_noise_marker_trace(self, trace_index: int):
    """
    Selects which trace the marker is placed on for phase noise measurements.
    Parameters:
    trace_index (int): Trace index (1-3).
    """
    if not (1 <= trace_index <= 3):
        raise ValueError("Trace index must be between 1 and 3.")
    self.instrument.write(f":CALC:PN:MARK:TRAC {trace_index}")

def get_phase_noise_marker_trace(self) -> int:
    """
    Queries which trace the marker is placed on for phase noise measurements.
    Returns:
    int: Trace index (1-3).
    """
    response = self.instrument.query(":CALC:PN:MARK:TRAC?")
    return int(response)

def enable_phase_noise_marker_delta(self, enable: bool):
    """
    Enables or disables the delta marker for phase noise measurements.
    Parameters:
    enable (bool): True to enable, False to disable.
    """
    self.instrument.write(f":CALC:PN:MARK:DELT {1 if enable else 0}")

def is_phase_noise_marker_delta_enabled(self) -> bool:
    """
    Queries if the delta marker is enabled for phase noise measurements.
    Returns:
    bool: True if enabled, False otherwise.
    """
    response = self.instrument.query(":CALC:PN:MARK:DELT?")
    return int(response) == 1

def set_phase_noise_marker_frequency(self, offset_hz: float):
    """
    Sets the marker frequency as an offset from the carrier frequency for phase noise measurements.
    Parameters:
    offset_hz (float): Frequency offset in Hz.
    """
    self.instrument.write(f":CALC:PN:MARK:X {offset_hz}")

def get_phase_noise_marker_frequency(self) -> float:
    """
    Queries the marker frequency as an offset from the carrier for phase noise measurements.
    Returns:
    float: Frequency offset in Hz.
    """
    response = self.instrument.query(":CALC:PN:MARK:X?")
    return float(response)

def get_phase_noise_marker_amplitude(self) -> float:
    """
    Queries the amplitude of the marker for phase noise measurements.
    Returns:
    float: Amplitude in dBc/Hz.
    """
    response = self.instrument.query(":CALC:PN:MARK:Y?")
    return float(response)

# --- Phase Noise Jitter Controls ---

def enable_phase_noise_jitter(self, enable: bool):
    """
    Enables or disables the jitter measurement for phase noise.
    Parameters:
    enable (bool): True to enable, False to disable.
    """
    self.instrument.write(f":CALC:PN:JITT:STAT {1 if enable else 0}")

def is_phase_noise_jitter_enabled(self) -> bool:
    """
    Queries if the jitter measurement is enabled for phase noise.
    Returns:
    bool: True if enabled, False otherwise.
    """
    response = self.instrument.query(":CALC:PN:JITT:STAT?")
    return int(response) == 1

def set_phase_noise_jitter_trace(self, trace_index: int):
    """
    Specifies the target trace of the jitter measurement for phase noise.
    Parameters:
    trace_index (int): Trace index (1-3).
    """
    if not (1 <= trace_index <= 3):
        raise ValueError("Trace index must be between 1 and 3.")
    self.instrument.write(f":CALC:PN:JITT:TRAC {trace_index}")

def get_phase_noise_jitter_trace(self) -> int:
    """
    Queries the target trace of the jitter measurement for phase noise.
    Returns:
    int: Trace index (1-3).
    """
    response = self.instrument.query(":CALC:PN:JITT:TRAC?")
    return int(response)

def set_phase_noise_jitter_start(self, offset_hz: float):
    """
    Specifies the start frequency of the jitter measurement as an offset from the carrier frequency.
    Parameters:
    offset_hz (float): Start offset in Hz.
    """
    self.instrument.write(f":CALC:PN:JITT:STAR {offset_hz}")

def get_phase_noise_jitter_start(self) -> float:
    """
    Queries the start frequency of the jitter measurement as an offset from the carrier frequency.
    Returns:
    float: Start offset in Hz.
    """
    response = self.instrument.query(":CALC:PN:JITT:STAR?")
    return float(response)

def set_phase_noise_jitter_stop(self, offset_hz: float):
    """
    Specifies the stop frequency of the jitter measurement as an offset from the carrier frequency.
    Parameters:
    offset_hz (float): Stop offset in Hz.
    """
    self.instrument.write(f":CALC:PN:JITT:STOP {offset_hz}")

def get_phase_noise_jitter_stop(self) -> float:
    """
    Queries the stop frequency of the jitter measurement as an offset from the carrier frequency.
    Returns:
    float: Stop offset in Hz.
    """
    response = self.instrument.query(":CALC:PN:JITT:STOP?")
    return float(response)

def get_phase_noise_jitter_rms(self) -> float:
    """
    Queries the RMS jitter of the measurement in seconds.
    Returns:
    float: RMS jitter in seconds.
    """
    response = self.instrument.query(":CALC:PN:JITT:RMS?")
    return float(response)

def get_phase_noise_jitter_phase(self) -> float:
    """
    Queries the phase jitter of the measurement in radians.
    Returns:
    float: Phase jitter in radians.
    """
    response = self.instrument.query(":CALC:PN:JITT:PHASE?")

# --- Harmonics Measurement Controls ---

def set_harmonics_number(self, number: int):
    self.instrument.write(f":SENS:HARM:NUMB {number}")

def get_harmonics_number(self) -> int:
    response = self.instrument.query(":SENS:HARM:NUMB?")
    return int(response)

def enable_harmonics_tracking(self, enable: bool):
    self.instrument.write(f":SENS:HARM:TRACK {1 if enable else 0}")

def is_harmonics_tracking_enabled(self) -> bool:
    response = self.instrument.query(":SENS:HARM:TRACK?")
    return int(response) == 1

def set_harmonics_mode(self, mode: str):
    valid_modes = {"PEAK", "CHPOWER"}
    mode_upper = mode.upper()
    if mode_upper not in valid_modes:
        raise ValueError(f"Invalid harmonics mode: '{mode}'. Must be 'PEAK' or 'CHPOWER'.")
    self.instrument.write(f":SENS:HARM:MODE {mode_upper}")

def get_harmonics_mode(self) -> str:
    response = self.instrument.query(":SENS:HARM:MODE?")
    return response.strip().upper()

def set_harmonics_fundamental_frequency(self, frequency_hz: float):
    self.instrument.write(f":SENS:HARM:FREQ:FUND {frequency_hz}")

def get_harmonics_fundamental_frequency(self) -> float:
    response = self.instrument.query(":SENS:HARM:FREQ:FUND?")
    return float(response)

def set_harmonics_frequency_step(self, step_hz: float):
    self.instrument.write(f":SENS:HARM:FREQ:STEP {step_hz}")

def get_harmonics_frequency_step(self) -> float:
    response = self.instrument.query(":SENS:HARM:FREQ:STEP?")
    return float(response)

def set_harmonics_frequency_span(self, span_hz: float):
    self.instrument.write(f":SENS:HARM:FREQ:SPAN {span_hz}")

def get_harmonics_frequency_span(self) -> float:
    response = self.instrument.query(":SENS:HARM:FREQ:SPAN?")
    return float(response)

def set_harmonics_bandwidth_resolution(self, rbw_hz: float):
    self.instrument.write(f":SENS:HARM:BAND:RES {rbw_hz}")

def get_harmonics_bandwidth_resolution(self) -> float:
    response = self.instrument.query(":SENS:HARM:BAND:RES?")
    return float(response)

def set_harmonics_bandwidth_video(self, vbw_hz: float):
    self.instrument.write(f":SENS:HARM:BAND:VID {vbw_hz}")

def get_harmonics_bandwidth_video(self) -> float:
    response = self.instrument.query(":SENS:HARM:BAND:VID?")
    return float(response)

def set_harmonics_power_reference_level(self, ref_level_dbm: float):
    self.instrument.write(f":SENS:HARM:POW:RF:RLEV {ref_level_dbm}")

def get_harmonics_power_reference_level(self) -> float:
    response = self.instrument.query(":SENS:HARM:POW:RF:RLEV?")
    return float(response)

def set_harmonics_view_reference_level(self, ref_level_dbm: float):
    self.instrument.write(f":SENS:HARM:VIEW:RLEV {ref_level_dbm}")

def get_harmonics_view_reference_level(self) -> float:
    response = self.instrument.query(":SENS:HARM:VIEW:RLEV?")
    return float(response)

def set_harmonics_view_division(self, division_db: float):
    self.instrument.write(f":SENS:HARM:VIEW:PDIV {division_db}")

def get_harmonics_view_division(self) -> float:
    response = self.instrument.query(":SENS:HARM:VIEW:PDIV?")
    return float(response)

def set_harmonics_trace_type(self, trace_type: str):
    valid_types = {"WRITE", "MAXHOLD"}
    trace_type_upper = trace_type.upper()
    if trace_type_upper not in valid_types:
        raise ValueError(f"Invalid trace type: '{trace_type}'. Must be 'WRITE' or 'MAXHOLD'.")
    self.instrument.write(f":SENS:HARM:TRAC:TYPE {trace_type_upper}")

def get_harmonics_trace_type(self) -> str:
    response = self.instrument.query(":SENS:HARM:TRAC:TYPE?")
    return response.strip().upper()

# --- Harmonics Fetch Results ---

def fetch_harmonics_frequency(self, harmonic_index: int) -> float:
    response = self.instrument.query(f":SENS:FETC:HARM:FREQ? {harmonic_index}")
    return float(response)

def fetch_harmonics_amplitude(self, harmonic_index: int) -> float:
    response = self.instrument.query(f":SENS:FETC:HARM:AMPL? {harmonic_index}")
    return float(response)

def fetch_harmonics_distortion(self) -> float:
    response = self.instrument.query(":SENS:FETC:HARM:DIST?")
    return float(response)

# --- Analog Demodulation Controls ---

def set_ademod_center_frequency(self, frequency_hz: float):
    self.instrument.write(f":SENS:ADEMOD:FREQ:CENT {frequency_hz}")

def get_ademod_center_frequency(self) -> float:
    response = self.instrument.query(":SENS:ADEMOD:FREQ:CENT?")
    return float(response)

def set_ademod_center_frequency_step(self, step_hz: float):
    self.instrument.write(f":SENS:ADEMOD:FREQ:CENT:STEP {step_hz}")

def get_ademod_center_frequency_step(self) -> float:
    response = self.instrument.query(":SENS:ADEMOD:FREQ:CENT:STEP?")
    return float(response)

def set_ademod_power_reference_level(self, ref_level_dbm: float):
    self.instrument.write(f":SENS:ADEMOD:POW:RF:RLEV {ref_level_dbm}")

def get_ademod_power_reference_level(self) -> float:
    response = self.instrument.query(":SENS:ADEMOD:POW:RF:RLEV?")
    return float(response)

def set_ademod_low_pass_filter(self, cutoff_hz: float):
    self.instrument.write(f":SENS:ADEMOD:LPF {cutoff_hz}")

def get_ademod_low_pass_filter(self) -> float:
    response = self.instrument.query(":SENS:ADEMOD:LPF?")
    return float(response)

# --- Analog Demodulation Fetch Results ---

def fetch_ademod_am_metrics(self, metrics: list) -> list:
    metrics_str = ",".join(str(m) for m in metrics)
    response = self.instrument.query(f":SENS:FETC:ADEMOD:AM? {metrics_str}")
    return [float(val) for val in response.split(',') if val.strip()]

def fetch_ademod_fm_metrics(self, metrics: list) -> list:
    metrics_str = ",".join(str(m) for m in metrics)
    response = self.instrument.query(f":SENS:FETC:ADEMOD:FM? {metrics_str}")
    return [float(val) for val in response.split(',') if val.strip()]

# --- Digital Demodulation Controls ---

def set_ddemod_center_frequency(self, frequency_hz: float):
    self.instrument.write(f":SENS:DDEMOD:FREQ:CENT {frequency_hz}")

def get_ddemod_center_frequency(self) -> float:
    response = self.instrument.query(":SENS:DDEMOD:FREQ:CENT?")
    return float(response)

def set_ddemod_center_frequency_step(self, step_hz: float):
    self.instrument.write(f":SENS:DDEMOD:FREQ:CENT:STEP {step_hz}")

def get_ddemod_center_frequency_step(self) -> float:
    response = self.instrument.query(":SENS:DDEMOD:FREQ:CENT:STEP?")
    return float(response)

def set_ddemod_power_reference_level(self, ref_level_dbm: float):
    self.instrument.write(f":SENS:DDEMOD:POW:RF:RLEV {ref_level_dbm}")

def get_ddemod_power_reference_level(self) -> float:
    response = self.instrument.query(":SENS:DDEMOD:POW:RF:RLEV?")
    return float(response)

def set_ddemod_sample_rate(self, sample_rate_hz: float):
    self.instrument.write(f":SENS:DDEMOD:SRAT {sample_rate_hz}")

def get_ddemod_sample_rate(self) -> float:
    response = self.instrument.query(":SENS:DDEMOD:SRAT?")
    return float(response)

def set_ddemod_modulation(self, modulation: str):
    valid_modulations = {
        "BPSK", "DBPSK", "QPSK", "DQPSK", "OQPSK", "PI4QPSK", "8PSK", "D8PSK",
        "QAM16", "QAM32", "QAM64", "QAM256", "QAM1024", "FSK2", "FSK4", "FSK8", "FSK16", "ASK2", "CUSTOM"
    }
    modulation_upper = modulation.upper()
    if modulation_upper not in valid_modulations:
        raise ValueError(f"Invalid modulation type: '{modulation}'. Must be one of {valid_modulations}.")
    self.instrument.write(f":SENS:DDEMOD:MOD {modulation_upper}")

def get_ddemod_modulation(self) -> str:
    response = self.instrument.query(":SENS:DDEMOD:MOD?")
    return response.strip().upper()

def set_ddemod_rlength(self, rlength: int):
    self.instrument.write(f":SENS:DDEMOD:RLEN {rlength}")

def get_ddemod_rlength(self) -> int:
    response = self.instrument.query(":SENS:DDEMOD:RLEN?")
    return int(response)

def set_ddemod_filter(self, filter_type: str):
    valid_filters = {"NYQUIST", "RNYQUIST", "GAUSSIAN", "RECTANGLE"}
    filter_upper = filter_type.upper()
    if filter_upper not in valid_filters:
        raise ValueError(f"Invalid filter type: '{filter_type}'. Must be one of {valid_filters}.")
    self.instrument.write(f":SENS:DDEMOD:FILT {filter_upper}")

def get_ddemod_filter(self) -> str:
    response = self.instrument.query(":SENS:DDEMOD:FILT?")
    return response.strip().upper()

def set_ddemod_filter_abt(self, abt_value: float):
    self.instrument.write(f":SENS:DDEMOD:FILT:ABT {abt_value}")

def get_ddemod_filter_abt(self) -> float:
    response = self.instrument.query(":SENS:DDEMOD:FILT:ABT?")
    return float(response)

def enable_ddemod_ifbw_auto(self, enable: bool):
    self.instrument.write(f":SENS:DDEMOD:IFBW:AUTO {1 if enable else 0}")

def is_ddemod_ifbw_auto_enabled(self) -> bool:
    response = self.instrument.query(":SENS:DDEMOD:IFBW:AUTO?")
    return int(response) == 1

def set_ddemod_ifbw(self, ifbw_hz: float):
    self.instrument.write(f":SENS:DDEMOD:IFBW {ifbw_hz}")

def get_ddemod_ifbw(self) -> float:
    response = self.instrument.query(":SENS:DDEMOD:IFBW?")
    return float(response)

def enable_ddemod_average(self, enable: bool):
    self.instrument.write(f":SENS:DDEMOD:AVER {1 if enable else 0}")

def is_ddemod_average_enabled(self) -> bool:
    response = self.instrument.query(":SENS:DDEMOD:AVER?")
    return int(response) == 1

def set_ddemod_average_count(self, count: int):
    self.instrument.write(f":SENS:DDEMOD:AVER:COUN {count}")

def get_ddemod_average_count(self) -> int:
    response = self.instrument.query(":SENS:DDEMOD:AVER:COUN?")
    return int(response)

def enable_ddemod_wce(self, enable: bool):
    self.instrument.write(f":SENS:DDEMOD:WCE {1 if enable else 0}")

def is_ddemod_wce_enabled(self) -> bool:
    response = self.instrument.query(":SENS:DDEMOD:WCE?")
    return int(response) == 1

def set_ddemod_wce_range(self, range_hz: float):
    self.instrument.write(f":SENS:DDEMOD:WCE:RANG {range_hz}")

def get_ddemod_wce_range(self) -> float:
    response = self.instrument.query(":SENS:DDEMOD:WCE:RANG?")
    return float(response)
# --- Digital Demodulation Custom Modulation Controls ---

def is_ddemod_custom_iq_valid(self) -> bool:
    """
    Returns True if the custom constellation is valid.
    """
    response = self.instrument.query(":SENS:DDEMOD:CUST:IQ:VAL?")
    return int(response) == 1

def get_ddemod_custom_iq_length(self) -> int:
    """
    Returns the number of symbols in the custom constellation.
    """
    response = self.instrument.query(":SENS:DDEMOD:CUST:IQ:LENG?")
    return int(response)

def set_ddemod_custom_iq_data(self, iq_values: list):
    """
    Specifies the constellation symbols as IQ values (alternating I/Q floats).
    """
    iq_str = ",".join(str(v) for v in iq_values)
    self.instrument.write(f":SENS:DDEMOD:CUST:IQ:DATA {iq_str}")

def get_ddemod_custom_iq_data(self) -> list:
    """
    Returns the constellation symbols as a comma separated list of alternating IQ values.
    """
    response = self.instrument.query(":SENS:DDEMOD:CUST:IQ:DATA?")
    return [float(x) for x in response.split(',') if x.strip()]

# --- Digital Demodulation Trigger Controls ---

def set_ddemod_trigger_source(self, source: str):
    """
    Sets the trigger source for digital demodulation.
    Allowed values: 'IMMEDIATE', 'IF', 'EXTERNAL'
    """
    valid_sources = {"IMMEDIATE", "IF", "EXTERNAL"}
    source_upper = source.upper()
    if source_upper not in valid_sources:
        raise ValueError(f"Invalid trigger source: '{source}'. Must be one of {valid_sources}.")
    self.instrument.write(f":TRIG:DDEMOD:SOUR {source_upper}")

def get_ddemod_trigger_source(self) -> str:
    """
    Queries the trigger source for digital demodulation.
    """
    response = self.instrument.query(":TRIG:DDEMOD:SOUR?")
    return response.strip().upper()

def set_ddemod_trigger_if_level(self, amplitude_dbm: float):
    """
    Sets the trigger level for IF trigger in digital demodulation.
    """
    self.instrument.write(f":TRIG:DDEMOD:IF:LEV {amplitude_dbm}")

def get_ddemod_trigger_if_level(self) -> float:
    """
    Queries the trigger level for IF trigger in digital demodulation.
    """
    response = self.instrument.query(":TRIG:DDEMOD:IF:LEV?")
    return float(response)

def set_ddemod_trigger_delay(self, delay_symbols: int):
    """
    Sets the trigger delay (number of symbols after trigger to start measurement).
    """
    self.instrument.write(f":TRIG:DDEMOD:DELAY {delay_symbols}")

def get_ddemod_trigger_delay(self) -> int:
    """
    Queries the trigger delay for digital demodulation.
    """
    response = self.instrument.query(":TRIG:DDEMOD:DELAY?")
    return int(response)

# --- Digital Demodulation Sync Search Controls ---

def enable_ddemod_sync_search(self, enable: bool):
    """
    Enables or disables sync search.
    """
    self.instrument.write(f":SENS:DDEMOD:SYNC {1 if enable else 0}")

def is_ddemod_sync_search_enabled(self) -> bool:
    """
    Queries if sync search is enabled.
    """
    response = self.instrument.query(":SENS:DDEMOD:SYNC?")
    return int(response) == 1

def set_ddemod_sync_pattern(self, pattern: str):
    """
    Sets the sync search pattern (hex string).
    """
    self.instrument.write(f":SENS:DDEMOD:SYNC:SWOR:PATT {pattern.upper()}")

def get_ddemod_sync_pattern(self) -> str:
    """
    Queries the sync search pattern.
    """
    response = self.instrument.query(":SENS:DDEMOD:SYNC:SWOR:PATT?")
    return response.strip().upper()

def set_ddemod_sync_pattern_length(self, length: int):
    """
    Sets the length in symbols of the pattern trigger.
    """
    self.instrument.write(f":SENS:DDEMOD:SYNC:SWOR:LENG {length}")

def get_ddemod_sync_pattern_length(self) -> int:
    """
    Queries the length in symbols of the pattern trigger.
    """
    response = self.instrument.query(":SENS:DDEMOD:SYNC:SWOR:LENG?")
    return int(response)

def set_ddemod_sync_search_length(self, length: int):
    """
    Sets the search length for the pattern trigger.
    """
    self.instrument.write(f":SENS:DDEMOD:SYNC:SLEN {length}")

def get_ddemod_sync_search_length(self) -> int:
    """
    Queries the search length for the pattern trigger.
    """
    response = self.instrument.query(":SENS:DDEMOD:SYNC:SLEN?")
    return int(response)

def set_ddemod_sync_offset(self, offset: int):
    """
    Sets the offset from the beginning of a successful sync search.
    """
    self.instrument.write(f":SENS:DDEMOD:SYNC:OFFS {offset}")

def get_ddemod_sync_offset(self) -> int:
    """
    Queries the offset from the beginning of a successful sync search.
    """
    response = self.instrument.query(":SENS:DDEMOD:SYNC:OFFS?")
    return int(response)

# --- Digital Demodulation Compensation Controls ---

def enable_ddemod_compensate_iq_inversion(self, enable: bool):
    """
    Enables or disables IQ inversion compensation.
    """
    self.instrument.write(f":SENS:DDEMOD:COMP:IQINV {1 if enable else 0}")

def is_ddemod_compensate_iq_inversion_enabled(self) -> bool:
    """
    Queries if IQ inversion compensation is enabled.
    """
    response = self.instrument.query(":SENS:DDEMOD:COMP:IQINV?")
    return int(response) == 1

def enable_ddemod_compensate_iq_offset(self, enable: bool):
    """
    Enables or disables IQ offset compensation.
    """
    self.instrument.write(f":SENS:DDEMOD:COMP:IQOFF {1 if enable else 0}")

def is_ddemod_compensate_iq_offset_enabled(self) -> bool:
    """
    Queries if IQ offset compensation is enabled.
    """
    response = self.instrument.query(":SENS:DDEMOD:COMP:IQOFF?")
    return int(response) == 1

def enable_ddemod_compensate_ad_droop(self, enable: bool):
    """
    Enables or disables amplitude droop compensation.
    """
    self.instrument.write(f":SENS:DDEMOD:COMP:ADR {1 if enable else 0}")

def is_ddemod_compensate_ad_droop_enabled(self) -> bool:
    """
    Queries if amplitude droop compensation is enabled.
    """
    response = self.instrument.query(":SENS:DDEMOD:COMP:ADR?")
    return int(response) == 1

# --- Digital Demodulation Equalization Controls ---

def enable_ddemod_equalization(self, enable: bool):
    """
    Enables or disables adaptive equalization.
    """
    self.instrument.write(f":SENS:DDEMOD:EQU {1 if enable else 0}")

def is_ddemod_equalization_enabled(self) -> bool:
    """
    Queries if adaptive equalization is enabled.
    """
    response = self.instrument.query(":SENS:DDEMOD:EQU?")
    return int(response) == 1

def set_ddemod_equalization_length(self, length: int):
    """
    Sets the length of the equalization filter in symbols (must be odd).
    """
    self.instrument.write(f":SENS:DDEMOD:EQU:LENG {length}")

def get_ddemod_equalization_length(self) -> int:
    """
    Queries the length of the equalization filter in symbols.
    """
    response = self.instrument.query(":SENS:DDEMOD:EQU:LENG?")
    return int(response)

def set_ddemod_equalization_convergence(self, convergence: float):
    """
    Sets the adaptive rate for equalization.
    """
    self.instrument.write(f":SENS:DDEMOD:EQU:CONV {convergence}")

def get_ddemod_equalization_convergence(self) -> float:
    """
    Queries the adaptive rate for equalization.
    """
    response = self.instrument.query(":SENS:DDEMOD:EQU:CONV?")
    return float(response)

def enable_ddemod_equalization_hold(self, enable: bool):
    """
    Enables or disables hold for equalization.
    """
    self.instrument.write(f":SENS:DDEMOD:EQU:HOLD {1 if enable else 0}")

def is_ddemod_equalization_hold_enabled(self) -> bool:
    """
    Queries if hold is enabled for equalization.
    """
    response = self.instrument.query(":SENS:DDEMOD:EQU:HOLD?")
    return int(response) == 1

def reset_ddemod_equalization(self):
    """
    Resets the equalization filter to the unit impulse response.
    """
    self.instrument.write(":SENS:DDEMOD:EQU:RESET")

# --- Digital Demodulation Trace Sweep Controls ---

def get_ddemod_trace_sweep_xstart(self) -> float:
    """
    Gets the frequency value associated with the first sample in the returned data.
    """
    response = self.instrument.query(":SENS:DDEMOD:TRAC:SWE:XSTAR?")
    return float(response)

def get_ddemod_trace_sweep_xincrement(self) -> float:
    """
    Gets the frequency spacing for the samples in the returned data.
    """
    response = self.instrument.query(":SENS:DDEMOD:TRAC:SWE:XINC?")
    return float(response)

def get_ddemod_trace_sweep_points(self) -> int:
    """
    Gets the number of points returned by the DATA function.
    """
    response = self.instrument.query(":SENS:DDEMOD:TRAC:SWE:POIN?")
    return int(response)

def get_ddemod_trace_sweep_data(self) -> list:
    """
    Gets the spectrum trace data.
    """
    response = self.instrument.query(":SENS:DDEMOD:TRAC:SWE:DATA?")
    return [float(x) for x in response.split(',') if x.strip()]

# --- Digital Demodulation Fetch Results ---

def fetch_ddemod_metrics(self, metrics: list) -> list:
    """
    Fetches digital demodulation metrics.
    metrics: list of metric indices (see documentation for allowed values).
    Returns: list of metric values in the order requested.
    """
    metrics_str = ",".join(str(m) for m in metrics)
    response = self.instrument.query(f":FETC:DDEMOD? {metrics_str}")
    return [float(val) for val in response.split(',') if val.strip()]

def fetch_ddemod_constellation_length(self) -> int:
    """
    Returns the constellation result length.
    """
    response = self.instrument.query(":FETC:DDEMOD? 40")
    return int(response)

def fetch_ddemod_constellation_data(self) -> list:
    """
    Returns the constellation results (I/Q values or frequency samples).
    """
    response = self.instrument.query(":FETC:DDEMOD? 41")
    return [float(x) for x in response.split(',') if x.strip()]

# --- SEM (Spectrum Emission Mask) Frequency Controls ---

def set_sem_center_frequency(self, frequency_hz: float):
    """
    Sets the center frequency for SEM measurement.
    """
    self.instrument.write(f":SENS:SEMASK:FREQ:CENT {frequency_hz}")

def get_sem_center_frequency(self) -> float:
    """
    Queries the center frequency for SEM measurement.
    """
    response = self.instrument.query(":SENS:SEMASK:FREQ:CENT?")
    return float(response)

def set_sem_center_frequency_step(self, step_hz: float):
    """
    Sets the center frequency step amount for SEM measurement.
    """
    self.instrument.write(f":SENS:SEMASK:FREQ:CENT:STEP {step_hz}")

def get_sem_center_frequency_step(self) -> float:
    """
    Queries the center frequency step amount for SEM measurement.
    """
    response = self.instrument.query(":SENS:SEMASK:FREQ:CENT:STEP?")
    return float(response)

def set_sem_span(self, span_hz: float):
    """
    Sets the sweep span for SEM measurement.
    """
    self.instrument.write(f":SENS:SEMASK:FREQ:SPAN {span_hz}")

def get_sem_span(self) -> float:
    """
    Queries the sweep span for SEM measurement.
    """
    response = self.instrument.query(":SENS:SEMASK:FREQ:SPAN?")
    return float(response)

# --- SEM Bandwidth Controls ---

def set_sem_bandwidth_resolution(self, rbw_hz: float):
    """
    Sets the RBW for SEM measurement.
    """
    self.instrument.write(f":SENS:SEMASK:BAND:RES {rbw_hz}")

def get_sem_bandwidth_resolution(self) -> float:
    """
    Queries the RBW for SEM measurement.
    """
    response = self.instrument.query(":SENS:SEMASK:BAND:RES?")
    return float(response)

def enable_sem_bandwidth_resolution_auto(self, enable: bool):
    """
    Enables/disables auto RBW for SEM measurement.
    """
    self.instrument.write(f":SENS:SEMASK:BAND:RES:AUTO {1 if enable else 0}")

def is_sem_bandwidth_resolution_auto_enabled(self) -> bool:
    """
    Queries if auto RBW is enabled for SEM measurement.
    """
    response = self.instrument.query(":SENS:SEMASK:BAND:RES:AUTO?")
    return int(response) == 1

def set_sem_bandwidth_video(self, vbw_hz: float):
    """
    Sets the VBW for SEM measurement.
    """
    self.instrument.write(f":SENS:SEMASK:BAND:VID {vbw_hz}")

def get_sem_bandwidth_video(self) -> float:
    """
    Queries the VBW for SEM measurement.
    """
    response = self.instrument.query(":SENS:SEMASK:BAND:VID?")
    return float(response)

def enable_sem_bandwidth_video_auto(self, enable: bool):
    """
    Enables/disables auto VBW for SEM measurement.
    """
    self.instrument.write(f":SENS:SEMASK:BAND:VID:AUTO {1 if enable else 0}")

def is_sem_bandwidth_video_auto_enabled(self) -> bool:
    """
    Queries if auto VBW is enabled for SEM measurement.
    """
    response = self.instrument.query(":SENS:SEMASK:BAND:VID:AUTO?")
    return int(response) == 1

# --- SEM Amplitude Controls ---

def set_sem_power_reference_level(self, ref_level_dbm: float):
    """
    Sets the reference level for SEM measurement.
    """
    self.instrument.write(f":SENS:POWER:RF:RLEV {ref_level_dbm}")

def get_sem_power_reference_level(self) -> float:
    """
    Queries the reference level for SEM measurement.
    """
    response = self.instrument.query(":SENS:POWER:RF:RLEV?")
    return float(response)

def set_sem_plot_division(self, division_db: float):
    """
    Sets the plot vertical division for SEM measurement.
    """
    self.instrument.write(f":SENS:POWER:RF:PDIV {division_db}")

def get_sem_plot_division(self) -> float:
    """
    Queries the plot vertical division for SEM measurement.
    """
    response = self.instrument.query(":SENS:POWER:RF:PDIV?")
    return float(response)

# --- SEM Detector / Trace Controls ---

def set_sem_detector_function(self, function: str):
    """
    Sets the detector function for SEM measurement.
    Allowed values: 'AVERAGE', 'MINMAX'
    """
    valid = {"AVERAGE", "MINMAX"}
    func_upper = function.upper()
    if func_upper not in valid:
        raise ValueError("Invalid detector function.")
    self.instrument.write(f":SENS:SEMASK:SWE:DET:FUNC {func_upper}")

def get_sem_detector_function(self) -> str:
    """
    Queries the detector function for SEM measurement.
    """
    response = self.instrument.query(":SENS:SEMASK:SWE:DET:FUNC?")
    return response.strip().upper()

def set_sem_detector_units(self, units: str):
    """
    Sets the detector units for SEM measurement.
    Allowed values: 'POWER', 'SAMPLE', 'VOLTAGE', 'LOG'
    """
    valid = {"POWER", "SAMPLE", "VOLTAGE", "LOG"}
    units_upper = units.upper()
    if units_upper not in valid:
        raise ValueError("Invalid detector units.")
    self.instrument.write(f":SENS:SEMASK:SWE:DET:UNIT {units_upper}")

def get_sem_detector_units(self) -> str:
    """
    Queries the detector units for SEM measurement.
    """
    response = self.instrument.query(":SENS:SEMASK:SWE:DET:UNIT?")
    return response.strip().upper()

def set_sem_trace_type(self, trace_type: str):
    """
    Sets the trace type for SEM measurement.
    Allowed values: 'WRITE', 'MAXHOLD'
    """
    valid = {"WRITE", "MAXHOLD"}
    trace_type_upper = trace_type.upper()
    if trace_type_upper not in valid:
        raise ValueError("Invalid trace type.")
    self.instrument.write(f":TRAC:SEMASK:TYPE {trace_type_upper}")

def get_sem_trace_type(self) -> str:
    """
    Queries the trace type for SEM measurement.
    """
    response = self.instrument.query(":TRAC:SEMASK:TYPE?")
    return response.strip().upper()

# --- SEM Reference Controls ---

def set_sem_reference_type(self, ref_type: str):
    """
    Sets the reference type for SEM mask construction.
    Allowed values: 'PSD', 'PEAK', 'DIRECT'
    """
    valid_types = {"PSD", "PEAK", "DIRECT"}
    ref_type_upper = ref_type.upper()
    if ref_type_upper not in valid_types:
        raise ValueError(f"Invalid reference type: '{ref_type}'. Must be one of {valid_types}.")
    self.instrument.write(f":SENS:SEMASK:REF:TYPE {ref_type_upper}")

def get_sem_reference_type(self) -> str:
    """
    Queries the reference type for SEM mask construction.
    Returns:
    str: The reference type ('PSD', 'PEAK', 'DIRECT').
    """
    response = self.instrument.query(":SENS:SEMASK:REF:TYPE?")
    return response.strip().upper()

def set_sem_reference_bandwidth_mode(self, mode: str):
    """
    Sets the reference bandwidth mode for SEM mask.
    Allowed values: 'AUTO', 'MANUAL'
    """
    valid_modes = {"AUTO", "MANUAL"}
    mode_upper = mode.upper()
    if mode_upper not in valid_modes:
        raise ValueError(f"Invalid bandwidth mode: '{mode}'. Must be 'AUTO' or 'MANUAL'.")
    self.instrument.write(f":SENS:SEMASK:REF:BAND:MODE {mode_upper}")

def get_sem_reference_bandwidth_mode(self) -> str:
    """
    Queries the reference bandwidth mode for SEM mask.
    Returns:
    str: The bandwidth mode ('AUTO', 'MANUAL').
    """
    response = self.instrument.query(":SENS:SEMASK:REF:BAND:MODE?")
    return response.strip().upper()

def set_sem_reference_bandwidth(self, bandwidth_hz: float):
    """
    Sets the reference bandwidth for SEM mask.
    Parameters:
    bandwidth_hz (float): Reference bandwidth in Hz.
    """
    self.instrument.write(f":SENS:SEMASK:REF:BAND {bandwidth_hz}")

def get_sem_reference_bandwidth(self) -> float:
    """
    Queries the reference bandwidth for SEM mask.
    Returns:
    float: Reference bandwidth in Hz.
    """
    response = self.instrument.query(":SENS:SEMASK:REF:BAND?")
    return float(response)

def set_sem_reference_level(self, level_dbm: float):
    """
    Sets the reference amplitude level for SEM mask.
    Parameters:
    level_dbm (float): Reference level in dBm.
    """
    self.instrument.write(f":SENS:SEMASK:REF:LEVEL {level_dbm}")

def get_sem_reference_level(self) -> float:
    """
    Queries the reference amplitude level for SEM mask.
    Returns:
    float: Reference level in dBm.
    """
    response = self.instrument.query(":SENS:SEMASK:REF:LEVEL?")
    return float(response)

# --- SEM Offset Table Controls ---

def set_sem_offset_data(self, offset_data: list):
    """
    Loads offset table data for SEM mask.
    offset_data: list of tuples (enabled, startFreq, stopFreq, startLimit, stopLimit, mode)
    """
    flat = []
    for entry in offset_data:
        flat.extend(entry)
    data_str = ",".join(str(x) for x in flat)
    self.instrument.write(f":SENS:SEMASK:OFFS:DATA {data_str}")

def get_sem_offset_data(self) -> list:
    """
    Queries the offset table data for SEM mask.
    Returns a list of floats.
    """
    response = self.instrument.query(":SENS:SEMASK:OFFS:DATA?")
    return [float(x) for x in response.split(',') if x.strip()]

# --- SEM Offset Table Measurement Results ---

def get_sem_carrier_power(self) -> float:
    """
    Retrieves the current power used as the reference for the SEM mask.
    Returns:
    float: Carrier power in dBm.
    """
    response = self.instrument.query(":SENS:SEMASK:CARR:POW?")
    return float(response)

def is_sem_offset_fail(self) -> bool:
    """
    Returns True if the current mask fails, False if passes.
    """
    response = self.instrument.query(":SENS:SEMASK:OFFS:FAIL?")
    return int(response) == 1

def is_sem_offset_index_fail(self, index: int) -> bool:
    """
    Returns True if the specified offset fails, False if passes.
    Parameters:
    index (int): Offset index (1-16).
    """
    response = self.instrument.query(f":SENS:SEMASK:OFFS{index}:FAIL?")
    return int(response) == 1

def is_sem_offset_lower_fail(self, index: int) -> bool:
    """
    Returns True if lower range of specified offset fails, False if passes.
    Parameters:
    index (int): Offset index (1-16).
    """
    response = self.instrument.query(f":SENS:SEMASK:OFFS{index}:LOW:FAIL?")
    return int(response) == 1

def is_sem_offset_upper_fail(self, index: int) -> bool:
    """
    Returns True if upper range of specified offset fails, False if passes.
    Parameters:
    index (int): Offset index (1-16).
    """
    response = self.instrument.query(f":SENS:SEMASK:OFFS{index}:UPP:FAIL?")
    return int(response) == 1

def get_sem_offset_margin(self, index: int) -> float:
    """
    Retrieves worst margin (limit - peak) of specified offset.
    Parameters:
    index (int): Offset index (1-16).
    Returns:
    float: Margin value.
    """
    response = self.instrument.query(f":SENS:SEMASK:OFFS{index}:MARG?")
    return float(response)

def get_sem_offset_margin_lower(self, index: int) -> float:
    """
    Retrieves margin (limit - peak) of lower range of specified offset.
    Parameters:
    index (int): Offset index (1-16).
    Returns:
    float: Margin value.
    """
    response = self.instrument.query(f":SENS:SEMASK:OFFS{index}:MARG:LOW?")
    return float(response)

def get_sem_offset_margin_upper(self, index: int) -> float:
    """
    Retrieves margin (limit - peak) of upper range of specified offset.
    Parameters:
    index (int): Offset index (1-16).
    Returns:
    float: Margin value.
    """
    response = self.instrument.query(f":SENS:SEMASK:OFFS{index}:MARG:UPP?")
    return float(response)

def get_sem_offset_peak_level_lower(self, index: int) -> float:
    """
    Retrieves peak level of lower range of specified offset.
    Parameters:
    index (int): Offset index (1-16).
    Returns:
    float: Peak level.
    """
    response = self.instrument.query(f":SENS:SEMASK:OFFS{index}:PEAK:LEV:LOW?")
    return float(response)

def get_sem_offset_peak_level_upper(self, index: int) -> float:
    """
    Retrieves peak level of upper range of specified offset.
    Parameters:
    index (int): Offset index (1-16).
    Returns:
    float: Peak level.
    """
    response = self.instrument.query(f":SENS:SEMASK:OFFS{index}:PEAK:LEV:UPP?")
    return float(response)

def get_sem_offset_peak_frequency_lower(self, index: int) -> float:
    """
    Retrieves frequency at peak of lower range of specified offset.
    Parameters:
    index (int): Offset index (1-16).
    Returns:
    float: Frequency in Hz.
    """
    response = self.instrument.query(f":SENS:SEMASK:OFFS{index}:PEAK:FREQ:LOW?")
    return float(response)

def get_sem_offset_peak_frequency_upper(self, index: int) -> float:
    """
    Retrieves frequency at peak of upper range of specified offset.
    Parameters:
    index (int): Offset index (1-16).
    Returns:
    float: Frequency in Hz.
    """
    response = self.instrument.query(f":SENS:SEMASK:OFFS{index}:PEAK:FREQ:UPP?")
    return float(response)

# --- SEM Marker Controls ---

def enable_sem_marker(self, enable: bool):
    """
    Turns the SEM marker on or off.
    Parameters:
    enable (bool): True to enable, False to disable.
    """
    self.instrument.write(f":CALC:SEMASK:MARK:STAT {1 if enable else 0}")

def is_sem_marker_enabled(self) -> bool:
    """
    Queries if the SEM marker is enabled.
    Returns:
    bool: True if enabled, False otherwise.
    """
    response = self.instrument.query(":CALC:SEMASK:MARK:STAT?")
    return int(response) == 1

def enable_sem_marker_delta(self, enable: bool):
    """
    Enables or disables the delta marker for SEM.
    Parameters:
    enable (bool): True to enable, False to disable.
    """
    self.instrument.write(f":CALC:SEMASK:MARK:DELT {1 if enable else 0}")

def is_sem_marker_delta_enabled(self) -> bool:
    """
    Queries if the delta marker is enabled for SEM.
    Returns:
    bool: True if enabled, False otherwise.
    """
    response = self.instrument.query(":CALC:SEMASK:MARK:DELT?")
    return int(response) == 1

def set_sem_marker_frequency(self, frequency_hz: float):
    """
    Moves the SEM marker to the specified frequency.
    Parameters:
    frequency_hz (float): Frequency in Hz.
    """
    self.instrument.write(f":CALC:SEMASK:MARK:X {frequency_hz}")

def get_sem_marker_frequency(self) -> float:
    """
    Retrieves the SEM marker position frequency in Hz.
    Returns:
    float: Frequency in Hz.
    """
    response = self.instrument.query(":CALC:SEMASK:MARK:X?")
    return float(response)

def get_sem_marker_amplitude(self) -> float:
    """
    Retrieves the SEM marker position amplitude.
    Returns:
    float: Amplitude value.
    """
    response = self.instrument.query(":CALC:SEMASK:MARK:Y?")
    return float(response)

def perform_sem_marker_peak_search(self):
    """
    Performs a peak search for the SEM marker.
    """
    self.instrument.write(":CALC:SEMASK:MARK:MAX")

def perform_sem_marker_min_search(self):
    """
    Performs a minimum search for the SEM marker.
    """
    self.instrument.write(":CALC:SEMASK:MARK:MIN")

def move_sem_marker_to_next(self):
    """
    Moves the SEM marker to the next graph on the plot.
    """
    self.instrument.write(":CALC:SEMASK:MARK:NEXT")

def move_sem_marker_to_previous(self):
    """
    Moves the SEM marker to the previous graph on the plot.
    """
    self.instrument.write(":CALC:SEMASK:MARK:PREV")

# --- Noise Figure Frequency List Controls ---

def set_noise_figure_frequency_mode(self, mode: str):
    """
    Sets how the list of measurement frequencies is determined.
    Allowed values: 'SWEPT', 'FIXED'
    """
    valid_modes = {"SWEPT", "FIXED"}
    mode_upper = mode.upper()
    if mode_upper not in valid_modes:
        raise ValueError(f"Invalid frequency mode: '{mode}'. Must be 'SWEPT' or 'FIXED'.")
    self.instrument.write(f":SENS:NFIG:FREQ:MODE {mode_upper}")

def get_noise_figure_frequency_mode(self) -> str:
    """
    Queries how the list of measurement frequencies is determined.
    Returns:
    str: Frequency mode ('SWEPT' or 'FIXED').
    """
    response = self.instrument.query(":SENS:NFIG:FREQ:MODE?")
    return response.strip().upper()

def set_noise_figure_frequency_start(self, frequency_hz: float):
    """
    Sets the measurement list start frequency in swept mode.
    Parameters:
    frequency_hz (float): Start frequency in Hz.
    """
    self.instrument.write(f":SENS:NFIG:FREQ:STAR {frequency_hz}")

def get_noise_figure_frequency_start(self) -> float:
    """
    Queries the current measurement list start frequency in Hz.
    Returns:
    float: Start frequency in Hz.
    """
    response = self.instrument.query(":SENS:NFIG:FREQ:STAR?")
    return float(response)

def set_noise_figure_frequency_stop(self, frequency_hz: float):
    """
    Sets the measurement list stop frequency in swept mode.
    Parameters:
    frequency_hz (float): Stop frequency in Hz.
    """
    self.instrument.write(f":SENS:NFIG:FREQ:STOP {frequency_hz}")

def get_noise_figure_frequency_stop(self) -> float:
    """
    Queries the current measurement list stop frequency in Hz.
    Returns:
    float: Stop frequency in Hz.
    """
    response = self.instrument.query(":SENS:NFIG:FREQ:STOP?")
    return float(response)

def set_noise_figure_frequency_center(self, frequency_hz: float):
    """
    Sets the measurement list center frequency in swept mode.
    Parameters:
    frequency_hz (float): Center frequency in Hz.
    """
    self.instrument.write(f":SENS:NFIG:FREQ:CENT {frequency_hz}")

def get_noise_figure_frequency_center(self, limit: str = None) -> float:
    """
    Queries the current measurement list center frequency in Hz.
    Optionally pass 'MIN' or 'MAX' to query limits.
    Parameters:
    limit (str): 'MIN' or 'MAX' (optional).
    Returns:
    float: Center frequency in Hz.
    """
    if limit:
        limit_upper = limit.upper()
        if limit_upper not in {"MIN", "MAX"}:
            raise ValueError("limit must be 'MIN' or 'MAX'")
        response = self.instrument.query(f":SENS:NFIG:FREQ:CENT? {limit_upper}")
    else:
        response = self.instrument.query(":SENS:NFIG:FREQ:CENT?")
    return float(response)

def set_noise_figure_frequency_span(self, span_hz: float):
    """
    Sets the measurement list span in swept mode.
    Parameters:
    span_hz (float): Span in Hz.
    """
    self.instrument.write(f":SENS:NFIG:FREQ:SPAN {span_hz}")

def get_noise_figure_frequency_span(self) -> float:
    """
    Queries the measurement list span in Hz.
    Returns:
    float: Span in Hz.
    """
    response = self.instrument.query(":SENS:NFIG:FREQ:SPAN?")
    return float(response)

def set_noise_figure_frequency_points(self, points: int):
    """
    Sets the number of measurement points distributed across the span in swept mode.
    Parameters:
    points (int): Number of points.
    """
    self.instrument.write(f":SENS:NFIG:FREQ:POIN {points}")

def get_noise_figure_frequency_points(self) -> int:
    """
    Queries the number of measurement points.
    Returns:
    int: Number of points.
    """
    response = self.instrument.query(":SENS:NFIG:FREQ:POIN?")
    return int(response)

def set_noise_figure_frequency_fixed(self, frequency_hz: float):
    """
    Sets the frequency of the measurement in fixed mode.
    Parameters:
    frequency_hz (float): Fixed frequency in Hz.
    """
    self.instrument.write(f":SENS:NFIG:FREQ:FIX {frequency_hz}")

def get_noise_figure_frequency_fixed(self) -> float:
    """
    Queries the frequency of the measurement in fixed mode.
    Returns:
    float: Fixed frequency in Hz.
    """
    response = self.instrument.query(":SENS:NFIG:FREQ:FIX?")
    return float(response)

def get_noise_figure_frequency_list_data(self) -> list:
    """
    Gets the list of measurement frequencies in Hz.
    Returns:
    list: List of frequencies in Hz.
    """
    response = self.instrument.query(":SENS:NFIG:FREQ:LIST:DATA?")
    return [float(x) for x in response.split(',') if x.strip()]

# --- Noise Figure Measurement Controls ---

def set_noise_figure_power_reference_level(self, ref_level_dbm: float):
    """
    Sets the reference level for noise figure measurement.
    """
    self.instrument.write(f":SENS:NFIG:POW:RF:RLEV {ref_level_dbm}")

def get_noise_figure_power_reference_level(self) -> float:
    """
    Queries the reference level for noise figure measurement.
    """
    response = self.instrument.query(":SENS:NFIG:POW:RF:RLEV?")
    return float(response)

def set_noise_figure_bandwidth_resolution(self, rbw_hz: float):
    """
    Sets the RBW for noise figure measurement.
    """
    self.instrument.write(f":SENS:NFIG:BAND:RES {rbw_hz}")

def get_noise_figure_bandwidth_resolution(self) -> float:
    """
    Queries the RBW for noise figure measurement.
    """
    response = self.instrument.query(":SENS:NFIG:BAND:RES?")
    return float(response)

def enable_noise_figure_bandwidth_resolution_auto(self, enable: bool):
    """
    Enables/disables auto RBW for noise figure measurement.
    """
    self.instrument.write(f":SENS:NFIG:BAND:RES:AUTO {1 if enable else 0}")

def is_noise_figure_bandwidth_resolution_auto_enabled(self) -> bool:
    """
    Queries if auto RBW is enabled for noise figure measurement.
    """
    response = self.instrument.query(":SENS:NFIG:BAND:RES:AUTO?")
    return int(response) == 1

def set_noise_figure_bandwidth_video(self, vbw_hz: float):
    """
    Sets the VBW for noise figure measurement.
    """
    self.instrument.write(f":SENS:NFIG:BAND:VID {vbw_hz}")

def get_noise_figure_bandwidth_video(self) -> float:
    """
    Queries the VBW for noise figure measurement.
    """
    response = self.instrument.query(":SENS:NFIG:BAND:VID?")
    return float(response)

def enable_noise_figure_bandwidth_video_auto(self, enable: bool):
    """
    Enables/disables auto VBW for noise figure measurement.
    """
    self.instrument.write(f":SENS:NFIG:BAND:VID:AUTO {1 if enable else 0}")

def is_noise_figure_bandwidth_video_auto_enabled(self) -> bool:
    """
    Queries if auto VBW is enabled for noise figure measurement.
    """
    response = self.instrument.query(":SENS:NFIG:BAND:VID:AUTO?")
    return int(response) == 1

def set_noise_figure_meas_span(self, span_hz: float):
    """
    Sets the span for noise figure measurement.
    """
    self.instrument.write(f":SENS:NFIG:MEAS:SPAN {span_hz}")

def get_noise_figure_meas_span(self) -> float:
    """
    Queries the span for noise figure measurement.
    """
    response = self.instrument.query(":SENS:NFIG:MEAS:SPAN?")
    return float(response)

def enable_noise_figure_averaging(self, enable: bool):
    """
    Enables/disables averaging for noise figure measurement.
    """
    self.instrument.write(f":SENS:NFIG:AVER {1 if enable else 0}")

def is_noise_figure_averaging_enabled(self) -> bool:
    """
    Queries if averaging is enabled for noise figure measurement.
    """
    response = self.instrument.query(":SENS:NFIG:AVER?")
    return int(response) == 1

def set_noise_figure_average_count(self, count: int):
    """
    Sets the number of sweeps to average for noise figure measurement.
    """
    self.instrument.write(f":SENS:NFIG:AVER:COUN {count}")

def get_noise_figure_average_count(self) -> int:
    """
    Queries the number of sweeps averaged for noise figure measurement.
    """
    response = self.instrument.query(":SENS:NFIG:AVER:COUN?")
    return int(response)

def set_noise_figure_cold_temperature(self, temp_kelvin: float):
    """
    Sets the room temperature for noise figure measurement (Kelvin).
    """
    self.instrument.write(f":SENS:NFIG:CORR:TCOLD:VAL {temp_kelvin}")

def get_noise_figure_cold_temperature(self) -> float:
    """
    Queries the room temperature for noise figure measurement (Kelvin).
    """
    response = self.instrument.query(":SENS:NFIG:CORR:TCOLD:VAL?")
    return float(response)

def enable_noise_figure_alert(self, enable: bool):
    """
    Enables/disables alert beep on sweep completion.
    """
    self.instrument.write(f":SENS:NFIG:ALERT {1 if enable else 0}")

def is_noise_figure_alert_enabled(self) -> bool:
    """
    Queries if alert beep is enabled on sweep completion.
    """
    response = self.instrument.query(":SENS:NFIG:ALERT?")
    return int(response) == 1

# --- Noise Figure ENR Table Controls ---

def get_noise_figure_enr_table_count(self) -> int:
    """
    Queries the count of ENR tables.
    """
    response = self.instrument.query(":SENS:NFIG:CORR:ENR:TABL:COUN?")
    return int(response)

def create_noise_figure_enr_table(self):
    """
    Creates a new ENR table.
    """
    self.instrument.write(":SENS:NFIG:CORR:ENR:TABL:NEW")

def load_noise_figure_enr_table(self, table_id: int):
    """
    Loads an ENR table by ID.
    """
    self.instrument.write(f":SENS:NFIG:CORR:ENR:TABL:LOAD {table_id}")

def get_noise_figure_enr_table_id(self) -> int:
    """
    Queries the ID of the currently loaded ENR table.
    """
    response = self.instrument.query(":SENS:NFIG:CORR:ENR:TABL?")
    return int(response)

def set_noise_figure_enr_table_title(self, title: str):
    """
    Sets the title of the currently loaded ENR table.
    """
    self.instrument.write(f":SENS:NFIG:CORR:ENR:TABL:TITL {title}")

def get_noise_figure_enr_table_title(self) -> str:
    """
    Queries the title of the loaded ENR table.
    """
    response = self.instrument.query(":SENS:NFIG:CORR:ENR:TABL:TITL?")
    return response.strip()

def get_noise_figure_enr_table_points(self) -> int:
    """
    Queries the number of points in the loaded ENR table.
    """
    response = self.instrument.query(":SENS:NFIG:CORR:ENR:TABL:POIN?")
    return int(response)

def set_noise_figure_enr_table_data(self, data: list):
    """
    Sets the (frequency, enr) points in the loaded ENR table.
    data: list of tuples (frequency, enr)
    """
    flat = []
    for entry in data:
        flat.extend(entry)
    data_str = ",".join(str(x) for x in flat)
    self.instrument.write(f":SENS:NFIG:CORR:ENR:TABL:DATA {data_str}")

def get_noise_figure_enr_table_data(self) -> list:
    """
    Gets the list of points in the loaded ENR table.
    """
    response = self.instrument.query(":SENS:NFIG:CORR:ENR:TABL:DATA?")
    return [float(x) for x in response.split(',') if x.strip()]

def set_noise_figure_enr_calibration_table(self, table_id: int):
    """
    Specifies which ENR table will be used for calibration.
    """
    self.instrument.write(f":SENS:NFIG:CORR:ENR:CAL:TABL {table_id}")

def get_noise_figure_enr_calibration_table(self) -> int:
    """
    Queries the calibration ENR table.
    """
    response = self.instrument.query(":SENS:NFIG:CORR:ENR:CAL:TABL?")
    return int(response)

def set_noise_figure_enr_measurement_table(self, table_id: int):
    """
    Specifies which ENR table will be used for measurement.
    """
    self.instrument.write(f":SENS:NFIG:CORR:ENR:MEAS:TABL {table_id}")

def get_noise_figure_enr_measurement_table(self) -> int:
    """
    Queries the measurement ENR table.
    """
    response = self.instrument.query(":SENS:NFIG:CORR:ENR:MEAS:TABL?")
    return int(response)

# --- Noise Figure Calibration and Measurement Controls ---

def get_noise_figure_calibration_state(self) -> str:
    """
    Returns the current calibration state: 'UNCAL', 'SEMICAL', or 'CAL'.
    """
    response = self.instrument.query(":SENS:NFIG:CAL:STAT?")
    return response.strip().upper()

def initiate_noise_figure_calibration(self):
    """
    Begins the calibration process.
    """
    self.instrument.write(":SENS:NFIG:CAL:INIT")

def initiate_noise_figure_measurement(self):
    """
    Begins the measurement process.
    """
    self.instrument.write(":SENS:NFIG:MEAS:INIT")

def continue_noise_figure(self):
    """
    Continues calibration or measurement after the next action.
    """
    self.instrument.write(":SENS:NFIG:CONT")

def abort_noise_figure(self):
    """
    Stops any calibration or measurement in progress.
    """
    self.instrument.write(":SENS:NFIG:ABOR")

def get_noise_figure_next_action(self) -> str:
    """
    Queries the next action user needs to take before continuing measurement.
    """
    response = self.instrument.query(":STAT:NFIG:NEXT?")
    return response.strip()

def get_noise_figure_progress(self) -> float:
    """
    Queries the percentage progress of the current sweep.
    """
    response = self.instrument.query(":STAT:NFIG:PROG?")
    return float(response)

# --- Noise Figure Fetch Results ---

def fetch_noise_figure(self) -> list:
    """
    Fetches the list of noise figure measurements for each point in the frequency list.
    """
    response = self.instrument.query(":FETC:NFIG?")
    return [float(x) for x in response.split(',') if x.strip()]

def fetch_noise_figure_gain(self) -> list:
    """
    Fetches the list of gain measurements for each point in the frequency list.
    """
    response = self.instrument.query(":FETC:NFIG:GAIN?")
    return [float(x) for x in response.split(',') if x.strip()]

# --- BLE Measurement Controls ---

def set_ble_measurement(self, meas_type: str):
    """
    Sets the active Bluetooth measurement type.
    Allowed values: 'DEMOD', 'IBE'
    """
    valid_types = {"DEMOD", "IBE"}
    meas_type_upper = meas_type.upper()
    if meas_type_upper not in valid_types:
        raise ValueError(f"Invalid BLE measurement type: '{meas_type}'. Must be 'DEMOD' or 'IBE'.")
    self.instrument.write(f":SENS:BLE:MEAS {meas_type_upper}")

def get_ble_measurement(self) -> str:
    """
    Queries the active Bluetooth measurement type.
    """
    response = self.instrument.query(":SENS:BLE:MEAS?")
    return response.strip().upper()

def set_ble_center_frequency(self, frequency_hz: float):
    """
    Sets the center frequency for BLE measurement.
    """
    self.instrument.write(f":SENS:BLE:FREQ:CENT {frequency_hz}")

def get_ble_center_frequency(self) -> float:
    """
    Queries the center frequency for BLE measurement.
    """
    response = self.instrument.query(":SENS:BLE:FREQ:CENT?")
    return float(response)

def set_ble_center_frequency_step(self, step_hz: float):
    """
    Sets the center frequency step size for BLE measurement.
    """
    self.instrument.write(f":SENS:BLE:FREQ:CENT:STEP {step_hz}")

def get_ble_center_frequency_step(self) -> float:
    """
    Queries the center frequency step size for BLE measurement.
    """
    response = self.instrument.query(":SENS:BLE:FREQ:CENT:STEP?")
    return float(response)

def set_ble_if_bandwidth(self, bandwidth_hz: float):
    """
    Sets the IF bandwidth for BLE measurement.
    """
    self.instrument.write(f":SENS:BLE:IFBW {bandwidth_hz}")

def get_ble_if_bandwidth(self) -> float:
    """
    Queries the IF bandwidth for BLE measurement.
    """
    response = self.instrument.query(":SENS:BLE:IFBW?")
    return float(response)

def set_ble_channel_index(self, index: int):
    """
    Sets the BLE channel index.
    """
    self.instrument.write(f":SENS:BLE:CHAN:INDEX {index}")

def get_ble_channel_index(self) -> int:
    """
    Queries the BLE channel index.
    """
    response = self.instrument.query(":SENS:BLE:CHAN:INDEX?")
    return int(response)

def enable_ble_channel_auto(self, enable: bool):
    """
    Enables/disables auto channel index for BLE measurement.
    """
    self.instrument.write(f":SENS:BLE:CHAN:AUTO {1 if enable else 0}")

def is_ble_channel_auto_enabled(self) -> bool:
    """
    Queries if auto channel index is enabled for BLE measurement.
    """
    response = self.instrument.query(":SENS:BLE:CHAN:AUTO?")
    return int(response) == 1

def set_ble_power_reference_level(self, ref_level_dbm: float):
    """
    Sets the reference level for BLE measurement.
    """
    self.instrument.write(f":SENS:BLE:POW:RF:RLEV {ref_level_dbm}")

def get_ble_power_reference_level(self) -> float:
    """
    Queries the reference level for BLE measurement.
    """
    response = self.instrument.query(":SENS:BLE:POW:RF:RLEV?")
    return float(response)

# --- BLE Trigger Controls ---

def set_ble_trigger_search_length(self, time_s: float):
    """
    Sets the measurement capture length for BLE trigger.
    """
    self.instrument.write(f":TRIG:BLE:SLEN {time_s}")

def get_ble_trigger_search_length(self) -> float:
    """
    Queries the measurement capture length for BLE trigger.
    """
    response = self.instrument.query(":TRIG:BLE:SLEN?")
    return float(response)

# --- BLE Fetch Results ---

def fetch_ble_metrics(self, metrics: list) -> list:
    """
    Fetches BLE demodulation metrics.
    metrics: list of metric indices.
    Returns: list of metric values in the order requested.
    """
    metrics_str = ",".join(str(m) for m in metrics)
    response = self.instrument.query(f":FETC:BLE {metrics_str}")
    return [float(val) for val in response.split(',') if val.strip()]

# --- WLAN Measurement Controls ---

def set_wlan_standard(self, standard: str):
    """
    Sets the WLAN modulation standard.
    Allowed values: 'BG', 'AG', 'N20', 'N40', 'AC20', 'AC40', 'AH'
    """
    valid_standards = {"BG", "AG", "N20", "N40", "AC20", "AC40", "AH"}
    standard_upper = standard.upper()
    if standard_upper not in valid_standards:
        raise ValueError(f"Invalid WLAN standard: '{standard}'. Must be one of {valid_standards}.")
    self.instrument.write(f":SENS:WLAN:STAN {standard_upper}")

def get_wlan_standard(self) -> str:
    """
    Queries the WLAN modulation standard.
    """
    response = self.instrument.query(":SENS:WLAN:STAN?")
    return response.strip().upper()

def set_wlan_symbols_dsss(self, count: int):
    """
    Sets the number of DSSS symbols to demodulate/decode.
    """
    self.instrument.write(f":SENS:WLAN:SYMB:DSSS {count}")

def get_wlan_symbols_dsss(self) -> int:
    """
    Queries the number of DSSS symbols to demodulate/decode.
    """
    response = self.instrument.query(":SENS:WLAN:SYMB:DSSS?")
    return int(response)

def enable_wlan_psdu_decode(self, enable: bool):
    """
    Enables/disables OFDM PSDU decoding for BCC encoded waveforms.
    """
    self.instrument.write(f":SENS:WLAN:PSDU:DEC {1 if enable else 0}")

def is_wlan_psdu_decode_enabled(self) -> bool:
    """
    Queries if OFDM PSDU decoding is enabled.
    """
    response = self.instrument.query(":SENS:WLAN:PSDU:DEC?")
    return int(response) == 1

def set_wlan_symbol_offset(self, offset_percent: float):
    """
    Sets the GI timing offset between -100 and 0 (%).
    """
    self.instrument.write(f":SENS:WLAN:SYMB:OFFS {offset_percent}")

def get_wlan_symbol_offset(self) -> float:
    """
    Queries the GI timing offset.
    """
    response = self.instrument.query(":SENS:WLAN:SYMB:OFFS?")
    return float(response)

def set_wlan_center_frequency(self, frequency_hz: float):
    """
    Sets the center frequency for WLAN measurement.
    """
    self.instrument.write(f":SENS:WLAN:FREQ:CENT {frequency_hz}")

def get_wlan_center_frequency(self) -> float:
    """
    Queries the center frequency for WLAN measurement.
    """
    response = self.instrument.query(":SENS:WLAN:FREQ:CENT?")
    return float(response)

def set_wlan_center_frequency_step(self, step_hz: float):
    """
    Sets the center frequency step size for WLAN measurement.
    """
    self.instrument.write(f":SENS:WLAN:FREQ:CENT:STEP {step_hz}")

def get_wlan_center_frequency_step(self) -> float:
    """
    Queries the center frequency step size for WLAN measurement.
    """
    response = self.instrument.query(":SENS:WLAN:FREQ:CENT:STEP?")
    return float(response)

def set_wlan_if_bandwidth(self, bandwidth_hz: float):
    """
    Sets the IF bandwidth for WLAN measurement.
    """
    self.instrument.write(f":SENS:WLAN:IFBW {bandwidth_hz}")

def get_wlan_if_bandwidth(self) -> float:
    """
    Queries the IF bandwidth for WLAN measurement.
    """
    response = self.instrument.query(":SENS:WLAN:IFBW?")
    return float(response)

def set_wlan_power_reference_level(self, ref_level_dbm: float):
    """
    Sets the reference level for WLAN measurement.
    """
    self.instrument.write(f":SENS:WLAN:POW:RF:RLEV {ref_level_dbm}")

def get_wlan_power_reference_level(self) -> float:
    """
    Queries the reference level for WLAN measurement.
    """
    response = self.instrument.query(":SENS:WLAN:POW:RF:RLEV?")
    return float(response)

# --- WLAN Trigger Controls ---

def set_wlan_trigger_search_length(self, time_s: float):
    """
    Sets the measurement capture length for WLAN trigger.
    """
    self.instrument.write(f":TRIG:WLAN:SLEN {time_s}")

def get_wlan_trigger_search_length(self) -> float:
    """
    Queries the measurement capture length for WLAN trigger.
    """
    response = self.instrument.query(":TRIG:WLAN:SLEN?")
    return float(response)

def set_wlan_trigger_if_threshold(self, threshold_db: float):
    """
    Sets the OFDM trigger threshold in dB.
    """
    self.instrument.write(f":TRIG:WLAN:IF:THR {threshold_db}")

def get_wlan_trigger_if_threshold(self) -> float:
    """
    Queries the OFDM trigger threshold in dB.
    """
    response = self.instrument.query(":TRIG:WLAN:IF:THR?")
    return float(response)

def set_wlan_trigger_if_level(self, level_dbm: float):
    """
    Sets the DSSS video trigger level in dBm.
    """
    self.instrument.write(f":TRIG:WLAN:IF:LEV {level_dbm}")

def get_wlan_trigger_if_level(self) -> float:
    """
    Queries the DSSS video trigger level in dBm.
    """
    response = self.instrument.query(":TRIG:WLAN:IF:LEV?")
    return float(response)

# --- WLAN Fetch Results ---

def fetch_wlan_metrics(self, metrics: list) -> list:
    """
    Fetches WLAN demodulation metrics.
    metrics: list of metric indices.
    Returns: list of metric values in the order requested.
    """
    metrics_str = ",".join(str(m) for m in metrics)
    response = self.instrument.query(f":FETC:WLAN {metrics_str}")
    return [val.strip() for val in response.split(',') if val.strip()]

# --- LTE Measurement Controls ---

def set_lte_center_frequency(self, frequency_hz: float):
    """
    Sets the center frequency for LTE measurement.
    """
    self.instrument.write(f":SENS:LTE:FREQ:CENT {frequency_hz}")

def get_lte_center_frequency(self) -> float:
    """
    Queries the center frequency for LTE measurement.
    """
    response = self.instrument.query(":SENS:LTE:FREQ:CENT?")
    return float(response)

def set_lte_center_frequency_step(self, step_hz: float):
    """
    Sets the center frequency step for LTE measurement.
    """
    self.instrument.write(f":SENS:LTE:FREQ:CENT:STEP {step_hz}")

def get_lte_center_frequency_step(self) -> float:
    """
    Queries the center frequency step for LTE measurement.
    """
    response = self.instrument.query(":SENS:LTE:FREQ:CENT:STEP?")
    return float(response)

def set_lte_correlation_threshold(self, threshold: float):
    """
    Sets the cell search correlation threshold (0-1).
    """
    if not (0 <= threshold <= 1):
        raise ValueError("Threshold must be between 0 and 1.")
    self.instrument.write(f":SENS:LTE:CORR:THR {threshold}")

def get_lte_correlation_threshold(self) -> float:
    """
    Queries the cell search correlation threshold.
    """
    response = self.instrument.query(":SENS:LTE:CORR:THR?")
    return float(response)

def set_lte_power_reference_level(self, ref_level_dbm: float):
    """
    Sets the reference level for LTE measurement.
    """
    self.instrument.write(f":SENS:LTE:POW:RF:RLEV {ref_level_dbm}")

def get_lte_power_reference_level(self) -> float:
    """
    Queries the reference level for LTE measurement.
    """
    response = self.instrument.query(":SENS:LTE:POW:RF:RLEV?")
    return float(response)

def enable_lte_measurement_include(self, enable: bool):
    """
    Enables/disables inclusion of single frequency measurements in cell search results.
    """
    self.instrument.write(f":SENS:LTE:MEAS:INCL {1 if enable else 0}")

def is_lte_measurement_include_enabled(self) -> bool:
    """
    Queries if inclusion of single frequency measurements in cell search results is enabled.
    """
    response = self.instrument.query(":SENS:LTE:MEAS:INCL?")
    return int(response) == 1

def set_lte_scan_type(self, scan_type: str):
    """
    Sets the LTE scan type. Allowed values: 'SINGLE', 'CONTINUOUS'
    """
    valid_types = {"SINGLE", "CONTINUOUS"}
    scan_type_upper = scan_type.upper()
    if scan_type_upper not in valid_types:
        raise ValueError(f"Invalid scan type: '{scan_type}'. Must be 'SINGLE' or 'CONTINUOUS'.")
    self.instrument.write(f":SENS:LTE:SCAN:TYPE {scan_type_upper}")

def get_lte_scan_type(self) -> str:
    """
    Queries the LTE scan type.
    """
    response = self.instrument.query(":SENS:LTE:SCAN:TYPE?")
    return response.strip().upper()

def set_lte_scan_results_sort(self, sort_type: str):
    """
    Sets how cell search result entries are sorted. Allowed values: 'RSSI', 'FREQUENCY', 'TIME'
    """
    valid_types = {"RSSI", "FREQUENCY", "TIME"}
    sort_type_upper = sort_type.upper()
    if sort_type_upper not in valid_types:
        raise ValueError(f"Invalid sort type: '{sort_type}'. Must be 'RSSI', 'FREQUENCY', or 'TIME'.")
    self.instrument.write(f":SENS:LTE:SCAN:RES:SORT {sort_type_upper}")

def get_lte_scan_results_sort(self) -> str:
    """
    Queries how cell search result entries are sorted.
    """
    response = self.instrument.query(":SENS:LTE:SCAN:RES:SORT?")
    return response.strip().upper()

def set_lte_scan_results_keep(self, keep_type: str):
    """
    Sets which measurement is displayed for grouped results. Allowed values: 'LAST', 'PEAK'
    """
    valid_types = {"LAST", "PEAK"}
    keep_type_upper = keep_type.upper()
    if keep_type_upper not in valid_types:
        raise ValueError(f"Invalid keep type: '{keep_type}'. Must be 'LAST' or 'PEAK'.")
    self.instrument.write(f":SENS:LTE:SCAN:RES:KEEP {keep_type_upper}")

def get_lte_scan_results_keep(self) -> str:
    """
    Queries which measurement is displayed for grouped results.
    """
    response = self.instrument.query(":SENS:LTE:SCAN:RES:KEEP?")
    return response.strip().upper()

def enable_lte_scan_results_group(self, enable: bool):
    """
    Enables/disables cell search result grouping.
    """
    self.instrument.write(f":SENS:LTE:SCAN:RES:GROUP {1 if enable else 0}")

def is_lte_scan_results_group_enabled(self) -> bool:
    """
    Queries if cell search result grouping is enabled.
    """
    response = self.instrument.query(":SENS:LTE:SCAN:RES:GROUP?")
    return int(response) == 1

def set_lte_scan_results_max(self, max_entries: int):
    """
    Sets the maximum number of entries visible in the cell search results window.
    """
    self.instrument.write(f":SENS:LTE:SCAN:RES:MAX {max_entries}")

def get_lte_scan_results_max(self) -> int:
    """
    Queries the maximum number of entries visible in the cell search results window.
    """
    response = self.instrument.query(":SENS:LTE:SCAN:RES:MAX?")
    return int(response)

def start_lte_scan(self) -> bool:
    """
    Starts the LTE scan. Returns True once started.
    """
    response = self.instrument.query(":SENS:LTE:SCAN:STAR?")
    return int(response) == 1

def is_lte_scan_active(self) -> bool:
    """
    Returns True if the LTE scan is active.
    """
    response = self.instrument.query(":SENS:LTE:SCAN:ACT?")
    return int(response) == 1

def stop_lte_scan(self) -> bool:
    """
    Stops the LTE scan. Returns True when complete.
    """
    response = self.instrument.query(":SENS:LTE:SCAN:STOP?")
    return int(response) == 1

def get_lte_scan_results_count(self) -> int:
    """
    Returns the number of rows in the cell scan results table.
    """
    response = self.instrument.query(":SENS:LTE:SCAN:RES:COUN?")
    return int(response)

def set_lte_scan_results_index(self, index: int):
    """
    Sets the index into the cell scan results table to be used with the FETCH command.
    """
    self.instrument.write(f":SENS:LTE:SCAN:RES:INDEX {index}")

def get_lte_scan_results_index(self) -> int:
    """
    Queries the index into the cell scan results table.
    """
    response = self.instrument.query(":SENS:LTE:SCAN:RES:INDEX?")
    return int(response)

def clear_lte_scan_results(self):
    """
    Clears the cell search results table.
    """
    self.instrument.write(":SENS:LTE:SCAN:RES:CLE")

# --- LTE Fetch Results ---

def fetch_lte_metrics(self, metrics: list) -> list:
    """
    Fetches LTE measurement values.
    metrics: list of metric indices.
    Returns: list of metric values in the order requested.
    """
    metrics_str = ",".join(str(m) for m in metrics)
    response = self.instrument.query(f":FETC:LTE? {metrics_str}")
    return [val.strip() for val in response.split(',') if val.strip()]

# --- VCO Characterization Controls ---

def get_vco_sweep_source(self) -> str:
    """
    Queries the sweep source for VCO characterization.
    """
    response = self.instrument.query(":SENS:VCO:SWE:SOUR?")
    return response.strip().upper()

def set_vco_sweep_start(self, voltage: float):
    """
    Sets the starting voltage for the sweep.
    """
    self.instrument.write(f":SENS:VCO:SWE:STAR {voltage}")

def get_vco_sweep_start(self) -> float:
    """
    Queries the starting voltage for the sweep.
    """
    response = self.instrument.query(":SENS:VCO:SWE:STAR?")
    return float(response)

def set_vco_sweep_stop(self, voltage: float):
    """
    Sets the stopping voltage for the sweep.
    """
    self.instrument.write(f":SENS:VCO:SWE:STOP {voltage}")

def get_vco_sweep_stop(self) -> float:
    """
    Queries the stopping voltage for the sweep.
    """
    response = self.instrument.query(":SENS:VCO:SWE:STOP?")
    return float(response)

def set_vco_sweep_points(self, points: int):
    """
    Sets the number of points to measure in the sweep.
    """
    self.instrument.write(f":SENS:VCO:SWE:POIN {points}")

def get_vco_sweep_points(self) -> int:
    """
    Queries the number of points to measure in the sweep.
    """
    response = self.instrument.query(":SENS:VCO:SWE:POIN?")
    return int(response)

def set_vco_sweep_power_reference_level(self, ref_level_dbm: float):
    """
    Sets the reference level for VCO sweep.
    """
    self.instrument.write(f":SENS:VCO:SWE:RF:RLEV {ref_level_dbm}")

def get_vco_sweep_power_reference_level(self) -> float:
    """
    Queries the reference level for VCO sweep.
    """
    response = self.instrument.query(":SENS:VCO:SWE:RF:RLEV?")
    return float(response)

def enable_vco_sweep_band_auto(self, enable: bool):
    """
    Enables/disables automatic frequency band search range.
    """
    self.instrument.write(f":SENS:VCO:SWE:FREQ:BAND:AUTO {1 if enable else 0}")

def is_vco_sweep_band_auto_enabled(self) -> bool:
    """
    Queries if automatic frequency band search range is enabled.
    """
    response = self.instrument.query(":SENS:VCO:SWE:FREQ:BAND:AUTO?")
    return int(response) == 1

def set_vco_sweep_band_start(self, frequency_hz: float):
    """
    Sets the start frequency of the search range.
    """
    self.instrument.write(f":SENS:VCO:SWE:FREQ:BAND:STAR {frequency_hz}")

def get_vco_sweep_band_start(self) -> float:
    """
    Queries the start frequency of the search range.
    """
    response = self.instrument.query(":SENS:VCO:SWE:FREQ:BAND:STAR?")
    return float(response)

def set_vco_sweep_band_stop(self, frequency_hz: float):
    """
    Sets the stop frequency of the search range.
    """
    self.instrument.write(f":SENS:VCO:SWE:FREQ:BAND:STOP {frequency_hz}")

def get_vco_sweep_band_stop(self) -> float:
    """
    Queries the stop frequency of the search range.
    """
    response = self.instrument.query(":SENS:VCO:SWE:FREQ:BAND:STOP?")
    return float(response)

def set_vco_sweep_fcounter_resolution(self, resolution_hz: float):
    """
    Sets the frequency counter resolution for VCO sweep.
    """
    self.instrument.write(f":SENS:VCO:SWE:FCO:RES {resolution_hz}")

def get_vco_sweep_fcounter_resolution(self) -> float:
    """
    Queries the frequency counter resolution for VCO sweep.
    """
    response = self.instrument.query(":SENS:VCO:SWE:FCO:RES?")
    return float(response)

def set_vco_sweep_chpower_width(self, width_hz: float):
    """
    Sets the channel power width for VCO sweep.
    """
    self.instrument.write(f":SENS:VCO:SWE:CHP:WID {width_hz}")

def get_vco_sweep_chpower_width(self) -> float:
    """
    Queries the channel power width for VCO sweep.
    """
    response = self.instrument.query(":SENS:VCO:SWE:CHP:WID?")
    return float(response)

def set_vco_sweep_delay(self, delay_s: float):
    """
    Sets the dwell time for each measurement.
    """
    self.instrument.write(f":SENS:VCO:SWE:DEL {delay_s}")

def get_vco_sweep_delay(self) -> float:
    """
    Queries the dwell time for each measurement.
    """
    response = self.instrument.query(":SENS:VCO:SWE:DEL?")
    return float(response)

# --- VCO DC Source Controls ---

def enable_vco_dc_power(self, enable: bool):
    """
    Enables/disables overall DC power.
    """
    self.instrument.write(f":SENS:VCO:SOUR:VOLT:STAT {1 if enable else 0}")

def is_vco_dc_power_enabled(self) -> bool:
    """
    Queries if overall DC power is enabled.
    """
    response = self.instrument.query(":SENS:VCO:SOUR:VOLT:STAT?")
    return int(response) == 1

def set_vco_dc_fixed_level(self, voltage: float):
    """
    Sets the output level of the fixed power source in volts.
    """
    self.instrument.write(f":SENS:VCO:SOUR:VOLT:FIX {voltage}")

def get_vco_dc_fixed_level(self) -> float:
    """
    Queries the output level of the fixed power source in volts.
    """
    response = self.instrument.query(":SENS:VCO:SOUR:VOLT:FIX?")
    return float(response)

def set_vco_dc_vtune_limit_low(self, voltage: float):
    """
    Sets the minimum output level of the V Tune port in volts.
    """
    self.instrument.write(f":SENS:VCO:SOUR:VOLT:VTUN:LIM:LOW {voltage}")

def get_vco_dc_vtune_limit_low(self) -> float:
    """
    Queries the minimum output level of the V Tune port in volts.
    """
    response = self.instrument.query(":SENS:VCO:SOUR:VOLT:VTUN:LIM:LOW?")
    return float(response)

def set_vco_dc_vtune_limit_high(self, voltage: float):
    """
    Sets the maximum output level of the V Tune port in volts.
    """
    self.instrument.write(f":SENS:VCO:SOUR:VOLT:VTUN:LIM:HIGH {voltage}")

def get_vco_dc_vtune_limit_high(self) -> float:
    """
    Queries the maximum output level of the V Tune port in volts.
    """
    response = self.instrument.query(":SENS:VCO:SOUR:VOLT:VTUN:LIM:HIGH?")
    return float(response)

def set_vco_dc_vsupply_limit_low(self, voltage: float):
    """
    Sets the minimum output level of the V Supply port in volts.
    """
    self.instrument.write(f":SENS:VCO:SOUR:VOLT:VSUP:LIM:LOW {voltage}")

def get_vco_dc_vsupply_limit_low(self) -> float:
    """
    Queries the minimum output level of the V Supply port in volts.
    """
    response = self.instrument.query(":SENS:VCO:SOUR:VOLT:VSUP:LIM:LOW?")
    return float(response)

def set_vco_dc_vsupply_limit_high(self, voltage: float):
    """
    Sets the maximum output level of the V Supply port in volts.
    """
    self.instrument.write(f":SENS:VCO:SOUR:VOLT:VSUP:LIM:HIGH {voltage}")

def get_vco_dc_vsupply_limit_high(self) -> float:
    """
    Queries the maximum output level of the V Supply port in volts.
    """
    response = self.instrument.query(":SENS:VCO:SOUR:VOLT:VSUP:LIM:HIGH?")
    return float(response)

# --- VCO Fetch Results ---

def fetch_vco_frequency(self) -> list:
    """
    Fetches the frequency vs. voltage measurement data.
    """
    response = self.instrument.query(":FETC:VCO:FREQ?")
    return [float(x) for x in response.split(',') if x.strip()]

def fetch_vco_sensitivity(self) -> list:
    """
    Fetches the frequency delta vs. voltage delta measurement data.
    """
    response = self.instrument.query(":FETC:VCO:SENS?")
    return [float(x) for x in response.split(',') if x.strip()]

def fetch_vco_power(self) -> list:
    """
    Fetches the amplitude vs. voltage measurement data.
    """
    response = self.instrument.query(":FETC:VCO:POW?")
    return [float(x) for x in response.split(',') if x.strip()]

def fetch_vco_current(self) -> list:
    """
    Fetches the current vs. voltage measurement data.
    """
    response = self.instrument.query(":FETC:VCO:CURR?")
    return [float(x) for x in response.split(',') if x.strip()]

def fetch_vco_harmonics(self, harmonic_index: int) -> list:
    """
    Fetches the harmonic amplitude vs. voltage measurement data.
    harmonic_index: 1-6
    """
    response = self.instrument.query(f":FETC:VCO:HARM? {harmonic_index}")
    return [float(x) for x in response.split(',') if x.strip()]

# --- Audio Player Controls ---

def start_audio_player(self):
    """
    Opens the audio player.
    """
    self.instrument.write(":SENS:AUD:STAR")

def stop_audio_player(self):
    """
    Closes the audio player.
    """
    self.instrument.write(":SENS:AUD:STOP")

def set_audio_player_center_frequency(self, frequency_hz: float):
    """
    Sets the center frequency of the audio player.
    """
    self.instrument.write(f":SENS:AUD:FREQ:CENT {frequency_hz}")

def get_audio_player_center_frequency(self) -> float:
    """
    Queries the center frequency of the audio player.
    """
    response = self.instrument.query(":SENS:AUD:FREQ:CENT?")
    return float(response)

def set_audio_player_modulation(self, modulation: str):
    """
    Sets the audio demodulation type. Allowed values: 'AM', 'FM', 'LSB', 'USB', 'CW'
    """
    valid_mods = {"AM", "FM", "LSB", "USB", "CW"}
    modulation_upper = modulation.upper()
    if modulation_upper not in valid_mods:
        raise ValueError(f"Invalid modulation: '{modulation}'. Must be one of {valid_mods}.")
    self.instrument.write(f":SENS:AUD:MOD {modulation_upper}")

def get_audio_player_modulation(self) -> str:
    """
    Queries the audio demodulation type.
    """
    response = self.instrument.query(":SENS:AUD:MOD?")
    return response.strip().upper()

def set_audio_player_if_bandwidth(self, bandwidth_hz: float):
    """
    Sets the IF bandwidth of the audio player.
    """
    self.instrument.write(f":SENS:AUD:BAND:IF {bandwidth_hz}")

def get_audio_player_if_bandwidth(self) -> float:
    """
    Queries the IF bandwidth of the audio player.
    """
    response = self.instrument.query(":SENS:AUD:BAND:IF?")
    return float(response)

def set_audio_player_low_pass(self, cutoff_hz: float):
    """
    Sets the audio low pass filter.
    """
    self.instrument.write(f":SENS:AUD:BAND:LOW {cutoff_hz}")

def get_audio_player_low_pass(self) -> float:
    """
    Queries the audio low pass filter.
    """
    response = self.instrument.query(":SENS:AUD:BAND:LOW?")
    return float(response)

def set_audio_player_high_pass(self, cutoff_hz: float):
    """
    Sets the audio high pass filter.
    """
    self.instrument.write(f":SENS:AUD:BAND:HIGH {cutoff_hz}")

def get_audio_player_high_pass(self) -> float:
    """
    Queries the audio high pass filter.
    """
    response = self.instrument.query(":SENS:AUD:BAND:HIGH?")
    return float(response)

def set_audio_player_fm_deemphasis(self, deemphasis_us: float):
    """
    Sets the FM deemphasis in microseconds.
    """
    self.instrument.write(f":SENS:AUD:FM:DEEM {deemphasis_us}")

def get_audio_player_fm_deemphasis(self) -> float:
    """
    Queries the IF bandwidth of the audio player.
    """
    response = self.instrument.query(":SENS:AUD:BAND:IF?")
    return float(response)

def set_audio_player_low_pass(self, cutoff_hz: float):
    """
    Sets the audio low pass filter.
    """
    self.instrument.write(f":SENS:AUD:BAND:LOW {cutoff_hz}")

def get_audio_player_low_pass(self) -> float:
    """
    Queries the audio low pass filter.
    """
    response = self.instrument.query(":SENS:AUD:BAND:LOW?")
    return float(response)

def set_audio_player_high_pass(self, cutoff_hz: float):
    """
    Sets the audio high pass filter.
    """
    self.instrument.write(f":SENS:AUD:BAND:HIGH {cutoff_hz}")

def get_audio_player_high_pass(self) -> float:
    """
    Queries the audio high pass filter.
    """
    response = self.instrument.query(":SENS:AUD:BAND:HIGH?")
    return float(response)

def set_audio_player_fm_deemphasis(self, deemphasis_us: float):
    """
    Sets the FM deemphasis in microseconds.
    """
    self.instrument.write(f":SENS:AUD:FM:DEEM {deemphasis_us}")

def get_audio_player_fm_deemphasis(self) -> float:
    """
    Queries the FM deemphasis in microseconds.
    """
    response = self.instrument.query(":SENS:AUD:FM:DEEM?")
    return float(response)
