
from time import sleep

import pyvisa
from Instruments.EFileType import EFileType
from Instruments.Instrument import Instrument
from Instruments.EInstrument import EInstrument
from PIL import Image

class Oscilloscope(Instrument):

    def __init__(self, instrument, save_files_path=None):
        """Initialize the Oscilloscope class.

        :param instrument: The instrument to control.
        :type instrument: pyvisa.Resource
        :param save_files_path: Path to save files for the oscilloscope.
        :type save_files_path: str
        """
        super().__init__(instrument, EInstrument.OSCILLOSCOPE, save_files_path)

        self.acquisition = Acquisition(self.instrument,self.data_handler)
        self.calibrate = Calibrate(self.instrument,self.data_handler)
        self.channel_1 = Channel(self.instrument,self.data_handler,1)
        self.channel_2 = Channel(self.instrument,self.data_handler,2)
        self.cursor = Cursor(self.instrument,self.data_handler)
        
        self.display = Display(self.instrument,self.data_handler)
    
        self.function = Function(self.instrument,self.data_handler)
        self.lan = LAN(self.instrument,self.data_handler)
        self.math = Math(self.instrument,self.data_handler)
        self.mask = Mask(self.instrument,self.data_handler)
        self.measure = Measure(self.instrument,self.data_handler)
        self.reference = Reference(self.instrument,self.data_handler)
        self.storage = Storage(self.instrument,self.data_handler)
        self.system = System(self.instrument,self.data_handler)
        self.timebase = Timebase(self.instrument,self.data_handler)
        self.trigger = Trigger(self.instrument,self.data_handler)

    def autoscale(self):
        """Enable the waveform auto setting function. The oscilloscope will automatically adjust the vertical scale, horizontal timebase, and trigger mode according to the input signal to realize optimum waveform display.
        """
        self.instrument.write(":AUT")
    
    def clear(self):
        """Clear all the waveforms on the screen. If the oscilloscope is in the RUN state, waveform will still be displayed."""
        self.instrument.write(":CLE")
        #instrument.clear_display_window_graphics()
    def run(self):
        """Start collecting measurements."""
        self.instrument.write(":RUN")
    def stop(self):
        """Stop collecting measurements."""
        self.instrument.write(":STOP")
 #Acquisition Commands
class Acquisition:
    
    def __init__(self, instrument,data_handler):
        """The Aquire commands are used to set and query the memory depth, acquisition mode and the number of averages as well as query the current sample rate of the oscilloscope.
        
        :param instrument: The instrument to control.
        :type instrument: pyvisa.Resource
        :param data_handler: The data handler for processing data.
        :type data_handler: DataHandler"""
        self.instrument = instrument
        self.data_handler = data_handler
    def set_mode(self, mode):
        """Set acquisition mode. 

        :param mode: Mode Options - Normal:  Samples the signal at equal time interval to rebuild the waveform. Averages:  Averages the waveforms from multiple samples to reduce the random noise of the input signal. Peak: Acquires the maximum and minimum values of the signal within the sample interval to get the envelope of the signal. HRESolution:  ultra-sample technique to average the neighboring points of the sample waveform to reduce the random noise on the input signal and generate much smoother waveforms.
        :type mode: str"""

        comm_mode = ":ACQuire:TYPE "+mode
        self.instrument.write(comm_mode)

    def get_mode(self):
        """Get acquisition mode. Normal:  Samples the signal at equal time interval to rebuild the waveform. Averages:  Averages the waveforms from multiple samples to reduce the random noise of the input signal. Peak: Acquires the maximum and minimum values of the signal within the sample interval to get the envelope of the signal. HRESolution:  ultra-sample technique to average the neighboring points of the sample waveform to reduce the random noise on the input signal and generate much smoother waveforms """
        comm_mode = ":ACQuire:TYPE?"
        return self.instrument.query(comm_mode)

    def set_number_of_averages(self, avg):
        """In the average acquisition mode, greater number of averages can lower the noise and increase the vertical resolution, but will also slow the response of the displayed waveform to the waveform changes. 
        
        :param avg: 2 to 1024
        :type avg: int"""
        if avg<2 or avg>1024:
            print("Average is an invalid value. Please enter a number between 2 and 1024")
        else:
            comm_mode = ":ACQuire:AVERages "+avg
            self.instrument.write(comm_mode)

    def get_number_of_averages(self):
        """In the average acquisition mode, greater number of averages can lower the noise and increase the vertical resolution."""
        comm_mode = ":ACQuire:AVERages?"
        return self.instrument.query(comm_mode)
    
    def set_memory_depth(self, mdpth):
        """Set memory depth of the oscilloscope.

        :param mdpth: Memory depth to set. Allowed values for single-channel: 'AUTO', 12000, 120000, 1200000, 12000000, 24000000. Allowed values for dual-channel: 'AUTO', 6000, 60000, 600000, 6000000, 12000000. The value may be provided as a string (e.g. "AUTO") or an integer.
        :type mdpth: str or int
        """
        

        sc_allowed_values = ["AUTO",12000,120000,1200000,12000000,24000000]
        dc_allowed_values = ["AUTO",6000,60000,600000,6000000,12000000]
        if mdpth in sc_allowed_values or mdpth in dc_allowed_values:
            comm_mode = ":ACQuire:MDEPth "+mdpth
            self.instrument.write(comm_mode)
        else:
            print("Invalid memory depth.")

    def get_memory_depth(self):
        """ Get memory depth of the oscilloscope (namely the number of waveform points that can be stored in a single trigger sample)."""
        comm_mode = ":ACQuire:MDEPth?"
        return self.instrument.query(comm_mode)


    def get_sample_rate(self):
        """ Query the current sample rate. The default unit is Sa/s."""
        comm_mode = ":ACQuire:SRATe?"
        return self.instrument.query(comm_mode)
        # Calibration Commands
class Calibrate:
    """
    The Calibrate commands are used to control the oscilloscope's self-calibration process.
    """
    def __init__(self, instrument,data_handler):
        self.instrument = instrument
        self.data_handler = data_handler
    
    def start(self):
        """
        Start the oscilloscope self-calibration process.
        """
        self.instrument.write(":CALibrate:STARt")

    def quit(self):
        """
        Exit the self-calibration process at any time.
        """
        self.instrument.write(":CALibrate:QUIT")

class Channel:
    """The Channel commands are used to control and query channel-specific settings.
    
        :param instrument: The instrument to control.
        :type instrument: pyvisa.Resource
        :param data_handler: The data handler for processing data.
        :type data_handler: DataHandler
        :param channel: The channel number, either 1 or 2.
        :type channel: int
        :param decoder: The Decoder object for the channel.
        :type decoder: Decoder
        :param etable: The ETable object for the channel.
        :type etable: ETable
        """
    def __init__(self, instrument,data_handler, channel):
        self.instrument = instrument
        self.data_handler = data_handler
        self.channel = channel
        self.decoder = Decoder(self.instrument,self.data_handler, channel)
        self.etable = ETable(self.instrument,self.data_handler, channel)

    def set_bandwidth_limit(self,  bw):
        """Set bandwidth limit of the specified channel.

            :param bw: Bandwidth limit to set. Allowed values: "20M" or "OFF".
            :type bw: str
            """
        allowed_chnl_values = [1, 2]
        allowed_type_values = ["20M", "OFF"]
        if self.channel in allowed_chnl_values and bw in allowed_type_values:
            comm = f":CHANnel{self.channel}:BWLimit {bw}"
            self.instrument.write(comm)
        else:
            print("Invalid channel or bandwidth.")

    def get_bandwidth_limit(self, channel):
        """Query the bandwidth limit parameter of the specified channel.

        :param channel: The channel number, either 1 or 2.
        :type channel: int
        :return: The bandwidth limit, either "20M" or "OFF".
        :rtype: str"""
        comm_mode = f":CHANnel{self.channel}:BWLimit?"
        return self.instrument.query(comm_mode)

    def set_coupling_mode(self,  coupling_mode):
        """Set the coupling mode of the instrument for the channel specified by self.channel.

        :param coupling_mode: The coupling mode to set for the current channel. Must be one of "AC", "DC", or "GND".
        :type coupling_mode: str"""
        
        allowed_chnl_values = [1, 2]
        allowed_type_values = ["AC", "DC", "GND"]
        if self.channel in allowed_chnl_values and coupling_mode in allowed_type_values:
            comm = f":CHANnel{self.channel}:COUPling {coupling_mode}"
            self.instrument.write(comm)
        else:
            print("Invalid channel or coupling mode.")

    def get_coupling_mode(self, channel):
        """Query the coupling mode of the specified channel.

            :param channel: The channel to query (e.g., channel number or identifier).
            :type channel: int
            :return: The coupling mode reported by the instrument (for example 'DC', 'AC', or 'GND').
            :rtype: str"""
        
        comm_mode = f":CHANnel{self.channel}:COUPling?"
        return self.instrument.query(comm_mode)

    def invert_waveform(self,  type):
        """Set the invert mode of the specified channel.

        :param type: The invert mode to apply to the channel. Allowed values are "ON" or "OFF" (strings) or 1 or 2 (integers). The channel affected is taken from self.channel and must be 1 or 2.
        :type type: str or int
        """
       
        allowed_chnl_values = [1, 2]
        allowed_type_values = ["ON", "OFF", 1, 2]
        if self.channel in allowed_chnl_values and type in allowed_type_values:
            comm = f":CHANnel{self.channel}:INVert {type}"
            self.instrument.write(comm)
        else:
            print("Invalid channel or invert parameter.")

    def is_inverted(self, channel):
        """
        Query the invert mode of the specified channel.

        :param channel: The channel to query.
        :type channel: int
        :return: The invert mode reported by the instrument for the given channel (e.g., '1'/'0' or 'ON'/'OFF').
        :rtype: str
        """
       
        comm_mode = f":CHANnel{self.channel}:INVert?"
        return self.instrument.query(comm_mode)

    def set_offset(self,  param1):
        """Set the vertical offset of the specified channel (in volts).

        The method sets the vertical offset for self.channel by sending the appropriate command to the instrument. Valid channel values are 1 and 2; if self.channel is not valid, the method prints "Invalid channel." and does not send a command.

        :param param1: The offset value to set, in volts.
        :type param1: float
        """
        
        allowed_chnl_values = [1, 2]
        if self.channel in allowed_chnl_values:
            comm = f":CHANnel{self.channel}:OFFSet {param1}"
            self.instrument.write(comm)
        else:
            print("Invalid channel.")

    def get_offset(self, channel):
        """Query the vertical offset of the specified channel. The default unit is V.

            :param channel: The channel number, either 1 or 2.
            :type channel: int
            :return: The vertical offset value in volts.
            :rtype: str"""
        comm_mode = f":CHANnel{self.channel}:OFFSet?"
        return self.instrument.query(comm_mode)

    def set_range(self,  param1):
        """Set the vertical range of the specified channel. The default unit is V."""
        allowed_chnl_values = [1, 2]
        if self.channel in allowed_chnl_values:
            comm = f":CHANnel{self.channel}:RANGe {param1}"
            self.instrument.write(comm)
        else:
            print("Invalid channel.")

    def get_range(self, channel):
        """Query the vertical range of the specified channel. The default unit is V."""
        comm_mode = f":CHANnel{self.channel}:RANGe?"
        return self.instrument.query(comm_mode)

    def set_tcal(self,  val):
        """
        Set delay calibration time for the specified channel.
        val: delay time in seconds (e.g., 20e-9 for 20ns). Valid range: -100e-9 to 100e-9.
        """
        if self.channel in [1, 2] and isinstance(val, (float, int)) and -100e-9 <= val <= 100e-9:
            self.instrument.write(f":CHANnel{self.channel}:TCAL {val}")
        else:
            print("Invalid channel or value (must be float between -100e-9 and 100e-9)")

    def get_tcal(self, channel):
        """
        Query delay calibration time for the specified channel (in seconds).
        Returns value in scientific notation as float.
        """
        if self.channel in [1, 2]:
            response = self.instrument.query(f":CHANnel{self.channel}:TCAL?")
            return float(response)
        else:
            print("Invalid channel number.")
            return None

    def set_scale(self,  scale):
        """Set vertical scale of the channel (in V/div)."""
        self.instrument.write(f":CHANnel{self.channel}:SCALe {scale}")

    def get_scale(self, channel):
        """Query vertical scale of the channel."""
        return self.instrument.query(f":CHANnel{self.channel}:SCALe?")

    def set_probe_ratio(self,  ratio):
        """Set the probe attenuation ratio for a channel."""
        self.instrument.write(f":CHANnel{self.channel}:PROBe {ratio}")

    def get_probe_ratio(self, channel):
        """Query the probe attenuation ratio for a channel."""
        return self.instrument.query(f":CHANnel{self.channel}:PROBe?")

    def set_units(self,  unit):
        """Set the amplitude display unit for a channel. Options: VOLTage, WATT, AMPere, UNKNown."""
        self.instrument.write(f":CHANnel{self.channel}:UNITs {unit}")

    def get_units(self, channel):
        """Query the amplitude display unit for a channel."""
        return self.instrument.query(f":CHANnel{self.channel}:UNITs?")

    def set_vernier(self,  state):
        """Enable or disable fine adjustment (vernier) for vertical scale."""
        self.instrument.write(f":CHANnel{self.channel}:VERNier {state}")

    def get_vernier(self, channel):
        """Query vernier setting."""
        return self.instrument.query(f":CHANnel{self.channel}:VERNier?")
                    
class Cursor:
    """The Cursor commands are used to control and query cursor-specific settings."""
    def __init__(self, instrument,data_handler):
        self.instrument = instrument
        self.data_handler = data_handler
    
    def set_mode(self, mode):
        """
        Set cursor measurement mode.

        Parameters:
        mode (str): One of {"OFF", "MANual", "TRACk", "AUTO", "XY"}
        Note: XY mode only valid when timebase mode is also XY.
        """
        valid_modes = {"OFF", "MANual", "TRACk", "AUTO", "XY"}
        mode = mode.upper()
        if mode in {m.upper() for m in valid_modes}:
            self.instrument.write(f":CURSor:MODE {mode}")
        else:
            print(f"Invalid mode. Must be one of: {valid_modes}")

    def get_mode(self):
        """
        Query the current cursor measurement mode.

        Returns:
        str: One of {"OFF", "MAN", "TRAC", "AUTO", "XY"}
        """
        return self.instrument.query(":CURSor:MODE?")

    def set_manual_type(self, cursor_type):
        """
        Set the type of manual cursor.

        Parameters:
        cursor_type (str): Either "X" for vertical cursors (time) or "Y" for horizontal cursors (voltage).
        """
        cursor_type = cursor_type.upper()
        if cursor_type in ["X", "Y"]:
            self.instrument.write(f":CURSor:MANual:TYPE {cursor_type}")
        else:
            print("Invalid cursor type. Use 'X' or 'Y'.")

    def get_manual_type(self):
        """
        Query the current manual cursor type.

        Returns:
        str: "X" or "Y"
        """
        return self.instrument.query(":CURSor:MANual:TYPE?")

    def set_manual_source(self, source):
        """
        Set the source for manual cursor measurement.

        Parameters:
        source (str): Channel or source name. Valid options include:
                    "CHAN1", "CHAN2", "MATH", "REF1", "REF2", "REF3", "REF4"
        """
        source = source.upper()
        valid_sources = {"CHAN1", "CHAN2", "MATH"}
        if source in valid_sources:
            self.instrument.write(f":CURSor:MANual:SOURce {source}")
        else:
            print(f"Invalid source. Choose from: {valid_sources}")

    def get_manual_source(self):
        """
        Query the current source for manual cursor measurement.

        Returns:
        str: Current source, such as "CHAN1", "CHAN2", "MATH", etc.
        """
        return self.instrument.query(":CURSor:MANual:SOURce?")

    def set_manual_tunit(self, unit):
        """ Set the horizontal unit for manual cursor measurement. 
        Parameters:
        unit (str): The unit to set, such as "S", "HZ", "DEGREE", "PERCENT".
        """
        valid_units = ["S", "HZ", "DEGREE", "PERCENT"]
        unit = unit.upper()
        if unit in valid_units:
            self.instrument.write(f":CURSor:MANual:TUNit {unit}")
        else:
            print(f"Invalid unit. Valid options are: {valid_units}")

    def get_manual_tunit(self):
        """ Query the current horizontal unit in the manual cursor measurement mode. 
        Returns:
        str: The current horizontal unit, such as "S", "HZ", "DEGREE", "PERCENT".
        """
        return self.instrument.query(":CURSor:MANual:TUNit?")

    def set_manual_vunit(self, unit):
        """ Set the vertical unit for manual cursor measurement. 
        Parameters:
        unit (str): The unit to set, such as "PERCENT", "SOURCE".
        """
        valid_units = ["PERCENT", "SOURCE"]
        unit = unit.upper()
        if unit in valid_units:
            self.instrument.write(f":CURSor:MANual:VUNit {unit}")
        else:
            print(f"Invalid unit. Valid options are: {valid_units}")

    def get_manual_vunit(self):
        """ Query the current vertical unit in the manual cursor measurement mode. 
        Returns:
        str: The current vertical unit, such as "PERCENT", "SOURCE".
        """
        return self.instrument.query(":CURSor:MANual:VUNit?")

    def set_manual(self, cursor, x, y):
        """ Set the horizontal position of cursor A or B in the manual cursor measurement mode. 
        Parameters:
        cursor (str): Cursor identifier, either "A" or "B".
        
        """
        if 5 <= x <= 594:
            self.instrument.write(f":CURSor:MANual:{cursor}X {x}")
        else:
            print("Invalid position. x must be between 5 and 594.")
        if 5 <= y <= 394:
            self.instrument.write(f":CURSor:MANual:{cursor}Y {y}")
        else:
            print("Invalid position. y must be between 5 and 394.")

    def get_manual(self, cursor):
        """ Query the horizontal position of cursor A or B in the manual cursor measurement mode. 
        Parameters:
        cursor (str): Cursor identifier, either "A" or "B".
        Returns:
        str: The x and y coordinates of the cursor in the format "x;y".
        """
        return self.instrument.query(f":CURSor:MANual:{cursor}X?;{cursor}Y?")

    def get_manual_xdelta(self):
        """ Query the difference between the X values of cursor A and cursor B (BX - AX) in the manual cursor measurement mode. 
        Returns:
        float: The difference in X values (BX - AX) in scientific notation.
        """
        response = self.instrument.query(":CURSor:MANual:XDELta?")
        return float(response)

    def get_manual_ixdelta(self):
        """ Query the reciprocal of the absolute value of the difference between the X values of cursor A and cursor B (1/|dX|). 
        Returns:
        float: The reciprocal of the difference in X values (1/|dX|) in scientific notation.
        """
        response = self.instrument.query(":CURSor:MANual:IXDELta?")
        return float(response)

    def get_manual_ydelta(self):
        """ Query the difference between the Y values of cursor A and cursor B (BY - AY) in the manual cursor measurement mode. 
        Returns:
        float: The difference in Y values (BY - AY) in scientific notation.
        """
        response = self.instrument.query(":CURSor:MANual:YDELta?")
        return float(response)

    def set_track_source(self, source, n):
        """
        Set the channel source of cursor A in the track cursor measurement mode.

        Parameters:
            source (str): The source to set for the cursor. Must be one of "OFF", "CHANNEL1", "CHANNEL2", or "MATH".
            n (str): The cursor A|B.

        Returns:
            None
        """
        
        valid_sources = ["OFF", "CHANNEL1", "CHANNEL2", "MATH"]
        source = source.upper()
        if source in valid_sources:
            self.instrument.write(f":CURSor:TRACk:SOURce{n} {source}")
        else:
            print(f"Invalid source. Choose from: {valid_sources}")

    def get_track_source(self, cursor):
        """ Query the channel source of cursor A or B in the track cursor measurement mode. 
        Parameters: 
        cursor (str): Cursor identifier, either "A" or "B".
        Returns:
        int: The channel source of cursor A or B, such as "CHAN1", "CHAN2", "MATH", etc.
        """
        return self.instrument.query(f":CURSor:TRACk:SOURce{n}?")

    def set_xy(self, cursor, x, y):
        """ Set the horizontal position of cursor A or B in the XY cursor measurement mode. 
        Parameters:
        cursor (str): Cursor identifier, either "A" or "B".
        x (int): Horizontal position, must be between 5 and 394.
        y (int): Vertical position, must be between 5 and 394.
        """
        if 5 <= x <= 394 and 5 <= y <= 394:
            self.instrument.write(f":CURSor:XY:{cursor}X {x};{cursor}Y {y};")
        else:
            print("Invalid x or y position. Must be between 5 and 394.")

    def get_xy(self, cursor):
        """ Query the horizontal position of cursor A in the XY cursor measurement mode. 
        Parameters:
        cursor (str): Cursor identifier, either "A" or "B".
        Returns:
        str: The x and y coordinates of the cursor in the format "x;y".
        """
        response = self.instrument.query(f":CURSor:XY:{cursor}X?;{cursor}Y?")
        return response  # Returns an integer between 5 and 394
class Decoder:
    """
    The Decoder commands are used to execute decoding settings and operations.
    """
    def __init__(self, instrument,data_handler,n):
        self.instrument = instrument
        self.data_handler = data_handler
        if n not in [1, 2]:
            raise ValueError("Parameter n must be 1 or 2.")
        self.n = n
        self.uart = UART(instrument, data_handler, n)
        self.iic = IIC_Decoder(instrument, data_handler, n)
        self.spi = SPI_Decoder(instrument, data_handler, n)
        self.parallel = Parallel(instrument, data_handler, n)

    def get_current_decoder(self):
        """Query which decoder you are currently using.
        Returns:
            int: The decoder number (1 or 2).
        """
        return self.n
    def switch_decoder(self, n):
        """Set the current decoder number.
        Parameters:
            n (int): The decoder number to set (1 or 2).
        Returns:
            None
        """
        if n in [1, 2]:
            self.n = n
        else:
            print("Invalid decoder number. Use 1 or 2.")
    def set_mode(self, mode):
        """
        Set the decoder type.
        Parameter:
            mode (str): One of {"PARALLEL", "UART", "SPI", "IIC"}
        Return:
            None
        """
        allowed = {"PARALLEL", "UART", "SPI", "IIC"}
        mode = mode.upper()
        if mode in allowed:
            self.instrument.write(f":DECoder{self.n}:MODE {mode}")
        else:
            print(f"Invalid mode. Allowed: {allowed}")

    def get_mode(self):
        """
        Query the decoder type.
        Parameter:
            None
        Return:
            str: One of {"PAR", "UART", "SPI", "IIC"}
        """
        return self.instrument.query(f":DECoder{self.n}:MODE?")

    def enable_display(self, state):
        """
        Turn on or off the decoder display.
        Parameter:
            state (int or str): 1/0 or "ON"/"OFF"
        Return:
            None
        """
        if state in [1, 0]:
            val = state
        elif isinstance(state, str) and state.upper() in {"ON", "OFF"}:
            val = 1 if state.upper() == "ON" else 0
        else:
            print("Invalid state. Use 1, 0, 'ON', or 'OFF'.")
            return
        self.instrument.write(f":DECoder{self.n}:DISPlay {val}")

    def is_display_enabled(self):
        """
        Query the decoder display status.
        Parameter:
            None
        Return:
            int: 1 (on) or 0 (off)
        """
        return int(self.instrument.query(f":DECoder{self.n}:DISPlay?"))

    def set_format(self, fmt):
        """
        Set the bus display format.
        Parameter:
            fmt (str): One of {"HEX", "ASCII", "DEC", "BIN", "LINE"}
        Return:
            None
        """
        allowed = {"HEX", "ASCII", "DEC", "BIN", "LINE"}
        fmt = fmt.upper()
        if fmt in allowed:
            self.instrument.write(f":DECoder{self.n}:FORMat {fmt}")
        else:
            print(f"Invalid format. Allowed: {allowed}")

    def get_format(self):
        """
        Query the bus display format.
        Parameter:
            None
        Return:
            str: Format string
        """
        return self.instrument.query(f":DECoder{self.n}:FORMat?")

    def set_position(self, pos):
        """
        Set the vertical position of the bus on the screen.
        Parameter:
            pos (int): 50 to 350
        Return:
            None
        """
        if 50 <= pos <= 350:
            self.instrument.write(f":DECoder{self.n}:POSition {pos}")
        else:
            print("Invalid position. Must be between 50 and 350.")

    def get_position(self):
        """
        Query the vertical position of the bus.
        Parameter:
            None
        Return:
            int: Position value
        """
        return int(self.instrument.query(f":DECoder{self.n}:POSition?"))

    def set_threshold_channel(self,  threshold):
        """
        Set the threshold level of the specified analog channel.
        Parameter:
            channel (int): 1 or 2
            threshold (float): Threshold value
        Return:
            None
        """
        if self.channel not in [1, 2]:
            print("Invalid channel. Use 1 or 2.")
            return
        self.instrument.write(f":DECoder{self.n}:THREshold:CHANnel{self.channel} {threshold}")

    def get_threshold_channel(self, channel):
        """
        Query the threshold level of the specified analog channel.
        Parameter:
            channel (int): 1 or 2
        Return:
            float: Threshold value
        """
        if self.channel not in [1, 2]:
            print("Invalid channel. Use 1 or 2.")
            return None
        return float(self.instrument.query(f":DECoder{self.n}:THREshold:CHANnel{self.channel}?"))

    def set_threshold_auto(self, state):
        """
        Turn on or off the auto threshold function.
        Parameter:
            state (int or str): 1/0 or "ON"/"OFF"
        Return:
            None
        """
        if state in [1, 0]:
            val = state
        elif isinstance(state, str) and state.upper() in {"ON", "OFF"}:
            val = 1 if state.upper() == "ON" else 0
        else:
            print("Invalid state. Use 1, 0, 'ON', or 'OFF'.")
            return
        self.instrument.write(f":DECoder{self.n}:THREshold:AUTO {val}")

    def get_threshold_auto(self):
        """
        Query the auto threshold function status.
        Parameter:
            None
        Return:
            int: 1 (on) or 0 (off)
        """
        return int(self.instrument.query(f":DECoder{self.n}:THREshold:AUTO?"))

    def set_config_label(self, state):
        """
        Turn on or off the label display function.
        Parameter:
            state (int or str): 1/0 or "ON"/"OFF"
        Return:
            None
        """
        if state in [1, 0]:
            val = state
        elif isinstance(state, str) and state.upper() in {"ON", "OFF"}:
            val = 1 if state.upper() == "ON" else 0
        else:
            print("Invalid state. Use 1, 0, 'ON', or 'OFF'.")
            return
        self.instrument.write(f":DECoder{self.n}:CONFig:LABel {val}")

    def get_config_label(self):
        """
        Query the label display function status.
        Parameter:
            None
        Return:
            int: 1 (on) or 0 (off)
        """
        return int(self.instrument.query(f":DECoder{self.n}:CONFig:LABel?"))

    def set_config_line(self, state):
        """
        Turn on or off the bus display function.
        Parameter:
            state (int or str): 1/0 or "ON"/"OFF"
        Return:
            None
        """
        if state in [1, 0]:
            val = state
        elif isinstance(state, str) and state.upper() in {"ON", "OFF"}:
            val = 1 if state.upper() == "ON" else 0
        else:
            print("Invalid state. Use 1, 0, 'ON', or 'OFF'.")
            return
        self.instrument.write(f":DECoder{self.n}:CONFig:LINE {val}")

    def get_config_line(self):
        """
        Query the bus display function status.
        Parameter:
            None
        Return:
            int: 1 (on) or 0 (off)
        """
        return int(self.instrument.query(f":DECoder{self.n}:CONFig:LINE?"))

    def set_config_format(self, state):
        """
        Turn on or off the format display function.
        Parameter:
            state (int or str): 1/0 or "ON"/"OFF"
        Return:
            None
        """
        if state in [1, 0]:
            val = state
        elif isinstance(state, str) and state.upper() in {"ON", "OFF"}:
            val = 1 if state.upper() == "ON" else 0
        else:
            print("Invalid state. Use 1, 0, 'ON', or 'OFF'.")
            return
        self.instrument.write(f":DECoder{self.n}:CONFig:FORMat {val}")

    def get_config_format(self):
        """
        Query the format display function status.
        Parameter:
            None
        Return:
            int: 1 (on) or 0 (off)
        """
        return int(self.instrument.query(f":DECoder{self.n}:CONFig:FORMat?"))

    def set_config_endian(self, state):
        """
        Turn on or off the endian display function in serial bus decoding.
        Parameter:
            state (int or str): 1/0 or "ON"/"OFF"
        Return:
            None
        """
        if state in [1, 0]:
            val = state
        elif isinstance(state, str) and state.upper() in {"ON", "OFF"}:
            val = 1 if state.upper() == "ON" else 0
        else:
            print("Invalid state. Use 1, 0, 'ON', or 'OFF'.")
            return
        self.instrument.write(f":DECoder{self.n}:CONFig:ENDian {val}")

    def get_config_endian(self):
        """
        Query the endian display function status.
        Parameter:
            None
        Return:
            int: 1 (on) or 0 (off)
        """
        return int(self.instrument.query(f":DECoder{self.n}:CONFig:ENDian?"))

    def set_config_width(self, state):
        """
        Turn on or off the width display function.
        Parameter:
            state (int or str): 1/0 or "ON"/"OFF"
        Return:
            None
        """
        if state in [1, 0]:
            val = state
        elif isinstance(state, str) and state.upper() in {"ON", "OFF"}:
            val = 1 if state.upper() == "ON" else 0
        else:
            print("Invalid state. Use 1, 0, 'ON', or 'OFF'.")
            return
        self.instrument.write(f":DECoder{self.n}:CONFig:WIDth {val}")

    def get_config_width(self):
        """
        Query the width display function status.
        Parameter:
            None
        Return:
            int: 1 (on) or 0 (off)
        """
        return int(self.instrument.query(f":DECoder{self.n}:CONFig:WIDth?"))

class UART:
    """
    The UART commands are used to set the RS232 decoding parameters.
    """
    def __init__(self, instrument,data_handler,n):
        self.instrument = instrument
        self.data_handler = data_handler
        if n not in [1, 2]:
            raise ValueError("Parameter n must be 1 or 2.")
        self.n = n

    def set_tx(self, tx):
        """
        Set the TX channel source of RS232 decoding.
        Parameter:
            tx (str): "CHANNEL1", "CHANNEL2", or "OFF"
        Return:
            None
        """
        allowed = {"CHANNEL1", "CHANNEL2", "OFF"}
        tx = tx.upper()
        if tx in allowed:
            self.instrument.write(f":DECoder{self.n}:UART:TX {tx}")
        else:
            print(f"Invalid TX source. Allowed: {allowed}")

    def get_tx(self):
        """
        Query the TX channel source of RS232 decoding.
        Parameter:
            None
        Return:
            str: "CHAN1", "CHAN2", or "OFF"
        """
        return self.instrument.query(f":DECoder{self.n}:UART:TX?")

    def set_rx(self, rx):
        """
        Set the RX channel source of RS232 decoding.
        Parameter:
            rx (str): "CHANNEL1", "CHANNEL2", or "OFF"
        Return:
            None
        """
        allowed = {"CHANNEL1", "CHANNEL2", "OFF"}
        rx = rx.upper()
        if rx in allowed:
            self.instrument.write(f":DECoder{self.n}:UART:RX {rx}")
        else:
            print(f"Invalid RX source. Allowed: {allowed}")

    def get_rx(self):
        """
        Query the RX channel source of RS232 decoding.
        Parameter:
            None
        Return:
            str: "CHAN1", "CHAN2", or "OFF"
        """
        return self.instrument.query(f":DECoder{self.n}:UART:RX?")

    def set_polarity(self, polarity):
        """
        Set the polarity of RS232 decoding.
        Parameter:
            polarity (str): "NEGATIVE" or "POSITIVE"
        Return:
            None
        """
        allowed = {"NEGATIVE", "POSITIVE"}
        polarity = polarity.upper()
        if polarity in allowed:
            self.instrument.write(f":DECoder{self.n}:UART:POLarity {polarity}")
        else:
            print(f"Invalid polarity. Allowed: {allowed}")

    def get_polarity(self):
        """
        Query the polarity of RS232 decoding.
        Parameter:
            None
        Return:
            str: "NEG" or "POS"
        """
        return self.instrument.query(f":DECoder{self.n}:UART:POLarity?")

    def set_endian(self, endian):
        """
        Set the endian of RS232 decoding.
        Parameter:
            endian (str): "LSB" or "MSB"
        Return:
            None
        """
        allowed = {"LSB", "MSB"}
        endian = endian.upper()
        if endian in allowed:
            self.instrument.write(f":DECoder{self.n}:UART:ENDian {endian}")
        else:
            print(f"Invalid endian. Allowed: {allowed}")

    def get_endian(self):
        """
        Query the endian of RS232 decoding.
        Parameter:
            None
        Return:
            str: "LSB" or "MSB"
        """
        return self.instrument.query(f":DECoder{self.n}:UART:ENDian?")
    def set_baud(self, baud):
        """
        Set the baud rate of RS232 decoding.
        Parameter:
            baud (int): Baud rate, 110 to 20000000
        Return:
            None
        """
        if isinstance(baud, int) and 110 <= baud <= 20000000:
            self.instrument.write(f":DECoder{self.n}:UART:BAUD {baud}")
        else:
            print("Invalid baud rate. Must be integer between 110 and 20000000.")

    def get_baud(self):
        """
        Query the baud rate of RS232 decoding.
        Parameter:
            None
        Return:
            int: Current baud rate
        """
        return int(self.instrument.query(f":DECoder{self.n}:UART:BAUD?"))

    def set_width(self, width):
        """
        Set the width of each frame of data in RS232 decoding.
        Parameter:
            width (int): Data width, 5 to 8
        Return:
            None
        """
        if isinstance(width, int) and 5 <= width <= 8:
            self.instrument.write(f":DECoder{self.n}:UART:WIDTh {width}")
        else:
            print("Invalid width. Must be integer between 5 and 8.")

    def get_width(self):
        """
        Query the width of each frame of data in RS232 decoding.
        Parameter:
            None
        Return:
            int: Data width (5 to 8)
        """
        return int(self.instrument.query(f":DECoder{self.n}:UART:WIDTh?"))

    def set_stop(self, stop):
        """
        Set the stop bit after each frame of data in RS232 decoding.
        Parameter:
            stop (float): Stop bit, one of 1, 1.5, or 2
        Return:
            None
        """
        allowed = {1, 1.5, 2}
        if stop in allowed:
            self.instrument.write(f":DECoder{self.n}:UART:STOP {stop}")
        else:
            print("Invalid stop bit. Allowed: 1, 1.5, 2.")

    def get_stop(self):
        """
        Query the stop bit after each frame of data in RS232 decoding.
        Parameter:
            None
        Return:
            float: Stop bit (1, 1.5, or 2)
        """
        resp = self.instrument.query(f":DECoder{self.n}:UART:STOP?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_parity(self, parity):
        """
        Set the even-odd check mode of the data transmission in RS232 decoding.
        Parameter:
            parity (str): "NONE", "EVEN", or "ODD"
        Return:
            None
        """
        allowed = {"NONE", "EVEN", "ODD"}
        parity = parity.upper()
        if parity in allowed:
            self.instrument.write(f":DECoder{self.n}:UART:PARity {parity}")
        else:
            print("Invalid parity. Allowed: NONE, EVEN, ODD.")

    def get_parity(self):
        """
        Query the even-odd check mode of the data transmission in RS232 decoding.
        Parameter:
            None
        Return:
            str: "NONE", "EVEN", or "ODD"
        """
        return self.instrument.query(f":DECoder{self.n}:UART:PARity?")

class IIC_Decoder:
    """
    The IIC commands are used to set the I2C decoding parameters.
    """
    def __init__(self, instrument,data_handler,n):
        self.instrument = instrument
        self.data_handler = data_handler
        if n not in [1, 2]:
            raise ValueError("Parameter n must be 1 or 2.")
        self.n = n

    def set_clk(self, clk):
        """
        Set the signal source of the clock channel in I2C decoding.
        Parameter:
            clk (str): "CHANNEL1" or "CHANNEL2"
        Return:
            None
        """
        allowed = {"CHANNEL1", "CHANNEL2"}
        clk = clk.upper()
        if clk in allowed:
            self.instrument.write(f":DECoder{self.n}:IIC:CLK {clk}")
        else:
            print("Invalid clock channel. Allowed: CHANNEL1, CHANNEL2.")

    def get_clk(self):
        """
        Query the signal source of the clock channel in I2C decoding.
        Parameter:
            None
        Return:
            str: "CHAN1" or "CHAN2"
        """
        return self.instrument.query(f":DECoder{self.n}:IIC:CLK?")

    def set_data(self, data):
        """
        Set the signal source of the data channel in I2C decoding.
        Parameter:
            data (str): "CHANNEL1" or "CHANNEL2"
        Return:
            None
        """
        allowed = {"CHANNEL1", "CHANNEL2"}
        data = data.upper()
        if data in allowed:
            self.instrument.write(f":DECoder{self.n}:IIC:DATA {data}")
        else:
            print("Invalid data channel. Allowed: CHANNEL1, CHANNEL2.")

    def get_data(self):
        """
        Query the signal source of the data channel in I2C decoding.
        Parameter:
            None
        Return:
            str: "CHAN1" or "CHAN2"
        """
        return self.instrument.query(f":DECoder{self.n}:IIC:DATA?")

    def set_address(self, addr):
        """
        Set the address mode of I2C decoding.
        Parameter:
            addr (str): "NORMAL" or "RW"
        Return:
            None
        """
        allowed = {"NORMAL", "RW"}
        addr = addr.upper()
        if addr in allowed:
            self.instrument.write(f":DECoder{self.n}:IIC:ADDRess {addr}")
        else:
            print("Invalid address mode. Allowed: NORMAL, RW.")

    def get_address(self):
        """
        Query the address mode of I2C decoding.
        Parameter:
            None
        Return:
            str: "NORM" or "RW"
        """
        return self.instrument.query(f":DECoder{self.n}:IIC:ADDRess?")

class SPI_Decoder:
    """
    The SPI commands are used to set the SPI decoding parameters.
    """
    def __init__(self, instrument,data_handler,n):
        self.instrument = instrument
        self.data_handler = data_handler
        if n not in [1, 2]:
            raise ValueError("Parameter n must be 1 or 2.")
        self.n = n

    def set_clk(self, clk):
        """
        Set the signal source of the clock channel in SPI decoding.
        Parameter:
            clk (str): "CHANNEL1" or "CHANNEL2"
        Return:
            None
        """
        allowed = {"CHANNEL1", "CHANNEL2"}
        clk = clk.upper()
        if clk in allowed:
            self.instrument.write(f":DECoder{self.n}:SPI:CLK {clk}")
        else:
            print("Invalid clock channel. Allowed: CHANNEL1, CHANNEL2.")

    def get_clk(self):
        """
        Query the signal source of the clock channel in SPI decoding.
        Parameter:
            None
        Return:
            str: "CHAN1" or "CHAN2"
        """
        return self.instrument.query(f":DECoder{self.n}:SPI:CLK?")

    def set_miso(self, miso):
        """
        Set the MISO channel source in SPI decoding.
        Parameter:
            miso (str): "CHANNEL1", "CHANNEL2", or "OFF"
        Return:
            None
        """
        allowed = {"CHANNEL1", "CHANNEL2", "OFF"}
        miso = miso.upper()
        if miso in allowed:
            self.instrument.write(f":DECoder{self.n}:SPI:MISO {miso}")
        else:
            print("Invalid MISO channel. Allowed: CHANNEL1, CHANNEL2, OFF.")

    def get_miso(self):
        """
        Query the MISO channel source in SPI decoding.
        Parameter:
            None
        Return:
            str: "CHAN1", "CHAN2", or "OFF"
        """
        return self.instrument.query(f":DECoder{self.n}:SPI:MISO?")
    def set_mosi(self, mosi):
        """
        Set the MOSI channel source in SPI decoding.
        Parameter:
            mosi (str): "CHANNEL1", "CHANNEL2", or "OFF"
        Return:
            None
        """
        allowed = {"CHANNEL1", "CHANNEL2", "OFF"}
        mosi = mosi.upper()
        if mosi in allowed:
            self.instrument.write(f":DECoder{self.n}:SPI:MOSI {mosi}")
        else:
            print("Invalid MOSI channel. Allowed: CHANNEL1, CHANNEL2, OFF.")

    def get_mosi(self):
        """
        Query the MOSI channel source in SPI decoding.
        Parameter:
            None
        Return:
            str: "CHAN1", "CHAN2", or "OFF"
        """
        return self.instrument.query(f":DECoder{self.n}:SPI:MOSI?")

    def set_cs(self, cs):
        """
        Set the CS channel source in SPI decoding.
        Parameter:
            cs (str): "CHANNEL1" or "CHANNEL2"
        Return:
            None
        """
        allowed = {"CHANNEL1", "CHANNEL2"}
        cs = cs.upper()
        if cs in allowed:
            self.instrument.write(f":DECoder{self.n}:SPI:CS {cs}")
        else:
            print("Invalid CS channel. Allowed: CHANNEL1, CHANNEL2.")

    def get_cs(self):
        """
        Query the CS channel source in SPI decoding.
        Parameter:
            None
        Return:
            str: "CHAN1" or "CHAN2"
        """
        return self.instrument.query(f":DECoder{self.n}:SPI:CS?")

    def set_select(self, csncs):
        """
        Set the CS polarity in SPI decoding.
        Parameter:
            csncs (str): "NCS" or "CS"
        Return:
            None
        """
        allowed = {"NCS", "CS"}
        csncs = csncs.upper()
        if csncs in allowed:
            self.instrument.write(f":DECoder{self.n}:SPI:SELect {csncs}")
        else:
            print("Invalid CS polarity. Allowed: NCS, CS.")

    def get_select(self):
        """
        Query the CS polarity in SPI decoding.
        Parameter:
            None
        Return:
            str: "NCS" or "CS"
        """
        return self.instrument.query(f":DECoder{self.n}:SPI:SELect?")

    def set_mode(self, mode):
        """
        Set the frame synchronization mode of SPI decoding.
        Parameter:
            mode (str): "CS" or "TIMEOUT"
        Return:
            None
        """
        allowed = {"CS", "TIMEOUT"}
        mode = mode.upper()
        if mode in allowed:
            self.instrument.write(f":DECoder{self.n}:SPI:MODE {mode}")
        else:
            print("Invalid mode. Allowed: CS, TIMEOUT.")

    def get_mode(self):
        """
        Query the frame synchronization mode of SPI decoding.
        Parameter:
            None
        Return:
            str: "CS" or "TIM"
        """
        return self.instrument.query(f":DECoder{self.n}:SPI:MODE?")

    def set_timeout(self, tmo):
        """
        Set the timeout time in the timeout mode of SPI decoding.
        Parameter:
            tmo (float): Timeout time in seconds (e.g., 1e-6)
        Return:
            None
        """
        if isinstance(tmo, (float, int)) and tmo > 0:
            self.instrument.write(f":DECoder{self.n}:SPI:TIMeout {tmo}")
        else:
            print("Invalid timeout value. Must be a positive number.")

    def get_timeout(self):
        """
        Query the timeout time in the timeout mode of SPI decoding.
        Parameter:
            None
        Return:
            float: Timeout time in seconds
        """
        resp = self.instrument.query(f":DECoder{self.n}:SPI:TIMeout?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_polarity(self, pol):
        """
        Set the polarity of the SDA data line in SPI decoding.
        Parameter:
            pol (str): "NEGATIVE" or "POSITIVE"
        Return:
            None
        """
        allowed = {"NEGATIVE", "POSITIVE"}
        pol = pol.upper()
        if pol in allowed:
            self.instrument.write(f":DECoder{self.n}:SPI:POLarity {pol}")
        else:
            print("Invalid polarity. Allowed: NEGATIVE, POSITIVE.")

    def get_polarity(self):
        """
        Query the polarity of the SDA data line in SPI decoding.
        Parameter:
            None
        Return:
            str: "NEG" or "POS"
        """
        return self.instrument.query(f":DECoder{self.n}:SPI:POLarity?")

    def set_edge(self, edge):
        """
        Set the clock type when the instrument samples the data line in SPI decoding.
        Parameter:
            edge (str): "RISE" or "FALL"
        Return:
            None
        """
        allowed = {"RISE", "FALL"}
        edge = edge.upper()
        if edge in allowed:
            self.instrument.write(f":DECoder{self.n}:SPI:EDGE {edge}")
        else:
            print("Invalid edge. Allowed: RISE, FALL.")

    def get_edge(self):
        """
        Query the clock type when the instrument samples the data line in SPI decoding.
        Parameter:
            None
        Return:
            str: "RISE" or "FALL"
        """
        return self.instrument.query(f":DECoder{self.n}:SPI:EDGE?")

    def set_endian(self, endian):
        """
        Set the endian of the SPI decoding data.
        Parameter:
            endian (str): "LSB" or "MSB"
        Return:
            None
        """
        allowed = {"LSB", "MSB"}
        endian = endian.upper()
        if endian in allowed:
            self.instrument.write(f":DECoder{self.n}:SPI:ENDian {endian}")
        else:
            print("Invalid endian. Allowed: LSB, MSB.")

    def get_endian(self):
        """
        Query the endian of the SPI decoding data.
        Parameter:
            None
        Return:
            str: "LSB" or "MSB"
        """
        return self.instrument.query(f":DECoder{self.n}:SPI:ENDian?")

    def set_width(self, wid):
        """
        Set the number of bits of each frame of data in SPI decoding.
        Parameter:
            wid (int): Data width, 4 to 32
        Return:
            None
        """
        if isinstance(wid, int) and 4 <= wid <= 32:
            self.instrument.write(f":DECoder{self.n}:SPI:WIDTh {wid}")
        else:
            print("Invalid width. Must be integer between 4 and 32.")

    def get_width(self):
        """
        Query the number of bits of each frame of data in SPI decoding.
        Parameter:
            None
        Return:
            int: Data width (4 to 32)
        """
        resp = self.instrument.query(f":DECoder{self.n}:SPI:WIDTh?")
        try:
            return int(resp)
        except Exception:
            return resp
class Parallel:
    """
    The Parallel commands are used to set the parallel decoding parameters.
    """
    def __init__(self, instrument,data_handler,n):
        self.instrument = instrument
        self.data_handler = data_handler
        if n not in [1, 2]:
            raise ValueError("Parameter n must be 1 or 2.")
        self.n = n

    def set_clk(self, clk):
        """
        Set the CLK channel source of parallel decoding.
        Parameter:
            clk (str): "CHANNEL1", "CHANNEL2", or "OFF"
        Return:
            None
        """
        allowed = {"CHANNEL1", "CHANNEL2", "OFF"}
        clk = clk.upper()
        if clk in allowed:
            self.instrument.write(f":DECoder{self.n}:PARallel:CLK {clk}")
        else:
            print("Invalid clk. Allowed: CHANNEL1, CHANNEL2, OFF.")

    def get_clk(self):
        """
        Query the CLK channel source of parallel decoding.
        Parameter:
            None
        Return:
            str: "CHAN1", "CHAN2", or "OFF"
        """
        return self.instrument.query(f":DECoder{self.n}:PARallel:CLK?")

    def set_edge(self, edge):
        """
        Set the edge type of the clock channel for parallel decoding.
        Parameter:
            edge (str): "RISE", "FALL", or "BOTH"
        Return:
            None
        """
        allowed = {"RISE", "FALL", "BOTH"}
        edge = edge.upper()
        if edge in allowed:
            self.instrument.write(f":DECoder{self.n}:PARallel:EDGE {edge}")
        else:
            print("Invalid edge. Allowed: RISE, FALL, BOTH.")

    def get_edge(self):
        """
        Query the edge type of the clock channel for parallel decoding.
        Parameter:
            None
        Return:
            str: "RISE", "FALL", or "BOTH"
        """
        return self.instrument.query(f":DECoder{self.n}:PARallel:EDGE?")

    def set_width(self, wid):
        """
        Set the data width (number of bits per frame) for parallel decoding.
        Parameter:
            wid (int): Data width, 1 to 2
        Return:
            None
        """
        if isinstance(wid, int) and 1 <= wid <= 2:
            self.instrument.write(f":DECoder{self.n}:PARallel:WIDTh {wid}")
        else:
            print("Invalid width. Must be integer between 1 and 2.")

    def get_width(self):
        """
        Query the data width for parallel decoding.
        Parameter:
            None
        Return:
            int: Data width (1 to 2)
        """
        resp = self.instrument.query(f":DECoder{self.n}:PARallel:WIDTh?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_bitx(self, bit):
        """
        Set the data bit that requires a channel source on the parallel bus.
        Parameter:
            bit (int): Bit index, 0 to (data width - 1)
        Return:
            None
        """
        if isinstance(bit, int) and bit >= 0:
            self.instrument.write(f":DECoder{self.n}:PARallel:BITX {bit}")
        else:
            print("Invalid bit index.")

    def get_bitx(self):
        """
        Query the current data bit selected on the parallel bus.
        Parameter:
            None
        Return:
            int: Current bit index
        """
        resp = self.instrument.query(f":DECoder{self.n}:PARallel:BITX?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_source(self, src):
        """
        Set the channel source of the data bit currently selected.
        Parameter:
            src (str): "CHANNEL1" or "CHANNEL2"
        Return:
            None
        """
        allowed = {"CHANNEL1", "CHANNEL2"}
        src = src.upper()
        if src in allowed:
            self.instrument.write(f":DECoder{self.n}:PARallel:SOURce {src}")
        else:
            print("Invalid source. Allowed: CHANNEL1, CHANNEL2.")

    def get_source(self):
        """
        Query the channel source of the data bit currently selected.
        Parameter:
            None
        Return:
            str: "CHAN1" or "CHAN2"
        """
        return self.instrument.query(f":DECoder{self.n}:PARallel:SOURce?")

    def set_polarity(self, pol):
        """
        Set the data polarity of parallel decoding.
        Parameter:
            pol (str): "NEGATIVE" or "POSITIVE"
        Return:
            None
        """
        allowed = {"NEGATIVE", "POSITIVE"}
        pol = pol.upper()
        if pol in allowed:
            self.instrument.write(f":DECoder{self.n}:PARallel:POLarity {pol}")
        else:
            print("Invalid polarity. Allowed: NEGATIVE, POSITIVE.")

    def get_polarity(self):
        """
        Query the data polarity of parallel decoding.
        Parameter:
            None
        Return:
            str: "NEG" or "POS"
        """
        return self.instrument.query(f":DECoder{self.n}:PARallel:POLarity?")

    def enable_noise_rejection(self, enable):
        """
        Turn on or off the noise rejection function of parallel decoding.
        Parameter:
            enable (int or str): 1/0 or "ON"/"OFF"
        Return:
            None
        """
        if enable in [1, 0]:
            val = enable
        elif isinstance(enable, str) and enable.upper() in {"ON", "OFF"}:
            val = 1 if enable.upper() == "ON" else 0
        else:
            print("Invalid enable value. Use 1, 0, 'ON', or 'OFF'.")
            return
        self.instrument.write(f":DECoder{self.n}:PARallel:NREJect {val}")

    def is_noise_rejection_enabled(self):
        """
        Query the status of the noise rejection function of parallel decoding.
        Parameter:
            None
        Return:
            int: 1 (on) or 0 (off)
        """
        return int(self.instrument.query(f":DECoder{self.n}:PARallel:NREJect?"))

    def set_noise_rejection_time(self, time):
        """
        Set the noise rejection time of parallel decoding (in seconds).
        Parameter:
            time (float): 0.00s to 0.1s (100ms)
        Return:
            None
        """
        if isinstance(time, (float, int)) and 0.0 <= time <= 0.1:
            self.instrument.write(f":DECoder{self.n}:PARallel:NRTime {time}")
        else:
            print("Invalid time. Must be between 0.00 and 0.1 seconds.")

    def get_noise_rejection_time(self):
        """
        Query the noise rejection time of parallel decoding.
        Parameter:
            None
        Return:
            float: Noise rejection time in seconds
        """
        resp = self.instrument.query(f":DECoder{self.n}:PARallel:NRTime?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_compensation(self, comp):
        """
        Set the clock compensation time of parallel decoding (in seconds).
        Parameter:
            comp (float): -0.1s to 0.1s (-100ms to 100ms)
        Return:
            None
        """
        if isinstance(comp, (float, int)) and -0.1 <= comp <= 0.1:
            self.instrument.write(f":DECoder{self.n}:PARallel:CCOMpensation {comp}")
        else:
            print("Invalid compensation. Must be between -0.1 and 0.1 seconds.")

    def get_compensation(self):
        """
        Query the clock compensation time of parallel decoding.
        Parameter:
            None
        Return:
            float: Compensation time in seconds
        """
        resp = self.instrument.query(f":DECoder{self.n}:PARallel:CCOMpensation?")
        try:
            return float(resp)
        except Exception:
            return resp

    def enable_plot(self, enable):
        """
        Turn on or off the curve function of parallel decoding.
        
        Parameter:
        enable (int or str): 1/0 or "ON"/"OFF"
        
        Return:
        None
        """
        if enable in [1, 0]:
            val = enable
        elif isinstance(enable, str) and enable.upper() in {"ON", "OFF"}:
            val = 1 if enable.upper() == "ON" else 0
        else:
            print("Invalid enable value. Use 1, 0, 'ON', or 'OFF'.")
            return
        self.instrument.write(f":DECoder{self.n}:PARallel:PLOT {val}")

    def is_plot_enabled(self):
        """
        Query the status of the curve function of parallel decoding.
        
        Parameter:
        None
        
        Return:
        int: 1 (on) or 0 (off)
        """
        return int(self.instrument.query(f":DECoder{self.n}:PARallel:PLOT?"))



class Display:
    """
    The Display commands are used to set the waveform display mode, persistence time, waveform intensity, screen grid type and grid brightness.
    """
    def __init__(self, instrument,data_handler):
            self.instrument = instrument
            self.data_handler = data_handler

    def clear(self):
        """
        Clear all the waveforms on the screen.
        
        Parameter:
            None
        
        Return:
            None
        """
        self.instrument.write(":DISPlay:CLEar")

    def get_data(self, color=None, invert=None, fmt=None):
        """
        Read the data stream of the image currently displayed on the screen. If autosave is on, then also saves them to a png file.
        
        Parameter:
        color (str or None): "ON" or "OFF" (default ON)
        invert (int/str or None): 1/"ON" or 0/"OFF" (default 0)
        fmt (str or None): "BMP24", "BMP8", "PNG", "JPEG", "TIFF" (default BMP24)
            
        Return:
        bytes: Raw image data (TMC header included)
        Image: If auto save enabled, return PIL Image object, if not set to save return None
        """
        cmd = ":DISPlay:DATA?"
        args = []
        if color is not None:
            color = color.upper()
            if color not in {"ON", "OFF"}:
                print("Invalid color. Allowed: ON, OFF.")
            return None
            args.append(color)
        if invert is not None:
            if invert in [1, 0]:
                args.append(str(invert))
            elif isinstance(invert, str) and invert.upper() in {"ON", "OFF"}:
                args.append("1" if invert.upper() == "ON" else "0")
            else:
                print("Invalid invert. Allowed: 1, 0, ON, OFF.")
            return None
        if fmt is not None:
            fmt = fmt.upper()
            if fmt not in {"BMP24", "BMP8", "PNG", "JPEG", "TIFF"}:
                print("Invalid format. Allowed: BMP24, BMP8, PNG, JPEG, TIFF.")
            return None
            args.append(fmt)
        img = None
        if args:
            cmd += " " + ",".join(args)
        data = self.instrument.query_binary_values(cmd, datatype='B', container=bytes)
        if data and data[0] == ord('#'):  # Check for TMC header
            data = self.data_handler.remove_tmc_header(data)
        if self.data_handler.auto_save:
            img, data = self.data_handler.bytes_to_image("Osc_Display_Data", data, EFileType.PNG)  # Assuming PNG as default, adjust if needed
        return data, img
    def set_type(self, disp_type):
        """
        Set the waveform display mode.
        
        Parameter:
        disp_type (str): Allowed values depend on instrument, e.g., "VECTor", "DOTS"
        
        Return:
        None
        """
        allowed = {"VECTOR", "DOTS"}
        disp_type = disp_type.upper()
        if disp_type in allowed:
            self.instrument.write(f":DISPlay:TYPE {disp_type}")
        else:
            print(f"Invalid display type. Allowed: {allowed}")

    def get_type(self):
        """
        Query the waveform display mode.
        
        Parameter:
        None
        
        Return:
        str: Display type
        """
        return self.instrument.query(":DISPlay:TYPE?")

    def set_grading_time(self, time):
        """
        Set the persistence time of the waveform.
        
        Parameter:
        time (float): Persistence time in seconds
        
        Return:
        None
        """
        if isinstance(time, (float, int)) and time >= 0:
            self.instrument.write(f":DISPlay:GRADing:TIME {time}")
        else:
            print("Invalid time. Must be a non-negative number.")

    def get_grading_time(self):
        """
        Query the persistence time of the waveform.
        
        Parameter:
        None
        
        Return:
        float: Persistence time in seconds
        """
        resp = self.instrument.query(":DISPlay:GRADing:TIME?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_waveform_brightness(self, val):
        """
        Set the waveform intensity.
        
        Parameter:
        val (int): 0 to 100
        
        Return:
        None
        """
        if isinstance(val, int) and 0 <= val <= 100:
            self.instrument.write(f":DISPlay:WBRightness {val}")
        else:
            print("Invalid brightness. Must be integer between 0 and 100.")

    def get_waveform_brightness(self):
        """
        Query the waveform intensity.
        
        Parameter:
        None
        
        Return:
        int: Brightness (0 to 100)
        """
        resp = self.instrument.query(":DISPlay:WBRightness?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_grid(self, grid_type):
        """
        Set the screen grid type.
        
        Parameter:
        grid_type (str): "FULL", "HALF", "NONE"
        
        Return:
        None
        """
        allowed = {"FULL", "HALF", "NONE"}
        grid_type = grid_type.upper()
        if grid_type in allowed:
            self.instrument.write(f":DISPlay:GRID {grid_type}")
        else:
            print(f"Invalid grid type. Allowed: {allowed}")

    def get_grid(self):
        """
        Query the screen grid type.
        
        Parameter:
        None
        
        Return:
        str: Grid type
        """
        return self.instrument.query(":DISPlay:GRID?")

    def set_grid_brightness(self, val):
        """
        Set the grid brightness.
        
        Parameter:
        val (int): 0 to 100
        
        Return:
        None
        """
        if isinstance(val, int) and 0 <= val <= 100:
            self.instrument.write(f":DISPlay:GBRightness {val}")
        else:
            print("Invalid grid brightness. Must be integer between 0 and 100.")

    def get_grid_brightness(self):
        """
        Query the grid brightness.
        
        Parameter:
        None
        
        Return:
        int: Grid brightness (0 to 100)
        """
        resp = self.instrument.query(":DISPlay:GBRightness?")
        try:
            return int(resp)
        except Exception:
            return resp
class ETable:
    """
    The ETable commands are used to set the parameters related to the decoding event table.
    """
    def __init__(self, instrument,data_handler,n):
        self.instrument = instrument
        self.data_handler = data_handler
        if n not in [1, 2]:
            raise ValueError("Parameter n must be 1 or 2.")
        self.n = n

    def set_disp(self, state):
        """
        Turn on or off the decoding event table.
        
        Parameter:
        state (int or str): 1/0 or "ON"/"OFF"
        
        Return:
        None
        """
        if state in [1, 0]:
            val = state
        elif isinstance(state, str) and state.upper() in {"ON", "OFF"}:
            val = 1 if state.upper() == "ON" else 0
        else:
            print("Invalid state. Use 1, 0, 'ON', or 'OFF'.")
            return
        self.instrument.write(f":ETABle{self.n}:DISP {val}")

    def get_disp(self):
        """
        Query the status of the decoding event table.
        
        Parameter:
        None
        
        Return:
        int: 1 (on) or 0 (off)
        """
        return int(self.instrument.query(f":ETABle{self.n}:DISP?"))

    def set_format(self, fmt):
        """
        Set the data display format of the event table.
        
        Parameter:
        fmt (str): "HEX", "ASCII", or "DEC"
        
        Return:
        None
        """
        allowed = {"HEX", "ASCII", "DEC"}
        fmt = fmt.upper()
        if fmt in allowed:
            self.instrument.write(f":ETABle{self.n}:FORMat {fmt}")
        else:
            print("Invalid format. Allowed: HEX, ASCII, DEC.")

    def get_format(self):
        """
        Query the data display format of the event table.
        
        Parameter:
        None
        
        Return:
        str: "HEX", "ASC", or "DEC"
        """
        return self.instrument.query(f":ETABle{self.n}:FORMat?")

    def set_view(self, view):
        """
        Set the display mode of the event table.
        
        Parameter:
        view (str): "PACKAGE", "DETAIL", or "PAYLOAD"
        
        Return:
        None
        """
        allowed = {"PACKAGE", "DETAIL", "PAYLOAD"}
        view = view.upper()
        if view in allowed:
            self.instrument.write(f":ETABle{self.n}:VIEW {view}")
        else:
            print("Invalid view. Allowed: PACKAGE, DETAIL, PAYLOAD.")

    def get_view(self):
        """
        Query the display mode of the event table.
        
        Parameter:
        None
        
        Return:
        str: "PACK", "DET", or "PAYL"
        """
        return self.instrument.query(f":ETABle{self.n}:VIEW?")

    def set_column(self, col):
        """
        Set the current column of the event table.
        
        Parameter:
        col (str): "DATA", "TX", "RX", "MISO", or "MOSI"
        
        Return:
        None
        """
        allowed = {"DATA", "TX", "RX", "MISO", "MOSI"}
        col = col.upper()
        if col in allowed:
            self.instrument.write(f":ETABle{self.n}:COLumn {col}")
        else:
            print("Invalid column. Allowed: DATA, TX, RX, MISO, MOSI.")

    def get_column(self):
        """
        Query the current column of the event table.
        
        Parameter:
        None
        
        Return:
        str: "DATA", "TX", "RX", "MISO", or "MOSI"
        """
        return self.instrument.query(f":ETABle{self.n}:COLumn?")

    def set_row(self, row):
        """
        Set the current row of the event table.
        
        Parameter:
        row (int): Row number (1 to max rows)
        
        Return:
        None
        """
        if isinstance(row, int) and row >= 1:
            self.instrument.write(f":ETABle{self.n}:ROW {row}")
        else:
            print("Invalid row. Must be integer >= 1.")

    def get_row(self):
        """
        Query the current row of the event table.
        
        Parameter:
        None
        
        Return:
        int: Current row, or 0 if table is empty
        """
        resp = self.instrument.query(f":ETABle{self.n}:ROW?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_sort(self, sort):
        """
        Set the display type of the decoding results in the event table.
        
        Parameter:
        sort (str): "ASCEND" or "DESCEND"
        
        Return:
        None
        """
        allowed = {"ASCEND", "DESCEND"}
        sort = sort.upper()
        if sort in allowed:
            self.instrument.write(f":ETABle{self.n}:SORT {sort}")
        else:
            print("Invalid sort. Allowed: ASCEND, DESCEND.")

    def get_sort(self):
        """
        Query the display type of the decoding results in the event table.
        Parameter:
            None
        Return:
            str: "ASC" or "DESC"
        """
        return self.instrument.query(f":ETABle{self.n}:SORT?")

    def get_data(self):
        """
        Read the current event table data. If auto save is on, then also saves them to a csv file.
        
        Parameter:
        None
        
        Return:
        bytes: Raw event table data (TMC header included)
        """
        data = self.instrument.query_binary_values(f":ETABle{self.n}:DATA?", datatype='B', container=bytes)
        if data and data[0] == ord('#'):  # Check for TMC header
            data = self.data_handler.remove_tmc_header(data)
        if self.data_handler.auto_save:
            
            self.data_handler.write_to_file(f"ETable{self.n}_Data", data, EFileType.CSV)  # Assuming CSV, adjust if needed
        return data

class Function:
    """
    The Function commands are used to set the waveform recording and playback parameters.
    """
    def __init__(self, instrument,data_handler):
        self.instrument = instrument
        self.data_handler = data_handler
        self.WRecord = WRecord(instrument, data_handler)
        self.WReplay = WReplay(instrument, data_handler)

class WRecord:
    def __init__(self, instrument,data_handler):
        self.instrument = instrument
        self.data_handler = data_handler
    def set_wrecord_fend(self, frame):
        """
        Set the end frame of waveform recording.
        
        Parameter:
        frame (int): 1 to max frames (use get_wrecord_fmax to query max)
        
        Return:
        None
        """
        if isinstance(frame, int) and frame >= 1:
            self.instrument.write(f":FUNCtion:WRECord:FEND {frame}")
        else:
            print("Invalid frame value.")

    def get_wrecord_fend(self):
        """
        Query the end frame of waveform recording.
        
        Parameter:
        None
        
        Return:
        int: Current end frame
        """
        resp = self.instrument.query(":FUNCtion:WRECord:FEND?")
        try:
            return int(resp)
        except Exception:
            return resp

    def get_wrecord_fmax(self):
        """
        Query the maximum number of frames that can be recorded currently.
        
        Parameter:
        None
        
        Return:
        int: Maximum number of frames
        """
        resp = self.instrument.query(":FUNCtion:WRECord:FMAX?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_wrecord_finterval(self, interval):
        """
        Set the time interval between frames in waveform recording.
        
        Parameter:
        interval (float): 100e-9 to 10.0 (seconds)
        
        Return:
        None
        """
        if isinstance(interval, (float, int)) and 1e-7 <= interval <= 10.0:
            self.instrument.write(f":FUNCtion:WRECord:FINTerval {interval}")
        else:
            print("Invalid interval. Must be between 100ns and 10s.")

    def get_wrecord_finterval(self):
        """
        Query the time interval between frames in waveform recording.
        
        Parameter:
        None
        
        Return:
        float: Time interval in seconds
        """
        resp = self.instrument.query(":FUNCtion:WRECord:FINTerval?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_wrecord_prompt(self, state):
        """
        Turn on or off the sound prompt when recording finishes.
        
        Parameter:
        state (int or str): 1/0 or "ON"/"OFF"
        
        Return:
        None
        """
        if state in [1, 0]:
            val = state
        elif isinstance(state, str) and state.upper() in {"ON", "OFF"}:
            val = 1 if state.upper() == "ON" else 0
        else:
            print("Invalid state. Use 1, 0, 'ON', or 'OFF'.")
            return
        self.instrument.write(f":FUNCtion:WRECord:PROMpt {val}")

    def get_wrecord_prompt(self):
        """
        Query the status of the sound prompt when recording finishes.
        
        Parameter:
        None
        
        Return:
        int: 1 (on) or 0 (off)
        """
        resp = self.instrument.query(":FUNCtion:WRECord:PROMpt?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_wrecord_operate(self, opt):
        """
        Start or stop the waveform recording.
        
        Parameter:
        opt (str): "RUN" or "STOP"
        
        Return: 
        None
        """
        allowed = {"RUN", "STOP"}
        opt = opt.upper()
        if opt in allowed:
            self.instrument.write(f":FUNCtion:WRECord:OPERate {opt}")
        else:
            print("Invalid option. Allowed: RUN, STOP.")

    def get_wrecord_operate(self):
        """
        Query the status of the waveform recording.
        
        Parameter:
        None
        
        Return:
        str: "RUN" or "STOP"
        """
        return self.instrument.query(":FUNCtion:WRECord:OPERate?")

    def set_wrecord_enable(self, state):
        """
        Turn on or off the waveform recording function.
        
        Parameter:
        state (int or str): 1/0 or "ON"/"OFF"
        
        Return:
        None
        """
        if state in [1, 0]:
            val = state
        elif isinstance(state, str) and state.upper() in {"ON", "OFF"}:
            val = 1 if state.upper() == "ON" else 0
        else:
            print("Invalid state. Use 1, 0, 'ON', or 'OFF'.")
            return
        self.instrument.write(f":FUNCtion:WRECord:ENABle {val}")

    def get_wrecord_enable(self):
        """
        Query the status of the waveform recording function.
        
        Parameter:
        None
        
        Return:
        int: 1 (on) or 0 (off)
        """
        resp = self.instrument.query(":FUNCtion:WRECord:ENABle?")
        try:
            return int(resp)
        except Exception:
            return resp

class WReplay:
    def __init__(self, instrument,data_handler):
        self.instrument = instrument
        self.data_handler = data_handler
    def set_wreplay_fstart(self, frame):
        """
        Set the start frame of waveform playback.
        
        Parameter:
        frame (int): 1 to max frames recorded
        
        Return:
        None
        """
        if isinstance(frame, int) and frame >= 1:
            self.instrument.write(f":FUNCtion:WREPlay:FSTart {frame}")
        else:
            print("Invalid frame value.")

    def get_wreplay_fstart(self):
        """
        Query the start frame of waveform playback.
        
        Parameter:
        None
        
        Return:
        int: Start frame
        """
        resp = self.instrument.query(":FUNCtion:WREPlay:FSTart?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_wreplay_fend(self, frame):
        """
        Set the end frame of waveform playback.
        
        Parameter:
        frame (int): 1 to max frames recorded
        
        Return:
        None
        """
        if isinstance(frame, int) and frame >= 1:
            self.instrument.write(f":FUNCtion:WREPlay:FEND {frame}")
        else:
            print("Invalid frame value.")

    def get_wreplay_fend(self):
        """
        Query the end frame of waveform playback.
        
        Parameter:
        None
        
        Return:
        int: End frame
        """
        resp = self.instrument.query(":FUNCtion:WREPlay:FEND?")
        try:
            return int(resp)
        except Exception:
            return resp

    def get_wreplay_fmax(self):
        """
        Query the maximum number of frames that can be played (max frames recorded).
        
        Parameter:
        None
        
        Return:
        int: Maximum number of frames
        """
        resp = self.instrument.query(":FUNCtion:WREPlay:FMAX?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_wreplay_finterval(self, interval):
        """
        Set the time interval between frames in waveform playback.
        
        Parameter:
        interval (float): 100e-9 to 10.0 (seconds)
        
        Return:
        None
        """
        if isinstance(interval, (float, int)) and 1e-7 <= interval <= 10.0:
            self.instrument.write(f":FUNCtion:WREPlay:FINTerval {interval}")
        else:
            print("Invalid interval. Must be between 100ns and 10s.")

    def get_wreplay_finterval(self):
        """
        Query the time interval between frames in waveform playback.
        
        Parameter:
        None
        
        Return:
        float: Time interval in seconds
        """
        resp = self.instrument.query(":FUNCtion:WREPlay:FINTerval?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_wreplay_mode(self, mode):
        """
        Set the waveform playback mode.
        
        Parameter:
        mode (str): "REPEAT" or "SINGLE"
        
        Return:
        None
        """
        allowed = {"REPEAT", "SINGLE"}
        mode = mode.upper()
        if mode in allowed:
            self.instrument.write(f":FUNCtion:WREPlay:MODE {mode}")
        else:
            print("Invalid mode. Allowed: REPEAT, SINGLE.")

    def get_wreplay_mode(self):
        """
        Query the waveform playback mode.
        
        Parameter:
        None
        
        Return:
        str: "REP" or "SING"
        """
        return self.instrument.query(":FUNCtion:WREPlay:MODE?")

    def set_wreplay_direction(self, direction):
        """
        Set the waveform playback direction.
        
        Parameter:
        direction (str): "FORWARD" or "BACKWARD"
        
        Return:
        None
        """
        allowed = {"FORWARD", "BACKWARD"}
        direction = direction.upper()
        if direction in allowed:
            self.instrument.write(f":FUNCtion:WREPlay:DIRection {direction}")
        else:
            print("Invalid direction. Allowed: FORWARD, BACKWARD.")

    def get_wreplay_direction(self):
        """
        Query the waveform playback direction.
        
        Parameter:
        None
        
        Return:
        str: "FORW" or "BACK"
        """
        return self.instrument.query(":FUNCtion:WREPlay:DIRection?")

    def set_wreplay_operate(self, opt):
        """
        Start, pause, or stop the waveform playback.
        
        Parameter:
        opt (str): "PLAY", "PAUSE", or "STOP"
        
        Return:
        None
        """
        allowed = {"PLAY", "PAUSE", "STOP"}
        opt = opt.upper()
        if opt in allowed:
            self.instrument.write(f":FUNCtion:WREPlay:OPERate {opt}")
        else:
            print("Invalid option. Allowed: PLAY, PAUSE, STOP.")

    def get_wreplay_operate(self):
        """
        Query the status of the waveform playback.
        
        Parameter:
        None
        
        Return:
        str: "PLAY", "PAUS", or "STOP"
        """
        return self.instrument.query(":FUNCtion:WREPlay:OPERate?")

    def set_wreplay_fcurrent(self, frame):
        """
        Set the current frame in waveform playback.
        
        Parameter:
        frame (int): 1 to max frames recorded
        
        Return:
        None
        """
        if isinstance(frame, int) and frame >= 1:
            self.instrument.write(f":FUNCtion:WREPlay:FCURrent {frame}")
        else:
            print("Invalid frame value.")

    def get_wreplay_fcurrent(self):
        """
        Query the current frame in waveform playback.
        
        Parameter:
        None
        
        Return:
        int: Current frame
        """
        resp = self.instrument.query(":FUNCtion:WREPlay:FCURrent?")
        try:
            return int(resp)
        except Exception:
            return resp

class LAN:
    """
    The LAN commands are used to set/query network parameters.
    """
    def __init__(self, instrument,data_handler):
        self.instrument = instrument
        self.data_handler = data_handler

    def set_dhcp(self, state):
        """
        Turn on or off the DHCP configuration mode.
        
        Parameter:
        state (int or str): 1/0 or "ON"/"OFF"
        
        Return:
        None
        """
        if state in [1, 0]:
            val = state
        elif isinstance(state, str) and state.upper() in {"ON", "OFF"}:
            val = 1 if state.upper() == "ON" else 0
        else:
            print("Invalid state. Use 1, 0, 'ON', or 'OFF'.")
            return
        self.instrument.write(f":LAN:DHCP {val}")

    def get_dhcp(self):
        """
        Query the on/off status of the current DHCP configuration mode.
        
        Parameter:
        None
        
        Return:
        int: 1 (on) or 0 (off)
        """
        resp = self.instrument.query(":LAN:DHCP?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_autoip(self, state):
        """
        Turn on or off the Auto IP configuration mode.
        
        Parameter:
        state (int or str): 1/0 or "ON"/"OFF"
        
        Return:
        None
        """
        if state in [1, 0]:
            val = state
        elif isinstance(state, str) and state.upper() in {"ON", "OFF"}:
            val = 1 if state.upper() == "ON" else 0
        else:
            print("Invalid state. Use 1, 0, 'ON', or 'OFF'.")
            return
        self.instrument.write(f":LAN:AUT {val}")

    def get_autoip(self):
        """
        Query the on/off status of the current Auto IP configuration mode.
        
        Parameter:
        None
        
        Return:
        int: 1 (on) or 0 (off)
        """
        resp = self.instrument.query(":LAN:AUT?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_gateway(self, gateway):
        """
        Set the default gateway.
        
        Parameter:
        gateway (str): IP address in nnn,nnn,nnn,nnn format
        
        Return:
        None
        """
        self.instrument.write(f":LAN:GATeway {gateway}")

    def get_gateway(self):
        """
        Query the default gateway.
        
        Parameter:
        None
        
        Return:
        str: Current gateway
        """
        return self.instrument.query(":LAN:GATeway?")

    def set_dns(self, dns):
        """
        Set the DNS address.
        
        Parameter:
        dns (str): IP address in nnn,nnn,nnn,nnn format
       
        Return:
        None
        """
        self.instrument.write(f":LAN:DNS {dns}")

    def get_dns(self):
        """
        Query the DNS address.
        
        Parameter:
        None
        
        Return:
        str: Current DNS address
        """
        return self.instrument.query(":LAN:DNS?")

    def get_mac(self):
        """
        Query the MAC address of the instrument.
        
        Parameter:
        None
        
        Return:
        str: MAC address
        """
        return self.instrument.query(":LAN:MAC?")

    def set_manual(self, state):
        """
        Turn on or off the static IP configuration mode.
        
        Parameter:
        state (int or str): 1/0 or "ON"/"OFF"
       
        Return:
        None
        """
        if state in [1, 0]:
            val = state
        elif isinstance(state, str) and state.upper() in {"ON", "OFF"}:
            val = 1 if state.upper() == "ON" else 0
        else:
            print("Invalid state. Use 1, 0, 'ON', or 'OFF'.")
            return
        self.instrument.write(f":LAN:MANual {val}")

    def get_manual(self):
        """
        Query the on/off status of the static IP configuration mode.
        
        Parameter:
        None
        
        Return:
        int: 1 (on) or 0 (off)
        """
        resp = self.instrument.query(":LAN:MANual?")
        try:
            return int(resp)
        except Exception:
            return resp

    def initiate(self):
        """
        Initiate the network parameters.
        
        Parameter:
        None
        
        Return:
        None
        """
        self.instrument.write(":LAN:INITiate")

    def set_ipaddress(self, ip):
        """
        Set the IP address of the instrument.
        
        Parameter:
        ip (str): IP address in nnn,nnn,nnn,nnn format
        
        Return:
        None
        """
        self.instrument.write(f":LAN:IPADdress {ip}")

    def get_ipaddress(self):
        """
        Query the IP address of the instrument.
        
        Parameter:
        None
        
        Return:
        str: Current IP address
        """
        return self.instrument.query(":LAN:IPADdress?")

    def set_smask(self, mask):
        """
        Set the subnet mask.
        
        Parameter:
        mask (str): Subnet mask in nnn,nnn,nnn,nnn format
        
        Return:
        None
        """
        self.instrument.write(f":LAN:SMASk {mask}")

    def get_smask(self):
        """
        Query the subnet mask.
        
        Parameter:
        None
        
        Return:
        str: Current subnet mask
        """
        return self.instrument.query(":LAN:SMASk?")

    def get_status(self):
        """
        Query the current network configuration status.
        
        Parameter:
        None
        
        Return:
        str: One of "UNLINK", "INIT", "IPCONFLICT", "CONFIGURED", "DHCPFAILED"
        """
        return self.instrument.query(":LAN:STATus?")

    def get_visa(self):
        """
        Query the VISA address of the instrument.
        
        Parameter:
        None
        
        Return:
        str: VISA address
        """
        return self.instrument.query(":LAN:VISA?")

    def apply(self):
        """
        Apply the network configuration.
        
        Parameter:
        None
        
        Return:
        None
        """
        self.instrument.write(":LAN:APPLy")

class Math:
    """
    The Math commands are used to set the operations between the waveforms of multiple channels.
    """
    def __init__(self, instrument,data_handler):
        self.instrument = instrument
        self.data_handler = data_handler

    def set_display(self, state):
        """
        Turn on or off the math waveform display.
        
        Parameter:
        state (int or str): 1/0 or "ON"/"OFF"
        
        Return:
        None
        """
        if state in [1, 0]:
            val = state
        elif isinstance(state, str) and state.upper() in {"ON", "OFF"}:
            val = 1 if state.upper() == "ON" else 0
        else:
            print("Invalid state. Use 1, 0, 'ON', or 'OFF'.")
            return
        self.instrument.write(f":MATH:DISPlay {val}")

    def get_display(self):
        """
        Query the math waveform display status.
        
        Parameter:
        None
        
        Return:
        int: 1 (on) or 0 (off)
        """
        resp = self.instrument.query(":MATH:DISPlay?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_operator(self, op):
        """
        Set the math operation type.
        
        Parameter:
        op (str): Allowed values include "ADD", "SUB", "MUL", "DIV", "FFT", "AND", "OR", "XOR", "NOT", "INTG", "DIFF", "SQRT", "LG", "LN", "EXP", "ABS", "LPF", "HPF", "BPF", "BSF"
        
        Return:
        None
        """
        allowed = {"ADD", "SUB", "MUL", "DIV", "FFT", "AND", "OR", "XOR", "NOT", "INTG", "DIFF", "SQRT", "LG", "LN", "EXP", "ABS", "LPF", "HPF", "BPF", "BSF"}
        op = op.upper()
        if op in allowed:
            self.instrument.write(f":MATH:OPERator {op}")
        else:
            print(f"Invalid operator. Allowed: {allowed}")

    def get_operator(self):
        """
        Query the math operation type.
        Parameter:
            None
        Return:
            str: Operator
        """
        return self.instrument.query(":MATH:OPERator?")

    def set_source1(self, src):
        """
        Set the source 1 for the math operation.
        
        Parameter:
        src (str): "CHAN1", "CHAN2", "FX", etc.
        
        Return:
        None
        """
        allowed = {"CHAN1", "CHAN2", "FX"}
        src = src.upper()
        if src in allowed:
            self.instrument.write(f":MATH:SOURce1 {src}")
        else:
            print(f"Invalid source. Allowed: {allowed}")

    def get_source1(self):
        """
        Query the source 1 for the math operation.
        
        Parameter:
        None
        
        Return:
        str: Source 1
        """
        return self.instrument.query(":MATH:SOURce1?")

    def set_source2(self, src):
        """
        Set the source 2 for the math operation.
        
        Parameter:
        src (str): "CHAN1", "CHAN2", "FX", etc.
        
        Return:
        None
        """
        allowed = {"CHAN1", "CHAN2", "FX"}
        src = src.upper()
        if src in allowed:
            self.instrument.write(f":MATH:SOURce2 {src}")
        else:
            print(f"Invalid source. Allowed: {allowed}")

    def get_source2(self):
        """
        Query the source 2 for the math operation.
        
        Parameter:
        None
        
        Return:
        str: Source 2
        """
        return self.instrument.query(":MATH:SOURce2?")

    def set_scale(self, scale):
        """
        Set the vertical scale of the math waveform.
        
        Parameter:
        scale (float): Vertical scale in V/div
        
        Return:
        None
        """
        self.instrument.write(f":MATH:SCALe {scale}")

    def get_scale(self):
        """
        Query the vertical scale of the math waveform.
        
        Parameter:
        None
        
        Return:
        float: Vertical scale in V/div
        """
        resp = self.instrument.query(":MATH:SCALe?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_offset(self, offset):
        """
        Set the vertical offset of the math waveform.
        
        Parameter:
        offset (float): Vertical offset in V
        
        Return:
        None
        """
        self.instrument.write(f":MATH:OFFSet {offset}")

    def get_offset(self):
        """
        Query the vertical offset of the math waveform.
        
        Parameter:
        None
        
        Return:
        float: Vertical offset in V
        """
        resp = self.instrument.query(":MATH:OFFSet?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_invert(self, state):
        """
        Enable or disable math waveform inversion.
        
        Parameter:
        state (int or str): 1/0 or "ON"/"OFF"
        
        Return:
        None
        """
        if state in [1, 0]:
            val = state
        elif isinstance(state, str) and state.upper() in {"ON", "OFF"}:
            val = 1 if state.upper() == "ON" else 0
        else:
            print("Invalid state. Use 1, 0, 'ON', or 'OFF'.")
            return
        self.instrument.write(f":MATH:INVert {val}")

    def get_invert(self):
        """
        Query the math waveform inversion status.
        
        Parameter:
        None
        
        Return:
        int: 1 (on) or 0 (off)
        """
        resp = self.instrument.query(":MATH:INVert?")
        try:
            return int(resp)
        except Exception:
            return resp

    def reset(self):
        """
        Reset the math operation settings to default.
        
        Parameter:
        None
        
        Return:
        None
        """
        self.instrument.write(":MATH:RESet")
    def set_fft_source(self, src):
        """
        Set the source of FFT operation/filter.
        
        Parameter:
        src (str): "CHANnel1" or "CHANnel2"
        
        Return:
        None
        """
        allowed = {"CHANNEL1", "CHANNEL2", "CHAN1", "CHAN2"}
        src_up = src.upper()
        if src_up in allowed:
            val = "CHANnel1" if src_up in {"CHANNEL1", "CHAN1"} else "CHANnel2"
            self.instrument.write(f":MATH:FFT:SOURce {val}")
        else:
            print("Invalid source. Allowed: CHANnel1, CHANnel2.")

    def get_fft_source(self):
        """
        Query the source of FFT operation/filter.
        
        Parameter:
        None
        
        Return:
        str: "CHAN1" or "CHAN2"
        """
        return self.instrument.query(":MATH:FFT:SOURce?")

    def set_fft_window(self, wnd):
        """
        Set the window function of the FFT operation.
        
        Parameter:
        wnd (str): One of {"RECTangle", "BLACkman", "HANNing", "HAMMing", "FLATtop", "TRIangle"}
        
        Return:
        None
        """
        allowed = {"RECTANGLE", "BLACKMAN", "HANNING", "HAMMING", "FLATTOP", "TRIANGLE"}
        wnd_up = wnd.upper()
        if wnd_up in allowed:
            self.instrument.write(f":MATH:FFT:WINDow {wnd}")
        else:
            print("Invalid window. Allowed: RECTangle, BLACkman, HANNing, HAMMing, FLATtop, TRIangle.")

    def get_fft_window(self):
        """
        Query the window function of the FFT operation.
        
        Parameter:
        None
        
        Return:
        str: "RECT", "BLAC", "HANN", "HAMM", "FLAT", or "TRI"
        """
        return self.instrument.query(":MATH:FFT:WINDow?")

    def enable_fft_split(self, enable):
        """
        Enable or disable the half-screen display mode of the FFT operation.
        
        Parameter:
        enable (int or str): 1/0 or "ON"/"OFF"
        
        Return:
        None
        """
        if enable in [1, 0]:
            val = enable
        elif isinstance(enable, str) and enable.upper() in {"ON", "OFF"}:
            val = 1 if enable.upper() == "ON" else 0
        else:
            print("Invalid enable value. Use 1, 0, 'ON', or 'OFF'.")
            return
        self.instrument.write(f":MATH:FFT:SPLit {val}")

    def is_fft_split_enabled(self):
        """
        Query the status of the half-screen display mode of the FFT operation.
        
        Parameter:
        None
        
        Return:
        int: 1 (enabled) or 0 (disabled)
        """
        resp = self.instrument.query(":MATH:FFT:SPLit?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_fft_unit(self, unit):
        """
        Set the vertical unit of the FFT operation result.
        
        Parameter:
        unit (str): "VRMS" or "DB"
        
        Return:
        None
        """
        allowed = {"VRMS", "DB"}
        unit_up = unit.upper()
        if unit_up in allowed:
            self.instrument.write(f":MATH:FFT:UNIT {unit_up}")
        else:
            print("Invalid unit. Allowed: VRMS, DB.")

    def get_fft_unit(self):
        """
        Query the vertical unit of the FFT operation result.
        
        Parameter:
        None
        
        Return:
        str: "VRMS" or "DB"
        """
        return self.instrument.query(":MATH:FFT:UNIT?")

    def set_fft_hscale(self, hsc):
        """
        Set the horizontal scale of the FFT operation result (Hz).
        
        Parameter:
        hsc (float): Horizontal scale in Hz
        
        Return:
        None
        """
        self.instrument.write(f":MATH:FFT:HSCale {hsc}")

    def get_fft_hscale(self):
        """
        Query the horizontal scale of the FFT operation result (Hz).
        
        Parameter:
        None
        
        Return:
        float: Horizontal scale in Hz
        """
        resp = self.instrument.query(":MATH:FFT:HSCale?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_fft_hcenter(self, cent):
        """
        Set the center frequency of the FFT operation result (Hz).
        
        Parameter:
        cent (float): Center frequency in Hz
        
        Return:
        None
        """
        self.instrument.write(f":MATH:FFT:HCENter {cent}")

    def get_fft_hcenter(self):
        """
        Query the center frequency of the FFT operation result (Hz).
        
        Parameter:
        None
        
        Return:
        float: Center frequency in Hz
        """
        resp = self.instrument.query(":MATH:FFT:HCENter?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_fft_mode(self, mode):
        """
        Set the FFT mode.
        
        Parameter:
        mode (str): "TRACe" or "MEMory"
        
        Return:
        None
        """
        allowed = {"TRACE", "MEMORY", "TRACe", "MEMory"}
        mode_up = mode.upper()
        if mode_up in allowed:
            val = "TRACe" if mode_up.startswith("TRAC") else "MEMory"
            self.instrument.write(f":MATH:FFT:MODE {val}")
        else:
            print("Invalid mode. Allowed: TRACe, MEMory.")

    def get_fft_mode(self):
        """
        Query the FFT mode.
        
        Parameter:
        None
        
        Return:
        str: "TRAC" or "MEM"
        """
        return self.instrument.query(":MATH:FFT:MODE?")

    def set_filter_type(self, ftype):
        """
        Set the filter type for math filter operation.
        
        Parameter:
        ftype (str): "LPASs", "HPASs", "BPASs", or "BSTOP"
        
        Return:
        None
        """
        allowed = {"LPASS", "HPASS", "BPASS", "BSTOP", "LPASs", "HPASs", "BPASs", "BSTOP"}
        ftype_up = ftype.upper()
        if ftype_up in allowed:
            val = ftype if ftype_up in {"LPASs", "HPASs", "BPASs", "BSTOP"} else ftype_up.capitalize()
            self.instrument.write(f":MATH:FILTer:TYPE {val}")
        else:
            print("Invalid filter type. Allowed: LPASs, HPASs, BPASs, BSTOP.")

    def get_filter_type(self):
        """
        Query the filter type for math filter operation.
        
        Parameter:
        None
        
        Return:
        str: "LPAS", "HPAS", "BPAS", or "BSTO"
        """
        return self.instrument.query(":MATH:FILTer:TYPE?")

    def set_filter_w1(self, freq1):
        """
        Set the cutoff frequency 1 (ωc1) for filter operation (Hz).
        
        Parameter:
        freq1 (float): Cutoff frequency 1 in Hz
        
        Return:
        None
        """
        self.instrument.write(f":MATH:FILTer:W1 {freq1}")

    def get_filter_w1(self):
        """
        Query the cutoff frequency 1 (ωc1) for filter operation (Hz).
        
        Parameter:
        None
        
        Return:
        float: Cutoff frequency 1 in Hz
        """
        resp = self.instrument.query(":MATH:FILTer:W1?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_filter_w2(self, freq2):
        """
        Set the cutoff frequency 2 (ωc2) for filter operation (Hz).
        
        Parameter:
        freq2 (float): Cutoff frequency 2 in Hz
        
        Return:
        None
        """
        self.instrument.write(f":MATH:FILTer:W2 {freq2}")

    def get_filter_w2(self):
        """
        Query the cutoff frequency 2 (ωc2) for filter operation (Hz).
        
        Parameter:
        None
        
        Return:
        float: Cutoff frequency 2 in Hz
        """
        resp = self.instrument.query(":MATH:FILTer:W2?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_option_start(self, sta):
        """
        Set the start point of the waveform math operation.
        
        Parameter:
        sta (int): Start point (0 to end-1)
        
        Return:
        None
        """
        self.instrument.write(f":MATH:OPTion:STARt {sta}")

    def get_option_start(self):
        """
        Query the start point of the waveform math operation.
        
        Parameter:
        None
        
        Return:
        int: Start point
        """
        resp = self.instrument.query(":MATH:OPTion:STARt?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_option_end(self, end):
        """
        Set the end point of the waveform math operation.
        
        Parameter:
        end (int): End point (start+1 to 1199)
        
        Return:
        None
        """
        self.instrument.write(f":MATH:OPTion:END {end}")

    def get_option_end(self):
        """
        Query the end point of the waveform math operation.
        
        Parameter:
        None
        
        Return:
        int: End point
        """
        resp = self.instrument.query(":MATH:OPTion:END?")
        try:
            return int(resp)
        except Exception:
            return resp

    def enable_option_invert(self, enable):
        """
        Enable or disable the inverted display mode of the operation result.
        
        Parameter:
        enable (int or str): 1/0 or "ON"/"OFF"
        
        Return:
        None
        """
        if enable in [1, 0]:
            val = enable
        elif isinstance(enable, str) and enable.upper() in {"ON", "OFF"}:
            val = 1 if enable.upper() == "ON" else 0
        else:
            print("Invalid enable value. Use 1, 0, 'ON', or 'OFF'.")
            return
        self.instrument.write(f":MATH:OPTion:INVert {val}")

    def is_option_invert_enabled(self):
        """
        Query the inverted display mode status of the operation result.
        
        Parameter:
        None
        
        Return:
        int: 1 (enabled) or 0 (disabled)
        """
        resp = self.instrument.query(":MATH:OPTion:INVert?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_option_sensitivity(self, sens):
        """
        Set the sensitivity of the logic operation.
        
        Parameter:
        sens (float): Sensitivity (0 to 0.96, step 0.08)
        
        Return:
        None
        """
        self.instrument.write(f":MATH:OPTion:SENSitivity {sens}")

    def get_option_sensitivity(self):
        """
        Query the sensitivity of the logic operation.
        
        Parameter:
        None
        
        Return:
        float: Sensitivity
        """
        resp = self.instrument.query(":MATH:OPTion:SENSitivity?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_option_distance(self, dist):
        """
        Set the smoothing window width of differential operation.
        
        Parameter:
        dist (int): Window width (3 to 201)
        
        Return:
        None
        """
        self.instrument.write(f":MATH:OPTion:DIStance {dist}")

    def get_option_distance(self):
        """
        Query the smoothing window width of differential operation.
        
        Parameter:
        None
        
        Return:
        int: Window width
        """
        resp = self.instrument.query(":MATH:OPTion:DIStance?")
        try:
            return int(resp)
        except Exception:
            return resp

    def enable_option_ascale(self, enable):
        """
        Enable or disable the auto scale setting of the operation result.
        
        Parameter:
        enable (int or str): 1/0 or "ON"/"OFF"
        
        Return:
        None
        """
        if enable in [1, 0]:
            val = enable
        elif isinstance(enable, str) and enable.upper() in {"ON", "OFF"}:
            val = 1 if enable.upper() == "ON" else 0
        else:
            print("Invalid enable value. Use 1, 0, 'ON', or 'OFF'.")
            return
        self.instrument.write(f":MATH:OPTion:ASCale {val}")

    def is_option_ascale_enabled(self):
        """
        Query the status of the auto scale setting of the operation result.
        
        Parameter:
        None
        
        Return:
        int: 1 (enabled) or 0 (disabled)
        """
        resp = self.instrument.query(":MATH:OPTion:ASCale?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_option_threshold1(self, thre):
        """
        Set the threshold level of source A in logic operations.
        
        Parameter:
        thre (float): Threshold level in V
        
        Return:
        None
        """
        self.instrument.write(f":MATH:OPTion:THReshold1 {thre}")

    def get_option_threshold1(self):
        """
        Query the threshold level of source A in logic operations.
        
        Parameter:
        None
        
        Return:
        float: Threshold level in V
        """
        resp = self.instrument.query(":MATH:OPTion:THReshold1?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_option_threshold2(self, thre):
        """
        Set the threshold level of source B in logic operations.
        
        Parameter:
        thre (float): Threshold level in V
        
        Return:
        None
        """
        self.instrument.write(f":MATH:OPTion:THReshold2 {thre}")

    def get_option_threshold2(self):
        """
        Query the threshold level of source B in logic operations.
        
        Parameter:
        None
        
        Return:
        float: Threshold level in V
        """
        resp = self.instrument.query(":MATH:OPTion:THReshold2?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_option_fx_source1(self, src):
        """
        Set source A of the inner layer operation of compound operation.
        
        Parameter:
        src (str): "CHANnel1" or "CHANnel2"
        
        Return:
        None
        """
        allowed = {"CHANNEL1", "CHANNEL2", "CHAN1", "CHAN2"}
        src_up = src.upper()
        if src_up in allowed:
            val = "CHANnel1" if src_up in {"CHANNEL1", "CHAN1"} else "CHANnel2"
            self.instrument.write(f":MATH:OPTion:FX:SOURce1 {val}")
        else:
            print("Invalid source. Allowed: CHANnel1, CHANnel2.")

    def get_option_fx_source1(self):
        """
        Query source A of the inner layer operation of compound operation.
        
        Parameter:
        None
        
        Return:
        str: "CHAN1" or "CHAN2"
        """
        return self.instrument.query(":MATH:OPTion:FX:SOURce1?")

    def set_option_fx_source2(self, src):
        """
        Set source B of the inner layer operation of compound operation.
        
        Parameter:
        src (str): "CHANnel1" or "CHANnel2"
        
        Return:
        None
        """
        allowed = {"CHANNEL1", "CHANNEL2", "CHAN1", "CHAN2"}
        src_up = src.upper()
        if src_up in allowed:
            val = "CHANnel1" if src_up in {"CHANNEL1", "CHAN1"} else "CHANnel2"
            self.instrument.write(f":MATH:OPTion:FX:SOURce2 {val}")
        else:
            print("Invalid source. Allowed: CHANnel1, CHANnel2.")

    def get_option_fx_source2(self):
        """
        Query source B of the inner layer operation of compound operation.
        
        Parameter:
        None
        
        Return:
        str: "CHAN1" or "CHAN2"
        """
        return self.instrument.query(":MATH:OPTion:FX:SOURce2?")

    def set_option_fx_operator(self, op):
        """
        Set the operator of the inner layer operation of compound operation.
        
        Parameter:
        op (str): "ADD", "SUBTract", "MULTiply", or "DIVision"
        
        Return:
        None
        """
        allowed = {"ADD", "SUBTRACT", "MULTIPLY", "DIVISION", "SUBTRACT", "SUBTract", "MULTiply", "DIVision"}
        op_up = op.upper()
        if op_up in allowed:
            val = op if op_up in {"ADD", "SUBTRACT", "MULTIPLY", "DIVISION"} else op
            self.instrument.write(f":MATH:OPTion:FX:OPERator {val}")
        else:
            print("Invalid operator. Allowed: ADD, SUBTract, MULTiply, DIVision.")

    def get_option_fx_operator(self):
        """
        Query the operator of the inner layer operation of compound operation.
        
        Parameter:
        None
        
        Return:
        str: "ADD", "SUBT", "MULT", or "DIV"
        """
        return self.instrument.query(":MATH:OPTion:FX:OPERator?")
class Mask:
    """
    The Mask commands are used to set and query the pass/fail test parameters.
    """
    def __init__(self, instrument,data_handler):
        self.instrument = instrument
        self.data_handler = data_handler

    def enable(self, state):
        """
        Enable or disable the pass/fail test.
        
        Parameter:
        state (int or str): 1/0 or "ON"/"OFF"
        
        Return:
        None
        """
        if state in [1, 0]:
            val = state
        elif isinstance(state, str) and state.upper() in {"ON", "OFF"}:
            val = 1 if state.upper() == "ON" else 0
        else:
            print("Invalid state. Use 1, 0, 'ON', or 'OFF'.")
            return
        self.instrument.write(f":MASK:ENABle {val}")

    def is_enabled(self):
        """
        Query the status of the pass/fail test.
        
        Parameter:
        None
        
        Return:
        int: 1 (enabled) or 0 (disabled)
        """
        resp = self.instrument.query(":MASK:ENABle?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_source(self, source):
        """
        Set the source of the pass/fail test.
        
        Parameter:
        source (str): "CHANnel1" or "CHANnel2"
        
        Return:
        None
        """
        allowed = {"CHANNEL1", "CHANNEL2", "CHAN1", "CHAN2"}
        src_up = source.upper()
        if src_up in allowed:
            val = "CHANnel1" if src_up in {"CHANNEL1", "CHAN1"} else "CHANnel2"
            self.instrument.write(f":MASK:SOURce {val}")
        else:
            print("Invalid source. Allowed: CHANnel1, CHANnel2.")

    def get_source(self):
        """
        Query the source of the pass/fail test.
        
        Parameter:
        None
        
        Return:
        str: "CHAN1" or "CHAN2"
        """
        return self.instrument.query(":MASK:SOURce?")

    def operate(self, oper):
        """
        Run or stop the pass/fail test.
        
        Parameter:
        oper (str): "RUN" or "STOP"
        
        Return:
        None
        """
        allowed = {"RUN", "STOP"}
        oper_up = oper.upper()
        if oper_up in allowed:
            self.instrument.write(f":MASK:OPERate {oper_up}")
        else:
            print("Invalid operation. Allowed: RUN, STOP.")

    def get_operate(self):
        """
        Query the status of the pass/fail test.
        
        Parameter:
        None
        
        Return:
        str: "RUN" or "STOP"
        """
        return self.instrument.query(":MASK:OPERate?")

    def enable_display(self, state):
        """
        Enable or disable the statistic information when the pass/fail test is enabled.
        
        Parameter:
        state (int or str): 1/0 or "ON"/"OFF"
        
        Return:
        None
        """
        if state in [1, 0]:
            val = state
        elif isinstance(state, str) and state.upper() in {"ON", "OFF"}:
            val = 1 if state.upper() == "ON" else 0
        else:
            print("Invalid state. Use 1, 0, 'ON', or 'OFF'.")
            return
        self.instrument.write(f":MASK:MDISplay {val}")

    def is_display_enabled(self):
        """
        Query the status of the statistic information.
        
        Parameter:
        None
        
        Return:
        int: 1 (enabled) or 0 (disabled)
        """
        resp = self.instrument.query(":MASK:MDISplay?")
        try:
            return int(resp)
        except Exception:
            return resp

    def enable_stop_on_fail(self, state):
        """
        Turn the "Stop on Fail" function on or off.
        
        Parameter:
        state (int or str): 1/0 or "ON"/"OFF"
        
        Return:
        None
        """
        if state in [1, 0]:
            val = state
        elif isinstance(state, str) and state.upper() in {"ON", "OFF"}:
            val = 1 if state.upper() == "ON" else 0
        else:
            print("Invalid state. Use 1, 0, 'ON', or 'OFF'.")
            return
        self.instrument.write(f":MASK:SOOutput {val}")

    def is_stop_on_fail_enabled(self):
        """
        Query the status of the "Stop on Fail" function.
        
        Parameter:
        None
        
        Return:
        int: 1 (enabled) or 0 (disabled)
        """
        resp = self.instrument.query(":MASK:SOOutput?")
        try:
            return int(resp)
        except Exception:
            return resp

    def enable_sound(self, state):
        """
        Enable or disable the sound prompt when failed waveforms are detected.
        
        Parameter:
        state (int or str): 1/0 or "ON"/"OFF"
        
        Return:
        None
        """
        if state in [1, 0]:
            val = state
        elif isinstance(state, str) and state.upper() in {"ON", "OFF"}:
            val = 1 if state.upper() == "ON" else 0
        else:
            print("Invalid state. Use 1, 0, 'ON', or 'OFF'.")
            return
        self.instrument.write(f":MASK:OUTPut {val}")

    def is_sound_enabled(self):
        """
        Query the status of the sound prompt when failed waveforms are detected.
        
        Parameter:
        None
        
        Return:
        int: 1 (enabled) or 0 (disabled)
        """
        resp = self.instrument.query(":MASK:OUTPut?")
        try:
            return int(resp)
        except Exception:
            return resp
    def set_x(self, x):
        """
        Set the horizontal adjustment parameter in the pass/fail test mask.
        
        Parameter:
        x (float): Value between 0.02 and 4 (step 0.02)
        
        Return:
        None
        """
        if isinstance(x, (float, int)) and 0.02 <= x <= 4:
            self.instrument.write(f":MASK:X {x}")
        else:
            print("Invalid x value. Must be between 0.02 and 4.")

    def get_x(self):
        """
        Query the horizontal adjustment parameter in the pass/fail test mask.
        
        Parameter:
        None
        
        Return:
        float: Horizontal adjustment parameter
        """
        resp = self.instrument.query(":MASK:X?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_y(self, y):
        """
        Set the vertical adjustment parameter in the pass/fail test mask.
        Parameter:
        y (float): Value between 0.04 and 5.12 (step 0.04)
        Return:
        None
        """
        if isinstance(y, (float, int)) and 0.04 <= y <= 5.12:
            self.instrument.write(f":MASK:Y {y}")
        else:
            print("Invalid y value. Must be between 0.04 and 5.12.")

    def get_y(self):
        """
        Query the vertical adjustment parameter in the pass/fail test mask.
        
        Parameter:
        None
        
        Return:
        float: Vertical adjustment parameter
        """
        resp = self.instrument.query(":MASK:Y?")
        try:
            return float(resp)
        except Exception:
            return resp

    def create(self):
        """
        Create the pass/fail test mask using the current horizontal and vertical adjustment parameters.
        
        Parameter:
        None
        
        Return:
        None
        """
        self.instrument.write(":MASK:CREate")

    def get_passed(self):
        """
        Query the number of passed frames in the pass/fail test.
        
        Parameter:
        None
        
        Return:
        int: Number of passed frames
        """
        resp = self.instrument.query(":MASK:PASSed?")
        try:
            return int(resp)
        except Exception:
            return resp

    def get_failed(self):
        """
        Query the number of failed frames in the pass/fail test.
        
        Parameter:
        None
        
        Return:
        int: Number of failed frames
        """
        resp = self.instrument.query(":MASK:FAILed?")
        try:
            return int(resp)
        except Exception:
            return resp

    def get_total(self):
        """
        Query the total number of frames in the pass/fail test.
        
        Parameter:
        None
        
        Return:
        int: Total number of frames
        """
        resp = self.instrument.query(":MASK:TOTal?")
        try:
            return int(resp)
        except Exception:
            return resp

    def reset(self):
        """
        Reset the numbers of passed, failed, and total frames in the pass/fail test to 0.
        
        Parameter:
        None
        
        Return:
        None
        """
        self.instrument.write(":MASK:RESet")

class Measure:
    """
    The Measure commands are used to set and query measurement parameters and statistics.
    """
    def __init__(self, instrument,data_handler):
        self.instrument = instrument
        self.data_handler = data_handler

    def set_source(self, source):
        """
        Set the source for measurement.
        
        Parameter:
        source (str): "CHAN1", "CHAN2", "MATH", etc.
        
        Return:
        None
        """
        allowed = {"CHAN1", "CHAN2", "MATH"}
        src = source.upper()
        if src in allowed:
            self.instrument.write(f":MEAS:SOUR {src}")
        else:
            print(f"Invalid source. Allowed: {allowed}")

    def get_source(self):
        """
        Query the source for measurement.
        
        Parameter:
        None
        
        Return:
        str: Current source
        """
        return self.instrument.query(":MEAS:SOUR?")

    def clear(self):
        """
        Clear all measurement results.
        
        Parameter:
        None
        
        Return:
        None
        """
        self.instrument.write(":MEAS:CLE")

    def recover(self):
        """
        Recover the last measurement result.
        
        Parameter:
        None
        
        Return:
        None
        """
        self.instrument.write(":MEAS:REC")

    def set_display(self, state):
        """
        Enable or disable the measurement result display.
        
        Parameter:
        state (int or str): 1/0 or "ON"/"OFF"
        
        Return:
        None
        """
        if state in [1, 0]:
            val = state
        elif isinstance(state, str) and state.upper() in {"ON", "OFF"}:
            val = 1 if state.upper() == "ON" else 0
        else:
            print("Invalid state. Use 1, 0, 'ON', or 'OFF'.")
            return
        self.instrument.write(f":MEAS:ADIS {val}")

    def is_display_enabled(self):
        """
        Query if the measurement result display is enabled.
        
        Parameter:
        None
        
        Return:
        int: 1 (enabled) or 0 (disabled)
        """
        resp = self.instrument.query(":MEAS:ADIS?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_auto_measure_source(self, source):
        """
        Set the source for auto measurement.
        
        Parameter:
        source (str): "CHAN1", "CHAN2", "MATH"
        
        Return:
        None
        """
        allowed = {"CHAN1", "CHAN2", "MATH"}
        src = source.upper()
        if src in allowed:
            self.instrument.write(f":MEAS:AMS {src}")
        else:
            print(f"Invalid source. Allowed: {allowed}")

    def get_auto_measure_source(self):
        """
        Query the source for auto measurement.
        
        Parameter:
        None
        
        Return:
        str: Current source
        """
        return self.instrument.query(":MEAS:AMS?")

    def set_setup_max(self, value):
        """
        Set the maximum threshold for measurement.
        
        Parameter:
        value (float): Threshold value
        
        Return:
        None
        """
        self.instrument.write(f":MEAS:SET:MAX {value}")

    def get_setup_max(self):
        """
        Query the maximum threshold for measurement.
        
        Parameter:
        None
        
        Return:
        float: Threshold value
        """
        resp = self.instrument.query(":MEAS:SET:MAX?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_setup_mid(self, value):
        """
        Set the middle threshold for measurement.
        
        Parameter:
        value (float): Threshold value
        
        Return:
        None
        """
        self.instrument.write(f":MEAS:SET:MID {value}")

    def get_setup_mid(self):
        """
        Query the middle threshold for measurement.
        
        Parameter:  
        None
        
        Return:
        float: Threshold value
        """
        resp = self.instrument.query(":MEAS:SET:MID?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_setup_min(self, value):
        """
        Set the minimum threshold for measurement.
        
        Parameter:
        value (float): Threshold value
        
        Return:
        None
        """
        self.instrument.write(f":MEAS:SET:MIN {value}")

    def get_setup_min(self):
        """
        Query the minimum threshold for measurement.
        
        Parameter:
        None
        
        Return:
        float: Threshold value
        """
        resp = self.instrument.query(":MEAS:SET:MIN?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_setup_psa(self, value):
        """
        Set the positive slope threshold A for measurement.
        
        Parameter:
        value (float): Threshold value
        
        Return:
        None
        """
        self.instrument.write(f":MEAS:SET:PSA {value}")

    def get_setup_psa(self):
        """
        Query the positive slope threshold A for measurement.
        
        Parameter:
        None
        
        Return:
        float: Threshold value
        """
        resp = self.instrument.query(":MEAS:SET:PSA?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_setup_psb(self, value):
        """
        Set the positive slope threshold B for measurement.
        
        Parameter:
        value (float): Threshold value
        
        Return:
        None
        """
        self.instrument.write(f":MEAS:SET:PSB {value}")

    def get_setup_psb(self):
        """
        Query the positive slope threshold B for measurement.
        
        Parameter:
        None
        
        Return:
        float: Threshold value
        """
        resp = self.instrument.query(":MEAS:SET:PSB?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_setup_dsa(self, value):
        """
        Set the negative slope threshold A for measurement.
        
        Parameter:
        value (float): Threshold value
        
        Return:
        None
        """
        self.instrument.write(f":MEAS:SET:DSA {value}")

    def get_setup_dsa(self):
        """
        Query the negative slope threshold A for measurement.
        
        Parameter:
        None
        
        Return:
        float: Threshold value
        """
        resp = self.instrument.query(":MEAS:SET:DSA?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_setup_dsb(self, value):
        """
        Set the negative slope threshold B for measurement.
        
        Parameter:
        value (float): Threshold value
        
        Return:
        None
        """
        self.instrument.write(f":MEAS:SET:DSB {value}")

    def get_setup_dsb(self):
        """
        Query the negative slope threshold B for measurement.
        
        Parameter:
        None
        
        Return:
        float: Threshold value
        """
        resp = self.instrument.query(":MEAS:SET:DSB?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_statistic_display(self, state):
        """
        Enable or disable the statistic display for measurement.
        
        Parameter:
        state (int or str): 1/0 or "ON"/"OFF"
        
        Return:
        None
        """
        if state in [1, 0]:
            val = state
        elif isinstance(state, str) and state.upper() in {"ON", "OFF"}:
            val = 1 if state.upper() == "ON" else 0
        else:
            print("Invalid state. Use 1, 0, 'ON', or 'OFF'.")
            return
        self.instrument.write(f":MEAS:STAT:DISP {val}")

    def is_statistic_display_enabled(self):
        """
        Query if the statistic display for measurement is enabled.
        
        Parameter:
        None
        
        Return:
        int: 1 (enabled) or 0 (disabled)
        """
        resp = self.instrument.query(":MEAS:STAT:DISP?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_statistic_mode(self, mode):
        """
        Set the statistic mode for measurement.
        
        Parameter:
        mode (str): "ALL" or "CURR"
        
        Return:
        None
        """
        allowed = {"ALL", "CURR"}
        m = mode.upper()
        if m in allowed:
            self.instrument.write(f":MEAS:STAT:MODE {m}")
        else:
            print("Invalid mode. Allowed: ALL, CURR.")

    def get_statistic_mode(self):
        """
        Query the statistic mode for measurement.
        
        Parameter:
        None
        
        Return:
        str: "ALL" or "CURR"
        """
        return self.instrument.query(":MEAS:STAT:MODE?")

    def reset_statistic(self):
        """
        Reset the measurement statistics.
        
        Parameter:
        None
        
        Return:
        None
        """
        self.instrument.write(":MEAS:STAT:RES")

    def set_statistic_item(self, item):
        """
        Set the statistic item for measurement.
        Parameter:
            item (str): Measurement item name (e.g., "VPP", "VRMS", etc.)
        Return:
            None
        """
        allowed = {
            "VMAX", "VMIN", "VPP", "VTOP", "VBASE", "VAMP", "VUPPER", "VMID", "VLOWER",
            "VAVG", "VRMS", "OVERSHOOT", "PRESHOOT", "PER.VRMS", "VARIANCE",
            "PERIOD", "FREQ", "RISE", "FALL", "WIDTH", "DUTY", "DELAY", "PHASE",
            "+PULSES", "-PULSES", "+EDGES", "-EDGES", "+RATE", "-RATE", "AREA", "PER.AREA"
        }
        i = item.upper()
        if i in allowed:
            self.instrument.write(f":MEAS:STAT:ITEM {i}")
        else:
            print(f"Invalid item. Allowed: {allowed}")

    def get_statistic_item(self):
        """
        Query the statistic item for measurement.
        
        Parameter:
        None
        
        Return:
        str: Measurement item name
        """
        return self.instrument.query(":MEAS:STAT:ITEM?")

    def set_item(self, item):
        """
        Set the measurement item.
        
        Parameter:
        item (str): Measurement item name (e.g., "VPP", "VRMS", etc.)
        
        Return:
        None
        """
        allowed = {
            "VMAX", "VMIN", "VPP", "VTOP", "VBASE", "VAMP", "VUPPER", "VMID", "VLOWER",
            "VAVG", "VRMS", "OVERSHOOT", "PRESHOOT", "PER.VRMS", "VARIANCE",
            "PERIOD", "FREQ", "RISE", "FALL", "WIDTH", "DUTY", "DELAY", "PHASE",
            "+PULSES", "-PULSES", "+EDGES", "-EDGES", "+RATE", "-RATE", "AREA", "PER.AREA"
        }
        i = item.upper()
        if i in allowed:
            self.instrument.write(f":MEAS:ITEM {i}")
        else:
            print(f"Invalid item. Allowed: {allowed}")

    def get_item(self):
        """
        Query the measurement item.
        
        Parameter:
        None
        
        Return:
        str: Measurement item name
        """
        return self.instrument.query(":MEAS:ITEM?")

    def set_counter_source(self, source):
        """
        Set the source for the measurement counter.
        
        Parameter:
        source (str): "CHAN1", "CHAN2", "MATH"
        
        Return:
        None
        """
        allowed = {"CHAN1", "CHAN2", "MATH"}
        src = source.upper()
        if src in allowed:
            self.instrument.write(f":MEAS:COUN:SOUR {src}")
        else:
            print(f"Invalid source. Allowed: {allowed}")

    def get_counter_source(self):
        """
        Query the source for the measurement counter.
        
        Parameter:
        None
        
        Return:
        str: Current source
        """
        return self.instrument.query(":MEAS:COUN:SOUR?")

    def get_counter_value(self):
        """
        Query the value of the measurement counter.
        
        Parameter:
        None
        
        Return:
        int: Counter value
        """
        resp = self.instrument.query(":MEAS:COUN:VAL?")
        try:
            return int(resp)
        except Exception:
            return resp
class Reference:
    """
    The Reference commands are used to set the reference waveform parameters.
    """
    def __init__(self, instrument,data_handler):
        self.instrument = instrument
        self.data_handler = data_handler

    def set_display(self, state):
        """
        Enable or disable the REF function.
        
        Parameter:
        state (int or str): 1/0 or "ON"/"OFF"
        
        Return:
        None
        """
        if state in [1, 0]:
            val = state
        elif isinstance(state, str) and state.upper() in {"ON", "OFF"}:
            val = 1 if state.upper() == "ON" else 0
        else:
            print("Invalid state. Use 1, 0, 'ON', or 'OFF'.")
            return
        self.instrument.write(f":REF:DISP {val}")

    def get_display(self):
        """
        Query the status of the REF function.
        
        Parameter:
        None
        
        Return:
        int: 1 (enabled) or 0 (disabled)
        """
        resp = self.instrument.query(":REF:DISP?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_enable(self, n, state):
        """
        Enable or disable the specified reference channel.
        
        Parameter:
        n (int): Reference channel number (1-10)
        state (int or str): 1/0 or "ON"/"OFF"
       
        Return:
        None
        """
        if n not in range(1, 11):
            print("Invalid reference channel. Use 1-10.")
            return
        if state in [1, 0]:
            val = state
        elif isinstance(state, str) and state.upper() in {"ON", "OFF"}:
            val = 1 if state.upper() == "ON" else 0
        else:
            print("Invalid state. Use 1, 0, 'ON', or 'OFF'.")
            return
        self.instrument.write(f":REF{n}:ENAB {val}")

    def get_enable(self, n):
        """
        Query the status of the specified reference channel.
        
        Parameter:
        n (int): Reference channel number (1-10)
        
        Return:
        int: 1 (enabled) or 0 (disabled)
        """
        if n not in range(1, 11):
            print("Invalid reference channel. Use 1-10.")
            return None
        resp = self.instrument.query(f":REF{n}:ENAB?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_source(self, n, source):
        """
        Set the source of the current reference channel.
        
        Parameter:
        n (int): Reference channel number (1-10)
        source (str): "CHANNEL1", "CHANNEL2", or "MATH"
        
        Return:
        None
        """
        allowed = {"CHANNEL1", "CHANNEL2", "MATH", "CHAN1", "CHAN2"}
        if n not in range(1, 11):
            print("Invalid reference channel. Use 1-10.")
            return
        src_up = source.upper()
        if src_up in allowed:
            val = "CHANnel1" if src_up in {"CHANNEL1", "CHAN1"} else ("CHANnel2" if src_up in {"CHANNEL2", "CHAN2"} else "MATH")
            self.instrument.write(f":REF{n}:SOUR {val}")
        else:
            print("Invalid source. Allowed: CHANNEL1, CHANNEL2, MATH.")

    def get_source(self, n):
        """
        Query the source of the current reference channel.
        
        Parameter:
        n (int): Reference channel number (1-10)
        
        Return:
        str: "CHAN1", "CHAN2", or "MATH"
        """
        if n not in range(1, 11):
            print("Invalid reference channel. Use 1-10.")
            return None
        return self.instrument.query(f":REF{n}:SOUR?")

    def set_vscale(self, n, scale):
        """
        Set the vertical scale of the specified reference channel.
        
        Parameter:
        n (int): Reference channel number (1-10)
        scale (float): Vertical scale value
        
        Return:
        None
        """
        if n not in range(1, 11):
            print("Invalid reference channel. Use 1-10.")
            return
        self.instrument.write(f":REF{n}:VSCale {scale}")

    def get_vscale(self, n):
        """
        Query the vertical scale of the specified reference channel.
        
        Parameter:
        n (int): Reference channel number (1-10)
        
        Return:
        float: Vertical scale value
        """
        if n not in range(1, 11):
            print("Invalid reference channel. Use 1-10.")
            return None
        resp = self.instrument.query(f":REF{n}:VSCale?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_voffset(self, n, offset):
        """
        Set the vertical offset of the specified reference channel.
        
        Parameter:
        n (int): Reference channel number (1-10)
        offset (float): Vertical offset value
        
        Return:
        None
        """
        if n not in range(1, 11):
            print("Invalid reference channel. Use 1-10.")
            return
        self.instrument.write(f":REF{n}:VOFFset {offset}")

    def get_voffset(self, n):
        """
        Query the vertical offset of the specified reference channel.
        
        Parameter:
        n (int): Reference channel number (1-10)
        
        Return:
        float: Vertical offset value
        """
        if n not in range(1, 11):
            print("Invalid reference channel. Use 1-10.")
            return None
        resp = self.instrument.query(f":REF{n}:VOFFset?")
        try:
            return float(resp)
        except Exception:
            return resp

    def reset(self, n):
        """
        Reset the vertical scale and vertical offset of the specified reference channel to default.
        
        Parameter:
        n (int): Reference channel number (1-10)
        
        Return:
        None
        """
        if n not in range(1, 11):
            print("Invalid reference channel. Use 1-10.")
            return
        self.instrument.write(f":REF{n}:RESet")

    def set_current(self, n):
        """
        Select the current reference channel.
        
        Parameter:
        n (int): Reference channel number (1-10)
        
        Return:
        None
        """
        if n not in range(1, 11):
            print("Invalid reference channel. Use 1-10.")
            return
        self.instrument.write(f":REF{n}:CURR")

    def save(self, n):
        """
        Store the waveform of the current reference channel to internal memory.
        
        Parameter:
        n (int): Reference channel number (1-10)
        
        Return:
        None
        """
        if n not in range(1, 11):
            print("Invalid reference channel. Use 1-10.")
            return
        self.instrument.write(f":REF{n}:SAVE")

    def set_color(self, n, color):
        """
        Set the display color of the current reference channel.
        
        Parameter:
        n (int): Reference channel number (1-10)
        color (str): "GRAY", "GREEN", "LBLUE", "MAGENTA", "ORANGE"
        
        Return: 
        None
        """
        allowed = {"GRAY", "GREEN", "LBLUE", "MAGENTA", "ORANGE"}
        if n not in range(1, 11):
            print("Invalid reference channel. Use 1-10.")
            return
        color_up = color.upper()
        if color_up in allowed:
            val = color_up
            self.instrument.write(f":REF{n}:COLor {val}")
        else:
            print("Invalid color. Allowed: GRAY, GREEN, LBLUE, MAGENTA, ORANGE.")

    def get_color(self, n):
        """
        Query the display color of the current reference channel.
        
        Parameter:
        n (int): Reference channel number (1-10)
        
        Return:
        str: Color name
        """
        if n not in range(1, 11):
            print("Invalid reference channel. Use 1-10.")
            return None
        return self.instrument.query(f":REF{n}:COLor?")
class Storage:
    """
    The Storage commands are used to set the related parameters when storing images.
    """
    def __init__(self, instrument,data_handler):
        self.instrument = instrument
        self.data_handler = data_handler

    def set_image_type(self, img_type):
        """
        Set the image type when storing images.
        
        Parameter:
        img_type (str): "PNG", "BMP8", "BMP24", "JPEG", "TIFF"
        
        Return:
        None
        """
        allowed = {"PNG", "BMP8", "BMP24", "JPEG", "TIFF"}
        t = img_type.upper()
        if t in allowed:
            self.instrument.write(f":STOR:IMAG:TYPE {t}")
        else:
            print("Invalid image type. Allowed: PNG, BMP8, BMP24, JPEG, TIFF.")

    def get_image_type(self):
        """
        Query the image type when storing images.
        
        Parameter:
        None
        
        Return:
        str: Image type
        """
        return self.instrument.query(":STOR:IMAG:TYPE?")

    def set_image_invert(self, state):
        """
        Turn on or off the invert function when storing images.
        
        Parameter:
        state (int or str): 1/0 or "ON"/"OFF"
        
        Return:
        None
        """
        if state in [1, 0]:
            val = state
        elif isinstance(state, str) and state.upper() in {"ON", "OFF"}:
            val = 1 if state.upper() == "ON" else 0
        else:
            print("Invalid state. Use 1, 0, 'ON', or 'OFF'.")
            return
        self.instrument.write(f":STOR:IMAG:INVERT {val}")

    def get_image_invert(self):
        """
        Query the status of the invert function when storing images.
        
        Parameter:
        None
        
        Return:
        str: "ON" or "OFF"
        """
        return self.instrument.query(":STOR:IMAG:INVERT?")

    def set_image_color(self, state):
        """
        Set the image color when storing images to color (ON) or intensity graded color (OFF).
        
        Parameter:
        state (int or str): 1/0 or "ON"/"OFF"
        
        Return:
        None
        """
        if state in [1, 0]:
            val = "ON" if state == 1 else "OFF"
        elif isinstance(state, str) and state.upper() in {"ON", "OFF"}:
            val = state.upper()
        else:
            print("Invalid state. Use 1, 0, 'ON', or 'OFF'.")
            return
        self.instrument.write(f":STOR:IMAG:COLor {val}")

    def get_image_color(self):
        """
        Query the image color when storing images.
        
        Parameter:
        None
        
        Return:
        str: "ON" or "OFF"
        """
        return self.instrument.query(":STOR:IMAG:COLor?")

class System:
    """
    The System commands are used to set system-related parameters.
    """
    def __init__(self, instrument,data_handler):
        self.instrument = instrument
        self.data_handler = data_handler

    def set_autoscale(self, state):
        """
        Enable or disable the AUTO key on the front panel.
        
        Parameter:
        state (int or str): 1/0 or "ON"/"OFF"
        
        Return:
        None
        """
        if state in [1, 0]:
            val = 1 if state == 1 else 0
        elif isinstance(state, str) and state.upper() in {"ON", "OFF"}:
            val = 1 if state.upper() == "ON" else 0
        else:
            print("Invalid state. Use 1, 0, 'ON', or 'OFF'.")
            return
        self.instrument.write(f":SYST:AUToscale {val}")

    def get_autoscale(self):
        """
        Query the status of the AUTO key on the front panel.
        
        Parameter:
        None
        
        Return:
        int: 1 (enabled) or 0 (disabled)
        """
        resp = self.instrument.query(":SYST:AUToscale?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_beeper(self, state):
        """
        Enable or disable the beeper.
        
        Parameter:
        state (int or str): 1/0 or "ON"/"OFF"
        
        Return:
        None
        """
        if state in [1, 0]:
            val = 1 if state == 1 else 0
        elif isinstance(state, str) and state.upper() in {"ON", "OFF"}:
            val = 1 if state.upper() == "ON" else 0
        else:
            print("Invalid state. Use 1, 0, 'ON', or 'OFF'.")
            return
        self.instrument.write(f":SYST:BEEPer {val}")

    def get_beeper(self):
        """
        Query the status of the beeper.
        
        Parameter:
        None
        
        Return:
        int: 1 (enabled) or 0 (disabled)
        """
        resp = self.instrument.query(":SYST:BEEPer?")
        try:
            return int(resp)
        except Exception:
            return resp

    def get_error(self):
        """
        Query and delete the last system error message.
       
        Parameter:
        None
        
        Return:
        str: Error message in "<number>,<content>" format
        """
        return self.instrument.query(":SYST:ERRor?")

    def get_grid_count(self):
        """
        Query the number of grids in the horizontal direction of the instrument screen.
        
        Parameter:
        None
        
        Return:
        int: Always returns 12
        """
        resp = self.instrument.query(":SYST:GAM?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_language(self, lang):
        """
        Set the system language.
        
        Parameter:
        lang (str): "SCHINESE", "TCHINESE", "ENGLISH", "PORTUGUESE", "GERMAN", "POLISH", "KOREAN", "JAPANESE", "FRENCH", "RUSSIAN"
        
        Return:
        None
        """
        allowed = {"SCHINESE", "TCHINESE", "ENGLISH", "PORTUGUESE", "GERMAN", "POLISH", "KOREAN", "JAPANESE", "FRENCH", "RUSSIAN"}
        l = lang.upper()
        if l in allowed:
            self.instrument.write(f":SYST:LANG {l}")
        else:
            print("Invalid language. Allowed: " + ", ".join(allowed))

    def get_language(self):
        """
        Query the system language.
        
        Parameter:
        None
        
        Return:
        str: Language code
        """
        return self.instrument.query(":SYST:LANG?")

    def set_locked(self, state):
        """
        Enable or disable the keyboard lock function.
        Parameter:
            state (int or str): 1/0 or "ON"/"OFF"
        Return:
            None
        """
        if state in [1, 0]:
            val = 1 if state == 1 else 0
        elif isinstance(state, str) and state.upper() in {"ON", "OFF"}:
            val = 1 if state.upper() == "ON" else 0
        else:
            print("Invalid state. Use 1, 0, 'ON', or 'OFF'.")
            return
        self.instrument.write(f":SYST:LOCKed {val}")

    def get_locked(self):
        """
        Query the status of the keyboard lock function.
        
        Parameter:
        None
        
        Return:
        int: 1 (locked) or 0 (unlocked)
        """
        resp = self.instrument.query(":SYST:LOCKed?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_pon(self, pon):
        """
        Set the system configuration to be recalled at power-on.
        
        Parameter:
        pon (str): "LATEST" or "DEFAULT"
        
        Return:
        None
        """
        allowed = {"LATEST", "DEFAULT", "LAT", "DEF"}
        p = pon.upper()
        if p in allowed:
            self.instrument.write(f":SYST:PON {p}")
        else:
            print("Invalid PON value. Allowed: LATEST, DEFAULT.")

    def get_pon(self):
        """
        Query the system configuration to be recalled at power-on.
        
        Parameter:
        None

        Return:
        str: "LAT" or "DEF"
        """
        return self.instrument.query(":SYST:PON?")

    def install_option(self, license_code):
        """
        Install an option license.

        Parameter:
        license_code (str): 28-byte license string (uppercase letters and numbers)
        
        Return:
        None
        """
        if isinstance(license_code, str) and len(license_code) == 28 and license_code.isalnum() and license_code.isupper():
            self.instrument.write(f":SYST:OPT:INST {license_code}")
        else:
            print("Invalid license code. Must be 28 uppercase letters/numbers.")

    def uninstall_option(self):
        """
        Uninstall all installed options.

        Parameter:
        None

        Return:
        None
        """
        self.instrument.write(":SYST:OPT:UNINST")

    def get_ram(self):
        """
        Query the number of analog channels of the instrument.
        
        Parameter:
        None

        Return:
        int: Always returns 2
        """
        resp = self.instrument.query(":SYST:RAM?")
        try:
            return int(resp)
        except Exception:
            return resp

    def get_setup(self):
        """
        Query the setting of the oscilloscope (returns binary data with TMC header). If autosave is on, then also saves them to a bin file.
        
        Parameter:
        None

        Return:
        bytes: Setup data
        """
        data = self.instrument.query_binary_values(":SYST:SETup?", datatype='B', container=bytes)
        """if data and data[0] == ord('#'):  # Check for TMC header
            data = self.data_handler.remove_tmc_header(data)"""
        if self.data_handler.auto_save:
            self.data_handler.write_to_file("System_Setup", data, EFileType.BIN) 
        return data

    def set_setup(self, setup_stream):
        """
        Import the setting parameters of the oscilloscope.

        Parameter:
        setup_stream (bytes): Setup data (must be from get_setup)

        Return:
        None
        """
        self.instrument.write(":SYST:SETup", setup_stream)

class Timebase:
    """
    The Timebase commands are used to set the horizontal parameters.
    """
    def __init__(self, instrument,data_handler):
        self.instrument = instrument
        self.data_handler = data_handler

    def set_delay_enable(self, state):
        """
        Enable or disable the delayed sweep.

        Parameter:
        state (int or str): 1/0 or "ON"/"OFF"

        Return:
        None
        """
        if state in [1, 0]:
            val = 1 if state == 1 else 0
        elif isinstance(state, str) and state.upper() in {"ON", "OFF"}:
            val = 1 if state.upper() == "ON" else 0
        else:
            print("Invalid state. Use 1, 0, 'ON', or 'OFF'.")
            return
        self.instrument.write(f":TIM:DEL:ENAB {val}")

    def get_delay_enable(self):
        """
        Query the status of the delayed sweep.

        Parameter:
        None

        Return:
        int: 1 (enabled) or 0 (disabled)
        """
        resp = self.instrument.query(":TIM:DEL:ENAB?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_delay_offset(self, offset):
        """
        Set the delayed timebase offset (in seconds).

        Parameter:
        offset (float): Offset value in seconds

        Return:
        None
        """
        self.instrument.write(f":TIM:DEL:OFFS {offset}")

    def get_delay_offset(self):
        """
        Query the delayed timebase offset (in seconds).

        Parameter:
        None

        Return:
        float: Offset value in seconds
        """
        resp = self.instrument.query(":TIM:DEL:OFFS?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_delay_scale(self, scale):
        """
        Set the delayed timebase scale (in s/div).

        Parameter:
        scale (float): Scale value in seconds/div

        Return:
        None
        """
        self.instrument.write(f":TIM:DEL:SCAL {scale}")

    def get_delay_scale(self):
        """
        Query the delayed timebase scale (in s/div).

        Parameter:
        None

        Return:
        float: Scale value in seconds/div
        """
        resp = self.instrument.query(":TIM:DEL:SCAL?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_main_offset(self, offset):
        """
        Set the main timebase offset (in seconds).

        Parameter:
        offset (float): Offset value in seconds

        Return:
        None
        """
        self.instrument.write(f":TIM:MAIN:OFFS {offset}")

    def get_main_offset(self):
        """
        Query the main timebase offset (in seconds).

        Parameter:  
        None

        Return:
        float: Offset value in seconds
        """
        resp = self.instrument.query(":TIM:MAIN:OFFS?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_main_scale(self, scale):
        """
        Set the main timebase scale (in s/div).

        Parameter:
        scale (float): Scale value in seconds/div

        Return:
        None
        """
        self.instrument.write(f":TIM:MAIN:SCAL {scale}")

    def get_main_scale(self):
        """
        Query the main timebase scale (in s/div).

        Parameter:
        None

        Return:
        float: Scale value in seconds/div
        """
        resp = self.instrument.query(":TIM:MAIN:SCAL?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_mode(self, mode):
        """
        Set the mode of the horizontal timebase.

        Parameter:
        mode (str): "MAIN", "XY", or "ROLL"

        Return:
        None
        """
        allowed = {"MAIN", "XY", "ROLL"}
        m = mode.upper()
        if m in allowed:
            self.instrument.write(f":TIM:MODE {m}")
        else:
            print("Invalid mode. Allowed: MAIN, XY, ROLL.")

    def get_mode(self):
        """
        Query the mode of the horizontal timebase.

        Parameter:
        None

        Return:
        str: "MAIN", "XY", or "ROLL"
        """
        return self.instrument.query(":TIM:MODE?")
class Trigger:
    """
    The Trigger commands are used to set the trigger system of the oscilloscope.
    """
    def __init__(self, instrument,data_handler):
        self.instrument = instrument
        self.data_handler = data_handler
        self.rs232 = RS232(instrument, data_handler)
        self.iic = IIC_Trigger(instrument, data_handler)
        self.spi = SPI_Trigger(instrument, data_handler)

    def set_mode(self, mode):
        """
        Set the trigger type.

        Parameter:
        mode (str): One of {"EDGE", "PULSE", "RUNT", "WIND", "NEDG", "SLOPE", "VIDEO", "PATTERN", "DELAY", "TIMEOUT", "DURATION", "SHOLD", "RS232", "IIC", "SPI"}
        
        Return:
        None
        """
        allowed = {"EDGE", "PULSE", "RUNT", "WIND", "NEDG", "SLOPE", "VIDEO", "PATTERN", "DELAY", "TIMEOUT", "DURATION", "SHOLD", "RS232", "IIC", "SPI"}
        m = mode.upper()
        if m in allowed:
            self.instrument.write(f":TRIG:MODE {m}")
        else:
            print(f"Invalid mode. Allowed: {allowed}")

    def get_mode(self):
        """
        Query the trigger type.

        Parameter:
        None

        Return:
        str: Trigger mode
        """
        return self.instrument.query(":TRIG:MODE?")

    def set_coupling(self, coupling):
        """
        Set the trigger coupling type.

        Parameter:
        coupling (str): One of {"AC", "DC", "LFREJECT", "HFREJECT"}
        
        Return:
        None
        """
        allowed = {"AC", "DC", "LFREJECT", "HFREJECT"}
        c = coupling.upper()
        if c in allowed:
            self.instrument.write(f":TRIG:COUP {c}")
        else:
            print(f"Invalid coupling. Allowed: {allowed}")

    def get_coupling(self):
        """
        Query the trigger coupling type.
        
        Parameter:
        None
        
        Return:
        str: Coupling type
        """
        return self.instrument.query(":TRIG:COUP?")

    def get_status(self):
        """
        Query the current trigger status.
        
        Parameter:
        None
        
        Return:
        str: One of "TD", "WAIT", "RUN", "AUTO", "STOP"
        """
        return self.instrument.query(":TRIG:STAT?")

    def set_sweep(self, sweep):
        """
        Set the trigger mode (sweep).
        
        Parameter:
        sweep (str): One of {"AUTO", "NORMAL", "SINGLE"}
        
        Return:
        None
        """
        allowed = {"AUTO", "NORMAL", "SINGLE"}
        s = sweep.upper()
        if s in allowed:
            self.instrument.write(f":TRIG:SWEE {s}")
        else:
            print(f"Invalid sweep. Allowed: {allowed}")

    def get_sweep(self):
        """
        Query the trigger mode (sweep).
        
        Parameter:
        None

        Return:
        str: "AUTO", "NORM", or "SING"
        """
        return self.instrument.query(":TRIG:SWEE?")

    def set_holdoff(self, value):
        """
        Set the trigger holdoff time (in seconds).

        Parameter:
        value (float): Holdoff time, 16e-9 to 10

        Return:
        None
        """
        if isinstance(value, (float, int)) and 16e-9 <= value <= 10:
            self.instrument.write(f":TRIG:HOLD {value}")
        else:
            print("Invalid holdoff value. Must be between 16ns and 10s.")

    def get_holdoff(self):
        """
        Query the trigger holdoff time (in seconds).

        Parameter:
        None

        Return:
        float: Holdoff time
        """
        resp = self.instrument.query(":TRIG:HOLD?")
        try:
            return float(resp)
        except Exception:
            return resp

    def enable_noise_rejection(self, state):
        """
        Enable or disable noise rejection for trigger.

        Parameter:
        state (int or str): 1/0 or "ON"/"OFF"

        Return:
        None
        """
        if state in [1, 0]:
            val = state
        elif isinstance(state, str) and state.upper() in {"ON", "OFF"}:
            val = 1 if state.upper() == "ON" else 0
        else:
            print("Invalid state. Use 1, 0, 'ON', or 'OFF'.")
            return
        self.instrument.write(f":TRIG:NREJ {val}")

    def is_noise_rejection_enabled(self):
        """
        Query the status of noise rejection for trigger.

        Parameter:
        None

        Return:
        int: 1 (enabled) or 0 (disabled)
        """
        resp = self.instrument.query(":TRIG:NREJ?")
        try:
            return int(resp)
        except Exception:
            return resp

    def get_position(self):
        """
        Query the position in the internal memory that corresponds to the waveform trigger position.
        
        Parameter:
        None

        Return:
        int: -2 (not triggered), -1 (triggered outside memory), or >0 (position)
        """
        resp = self.instrument.query(":TRIG:POS?")
        try:
            return int(resp)
        except Exception:
            return resp

    # EDGE Subtree
    def set_edge_source(self, source):
        """
        Set the trigger source in edge trigger.

        Parameter:
        source (str): "CHANNEL1", "CHANNEL2", "AC", "EXT"

        Return:
        None
        """
        allowed = {"CHANNEL1", "CHANNEL2", "AC", "EXT", "CHAN1", "CHAN2"}
        s = source.upper()
        if s in allowed:
            val = "CHANnel1" if s in {"CHANNEL1", "CHAN1"} else ("CHANnel2" if s in {"CHANNEL2", "CHAN2"} else s)
            self.instrument.write(f":TRIG:EDGE:SOUR {val}")
        else:
            print("Invalid source. Allowed: CHANNEL1, CHANNEL2, AC, EXT.")

    def get_edge_source(self):
        """
        Query the trigger source in edge trigger.

        Parameter:
        None

        Return:
        str: "CHAN1", "CHAN2", "AC", or "EXT"
        """
        return self.instrument.query(":TRIG:EDGE:SOUR?")

    def set_edge_slope(self, slope):
        """
        Set the edge type in edge trigger.

        Parameter:
        slope (str): "POSITIVE", "NEGATIVE", "RFALL"

        Return:
        None
        """
        allowed = {"POSITIVE", "NEGATIVE", "RFALL", "POS", "NEG"}
        s = slope.upper()
        if s in allowed:
            val = "POS" if s.startswith("POS") else ("NEG" if s.startswith("NEG") else "RFAL")
            self.instrument.write(f":TRIG:EDGE:SLOP {val}")
        else:
            print("Invalid slope. Allowed: POSITIVE, NEGATIVE, RFALL.")

    def get_edge_slope(self):
        """
        Query the edge type in edge trigger.

        Parameter:
        None

        Return:
        str: "POS", "NEG", or "RFAL"
        """
        return self.instrument.query(":TRIG:EDGE:SLOP?")

    def set_edge_level(self, level):
        """
        Set the trigger level in edge trigger.

        Parameter:
        level (float): Level value

        Return:
        None
        """
        self.instrument.write(f":TRIG:EDGE:LEV {level}")

    def get_edge_level(self):
        """
        Query the trigger level in edge trigger.

        Parameter:
        None
        
        Return:
        float: Level value
        """
        resp = self.instrument.query(":TRIG:EDGE:LEV?")
        try:
            return float(resp)
        except Exception:
            return resp
    # PULSE Subtree
    def set_pulse_source(self, source):
        """
        Set the trigger source in pulse width trigger.

        Parameter:
        source (str): "CHANNEL1" or "CHANNEL2"

        Return:
        None
        """
        allowed = {"CHANNEL1", "CHANNEL2", "CHAN1", "CHAN2"}
        s = source.upper()
        if s in allowed:
            val = "CHANnel1" if s in {"CHANNEL1", "CHAN1"} else "CHANnel2"
            self.instrument.write(f":TRIG:PULS:SOUR {val}")
        else:
            print("Invalid source. Allowed: CHANNEL1, CHANNEL2.")

    def get_pulse_source(self):
        """
        Query the trigger source in pulse width trigger.

        Parameter:
        None

        Return:
        str: "CHAN1" or "CHAN2"
        """
        return self.instrument.query(":TRIG:PULS:SOUR?")

    def set_pulse_when(self, when):
        """
        Set the trigger condition in pulse width trigger.

        Parameter:
        when (str): "PGREATER", "PLESS", "NGREATER", "NLESS", "PGLESS", "NGLess"

        Return:
        None
        """
        allowed = {"PGREATER", "PLESS", "NGREATER", "NLESS", "PGLESS", "NGLess"}
        w = when.upper()
        if w in allowed:
            self.instrument.write(f":TRIG:PULS:WHEN {w}")
        else:
            print("Invalid when. Allowed: PGREATER, PLESS, NGREATER, NLESS, PGLESS, NGLess.")

    def get_pulse_when(self):
        """
        Query the trigger condition in pulse width trigger.

        Parameter:
        None

        Return:
        str: Condition code
        """
        return self.instrument.query(":TRIG:PULS:WHEN?")

    def set_pulse_width(self, width):
        """
        Set the pulse width in pulse width trigger (seconds).

        Parameter:
        width (float): 8e-9 to 10

        Return:
        None
        """
        if isinstance(width, (float, int)) and 8e-9 <= width <= 10:
            self.instrument.write(f":TRIG:PULS:WIDT {width}")
        else:
            print("Invalid width. Must be between 8ns and 10s.")

    def get_pulse_width(self):
        """
        Query the pulse width in pulse width trigger (seconds).

        Parameter:
        None

        Return:
        float: Pulse width
        """
        resp = self.instrument.query(":TRIG:PULS:WIDT?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_pulse_uwidth(self, width):
        """
        Set the upper pulse width in pulse width trigger (seconds).

        Parameter:
        width (float): 16e-9 to 10

        Return:
        None
        """
        if isinstance(width, (float, int)) and 16e-9 <= width <= 10:
            self.instrument.write(f":TRIG:PULS:UWID {width}")
        else:
            print("Invalid upper width. Must be between 16ns and 10s.")

    def get_pulse_uwidth(self):
        """
        Query the upper pulse width in pulse width trigger (seconds).

        Parameter:
        None

        Return:
        float: Upper pulse width
        """
        resp = self.instrument.query(":TRIG:PULS:UWID?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_pulse_lwidth(self, width):
        """
        Set the lower pulse width in pulse width trigger (seconds).

        Parameter:
        width (float): 8e-9 to 9.99

        Return:
        None
        """
        if isinstance(width, (float, int)) and 8e-9 <= width <= 9.99:
            self.instrument.write(f":TRIG:PULS:LWID {width}")
        else:
            print("Invalid lower width. Must be between 8ns and 9.99s.")

    def get_pulse_lwidth(self):
        """
        Query the lower pulse width in pulse width trigger (seconds).

        Parameter:
        None

        Return:
        float: Lower pulse width
        """
        resp = self.instrument.query(":TRIG:PULS:LWID?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_pulse_level(self, level):
        """
        Set the trigger level in pulse width trigger.

        Parameter:
        level (float): Level value

        Return:
        None
        """
        self.instrument.write(f":TRIG:PULS:LEV {level}")

    def get_pulse_level(self):
        """
        Query the trigger level in pulse width trigger.

        Parameter:
        None

        Return:
        float: Level value
        """
        resp = self.instrument.query(":TRIG:PULS:LEV?")
        try:
            return float(resp)
        except Exception:
            return resp

        # SLOPE Subtree
    def set_slope_source(self, source):
        """
        Set the trigger source in slope trigger.

        Parameter:
        source (str): "CHANNEL1" or "CHANNEL2"

        Return:
        None
        """
        allowed = {"CHANNEL1", "CHANNEL2", "CHAN1", "CHAN2"}
        s = source.upper()
        if s in allowed:
            val = "CHANnel1" if s in {"CHANNEL1", "CHAN1"} else "CHANnel2"
            self.instrument.write(f":TRIG:SLOP:SOUR {val}")
        else:
            print("Invalid source. Allowed: CHANNEL1, CHANNEL2.")

    def get_slope_source(self):
        """
        Query the trigger source in slope trigger.

        Parameter:
        None

        Return:
        str: "CHAN1" or "CHAN2"
        """
        return self.instrument.query(":TRIG:SLOP:SOUR?")

    def set_slope_when(self, when):
        """
        Set the trigger condition in slope trigger.

        Parameter:
        when (str): "PGREATER", "PLESS", "NGREATER", "NLESS", "PGLESS", "NGLess"

        Return:
        None
        """
        allowed = {"PGREATER", "PLESS", "NGREATER", "NLESS", "PGLESS", "NGLess"}
        w = when.upper()
        if w in allowed:
            self.instrument.write(f":TRIG:SLOP:WHEN {w}")
        else:
            print("Invalid when. Allowed: PGREATER, PLESS, NGREATER, NLESS, PGLESS, NGLess.")

    def get_slope_when(self):
        """
        Query the trigger condition in slope trigger.

        Parameter:
        None

        Return:
        str: Condition code
        """
        return self.instrument.query(":TRIG:SLOP:WHEN?")

    def set_slope_time(self, time):
        """
        Set the time value in slope trigger (seconds).

        Parameter:
        time (float): 8e-9 to 10

        Return:
        None
        """
        if isinstance(time, (float, int)) and 8e-9 <= time <= 10:
            self.instrument.write(f":TRIG:SLOP:TIME {time}")
        else:
            print("Invalid time. Must be between 8ns and 10s.")

    def get_slope_time(self):
        """
        Query the time value in slope trigger (seconds).

        Parameter:
        None

        Return:
        float: Time value
        """
        resp = self.instrument.query(":TRIG:SLOP:TIME?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_slope_tupper(self, time):
        """
        Set the upper limit of the time in slope trigger (seconds).

        Parameter:
        time (float): 16e-9 to 10

        Return:
        None
        """
        if isinstance(time, (float, int)) and 16e-9 <= time <= 10:
            self.instrument.write(f":TRIG:SLOP:TUPP {time}")
        else:
            print("Invalid upper time. Must be between 16ns and 10s.")

    def get_slope_tupper(self):
        """
        Query the upper limit of the time in slope trigger (seconds).

        Parameter:
        None

        Return:
        float: Upper time value
        """
        resp = self.instrument.query(":TRIG:SLOP:TUPP?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_slope_tlower(self, time):
        """
        Set the lower limit of the time in slope trigger (seconds).

        Parameter:
        time (float): 8e-9 to 9.99

        Return:
        None
        """
        if isinstance(time, (float, int)) and 8e-9 <= time <= 9.99:
            self.instrument.write(f":TRIG:SLOP:TLOW {time}")
        else:
            print("Invalid lower time. Must be between 8ns and 9.99s.")

    def get_slope_tlower(self):
        """
        Query the lower limit of the time in slope trigger (seconds).

        Parameter:
        None

        Return:
        float: Lower time value
        """
        resp = self.instrument.query(":TRIG:SLOP:TLOW?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_slope_window(self, window):
        """
        Set the vertical window type in slope trigger.
        
        Parameter:
        window (str): "TA", "TB", or "TAB"
        
        Return:
        None
        """
        allowed = {"TA", "TB", "TAB"}
        w = window.upper()
        if w in allowed:
            self.instrument.write(f":TRIG:SLOP:WIND {w}")
        else:
            print("Invalid window. Allowed: TA, TB, TAB.")

    def get_slope_window(self):
        """
        Query the vertical window type in slope trigger.
        
        Parameter:
        None
        
        Return:
        str: Window type
        """
        return self.instrument.query(":TRIG:SLOP:WIND?")

    def set_slope_alevel(self, level):
        """
        Set the upper limit of the trigger level in slope trigger.
        
        Parameter:
        level (float): Level value
        
        Return:
        None
        """
        self.instrument.write(f":TRIG:SLOP:ALEV {level}")

    def get_slope_alevel(self):
        """
        Query the upper limit of the trigger level in slope trigger.
        
        Parameter:
        None
        
        Return:
        float: Level value
        """
        resp = self.instrument.query(":TRIG:SLOP:ALEV?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_slope_blevel(self, level):
        """
        Set the lower limit of the trigger level in slope trigger.
        
        Parameter:
        level (float): Level value
        
        Return:
        None
        """
        self.instrument.write(f":TRIG:SLOP:BLEV {level}")

    def get_slope_blevel(self):
        """
        Query the lower limit of the trigger level in slope trigger.
        
        Parameter:
        None
        
        Return:
        float: Level value
        """
        resp = self.instrument.query(":TRIG:SLOP:BLEV?")
        try:
            return float(resp)
        except Exception:
            return resp

    # VIDEO Subtree
    def set_video_source(self, source):
        """
        Set the trigger source in video trigger.
        
        Parameter:
        source (str): "CHANNEL1" or "CHANNEL2"
        
        Return:
        None
        """
        allowed = {"CHANNEL1", "CHANNEL2", "CHAN1", "CHAN2"}
        s = source.upper()
        if s in allowed:
            val = "CHANnel1" if s in {"CHANNEL1", "CHAN1"} else "CHANnel2"
            self.instrument.write(f":TRIG:VID:SOUR {val}")
        else:
            print("Invalid source. Allowed: CHANNEL1, CHANNEL2.")

    def get_video_source(self):
        """
        Query the trigger source in video trigger.
        
        Parameter:
        None
        
        Return:
        str: "CHAN1" or "CHAN2"
        """
        return self.instrument.query(":TRIG:VID:SOUR?")

    def set_video_polarity(self, polarity):
        """
        Set the video polarity in video trigger.
        
        Parameter:
        polarity (str): "POSITIVE" or "NEGATIVE"
        
        Return:
        None
        """
        allowed = {"POSITIVE", "NEGATIVE", "POS", "NEG"}
        p = polarity.upper()
        if p in allowed:
            val = "POS" if p.startswith("POS") else "NEG"
            self.instrument.write(f":TRIG:VID:POL {val}")
        else:
            print("Invalid polarity. Allowed: POSITIVE, NEGATIVE.")

    def get_video_polarity(self):
        """
        Query the video polarity in video trigger.
        
        Parameter:
        None
        
        Return:
        str: "POS" or "NEG"
        """
        return self.instrument.query(":TRIG:VID:POL?")

    def set_video_mode(self, mode):
        """
        Set the sync type in video trigger.
        
        Parameter:
        mode (str): "ODDFIELD", "EVENFIELD", "LINE", or "ALINES"
        
        Return:
        None
        """
        allowed = {"ODDFIELD", "EVENFIELD", "LINE", "ALINES", "ODDF", "EVEN", "ALIN"}
        m = mode.upper()
        if m in allowed:
            val = "ODDF" if m.startswith("ODD") else ("EVEN" if m.startswith("EVEN") else ("LINE" if m.startswith("LINE") else "ALIN"))
            self.instrument.write(f":TRIG:VID:MODE {val}")
        else:
            print("Invalid mode. Allowed: ODDFIELD, EVENFIELD, LINE, ALINES.")

    def get_video_mode(self):
        """
        Query the sync type in video trigger.
        
        Parameter:
        None
        
        Return:
        str: "ODDF", "EVEN", "LINE", or "ALIN"
        """
        return self.instrument.query(":TRIG:VID:MODE?")

    def set_video_line(self, line):
        """
        Set the line number when the sync type in video trigger is LINE.
        
        Parameter:
        line (int): Line number (see documentation for valid range)
        
        Return:
        None
        """
        if isinstance(line, int) and line >= 1:
            self.instrument.write(f":TRIG:VID:LINE {line}")
        else:
            print("Invalid line number. Must be integer >= 1.")

    def get_video_line(self):
        """
        Query the line number when the sync type in video trigger is LINE.
        
        Parameter:
        None
        
        Return:
        int: Line number
        """
        resp = self.instrument.query(":TRIG:VID:LINE?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_video_standard(self, standard):
        """
        Set the video standard in video trigger.
        
        Parameter:
        standard (str): "PALSECAM", "NTSC", "480P", or "576P"
        
        Return:
        None
        """
        allowed = {"PALSECAM", "NTSC", "480P", "576P"}
        s = standard.upper()
        if s in allowed:
            self.instrument.write(f":TRIG:VID:STAN {s}")
        else:
            print("Invalid standard. Allowed: PALSECAM, NTSC, 480P, 576P.")

    def get_video_standard(self):
        """
        Query the video standard in video trigger.
        
        Parameter:
        None
        
        Return:
        str: "PALS", "NTSC", "480P", or "576P"
        """
        return self.instrument.query(":TRIG:VID:STAN?")

    def set_video_level(self, level):
        """
        Set the trigger level in video trigger.
        
        Parameter:
        level (float): Level value
        
        Return:
        None
        """
        self.instrument.write(f":TRIG:VID:LEV {level}")

    def get_video_level(self):
        """
        Query the trigger level in video trigger.
        
        Parameter:
        None
        
        Return:
        float: Level value
        """
        resp = self.instrument.query(":TRIG:VID:LEV?")
        try:
            return float(resp)
        except Exception:
            return resp

    # PATTERN Subtree
    def set_pattern_source(self, source):
        """
        Set the trigger source in pattern trigger.
        
        Parameter:
        source (str): "CHANNEL1" or "CHANNEL2"
        
        Return:
        None
        """
        allowed = {"CHANNEL1", "CHANNEL2", "CHAN1", "CHAN2"}
        s = source.upper()
        if s in allowed:
            val = "CHANnel1" if s in {"CHANNEL1", "CHAN1"} else "CHANnel2"
            self.instrument.write(f":TRIG:PATT:SOUR {val}")
        else:
            print("Invalid source. Allowed: CHANNEL1, CHANNEL2.")

    def get_pattern_source(self):
        """
        Query the trigger source in pattern trigger.
        
        Parameter:
        None
        
        Return:
        str: "CHAN1" or "CHAN2"
        """
        return self.instrument.query(":TRIG:PATT:SOUR?")

    def set_pattern_condition(self, cond):
        """
        Set the pattern condition in pattern trigger.
        
        Parameter:
        cond (str): "AND", "OR", "NAND", "NOR"
        
        Return:
        None
        """
        allowed = {"AND", "OR", "NAND", "NOR"}
        c = cond.upper()
        if c in allowed:
            self.instrument.write(f":TRIG:PATT:COND {c}")
        else:
            print("Invalid condition. Allowed: AND, OR, NAND, NOR.")

    def get_pattern_condition(self):
        """
        Query the pattern condition in pattern trigger.
        
        Parameter:
        None
        
        Return:
        str: Condition code
        """
        return self.instrument.query(":TRIG:PATT:COND?")

    def set_pattern_level(self, level):
        """
        Set the trigger level in pattern trigger.
        
        Parameter:
        level (float): Level value
        
        Return:
        None
        """
        self.instrument.write(f":TRIG:PATT:LEV {level}")

    def get_pattern_level(self):
        """
        Query the trigger level in pattern trigger.
        
        Parameter:
        None
        
        Return:
        float: Level value
        """
        resp = self.instrument.query(":TRIG:PATT:LEV?")
        try:
            return float(resp)
        except Exception:
            return resp

    # DURATION Subtree
    def set_duration_source(self, source):
        """
        Set the trigger source in duration trigger.
        
        Parameter:
        source (str): "CHANNEL1" or "CHANNEL2"
        
        Return:
        None
        """
        allowed = {"CHANNEL1", "CHANNEL2", "CHAN1", "CHAN2"}
        s = source.upper()
        if s in allowed:
            val = "CHANnel1" if s in {"CHANNEL1", "CHAN1"} else "CHANnel2"
            self.instrument.write(f":TRIG:DUR:SOUR {val}")
        else:
            print("Invalid source. Allowed: CHANNEL1, CHANNEL2.")

    def get_duration_source(self):
        """
        Query the trigger source in duration trigger.
        
        Parameter:
        None
        
        Return:
        str: "CHAN1" or "CHAN2"
        """
        return self.instrument.query(":TRIG:DUR:SOUR?")

    def set_duration_when(self, when):
        """
        Set the trigger condition in duration trigger.
        
        Parameter:
        when (str): "GREATER", "LESS"
        
        Return:
        None
        """
        allowed = {"GREATER", "LESS"}
        w = when.upper()
        if w in allowed:
            self.instrument.write(f":TRIG:DUR:WHEN {w}")
        else:
            print("Invalid when. Allowed: GREATER, LESS.")

    def get_duration_when(self):
        """
        Query the trigger condition in duration trigger.

        Parameter:
        None

        Return:
        str: Condition code
        """
        return self.instrument.query(":TRIG:DUR:WHEN?")

    def set_duration_time(self, time):
        """
        Set the time value in duration trigger (seconds).

        Parameter:
        time (float): 8e-9 to 10

        Return:
        None
        """
        if isinstance(time, (float, int)) and 8e-9 <= time <= 10:
            self.instrument.write(f":TRIG:DUR:TIME {time}")
        else:
            print("Invalid time. Must be between 8ns and 10s.")

    def get_duration_time(self):
        """
        Query the time value in duration trigger (seconds).

        Parameter:
        None

        Return:
        float: Time value
        """
        resp = self.instrument.query(":TRIG:DUR:TIME?")
        try:
            return float(resp)
        except Exception:
            return resp

    # TIMEOUT Subtree
    def set_timeout_source(self, source):
        """
        Set the trigger source in timeout trigger.

        Parameter:
        source (str): "CHANNEL1" or "CHANNEL2"

        Return:
        None
        """
        allowed = {"CHANNEL1", "CHANNEL2", "CHAN1", "CHAN2"}
        s = source.upper()
        if s in allowed:
            val = "CHANnel1" if s in {"CHANNEL1", "CHAN1"} else "CHANnel2"
            self.instrument.write(f":TRIG:TIME:SOUR {val}")
        else:
            print("Invalid source. Allowed: CHANNEL1, CHANNEL2.")

    def get_timeout_source(self):
        """
        Query the trigger source in timeout trigger.

        Parameter:
        None

        Return:
        str: "CHAN1" or "CHAN2"
        """
        return self.instrument.query(":TRIG:TIME:SOUR?")

    def set_timeout_when(self, when):
        """
        Set the trigger condition in timeout trigger.

        Parameter:
        when (str): "GREATER", "LESS"

        Return:
        None
        """
        allowed = {"GREATER", "LESS"}
        w = when.upper()
        if w in allowed:
            self.instrument.write(f":TRIG:TIME:WHEN {w}")
        else:
            print("Invalid when. Allowed: GREATER, LESS.")

    def get_timeout_when(self):
        """
        Query the trigger condition in timeout trigger.

        Parameter:
        None

        Return:
        str: Condition code
        """
        return self.instrument.query(":TRIG:TIME:WHEN?")

    def set_timeout_time(self, time):
        """
        Set the time value in timeout trigger (seconds).

        Parameter:
        time (float): 8e-9 to 10

        Return:
        None
        """
        if isinstance(time, (float, int)) and 8e-9 <= time <= 10:
            self.instrument.write(f":TRIG:TIME:TIME {time}")
        else:
            print("Invalid time. Must be between 8ns and 10s.")

    def get_timeout_time(self):
        """
        Query the time value in timeout trigger (seconds).

        Parameter:
        None

        Return:
        float: Time value
        """
        resp = self.instrument.query(":TRIG:TIME:TIME?")
        try:
            return float(resp)
        except Exception:
            return resp
    # RUNT Subtree
    def set_runt_source(self, source):
        """
        Set the trigger source in runt trigger.

        Parameter:
        source (str): "CHANNEL1" or "CHANNEL2"

        Return:
        None
        """
        allowed = {"CHANNEL1", "CHANNEL2", "CHAN1", "CHAN2"}
        s = source.upper()
        if s in allowed:
            val = "CHANnel1" if s in {"CHANNEL1", "CHAN1"} else "CHANnel2"
            self.instrument.write(f":TRIG:RUNT:SOUR {val}")
        else:
            print("Invalid source. Allowed: CHANNEL1, CHANNEL2.")

    def get_runt_source(self):
        """
        Query the trigger source in runt trigger.
        
        Parameter:
        None

        Return:
        str: "CHAN1" or "CHAN2"
        """
        return self.instrument.query(":TRIG:RUNT:SOUR?")

    def set_runt_polarity(self, polarity):
        """
        Set the pulse polarity in runt trigger.

        Parameter:
        polarity (str): "POSITIVE" or "NEGATIVE"

        Return:
        None
        """
        allowed = {"POSITIVE", "NEGATIVE", "POS", "NEG"}
        p = polarity.upper()
        if p in allowed:
            val = "POS" if p.startswith("POS") else "NEG"
            self.instrument.write(f":TRIG:RUNT:POL {val}")
        else:
            print("Invalid polarity. Allowed: POSITIVE, NEGATIVE.")

    def get_runt_polarity(self):
        """
        Query the pulse polarity in runt trigger.

        Parameter:
        None

        Return:
        str: "POS" or "NEG"
        """
        return self.instrument.query(":TRIG:RUNT:POL?")

    def set_runt_when(self, when):
        """
        Set the qualifier in runt trigger.

        Parameter:
        when (str): "NONE", "GREATER", "LESS", "GLESS"

        Return:
        None
        """
        allowed = {"NONE", "GREATER", "LESS", "GLESS"}
        w = when.upper()
        if w in allowed:
            val = w if w != "GLESS" else "GLES"
            self.instrument.write(f":TRIG:RUNT:WHEN {val}")
        else:
            print("Invalid when. Allowed: NONE, GREATER, LESS, GLESS.")

    def get_runt_when(self):
        """
        Query the qualifier in runt trigger.

        Parameter:
        None

        Return:
        str: Qualifier code
        """
        return self.instrument.query(":TRIG:RUNT:WHEN?")

    def set_runt_wupper(self, upper):
        """
        Set the pulse width upper limit in runt trigger (seconds).

        Parameter:
        upper (float): Upper limit, 16e-9 to 10

        Return:
        None
        """
        if isinstance(upper, (float, int)) and 16e-9 <= upper <= 10:
            self.instrument.write(f":TRIG:RUNT:WUPP {upper}")
        else:
            print("Invalid upper limit. Must be between 16ns and 10s.")

    def get_runt_wupper(self):
        """
        Query the pulse width upper limit in runt trigger (seconds).

        Parameter:
        None

        Return:
        float: Upper limit
        """
        resp = self.instrument.query(":TRIG:RUNT:WUPP?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_runt_wlower(self, lower):
        """
        Set the pulse width lower limit in runt trigger (seconds).

        Parameter:
        lower (float): Lower limit, 8e-9 to 9.99

        Return:
        None
        """
        if isinstance(lower, (float, int)) and 8e-9 <= lower <= 9.99:
            self.instrument.write(f":TRIG:RUNT:WLOW {lower}")
        else:
            print("Invalid lower limit. Must be between 8ns and 9.99s.")

    def get_runt_wlower(self):
        """
        Query the pulse width lower limit in runt trigger (seconds).

        Parameter:
        None

        Return:
        float: Lower limit
        """
        resp = self.instrument.query(":TRIG:RUNT:WLOW?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_runt_alevel(self, level):
        """
        Set the trigger level upper limit in runt trigger.

        Parameter:
        level (float): Level value

        Return:
        None
        """
        self.instrument.write(f":TRIG:RUNT:ALEV {level}")

    def get_runt_alevel(self):
        """
        Query the trigger level upper limit in runt trigger.

        Parameter:
        None

        Return:
        float: Level value
        """
        resp = self.instrument.query(":TRIG:RUNT:ALEV?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_runt_blevel(self, level):
        """
        Set the trigger level lower limit in runt trigger.

        Parameter:
        level (float): Level value

        Return:
        None
        """
        self.instrument.write(f":TRIG:RUNT:BLEV {level}")

    def get_runt_blevel(self):
        """
        Query the trigger level lower limit in runt trigger.

        Parameter:
        None

        Return:
        float: Level value
        """
        resp = self.instrument.query(":TRIG:RUNT:BLEV?")
        try:
            return float(resp)
        except Exception:
            return resp

    # WINDows Subtree
    def set_windows_source(self, source):
        """
        Set the trigger source in windows trigger.

        Parameter:
        source (str): "CHANNEL1" or "CHANNEL2"

        Return:
        None
        """
        allowed = {"CHANNEL1", "CHANNEL2", "CHAN1", "CHAN2"}
        s = source.upper()
        if s in allowed:
            val = "CHANnel1" if s in {"CHANNEL1", "CHAN1"} else "CHANnel2"
            self.instrument.write(f":TRIG:WIND:SOUR {val}")
        else:
            print("Invalid source. Allowed: CHANNEL1, CHANNEL2.")

    def get_windows_source(self):
        """
        Query the trigger source in windows trigger.

        Parameter:
        None

        Return:
        str: "CHAN1" or "CHAN2"
        """
        return self.instrument.query(":TRIG:WIND:SOUR?")

    def set_windows_slope(self, slope):
        """
        Set the windows type in windows trigger.

        Parameter:
        slope (str): "POSITIVE", "NEGATIVE", "RFALL"

        Return:
        None
        """
        allowed = {"POSITIVE", "NEGATIVE", "RFALL", "POS", "NEG"}
        s = slope.upper()
        if s in allowed:
            val = "POS" if s.startswith("POS") else ("NEG" if s.startswith("NEG") else "RFAL")
            self.instrument.write(f":TRIG:WIND:SLOP {val}")
        else:
            print("Invalid slope. Allowed: POSITIVE, NEGATIVE, RFALL.")

    def get_windows_slope(self):
        """
        Query the windows type in windows trigger.

        Parameter:
        None

        Return:
        str: "POS", "NEG", or "RFAL"
        """
        return self.instrument.query(":TRIG:WIND:SLOP?")

    def set_windows_position(self, pos):
        """
        Set the trigger position in windows trigger.

        Parameter:
        pos (str): "EXIT", "ENTER", "TIME"

        Return:
        None
        """
        allowed = {"EXIT", "ENTER", "TIME", "TIM"}
        p = pos.upper()
        if p in allowed:
            val = "TIM" if p.startswith("TIM") else p
            self.instrument.write(f":TRIG:WIND:POS {val}")
        else:
            print("Invalid position. Allowed: EXIT, ENTER, TIME.")

    def get_windows_position(self):
        """
        Query the trigger position in windows trigger.

        Parameter:
        None

        Return:
        str: "EXIT", "ENTER", or "TIM"
        """
        return self.instrument.query(":TRIG:WIND:POS?")

    def set_windows_time(self, time):
        """
        Set the hold time in windows trigger (seconds).

        Parameter:
        time (float): 8e-9 to 10

        Return:
        None
        """
        if isinstance(time, (float, int)) and 8e-9 <= time <= 10:
            self.instrument.write(f":TRIG:WIND:TIME {time}")
        else:
            print("Invalid time. Must be between 8ns and 10s.")

    def get_windows_time(self):
        """
        Query the hold time in windows trigger (seconds).

        Parameter:
        None

        Return:
        float: Hold time
        """
        resp = self.instrument.query(":TRIG:WIND:TIME?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_windows_alevel(self, level):
        """
        Set the trigger level upper limit in windows trigger.

        Parameter:
        level (float): Level value

        Return:
        None
        """
        self.instrument.write(f":TRIG:WIND:ALEV {level}")

    def get_windows_alevel(self):
        """
        Query the trigger level upper limit in windows trigger.

        Parameter:
        None

        Return:
        float: Level value
        """
        resp = self.instrument.query(":TRIG:WIND:ALEV?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_windows_blevel(self, level):
        """
        Set the trigger level lower limit in windows trigger.

        Parameter:
        level (float): Level value

        Return:
        None
        """
        self.instrument.write(f":TRIG:WIND:BLEV {level}")

    def get_windows_blevel(self):
        """
        Query the trigger level lower limit in windows trigger.
        Parameter:
        None
        Return:
        float: Level value
        """
        resp = self.instrument.query(":TRIG:WIND:BLEV?")
        try:
            return float(resp)
        except Exception:
            return resp

    # DELAY Subtree
    def set_delay_sa(self, source):
        """
        Set the trigger source A in delay trigger.

        Parameter:
        source (str): "CHANNEL1" or "CHANNEL2"

        Return:
        None
        """
        allowed = {"CHANNEL1", "CHANNEL2", "CHAN1", "CHAN2"}
        s = source.upper()
        if s in allowed:
            val = "CHANnel1" if s in {"CHANNEL1", "CHAN1"} else "CHANnel2"
            self.instrument.write(f":TRIG:DEL:SA {val}")
        else:
            print("Invalid source. Allowed: CHANNEL1, CHANNEL2.")

    def get_delay_sa(self):
        """
        Query the trigger source A in delay trigger.

        Parameter:
        None

        Return:
        str: "CHAN1" or "CHAN2"
        """
        return self.instrument.query(":TRIG:DEL:SA?")

    def set_delay_slopa(self, slope):
        """
        Set the edge type of edge A in delay trigger.

        Parameter:
        slope (str): "POSITIVE" or "NEGATIVE"

        Return:
        None
        """
        allowed = {"POSITIVE", "NEGATIVE", "POS", "NEG"}
        s = slope.upper()
        if s in allowed:
            val = "POS" if s.startswith("POS") else "NEG"
            self.instrument.write(f":TRIG:DEL:SLOPA {val}")
        else:
            print("Invalid slope. Allowed: POSITIVE, NEGATIVE.")

    def get_delay_slopa(self):
        """
        Query the edge type of edge A in delay trigger.

        Parameter:
        None

        Return:
        str: "POS" or "NEG"
        """
        return self.instrument.query(":TRIG:DEL:SLOPA?")

    def set_delay_sb(self, source):
        """
        Set the trigger source B in delay trigger.

        Parameter:
        source (str): "CHANNEL1" or "CHANNEL2"

        Return:
        None
        """
        allowed = {"CHANNEL1", "CHANNEL2", "CHAN1", "CHAN2"}
        s = source.upper()
        if s in allowed:
            val = "CHANnel1" if s in {"CHANNEL1", "CHAN1"} else "CHANnel2"
            self.instrument.write(f":TRIG:DEL:SB {val}")
        else:
            print("Invalid source. Allowed: CHANNEL1, CHANNEL2.")

    def get_delay_sb(self):
        """
        Query the trigger source B in delay trigger.

        Parameter:
        None

        Return:
        str: "CHAN1" or "CHAN2"
        """
        return self.instrument.query(":TRIG:DEL:SB?")

    def set_delay_slopb(self, slope):
        """
        Set the edge type of edge B in delay trigger.

        Parameter:
        slope (str): "POSITIVE" or "NEGATIVE"

        Return:
        None
        """
        allowed = {"POSITIVE", "NEGATIVE", "POS", "NEG"}
        s = slope.upper()
        if s in allowed:
            val = "POS" if s.startswith("POS") else "NEG"
            self.instrument.write(f":TRIG:DEL:SLOPB {val}")
        else:
            print("Invalid slope. Allowed: POSITIVE, NEGATIVE.")

    def get_delay_slopb(self):
        """
        Query the edge type of edge B in delay trigger.

        Parameter:
        None

        Return:
        str: "POS" or "NEG"
        """
        return self.instrument.query(":TRIG:DEL:SLOPB?")

    def set_delay_type(self, dtype):
        """
        Set the delay type in delay trigger.

        Parameter:
        dtype (str): "GREATER", "LESS", "GLESS", "GOUT"

        Return:
        None
        """
        allowed = {"GREATER", "LESS", "GLESS", "GOUT"}
        d = dtype.upper()
        if d in allowed:
            val = d if d != "GLESS" else "GLES"
            self.instrument.write(f":TRIG:DEL:TYPE {val}")
        else:
            print("Invalid delay type. Allowed: GREATER, LESS, GLESS, GOUT.")

    def get_delay_type(self):
        """
        Query the delay type in delay trigger.

        
        Return:
        str: Delay type code
        """
        return self.instrument.query(":TRIG:DEL:TYPE?")

    def set_delay_tupper(self, upper):
        """
        Set the upper limit of the delay time in delay trigger (seconds).

        Parameter:
        upper (float): 16e-9 to 10

        Return:
        None
        """
        if isinstance(upper, (float, int)) and 16e-9 <= upper <= 10:
            self.instrument.write(f":TRIG:DEL:TUPP {upper}")
        else:
            print("Invalid upper limit. Must be between 16ns and 10s.")

    def get_delay_tupper(self):
        """
        Query the upper limit of the delay time in delay trigger (seconds).

        Parameter:
        None

        Return:
        float: Upper limit
        """
        resp = self.instrument.query(":TRIG:DEL:TUPP?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_delay_tlower(self, lower):
        """
        Set the lower limit of the delay time in delay trigger (seconds).

        Parameter:
        lower (float): 8e-9 to 9.99

        Return:
        None
        """
        if isinstance(lower, (float, int)) and 8e-9 <= lower <= 9.99:
            self.instrument.write(f":TRIG:DEL:TLOW {lower}")
        else:
            print("Invalid lower limit. Must be between 8ns and 9.99s.")

    def get_delay_tlower(self):
        """
        Query the lower limit of the delay time in delay trigger (seconds).

        Parameter:
        None

        Return:
        float: Lower limit
        """
        resp = self.instrument.query(":TRIG:DEL:TLOW?")
        try:
            return float(resp)
        except Exception:
            return resp

    # SHOLd Subtree
    def set_shold_dsrc(self, source):
        """
        Set the data source in setup/hold trigger.

        Parameter:
        source (str): "CHANNEL1" or "CHANNEL2"

        Return:
        None
        """
        allowed = {"CHANNEL1", "CHANNEL2", "CHAN1", "CHAN2"}
        s = source.upper()
        if s in allowed:
            val = "CHANnel1" if s in {"CHANNEL1", "CHAN1"} else "CHANnel2"
            self.instrument.write(f":TRIG:SHOL:DSRC {val}")
        else:
            print("Invalid source. Allowed: CHANNEL1, CHANNEL2.")

    def get_shold_dsrc(self):
        """
        Query the data source in setup/hold trigger.

        Parameter:
        None

        Return:
        str: "CHAN1" or "CHAN2"
        """
        return self.instrument.query(":TRIG:SHOL:DSRC?")

    def set_shold_csrc(self, source):
        """
        Set the clock source in setup/hold trigger.

        Parameter:
        source (str): "CHANNEL1" or "CHANNEL2"

        Return:
        None
        """
        allowed = {"CHANNEL1", "CHANNEL2", "CHAN1", "CHAN2"}
        s = source.upper()
        if s in allowed:
            val = "CHANnel1" if s in {"CHANNEL1", "CHAN1"} else "CHANnel2"
            self.instrument.write(f":TRIG:SHOL:CSRC {val}")
        else:
            print("Invalid source. Allowed: CHANNEL1, CHANNEL2.")

    def get_shold_csrc(self):
        """
        Query the clock source in setup/hold trigger.

        Parameter:
        None

        Return:
        str: "CHAN1" or "CHAN2"
        """
        return self.instrument.query(":TRIG:SHOL:CSRC?")

    def set_shold_slope(self, slope):
        """
        Set the edge type of the clock in setup/hold trigger.

        Parameter:
        slope (str): "POSITIVE" or "NEGATIVE"

        Return:
        None
        """
        allowed = {"POSITIVE", "NEGATIVE", "POS", "NEG"}
        s = slope.upper()
        if s in allowed:
            val = "POS" if s.startswith("POS") else "NEG"
            self.instrument.write(f":TRIG:SHOL:SLOP {val}")
        else:
            print("Invalid slope. Allowed: POSITIVE, NEGATIVE.")

    def get_shold_slope(self):
        """
        Query the edge type of the clock in setup/hold trigger.

        Parameter:
        None

        Return:
        str: "POS" or "NEG"
        """
        return self.instrument.query(":TRIG:SHOL:SLOP?")

    def set_shold_pattern(self, pattern):
        """
        Set the pattern in setup/hold trigger.

        Parameter:
        pattern (str): "SETUP" or "HOLD"

        Return:
        None
        """
        allowed = {"SETUP", "HOLD"}
        p = pattern.upper()
        if p in allowed:
            self.instrument.write(f":TRIG:SHOL:PATT {p}")
        else:
            print("Invalid pattern. Allowed: SETUP, HOLD.")

    def get_shold_pattern(self):
        """
        Query the pattern in setup/hold trigger.

        Parameter:
        None

        Return:
        str: "SETU" or "HOLD"
        """
        return self.instrument.query(":TRIG:SHOL:PATT?")

    def set_shold_type(self, typ):
        """
        Set the trigger type in setup/hold trigger.

        Parameter:
        typ (str): "GREATER" or "LESS"

        Return:
        None
        """
        allowed = {"GREATER", "LESS"}
        t = typ.upper()
        if t in allowed:
            self.instrument.write(f":TRIG:SHOL:TYPE {t}")
        else:
            print("Invalid type. Allowed: GREATER, LESS.")

    def get_shold_type(self):
        """
        Query the trigger type in setup/hold trigger.

        Parameter:
        None

        Return:
        str: "GREA" or "LESS"
        """
        return self.instrument.query(":TRIG:SHOL:TYPE?")

    def set_shold_stime(self, time):
        """
        Set the setup time in setup/hold trigger (seconds).

        Parameter:
        time (float): Setup time in seconds

        Return:
        None
        """
        self.instrument.write(f":TRIG:SHOL:STIM {time}")

    def get_shold_stime(self):
        """
        Query the setup time in setup/hold trigger (seconds).

        Parameter:
        None

        Return:
        float: Setup time in seconds
        """
        resp = self.instrument.query(":TRIG:SHOL:STIM?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_shold_htime(self, time):
        """
        Set the hold time in setup/hold trigger (seconds).

        Parameter:
        time (float): Hold time in seconds

        Return:
        None
        """
        self.instrument.write(f":TRIG:SHOL:HTIM {time}")

    def get_shold_htime(self):
        """
        Query the hold time in setup/hold trigger (seconds).

        Parameter:
        None

        Return:
        float: Hold time in seconds
        """
        resp = self.instrument.query(":TRIG:SHOL:HTIM?")
        try:
            return float(resp)
        except Exception:
            return resp
    # --- Additional Trigger Functions ---

    # NEDG Subtree
    def set_nedg_source(self, source):
        """
        Set the trigger source in noise edge trigger.

        Parameter:
        source (str): "CHANNEL1" or "CHANNEL2"

        Return:
        None
        """
        allowed = {"CHANNEL1", "CHANNEL2", "CHAN1", "CHAN2"}
        s = source.upper()
        if s in allowed:
            val = "CHANnel1" if s in {"CHANNEL1", "CHAN1"} else "CHANnel2"
            self.instrument.write(f":TRIG:NEDG:SOUR {val}")
        else:
            print("Invalid source. Allowed: CHANNEL1, CHANNEL2.")

    def get_nedg_source(self):
        """
        Query the trigger source in noise edge trigger.

        Parameter:
        None

        Return:
        str: "CHAN1" or "CHAN2"
        """
        return self.instrument.query(":TRIG:NEDG:SOUR?")

    def set_nedg_slope(self, slope):
        """
        Set the edge type in noise edge trigger.

        Parameter:
        slope (str): "POSITIVE", "NEGATIVE", "RFALL"

        Return:
        None
        """
        allowed = {"POSITIVE", "NEGATIVE", "RFALL", "POS", "NEG"}
        s = slope.upper()
        if s in allowed:
            val = "POS" if s.startswith("POS") else ("NEG" if s.startswith("NEG") else "RFAL")
            self.instrument.write(f":TRIG:NEDG:SLOP {val}")
        else:
            print("Invalid slope. Allowed: POSITIVE, NEGATIVE, RFALL.")

    def get_nedg_slope(self):
        """
        Query the edge type in noise edge trigger.

        Parameter:
        None

        Return:
        str: "POS", "NEG", or "RFAL"
        """
        return self.instrument.query(":TRIG:NEDG:SLOP?")

    def set_nedg_level(self, level):
        """
        Set the trigger level in noise edge trigger.

        Parameter:
        level (float): Level value

        Return:
        None
        """
        self.instrument.write(f":TRIG:NEDG:LEV {level}")

    def get_nedg_level(self):
        """
        Query the trigger level in noise edge trigger.

        Parameter:
        None

        Return:
        float: Level value
        """
        resp = self.instrument.query(":TRIG:NEDG:LEV?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_nedg_idle(self, noise):
        """
        The query returns the idle time in scientific notation

        Parameter:
        noise (float): Noise value

        Return:
        None
        """
        self.instrument.write(f":TRIG:NEDG:IDLE {noise}")

    def get_nedg_idle(self):
        """
        Query the noise tolerance in noise edge trigger.
       
        Return:
        float: Noise value
        """
        resp = self.instrument.query(":TRIG:NEDG:IDLE?")
        try:
            return float(resp)
        except Exception:
            return resp

# RS232 Subtree
class RS232:
    """
    The RS232 trigger commands for the oscilloscope.
    """
    def __init__(self, instrument,data_handler):
        self.instrument = instrument
        self.data_handler = data_handler

    def set_source(self, source):
        """
        Set the trigger source in RS232 trigger.

        Parameter:
        source (str): "CHANNEL1" or "CHANNEL2"
        """
        allowed = {"CHANNEL1", "CHANNEL2", "CHAN1", "CHAN2"}
        s = source.upper()
        if s in allowed:
            val = "CHANnel1" if s in {"CHANNEL1", "CHAN1"} else "CHANnel2"
            self.instrument.write(f":TRIG:RS232:SOUR {val}")
        else:
            print("Invalid source. Allowed: CHANNEL1, CHANNEL2.")

    def get_source(self):
        """
        Query the trigger source in RS232 trigger.

        Returns:
        str: "CHAN1" or "CHAN2"
        """
        return self.instrument.query(":TRIG:RS232:SOUR?")

    def set_when(self, when):
        """
        Set the trigger condition in RS232 trigger.

        Parameter:
        when (str): "START", "STOP", "DATA", "PARITY", "ERROR"
        """
        allowed = {"START", "STOP", "DATA", "PARITY", "ERROR"}
        w = when.upper()
        if w in allowed:
            self.instrument.write(f":TRIG:RS232:WHEN {w}")
        else:
            print("Invalid when. Allowed: START, STOP, DATA, PARITY, ERROR.")

    def get_when(self):
        """
        Query the trigger condition in RS232 trigger.

        Returns:
        str: Condition
        """
        return self.instrument.query(":TRIG:RS232:WHEN?")

    def set_parity(self, parity):
        """
        Set the parity in RS232 trigger.

        Parameter:
        parity (str): "NONE", "EVEN", or "ODD"
        """
        allowed = {"NONE", "EVEN", "ODD"}
        p = parity.upper()
        if p in allowed:
            self.instrument.write(f":TRIG:RS232:PAR {p}")
        else:
            print("Invalid parity. Allowed: NONE, EVEN, ODD.")

    def get_parity(self):
        """
        Query the parity in RS232 trigger.

        Returns:
        str: Parity
        """
        return self.instrument.query(":TRIG:RS232:PAR?")

    def set_stop(self, stop):
        """
        Set the stop bit in RS232 trigger.

        Parameter:
        stop (float): Stop bit, one of 1, 1.5, or 2
        """
        allowed = {1, 1.5, 2}
        if stop in allowed:
            self.instrument.write(f":TRIG:RS232:STOP {stop}")
        else:
            print("Invalid stop bit. Allowed: 1, 1.5, 2.")

    def get_stop(self):
        """
        Query the stop bit in RS232 trigger.

        Returns:
        float: Stop bit
        """
        resp = self.instrument.query(":TRIG:RS232:STOP?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_data(self, data):
        """
        Set the data width in RS232 trigger.
        
        Parameter:
        data (int): Data width, 5 to 8
        """
        if isinstance(data, int) and 5 <= data <= 8:
            self.instrument.write(f":TRIG:RS232:DATA {data}")
        else:
            print("Invalid data width. Must be integer between 5 and 8.")

    def get_data(self):
        """
        Query the data width in RS232 trigger.
        
        Returns:
        int: Data width
        """
        resp = self.instrument.query(":TRIG:RS232:DATA?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_width(self, width):
        """
        Set the width in RS232 trigger.
        
        Parameter:
        width (int): Data width, 5 to 8
        """
        if isinstance(width, int) and 5 <= width <= 8:
            self.instrument.write(f":TRIG:RS232:WIDT {width}")
        else:
            print("Invalid width. Must be integer between 5 and 8.")

    def get_width(self):
        """
        Query the width in RS232 trigger.
        
        Returns:
        int: Data width
        """
        resp = self.instrument.query(":TRIG:RS232:WIDT?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_baud(self, baud):
        """
        Set the baud rate in RS232 trigger.
        
        Parameter:
        baud (int): Baud rate, 110 to 20000000
        """
        if isinstance(baud, int) and 110 <= baud <= 20000000:
            self.instrument.write(f":TRIG:RS232:BAUD {baud}")
        else:
            print("Invalid baud rate. Must be integer between 110 and 20000000.")

    def get_baud(self):
        """
        Query the baud rate in RS232 trigger.
        
        Returns:
        int: Baud rate
        """
        resp = self.instrument.query(":TRIG:RS232:BAUD?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_buser(self, buser):
        """
        Set the bus user value in RS232 trigger.
        
        Parameter:
        buser (int): User value (see instrument documentation for valid range)
        """
        if isinstance(buser, int):
            self.instrument.write(f":TRIG:RS232:BUS {buser}")
        else:
            print("Invalid bus user value. Must be integer.")

    def get_buser(self):
        """
        Query the bus user value in RS232 trigger.
        
        Returns:
        int: Bus user value
        """
        resp = self.instrument.query(":TRIG:RS232:BUS?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_level(self, level):
        """
        Set the trigger level in RS232 trigger.
        
        Parameter:
        level (float): Level value
        """
        self.instrument.write(f":TRIG:RS232:LEV {level}")

    def get_level(self):
        """
        Query the trigger level in RS232 trigger.
        
        Returns: 
        float: Level value
        """
        resp = self.instrument.query(":TRIG:RS232:LEV?")
        try:
            return float(resp)
        except Exception:
            return resp

class IIC_Trigger:
    """
    The IIC trigger commands for the oscilloscope.
    """
    def __init__(self, instrument,data_handler):
        self.instrument = instrument
        self.data_handler = data_handler

    def set_scl(self, source):
        """
        Set the channel source of SCL in I2C trigger.

        Parameters: source (str): "CHANNEL1" or "CHANNEL2"
        """
        allowed = {"CHANNEL1", "CHANNEL2", "CHAN1", "CHAN2"}
        s = source.upper()
        if s in allowed:
            val = "CHANnel1" if s in {"CHANNEL1", "CHAN1"} else "CHANnel2"
            self.instrument.write(f":TRIG:IIC:SCL {val}")
        else:
            print("Invalid source. Allowed: CHANNEL1, CHANNEL2.")

    def get_scl(self):
        """
        Query the channel source of SCL in I2C trigger.

        Returns: str: "CHAN1" or "CHAN2"
        """
        return self.instrument.query(":TRIG:IIC:SCL?")

    def set_sda(self, source):
        """
        Set the channel source of SDA in I2C trigger.
        
        Parameters: source (str): "CHANNEL1" or "CHANNEL2"
        """
        allowed = {"CHANNEL1", "CHANNEL2", "CHAN1", "CHAN2"}
        s = source.upper()
        if s in allowed:
            val = "CHANnel1" if s in {"CHANNEL1", "CHAN1"} else "CHANnel2"
            self.instrument.write(f":TRIG:IIC:SDA {val}")
        else:
            print("Invalid source. Allowed: CHANNEL1, CHANNEL2.")

    def get_sda(self):
        """
        Query the channel source of SDA in I2C trigger.
        
        Returns: str: "CHAN1" or "CHAN2"
        """
        return self.instrument.query(":TRIG:IIC:SDA?")

    def set_when(self, trig_type):
        """
        Set the trigger condition in I2C trigger.
        trig_type (str): "START", "RESTART", "STOP", "NACKNOWLEDGE", "ADDRESS", "DATA", "ADATA"
        """
        allowed = {"START", "RESTART", "STOP", "NACKNOWLEDGE", "ADDRESS", "DATA", "ADATA"}
        t = trig_type.upper()
        if t in allowed:
            val = {
                "START": "STARt",
                "RESTART": "RESTart",
                "STOP": "STOP",
                "NACKNOWLEDGE": "NACKnowledge",
                "ADDRESS": "ADDRess",
                "DATA": "DATA",
                "ADATA": "ADATa"
            }[t]
            self.instrument.write(f":TRIG:IIC:WHEN {val}")
        else:
            print("Invalid trigger type.")

    def get_when(self):
        """
        Query the trigger condition in I2C trigger.

        Returns: str
        """
        return self.instrument.query(":TRIG:IIC:WHEN?")

    def set_awidth(self, bits):
        """
        Set the address bits when trigger condition is ADDRESS or ADATA.
        bits (int): 7, 8, or 10
        """
        if bits in [7, 8, 10]:
            self.instrument.write(f":TRIG:IIC:AWIDth {bits}")
        else:
            print("Invalid address width. Allowed: 7, 8, 10.")

    def get_awidth(self):
        """
        Query the address bits for I2C trigger.

        Returns: int
        """
        resp = self.instrument.query(":TRIG:IIC:AWIDth?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_address(self, adr):
        """
        Set the address for ADDRESS or ADATA trigger.
        adr (int): 0 to 1023 (depends on address width)
        """
        if isinstance(adr, int) and 0 <= adr <= 1023:
            self.instrument.write(f":TRIG:IIC:ADDRess {adr}")
        else:
            print("Invalid address value.")

    def get_address(self):
        """
        Query the address for I2C trigger.

        Returns: int
        """
        resp = self.instrument.query(":TRIG:IIC:ADDRess?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_direction(self, direction):
        """
        Set the data direction for ADDRESS or ADATA trigger.
        direction (str): "READ", "WRITE", or "RWRITE"
        """
        allowed = {"READ", "WRITE", "RWRITE"}
        d = direction.upper()
        if d in allowed:
            val = {"READ": "READ", "WRITE": "WRITe", "RWRITE": "RWRite"}[d]
            self.instrument.write(f":TRIG:IIC:DIRection {val}")
        else:
            print("Invalid direction. Allowed: READ, WRITE, RWRITE.")

    def get_direction(self):
        """
        Query the data direction for I2C trigger.
        
        Returns: str
        """
        return self.instrument.query(":TRIG:IIC:DIRection?")

    def set_data(self, data):
        """
        Set the data for DATA or ADATA trigger.
        
        Parameters: data (int): 0 to 2^40-1 (max 40 bits)
        """
        if isinstance(data, int) and 0 <= data < 2**40:
            self.instrument.write(f":TRIG:IIC:DATA {data}")
        else:
            print("Invalid data value.")

    def get_data(self):
        """
        Query the data for I2C trigger.
        
        Returns: int
        """
        resp = self.instrument.query(":TRIG:IIC:DATA?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_clevel(self, level):
        """
        Set the trigger level of SCL in I2C trigger.
        
        Parameters: level (float): Level value
        """
        self.instrument.write(f":TRIG:IIC:CLEVel {level}")

    def get_clevel(self):
        """
        Query the trigger level of SCL in I2C trigger.
        
        Returns: float
        """
        resp = self.instrument.query(":TRIG:IIC:CLEVel?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_dlevel(self, level):
        """
        Set the trigger level of SDA in I2C trigger.
        
        Parameters: level (float): Level value
        """
        self.instrument.write(f":TRIG:IIC:DLEVel {level}")

    def get_dlevel(self):
        """
        Query the trigger level of SDA in I2C trigger.
        
        Returns: float
        """
        resp = self.instrument.query(":TRIG:IIC:DLEVel?")
        try:
            return float(resp)
        except Exception:
            return resp

class SPI_Trigger:
    """
    The SPI trigger commands for the oscilloscope.
    """
    def __init__(self, instrument,data_handler):
        self.instrument = instrument
        self.data_handler = data_handler

    def set_scl(self, source):
        """
        Set the channel source of SCL in SPI trigger.
        
        Parameters: source (str): "CHANNEL1" or "CHANNEL2"
        """
        allowed = {"CHANNEL1", "CHANNEL2", "CHAN1", "CHAN2"}
        s = source.upper()
        if s in allowed:
            val = "CHANnel1" if s in {"CHANNEL1", "CHAN1"} else "CHANnel2"
            self.instrument.write(f":TRIG:SPI:SCL {val}")
        else:
            print("Invalid source. Allowed: CHANNEL1, CHANNEL2.")

    def get_scl(self):
        """
        Query the channel source of SCL in SPI trigger.
        
        Returns: str: "CHAN1" or "CHAN2"
        """
        return self.instrument.query(":TRIG:SPI:SCL?")

    def set_sda(self, source):
        """
        Set the channel source of SDA in SPI trigger.
        
        Parameters: source (str): "CHANNEL1" or "CHANNEL2"
        """
        allowed = {"CHANNEL1", "CHANNEL2", "CHAN1", "CHAN2"}
        s = source.upper()
        if s in allowed:
            val = "CHANnel1" if s in {"CHANNEL1", "CHAN1"} else "CHANnel2"
            self.instrument.write(f":TRIG:SPI:SDA {val}")
        else:
            print("Invalid source. Allowed: CHANNEL1, CHANNEL2.")

    def get_sda(self):
        """
        Query the channel source of SDA in SPI trigger.
        
        Returns: str: "CHAN1" or "CHAN2"
        """
        return self.instrument.query(":TRIG:SPI:SDA?")

    def set_when(self, trig_type):
        """
        Set the trigger condition in SPI trigger.
        
        Parameters: trig_type (str): "CS" or "TIMEOUT"
        """
        allowed = {"CS", "TIMEOUT"}
        t = trig_type.upper()
        if t in allowed:
            val = "CS" if t == "CS" else "TIMeout"
            self.instrument.write(f":TRIG:SPI:WHEN {val}")
        else:
            print("Invalid trigger type. Allowed: CS, TIMEOUT.")

    def get_when(self):
        """
        Query the trigger condition in SPI trigger.
        
        Returns: str
        """
        return self.instrument.query(":TRIG:SPI:WHEN?")

    def set_width(self, width):
        """
        Set the data bits of the SDA channel in SPI trigger.
        
        Parameters: width (int): 4 to 32
        """
        if isinstance(width, int) and 4 <= width <= 32:
            self.instrument.write(f":TRIG:SPI:WIDTh {width}")
        else:
            print("Invalid width. Must be integer between 4 and 32.")

    def get_width(self):
        """
        Query the data bits of the SDA channel in SPI trigger.
        
        Returns: int
        """
        resp = self.instrument.query(":TRIG:SPI:WIDTh?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_data(self, data):
        """
        Set the data in SPI trigger.

        Parameters: data (int): 0 to 2^32-1
        """
        if isinstance(data, int) and 0 <= data < 2**32:
            self.instrument.write(f":TRIG:SPI:DATA {data}")
        else:
            print("Invalid data value.")

    def get_data(self):
        """
        Query the data in SPI trigger.

        Returns: int
        """
        resp = self.instrument.query(":TRIG:SPI:DATA?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_timeout(self, time_value):
        """
        Set the timeout value in SPI trigger (seconds).

        Parameters:  time_value (float): 100e-9 to 1
        """
        if isinstance(time_value, (float, int)) and 1e-7 <= time_value <= 1:
            self.instrument.write(f":TRIG:SPI:TIMeout {time_value}")
        else:
            print("Invalid timeout value. Must be between 100ns and 1s.")

    def get_timeout(self):
        """
        Query the timeout value in SPI trigger.
        
        Parameters: Returns: float
        """
        resp = self.instrument.query(":TRIG:SPI:TIMeout?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_slope(self, slope):
        """
        Set the clock edge in SPI trigger.
        
        Parameters: slope (str): "POSITIVE" or "NEGATIVE"
        """
        allowed = {"POSITIVE", "NEGATIVE", "POS", "NEG"}
        s = slope.upper()
        if s in allowed:
            val = "POSitive" if s.startswith("POS") else "NEGative"
            self.instrument.write(f":TRIG:SPI:SLOPe {val}")
        else:
            print("Invalid slope. Allowed: POSITIVE, NEGATIVE.")

    def get_slope(self):
        """
        Query the clock edge in SPI trigger.
        
        Parameters: Returns: str: "POS" or "NEG"
        """
        return self.instrument.query(":TRIG:SPI:SLOPe?")

    def set_clevel(self, level):
        """
        Set the trigger level of the SCL channel in SPI trigger.

        Parameters:
        level (float): Level value
        """
        self.instrument.write(f":TRIG:SPI:CLEVel {level}")

    def get_clevel(self):
        """
        Query the trigger level of the SCL channel in SPI trigger.
        
        Returns: float
        """
        resp = self.instrument.query(":TRIG:SPI:CLEVel?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_dlevel(self, level):
        """
        Set the trigger level of the SDA channel in SPI trigger.

        Parameters: 
        level (float): Level value
        """
        self.instrument.write(f":TRIG:SPI:DLEVel {level}")

    def get_dlevel(self):
        """
        Query the trigger level of the SDA channel in SPI trigger.
        
        Returns: float
        """
        resp = self.instrument.query(":TRIG:SPI:DLEVel?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_slevel(self, level):
        """
        Set the trigger level of the CS channel in SPI trigger.

        Parameters: level (float): Level value
        """
        self.instrument.write(f":TRIG:SPI:SLEVel {level}")

    def get_slevel(self):
        """
        Query the trigger level of the CS channel in SPI trigger.

        Returns: float
        """
        resp = self.instrument.query(":TRIG:SPI:SLEVel?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_mode(self, mode):
        """
        Set the CS mode when trigger condition is CS in SPI trigger.

        Parameters: mode (str): "HIGH" or "LOW"
        """
        allowed = {"HIGH", "LOW"}
        m = mode.upper()
        if m in allowed:
            self.instrument.write(f":TRIG:SPI:MODE {m}")
        else:
            print("Invalid mode. Allowed: HIGH, LOW.")

    def get_mode(self):
        """
        Query the CS mode when trigger condition is CS in SPI trigger.

        Returns: str: "HIGH" or "LOW"
        """
        return self.instrument.query(":TRIG:SPI:MODE?")

    def set_cs(self, source):
        """
        Set the data source of the CS signal in SPI trigger.

        Parameters: source (str): "CHANNEL1" or "CHANNEL2"
        """
        allowed = {"CHANNEL1", "CHANNEL2", "CHAN1", "CHAN2"}
        s = source.upper()
        if s in allowed:
            val = "CHANnel1" if s in {"CHANNEL1", "CHAN1"} else "CHANnel2"
            self.instrument.write(f":TRIG:SPI:CS {val}")
        else:
            print("Invalid source. Allowed: CHANNEL1, CHANNEL2.")

    def get_cs(self):
        """
        Query the data source of the CS signal in SPI trigger.

        Returns: str: "CHAN1" or "CHAN2"
        """
        return self.instrument.query(":TRIG:SPI:CS?")
class Waveform:
    """The Waveform commands are used to read the waveform data and its related settings.
    """
    def __init__(self, instrument,data_handler):
        self.instrument = instrument
        self.data_handler = data_handler

    def set_source(self, source):
        """Set the channel of which the waveform data will be read.

        Parameter: source (str): "CHANnel1", "CHANnel2", or "MATH"

        Return: None
        """
        allowed = {"CHANNEL1", "CHANNEL2", "MATH", "CHAN1", "CHAN2"}
        s = source.upper()
        if s in allowed:
            val = "CHANnel1" if s in {"CHANNEL1", "CHAN1"} else ("CHANnel2" if s in {"CHANNEL2", "CHAN2"} else "MATH")
            self.instrument.write(f":WAVeform:SOURce {val}")
        else:
            print("Invalid source. Allowed: CHANnel1, CHANnel2, MATH.")

    def get_source(self):
        """Query the channel of which the waveform data will be read.

        Parameter: None

        Return: str: "CHAN1", "CHAN2", or "MATH"
        """
        return self.instrument.query(":WAVeform:SOURce?")

    def set_mode(self, mode):
        """
        Set the reading mode used by :WAVeform:DATA?.

        Parameter: mode (str): "NORMal", "MAXimum", or "RAW"

        Return: None
        """
        allowed = {"NORMAL", "MAXIMUM", "RAW", "NORMal", "MAXimum"}
        m = mode.upper()
        if m in {"NORMAL", "NORMal"}:
            val = "NORMal"
        elif m in {"MAXIMUM", "MAXimum"}:
            val = "MAXimum"
        elif m == "RAW":
            val = "RAW"
        else:
            print("Invalid mode. Allowed: NORMal, MAXimum, RAW.")
            return
        self.instrument.write(f":WAVeform:MODE {val}")

    def get_mode(self):
        """Query the reading mode used by :WAVeform:DATA?.
        
        Parameter: None
        
        Return: str: "NORM", "MAX", or "RAW"
        """
        return self.instrument.query(":WAVeform:MODE?")

    def set_format(self, fmt):
        """Set the return format of the waveform data.
        
        Parameter: fmt (str): "WORD", "BYTE", or "ASCii"
        
        Return: None
        """
        allowed = {"WORD", "BYTE", "ASCII", "ASCii"}
        f = fmt.upper()
        if f in {"WORD"}:
            val = "WORD"
        elif f in {"BYTE"}:
            val = "BYTE"
        elif f in {"ASCII", "ASCii"}:
            val = "ASCii"
        else:
            print("Invalid format. Allowed: WORD, BYTE, ASCii.")
            return
        self.instrument.write(f":WAVeform:FORMat {val}")

    def get_format(self):
        """
        Query the return format of the waveform data.

        Parameter: None

        Return: str: "WORD", "BYTE", or "ASC"
        """
        return self.instrument.query(":WAVeform:FORMat?")

    def get_data(self):
        """Read the waveform data. If autosave is on, then also saves them to a csv file.
        
        Parameter: None
        
        Return: bytes or str: Raw waveform data (format depends on :WAVeform:FORMat)
        """
        fmt = self.get_format()
        if fmt == "ASC":
            data = self.instrument.query(":WAVeform:DATA?")
        else:
            data = self.instrument.query_binary_values(":WAVeform:DATA?", datatype='B', container=bytes)
            if data and data[0] == ord('#'):  # Check for TMC header
                data = self.data_handler.remove_tmc_header(data)

        if self.data_handler.auto_save:
            
            self.data_handler.write_to_file("Waveform_Data", data, EFileType.CSV)  

    def set_start(self, sta):
        """Set the start point of waveform data reading.
        
        Parameter: sta (int): Start point (see documentation for valid range)
        
        Return: None
        """
        if isinstance(sta, int) and sta >= 1:
            self.instrument.write(f":WAVeform:STARt {sta}")
        else:
            print("Invalid start point. Must be integer >= 1.")

    def get_start(self):
        """Query the start point of waveform data reading.
        
        Parameter: None
        
        Return: int: Start point
        """
        resp = self.instrument.query(":WAVeform:STARt?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_stop(self, stop):
        """Set the stop point of waveform data reading.
        
        Parameter: stop (int): Stop point (see documentation for valid range)
        
        Return: None"""
        if isinstance(stop, int) and stop >= 1:
            self.instrument.write(f":WAVeform:STOP {stop}")
        else:
            print("Invalid stop point. Must be integer >= 1.")

    def get_stop(self):
        """Query the stop point of waveform data reading.
        
        Parameter: None
        
        Return: int: Stop point"""
        resp = self.instrument.query(":WAVeform:STOP?")
        try:
            return int(resp)
        except Exception:
            return resp

    def get_xincrement(self):
        """Query the time difference between two neighboring points of the specified channel source in the X direction.
        
        Parameter: None
        
        Return:float: X increment (seconds or Hz)
        """
        resp = self.instrument.query(":WAVeform:XINCrement?")
        try:
            return float(resp)
        except Exception:
            return resp

    def get_xorigin(self):
        """Query the start time of the waveform data of the channel source currently selected in the X direction.
        
        Parameter: None
        
        Return: float: X origin (seconds or Hz)
        """
        resp = self.instrument.query(":WAVeform:XORigin?")
        try:
            return float(resp)
        except Exception:
            return resp

    def get_xreference(self):
        """Query the reference time of the specified channel source in the X direction.
        
        Parameter: None
        
        Return: 
        int: X reference (usually 0)
        """
        resp = self.instrument.query(":WAVeform:XREFerence?")
        try:
            return int(resp)
        except Exception:
            return resp

    def get_yincrement(self):
        """Query the waveform increment of the specified channel source in the Y direction.
        
        Parameter: None
        
        Return: 
        float: Y increment (amplitude unit)
        """
        resp = self.instrument.query(":WAVeform:YINCrement?")
        try:
            return float(resp)
        except Exception:
            return resp

    def get_yorigin(self):
        """
        Query the vertical offset relative to the vertical reference position of the specified channel source in the Y direction.
        
        Parameter: None
        
        Return: 
        int: Y origin
        """
        resp = self.instrument.query(":WAVeform:YORigin?")
        try:
            return int(resp)
        except Exception:
            return resp

    def get_yreference(self):
        """Query the vertical reference position of the specified channel source in the Y direction.
        
        Parameter: None
        
        Return: 
        int: Y reference (usually 127)
        """
        resp = self.instrument.query(":WAVeform:YREFerence?")
        try:
            return int(resp)
        except Exception:
            return resp

    def get_preamble(self):
        """Query and return all the waveform parameters.
        
        Parameter: None
        
        Return: 
        str: 10 waveform parameters separated by commas
        """
        return self.instrument.query(":WAVeform:PREamble?")