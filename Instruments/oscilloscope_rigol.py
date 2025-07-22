
from time import sleep
from time import sleep
from EFileType import EFileType
from Instruments import Instrument
import pyvisa
from EInstrument import EInstrument
from PIL import Image
class Oscilloscope(Instrument.Instrument):

    def __init__(self, instru):
        super().__init__(instru)
        self.name = EInstrument.OSCILLOSCOPE
        
    def autoscale(self):
        """Enable the waveform auto setting function. The oscilloscope will automatically adjust the
vertical scale, horizontal timebase, and trigger mode according to the input signal to
realize optimum waveform display"""
        self.instrument.write(":AUT")
    
    def clear(self):
        """Clear all the waveforms on the screen. If the oscilloscope is in the RUN state, waveform
will still be displayed."""
        self.instrument.write(":CLE")
        #instrument.clear_display_window_graphics()
    def run(self):
        """Start collecting measurements."""
        self.instrument.write(":RUN")
    def stop(self):
        """Stop collecting measurements."""
        self.instrument.write(":STOP")
 #Acquisition Commands
    def set_acquistion_mode(self, mode):
        """Set acquisition mode. Normal:  Samples the signal at equal time interval to
rebuild the waveform. Averages:  Averages the waveforms from multiple
samples to reduce the random noise of the input signal. Peak: Acquires the maximum and
minimum values of the signal within the sample interval to get the envelope of the
signal. HRESolution:  ultra-sample technique to average the neighboring points of the sample waveform to reduce the random noise
on the input signal and generate much smoother waveforms """
        comm_mode = ":ACQuire:TYPE "+mode
        self.instrument.write(comm_mode)

    def get_acquistion_mode(self):
        """Get acquisition mode. Normal:  Samples the signal at equal time interval to
rebuild the waveform. Averages:  Averages the waveforms from multiple
samples to reduce the random noise of the input signal. Peak: Acquires the maximum and
minimum values of the signal within the sample interval to get the envelope of the
signal. HRESolution:  ultra-sample technique to average the neighboring points of the sample waveform to reduce the random noise
on the input signal and generate much smoother waveforms """
        comm_mode = ":ACQuire:TYPE?"
        return self.instrument.query(comm_mode)

    def set_number_of_averages(self, avg):
        """In the average acquisition mode, greater number of averages can lower the noise
        and increase the vertical resolution, but will also slow the response of the displayed
        waveform to the waveform changes. Avg: 2 to 1024"""
        if avg<2 or avg>1024:
            print("Average is an invalid value. Please enter a number between 2 and 1024")
        else:
            comm_mode = ":ACQuire:AVERages "+avg
            self.instrument.write(comm_mode)

    def get_number_of_averages(self):
        """In the average acquisition mode, greater number of averages can lower the noise
        and increase the vertical resolution."""
        comm_mode = ":ACQuire:AVERages?"
        return self.instrument.query(comm_mode)
    
    def set_memory_depth(self, mdpth):
        """ Set memory depth of the oscilloscope (namely the number of waveform
points that can be stored in a single trigger sample). Single Channel: AUTO|12000|
120000|1200000|12000000|24000000. Dual Channel:  {AUTO|6000|60000|
600000|6000000|12000000}."""
#TODO: Add in check of channel status
        sc_allowed_values = ["AUTO",12000,120000,1200000,12000000,24000000]
        dc_allowed_values = ["AUTO",6000,60000,600000,6000000,12000000]
        if mdpth in sc_allowed_values or mdpth in dc_allowed_values:
            comm_mode = ":ACQuire:MDEPth "+mdpth
            self.instrument.write(comm_mode)
        else:
            print("Invalid memory depth.")

    def get_memory_depth(self):
        """ Get memory depth of the oscilloscope (namely the number of waveform
points that can be stored in a single trigger sample)."""
        comm_mode = ":ACQuire:MDEPth?"
        return self.instrument.query(comm_mode)

   
    def get_sample_rate(self):
        """ Query the current sample rate. The default unit is Sa/s."""
        comm_mode = ":ACQuire:SRATe?"
        return self.instrument.query(comm_mode)

#Channel Commands
    def set_channel_bandwidth_limit(self, channel, bw):
        """ Set or query the bandwidth limit parameter of the specified channel. OFF: disable the bandwidth limit and the high frequency components of the signal
under test can pass the channel.
20M: enable the bandwidth limit and the high frequency components of the signal
under test that exceed 20 MHz are attenuated. """
#TODO: Add in check of channel status
        allowed_chnl_values = [1, 2]
        allowed_type_values = ["20M", "OFF"]
        if channel in allowed_chnl_values or bw in allowed_type_values:
            comm = ":CHANnel"+str(channel)+":BWLimit "+bw
            self.instrument.write(comm)
        else:
            print("Invalid channel or bandwidth.")

    def get_channel_bandwidth_limit(self, channel):
        """ Query the bandwidth limit parameter of the specified channel."""
        comm_mode = ":CHANnel"+str(channel)+":BWLimit?"
        return self.instrument.query(comm_mode)

    def set_channel_coupling_mode(self, channel, coupling_mode):
        """ Set the coupling mode of the specified channel."""
#TODO: Add in check of channel status
        allowed_chnl_values = [1, 2]
        allowed_type_values = ["AC","DC","GND"]
        if channel in allowed_chnl_values or bw in allowed_type_values:
            comm = ":CHANnel"+str(channel)+":COUPling "+coupling_mode
            self.instrument.write(comm)
        else:
            print("Invalid channel or bandwidth.")

    def get_channel_coupling_mode(self, channel):
        """ Query the coupling mode of the specified channel."""
        comm_mode = ":CHANnel"+str(channel)+":COUPling?"
        return self.instrument.query(comm_mode)
    
    def channel_invert_waveform(self, channel, param1):
        """ Set the coupling mode of the specified channel."""
        #TODO: Add in check of channel status
        allowed_chnl_values = [1, 2]
        allowed_type_values = ["ON","OFF",1, 2]
        if channel in allowed_chnl_values or param1 in allowed_type_values:
            comm = ":CHANnel"+str(channel)+":INVert "+param1
            self.instrument.write(comm)
        else:
            print("Invalid channel or bandwidth.")

    def channel_is_inverted(self, channel):
        """ Query the coupling mode of the specified channel."""
        comm_mode = ":CHANnel"+str(channel)+":INVert?"
        return self.instrument.query(comm_mode)
    
    def set_channel_offset(self, channel, param1):
        """ Set the vertical offset of the specified channel. The default unit is V."""
    #TODO: Add in check of channel status
        allowed_chnl_values = [1, 2]
        #allowed_type_values = ["AC","DC","GND"]
        if channel in allowed_chnl_values: #or param1 in allowed_type_values:
            comm = ":CHANnel"+str(channel)+":OFFSet "+param1
            self.instrument.write(comm)
        else:
            print("Invalid channel or bandwidth.")

    def get_channel_offset(self, channel):
        """ Query the vertical offset of the specified channel. The default unit is V."""
        comm_mode = ":CHANnel"+str(channel)+":OFFSet?"
        return self.instrument.query(comm_mode)
    
    def set_channel_range(self, channel, param1):
        """ Set the vertical offset of the specified channel. The default unit is V."""
    #TODO: Add in check of channel status
        allowed_chnl_values = [1, 2]
        #allowed_type_values = ["AC","DC","GND"]
        if channel in allowed_chnl_values: #or param1 in allowed_type_values:
            comm = ":CHANnel"+str(channel)+":OFFSet "+param1
            self.instrument.write(comm)
        else:
            print("Invalid channel or bandwidth.")

    def get_channel_range(self, channel):
        """ Query the vertical offset of the specified channel. The default unit is V."""
        comm_mode = ":CHANnel"+str(channel)+":OFFSet?"
        return self.instrument.query(comm_mode)
    
    def set_channel_tcal(self, channel, val):
        """
        Set delay calibration time for the specified channel.
        val: delay time in seconds (e.g., 20e-9 for 20ns). Valid range: -100e-9 to 100e-9.
        NOTE: Must match timing step for current timebase scale; oscilloscope rounds if needed.
        """
        if channel in [1, 2] and isinstance(val, (float, int)) and -100e-9 <= val <= 100e-9:
            self.instrument.write(f":CHANnel{channel}:TCAL {val}")
        else:
            print("Invalid channel or value (must be float between -100e-9 and 100e-9)")

    def get_channel_tcal(self, channel):
        """
        Query delay calibration time for the specified channel (in seconds).
        Returns value in scientific notation as float.
        """
        if channel in [1, 2]:
            response = self.instrument.query(f":CHANnel{channel}:TCAL?")
            return float(response)
        else:
            print("Invalid channel number.")
            return None
    
    def set_channel_scale(self, channel, scale):
        """Set vertical scale of the channel (in V/div)."""
        self.instrument.write(f":CHANnel{channel}:SCALe {scale}")

    def get_channel_scale(self, channel):
        """Query vertical scale of the channel."""
        return self.instrument.query(f":CHANnel{channel}:SCALe?")

    def set_probe_ratio(self, channel, ratio):
        """Set the probe attenuation ratio for a channel."""
        self.instrument.write(f":CHANnel{channel}:PROBe {ratio}")

    def get_probe_ratio(self, channel):
        """Query the probe attenuation ratio for a channel."""
        return self.instrument.query(f":CHANnel{channel}:PROBe?")

    def set_channel_units(self, channel, unit):
        """Set the amplitude display unit for a channel. Options: VOLTage, WATT, AMPere, UNKNown."""
        self.instrument.write(f":CHANnel{channel}:UNITs {unit}")

    def get_channel_units(self, channel):
        """Query the amplitude display unit for a channel."""
        return self.instrument.query(f":CHANnel{channel}:UNITs?")

    def set_vernier(self, channel, state):
        """Enable or disable fine adjustment (vernier) for vertical scale. By default, the fine adjustment is off. At this point, you can only set the vertical scale in
1-2-5 step, namely 10mV, 20mV, 50mV, 100mV…100V (the probe ratio is 10X). When the
fine adjustment is on, you can further adjust the vertical scale within a relatively smaller
range to improve the vertical resolution. If the amplitude of the input waveform is a little
bit greater than the full scale under the current scale and the amplitude would be a little
bit lower if the next scale is used, fine adjustment can be used to improve the display
amplitude of the waveform to view the signal details. State: {{1|ON}|{0|OFF}}"""
        self.instrument.write(f":CHANnel{channel}:VERNier {state}")

    def get_vernier(self, channel):
        """Query vernier setting."""
        return self.instrument.query(f":CHANnel{channel}:VERNier?")
    

#Cursor Commands
    def set_cursor_mode(self, mode):
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

    def get_cursor_mode(self):
        """
        Query the current cursor measurement mode.

        Returns:
        str: One of {"OFF", "MAN", "TRAC", "AUTO", "XY"}
        """
        return self.instrument.query(":CURSor:MODE?")
    
    def set_cursor_manual_type(self, cursor_type):
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
    
    def get_cursor_manual_type(self):
        """
        Query the current manual cursor type.

        Returns:
        str: "X" or "Y"
        """
        return self.instrument.query(":CURSor:MANual:TYPE?")

    def get_cursor_manual_source(self):
        """
        Query the current source for manual cursor measurement.

        Returns:
        str: Current source, such as "CHAN1", "CHAN2", "MATH", etc.
        """
        return self.instrument.query(":CURSor:MANual:SOURce?")
    
    def set_cursor_manual_source(self, source):
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

    def get_cursor_manual_source(self):
        """
        Query the current source for manual cursor measurement.

        Returns:
        str: Current source, such as "CHAN1", "CHAN2", "MATH", etc.
        """
        return self.instrument.query(":CURSor:MANual:SOURce?")

    def get_cursor_manual_tunit(self):
        """ Query the current horizontal unit in the manual cursor measurement mode. """
        return self.instrument.query(":CURSor:MANual:TUNit?")

    def set_cursor_manual_tunit(self, unit):
        """ Set the horizontal unit for manual cursor measurement. """
        valid_units = ["S", "HZ", "DEGRee", "PERCent"]
        unit = unit.upper()
        if unit in valid_units:
            self.instrument.write(f":CURSor:MANual:TUNit {unit}")
        else:
            print(f"Invalid unit. Valid options are: {valid_units}")
    def get_cursor_manual_vunit(self):
        """ Query the current vertical unit in the manual cursor measurement mode. """
        return self.instrument.query(":CURSor:MANual:VUNit?")

    def set_cursor_manual_vunit(self, unit):
        """ Set the vertical unit for manual cursor measurement. """
        valid_units = ["PERCent", "SOURce"]
        unit = unit.upper()
        if unit in valid_units:
            self.instrument.write(f":CURSor:MANual:VUNit {unit}")
        else:
            print(f"Invalid unit. Valid options are: {valid_units}")

    def set_cursor_manual(self, cursor, x, y):
        """ Set the horizontal position of cursor A or B  in the manual cursor measurement mode. """
        if 5 <= x <= 594:  # Ensure the position is within the valid range
            self.instrument.write(f":CURSor:MANual:"+cursor+"X {x}")
        else:
            print("Invalid position. x must be between 5 and 594.")
        
        if 5 <= y <= 394:  # Ensure the position is within the valid range
            self.instrument.write(f":CURSor:MANual:"+cursor+"Y {y}")
        else:
            print("Invalid position. y must be between 5 and 394.")

    def get_cursor_manual(self,cursor):
        """ Query the horizontal position of cursor A or B in the manual cursor measurement mode. """
        return self.instrument.query(":CURSor:MANual:"+cursor+"X?;"+cursor+"Y?")

    def get_cursor_manual_xdelta(self):
        """ Query the difference between the X values of cursor A and cursor B (BX - AX) in the manual cursor measurement mode. """
        response = self.instrument.query(":CURSor:MANual:XDELta?")
        return float(response)  # Returns the difference in scientific notation

    def get_cursor_manual_xdelta(self):
        """ Query the reciprocal of the absolute value of the difference between the X values of cursor A and cursor B (1/|dX|). """
        response = self.instrument.query(":CURSor:MANual:IXDELta?")
        return float(response)  # Returns the reciprocal in scientific notation
    
    def get_cursor_manual_ydelta(self):
        """ Query the difference between the Y values of cursor A and cursor B (BY - AY) in the manual cursor measurement mode. """
        response = self.instrument.query(":CURSor:MANual:YDELta?")
        return float(response)  # Returns the difference in scientific notation

    def set_cursor_track_source(self, source, n):
        """ Set the channel source of cursor A in the track cursor measurement mode. """
        valid_sources = ["OFF", "CHANnel1", "CHANnel2", "MATH"]
        source = source.upper()  # Ensure source is in uppercase

        if source in valid_sources:
            self.instrument.write(f":CURSor:TRACk:SOURce"+str(n)+ " {source}")
        else:
            print(f"Invalid source. Choose from: {valid_sources}")

    def get_cursor_track_source(self, n):
        """ Query the channel source of cursor A in the track cursor measurement mode. """
        return self.instrument.query(":CURSor:TRACk:SOURce"+str(n)+"?")
    
    def set_cursor_xy(self, cursor, x, y):
        """ Set the horizontal position of cursor A in the XY cursor measurement mode. """
        if 5 <= x <= 394 and 5 <= y <= 394:
            self.instrument.write(f":CURSor:XY:"+cursor+"X {x};"+cursor+"Y {y};")
        else:
            print("Invalid x or y position. Must be between 5 and 394.")

    def get_cursor_xy(self, cursor):
        """ Query the horizontal position of cursor A in the XY cursor measurement mode. """
        response = self.instrument.query(":CURSor:XY:)"+cursor+"X?;"+cursor+"Y?")
        return response # Returns an integer between 5 and 394

#Decoding Commands
    def set_decoder_mode(self, n, mode):
        """
        Set the decoder type for the specified decoder channel.
        
        Parameters:
        n (int): The decoder channel, either 1 or 2.
        mode (str): The decoder type, one of {"PARallel", "UART", "SPI", "IIC"}.
        """
        valid_decoders = [1, 2]
        valid_modes = ["PARallel", "UART", "SPI", "IIC"]

        if n in valid_decoders and mode.upper() in valid_modes:
            self.instrument.write(f":DECoder{n}:MODE {mode.upper()}")
        else:
            print(f"Invalid decoder or mode. Decoder: {valid_decoders}, Mode: {valid_modes}")

    def get_decoder_mode(self, n):
        """
        Query the decoder type for the specified decoder channel.
        
        Parameters:
        n (int): The decoder channel, either 1 or 2.
        
        Returns:
        str: The decoder type, one of {"PAR", "UART", "SPI", "IIC"}.
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:MODE?")
            return response.strip().upper()  # Returns the mode (e.g., PAR, UART, SPI, IIC)
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None

    def set_decoder_display(self, n, display_status):
        """
        Turn on or off the decoder or query the status of the decoder.
        
        Parameters:
        n (int): The decoder channel, either 1 or 2.
        display_status (bool or str): Whether to turn on (True/1/"ON") or off (False/0/"OFF") the decoder.
        """
        valid_decoders = [1, 2]
        
        # Handle different input types
        if isinstance(display_status, bool):
            status = "ON" if display_status else "OFF"
        elif isinstance(display_status, (int, str)):
            if str(display_status).upper() in ["1", "ON"]:
                status = "ON"
            elif str(display_status).upper() in ["0", "OFF"]:
                status = "OFF"
            else:
                print("Invalid display status. Use True/False, 1/0, or 'ON'/'OFF'.")
                return
        else:
            print("Invalid display status. Use True/False, 1/0, or 'ON'/'OFF'.")
            return
        
        if n in valid_decoders:
            self.instrument.write(f":DECoder{n}:DISPlay {status}")
        else:
            print(f"Invalid decoder. Choose from {valid_decoders}.")

    def get_decoder_display(self, n):
        """
        Query the status of the decoder.
        
        Parameters:
        n (int): The decoder channel, either 1 or 2.
        
        Returns:
        int: The status of the decoder (1 for ON, 0 for OFF).
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:DISPlay?")
            return int(response.strip())  # Returns 1 for ON, 0 for OFF
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None
        
    def set_decoder_format(self, n, fmt):
        """
        Set the bus display format for the specified decoder channel.
        
        Parameters:
        n (int): The decoder channel, either 1 or 2.
        fmt (str): The bus display format, one of {"HEX", "ASCii", "DEC", "BIN", "LINE"}.
        """
        valid_decoders = [1, 2]
        valid_formats = ["HEX", "ASCii", "DEC", "BIN", "LINE"]

        if n in valid_decoders and fmt.upper() in valid_formats:
            self.instrument.write(f":DECoder{n}:FORMat {fmt.upper()}")
        else:
            print(f"Invalid decoder or format. Decoder: {valid_decoders}, Format: {valid_formats}")

    def get_decoder_format(self, n):
        """
        Query the bus display format for the specified decoder channel.
        
        Parameters:
        n (int): The decoder channel, either 1 or 2.
        
        Returns:
        str: The bus display format, one of {"HEX", "ASC", "DEC", "BIN", "LINE"}.
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:FORMat?")
            return response.strip().upper()  # Returns the format (e.g., HEX, ASC, DEC, BIN, LINE)
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None
    
    def set_decoder_position(self, n, pos):
        """
        Set the vertical position of the bus on the screen for the specified decoder.
        
        Parameters:
        n (int): The decoder channel, either 1 or 2.
        pos (int): The vertical position, range 50 to 350.
        """
        valid_decoders = [1, 2]
        if n in valid_decoders and 50 <= pos <= 350:
            self.instrument.write(f":DECoder{n}:POSition {pos}")
        else:
            print(f"Invalid decoder or position. Decoder: {valid_decoders}, Position: 50-350")

    def get_decoder_position(self, n):
        """
        Query the vertical position of the bus on the screen for the specified decoder.
        
        Parameters:
        n (int): The decoder channel, either 1 or 2.
        
        Returns:
        int: The vertical position (integer between 50 and 350).
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:POSition?")
            return int(response.strip())  # Returns the position as an integer
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None
        
    def set_decoder_threshold_channel(self, channel, n, thre):
        """
        Set the threshold level for the specified decoder channel 1.
        
        Parameters:
        n (int): The decoder channel, either 1 or 2.
        thre (float): The threshold level, in volts. Should be within the range of the vertical scale and offset.
        """
        valid_decoders = [1, 2]
        if n in valid_decoders:
            self.instrument.write(f":DECoder{n}:THREshold:CHANnel"+channel+" {thre}")
        else:
            print(f"Invalid decoder. Choose from {valid_decoders}.")

    def get_decoder_threshold_channel(self, channel, n):
        """
        Query the threshold level for the specified decoder channel 1 or 2.
        
        Parameters:
        n (int): The decoder channel, either 1 or 2.
        
        Returns:
        float: The threshold level in scientific notation (volts).
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:THREshold:CHANnel1?")
            return float(response.strip())  # Returns the threshold level as a float
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None
    def set_decoder_auto_threshold(self, n, auto):
        """
        Turn on or off the auto threshold function for the specified decoder channel.
        
        Parameters:
        n (int): The decoder channel, either 1 or 2.
        auto (bool): Whether to turn on (1) or off (0) the auto threshold function.
        """
        valid_decoders = [1, 2]
        if n in valid_decoders:
            self.instrument.write(f":DECoder{n}:THREshold:AUTO {'ON' if auto else 'OFF'}")
        else:
            print(f"Invalid decoder. Choose from {valid_decoders}.")

    def get_decoder_auto_threshold(self, n):
        """
        Query the status of the auto threshold function for the specified decoder channel.
        
        Parameters:
        n (int): The decoder channel, either 1 or 2.
        
        Returns:
        bool: The status of the auto threshold function (1 for ON, 0 for OFF).
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:THREshold:AUTO?")
            return int(response.strip())  # Returns 1 for ON, 0 for OFF
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None
    def set_decoder_label_display(self, n, label_status):
        """
        Turn on or off the label display function for the specified decoder.
        
        Parameters:
        n (int): The decoder channel, either 1 or 2.
        label_status (bool): Whether to turn on (1) or off (0) the label display function.
        """
        valid_decoders = [1, 2]
        if n in valid_decoders:
            self.instrument.write(f":DECoder{n}:CONFig:LABel {'ON' if label_status else 'OFF'}")
        else:
            print(f"Invalid decoder. Choose from {valid_decoders}.")

    def get_decoder_label_display(self, n):
        """
        Query the status of the label display function for the specified decoder.
        
        Parameters:
        n (int): The decoder channel, either 1 or 2.
        
        Returns:
        bool: The status of the label display function (1 for ON, 0 for OFF).
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:CONFig:LABel?")
            return int(response.strip())  # Returns 1 for ON, 0 for OFF
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None

    def set_decoder_bus_display(self, n, line_status):
        """
        Turn on or off the bus display function for the specified decoder.
        
        Parameters:
        n (int): The decoder channel, either 1 or 2.
        line_status (bool): Whether to turn on (1) or off (0) the bus display function.
        """
        valid_decoders = [1, 2]
        if n in valid_decoders:
            self.instrument.write(f":DECoder{n}:CONFig:LINE {'ON' if line_status else 'OFF'}")
        else:
            print(f"Invalid decoder. Choose from {valid_decoders}.")

    def get_decoder_bus_display(self, n):
        """
        Query the status of the bus display function for the specified decoder.
        
        Parameters:
        n (int): The decoder channel, either 1 or 2.
        
        Returns:
        bool: The status of the bus display function (1 for ON, 0 for OFF).
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:CONFig:LINE?")
            return int(response.strip())  # Returns 1 for ON, 0 for OFF
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None

    def set_decoder_format_display(self, n, format_status):
        """
        Turn on or off the format display function for the specified decoder.
        
        Parameters:
        n (int): The decoder channel, either 1 or 2.
        format_status (bool): Whether to turn on (1) or off (0) the format display function.
        """
        valid_decoders = [1, 2]
        if n in valid_decoders:
            self.instrument.write(f":DECoder{n}:CONFig:FORMat {'ON' if format_status else 'OFF'}")
        else:
            print(f"Invalid decoder. Choose from {valid_decoders}.")

    def get_decoder_format_display(self, n):
        """
        Query the status of the format display function for the specified decoder.
        
        Parameters:
        n (int): The decoder channel, either 1 or 2.
        
        Returns:
        bool: The status of the format display function (1 for ON, 0 for OFF).
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:CONFig:FORMat?")
            return int(response.strip())  # Returns 1 for ON, 0 for OFF
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None
    def set_decoder_endian_display(self, n, endian_status):
        """
        Turn on or off the endian display function for the specified decoder.
        
        Parameters:
        n (int): The decoder channel, either 1 or 2.
        endian_status (bool): Whether to turn on (1) or off (0) the endian display function.
        """
        valid_decoders = [1, 2]
        if n in valid_decoders:
            self.instrument.write(f":DECoder{n}:CONFig:ENDian {'ON' if endian_status else 'OFF'}")
        else:
            print(f"Invalid decoder. Choose from {valid_decoders}.")

    def get_decoder_endian_display(self, n):
        """
        Query the status of the endian display function for the specified decoder.
        
        Parameters:
        n (int): The decoder channel, either 1 or 2.
        
        Returns:
        bool: The status of the endian display function (1 for ON, 0 for OFF).
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:CONFig:ENDian?")
            return int(response.strip())  # Returns 1 for ON, 0 for OFF
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None
    def set_decoder_width_display(self, n, width_status):
        """
        Turn on or off the width display function for the specified decoder.
        
        Parameters:
        n (int): The decoder channel, either 1 or 2.
        width_status (bool): Whether to turn on (1) or off (0) the width display function.
        """
        valid_decoders = [1, 2]
        if n in valid_decoders:
            self.instrument.write(f":DECoder{n}:CONFig:WIDth {'ON' if width_status else 'OFF'}")
        else:
            print(f"Invalid decoder. Choose from {valid_decoders}.")

    def get_decoder_width_display(self, n):
        """
        Query the status of the width display function for the specified decoder.
        
        Parameters:
        n (int): The decoder channel, either 1 or 2.
        
        Returns:
        bool: The status of the width display function (1 for ON, 0 for OFF).
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:CONFig:WIDth?")
            return int(response.strip())  # Returns 1 for ON, 0 for OFF
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None
    # UART Decoding Commands
    def set_decoder_uart_tx_source(self, n, tx_source):
        """
        Set the TX channel source of RS232 decoding for the specified decoder.

        Parameters:
        n (int): The decoder channel, either 1 or 2.
        tx_source (str): The TX channel source, one of {"CHANnel1", "CHANnel2", "OFF"}.
        """
        valid_decoders = [1, 2]
        valid_sources = {"CHANnel1", "CHANnel2", "OFF"}
        tx_source = tx_source.upper()

        if n in valid_decoders and tx_source in valid_sources:
            self.instrument.write(f":DECoder{n}:UART:TX {tx_source}")
        else:
            print(f"Invalid decoder ({n}) or TX source ({tx_source}). Decoder: {valid_decoders}, Source: {valid_sources}")

    def get_decoder_uart_tx_source(self, n):
        """
        Query the TX channel source of RS232 decoding for the specified decoder.

        Parameters:
        n (int): The decoder channel, either 1 or 2.

        Returns:
        str: The TX channel source, one of {"CHAN1", "CHAN2", "OFF"}.
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:UART:TX?")
            return response.strip().upper()
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None

    def set_decoder_uart_rx_source(self, n, rx_source):
        """
        Set the RX channel source of RS232 decoding for the specified decoder.

        Parameters:
        n (int): The decoder channel, either 1 or 2.
        rx_source (str): The RX channel source, one of {"CHANnel1", "CHANnel2", "OFF"}.
        """
        valid_decoders = [1, 2]
        valid_sources = {"CHANnel1", "CHANnel2", "OFF"}
        rx_source = rx_source.upper()

        if n in valid_decoders and rx_source in valid_sources:
            self.instrument.write(f":DECoder{n}:UART:RX {rx_source}")
        else:
            print(f"Invalid decoder ({n}) or RX source ({rx_source}). Decoder: {valid_decoders}, Source: {valid_sources}")

    def get_decoder_uart_rx_source(self, n):
        """
        Query the RX channel source of RS232 decoding for the specified decoder.

        Parameters:
        n (int): The decoder channel, either 1 or 2.

        Returns:
        str: The RX channel source, one of {"CHAN1", "CHAN2", "OFF"}.
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:UART:RX?")
            return response.strip().upper()
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None

    def set_decoder_uart_polarity(self, n, polarity):
        """
        Set the polarity of RS232 decoding for the specified decoder.

        Parameters:
        n (int): The decoder channel, either 1 or 2.
        polarity (str): The polarity, one of {"NEGative", "POSitive"}.
        """
        valid_decoders = [1, 2]
        valid_polarities = {"NEGative", "POSitive"}
        polarity = polarity.upper()

        if n in valid_decoders and polarity in valid_polarities:
            self.instrument.write(f":DECoder{n}:UART:POLarity {polarity}")
        else:
            print(f"Invalid decoder ({n}) or polarity ({polarity}). Decoder: {valid_decoders}, Polarity: {valid_polarities}")

    def get_decoder_uart_polarity(self, n):
        """
        Query the polarity of RS232 decoding for the specified decoder.

        Parameters:
        n (int): The decoder channel, either 1 or 2.

        Returns:
        str: The polarity, one of {"NEG", "POS"}.
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:UART:POLarity?")
            return response.strip().upper()
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None

    def set_decoder_uart_endian(self, n, endian):
        """
        Set the endian of RS232 decoding for the specified decoder.

        Parameters:
        n (int): The decoder channel, either 1 or 2.
        endian (str): The endian, one of {"LSB", "MSB"}.
        """
        valid_decoders = [1, 2]
        valid_endians = {"LSB", "MSB"}
        endian = endian.upper()

        if n in valid_decoders and endian in valid_endians:
            self.instrument.write(f":DECoder{n}:UART:ENDian {endian}")
        else:
            print(f"Invalid decoder ({n}) or endian ({endian}). Decoder: {valid_decoders}, Endian: {valid_endians}")

    def get_decoder_uart_endian(self, n):
        """
        Query the endian of RS232 decoding for the specified decoder.

        Parameters:
        n (int): The decoder channel, either 1 or 2.

        Returns:
        str: The endian, one of {"LSB", "MSB"}.
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:UART:ENDian?")
            return response.strip().upper()
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None

    def set_decoder_uart_baud_rate(self, n, baud):
        """
        Set the baud rate of RS232 decoding for the specified decoder.

        Parameters:
        n (int): The decoder channel, either 1 or 2.
        baud (int): The baud rate in bps, from 110 to 20,000,000.
        """
        valid_decoders = [1, 2]
        if n in valid_decoders and isinstance(baud, int) and 110 <= baud <= 20000000:
            self.instrument.write(f":DECoder{n}:UART:BAUD {baud}")
        else:
            print(f"Invalid decoder ({n}) or baud rate ({baud}). Baud rate must be an integer between 110 and 20M.")

    def get_decoder_uart_baud_rate(self, n):
        """
        Query the baud rate of RS232 decoding for the specified decoder.

        Parameters:
        n (int): The decoder channel, either 1 or 2.

        Returns:
        int: The current baud rate.
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:UART:BAUD?")
            return int(response.strip())
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None

    def set_decoder_uart_data_width(self, n, width):
        """
        Set the width of each frame of data in RS232 decoding for the specified decoder.

        Parameters:
        n (int): The decoder channel, either 1 or 2.
        width (int): The data width, from 5 to 8 bits.
        """
        valid_decoders = [1, 2]
        if n in valid_decoders and isinstance(width, int) and 5 <= width <= 8:
            self.instrument.write(f":DECoder{n}:UART:WIDTH {width}")
        else:
            print(f"Invalid decoder ({n}) or width ({width}). Width must be an integer between 5 and 8.")

    def get_decoder_uart_data_width(self, n):
        """
        Query the width of each frame of data in RS232 decoding for the specified decoder.

        Parameters:
        n (int): The decoder channel, either 1 or 2.

        Returns:
        int: The data width.
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:UART:WIDTH?")
            return int(response.strip())
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None

    def set_decoder_uart_stop_bit(self, n, stop_bit):
        """
        Set the stop bit after each frame of data in RS232 decoding for the specified decoder.

        Parameters:
        n (int): The decoder channel, either 1 or 2.
        stop_bit (float): The stop bit value, one of {1, 1.5, 2}.
        """
        valid_decoders = [1, 2]
        valid_stop_bits = {1.0, 1.5, 2.0}
        if n in valid_decoders and stop_bit in valid_stop_bits:
            self.instrument.write(f":DECoder{n}:UART:STOP {stop_bit}")
        else:
            print(f"Invalid decoder ({n}) or stop bit ({stop_bit}). Stop bit must be 1, 1.5, or 2.")

    def get_decoder_uart_stop_bit(self, n):
        """
        Query the stop bit after each frame of data in RS232 decoding for the specified decoder.

        Parameters:
        n (int): The decoder channel, either 1 or 2.

        Returns:
        float: The stop bit value.
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:UART:STOP?")
            return float(response.strip())
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None

    def set_decoder_uart_parity(self, n, parity):
        """
        Set the even-odd check mode of the data transmission in RS232 decoding for the specified decoder.

        Parameters:
        n (int): The decoder channel, either 1 or 2.
        parity (str): The parity mode, one of {"NONE", "EVEN", "ODD"}.
        """
        valid_decoders = [1, 2]
        valid_parities = {"NONE", "EVEN", "ODD"}
        parity = parity.upper()

        if n in valid_decoders and parity in valid_parities:
            self.instrument.write(f":DECoder{n}:UART:PARity {parity}")
        else:
            print(f"Invalid decoder ({n}) or parity ({parity}). Parity: {valid_parities}")

    def get_decoder_uart_parity(self, n):
        """
        Query the even-odd check mode of the data transmission in RS232 decoding for the specified decoder.

        Parameters:
        n (int): The decoder channel, either 1 or 2.

        Returns:
        str: The parity mode, one of {"NONE", "EVEN", "ODD"}.
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:UART:PARity?")
            return response.strip().upper()
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None

    # I2C Decoding Commands
    def set_decoder_iic_clk_source(self, n, clk_source):
        """
        Set the signal source of the clock channel in I2C decoding for the specified decoder.

        Parameters:
        n (int): The decoder channel, either 1 or 2.
        clk_source (str): The clock channel source, one of {"CHANnel1", "CHANnel2"}.
        """
        valid_decoders = [1, 2]
        valid_sources = {"CHANnel1", "CHANnel2"}
        clk_source = clk_source.upper()

        if n in valid_decoders and clk_source in valid_sources:
            self.instrument.write(f":DECoder{n}:IIC:CLK {clk_source}")
        else:
            print(f"Invalid decoder ({n}) or clock source ({clk_source}). Decoder: {valid_decoders}, Source: {valid_sources}")

    def get_decoder_iic_clk_source(self, n):
        """
        Query the signal source of the clock channel in I2C decoding for the specified decoder.

        Parameters:
        n (int): The decoder channel, either 1 or 2.

        Returns:
        str: The clock channel source, one of {"CHAN1", "CHAN2"}.
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:IIC:CLK?")
            return response.strip().upper()
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None

    def set_decoder_iic_data_source(self, n, data_source):
        """
        Set the signal source of the data channel in I2C decoding for the specified decoder.

        Parameters:
        n (int): The decoder channel, either 1 or 2.
        data_source (str): The data channel source, one of {"CHANnel1", "CHANnel2"}.
        """
        valid_decoders = [1, 2]
        valid_sources = {"CHANnel1", "CHANnel2"}
        data_source = data_source.upper()

        if n in valid_decoders and data_source in valid_sources:
            self.instrument.write(f":DECoder{n}:IIC:DATA {data_source}")
        else:
            print(f"Invalid decoder ({n}) or data source ({data_source}). Decoder: {valid_decoders}, Source: {valid_sources}")

    def get_decoder_iic_data_source(self, n):
        """
        Query the signal source of the data channel in I2C decoding for the specified decoder.

        Parameters:
        n (int): The decoder channel, either 1 or 2.

        Returns:
        str: The data channel source, one of {"CHAN1", "CHAN2"}.
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:IIC:DATA?")
            return response.strip().upper()
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None

    def set_decoder_iic_address_mode(self, n, addr_mode):
        """
        Set the address mode of I2C decoding for the specified decoder.

        Parameters:
        n (int): The decoder channel, either 1 or 2.
        addr_mode (str): The address mode, one of {"NORMal", "RW"}.
        """
        valid_decoders = [1, 2]
        valid_modes = {"NORMal", "RW"}
        addr_mode = addr_mode.upper()

        if n in valid_decoders and addr_mode in valid_modes:
            self.instrument.write(f":DECoder{n}:IIC:ADDRess {addr_mode}")
        else:
            print(f"Invalid decoder ({n}) or address mode ({addr_mode}). Decoder: {valid_decoders}, Mode: {valid_modes}")

    def get_decoder_iic_address_mode(self, n):
        """
        Query the address mode of I2C decoding for the specified decoder.

        Parameters:
        n (int): The decoder channel, either 1 or 2.

        Returns:
        str: The address mode, one of {"NORM", "RW"}.
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:IIC:ADDRess?")
            return response.strip().upper()
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None

    # SPI Decoding Commands
    def set_decoder_spi_clk_source(self, n, clk_source):
        """
        Set the signal source of the clock channel in SPI decoding for the specified decoder.

        Parameters:
        n (int): The decoder channel, either 1 or 2.
        clk_source (str): The clock channel source, one of {"CHANnel1", "CHANnel2"}.
        """
        valid_decoders = [1, 2]
        valid_sources = {"CHANnel1", "CHANnel2"}
        clk_source = clk_source.upper()

        if n in valid_decoders and clk_source in valid_sources:
            self.instrument.write(f":DECoder{n}:SPI:CLK {clk_source}")
        else:
            print(f"Invalid decoder ({n}) or clock source ({clk_source}). Decoder: {valid_decoders}, Source: {valid_sources}")

    def get_decoder_spi_clk_source(self, n):
        """
        Query the signal source of the clock channel in SPI decoding for the specified decoder.

        Parameters:
        n (int): The decoder channel, either 1 or 2.

        Returns:
        str: The clock channel source, one of {"CHAN1", "CHAN2"}.
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:SPI:CLK?")
            return response.strip().upper()
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None

    def set_decoder_spi_miso_source(self, n, miso_source):
        """
        Set the MISO channel source in SPI decoding for the specified decoder.

        Parameters:
        n (int): The decoder channel, either 1 or 2.
        miso_source (str): The MISO channel source, one of {"CHANnel1", "CHANnel2", "OFF"}.
        """
        valid_decoders = [1, 2]
        valid_sources = {"CHANnel1", "CHANnel2", "OFF"}
        miso_source = miso_source.upper()

        if n in valid_decoders and miso_source in valid_sources:
            self.instrument.write(f":DECoder{n}:SPI:MISO {miso_source}")
        else:
            print(f"Invalid decoder ({n}) or MISO source ({miso_source}). Decoder: {valid_decoders}, Source: {valid_sources}")

    def get_decoder_spi_miso_source(self, n):
        """
        Query the MISO channel source in SPI decoding for the specified decoder.

        Parameters:
        n (int): The decoder channel, either 1 or 2.

        Returns:
        str: The MISO channel source, one of {"CHAN1", "CHAN2", "OFF"}.
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:SPI:MISO?")
            return response.strip().upper()
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None

    def set_decoder_spi_mosi_source(self, n, mosi_source):
        """
        Set the MOSI channel source in SPI decoding for the specified decoder.

        Parameters:
        n (int): The decoder channel, either 1 or 2.
        mosi_source (str): The MOSI channel source, one of {"CHANnel1", "CHANnel2", "OFF"}.
        """
        valid_decoders = [1, 2]
        valid_sources = {"CHANnel1", "CHANnel2", "OFF"}
        mosi_source = mosi_source.upper()

        if n in valid_decoders and mosi_source in valid_sources:
            self.instrument.write(f":DECoder{n}:SPI:MOSI {mosi_source}")
        else:
            print(f"Invalid decoder ({n}) or MOSI source ({mosi_source}). Decoder: {valid_decoders}, Source: {valid_sources}")

    def get_decoder_spi_mosi_source(self, n):
        """
        Query the MOSI channel source in SPI decoding for the specified decoder.

        Parameters:
        n (int): The decoder channel, either 1 or 2.

        Returns:
        str: The MOSI channel source, one of {"CHAN1", "CHAN2", "OFF"}.
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:SPI:MOSI?")
            return response.strip().upper()
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None

    def set_decoder_spi_cs_source(self, n, cs_source):
        """
        Set the CS channel source in SPI decoding for the specified decoder. This command is only valid in CS mode.

        Parameters:
        n (int): The decoder channel, either 1 or 2.
        cs_source (str): The CS channel source, one of {"CHANnel1", "CHANnel2"}.
        """
        valid_decoders = [1, 2]
        valid_sources = {"CHANnel1", "CHANnel2"}
        cs_source = cs_source.upper()

        if n in valid_decoders and cs_source in valid_sources:
            self.instrument.write(f":DECoder{n}:SPI:CS {cs_source}")
        else:
            print(f"Invalid decoder ({n}) or CS source ({cs_source}). Decoder: {valid_decoders}, Source: {valid_sources}")

    def get_decoder_spi_cs_source(self, n):
        """
        Query the CS channel source in SPI decoding for the specified decoder.

        Parameters:
        n (int): The decoder channel, either 1 or 2.

        Returns:
        str: The CS channel source, one of {"CHAN1", "CHAN2"}.
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:SPI:CS?")
            return response.strip().upper()
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None

    def set_decoder_spi_cs_polarity(self, n, polarity):
        """
        Set the CS polarity in SPI decoding for the specified decoder. This command is only valid in CS mode.

        Parameters:
        n (int): The decoder channel, either 1 or 2.
        polarity (str): The CS polarity, one of {"NCS", "CS"}.
                        NCS: low level is valid. CS: high level is valid.
        """
        valid_decoders = [1, 2]
        valid_polarities = {"NCS", "CS"}
        polarity = polarity.upper()

        if n in valid_decoders and polarity in valid_polarities:
            self.instrument.write(f":DECoder{n}:SPI:SELect {polarity}")
        else:
            print(f"Invalid decoder ({n}) or CS polarity ({polarity}). Decoder: {valid_decoders}, Polarity: {valid_polarities}")

    def get_decoder_spi_cs_polarity(self, n):
        """
        Query the CS polarity in SPI decoding for the specified decoder.

        Parameters:
        n (int): The decoder channel, either 1 or 2.

        Returns:
        str: The CS polarity, one of {"NCS", "CS"}.
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:SPI:SELect?")
            return response.strip().upper()
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None

    def set_decoder_spi_frame_sync_mode(self, n, mode):
        """
        Set the frame synchronization mode of SPI decoding for the specified decoder.

        Parameters:
        n (int): The decoder channel, either 1 or 2.
        mode (str): The frame synchronization mode, one of {"CS", "TIMeout"}.
        """
        valid_decoders = [1, 2]
        valid_modes = {"CS", "TIMeout"}
        mode = mode.upper()

        if n in valid_decoders and mode in valid_modes:
            self.instrument.write(f":DECoder{n}:SPI:MODE {mode}")
        else:
            print(f"Invalid decoder ({n}) or mode ({mode}). Decoder: {valid_decoders}, Mode: {valid_modes}")

    def get_decoder_spi_frame_sync_mode(self, n):
        """
        Query the frame synchronization mode of SPI decoding for the specified decoder.

        Parameters:
        n (int): The decoder channel, either 1 or 2.

        Returns:
        str: The frame synchronization mode, one of {"CS", "TIM"}.
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:SPI:MODE?")
            return response.strip().upper()
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None

    def set_decoder_spi_timeout_time(self, n, timeout_time):
        """
        Set the timeout time in the timeout mode of SPI decoding for the specified decoder.
        This command is only valid in timeout mode.

        Parameters:
        n (int): The decoder channel, either 1 or 2.
        timeout_time (float): The timeout time in seconds.
        """
        valid_decoders = [1, 2]
        if n in valid_decoders and isinstance(timeout_time, (float, int)) and timeout_time >= 0: # Range is "Refer to Explanation", so assuming non-negative.
            self.instrument.write(f":DECoder{n}:SPI:TIMeout {timeout_time}")
        else:
            print(f"Invalid decoder ({n}) or timeout time ({timeout_time}). Timeout time must be a non-negative float.")

    def get_decoder_spi_timeout_time(self, n):
        """
        Query the timeout time in the timeout mode of SPI decoding for the specified decoder.

        Parameters:
        n (int): The decoder channel, either 1 or 2.

        Returns:
        float: The timeout time in scientific notation (seconds).
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:SPI:TIMeout?")
            return float(response.strip())
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None

    def set_decoder_spi_polarity(self, n, polarity):
        """
        Set the polarity of the SDA data line in SPI decoding for the specified decoder.

        Parameters:
        n (int): The decoder channel, either 1 or 2.
        polarity (str): The polarity, one of {"NEGative", "POSitive"}.
        """
        valid_decoders = [1, 2]
        valid_polarities = {"NEGative", "POSitive"}
        polarity = polarity.upper()

        if n in valid_decoders and polarity in valid_polarities:
            self.instrument.write(f":DECoder{n}:SPI:POLarity {polarity}")
        else:
            print(f"Invalid decoder ({n}) or polarity ({polarity}). Decoder: {valid_decoders}, Polarity: {valid_polarities}")

    def get_decoder_spi_polarity(self, n):
        """
        Query the polarity of the SDA data line in SPI decoding for the specified decoder.

        Parameters:
        n (int): The decoder channel, either 1 or 2.

        Returns:
        str: The polarity, one of {"NEG", "POS"}.
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:SPI:POLarity?")
            return response.strip().upper()
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None

    def set_decoder_spi_clock_edge(self, n, edge):
        """
        Set the clock type when the instrument samples the data line in SPI decoding for the specified decoder.

        Parameters:
        n (int): The decoder channel, either 1 or 2.
        edge (str): The clock edge, one of {"RISE", "FALL"}.
        """
        valid_decoders = [1, 2]
        valid_edges = {"RISE", "FALL"}
        edge = edge.upper()

        if n in valid_decoders and edge in valid_edges:
            self.instrument.write(f":DECoder{n}:SPI:EDGE {edge}")
        else:
            print(f"Invalid decoder ({n}) or edge ({edge}). Decoder: {valid_decoders}, Edge: {valid_edges}")

    def get_decoder_spi_clock_edge(self, n):
        """
        Query the clock type when the instrument samples the data line in SPI decoding for the specified decoder.

        Parameters:
        n (int): The decoder channel, either 1 or 2.

        Returns:
        str: The clock edge, one of {"RISE", "FALL"}.
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:SPI:EDGE?")
            return response.strip().upper()
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None

    def set_decoder_spi_endian(self, n, endian):
        """
        Set the endian of the SPI decoding data for the specified decoder.

        Parameters:
        n (int): The decoder channel, either 1 or 2.
        endian (str): The endian, one of {"LSB", "MSB"}.
        """
        valid_decoders = [1, 2]
        valid_endians = {"LSB", "MSB"}
        endian = endian.upper()

        if n in valid_decoders and endian in valid_endians:
            self.instrument.write(f":DECoder{n}:SPI:ENDian {endian}")
        else:
            print(f"Invalid decoder ({n}) or endian ({endian}). Decoder: {valid_decoders}, Endian: {valid_endians}")

    def get_decoder_spi_endian(self, n):
        """
        Query the endian of the SPI decoding data for the specified decoder.

        Parameters:
        n (int): The decoder channel, either 1 or 2.

        Returns:
        str: The endian, one of {"LSB", "MSB"}.
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:SPI:ENDian?")
            return response.strip().upper()
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None

    def set_decoder_spi_data_width(self, n, width):
        """
        Set the number of bits of each frame of data in SPI decoding for the specified decoder.

        Parameters:
        n (int): The decoder channel, either 1 or 2.
        width (int): The data width, from 4 to 32 bits.
        """
        valid_decoders = [1, 2]
        if n in valid_decoders and isinstance(width, int) and 4 <= width <= 32:
            self.instrument.write(f":DECoder{n}:SPI:WIDTh {width}")
        else:
            print(f"Invalid decoder ({n}) or width ({width}). Width must be an integer between 4 and 32.")

    def get_decoder_spi_data_width(self, n):
        """
        Query the number of bits of each frame of data in SPI decoding for the specified decoder.

        Parameters:
        n (int): The decoder channel, either 1 or 2.

        Returns:
        int: The data width.
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:SPI:WIDTh?")
            return int(response.strip())
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None

    # Parallel Decoding Commands
    def set_decoder_parallel_clk_source(self, n, clk_source):
        """
        Set the CLK channel source of parallel decoding for the specified decoder.

        Parameters:
        n (int): The decoder channel, either 1 or 2.
        clk_source (str): The clock channel source, one of {"CHANnel1", "CHANnel2", "OFF"}.
        """
        valid_decoders = [1, 2]
        valid_sources = {"CHANnel1", "CHANnel2", "OFF"}
        clk_source = clk_source.upper()

        if n in valid_decoders and clk_source in valid_sources:
            self.instrument.write(f":DECoder{n}:PARallel:CLK {clk_source}")
        else:
            print(f"Invalid decoder ({n}) or clock source ({clk_source}). Decoder: {valid_decoders}, Source: {valid_sources}")

    def get_decoder_parallel_clk_source(self, n):
        """
        Query the CLK channel source of parallel decoding for the specified decoder.

        Parameters:
        n (int): The decoder channel, either 1 or 2.

        Returns:
        str: The clock channel source, one of {"CHAN1", "CHAN2", "OFF"}.
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:PARallel:CLK?")
            return response.strip().upper()
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None

    def set_decoder_parallel_clock_edge(self, n, edge):
        """
        Set the edge type of the clock channel when the instrument samples the data channel in parallel decoding.

        Parameters:
        n (int): The decoder channel, either 1 or 2.
        edge (str): The clock edge type, one of {"RISE", "FALL", "BOTH"}.
        """
        valid_decoders = [1, 2]
        valid_edges = {"RISE", "FALL", "BOTH"}
        edge = edge.upper()

        if n in valid_decoders and edge in valid_edges:
            self.instrument.write(f":DECoder{n}:PARallel:EDGE {edge}")
        else:
            print(f"Invalid decoder ({n}) or edge ({edge}). Decoder: {valid_decoders}, Edge: {valid_edges}")

    def get_decoder_parallel_clock_edge(self, n):
        """
        Query the edge type of the clock channel when the instrument samples the data channel in parallel decoding.

        Parameters:
        n (int): The decoder channel, either 1 or 2.

        Returns:
        str: The clock edge type, one of {"RISE", "FALL", "BOTH"}.
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:PARallel:EDGE?")
            return response.strip().upper()
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None

    def set_decoder_parallel_data_width(self, n, width):
        """
        Set the data width (number of bits of each frame of data) of the parallel bus.

        Parameters:
        n (int): The decoder channel, either 1 or 2.
        width (int): The data width, from 1 to 2.
        """
        valid_decoders = [1, 2]
        if n in valid_decoders and isinstance(width, int) and 1 <= width <= 2:
            self.instrument.write(f":DECoder{n}:PARallel:WIDTh {width}")
        else:
            print(f"Invalid decoder ({n}) or width ({width}). Width must be an integer between 1 and 2.")

    def get_decoder_parallel_data_width(self, n):
        """
        Query the data width of the parallel bus.

        Parameters:
        n (int): The decoder channel, either 1 or 2.

        Returns:
        int: The data width.
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:PARallel:WIDTh?")
            return int(response.strip())
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None

    def set_decoder_parallel_bit_selection(self, n, bit):
        """
        Set the data bit that requires a channel source on the parallel bus.
        The range is 0 to (data width - 1).

        Parameters:
        n (int): The decoder channel, either 1 or 2.
        bit (int): The data bit to select.
        """
        valid_decoders = [1, 2]
        # Note: Actual max bit depends on current data width, which needs to be queried or known.
        # For now, we'll assume the user provides a valid bit within the *current* width.
        if n in valid_decoders and isinstance(bit, int) and bit >= 0:
            self.instrument.write(f":DECoder{n}:PARallel:BITX {bit}")
        else:
            print(f"Invalid decoder ({n}) or bit ({bit}). Bit must be a non-negative integer.")

    def get_decoder_parallel_bit_selection(self, n):
        """
        Query the data bit that requires a channel source on the parallel bus.

        Parameters:
        n (int): The decoder channel, either 1 or 2.

        Returns:
        int: The current data bit.
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:PARallel:BITX?")
            return int(response.strip())
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None

    def set_decoder_parallel_bit_source(self, n, source):
        """
        Set the channel source of the data bit currently selected on the parallel bus.
        Before sending this command, use set_decoder_parallel_bit_selection to select the desired data bit.

        Parameters:
        n (int): The decoder channel, either 1 or 2.
        source (str): The channel source, one of {"CHANnel1", "CHANnel2"}.
        """
        valid_decoders = [1, 2]
        valid_sources = {"CHANnel1", "CHANnel2"}
        source = source.upper()

        if n in valid_decoders and source in valid_sources:
            self.instrument.write(f":DECoder{n}:PARallel:SOURce {source}")
        else:
            print(f"Invalid decoder ({n}) or source ({source}). Decoder: {valid_decoders}, Source: {valid_sources}")

    def get_decoder_parallel_bit_source(self, n):
        """
        Query the channel source of the data bit currently selected on the parallel bus.

        Parameters:
        n (int): The decoder channel, either 1 or 2.

        Returns:
        str: The channel source, one of {"CHAN1", "CHAN2"}.
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:PARallel:SOURce?")
            return response.strip().upper()
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None

    def set_decoder_parallel_polarity(self, n, polarity):
        """
        Set the data polarity of parallel decoding for the specified decoder.

        Parameters:
        n (int): The decoder channel, either 1 or 2.
        polarity (str): The polarity, one of {"NEGative", "POSitive"}.
                        NEGative: low level is 1. POSitive: high level is 1.
        """
        valid_decoders = [1, 2]
        valid_polarities = {"NEGative", "POSitive"}
        polarity = polarity.upper()

        if n in valid_decoders and polarity in valid_polarities:
            self.instrument.write(f":DECoder{n}:PARallel:POLarity {polarity}")
        else:
            print(f"Invalid decoder ({n}) or polarity ({polarity}). Decoder: {valid_decoders}, Polarity: {valid_polarities}")

    def get_decoder_parallel_polarity(self, n):
        """
        Query the data polarity of parallel decoding for the specified decoder.

        Parameters:
        n (int): The decoder channel, either 1 or 2.

        Returns:
        str: The polarity, one of {"NEG", "POS"}.
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:PARallel:POLarity?")
            return response.strip().upper()
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None

    def set_decoder_parallel_noise_reject(self, n, state):
        """
        Turn on or off the noise rejection function of parallel decoding.

        Parameters:
        n (int): The decoder channel, either 1 or 2.
        state (bool): Whether to turn on (True) or off (False) the noise rejection function.
        """
        valid_decoders = [1, 2]
        if n in valid_decoders:
            self.instrument.write(f":DECoder{n}:PARallel:NREJect {'ON' if state else 'OFF'}")
        else:
            print(f"Invalid decoder. Choose from {valid_decoders}.")

    def get_decoder_parallel_noise_reject(self, n):
        """
        Query the status of the noise rejection function of parallel decoding.

        Parameters:
        n (int): The decoder channel, either 1 or 2.

        Returns:
        bool: The status of the noise rejection function (True for ON, False for OFF).
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:PARallel:NREJect?")
            return bool(int(response.strip()))
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None

    def set_decoder_parallel_noise_reject_time(self, n, time):
        """
        Set the noise rejection time of parallel decoding.
        Before sending this command, turn on the noise rejection function.

        Parameters:
        n (int): The decoder channel, either 1 or 2.
        time (float): The noise rejection time in seconds (0.00s to 100ms).
        """
        valid_decoders = [1, 2]
        if n in valid_decoders and isinstance(time, (float, int)) and 0.0 <= time <= 0.1: # 100ms = 0.1s
            self.instrument.write(f":DECoder{n}:PARallel:NRTime {time}")
        else:
            print(f"Invalid decoder ({n}) or time ({time}). Time must be a float between 0.0 and 0.1 (100ms).")

    def get_decoder_parallel_noise_reject_time(self, n):
        """
        Query the noise rejection time of parallel decoding.

        Parameters:
        n (int): The decoder channel, either 1 or 2.

        Returns:
        float: The noise rejection time in scientific notation (seconds).
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:PARallel:NRTime?")
            return float(response.strip())
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None

    def set_decoder_parallel_clock_compensation(self, n, compensation):
        """
        Set the clock compensation time of parallel decoding.

        Parameters:
        n (int): The decoder channel, either 1 or 2.
        compensation (float): The clock compensation time in seconds (-100ms to 100ms).
        """
        valid_decoders = [1, 2]
        if n in valid_decoders and isinstance(compensation, (float, int)) and -0.1 <= compensation <= 0.1: # 100ms = 0.1s
            self.instrument.write(f":DECoder{n}:PARallel:CCOMpensation {compensation}")
        else:
            print(f"Invalid decoder ({n}) or compensation ({compensation}). Compensation must be a float between -0.1 and 0.1 (100ms).")

    def get_decoder_parallel_clock_compensation(self, n):
        """
        Query the clock compensation time of parallel decoding.

        Parameters:
        n (int): The decoder channel, either 1 or 2.

        Returns:
        float: The compensation time in scientific notation (seconds).
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:PARallel:CCOMpensation?")
            return float(response.strip())
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None

    def set_decoder_parallel_plot_function(self, n, state):
        """
        Turn on or off the curve (plot) function of parallel decoding.

        Parameters:
        n (int): The decoder channel, either 1 or 2.
        state (bool): Whether to turn on (True) or off (False) the curve function.
        """
        valid_decoders = [1, 2]
        if n in valid_decoders:
            self.instrument.write(f":DECoder{n}:PARallel:PLOT {'ON' if state else 'OFF'}")
        else:
            print(f"Invalid decoder. Choose from {valid_decoders}.")

    def get_decoder_parallel_plot_function(self, n):
        """
        Query the status of the curve (plot) function of parallel decoding.

        Parameters:
        n (int): The decoder channel, either 1 or 2.

        Returns:
        bool: The status of the curve function (True for ON, False for OFF).
        """
        if n in [1, 2]:
            response = self.instrument.query(f":DECoder{n}:PARallel:PLOT?")
            return bool(int(response.strip()))
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None
#Display Commands
    def clear_display(self):
        """
        Clear all the waveforms on the screen.
        This command is equivalent to pressing the CLEAR key on the front panel.
        If the oscilloscope is in the RUN state, waveform will still be displayed.
        """
        self.instrument.write(":DISPlay:CLEar")

    def get_display_data(self, filename = "osc_display_data",color=None, invert=None, fmt=None):
        """
        Read the data stream of the image currently displayed on the screen.
        Optionally set the color, invert display, and format of the image acquired.

        Parameters:
        color (bool, optional): True for color, False for intensity graded color. Default is ON.
        invert (bool, optional): True to turn on invert function, False to turn off. Default is OFF.
        fmt (str, optional): Image format, one of {"BMP24", "BMP8", "PNG", "JPEG", "TIFF"}. Default is BMP24.

        Returns:
        Image: An image object containing the display data.
        bytes: The raw image data stream, including the TMC Blockheader.
               The user needs to handle parsing this data (remove TMC header).
        """
        command_parts = []
        if color is not None:
            command_parts.append("ON" if color else "OFF")
        if invert is not None:
            command_parts.append("ON" if invert else "OFF") # PDF says 1|ON or 0|OFF, but ON/OFF is cleaner
        if fmt is not None:
            valid_formats = {"BMP24", "BMP8", "PNG", "JPEG", "TIFF"}
            if fmt.upper() in valid_formats:
                command_parts.append(fmt.upper())
            else:
                print(f"Invalid format: {fmt}. Using default.")
                command_parts = [] # Reset to use default if format is invalid

        command = ":DISPlay:DATA?"
        if command_parts:
            command += " " + ",".join(command_parts)


        # Use query_binary_values to read the image data
        # The 'B' datatype is for 8-bit unsigned integers (bytes)
        # The PDF notes a TMC header which needs to be stripped by the user.
        # It also mentions potential timeout issues for large data.
        try:
            # It's crucial to set a proper timeout for large binary transfers
            # self.instrument.timeout = 5000 # Example: 5 seconds timeout
            data = self.instrument.query(command)
            self.instrument.timeout = 2000 # Reset to default if needed
            return data #self.data_handler.bytes_to_image(data, self.default_save_path+"/"+filename,fmt, "TMC"), data  # Convert bytes to image format
        except pyvisa.errors.VisaIOError as e:
            print(f"VISA IO Error while getting display data: {e}")
            print("Consider increasing the instrument's timeout.")
            return b""
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return b""


    def set_display_type(self, display_type):
        """
        Set the display mode of the waveform on the screen.

        Parameters:
        display_type (str): The display mode, one of {"VECTors", "DOTS"}.
        """
        valid_types = {"VECTors", "DOTS"}
        display_type = display_type.upper()
        if display_type in valid_types:
            self.instrument.write(f":DISPlay:TYPE {display_type}")
        else:
            print(f"Invalid display type. Choose from {valid_types}.")

    def get_display_type(self):
        """
        Query the display mode of the waveform on the screen.

        Returns:
        str: The display mode, one of {"VECT", "DOTS"}.
        """
        response = self.instrument.query(":DISPlay:TYPE?")
        return response.strip().upper()

    def set_display_persistence_time(self, time):
        """
        Set the persistence time.

        Parameters:
        time (str or float): The persistence time, one of {"MIN", 0.1, 0.2, 0.5, 1, 5, 10, "INFinite"}.
        """
        valid_times_str = {"MIN", "INFINITE"}
        valid_times_float = {0.1, 0.2, 0.5, 1.0, 5.0, 10.0}

        if isinstance(time, str):
            time = time.upper()
            if time in valid_times_str:
                self.instrument.write(f":DISPlay:GRADing:TIME {time}")
            else:
                print(f"Invalid persistence time string. Choose from {valid_times_str}.")
        elif isinstance(time, (int, float)):
            if float(time) in valid_times_float:
                self.instrument.write(f":DISPlay:GRADing:TIME {float(time)}")
            else:
                print(f"Invalid persistence time float/int. Choose from {valid_times_float}.")
        else:
            print(f"Invalid persistence time type. Must be a string or a float/int from allowed values.")


    def get_display_persistence_time(self):
        """
        Query the persistence time.

        Returns:
        str or float: The persistence time, one of {"MIN", 0.1, 0.2, 0.5, 1.0, 5.0, 10.0, "INF"}.
        """
        response = self.instrument.query(":DISPlay:GRADing:TIME?")
        response_str = response.strip().upper()
        try:
            return float(response_str)
        except ValueError:
            return response_str # Returns MIN or INF

    def set_waveform_brightness(self, brightness):
        """
        Set the waveform brightness.

        Parameters:
        brightness (int): The brightness level, from 0 to 100.
        """
        if isinstance(brightness, int) and 0 <= brightness <= 100:
            self.instrument.write(f":DISPlay:WBRightness {brightness}")
        else:
            print("Invalid brightness value. Must be an integer between 0 and 100.")

    def get_waveform_brightness(self):
        """
        Query the waveform brightness.

        Returns:
        int: The brightness level (0 to 100).
        """
        response = self.instrument.query(":DISPlay:WBRightness?")
        return int(response.strip())

    def set_grid_type(self, grid_type):
        """
        Set the grid type of screen display.

        Parameters:
        grid_type (str): The grid type, one of {"FULL", "HALF", "NONE"}.
        """
        valid_types = {"FULL", "HALF", "NONE"}
        grid_type = grid_type.upper()
        if grid_type in valid_types:
            self.instrument.write(f":DISPlay:GRID {grid_type}")
        else:
            print(f"Invalid grid type. Choose from {valid_types}.")

    def get_grid_type(self):
        """
        Query the grid type of screen display.

        Returns:
        str: The grid type, one of {"FULL", "HALF", "NONE"}.
        """
        response = self.instrument.query(":DISPlay:GRID?")
        return response.strip().upper()

    def set_grid_brightness(self, brightness):
        """
        Set the brightness of the screen grid.

        Parameters:
        brightness (int): The brightness level, from 0 to 100.
        """
        if isinstance(brightness, int) and 0 <= brightness <= 100:
            self.instrument.write(f":DISPlay:GBRightness {brightness}")
        else:
            print("Invalid brightness value. Must be an integer between 0 and 100.")

    def get_grid_brightness(self,):
        """
        Query the brightness of the screen grid.

        Returns:
        int: The brightness level (0 to 100).
        """
        response = self.instrument.query(":DISPlay:GBRightness?")
        return int(response.strip())

    # Event Table Commands
    def set_event_table_display(self, n, state):
        """
        Turn on or off the decoding event table.
        This command is only valid when the decoder is turned on (:DECoder<n>:DISPlay).

        Parameters:
        n (int): The decoder channel, either 1 or 2.
        state (bool): Whether to turn on (True) or off (False) the event table display.
        """
        valid_decoders = [1, 2]
        if n in valid_decoders:
            self.instrument.write(f":ETABle{n}:DISP {'ON' if state else 'OFF'}")
        else:
            print(f"Invalid decoder channel. Choose from {valid_decoders}.")

    def get_event_table_display(self, n):
        """
        Query the status of the decoding event table.

        Parameters:
        n (int): The decoder channel, either 1 or 2.

        Returns:
        bool: The status of the decoding event table (True for ON, False for OFF).
        """
        if n in [1, 2]:
            response = self.instrument.query(f":ETABle{n}:DISP?")
            return bool(int(response.strip()))
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None

    def set_event_table_format(self, n, fmt):
        """
        Set the data display format of the event table.

        Parameters:
        n (int): The decoder channel, either 1 or 2.
        fmt (str): The data display format, one of {"HEX", "ASCII", "DEC"}.
        """
        valid_decoders = [1, 2]
        valid_formats = {"HEX", "ASCII", "DEC"}
        fmt = fmt.upper()

        if n in valid_decoders and fmt in valid_formats:
            self.instrument.write(f":ETABle{n}:FORMat {fmt}")
        else:
            print(f"Invalid decoder ({n}) or format ({fmt}). Format: {valid_formats}")

    def get_event_table_format(self, n):
        """
        Query the data display format of the event table.

        Parameters:
        n (int): The decoder channel, either 1 or 2.

        Returns:
        str: The data display format, one of {"HEX", "ASC", "DEC"}.
        """
        if n in [1, 2]:
            response = self.instrument.query(f":ETABle{n}:FORMat?")
            return response.strip().upper()
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None

    def set_event_table_view_mode(self, n, view_mode):
        """
        Set the display mode of the event table.

        Parameters:
        n (int): The decoder channel, either 1 or 2.
        view_mode (str): The display mode, one of {"PACKage", "DETail", "PAYLoad"}.
        """
        valid_decoders = [1, 2]
        valid_modes = {"PACKage", "DETail", "PAYLoad"}
        view_mode = view_mode.upper()

        if n in valid_decoders and view_mode in valid_modes:
            self.instrument.write(f":ETABle{n}:VIEW {view_mode}")
        else:
            print(f"Invalid decoder ({n}) or view mode ({view_mode}). View modes: {valid_modes}")

    def get_event_table_view_mode(self, n):
        """
        Query the display mode of the event table.

        Parameters:
        n (int): The decoder channel, either 1 or 2.

        Returns:
        str: The display mode, one of {"PACK", "DET", "PAYL"}.
        """
        if n in [1, 2]:
            response = self.instrument.query(f":ETABle{n}:VIEW?")
            return response.strip().upper()
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None

    def set_event_table_column(self, n, column):
        """
        Set the current column of the event table.
        The valid range for <col> differs based on the selected decoder mode.

        Parameters:
        n (int): The decoder channel, either 1 or 2.
        column (str): The column to set, e.g., "DATA", "TX", "RX", "MISO", "MOSI".
        """
        valid_decoders = [1, 2]
        valid_columns = {"DATA", "TX", "RX", "MISO", "MOSI"} # General list, actual validity depends on decoder mode
        column = column.upper()

        if n in valid_decoders and column in valid_columns:
            self.instrument.write(f":ETABle{n}:COLumn {column}")
        else:
            print(f"Invalid decoder ({n}) or column ({column}). Column: {valid_columns}")
            print("Note: Column validity depends on the active decoder mode.")

    def get_event_table_column(self, n):
        """
        Query the current column of the event table.

        Parameters:
        n (int): The decoder channel, either 1 or 2.

        Returns:
        str: The current column, e.g., "DATA", "TX", "RX", "MISO", "MOSI".
        """
        if n in [1, 2]:
            response = self.instrument.query(f":ETABle{n}:COLumn?")
            return response.strip().upper()
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None

    def set_event_table_row(self, n, row):
        """
        Set the current row of the event table.

        Parameters:
        n (int): The decoder channel, either 1 or 2.
        row (int): The row number, from 1 to the maximum number of rows of the current event table.
        """
        valid_decoders = [1, 2]
        if n in valid_decoders and isinstance(row, int) and row >= 1: # Max row is dynamic, so only check for >=1
            self.instrument.write(f":ETABle{n}:ROW {row}")
        else:
            print(f"Invalid decoder ({n}) or row ({row}). Row must be an integer >= 1.")

    def get_event_table_row(self, n):
        """
        Query the current row of the event table.

        Parameters:
        n (int): The decoder channel, either 1 or 2.

        Returns:
        int: The current row in integer. Returns 0 if the event table is empty.
        """
        if n in [1, 2]:
            response = self.instrument.query(f":ETABle{n}:ROW?")
            return int(response.strip())
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None

    def set_event_table_sort_type(self, n, sort_type):
        """
        Set the display type of the decoding results in the event table.

        Parameters:
        n (int): The decoder channel, either 1 or 2.
        sort_type (str): The sort type, one of {"ASCend", "DESCend"}.
        """
        valid_decoders = [1, 2]
        valid_types = {"ASCend", "DESCend"}
        sort_type = sort_type.upper()

        if n in valid_decoders and sort_type in valid_types:
            self.instrument.write(f":ETABle{n}:SORT {sort_type}")
        else:
            print(f"Invalid decoder ({n}) or sort type ({sort_type}). Sort types: {valid_types}")

    def get_event_table_sort_type(self, n):
        """
        Query the display type of the decoding results in the event table.

        Parameters:
        n (int): The decoder channel, either 1 or 2.

        Returns:
        str: The sort type, one of {"ASC", "DESC"}.
        """
        if n in [1, 2]:
            response = self.instrument.query(f":ETABle{n}:SORT?")
            return response.strip().upper()
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return None

    def get_event_table_data(self, n):
        """
        Read the current event table data.

        Parameters:
        n (int): The decoder channel, either 1 or 2.

        Returns:
        bytes: The raw event table data, including the TMC data description header.
               
        """
        if n in [1, 2]:
            try:
                # Use query_binary_values to read the event table data
                data = self.instrument.query(f":ETABle{n}:DATA?")
                return data
            except pyvisa.errors.VisaIOError as e:
                print(f"VISA IO Error while getting event table data: {e}")
                print("Consider increasing the instrument's timeout.")
                return b""
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                return b""
        else:
            print("Invalid decoder channel. Choose 1 or 2.")
            return b""
#Function Commands
    # Function Commands (Waveform Recording)
    def set_waveform_record_end_frame(self, frame):
        """
        Set the end frame of waveform recording. 

        Parameters:
        frame (int): The end frame number, from 1 to the maximum number of frames that can be recorded. 
        """
        # The PDF states "1 to the maximum number of frames can be recorded currently" 
        # We can't query max frames here to validate, so we'll just check for >= 1.
        if isinstance(frame, int) and frame >= 1:
            self.instrument.write(f":FUNCtion:WRECord:FEND {frame}") 
        else:
            print(f"Invalid frame value ({frame}). Frame must be an integer >= 1.")

    def get_waveform_record_end_frame(self):
        """
        Query the end frame of waveform recording. 

        Returns:
        int: The current end frame in integer. 
        """
        response = self.instrument.query(":FUNCtion:WRECord:FEND?") 
        return int(response.strip())

    def get_waveform_record_max_frames(self):
        """
        Query the maximum number of frames that can be recorded currently. 

        Returns:
        int: The maximum number of frames.
        """
        response = self.instrument.query(":FUNCtion:WRECord:FMAX?")
        return int(response.strip())

    def set_waveform_record_interval(self, interval):
        """
        Set the time interval between adjacent frames during waveform recording. 

        Parameters:
        interval (float): The time interval in seconds. Range: 1e-6 to 1000 seconds. 
                          You can also use "MIN" for the minimum interval. 
        """
        if isinstance(interval, str) and interval.upper() == "MIN":
            self.instrument.write(":FUNCtion:WRECord:FINTerval MIN") 
        elif isinstance(interval, (float, int)) and 1e-6 <= float(interval) <= 1000:
            self.instrument.write(f":FUNCtion:WRECord:FINTerval {float(interval)}") 
        else:
            print(f"Invalid interval value ({interval}). Must be 'MIN' or a float between 1e-6 and 1000.")

    def get_waveform_record_interval(self):
        """
        Query the time interval between adjacent frames during waveform recording. 

        Returns:
        float or str: The interval in seconds, or "MIN". 
        """
        response = self.instrument.query(":FUNCtion:WRECord:FINTerval?") 
        response_str = response.strip().upper()
        try:
            return float(response_str)
        except ValueError:
            return response_str # Returns MIN

    def set_waveform_record_prompt_state(self, state):
        """
        Turn on or off the prompt for waveform recording. 
        When turned on, a prompt box will pop up when the internal storage is full. 

        Parameters:
        state (bool): True to turn on (1|ON), False to turn off (0|OFF). 
        """
        self.instrument.write(f":FUNCtion:WRECord:PROMpt {'ON' if state else 'OFF'}") 

    def get_waveform_record_prompt_state(self):
        """
        Query the status of the prompt for waveform recording. 

        Returns:
        bool: True if prompt is ON, False if OFF. 
        """
        response = self.instrument.query(":FUNCtion:WRECord:PROMpt?") 
        return bool(int(response.strip())) # Returns 1 for ON, 0 for OFF 

    def set_waveform_record_operation(self, operate_mode):
        """
        Set the operation type of waveform recording. 

        Parameters:
        operate_mode (str): The operation type, one of {"REC", "STOP", "SAVE"}. 
        """
        valid_modes = {"REC", "STOP", "SAVE"} 
        operate_mode = operate_mode.upper() 

        if operate_mode in valid_modes:
            self.instrument.write(f":FUNCtion:WRECord:OPERate {operate_mode}") 
        else:
            print(f"Invalid operation mode ({operate_mode}). Choose from {valid_modes}.")

    def get_waveform_record_operation(self):
        """
        Query the status of waveform recording. 

        Returns:
        str: The status, one of {"REC", "STOP", "SAVE"}. 
        """
        response = self.instrument.query(":FUNCtion:WRECord:OPERate?") 
        return response.strip().upper() 

    def set_waveform_record_enable(self, state):
        """
        Turn on or off the waveform recording function. 

        Parameters:
        state (bool): True to enable (ON), False to disable (OFF). 
        """
        self.instrument.write(f":FUNCtion:WRECord:ENABle {'ON' if state else 'OFF'}") 

    def get_waveform_record_enable(self):
        """
        Query the status of the waveform recording function. 

        Returns:
        bool: True if enabled, False if disabled. 
        """
        response = self.instrument.query(":FUNCtion:WRECord:ENABle?") 
        return bool(int(response.strip())) # Returns 1 for ON, 0 for OFF 

    # Function Commands (Waveform Playback)
    def set_waveform_replay_start_frame(self, frame):
        """
        Set the start frame of waveform playback. 

        Parameters:
        frame (int): The start frame number, from 1 to the maximum number of frames recorded. 
        """
        # Similar to end frame, we'll just check for >= 1. 
        if isinstance(frame, int) and frame >= 1:
            self.instrument.write(f":FUNCtion:WREPlay:FSTart {frame}") 
        else:
            print(f"Invalid frame value ({frame}). Frame must be an integer >= 1.")

    def get_waveform_replay_start_frame(self):
        """
        Query the start frame of waveform playback. 

        Returns:
        int: The current start frame in integer. 
        """
        response = self.instrument.query(":FUNCtion:WREPlay:FSTart?") 
        return int(response.strip())

    def set_waveform_replay_end_frame(self, frame):
        """
        Set the end frame of waveform playback. 

        Parameters:
        frame (int): The end frame number, from 1 to the maximum number of frames recorded. 
        """
        # Similar to start frame, we'll just check for >= 1. 
        if isinstance(frame, int) and frame >= 1:
            self.instrument.write(f":FUNCtion:WREPlay:FEND {frame}") 
        else:
            print(f"Invalid frame value ({frame}). Frame must be an integer >= 1.")

    def get_waveform_replay_end_frame(self):
        """
        Query the end frame of waveform playback. 

        Returns:
        int: The current end frame in integer. 
        """
        response = self.instrument.query(":FUNCtion:WREPlay:FEND?") 
        return int(response.strip())

    def get_waveform_replay_max_frames(self):
        """
        Query the maximum number of frames that can be replayed currently. 

        Returns:
        int: The maximum number of frames. 
        """
        response = self.instrument.query(":FUNCtion:WREPlay:FMAX?") 
        return int(response.strip())

    def set_waveform_replay_interval(self, interval):
        """
        Set the time interval between adjacent frames during waveform playback. 

        Parameters:
        interval (float): The time interval in seconds. Range: 1e-6 to 1000 seconds. 
                          You can also use "MIN" for the minimum interval. 
        """
        if isinstance(interval, str) and interval.upper() == "MIN":
            self.instrument.write(":FUNCtion:WREPlay:FINTerval MIN") 
        elif isinstance(interval, (float, int)) and 1e-6 <= float(interval) <= 1000:
            self.instrument.write(f":FUNCtion:WREPlay:FINTerval {float(interval)}") 
        else:
            print(f"Invalid interval value ({interval}). Must be 'MIN' or a float between 1e-6 and 1000.")

    def get_waveform_replay_interval(self):
        """
        Query the time interval between adjacent frames during waveform playback. 

        Returns:
        float or str: The interval in seconds, or "MIN". 
        """
        response = self.instrument.query(":FUNCtion:WREPlay:FINTerval?") 
        response_str = response.strip().upper()
        try:
            return float(response_str)
        except ValueError:
            return response_str # Returns MIN

    def set_waveform_replay_mode(self, mode):
        """
        Set the playback mode of the waveform. 

        Parameters:
        mode (str): The playback mode, one of {"NORMal", "LOOP"}. 
        """
        valid_modes = {"NORMal", "LOOP"} 
        mode = mode.upper() 

        if mode in valid_modes:
            self.instrument.write(f":FUNCtion:WREPlay:MODE {mode}") 
        else:
            print(f"Invalid mode ({mode}). Choose from {valid_modes}.")

    def get_waveform_replay_mode(self):
        """
        Query the playback mode of the waveform. 

        Returns:
        str: The playback mode, one of {"NORM", "LOOP"}. 
        """
        response = self.instrument.query(":FUNCtion:WREPlay:MODE?") 
        return response.strip().upper() 

    def set_waveform_replay_direction(self, direction):
        """
        Set the playback direction of the waveform. 

        Parameters:
        direction (str): The playback direction, one of {"FORWard", "BACKward"}. 
        """
        valid_directions = {"FORWard", "BACKward"} 
        direction = direction.upper() 

        if direction in valid_directions:
            self.instrument.write(f":FUNCtion:WREPlay:DIRection {direction}") 
        else:
            print(f"Invalid direction ({direction}). Choose from {valid_directions}.")

    def get_waveform_replay_direction(self):
        """
        Query the playback direction of the waveform. 

        Returns:
        str: The playback direction, one of {"FORW", "BACK"}. 
        """
        response = self.instrument.query(":FUNCtion:WREPlay:DIRection?") 
        return response.strip().upper() 

    def set_waveform_replay_operate(self, operate_type):
        """
        Set the operation type of waveform playback. 

        Parameters:
        operate_type (str): The operation type, one of {"PLAY", "PAUSE", "STOP"}. 
        """
        valid_types = {"PLAY", "PAUSE", "STOP"} 
        operate_type = operate_type.upper() 

        if operate_type in valid_types:
            self.instrument.write(f":FUNCtion:WREPlay:OPERate {operate_type}") 
        else:
            print(f"Invalid operation type ({operate_type}). Choose from {valid_types}.")

    def get_waveform_replay_operate(self):
        """
        Query the status of the waveform playback. 

        Returns:
        str: The status, one of {"PLAY", "PAUS", "STOP"}. 
        """
        response = self.instrument.query(":FUNCtion:WREPlay:OPERate?") 
        return response.strip().upper() 

    def set_waveform_replay_current_frame(self, current_frame):
        """
        Set the current frame in waveform playback. 

        Parameters:
        current_frame (int): The current frame number, from 1 to the maximum number of frames recorded. 
        """
        # We can't query max frames here to validate, so we'll just check for >= 1. 
        if isinstance(current_frame, int) and current_frame >= 1:
            self.instrument.write(f":FUNCtion:WREPlay:FCURrent {current_frame}") 
        else:
            print(f"Invalid current frame ({current_frame}). Frame must be an integer >= 1.")

    def get_waveform_replay_current_frame(self):
        """
        Query the current frame in waveform playback. 

        Returns:
        int: The current frame in integer. 
        """
        response = self.instrument.query(":FUNCtion:WREPlay:FCURrent?") 
        return int(response.strip())
    



    # LAN Commands
    def set_lan_dhcp_mode(self, state):
        """
        Turn on or off the DHCP configuration mode.

        Parameters:
        state (bool): True to turn on (ON), False to turn off (OFF).
        """
        self.instrument.write(f":LAN:DHCP {'ON' if state else 'OFF'}")

    def get_lan_dhcp_mode(self):
        """
        Query the on/off status of the current DHCP configuration mode.

        Returns:
        bool: True if DHCP is ON, False if OFF.
        """
        response = self.instrument.query(":LAN:DHCP?")
        return bool(int(response.strip()))

    def set_lan_autoip_mode(self, state):
        """
        Turn on or off the Auto IP configuration mode.

        Parameters:
        state (bool): True to turn on (ON), False to turn off (OFF).
        """
        self.instrument.write(f":LAN:AUToip {'ON' if state else 'OFF'}")

    def get_lan_autoip_mode(self):
        """
        Query the on/off status of the current Auto IP configuration mode.

        Returns:
        bool: True if Auto IP is ON, False if OFF.
        """
        response = self.instrument.query(":LAN:AUToip?")
        return bool(int(response.strip()))

    def set_lan_gateway(self, gateway_ip):
        """
        Set the default gateway.

        Parameters:
        gateway_ip (str): The gateway IP address in "nnn.nnn.nnn.nnn" format.
                          The first section (nnn) can be 0-223 (except 127).
                          Other sections (nnn) can be 0-255.
        """
        # Basic regex for IP address validation (simplified)
       
        self.instrument.write(f":LAN:GATeway {gateway_ip}")
          
    def get_lan_gateway(self):
        """
        Query the current default gateway.

        Returns:
        str: The current gateway IP address.
        """
        response = self.instrument.query(":LAN:GATeway?")
        return response.strip()

    def set_lan_dns(self, dns_ip):
        """
        Set the DNS address.

        Parameters:
        dns_ip (str): The DNS IP address in "nnn.nnn.nnn.nnn" format.
                      The first section (nnn) can be 0-223 (except 127).
                      Other sections (nnn) can be 0-255.
        """
        
        self.instrument.write(f":LAN:DNS {dns_ip}")
       
    def get_lan_dns(self):
        """
        Query the current DNS address.

        Returns:
        str: The current DNS IP address.
        """
        response = self.instrument.query(":LAN:DNS?")
        return response.strip()

    def get_lan_mac_address(self):
        """
        Query the MAC address of the instrument.

        Returns:
        str: The MAC address in "XX-XX-XX-XX-XX-XX" format.
        """
        response = self.instrument.query(":LAN:MAC?")
        return response.strip()

    def set_lan_manual_ip_mode(self, state):
        """
        Turn on or off the static IP configuration mode.

        Parameters:
        state (bool): True to turn on (ON), False to turn off (OFF).
        """
        self.instrument.write(f":LAN:MANual {'ON' if state else 'OFF'}")

    def get_lan_manual_ip_mode(self):
        """
        Query the on/off status of the static IP configuration mode.

        Returns:
        bool: True if static IP is ON, False if OFF.
        """
        response = self.instrument.query(":LAN:MANual?")
        return bool(int(response.strip()))

    def initiate_lan_parameters(self):
        """
        Initiate the network parameters (:LAN:INITiate).
        Before running the command, confirm that the oscilloscope has been connected to the network properly.
        """
        self.instrument.write(":LAN:INITiate")

    def set_lan_ip_address(self, ip_address):
        """
        Set the IP address of the instrument.
        #todo check this

        Parameters:
        ip_address (str): The IP address in "nnn.nnn.nnn.nnn" format.
                          The first section (nnn) can be 0-223 (except 127).
                          Other sections (nnn) can be 0-255.
        """
        
        self.instrument.write(f":LAN:IPADdress {ip_address}")


    def get_lan_ip_address(self):
        """
        Query the IP address of the instrument.

        Returns:
        str: The current IP address.
        """
        response = self.instrument.query(":LAN:IPADdress?")
        return response.strip()

    def set_lan_subnet_mask(self, subnet_mask):
        """
        Set the subnet mask.

        Parameters:
        subnet_mask (str): The subnet mask in "nnn.nnn.nnn.nnn" format.
                           Each section (nnn) can be 0-255.
        """

        self.instrument.write(f":LAN:SMASK {subnet_mask}")
        
    def get_lan_subnet_mask(self):
        """
        Query the current subnet mask.

        Returns:
        str: The current subnet mask.
        """
        response = self.instrument.query(":LAN:SMASK?")
        return response.strip()

    def get_lan_status(self):
        """
        Query the current network configuration status.

        Returns:
        str: The status, one of {"UNLINK", "INIT", "IPCONFLICT", "CONFIGURED", "DHCPFAILED"}.
        """
        response = self.instrument.query(":LAN:STATus?")
        return response.strip().upper()

    def get_lan_visa_address(self):
        """
        Query the VISA address of the instrument.

        Returns:
        str: The VISA address, e.g., "TCPIP::172.16.3.119::INSTR".
        """
        response = self.instrument.query(":LAN:VISA?")
        return response.strip()

    def apply_lan_configuration(self):
        """
        Apply the network configuration (:LAN:APPLY).
        """
        self.instrument.write(":LAN:APPLY")

    # MATH Commands
    def enable_math_display(self, state):
        """
        Enable or disable the math operation function.

        Parameters:
        state (bool): True to enable (ON), False to disable (OFF).
        """
        self.instrument.write(f":MATH:DISPlay {'ON' if state else 'OFF'}")

    def is_math_display_enabled(self):
        """
        Query the math operation status.

        Returns:
        bool: True if math operation is ON, False if OFF.
        """
        response = self.instrument.query(":MATH:DISPlay?")
        return bool(int(response.strip()))

    def set_math_operator(self, operator):
        """
        Set the operator of the math operation.

        Parameters:
        operator (str): The operator, one of {"ADD", "SUBTract", "MULTiply", "DIVision",
                        "AND", "OR", "XOR", "NOT", "FFT", "INTG", "DIFF", "SQRT",
                        "LOG", "LN", "EXP", "ABS", "FILTer"}.
        """
        valid_operators = {"ADD", "SUBTract", "MULTiply", "DIVision", "AND", "OR",
                           "XOR", "NOT", "FFT", "INTG", "DIFF", "SQRT", "LOG", "LN",
                           "EXP", "ABS", "FILTer"}
        operator = operator.upper()
        if operator in valid_operators:
            self.instrument.write(f":MATH:OPERator {operator}")
        else:
            print(f"Invalid operator ({operator}). Choose from {valid_operators}.")

    def get_math_operator(self):
        """
        Query the operator of the math operation.

        Returns:
        str: The operator, one of {"ADD", "SUBT", "MULT", "DIV", "AND", "OR", "XOR",
                                   "NOT", "FFT", "INTG", "DIFF", "SQRT", "LOG", "LN",
                                   "EXP", "ABS", "FILT"}.
        """
        response = self.instrument.query(":MATH:OPERator?")
        return response.strip().upper()

    def set_math_source1(self, source):
        """
        Set the source or source A of algebraic operation/functional operation/
        the outer layer operation of compound operation.

        Parameters:
        source (str): The source, one of {"CHANnel1", "CHANnel2", "FX"}.
        """
        valid_sources = {"CHANnel1", "CHANnel2", "FX"}
        source = source.upper()
        if source in valid_sources:
            self.instrument.write(f":MATH:SOURce1 {source}")
        else:
            print(f"Invalid source ({source}). Choose from {valid_sources}.")

    def get_math_source1(self):
        """
        Query the source or source A of algebraic operation/functional operation/
        the outer layer operation of compound operation.

        Returns:
        str: The source, one of {"CHAN1", "CHAN2", "FX"}.
        """
        response = self.instrument.query(":MATH:SOURce1?")
        return response.strip().upper()

    def set_math_source2(self, source):
        """
        Set source B of algebraic operation/the outer layer operation of compound operation.

        Parameters:
        source (str): The source, one of {"CHANnel1", "CHANnel2", "FX"}.
        """
        valid_sources = {"CHANnel1", "CHANnel2", "FX"}
        source = source.upper()
        if source in valid_sources:
            self.instrument.write(f":MATH:SOURce2 {source}")
        else:
            print(f"Invalid source ({source}). Choose from {valid_sources}.")

    def get_math_source2(self):
        """
        Query source B of algebraic operation/the outer layer operation of compound operation.

        Returns:
        str: The source, one of {"CHAN1", "CHAN2", "FX"}.
        """
        response = self.instrument.query(":MATH:SOURce2?")
        return response.strip().upper()

    def set_math_logic_source1(self, source):
        """
        Set source A of logic operation.

        Parameters:
        source (str): The source, one of {"CHANnel1", "CHANnel2"}.
        """
        valid_sources = {"CHANnel1", "CHANnel2"}
        source = source.upper()
        if source in valid_sources:
            self.instrument.write(f":MATH:LSOUrce1 {source}")
        else:
            print(f"Invalid source ({source}). Choose from {valid_sources}.")

    def get_math_logic_source1(self):
        """
        Query source A of logic operation.

        Returns:
        str: The source, one of {"CHAN1", "CHAN2"}.
        """
        response = self.instrument.query(":MATH:LSOUrce1?")
        return response.strip().upper()

    def set_math_logic_source2(self, source):
        """
        Set source B of logic operation.

        Parameters:
        source (str): The source, one of {"CHANnel1", "CHANnel2"}.
        """
        valid_sources = {"CHANnel1", "CHANnel2"}
        source = source.upper()
        if source in valid_sources:
            self.instrument.write(f":MATH:LSOUrce2 {source}")
        else:
            print(f"Invalid source ({source}). Choose from {valid_sources}.")

    def get_math_logic_source2(self):
        """
        Query source B of logic operation.

        Returns:
        str: The source, one of {"CHAN1", "CHAN2"}.
        """
        response = self.instrument.query(":MATH:LSOUrce2?")
        return response.strip().upper()

    def set_math_scale(self, scale):
        """
        Set the vertical scale of the operation result. The unit depends on the operator
        currently selected and the unit of the source.

        Parameters:
        scale (float): The vertical scale. The max range is from 1p to 5T (in 1-2-5 step).
        """
        # The range is very broad and depends on operator/source, so basic type check.
        if isinstance(scale, (float, int)) and scale > 0: # Scale should be positive
            self.instrument.write(f":MATH:SCALE {float(scale)}")
        else:
            print(f"Invalid scale value ({scale}). Must be a positive number.")

    def get_math_scale(self):
        """
        Query the vertical scale of the operation result.

        Returns:
        float: The vertical scale of the operation result in scientific notation.
        """
        response = self.instrument.query(":MATH:SCALE?")
        return float(response.strip())

    def set_math_offset(self, offset):
        """
        Set the vertical offset of the operation result. The unit depends on the operator
        currently selected and the unit of the source.

        Parameters:
        offset (float): The vertical offset. Range: (-1000 * MathVerticalScale) to
                        (1000 * MathVerticalScale). Step: MathVerticalScale/50.
        """
        # Validation for offset range is complex as it depends on current MathVerticalScale.
        # We'll just ensure it's a number for now.
        if isinstance(offset, (float, int)):
            self.instrument.write(f":MATH:OFFSet {float(offset)}")
        else:
            print(f"Invalid offset value ({offset}). Must be a number.")

    def get_math_offset(self):
        """
        Query the vertical offset of the operation result.

        Returns:
        float: The vertical offset of the operation result in scientific notation.
        """
        response = self.instrument.query(":MATH:OFFSet?")
        return float(response.strip())

    def enable_math_invert_display(self, state):
        """
        Enable or disable the inverted display mode of the operation result.
        This command is invalid for the FFT operation.

        Parameters:
        state (bool): True to enable (ON), False to disable (OFF).
        """
        self.instrument.write(f":MATH:INVert {'ON' if state else 'OFF'}")

    def is_math_invert_display_enabled(self):
        """
        Query the inverted display mode status of the operation result.

        Returns:
        bool: True if inverted display mode is ON, False if OFF.
        """
        response = self.instrument.query(":MATH:INVert?")
        return bool(int(response.strip()))

    def reset_math_settings(self):
        """
        Adjusts the vertical scale of the operation result to the most proper value
        according to the current operator and the horizontal timebase of the source (:MATH:RESet).
        """
        self.instrument.write(":MATH:RESet")

    def set_math_fft_source(self, source):
        """
        Set the source of FFT operation/filter.

        Parameters:
        source (str): The source, one of {"CHANnel1", "CHANnel2"}.
        """
        valid_sources = {"CHANnel1", "CHANnel2"}
        source = source.upper()
        if source in valid_sources:
            self.instrument.write(f":MATH:FFT:SOURce {source}")
        else:
            print(f"Invalid source ({source}). Choose from {valid_sources}.")

    def get_math_fft_source(self):
        """
        Query the source of FFT operation/filter.

        Returns:
        str: The source, one of {"CHAN1", "CHAN2"}.
        """
        response = self.instrument.query(":MATH:FFT:SOURce?")
        return response.strip().upper()

    def set_math_fft_window(self, window_type):
        """
        Set the window function of the FFT operation.

        Parameters:
        window_type (str): The window function, one of {"RECTangle", "BLACkman",
                                                      "HANNing", "HAMMing",
                                                      "FLATtop", "TRIangle"}.
        """
        valid_windows = {"RECTangle", "BLACkman", "HANNing", "HAMMing", "FLATtop", "TRIangle"}
        window_type = window_type.upper()
        if window_type in valid_windows:
            self.instrument.write(f":MATH:FFT:WINDow {window_type}")
        else:
            print(f"Invalid window type ({window_type}). Choose from {valid_windows}.")

    def get_math_fft_window(self):
        """
        Query the window function of the FFT operation.

        Returns:
        str: The window function, one of {"RECT", "BLAC", "HANN", "HAMM", "FLAT", "TRI"}.
        """
        response = self.instrument.query(":MATH:FFT:WINDow?")
        return response.strip().upper()

    def enabled_math_fft_split_display(self, state):
        """
        Enable or disable the half-screen display mode of the FFT operation.
        When enabled, source channel and FFT results are displayed separately.

        Parameters:
        state (bool): True to enable (ON), False to disable (OFF).
        """
        self.instrument.write(f":MATH:FFT:SPLit {'ON' if state else 'OFF'}")

    def is_math_fft_split_display_enabled(self):
        """
        Query the status of the half display mode of the FFT operation.

        Returns:
        bool: True if half-screen display mode is ON, False if OFF.
        """
        response = self.instrument.query(":MATH:FFT:SPLit?")
        return bool(int(response.strip()))

    def set_math_fft_vertical_unit(self, unit):
        """
        Set the vertical unit of the FFT operation result.

        Parameters:
        unit (str): The vertical unit, one of {"VRMS", "DB"}.
        """
        valid_units = {"VRMS", "DB"}
        unit = unit.upper()
        if unit in valid_units:
            self.instrument.write(f":MATH:FFT:UNIT {unit}")
        else:
            print(f"Invalid unit ({unit}). Choose from {valid_units}.")

    def get_math_fft_vertical_unit(self):
        """
        Query the vertical unit of the FFT operation result.

        Returns:
        str: The vertical unit, one of {"VRMS", "DB"}.
        """
        response = self.instrument.query(":MATH:FFT:UNIT?")
        return response.strip().upper()

    def set_math_fft_horizontal_scale(self, h_scale):
        """
        Set the horizontal scale of the FFT operation result. Default unit is Hz.

        Parameters:
        h_scale (float): The horizontal scale. Range depends on FFT mode and sample rate.
        """
        if isinstance(h_scale, (float, int)) and h_scale > 0:
            self.instrument.write(f":MATH:FFT:HSCale {float(h_scale)}")
        else:
            print(f"Invalid horizontal scale ({h_scale}). Must be a positive number.")

    def get_math_fft_horizontal_scale(self):
        """
        Query the horizontal scale of the FFT operation result.

        Returns:
        float: The horizontal scale in scientific notation (Hz).
        """
        response = self.instrument.query(":MATH:FFT:HSCale?")
        return float(response.strip())

    def set_math_fft_horizontal_center(self, center_freq):
        """
        Set the center frequency of the FFT operation result. Default unit is Hz.

        Parameters:
        center_freq (float): The center frequency. Range depends on FFT mode and sample rate.
        """
        if isinstance(center_freq, (float, int)) and center_freq >= 0:
            self.instrument.write(f":MATH:FFT:HCENter {float(center_freq)}")
        else:
            print(f"Invalid center frequency ({center_freq}). Must be a non-negative number.")

    def get_math_fft_horizontal_center(self):
        """
        Query the center frequency of the FFT operation result.

        Returns:
        float: The current center frequency in scientific notation (Hz).
        """
        response = self.instrument.query(":MATH:FFT:HCENter?")
        return float(response.strip())

    def set_math_fft_mode(self, mode):
        """
        Set the FFT mode.

        Parameters:
        mode (str): The FFT mode, one of {"TRACE", "MEMory"}.
                    TRACE: data source is displayed waveform. MEMory: data source is waveform in memory.
        """
        valid_modes = {"TRACE", "MEMory"}
        mode = mode.upper()
        if mode in valid_modes:
            self.instrument.write(f":MATH:FFT:MODE {mode}")
        else:
            print(f"Invalid mode ({mode}). Choose from {valid_modes}.")

    def get_math_fft_mode(self):
        """
        Query the FFT mode.

        Returns:
        str: The FFT mode, one of {"TRAC", "MEM"}.
        """
        response = self.instrument.query(":MATH:FFT:MODE?")
        return response.strip().upper()

    def set_math_filter_type(self, filter_type):
        """
        Set the filter type.

        Parameters:
        filter_type (str): The filter type, one of {"LPASS", "HPASS", "BPASS", "BSTOP"}.
        """
        valid_types = {"LPASS", "HPASS", "BPASS", "BSTOP"}
        filter_type = filter_type.upper()
        if filter_type in valid_types:
            self.instrument.write(f":MATH:FILTer:TYPE {filter_type}")
        else:
            print(f"Invalid filter type ({filter_type}). Choose from {valid_types}.")

    def get_math_filter_type(self):
        """
        Query the filter type.

        Returns:
        str: The filter type, one of {"LPAS", "HPAS", "BPAS", "BSTOP"}.
        """
        response = self.instrument.query(":MATH:FILTer:TYPE?")
        return response.strip().upper()

    def set_math_filter_w1(self, freq1):
        """
        Set the cutoff frequency (wc1) of the low pass/high pass filter or cutoff
        frequency 1 (wc1) of the band pass/band stop filter. Default unit is Hz.

        Parameters:
        freq1 (float): The cutoff frequency. Range depends on filter type and screen sample rate.
        """
        if isinstance(freq1, (float, int)) and freq1 >= 0: # Frequencies should be non-negative
            self.instrument.write(f":MATH:FILTer:W1 {float(freq1)}")
        else:
            print(f"Invalid frequency ({freq1}). Must be a non-negative number.")

    def get_math_filter_w1(self):
        """
        Query the cutoff frequency (wc1) of the low pass/high pass filter or cutoff
        frequency 1 (wc1) of the band pass/band stop filter.

        Returns:
        float: The current cutoff frequency or cutoff frequency 1 in scientific notation (Hz).
        """
        response = self.instrument.query(":MATH:FILTer:W1?")
        return float(response.strip())

    def set_math_filter_w2(self, freq2):
        """
        Set the cutoff frequency 2 (wc2) of the band pass/band stop filter. Default unit is Hz.
        This command is only applicable to band pass/band stop filters.

        Parameters:
        freq2 (float): The cutoff frequency 2. Range depends on filter type and screen sample rate.
        """
        if isinstance(freq2, (float, int)) and freq2 >= 0: # Frequencies should be non-negative
            self.instrument.write(f":MATH:FILTer:W2 {float(freq2)}")
        else:
            print(f"Invalid frequency ({freq2}). Must be a non-negative number.")

    def get_math_filter_w2(self):
        """
        Query the cutoff frequency 2 (wc2) of the band pass/band stop filter.

        Returns:
        float: Current cutoff frequency 2 in scientific notation (Hz).
        """
        response = self.instrument.query(":MATH:FILTer:W2?")
        return float(response.strip())

    def set_math_option_start_point(self, start_point):
        """
        Set the start point of the waveform math operation.
        This command is invalid for the FFT operation. The source selected is equally
        divided into 1200 parts horizontally, in which the leftmost is 0 and the rightmost is 1199.

        Parameters:
        start_point (int): The start point, from 0 to (End point currently set - 1).
        """
        if isinstance(start_point, int) and 0 <= start_point <= 1198: # Max end point is 1199, so start can be up to 1198
            self.instrument.write(f":MATH:OPTion:STARt {start_point}")
        else:
            print(f"Invalid start point ({start_point}). Must be an integer between 0 and 1198.")

    def get_math_option_start_point(self):
        """
        Query the start point of the waveform math operation.

        Returns:
        int: The start point in integer.
        """
        response = self.instrument.query(":MATH:OPTion:STARt?")
        return int(response.strip())

    def set_math_option_end_point(self, end_point):
        """
        Set the end point of the waveform math operation.
        This command is invalid for the FFT operation. The source selected is equally
        divided into 1200 parts horizontally, in which the leftmost is 0 and the rightmost is 1199.

        Parameters:
        end_point (int): The end point, from (Start point currently set + 1) to 1199.
        """
        if isinstance(end_point, int) and 1 <= end_point <= 1199: # Min start point is 0, so end can be at least 1
            self.instrument.write(f":MATH:OPTion:END {end_point}")
        else:
            print(f"Invalid end point ({end_point}). Must be an integer between 1 and 1199.")

    def get_math_option_end_point(self):
        """
        Query the end point of the waveform math operation.

        Returns:
        int: The end point in integer.
        """
        response = self.instrument.query(":MATH:OPTion:END?")
        return int(response.strip())

    def enabled_math_option_invert_display(self, state):
        """
        Enable or disable the inverted display mode of the operation result.
        This command is invalid for the FFT operation.

        Parameters:
        state (bool): True to enable (ON), False to disable (OFF).
        """
        self.instrument.write(f":MATH:OPTion:INVert {'ON' if state else 'OFF'}")

    def is_math_option_invert_display_enabled(self):
        """
        Query the inverted display mode status of the operation result.

        Returns:
        bool: True if inverted display mode is ON, False if OFF.
        """
        response = self.instrument.query(":MATH:OPTion:INVert?")
        return bool(int(response.strip()))

    def set_math_option_sensitivity(self, sensitivity):
        """
        Set the sensitivity of the logic operation. Default unit is div (current vertical scale).
        This command is only applicable to logic operations (A&&B, A||B, A^B, and !A).

        Parameters:
        sensitivity (float): The sensitivity, from 0 to 0.96, step is 0.08.
        """
        if isinstance(sensitivity, (float, int)) and 0 <= sensitivity <= 0.96:
            # Optional: Add check for step 0.08 if strict adherence is needed
            self.instrument.write(f":MATH:OPTion:SENSitivity {float(sensitivity)}")
        else:
            print(f"Invalid sensitivity ({sensitivity}). Must be a float between 0 and 0.96.")

    def get_math_option_sensitivity(self):
        """
        Query the sensitivity of the logic operation.

        Returns:
        float: The current sensitivity in scientific notation.
        """
        response = self.instrument.query(":MATH:OPTion:SENSitivity?")
        return float(response.strip())

    def set_math_option_distance(self, distance):
        """
        Set the smoothing window width of differential operation (diff).
        This command is only applicable to differential operation (diff).

        Parameters:
        distance (int): The smoothing window width, from 3 to 201.
        """
        if isinstance(distance, int) and 3 <= distance <= 201:
            self.instrument.write(f":MATH:OPTion:DIStance {distance}")
        else:
            print(f"Invalid distance ({distance}). Must be an integer between 3 and 201.")

    def get_math_option_distance(self):
        """
        Query the smoothing window width of differential operation (diff).

        Returns:
        int: The smoothing window width.
        """
        response = self.instrument.query(":MATH:OPTion:DIStance?")
        return int(response.strip())

    def enabled_math_option_auto_scale(self, state):
        """
        Enable or disable the auto scale setting of the operation result.

        Parameters:
        state (bool): True to enable (ON), False to disable (OFF).
        """
        self.instrument.write(f":MATH:OPTion:ASCale {'ON' if state else 'OFF'}")

    def is_math_option_auto_scale_enabled(self):
        """
        Query the status of the auto scale setting.

        Returns:
        bool: True if auto scale is ON, False if OFF.
        """
        response = self.instrument.query(":MATH:OPTion:ASCale?")
        return bool(int(response.strip()))

    def set_math_option_threshold1(self, threshold):
        """
        Set the threshold level of source A in logic operations. Default unit is V.
        This command is only applicable to A&&B, A||B, A^B, and !A logic operations
        of which source A is an analog channel.

        Parameters:
        threshold (float): The threshold level. Range: (-4 * VerticalScale - VerticalOffset) to
                           (4 * VerticalScale - VerticalOffset). Step: VerticalScale/50.
        """
        # Range depends on source A's scale and offset, so only basic type check.
        if isinstance(threshold, (float, int)):
            self.instrument.write(f":MATH:OPTion:THReshold1 {float(threshold)}")
        else:
            print(f"Invalid threshold ({threshold}). Must be a number.")

    def get_math_option_threshold1(self):
        """
        Query the threshold level of source A in logic operations.

        Returns:
        float: The threshold level in scientific notation (V).
        """
        response = self.instrument.query(":MATH:OPTion:THReshold1?")
        return float(response.strip())

    def set_math_option_threshold2(self, threshold):
        """
        Set the threshold level of source B in logic operations. Default unit is V.
        This command is only applicable to A&&B, A||B, and A^B logic operations
        of which source B is an analog channel.

        Parameters:
        threshold (float): The threshold level. Range: (-4 * VerticalScale - VerticalOffset) to
                           (4 * VerticalScale - VerticalOffset). Step: VerticalScale/50.
        """
        # Range depends on source B's scale and offset, so only basic type check.
        if isinstance(threshold, (float, int)):
            self.instrument.write(f":MATH:OPTion:THReshold2 {float(threshold)}")
        else:
            print(f"Invalid threshold ({threshold}). Must be a number.")

    def get_math_option_threshold2(self):
        """
        Query the threshold level of source B in logic operations.

        Returns:
        float: The threshold level in scientific notation (V).
        """
        response = self.instrument.query(":MATH:OPTion:THReshold2?")
        return float(response.strip())

    def set_math_option_fx_source1(self, source):
        """
        Set source A of the inner layer operation of compound operation.

        Parameters:
        source (str): The source, one of {"CHANnel1", "CHANnel2"}.
        """
        valid_sources = {"CHANnel1", "CHANnel2"}
        source = source.upper()
        if source in valid_sources:
            self.instrument.write(f":MATH:OPTion:FX:SOURce1 {source}")
        else:
            print(f"Invalid source ({source}). Choose from {valid_sources}.")

    def get_math_option_fx_source1(self):
        """
        Query source A of the inner layer operation of compound operation.

        Returns:
        str: The source, one of {"CHAN1", "CHAN2"}.
        """
        response = self.instrument.query(":MATH:OPTion:FX:SOURce1?")
        return response.strip().upper()

    def set_math_option_fx_source2(self, source):
        """
        Set source B of the inner layer operation of compound operation.

        Parameters:
        source (str): The source, one of {"CHANnel1", "CHANnel2"}.
        """
        valid_sources = {"CHANnel1", "CHANnel2"}
        source = source.upper()
        if source in valid_sources:
            self.instrument.write(f":MATH:OPTion:FX:SOURce2 {source}")
        else:
            print(f"Invalid source ({source}). Choose from {valid_sources}.")

    def get_math_option_fx_source2(self):
        """
        Query source B of the inner layer operation of compound operation.

        Returns:
        str: The source, one of {"CHAN1", "CHAN2"}.
        """
        response = self.instrument.query(":MATH:OPTion:FX:SOURce2?")
        return response.strip().upper()

    def set_math_option_fx_operator(self, operator):
        """
        Set the operator of the inner layer operation of compound operation.

        Parameters:
        operator (str): The operator, one of {"ADD", "SUBTract", "MULTiply", "DIVision"}.
        """
        valid_operators = {"ADD", "SUBTract", "MULTiply", "DIVision"}
        operator = operator.upper()
        if operator in valid_operators:
            self.instrument.write(f":MATH:OPTion:FX:OPERator {operator}")
        else:
            print(f"Invalid operator ({operator}). Choose from {valid_operators}.")

    def get_math_option_fx_operator(self):
        """
        Query the operator of the inner layer operation of compound operation.

        Returns:
        str: The operator, one of {"ADD", "SUBT", "MULT", "DIV"}.
        """
        response = self.instrument.query(":MATH:OPTion:FX:OPERator?")
        return response.strip().upper()

    # MASK Commands
    def enable_mask(self, state):
        """
        Enable or disable the pass/fail test.

        Parameters:
        state (bool): True to enable (ON), False to disable (OFF).
        """
        self.instrument.write(f":MASK:ENABle {'ON' if state else 'OFF'}")

    def is_mask_enabled(self):
        """
        Query the status of the pass/fail test.

        Returns:
        bool: True if pass/fail test is ON, False if OFF.
        """
        response = self.instrument.query(":MASK:ENABle?")
        return bool(int(response.strip()))

    def set_mask_source(self, source):
        """
        Set the source of the pass/fail test.

        Parameters:
        source (str): The source channel, one of {"CHANnel1", "CHANnel2"}.
        """
        valid_sources = {"CHANnel1", "CHANnel2"}
        source = source.upper()
        if source in valid_sources:
            self.instrument.write(f":MASK:SOURce {source}")
        else:
            print(f"Invalid source ({source}). Choose from {valid_sources}.")

    def get_mask_source(self):
        """
        Query the source of the pass/fail test.

        Returns:
        str: The source channel, one of {"CHAN1", "CHAN2"}.
        """
        response = self.instrument.query(":MASK:SOURce?")
        return response.strip().upper()

    def set_mask_operate(self, operate_mode):
        """
        Run or stop the pass/fail test.

        Parameters:
        operate_mode (str): The operation mode, one of {"RUN", "STOP"}.
        """
        valid_modes = {"RUN", "STOP"}
        operate_mode = operate_mode.upper()
        if operate_mode in valid_modes:
            self.instrument.write(f":MASK:OPERate {operate_mode}")
        else:
            print(f"Invalid operate mode ({operate_mode}). Choose from {valid_modes}.")

    def get_mask_operate(self):
        """
        Query the status of the pass/fail test.

        Returns:
        str: The status, one of {"RUN", "STOP"}.
        """
        response = self.instrument.query(":MASK:OPERate?")
        return response.strip().upper()

    def enable_mask_display_statistics(self, state):
        """
        Enable or disable the statistic information when the pass/fail test is enabled.

        Parameters:
        state (bool): True to enable (ON), False to disable (OFF).
        """
        self.instrument.write(f":MASK:MDISplay {'ON' if state else 'OFF'}")

    def is_mask_display_statistics_enabled(self):
        """
        Query the status of the statistic information.

        Returns:
        bool: True if statistic information is ON, False if OFF.
        """
        response = self.instrument.query(":MASK:MDISplay?")
        return bool(int(response.strip()))

    def set_mask_stop_on_fail_output(self, state):
        """
        Turn the "Stop on Fail" function on or off.
        When ON, oscilloscope stops test and enters "STOP" state on failed waveforms.

        Parameters:
        state (bool): True to turn on (ON), False to turn off (OFF).
        """
        self.instrument.write(f":MASK:SOOutput {'ON' if state else 'OFF'}")

    def get_mask_stop_on_fail_output(self):
        """
        Query the status of the "Stop on Fail" function.

        Returns:
        bool: True if "Stop on Fail" is ON, False if OFF.
        """
        response = self.instrument.query(":MASK:SOOutput?")
        return bool(int(response.strip()))

    def enable_mask_sound_output(self, state):
        """
        Enable or disable the sound prompt when failed waveforms are detected.

        Parameters:
        state (bool): True to enable (ON), False to disable (OFF).
        """
        self.instrument.write(f":MASK:OUTPut {'ON' if state else 'OFF'}")

    def is_mask_sound_output_enabled(self):
        """
        Query the status of the sound prompt.

        Returns:
        bool: True if sound prompt is ON, False if OFF.
        """
        response = self.instrument.query(":MASK:OUTPut?")
        return bool(int(response.strip()))

    def set_mask_x_adjustment(self, x_value):
        """
        Set the horizontal adjustment parameter in the pass/fail test mask. Default unit is div.

        Parameters:
        x_value (float): The horizontal adjustment parameter, from 0.02 to 4, step is 0.02.
        """
        if isinstance(x_value, (float, int)) and 0.02 <= x_value <= 4.0:
            self.instrument.write(f":MASK:X {float(x_value)}")
        else:
            print(f"Invalid X adjustment value ({x_value}). Must be a float between 0.02 and 4.0.")

    def get_mask_x_adjustment(self):
        """
        Query the horizontal adjustment parameter in the pass/fail test mask.

        Returns:
        float: The horizontal adjustment parameter in scientific notation.
        """
        response = self.instrument.query(":MASK:X?")
        return float(response.strip())

    def set_mask_y_adjustment(self, y_value):
        """
        Set the vertical adjustment parameter in the pass/fail test mask. Default unit is div.

        Parameters:
        y_value (float): The vertical adjustment parameter, from 0.04 to 5.12, step is 0.04.
        """
        if isinstance(y_value, (float, int)) and 0.04 <= y_value <= 5.12:
            self.instrument.write(f":MASK:Y {float(y_value)}")
        else:
            print(f"Invalid Y adjustment value ({y_value}). Must be a float between 0.04 and 5.12.")

    def get_mask_y_adjustment(self):
        """
        Query the vertical adjustment parameter in the pass/fail test mask.

        Returns:
        float: The vertical adjustment parameter in scientific notation.
        """
        response = self.instrument.query(":MASK:Y?")
        return float(response.strip())

    def create_mask(self):
        """
        Create the pass/fail test mask using the current horizontal adjustment parameter
        and vertical adjustment parameter (:MASK:CREate).
        This command is valid only when the pass/fail test is enabled and is not in the run state.
        """
        self.instrument.write(":MASK:CREate")

    def get_mask_passed_frames(self):
        """
        Query the number of passed frames in the pass/fail test.

        Returns:
        int: The number of passed frames.
        """
        response = self.instrument.query(":MASK:PASSed?")
        return int(response.strip())

    def get_mask_failed_frames(self):
        """
        Query the number of failed frames in the pass/fail test.

        Returns:
        int: The number of failed frames.
        """
        response = self.instrument.query(":MASK:FAILed?")
        return int(response.strip())

    def get_mask_total_frames(self):
        """
        Query the total number of frames in the pass/fail test.

        Returns:
        int: The total number of frames.
        """
        response = self.instrument.query(":MASK:TOTal?")
        return int(response.strip())

    def reset_mask_statistics(self):
        """
        Reset the numbers of passed frames and failed frames as well as the total number
        of frames in the pass/fail test to 0 (:MASK:RESet).
        """
        self.instrument.write(":MASK:RESet")

    # MEASURE Commands
    def set_measure_source(self, source):
        """
        Set the source of the current measurement parameter.

        Parameters:
        source (str): The source, one of {"CHANnel1", "CHANnel2", "MATH"}.
        """
        valid_sources = {"CHANnel1", "CHANnel2", "MATH"}
        source = source.upper()
        if source in valid_sources:
            self.instrument.write(f":MEASure:SOURce {source}")
        else:
            print(f"Invalid source ({source}). Choose from {valid_sources}.")

    def get_measure_source(self):
        """
        Query the source of the current measurement parameter.

        Returns:
        str: The source, one of {"CHAN1", "CHAN2", "MATH"}.
        """
        response = self.instrument.query(":MEASure:SOURce?")
        return response.strip().upper()

    def set_measure_counter_source(self, source):
        """
        Set the source of the frequency counter, or disable the frequency counter.

        Parameters:
        source (str): The source, one of {"CHANnel1", "CHANnel2", "OFF"}.
        """
        valid_sources = {"CHANnel1", "CHANnel2", "OFF"}
        source = source.upper()
        if source in valid_sources:
            self.instrument.write(f":MEASure:COUNter:SOURce {source}")
        else:
            print(f"Invalid source ({source}). Choose from {valid_sources}.")

    def get_measure_counter_source(self):
        """
        Query the source of the frequency counter.

        Returns:
        str: The source, one of {"CHAN1", "CHAN2", "OFF"}.
        """
        response = self.instrument.query(":MEASure:COUNter:SOURce?")
        return response.strip().upper()

    def get_measure_counter_value(self):
        """
        Query the measurement result of the frequency counter. Default unit is Hz.

        Returns:
        float: The measurement result in scientific notation. Returns 0.0 if disabled.
        """
        response = self.instrument.query(":MEASure:COUNter:VALue?")
        return float(response.strip())

    def clear_measure_item(self, item):
        """
        Clear one or all of the last five measurement items enabled.

        Parameters:
        item (str): The item to clear, one of {"ITEM1", "ITEM2", "ITEM3", "ITEM4", "ITEM5", "ALL"}.
        """
        valid_items = {"ITEM1", "ITEM2", "ITEM3", "ITEM4", "ITEM5", "ALL"}
        item = item.upper()
        if item in valid_items:
            self.instrument.write(f":MEASure:CLEar {item}")
        else:
            print(f"Invalid item ({item}). Choose from {valid_items}.")

    def recover_measure_item(self, item):
        """
        Recover the measurement item which has been cleared.

        Parameters:
        item (str): The item to recover, one of {"ITEM1", "ITEM2", "ITEM3", "ITEM4", "ITEM5", "ALL"}.
        """
        valid_items = {"ITEM1", "ITEM2", "ITEM3", "ITEM4", "ITEM5", "ALL"}
        item = item.upper()
        if item in valid_items:
            self.instrument.write(f":MEASure:RECover {item}")
        else:
            print(f"Invalid item ({item}). Choose from {valid_items}.")

    def enable_all_measure_display(self, state):
        """
        Enable or disable the all measurement function.

        Parameters:
        state (bool): True to enable (ON), False to disable (OFF).
        """
        self.instrument.write(f":MEASure:ADISplay {'ON' if state else 'OFF'}")

    def is_all_measure_display_enabled(self):
        """
        Query the status of the all measurement function.

        Returns:
        bool: True if all measurement function is ON, False if OFF.
        """
        response = self.instrument.query(":MEASure:ADISplay?")
        return bool(int(response.strip()))

    def set_all_measure_source(self, sources):
        """
        Set the source(s) of the all measurement function.

        Parameters:
        sources (str or list): A single source string or a list of source strings,
                               e.g., "CHANnel1", ["CHANnel1", "CHANnel2"].
                               Valid sources: {"CHANnel1", "CHANnel2", "MATH"}.
        """
        valid_sources = {"CHANnel1", "CHANnel2", "MATH"}
        if isinstance(sources, str):
            sources = [sources]

        formatted_sources = []
        for src in sources:
            src_upper = src.upper()
            if src_upper in valid_sources:
                formatted_sources.append(src_upper)
            else:
                print(f"Invalid source ({src}). Skipping. Valid sources: {valid_sources}")
        
        if formatted_sources:
            self.instrument.write(f":MEASure:AMSource {','.join(formatted_sources)}")
        else:
            print("No valid sources provided for all measurement function.")

    def get_all_measure_source(self):
        """
        Query the source(s) of the all measurement function.

        Returns:
        list of str: The sources, e.g., ["CHAN1", "CHAN2"].
        """
        response = self.instrument.query(":MEASure:AMSource?")
        return [s.strip().upper() for s in response.strip().split(',')]

    def set_measure_setup_max_threshold(self, value):
        """
        Set the upper limit of the threshold (expressed in the percentage of amplitude)
        in time, delay, and phase measurements.

        Parameters:
        value (int): The percentage value, from 7 to 95.
        """
        if isinstance(value, int) and 7 <= value <= 95:
            self.instrument.write(f":MEASure:SETup:MAX {value}")
        else:
            print(f"Invalid value ({value}). Must be an integer between 7 and 95.")

    def get_measure_setup_max_threshold(self):
        """
        Query the upper limit of the threshold.

        Returns:
        int: The percentage value (7 to 95).
        """
        response = self.instrument.query(":MEASure:SETup:MAX?")
        return int(response.strip())

    def set_measure_setup_mid_threshold(self, value):
        """
        Set the middle point of the threshold (expressed in the percentage of amplitude)
        in time, delay, and phase measurements.

        Parameters:
        value (int): The percentage value, from 6 to 94.
        """
        if isinstance(value, int) and 6 <= value <= 94:
            self.instrument.write(f":MEASure:SETup:MID {value}")
        else:
            print(f"Invalid value ({value}). Must be an integer between 6 and 94.")

    def get_measure_setup_mid_threshold(self):
        """
        Query the middle point of the threshold.

        Returns:
        int: The percentage value (6 to 94).
        """
        response = self.instrument.query(":MEASure:SETup:MID?")
        return int(response.strip())

    def set_measure_setup_min_threshold(self, value):
        """
        Set the lower limit of the threshold (expressed in the percentage of amplitude)
        in time, delay, and phase measurements.

        Parameters:
        value (int): The percentage value, from 5 to 93.
        """
        if isinstance(value, int) and 5 <= value <= 93:
            self.instrument.write(f":MEASure:SETup:MIN {value}")
        else:
            print(f"Invalid value ({value}). Must be an integer between 5 and 93.")

    def get_measure_setup_min_threshold(self):
        """
        Query the lower limit of the threshold.

        Returns:
        int: The percentage value (5 to 93).
        """
        response = self.instrument.query(":MEASure:SETup:MIN?")
        return int(response.strip())

    def set_measure_setup_phase_source_a(self, source):
        """
        Set source A of Phase 1→2 and Phase 1→2 measurements.

        Parameters:
        source (str): The source, one of {"CHANnel1", "CHANnel2"}.
        """
        valid_sources = {"CHANnel1", "CHANnel2"}
        source = source.upper()
        if source in valid_sources:
            self.instrument.write(f":MEASure:SETup:PSA {source}")
        else:
            print(f"Invalid source ({source}). Choose from {valid_sources}.")

    def get_measure_setup_phase_source_a(self):
        """
        Query source A of Phase 1→2 and Phase 1→2 measurements.

        Returns:
        str: The source, one of {"CHAN1", "CHAN2"}.
        """
        response = self.instrument.query(":MEASure:SETup:PSA?")
        return response.strip().upper()

    def set_measure_setup_phase_source_b(self, source):
        """
        Set source B of Phase 1→2 and Phase 1→2 measurements.

        Parameters:
        source (str): The source, one of {"CHANnel1", "CHANnel2"}.
        """
        valid_sources = {"CHANnel1", "CHANnel2"}
        source = source.upper()
        if source in valid_sources:
            self.instrument.write(f":MEASure:SETup:PSB {source}")
        else:
            print(f"Invalid source ({source}). Choose from {valid_sources}.")

    def get_measure_setup_phase_source_b(self):
        """
        Query source B of Phase 1→2 and Phase 1→2 measurements.

        Returns:
        str: The source, one of {"CHAN1", "CHAN2"}.
        """
        response = self.instrument.query(":MEASure:SETup:PSB?")
        return response.strip().upper()

    def set_measure_setup_delay_source_a(self, source):
        """
        Set source A of Delay 1→2 and Delay 1→2 measurements.

        Parameters:
        source (str): The source, one of {"CHANnel1", "CHANnel2"}.
        """
        valid_sources = {"CHANnel1", "CHANnel2"}
        source = source.upper()
        if source in valid_sources:
            self.instrument.write(f":MEASure:SETup:DSA {source}")
        else:
            print(f"Invalid source ({source}). Choose from {valid_sources}.")

    def get_measure_setup_delay_source_a(self):
        """
        Query source A of Delay 1→2 and Delay 1→2 measurements.

        Returns:
        str: The source, one of {"CHAN1", "CHAN2"}.
        """
        response = self.instrument.query(":MEASure:SETup:DSA?")
        return response.strip().upper()

    def set_measure_setup_delay_source_b(self, source):
        """
        Set source B of Delay 1→2 and Delay 1→2 measurements.

        Parameters:
        source (str): The source, one of {"CHANnel1", "CHANnel2"}.
        """
        valid_sources = {"CHANnel1", "CHANnel2"}
        source = source.upper()
        if source in valid_sources:
            self.instrument.write(f":MEASure:SETup:DSB {source}")
        else:
            print(f"Invalid source ({source}). Choose from {valid_sources}.")

    def get_measure_setup_delay_source_b(self):
        """
        Query source B of Delay 1→2 and Delay 1→2 measurements.

        Returns:
        str: The source, one of {"CHAN1", "CHAN2"}.
        """
        response = self.instrument.query(":MEASure:SETup:DSB?")
        return response.strip().upper()

    def enable_measure_statistic_display(self, state):
        """
        Enable or disable the statistic function.

        Parameters:
        state (bool): True to enable (ON), False to disable (OFF).
        """
        self.instrument.write(f":MEASure:STATistic:DISPlay {'ON' if state else 'OFF'}")

    def is_measure_statistic_display_enabled(self):
        """
        Query the status of the statistic function.

        Returns:
        bool: True if statistic function is ON, False if OFF.
        """
        response = self.instrument.query(":MEASure:STATistic:DISPlay?")
        return bool(int(response.strip()))

    def set_measure_statistic_mode(self, mode):
        """
        Set the statistic mode.

        Parameters:
        mode (str): The statistic mode, one of {"DIFFerence", "EXTRemum"}.
        """
        valid_modes = {"DIFFerence", "EXTRemum"}
        mode = mode.upper()
        if mode in valid_modes:
            self.instrument.write(f":MEASure:STATistic:MODE {mode}")
        else:
            print(f"Invalid mode ({mode}). Choose from {valid_modes}.")

    def get_measure_statistic_mode(self):
        """
        Query the statistic mode.

        Returns:
        str: The statistic mode, one of {"DIFF", "EXTR"}.
        """
        response = self.instrument.query(":MEASure:STATistic:MODE?")
        return response.strip().upper()

    def reset_measure_statistic(self):
        """
        Clear the history data and make statistic again (:MEASure:STATistic:RESet).
        """
        self.instrument.write(":MEASure:STATistic:RESet")

    def set_measure_statistic_item(self, item, sources=None):
        """
        Enable the statistic function of any waveform parameter of the specified source.

        Parameters:
        item (str): The waveform parameter. See PDF for full list.
        sources (str or list, optional): A single source string or a list of source strings.
                                         Valid sources: {"CHANnel1", "CHANnel2", "MATH"}.
                                         Required for two-source parameters (RDELay, FDELay, RPHase, FPHase).
        """
        valid_items = {"VMAX", "VMIN", "VPP", "VTOP", "VBASe", "VAMP", "VAVG", "VRMS",
                       "OVERshoot", "PREShoot", "MARea", "MPARea", "PERiod", "FREQuency",
                       "RTIMe", "FTIMe", "PWIDth", "NWIDth", "PDUTy", "NDUTy", "RDELay",
                       "FDELay", "RPHase", "FPHase", "TVMAX", "TVMIN", "PSLEWrate",
                       "NSLEWrate", "VUPper", "VMID", "VLOWer", "VARIance", "PVRMS",
                       "PPULses", "NPULses", "PEDGes", "NEDGes"}
        valid_sources = {"CHANnel1", "CHANnel2", "MATH"}

        item = item.upper()
        if item not in valid_items:
            print(f"Invalid measurement item ({item}).")
            return

        command_parts = [item]
        if sources:
            if isinstance(sources, str):
                sources = [sources]
            for src in sources:
                src_upper = src.upper()
                if src_upper in valid_sources:
                    command_parts.append(src_upper)
                else:
                    print(f"Invalid source ({src}) for item {item}. Skipping.")
                    return # Stop if an invalid source is provided

        self.instrument.write(f":MEASure:STATistic:ITEM {','.join(command_parts)}")

    def get_measure_statistic_item(self, stat_type, item, sources=None):
        """
        Query the statistic result of any waveform parameter of the specified source.

        Parameters:
        stat_type (str): The statistic type, one of {"MAXimum", "MINimum", "CURRent", "AVERages", "DEViation"}.
        item (str): The waveform parameter. See PDF for full list.
        sources (str or list, optional): A single source string or a list of source strings.
                                         Valid sources: {"CHANnel1", "CHANnel2", "MATH"}.
                                         Required for two-source parameters (RDELay, FDELay, RPHase, FPHase).

        Returns:
        float: The statistic result in scientific notation.
        """
        valid_stat_types = {"MAXimum", "MINimum", "CURRent", "AVERages", "DEViation"}
        valid_items = {"VMAX", "VMIN", "VPP", "VTOP", "VBASe", "VAMP", "VAVG", "VRMS",
                       "OVERshoot", "PREShoot", "MARea", "MPARea", "PERiod", "FREQuency",
                       "RTIMe", "FTIMe", "PWIDth", "NWIDth", "PDUTy", "NDUTy", "RDELay",
                       "FDELay", "RPHase", "FPHase", "TVMAX", "TVMIN", "PSLEWrate",
                       "NSLEWrate", "VUPper", "VMID", "VLOWer", "VARIance", "PVRMS",
                       "PPULses", "NPULses", "PEDGes", "NEDGes"}
        valid_sources = {"CHANnel1", "CHANnel2", "MATH"}

        stat_type = stat_type.upper()
        item = item.upper()

        if stat_type not in valid_stat_types:
            print(f"Invalid statistic type ({stat_type}).")
            return None
        if item not in valid_items:
            print(f"Invalid measurement item ({item}).")
            return None

        command_parts = [stat_type, item]
        if sources:
            if isinstance(sources, str):
                sources = [sources]
            for src in sources:
                src_upper = src.upper()
                if src_upper in valid_sources:
                    command_parts.append(src_upper)
                else:
                    print(f"Invalid source ({src}) for item {item}. Skipping.")
                    return None # Stop if an invalid source is provided

        response = self.instrument.query(f":MEASure:STATistic:ITEM? {','.join(command_parts)}")
        return float(response.strip())

    def set_measure_item(self, item, sources=None):
        """
        Measure any waveform parameter of the specified source.

        Parameters:
        item (str): The waveform parameter. See PDF for full list.
        sources (str or list, optional): A single source string or a list of source strings.
                                         Valid sources: {"CHANnel1", "CHANnel2", "MATH"}.
                                         Required for two-source parameters (RDELay, FDELay, RPHase, FPHase).
        """
        valid_items = {"VMAX", "VMIN", "VPP", "VTOP", "VBASe", "VAMP", "VAVG", "VRMS",
                       "OVERshoot", "PREShoot", "MARea", "MPARea", "PERiod", "FREQuency",
                       "RTIMe", "FTIMe", "PWIDth", "NWIDth", "PDUTy", "NDUTy", "RDELay",
                       "FDELay", "RPHase", "FPHase", "TVMAX", "TVMIN", "PSLEWrate",
                       "NSLEWrate", "VUPper", "VMID", "VLOWer", "VARIance", "PVRMS",
                       "PPULses", "NPULses", "PEDGes", "NEDGes"}
        valid_sources = {"CHANnel1", "CHANnel2", "MATH"}

        item = item.upper()
        if item not in valid_items:
            print(f"Invalid measurement item ({item}).")
            return

        command_parts = [item]
        if sources:
            if isinstance(sources, str):
                sources = [sources]
            for src in sources:
                src_upper = src.upper()
                if src_upper in valid_sources:
                    command_parts.append(src_upper)
                else:
                    print(f"Invalid source ({src}) for item {item}. Skipping.")
                    return # Stop if an invalid source is provided

        self.instrument.write(f":MEASure:ITEM {','.join(command_parts)}")

    def get_measure_item(self, item, sources=None):
        """
        Query the measurement result of any waveform parameter of the specified source.

        Parameters:
        item (str): The waveform parameter. See PDF for full list.
        sources (str or list, optional): A single source string or a list of source strings.
                                         Valid sources: {"CHANnel1", "CHANnel2", "MATH"}.
                                         Required for two-source parameters (RDELay, FDELay, RPHase, FPHase).

        Returns:
        float: The measurement result in scientific notation.
        """
        valid_items = {"VMAX", "VMIN", "VPP", "VTOP", "VBASe", "VAMP", "VAVG", "VRMS",
                       "OVERshoot", "PREShoot", "MARea", "MPARea", "PERiod", "FREQuency",
                       "RTIMe", "FTIMe", "PWIDth", "NWIDth", "PDUTy", "NDUTy", "RDELay",
                       "FDELay", "RPHase", "FPHase", "TVMAX", "TVMIN", "PSLEWrate",
                       "NSLEWrate", "VUPper", "VMID", "VLOWer", "VARIance", "PVRMS",
                       "PPULses", "NPULses", "PEDGes", "NEDGes"}
        valid_sources = {"CHANnel1", "CHANnel2", "MATH"}

        item = item.upper()
        if item not in valid_items:
            print(f"Invalid measurement item ({item}).")
            return None

        command_parts = [item]
        if sources:
            if isinstance(sources, str):
                sources = [sources]
            for src in sources:
                src_upper = src.upper()
                if src_upper in valid_sources:
                    command_parts.append(src_upper)
                else:
                    print(f"Invalid source ({src}) for item {item}. Skipping.")
                    return None # Stop if an invalid source is provided

        response = self.instrument.query(f":MEASure:ITEM? {','.join(command_parts)}")
        return float(response.strip())

    # Reference Commands - For controlling 
    # llhand set a reference waveform to compare the measured waveform against
    def enable_reference_display(self, state):
        """
        Enable or disable the REF function.

        Parameters:
        state (bool): True to enable (ON), False to disable (OFF).
        """
        self.instrument.write(f":REFerence:DISPlay {'ON' if state else 'OFF'}")

    def is_reference_display_enabled(self):
        """
        Query the status of the REF function.

        Returns:
        bool: True if REF function is ON, False if OFF.
        """
        response = self.instrument.query(":REFerence:DISPlay?")
        return bool(int(response.strip()))

    def enable_reference_channel_enable(self, n, state):
        """
        Enable or disable the specified reference channel.

        Parameters:
        n (int): The reference channel number, from 1 to 10.
        state (bool): True to enable (ON), False to disable (OFF).
        """
        valid_channels = list(range(1, 11))
        if n in valid_channels:
            self.instrument.write(f":REFerence{n}:ENABle {'ON' if state else 'OFF'}")
        else:
            print(f"Invalid reference channel ({n}). Choose from {valid_channels}.")

    def is_reference_channel_enabled(self, n):
        """
        Query the status of the specified reference channel.

        Parameters:
        n (int): The reference channel number, from 1 to 10.

        Returns:
        bool: True if reference channel is ON, False if OFF.
        """
        valid_channels = list(range(1, 11))
        if n in valid_channels:
            response = self.instrument.query(f":REFerence{n}:ENABle?")
            return bool(int(response.strip()))
        else:
            print(f"Invalid reference channel ({n}). Choose from {valid_channels}.")
            return None

    def set_reference_channel_source(self, n, source):
        """
        Set the source of the current reference channel.

        Parameters:
        n (int): The reference channel number, from 1 to 10.
        source (str): The source, one of {"CHANnel1", "CHANnel2", "MATH"}.
        """
        valid_channels = list(range(1, 11))
        valid_sources = {"CHANnel1", "CHANnel2", "MATH"}
        source = source.upper()
        if n in valid_channels and source in valid_sources:
            self.instrument.write(f":REFerence{n}:SOURce {source}")
        else:
            print(f"Invalid reference channel ({n}) or source ({source}).")

    def get_reference_channel_source(self, n):
        """
        Query the source of the current reference channel.

        Parameters:
        n (int): The reference channel number, from 1 to 10.

        Returns:
        str: The source, one of {"CHAN1", "CHAN2", "MATH"}.
        """
        valid_channels = list(range(1, 11))
        if n in valid_channels:
            response = self.instrument.query(f":REFerence{n}:SOURce?")
            return response.strip().upper()
        else:
            print(f"Invalid reference channel ({n}). Choose from {valid_channels}.")
            return None

    def set_reference_channel_vertical_scale(self, n, scale):
        """
        Set the vertical scale of the specified reference channel.

        Parameters:
        n (int): The reference channel number, from 1 to 10.
        scale (float): The vertical scale. Range related to probe ratio (e.g., 1mV to 10V for 1X).
        """
        valid_channels = list(range(1, 11))
        if n in valid_channels and isinstance(scale, (float, int)) and scale > 0:
            self.instrument.write(f":REFerence{n}:VSCale {float(scale)}")
        else:
            print(f"Invalid reference channel ({n}) or scale ({scale}). Scale must be a positive number.")

    def get_reference_channel_vertical_scale(self, n):
        """
        Query the vertical scale of the specified reference channel.

        Parameters:
        n (int): The reference channel number, from 1 to 10.

        Returns:
        float: The vertical scale in scientific notation.
        """
        valid_channels = list(range(1, 11))
        if n in valid_channels:
            response = self.instrument.query(f":REFerence{n}:VSCale?")
            return float(response.strip())
        else:
            print(f"Invalid reference channel ({n}). Choose from {valid_channels}.")
            return None

    def set_reference_channel_vertical_offset(self, n, offset):
        """
        Set the vertical offset of the specified reference channel.

        Parameters:
        n (int): The reference channel number, from 1 to 10.
        offset (float): The vertical offset. Range: (-10 * RefVerticalScale) to (10 * RefVerticalScale).
        """
        valid_channels = list(range(1, 11))
        if n in valid_channels and isinstance(offset, (float, int)):
            self.instrument.write(f":REFerence{n}:VOFFset {float(offset)}")
        else:
            print(f"Invalid reference channel ({n}) or offset ({offset}). Must be a number.")

    def get_reference_channel_vertical_offset(self, n):
        """
        Query the vertical offset of the specified reference channel.

        Parameters:
        n (int): The reference channel number, from 1 to 10.

        Returns:
        float: The vertical offset in scientific notation.
        """
        valid_channels = list(range(1, 11))
        if n in valid_channels:
            response = self.instrument.query(f":REFerence{n}:VOFFset?")
            return float(response.strip())
        else:
            print(f"Invalid reference channel ({n}). Choose from {valid_channels}.")
            return None

    def reset_reference_channel(self, n):
        """
        Reset the vertical scale and vertical offset of the specified reference channel to their default values.

        Parameters:
        n (int): The reference channel number, from 1 to 10.
        """
        valid_channels = list(range(1, 11))
        if n in valid_channels:
            self.instrument.write(f":REFerence{n}:RESet")
        else:
            print(f"Invalid reference channel ({n}). Choose from {valid_channels}.")

    def select_current_reference_channel(self, n):
        """
        Select the current reference channel.

        Parameters:
        n (int): The reference channel number, from 1 to 10.
        """
        valid_channels = list(range(1, 11))
        if n in valid_channels:
            self.instrument.write(f":REFerence{n}:CURRent")
        else:
            print(f"Invalid reference channel ({n}). Choose from {valid_channels}.")

    def save_reference_waveform(self, n):
        """
        Store the waveform of the current reference channel to the internal memory as reference waveform.

        Parameters:
        n (int): The reference channel number, from 1 to 10.
        """
        valid_channels = list(range(1, 11))
        if n in valid_channels:
            self.instrument.write(f":REFerence{n}:SAVe")
        else:
            print(f"Invalid reference channel ({n}). Choose from {valid_channels}.")

    def set_reference_channel_color(self, n, color):
        """
        Set the display color of the current reference channel.

        Parameters:
        n (int): The reference channel number, from 1 to 10.
        color (str): The color, one of {"GRAY", "GREEn", "LBLue", "MAGenta", "ORANge"}.
        """
        valid_channels = list(range(1, 11))
        valid_colors = {"GRAY", "GREEn", "LBLue", "MAGenta", "ORANge"}
        color = color.upper()
        if n in valid_channels and color in valid_colors:
            self.instrument.write(f":REFerence{n}:COLor {color}")
        else:
            print(f"Invalid reference channel ({n}) or color ({color}). Choose from {valid_colors}.")

    def get_reference_channel_color(self, n):
        """
        Query the display color of the current reference channel.

        Parameters:
        n (int): The reference channel number, from 1 to 10.

        Returns:
        str: The color, one of {"GRAY", "GREE", "LBL", "MAG", "ORAN"}.
        """
        valid_channels = list(range(1, 11))
        if n in valid_channels:
            response = self.instrument.query(f":REFerence{n}:COLor?")
            return response.strip().upper()
        else:
            print(f"Invalid reference channel ({n}). Choose from {valid_channels}.")
            return None

    # STORage Commands
    def set_storage_image_type(self, img_type):
        """
        Set the image type when storing images.

        Parameters:
        img_type (str): The image type, one of {"PNG", "BMP8", "BMP24", "JPEG", "TIFF"}.
        """
        valid_types = {"PNG", "BMP8", "BMP24", "JPEG", "TIFF"}
        img_type = img_type.upper()
        if img_type in valid_types:
            self.instrument.write(f":STORage:IMAGe:TYPE {img_type}")
        else:
            print(f"Invalid image type ({img_type}). Choose from {valid_types}.")

    def get_storage_image_type(self):
        """
        Query the image type when storing images.

        Returns:
        str: The image type, one of {"PNG", "BMP8", "BMP24", "JPEG", "TIFF"}.
        """
        response = self.instrument.query(":STORage:IMAGe:TYPE?")
        return response.strip().upper()

    def set_storage_image_invert(self, state):
        """
        Turn on or off the invert function when storing images.

        Parameters:
        state (bool): True to turn on (ON), False to turn off (OFF).
        """
        self.instrument.write(f":STORage:IMAGe:INVERT {'ON' if state else 'OFF'}")

    def get_storage_image_invert(self):
        """
        Query the status of the invert function when storing images.

        Returns:
        str: "ON" or "OFF".
        """
        response = self.instrument.query(":STORage:IMAGe:INVERT?")
        return response.strip().upper()

    def set_storage_image_color_mode(self, state):
        """
        Set the image color when storing images to color (ON) or intensity graded color (OFF).

        Parameters:
        state (bool): True for color (ON), False for intensity graded color (OFF).
        """
        self.instrument.write(f":STORage:IMAGe:COLor {'ON' if state else 'OFF'}")

    def get_storage_image_color_mode(self):
        """
        Query the image color when storing images.

        Returns:
        str: "ON" or "OFF".
        """
        response = self.instrument.query(":STORage:IMAGe:COLor?")
        return response.strip().upper()

    # SYSTem Commands
    def enable_system_autoscale_key(self, state):
        """
        Enable or disable the AUTO key on the front panel.

        Parameters:
        state (bool): True to enable (ON), False to disable (OFF).
        """
        self.instrument.write(f":SYSTem:AUToscale {'ON' if state else 'OFF'}")

    def is_system_autoscale_key_enabled(self):
        """
        Query the status of the AUTO key.

        Returns:
        bool: True if AUTO key is ON, False if OFF.
        """
        response = self.instrument.query(":SYSTem:AUToscale?")
        return bool(int(response.strip()))

    
    def query_system_horizontal_grids(self):
        """
        Query the number of grids in the horizontal direction of the instrument screen.

        Returns:
        int: The number of horizontal grids (always 12).
        """
        response = self.instrument.query(":SYSTem:GAM?")
        return int(response.strip())

  

    def enable_system_keyboard_lock(self, state):
        """
        Enable or disable the keyboard lock function.

        Parameters:
        state (bool): True to enable (ON), False to disable (OFF).
        """
        self.instrument.write(f":SYSTem:LOCKed {'ON' if state else 'OFF'}")

    def is_system_keyboard_lock_enabled(self):
        """
        Query the status of the keyboard lock function.

        Returns:
        bool: True if keyboard lock is ON, False if OFF.
        """
        response = self.instrument.query(":SYSTem:LOCKed?")
        return bool(int(response.strip()))

    def set_system_power_on_recall(self, pon_mode):
        """
        Set the system configuration to be recalled when the oscilloscope is powered on again after power-off.

        Parameters:
        pon_mode (str): The power-on recall mode, one of {"LATest", "DEFault"}.
        """
        valid_modes = {"LATest", "DEFault"}
        pon_mode = pon_mode.upper()
        if pon_mode in valid_modes:
            self.instrument.write(f":SYSTem:PON {pon_mode}")
        else:
            print(f"Invalid power-on recall mode ({pon_mode}). Choose from {valid_modes}.")

    def get_system_power_on_recall(self):
        """
        Query the system configuration to be recalled when the oscilloscope is powered on again after power-off.

        Returns:
        str: The power-on recall mode, one of {"LAT", "DEF"}.
        """
        response = self.instrument.query(":SYSTem:PON?")
        return response.strip().upper()

    def install_system_option(self, license_key):
        """
        Install an option using the provided license key.
        The license key should be a 28-byte string (uppercase English characters and numbers),
        with hyphens omitted.

        Parameters:
        license_key (str): The option license key.
        """
        if isinstance(license_key, str) and len(license_key) == 28 and license_key.isalnum() and license_key.isupper():
            self.instrument.write(f":SYSTem:OPTion:INSTall {license_key}")
        else:
            print(f"Invalid license key format ({license_key}). Must be a 28-character uppercase alphanumeric string.")

    def uninstall_system_options(self):
        """
        Uninstall the options installed (:SYSTem:OPTion:UNINSTall).
        """
        self.instrument.write(":SYSTem:OPTion:UNINSTall")

    def query_system_analog_channels(self):
        """
        Query the number of analog channels of the instrument.

        Returns:
        int: The number of analog channels (always 2 for DS1000Z-E).
        """
        response = self.instrument.query(":SYSTem:RAM?")
        return int(response.strip())

    def set_system_parameters(self, setup_stream, use_file = False):
        """
        Import the setting parameters of the oscilloscope to restore the oscilloscope to the specified setting.
        The `setup_stream` must be a value previously acquired from `get_system_setup()`. Or the path to a file contianing the set up.

        Parameters:
        use_file: True if reading setup bytes from file
        setup_stream (bytes): The binary setup data stream, including the TMC header.
        """
        if isinstance(setup_stream, bytes):
            # For binary data, write_raw might be more appropriate depending on PyVISA implementation
            # However, SCPI commands usually expect string arguments.
            # If the instrument expects the raw bytes including TMC header, this might need adjustment
            # to use instrument.write_raw() or similar, or ensure the string conversion is handled correctly.
            # For now, assuming it expects a string representation of the bytes.
            # This is a complex command, and direct string conversion might not work for binary data.
            # A more robust solution might involve sending raw bytes.
            try:
                if use_file:
                    self.data_handler.read_file(setup_stream, EFileType.BIN)
                self.instrument.write(":SYSTem:SETup "+str(setup_stream))
            except Exception as e:
                print(f"Error setting system setup: {e}")
                print("This command often requires specific binary write methods depending on PyVISA.")
        else:
            print("Invalid setup_stream. Must be bytes object obtained from get_system_setup().")

    def get_system_parameters(self, filename = "oscilloscope_setup", save_to_file = False):
        """
        Query the setting of the oscilloscope.
        params: filename: The name of the file to save the setup data.
        save_to_file: If True, the setup data will be saved to a file even if auto save is not on.
        Returns:
        bytes: The setting data stream, including the TMC data description header.
               The user needs to handle parsing this data (remove TMC header).
        """
        try:
            # It's crucial to set a proper timeout for large binary transfers
            self.instrument.timeout = 5000 # Example: 5 seconds timeout
            self.instrument.write(":SYSTem:SETup?")
            data = self.instrument.read_raw()
            # self.instrument.timeout = 2000 # Reset to default if needed
            #TODO: CHeck if remove header
            #print("Data "+str(data))
            #data = self.data_handler.remove_tmc_header(data)
            #print(data)    
            if self.auto_save or save_to_file:
                self.data_handler.write_to_file(self.default_save_path+"/"+filename, data, EFileType.TXT)
            return data
        except pyvisa.errors.VisaIOError as e:
            print(f"VISA IO Error while getting system setup data: {e}")
            print("Consider increasing the instrument's timeout.")
            return b""
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return b""

    # TIMebase Commands
    def enable_timebase_delaye(self, state):
        """
        Enable or disable the delayed sweep.

        Parameters:
        state (bool): True to enable (ON), False to disable (OFF).
        """
        self.instrument.write(f":TIMebase:DELay:ENABle {'ON' if state else 'OFF'}")

    def is_timebase_delay_enabled(self):
        """
        Query the status of the delayed sweep.

        Returns:
        bool: True if delayed sweep is ON, False if OFF.
        """
        response = self.instrument.query(":TIMebase:DELay:ENABle?")
        return bool(int(response.strip()))

    def set_timebase_delay_offset(self, offset):
        """
        Set the delayed timebase offset. Default unit is s.

        Parameters:
        offset (float): The offset in seconds. Range depends on main timebase settings.
        """
        if isinstance(offset, (float, int)):
            self.instrument.write(f":TIMebase:DELay:OFFSet {float(offset)}")
        else:
            print(f"Invalid offset value ({offset}). Must be a number.")

    def get_timebase_delay_offset(self):
        """
        Query the delayed timebase offset.

        Returns:
        float: The delayed timebase offset in scientific notation (seconds).
        """
        response = self.instrument.query(":TIMebase:DELay:OFFSet?")
        return float(response.strip())

    def set_timebase_delay_scale(self, scale):
        """
        Set the delayed timebase scale. Default unit is s/div.

        Parameters:
        scale (float): The scale in s/div. Range depends on main timebase and sample rate.
        """
        if isinstance(scale, (float, int)) and scale > 0:
            self.instrument.write(f":TIMebase:DELay:SCALe {float(scale)}")
        else:
            print(f"Invalid scale value ({scale}). Must be a positive number.")

    def get_timebase_delay_scale(self):
        """
        Query the delayed timebase scale.

        Returns:
        float: The delayed timebase scale in scientific notation (s/div).
        """
        response = self.instrument.query(":TIMebase:DELay:SCALe?")
        return float(response.strip())

    def set_timebase_main_offset(self, offset):
        """
        Set the main timebase offset. Default unit is s.

        Parameters:
        offset (float): The offset in seconds. Range depends on timebase mode and run state.
        """
        if isinstance(offset, (float, int)):
            self.instrument.write(f":TIMebase:MAIN:OFFSet {float(offset)}")
        else:
            print(f"Invalid offset value ({offset}). Must be a number.")

    def get_timebase_main_offset(self):
        """
        Query the main timebase offset.

        Returns:
        float: The main timebase offset in scientific notation (seconds).
        """
        response = self.instrument.query(":TIMebase:MAIN:OFFSet?")
        return float(response.strip())

    def set_timebase_main_scale(self, scale):
        """
        Set the main timebase scale. Default unit is s/div.

        Parameters:
        scale (float): The scale in s/div. YT mode: 2ns/div to 50s/div. Roll mode: 100ms/div to 50s/div.
        """
        if isinstance(scale, (float, int)) and scale > 0:
            self.instrument.write(f":TIMebase:MAIN:SCALe {float(scale)}")
        else:
            print(f"Invalid scale value ({scale}). Must be a positive number.")

    def get_timebase_main_scale(self):
        """
        Query the main timebase scale.

        Returns:
        float: The main timebase scale in scientific notation (s/div).
        """
        response = self.instrument.query(":TIMebase:MAIN:SCALe?")
        return float(response.strip())

    def set_timebase_mode(self, mode):
        """
        Set the mode of the horizontal timebase.

        Parameters:
        mode (str): The timebase mode, one of {"MAIN", "XY", "ROLL"}.
                    MAIN: YT mode. XY: XY mode. ROLL: Roll mode.
        """
        valid_modes = {"MAIN", "XY", "ROLL"}
        mode = mode.upper()
        if mode in valid_modes:
            self.instrument.write(f":TIMebase:MODE {mode}")
        else:
            print(f"Invalid mode ({mode}). Choose from {valid_modes}.")

    def get_timebase_mode(self):
        """
        Query the mode of the horizontal timebase.

        Returns:
        str: The timebase mode, one of {"MAIN", "XY", "ROLL"}.
        """
        response = self.instrument.query(":TIMebase:MODE?")
        return response.strip().upper()

    # TRIGger Commands
    def set_trigger_mode(self, mode):
        """
        Select the trigger type.

        Parameters:
        mode (str): The trigger type, one of {"EDGE", "PULSE", "RUNT", "WINDows", "NEDGE",
                                            "SLOPE", "VIDeo", "PATTern", "DELay", "TIMeout",
                                            "DURation", "SHOLD", "RS232", "IIC", "SPI"}.
        """
        valid_modes = {"EDGE", "PULSE", "RUNT", "WINDows", "NEDGE", "SLOPE",
                       "VIDeo", "PATTern", "DELay", "TIMeout", "DURation",
                       "SHOLD", "RS232", "IIC", "SPI"}
        mode = mode.upper()
        if mode in valid_modes:
            self.instrument.write(f":TRIGger:MODE {mode}")
        else:
            print(f"Invalid trigger mode ({mode}). Choose from {valid_modes}.")

    def get_trigger_mode(self):
        """
        Query the trigger type.

        Returns:
        str: The trigger type, one of {"EDGE", "PULS", "RUNT", "WIND", "NEDG", "SLOP",
                                       "VID", "PATT", "DEL", "TIM", "DUR", "SHOL",
                                       "RS232", "IIC", "SPI"}.
        """
        response = self.instrument.query(":TRIGger:MODE?")
        return response.strip().upper()


    def get_trigger_status(self):
        """
        Query the current trigger status.

        Returns:
        str: The status, one of {"TD", "WAIT", "RUN", "AUTO", "STOP"}.
        """
        response = self.instrument.query(":TRIGger:STATus?")
        return response.strip().upper()

    def set_trigger_sweep_mode(self, sweep_mode):
        """
        Set the trigger mode (sweep mode).

        Parameters:
        sweep_mode (str): The sweep mode, one of {"AUTO", "NORMal", "SINGle"}.
        """
        valid_modes = {"AUTO", "NORMal", "SINGle"}
        sweep_mode = sweep_mode.upper()
        if sweep_mode in valid_modes:
            self.instrument.write(f":TRIGger:SWEep {sweep_mode}")
        else:
            print(f"Invalid sweep mode ({sweep_mode}). Choose from {valid_modes}.")

    def get_trigger_sweep_mode(self):
        """
        Query the trigger mode (sweep mode).

        Returns:
        str: The sweep mode, one of {"AUTO", "NORM", "SING"}.
        """
        response = self.instrument.query(":TRIGger:SWEep?")
        return response.strip().upper()


    def enable_trigger_noise_reject(self, state):
        """
        Enable or disable noise rejection.

        Parameters:
        state (bool): True to enable (ON), False to disable (OFF).
        """
        self.instrument.write(f":TRIGger:NREJect {'ON' if state else 'OFF'}")

    def is_trigger_noise_reject_enabled(self):
        """
        Query the status of noise rejection.

        Returns:
        bool: True if noise rejection is ON, False if OFF.
        """
        response = self.instrument.query(":TRIGger:NREJect?")
        return bool(int(response.strip()))

    def get_trigger_position(self):
        """
        Query the position in the internal memory that corresponds to the waveform trigger position.

        Returns:
        int: The position (integer). -2 if not triggered, -1 if triggered outside internal memory, >0 for position.
        """
        response = self.instrument.query(":TRIGger:POSition?")
        return int(response.strip())

    # TRIGger:EDGE Commands
    def set_trigger_edge_source(self, source):
        """
        Set the trigger source in edge trigger.

        Parameters:
        source (str): The source, one of {"CHANnel1", "CHANnel2", "AC", "EXT"}.
        """
        valid_sources = {"CHANnel1", "CHANnel2", "AC", "EXT"}
        source = source.upper()
        if source in valid_sources:
            self.instrument.write(f":TRIGger:EDGE:SOURce {source}")
        else:
            print(f"Invalid edge trigger source ({source}). Choose from {valid_sources}.")

    def get_trigger_edge_source(self):
        """
        Query the trigger source in edge trigger.

        Returns:
        str: The source, one of {"CHAN1", "CHAN2", "AC", "EXT"}.
        """
        response = self.instrument.query(":TRIGger:EDGE:SOURce?")
        return response.strip().upper()

    def set_trigger_edge_slope(self, slope_type):
        """
        Set the edge type in edge trigger.

        Parameters:
        slope_type (str): The slope type, one of {"POSitive", "NEGative", "RFALl"}.
                          POSitive: rising edge. NEGative: falling edge. RFALl: rising/falling edge.
        """
        valid_types = {"POSitive", "NEGative", "RFALl"}
        slope_type = slope_type.upper()
        if slope_type in valid_types:
            self.instrument.write(f":TRIGger:EDGE:SLOPE {slope_type}")
        else:
            print(f"Invalid edge slope type ({slope_type}). Choose from {valid_types}.")

    def get_trigger_edge_slope(self):
        """
        Query the edge type in edge trigger.

        Returns:
        str: The slope type, one of {"POS", "NEG", "RFAL"}.
        """
        response = self.instrument.query(":TRIGger:EDGE:SLOPE?")
        return response.strip().upper()

    def set_trigger_edge_level(self, level):
        """
        Set the trigger level in edge trigger. The unit is the same as the current amplitude unit of the signal source.

        Parameters:
        level (float): The trigger level. Range: (-5 * VerticalScale - OFFSet) to (5 * VerticalScale - OFFSet).
        """
        if isinstance(level, (float, int)):
            self.instrument.write(f":TRIGger:EDGE:LEVel {float(level)}")
        else:
            print(f"Invalid edge trigger level ({level}). Must be a number.")

    def get_trigger_edge_level(self):
        """
        Query the trigger level in edge trigger.

        Returns:
        float: The trigger level in scientific notation.
        """
        response = self.instrument.query(":TRIGger:EDGE:LEVel?")
        return float(response.strip())

    # TRIGger:PULSE Commands
    def set_trigger_pulse_source(self, source):
        """
        Set the trigger source in pulse width trigger.

        Parameters:
        source (str): The source, one of {"CHANnel1", "CHANnel2"}.
        """
        valid_sources = {"CHANnel1", "CHANnel2"}
        source = source.upper()
        if source in valid_sources:
            self.instrument.write(f":TRIGger:PULSE:SOURce {source}")
        else:
            print(f"Invalid pulse trigger source ({source}). Choose from {valid_sources}.")

    def get_trigger_pulse_source(self):
        """
        Query the trigger source in pulse width trigger.

        Returns:
        str: The source, one of {"CHAN1", "CHAN2"}.
        """
        response = self.instrument.query(":TRIGger:PULSE:SOURce?")
        return response.strip().upper()

    def set_trigger_pulse_when(self, when_condition):
        """
        Set the trigger condition in pulse width trigger.

        Parameters:
        when_condition (str): The condition, one of {"PGReater", "PLESS", "NGReater",
                                                    "NLESS", "PGLess", "NGLess"}.
        """
        valid_conditions = {"PGReater", "PLESS", "NGReater", "NLESS", "PGLess", "NGLess"}
        when_condition = when_condition.upper()
        if when_condition in valid_conditions:
            self.instrument.write(f":TRIGger:PULSE:WHEN {when_condition}")
        else:
            print(f"Invalid pulse trigger condition ({when_condition}). Choose from {valid_conditions}.")

    def get_trigger_pulse_when(self):
        """
        Query the trigger condition in pulse width trigger.

        Returns:
        str: The condition, one of {"PGR", "PLES", "NGR", "NLES", "PGL", "NGL"}.
        """
        response = self.instrument.query(":TRIGger:PULSE:WHEN?")
        return response.strip().upper()

    def set_trigger_pulse_width(self, width):
        """
        Set the pulse width in pulse width trigger. Default unit is s.
        This command is available when the trigger condition is PGReater, PLESS, NGReater, and NLESS.

        Parameters:
        width (float): The pulse width in seconds, from 8ns to 10s.
        """
        if isinstance(width, (float, int)) and 8e-9 <= width <= 10.0:
            self.instrument.write(f":TRIGger:PULSE:WIDTH {float(width)}")
        else:
            print(f"Invalid pulse width ({width}). Must be a float between 8ns and 10s.")

    def get_trigger_pulse_width(self):
        """
        Query the pulse width in pulse width trigger.

        Returns:
        float: The pulse width in scientific notation (seconds).
        """
        response = self.instrument.query(":TRIGger:PULSE:WIDTH?")
        return float(response.strip())

    def set_trigger_pulse_upper_width(self, width):
        """
        Set the upper pulse width in pulse width trigger. Default unit is s.
        This command is available when the trigger condition is PGLess and NGLess.

        Parameters:
        width (float): The upper pulse width in seconds, from 16ns to 10s.
        """
        if isinstance(width, (float, int)) and 16e-9 <= width <= 10.0:
            self.instrument.write(f":TRIGger:PULSE:UWIDth {float(width)}")
        else:
            print(f"Invalid upper pulse width ({width}). Must be a float between 16ns and 10s.")

    def get_trigger_pulse_upper_width(self):
        """
        Query the upper pulse width in pulse width trigger.

        Returns:
        float: The upper pulse width in scientific notation (seconds).
        """
        response = self.instrument.query(":TRIGger:PULSE:UWIDth?")
        return float(response.strip())

    def set_trigger_pulse_lower_width(self, width):
        """
        Set the lower pulse width in pulse width trigger. Default unit is s.
        This command is available when the trigger condition is PGLess and NGLess.

        Parameters:
        width (float): The lower pulse width in seconds, from 8ns to 9.99s.
        """
        if isinstance(width, (float, int)) and 8e-9 <= width <= 9.99:
            self.instrument.write(f":TRIGger:PULSE:LWIDth {float(width)}")
        else:
            print(f"Invalid lower pulse width ({width}). Must be a float between 8ns and 9.99s.")

    def get_trigger_pulse_lower_width(self):
        """
        Query the lower pulse width in pulse width trigger.

        Returns:
        float: The lower pulse width in scientific notation (seconds).
        """
        response = self.instrument.query(":TRIGger:PULSE:LWIDth?")
        return float(response.strip())

    def set_trigger_pulse_level(self, level):
        """
        Set the trigger level in pulse width trigger. The unit is the same as the current amplitude unit.

        Parameters:
        level (float): The trigger level. Range: (-5 * VerticalScale - OFFSet) to (5 * VerticalScale - OFFSet).
        """
        if isinstance(level, (float, int)):
            self.instrument.write(f":TRIGger:PULSE:LEVel {float(level)}")
        else:
            print(f"Invalid pulse trigger level ({level}). Must be a number.")

    def get_trigger_pulse_level(self):
        """
        Query the trigger level in pulse width trigger.

        Returns:
        float: The trigger level in scientific notation.
        """
        response = self.instrument.query(":TRIGger:PULSE:LEVel?")
        return float(response.strip())

    # TRIGger:SLOPE Commands
    def set_trigger_slope_source(self, source):
        """
        Set the trigger source in slope trigger.

        Parameters:
        source (str): The source, one of {"CHANnel1", "CHANnel2"}.
        """
        valid_sources = {"CHANnel1", "CHANnel2"}
        source = source.upper()
        if source in valid_sources:
            self.instrument.write(f":TRIGger:SLOPE:SOURce {source}")
        else:
            print(f"Invalid slope trigger source ({source}). Choose from {valid_sources}.")

    def get_trigger_slope_source(self):
        """
        Query the trigger source in slope trigger.

        Returns:
        str: The source, one of {"CHAN1", "CHAN2"}.
        """
        response = self.instrument.query(":TRIGger:SLOPE:SOURce?")
        return response.strip().upper()

    def set_trigger_slope_when(self, when_condition):
        """
        Set the trigger condition in slope trigger.

        Parameters:
        when_condition (str): The condition, one of {"PGReater", "PLESS", "NGReater",
                                                    "NLESS", "PGLess", "NGLess"}.
        """
        valid_conditions = {"PGReater", "PLESS", "NGReater", "NLESS", "PGLess", "NGLess"}
        when_condition = when_condition.upper()
        if when_condition in valid_conditions:
            self.instrument.write(f":TRIGger:SLOPE:WHEN {when_condition}")
        else:
            print(f"Invalid slope trigger condition ({when_condition}). Choose from {valid_conditions}.")

    def get_trigger_slope_when(self):
        """
        Query the trigger condition in slope trigger.

        Returns:
        str: The condition, one of {"PGR", "PLES", "NGR", "NLES", "PGL", "NGL"}.
        """
        response = self.instrument.query(":TRIGger:SLOPE:WHEN?")
        return response.strip().upper()

    def set_trigger_slope_time(self, time_value):
        """
        Set the time value in slope trigger. Default unit is s.
        This command is available when the trigger condition is PGReater, PLESS, NGReater, and NLESS.

        Parameters:
        time_value (float): The time value in seconds, from 8ns to 10s.
        """
        if isinstance(time_value, (float, int)) and 8e-9 <= time_value <= 10.0:
            self.instrument.write(f":TRIGger:SLOPE:TIME {float(time_value)}")
        else:
            print(f"Invalid slope time value ({time_value}). Must be a float between 8ns and 10s.")

    def get_trigger_slope_time(self):
        """
        Query the time value in slope trigger.

        Returns:
        float: The time value in scientific notation (seconds).
        """
        response = self.instrument.query(":TRIGger:SLOPE:TIME?")
        return float(response.strip())

    def set_trigger_slope_upper_time(self, time_value):
        """
        Set the upper limit of the time in slope trigger. Default unit is s.
        This command is available when the trigger condition is PGLess and NGLess.

        Parameters:
        time_value (float): The upper limit of the time in seconds, from 16ns to 10s.
        """
        if isinstance(time_value, (float, int)) and 16e-9 <= time_value <= 10.0:
            self.instrument.write(f":TRIGger:SLOPE:TUPPer {float(time_value)}")
        else:
            print(f"Invalid slope upper time ({time_value}). Must be a float between 16ns and 10s.")

    def get_trigger_slope_upper_time(self):
        """
        Query the upper limit of the time in slope trigger.

        Returns:
        float: The upper limit of the time in scientific notation (seconds).
        """
        response = self.instrument.query(":TRIGger:SLOPE:TUPPer?")
        return float(response.strip())

    def set_trigger_slope_lower_time(self, time_value):
        """
        Set the lower limit of the time in slope trigger. Default unit is s.
        This command is available when the trigger condition is PGLess and NGLess.

        Parameters:
        time_value (float): The lower limit of the time in seconds, from 8ns to 9.99s.
        """
        if isinstance(time_value, (float, int)) and 8e-9 <= time_value <= 9.99:
            self.instrument.write(f":TRIGger:SLOPE:TLOWer {float(time_value)}")
        else:
            print(f"Invalid slope lower time ({time_value}). Must be a float between 8ns and 9.99s.")

    def get_trigger_slope_lower_time(self):
        """
        Query the lower limit of the time in slope trigger.

        Returns:
        float: The lower limit of the time in scientific notation (seconds).
        """
        response = self.instrument.query(":TRIGger:SLOPE:TLOWer?")
        return float(response.strip())

    def set_trigger_slope_window(self, window_type):
        """
        Set the vertical window type in slope trigger.

        Parameters:
        window_type (str): The window type, one of {"TA", "TB", "TAB"}.
                           TA: adjust upper limit. TB: adjust lower limit. TAB: adjust both.
        """
        valid_types = {"TA", "TB", "TAB"}
        window_type = window_type.upper()
        if window_type in valid_types:
            self.instrument.write(f":TRIGger:SLOPE:WINDow {window_type}")
        else:
            print(f"Invalid slope window type ({window_type}). Choose from {valid_types}.")

    def get_trigger_slope_window(self):
        """
        Query the vertical window type in slope trigger.

        Returns:
        str: The window type, one of {"TA", "TB", "TAB"}.
        """
        response = self.instrument.query(":TRIGger:SLOPE:WINDow?")
        return response.strip().upper()

    def set_trigger_slope_upper_level(self, level):
        """
        Set the upper limit of the trigger level in slope trigger. The unit is the same as the current amplitude unit.

        Parameters:
        level (float): The upper limit level. Range: (-5 * VerticalScale - OFFSet) to (5 * VerticalScale - OFFSet).
        """
        if isinstance(level, (float, int)):
            self.instrument.write(f":TRIGger:SLOPE:ALEVel {float(level)}")
        else:
            print(f"Invalid slope upper level ({level}). Must be a number.")

    def get_trigger_slope_upper_level(self):
        """
        Query the upper limit of the trigger level in slope trigger.

        Returns:
        float: The upper limit of the trigger level in scientific notation.
        """
        response = self.instrument.query(":TRIGger:SLOPE:ALEVel?")
        return float(response.strip())

    def set_trigger_slope_lower_level(self, level):
        """
        Set the lower limit of the trigger level in slope trigger. The unit is the same as the current amplitude unit.

        Parameters:
        level (float): The lower limit level. Range: (-5 * VerticalScale - OFFSet) to (5 * VerticalScale - OFFSet).
        """
        if isinstance(level, (float, int)):
            self.instrument.write(f":TRIGger:SLOPE:BLEVel {float(level)}")
        else:
            print(f"Invalid slope lower level ({level}). Must be a number.")

    def get_trigger_slope_lower_level(self):
        """
        Query the lower limit of the trigger level in slope trigger.

        Returns:
        float: The lower limit of the trigger level in scientific notation.
        """
        response = self.instrument.query(":TRIGger:SLOPE:BLEVel?")
        return float(response.strip())

    # TRIGger:VIDeo Commands
    def set_trigger_video_source(self, source):
        """
        Select the trigger source in video trigger.

        Parameters:
        source (str): The source, one of {"CHANnel1", "CHANnel2"}.
        """
        valid_sources = {"CHANnel1", "CHANnel2"}
        source = source.upper()
        if source in valid_sources:
            self.instrument.write(f":TRIGger:VIDeo:SOURce {source}")
        else:
            print(f"Invalid video trigger source ({source}). Choose from {valid_sources}.")

    def get_trigger_video_source(self):
        """
        Query the trigger source in video trigger.

        Returns:
        str: The source, one of {"CHAN1", "CHAN2"}.
        """
        response = self.instrument.query(":TRIGger:VIDeo:SOURce?")
        return response.strip().upper()

    def set_trigger_video_polarity(self, polarity):
        """
        Select the video polarity in video trigger.

        Parameters:
        polarity (str): The polarity, one of {"POSitive", "NEGative"}.
        """
        valid_polarities = {"POSitive", "NEGative"}
        polarity = polarity.upper()
        if polarity in valid_polarities:
            self.instrument.write(f":TRIGger:VIDeo:POLarity {polarity}")
        else:
            print(f"Invalid video polarity ({polarity}). Choose from {valid_polarities}.")

    def get_trigger_video_polarity(self):
        """
        Query the video polarity in video trigger.

        Returns:
        str: The polarity, one of {"POS", "NEG"}.
        """
        response = self.instrument.query(":TRIGger:VIDeo:POLarity?")
        return response.strip().upper()

    def set_trigger_video_sync_mode(self, mode):
        """
        Set the sync type in video trigger.

        Parameters:
        mode (str): The sync type, one of {"ODDField", "EVENfield", "LINE", "ALINes"}.
        """
        valid_modes = {"ODDField", "EVENfield", "LINE", "ALINes"}
        mode = mode.upper()
        if mode in valid_modes:
            self.instrument.write(f":TRIGger:VIDeo:MODE {mode}")
        else:
            print(f"Invalid video sync mode ({mode}). Choose from {valid_modes}.")

    def get_trigger_video_sync_mode(self):
        """
        Query the sync type in video trigger.

        Returns:
        str: The sync type, one of {"ODDF", "EVEN", "LINE", "ALIN"}.
        """
        response = self.instrument.query(":TRIGger:VIDeo:MODE?")
        return response.strip().upper()

    def set_trigger_video_standard(self, standard):
        """
        Set the video standard in video trigger.

        Parameters:
        standard (str): The video standard, one of {"PALSecam", "NTSC", "480P", "576P"}.
        """
        valid_standards = {"PALSecam", "NTSC", "480P", "576P"}
        standard = standard.upper()
        if standard in valid_standards:
            self.instrument.write(f":TRIGger:VIDeo:STANdard {standard}")
        else:
            print(f"Invalid video standard ({standard}). Choose from {valid_standards}.")

    def get_trigger_video_standard(self):
        """
        Query the video standard in video trigger.

        Returns:
        str: The video standard, one of {"PALS", "NTSC", "480P", "576P"}.
        """
        response = self.instrument.query(":TRIGger:VIDeo:STANdard?")
        return response.strip().upper()

    def set_trigger_video_level(self, level):
        """
        Set the trigger level in video trigger. The unit is the same as the current amplitude unit.

        Parameters:
        level (float): The trigger level. Range: (-5 * VerticalScale - OFFSet) to (5 * VerticalScale - OFFSet).
        """
        if isinstance(level, (float, int)):
            self.instrument.write(f":TRIGger:VIDeo:LEVel {float(level)}")
        else:
            print(f"Invalid video trigger level ({level}). Must be a number.")

    def get_trigger_video_level(self):
        """
        Query the trigger level in video trigger.

        Returns:
        float: The trigger level in scientific notation.
        """
        response = self.instrument.query(":TRIGger:VIDeo:LEVel?")
        return float(response.strip())

    # TRIGger:PATTern Commands
    def set_trigger_pattern(self, pa_ch1, pa_ch2=None):
        """
        Set the pattern of each channel in pattern trigger.

        Parameters:
        pa_ch1 (str): Pattern for CH1, one of {"H", "L", "X", "R", "F"}.
        pa_ch2 (str, optional): Pattern for CH2, one of {"H", "L", "X", "R", "F"}.
                                If omitted, CH2's pattern remains unchanged.
        """
        valid_patterns = {"H", "L", "X", "R", "F"}
        pa_ch1 = pa_ch1.upper()

        if pa_ch1 not in valid_patterns:
            print(f"Invalid pattern for CH1 ({pa_ch1}). Choose from {valid_patterns}.")
            return

        command = f":TRIGger:PATTern:PATTern {pa_ch1}"
        if pa_ch2 is not None:
            pa_ch2 = pa_ch2.upper()
            if pa_ch2 not in valid_patterns:
                print(f"Invalid pattern for CH2 ({pa_ch2}). Choose from {valid_patterns}.")
                return
            command += f",{pa_ch2}"
        self.instrument.write(command)

    def get_trigger_pattern(self):
        """
        Query the patterns of all the channels (2) in pattern trigger.

        Returns:
        list of str: The patterns, e.g., ["H", "X"].
        """
        response = self.instrument.query(":TRIGger:PATTern:PATTern?")
        return [p.strip().upper() for p in response.strip().split(',')]

    def set_trigger_pattern_level(self, channel, level):
        """
        Set the trigger level of the specified channel in pattern trigger.
        The unit is the same as the current amplitude unit.

        Parameters:
        channel (str): The channel, one of {"CHANnel1", "CHANnel2"}.
        level (float): The trigger level. Range: (-5 * VerticalScale - OFFSet) to (5 * VerticalScale - OFFSet).
        """
        valid_channels = {"CHANnel1", "CHANnel2"}
        channel = channel.upper()
        if channel not in valid_channels:
            print(f"Invalid channel ({channel}). Choose from {valid_channels}.")
            return
        if isinstance(level, (float, int)):
            self.instrument.write(f":TRIGger:PATTern:LEVel {channel},{float(level)}")
        else:
            print(f"Invalid pattern trigger level ({level}). Must be a number.")

    def get_trigger_pattern_level(self, channel):
        """
        Query the trigger level of the specified channel in pattern trigger.

        Parameters:
        channel (str): The channel, one of {"CHANnel1", "CHANnel2"}.

        Returns:
        float: The trigger level in scientific notation.
        """
        valid_channels = {"CHANnel1", "CHANnel2"}
        channel = channel.upper()
        if channel not in valid_channels:
            print(f"Invalid channel ({channel}). Choose from {valid_channels}.")
            return None
        response = self.instrument.query(f":TRIGger:PATTern:LEVel? {channel}")
        return float(response.strip())

    # TRIGger:DURATion Commands
    def set_trigger_duration_source(self, source):
        """
        Set the trigger source in duration trigger.

        Parameters:
        source (str): The source, one of {"CHANnel1", "CHANnel2"}.
        """
        valid_sources = {"CHANnel1", "CHANnel2"}
        source = source.upper()
        if source in valid_sources:
            self.instrument.write(f":TRIGger:DURATion:SOURce {source}")
        else:
            print(f"Invalid duration trigger source ({source}). Choose from {valid_sources}.")

    def get_trigger_duration_source(self):
        """
        Query the trigger source in duration trigger.

        Returns:
        str: The source, one of {"CHAN1", "CHAN2"}.
        """
        response = self.instrument.query(":TRIGger:DURATion:SOURce?")
        return response.strip().upper()

    def set_trigger_duration_type(self, type_ch1, type_ch2=None):
        """
        Set the pattern of each channel in duration trigger.

        Parameters:
        type_ch1 (str): Pattern for CH1, one of {"H", "L", "X"}.
        type_ch2 (str, optional): Pattern for CH2, one of {"H", "L", "X"}.
                                  If omitted, CH2's pattern remains unchanged.
        """
        valid_types = {"H", "L", "X"}
        type_ch1 = type_ch1.upper()

        if type_ch1 not in valid_types:
            print(f"Invalid type for CH1 ({type_ch1}). Choose from {valid_types}.")
            return

        command = f":TRIGger:DURATion:TYPe {type_ch1}"
        if type_ch2 is not None:
            type_ch2 = type_ch2.upper()
            if type_ch2 not in valid_types:
                print(f"Invalid type for CH2 ({type_ch2}). Choose from {valid_types}.")
                return
            command += f",{type_ch2}"
        self.instrument.write(command)

    def get_trigger_duration_type(self):
        """
        Query the patterns of all the channels (2) in duration trigger.

        Returns:
        list of str: The patterns, e.g., ["L", "X"].
        """
        response = self.instrument.query(":TRIGger:DURATion:TYPe?")
        return [t.strip().upper() for t in response.strip().split(',')]

    def set_trigger_duration_when(self, when_condition):
        """
        Set the trigger condition in duration trigger.

        Parameters:
        when_condition (str): The condition, one of {"GREater", "LESS", "GLESs"}.
        """
        valid_conditions = {"GREater", "LESS", "GLESs"}
        when_condition = when_condition.upper()
        if when_condition in valid_conditions:
            self.instrument.write(f":TRIGger:DURATion:WHEN {when_condition}")
        else:
            print(f"Invalid duration trigger condition ({when_condition}). Choose from {valid_conditions}.")

    def get_trigger_duration_when(self):
        """
        Query the trigger condition in duration trigger.

        Returns:
        str: The condition, one of {"GRE", "LESS", "GLES"}.
        """
        response = self.instrument.query(":TRIGger:DURATion:WHEN?")
        return response.strip().upper()

    def set_trigger_duration_upper_time(self, time_value):
        """
        Set the duration time upper limit in duration trigger. Default unit is s.
        This command is available when the trigger condition is LESS or GLESs.

        Parameters:
        time_value (float): The upper limit in seconds. Range depends on trigger condition.
        """
        if isinstance(time_value, (float, int)) and time_value >= 8e-9: # Minimum value is 8ns or 16ns
            self.instrument.write(f":TRIGger:DURATion:TUPPer {float(time_value)}")
        else:
            print(f"Invalid duration upper time ({time_value}). Must be a float >= 8ns.")

    def get_trigger_duration_upper_time(self):
        """
        Query the duration time upper limit in duration trigger.

        Returns:
        float: The duration time upper limit in scientific notation (seconds).
        """
        response = self.instrument.query(":TRIGger:DURATion:TUPPer?")
        return float(response.strip())

    def set_trigger_duration_lower_time(self, time_value):
        """
        Set the duration time lower limit in duration trigger. Default unit is s.
        This command is available when the trigger condition is GREater or GLESs.

        Parameters:
        time_value (float): The lower limit in seconds, from 8ns to 9.99s.
        """
        if isinstance(time_value, (float, int)) and 8e-9 <= time_value <= 9.99:
            self.instrument.write(f":TRIGger:DURATion:TLOWer {float(time_value)}")
        else:
            print(f"Invalid duration lower time ({time_value}). Must be a float between 8ns and 9.99s.")

    def get_trigger_duration_lower_time(self):
        """
        Query the duration time lower limit in duration trigger.

        Returns:
        float: The duration time lower limit in scientific notation (seconds).
        """
        response = self.instrument.query(":TRIGger:DURATion:TLOWer?")
        return float(response.strip())

    # TRIGger:TIMeout Commands
    def set_trigger_timeout_source(self, source):
        """
        Set the trigger source in timeout trigger.

        Parameters:
        source (str): The source, one of {"CHANnel1", "CHANnel2"}.
        """
        valid_sources = {"CHANnel1", "CHANnel2"}
        source = source.upper()
        if source in valid_sources:
            self.instrument.write(f":TRIGger:TIMeout:SOURce {source}")
        else:
            print(f"Invalid timeout trigger source ({source}). Choose from {valid_sources}.")

    def get_trigger_timeout_source(self):
        """
        Query the trigger source in timeout trigger.

        Returns:
        str: The source, one of {"CHAN1", "CHAN2"}.
        """
        response = self.instrument.query(":TRIGger:TIMeout:SOURce?")
        return response.strip().upper()

    def set_trigger_timeout_slope(self, slope_type):
        """
        Set the edge type in timeout trigger.

        Parameters:
        slope_type (str): The slope type, one of {"POSitive", "NEGative", "RFALl"}.
        """
        valid_types = {"POSitive", "NEGative", "RFALl"}
        slope_type = slope_type.upper()
        if slope_type in valid_types:
            self.instrument.write(f":TRIGger:TIMeout:SLOPe {slope_type}")
        else:
            print(f"Invalid timeout slope type ({slope_type}). Choose from {valid_types}.")

    def get_trigger_timeout_slope(self):
        """
        Query the edge type in timeout trigger.

        Returns:
        str: The slope type, one of {"POS", "NEG", "RFAL"}.
        """
        response = self.instrument.query(":TRIGger:TIMeout:SLOPe?")
        return response.strip().upper()

    def set_trigger_timeout_time(self, time_value):
        """
        Set the timeout time in timeout trigger. Default unit is s.

        Parameters:
        time_value (float): The timeout time in seconds, from 16ns to 10s.
        """
        if isinstance(time_value, (float, int)) and 16e-9 <= time_value <= 10.0:
            self.instrument.write(f":TRIGger:TIMeout:TIMe {float(time_value)}")
        else:
            print(f"Invalid timeout time ({time_value}). Must be a float between 16ns and 10s.")

    def get_trigger_timeout_time(self):
        """
        Query the timeout time in timeout trigger.

        Returns:
        float: The timeout time in scientific notation (seconds).
        """
        response = self.instrument.query(":TRIGger:TIMeout:TIMe?")
        return float(response.strip())

    # TRIGger:RUNT Commands
    def set_trigger_runt_source(self, source):
        """
        Set the trigger source in runt trigger.

        Parameters:
        source (str): The source, one of {"CHANnel1", "CHANnel2"}.
        """
        valid_sources = {"CHANnel1", "CHANnel2"}
        source = source.upper()
        if source in valid_sources:
            self.instrument.write(f":TRIGger:RUNT:SOURce {source}")
        else:
            print(f"Invalid runt trigger source ({source}). Choose from {valid_sources}.")

    def get_trigger_runt_source(self):
        """
        Query the trigger source in runt trigger.

        Returns:
        str: The source, one of {"CHAN1", "CHAN2"}.
        """
        response = self.instrument.query(":TRIGger:RUNT:SOURce?")
        return response.strip().upper()

    def set_trigger_runt_polarity(self, polarity):
        """
        Set the pulse polarity in runt trigger.

        Parameters:
        polarity (str): The polarity, one of {"POSitive", "NEGative"}.
        """
        valid_polarities = {"POSitive", "NEGative"}
        polarity = polarity.upper()
        if polarity in valid_polarities:
            self.instrument.write(f":TRIGger:RUNT:POLarity {polarity}")
        else:
            print(f"Invalid runt polarity ({polarity}). Choose from {valid_polarities}.")

    def get_trigger_runt_polarity(self):
        """
        Query the pulse polarity in runt trigger.

        Returns:
        str: The polarity, one of {"POS", "NEG"}.
        """
        response = self.instrument.query(":TRIGger:RUNT:POLarity?")
        return response.strip().upper()

    def set_trigger_runt_when(self, when_qualifier):
        """
        Set the qualifier in runt trigger.

        Parameters:
        when_qualifier (str): The qualifier, one of {"NONE", "GREater", "LESS", "GLESs"}.
        """
        valid_qualifiers = {"NONE", "GREater", "LESS", "GLESs"}
        when_qualifier = when_qualifier.upper()
        if when_qualifier in valid_qualifiers:
            self.instrument.write(f":TRIGger:RUNT:WHEN {when_qualifier}")
        else:
            print(f"Invalid runt qualifier ({when_qualifier}). Choose from {valid_qualifiers}.")

    def get_trigger_runt_when(self):
        """
        Query the qualifier in runt trigger.

        Returns:
        str: The qualifier, one of {"NONE", "GRE", "LESS", "GLES"}.
        """
        response = self.instrument.query(":TRIGger:RUNT:WHEN?")
        return response.strip().upper()

    def set_trigger_runt_upper_width(self, width):
        """
        Set the pulse width upper limit in runt trigger. Default unit is s.
        This command is available when the qualifier is LESS or GLESs.

        Parameters:
        width (float): The upper limit in seconds. Range depends on qualifier.
        """
        if isinstance(width, (float, int)) and width >= 8e-9: # Min 8ns or 16ns
            self.instrument.write(f":TRIGger:RUNT:WUPPer {float(width)}")
        else:
            print(f"Invalid runt upper width ({width}). Must be a float >= 8ns.")

    def get_trigger_runt_upper_width(self):
        """
        Query the pulse width upper limit in runt trigger.

        Returns:
        float: The pulse width upper limit in scientific notation (seconds).
        """
        response = self.instrument.query(":TRIGger:RUNT:WUPPer?")
        return float(response.strip())

    def set_trigger_runt_lower_width(self, width):
        """
        Set the pulse width lower limit in runt trigger. Default unit is s.
        This command is available when the qualifier is GREater or GLESs.

        Parameters:
        width (float): The lower limit in seconds. Range depends on qualifier.
        """
        if isinstance(width, (float, int)) and width >= 8e-9 and width <= 9.99: # Max 9.99s
            self.instrument.write(f":TRIGger:RUNT:WLOWer {float(width)}")
        else:
            print(f"Invalid runt lower width ({width}). Must be a float between 8ns and 9.99s.")

    def get_trigger_runt_lower_width(self):
        """
        Query the pulse width lower limit in runt trigger.

        Returns:
        float: The pulse width lower limit in scientific notation (seconds).
        """
        response = self.instrument.query(":TRIGger:RUNT:WLOWer?")
        return float(response.strip())

    def set_trigger_runt_upper_level(self, level):
        """
        Set the trigger level upper limit in runt trigger. The unit is the same as the current amplitude unit.

        Parameters:
        level (float): The upper limit level. Range: (-5 * VerticalScale - OFFSet) to (5 * VerticalScale - OFFSet).
        """
        if isinstance(level, (float, int)):
            self.instrument.write(f":TRIGger:RUNT:ALEVel {float(level)}")
        else:
            print(f"Invalid runt upper level ({level}). Must be a number.")

    def get_trigger_runt_upper_level(self):
        """
        Query the trigger level upper limit in runt trigger.

        Returns:
        float: The trigger level upper limit in scientific notation.
        """
        response = self.instrument.query(":TRIGger:RUNT:ALEVel?")
        return float(response.strip())

    def set_trigger_runt_lower_level(self, level):
        """
        Set the trigger level lower limit in runt trigger. The unit is the same as the current amplitude unit.

        Parameters:
        level (float): The lower limit level. Range: (-5 * VerticalScale - OFFSet) to (5 * VerticalScale - OFFSet).
        """
        if isinstance(level, (float, int)):
            self.instrument.write(f":TRIGger:RUNT:BLEVel {float(level)}")
        else:
            print(f"Invalid runt lower level ({level}). Must be a number.")

    def get_trigger_runt_lower_level(self):
        """
        Query the trigger level lower limit in runt trigger.

        Returns:
        float: The trigger level lower limit in scientific notation.
        """
        response = self.instrument.query(":TRIGger:RUNT:BLEVel?")
        return float(response.strip())

    # TRIGger:WINDows Commands
    def set_trigger_windows_source(self, source):
        """
        Set the trigger source in windows trigger.

        Parameters:
        source (str): The source, one of {"CHANnel1", "CHANnel2"}.
        """
        valid_sources = {"CHANnel1", "CHANnel2"}
        source = source.upper()
        if source in valid_sources:
            self.instrument.write(f":TRIGger:WINDows:SOURce {source}")
        else:
            print(f"Invalid windows trigger source ({source}). Choose from {valid_sources}.")

    def get_trigger_windows_source(self):
        """
        Query the trigger source in windows trigger.

        Returns:
        str: The source, one of {"CHAN1", "CHAN2"}.
        """
        response = self.instrument.query(":TRIGger:WINDows:SOURce?")
        return response.strip().upper()

    def set_trigger_windows_slope(self, window_type):
        """
        Set the windows type in windows trigger.

        Parameters:
        window_type (str): The window type, one of {"POSitive", "NEGative", "RFALl"}.
        """
        valid_types = {"POSitive", "NEGative", "RFALl"}
        window_type = window_type.upper()
        if window_type in valid_types:
            self.instrument.write(f":TRIGger:WINDows:SLOPe {window_type}")
        else:
            print(f"Invalid windows type ({window_type}). Choose from {valid_types}.")

    def get_trigger_windows_slope(self):
        """
        Query the windows type in windows trigger.

        Returns:
        str: The window type, one of {"POS", "NEG", "RFAL"}.
        """
        response = self.instrument.query(":TRIGger:WINDows:SLOPe?")
        return response.strip().upper()

    def set_trigger_windows_position(self, position_type):
        """
        Set the trigger position in windows trigger.

        Parameters:
        position_type (str): The position type, one of {"EXIT", "ENTER", "TIMe"}.
        """
        valid_types = {"EXIT", "ENTER", "TIMe"}
        position_type = position_type.upper()
        if position_type in valid_types:
            self.instrument.write(f":TRIGger:WINDows:POSition {position_type}")
        else:
            print(f"Invalid windows position type ({position_type}). Choose from {valid_types}.")

    def get_trigger_windows_position(self):
        """
        Query the trigger position in windows trigger.

        Returns:
        str: The position type, one of {"EXIT", "ENTER", "TIM"}.
        """
        response = self.instrument.query(":TRIGger:WINDows:POSition?")
        return response.strip().upper()

    def set_trigger_windows_time(self, time_value):
        """
        Set the hold time in windows trigger. Default unit is s.

        Parameters:
        time_value (float): The hold time in seconds, from 8ns to 10s.
        """
        if isinstance(time_value, (float, int)) and 8e-9 <= time_value <= 10.0:
            self.instrument.write(f":TRIGger:WINDows:TIMe {float(time_value)}")
        else:
            print(f"Invalid windows time ({time_value}). Must be a float between 8ns and 10s.")

    def get_trigger_windows_time(self):
        """
        Query the hold time in windows trigger.

        Returns:
        float: The hold time in scientific notation (seconds).
        """
        response = self.instrument.query(":TRIGger:WINDows:TIMe?")
        return float(response.strip())

    def set_trigger_windows_upper_level(self, level):
        """
        Set the trigger level upper limit in windows trigger. The unit is the same as the current amplitude unit.

        Parameters:
        level (float): The upper limit level. Range: (-5 * VerticalScale - OFFSet) to (5 * VerticalScale - OFFSet).
        """
        if isinstance(level, (float, int)):
            self.instrument.write(f":TRIGger:WINDows:ALEVel {float(level)}")
        else:
            print(f"Invalid windows upper level ({level}). Must be a number.")

    def get_trigger_windows_upper_level(self):
        """
        Query the trigger level upper limit in windows trigger.

        Returns:
        float: The trigger level upper limit in scientific notation.
        """
        response = self.instrument.query(":TRIGger:WINDows:ALEVel?")
        return float(response.strip())

    def set_trigger_windows_lower_level(self, level):
        """
        Set the trigger level lower limit in windows trigger. The unit is the same as the current amplitude unit.

        Parameters:
        level (float): The lower limit level. Range: (-5 * VerticalScale - OFFSet) to (5 * VerticalScale - OFFSet).
        """
        if isinstance(level, (float, int)):
            self.instrument.write(f":TRIGger:WINDows:BLEVel {float(level)}")
        else:
            print(f"Invalid windows lower level ({level}). Must be a number.")

    def get_trigger_windows_lower_level(self):
        """
        Query the trigger level lower limit in windows trigger.

        Returns:
        float: The trigger level lower limit in scientific notation.
        """
        response = self.instrument.query(":TRIGger:WINDows:BLEVel?")
        return float(response.strip())

    # TRIGger:DELay Commands
    def set_trigger_delay_source_a(self, source):
        """
        Set the trigger source A in delay trigger.

        Parameters:
        source (str): The source, one of {"CHANnel1", "CHANnel2"}.
        """
        valid_sources = {"CHANnel1", "CHANnel2"}
        source = source.upper()
        if source in valid_sources:
            self.instrument.write(f":TRIGger:DELay:SA {source}")
        else:
            print(f"Invalid delay trigger source A ({source}). Choose from {valid_sources}.")

    def get_trigger_delay_source_a(self):
        """
        Query the trigger source A in delay trigger.

        Returns:
        str: The source, one of {"CHAN1", "CHAN2"}.
        """
        response = self.instrument.query(":TRIGger:DELay:SA?")
        return response.strip().upper()

    def set_trigger_delay_slope_a(self, slope_type):
        """
        Set the edge type of edge A in delay trigger.

        Parameters:
        slope_type (str): The slope type, one of {"POSitive", "NEGative"}.
        """
        valid_types = {"POSitive", "NEGative"}
        slope_type = slope_type.upper()
        if slope_type in valid_types:
            self.instrument.write(f":TRIGger:DELay:SLOPA {slope_type}")
        else:
            print(f"Invalid delay slope A type ({slope_type}). Choose from {valid_types}.")

    def get_trigger_delay_slope_a(self):
        """
        Query the edge type of edge A in delay trigger.

        Returns:
        str: The slope type, one of {"POS", "NEG"}.
        """
        response = self.instrument.query(":TRIGger:DELay:SLOPA?")
        return response.strip().upper()

    def set_trigger_delay_source_b(self, source):
        """
        Set the trigger source B in delay trigger.

        Parameters:
        source (str): The source, one of {"CHANnel1", "CHANnel2"}.
        """
        valid_sources = {"CHANnel1", "CHANnel2"}
        source = source.upper()
        if source in valid_sources:
            self.instrument.write(f":TRIGger:DELay:SB {source}")
        else:
            print(f"Invalid delay trigger source B ({source}). Choose from {valid_sources}.")

    def get_trigger_delay_source_b(self):
        """
        Query the trigger source B in delay trigger.

        Returns:
        str: The source, one of {"CHAN1", "CHAN2"}.
        """
        response = self.instrument.query(":TRIGger:DELay:SB?")
        return response.strip().upper()

    def set_trigger_delay_slope_b(self, slope_type):
        """
        Set the edge type of edge B in delay trigger.

        Parameters:
        slope_type (str): The slope type, one of {"POSitive", "NEGative"}.
        """
        valid_types = {"POSitive", "NEGative"}
        slope_type = slope_type.upper()
        if slope_type in valid_types:
            self.instrument.write(f":TRIGger:DELay:SLOPB {slope_type}")
        else:
            print(f"Invalid delay slope B type ({slope_type}). Choose from {valid_types}.")

    def get_trigger_delay_slope_b(self):
        """
        Query the edge type of edge B in delay trigger.

        Returns:
        str: The slope type, one of {"POS", "NEG"}.
        """
        response = self.instrument.query(":TRIGger:DELay:SLOPB?")
        return response.strip().upper()

    def set_trigger_delay_type(self, delay_type):
        """
        Set the delay type in delay trigger.

        Parameters:
        delay_type (str): The delay type, one of {"GREater", "LESS", "GLESs", "GOUT"}.
        """
        valid_types = {"GREater", "LESS", "GLESs", "GOUT"}
        delay_type = delay_type.upper()
        if delay_type in valid_types:
            self.instrument.write(f":TRIGger:DELay:TYPe {delay_type}")
        else:
            print(f"Invalid delay type ({delay_type}). Choose from {valid_types}.")

    def get_trigger_delay_type(self):
        """
        Query the delay type in delay trigger.

        Returns:
        str: The delay type, one of {"GOUT", "GRE", "LESS", "GLES"}.
        """
        response = self.instrument.query(":TRIGger:DELay:TYPe?")
        return response.strip().upper()

    def set_trigger_delay_upper_time(self, time_value):
        """
        Set the upper limit of the delay time in delay trigger. Default unit is s.
        This command is available when the delay type is LESS, GOUT, or GLESs.

        Parameters:
        time_value (float): The upper limit in seconds, from 16ns to 10s.
        """
        if isinstance(time_value, (float, int)) and 16e-9 <= time_value <= 10.0:
            self.instrument.write(f":TRIGger:DELay:TUPPer {float(time_value)}")
        else:
            print(f"Invalid delay upper time ({time_value}). Must be a float between 16ns and 10s.")

    def get_trigger_delay_upper_time(self):
        """
        Query the upper limit of the delay time in delay trigger.

        Returns:
        float: The upper limit of the delay time in scientific notation (seconds).
        """
        response = self.instrument.query(":TRIGger:DELay:TUPPer?")
        return float(response.strip())

    def set_trigger_delay_lower_time(self, time_value):
        """
        Set the lower limit of the delay time in delay trigger. Default unit is s.
        This command is available when the delay type is GREater, GOUT, or GLESs.

        Parameters:
        time_value (float): The lower limit in seconds. Range depends on delay type.
        """
        if isinstance(time_value, (float, int)) and 8e-9 <= time_value <= 9.99: # Max 9.99s
            self.instrument.write(f":TRIGger:DELay:TLOWer {float(time_value)}")
        else:
            print(f"Invalid delay lower time ({time_value}). Must be a float between 8ns and 9.99s.")

    def get_trigger_delay_lower_time(self):
        """
        Query the lower limit of the delay time in delay trigger.

        Returns:
        float: The lower limit of the delay time in scientific notation (seconds).
        """
        response = self.instrument.query(":TRIGger:DELay:TLOWer?")
        return float(response.strip())

    # TRIGger:SHOLd Commands
    def set_trigger_setup_hold_data_source(self, source):
        """
        Set the data source in setup/hold trigger.

        Parameters:
        source (str): The source, one of {"CHANnel1", "CHANnel2"}.
        """
        valid_sources = {"CHANnel1", "CHANnel2"}
        source = source.upper()
        if source in valid_sources:
            self.instrument.write(f":TRIGger:SHOLd:DSrc {source}")
        else:
            print(f"Invalid setup/hold data source ({source}). Choose from {valid_sources}.")

    def get_trigger_setup_hold_data_source(self):
        """
        Query the data source in setup/hold trigger.

        Returns:
        str: The source, one of {"CHAN1", "CHAN2"}.
        """
        response = self.instrument.query(":TRIGger:SHOLd:DSrc?")
        return response.strip().upper()

    def set_trigger_setup_hold_clock_source(self, source):
        """
        Set the clock source in setup/hold trigger.

        Parameters:
        source (str): The source, one of {"CHANnel1", "CHANnel2"}.
        """
        valid_sources = {"CHANnel1", "CHANnel2"}
        source = source.upper()
        if source in valid_sources:
            self.instrument.write(f":TRIGger:SHOLd:CSrc {source}")
        else:
            print(f"Invalid setup/hold clock source ({source}). Choose from {valid_sources}.")

    def get_trigger_setup_hold_clock_source(self):
        """
        Query the clock source in setup/hold trigger.

        Returns:
        str: The source, one of {"CHAN1", "CHAN2"}.
        """
        response = self.instrument.query(":TRIGger:SHOLd:CSrc?")
        return response.strip().upper()

    def set_trigger_setup_hold_slope(self, slope_type):
        """
        Set the edge type in setup/hold trigger.

        Parameters:
        slope_type (str): The slope type, one of {"POSitive", "NEGative"}.
        """
        valid_types = {"POSitive", "NEGative"}
        slope_type = slope_type.upper()
        if slope_type in valid_types:
            self.instrument.write(f":TRIGger:SHOLd:SLOPe {slope_type}")
        else:
            print(f"Invalid setup/hold slope type ({slope_type}). Choose from {valid_types}.")

    def get_trigger_setup_hold_slope(self):
        """
        Query the edge type in setup/hold trigger.

        Returns:
        str: The slope type, one of {"POS", "NEG"}.
        """
        response = self.instrument.query(":TRIGger:SHOLd:SLOPe?")
        return response.strip().upper()

    def set_trigger_setup_hold_pattern(self, pattern_type):
        """
        Set the data type in setup/hold trigger.

        Parameters:
        pattern_type (str): The pattern type, one of {"H", "L"}.
        """
        valid_types = {"H", "L"}
        pattern_type = pattern_type.upper()
        if pattern_type in valid_types:
            self.instrument.write(f":TRIGger:SHOLd:PATTern {pattern_type}")
        else:
            print(f"Invalid setup/hold pattern type ({pattern_type}). Choose from {valid_types}.")

    def get_trigger_setup_hold_pattern(self):
        """
        Query the data type in setup/hold trigger.

        Returns:
        str: The pattern type, one of {"H", "L"}.
        """
        response = self.instrument.query(":TRIGger:SHOLd:PATTern?")
        return response.strip().upper()

    def set_trigger_setup_hold_type(self, setup_type):
        """
        Set the setup type in setup/hold trigger.

        Parameters:
        setup_type (str): The setup type, one of {"SETup", "HOLd", "SETHOLd"}.
        """
        valid_types = {"SETup", "HOLd", "SETHOLd"}
        setup_type = setup_type.upper()
        if setup_type in valid_types:
            self.instrument.write(f":TRIGger:SHOLd:TYPe {setup_type}")
        else:
            print(f"Invalid setup/hold type ({setup_type}). Choose from {valid_types}.")

    def get_trigger_setup_hold_type(self):
        """
        Query the setup type in setup/hold trigger.

        Returns:
        str: The setup type, one of {"SET", "HOL", "SETHOL"}.
        """
        response = self.instrument.query(":TRIGger:SHOLd:TYPe?")
        return response.strip().upper()

    def set_trigger_setup_hold_setup_time(self, time_value):
        """
        Set the setup time in setup/hold trigger. Default unit is s.
        This command is available when the setup type is SETup or SETHOLd.

        Parameters:
        time_value (float): The setup time in seconds, from 8ns to 1s.
        """
        if isinstance(time_value, (float, int)) and 8e-9 <= time_value <= 1.0:
            self.instrument.write(f":TRIGger:SHOLd:STIMe {float(time_value)}")
        else:
            print(f"Invalid setup time ({time_value}). Must be a float between 8ns and 1s.")

    def get_trigger_setup_hold_setup_time(self):
        """
        Query the setup time in setup/hold trigger.

        Returns:
        float: The setup time in scientific notation (seconds).
        """
        response = self.instrument.query(":TRIGger:SHOLd:STIMe?")
        return float(response.strip())

    def set_trigger_setup_hold_hold_time(self, time_value):
        """
        Set the hold time in setup/hold trigger. Default unit is s.
        This command is available when the setup type is HOLd or SETHOLd.

        Parameters:
        time_value (float): The hold time in seconds, from 8ns to 1s.
        """
        if isinstance(time_value, (float, int)) and 8e-9 <= time_value <= 1.0:
            self.instrument.write(f":TRIGger:SHOLd:HTIMe {float(time_value)}")
        else:
            print(f"Invalid hold time ({time_value}). Must be a float between 8ns and 1s.")

    def get_trigger_setup_hold_hold_time(self):
        """
        Query the hold time in setup/hold trigger.

        Returns:
        float: The hold time in scientific notation (seconds).
        """
        response = self.instrument.query(":TRIGger:SHOLd:HTIMe?")
        return float(response.strip())

    # TRIGger:NEDGe Commands
    def set_trigger_nth_edge_source(self, source):
        """
        Set the trigger source in Nth edge trigger.

        Parameters:
        source (str): The source, one of {"CHANnel1", "CHANnel2"}.
        """
        valid_sources = {"CHANnel1", "CHANnel2"}
        source = source.upper()
        if source in valid_sources:
            self.instrument.write(f":TRIGger:NEDGe:SOURce {source}")
        else:
            print(f"Invalid Nth edge trigger source ({source}). Choose from {valid_sources}.")

    def get_trigger_nth_edge_source(self):
        """
        Query the trigger source in Nth edge trigger.

        Returns:
        str: The source, one of {"CHAN1", "CHAN2"}.
        """
        response = self.instrument.query(":TRIGger:NEDGe:SOURce?")
        return response.strip().upper()

    def set_trigger_nth_edge_slope(self, slope_type):
        """
        Set the edge type in Nth edge trigger.

        Parameters:
        slope_type (str): The slope type, one of {"POSitive", "NEGative"}.
        """
        valid_types = {"POSitive", "NEGative"}
        slope_type = slope_type.upper()
        if slope_type in valid_types:
            self.instrument.write(f":TRIGger:NEDGe:SLOPe {slope_type}")
        else:
            print(f"Invalid Nth edge slope type ({slope_type}). Choose from {valid_types}.")

    def get_trigger_nth_edge_slope(self):
        """
        Query the edge type in Nth edge trigger.

        Returns:
        str: The slope type, one of {"POS", "NEG"}.
        """
        response = self.instrument.query(":TRIGger:NEDGe:SLOPe?")
        return response.strip().upper()

    def set_trigger_nth_edge_idle_time(self, time_value):
        """
        Set the idle time in Nth edge trigger. Default unit is s.

        Parameters:
        time_value (float): The idle time in seconds, from 16ns to 10s.
        """
        if isinstance(time_value, (float, int)) and 16e-9 <= time_value <= 10.0:
            self.instrument.write(f":TRIGger:NEDGe:IDLE {float(time_value)}")
        else:
            print(f"Invalid Nth edge idle time ({time_value}). Must be a float between 16ns and 10s.")

    def get_trigger_nth_edge_idle_time(self):
        """
        Query the idle time in Nth edge trigger.

        Returns:
        float: The idle time in scientific notation (seconds).
        """
        response = self.instrument.query(":TRIGger:NEDGe:IDLE?")
        return float(response.strip())

    def set_trigger_nth_edge_count(self, count):
        """
        Set the number of edges in Nth edge trigger.

        Parameters:
        count (int): The number of edges, from 1 to 65535.
        """
        if isinstance(count, int) and 1 <= count <= 65535:
            self.instrument.write(f":TRIGger:NEDGe:EDGE {count}")
        else:
            print(f"Invalid Nth edge count ({count}). Must be an integer between 1 and 65535.")

    def get_trigger_nth_edge_count(self):
        """
        Query the number of edges in Nth edge trigger.

        Returns:
        int: The number of edges.
        """
        response = self.instrument.query(":TRIGger:NEDGe:EDGE?")
        return int(response.strip())

    def set_trigger_nth_edge_level(self, level):
        """
        Set the trigger level in Nth edge trigger. The unit is the same as the current amplitude unit.

        Parameters:
        level (float): The trigger level. Range: (-5 * VerticalScale - OFFSet) to (5 * VerticalScale - OFFSet).
        """
        if isinstance(level, (float, int)):
            self.instrument.write(f":TRIGger:NEDGe:LEVel {float(level)}")
        else:
            print(f"Invalid Nth edge trigger level ({level}). Must be a number.")

    def get_trigger_nth_edge_level(self):
        """
        Query the trigger level in Nth edge trigger.

        Returns:
        float: The trigger level in scientific notation.
        """
        response = self.instrument.query(":TRIGger:NEDGe:LEVel?")
        return float(response.strip())

    # TRIGger:RS232 Commands
    def set_trigger_rs232_source(self, source):
        """
        Set the trigger source in RS232 trigger.

        Parameters:
        source (str): The source, one of {"CHANnel1", "CHANnel2"}.
        """
        valid_sources = {"CHANnel1", "CHANnel2"}
        source = source.upper()
        if source in valid_sources:
            self.instrument.write(f":TRIGger:RS232:SOURce {source}")
        else:
            print(f"Invalid RS232 trigger source ({source}). Choose from {valid_sources}.")

    def get_trigger_rs232_source(self):
        """
        Query the trigger source in RS232 trigger.

        Returns:
        str: The source, one of {"CHAN1", "CHAN2"}.
        """
        response = self.instrument.query(":TRIGger:RS232:SOURce?")
        return response.strip().upper()

    def set_trigger_rs232_when(self, when_condition):
        """
        Set the trigger condition in RS232 trigger.

        Parameters:
        when_condition (str): The condition, one of {"STARt", "ERRor", "PARity", "DATA"}.
        """
        valid_conditions = {"STARt", "ERRor", "PARity", "DATA"}
        when_condition = when_condition.upper()
        if when_condition in valid_conditions:
            self.instrument.write(f":TRIGger:RS232:WHEN {when_condition}")
        else:
            print(f"Invalid RS232 trigger condition ({when_condition}). Choose from {valid_conditions}.")

    def get_trigger_rs232_when(self):
        """
        Query the trigger condition in RS232 trigger.

        Returns:
        str: The condition, one of {"STAR", "ERR", "PAR", "DATA"}.
        """
        response = self.instrument.query(":TRIGger:RS232:WHEN?")
        return response.strip().upper()

    def set_trigger_rs232_parity(self, parity_type):
        """
        Set the parity type when the trigger condition is ERRor or PARity in RS232 trigger.

        Parameters:
        parity_type (str): The parity type, one of {"EVEN", "ODD", "NONE"}.
        """
        valid_types = {"EVEN", "ODD", "NONE"}
        parity_type = parity_type.upper()
        if parity_type in valid_types:
            self.instrument.write(f":TRIGger:RS232:PARity {parity_type}")
        else:
            print(f"Invalid RS232 parity type ({parity_type}). Choose from {valid_types}.")

    def get_trigger_rs232_parity(self):
        """
        Query the parity type in RS232 trigger.

        Returns:
        str: The parity type, one of {"EVEN", "ODD", "NONE"}.
        """
        response = self.instrument.query(":TRIGger:RS232:PARity?")
        return response.strip().upper()

    def set_trigger_rs232_stop_bit(self, bit):
        """
        Set the stop bit when the trigger condition is ERRor in RS232 trigger.

        Parameters:
        bit (int): The stop bit, one of {1, 2}.
        """
        valid_bits = {1, 2}
        if bit in valid_bits:
            self.instrument.write(f":TRIGger:RS232:STOP {bit}")
        else:
            print(f"Invalid RS232 stop bit ({bit}). Choose from {valid_bits}.")

    def get_trigger_rs232_stop_bit(self):
        """
        Query the stop bit in RS232 trigger.

        Returns:
        int: The stop bit, one of {1, 2}.
        """
        response = self.instrument.query(":TRIGger:RS232:STOP?")
        return int(response.strip())

    def set_trigger_rs232_data(self, data_value):
        """
        Set the data when the trigger condition is DATA in RS232 trigger.

        Parameters:
        data_value (int): The data value. Range depends on current data bits (e.g., 0 to 2^n - 1).
        """
        if isinstance(data_value, int) and data_value >= 0: # Max value depends on data bits, hard to validate here.
            self.instrument.write(f":TRIGger:RS232:DATA {data_value}")
        else:
            print(f"Invalid RS232 data value ({data_value}). Must be a non-negative integer.")

    def get_trigger_rs232_data(self):
        """
        Query the data in RS232 trigger.

        Returns:
        int: The data value.
        """
        response = self.instrument.query(":TRIGger:RS232:DATA?")
        return int(response.strip())

    def set_trigger_rs232_data_width(self, width):
        """
        Set the data bits when the trigger condition is DATA in RS232 trigger.

        Parameters:
        width (int): The data bits, one of {5, 6, 7, 8}.
        """
        valid_widths = {5, 6, 7, 8}
        if width in valid_widths:
            self.instrument.write(f":TRIGger:RS232:WIDTh {width}")
        else:
            print(f"Invalid RS232 data width ({width}). Choose from {valid_widths}.")

    def get_trigger_rs232_data_width(self):
        """
        Query the data bits when the trigger condition is DATA in RS232 trigger.

        Returns:
        int: The data bits, one of {5, 6, 7, 8}.
        """
        response = self.instrument.query(":TRIGger:RS232:WIDTh?")
        return int(response.strip())

    def set_trigger_rs232_baud_rate(self, baud_rate):
        """
        Set the baud rate in RS232 trigger. Default unit is bps.

        Parameters:
        baud_rate (int or str): The baud rate, one of {2400, 4800, 9600, 19200, 38400, 57600,
                                                   115200, 230400, 460800, 921600, 1000000} or "USER".
        """
        valid_rates = {2400, 4800, 9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600, 1000000}
        if isinstance(baud_rate, int) and baud_rate in valid_rates:
            self.instrument.write(f":TRIGger:RS232:BAUD {baud_rate}")
        elif isinstance(baud_rate, str) and baud_rate.upper() == "USER":
            self.instrument.write(":TRIGger:RS232:BAUD USER")
        else:
            print(f"Invalid RS232 baud rate ({baud_rate}). Choose from {valid_rates} or 'USER'.")

    def get_trigger_rs232_baud_rate(self):
        """
        Query the baud rate in RS232 trigger.

        Returns:
        int or str: The baud rate (integer) or "USER".
        """
        response = self.instrument.query(":TRIGger:RS232:BAUD?")
        try:
            return int(response.strip())
        except ValueError:
            return response.strip().upper()

    def set_trigger_rs232_user_baud_rate(self, user_baud):
        """
        Set the user-defined baud rate in RS232 trigger. Default unit is bps.

        Parameters:
        user_baud (int): The user-defined baud rate, from 110 to 20000000.
        """
        if isinstance(user_baud, int) and 110 <= user_baud <= 20000000:
            self.instrument.write(f":TRIGger:RS232:BUSer {user_baud}")
        else:
            print(f"Invalid RS232 user baud rate ({user_baud}). Must be an integer between 110 and 20000000.")

    def get_trigger_rs232_user_baud_rate(self):
        """
        Query the user-defined baud rate in RS232 trigger.

        Returns:
        int: The user-defined baud rate.
        """
        response = self.instrument.query(":TRIGger:RS232:BUSer?")
        return int(response.strip())

    def set_trigger_rs232_level(self, level):
        """
        Set the trigger level in RS232 trigger. The unit is the same as the current amplitude unit.

        Parameters:
        level (float): The trigger level. Range: (-5 * VerticalScale - OFFSet) to (5 * VerticalScale - OFFSet).
        """
        if isinstance(level, (float, int)):
            self.instrument.write(f":TRIGger:RS232:LEVel {float(level)}")
        else:
            print(f"Invalid RS232 trigger level ({level}). Must be a number.")

    def get_trigger_rs232_level(self):
        """
        Query the trigger level in RS232 trigger.

        Returns:
        float: The trigger level in scientific notation.
        """
        response = self.instrument.query(":TRIGger:RS232:LEVel?")
        return float(response.strip())

    # TRIGger:IIC Commands
    def set_trigger_i2c_scl_source(self, source):
        """
        Set the channel source of SCL in I2C trigger.

        Parameters:
        source (str): The source, one of {"CHANnel1", "CHANnel2"}.
        """
        valid_sources = {"CHANnel1", "CHANnel2"}
        source = source.upper()
        if source in valid_sources:
            self.instrument.write(f":TRIGger:IIC:SCL {source}")
        else:
            print(f"Invalid I2C SCL source ({source}). Choose from {valid_sources}.")

    def get_trigger_i2c_scl_source(self):
        """
        Query the channel source of SCL in I2C trigger.

        Returns:
        str: The source, one of {"CHAN1", "CHAN2"}.
        """
        response = self.instrument.query(":TRIGger:IIC:SCL?")
        return response.strip().upper()

    def set_trigger_i2c_sda_source(self, source):
        """
        Set the channel source of SDA in I2C trigger.

        Parameters:
        source (str): The source, one of {"CHANnel1", "CHANnel2"}.
        """
        valid_sources = {"CHANnel1", "CHANnel2"}
        source = source.upper()
        if source in valid_sources:
            self.instrument.write(f":TRIGger:IIC:SDA {source}")
        else:
            print(f"Invalid I2C SDA source ({source}). Choose from {valid_sources}.")

    def get_trigger_i2c_sda_source(self):
        """
        Query the channel source of SDA in I2C trigger.

        Returns:
        str: The source, one of {"CHAN1", "CHAN2"}.
        """
        response = self.instrument.query(":TRIGger:IIC:SDA?")
        return response.strip().upper()

    def set_trigger_i2c_when(self, trig_type):
        """
        Set the trigger condition in I2C trigger.

        Parameters:
        trig_type (str): The trigger type, one of {"STARt", "RESTart", "STOP",
                                                  "NACKnowledge", "ADDRess", "DATA", "ADATa"}.
        """
        valid_types = {"STARt", "RESTart", "STOP", "NACKnowledge", "ADDRess", "DATA", "ADATa"}
        trig_type = trig_type.upper()
        if trig_type in valid_types:
            self.instrument.write(f":TRIGger:IIC:WHEN {trig_type}")
        else:
            print(f"Invalid I2C trigger condition ({trig_type}). Choose from {valid_types}.")

    def get_trigger_i2c_when(self):
        """
        Query the trigger condition in I2C trigger.

        Returns:
        str: The trigger type, one of {"STAR", "STOP", "NACK", "REST", "ADDR", "DATA", "ADAT"}.
        """
        response = self.instrument.query(":TRIGger:IIC:WHEN?")
        return response.strip().upper()

    def set_trigger_i2c_address_width(self, bits):
        """
        Set the address bits when the trigger condition is ADDRess or ADATa in I2C trigger.

        Parameters:
        bits (int): The address bits, one of {7, 8, 10}.
        """
        valid_bits = {7, 8, 10}
        if bits in valid_bits:
            self.instrument.write(f":TRIGger:IIC:AWIDth {bits}")
        else:
            print(f"Invalid I2C address width ({bits}). Choose from {valid_bits}.")

    def get_trigger_i2c_address_width(self):
        """
        Query the address bits when the trigger condition is ADDRess or ADATa in I2C trigger.

        Returns:
        int: The address bits, one of {7, 8, 10}.
        """
        response = self.instrument.query(":TRIGger:IIC:AWIDth?")
        return int(response.strip())

    def set_trigger_i2c_address(self, address_value):
        """
        Set the address when the trigger condition is ADDRess or ADATa in I2C trigger.

        Parameters:
        address_value (int): The address value. Range depends on address bits (e.g., 0 to 127 for 7-bit).
        """
        if isinstance(address_value, int) and address_value >= 0: # Max value depends on address bits, hard to validate here.
            self.instrument.write(f":TRIGger:IIC:ADDRess {address_value}")
        else:
            print(f"Invalid I2C address value ({address_value}). Must be a non-negative integer.")

    def get_trigger_i2c_address(self):
        """
        Query the address when the trigger condition is ADDRess or ADATa in I2C trigger.

        Returns:
        int: The address value.
        """
        response = self.instrument.query(":TRIGger:IIC:ADDRess?")
        return int(response.strip())

    def set_trigger_i2c_direction(self, direction):
        """
        Set the data direction when the trigger condition is ADDRess or ADATa in I2C trigger.

        Parameters:
        direction (str): The direction, one of {"READ", "WRITe", "RWRite"}.
        """
        valid_directions = {"READ", "WRITe", "RWRite"}
        direction = direction.upper()
        if direction in valid_directions:
            self.instrument.write(f":TRIGger:IIC:DIRection {direction}")
        else:
            print(f"Invalid I2C direction ({direction}). Choose from {valid_directions}.")

    def get_trigger_i2c_direction(self):
        """
        Query the data direction when the trigger condition is ADDRess or ADATa in I2C trigger.

        Returns:
        str: The direction, one of {"READ", "WRIT", "RWR"}.
        """
        response = self.instrument.query(":TRIGger:IIC:DIRection?")
        return response.strip().upper()

    def set_trigger_i2c_data(self, data_value):
        """
        Set the data when the trigger condition is DATA or ADATa in I2C trigger.

        Parameters:
        data_value (int): The data value. Range depends on byte length (0 to 2^40 - 1).
        """
        if isinstance(data_value, int) and data_value >= 0: # Max value 2^40 - 1, hard to validate.
            self.instrument.write(f":TRIGger:IIC:DATA {data_value}")
        else:
            print(f"Invalid I2C data value ({data_value}). Must be a non-negative integer.")

    def get_trigger_i2c_data(self):
        """
        Query the data when the trigger condition is DATA or ADATa in I2C trigger.

        Returns:
        int: The data value.
        """
        response = self.instrument.query(":TRIGger:IIC:DATA?")
        return int(response.strip())

    def set_trigger_i2c_scl_level(self, level):
        """
        Set the trigger level of SCL in I2C trigger. The unit is the same as the current amplitude unit.

        Parameters:
        level (float): The trigger level. Range: (-5 * VerticalScale - OFFSet) to (5 * VerticalScale - OFFSet).
        """
        if isinstance(level, (float, int)):
            self.instrument.write(f":TRIGger:IIC:CLEVel {float(level)}")
        else:
            print(f"Invalid I2C SCL level ({level}). Must be a number.")

    def get_trigger_i2c_scl_level(self):
        """
        Query the trigger level of SCL in I2C trigger.

        Returns:
        float: The trigger level of SCL in scientific notation.
        """
        response = self.instrument.query(":TRIGger:IIC:CLEVel?")
        return float(response.strip())

    def set_trigger_i2c_sda_level(self, level):
        """
        Set the trigger level of SDA in I2C trigger. The unit is the same as the current amplitude unit.

        Parameters:
        level (float): The trigger level. Range: (-5 * VerticalScale - OFFSet) to (5 * VerticalScale - OFFSet).
        """
        if isinstance(level, (float, int)):
            self.instrument.write(f":TRIGger:IIC:DLEVel {float(level)}")
        else:
            print(f"Invalid I2C SDA level ({level}). Must be a number.")

    def get_trigger_i2c_sda_level(self):
        """
        Query the trigger level of SDA in I2C trigger.

        Returns:
        float: The trigger level of SDA in scientific notation.
        """
        response = self.instrument.query(":TRIGger:IIC:DLEVel?")
        return float(response.strip())

    # TRIGger:SPI Commands
    def set_trigger_spi_scl_source(self, source):
        """
        Set the channel source of SCL in SPI trigger.

        Parameters:
        source (str): The source, one of {"CHANnel1", "CHANnel2"}.
        """
        valid_sources = {"CHANnel1", "CHANnel2"}
        source = source.upper()
        if source in valid_sources:
            self.instrument.write(f":TRIGger:SPI:SCL {source}")
        else:
            print(f"Invalid SPI SCL source ({source}). Choose from {valid_sources}.")

    def get_trigger_spi_scl_source(self):
        """
        Query the channel source of SCL in SPI trigger.

        Returns:
        str: The source, one of {"CHAN1", "CHAN2"}.
        """
        response = self.instrument.query(":TRIGger:SPI:SCL?")
        return response.strip().upper()

    def set_trigger_spi_sda_source(self, source):
        """
        Set the channel source of SDA in SPI trigger.

        Parameters:
        source (str): The source, one of {"CHANnel1", "CHANnel2"}.
        """
        valid_sources = {"CHANnel1", "CHANnel2"}
        source = source.upper()
        if source in valid_sources:
            self.instrument.write(f":TRIGger:SPI:SDA {source}")
        else:
            print(f"Invalid SPI SDA source ({source}). Choose from {valid_sources}.")

    def get_trigger_spi_sda_source(self):
        """
        Query the channel source of SDA in SPI trigger.

        Returns:
        str: The source, one of {"CHAN1", "CHAN2"}.
        """
        response = self.instrument.query(":TRIGger:SPI:SDA?")
        return response.strip().upper()

    def set_trigger_spi_when(self, trig_type):
        """
        Set the trigger condition in SPI trigger.

        Parameters:
        trig_type (str): The trigger type, one of {"CS", "TIMeout"}.
        """
        valid_types = {"CS", "TIMeout"}
        trig_type = trig_type.upper()
        if trig_type in valid_types:
            self.instrument.write(f":TRIGger:SPI:WHEN {trig_type}")
        else:
            print(f"Invalid SPI trigger condition ({trig_type}). Choose from {valid_types}.")

    def get_trigger_spi_when(self):
        """
        Query the trigger condition in SPI trigger.

        Returns:
        str: The trigger type, one of {"CS", "TIM"}.
        """
        response = self.instrument.query(":TRIGger:SPI:WHEN?")
        return response.strip().upper()

    def set_trigger_spi_data_width(self, width):
        """
        Set the data bits of the SDA channel in SPI trigger.

        Parameters:
        width (int): The data bits, from 4 to 32.
        """
        if isinstance(width, int) and 4 <= width <= 32:
            self.instrument.write(f":TRIGger:SPI:WIDTh {width}")
        else:
            print(f"Invalid SPI data width ({width}). Must be an integer between 4 and 32.")

    def get_trigger_spi_data_width(self):
        """
        Query the data bits of the SDA channel in SPI trigger.

        Returns:
        int: The data bits.
        """
        response = self.instrument.query(":TRIGger:SPI:WIDTh?")
        return int(response.strip())

    def set_trigger_spi_data(self, data_value):
        """
        Set the data in SPI trigger.

        Parameters:
        data_value (int): The data value. Range depends on data bits (0 to 2^32 - 1).
        """
        if isinstance(data_value, int) and data_value >= 0: # Max value 2^32 - 1, hard to validate.
            self.instrument.write(f":TRIGger:SPI:DATA {data_value}")
        else:
            print(f"Invalid SPI data value ({data_value}). Must be a non-negative integer.")

    def get_trigger_spi_data(self):
        """
        Query the data in SPI trigger.

        Returns:
        int: The data value.
        """
        response = self.instrument.query(":TRIGger:SPI:DATA?")
        return int(response.strip())

    def set_trigger_spi_timeout(self, time_value):
        """
        Set the timeout value when the trigger condition is TIMeout in SPI trigger. Default unit is s.

        Parameters:
        time_value (float): The timeout value in seconds, from 100ns to 1s.
        """
        if isinstance(time_value, (float, int)) and 100e-9 <= time_value <= 1.0:
            self.instrument.write(f":TRIGger:SPI:TIMeout {float(time_value)}")
        else:
            print(f"Invalid SPI timeout value ({time_value}). Must be a float between 100ns and 1s.")

    def get_trigger_spi_timeout(self):
        """
        Query the timeout value when the trigger condition is TIMeout in SPI trigger.

        Returns:
        float: The timeout value in scientific notation (seconds).
        """
        response = self.instrument.query(":TRIGger:SPI:TIMeout?")
        return float(response.strip())

    def set_trigger_spi_clock_edge(self, slope_type):
        """
        Set the clock edge in SPI trigger.

        Parameters:
        slope_type (str): The clock edge, one of {"POSitive", "NEGative"}.
        """
        valid_types = {"POSitive", "NEGative"}
        slope_type = slope_type.upper()
        if slope_type in valid_types:
            self.instrument.write(f":TRIGger:SPI:SLOPe {slope_type}")
        else:
            print(f"Invalid SPI clock edge ({slope_type}). Choose from {valid_types}.")

    def get_trigger_spi_clock_edge(self):
        """
        Query the clock edge in SPI trigger.

        Returns:
        str: The clock edge, one of {"POS", "NEG"}.
        """
        response = self.instrument.query(":TRIGger:SPI:SLOPe?")
        return response.strip().upper()

    def set_trigger_spi_scl_level(self, level):
        """
        Set the trigger level of the SCL channel in SPI trigger. The unit is the same as the current amplitude unit.

        Parameters:
        level (float): The trigger level. Range: (-5 * VerticalScale - OFFSet) to (5 * VerticalScale - OFFSet).
        """
        if isinstance(level, (float, int)):
            self.instrument.write(f":TRIGger:SPI:CLEVel {float(level)}")
        else:
            print(f"Invalid SPI SCL level ({level}). Must be a number.")

    def get_trigger_spi_scl_level(self):
        """
        Query the trigger level of the SCL channel in SPI trigger.

        Returns:
        float: The trigger level of the SCL channel in scientific notation.
        """
        response = self.instrument.query(":TRIGger:SPI:CLEVel?")
        return float(response.strip())

    def set_trigger_spi_sda_level(self, level):
        """
        Set the trigger level of the SDA channel in SPI trigger. The unit is the same as the current amplitude unit.

        Parameters:
        level (float): The trigger level. Range: (-5 * VerticalScale - OFFSet) to (5 * VerticalScale - OFFSet).
        """
        if isinstance(level, (float, int)):
            self.instrument.write(f":TRIGger:SPI:DLEVel {float(level)}")
        else:
            print(f"Invalid SPI SDA level ({level}). Must be a number.")

    def get_trigger_spi_sda_level(self):
        """
        Query the trigger level of the SDA channel in SPI trigger.

        Returns:
        float: The trigger level of the SDA channel in scientific notation.
        """
        response = self.instrument.query(":TRIGger:SPI:DLEVel?")
        return float(response.strip())

    def set_trigger_spi_cs_level(self, level):
        """
        Set or query the trigger level of the CS channel in SPI trigger. The unit is the same as the current amplitude unit.

        Parameters:
        level (float): The trigger level. Range: (-5 * VerticalScale - OFFSet) to (5 * VerticalScale - OFFSet).
        """
        if isinstance(level, (float, int)):
            self.instrument.write(f":TRIGger:SPI:SLEVel {float(level)}")
        else:
            print(f"Invalid SPI CS level ({level}). Must be a number.")

    def get_trigger_spi_cs_level(self):
        """
        Query the trigger level of the CS channel in SPI trigger.

        Returns:
        float: The trigger level of the CS channel in scientific notation.
        """
        response = self.instrument.query(":TRIGger:SPI:SLEVel?")
        return float(response.strip())

    def set_trigger_spi_cs_mode(self, mode):
        """
        Set the CS mode when the trigger condition is CS in SPI trigger.

        Parameters:
        mode (str): The CS mode, one of {"HIGH", "LOW"}.
        """
        valid_modes = {"HIGH", "LOW"}
        mode = mode.upper()
        if mode in valid_modes:
            self.instrument.write(f":TRIGger:SPI:MODE {mode}")
        else:
            print(f"Invalid SPI CS mode ({mode}). Choose from {valid_modes}.")

    def get_trigger_spi_cs_mode(self):
        """
        Query the CS mode when the trigger condition is CS in SPI trigger.

        Returns:
        str: The CS mode, one of {"HIGH", "LOW"}.
        """
        response = self.instrument.query(":TRIGger:SPI:MODE?")
        return response.strip().upper()

    def set_trigger_spi_cs_source(self, source):
        """
        Set the data source of the CS signal in SPI trigger.

        Parameters:
        source (str): The source, one of {"CHANnel1", "CHANnel2"}.
        """
        valid_sources = {"CHANnel1", "CHANnel2"}
        source = source.upper()
        if source in valid_sources:
            self.instrument.write(f":TRIGger:SPI:CS {source}")
        else:
            print(f"Invalid SPI CS source ({source}). Choose from {valid_sources}.")

    def get_trigger_spi_cs_source(self):
        """
        Query the data source of the CS signal in SPI trigger.

        Returns:
        str: The source, one of {"CHAN1", "CHAN2"}.
        """
        response = self.instrument.query(":TRIGger:SPI:CS?")
        return response.strip().upper()

    # WAVeform Commands
    def set_waveform_source(self, source):
        """
        Set the channel of which the waveform data will be read.

        Parameters:
        source (str): The source, one of {"CHANnel1", "CHANnel2", "MATH"}.
        """
        valid_sources = {"CHANnel1", "CHANnel2", "MATH"}
        source = source.upper()
        if source in valid_sources:
            self.instrument.write(f":WAVeform:SOURce {source}")
        else:
            print(f"Invalid waveform source ({source}). Choose from {valid_sources}.")

    def get_waveform_source(self):
        """
        Query the channel of which the waveform data will be read.

        Returns:
        str: The source, one of {"CHAN1", "CHAN2", "MATH"}.
        """
        response = self.instrument.query(":WAVeform:SOURce?")
        return response.strip().upper()

    def set_waveform_mode(self, mode):
        """
        Set the reading mode used by :WAVeform:DATA?.

        Parameters:
        mode (str): The reading mode, one of {"NORMal", "MAXimum", "RAW"}.
                    NORMal: read displayed waveform data.
                    MAXimum: read displayed waveform data (run state) or internal memory data (stop state).
                    RAW: read internal memory waveform data.
        """
        valid_modes = {"NORMal", "MAXimum", "RAW"}
        mode = mode.upper()
        if mode in valid_modes:
            self.instrument.write(f":WAVeform:MODE {mode}")
        else:
            print(f"Invalid waveform mode ({mode}). Choose from {valid_modes}.")

    def get_waveform_mode(self):
        """
        Query the reading mode used by :WAVeform:DATA?.

        Returns:
        str: The reading mode, one of {"NORM", "MAX", "RAW"}.
        """
        response = self.instrument.query(":WAVeform:MODE?")
        return response.strip().upper()

    def set_waveform_format(self, fmt):
        """
        Set the return format of the waveform data.
        Parameters:
        fmt (str): The format, one of {"WORD", "BYTE", "ASCII"}.
                   WORD: 16 bits per point (lower 8 valid, higher 8 are 0).
                   BYTE: 8 bits per point.
                   ASCII: actual voltage value in scientific notation, separated by commas.
        """
        valid_formats = {"WORD", "BYTE", "ASCII"}
        fmt = fmt.upper()
        if fmt in valid_formats:
            self.instrument.write(f":WAVeform:FORMat {fmt}")
        else:
            print(f"Invalid waveform format ({fmt}). Choose from {valid_formats}.")

    def get_waveform_format(self):
        """
        Query the return format of the waveform data.

        Returns:
        str: The format, one of {"WORD", "BYTE", "ASC"}.
        """
        response = self.instrument.query(":WAVeform:FORMat?")
        return response.strip().upper()

    def get_waveform_data(self, filename="waveform_data"):
        """
        Read the waveform data. The format depends on the current waveform format setting.

        Returns:
        bytes or str: The waveform data.
                      If format is BYTE or WORD, returns bytes (including TMC header).
                      If format is ASCII, returns a comma-separated string of float values.
        """
        current_format = self.get_waveform_format()
        response = ""
        header = None
        if current_format in ["BYTE", "WORD"]:
            header = "TMC"
            try:
                # Use query_binary_values for BYTE and WORD formats
                response = self.instrument.query(":WAVeform:DATA?")
        
            except pyvisa.errors.VisaIOError as e:
                print(f"VISA IO Error while getting waveform data: {e}")
                print("Consider increasing the instrument's timeout.")
                return b""
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                return b""
        elif current_format == "ASC":
            response = self.instrument.query(":WAVeform:DATA?")
            
        else:
            print(f"Unsupported waveform format: {current_format}")
            return None
        #self.data_handler.write_to_file(self.default_save_path+"/waveform", response, EFileType.CSV, header)
        return response
    def get_waveform_x_increment(self):
        """
        Query the time difference between two neighboring points of the specified channel source in the X direction.

        Returns:
        float: The X increment in scientific notation (s or Hz, depending on source).
        """
        response = self.instrument.query(":WAVeform:XINCrement?")
        return float(response.strip())

    def get_waveform_x_origin(self):
        """
        Query the start time of the waveform data of the channel source currently selected in the X direction.

        Returns:
        float: The X origin in scientific notation (s or Hz, depending on source).
        """
        response = self.instrument.query(":WAVeform:XORigin?")
        return float(response.strip())

    def get_waveform_x_reference(self):
        """
        Query the reference time of the specified channel source in the X direction.

        Returns:
        int: The X reference (always 0, representing the first point on screen or in internal memory).
        """
        response = self.instrument.query(":WAVeform:XREFerence?")
        return int(response.strip())

    def get_waveform_y_increment(self):
        """
        Query the waveform increment of the specified channel source in the Y direction.
        The unit is the same as the current amplitude unit.

        Returns:
        float: The Y increment in scientific notation.
        """
        response = self.instrument.query(":WAVeform:YINCrement?")
        return float(response.strip())

    def get_waveform_y_origin(self):
        """
        Query the vertical offset relative to the vertical reference position of the specified channel source in the Y direction.

        Returns:
        int: The Y origin (integer).
        """
        response = self.instrument.query(":WAVeform:YORigin?")
        return int(response.strip())

    def get_waveform_y_reference(self):
        """
        Query the vertical reference position of the specified channel source in the Y direction.

        Returns:
        int: The Y reference (always 127, where screen bottom is 0 and top is 255).
        """
        response = self.instrument.query(":WAVeform:YREFerence?")
        return int(response.strip())

    def set_waveform_start_point(self, start_point):
        """
        Set the start point of waveform data reading.

        Parameters:
        start_point (int): The start point. Range depends on current mode (NORMal: 1-1200,
                           MAX: 1 to effective points, RAW: 1 to max memory depth).
        """
        if isinstance(start_point, int) and start_point >= 1:
            self.instrument.write(f":WAVeform:STARt {start_point}")
        else:
            print(f"Invalid waveform start point ({start_point}). Must be an integer >= 1.")

    def get_waveform_start_point(self):
        """
        Query the start point of waveform data reading.

        Returns:
        int: The start point.
        """
        response = self.instrument.query(":WAVeform:STARt?")
        return int(response.strip())

    def set_waveform_stop_point(self, stop_point):
        """
        Set the stop point of waveform data reading.

        Parameters:
        stop_point (int): The stop point. Range depends on current mode (NORMal: 1-1200,
                          MAX: 1 to effective points, RAW: 1 to max memory depth).
        """
        if isinstance(stop_point, int) and stop_point >= 1:
            self.instrument.write(f":WAVeform:STOP {stop_point}")
        else:
            print(f"Invalid waveform stop point ({stop_point}). Must be an integer >= 1.")

    def get_waveform_stop_point(self):
        """
        Query the stop point of waveform data reading.

        Returns:
        int: The stop point.
        """
        response = self.instrument.query(":WAVeform:STOP?")
        return int(response.strip())

    def get_waveform_preamble(self):
        """
        Query and return all the waveform parameters.

        Returns:
        dict: A dictionary containing the 10 waveform parameters:
              'format', 'type', 'points', 'count', 'xincrement', 'xorigin',
              'xreference', 'yincrement', 'yorigin', 'yreference'.
              Values are converted to appropriate types (int, float).
        """
        response = self.instrument.query(":WAVeform:PREamble?")
        params = response.strip().split(',')
        if len(params) == 10:
            # Convert string parameters to appropriate types
            try:
                # Format: 0 (BYTE), 1 (WORD), or 2 (ASC)
                fmt = int(params[0])
                # Type: 0 (NORMal), 1 (MAXimum), or 2 (RAW)
                data_type = int(params[1])
                points = int(params[2])
                count = int(params[3])
                xincrement = float(params[4])
                xorigin = float(params[5])
                xreference = int(params[6])
                yincrement = float(params[7])
                yorigin = int(params[8])
                yreference = int(params[9])

                return {
                    'format': fmt,
                    'type': data_type,
                    'points': points,
                    'count': count,
                    'xincrement': xincrement,
                    'xorigin': xorigin,
                    'xreference': xreference,
                    'yincrement': yincrement,
                    'yorigin': yorigin,
                    'yreference': yreference
                }
            except ValueError as e:
                print(f"Error parsing waveform preamble: {e}. Raw response: {response}")
                return None
        else:
            print(f"Unexpected number of parameters in waveform preamble. Expected 10, got {len(params)}. Raw response: {response}")
            return None