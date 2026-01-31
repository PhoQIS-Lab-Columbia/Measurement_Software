
from time import sleep

import pyvisa
from Instruments.EFileType import EFileType
from Instruments.Instrument import Instrument
from Instruments.EInstrument import EInstrument
from PIL import Image

class Oscilloscope(Instrument):
    """The main Rigol Oscillscope."""
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
    """The Aquire commands are used to set and query the memory depth, acquisition mode and the number of averages as well as query the current sample rate of the oscilloscope."""
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
        """Get acquisition mode. Normal:  Samples the signal at equal time interval to rebuild the waveform. Averages:  Averages the waveforms from multiple samples to reduce the random noise of the input signal. Peak: Acquires the maximum and minimum values of the signal within the sample interval to get the envelope of the signal. HRESolution:  ultra-sample technique to average the neighboring points of the sample waveform to reduce the random noise on the input signal and generate much smoother waveforms 
        
        :return: Acquisition mode
        :rtype: str"""
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
        """In the average acquisition mode, a greater number of averages can reduce noise and increase vertical resolution.
        
        :return: Number of averages (2 to 1024)
        :rtype: str"""
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
        """ Get memory depth of the oscilloscope (namely the number of waveform points that can be stored in a single trigger sample).
        
        :return: Memory depth
        :rtype: str"""
        comm_mode = ":ACQuire:MDEPth?"
        return self.instrument.query(comm_mode)


    def get_sample_rate(self):
        """ Query the current sample rate. The default unit is Sa/s.
        
        :return: Sample rate
        :rtype: str"""
        comm_mode = ":ACQuire:SRATe?"
        return self.instrument.query(comm_mode)
        # Calibration Commands
class Calibrate:
    """
    The calibrate commands are used to control the oscilloscope's self-calibration process.
    """
    def __init__(self, instrument,data_handler):
        """The calibrate class is used to control the oscilloscope's self-calibration process.
        

        :param instrument: The instrument to control.
        :type instrument: pyvisa.Resource

        :param data_handler: The data handler for processing data.
        :type data_handler: DataHandler"""

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
        """
    def __init__(self, instrument,data_handler, channel):
        """Initalize the channel class.
        

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
        """
        Set the invert mode of the specified channel.


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


        :param param1: The offset value to set, in volts.
        :type param1: float
        """
        
        allowed_chnl_values = [1, 2]
        if self.channel in allowed_chnl_values:
            comm = f":CHANnel{self.channel}:OFFSet {param1}"
            self.instrument.write(comm)
        else:
            print("Invalid channel.")

    def get_offset(self):
        """
        Query the vertical offset of the specified channel. The default unit is V.

        :return: The vertical offset value in volts.
        :rtype: str"""
        comm_mode = f":CHANnel{self.channel}:OFFSet?"
        return self.instrument.query(comm_mode)

    def set_range(self,  param1):
        """Set the vertical range of the specified channel. The default unit is V.
        

        :param param1: The vertical range value to set, in volts.
        :type param1: float"""
        allowed_chnl_values = [1, 2]
        if self.channel in allowed_chnl_values:
            comm = f":CHANnel{self.channel}:RANGe {param1}"
            self.instrument.write(comm)
        else:
            print("Invalid channel.")

    def get_range(self):
        """Query the vertical range of the specified channel. The default unit is V.

        :return: The vertical range value in volts.
        :rtype: str
        """
        comm_mode = f":CHANnel{self.channel}:RANGe?"
        return self.instrument.query(comm_mode)

    def set_tcal(self,  val):
        """
        Set delay calibration time for the specified channel.


        :param val: delay time in seconds (e.g., 20e-9 for 20ns). Valid range: -100e-9 to 100e-9.
        :type val: float
        """
        if self.channel in [1, 2] and isinstance(val, (float, int)) and -100e-9 <= val <= 100e-9:
            self.instrument.write(f":CHANnel{self.channel}:TCAL {val}")
        else:
            print("Invalid channel or value (must be float between -100e-9 and 100e-9)")

    def get_tcal(self):
        """
        Query delay calibration time for the specified channel (in seconds).
        
        :return: value in scientific notation as float.
        :rtype: float
        """
        if self.channel in [1, 2]:
            response = self.instrument.query(f":CHANnel{self.channel}:TCAL?")
            return float(response)
        else:
            print("Invalid channel number.")
            return None

    def set_scale(self,  scale):
        """Set vertical scale of the channel (in V/div).
        

        :param scale: Vertical scale value to set, in volts per division.
        :type scale: float"""
        self.instrument.write(f":CHANnel{self.channel}:SCALe {scale}")

    def get_scale(self):
        """Query vertical scale of the channel.
        
        :return: Vertical scale value in volts per division.
        :rtype: str"""
        return self.instrument.query(f":CHANnel{self.channel}:SCALe?")

    def set_probe_ratio(self,  ratio):
        """Set the probe attenuation ratio for a channel.
        

        :param ratio: Probe attenuation ratio to set.
        :type ratio: float"""
        self.instrument.write(f":CHANnel{self.channel}:PROBe {ratio}")

    def get_probe_ratio(self):
        """Query the probe attenuation ratio for a channel.
        
        :return: Probe attenuation ratio.
        :rtype: str"""
        return self.instrument.query(f":CHANnel{self.channel}:PROBe?")

    def set_units(self,  unit):
        """Set the amplitude display unit for a channel. 
        

        :param unit: Options: VOLTage, WATT, AMPere, UNKNown.
        :type unit: str"""
        self.instrument.write(f":CHANnel{self.channel}:UNITs {unit}")

    def get_units(self):
        """Query the amplitude display unit for a channel.
        
        :return: Amplitude display unit.
        :rtype: str"""
        return self.instrument.query(f":CHANnel{self.channel}:UNITs?")

    def set_vernier(self,  state):
        """Enable or disable fine adjustment (vernier) for vertical scale.
        

        :param state: "ON" to enable vernier, "OFF" to disable.
        :type state: str"""

        self.instrument.write(f":CHANnel{self.channel}:VERNier {state}")

    def get_vernier(self):
        """Query vernier setting.
        
        :return: "ON" if vernier is enabled, "OFF" if disabled.
        :rtype: str"""
        return self.instrument.query(f":CHANnel{self.channel}:VERNier?")
                    
class Cursor:
    """The Cursor commands are used to control and query cursor-specific settings."""
    def __init__(self, instrument,data_handler):
        """Initalize the Cursor class.
        

        :param instrument: The instrument to control.
        :type instrument: pyvisa.Resource"""
        self.instrument = instrument
        self.data_handler = data_handler
    
    def set_mode(self, mode):
        """
        Set cursor measurement mode.


        :param mode: One of {"OFF", "MANual", "TRACk", "AUTO", "XY"} Note: XY mode only valid when timebase mode is also XY.
        :type mode: str
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

        :returns: One of {"OFF", "MAN", "TRAC", "AUTO", "XY"}
        :rtype: str
        """
        return self.instrument.query(":CURSor:MODE?")

    def set_manual_type(self, cursor_type):
        """
        Set the type of manual cursor.


        :param cursor_type: Either "X" for vertical cursors (time) or "Y" for horizontal cursors (voltage).
        :type cursor_type: str
        """
        cursor_type = cursor_type.upper()
        if cursor_type in ["X", "Y"]:
            self.instrument.write(f":CURSor:MANual:TYPE {cursor_type}")
        else:
            print("Invalid cursor type. Use 'X' or 'Y'.")

    def get_manual_type(self):
        """
        Query the current manual cursor type.

        :return: "X" or "Y"
        :rtype: str 
        """
        return self.instrument.query(":CURSor:MANual:TYPE?")

    def set_manual_source(self, source):
        """
        Set the source for manual cursor measurement.


        :param source: Channel or source name. Valid options include: "CHAN1", "CHAN2", "MATH", "REF1", "REF2", "REF3", "REF4"
        :type source: str
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

        :return: Current source, such as "CHAN1", "CHAN2", "MATH", etc.
        :rtype: str
        """
        return self.instrument.query(":CURSor:MANual:SOURce?")

    def set_manual_tunit(self, unit):
        """ Set the horizontal unit for manual cursor measurement. 


        :param unit: The unit to set, such as "S", "HZ", "DEGREE", "PERCENT".
        :type unit: str
        """
        valid_units = ["S", "HZ", "DEGREE", "PERCENT"]
        unit = unit.upper()
        if unit in valid_units:
            self.instrument.write(f":CURSor:MANual:TUNit {unit}")
        else:
            print(f"Invalid unit. Valid options are: {valid_units}")

    def get_manual_tunit(self):
        """ Query the current horizontal unit in the manual cursor measurement mode. 

        :return: The current horizontal unit, such as "S", "HZ", "DEGREE", "PERCENT".
        :rtype: str
        """
        return self.instrument.query(":CURSor:MANual:TUNit?")

    def set_manual_vunit(self, unit):
        """ Set the vertical unit for manual cursor measurement. 


        :param unit: The unit to set, such as "PERCENT", "SOURCE".
        :type unit: str
        """
        valid_units = ["PERCENT", "SOURCE"]
        unit = unit.upper()
        if unit in valid_units:
            self.instrument.write(f":CURSor:MANual:VUNit {unit}")
        else:
            print(f"Invalid unit. Valid options are: {valid_units}")

    def get_manual_vunit(self):
        """ Query the current vertical unit in the manual cursor measurement mode. 

        :return: The current vertical unit, such as "PERCENT", "SOURCE".
        :rtype: str
        """
        return self.instrument.query(":CURSor:MANual:VUNit?")

    def set_manual(self, cursor, x, y):
        """ Set the horizontal position of cursor A or B in the manual cursor measurement mode. 


        :param cursor: Cursor identifier, either "A" or "B".
        :type cursor: str

        :param x: Horizontal position, must be between 5 and 594.
        :type x: int

        :param y: Vertical position, must be between 5 and 394.
        :type y: int
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


        :param cursor: Cursor identifier, either "A" or "B".
        :type cursor: str
        :return: The x and y coordinates of the cursor in the format "x;y".
        :rtype: str
        """
        return self.instrument.query(f":CURSor:MANual:{cursor}X?;{cursor}Y?")

    def get_manual_xdelta(self):
        """ Query the difference between the X values of cursor A and cursor B (BX - AX) in the manual cursor measurement mode. 
        
        :return: The difference in X values (BX - AX) in scientific notation.
        :rtype: float
        """
        response = self.instrument.query(":CURSor:MANual:XDELta?")
        return float(response)

    def get_manual_ixdelta(self):
        """ 
        Query the reciprocal of the absolute value of the difference between the X values of cursor A and cursor B (1/dX). 
        
        :return: The reciprocal of the difference in X values (1/dX) in scientific notation.
        :rtype: float
        """
        response = self.instrument.query(":CURSor:MANual:IXDELta?")
        return float(response)

    def get_manual_ydelta(self):
        """ Query the difference between the Y values of cursor A and cursor B (BY - AY) in the manual cursor measurement mode. 
        
        :return: The difference in Y values (BY - AY) in scientific notation.
        :rtype: float
        """
        response = self.instrument.query(":CURSor:MANual:YDELta?")
        return float(response)

    def set_track_source(self, source, n):
        """
        Set the channel source of cursor A in the track cursor measurement mode.


        :param source: The source to set for the cursor. Must be one of "OFF", "CHANNEL1", "CHANNEL2", or "MATH".
        :type source: str

        :param n: The cursor A|B.
        :type n: str
        """
        
        valid_sources = ["OFF", "CHANNEL1", "CHANNEL2", "MATH"]
        source = source.upper()
        if source in valid_sources:
            self.instrument.write(f":CURSor:TRACk:SOURce{n} {source}")
        else:
            print(f"Invalid source. Choose from: {valid_sources}")

    def get_track_source(self, cursor):
        """ Query the channel source of cursor A or B in the track cursor measurement mode. 


        :param cursor: Cursor identifier, either "A" or "B".
        :type cursor: str
        :return: The channel source of cursor A or B, such as "CHAN1", "CHAN2", "MATH", etc.
        :rtype: str
        """
        return self.instrument.query(f":CURSor:TRACk:SOURce{n}?")

    def set_xy(self, cursor, x, y):
        """ Set the horizontal position of cursor A or B in the XY cursor measurement mode. 


        :param cursor: Cursor identifier, either "A" or "B".
        :type cursor: str

        :param x: Horizontal position, must be between 5 and 394.
        :type x: int

        :param y: Vertical position, must be between 5 and 394.
        :type y: int
        """
        if 5 <= x <= 394 and 5 <= y <= 394:
            self.instrument.write(f":CURSor:XY:{cursor}X {x};{cursor}Y {y};")
        else:
            print("Invalid x or y position. Must be between 5 and 394.")

    def get_xy(self, cursor):
        """ Query the horizontal position of cursor A in the XY cursor measurement mode.

        :param cursor: Cursor identifier, either "A" or "B".
        :type cursor: str
        :return: The x and y coordinates of the cursor in the format "x;y".
        :rtype: str
        """
        response = self.instrument.query(f":CURSor:XY:{cursor}X?;{cursor}Y?")
        return response  # Returns an integer between 5 and 394
class Decoder:
    """
    The Decoder commands are used to execute decoding settings and operations.
    """
    def __init__(self, instrument,data_handler,n=1):
        """The Decoder class is used to execute decoding settings and operations. The default decoder mode is Parallel.


        :param instrument: The instrument to control.
        :type instrument: pyvisa.Resource

        :param data_handler: The data handler for processing data.
        :type data_handler: DataHandler

        :param n: The decoder number (1 or 2).
        :type n: int
        """
        self.instrument = instrument
        self.data_handler = data_handler

        if n not in [1, 2]:
            raise ValueError("Parameter n must be 1 or 2.")
        self.n = n
        self.uart = self.UART(instrument, data_handler, n)
        self.iic = self.IIC_Decoder(instrument, data_handler, n)
        self.spi = self.SPI_Decoder(instrument, data_handler, n)
        self.parallel = self.Parallel(instrument, data_handler, n)

    def get_current_decoder(self):
        """Query which decoder you are currently using.

        :return: The decoder number (1 or 2).
        :rtype: int
        """
        return self.n
    def switch_decoder(self, n):
        """Set the current decoder number.

        :param n: The decoder number to set (1 or 2).
        :type n: int
        """
        if n in [1, 2]:
            self.n = n
            self.uart.n = n
            self.iic.n = n
            self.spi.n = n
            self.parallel.n = n
        else:
            print("Invalid decoder number. Use 1 or 2.")

    def set_mode(self, mode):
        """
        Set the decoder type.


        :param mode: One of {"PARALLEL", "UART", "SPI", "IIC"}
        :type mode: str
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

        :return: One of {"PAR", "UART", "SPI", "IIC"}
        :rtype: str
        """
        return self.instrument.query(f":DECoder{self.n}:MODE?")

    def enable_display(self, state):
        """
        Turn on or off the decoder display.


        :param state: 1/0 or "ON"/"OFF"
        :type state: int or str
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

        :return: 1 (on) or 0 (off)
        :rtype: int
        """
        return int(self.instrument.query(f":DECoder{self.n}:DISPlay?"))

    def set_format(self, fmt):
        """
        Set the bus display format.


        :param fmt: One of {"HEX", "ASCII", "DEC", "BIN", "LINE"}
        :type fmt: str
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

        :return: Format string
        :rtype: str
        """
        return self.instrument.query(f":DECoder{self.n}:FORMat?")

    def set_position(self, pos):
        """
        Set the vertical position of the bus on the screen.


        :param pos: 50 to 350
        :type pos: int
        """
        if 50 <= pos <= 350:
            self.instrument.write(f":DECoder{self.n}:POSition {pos}")
        else:
            print("Invalid position. Must be between 50 and 350.")

    def get_position(self):
        """
        Query the vertical position of the bus.

        :return: Position value
        :rtype: int
        """
        return int(self.instrument.query(f":DECoder{self.n}:POSition?"))

    def set_threshold_channel(self,  threshold):
        """
        Set the threshold level of the specified analog channel.


        :param channel: 1 or 2
        :type channel: int

        :param threshold: Threshold value
        :type threshold: float
        """
        if self.channel not in [1, 2]:
            print("Invalid channel. Use 1 or 2.")
            return
        self.instrument.write(f":DECoder{self.n}:THREshold:CHANnel{self.channel} {threshold}")

    def get_threshold_channel(self):
        """
        Query the threshold level of the specified analog channel.

        :return: Threshold value
        :rtype: float
        """
        if self.channel not in [1, 2]:
            print("Invalid channel. Use 1 or 2.")
            return None
        return float(self.instrument.query(f":DECoder{self.n}:THREshold:CHANnel{self.channel}?"))

    def set_threshold_auto(self, state):
        """
        Turn on or off the auto threshold function.


        :param state: 1/0 or "ON"/"OFF"
        :type state: int or str
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
        
        :return: 1 (on) or 0 (off)
        :rtype: int
        """
        return int(self.instrument.query(f":DECoder{self.n}:THREshold:AUTO?"))

    def set_config_label(self, state):
        """
        Turn on or off the label display function.

        :param state: 1/0 or "ON"/"OFF"
        :type state: int or str
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
        
        :return: 1 (on) or 0 (off)
        :rtype: int
        """
        return int(self.instrument.query(f":DECoder{self.n}:CONFig:LABel?"))

    def set_config_line(self, state):
        """
        Turn on or off the bus display function.

        :param state: 1/0 or "ON"/"OFF"
        :type state: int or str
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
        
        :return: 1 (on) or 0 (off)
        :rtype: int
        """
        return int(self.instrument.query(f":DECoder{self.n}:CONFig:LINE?"))

    def set_config_format(self, state):
        """
        Turn on or off the format display function.

        :param state: 1/0 or "ON"/"OFF"
        :type state: int or str
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
        
        :return: 1 (on) or 0 (off)
        :rtype: int
        """
        return int(self.instrument.query(f":DECoder{self.n}:CONFig:FORMat?"))

    def set_config_endian(self, state):
        """
        Turn on or off the endian display function in serial bus decoding.

        :param state: 1/0 or "ON"/"OFF"
        :type state: int or str
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
        
        :return: 1 (on) or 0 (off)
        :rtype: int
        """
        return int(self.instrument.query(f":DECoder{self.n}:CONFig:ENDian?"))

    def set_config_width(self, state):
        """
        Turn on or off the width display function.

        :param state: 1/0 or "ON"/"OFF"
        :type state: int or str
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
        
        :return: 1 (on) or 0 (off)
        :rtype: int
        """
        return int(self.instrument.query(f":DECoder{self.n}:CONFig:WIDth?"))

    class UART:
        """
        The UART commands are used to set the RS232 decoding parameters.
        """
        def __init__(self, instrument,data_handler,n):
            """The UART class is used to set the RS232 decoding parameters.
            

            :param instrument: The instrument to control.
            :type instrument: pyvisa.Resource

            :param data_handler: The data handler for processing data.
            :type data_handler: DataHandler"""

            self.instrument = instrument
            self.data_handler = data_handler
            if n not in [1, 2]:
                raise ValueError("Parameter n must be 1 or 2.")
            self.n = n

        def set_tx(self, tx):
            """
            Set the TX channel source of RS232 decoding.

            :param tx: "CHANNEL1", "CHANNEL2", or "OFF"
            :type tx: str
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
            
            :return: "CHAN1", "CHAN2", or "OFF"
            :rtype: str
            """
            return self.instrument.query(f":DECoder{self.n}:UART:TX?")

        def set_rx(self, rx):
            """
            Set the RX channel source of RS232 decoding.

            :param rx: "CHANNEL1", "CHANNEL2", or "OFF"
            :type rx: str
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
            
            :return: "CHAN1", "CHAN2", or "OFF"
            :rtype: str
            """
            return self.instrument.query(f":DECoder{self.n}:UART:RX?")

        def set_polarity(self, polarity):
            """
            Set the polarity of RS232 decoding.

            :param polarity: "NEGATIVE" or "POSITIVE"
            :type polarity: str
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
            
            :return: "NEG" or "POS"
            :rtype: str
            """
            return self.instrument.query(f":DECoder{self.n}:UART:POLarity?")

        def set_endian(self, endian):
            """
            Set the endian of RS232 decoding.

            :param endian: "LSB" or "MSB"
            :type endian: str
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
            
            :return: "LSB" or "MSB"
            :rtype: str
            """
            return self.instrument.query(f":DECoder{self.n}:UART:ENDian?")
        def set_baud(self, baud):
            """
            Set the baud rate of RS232 decoding.

            :param baud: Baud rate, 110 to 20000000
            :type baud: int
            """
            if isinstance(baud, int) and 110 <= baud <= 20000000:
                self.instrument.write(f":DECoder{self.n}:UART:BAUD {baud}")
            else:
                print("Invalid baud rate. Must be integer between 110 and 20000000.")

        def get_baud(self):
            """
            Query the baud rate of RS232 decoding.
            
            :return: Current baud rate
            :rtype: int
            """
            return int(self.instrument.query(f":DECoder{self.n}:UART:BAUD?"))

        def set_width(self, width):
            """
            Set the width of each frame of data in RS232 decoding.

            :param width: Data width, 5 to 8
            :type width: int
            """
            if isinstance(width, int) and 5 <= width <= 8:
                self.instrument.write(f":DECoder{self.n}:UART:WIDTh {width}")
            else:
                print("Invalid width. Must be integer between 5 and 8.")

        def get_width(self):
            """
            Query the width of each frame of data in RS232 decoding.
            
            :return: Data width (5 to 8)
            :rtype: int
            """
            return int(self.instrument.query(f":DECoder{self.n}:UART:WIDTh?"))

        def set_stop(self, stop):
            """
            Set the stop bit after each frame of data in RS232 decoding.

            :param stop: Stop bit, one of 1, 1.5, or 2
            :type stop: float
            """
            allowed = {1, 1.5, 2}
            if stop in allowed:
                self.instrument.write(f":DECoder{self.n}:UART:STOP {stop}")
            else:
                print("Invalid stop bit. Allowed: 1, 1.5, 2.")

        def get_stop(self):
            """
            Query the stop bit after each frame of data in RS232 decoding.
            
            :return: Stop bit (1, 1.5, or 2)
            :rtype: float or str
            """
            resp = self.instrument.query(f":DECoder{self.n}:UART:STOP?")
            try:
                return float(resp)
            except Exception:
                return resp

        def set_parity(self, parity):
            """
            Set the even-odd check mode of the data transmission in RS232 decoding.

            :param parity: "NONE", "EVEN", or "ODD"
            :type parity: str
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
            
            :return: "NONE", "EVEN", or "ODD"
            :rtype: str
            """
            return self.instrument.query(f":DECoder{self.n}:UART:PARity?")

    class IIC_Decoder:
        """
        The IIC commands are used to set the I2C decoding parameters.
        """
        def __init__(self, instrument,data_handler,n):
            """The IIC_Decoder class is used to set the I2C decoding parameters.
            
            :param instrument: The instrument to control.
            :type instrument: pyvisa.Resource
            :param data_handler: The data handler for processing data.
            :type data_handler: DataHandler"""
            self.instrument = instrument
            self.data_handler = data_handler
            if n not in [1, 2]:
                raise ValueError("Parameter n must be 1 or 2.")
            self.n = n

        def set_clk(self, clk):
            """
            Set the signal source of the clock channel in I2C decoding.

            :param clk: "CHANNEL1" or "CHANNEL2"
            :type clk: str
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
            
            :return: "CHAN1" or "CHAN2"
            :rtype: str
            """
            return self.instrument.query(f":DECoder{self.n}:IIC:CLK?")

        def set_data(self, data):
            """
            Set the signal source of the data channel in I2C decoding.

            :param data: "CHANNEL1" or "CHANNEL2"
            :type data: str
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
            
            :return: "CHAN1" or "CHAN2"
            :rtype: str
            """
            return self.instrument.query(f":DECoder{self.n}:IIC:DATA?")

        def set_address(self, addr):
            """
            Set the address mode of I2C decoding.

            :param addr: "NORMAL" or "RW"
            :type addr: str
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
            
            :return: "NORM" or "RW"
            :rtype: str
            """
            return self.instrument.query(f":DECoder{self.n}:IIC:ADDRess?")

    class SPI_Decoder:
        """
        The SPI commands are used to set the SPI decoding parameters.
        """
        def __init__(self, instrument,data_handler,n):
            """The SPI_Decoder class is used to set the SPI decoding parameters.
            
            :param instrument: The instrument to control.
            :type instrument: pyvisa.Resource
            :param data_handler: The data handler for processing data.
            :type data_handler: DataHandler"""
            self.instrument = instrument
            self.data_handler = data_handler
            if n not in [1, 2]:
                raise ValueError("Parameter n must be 1 or 2.")
            self.n = n

        def set_clk(self, clk):
            """
            Set the signal source of the clock channel in SPI decoding.

            :param clk: "CHANNEL1" or "CHANNEL2"
            :type clk: str
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
            
            :return: "CHAN1" or "CHAN2"
            :rtype: str
            """
            return self.instrument.query(f":DECoder{self.n}:SPI:CLK?")

        def set_miso(self, miso):
            """
            Set the MISO channel source in SPI decoding.

            :param miso: "CHANNEL1", "CHANNEL2", or "OFF"
            :type miso: str
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
            
            :return: "CHAN1", "CHAN2", or "OFF"
            :rtype: str
            """
            return self.instrument.query(f":DECoder{self.n}:SPI:MISO?")
        def set_mosi(self, mosi):
            """
            Set the MOSI channel source in SPI decoding.

            :param mosi: "CHANNEL1", "CHANNEL2", or "OFF"
            :type mosi: str
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
            
            :return: "CHAN1", "CHAN2", or "OFF"
            :rtype: str
            """
            return self.instrument.query(f":DECoder{self.n}:SPI:MOSI?")

        def set_cs(self, cs):
            """
            Set the CS channel source in SPI decoding.

            :param cs: "CHANNEL1" or "CHANNEL2"
            :type cs: str
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
            
            :return: "CHAN1" or "CHAN2"
            :rtype: str
            """
            return self.instrument.query(f":DECoder{self.n}:SPI:CS?")

        def set_select(self, csncs):
            """
            Set the CS polarity in SPI decoding.

            :param csncs: "NCS" or "CS"
            :type csncs: str
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
            
            :return: "NCS" or "CS"
            :rtype: str
            """
            return self.instrument.query(f":DECoder{self.n}:SPI:SELect?")

        def set_mode(self, mode):
            """
            Set the frame synchronization mode of SPI decoding.

            :param mode: "CS" or "TIMEOUT"
            :type mode: str
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
            
            :return: "CS" or "TIM"
            :rtype: str
            """
            return self.instrument.query(f":DECoder{self.n}:SPI:MODE?")

        def set_timeout(self, tmo):
            """
            Set the timeout time in the timeout mode of SPI decoding.

            :param tmo: Timeout time in seconds (e.g., 1e-6)
            :type tmo: float
            """
            if isinstance(tmo, (float, int)) and tmo > 0:
                self.instrument.write(f":DECoder{self.n}:SPI:TIMeout {tmo}")
            else:
                print("Invalid timeout value. Must be a positive number.")

        def get_timeout(self):
            """
            Query the timeout time in the timeout mode of SPI decoding.
            
            :return: Timeout time in seconds
            :rtype: float or str
            """
            resp = self.instrument.query(f":DECoder{self.n}:SPI:TIMeout?")
            try:
                return float(resp)
            except Exception:
                return resp

        def set_polarity(self, pol):
            """
            Set the polarity of the SDA data line in SPI decoding.

            :param pol: "NEGATIVE" or "POSITIVE"
            :type pol: str
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
            
            :return: "NEG" or "POS"
            :rtype: str
            """
            return self.instrument.query(f":DECoder{self.n}:SPI:POLarity?")

        def set_edge(self, edge):
            """
            Set the clock type when the instrument samples the data line in SPI decoding.

            :param edge: "RISE" or "FALL"
            :type edge: str
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
            
            :return: "RISE" or "FALL"
            :rtype: str
            """
            return self.instrument.query(f":DECoder{self.n}:SPI:EDGE?")

        def set_endian(self, endian):
            """
            Set the endian of the SPI decoding data.

            :param endian: "LSB" or "MSB"
            :type endian: str
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
            
            :return: "LSB" or "MSB"
            :rtype: str
            """
            return self.instrument.query(f":DECoder{self.n}:SPI:ENDian?")

        def set_width(self, wid):
            """
            Set the number of bits of each frame of data in SPI decoding.

            :param wid: Data width, 4 to 32
            :type wid: int
            """
            if isinstance(wid, int) and 4 <= wid <= 32:
                self.instrument.write(f":DECoder{self.n}:SPI:WIDTh {wid}")
            else:
                print("Invalid width. Must be integer between 4 and 32.")

        def get_width(self):
            """
            Query the number of bits of each frame of data in SPI decoding.
            
            :return: Data width (4 to 32)
            :rtype: int
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
            """The Parallel class is used to set the parallel decoding parameters.
            
            :param instrument: The instrument to control.
            :type instrument: pyvisa.Resource
            :param data_handler: The data handler for processing data.
            :type data_handler: DataHandler
            :param n: Decoder number (1 or 2)
            :type n: int"""

            self.instrument = instrument
            self.data_handler = data_handler
            if n not in [1, 2]:
                raise ValueError("Parameter n must be 1 or 2.")
            self.n = n

        def set_clk(self, clk):
            """
            Set the CLK channel source of parallel decoding.

            :param clk: "CHANNEL1", "CHANNEL2", or "OFF"
            :type clk: str
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
            
            :return: "CHAN1", "CHAN2", or "OFF"
            :rtype: str
            """
            return self.instrument.query(f":DECoder{self.n}:PARallel:CLK?")

        def set_edge(self, edge):
            """
            Set the edge type of the clock channel for parallel decoding.

            :param edge: "RISE", "FALL", or "BOTH"
            :type edge: str
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
            
            :return: "RISE", "FALL", or "BOTH"
            :rtype: str
            """
            return self.instrument.query(f":DECoder{self.n}:PARallel:EDGE?")

        def set_width(self, wid):
            """
            Set the data width (number of bits per frame) for parallel decoding.

            :param wid: Data width, 1 to 2
            :type wid: int
            """
            if isinstance(wid, int) and 1 <= wid <= 2:
                self.instrument.write(f":DECoder{self.n}:PARallel:WIDTh {wid}")
            else:
                print("Invalid width. Must be integer between 1 and 2.")

        def get_width(self):
            """
            Query the data width for parallel decoding.
            
            :return: Data width (1 to 2)
            :rtype: int
            """
            resp = self.instrument.query(f":DECoder{self.n}:PARallel:WIDTh?")
            try:
                return int(resp)
            except Exception:
                return resp

        def set_bitx(self, bit):
            """
            Set the data bit that requires a channel source on the parallel bus.

            :param bit: Bit index, 0 to (data width - 1)
            :type bit: int
            """
            if isinstance(bit, int) and bit >= 0:
                self.instrument.write(f":DECoder{self.n}:PARallel:BITX {bit}")
            else:
                print("Invalid bit index.")

        def get_bitx(self):
            """
            Query the current data bit selected on the parallel bus.
            
            :return: Current bit index
            :rtype: int
            """
            resp = self.instrument.query(f":DECoder{self.n}:PARallel:BITX?")
            try:
                return int(resp)
            except Exception:
                return resp

        def set_source(self, src):
            """
            Set the channel source of the data bit currently selected.

            :param src: "CHANNEL1" or "CHANNEL2"
            :type src: str
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
            
            :return: "CHAN1" or "CHAN2"
            :rtype: str
            """
            return self.instrument.query(f":DECoder{self.n}:PARallel:SOURce?")

        def set_polarity(self, pol):
            """
            Set the data polarity of parallel decoding.

            :param pol: "NEGATIVE" or "POSITIVE"
            :type pol: str
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
            
            :return: "NEG" or "POS"
            :rtype: str
            """
            return self.instrument.query(f":DECoder{self.n}:PARallel:POLarity?")

        def enable_noise_rejection(self, enable):
            """
            Turn on or off the noise rejection function of parallel decoding.

            :param enable: 1/0 or "ON"/"OFF"
            :type enable: int or str
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
            
            :return: 1 (on) or 0 (off)
            :rtype: int
            """
            return int(self.instrument.query(f":DECoder{self.n}:PARallel:NREJect?"))

        def set_noise_rejection_time(self, time):
            """
            Set the noise rejection time of parallel decoding (in seconds).

            :param time: 0.00s to 0.1s (100ms)
            :type time: float
            """
            if isinstance(time, (float, int)) and 0.0 <= time <= 0.1:
                self.instrument.write(f":DECoder{self.n}:PARallel:NRTime {time}")
            else:
                print("Invalid time. Must be between 0.00 and 0.1 seconds.")

        def get_noise_rejection_time(self):
            """
            Query the noise rejection time of parallel decoding.
            
            :return: Noise rejection time in seconds
            :rtype: float or str
            """
            resp = self.instrument.query(f":DECoder{self.n}:PARallel:NRTime?")
            try:
                return float(resp)
            except Exception:
                return resp

        def set_compensation(self, comp):
            """
            Set the clock compensation time of parallel decoding (in seconds).

            :param comp: -0.1s to 0.1s (-100ms to 100ms)
            :type comp: float
            """
            if isinstance(comp, (float, int)) and -0.1 <= comp <= 0.1:
                self.instrument.write(f":DECoder{self.n}:PARallel:CCOMpensation {comp}")
            else:
                print("Invalid compensation. Must be between -0.1 and 0.1 seconds.")

        def get_compensation(self):
            """
            Query the clock compensation time of parallel decoding.
            
            :return: Compensation time in seconds
            :rtype: float or str
            """
            resp = self.instrument.query(f":DECoder{self.n}:PARallel:CCOMpensation?")
            try:
                return float(resp)
            except Exception:
                return resp

        def enable_plot(self, enable):
            """
            Turn on or off the curve function of parallel decoding.
            

            :param enable: 1/0 or "ON"/"OFF"
            :type enable: int or str
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
            
            :return: 1 (on) or 0 (off)
            :rtype: int
            """
            return int(self.instrument.query(f":DECoder{self.n}:PARallel:PLOT?"))



class Display:
    """
    The Display commands are used to set the waveform display mode, persistence time, waveform intensity, screen grid type and grid brightness.
    """
    def __init__(self, instrument,data_handler):
            """The Display class is used to set the waveform display mode, persistence time, waveform intensity, screen grid type and grid brightness.
            
            :param instrument: The instrument to control.
            :type instrument: pyvisa.Resource
            :param data_handler: The data handler for processing data.
            :type data_handler: DataHandler"""
            self.instrument = instrument
            self.data_handler = data_handler

    def clear(self):
        """
        Clear all the waveforms on the screen.
        """
        self.instrument.write(":DISPlay:CLEar")

    def get_data(self, color=None, invert=None, fmt=None):
        """
        Read the data stream of the image currently displayed on the screen. If autosave is on, then also saves them to a png file.
        
        :param color: "ON" or "OFF" (default ON)
        :param invert: 1/"ON" or 0/"OFF" (default 0)
        :param fmt: "BMP24", "BMP8", "PNG", "JPEG", "TIFF" (default BMP24)
            
        :return: Raw image data (TMC header included)
        :rtype Image: If auto save enabled, return PIL Image object, if not set to save return None
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
        
        :param disp_type: Allowed values depend on instrument, e.g., "VECTor", "DOTS"
        :type disp_type: str
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
        
        :return: Display type
        :rtype: str
        """
        return self.instrument.query(":DISPlay:TYPE?")

    def set_grading_time(self, time):
        """
        Set the persistence time of the waveform.
        
        :param time: Persistence time in seconds
        :type time: float
        """
        if isinstance(time, (float, int)) and time >= 0:
            self.instrument.write(f":DISPlay:GRADing:TIME {time}")
        else:
            print("Invalid time. Must be a non-negative number.")

    def get_grading_time(self):
        """
        Query the persistence time of the waveform.
        
        :return: Persistence time in seconds
        :rtype: float or str
        """
        resp = self.instrument.query(":DISPlay:GRADing:TIME?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_waveform_brightness(self, val):
        """
        Set the waveform intensity.
        
        :param val: 0 to 100
        :type val: int
        """
        if isinstance(val, int) and 0 <= val <= 100:
            self.instrument.write(f":DISPlay:WBRightness {val}")
        else:
            print("Invalid brightness. Must be integer between 0 and 100.")

    def get_waveform_brightness(self):
        """
        Query the waveform intensity.
        
        :return: Brightness (0 to 100)
        :rtype: int or str
        """
        resp = self.instrument.query(":DISPlay:WBRightness?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_grid(self, grid_type):
        """
        Set the screen grid type.
        
        :param grid_type: "FULL", "HALF", "NONE"
        :type grid_type: str
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
        
        :return: Grid type
        :rtype: str
        """
        return self.instrument.query(":DISPlay:GRID?")

    def set_grid_brightness(self, val):
        """
        Set the grid brightness.
        
        :param val: 0 to 100
        :type val: int
        """
        if isinstance(val, int) and 0 <= val <= 100:
            self.instrument.write(f":DISPlay:GBRightness {val}")
        else:
            print("Invalid grid brightness. Must be integer between 0 and 100.")

    def get_grid_brightness(self):
        """
        Query the grid brightness.
        
        :return: Grid brightness (0 to 100)
        :rtype: int or str
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
        """The ETable class is used to set the parameters related to the decoding event table.
        
        :param instrument: The instrument to control.
        :type instrument: pyvisa.Resource
        :param data_handler: The data handler for processing data.
        :type data_handler: DataHandler"""
        self.instrument = instrument
        self.data_handler = data_handler
        if n not in [1, 2]:
            raise ValueError("Parameter n must be 1 or 2.")
        self.n = n

    def set_disp(self, state):
        """
        Turn on or off the decoding event table.
        
        :param state: 1/0 or "ON"/"OFF"
        :type state: int or str
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
        
        :return: 1 (on) or 0 (off)
        :rtype: int
        """
        return int(self.instrument.query(f":ETABle{self.n}:DISP?"))

    def set_format(self, fmt):
        """
        Set the data display format of the event table.
        
        :param fmt: "HEX", "ASCII", or "DEC"
        :type fmt: str
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
        
        :return: "HEX", "ASC", or "DEC"
        :rtype: str
        """
        return self.instrument.query(f":ETABle{self.n}:FORMat?")

    def set_view(self, view):
        """
        Set the display mode of the event table.
        
        :param view: "PACKAGE", "DETAIL", or "PAYLOAD"
        :type view: str
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
        
        :return: "PACK", "DET", or "PAYL"
        :rtype: str
        """
        return self.instrument.query(f":ETABle{self.n}:VIEW?")

    def set_column(self, col):
        """
        Set the current column of the event table.
        
        :param col: "DATA", "TX", "RX", "MISO", or "MOSI"
        :type col: str
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
        
        :return: "DATA", "TX", "RX", "MISO", or "MOSI"
        :rtype: str
        """
        return self.instrument.query(f":ETABle{self.n}:COLumn?")

    def set_row(self, row):
        """
        Set the current row of the event table.
        
        :param row: Row number (1 to max rows)
        :type row: int
        """
        if isinstance(row, int) and row >= 1:
            self.instrument.write(f":ETABle{self.n}:ROW {row}")
        else:
            print("Invalid row. Must be integer >= 1.")

    def get_row(self):
        """
        Query the current row of the event table.
        
        :return: Current row, or 0 if table is empty
        :rtype: int or str
        """
        resp = self.instrument.query(f":ETABle{self.n}:ROW?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_sort(self, sort):
        """
        Set the display type of the decoding results in the event table.
        
        :param sort: "ASCEND" or "DESCEND"
        :type sort: str
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
        
        :return: "ASC" or "DESC"
        :rtype: str
        """
        return self.instrument.query(f":ETABle{self.n}:SORT?")

    def get_data(self):
        """
        Read the current event table data. If auto save is on, then also saves them to a csv file.
        
        :return: Raw event table data (TMC header included)
        :rtype: bytes
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
        """The Function class is used to set the waveform recording and playback parameters.
        
        :param instrument: The instrument to control.
        :type instrument: pyvisa.Resource
        :param data_handler: The data handler for processing data.
        :type data_handler: DataHandler"""

        self.instrument = instrument
        self.data_handler = data_handler
        self.WRecord = self.WRecord(instrument, data_handler)
        self.WReplay = self.WReplay(instrument, data_handler)

    class WRecord:
        """Waveform Record commands."""
        def __init__(self, instrument,data_handler):
            """Initialize WRecord class.
            
            :param instrument: The instrument to control.
            :type instrument: pyvisa.Resource
            :param data_handler: The data handler for processing data.
            :type data_handler: DataHandler"""

            self.instrument = instrument
            self.data_handler = data_handler
        def set_wrecord_fend(self, frame):
            """
            Set the end frame of waveform recording.
            
            :param frame: 1 to max frames (use get_wrecord_fmax to query max)
            :type frame: int
            """
            if isinstance(frame, int) and frame >= 1:
                self.instrument.write(f":FUNCtion:WRECord:FEND {frame}")
            else:
                print("Invalid frame value.")

        def get_wrecord_fend(self):
            """
            Query the end frame of waveform recording.
            
            :return: Current end frame
            :rtype: int or str
            """
            resp = self.instrument.query(":FUNCtion:WRECord:FEND?")
            try:
                return int(resp)
            except Exception:
                return resp

        def get_wrecord_fmax(self):
            """
            Query the maximum number of frames that can be recorded currently.
            
            :return: Maximum number of frames
            :rtype: int or str
            """
            resp = self.instrument.query(":FUNCtion:WRECord:FMAX?")
            try:
                return int(resp)
            except Exception:
                return resp

        def set_wrecord_finterval(self, interval):
            """
            Set the time interval between frames in waveform recording.
            
            :param interval: 100e-9 to 10.0 (seconds)
            :type interval: float
            """
            if isinstance(interval, (float, int)) and 1e-7 <= interval <= 10.0:
                self.instrument.write(f":FUNCtion:WRECord:FINTerval {interval}")
            else:
                print("Invalid interval. Must be between 100ns and 10s.")

        def get_wrecord_finterval(self):
            """
            Query the time interval between frames in waveform recording.
            
            :return: Time interval in seconds
            :rtype: float or str
            """
            resp = self.instrument.query(":FUNCtion:WRECord:FINTerval?")
            try:
                return float(resp)
            except Exception:
                return resp

        def set_wrecord_prompt(self, state):
            """
            Turn on or off the sound prompt when recording finishes.
            
            :param state: 1/0 or "ON"/"OFF"
            :type state: int or str

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
            
            :return: 1 (on) or 0 (off)
            :rtype: int or str
            """
            resp = self.instrument.query(":FUNCtion:WRECord:PROMpt?")
            try:
                return int(resp)
            except Exception:
                return resp

        def set_wrecord_operate(self, opt):
            """
            Start or stop the waveform recording.
            
            :param opt: "RUN" or "STOP"
            :type opt: str
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
            
            :return: "RUN" or "STOP"
            :rtype: str
            """
            return self.instrument.query(":FUNCtion:WRECord:OPERate?")

        def set_wrecord_enable(self, state):
            """
            Turn on or off the waveform recording function.
            
            :param state: 1/0 or "ON"/"OFF"
            :type state: int or str
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

            :return: 1 (on) or 0 (off)
            :rtype: int or str
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
            
            :param frame: 1 to max frames recorded
            :type frame: int
            """
            if isinstance(frame, int) and frame >= 1:
                self.instrument.write(f":FUNCtion:WREPlay:FSTart {frame}")
            else:
                print("Invalid frame value.")

        def get_wreplay_fstart(self):
            """
            Query the start frame of waveform playback.
            
            :return: Start frame
            :rtype: int or str
            """
            resp = self.instrument.query(":FUNCtion:WREPlay:FSTart?")
            try:
                return int(resp)
            except Exception:
                return resp

        def set_wreplay_fend(self, frame):
            """
            Set the end frame of waveform playback.
            
            :param frame: 1 to max frames recorded
            :type frame: int
            """
            if isinstance(frame, int) and frame >= 1:
                self.instrument.write(f":FUNCtion:WREPlay:FEND {frame}")
            else:
                print("Invalid frame value.")

        def get_wreplay_fend(self):
            """
            Query the end frame of waveform playback.
            
            :return: End frame
            :rtype: int or str
            """
            resp = self.instrument.query(":FUNCtion:WREPlay:FEND?")
            try:
                return int(resp)
            except Exception:
                return resp

        def get_wreplay_fmax(self):
            """
            Query the maximum number of frames that can be played (max frames recorded).
            
            :return: Maximum number of frames
            :rtype: int or str
            """
            resp = self.instrument.query(":FUNCtion:WREPlay:FMAX?")
            try:
                return int(resp)
            except Exception:
                return resp

        def set_wreplay_finterval(self, interval):
            """
            Set the time interval between frames in waveform playback.
            
            :param interval: 100e-9 to 10.0 (seconds)
            :type interval: float
            """
            if isinstance(interval, (float, int)) and 1e-7 <= interval <= 10.0:
                self.instrument.write(f":FUNCtion:WREPlay:FINTerval {interval}")
            else:
                print("Invalid interval. Must be between 100ns and 10s.")

        def get_wreplay_finterval(self):
            """
            Query the time interval between frames in waveform playback.
            
            :return: Time interval in seconds
            :rtype: float or str
            """
            resp = self.instrument.query(":FUNCtion:WREPlay:FINTerval?")
            try:
                return float(resp)
            except Exception:
                return resp

        def set_wreplay_mode(self, mode):
            """
            Set the waveform playback mode.
            
            :param mode: "REPEAT" or "SINGLE"
            :type mode: str
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
            
            :return: "REP" or "SING"
            :rtype: str
            """
            return self.instrument.query(":FUNCtion:WREPlay:MODE?")

        def set_wreplay_direction(self, direction):
            """
            Set the waveform playback direction.
            
            :param direction: "FORWARD" or "BACKWARD"
            :type direction: str
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
            
            :return: "FORW" or "BACK"
            :rtype: str
            """
            return self.instrument.query(":FUNCtion:WREPlay:DIRection?")

        def set_wreplay_operate(self, opt):
            """
            Start, pause, or stop the waveform playback.
            
            :param opt: "PLAY", "PAUSE", or "STOP"
            :type opt: str
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
            
            :return: "PLAY", "PAUS", or "STOP"
            :rtype: str
            """
            return self.instrument.query(":FUNCtion:WREPlay:OPERate?")

        def set_wreplay_fcurrent(self, frame):
            """
            Set the current frame in waveform playback.
            
            :param frame: 1 to max frames recorded
            :type frame: int
            """
            if isinstance(frame, int) and frame >= 1:
                self.instrument.write(f":FUNCtion:WREPlay:FCURrent {frame}")
            else:
                print("Invalid frame value.")

        def get_wreplay_fcurrent(self):
            """
            Query the current frame in waveform playback.
            
            :return: Current frame
            :rtype: int or str
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
        """The LAN class is used to set/query network parameters.
        
        :param instrument: The instrument to control.
        :type instrument: pyvisa.Resource
        :param data_handler: The data handler for processing data.
        :type data_handler: DataHandler"""
        self.instrument = instrument
        self.data_handler = data_handler

    def set_dhcp(self, state):
        """
        Turn on or off the DHCP configuration mode.
        
        :param state: 1/0 or "ON"/"OFF"
        :type state: int or str
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
        
        :return: 1 (on) or 0 (off)
        :rtype: int
        """
        resp = self.instrument.query(":LAN:DHCP?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_autoip(self, state):
        """
        Turn on or off the Auto IP configuration mode.
        
        :param state: 1/0 or "ON"/"OFF"
        :type state: int or str
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

        :return: 1 (on) or 0 (off)
        :rtype: int
        """
        resp = self.instrument.query(":LAN:AUT?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_gateway(self, gateway):
        """
        Set the default gateway.
        
        :param gateway: IP address in nnn,nnn,nnn,nnn format
        :type gateway: str
        """
        self.instrument.write(f":LAN:GATeway {gateway}")

    def get_gateway(self):
        """
        Query the default gateway.
        
        :return: Current gateway
        :rtype: str
        """
        return self.instrument.query(":LAN:GATeway?")

    def set_dns(self, dns):
        """
        Set the DNS address.
        
        :param dns: IP address in nnn,nnn,nnn,nnn format
        :type dns: str
        """
        self.instrument.write(f":LAN:DNS {dns}")

    def get_dns(self):
        """
        Query the DNS address.

        :return: Current DNS address
        :rtype: str
        """
        return self.instrument.query(":LAN:DNS?")

    def get_mac(self):
        """
        Query the MAC address of the instrument.
        
        :return: MAC address
        :rtype: str
        """
        return self.instrument.query(":LAN:MAC?")

    def set_manual(self, state):
        """
        Turn on or off the static IP configuration mode.
        
        :param state: 1/0 or "ON"/"OFF"
        :type state: int or str
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

        :return: 1 (on) or 0 (off)
        :rtype: int
        """
        resp = self.instrument.query(":LAN:MANual?")
        try:
            return int(resp)
        except Exception:
            return resp

    def initiate(self):
        """
        Initiate the network parameters.
        """
        self.instrument.write(":LAN:INITiate")

    def set_ipaddress(self, ip):
        """
        Set the IP address of the instrument.
        
        :param ip: IP address in nnn,nnn,nnn,nnn format
        :type ip: str

        """
        self.instrument.write(f":LAN:IPADdress {ip}")

    def get_ipaddress(self):
        """
        Query the IP address of the instrument.
        
        :return: Current IP address
        :rtype: str
        """
        return self.instrument.query(":LAN:IPADdress?")

    def set_smask(self, mask):
        """
        Set the subnet mask.
        
        :param mask: Subnet mask in nnn,nnn,nnn,nnn format
        :type mask: str

        """
        self.instrument.write(f":LAN:SMASk {mask}")

    def get_smask(self):
        """
        Query the subnet mask.
        
        :return: Current subnet mask
        :rtype: str
        """
        return self.instrument.query(":LAN:SMASk?")

    def get_status(self):
        """
        Query the current network configuration status.
        
        
        :return: One of "UNLINK", "INIT", "IPCONFLICT", "CONFIGURED", "DHCPFAILED"
        :rtype: str
        """
        return self.instrument.query(":LAN:STATus?")

    def get_visa(self):
        """
        Query the VISA address of the instrument.
        

        
        :return: VISA address
        :rtype: str
        """
        return self.instrument.query(":LAN:VISA?")

    def apply(self):
        """
        Apply the network configuration.
        
        """
        self.instrument.write(":LAN:APPLy")

class Math:
    """
    The Math commands are used to set the operations between the waveforms of multiple channels.
    """
    def __init__(self, instrument,data_handler):
        """The Math class is used to set the operations between the waveforms of multiple channels.
        
        :param instrument: The instrument to control.
        :type instrument: pyvisa.Resource
        :param data_handler: The data handler for processing data.
        :type data_handler: DataHandler"""
        self.instrument = instrument
        self.data_handler = data_handler

    def set_display(self, state):
        """
        Turn on or off the math waveform display.
        
        :param state: 1/0 or "ON"/"OFF"
        :type state: int or str
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
        
        :return: 1 (on) or 0 (off)
        :rtype: int
        """
        resp = self.instrument.query(":MATH:DISPlay?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_operator(self, op):
        """
        Set the math operation type.
        
        :param op: Allowed values include "ADD", "SUB", "MUL", "DIV", "FFT", "AND", "OR", "XOR", "NOT", "INTG", "DIFF", "SQRT", "LG", "LN", "EXP", "ABS", "LPF", "HPF", "BPF", "BSF"
        :type op: str

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
        
        :return: Operator
        :rtype: str
        """
        return self.instrument.query(":MATH:OPERator?")

    def set_source1(self, src):
        """
        Set the source 1 for the math operation.
        
        :param src: "CHAN1", "CHAN2", "FX", etc.
        :type src: str

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
        

        
        :return: Source 1
        :rtype: str
        """
        return self.instrument.query(":MATH:SOURce1?")

    def set_source2(self, src):
        """
        Set the source 2 for the math operation.
        
        :param src: "CHAN1", "CHAN2", "FX", etc.
        :type src: str
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
        
        :return: Source 2
        :rtype: str
        """
        return self.instrument.query(":MATH:SOURce2?")

    def set_scale(self, scale):
        """
        Set the vertical scale of the math waveform.
        
        :param scale: Vertical scale in V/div
        :type scale: float

        """
        self.instrument.write(f":MATH:SCALe {scale}")

    def get_scale(self):
        """
        Query the vertical scale of the math waveform.
        
        :return: Vertical scale in V/div
        :rtype: float or str
        """
        resp = self.instrument.query(":MATH:SCALe?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_offset(self, offset):
        """
        Set the vertical offset of the math waveform.
        
        :param offset: Vertical offset in V
        :type offset: float
        """
        self.instrument.write(f":MATH:OFFSet {offset}")

    def get_offset(self):
        """
        Query the vertical offset of the math waveform.
        
        :return: Vertical offset in V
        :rtype: float or str
        """
        resp = self.instrument.query(":MATH:OFFSet?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_invert(self, state):
        """
        Enable or disable math waveform inversion.
        
        :param state: 1/0 or "ON"/"OFF"
        :type state: int or str
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
        
        :return: 1 (on) or 0 (off)
        :rtype: int
        """
        resp = self.instrument.query(":MATH:INVert?")
        try:
            return int(resp)
        except Exception:
            return resp

    def reset(self):
        """
        Reset the math operation settings to default.
        """
        self.instrument.write(":MATH:RESet")
    def set_fft_source(self, src):
        """
        Set the source of FFT operation/filter.
        
        :param src: "CHANnel1" or "CHANnel2"
        :type src: str

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
   
        :return: "CHAN1" or "CHAN2"
        :rtype: str
        """
        return self.instrument.query(":MATH:FFT:SOURce?")

    def set_fft_window(self, wnd):
        """
        Set the window function of the FFT operation.
        
        :param wnd: One of {"RECTangle", "BLACkman", "HANNing", "HAMMing", "FLATtop", "TRIangle"}
        :type wnd: str
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
        
        :return: "RECT", "BLAC", "HANN", "HAMM", "FLAT", or "TRI"
        :rtype: str
        """
        return self.instrument.query(":MATH:FFT:WINDow?")

    def enable_fft_split(self, enable):
        """
        Enable or disable the half-screen display mode of the FFT operation.
        
        :param enable: 1/0 or "ON"/"OFF"
        :type enable: int or str

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
        
        :return: 1 (enabled) or 0 (disabled)
        :rtype: int
        """
        resp = self.instrument.query(":MATH:FFT:SPLit?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_fft_unit(self, unit):
        """
        Set the vertical unit of the FFT operation result.
        
        :param unit: "VRMS" or "DB"
        :type unit: str
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
          
        :return: "VRMS" or "DB"
        :rtype: str 
        """
        return self.instrument.query(":MATH:FFT:UNIT?")

    def set_fft_hscale(self, hsc):
        """
        Set the horizontal scale of the FFT operation result (Hz).
        
        :param hsc: Horizontal scale in Hz
        :type hsc: float

        """
        self.instrument.write(f":MATH:FFT:HSCale {hsc}")

    def get_fft_hscale(self):
        """
        Query the horizontal scale of the FFT operation result (Hz).
        
        :return: Horizontal scale in Hz
        :rtype: float or str
        """
        resp = self.instrument.query(":MATH:FFT:HSCale?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_fft_hcenter(self, cent):
        """
        Set the center frequency of the FFT operation result (Hz).
        
        :param cent: Center frequency in Hz
        :type cent: float
        """
        self.instrument.write(f":MATH:FFT:HCENter {cent}")

    def get_fft_hcenter(self):
        """
        Query the center frequency of the FFT operation result (Hz).
        
        :return: Center frequency in Hz
        :rtype: float or str
        """
        resp = self.instrument.query(":MATH:FFT:HCENter?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_fft_mode(self, mode):
        """
        Set the FFT mode.
        
        :param mode: "TRACe" or "MEMory"
        :type mode: str

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
         
        :return: "TRAC" or "MEM"
        :rtype: str
        """
        return self.instrument.query(":MATH:FFT:MODE?")

    def set_filter_type(self, ftype):
        """
        Set the filter type for math filter operation.
        
        :param ftype: "LPASs", "HPASs", "BPASs", or "BSTOP"
        :type ftype: str

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
        
        :return: "LPAS", "HPAS", "BPAS", or "BSTO"
        :rtype: str
        """
        return self.instrument.query(":MATH:FILTer:TYPE?")

    def set_filter_w1(self, freq1):
        """
        Set the cutoff frequency 1 (ωc1) for filter operation (Hz).
        
        :param freq1: Cutoff frequency 1 in Hz
        :type freq1: float

        """
        self.instrument.write(f":MATH:FILTer:W1 {freq1}")

    def get_filter_w1(self):
        """
        Query the cutoff frequency 1 (ωc1) for filter operation (Hz).
        
        :return: Cutoff frequency 1 in Hz
        :rtype: float or str
        """
        resp = self.instrument.query(":MATH:FILTer:W1?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_filter_w2(self, freq2):
        """
        Set the cutoff frequency 2 (ωc2) for filter operation (Hz).
        
        :param freq2: Cutoff frequency 2 in Hz
        :type freq2: float

        """
        self.instrument.write(f":MATH:FILTer:W2 {freq2}")

    def get_filter_w2(self):
        """
        Query the cutoff frequency 2 (ωc2) for filter operation (Hz).
        
        :return: Cutoff frequency 2 in Hz
        :rtype: float or str
        """
        resp = self.instrument.query(":MATH:FILTer:W2?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_option_start(self, sta):
        """
        Set the start point of the waveform math operation.
        
        :param sta: Start point (0 to end-1)
        :type sta: int
        """
        self.instrument.write(f":MATH:OPTion:STARt {sta}")

    def get_option_start(self):
        """
        Query the start point of the waveform math operation.
        
        :return: Start point
        :rtype: int
        """
        resp = self.instrument.query(":MATH:OPTion:STARt?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_option_end(self, end):
        """
        Set the end point of the waveform math operation.
        
        :param end: End point (start+1 to 1199)
        :type end: int
        """
        self.instrument.write(f":MATH:OPTion:END {end}")

    def get_option_end(self):
        """
        Query the end point of the waveform math operation.

        :return: End point
        :rtype: int
        """
        resp = self.instrument.query(":MATH:OPTion:END?")
        try:
            return int(resp)
        except Exception:
            return resp

    def enable_option_invert(self, enable):
        """
        Enable or disable the inverted display mode of the operation result.
        
        :param enable: 1/0 or "ON"/"OFF"
        :type enable: int or str

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
        
        :return: 1 (enabled) or 0 (disabled)
        :rtype: int
        """
        resp = self.instrument.query(":MATH:OPTion:INVert?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_option_sensitivity(self, sens):
        """
        Set the sensitivity of the logic operation.
        
        :param sens: Sensitivity (0 to 0.96, step 0.08)
        :type sens: float

        """
        self.instrument.write(f":MATH:OPTion:SENSitivity {sens}")

    def get_option_sensitivity(self):
        """
        Query the sensitivity of the logic operation.
        
        :return: Sensitivity
        :rtype: float or str
        """
        resp = self.instrument.query(":MATH:OPTion:SENSitivity?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_option_distance(self, dist):
        """
        Set the smoothing window width of differential operation.
        
        :param dist: Window width (3 to 201)
        :type dist: int

        """
        self.instrument.write(f":MATH:OPTion:DIStance {dist}")

    def get_option_distance(self):
        """
        Query the smoothing window width of differential operation.
        
        :return: Window width
        :rtype: int
        """
        resp = self.instrument.query(":MATH:OPTion:DIStance?")
        try:
            return int(resp)
        except Exception:
            return resp

    def enable_option_ascale(self, enable):
        """
        Enable or disable the auto scale setting of the operation result.
        
        :param enable: 1/0 or "ON"/"OFF"
        :type enable: int or str

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
        
        :return: 1 (enabled) or 0 (disabled)
        :rtype: int
        """
        resp = self.instrument.query(":MATH:OPTion:ASCale?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_option_threshold1(self, thre):
        """
        Set the threshold level of source A in logic operations.
        
        :param thre: Threshold level in V
        :type thre: float

        """
        self.instrument.write(f":MATH:OPTion:THReshold1 {thre}")

    def get_option_threshold1(self):
        """
        Query the threshold level of source A in logic operations.
        
        :return: Threshold level in V
        :rtype: float or str
        """
        resp = self.instrument.query(":MATH:OPTion:THReshold1?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_option_threshold2(self, thre):
        """
        Set the threshold level of source B in logic operations.
        
        :param thre: Threshold level in V
        :type thre: float

        """
        self.instrument.write(f":MATH:OPTion:THReshold2 {thre}")

    def get_option_threshold2(self):
        """
        Query the threshold level of source B in logic operations.
        
        :return: Threshold level in V
        :rtype: float or str
        """
        resp = self.instrument.query(":MATH:OPTion:THReshold2?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_option_fx_source1(self, src):
        """
        Set source A of the inner layer operation of compound operation.
        
        :param src: "CHANnel1" or "CHANnel2"
        :type src: str

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
        
        :return: "CHAN1" or "CHAN2"
        :rtype: str
        """
        return self.instrument.query(":MATH:OPTion:FX:SOURce1?")

    def set_option_fx_source2(self, src):
        """
        Set source B of the inner layer operation of compound operation.
        
        :param src: "CHANnel1" or "CHANnel2"
        :type src: str

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
        
        :return: "CHAN1" or "CHAN2"
        :rtype: str
        """
        return self.instrument.query(":MATH:OPTion:FX:SOURce2?")

    def set_option_fx_operator(self, op):
        """
        Set the operator of the inner layer operation of compound operation.
        
        :param op: "ADD", "SUBTract", "MULTiply", or "DIVision"
        :type op: str

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
        
        :return: "ADD", "SUBT", "MULT", or "DIV"
        :rtype: str
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
        
        :param state: 1/0 or "ON"/"OFF"
        :type state: int or str

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
        
        :return: 1 (enabled) or 0 (disabled)
        :rtype: int
        """
        resp = self.instrument.query(":MASK:ENABle?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_source(self, source):
        """
        Set the source of the pass/fail test.
        
        :param source: "CHANnel1" or "CHANnel2"
        :type source: str

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
        
        :return: "CHAN1" or "CHAN2"
        :rtype: str
        """
        return self.instrument.query(":MASK:SOURce?")

    def operate(self, oper):
        """
        Run or stop the pass/fail test.
        
        :param oper: "RUN" or "STOP"
        :type oper: str

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
        
        :return: "RUN" or "STOP"
        :rtype: str
        """
        return self.instrument.query(":MASK:OPERate?")

    def enable_display(self, state):
        """
        Enable or disable the statistic information when the pass/fail test is enabled.
        
        :param state: 1/0 or "ON"/"OFF"
        :type state: int or str

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
       
        :return: 1 (enabled) or 0 (disabled)
        :rtype: int
        """
        resp = self.instrument.query(":MASK:MDISplay?")
        try:
            return int(resp)
        except Exception:
            return resp

    def enable_stop_on_fail(self, state):
        """
        Turn the "Stop on Fail" function on or off.
        
        :param state: 1/0 or "ON"/"OFF"
        :type state: int or str

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
    
        :return: 1 (enabled) or 0 (disabled)
        :rtype: int
        """
        resp = self.instrument.query(":MASK:SOOutput?")
        try:
            return int(resp)
        except Exception:
            return resp

    def enable_sound(self, state):
        """
        Enable or disable the sound prompt when failed waveforms are detected.
        
        :param state: 1/0 or "ON"/"OFF"
        :type state: int or str

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
        
        :return: 1 (enabled) or 0 (disabled)
        :rtype: int
        """
        resp = self.instrument.query(":MASK:OUTPut?")
        try:
            return int(resp)
        except Exception:
            return resp
    def set_x(self, x):
        """
        Set the horizontal adjustment parameter in the pass/fail test mask.
        
        :param x: Value between 0.02 and 4 (step 0.02)
        :type x: float
        """
        if isinstance(x, (float, int)) and 0.02 <= x <= 4:
            self.instrument.write(f":MASK:X {x}")
        else:
            print("Invalid x value. Must be between 0.02 and 4.")

    def get_x(self):
        """
        Query the horizontal adjustment parameter in the pass/fail test mask.
   
        :return: Horizontal adjustment parameter
        :rtype: float or str
        """
        resp = self.instrument.query(":MASK:X?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_y(self, y):
        """
        Set the vertical adjustment parameter in the pass/fail test mask.

        :param y: Value between 0.04 and 5.12 (step 0.04)
        :type y: float
        """
        if isinstance(y, (float, int)) and 0.04 <= y <= 5.12:
            self.instrument.write(f":MASK:Y {y}")
        else:
            print("Invalid y value. Must be between 0.04 and 5.12.")

    def get_y(self):
        """
        Query the vertical adjustment parameter in the pass/fail test mask.
        
        :return: Vertical adjustment parameter
        :rtype: float or str
        """
        resp = self.instrument.query(":MASK:Y?")
        try:
            return float(resp)
        except Exception:
            return resp

    def create(self):
        """
        Create the pass/fail test mask using the current horizontal and vertical adjustment parameters.
        """
        self.instrument.write(":MASK:CREate")

    def get_passed(self):
        """
        Query the number of passed frames in the pass/fail test.

        :return: Number of passed frames
        :rtype: int
        """
        resp = self.instrument.query(":MASK:PASSed?")
        try:
            return int(resp)
        except Exception:
            return resp

    def get_failed(self):
        """
        Query the number of failed frames in the pass/fail test.
        
        :return: Number of failed frames
        :rtype: int
        """
        resp = self.instrument.query(":MASK:FAILed?")
        try:
            return int(resp)
        except Exception:
            return resp

    def get_total(self):
        """
        Query the total number of frames in the pass/fail test.
        
        :return: Total number of frames
        :rtype: int
        """
        resp = self.instrument.query(":MASK:TOTal?")
        try:
            return int(resp)
        except Exception:
            return resp

    def reset(self):
        """
        Reset the numbers of passed, failed, and total frames in the pass/fail test to 0.

        """
        self.instrument.write(":MASK:RESet")

class Measure:
    """
    The Measure commands are used to set and query measurement parameters and statistics.
    """
    def __init__(self, instrument,data_handler):
        """Initialize the Measure class.
        
        :param instrument: The instrument instance to communicate with.
        :type instrument: object
        :param data_handler: The data handler instance for processing data.
        :type data_handler: object
        """
        self.instrument = instrument
        self.data_handler = data_handler

    def set_source(self, source):
        """
        Set the source for measurement.
        
        :param source: "CHAN1", "CHAN2", "MATH", etc.
        :type source: str
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
        
        :return: Current source
        :rtype: str
        """
        return self.instrument.query(":MEAS:SOUR?")

    def clear(self):
        """
        Clear all measurement results.
       
        """
        self.instrument.write(":MEAS:CLE")

    def recover(self):
        """
        Recover the last measurement result.
        
        """
        self.instrument.write(":MEAS:REC")

    def set_display(self, state):
        """
        Enable or disable the measurement result display.
        
        :param state: 1/0 or "ON"/"OFF"
        :type state: int or str

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
        
        :return: 1 (enabled) or 0 (disabled)
        :rtype: int
        """
        resp = self.instrument.query(":MEAS:ADIS?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_auto_measure_source(self, source):
        """
        Set the source for auto measurement.
        
        :param source: "CHAN1", "CHAN2", "MATH"
        :type source: str

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
    
        :return: Current source
        :rtype: str
        """
        return self.instrument.query(":MEAS:AMS?")

    def set_setup_max(self, value):
        """
        Set the maximum threshold for measurement.
        
        :param value: Threshold value
        :type value: float

        """
        self.instrument.write(f":MEAS:SET:MAX {value}")

    def get_setup_max(self):
        """
        Query the maximum threshold for measurement.
        
        :return: Threshold value
        :rtype: float or str
        """
        resp = self.instrument.query(":MEAS:SET:MAX?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_setup_mid(self, value):
        """
        Set the middle threshold for measurement.
        
        :param value: Threshold value
        :type value: float

        """
        self.instrument.write(f":MEAS:SET:MID {value}")

    def get_setup_mid(self):
        """
        Query the middle threshold for measurement.
       
        :return: Threshold value
        :rtype: float or str
        """
        resp = self.instrument.query(":MEAS:SET:MID?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_setup_min(self, value):
        """
        Set the minimum threshold for measurement.
        
        :param value: Threshold value
        :type value: float

        """
        self.instrument.write(f":MEAS:SET:MIN {value}")

    def get_setup_min(self):
        """
        Query the minimum threshold for measurement.
        

        
        :return: Threshold value
        :rtype: float or str
        """
        resp = self.instrument.query(":MEAS:SET:MIN?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_setup_psa(self, value):
        """
        Set the positive slope threshold A for measurement.
        
        :param value: Threshold value
        :type value: float

        """
        self.instrument.write(f":MEAS:SET:PSA {value}")

    def get_setup_psa(self):
        """
        Query the positive slope threshold A for measurement.
        
        :return: Threshold value
        :rtype: float or str
        """
        resp = self.instrument.query(":MEAS:SET:PSA?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_setup_psb(self, value):
        """
        Set the positive slope threshold B for measurement.
        
        :param value: Threshold value
        :type value: float

        """
        self.instrument.write(f":MEAS:SET:PSB {value}")

    def get_setup_psb(self):
        """
        Query the positive slope threshold B for measurement.
        
        :return: Threshold value
        :rtype: float or str
        """
        resp = self.instrument.query(":MEAS:SET:PSB?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_setup_dsa(self, value):
        """
        Set the negative slope threshold A for measurement.
        
        :param value: Threshold value
        :type value: float

        """
        self.instrument.write(f":MEAS:SET:DSA {value}")

    def get_setup_dsa(self):
        """
        Query the negative slope threshold A for measurement.
        

        
        :return: Threshold value
        :rtype: float or str
        """
        resp = self.instrument.query(":MEAS:SET:DSA?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_setup_dsb(self, value):
        """
        Set the negative slope threshold B for measurement.
        
        :param value: Threshold value
        :type value: float

        """
        self.instrument.write(f":MEAS:SET:DSB {value}")

    def get_setup_dsb(self):
        """
        Query the negative slope threshold B for measurement.
        

        
        :return: Threshold value
        :rtype: float or str
        """
        resp = self.instrument.query(":MEAS:SET:DSB?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_statistic_display(self, state):
        """
        Enable or disable the statistic display for measurement.
        
        :param state: 1/0 or "ON"/"OFF"
        :type state: int or str

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
        
        :return: 1 (enabled) or 0 (disabled)
        :rtype: int
        """
        resp = self.instrument.query(":MEAS:STAT:DISP?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_statistic_mode(self, mode):
        """
        Set the statistic mode for measurement.
        
        :param mode: "ALL" or "CURR"
        :type mode: str

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
        

        
        :return: "ALL" or "CURR"
        :rtype: str
        """
        return self.instrument.query(":MEAS:STAT:MODE?")

    def reset_statistic(self):
        """
        Reset the measurement statistics.

        """
        self.instrument.write(":MEAS:STAT:RES")

    def set_statistic_item(self, item):
        """
        Set the statistic item for measurement.

        :param item: Measurement item name (e.g., "VPP", "VRMS", etc.)
        :type item: str
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
        

        
        :return: Measurement item name
        :rtype: str
        """
        return self.instrument.query(":MEAS:STAT:ITEM?")

    def set_item(self, item):
        """
        Set the measurement item.
        
        :param item: Measurement item name (e.g., "VPP", "VRMS", etc.)
        :type item: str

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
        

        
        :return: Measurement item name
        :rtype: str
        """
        return self.instrument.query(":MEAS:ITEM?")

    def set_counter_source(self, source):
        """
        Set the source for the measurement counter.
        
        :param source: "CHAN1", "CHAN2", "MATH"
        :type source: str

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
        

        
        :return: Current source
        :rtype: str
        """
        return self.instrument.query(":MEAS:COUN:SOUR?")

    def get_counter_value(self):
        """
        Query the value of the measurement counter.
        

        
        :return: Counter value
        :rtype: int or str
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
        """Initialize the Reference class.
        
        :param instrument: The instrument instance to communicate with.
        :type instrument: object
        :param data_handler: The data handler instance for processing data.
        :type data_handler: object
        """
        self.instrument = instrument
        self.data_handler = data_handler

    def set_display(self, state):
        """
        Enable or disable the REF function.
        
        :param state: 1/0 or "ON"/"OFF"
        :type state: int or str

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
        
        :return: 1 (enabled) or 0 (disabled)
        :rtype: int
        """
        resp = self.instrument.query(":REF:DISP?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_enable(self, n, state):
        """
        Enable or disable the specified reference channel.
        
        :param n: Reference channel number (1-10)
        :type n: int
        :param state: 1/0 or "ON"/"OFF"
        :type state: int or str
       

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
        
        :param n: Reference channel number (1-10)
        :type n: int
        :return: 1 (enabled) or 0 (disabled)
        :rtype: int
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
        
        :param n: Reference channel number (1-10)
        :type n: int
        :param source: "CHANNEL1", "CHANNEL2", or "MATH"
        :type source: str
        

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
        
        :param n: Reference channel number (1-10)
        :type n: int
        :return: "CHAN1", "CHAN2", or "MATH"
        :rtype: str
        """
        if n not in range(1, 11):
            print("Invalid reference channel. Use 1-10.")
            return None
        return self.instrument.query(f":REF{n}:SOUR?")

    def set_vscale(self, n, scale):
        """
        Set the vertical scale of the specified reference channel.
        
        :param n: Reference channel number (1-10)
        :type n: int
        :param scale: Vertical scale value
        :type scale: float
        

        """
        if n not in range(1, 11):
            print("Invalid reference channel. Use 1-10.")
            return
        self.instrument.write(f":REF{n}:VSCale {scale}")

    def get_vscale(self, n):
        """
        Query the vertical scale of the specified reference channel.
        
        :param n: Reference channel number (1-10)
        :type n: int
        :return: Vertical scale value
        :rtype: float or str
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
        
        :param n: Reference channel number (1-10)
        :type n: int
        :param offset: Vertical offset value
        :type offset: float

        """
        if n not in range(1, 11):
            print("Invalid reference channel. Use 1-10.")
            return
        self.instrument.write(f":REF{n}:VOFFset {offset}")

    def get_voffset(self, n):
        """
        Query the vertical offset of the specified reference channel.
        
        :param n: Reference channel number (1-10)
        :type n: int
        :return: Vertical offset value
        :rtype: float or str
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
        
        :param n: Reference channel number (1-10)
        :type n: int

        """
        if n not in range(1, 11):
            print("Invalid reference channel. Use 1-10.")
            return
        self.instrument.write(f":REF{n}:RESet")

    def set_current(self, n):
        """
        Select the current reference channel.
        
        :param n: Reference channel number (1-10)
        :type n: int

        """
        if n not in range(1, 11):
            print("Invalid reference channel. Use 1-10.")
            return
        self.instrument.write(f":REF{n}:CURR")

    def save(self, n):
        """
        Store the waveform of the current reference channel to internal memory.
        
        :param n: Reference channel number (1-10)
        :type n: int

        """
        if n not in range(1, 11):
            print("Invalid reference channel. Use 1-10.")
            return
        self.instrument.write(f":REF{n}:SAVE")

    def set_color(self, n, color):
        """
        Set the display color of the current reference channel.
        
        :param n: Reference channel number (1-10)
        :type n: int
        :param color: "GRAY", "GREEN", "LBLUE", "MAGENTA", "ORANGE"
        :type color: str
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
        
        :param n: Reference channel number (1-10)
        :type n: int
        :return: Color name
        :rtype: str
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
        """Initialize the Storage class.
        
        :param instrument: The instrument instance to communicate with.
        :type instrument: object
        :param data_handler: The data handler instance for processing data.
        :type data_handler: object
        """
        self.instrument = instrument
        self.data_handler = data_handler

    def set_image_type(self, img_type):
        """
        Set the image type when storing images.
        
        :param img_type: "PNG", "BMP8", "BMP24", "JPEG", "TIFF"
        

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
         
        :return: Image type
        :rtype: str
        """
        return self.instrument.query(":STOR:IMAG:TYPE?")

    def set_image_invert(self, state):
        """
        Turn on or off the invert function when storing images.
        
        :param state: 1/0 or "ON"/"OFF"
        :type state: int or str

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
        
        :return: "ON" or "OFF"
        :rtype: str
        """
        return self.instrument.query(":STOR:IMAG:INVERT?")

    def set_image_color(self, state):
        """
        Set the image color when storing images to color (ON) or intensity graded color (OFF).
        
        :param state: 1/0 or "ON"/"OFF"
        :type state: int or str

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
        
        :return: "ON" or "OFF"
        :rtype: str
        """
        return self.instrument.query(":STOR:IMAG:COLor?")

class System:
    """
    The System commands are used to set system-related parameters.
    """
    def __init__(self, instrument,data_handler):
        """Initialize the System class.
        
        :param instrument: The instrument instance to communicate with.
        :type instrument: object
        :param data_handler: The data handler instance for processing data.
        :type data_handler: object
        """

        self.instrument = instrument
        self.data_handler = data_handler

    def set_autoscale(self, state):
        """
        Enable or disable the AUTO key on the front panel.
        
        :param state: 1/0 or "ON"/"OFF"
        :type state: int or str

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
        
        :return: 1 (enabled) or 0 (disabled)
        :rtype: int
        """
        resp = self.instrument.query(":SYST:AUToscale?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_beeper(self, state):
        """
        Enable or disable the beeper.
        
        :param state: 1/0 or "ON"/"OFF"
        :type state: int or str

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
        
        :return: 1 (enabled) or 0 (disabled)
        :rtype: int
        """
        resp = self.instrument.query(":SYST:BEEPer?")
        try:
            return int(resp)
        except Exception:
            return resp

    def get_error(self):
        """
        Query and delete the last system error message.
       
        :return: Error message in "<number>,<content>" format
        :rtype: str
        """
        return self.instrument.query(":SYST:ERRor?")

    def get_grid_count(self):
        """
        Query the number of grids in the horizontal direction of the instrument screen.
        
        :return: Always returns 12
        :rtype: int
        """
        resp = self.instrument.query(":SYST:GAM?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_language(self, lang):
        """
        Set the system language.
        
        :param lang: "SCHINESE", "TCHINESE", "ENGLISH", "PORTUGUESE", "GERMAN", "POLISH", "KOREAN", "JAPANESE", "FRENCH", "RUSSIAN"
        :type lang: str

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
        

        
        :return: Language code
        :rtype: str
        """
        return self.instrument.query(":SYST:LANG?")

    def set_locked(self, state):
        """
        Enable or disable the keyboard lock function.

        :param state: 1/0 or "ON"/"OFF"
        :type state: int or str
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
        

        
        :return: 1 (locked) or 0 (unlocked)
        :rtype: int
        """
        resp = self.instrument.query(":SYST:LOCKed?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_pon(self, pon):
        """
        Set the system configuration to be recalled at power-on.
        
        :param pon: "LATEST" or "DEFAULT"
        :type pon: str

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
        


        :return: "LAT" or "DEF"
        :rtype: str
        """
        return self.instrument.query(":SYST:PON?")

    def install_option(self, license_code):
        """
        Install an option license.

        :param license_code: 28-byte license string (uppercase letters and numbers)
        :type license_code: str

        """
        if isinstance(license_code, str) and len(license_code) == 28 and license_code.isalnum() and license_code.isupper():
            self.instrument.write(f":SYST:OPT:INST {license_code}")
        else:
            print("Invalid license code. Must be 28 uppercase letters/numbers.")

    def uninstall_option(self):
        """
        Uninstall all installed options.
        """
        self.instrument.write(":SYST:OPT:UNINST")

    def get_ram(self):
        """
        Query the number of analog channels of the instrument.

        :return: Always returns 2
        :rtype: int
        """
        resp = self.instrument.query(":SYST:RAM?")
        try:
            return int(resp)
        except Exception:
            return resp

    def get_setup(self):
        """
        Query the setting of the oscilloscope (returns binary data with TMC header). If autosave is on, then also saves them to a bin file.
        


        :return: Setup data
        :rtype: bytes
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

        :param setup_stream: Setup data (must be from get_setup)
        :type setup_stream: bytes

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

        :param state: 1/0 or "ON"/"OFF"
        :type state: int or str

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

        :return: 1 (enabled) or 0 (disabled)
        :rtype: int
        """
        resp = self.instrument.query(":TIM:DEL:ENAB?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_delay_offset(self, offset):
        """
        Set the delayed timebase offset (in seconds).

        :param offset: Offset value in seconds
        :type offset: float

        """
        self.instrument.write(f":TIM:DEL:OFFS {offset}")

    def get_delay_offset(self):
        """
        Query the delayed timebase offset (in seconds).



        :return: Offset value in seconds
        :rtype: float or str
        """
        resp = self.instrument.query(":TIM:DEL:OFFS?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_delay_scale(self, scale):
        """
        Set the delayed timebase scale (in s/div).

        :param scale: Scale value in seconds/div
        :type scale: float

        """
        self.instrument.write(f":TIM:DEL:SCAL {scale}")

    def get_delay_scale(self):
        """
        Query the delayed timebase scale (in s/div).



        :return: Scale value in seconds/div
        :rtype: float or str
        """
        resp = self.instrument.query(":TIM:DEL:SCAL?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_main_offset(self, offset):
        """
        Set the main timebase offset (in seconds).

        :param offset: Offset value in seconds
        :type offset: float

        """
        self.instrument.write(f":TIM:MAIN:OFFS {offset}")

    def get_main_offset(self):
        """
        Query the main timebase offset (in seconds).



        :return: Offset value in seconds
        :rtype: float or str
        """
        resp = self.instrument.query(":TIM:MAIN:OFFS?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_main_scale(self, scale):
        """
        Set the main timebase scale (in s/div).

        :param scale: Scale value in seconds/div
        :type scale: float

        """
        self.instrument.write(f":TIM:MAIN:SCAL {scale}")

    def get_main_scale(self):
        """
        Query the main timebase scale (in s/div).



        :return: Scale value in seconds/div
        :rtype: float or str
        """
        resp = self.instrument.query(":TIM:MAIN:SCAL?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_mode(self, mode):
        """
        Set the mode of the horizontal timebase.

        :param mode: "MAIN", "XY", or "ROLL"
        :type mode: str

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



        :return: "MAIN", "XY", or "ROLL"
        :rtype: str
        """
        return self.instrument.query(":TIM:MODE?")
class Trigger:
    """
    The Trigger commands are used to set the trigger system of the oscilloscope.
    """
    def __init__(self, instrument,data_handler):
        self.instrument = instrument
        self.data_handler = data_handler
        self.rs232 = self.RS232(instrument, data_handler)
        self.iic = self.IIC_Trigger(instrument, data_handler)
        self.spi = self.SPI_Trigger(instrument, data_handler)

    def set_mode(self, mode):
        """
        Set the trigger type.

        :param mode: One of {"EDGE", "PULSE", "RUNT", "WIND", "NEDG", "SLOPE", "VIDEO", "PATTERN", "DELAY", "TIMEOUT", "DURATION", "SHOLD", "RS232", "IIC", "SPI"}
        :type mode: str
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

        :return: Trigger mode
        :rtype: str
        """
        return self.instrument.query(":TRIG:MODE?")

    def set_coupling(self, coupling):
        """
        Set the trigger coupling type.

        :param coupling: One of {"AC", "DC", "LFREJECT", "HFREJECT"}
        :type coupling: str
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
        
        :return: Coupling type
        :rtype: str
        """
        return self.instrument.query(":TRIG:COUP?")

    def get_status(self):
        """
        Query the current trigger status.
        

        
        :return: One of "TD", "WAIT", "RUN", "AUTO", "STOP"
        :rtype: str
        """
        return self.instrument.query(":TRIG:STAT?")

    def set_sweep(self, sweep):
        """
        Set the trigger mode (sweep).
        
        :param sweep: One of {"AUTO", "NORMAL", "SINGLE"}
        :type sweep: str

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
        
        :return: "AUTO", "NORM", or "SING"
        :rtype: str
        """
        return self.instrument.query(":TRIG:SWEE?")

    def set_holdoff(self, value):
        """
        Set the trigger holdoff time (in seconds).

        :param value: Holdoff time, 16e-9 to 10
        :type value: float

        """
        if isinstance(value, (float, int)) and 16e-9 <= value <= 10:
            self.instrument.write(f":TRIG:HOLD {value}")
        else:
            print("Invalid holdoff value. Must be between 16ns and 10s.")

    def get_holdoff(self):
        """
        Query the trigger holdoff time (in seconds).

        :return: Holdoff time
        :rtype: float or str
        """
        resp = self.instrument.query(":TRIG:HOLD?")
        try:
            return float(resp)
        except Exception:
            return resp

    def enable_noise_rejection(self, state):
        """
        Enable or disable noise rejection for trigger.

        :param state: 1/0 or "ON"/"OFF"
        :type state: int or str

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



        :return: 1 (enabled) or 0 (disabled)
        :rtype: int
        """
        resp = self.instrument.query(":TRIG:NREJ?")
        try:
            return int(resp)
        except Exception:
            return resp

    def get_position(self):
        """
        Query the position in the internal memory that corresponds to the waveform trigger position.
        

        :return: -2 (not triggered), -1 (triggered outside memory), or >0 (position)
        :rtype: int or str
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

        :param source: "CHANNEL1", "CHANNEL2", "AC", "EXT"
        :type source: str

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



        :return: "CHAN1", "CHAN2", "AC", or "EXT"
        :rtype: str
        """
        return self.instrument.query(":TRIG:EDGE:SOUR?")

    def set_edge_slope(self, slope):
        """
        Set the edge type in edge trigger.

        :param slope: "POSITIVE", "NEGATIVE", "RFALL"
        :type slope: str

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



        :return: "POS", "NEG", or "RFAL"
        :rtype: str
        """
        return self.instrument.query(":TRIG:EDGE:SLOP?")

    def set_edge_level(self, level):
        """
        Set the trigger level in edge trigger.

        :param level: Level value
        :type level: float

        """
        self.instrument.write(f":TRIG:EDGE:LEV {level}")

    def get_edge_level(self):
        """
        Query the trigger level in edge trigger.

        :return: Level value
        :rtype: float or str
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

        :param source: "CHANNEL1" or "CHANNEL2"
        :type source: str

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

        :return: "CHAN1" or "CHAN2"
        :rtype: str
        """
        return self.instrument.query(":TRIG:PULS:SOUR?")

    def set_pulse_when(self, when):
        """
        Set the trigger condition in pulse width trigger.

        :param when: "PGREATER", "PLESS", "NGREATER", "NLESS", "PGLESS", "NGLess"
        :type when: str

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

        :return: Condition code
        :rtype: str
        """
        return self.instrument.query(":TRIG:PULS:WHEN?")

    def set_pulse_width(self, width):
        """
        Set the pulse width in pulse width trigger (seconds).

        :param width: 8e-9 to 10
        :type width: float

        """
        if isinstance(width, (float, int)) and 8e-9 <= width <= 10:
            self.instrument.write(f":TRIG:PULS:WIDT {width}")
        else:
            print("Invalid width. Must be between 8ns and 10s.")

    def get_pulse_width(self):
        """
        Query the pulse width in pulse width trigger (seconds).



        :return: Pulse width
        :rtype: float or str
        """
        resp = self.instrument.query(":TRIG:PULS:WIDT?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_pulse_uwidth(self, width):
        """
        Set the upper pulse width in pulse width trigger (seconds).

        :param width: 16e-9 to 10
        :type width: float

        """
        if isinstance(width, (float, int)) and 16e-9 <= width <= 10:
            self.instrument.write(f":TRIG:PULS:UWID {width}")
        else:
            print("Invalid upper width. Must be between 16ns and 10s.")

    def get_pulse_uwidth(self):
        """
        Query the upper pulse width in pulse width trigger (seconds).

        :return: Upper pulse width
        :rtype: float or str
        """
        resp = self.instrument.query(":TRIG:PULS:UWID?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_pulse_lwidth(self, width):
        """
        Set the lower pulse width in pulse width trigger (seconds).

        :param width: 8e-9 to 9.99
        :type width: float
        """
        if isinstance(width, (float, int)) and 8e-9 <= width <= 9.99:
            self.instrument.write(f":TRIG:PULS:LWID {width}")
        else:
            print("Invalid lower width. Must be between 8ns and 9.99s.")

    def get_pulse_lwidth(self):
        """
        Query the lower pulse width in pulse width trigger (seconds).



        :return: Lower pulse width
        :rtype: float or str
        """
        resp = self.instrument.query(":TRIG:PULS:LWID?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_pulse_level(self, level):
        """
        Set the trigger level in pulse width trigger.

        :param level: Level value
        :type level: float

        """
        self.instrument.write(f":TRIG:PULS:LEV {level}")

    def get_pulse_level(self):
        """
        Query the trigger level in pulse width trigger.



        :return: Level value
        :rtype: float or str
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

        :param source: "CHANNEL1" or "CHANNEL2"
        :type source: str

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



        :return: "CHAN1" or "CHAN2"
        :rtype: str
        """
        return self.instrument.query(":TRIG:SLOP:SOUR?")

    def set_slope_when(self, when):
        """
        Set the trigger condition in slope trigger.

        :param when: "PGREATER", "PLESS", "NGREATER", "NLESS", "PGLESS", "NGLess"
        :type when: str

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



        :return: Condition code
        :rtype: str
        """
        return self.instrument.query(":TRIG:SLOP:WHEN?")

    def set_slope_time(self, time):
        """
        Set the time value in slope trigger (seconds).

        :param time: 8e-9 to 10
        :type time: float

        """
        if isinstance(time, (float, int)) and 8e-9 <= time <= 10:
            self.instrument.write(f":TRIG:SLOP:TIME {time}")
        else:
            print("Invalid time. Must be between 8ns and 10s.")

    def get_slope_time(self):
        """
        Query the time value in slope trigger (seconds).



        :return: Time value
        :rtype: float or str
        """
        resp = self.instrument.query(":TRIG:SLOP:TIME?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_slope_tupper(self, time):
        """
        Set the upper limit of the time in slope trigger (seconds).

        :param time: 16e-9 to 10
        :type time: float

        """
        if isinstance(time, (float, int)) and 16e-9 <= time <= 10:
            self.instrument.write(f":TRIG:SLOP:TUPP {time}")
        else:
            print("Invalid upper time. Must be between 16ns and 10s.")

    def get_slope_tupper(self):
        """
        Query the upper limit of the time in slope trigger (seconds).



        :return: Upper time value
        :rtype: float or str
        """
        resp = self.instrument.query(":TRIG:SLOP:TUPP?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_slope_tlower(self, time):
        """
        Set the lower limit of the time in slope trigger (seconds).

        :param time: 8e-9 to 9.99
        :type time: float

        """
        if isinstance(time, (float, int)) and 8e-9 <= time <= 9.99:
            self.instrument.write(f":TRIG:SLOP:TLOW {time}")
        else:
            print("Invalid lower time. Must be between 8ns and 9.99s.")

    def get_slope_tlower(self):
        """
        Query the lower limit of the time in slope trigger (seconds).



        :return: Lower time value
        :rtype: float or str
        """
        resp = self.instrument.query(":TRIG:SLOP:TLOW?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_slope_window(self, window):
        """
        Set the vertical window type in slope trigger.
        
        :param window: "TA", "TB", or "TAB"
        :type window: str

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
        

        
        :return: Window type
        :rtype: str
        """
        return self.instrument.query(":TRIG:SLOP:WIND?")

    def set_slope_alevel(self, level):
        """
        Set the upper limit of the trigger level in slope trigger.
        
        :param level: Level value
        :type level: float

        """
        self.instrument.write(f":TRIG:SLOP:ALEV {level}")

    def get_slope_alevel(self):
        """
        Query the upper limit of the trigger level in slope trigger.
        

        
        :return: Level value
        :rtype: float or str
        """
        resp = self.instrument.query(":TRIG:SLOP:ALEV?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_slope_blevel(self, level):
        """
        Set the lower limit of the trigger level in slope trigger.
        
        :param level: Level value
        :type level: float

        """
        self.instrument.write(f":TRIG:SLOP:BLEV {level}")

    def get_slope_blevel(self):
        """
        Query the lower limit of the trigger level in slope trigger.
        

        
        :return: Level value
        :rtype: float or str
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
        
        :param source: "CHANNEL1" or "CHANNEL2"
        :type source: str

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
        
        :return: "CHAN1" or "CHAN2"
        :rtype: str
        """
        return self.instrument.query(":TRIG:VID:SOUR?")

    def set_video_polarity(self, polarity):
        """
        Set the video polarity in video trigger.
        
        :param polarity: "POSITIVE" or "NEGATIVE"
        :type polarity: str
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
        
        :return: "POS" or "NEG"
        :rtype: str
        """
        return self.instrument.query(":TRIG:VID:POL?")

    def set_video_mode(self, mode):
        """
        Set the sync type in video trigger.
        
        :param mode: "ODDFIELD", "EVENFIELD", "LINE", or "ALINES"
        :type mode: str
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
        
        :return: "ODDF", "EVEN", "LINE", or "ALIN"
        :rtype: str
        """
        return self.instrument.query(":TRIG:VID:MODE?")

    def set_video_line(self, line):
        """
        Set the line number when the sync type in video trigger is LINE.
        
        :param line: Line number (see documentation for valid range)
        :type line: int

        """
        if isinstance(line, int) and line >= 1:
            self.instrument.write(f":TRIG:VID:LINE {line}")
        else:
            print("Invalid line number. Must be integer >= 1.")

    def get_video_line(self):
        """
        Query the line number when the sync type in video trigger is LINE.
        

        
        :return: Line number
        :rtype: int or str
        """
        resp = self.instrument.query(":TRIG:VID:LINE?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_video_standard(self, standard):
        """
        Set the video standard in video trigger.
        
        :param standard: "PALSECAM", "NTSC", "480P", or "576P"
        :type standard: str

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
        

        
        :return: "PALS", "NTSC", "480P", or "576P"
        :rtype: str
        """
        return self.instrument.query(":TRIG:VID:STAN?")

    def set_video_level(self, level):
        """
        Set the trigger level in video trigger.
        
        :param level: Level value
        :type level: float

        """
        self.instrument.write(f":TRIG:VID:LEV {level}")

    def get_video_level(self):
        """
        Query the trigger level in video trigger.
        
        :return: Level value
        :rtype: float or str
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
        
        :param source: "CHANNEL1" or "CHANNEL2"
        :type source: str

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
        

        
        :return: "CHAN1" or "CHAN2"
        :rtype: str
        """
        return self.instrument.query(":TRIG:PATT:SOUR?")

    def set_pattern_condition(self, cond):
        """
        Set the pattern condition in pattern trigger.
        
        :param cond: "AND", "OR", "NAND", "NOR"
        :type cond: str
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
        
        :return: Condition code
        :rtype: str
        """
        return self.instrument.query(":TRIG:PATT:COND?")

    def set_pattern_level(self, level):
        """
        Set the trigger level in pattern trigger.
        
        :param level: Level value
        :type level: float
        """
        self.instrument.write(f":TRIG:PATT:LEV {level}")

    def get_pattern_level(self):
        """
        Query the trigger level in pattern trigger.
        
        :return: Level value
        :rtype: float or str
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
        
        :param source: "CHANNEL1" or "CHANNEL2"
        :type source: str
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
        
        :return: "CHAN1" or "CHAN2"
        :rtype: str
        """
        return self.instrument.query(":TRIG:DUR:SOUR?")

    def set_duration_when(self, when):
        """
        Set the trigger condition in duration trigger.
        
        :param when: "GREATER", "LESS"
        :type when: str

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

        :return: Condition code
        :rtype: str
        """
        return self.instrument.query(":TRIG:DUR:WHEN?")

    def set_duration_time(self, time):
        """
        Set the time value in duration trigger (seconds).

        :param time: 8e-9 to 10
        :type time: float
        """
        if isinstance(time, (float, int)) and 8e-9 <= time <= 10:
            self.instrument.write(f":TRIG:DUR:TIME {time}")
        else:
            print("Invalid time. Must be between 8ns and 10s.")

    def get_duration_time(self):
        """
        Query the time value in duration trigger (seconds).



        :return: Time value
        :rtype: float or str
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

        :param source: "CHANNEL1" or "CHANNEL2"
        :type source: str

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



        :return: "CHAN1" or "CHAN2"
        :rtype: str
        """
        return self.instrument.query(":TRIG:TIME:SOUR?")

    def set_timeout_when(self, when):
        """
        Set the trigger condition in timeout trigger.

        :param when: "GREATER", "LESS"
        :type when: str

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



        :return: Condition code
        :rtype: str
        """
        return self.instrument.query(":TRIG:TIME:WHEN?")

    def set_timeout_time(self, time):
        """
        Set the time value in timeout trigger (seconds).

        :param time: 8e-9 to 10
        :type time: float

        """
        if isinstance(time, (float, int)) and 8e-9 <= time <= 10:
            self.instrument.write(f":TRIG:TIME:TIME {time}")
        else:
            print("Invalid time. Must be between 8ns and 10s.")

    def get_timeout_time(self):
        """
        Query the time value in timeout trigger (seconds).



        :return: Time value
        :rtype: float or str
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

        :param source: "CHANNEL1" or "CHANNEL2"
        :type source: str

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
        


        :return: "CHAN1" or "CHAN2"
        :rtype: str
        """
        return self.instrument.query(":TRIG:RUNT:SOUR?")

    def set_runt_polarity(self, polarity):
        """
        Set the pulse polarity in runt trigger.

        :param polarity: "POSITIVE" or "NEGATIVE"
        :type polarity: str

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



        :return: "POS" or "NEG"
        :rtype: str
        """
        return self.instrument.query(":TRIG:RUNT:POL?")

    def set_runt_when(self, when):
        """
        Set the qualifier in runt trigger.

        :param when: "NONE", "GREATER", "LESS", "GLESS"
        :type when: str

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



        :return: Qualifier code
        :rtype: str
        """
        return self.instrument.query(":TRIG:RUNT:WHEN?")

    def set_runt_wupper(self, upper):
        """
        Set the pulse width upper limit in runt trigger (seconds).

        :param upper: Upper limit, 16e-9 to 10
        :type upper: float

        """
        if isinstance(upper, (float, int)) and 16e-9 <= upper <= 10:
            self.instrument.write(f":TRIG:RUNT:WUPP {upper}")
        else:
            print("Invalid upper limit. Must be between 16ns and 10s.")

    def get_runt_wupper(self):
        """
        Query the pulse width upper limit in runt trigger (seconds).



        :return: Upper limit
        :rtype: float or str
        """
        resp = self.instrument.query(":TRIG:RUNT:WUPP?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_runt_wlower(self, lower):
        """
        Set the pulse width lower limit in runt trigger (seconds).

        :param lower: Lower limit, 8e-9 to 9.99
        :type lower: float

        """
        if isinstance(lower, (float, int)) and 8e-9 <= lower <= 9.99:
            self.instrument.write(f":TRIG:RUNT:WLOW {lower}")
        else:
            print("Invalid lower limit. Must be between 8ns and 9.99s.")

    def get_runt_wlower(self):
        """
        Query the pulse width lower limit in runt trigger (seconds).

        :return: Lower limit
        :rtype: float or str
        """
        resp = self.instrument.query(":TRIG:RUNT:WLOW?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_runt_alevel(self, level):
        """
        Set the trigger level upper limit in runt trigger.

        :param level: Level value
        :type level: float

        """
        self.instrument.write(f":TRIG:RUNT:ALEV {level}")

    def get_runt_alevel(self):
        """
        Query the trigger level upper limit in runt trigger.

        :return: Level value
        :rtype: float or str
        """
        resp = self.instrument.query(":TRIG:RUNT:ALEV?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_runt_blevel(self, level):
        """
        Set the trigger level lower limit in runt trigger.

        :param level: Level value
        :type level: float

        """
        self.instrument.write(f":TRIG:RUNT:BLEV {level}")

    def get_runt_blevel(self):
        """
        Query the trigger level lower limit in runt trigger.



        :return: Level value
        :rtype: float or str
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

        :param source: "CHANNEL1" or "CHANNEL2"
        :type source: str

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



        :return: "CHAN1" or "CHAN2"
        :rtype: str
        """
        return self.instrument.query(":TRIG:WIND:SOUR?")

    def set_windows_slope(self, slope):
        """
        Set the windows type in windows trigger.

        :param slope: "POSITIVE", "NEGATIVE", "RFALL"
        :type slope: str
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

        :return: "POS", "NEG", or "RFAL"
        :rtype: str
        """
        return self.instrument.query(":TRIG:WIND:SLOP?")

    def set_windows_position(self, pos):
        """
        Set the trigger position in windows trigger.

        :param pos: "EXIT", "ENTER", "TIME"
        :type pos: str

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



        :return: "EXIT", "ENTER", or "TIM"
        :rtype: str
        """
        return self.instrument.query(":TRIG:WIND:POS?")

    def set_windows_time(self, time):
        """
        Set the hold time in windows trigger (seconds).

        :param time: 8e-9 to 10
        :type time: float

        """
        if isinstance(time, (float, int)) and 8e-9 <= time <= 10:
            self.instrument.write(f":TRIG:WIND:TIME {time}")
        else:
            print("Invalid time. Must be between 8ns and 10s.")

    def get_windows_time(self):
        """
        Query the hold time in windows trigger (seconds).



        :return: Hold time
        :rtype: float or str
        """
        resp = self.instrument.query(":TRIG:WIND:TIME?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_windows_alevel(self, level):
        """
        Set the trigger level upper limit in windows trigger.

        :param level: Level value
        :type level: float

        """
        self.instrument.write(f":TRIG:WIND:ALEV {level}")

    def get_windows_alevel(self):
        """
        Query the trigger level upper limit in windows trigger.

        :return: Level value
        :rtype: float or str
        """
        resp = self.instrument.query(":TRIG:WIND:ALEV?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_windows_blevel(self, level):
        """
        Set the trigger level lower limit in windows trigger.

        :param level: Level value
        :type level: float

        """
        self.instrument.write(f":TRIG:WIND:BLEV {level}")

    def get_windows_blevel(self):
        """
        Query the trigger level lower limit in windows trigger.

        :return: Level value
        :rtype: float or str
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

        :param source: "CHANNEL1" or "CHANNEL2"
        :type source: str


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



        :return: "CHAN1" or "CHAN2"
        :rtype: str
        """
        return self.instrument.query(":TRIG:DEL:SA?")

    def set_delay_slopa(self, slope):
        """
        Set the edge type of edge A in delay trigger.

        :param slope: "POSITIVE" or "NEGATIVE"
        :type slope: str

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



        :return: "POS" or "NEG"
        :rtype: str
        """
        return self.instrument.query(":TRIG:DEL:SLOPA?")

    def set_delay_sb(self, source):
        """
        Set the trigger source B in delay trigger.

        :param source: "CHANNEL1" or "CHANNEL2"
        :type source: str
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



        :return: "CHAN1" or "CHAN2"
        :rtype: str
        """
        return self.instrument.query(":TRIG:DEL:SB?")

    def set_delay_slopb(self, slope):
        """
        Set the edge type of edge B in delay trigger.

        :param slope: "POSITIVE" or "NEGATIVE"
        :type slope: str


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



        :return: "POS" or "NEG"
        :rtype: str
        """
        return self.instrument.query(":TRIG:DEL:SLOPB?")

    def set_delay_type(self, dtype):
        """
        Set the delay type in delay trigger.

        :param dtype: "GREATER", "LESS", "GLESS", "GOUT"
        :type dtype: str


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

        
        :return: Delay type code
        :rtype: str
        """
        return self.instrument.query(":TRIG:DEL:TYPE?")

    def set_delay_tupper(self, upper):
        """
        Set the upper limit of the delay time in delay trigger (seconds).

        :param upper: 16e-9 to 10
        :type upper: float


        """
        if isinstance(upper, (float, int)) and 16e-9 <= upper <= 10:
            self.instrument.write(f":TRIG:DEL:TUPP {upper}")
        else:
            print("Invalid upper limit. Must be between 16ns and 10s.")

    def get_delay_tupper(self):
        """
        Query the upper limit of the delay time in delay trigger (seconds).



        :return: Upper limit
        :rtype: float or str
        """
        resp = self.instrument.query(":TRIG:DEL:TUPP?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_delay_tlower(self, lower):
        """
        Set the lower limit of the delay time in delay trigger (seconds).

        :param lower: 8e-9 to 9.99
        :type lower: float


        """
        if isinstance(lower, (float, int)) and 8e-9 <= lower <= 9.99:
            self.instrument.write(f":TRIG:DEL:TLOW {lower}")
        else:
            print("Invalid lower limit. Must be between 8ns and 9.99s.")

    def get_delay_tlower(self):
        """
        Query the lower limit of the delay time in delay trigger (seconds).



        :return: Lower limit
        :rtype: float or str
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

        :param source: "CHANNEL1" or "CHANNEL2"
        :type source: str


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



        :return: "CHAN1" or "CHAN2"
        :rtype: str
        """
        return self.instrument.query(":TRIG:SHOL:DSRC?")

    def set_shold_csrc(self, source):
        """
        Set the clock source in setup/hold trigger.

        :param source: "CHANNEL1" or "CHANNEL2"
        :type source: str
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

        :return: "CHAN1" or "CHAN2"
        :rtype: str
        """
        return self.instrument.query(":TRIG:SHOL:CSRC?")

    def set_shold_slope(self, slope):
        """
        Set the edge type of the clock in setup/hold trigger.

        :param slope: "POSITIVE" or "NEGATIVE"
        :type slope: str
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

        :return: "POS" or "NEG"
        :rtype: str
        """
        return self.instrument.query(":TRIG:SHOL:SLOP?")

    def set_shold_pattern(self, pattern):
        """
        Set the pattern in setup/hold trigger.

        :param pattern: "SETUP" or "HOLD"
        :type pattern: str
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

        :return: "SETU" or "HOLD"
        :rtype: str
        """
        return self.instrument.query(":TRIG:SHOL:PATT?")

    def set_shold_type(self, typ):
        """
        Set the trigger type in setup/hold trigger.

        :param typ: "GREATER" or "LESS"
        :type typ: str
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

        :return: "GREA" or "LESS"
        :rtype: str
        """
        return self.instrument.query(":TRIG:SHOL:TYPE?")

    def set_shold_stime(self, time):
        """
        Set the setup time in setup/hold trigger (seconds).

        :param time: Setup time in seconds
        :type time: float


        """
        self.instrument.write(f":TRIG:SHOL:STIM {time}")

    def get_shold_stime(self):
        """
        Query the setup time in setup/hold trigger (seconds).



        :return: Setup time in seconds
        :rtype: float or str
        """
        resp = self.instrument.query(":TRIG:SHOL:STIM?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_shold_htime(self, time):
        """
        Set the hold time in setup/hold trigger (seconds).

        :param time: Hold time in seconds
        :type time: float


        """
        self.instrument.write(f":TRIG:SHOL:HTIM {time}")

    def get_shold_htime(self):
        """
        Query the hold time in setup/hold trigger (seconds).



        :return: Hold time in seconds
        :rtype: float or str
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

        :param source: "CHANNEL1" or "CHANNEL2"
        :type source: str


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



        :return: "CHAN1" or "CHAN2"
        :rtype: str
        """
        return self.instrument.query(":TRIG:NEDG:SOUR?")

    def set_nedg_slope(self, slope):
        """
        Set the edge type in noise edge trigger.

        :param slope: "POSITIVE", "NEGATIVE", "RFALL"
        :type slope: str


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



        :return: "POS", "NEG", or "RFAL"
        :rtype: str
        """
        return self.instrument.query(":TRIG:NEDG:SLOP?")

    def set_nedg_level(self, level):
        """
        Set the trigger level in noise edge trigger.

        :param level: Level value
        :type level: float


        """
        self.instrument.write(f":TRIG:NEDG:LEV {level}")

    def get_nedg_level(self):
        """
        Query the trigger level in noise edge trigger.



        :return: Level value
        :rtype: float or str
        """
        resp = self.instrument.query(":TRIG:NEDG:LEV?")
        try:
            return float(resp)
        except Exception:
            return resp

    def set_nedg_idle(self, noise):
        """
        The query returns the idle time in scientific notation

        :param noise: Noise value
        :type noise: float


        """
        self.instrument.write(f":TRIG:NEDG:IDLE {noise}")

    def get_nedg_idle(self):
        """
        Query the noise tolerance in noise edge trigger.
       
        :return: Noise value
        :rtype: float or str
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
            """Initalize RS232 trigger commands.
            
            :param instrument: The instrument instance
            :type instrument: Instrument
            :param data_handler: The data handler instance
            :type data_handler: Data_Handler
            """
            self.instrument = instrument
            self.data_handler = data_handler

        def set_source(self, source):
            """
            Set the trigger source in RS232 trigger.

            :param source: "CHANNEL1" or "CHANNEL2"
            :type source: str
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

            :return: "CHAN1" or "CHAN2"
            :rtype: str
            """
            return self.instrument.query(":TRIG:RS232:SOUR?")

        def set_when(self, when):
            """
            Set the trigger condition in RS232 trigger.

            :param when: "START", "STOP", "DATA", "PARITY", "ERROR"
            :type when: str
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

            :return: Condition
            :rtype: str
            """
            return self.instrument.query(":TRIG:RS232:WHEN?")

        def set_parity(self, parity):
            """
            Set the parity in RS232 trigger.

            :param parity: "NONE", "EVEN", or "ODD"
            :type parity: str
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

            :return: Parity
            :rtype: str
            """
            return self.instrument.query(":TRIG:RS232:PAR?")

        def set_stop(self, stop):
            """
            Set the stop bit in RS232 trigger.

            :param stop: Stop bit, one of 1, 1.5, or 2
            :type stop: float
            """
            allowed = {1, 1.5, 2}
            if stop in allowed:
                self.instrument.write(f":TRIG:RS232:STOP {stop}")
            else:
                print("Invalid stop bit. Allowed: 1, 1.5, 2.")

        def get_stop(self):
            """
            Query the stop bit in RS232 trigger.

            :return: Stop bit
            :rtype: float or str
            """
            resp = self.instrument.query(":TRIG:RS232:STOP?")
            try:
                return float(resp)
            except Exception:
                return resp

        def set_data(self, data):
            """
            Set the data width in RS232 trigger.
            
            :param data: Data width, 5 to 8
            :type data: int
            """
            if isinstance(data, int) and 5 <= data <= 8:
                self.instrument.write(f":TRIG:RS232:DATA {data}")
            else:
                print("Invalid data width. Must be integer between 5 and 8.")

        def get_data(self):
            """
            Query the data width in RS232 trigger.
            
            :return: Data width
            :rtype: int or str
            """
            resp = self.instrument.query(":TRIG:RS232:DATA?")
            try:
                return int(resp)
            except Exception:
                return resp

        def set_width(self, width):
            """
            Set the width in RS232 trigger.
            
            :param width: Data width, 5 to 8
            :type width: int
            """
            if isinstance(width, int) and 5 <= width <= 8:
                self.instrument.write(f":TRIG:RS232:WIDT {width}")
            else:
                print("Invalid width. Must be integer between 5 and 8.")

        def get_width(self):
            """
            Query the width in RS232 trigger.
            
            :return: Data width
            :rtype: int or str
            """
            resp = self.instrument.query(":TRIG:RS232:WIDT?")
            try:
                return int(resp)
            except Exception:
                return resp

        def set_baud(self, baud):
            """
            Set the baud rate in RS232 trigger.
            
            :param baud: Baud rate, 110 to 20000000
            :type baud: int
            """
            if isinstance(baud, int) and 110 <= baud <= 20000000:
                self.instrument.write(f":TRIG:RS232:BAUD {baud}")
            else:
                print("Invalid baud rate. Must be integer between 110 and 20000000.")

        def get_baud(self):
            """
            Query the baud rate in RS232 trigger.
            
            :return: Baud rate
            :rtype: int or str
            """
            resp = self.instrument.query(":TRIG:RS232:BAUD?")
            try:
                return int(resp)
            except Exception:
                return resp

        def set_buser(self, buser):
            """
            Set the bus user value in RS232 trigger.
            
            :param buser: User value (see instrument documentation for valid range)
            :type buser: int
            """
            if isinstance(buser, int):
                self.instrument.write(f":TRIG:RS232:BUS {buser}")
            else:
                print("Invalid bus user value. Must be integer.")

        def get_buser(self):
            """
            Query the bus user value in RS232 trigger.
            
            :return: Bus user value
            :rtype: int or str
            """
            resp = self.instrument.query(":TRIG:RS232:BUS?")
            try:
                return int(resp)
            except Exception:
                return resp

        def set_level(self, level):
            """
            Set the trigger level in RS232 trigger.
            
            :param level: Level value
            :type level: float
            """
            self.instrument.write(f":TRIG:RS232:LEV {level}")

        def get_level(self):
            """
            Query the trigger level in RS232 trigger.
            
            :return: Level value
            :rtype: float or str
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
            """Initalize IIC trigger commands.
            
            :param instrument: The instrument instance
            :type instrument: Instrument
            :param data_handler: The data handler instance
            :type data_handler: Data_Handler
            """
            self.instrument = instrument
            self.data_handler = data_handler

        def set_scl(self, source):
            """
            Set the channel source of SCL in I2C trigger.

            :param source: "CHANNEL1" or "CHANNEL2"
            :type source: str
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

            :return: "CHAN1" or "CHAN2"
            :rtype: str
            """
            return self.instrument.query(":TRIG:IIC:SCL?")

        def set_sda(self, source):
            """
            Set the channel source of SDA in I2C trigger.
            
            :param source: "CHANNEL1" or "CHANNEL2"
            :type source: str
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
            
            :return: "CHAN1" or "CHAN2"
            :rtype: str
            """
            return self.instrument.query(":TRIG:IIC:SDA?")

        def set_when(self, trig_type):
            """
            Set the trigger condition in I2C trigger.

            :param trig_type: "START", "RESTART", "STOP", "NACKNOWLEDGE", "ADDRESS", "DATA", "ADATA"
            :type trig_type: str
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

            :return: when
            :rtype: str
            """
            return self.instrument.query(":TRIG:IIC:WHEN?")

        def set_awidth(self, bits):
            """
            Set the address bits when trigger condition is ADDRESS or ADATA.
            
            :param bits: 7, 8, or 10
            :type bits: int
            """
            if bits in [7, 8, 10]:
                self.instrument.write(f":TRIG:IIC:AWIDth {bits}")
            else:
                print("Invalid address width. Allowed: 7, 8, 10.")

        def get_awidth(self):
            """
            Query the address bits for I2C trigger.

            :return: int
            :rtype: int or str
            """
            resp = self.instrument.query(":TRIG:IIC:AWIDth?")
            try:
                return int(resp)
            except Exception:
                return resp

        def set_address(self, adr):
            """
            Set the address for ADDRESS or ADATA trigger.
            
            :param adr: 0 to 1023 (depends on address width)
            :type adr: int
            """
            if isinstance(adr, int) and 0 <= adr <= 1023:
                self.instrument.write(f":TRIG:IIC:ADDRess {adr}")
            else:
                print("Invalid address value.")

        def get_address(self):
            """
            Query the address for I2C trigger.

            :return: int
            :rtype: int or str
            """
            resp = self.instrument.query(":TRIG:IIC:ADDRess?")
            try:
                return int(resp)
            except Exception:
                return resp

        def set_direction(self, direction):
            """
            Set the data direction for ADDRESS or ADATA trigger.
            
            :param direction: "READ", "WRITE", or "RWRITE"
            :type direction: str
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
            
            :return: str
            :rtype: str
            """
            return self.instrument.query(":TRIG:IIC:DIRection?")

        def set_data(self, data):
            """
            Set the data for DATA or ADATA trigger.
            
            :param data: 0 to 2^40-1 (max 40 bits)
            :type data: int
            """
            if isinstance(data, int) and 0 <= data < 2**40:
                self.instrument.write(f":TRIG:IIC:DATA {data}")
            else:
                print("Invalid data value.")

        def get_data(self):
            """
            Query the data for I2C trigger.
            
            :return: int
            :rtype: int or str
            """
            resp = self.instrument.query(":TRIG:IIC:DATA?")
            try:
                return int(resp)
            except Exception:
                return resp

        def set_clevel(self, level):
            """
            Set the trigger level of SCL in I2C trigger.
            
            :param level: Level value
            :type level: float
            """
            self.instrument.write(f":TRIG:IIC:CLEVel {level}")

        def get_clevel(self):
            """
            Query the trigger level of SCL in I2C trigger.
            
            :return: float
            :rtype: float
            """
            resp = self.instrument.query(":TRIG:IIC:CLEVel?")
            try:
                return float(resp)
            except Exception:
                return resp

        def set_dlevel(self, level):
            """
            Set the trigger level of SDA in I2C trigger.
            
            :param level: Level value
            :type level: float
            """
            self.instrument.write(f":TRIG:IIC:DLEVel {level}")

        def get_dlevel(self):
            """
            Query the trigger level of SDA in I2C trigger.
            
            :return: float
            :rtype: float
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
            """Initalize SPI trigger commands.
            
            :param instrument: The instrument instance
            :type instrument: Instrument
            :param data_handler: The data handler instance
            :type data_handler: Data_Handler
            """
            self.instrument = instrument
            self.data_handler = data_handler

        def set_scl(self, source):
            """
            Set the channel source of SCL in SPI trigger.
            
            :param source: "CHANNEL1" or "CHANNEL2"
            :type source: str
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
            
            :return: "CHAN1" or "CHAN2"
            :rtype: str
            """
            return self.instrument.query(":TRIG:SPI:SCL?")

        def set_sda(self, source):
            """
            Set the channel source of SDA in SPI trigger.
            
            :param source: "CHANNEL1" or "CHANNEL2"
            :type source: str
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
            
            :return: "CHAN1" or "CHAN2"
            :rtype: str
            """
            return self.instrument.query(":TRIG:SPI:SDA?")

        def set_when(self, trig_type):
            """
            Set the trigger condition in SPI trigger.
            
            :param trig_type: "CS" or "TIMEOUT"
            :type trig_type: str
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
            
            :return: str
            :rtype: str
            """
            return self.instrument.query(":TRIG:SPI:WHEN?")

        def set_width(self, width):
            """
            Set the data bits of the SDA channel in SPI trigger.
            
            :param width: 4 to 32
            :type width: int
            """
            if isinstance(width, int) and 4 <= width <= 32:
                self.instrument.write(f":TRIG:SPI:WIDTh {width}")
            else:
                print("Invalid width. Must be integer between 4 and 32.")

        def get_width(self):
            """
            Query the data bits of the SDA channel in SPI trigger.
            
            :return: int
            :rtype: int or str
            """
            resp = self.instrument.query(":TRIG:SPI:WIDTh?")
            try:
                return int(resp)
            except Exception:
                return resp

        def set_data(self, data):
            """
            Set the data in SPI trigger.

            :param data: 0 to 2^32-1
            :type data: int
            """
            if isinstance(data, int) and 0 <= data < 2**32:
                self.instrument.write(f":TRIG:SPI:DATA {data}")
            else:
                print("Invalid data value.")

        def get_data(self):
            """
            Query the data in SPI trigger.

            :return: int
            :rtype: int or str
            """
            resp = self.instrument.query(":TRIG:SPI:DATA?")
            try:
                return int(resp)
            except Exception:
                return resp

        def set_timeout(self, time_value):
            """
            Set the timeout value in SPI trigger (seconds).

            :param  time_value: 100e-9 to 1
            :type time_value: float
            """
            if isinstance(time_value, (float, int)) and 1e-7 <= time_value <= 1:
                self.instrument.write(f":TRIG:SPI:TIMeout {time_value}")
            else:
                print("Invalid timeout value. Must be between 100ns and 1s.")

        def get_timeout(self):
            """
            Query the timeout value in SPI trigger.
            
            :return: Timeout value
            :rtype: float or str
            """
            resp = self.instrument.query(":TRIG:SPI:TIMeout?")
            try:
                return float(resp)
            except Exception:
                return resp

        def set_slope(self, slope):
            """
            Set the clock edge in SPI trigger.
            
            :param slope: "POSITIVE" or "NEGATIVE"
            :type slope: str
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
            
            :param clockedge: "POS" or "NEG"
            :rtype: str
            """
            return self.instrument.query(":TRIG:SPI:SLOPe?")

        def set_clevel(self, level):
            """
            Set the trigger level of the SCL channel in SPI trigger.


            :param level: Level value
            :type level: float
            """
            self.instrument.write(f":TRIG:SPI:CLEVel {level}")

        def get_clevel(self):
            """
            Query the trigger level of the SCL channel in SPI trigger.
            
            :return: float
            :rtype: float
            """
            resp = self.instrument.query(":TRIG:SPI:CLEVel?")
            try:
                return float(resp)
            except Exception:
                return resp

        def set_dlevel(self, level):
            """
            Set the trigger level of the SDA channel in SPI trigger.

            :param level: Level value
            :type level: float
            """
            self.instrument.write(f":TRIG:SPI:DLEVel {level}")

        def get_dlevel(self):
            """
            Query the trigger level of the SDA channel in SPI trigger.
            
            :return: float
            :rtype: float
            """
            resp = self.instrument.query(":TRIG:SPI:DLEVel?")
            try:
                return float(resp)
            except Exception:
                return resp

        def set_slevel(self, level):
            """
            Set the trigger level of the CS channel in SPI trigger.

            :param level: Level value
            :type level: float
            """
            self.instrument.write(f":TRIG:SPI:SLEVel {level}")

        def get_slevel(self):
            """
            Query the trigger level of the CS channel in SPI trigger.

            :return: float
            :rtype: float
            """
            resp = self.instrument.query(":TRIG:SPI:SLEVel?")
            try:
                return float(resp)
            except Exception:
                return resp

        def set_mode(self, mode):
            """
            Set the CS mode when trigger condition is CS in SPI trigger.

            :param mode: "HIGH" or "LOW"
            :type mode: str
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

            :return: "HIGH" or "LOW"
            :rtype: str
            """
            return self.instrument.query(":TRIG:SPI:MODE?")

        def set_cs(self, source):
            """
            Set the data source of the CS signal in SPI trigger.

            :param source: "CHANNEL1" or "CHANNEL2"
            :type source: str
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

            :return: "CHAN1" or "CHAN2"
            :rtype: str
            """
            return self.instrument.query(":TRIG:SPI:CS?")
class Waveform:
    """The Waveform commands are used to read the waveform data and its related settings.
    """
    def __init__(self, instrument,data_handler):
        """Initialize Waveform commands.
        
        :param instrument: The instrument instance
        :type instrument: Instrument
        :param data_handler: The data handler instance
        :type data_handler: Data_Handler
        """
        self.instrument = instrument
        self.data_handler = data_handler

    def set_source(self, source):
        """Set the channel of which the waveform data will be read.

        :param source: "CHANnel1", "CHANnel2", or "MATH"
        :type source: str
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

        :return: "CHAN1", "CHAN2", or "MATH"
        :rtype: str
        """
        return self.instrument.query(":WAVeform:SOURce?")

    def set_mode(self, mode):
        """
        Set the reading mode used by :WAVeform:DATA?.

        :param mode: "NORMal", "MAXimum", or "RAW"
        :type mode: str
        
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
        
        
        
        :return: "NORM", "MAX", or "RAW"
        :rtype: str
        """
        return self.instrument.query(":WAVeform:MODE?")

    def set_format(self, fmt):
        """Set the return format of the waveform data.
        
        :param fmt: "WORD", "BYTE", or "ASCii"
        :type fmt: str
        
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

        

        :return: "WORD", "BYTE", or "ASC"
        :rtype: str
        """
        return self.instrument.query(":WAVeform:FORMat?")

    def get_data(self):
        """Read the waveform data. If autosave is on, then also saves them to a csv file.
        
        
        
        :return: Raw waveform data (format depends on :WAVeform:FORMat)
        :rtype: str or bytes
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
        
        :param sta: Start point (see documentation for valid range)
        :type sta: int
        
        """
        if isinstance(sta, int) and sta >= 1:
            self.instrument.write(f":WAVeform:STARt {sta}")
        else:
            print("Invalid start point. Must be integer >= 1.")

    def get_start(self):
        """Query the start point of waveform data reading.
        
        
        
        :return: Start point
        :rtype: int
        """
        resp = self.instrument.query(":WAVeform:STARt?")
        try:
            return int(resp)
        except Exception:
            return resp

    def set_stop(self, stop):
        """Set the stop point of waveform data reading.
        
        :param stop: Stop point (see documentation for valid range)
        :type stop: int
        """
        if isinstance(stop, int) and stop >= 1:
            self.instrument.write(f":WAVeform:STOP {stop}")
        else:
            print("Invalid stop point. Must be integer >= 1.")

    def get_stop(self):
        """Query the stop point of waveform data reading.
        
        
        
        :return: Stop point
        :rtype: int"""
        resp = self.instrument.query(":WAVeform:STOP?")
        try:
            return int(resp)
        except Exception:
            return resp

    def get_xincrement(self):
        """Query the time difference between two neighboring points of the specified channel source in the X direction.
        
        
        
        :return: X increment (seconds or Hz)
        :rtype: float
        """
        resp = self.instrument.query(":WAVeform:XINCrement?")
        try:
            return float(resp)
        except Exception:
            return resp

    def get_xorigin(self):
        """Query the start time of the waveform data of the channel source currently selected in the X direction.
        
        
        
        :return: float: X origin (seconds or Hz)
        :rtype: float
        """
        resp = self.instrument.query(":WAVeform:XORigin?")
        try:
            return float(resp)
        except Exception:
            return resp

    def get_xreference(self):
        """Query the reference time of the specified channel source in the X direction.
        
        
        
        :return: X reference (usually 0)
        :rtype: int
        """
        resp = self.instrument.query(":WAVeform:XREFerence?")
        try:
            return int(resp)
        except Exception:
            return resp

    def get_yincrement(self):
        """Query the waveform increment of the specified channel source in the Y direction.
        
        :return: Y increment (amplitude unit)
        :rtype: float
        """
        resp = self.instrument.query(":WAVeform:YINCrement?")
        try:
            return float(resp)
        except Exception:
            return resp

    def get_yorigin(self):
        """
        Query the vertical offset relative to the vertical reference position of the specified channel source in the Y direction.
        
        :return: Y origin
        :rtype: int
        """
        resp = self.instrument.query(":WAVeform:YORigin?")
        try:
            return int(resp)
        except Exception:
            return resp

    def get_yreference(self):
        """Query the vertical reference position of the specified channel source in the Y direction.
        
        :return: Y reference (usually 127)
        :rtype: int
        """
        resp = self.instrument.query(":WAVeform:YREFerence?")
        try:
            return int(resp)
        except Exception:
            return resp

    def get_preamble(self):
        """Query and return all the waveform parameters.
        
        :return: 10 waveform parameters separated by commas
        :rtype: str
        """
        return self.instrument.query(":WAVeform:PREamble?")