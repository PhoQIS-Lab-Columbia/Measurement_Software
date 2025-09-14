from Instruments.Instrument import Instrument
import pyvisa
from Instruments.EInstrument import EInstrument
from Instruments.EFileType import EFileType
import subprocess
import sys
import json
class VNA(Instrument):

    def __init__(self, instrument, app, program_path, save_files_path=None):
        super().__init__(instrument, EInstrument.VECTOR_NETWORK_ANALYZER, save_files_path)
        
        self.program_path = program_path
        self.app = app
        
        # Add instance variables for each direct subclass under VNA

        # Instances for each channel (1-based index)
        self.calculate_channel1 = Calculate(self.instrument, self.data_handler, channel=1)
        self.calculate_channel2 = Calculate(self.instrument, self.data_handler, channel=2)
        self.calculate_channel3 = Calculate(self.instrument, self.data_handler, channel=3)
        self.calculate_channel4 = Calculate(self.instrument, self.data_handler, channel=4)  
        self.calculate_channel5 = Calculate(self.instrument, self.data_handler, channel=5)
        self.calculate_channel6 = Calculate(self.instrument, self.data_handler, channel=6)
        self.calculate_channel7 = Calculate(self.instrument, self.data_handler, channel=7)
        self.calculate_channel8 = Calculate(self.instrument, self.data_handler, channel=8)
        self.calculate_channel9 = Calculate(self.instrument, self.data_handler, channel=9)
        self.calculate_channel10 = Calculate(self.instrument, self.data_handler, channel=10)
        self.calculate_channel11 = Calculate(self.instrument, self.data_handler, channel=11)
        self.calculate_channel12 = Calculate(self.instrument, self.data_handler, channel=12)  
        self.calculate_channel13 = Calculate(self.instrument, self.data_handler, channel=13)
        self.calculate_channel14 = Calculate(self.instrument, self.data_handler, channel=14)
        self.calculate_channel15 = Calculate(self.instrument, self.data_handler, channel=15)
        self.calculate_channel6 = Calculate(self.instrument, self.data_handler, channel=16)  

        self.display_channel1 = Display(self.instrument, self.data_handler)
        
        self.initate_channel1 = Initate(self.instrument, self.data_handler, channel=1)
        self.initate_channel2 = Initate(self.instrument, self.data_handler, channel=2)
        self.initate_channel3 = Initate(self.instrument, self.data_handler, channel=3)
        self.initate_channel4 = Initate(self.instrument, self.data_handler, channel=4)
        self.initate_channel5 = Initate(self.instrument, self.data_handler, channel=5)
        self.initate_channel6 = Initate(self.instrument, self.data_handler, channel=6)
        self.initate_channel7 = Initate(self.instrument, self.data_handler, channel=7)
        self.initate_channel8 = Initate(self.instrument, self.data_handler, channel=8)
        self.initate_channel9 = Initate(self.instrument, self.data_handler, channel=9)
        self.initate_channel10 = Initate(self.instrument, self.data_handler, channel=10)
        self.initate_channel11 = Initate(self.instrument, self.data_handler, channel=11)
        self.initate_channel12 = Initate(self.instrument, self.data_handler, channel=12)
        self.initate_channel13 = Initate(self.instrument, self.data_handler, channel=13)
        self.initate_channel14 = Initate(self.instrument, self.data_handler, channel=14)
        self.initate_channel15= Initate(self.instrument, self.data_handler, channel=15)
        self.initate_channel16 = Initate(self.instrument, self.data_handler, channel=16)

        self.mmemory = MMemory(self.instrument, self.data_handler)
        
        self.sense_channel1 = Sense(self.instrument, self.data_handler, channel=1)
        self.sense_channel2 = Sense(self.instrument, self.data_handler, channel=2)
        self.sense_channel3 = Sense(self.instrument, self.data_handler, channel=3)
        self.sense_channel4 = Sense(self.instrument, self.data_handler, channel=4)
        self.sense_channel5 = Sense(self.instrument, self.data_handler, channel=5)
        self.sense_channel6 = Sense(self.instrument, self.data_handler, channel=6)
        self.sense_channel7 = Sense(self.instrument, self.data_handler, channel=7)
        self.sense_channel8 = Sense(self.instrument, self.data_handler, channel=8)
        self.sense_channel9 = Sense(self.instrument, self.data_handler, channel=9)
        self.sense_channel10 = Sense(self.instrument, self.data_handler, channel=10)
        self.sense_channel11 = Sense(self.instrument, self.data_handler, channel=11)
        self.sense_channel12 = Sense(self.instrument, self.data_handler, channel=12)
        self.sense_channel13 = Sense(self.instrument, self.data_handler, channel=13)
        self.sense_channel14 = Sense(self.instrument, self.data_handler, channel=14)
        self.sense_channel15 = Sense(self.instrument, self.data_handler, channel=15)
        self.sense_channel16 = Sense(self.instrument, self.data_handler, channel=16)

        self.status = Status(self.instrument, self.data_handler)
        self.source = Source(self.instrument, self.data_handler)
        self.system = System(self.instrument, self.data_handler)
        
        self.trigger = Trigger(self.instrument, self.data_handler)
        # Single instance subclasses (not channel-dependent)
        self.format = Format(self.instrument, self.data_handler)
        self.hcopy = HCopy(self.instrument, self.data_handler)
        self.output = Output(self.instrument, self.data_handler)
        #TODO Check service channel values
        self.service = Service(self.instrument, self.data_handler, 1)
        
    
    def open_software(self):
        subprocess.Popen(['C:/VNA/S4VNA/S4VNA.exe'], shell = False)
    def disconnect(self):
        super().disconnect()
        self.app.terminate()
#TODO Switch channel and calc, sense etc around
#TODO fix descriptions
class Calculate:
    """
    Data processing (conversion, electrical delay, phase offset,
gating, fixture simulation, trace hold, smoothing, time domain),
trace analysis, limit tests, markers, trace memory, math, statistic,
trace data transfer.
    """
    def __init__(self, instrument, data_handler,channel):
        self.instrument = instrument
        self.data_handler = data_handler
        self.n  = channel
        self.marker = self.Marker(self.instrument, self.data_handler, channel)
        self.math = self.Math(self.instrument, self.data_handler, channel)
        self.mst = self.MST(self.instrument, self.data_handler, channel)
        self.rlim = self.RLIM(self.instrument, self.data_handler, channel)
        self.smo = self.SMO(self.instrument, self.data_handler, channel)
        self.tran = self.TRAN(self.instrument, self.data_handler, channel)
        self.electrical_delay = self.ElectricalDelay(self.instrument, self.data_handler,channel)
        self.filter = self.Filter(self.instrument, self.data_handler,channel)
        self.trace_analysis = self.Trace(self.instrument, self.data_handler,channel)
        self.limit = self.Limit(self.instrument, self.data_handler,channel)
    # CALC:CONV - S-parameter Conversion ON/OFF
    def enable_conversion(self, enable: bool):
        """
        Enable or disable the S-parameter conversion function.

        Parameter:
        enable (bool): True to enable, False to disable

        Return:
        None
        """
        self.instrument.write(f":CALC{self.n}:CONV {1 if enable else 0}")

    def is_conversion_enabled(self) -> bool:
        """
        Query if the S-parameter conversion function is enabled.

        Parameter:
        None

        Return:
        bool: True if enabled, False otherwise
        """
        return bool(int(self.instrument.query(f":CALC{self.n}:CONV?")))

    # CALC:CONV:FUNC - S-parameter conversion function type
    def set_conversion_type(self, conv_type: str):
        """
        Set the S-parameter conversion function type.

        Parameter:
        conv_type (str): Conversion type, one of ['ZREF', 'ZTR', 'YREF', 'YTR', 'INV', 'ZTSH', 'YTSH', 'CONJ']

        Return:
        None
        """
        allowed = ['ZREF', 'ZTR', 'YREF', 'YTR', 'INV', 'ZTSH', 'YTSH', 'CONJ']
        if conv_type not in allowed:
            raise ValueError(f"conv_type must be one of {allowed}")
        self.instrument.write(f":CALC{self.n}:CONV:FUNC {conv_type}")

    def get_conversion_type(self) -> str:
        """
        Get the S-parameter conversion function type.

        Parameter:
        None

        Return:
        str: Current conversion function type
        """
        return self.instrument.query(f":CALC{self.n}:CONV:FUNC?").strip()

    class ElectricalDelay:
        """Commands to modify electrical delay parameters."""
        def __init__(self, instrument, data_handler, channel):
            self.n = channel
            self.instrument = instrument
            self.data_handler = data_handler

        # CALC:CORR:EDEL:DIST - Equivalent distance in the electrical delay function
        def set_equivalent_distance(self, distance: float):
            """
            Set the value of the equivalent distance in the electrical delay function.

            Parameter:
                distance (float): Distance value

            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:CORR:EDEL:DIST {distance}")

        def get_equivalent_distance(self) -> float:
            """
            Get the value of the equivalent distance in the electrical delay function.

            Parameter:
                None

            Return:
                float: Distance value
            """
            return float(self.instrument.query(f":CALC{self.n}:CORR:EDEL:DIST?"))

        # CALC:CORR:EDEL:DIST:UNIT - Distance units in the electrical delay function
        def set_distance_unit(self, unit: str):
            """
            Set the distance units in the electrical delay function.

            Parameter:
                unit (str): Unit, one of ['MET', 'FEET', 'INCH']

            Return:
                None
            """
            allowed = ['MET', 'FEET', 'INCH']
            if unit not in allowed:
                raise ValueError(f"unit must be one of {allowed}")
            self.instrument.write(f":CALC{self.n}:CORR:EDEL:DIST:UNIT {unit}")

        def get_distance_unit(self) -> str:
            """
            Get the distance units in the electrical delay function.

            Parameter:
                None

            Return:
                str: Unit
            """
            return self.instrument.query(f":CALC{self.n}:CORR:EDEL:DIST:UNIT?").strip()

        # CALC:CORR:EDEL:MED - Type of media in the electrical delay function
        def set_media(self, media: str):
            """
            Set the type of media in the electrical delay function.

            Parameter:
                media (str): Media type, one of ['COAX', 'WAV']

            Return:
                None
            """
            allowed = ['COAX', 'WAV']
            if media not in allowed:
                raise ValueError(f"media must be one of {allowed}")
            self.instrument.write(f":CALC{self.n}:CORR:EDEL:MED {media}")

        def get_media(self) -> str:
            """
            Get the type of media in the electrical delay function.

            Parameter:
                None

            Return:
                str: Media type
            """
            return self.instrument.query(f":CALC{self.n}:CORR:EDEL:MED?").strip()

        # CALC:CORR:EDEL:RVEL - Velocity factor used to calculate between delay and distance
        def set_velocity_factor(self, factor: float):
            """
            Set the value of the velocity factor used to calculate between delay and distance.

            Parameter:
                factor (float): Velocity factor (0 to 1)

            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:CORR:EDEL:RVEL {factor}")

        def get_velocity_factor(self) -> float:
            """
            Get the value of the velocity factor used to calculate between delay and distance.

            Parameter:
                None

            Return:
                float: Velocity factor
            """
            return float(self.instrument.query(f":CALC{self.n}:CORR:EDEL:RVEL?"))

        # CALC:CORR:EDEL:TIME - Value of the electrical delay
        def set_electrical_delay(self, delay: float):
            """
            Set the value of the electrical delay.

            Parameter:
                delay (float): Delay in seconds

            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:CORR:EDEL:TIME {delay}")

        def get_electrical_delay(self) -> float:
            """
            Get the value of the electrical delay.

            Parameter:
                None

            Return:
                float: Delay in seconds
            """
            return float(self.instrument.query(f":CALC{self.n}:CORR:EDEL:TIME?"))

        # CALC:CORR:EDEL:WAV:CUT - Waveguide cutoff frequency in the electrical delay function
        def set_waveguide_cutoff(self, freq: float):
            """
            Set the value of the waveguide cutoff frequency in the electrical delay function.

            Parameter:
                freq (float): Frequency in Hz

            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:CORR:EDEL:WAV:CUT {freq}")

        def get_waveguide_cutoff(self) -> float:
            """
            Get the value of the waveguide cutoff frequency in the electrical delay function.

            Parameter:
                None

            Return:
                float: Frequency in Hz
            """
            return float(self.instrument.query(f":CALC{self.n}:CORR:EDEL:WAV:CUT?"))

    class Filter:
        """Commands for modifying the gating function parameters."""
        def __init__(self, instrument, data_handler, channel):
            self.instrument = instrument
            self.data_handler = data_handler
            self.n = channel

        # CALC:FILT:TIME - Gate type of the gating function
        def set_gate_type(self, gate_type: str):
            """
            Set the gate type of the gating function.

            Parameter:
                gate_type (str): Gate type, one of ['BPAS', 'NOTC']

            Return:
                None
            """
            allowed = ['BPAS', 'NOTC']
            if gate_type not in allowed:
                raise ValueError(f"gate_type must be one of {allowed}")
            self.instrument.write(f":CALC{self.n}:FILT:TIME {gate_type}")

        def get_gate_type(self) -> str:
            """
            Get the gate type of the gating function.

            Parameter:
                None

            Return:
                str: Gate type
            """
            return self.instrument.query(f":CALC{self.n}:FILT:TIME?").strip()

        # CALC:FILT:TIME:CENT - Gate center value of the gating function
        def set_gate_center(self, center: float):
            """
            Set the gate center value of the gating function.

            Parameter:
                center (float): Center value

            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:FILT:TIME:CENT {center}")

        def get_gate_center(self) -> float:
            """
            Get the gate center value of the gating function.

            Parameter:
                None

            Return:
                float: Center value
            """
            return float(self.instrument.query(f":CALC{self.n}:FILT:TIME:CENT?"))

        # CALC:FILT:TIME:SHAP - Gate shape of the gating function
        def set_gate_shape(self, shape: str):
            """
            Set the gate shape of the gating function.

            Parameter:
                shape (str): Gate shape, one of ['MAX', 'WIDE', 'NORM', 'MIN']

            Return:
                None
            """
            allowed = ['MAX', 'WIDE', 'NORM', 'MIN']
            if shape not in allowed:
                raise ValueError(f"shape must be one of {allowed}")
            self.instrument.write(f":CALC{self.n}:FILT:TIME:SHAP {shape}")

        def get_gate_shape(self) -> str:
            """
            Get the gate shape of the gating function.

            Parameter:
                None

            Return:
                str: Gate shape
            """
            return self.instrument.query(f":CALC{self.n}:FILT:TIME:SHAP?").strip()

        # CALC:FILT:TIME:SPAN - Gate span value of the gating function
        def set_gate_span(self, span: float):
            """
            Set the gate span value of the gating function.

            Parameter:
                span (float): Span value

            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:FILT:TIME:SPAN {span}")

        def get_gate_span(self) -> float:
            """
            Get the gate span value of the gating function.

            Parameter:
                None

            Return:
                float: Span value
            """
            return float(self.instrument.query(f":CALC{self.n}:FILT:TIME:SPAN?"))

        # CALC:FILT:TIME:STAR - Gate start value of the gating function
        def set_gate_start(self, start: float):
            """
            Set the gate start value of the gating function.

            Parameter:
                start (float): Start value

            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:FILT:TIME:STAR {start}")

        def get_gate_start(self) -> float:
            """
            Get the gate start value of the gating function.

            Parameter:
                None

            Return:
                float: Start value
            """
            return float(self.instrument.query(f":CALC{self.n}:FILT:TIME:STAR?"))

        # CALC:FILT:TIME:STAT - Gating function ON/OFF
        def enable_gating(self, enable: bool):
            """
            Enable or disable the gating function.

            Parameter:
                enable (bool): True to enable, False to disable

            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:FILT:TIME:STAT {1 if enable else 0}")

        def is_gating_enabled(self) -> bool:
            """
            Query if the gating function is enabled.

            Parameter:
                None

            Return:
                bool: True if enabled, False otherwise
            """
            return bool(int(self.instrument.query(f":CALC{self.n}:FILT:TIME:STAT?")))

        # CALC:FILT:TIME:STOP - Gate stop value of the gating function
        def set_gate_stop(self, stop: float):
            """
            Set the gate stop value of the gating function.

            Parameter:
                stop (float): Stop value

            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:FILT:TIME:STOP {stop}")

        def get_gate_stop(self) -> float:
            """
            Get the gate stop value of the gating function.

            Parameter:
                None

            Return:
                float: Stop value
            """
            return float(self.instrument.query(f":CALC{self.n}:FILT:TIME:STOP?"))

    # CALC:CORR:OFFS:PHAS - Phase offset
    def set_phase_offset(self, offset: float):
        """
        Set the value of the phase offset.

        Parameter:
        offset (float): Phase offset value in degrees

        Return:
        None
        """
        self.instrument.write(f":CALC{self.n}:CORR:OFFS:PHAS {offset}")

    def get_phase_offset(self) -> float:
        """
        Get the value of the phase offset.

        Parameter:
        None

        Return:
        float: Phase offset in degrees
        """
        return float(self.instrument.query(f":CALC{self.n}:CORR:OFFS:PHAS?"))

    # CALC:CORR:STAT? - Interpolation/extrapolation status of the error correction
    def get_correction_status(self) -> str:
        """
        Read out the interpolation/extrapolation status of the error correction.

        Parameter:
        None

        Return:
        str: Status
        """
        return self.instrument.query(f":CALC{self.n}:CORR:STAT?").strip()

    # CALC:DATA:FDAT - Formatted data array
    def get_formatted_data(self):
        """
        Read out the formatted data array.

        Parameter:
        None

        Return:
        list: Formatted data array
        """
        data = self.instrument.query(f":CALC{self.n}:DATA:FDAT?")
        if self.data_handler.is_auto_saving_data_enabled():
                self.data_handler.write_to_file(self, f"FORMATTED_DATA", data, file_type = EFileType.CSV)
        return self.data_handler.parse_array(data)

    # CALC:DATA:FMEM - Formatted memory array
    def get_formatted_memory(self):
        """
        Read out the formatted memory array.

        Parameter:
        None

        Return:
        list: Formatted memory array
        """
        data = self.instrument.query(f":CALC{self.n}:DATA:FMEM?")
        if self.data_handler.is_auto_saving_data_enabled():
                self.data_handler.write_to_file(self, f"FORMAT_MEM", data, file_type = EFileType.CSV)
        return self.data_handler.parse_array(data)

    # CALC:DATA:SDAT - Corrected data array
    def get_corrected_data(self):
        """
        Read out the corrected data array.

        Parameter:
        None

        Return:
        list: Corrected data array
        """
        data = self.instrument.query(f":CALC{self.n}:DATA:SDAT?")
        if self.data_handler.is_auto_saving_data_enabled():
                self.data_handler.write_to_file(self, f"CORR_DATA", data, file_type = EFileType.CSV)
        return self.data_handler.parse_array(data)

    # CALC:DATA:SMEM - Corrected memory array
    def get_corrected_memory(self):
        """
        Read out the corrected memory array.

        Parameter:
        None

        Return:
        list: Corrected memory array
        """
        data = self.instrument.query(f":CALC{self.n}:DATA:SMEM?")
        if self.data_handler.is_auto_saving_data_enabled():
                self.data_handler.write_to_file(self, f"CORR_MEM", data, file_type = EFileType.CSV)
        return self.data_handler.parse_array(data)

    # CALC:DATA:XAX? - X-axis values array
    def get_x_axis(self):
        """
        Read out the X-axis values array.

        Parameter:
        None

        Return:
        list: X-axis values
        """
        data = self.instrument.query(f":CALC{self.n}:DATA:XAX?")
        if self.data_handler.is_auto_saving_data_enabled():
            self.data_handler.write_to_file(self, f"X_AXIS", data, file_type = EFileType.CSV)
        return self.data_handler.parse_array(data)

    # CALC:FORM - Trace format
    def set_trace_format(self, fmt: str):
        """
        Set the trace format.

        Parameter:
        fmt (str): Trace format, e.g., 'MLOG', 'PHAS', 'UPH', 'MLIN', etc.

        Return:
        None
        """
        allowed = ['MLOG', 'PHAS', 'UPH', 'MLIN', 'REAL', 'IMAG', 'POL', 'SMIT', 'SMIC', 'SWR', 'GDEL', 'K']
        if fmt not in allowed:
            raise ValueError(f"fmt must be one of {allowed}")
        self.instrument.write(f":CALC{self.n}:FORM {fmt}")

    def get_trace_format(self) -> str:
        """
        Get the trace format.

        Parameter:
        None

        Return:
        str: Trace format
        """
        return self.instrument.query(f":CALC{self.n}:FORM?").strip()

    # CALC:PAR:COUN - Number of traces in the channel
    def get_trace_count(self) -> int:
        """
        Get the number of traces in the channel.

        Parameter:
        None

        Return:
        int: Number of traces
        """
        return int(self.instrument.query(f":CALC{self.n}:PAR:COUN?"))

    # CALC:PAR:SEL - Active trace number (write)
    def set_active_trace(self, trace_num: int):
        """
        Set the active trace number.

        Parameter:
        trace_num (int): Trace number

        Return:
        None
        """
        self.instrument.write(f":CALC{self.n}:PAR:SEL {trace_num}")

    def get_active_trace(self) -> int:
        """
        Get the active trace number.

        Parameter:
        None

        Return:
        int: Active trace number
        """
        return int(self.instrument.query(f":CALC{self.n}:PAR:SEL?"))
    
    def is_port_z_conversion_enabled(self) -> bool:
        """
        Query if port Z conversion is enabled.

        Parameter:
            None

        Return:
            bool: True if enabled, False otherwise
        """
        return bool(int(self.instrument.query(f":CALC{self.n}:FSIM:SEND:ZCON:STAT?")))

    # CALC:FSIM:SEND:ZCON:THE - Theory of Port Z Conversion
    def get_port_z_conversion_theory(self) -> str:
        """
        Get the theory of port Z conversion.

        Parameter:
            None

        Return:
            str: Theory description
        """
        return self.instrument.query(f":CALC{self.n}:FSIM:SEND:ZCON:THE?").strip()

    # CALC:FSIM:STAT - Fixture simulation ON/OFF
    def enable_fixture_simulation(self, enable: bool):
        """
        Enable or disable fixture simulation function.

        Parameter:
            enable (bool): True to enable, False to disable

        Return:
            None
        """
        self.instrument.write(f":CALC{self.n}:FSIM:STAT {1 if enable else 0}")

    def is_fixture_simulation_enabled(self) -> bool:
        """
        Query if fixture simulation function is enabled.

        Parameter:
            None

        Return:
            bool: True if enabled, False otherwise
        """
        return bool(int(self.instrument.query(f":CALC{self.n}:FSIM:STAT?")))

    class Trace:
        """
        Trace analysis, limit tests, markers, trace memory, math, statistic, trace data transfer.
        """
        def __init__(self, instrument, data_handler,channel):
            self.instrument = instrument
            self.data_handler = data_handler
            self.n = channel
            self.hold = self.Hold(self.instrument, self.data_handler,channel)

        # CALC:FUNC:DATA? - Analysis result data array
        def get_analysis_result_data(self):
            """
            Get the analysis result data array.

            Parameter:
                None

            Return:
                list: Analysis result data array
            """
            data = self.instrument.query(f":CALC{self.n}:FUNC:DATA?")
            if self.data_handler.is_auto_saving_data_enabled():
                self.data_handler.write_to_file(self, "ANALYSIS_RESULT", data, file_type = EFileType.CSV)
            return self.data_handler.parse_array(data)

        # CALC:FUNC:DOM - Arbitrary sweep range ON/OFF
        def enable_arbitrary_sweep_range(self, enable: bool):
            """
            Enable or disable arbitrary sweep range.

            Parameter:
                enable (bool): True to enable, False to disable

            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:FUNC:DOM {1 if enable else 0}")

        def is_arbitrary_sweep_range_enabled(self) -> bool:
            """
            Query if arbitrary sweep range is enabled.

            Parameter:
                None

            Return:
                bool: True if enabled, False otherwise
            """
            return bool(int(self.instrument.query(f":CALC{self.n}:FUNC:DOM?")))

        # CALC:FUNC:DOM:COUP - Coupling range ON/OFF
        def enable_coupling_range(self, enable: bool):
            """
            Enable or disable coupling range.

            Parameter:
                enable (bool): True to enable, False to disable

            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:FUNC:DOM:COUP {1 if enable else 0}")

        def is_coupling_range_enabled(self) -> bool:
            """
            Query if coupling range is enabled.

            Parameter:
                None

            Return:
                bool: True if enabled, False otherwise
            """
            return bool(int(self.instrument.query(f":CALC{self.n}:FUNC:DOM:COUP?")))

        # CALC:FUNC:DOM:STAR - Analysis range start
        def set_analysis_range_start(self, value: float):
            """
            Set the analysis range start.

            Parameter:
                value (float): Start value

            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:FUNC:DOM:STAR {value}")

        def get_analysis_range_start(self) -> float:
            """
            Get the analysis range start.

            Parameter:
                None

            Return:
                float: Start value
            """
            return float(self.instrument.query(f":CALC{self.n}:FUNC:DOM:STAR?"))

        # CALC:FUNC:DOM:STOP - Analysis range stop
        def set_analysis_range_stop(self, value: float):
            """
            Set the analysis range stop.

            Parameter:
                value (float): Stop value

            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:FUNC:DOM:STOP {value}")

        def get_analysis_range_stop(self) -> float:
            """
            Get the analysis range stop.

            Parameter:
                None

            Return:
                float: Stop value
            """
            return float(self.instrument.query(f":CALC{self.n}:FUNC:DOM:STOP?"))

        # CALC:FUNC:EXEC - Execute analysis
        def execute_analysis(self):
            """
            Execute analysis.

            Parameter:
                None

            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:FUNC:EXEC")

        # CALC:FUNC:PEXC - Lower limit for the peak excursion value
        def set_peak_excursion_limit(self, value: float):
            """
            Set the lower limit for the peak excursion value.

            Parameter:
                value (float): Lower limit

            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:FUNC:PEXC {value}")

        def get_peak_excursion_limit(self) -> float:
            """
            Get the lower limit for the peak excursion value.

            Parameter:
                None

            Return:
                float: Lower limit
            """
            return float(self.instrument.query(f":CALC{self.n}:FUNC:PEXC?"))

        # CALC:FUNC:POIN? - Number of points (data pairs)
        def get_number_of_points(self) -> int:
            """
            Get the number of points (data pairs).

            Parameter:
                None

            Return:
                int: Number of points
            """
            return int(self.instrument.query(f":CALC{self.n}:FUNC:POIN?"))

        # CALC:FUNC:PPOL - Peak polarity
        def set_peak_polarity(self, polarity: str):
            """
            Set the peak polarity.

            Parameter:
                polarity (str): One of ['POS', 'NEG', 'BOTH']

            Return:
                None
            """
            allowed = ['POS', 'NEG', 'BOTH']
            if polarity not in allowed:
                raise ValueError(f"polarity must be one of {allowed}")
            self.instrument.write(f":CALC{self.n}:FUNC:PPOL {polarity}")

        def get_peak_polarity(self) -> str:
            """
            Get the peak polarity.

            Parameter:
                None

            Return:
                str: Peak polarity
            """
            return self.instrument.query(f":CALC{self.n}:FUNC:PPOL?").strip()

        # CALC:FUNC:TARG - Target level
        def set_target_level(self, value: float):
            """
            Set the target level.

            Parameter:
                value (float): Target level

            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:FUNC:TARG {value}")

        def get_target_level(self) -> float:
            """
            Get the target level.

            Parameter:
                None

            Return:
                float: Target level
            """
            return float(self.instrument.query(f":CALC{self.n}:FUNC:TARG?"))

        # CALC:FUNC:TTR - Transition type
        def set_transition_type(self, ttype: str):
            """
            Set the transition type.

            Parameter:
                ttype (str): One of ['RISE', 'FALL', 'BOTH']

            Return:
                None
            """
            allowed = ['RISE', 'FALL', 'BOTH']
            if ttype not in allowed:
                raise ValueError(f"ttype must be one of {allowed}")
            self.instrument.write(f":CALC{self.n}:FUNC:TTR {ttype}")

        def get_transition_type(self) -> str:
            """
            Get the transition type.

            Parameter:
                None

            Return:
                str: Transition type
            """
            return self.instrument.query(f":CALC{self.n}:FUNC:TTR?").strip()

        # CALC:FUNC:TYPE - Analysis type
        def set_analysis_type(self, atype: str):
            """
            Set the analysis type.

            Parameter:
                atype (str): Analysis type, e.g., 'PEAK', 'VALLEY', etc.

            Return:
                None
            """
            allowed = ['PEAK', 'VALLEY', 'EDGE', 'LEVEL', 'BWID', 'FLAT', 'TTR']
            if atype not in allowed:
                raise ValueError(f"atype must be one of {allowed}")
            self.instrument.write(f":CALC{self.n}:FUNC:TYPE {atype}")

        def get_analysis_type(self) -> str:
            """
            Get the analysis type.

            Parameter:
                None

            Return:
                str: Analysis type
            """
            return self.instrument.query(f":CALC{self.n}:FUNC:TYPE?").strip()

        class Hold:
            """
            Commands for trace hold functionality.
            """
            def __init__(self, instrument,data_handler, channel):
                self.instrument = instrument
                self.data_handler = data_handler
                self.n = channel
            # CALC:HOLD:TYPE - Trace hold type
            def set_trace_hold_type(self, hold_type: str):
                """
                Set the trace hold type.

                Parameter:
                    hold_type (str): Trace hold type, e.g., 'NONE', 'MAX', 'MIN', etc.

                Return:
                    None
                """
                allowed = ['NONE', 'MAX', 'MIN', 'AVER']
                if hold_type not in allowed:
                    raise ValueError(f"hold_type must be one of {allowed}")
                self.instrument.write(f":CALC{self.n}:HOLD:TYPE {hold_type}")

            def get_trace_hold_type(self) -> str:
                """
                Get the trace hold type.

                Parameter:
                    None

                Return:
                    str: Trace hold type
                """
                return self.instrument.query(f":CALC{self.n}:HOLD:TYPE?").strip()

            # CALC:HOLD:CLE - Trace hold restart
            def restart_trace_hold(self):
                """
                Restart trace hold.

                Parameter:
                    None

                Return:
                    None
                """
                self.instrument.write(f":CALC{self.n}:HOLD:CLE")

    class Limit:
        """
            Commands for limit tests, limit line table, limits display, limit test result,
            """
        def __init__(self, instrument, data_handler, channel):
            self.instrument = instrument
            self.data_handler = data_handler
            self.n = channel
        # CALC:LIM - Limit test ON/OFF
        def enable_limit_test(self, enable: bool):
            """
            Enable or disable limit test.

            Parameter:
                enable (bool): True to enable, False to disable

            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:LIM {1 if enable else 0}")

        def is_limit_test_enabled(self) -> bool:
            """
            Query if limit test is enabled.

            Parameter:
                None

            Return:
                bool: True if enabled, False otherwise
            """
            return bool(int(self.instrument.query(f":CALC{self.n}:LIM?")))

        # CALC:LIM:DATA - Limit line table
        def set_limit_line_table(self, table: str):
            """
            Set the limit line table.

            Parameter:
                table (str): Limit line table string

            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:LIM:DATA {table}")

        def get_limit_line_table(self) -> str:
            """
            Get the limit line table.

            Parameter:
                None

            Return:
                str: Limit line table string
            """
            data = self.instrument.query(f":CALC{self.n}:LIM:DATA?").strip()
            if self.data_handler.is_auto_saving_data_enabled():
                self.data_handler.write_to_file(self, "LIMIT_LINE", data, file_type = EFileType.CSV)
            return data
        # CALC:LIM:DISP - Limits display ON/OFF
        def enable_limits_display(self, enable: bool):
            """
            Enable or disable limits display.

            Parameter:
                enable (bool): True to enable, False to disable

            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:LIM:DISP {1 if enable else 0}")

        def is_limits_display_enabled(self) -> bool:
            """
            Query if limits display is enabled.

            Parameter:
                None

            Return:
                bool: True if enabled, False otherwise
            """
            return bool(int(self.instrument.query(f":CALC{self.n}:LIM:DISP?")))

        # CALC:LIM:FAIL? - Limit test result
        def get_limit_test_result(self) -> bool:
            """
            Get the limit test result.

            Parameter:
                None

            Return:
                bool: True if test failed, False otherwise
            """
            return bool(int(self.instrument.query(f":CALC{self.n}:LIM:FAIL?")))

        # CALC:LIM:OFFS:AMPL - Limit line Y-offset
        def set_limit_line_y_offset(self, value: float):
            """
            Set the limit line Y-offset.

            Parameter:
                value (float): Y-offset value

            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:LIM:OFFS:AMPL {value}")

        def get_limit_line_y_offset(self) -> float:
            """
            Get the limit line Y-offset.

            Parameter:
                None

            Return:
                float: Y-offset value
            """
            return float(self.instrument.query(f":CALC{self.n}:LIM:OFFS:AMPL?"))

        # CALC:LIM:OFFS:MARK - Limit line Y-offset to active marker value
        def set_limit_line_y_offset_to_marker(self, value: float):
            """
            Set the limit line Y-offset to active marker value.

            Parameter:
                value (float): Y-offset value

            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:LIM:OFFS:MARK {value}")

        def get_limit_line_y_offset_to_marker(self) -> float:
            """
            Get the limit line Y-offset to active marker value.

            Parameter:
                None

            Return:
                float: Y-offset value
            """
            return float(self.instrument.query(f":CALC{self.n}:LIM:OFFS:MARK?"))

        # CALC:LIM:OFFS:STIM - Limit line X-offset
        def set_limit_line_x_offset(self, value: float):
            """
            Set the limit line X-offset.

            Parameter:
                value (float): X-offset value

            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:LIM:OFFS:STIM {value}")

        def get_limit_line_x_offset(self) -> float:
            """
            Get the limit line X-offset.

            Parameter:
                None

            Return:
                float: X-offset value
            """
            return float(self.instrument.query(f":CALC{self.n}:LIM:OFFS:STIM?"))

        # CALC:LIM:REP:ALL? - Limit test result report
        def get_limit_test_result_report(self) -> str:
            """
            Get the limit test result report.

            Parameter:
                None

            Return:
                str: Limit test result report
            """
            return self.instrument.query(f":CALC{self.n}:LIM:REP:ALL?").strip()

        # CALC:LIM:REP:POIN? - Failed points
        def get_failed_points(self) -> str:
            """
            Get the failed points.

            Parameter:
                None

            Return:
                str: Failed points
            """
            return self.instrument.query(f":CALC{self.n}:LIM:REP:POIN?").strip()

        # CALC:LIM:REP? - Stimulus values of failed points
        def get_failed_points_stimulus_values(self) -> str:
            """
            Get the stimulus values of failed points.

            Parameter:
                None

            Return:
                str: Stimulus values
            """
            return self.instrument.query(f":CALC{self.n}:LIM:REP?").strip()

    class Marker:
        """
            Commands for modifying the marker function parameters.
            """
        def __init__(self, instrument, data_handler, channel):
            self.instrument = instrument
            self.data_handler = data_handler
            self.n = channel
        # CALC:MARK - Marker ON/OFF
        def enable_marker(self, marker: int, enable: bool):
            """
            Enable or disable marker.
    
            Parameter:
                marker (int): Marker number
                enable (bool): True to enable, False to disable
    
            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:MARK{marker} {1 if enable else 0}")
    
        def is_marker_enabled(self, marker: int) -> bool:
            """
            Query if marker is enabled.
    
            Parameter:
                marker (int): Marker number
    
            Return:
                bool: True if enabled, False otherwise
            """
            return bool(int(self.instrument.query(f":CALC{self.n}:MARK{marker}?")))
    
        # CALC:MARK:ACT - Sets active marker
        def set_active_marker(self, marker: int):
            """
            Set the active marker.
    
            Parameter:
                marker (int): Marker number
    
            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:MARK:ACT {marker}")
    
        def get_active_marker(self) -> int:
            """
            Get the active marker.
    
            Parameter:
                None
    
            Return:
                int: Active marker number
            """
            return int(self.instrument.query(f":CALC{self.n}:MARK:ACT?"))
    
        # CALC:MARK:COUN - Number of markers
        def set_marker_count(self, count: int):
            """
            Set the number of markers.
    
            Parameter:
                count (int): Number of markers
    
            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:MARK:COUN {count}")
    
        def get_marker_count(self) -> int:
            """
            Get the number of markers.
    
            Parameter:
                None
    
            Return:
                int: Number of markers
            """
            return int(self.instrument.query(f":CALC{self.n}:MARK:COUN?"))
    
        # CALC:MARK:COUP - Coupling of markers ON/OFF
        def enable_marker_coupling(self, enable: bool):
            """
            Enable or disable coupling of markers.
    
            Parameter:
                enable (bool): True to enable, False to disable
    
            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:MARK:COUP {1 if enable else 0}")
    
        def is_marker_coupling_enabled(self) -> bool:
            """
            Query if coupling of markers is enabled.
    
            Parameter:
                None
    
            Return:
                bool: True if enabled, False otherwise
            """
            return bool(int(self.instrument.query(f":CALC{self.n}:MARK:COUP?")))
    
        # CALC:MARK:DATA? - Response and stimulus values of all trace marker
        def get_all_marker_data(self):
            """
            Get response and stimulus values of all trace markers.
    
            Parameter:
                None
    
            Return:
                list: Marker data array
            """
            data = self.instrument.query(f":CALC{self.n}:MARK:DATA?")
            if self.data_handler.is_auto_saving_data_enabled():
                self.data_handler.write_to_file(self, "MARKER", data, file_type = EFileType.CSV)
            return self.data_handler.parse_array(data)
    
        # CALC:MARK:DISC - Marker discrete mode ON/OFF
        def enable_marker_discrete_mode(self, enable: bool):
            """
            Enable or disable marker discrete mode.
    
            Parameter:
                enable (bool): True to enable, False to disable
    
            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:MARK:DISC {1 if enable else 0}")
    
        def is_marker_discrete_mode_enabled(self) -> bool:
            """
            Query if marker discrete mode is enabled.
    
            Parameter:
                None
    
            Return:
                bool: True if enabled, False otherwise
            """
            return bool(int(self.instrument.query(f":CALC{self.n}:MARK:DISC?")))
    
        # CALC:MARK:REF - Reference marker ON/OFF
        def enable_reference_marker(self, marker: int, enable: bool):
            """
            Enable or disable reference marker.
    
            Parameter:
                marker (int): Marker number
                enable (bool): True to enable, False to disable
    
            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:MARK{marker}:REF {1 if enable else 0}")
    
        def is_reference_marker_enabled(self, marker: int) -> bool:
            """
            Query if reference marker is enabled.
    
            Parameter:
                marker (int): Marker number
    
            Return:
                bool: True if enabled, False otherwise
            """
            return bool(int(self.instrument.query(f":CALC{self.n}:MARK{marker}:REF?")))
    
        # CALC:MARK:X - Stimulus value of marker
        def set_marker_x(self, marker: int, value: float):
            """
            Set the stimulus value of marker.
    
            Parameter:
                marker (int): Marker number
                value (float): Stimulus value
    
            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:MARK{marker}:X {value}")
    
        def get_marker_x(self, marker: int) -> float:
            """
            Get the stimulus value of marker.
    
            Parameter:
                marker (int): Marker number
    
            Return:
                float: Stimulus value
            """
            return float(self.instrument.query(f":CALC{self.n}:MARK{marker}:X?"))
    
        # CALC:MARK:Y? - Response value of marker
        def get_marker_y(self, marker: int) -> float:
            """
            Get the response value of marker.
    
            Parameter:
                marker (int): Marker number
    
            Return:
                float: Response value
            """
            return float(self.instrument.query(f":CALC{self.n}:MARK{marker}:Y?"))
    
        # CALC:MARK:BWID - Bandwidth search ON/OFF
        def enable_bandwidth_search(self, marker: int, enable: bool):
            """
            Enable or disable bandwidth search for marker.
    
            Parameter:
                marker (int): Marker number
                enable (bool): True to enable, False to disable
    
            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:MARK{marker}:BWID {1 if enable else 0}")
    
        def is_bandwidth_search_enabled(self, marker: int) -> bool:
            """
            Query if bandwidth search for marker is enabled.
    
            Parameter:
                marker (int): Marker number
    
            Return:
                bool: True if enabled, False otherwise
            """
            return bool(int(self.instrument.query(f":CALC{self.n}:MARK{marker}:BWID?")))
    
        # CALC:MARK:BWID:DATA? - Bandwidth search result
        def get_bandwidth_search_result(self, marker: int):
            """
            Get bandwidth search result for marker.
    
            Parameter:
                marker (int): Marker number
    
            Return:
                list: Bandwidth search result array
            """
            data = self.instrument.query(f":CALC{self.n}:MARK{marker}:BWID:DATA?")
            if self.data_handler.is_auto_saving_data_enabled():
                self.data_handler.write_to_file(self, "BWDTH_SEARCH", data, file_type = EFileType.CSV)
            return self.data_handler.parse_array(data)
    
        # CALC:MARK:BWID:REF - Reference of search
        def set_bandwidth_search_reference(self, marker: int, value: float):
            """
            Set reference of bandwidth search for marker.
    
            Parameter:
                marker (int): Marker number
                value (float): Reference value
    
            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:MARK{marker}:BWID:REF {value}")
    
        def get_bandwidth_search_reference(self, marker: int) -> float:
            """
            Get reference of bandwidth search for marker.
    
            Parameter:
                marker (int): Marker number
    
            Return:
                float: Reference value
            """
            return float(self.instrument.query(f":CALC{self.n}:MARK{marker}:BWID:REF?"))
    
        # CALC:MARK:BWID:THR - Bandwidth threshold value
        def set_bandwidth_threshold(self, marker: int, value: float):
            """
            Set bandwidth threshold value for marker.
    
            Parameter:
                marker (int): Marker number
                value (float): Threshold value
    
            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:MARK{marker}:BWID:THR {value}")
    
        def get_bandwidth_threshold(self, marker: int) -> float:
            """
            Get bandwidth threshold value for marker.
    
            Parameter:
                marker (int): Marker number
    
            Return:
                float: Threshold value
            """
            return float(self.instrument.query(f":CALC{self.n}:MARK{marker}:BWID:THR?"))
    
        # CALC:MARK:BWID:TYPE - Type of search
        def set_bandwidth_search_type(self, marker: int, search_type: str):
            """
            Set type of bandwidth search for marker.
    
            Parameter:
                marker (int): Marker number
                search_type (str): One of ['3DB', '6DB', 'XDB']
    
            Return:
                None
            """
            allowed = ['3DB', '6DB', 'XDB']
            if search_type not in allowed:
                raise ValueError(f"search_type must be one of {allowed}")
            self.instrument.write(f":CALC{self.n}:MARK{marker}:BWID:TYPE {search_type}")
    
        def get_bandwidth_search_type(self, marker: int) -> str:
            """
            Get type of bandwidth search for marker.
    
            Parameter:
                marker (int): Marker number
    
            Return:
                str: Search type
            """
            return self.instrument.query(f":CALC{self.n}:MARK{marker}:BWID:TYPE?").strip()
    
        # CALC:MARK:FUNC:DOM - Marker search arbitrary range ON/OFF
        def enable_marker_search_arbitrary_range(self, marker: int, enable: bool):
            """
            Enable or disable marker search arbitrary range.
    
            Parameter:
                marker (int): Marker number
                enable (bool): True to enable, False to disable
    
            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:MARK{marker}:FUNC:DOM {1 if enable else 0}")
    
        def is_marker_search_arbitrary_range_enabled(self, marker: int) -> bool:
            """
            Query if marker search arbitrary range is enabled.
    
            Parameter:
                marker (int): Marker number
    
            Return:
                bool: True if enabled, False otherwise
            """
            return bool(int(self.instrument.query(f":CALC{self.n}:MARK{marker}:FUNC:DOM?")))
    
        # CALC:MARK:FUNC:DOM:COUP - Coupling of marker search ranges ON/OFF
        def enable_marker_search_range_coupling(self, marker: int, enable: bool):
            """
            Enable or disable coupling of marker search ranges.
    
            Parameter:
                marker (int): Marker number
                enable (bool): True to enable, False to disable
    
            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:MARK{marker}:FUNC:DOM:COUP {1 if enable else 0}")
    
        def is_marker_search_range_coupling_enabled(self, marker: int) -> bool:
            """
            Query if coupling of marker search ranges is enabled.
    
            Parameter:
                marker (int): Marker number
    
            Return:
                bool: True if enabled, False otherwise
            """
            return bool(int(self.instrument.query(f":CALC{self.n}:MARK{marker}:FUNC:DOM:COUP?")))
    
        # CALC:MARK:FUNC:DOM:STAR - Start of the marker search range
        def set_marker_search_range_start(self, marker: int, value: float):
            """
            Set start of the marker search range.
    
            Parameter:
                marker (int): Marker number
                value (float): Start value
    
            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:MARK{marker}:FUNC:DOM:STAR {value}")
    
        def get_marker_search_range_start(self, marker: int) -> float:
            """
            Get start of the marker search range.
    
            Parameter:
                marker (int): Marker number
    
            Return:
                float: Start value
            """
            return float(self.instrument.query(f":CALC{self.n}:MARK{marker}:FUNC:DOM:STAR?"))
    
        # CALC:MARK:FUNC:DOM:STOP - Stop of the marker search range
        def set_marker_search_range_stop(self, marker: int, value: float):
            """
            Set stop of the marker search range.
    
            Parameter:
                marker (int): Marker number
                value (float): Stop value
    
            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:MARK{marker}:FUNC:DOM:STOP {value}")
    
        def get_marker_search_range_stop(self, marker: int) -> float:
            """
            Get stop of the marker search range.
    
            Parameter:
                marker (int): Marker number
    
            Return:
                float: Stop value
            """
            return float(self.instrument.query(f":CALC{self.n}:MARK{marker}:FUNC:DOM:STOP?"))
    
        # CALC:MARK:FUNC:EXEC - Executes search
        def execute_marker_search(self, marker: int):
            """
            Execute marker search.
    
            Parameter:
                marker (int): Marker number
    
            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:MARK{marker}:FUNC:EXEC")
    
        # CALC:MARK:FUNC:PEXC - Peak excursion value
        def set_marker_peak_excursion(self, marker: int, value: float):
            """
            Set peak excursion value for marker.
    
            Parameter:
                marker (int): Marker number
                value (float): Peak excursion value
    
            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:MARK{marker}:FUNC:PEXC {value}")
    
        def get_marker_peak_excursion(self, marker: int) -> float:
            """
            Get peak excursion value for marker.
    
            Parameter:
                marker (int): Marker number
    
            Return:
                float: Peak excursion value
            """
            return float(self.instrument.query(f":CALC{self.n}:MARK{marker}:FUNC:PEXC?"))
    
        # CALC:MARK:FUNC:PPOL - Peak polarity
        def set_marker_peak_polarity(self, marker: int, polarity: str):
            """
            Set peak polarity for marker.
    
            Parameter:
                marker (int): Marker number
                polarity (str): One of ['POS', 'NEG', 'BOTH']
    
            Return:
                None
            """
            allowed = ['POS', 'NEG', 'BOTH']
            if polarity not in allowed:
                raise ValueError(f"polarity must be one of {allowed}")
            self.instrument.write(f":CALC{self.n}:MARK{marker}:FUNC:PPOL {polarity}")
    
        def get_marker_peak_polarity(self, marker: int) -> str:
            """
            Get peak polarity for marker.
    
            Parameter:
                marker (int): Marker number
    
            Return:
                str: Peak polarity
            """
            return self.instrument.query(f":CALC{self.n}:MARK{marker}:FUNC:PPOL?").strip()
    
        # CALC:MARK:FUNC:TARG - Target value
        def set_marker_target_value(self, marker: int, value: float):
            """
            Set target value for marker.
    
            Parameter:
                marker (int): Marker number
                value (float): Target value
    
            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:MARK{marker}:FUNC:TARG {value}")
    
        def get_marker_target_value(self, marker: int) -> float:
            """
            Get target value for marker.
    
            Parameter:
                marker (int): Marker number
    
            Return:
                float: Target value
            """
            return float(self.instrument.query(f":CALC{self.n}:MARK{marker}:FUNC:TARG?"))
    
        # CALC:MARK:FUNC:TRAC - Marker search tracking ON/OFF
        def enable_marker_search_tracking(self, marker: int, enable: bool):
            """
            Enable or disable marker search tracking.
    
            Parameter:
                marker (int): Marker number
                enable (bool): True to enable, False to disable
    
            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:MARK{marker}:FUNC:TRAC {1 if enable else 0}")
    
        def is_marker_search_tracking_enabled(self, marker: int) -> bool:
            """
            Query if marker search tracking is enabled.
    
            Parameter:
                marker (int): Marker number
    
            Return:
                bool: True if enabled, False otherwise
            """
            return bool(int(self.instrument.query(f":CALC{self.n}:MARK{marker}:FUNC:TRAC?")))
    
        # CALC:MARK:FUNC:TTR - Type of target transition
        def set_marker_target_transition_type(self, marker: int, ttype: str):
            """
            Set type of target transition for marker.
    
            Parameter:
                marker (int): Marker number
                ttype (str): One of ['RISE', 'FALL', 'BOTH']
    
            Return:
                None
            """
            allowed = ['RISE', 'FALL', 'BOTH']
            if ttype not in allowed:
                raise ValueError(f"ttype must be one of {allowed}")
            self.instrument.write(f":CALC{self.n}:MARK{marker}:FUNC:TTR {ttype}")
    
        def get_marker_target_transition_type(self, marker: int) -> str:
            """
            Get type of target transition for marker.
    
            Parameter:
                marker (int): Marker number
    
            Return:
                str: Transition type
            """
            return self.instrument.query(f":CALC{self.n}:MARK{marker}:FUNC:TTR?").strip()
    
        # CALC:MARK:FUNC:TYPE - Search type
        def set_marker_search_type(self, marker: int, search_type: str):
            """
            Set search type for marker.
    
            Parameter:
                marker (int): Marker number
                search_type (str): One of ['PEAK', 'VALLEY', 'EDGE', 'LEVEL', 'BWID', 'FLAT', 'TTR']
    
            Return:
                None
            """
            allowed = ['PEAK', 'VALLEY', 'EDGE', 'LEVEL', 'BWID', 'FLAT', 'TTR']
            if search_type not in allowed:
                raise ValueError(f"search_type must be one of {allowed}")
            self.instrument.write(f":CALC{self.n}:MARK{marker}:FUNC:TYPE {search_type}")
    
        def get_marker_search_type(self, marker: int) -> str:
            """
            Get search type for marker.
    
            Parameter:
                marker (int): Marker number
    
            Return:
                str: Search type
            """
            return self.instrument.query(f":CALC{self.n}:MARK{marker}:FUNC:TYPE?").strip()
    
        # CALC:MARK:MATH:FLAT:DATA? - Flatness function data
        def get_marker_flatness_data(self, marker: int):
            """
            Get flatness function data for marker.
    
            Parameter:
                marker (int): Marker number
    
            Return:
                list: Flatness data array
            """
            data = self.instrument.query(f":CALC{self.n}:MARK{marker}:MATH:FLAT:DATA?")
            if self.data_handler.is_auto_saving_data_enabled():
                self.data_handler.write_to_file(self, "MARKER_FLATNESS", data, file_type = EFileType.CSV)
            return self.data_handler.parse_array(data)
    
        # CALC:MARK:MATH:FLAT:STAT - Marker flatness ON/OFF
        def enable_marker_flatness(self, marker: int, enable: bool):
            """
            Enable or disable marker flatness.
    
            Parameter:
                marker (int): Marker number
                enable (bool): True to enable, False to disable
    
            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:MARK{marker}:MATH:FLAT:STAT {1 if enable else 0}")
    
        def is_marker_flatness_enabled(self, marker: int) -> bool:
            """
            Query if marker flatness is enabled.
    
            Parameter:
                marker (int): Marker number
    
            Return:
                bool: True if enabled, False otherwise
            """
            return bool(int(self.instrument.query(f":CALC{self.n}:MARK{marker}:MATH:FLAT:STAT?")))
    
        # CALC:MARK:MATH:FLAT:DOM:STAR - Marker specifying start of frequency range
        def set_marker_flatness_range_start(self, marker: int, value: float):
            """
            Set marker specifying start of frequency range for flatness.
    
            Parameter:
                marker (int): Marker number
                value (float): Start value
    
            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:MARK{marker}:MATH:FLAT:DOM:STAR {value}")
    
        def get_marker_flatness_range_start(self, marker: int) -> float:
            """
            Get marker specifying start of frequency range for flatness.
    
            Parameter:
                marker (int): Marker number
    
            Return:
                float: Start value
            """
            return float(self.instrument.query(f":CALC{self.n}:MARK{marker}:MATH:FLAT:DOM:STAR?"))
    
        # CALC:MARK:MATH:FLAT:DOM:STOP - Marker specifying stop of frequency range
        def set_marker_flatness_range_stop(self, marker: int, value: float):
            """
            Set marker specifying stop of frequency range for flatness.
    
            Parameter:
                marker (int): Marker number
                value (float): Stop value
    
            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:MARK{marker}:MATH:FLAT:DOM:STOP {value}")
    
        def get_marker_flatness_range_stop(self, marker: int) -> float:
            """
            Get marker specifying stop of frequency range for flatness.
    
            Parameter:
                marker (int): Marker number
    
            Return:
                float: Stop value
            """
            return float(self.instrument.query(f":CALC{self.n}:MARK{marker}:MATH:FLAT:DOM:STOP?"))
    
        # CALC:MARK:SET - Sets item value according to the position of the marker
        def set_item_value_by_marker(self, marker: int):
            """
            Set item value according to the position of the marker.
    
            Parameter:
                marker (int): Marker number
    
            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:MARK{marker}:SET")
    
    class Math:
        """
        Memory Trace Function, Math operation, statistics, smoothing, ripple limit, and time domain.
        """
        def __init__(self, instrument, data_handler, channel):
            self.instrument = instrument
            self.data_handler = data_handler
            self.n = channel
        # CALC:MATH:FUNC - Math operation
        def set_math_operation(self, operation: str):
            """
            Set the math operation for memory trace.

            Parameter:
                operation (str): Math operation, e.g., 'ADD', 'SUB', 'MUL', 'DIV', etc.

            Return:
                None
            """
            allowed = ['ADD', 'SUB', 'MUL', 'DIV', 'NONE']
            if operation not in allowed:
                raise ValueError(f"operation must be one of {allowed}")
            self.instrument.write(f":CALC{self.n}:MATH:FUNC {operation}")

        def get_math_operation(self) -> str:
            """
            Get the current math operation for memory trace.

            Parameter:
                None

            Return:
                str: Math operation
            """
            return self.instrument.query(f":CALC{self.n}:MATH:FUNC?").strip()

        # CALC:MATH:MEM - Data => Memory
        def store_data_to_memory(self):
            """
            Store current data to memory.

            Parameter:
                None

            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:MATH:MEM")

    class MST:
        """
         Commands math statistics commands.
        """
        def __init__(self, instrument, data_handler, channel):
            self.instrument = instrument
            self.data_handler = data_handler
            self.n = channel
        # CALC:MST - Math statistics ON/OFF
        def enable_statistics(self, enable: bool):
            """
            Enable or disable math statistics.

            Parameter:
                enable (bool): True to enable, False to disable

            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:MST {1 if enable else 0}")

        def is_statistics_enabled(self) -> bool:
            """
            Query if math statistics is enabled.

            Parameter:
                None

            Return:
                bool: True if enabled, False otherwise
            """
            return bool(int(self.instrument.query(f":CALC{self.n}:MST?")))

        # CALC:MST:DATA? - Math statistics data
        def get_statistics_data(self):
            """
            Get math statistics data.

            Parameter:
                None

            Return:
                list: Statistics data array
            """
            data = self.instrument.query(f":CALC{self.n}:MST:DATA?")
            if self.data_handler.is_auto_saving_data_enabled():
                self.data_handler.write_to_file(self, "MSTH_STATS", data, file_type = EFileType.CSV)
            return self.data_handler.parse_array(data)

        # CALC:MST:DOM - Partial frequency range ON/OFF
        def enable_partial_frequency_range(self, enable: bool):
            """
            Enable or disable partial frequency range for statistics.

            Parameter:
                enable (bool): True to enable, False to disable

            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:MST:DOM {1 if enable else 0}")

        def is_partial_frequency_range_enabled(self) -> bool:
            """
            Query if partial frequency range is enabled for statistics.

            Parameter:
                None

            Return:
                bool: True if enabled, False otherwise
            """
            return bool(int(self.instrument.query(f":CALC{self.n}:MST:DOM?")))

        # CALC:MST:DOM:STAR - Marker specifying start of frequency range
        def set_statistics_range_start(self, value: float):
            """
            Set marker specifying start of frequency range for statistics.

            Parameter:
                value (float): Start value

            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:MST:DOM:STAR {value}")

        def get_statistics_range_start(self) -> float:
            """
            Get marker specifying start of frequency range for statistics.

            Parameter:
                None

            Return:
                float: Start value
            """
            return float(self.instrument.query(f":CALC{self.n}:MST:DOM:STAR?"))

        # CALC:MST:DOM:STOP - Marker specifying stop of frequency range
        def set_statistics_range_stop(self, value: float):
            """
            Set marker specifying stop of frequency range for statistics.

            Parameter:
                value (float): Stop value

            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:MST:DOM:STOP {value}")

        def get_statistics_range_stop(self) -> float:
            """
            Get marker specifying stop of frequency range for statistics.

            Parameter:
                None

            Return:
                float: Stop value
            """
            return float(self.instrument.query(f":CALC{self.n}:MST:DOM:STOP?"))
    # CALC:PAR:DEF - Define a new trace
    def define_trace(self, trace_name: str, parameter: str):
        """
        Define a new trace with the given name and parameter.

        Parameter:
        trace_name (str): Name of the trace
        parameter (str): S-parameter (e.g., 'S11', 'S21', etc.)

        Return:
        None
        """
        self.instrument.write(f":CALC{self.n}:PAR:DEF '{trace_name}',{parameter}")

    # CALC:PAR:SPOR - Select trace by name
    def select_trace_by_name(self, trace_name: str):
        """
        Select the trace by its name.

        Parameter:
        trace_name (str): Name of the trace

        Return:
        None
        """
        self.instrument.write(f":CALC{self.n}:PAR:SPOR '{trace_name}'")

    class RLIM:
        """
        Ripple Limit Test commands.
        """
        def __init__(self, instrument, data_handler, channel):
            self.instrument = instrument
            self.data_handler = data_handler
            self.n = channel
        # CALC:RLIM - Ripple limit test ON/OFF
        def enable_ripple_limit_test(self, enable: bool):
            """
            Enable or disable ripple limit test.

            Parameter:
                enable (bool): True to enable, False to disable

            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:RLIM {1 if enable else 0}")

        def is_ripple_limit_test_enabled(self) -> bool:
            """
            Query if ripple limit test is enabled.

            Parameter:
                None

            Return:
                bool: True if enabled, False otherwise
            """
            return bool(int(self.instrument.query(f":CALC{self.n}:RLIM?")))

        # CALC:RLIM:DATA - Ripple limit line table
        def set_ripple_limit_line_table(self, table: str):
            """
            Set the ripple limit line table.

            Parameter:
                table (str): Ripple limit line table string

            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:RLIM:DATA {table}")

        def get_ripple_limit_line_table(self) -> str:
            """
            Get the ripple limit line table.

            Parameter:
                None

            Return:
                str: Ripple limit line table string
            """
            data = self.instrument.query(f":CALC{self.n}:RLIM:DATA?").strip()
            if self.data_handler.is_auto_saving_data_enabled():
                self.data_handler.write_to_file(self, "RIPPLE_LIMIT_LINE", data, file_type = EFileType.CSV)
            return data

        # CALC:RLIM:DISP:LINE - Ripple Limit line display ON/OFF
        def enable_ripple_limit_line_display(self, enable: bool):
            """
            Enable or disable ripple limit line display.

            Parameter:
                enable (bool): True to enable, False to disable

            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:RLIM:DISP:LINE {1 if enable else 0}")

        def is_ripple_limit_line_display_enabled(self) -> bool:
            """
            Query if ripple limit line display is enabled.

            Parameter:
                None

            Return:
                bool: True if enabled, False otherwise
            """
            return bool(int(self.instrument.query(f":CALC{self.n}:RLIM:DISP:LINE?")))

        # CALC:RLIM:DISP:SEL - Number of band for ripple value display
        def set_ripple_band_display(self, band: int):
            """
            Set the number of band for ripple value display.

            Parameter:
                band (int): Band number

            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:RLIM:DISP:SEL {band}")

        def get_ripple_band_display(self) -> int:
            """
            Get the number of band for ripple value display.

            Parameter:
                None

            Return:
                int: Band number
            """
            return int(self.instrument.query(f":CALC{self.n}:RLIM:DISP:SEL?"))

        # CALC:RLIM:DISP:VAL - Display type of ripple value
        def set_ripple_value_display_type(self, dtype: str):
            """
            Set the display type of ripple value.

            Parameter:
                dtype (str): Display type, e.g., 'MAX', 'MIN', 'AVG'

            Return:
                None
            """
            allowed = ['MAX', 'MIN', 'AVG']
            if dtype not in allowed:
                raise ValueError(f"dtype must be one of {allowed}")
            self.instrument.write(f":CALC{self.n}:RLIM:DISP:VAL {dtype}")

        def get_ripple_value_display_type(self) -> str:
            """
            Get the display type of ripple value.

            Parameter:
                None

            Return:
                str: Display type
            """
            return self.instrument.query(f":CALC{self.n}:RLIM:DISP:VAL?").strip()

        # CALC:RLIM:FAIL? - Ripple limit test result
        def get_ripple_limit_test_result(self) -> bool:
            """
            Get the ripple limit test result.

            Parameter:
                None

            Return:
                bool: True if test failed, False otherwise
            """
            return bool(int(self.instrument.query(f":CALC{self.n}:RLIM:FAIL?")))

        # CALC:RLIM:REP? - Ripple limit test result report
        def get_ripple_limit_test_result_report(self) -> str:
            """
            Get the ripple limit test result report.

            Parameter:
                None

            Return:
                str: Ripple limit test result report
            """
            return self.instrument.query(f":CALC{self.n}:RLIM:REP?").strip()

    class SMO:
        """
        Smoothing commands.
        """
        def __init__(self, instrument, data_handler, channel):
            self.instrument = instrument
            self.data_handler = data_handler
            self.n = channel
        # CALC:SMO - Trace smoothing ON/OFF
        def enable_smoothing(self, enable: bool):
            """
            Enable or disable trace smoothing.

            Parameter:
                enable (bool): True to enable, False to disable

            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:SMO {1 if enable else 0}")

        def is_smoothing_enabled(self) -> bool:
            """
            Query if trace smoothing is enabled.

            Parameter:
                None

            Return:
                bool: True if enabled, False otherwise
            """
            return bool(int(self.instrument.query(f":CALC{self.n}:SMO?")))

        # CALC:SMO:APER - Smoothing aperture
        def set_smoothing_aperture(self, value: float):
            """
            Set the smoothing aperture.

            Parameter:
                value (float): Aperture value

            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:SMO:APER {value}")

        def get_smoothing_aperture(self) -> float:
            """
            Get the smoothing aperture.

            Parameter:
                None

            Return:
                float: Aperture value
            """
            return float(self.instrument.query(f":CALC{self.n}:SMO:APER?"))

    class TRAN:
        """
        Time Domain related commands.
        """
        def __init__(self, instrument, data_handler, channel):
            self.instrument = instrument
            self.data_handler = data_handler
            self.n = channel
        # CALC:TRAN:TIME - Setting Time Domain Parameters (Band-pass/Low-pass)
        def set_time_domain_type(self, td_type: str):
            """
            Set the time domain type (Band-pass/Low-pass).

            Parameter:
                td_type (str): 'BPAS' for Band-pass, 'LPAS' for Low-pass

            Return:
                None
            """
            allowed = ['BPAS', 'LPAS']
            if td_type not in allowed:
                raise ValueError(f"td_type must be one of {allowed}")
            self.instrument.write(f":CALC{self.n}:TRAN:TIME {td_type}")

        def get_time_domain_type(self) -> str:
            """
            Get the time domain type.

            Parameter:
                None

            Return:
                str: Time domain type
            """
            return self.instrument.query(f":CALC{self.n}:TRAN:TIME?").strip()

        # CALC:TRAN:TIME:CENT - Time domain center
        def set_time_domain_center(self, value: float):
            """
            Set the time domain center.

            Parameter:
                value (float): Center value

            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:TRAN:TIME:CENT {value}")

        def get_time_domain_center(self) -> float:
            """
            Get the time domain center.

            Parameter:
                None

            Return:
                float: Center value
            """
            return float(self.instrument.query(f":CALC{self.n}:TRAN:TIME:CENT?"))

        # CALC:TRAN:TIME:DC:VAL - DC value
        def set_time_domain_dc_value(self, value: float):
            """
            Set the DC value for time domain.

            Parameter:
                value (float): DC value

            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:TRAN:TIME:DC:VAL {value}")

        def get_time_domain_dc_value(self) -> float:
            """
            Get the DC value for time domain.

            Parameter:
                None

            Return:
                float: DC value
            """
            return float(self.instrument.query(f":CALC{self.n}:TRAN:TIME:DC:VAL?"))

        # CALC:TRAN:TIME:EXTR:DC - DC extrapolation ON/OFF
        def enable_time_domain_dc_extrapolation(self, enable: bool):
            """
            Enable or disable DC extrapolation in time domain.

            Parameter:
                enable (bool): True to enable, False to disable

            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:TRAN:TIME:EXTR:DC {1 if enable else 0}")

        def is_time_domain_dc_extrapolation_enabled(self) -> bool:
            """
            Query if DC extrapolation in time domain is enabled.

            Parameter:
                None

            Return:
                bool: True if enabled, False otherwise
            """
            return bool(int(self.instrument.query(f":CALC{self.n}:TRAN:TIME:EXTR:DC?")))

        # CALC:TRAN:TIME:IMP:WIDT - Impulse Width
        def set_time_domain_impulse_width(self, value: float):
            """
            Set the impulse width for time domain.

            Parameter:
                value (float): Impulse width

            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:TRAN:TIME:IMP:WIDT {value}")

        def get_time_domain_impulse_width(self) -> float:
            """
            Get the impulse width for time domain.

            Parameter:
                None

            Return:
                float: Impulse width
            """
            return float(self.instrument.query(f":CALC{self.n}:TRAN:TIME:IMP:WIDT?"))

        # CALC:TRAN:TIME:KBES - Kaiser-Bessel β
        def set_time_domain_kaiser_bessel_beta(self, value: float):
            """
            Set the Kaiser-Bessel β for time domain.

            Parameter:
                value (float): Beta value

            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:TRAN:TIME:KBES {value}")

        def get_time_domain_kaiser_bessel_beta(self) -> float:
            """
            Get the Kaiser-Bessel β for time domain.

            Parameter:
                None

            Return:
                float: Beta value
            """
            return float(self.instrument.query(f":CALC{self.n}:TRAN:TIME:KBES?"))

        # CALC:TRAN:TIME:LPFR - Sets frequency Low-Pass
        def set_time_domain_lowpass_frequency(self, value: float):
            """
            Set the frequency for a Low-Pass in time domain.

            Parameter:
                value (float): Frequency value

            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:TRAN:TIME:LPFR {value}")

        def get_time_domain_lowpass_frequency(self) -> float:
            """
            Get the frequency for Low-Pass in time domain.

            Parameter:
                None

            Return:
                float: Frequency value
            """
            return float(self.instrument.query(f":CALC{self.n}:TRAN:TIME:LPFR?"))

        # CALC:TRAN:TIME:REFL:TYPE - Selects One way/Round trip
        def set_time_domain_reflection_type(self, refl_type: str):
            """
            Set the reflection type for time domain.

            Parameter:
                refl_type (str): 'ONEW' for One way, 'ROUN' for Round trip

            Return:
                None
            """
            allowed = ['ONEW', 'ROUN']
            if refl_type not in allowed:
                raise ValueError(f"refl_type must be one of {allowed}")
            self.instrument.write(f":CALC{self.n}:TRAN:TIME:REFL:TYPE {refl_type}")

        def get_time_domain_reflection_type(self) -> str:
            """
            Get the reflection type for time domain.

            Parameter:
                None

            Return:
                str: Reflection type
            """
            return self.instrument.query(f":CALC{self.n}:TRAN:TIME:REFL:TYPE?").strip()

        # CALC:TRAN:TIME:SPAN - Time domain Span
        def set_time_domain_span(self, value: float):
            """
            Set the time domain span.

            Parameter:
                value (float): Span value

            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:TRAN:TIME:SPAN {value}")

        def get_time_domain_span(self) -> float:
            """
            Get the time domain span.

            Parameter:
                None

            Return:
                float: Span value
            """
            return float(self.instrument.query(f":CALC{self.n}:TRAN:TIME:SPAN?"))

        # CALC:TRAN:TIME:STAR - Time domain Start
        def set_time_domain_start(self, value: float):
            """
            Set the time domain start.

            Parameter:
                value (float): Start value

            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:TRAN:TIME:STAR {value}")

        def get_time_domain_start(self) -> float:
            """
            Get the time domain start.

            Parameter:
                None

            Return:
                float: Start value
            """
            return float(self.instrument.query(f":CALC{self.n}:TRAN:TIME:STAR?"))

        # CALC:TRAN:TIME:STOP - Time domain Stop
        def set_time_domain_stop(self, value: float):
            """
            Set the time domain stop.

            Parameter:
                value (float): Stop value

            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:TRAN:TIME:STOP {value}")

        def get_time_domain_stop(self) -> float:
            """
            Get the time domain stop.

            Parameter:
                None

            Return:
                float: Stop value
            """
            return float(self.instrument.query(f":CALC{self.n}:TRAN:TIME:STOP?"))

        # CALC:TRAN:TIME:STAT - Time domain transformation ON/OFF
        def enable_time_domain_transformation(self, enable: bool):
            """
            Enable or disable time domain transformation.

            Parameter:
                enable (bool): True to enable, False to disable

            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:TRAN:TIME:STAT {1 if enable else 0}")

        def is_time_domain_transformation_enabled(self) -> bool:
            """
            Query if time domain transformation is enabled.

            Parameter:
                None

            Return:
                bool: True if enabled, False otherwise
            """
            return bool(int(self.instrument.query(f":CALC{self.n}:TRAN:TIME:STAT?")))

        # CALC:TRAN:TIME:STEP:RTIM - Step rise time
        def set_time_domain_step_rise_time(self, value: float):
            """
            Set the step rise time for time domain.

            Parameter:
                value (float): Rise time

            Return:
                None
            """
            self.instrument.write(f":CALC{self.n}:TRAN:TIME:STEP:RTIM {value}")

        def get_time_domain_step_rise_time(self) -> float:
            """
            Get the step rise time for time domain.

            Parameter:
                None

            Return:
                float: Rise time
            """
            return float(self.instrument.query(f":CALC{self.n}:TRAN:TIME:STEP:RTIM?"))

        # CALC:TRAN:TIME:STIM - Selects Impulse/Step type
        def set_time_domain_stimulus_type(self, stim_type: str):
            """
            Set the stimulus type for time domain.

            Parameter:
                stim_type (str): 'IMP' for Impulse, 'STEP' for Step

            Return:
                None
            """
            allowed = ['IMP', 'STEP']
            if stim_type not in allowed:
                raise ValueError(f"stim_type must be one of {allowed}")
            self.instrument.write(f":CALC{self.n}:TRAN:TIME:STIM {stim_type}")

        def get_time_domain_stimulus_type(self) -> str:
            """
            Get the stimulus type for time domain.

            Parameter:
                None

            Return:
                str: Stimulus type
            """
            return self.instrument.query(f":CALC{self.n}:TRAN:TIME:STIM?").strip()

        # CALC:TRAN:TIME:UNIT - Time domain Unit
        def set_time_domain_unit(self, unit: str):
            """
            Set the time domain unit.

            Parameter:
                unit (str): 'SEC' for seconds, 'M' for meters

            Return:
                None
            """
            allowed = ['SEC', 'M']
            if unit not in allowed:
                raise ValueError(f"unit must be one of {allowed}")
            self.instrument.write(f":CALC{self.n}:TRAN:TIME:UNIT {unit}")

        def get_time_domain_unit(self) -> str:
            """
            Get the time domain unit.

            Parameter:
                None

            Return:
                str: Unit
            """
            return self.instrument.query(f":CALC{self.n}:TRAN:TIME:UNIT?").strip()
class Display:
    """
        Command display settings.
    """
    def __init__(self, instrument, data_handler):
        self.instrument = instrument
        self.data_handler = data_handler
        
        self.color = self.Color(self.instrument,self.data_handler)
        self.interface = self.Interface(self.instrument,self.data_handler)
        self.marker = self.Marker(self.instrument,self.data_handler)
    class Color:
        """
        Display color settings.
        """
        def __init__(self, instrument, data_handler):
            self.instrument = instrument
            self.data_handler = data_handler
        # DISP:COL:BACK - Background color
        def set_background(self, r: int, g: int, b: int):
            """
            Set the background color for trace display.

            Parameter:
            r (int): Red value (0-255)
            g (int): Green value (0-255)
            b (int): Blue value (0-255)

            Return:
            None
            """
            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))
            self.instrument.write(f":DISP:COL:BACK {r},{g},{b}")

        def get_background(self):
            """
            Get the background color for trace display.

            Parameter:
            None

            Return:
            tuple: (r, g, b)
            """
            data = self.instrument.query(":DISP:COL:BACK?").strip()
            return tuple(map(int, data.split(',')))

        # DISP:COL:GRAT - Grid and graticule label color
        def set_graticule(self, r: int, g: int, b: int):
            """
            Set the grid and graticule label color.

            Parameter:
            r (int): Red value (0-255)
            g (int): Green value (0-255)
            b (int): Blue value (0-255)

            Return:
            None
            """
            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))
            self.instrument.write(f":DISP:COL:GRAT {r},{g},{b}")

        def get_graticule(self):
            """
            Get the grid and graticule label color.

            Parameter:
            None

            Return:
            tuple: (r, g, b)
            """
            data = self.instrument.query(":DISP:COL:GRAT?").strip()
            return tuple(map(int, data.split(',')))

        # DISP:COL:TRAC:DATA - Data trace color
        def set_trace_data(self, trace: int, r: int, g: int, b: int):
            """
            Set the data trace color for a specific trace.

            Parameter:
            trace (int): Trace number (1-16)
            r (int): Red value (0-255)
            g (int): Green value (0-255)
            b (int): Blue value (0-255)

            Return:
            None
            """
            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))
            self.instrument.write(f":DISP:COL:TRAC{trace}:DATA {r},{g},{b}")

        def get_trace_data(self, trace: int):
            """
            Get the data trace color for a specific trace.

            Parameter:
            trace (int): Trace number (1-16)

            Return:
            tuple: (r, g, b)
            """
            data = self.instrument.query(f":DISP:COL:TRAC{trace}:DATA?").strip()
            return tuple(map(int, data.split(',')))

        # DISP:COL:TRAC:MEM - Memory trace color
        def set_trace_memory(self, trace: int, r: int, g: int, b: int):
            """
            Set the memory trace color for a specific trace.

            Parameter:
            trace (int): Trace number (1-16)
            r (int): Red value (0-255)
            g (int): Green value (0-255)
            b (int): Blue value (0-255)

            Return:
            None
            """
            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))
            self.instrument.write(f":DISP:COL:TRAC{trace}:MEM {r},{g},{b}")

        def get_trace_memory(self, trace: int):
            """
            Get the memory trace color for a specific trace.

            Parameter:
            trace (int): Trace number (1-16)

            Return:
            tuple: (r, g, b)
            """
            data = self.instrument.query(f":DISP:COL:TRAC{trace}:MEM?").strip()
            return tuple(map(int, data.split(',')))

        # DISP:COL:RES - Restore display settings to default
        def restore_defaults(self):
            """
            Restore the display settings to the default values.

            Parameter:
            None

            Return:
            None
            """
            self.instrument.write(":DISP:COL:RES")

    class Interface:
        """
        Display interface settings.
        """
        def __init__(self, instrument, data_handler):
            self.instrument = instrument
            self.data_handler = data_handler
        # DISP:FONT:SIZE - Font size for all elements
        def set_font_size(self, size: int):
            """
            Set the font size for all displayed elements.

            Parameter:
            size (int): Font size (10-22)

            Return:
            None
            """
            size = max(10, min(22, size))
            self.instrument.write(f":DISP:FONT:SIZE {size}")

        def get_font_size(self) -> int:
            """
            Get the font size for all displayed elements.

            Parameter:
            None

            Return:
            int: Font size
            """
            return int(self.instrument.query(":DISP:FONT:SIZE?"))

        # DISP:PART:FONT:SIZE - Font size of specified element
        def set_partition_font_size(self, item: str, size: int):
            """
            Set the font size of the specified display item.

            Parameter:
            item (str): Display item ('BUTT', 'MENU', 'CST', 'AST', 'CHAN')
            size (int): Font size (10-22)

            Return:
            None
            """
            allowed = ['BUTT', 'MENU', 'CST', 'AST', 'CHAN']
            if item not in allowed:
                raise ValueError(f"item must be one of {allowed}")
            size = max(10, min(22, size))
            self.instrument.write(f":DISP:PART:FONT:SIZE {item},{size}")

        def get_partition_font_size(self, item: str) -> int:
            """
            Get the font size of the specified display item.

            Parameter:
            item (str): Display item ('BUTT', 'MENU', 'CST', 'AST', 'CHAN')

            Return:
            int: Font size
            """
            allowed = ['BUTT', 'MENU', 'CST', 'AST', 'CHAN']
            if item not in allowed:
                raise ValueError(f"item must be one of {allowed}")
            return int(self.instrument.query(f":DISP:PART:FONT:SIZE? {item}"))

        # DISP:PART:FONT:SIZE:STATe - Individual font sizes ON/OFF
        def enable_individual_font_sizes(self, enable: bool):
            """
            Enable or disable individual font sizes for elements.

            Parameter:
            enable (bool): True for individual, False for same size

            Return:
            None
            """
            self.instrument.write(f":DISP:PART:FONT:SIZE:STAT {1 if enable else 0}")

        def is_individual_font_sizes_enabled(self) -> bool:
            """
            Query if individual font sizes for elements are enabled.

            Parameter:
            None

            Return:
            bool: True if enabled, False otherwise
            """
            return bool(int(self.instrument.query(":DISP:PART:FONT:SIZE:STAT?")))

        # DISP:PART:VIS - Show/hide display partition
        def set_partition_visible(self, partition: str, enable: bool):
            """
            Show or hide the specified display partition.

            Parameter:
            partition (str): Display partition ('BUTT', 'MENU', 'CST', 'AST', 'TIT', 'FLA', 'MTA')
            enable (bool): True to show, False to hide

            Return:
            None
            """
            allowed = ['BUTT', 'MENU', 'CST', 'AST', 'TIT', 'FLA', 'MTA']
            if partition not in allowed:
                raise ValueError(f"partition must be one of {allowed}")
            self.instrument.write(f":DISP:PART:VIS {partition},{1 if enable else 0}")

        def is_partition_visible(self, partition: str) -> bool:
            """
            Query if the specified display partition is visible.

            Parameter:
            partition (str): Display partition ('BUTT', 'MENU', 'CST', 'AST', 'TIT', 'FLA', 'MTA')

            Return:
            bool: True if visible, False otherwise
            """
            allowed = ['BUTT', 'MENU', 'CST', 'AST', 'TIT', 'FLA', 'MTA']
            if partition not in allowed:
                raise ValueError(f"partition must be one of {allowed}")
            return bool(int(self.instrument.query(f":DISP:PART:VIS? {partition}")))

    class Marker:
        """
        Display marker annotation settings.
        """
        def __init__(self, instrument, data_handler):
            self.instrument = instrument
            self.data_handler = data_handler
        # DISP:MARK:TABL - Marker table ON/OFF
        def enable_table(self, enable: bool):
            """
            Enable or disable the marker table.

            Parameter:
            enable (bool): True to enable, False to disable

            Return:
            None
            """
            self.instrument.write(f":DISP:MARK:TABL {1 if enable else 0}")

        def is_table_enabled(self) -> bool:
            """
            Query if the marker table is enabled.

            Parameter:
            None

            Return:
            bool: True if enabled, False otherwise
            """
            return bool(int(self.instrument.query(":DISP:MARK:TABL?")))

        # DISP:WIND:ANN:MARK:ALIG - Marker annotation alignment
        def set_annotation_alignment(self,  alignment: str):
            """
            Set the alignment of the marker annotation.

            Parameter:
            channel (int): Channel number (1-16)
            alignment (str): 'NONE', 'VERT', or 'HOR'

            Return:
            None
            """
            allowed = ['NONE', 'VERT', 'HOR']
            if alignment not in allowed:
                raise ValueError(f"alignment must be one of {allowed}")
            self.instrument.write(f":DISP:WIND{self.n}:ANN:MARK:ALIG {alignment}")

        def get_annotation_alignment(self, channel: int) -> str:
            """
            Get the alignment of the marker annotation.

            Parameter:
            channel (int): Channel number (1-16)

            Return:
            str: Alignment
            """
            return self.instrument.query(f":DISP:WIND{self.n}:ANN:MARK:ALIG?").strip()

        # DISP:WIND:ANN:MARK:SING - Active marker only ON/OFF
        def enable_active_only(self,  enable: bool):
            """
            Enable or disable display of only the active trace markers.

            Parameter:
            channel (int): Channel number (1-16)
            enable (bool): True for active only, False for all

            Return:
            None
            """
            self.instrument.write(f":DISP:WIND{self.n}:ANN:MARK:SING {1 if enable else 0}")

        def is_active_only_enabled(self, channel: int) -> bool:
            """
            Query if only the active trace markers are displayed.

            Parameter:
            channel (int): Channel number (1-16)

            Return:
            bool: True if active only, False otherwise
            """
            return bool(int(self.instrument.query(f":DISP:WIND{self.n}:ANN:MARK:SING?")))

        # DISP:WIND:TRAC:ANN:MARK:POS:X - Marker annotation X position
        def set_annotation_x(self,  trace: int, value: float):
            """
            Set the X position of marker annotation (percent of display width).

            Parameter:
            channel (int): Channel number (1-16)
            trace (int): Trace number (1-16)
            value (float): Position (0-100)

            Return:
            None
            """
            value = max(0, min(100, value))
            self.instrument.write(f":DISP:WIND{self.n}:TRAC{trace}:ANN:MARK:POS:X {value}")

        def get_annotation_x(self,  trace: int) -> float:
            """
            Get the X position of marker annotation.

            Parameter:
            channel (int): Channel number (1-16)
            trace (int): Trace number (1-16)

            Return:
            float: Position (0-100)
            """
            return float(self.instrument.query(f":DISP:WIND{self.n}:TRAC{trace}:ANN:MARK:POS:X?"))

        # DISP:WIND:TRAC:ANN:MARK:POS:Y - Marker annotation Y position
        def set_annotation_y(self,  trace: int, value: float):
            """
            Set the Y position of marker annotation (percent of display height).

            Parameter:
            channel (int): Channel number (1-16)
            trace (int): Trace number (1-16)
            value (float): Position (0-100)

            Return:
            None
            """
            value = max(0, min(100, value))
            self.instrument.write(f":DISP:WIND{self.n}:TRAC{trace}:ANN:MARK:POS:Y {value}")

        def get_annotation_y(self,  trace: int) -> float:
            """
            Get the Y position of marker annotation.

            Parameter:
            channel (int): Channel number (1-16)
            trace (int): Trace number (1-16)

            Return:
            float: Position (0-100)
            """
            return float(self.instrument.query(f":DISP:WIND{self.n}:TRAC{trace}:ANN:MARK:POS:Y?"))
    def set_background_color(self, r: int, g: int, b: int):
        """
        Set the background color for trace display.

        Parameter:
        r (int): Red value (0-255)
        g (int): Green value (0-255)
        b (int): Blue value (0-255)

        Return:
        None
        """
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))
        self.instrument.write(f":DISP:COL:BACK {r},{g},{b}")

    def get_background_color(self):
        """
        Get the background color for trace display.

        Parameter:
        None

        Return:
        tuple: (r, g, b)
        """
        data = self.instrument.query(":DISP:COL:BACK?").strip()
        return tuple(map(int, data.split(',')))

    # DISP:COL:GRAT - Grid and graticule label color
    def set_graticule_color(self, r: int, g: int, b: int):
        """
        Set the grid and graticule label color.

        Parameter:
        r (int): Red value (0-255)
        g (int): Green value (0-255)
        b (int): Blue value (0-255)

        Return:
        None
        """
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))
        self.instrument.write(f":DISP:COL:GRAT {r},{g},{b}")

    def get_graticule_color(self):
        """
        Get the grid and graticule label color.

        Parameter:
        None

        Return:
        tuple: (r, g, b)
        """
        data = self.instrument.query(":DISP:COL:GRAT?").strip()
        return tuple(map(int, data.split(',')))

    # DISP:COL:RES - Restore display settings to default
    def restore_display_defaults(self):
        """
        Restore the display settings to the default values.

        Parameter:
        None

        Return:
        None
        """
        self.instrument.write(":DISP:COL:RES")

    # DISP:COL:TRAC:DATA - Data trace color
    def set_data_trace_color(self, trace: int, r: int, g: int, b: int):
        """
        Set the data trace color for a specific trace.

        Parameter:
        trace (int): Trace number (1-16)
        r (int): Red value (0-255)
        g (int): Green value (0-255)
        b (int): Blue value (0-255)

        Return:
        None
        """
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))
        self.instrument.write(f":DISP:COL:TRAC{trace}:DATA {r},{g},{b}")

    def get_data_trace_color(self, trace: int):
        """
        Get the data trace color for a specific trace.

        Parameter:
        trace (int): Trace number (1-16)

        Return:
        tuple: (r, g, b)
        """
        data = self.instrument.query(f":DISP:COL:TRAC{trace}:DATA?").strip()
        return tuple(map(int, data.split(',')))

    # DISP:COL:TRAC:MEM - Memory trace color
    def set_memory_trace_color(self, trace: int, r: int, g: int, b: int):
        """
        Set the memory trace color for a specific trace.

        Parameter:
        trace (int): Trace number (1-16)
        r (int): Red value (0-255)
        g (int): Green value (0-255)
        b (int): Blue value (0-255)

        Return:
        None
        """
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))
        self.instrument.write(f":DISP:COL:TRAC{trace}:MEM {r},{g},{b}")

    def get_memory_trace_color(self, trace: int):
        """
        Get the memory trace color for a specific trace.

        Parameter:
        trace (int): Trace number (1-16)

        Return:
        tuple: (r, g, b)
        """
        data = self.instrument.query(f":DISP:COL:TRAC{trace}:MEM?").strip()
        return tuple(map(int, data.split(',')))

    # DISP:ENAB - Display update ON/OFF
    def enable_display_update(self, enable: bool):
        """
        Enable or disable display update.

        Parameter:
        enable (bool): True to enable, False to disable

        Return:
        None
        """
        self.instrument.write(f":DISP:ENAB {1 if enable else 0}")

    def is_display_update_enabled(self) -> bool:
        """
        Query if display update is enabled.

        Parameter:
        None

        Return:
        bool: True if enabled, False otherwise
        """
        return bool(int(self.instrument.query(":DISP:ENAB?")))

    # DISP:FONT:SIZE - Font size for all elements
    def set_font_size(self, size: int):
        """
        Set the font size for all displayed elements.

        Parameter:
        size (int): Font size (10-22)

        Return:
        None
        """
        size = max(10, min(22, size))
        self.instrument.write(f":DISP:FONT:SIZE {size}")

    def get_font_size(self) -> int:
        """
        Get the font size for all displayed elements.

        Parameter:
        None

        Return:
        int: Font size
        """
        return int(self.instrument.query(":DISP:FONT:SIZE?"))

    # DISP:FSIG - "Fail" sign display ON/OFF
    def enable_fail_sign(self, enable: bool):
        """
        Enable or disable the "Fail" sign display.

        Parameter:
        enable (bool): True to enable, False to disable

        Return:
        None
        """
        self.instrument.write(f":DISP:FSIG {1 if enable else 0}")

    def is_fail_sign_enabled(self) -> bool:
        """
        Query if the "Fail" sign display is enabled.

        Parameter:
        None

        Return:
        bool: True if enabled, False otherwise
        """
        return bool(int(self.instrument.query(":DISP:FSIG?")))

    # DISP:GLAB - Graticule Label state
    def set_graticule_label_state(self, state: str):
        """
        Set the Graticule Label state.

        Parameter:
        state (str): 'OFF', 'ACT', or 'ALL'

        Return:
        None
        """
        allowed = ['OFF', 'ACT', 'ALL']
        if state not in allowed:
            raise ValueError(f"state must be one of {allowed}")
        self.instrument.write(f":DISP:GLAB {state}")

    def get_graticule_label_state(self) -> str:
        """
        Get the Graticule Label state.

        Parameter:
        None

        Return:
        str: Graticule Label state
        """
        return self.instrument.query(":DISP:GLAB?").strip()

    # DISP:IMAG - Inversion of display colors
    def set_display_inversion(self, mode: str):
        """
        Set the inversion of display colors of the trace area.

        Parameter:
        mode (str): 'NORM' for normal, 'INV' for inverted

        Return:
        None
        """
        allowed = ['NORM', 'INV']
        if mode not in allowed:
            raise ValueError(f"mode must be one of {allowed}")
        self.instrument.write(f":DISP:IMAG {mode}")

    def get_display_inversion(self) -> str:
        """
        Get the inversion mode of display colors.

        Parameter:
        None

        Return:
        str: Inversion mode
        """
        return self.instrument.query(":DISP:IMAG?").strip()

    # DISP:HIDE - Hide Analyzer window
    def hide_analyzer_window(self):
        """
        Hide the Analyzer window (shows "Remote Control" label).

        Parameter:
        None

        Return:
        None
        """
        self.instrument.write(":DISP:HIDE")

    # DISP:MARK:TABL - Marker table ON/OFF
    def enable_marker_table(self, enable: bool):
        """
        Enable or disable the marker table.

        Parameter:
        enable (bool): True to enable, False to disable

        Return:
        None
        """
        self.instrument.write(f":DISP:MARK:TABL {1 if enable else 0}")

    def is_marker_table_enabled(self) -> bool:
        """
        Query if the marker table is enabled.

        Parameter:
        None

        Return:
        bool: True if enabled, False otherwise
        """
        return bool(int(self.instrument.query(":DISP:MARK:TABL?")))

    # DISP:MAX - Maximization of the active channel window ON/OFF
    def enable_channel_maximization(self, enable: bool):
        """
        Enable or disable maximization of the active channel window.

        Parameter:
        enable (bool): True to enable, False to disable

        Return:
        None
        """
        self.instrument.write(f":DISP:MAX {1 if enable else 0}")

    def is_channel_maximization_enabled(self) -> bool:
        """
        Query if maximization of the active channel window is enabled.

        Parameter:
        None

        Return:
        bool: True if enabled, False otherwise
        """
        return bool(int(self.instrument.query(":DISP:MAX?")))

    # DISP:PART:FONT:SIZE - Font size of specified element
    def set_partition_font_size(self, item: str, size: int):
        """
        Set the font size of the specified display item.

        Parameter:
        item (str): Display item ('BUTT', 'MENU', 'CST', 'AST', 'CHAN')
        size (int): Font size (10-22)

        Return:
        None
        """
        allowed = ['BUTT', 'MENU', 'CST', 'AST', 'CHAN']
        if item not in allowed:
            raise ValueError(f"item must be one of {allowed}")
        size = max(10, min(22, size))
        self.instrument.write(f":DISP:PART:FONT:SIZE {item},{size}")

    def get_partition_font_size(self, item: str) -> int:
        """
        Get the font size of the specified display item.

        Parameter:
        item (str): Display item ('BUTT', 'MENU', 'CST', 'AST', 'CHAN')

        Return:
        int: Font size
        """
        allowed = ['BUTT', 'MENU', 'CST', 'AST', 'CHAN']
        if item not in allowed:
            raise ValueError(f"item must be one of {allowed}")
        return int(self.instrument.query(f":DISP:PART:FONT:SIZE? {item}"))

    # DISP:PART:FONT:SIZE:STATe - Individual font sizes ON/OFF
    def enable_individual_font_sizes(self, enable: bool):
        """
        Enable or disable individual font sizes for elements.

        Parameter:
        enable (bool): True for individual, False for same size

        Return:
        None
        """
        self.instrument.write(f":DISP:PART:FONT:SIZE:STAT {1 if enable else 0}")

    def is_individual_font_sizes_enabled(self) -> bool:
        """
        Query if individual font sizes for elements are enabled.

        Parameter:
        None

        Return:
        bool: True if enabled, False otherwise
        """
        return bool(int(self.instrument.query(":DISP:PART:FONT:SIZE:STAT?")))

    # DISP:PART:VIS - Show/hide display partition
    def set_partition_visible(self, partition: str, enable: bool):
        """
        Show or hide the specified display partition.

        Parameter:
        partition (str): Display partition ('BUTT', 'MENU', 'CST', 'AST', 'TIT', 'FLA', 'MTA')
        enable (bool): True to show, False to hide

        Return:
        None
        """
        allowed = ['BUTT', 'MENU', 'CST', 'AST', 'TIT', 'FLA', 'MTA']
        if partition not in allowed:
            raise ValueError(f"partition must be one of {allowed}")
        self.instrument.write(f":DISP:PART:VIS {partition},{1 if enable else 0}")

    def is_partition_visible(self, partition: str) -> bool:
        """
        Query if the specified display partition is visible.

        Parameter:
        partition (str): Display partition ('BUTT', 'MENU', 'CST', 'AST', 'TIT', 'FLA', 'MTA')

        Return:
        bool: True if visible, False otherwise
        """
        allowed = ['BUTT', 'MENU', 'CST', 'AST', 'TIT', 'FLA', 'MTA']
        if partition not in allowed:
            raise ValueError(f"partition must be one of {allowed}")
        return bool(int(self.instrument.query(f":DISP:PART:VIS? {partition}")))

    # DISP:POS - Analyzer window position and size
    def set_window_position(self, left: int, top: int, width: int, height: int):
        """
        Set the Analyzer window position and size.

        Parameter:
        left (int): Left coordinate
        top (int): Top coordinate
        width (int): Window width
        height (int): Window height

        Return:
        None
        """
        self.instrument.write(f":DISP:POS {left},{top},{width},{height}")

    def get_window_position(self):
        """
        Get the Analyzer window position and size.

        Parameter:
        None

        Return:
        tuple: (left, top, width, height)
        """
        data = self.instrument.query(":DISP:POS?").strip()
        return tuple(map(int, data.split(',')))

    # DISP:SHOW - Show Analyzer window
    def show_analyzer_window(self):
        """
        Show the Analyzer window hidden by DISP:HIDE.

        Parameter:
        None

        Return:
        None
        """
        self.instrument.write(":DISP:SHOW")

    # DISP:SPL - Number and layout of channels
    def set_channel_layout(self, layout_code: int):
        """
        Set the number and layout of channels on the screen.

        Parameter:
        layout_code (int): Layout code (1-16)

        Return:
        None
        """
        layout_code = max(1, min(16, layout_code))
        self.instrument.write(f":DISP:SPL {layout_code}")

    def get_channel_layout(self) -> int:
        """
        Get the number and layout of channels on the screen.

        Parameter:
        None

        Return:
        int: Layout code
        """
        return int(self.instrument.query(":DISP:SPL?"))

    # DISP:UPD - One-time display update
    def update_display_once(self):
        """
        Update the display once when display update is OFF.

        Parameter:
        None

        Return:
        None
        """
        self.instrument.write(":DISP:UPD")

    # DISP:WIND:ACT - Set active channel
    def set_active_channel(self, channel: int):
        """
        Set the active channel.

        Parameter:
        channel (int): Channel number (1-16)

        Return:
        None
        """
        self.instrument.write(f":DISP:WIND{self.n}:ACT")

    # DISP:WIND:ANN:MARK:ALIG - Marker annotation alignment
    def set_marker_annotation_alignment(self,  alignment: str):
        """
        Set the alignment of the marker annotation.

        Parameter:
        channel (int): Channel number (1-16)
        alignment (str): 'NONE', 'VERT', or 'HOR'

        Return:
        None
        """
        allowed = ['NONE', 'VERT', 'HOR']
        if alignment not in allowed:
            raise ValueError(f"alignment must be one of {allowed}")
        self.instrument.write(f":DISP:WIND{self.n}:ANN:MARK:ALIG {alignment}")

    def get_marker_annotation_alignment(self, channel: int) -> str:
        """
        Get the alignment of the marker annotation.

        Parameter:
        channel (int): Channel number (1-16)

        Return:
        str: Alignment
        """
        return self.instrument.query(f":DISP:WIND{self.n}:ANN:MARK:ALIG?").strip()

    # DISP:WIND:ANN:MARK:SING - Active marker only ON/OFF
    def enable_active_marker_only(self,  enable: bool):
        """
        Enable or disable display of only the active trace markers.

        Parameter:
        channel (int): Channel number (1-16)
        enable (bool): True for active only, False for all

        Return:
        None
        """
        self.instrument.write(f":DISP:WIND{self.n}:ANN:MARK:SING {1 if enable else 0}")

    def is_active_marker_only_enabled(self, channel: int) -> bool:
        """
        Query if only the active trace markers are displayed.

        Parameter:
        channel (int): Channel number (1-16)

        Return:
        bool: True if active only, False otherwise
        """
        return bool(int(self.instrument.query(f":DISP:WIND{self.n}:ANN:MARK:SING?")))

    # DISP:WIND:MAX - Maximize trace in channel ON/OFF
    def enable_trace_maximization(self,  enable: bool):
        """
        Enable or disable maximization of the active trace in the specified channel.

        Parameter:
        channel (int): Channel number (1-16)
        enable (bool): True to enable, False to disable

        Return:
        None
        """
        self.instrument.write(f":DISP:WIND{self.n}:MAX {1 if enable else 0}")

    def is_trace_maximization_enabled(self, channel: int) -> bool:
        """
        Query if maximization of the active trace in the specified channel is enabled.

        Parameter:
        channel (int): Channel number (1-16)

        Return:
        bool: True if enabled, False otherwise
        """
        return bool(int(self.instrument.query(f":DISP:WIND{self.n}:MAX?")))

    # DISP:WIND:SPL - Graph layout in channel window
    def set_channel_graph_layout(self,  layout: int):
        """
        Set the graph layout in the channel window.

        Parameter:
        channel (int): Channel number (1-16)
        layout (int): Layout code (1-16)

        Return:
        None
        """
        layout = max(1, min(16, layout))
        self.instrument.write(f":DISP:WIND{self.n}:SPL {layout}")

    def get_channel_graph_layout(self, channel: int) -> int:
        """
        Get the graph layout in the channel window.

        Parameter:
        channel (int): Channel number (1-16)

        Return:
        int: Layout code
        """
        return int(self.instrument.query(f":DISP:WIND{self.n}:SPL?"))

    # DISP:WIND:TITL - Channel title display ON/OFF
    def enable_channel_title(self,  enable: bool):
        """
        Enable or disable the channel title display.

        Parameter:
        channel (int): Channel number (1-16)
        enable (bool): True to enable, False to disable

        Return:
        None
        """
        self.instrument.write(f":DISP:WIND{self.n}:TITL {1 if enable else 0}")

    def is_channel_title_enabled(self, channel: int) -> bool:
        """
        Query if the channel title display is enabled.

        Parameter:
        channel (int): Channel number (1-16)

        Return:
        bool: True if enabled, False otherwise
        """
        return bool(int(self.instrument.query(f":DISP:WIND{self.n}:TITL?")))

    # DISP:WIND:TITL:DATA - Channel title label
    def set_channel_title_label(self,  label: str):
        """
        Set the channel title label.

        Parameter:
        channel (int): Channel number (1-16)
        label (str): Title label (up to 256 characters)

        Return:
        None
        """
        self.instrument.write(f":DISP:WIND{self.n}:TITL:DATA \"{label}\"")

    def get_channel_title_label(self, channel: int) -> str:
        """
        Get the channel title label.

        Parameter:
        channel (int): Channel number (1-16)

        Return:
        str: Title label
        """
        return self.instrument.query(f":DISP:WIND{self.n}:TITL:DATA?").strip()

    # DISP:WIND:TRAC:ANN:MARK:POS:X - Marker annotation X position
    def set_marker_annotation_x(self,  trace: int, value: float):
        """
        Set the X position of marker annotation (percent of display width).

        Parameter:
        channel (int): Channel number (1-16)
        trace (int): Trace number (1-16)
        value (float): Position (0-100)

        Return:
        None
        """
        value = max(0, min(100, value))
        self.instrument.write(f":DISP:WIND{self.n}:TRAC{trace}:ANN:MARK:POS:X {value}")

    def get_marker_annotation_x(self,  trace: int) -> float:
        """
        Get the X position of marker annotation.

        Parameter:
        channel (int): Channel number (1-16)
        trace (int): Trace number (1-16)

        Return:
        float: Position (0-100)
        """
        return float(self.instrument.query(f":DISP:WIND{self.n}:TRAC{trace}:ANN:MARK:POS:X?"))

    # DISP:WIND:TRAC:ANN:MARK:POS:Y - Marker annotation Y position
    def set_marker_annotation_y(self,  trace: int, value: float):
        """
        Set the Y position of marker annotation (percent of display height).

        Parameter:
        channel (int): Channel number (1-16)
        trace (int): Trace number (1-16)
        value (float): Position (0-100)

        Return:
        None
        """
        value = max(0, min(100, value))
        self.instrument.write(f":DISP:WIND{self.n}:TRAC{trace}:ANN:MARK:POS:Y {value}")

    def get_marker_annotation_y(self,  trace: int) -> float:
        """
        Get the Y position of marker annotation.

        Parameter:
        channel (int): Channel number (1-16)
        trace (int): Trace number (1-16)

        Return:
        float: Position (0-100)
        """
        return float(self.instrument.query(f":DISP:WIND{self.n}:TRAC{trace}:ANN:MARK:POS:Y?"))
    # DISP:SPL - Number and layout of channels
    def set_number_and_layout_of_channels(self, layout_code: int):
        """
        Set the number and layout of channels on the screen.

        Parameter:
        layout_code (int): Layout code (1-16)

        Return:
        None
        """
        layout_code = max(1, min(16, layout_code))
        self.instrument.write(f":DISP:SPL {layout_code}")

    def get_number_and_layout_of_channels(self) -> int:
        """
        Get the number and layout of channels on the screen.

        Parameter:
        None

        Return:
        int: Layout code
        """
        return int(self.instrument.query(":DISP:SPL?"))

    # DISP:WIND:TRAC:MEM[:STATe] - Memory trace display ON/OFF
    def enable_memory_trace_display(self,  trace: int, enable: bool):
        """
        Enable or disable the memory trace display for a trace.

        Parameter:
        channel (int): Channel number (1-16)
        trace (int): Trace number (1-16)
        enable (bool): True to enable, False to disable

        Return:
        None
        """
        self.instrument.write(f":DISP:WIND{self.n}:TRAC{trace}:MEM:STAT {1 if enable else 0}")

    def is_memory_trace_display_enabled(self,  trace: int) -> bool:
        """
        Query if the memory trace display is enabled for a trace.

        Parameter:
        channel (int): Channel number (1-16)
        trace (int): Trace number (1-16)

        Return:
        bool: True if enabled, False otherwise
        """
        return bool(int(self.instrument.query(f":DISP:WIND{self.n}:TRAC{trace}:MEM:STAT?")))

    # DISP:WIND:TRAC:STATe - Data trace display ON/OFF
    def enable_data_trace_display(self,  trace: int, enable: bool):
        """
        Enable or disable the data trace display for a trace.

        Parameter:
        channel (int): Channel number (1-16)
        trace (int): Trace number (1-16)
        enable (bool): True to enable, False to disable

        Return:
        None
        """
        self.instrument.write(f":DISP:WIND{self.n}:TRAC{trace}:STAT {1 if enable else 0}")

    def is_data_trace_display_enabled(self,  trace: int) -> bool:
        """
        Query if the data trace display is enabled for a trace.

        Parameter:
        channel (int): Channel number (1-16)
        trace (int): Trace number (1-16)

        Return:
        bool: True if enabled, False otherwise
        """
        return bool(int(self.instrument.query(f":DISP:WIND{self.n}:TRAC{trace}:STAT?")))

    # DISP:WIND:TRAC:Y:SCALe:AUTO - Auto scale function for the trace
    def auto_scale_trace(self,  trace: int):
        """
        Execute the auto scale function for the trace.

        Parameter:
        channel (int): Channel number (1-16)
        trace (int): Trace number (1-16)

        Return:
        None
        """
        self.instrument.write(f":DISP:WIND{self.n}:TRAC{trace}:Y:SCAL:AUTO")

    # DISP:WIND:TRAC:Y:SCALe:PDIVision - Set/read trace scale per division
    def set_trace_scale_per_division(self,  trace: int, value: float):
        """
        Set the trace scale per division.

        Parameter:
        channel (int): Channel number (1-16)
        trace (int): Trace number (1-16)
        value (float): Scale value (10e-18 to 1e18)

        Return:
        None
        """
        self.instrument.write(f":DISP:WIND{self.n}:TRAC{trace}:Y:SCAL:PDIV {value}")

    def get_trace_scale_per_division(self,  trace: int) -> float:
        """
        Get the trace scale per division.

        Parameter:
        channel (int): Channel number (1-16)
        trace (int): Trace number (1-16)

        Return:
        float: Scale value
        """
        return float(self.instrument.query(f":DISP:WIND{self.n}:TRAC{trace}:Y:SCAL:PDIV?"))

    # DISP:WIND:TRAC:Y:SCALe:RLEVel - Set/read reference line value
    def set_reference_line_value(self,  trace: int, value: float):
        """
        Set the value of the reference line.

        Parameter:
        channel (int): Channel number (1-16)
        trace (int): Trace number (1-16)
        value (float): Reference line value (10e-18 to 1e18)

        Return:
        None
        """
        self.instrument.write(f":DISP:WIND{self.n}:TRAC{trace}:Y:SCAL:RLEV {value}")

    def get_reference_line_value(self,  trace: int) -> float:
        """
        Get the value of the reference line.

        Parameter:
        channel (int): Channel number (1-16)
        trace (int): Trace number (1-16)

        Return:
        float: Reference line value
        """
        return float(self.instrument.query(f":DISP:WIND{self.n}:TRAC{trace}:Y:SCAL:RLEV?"))

    # DISP:WIND:TRAC:Y:SCALe:RLEVel:AUTO - Auto reference function for the trace
    def auto_reference_line(self,  trace: int):
        """
        Execute the auto reference function for the trace.

        Parameter:
        channel (int): Channel number (1-16)
        trace (int): Trace number (1-16)

        Return:
        None
        """
        self.instrument.write(f":DISP:WIND{self.n}:TRAC{trace}:Y:SCAL:RLEV:AUTO")

    # DISP:WIND:TRAC:Y:SCALe:RPOSition - Set/read reference line position
    def set_reference_line_position(self,  trace: int, value: float):
        """
        Set the position of the reference line.

        Parameter:
        channel (int): Channel number (1-16)
        trace (int): Trace number (1-16)
        value (float): Reference line position (0 to number of scale divisions)

        Return:
        None
        """
        self.instrument.write(f":DISP:WIND{self.n}:TRAC{trace}:Y:SCAL:RPOS {value}")

    def get_reference_line_position(self,  trace: int) -> float:
        """
        Get the position of the reference line.

        Parameter:
        channel (int): Channel number (1-16)
        trace (int): Trace number (1-16)

        Return:
        float: Reference line position
        """
        return float(self.instrument.query(f":DISP:WIND{self.n}:TRAC{trace}:Y:SCAL:RPOS?"))

    # DISP:WIND:X:SPACing - Set/read display method of horizontal axis for segment sweep
    def set_x_axis_spacing(self,  spacing: str):
        """
        Set the display method of the graph horizontal axis for the segment sweep.

        Parameter:
        channel (int): Channel number (1-16)
        spacing (str): 'LIN' or 'OBAS'

        Return:
        None
        """
        allowed = ['LIN', 'OBAS']
        if spacing not in allowed:
            raise ValueError(f"spacing must be one of {allowed}")
        self.instrument.write(f":DISP:WIND{self.n}:X:SPAC {spacing}")

    def get_x_axis_spacing(self, channel: int) -> str:
        """
        Get the display method of the graph horizontal axis for the segment sweep.

        Parameter:
        channel (int): Channel number (1-16)

        Return:
        str: Spacing method
        """
        return self.instrument.query(f":DISP:WIND{self.n}:X:SPAC?").strip()

    # DISP:WIND:Y:SCALe:DIVisions - Set/read number of vertical scale divisions
    def set_vertical_scale_divisions(self,  value: int):
        """
        Set the number of the vertical scale divisions.

        Parameter:
        channel (int): Channel number (1-16)
        value (int): Number of divisions (4-30)

        Return:
        None
        """
        value = max(4, min(30, value))
        self.instrument.write(f":DISP:WIND{self.n}:Y:SCAL:DIV {value}")

    def get_vertical_scale_divisions(self, channel: int) -> int:
        """
        Get the number of the vertical scale divisions.

        Parameter:
        channel (int): Channel number (1-16)

        Return:
        int: Number of divisions
        """
        return int(self.instrument.query(f":DISP:WIND{self.n}:Y:SCAL:DIV?"))

    # DISP:WIND:TRAC:ANN:MARK:POS:Y - Marker annotation Y position (already implemented above)
class Format:
    """
        Command format settings.
    """
    def __init__(self, instrument, data_handler):
        self.instrument = instrument
        self.data_handler = data_handler
    # FORM:BORDer - Set/read byte order for binary data transfer
    def set_byte_order(self, order: str):
        """
        Set the transfer order of each byte in binary data transfer format.

        Parameter:
            order (str): Byte order, one of ['NORM', 'SWAP']

        Return:
            None
        """
        allowed = ['NORM', 'SWAP']
        if order not in allowed:
            raise ValueError(f"order must be one of {allowed}")
        self.instrument.write(f":FORM:BORD {order}")

    def get_byte_order(self) -> str:
        """
        Get the transfer order of each byte in binary data transfer format.

        Parameter:
            None

        Return:
            str: Byte order ('NORM' or 'SWAP')
        """
        return self.instrument.query(":FORM:BORD?").strip()

    # FORM:DATA - Set/read data transfer format
    def set_data_format(self, fmt: str):
        """
        Set the data transfer format for binary or ASCII data.

        Parameter:
            fmt (str): Data format, one of ['ASC', 'REAL', 'REAL32']

        Return:
            None
        """
        allowed = ['ASC', 'REAL', 'REAL32']
        if fmt not in allowed:
            raise ValueError(f"fmt must be one of {allowed}")
        self.instrument.write(f":FORM:DATA {fmt}")

    def get_data_format(self) -> str:
        """
        Get the data transfer format for binary or ASCII data.

        Parameter:
            None

        Return:
            str: Data format ('ASC', 'REAL', or 'REAL32')
        """
        return self.instrument.query(":FORM:DATA?").strip()

    # FORM:PUSH - Save current format and byte order, set new values
    def push_format(self, fmt: str, border: str):
        """
        Save current settings and set new values for data transfer format and byte order.

        Parameter:
            fmt (str): Data format, one of ['ASC', 'REAL', 'REAL32']
            border (str): Byte order, one of ['NORM', 'SWAP']

        Return:
            None
        """
        allowed_fmt = ['ASC', 'REAL', 'REAL32']
        allowed_border = ['NORM', 'SWAP']
        if fmt not in allowed_fmt:
            raise ValueError(f"fmt must be one of {allowed_fmt}")
        if border not in allowed_border:
            raise ValueError(f"border must be one of {allowed_border}")
        self.instrument.write(f":FORM:PUSH {fmt},{border}")

    # FORM:POP - Restore format and byte order from last FORM:PUSH
    def pop_format(self):
        """
        Restore the settings for the data transfer format and byte order saved by the preceding FORM:PUSH command.

        Parameter:
            None

        Return:
            None
        """
        self.instrument.write(":FORM:POP")

class HCopy:
    """ Hardcopy printing commands. Only use if connected to printer."""
    def __init__(self, instrument, data_handler):
        self.instrument = instrument
        self.data_handler = data_handler
    # HCOPy[:IMMediate] - Print out the image displayed on the screen
    def print_image(self):
        """
        Print out the image displayed on the screen without previewing.

        Parameter:
        None

        Return:
        None
        """
        self.instrument.write(":HCOPy:IMMediate")

    # HCOPy:ABORt - Abort the printout
    def abort_printout(self):
        """
        Abort the printout.

        Parameter:
        None

        Return:
        None
        """
        self.instrument.write(":HCOPy:ABORt")

    # HCOPy:DATE:STAMp - Date and time stamp ON/OFF
    def enable_date_stamp(self, enable: bool):
        """
        Enable or disable the date and time printout in the upper right corner of the image.

        Parameter:
        enable (bool): True to enable, False to disable

        Return:
        None
        """
        self.instrument.write(f":HCOPy:DATE:STAMp {1 if enable else 0}")

    def is_date_stamp_enabled(self) -> bool:
        """
        Query if the date and time printout is enabled.

        Parameter:
        None

        Return:
        bool: True if enabled, False otherwise
        """
        return bool(int(self.instrument.query(":HCOPy:DATE:STAMp?")))

    # HCOPy:IMAGe - Inverted color image printout
    def set_image_inversion(self, mode: str):
        """
        Set the inverted color image printout.

        Parameter:
        mode (str): 'NORM' for normal, 'INV' for inverted

        Return:
        None
        """
        allowed = ['NORM', 'INV']
        if mode not in allowed:
            raise ValueError(f"mode must be one of {allowed}")
        self.instrument.write(f":HCOPy:IMAGe {mode}")

    def get_image_inversion(self) -> str:
        """
        Get the inverted color image printout mode.

        Parameter:
        None

        Return:
        str: 'NORM' or 'INV'
        """
        return self.instrument.query(":HCOPy:IMAGe?").strip()

    # HCOPy:PAINt - Color chart for image printout
    def set_paint_mode(self, mode: str):
        """
        Set the color chart for the image printout.

        Parameter:
        mode (str): 'COL' for color, 'GRAY' for grayscale, 'BW' for black & white

        Return:
        None
        """
        allowed = ['COL', 'GRAY', 'BW']
        if mode not in allowed:
            raise ValueError(f"mode must be one of {allowed}")
        self.instrument.write(f":HCOPy:PAINt {mode}")

    def get_paint_mode(self) -> str:
        """
        Get the color chart mode for the image printout.

        Parameter:
        None

        Return:
        str: 'COL', 'GRAY', or 'BW'
        """
        return self.instrument.query(":HCOPy:PAINt?").strip()
class Initate:

    """ Commands Channel initiation mode."""
    def __init__(self, instrument, data_handler, channel):
        self.instrument = instrument
        self.data_handler = data_handler
        self.n = channel
    # INITiate<Ch>[:IMMediate] - Initiate channel once (trigger)
    def initiate(self):
        """
        Put the channel into the Trigger Waiting state for one trigger event.

        Parameter:
        None

        Return:
        None
        """
        self.instrument.write(f":INITiate{self.n}:IMMediate")

    # INITiate<Ch>:CONTinuous - Continuous channel initiation mode ON/OFF
    def enable_continuous(self, enable: bool):
        """
        Enable or disable continuous trigger initiation mode for the channel.

        Parameter:
        enable (bool): True to enable, False to disable

        Return:
        None
        """
        self.instrument.write(f":INITiate{self.n}:CONTinuous {1 if enable else 0}")

    def is_continuous_enabled(self) -> bool:
        """
        Query if continuous trigger initiation mode is enabled for the channel.

        Parameter:
        None

        Return:
        bool: True if enabled, False otherwise
        """
        return bool(int(self.instrument.query(f":INITiate{self.n}:CONTinuous?")))

    # INITiate:CONTinuous:ALL - Continuous channel initiation mode for all channels ON/OFF
    @staticmethod
    def enable_continuous_all(instrument, enable: bool):
        """
        Enable or disable continuous trigger initiation mode for all channels.

        Parameter:
        instrument: Instrument instance
        enable (bool): True to enable, False to disable

        Return:
        None
        """
        instrument.write(f":INITiate:CONTinuous:ALL {1 if enable else 0}")
class MMemory:
    """
        File saving and manipulation operations commands.
    """
    def __init__(self, instrument, data_handler):
        self.instrument = instrument
        self.data_handler = data_handler
        
        self.catalog = self.Catalog(self.instrument, data_handler)
        self.copy = self.Copy(self.instrument, data_handler)
        self.delete = self.Delete(self.instrument, data_handler)
        self.directory = self.Directory(self.instrument, data_handler)
        self.load = self.Load(self.instrument, data_handler)
        self.store = self.Store(self.instrument, data_handler)
        
    class Catalog:
        """
        Commands for reading out information about the hard drive and files.
        """
        def __init__(self, instrument, data_handler):
            self.instrument = instrument
            self.data_handler = data_handler
        # MMEMory:CATalog? <string>
        def get_catalog(self, directory: str = "\\."):
            """
            Read out information about the hard drive and files in the specified directory.

            Parameter:
                directory (str): Directory name (default: "\\.")

            Return:
                str: Catalog information string
            """
            return self.instrument.query(f":MMEMory:CATalog? \"{directory}\"").strip()

    class Copy:
        """
        Commands for copying files.
        """
        def __init__(self, instrument, data_handler):
            self.instrument = instrument
            self.data_handler = data_handler
        # MMEMory:COPY <string1>,<string2>
        def copy_file(self, src: str, dst: str):
            """
            Copy a file from source to destination.

            Parameter:
                src (str): Source file name
                dst (str): Destination file name

            Return:
                None
            """
            self.instrument.write(f":MMEMory:COPY \"{src}\",\"{dst}\"")

    class Delete:
        """
        File delete operations.
        """
        def __init__(self, instrument, data_handler):
            self.instrument = instrument
            self.data_handler = data_handler
        # MMEMory:DELete <string>
        def delete_file(self, filename: str):
            """
            Delete a file.

            Parameter:
                filename (str): File name

            Return:
                None
            """
            self.instrument.write(f":MMEMory:DELete \"{filename}\"")

    class Directory:
        """
        Directory operations.
        """
        def __init__(self, instrument, data_handler):
            self.instrument = instrument
            self.data_handler = data_handler
        # MMEMory:MDIRectory <string>
        def create_directory(self, path: str):
            """
            Create a new directory.

            Parameter:
                path (str): Directory full name

            Return:
                None
            """
            self.instrument.write(f":MMEMory:MDIRectory \"{path}\"")

    class Load:
        """
        addition File load operations.
        """
        def __init__(self, instrument, data_handler):
            self.instrument = instrument
            self.data_handler = data_handler
        # MMEMory:LOAD[:STATe] <string>
        def load_state(self, filename: str):
            """
            Recall the specified Analyzer state file.

            Parameter:
                filename (str): File name

            Return:
                None
            """
            self.instrument.write(f":MMEMory:LOAD:STATe \"{filename}\"")

        # MMEMory:LOAD:CHANnel[:STATe] <char>
        def load_channel_state(self, register: str):
            """
            Recall the channel state from memory register.

            Parameter:
                register (str): Register ('A', 'B', 'C', 'D')

            Return:
                None
            """
            allowed = ['A', 'B', 'C', 'D']
            if register not in allowed:
                raise ValueError(f"register must be one of {allowed}")
            self.instrument.write(f":MMEMory:LOAD:CHANnel:STATe \"{register}\"")

        # MMEMory:LOAD:CHANnel<ch>:CALibration <string>
        def load_channel_calibration(self, channel: int, filename: str):
            """
            Recall the calibration for the specified channel from the file.

            Parameter:
                channel (int): Channel number (1-16)
                filename (str): File name

            Return:
                None
            """
            if not (1 <= channel <= 16):
                        raise ValueError("channel must be 1-16")
            self.instrument.write(f":MMEMory:LOAD:CHANnel{channel}:CALibration \"{filename}\"")

        # MMEMory:LOAD:CKIT<Ck> <string>
        def load_cal_kit(self, kit: int, filename: str):
            """
            Recall the definition file for the calibration kit.

            Parameter:
                kit (int): Calibration kit number (1-50)
                filename (str): File name

            Return:
                None
            """
            if not (1 <= kit <= 50):
                raise ValueError("kit must be 1-50")
            self.instrument.write(f":MMEMory:LOAD:CKIT{kit} \"{filename}\"")

        # MMEMory:LOAD:LIMit <string>
        def load_limit_table(self, filename: str):
            """
            Recall the limit table file.

            Parameter:
                filename (str): File name

            Return:
                None
            """
            self.instrument.write(f":MMEMory:LOAD:LIMit \"{filename}\"")

        # MMEMory:LOAD:PLOSs<Pt> <string>
        def load_loss_compensation(self, port: int, filename: str):
            """
            Recall the loss compensation file for the specified port.

            Parameter:
                port (int): Port number (1-4)
                filename (str): File name

            Return:
                None
            """
            if not (1 <= port <= 4):
                raise ValueError("port must be 1-4")
            self.instrument.write(f":MMEMory:LOAD:PLOSs{port} \"{filename}\"")

        # MMEMory:LOAD:RLIMit <string>
        def load_ripple_limit_table(self, filename: str):
            """
            Recall the ripple limit table file.

            Parameter:
                filename (str): File name

            Return:
                None
            """
            self.instrument.write(f":MMEMory:LOAD:RLIMit \"{filename}\"")

        # MMEMory:LOAD:SEGMent <string>
        def load_segment_table(self, filename: str):
            """
            Recall the segment table file.

            Parameter:
                filename (str): File name

            Return:
                None
            """
            self.instrument.write(f":MMEMory:LOAD:SEGMent \"{filename}\"")

        # MMEMory:LOAD:SNP[:DATA] <string>
        def load_touchstone_file(self, filename: str):
            """
            Load the touchstone file to the measured S-parameters of the active channel.

            Parameter:
                filename (str): File name

            Return:
                None
            """
            self.instrument.write(f":MMEMory:LOAD:SNP:DATA \"{filename}\"")

        # MMEMory:LOAD:SNP:FREQuency[:STATe] {OFF|ON|0|1}
        def enable_snp_frequency_from_file(self, enable: bool):
            """
            Enable or disable setting frequency from touchstone file when loading.

            Parameter:
                enable (bool): True to enable, False to disable

            Return:
                None
            """
            self.instrument.write(f":MMEMory:LOAD:SNP:FREQuency:STATe {1 if enable else 0}")

        def is_snp_frequency_from_file_enabled(self) -> bool:
            """
            Query if frequency is set from touchstone file when loading.

            Parameter:
                None

            Return:
                bool: True if enabled, False otherwise
            """
            return bool(int(self.instrument.query(":MMEMory:LOAD:SNP:FREQuency:STATe?")))

        # MMEMory:LOAD:SNP:TRACe<Tr>:MEMory <string>
        def load_touchstone_to_memory_trace(self, trace: int, filename: str):
            """
            Load the Touchstone file to the memory trace.

            Parameter:
                trace (int): Trace number (1-16)
                filename (str): File name

            Return:
                None
            """
            if not (1 <= trace <= 16):
                raise ValueError("trace must be 1-16")
            self.instrument.write(f":MMEMory:LOAD:SNP:TRACe{trace}:MEMory \"{filename}\"")

    class Store:
        """
        File store operations.
        """
        def __init__(self, instrument, data_handler):
            self.instrument = instrument
            self.data_handler = data_handler
            self.fdat = self.Fdat(self.instrument, self.data_handler)
            self.snp = self.Snp(self.instrument)
        # MMEMory:STORe[:STATe] <string>
        def store_state(self, filename: str):
            """
            Save the Analyzer state into a file.

            Parameter:
                filename (str): File name

            Return:
                None
            """
            self.instrument.write(f":MMEMory:STORe:STATe \"{filename}\"")

        # MMEMory:STORe:CHANnel[:STATe] <char>
        def store_channel_state(self, register: str):
            """
            Store the state of the active channel in a memory register.

            Parameter:
                register (str): Register ('A', 'B', 'C', 'D')

            Return:
                None
            """
            allowed = ['A', 'B', 'C', 'D']
            if register not in allowed:
                raise ValueError(f"register must be one of {allowed}")
            self.instrument.write(f":MMEMory:STORe:CHANnel:STATe \"{register}\"")

        # MMEMory:STORe:CHANnel<ch>:CALibration <string>
        def store_channel_calibration(self, channel: int, filename: str):
            """
            Store the calibration of the specified channel to the file.

            Parameter:
                channel (int): Channel number (1-16)
                filename (str): File name

            Return:
                None
            """
            if not (1 <= channel <= 16):
                        raise ValueError("channel must be 1-16")
            self.instrument.write(f":MMEMory:STORe:CHANnel{channel}:CALibration \"{filename}\"")

        # MMEMory:STORe:CHANnel:CLEar
        def clear_channel_memory(self):
            """
            Clear the memory of the channel state saved using the store channel command.

            Parameter:
                None

            Return:
                None
            """
            self.instrument.write(":MMEMory:STORe:CHANnel:CLEar")

        # MMEMory:STORe:CKIT<Ck> <string>
        def store_cal_kit(self, kit: int, filename: str):
            """
            Save the definition file for the calibration kit.

            Parameter:
                kit (int): Calibration kit number (1-50)
                filename (str): File name

            Return:
                None
            """
            if not (1 <= kit <= 50):
                raise ValueError("kit must be 1-50")
            self.instrument.write(f":MMEMory:STORe:CKIT{kit} \"{filename}\"")

        # MMEMory:STORe:FDATa <string>
        def store_trace_data_csv(self, filename: str):
            """
            Save the data of one or several traces to a CSV file.

            Parameter:
                filename (str): File name

            Return:
                None
            """
            self.instrument.write(f":MMEMory:STORe:FDATa \"{filename}\"")

        # MMEMory:STORe:IMAGe <string>
        def store_display_image(self, filename: str):
            """
            Save the display image in BMP or PNG format into a file.

            Parameter:
                filename (str): File name

            Return:
                None
            """
            self.instrument.write(f":MMEMory:STORe:IMAGe \"{filename}\"")

        # MMEMory:STORe:LIMit <string>
        def store_limit_table(self, filename: str):
            """
            Save the limit table into a file.

            Parameter:
                filename (str): File name

            Return:
                None
            """
            self.instrument.write(f":MMEMory:STORe:LIMit \"{filename}\"")

        # MMEMory:STORe:PLOSs<Pt> <string>
        def store_loss_compensation(self, port: int, filename: str):
            """
            Save the loss compensation file.

            Parameter:
                port (int): Port number (1-4)
                filename (str): File name

            Return:
                None
            """
            if not (1 <= port <= 4):
                raise ValueError("port must be 1-4")
            self.instrument.write(f":MMEMory:STORe:PLOSs{port} \"{filename}\"")

        # MMEMory:STORe:RLIMit <string>
        def store_ripple_limit_table(self, filename: str):
            """
            Save the ripple limit table into a file.

            Parameter:
                filename (str): File name

            Return:
                None
            """
            self.instrument.write(f":MMEMory:STORe:RLIMit \"{filename}\"")

        # MMEMory:STORe:SEGMent <string>
        def store_segment_table(self, filename: str):
            """
            Save the segment table into a file.

            Parameter:
                filename (str): File name

            Return:
                None
            """
            self.instrument.write(f":MMEMory:STORe:SEGMent \"{filename}\"")

        # MMEMory:STORe:SNP[:DATA] <string>
        def store_touchstone_file(self, filename: str):
            """
            Save the measured S-parameters of the active channel into a Touchstone file.

            Parameter:
                filename (str): File name

            Return:
                None
            """
            self.instrument.write(f":MMEMory:STORe:SNP:DATA \"{filename}\"")

        class Fdat:
            """
            Store trace data CSV options.
            """
            def __init__(self, instrument, data_handler):
                self.instrument = instrument
                self.data_handler = data_handler
            # MMEMory:STORe:FDAT:SCOPe {ACTive|ALL}
            def set_scope(self, scope: str):
                """
                Set whether the active trace or all traces of the active channel will be saved.

                Parameter:
                    scope (str): 'ACTive' or 'ALL'

                Return:
                    None
                """
                allowed = ['ACTive', 'ALL']
                if scope not in allowed:
                    raise ValueError(f"scope must be one of {allowed}")
                self.instrument.write(f":MMEMory:STORe:FDAT:SCOPe {scope}")

            def get_scope(self) -> str:
                """
                Get the scope for saving trace data.

                Parameter:
                    None

                Return:
                    str: 'ACT' or 'ALL'
                """
                return self.instrument.query(":MMEMory:STORe:FDAT:SCOPe?").strip()

            # MMEMory:STORe:FDAT:FORMat {DB|RI|DISPlayed}
            def set_format(self, fmt: str):
                """
                Set the data format when the CSV file is saved.

                Parameter:
                    fmt (str): 'DB', 'RI', or 'DISPlayed'

                Return:
                    None
                """
                allowed = ['DB', 'RI', 'DISPlayed']
                if fmt not in allowed:
                    raise ValueError(f"fmt must be one of {allowed}")
                self.instrument.write(f":MMEMory:STORe:FDAT:FORMat {fmt}")

            def get_format(self) -> str:
                """
                Get the data format for saving CSV.

                Parameter:
                    None

                Return:
                    str: 'DB', 'RI', or 'DISP'
                """
                return self.instrument.query(":MMEMory:STORe:FDAT:FORMat?").strip()

            # MMEMory:STORe:FDAT:COMMent[:STATe] {OFF|ON|0|1}
            def enable_comment(self, enable: bool):
                """
                Enable or disable comment strings at the beginning of the CSV file.

                Parameter:
                    enable (bool): True to enable, False to disable

                Return:
                    None
                """
                self.instrument.write(f":MMEMory:STORe:FDAT:COMMent:STATe {1 if enable else 0}")

            def is_comment_enabled(self) -> bool:
                """
                Query if comment strings are enabled in the CSV file.

                Parameter:
                    None

                Return:
                    bool: True if enabled, False otherwise
                """
                return bool(int(self.instrument.query(":MMEMory:STORe:FDAT:COMMent:STATe?")))

            # MMEMory:STORe:FDAT:STIMulus[:STATe] {OFF|ON|0|1}
            def enable_stimulus_column(self, enable: bool):
                """
                Enable or disable the stimulus column in the CSV file.

                Parameter:
                    enable (bool): True to enable, False to disable

                Return:
                    None
                """
                self.instrument.write(f":MMEMory:STORe:FDAT:STIMulus:STATe {1 if enable else 0}")

            def is_stimulus_column_enabled(self) -> bool:
                """
                Query if the stimulus column is enabled in the CSV file.

                Parameter:
                    None

                Return:
                    bool: True if enabled, False otherwise
                """
                return bool(int(self.instrument.query(":MMEMory:STORe:FDAT:STIMulus:STATe?")))

            # MMEMory:STORe:FDAT:SEParator {POINt|LOCal}
            def set_separator(self, sep: str):
                """
                Set the separators used when the CSV file is saved.

                Parameter:
                    sep (str): 'POINt' or 'LOCal'

                Return:
                    None
                """
                allowed = ['POINt', 'LOCal']
                if sep not in allowed:
                    raise ValueError(f"sep must be one of {allowed}")
                self.instrument.write(f":MMEMory:STORe:FDAT:SEParator {sep}")

            def get_separator(self) -> str:
                """
                Get the separator used for saving CSV.

                Parameter:
                    None

                Return:
                    str: 'POIN' or 'LOC'
                """
                return self.instrument.query(":MMEMory:STORe:FDAT:SEParator?").strip()

        class Snp:
            """
            Store Touchstone file options.
            """
            def __init__(self, instrument):
                self.instrument = instrument

            # MMEMory:STORe:SNP:FORMat <char>
            def set_format(self, fmt: str):
                """
                Set the data format for the S-parameter saved.

                Parameter:
                    fmt (str): 'DB', 'MA', or 'RI'

                Return:
                    None
                """
                allowed = ['DB', 'MA', 'RI']
                if fmt not in allowed:
                    raise ValueError(f"fmt must be one of {allowed}")
                self.instrument.write(f":MMEMory:STORe:SNP:FORMat {fmt}")

            def get_format(self) -> str:
                """
                Get the data format for the S-parameter saved.

                Parameter:
                    None

                Return:
                    str: 'RI', 'DB', or 'MA'
                """
                return self.instrument.query(":MMEMory:STORe:SNP:FORMat?").strip()

            # MMEMory:STORe:SNP:SEParator <char>
            def set_separator(self, sep: str):
                """
                Set the Touchstone file separator symbol.

                Parameter:
                    sep (str): 'TAB' or 'SPACe'

                Return:
                    None
                """
                allowed = ['TAB', 'SPACe']
                if sep not in allowed:
                    raise ValueError(f"sep must be one of {allowed}")
                self.instrument.write(f":MMEMory:STORe:SNP:SEParator {sep}")

            def get_separator(self) -> str:
                """
                Get the Touchstone file separator symbol.

                Parameter:
                    None

                Return:
                    str: 'TAB' or 'SPAC'
                """
                return self.instrument.query(":MMEMory:STORe:SNP:SEParator?").strip()

            # MMEMory:STORe:SNP:TRACe:TRANsform[:STATe] {OFF|ON|0|1}
            def enable_trace_transform(self, enable: bool):
                """
                Enable or disable including trace transform in the Touchstone file.

                Parameter:
                    enable (bool): True to enable, False to disable

                Return:
                    None
                """
                self.instrument.write(f":MMEMory:STORe:SNP:TRACe:TRANsform:STATe {1 if enable else 0}")

            def is_trace_transform_enabled(self) -> bool:
                """
                Query if including trace transform is enabled in the Touchstone file.

                Parameter:
                    None

                Return:
                    bool: True if enabled, False otherwise
                """
                return bool(int(self.instrument.query(":MMEMory:STORe:SNP:TRACe:TRANsform:STATe?")))
            # MMEMory:STORe:SNP:TYPE?
            def get_touchstone_file_type(self):
                """
                Reads out the type of Touchstone file (S1P, S2P, S3P or S4P) to be used when saving S–parameters.

                Parameter:
                    None

                Return:
                    str: Touchstone file type ('S1P', 'S2P', 'S3P', or 'S4P')
                """
                return self.instrument.query(":MMEMory:STORe:SNP:TYPE?").strip()

            # MMEMory:STORe:SNP:TYPE:S1P <port>
            # MMEMory:STORe:SNP:TYPE:S1P?
            def set_touchstone_type_s1p(self, port: int):
                """
                Sets the 1-port Touchstone file type (*.S1P) and the port number.

                Parameter:
                    port (int): Port number from 1 to 4

                Return:
                    None
                """
                if not (1 <= port <= 4):
                    raise ValueError("port must be 1-4")
                self.instrument.write(f":MMEMory:STORe:SNP:TYPE:S1P {port}")

            def get_touchstone_type_s1p(self) -> int:
                """
                Reads out the port number for the 1-port Touchstone file type.

                Parameter:
                    None

                Return:
                    int: Port number
                """
                return int(self.instrument.query(":MMEMory:STORe:SNP:TYPE:S1P?"))

            # MMEMory:STORe:SNP:TYPE:S2P <port1>,<port2>
            # MMEMory:STORe:SNP:TYPE:S2P?
            def set_touchstone_type_s2p(self, port1: int, port2: int):
                """
                Sets the 2-port Touchstone file type (*.S2P) and the port numbers.

                Parameter:
                    port1 (int): First port number (1-4)
                    port2 (int): Second port number (1-4)

                Return:
                    None
                """
                if not (1 <= port1 <= 4 and 1 <= port2 <= 4):
                    raise ValueError("port1 and port2 must be 1-4")
                self.instrument.write(f":MMEMory:STORe:SNP:TYPE:S2P {port1},{port2}")

            def get_touchstone_type_s2p(self):
                """
                Reads out the port numbers for the 2-port Touchstone file type.

                Parameter:
                    None

                Return:
                    tuple: (port1, port2)
                """
                resp = self.instrument.query(":MMEMory:STORe:SNP:TYPE:S2P?").strip()
                return tuple(map(int, resp.split(',')))

            # MMEMory:STORe:SNP:TYPE:S3P <port1>,<port2>,<port3>
            # MMEMory:STORe:SNP:TYPE:S3P?
            def set_touchstone_type_s3p(self, port1: int, port2: int, port3: int):
                """
                Sets the 3-port Touchstone file type (*.S3P) and the port numbers.

                Parameter:
                    port1 (int): First port number (1-4)
                    port2 (int): Second port number (1-4)
                    port3 (int): Third port number (1-4)

                Return:
                    None
                """
                if not (1 <= port1 <= 4 and 1 <= port2 <= 4 and 1 <= port3 <= 4):
                    raise ValueError("port1, port2, and port3 must be 1-4")
                self.instrument.write(f":MMEMory:STORe:SNP:TYPE:S3P {port1},{port2},{port3}")

            def get_touchstone_type_s3p(self):
                """
                Reads out the port numbers for the 3-port Touchstone file type.

                Parameter:
                    None

                Return:
                    tuple: (port1, port2, port3)
                """
                resp = self.instrument.query(":MMEMory:STORe:SNP:TYPE:S3P?").strip()
                return tuple(map(int, resp.split(',')))

            # MMEMory:STORe:SNP:TYPE:S4P <port1>,<port2>,<port3>,<port4>
            # MMEMory:STORe:SNP:TYPE:S4P?
            def set_touchstone_type_s4p(self, port1: int, port2: int, port3: int, port4: int):
                """
                Sets the 4-port Touchstone file type (*.S4P) and the port numbers.

                Parameter:
                    port1 (int): First port number (1-4)
                    port2 (int): Second port number (1-4)
                    port3 (int): Third port number (1-4)
                    port4 (int): Fourth port number (1-4)

                Return:
                    None
                """
                if not (1 <= port1 <= 4 and 1 <= port2 <= 4 and 1 <= port3 <= 4 and 1 <= port4 <= 4):
                    raise ValueError("port1, port2, port3, and port4 must be 1-4")
                self.instrument.write(f":MMEMory:STORe:SNP:TYPE:S4P {port1},{port2},{port3},{port4}")

            def get_touchstone_type_s4p(self):
                """
                Reads out the port numbers for the 4-port Touchstone file type.

                Parameter:
                    None

                Return:
                    tuple: (port1, port2, port3, port4)
                """
                resp = self.instrument.query(":MMEMory:STORe:SNP:TYPE:S4P?").strip()
                return tuple(map(int, resp.split(',')))

            # MMEMory:STORe:STYPe <char>
            # MMEMory:STORe:STYPe?
            def set_save_type(self, save_type: str):
                """
                Selects the type of the Analyzer or channel state saving.

                Parameter:
                    save_type (str): One of ['STATe', 'CSTate', 'DSTate', 'CDSTate', 'CMSTate']

                Return:
                    None
                """
                allowed = ['STATe', 'CSTate', 'DSTate', 'CDSTate', 'CMSTate']
                if save_type not in allowed:
                    raise ValueError(f"save_type must be one of {allowed}")
                self.instrument.write(f":MMEMory:STORe:STYPe {save_type}")

            def get_save_type(self) -> str:
                """
                Reads out the type of the Analyzer or channel state saving.

                Parameter:
                    None

                Return:
                    str: Save type ('STAT', 'CST', 'DST', 'CDST', 'CMST')
                """
                return self.instrument.query(":MMEMory:STORe:STYPe?").strip()
            # MMEMory:TRANsfer? <string>
            def transfer_file_from_analyzer(self, filename: str) -> bytes:
                """
                Transfer the contents of a specified file from the Analyzer to the external PC.

                Parameter:
                filename (str): The file name with the full path

                Return:
                bytes: The file contents as bytes
                """
                response = self.instrument.query_binary_values(
                f":MMEMory:TRANsfer? \"{filename}\"", datatype='B', is_big_endian=True
                )
                return bytes(response)

    
class Output:
    """
        addition Commands output settings.
    """
    def __init__(self, instrument, data_handler):
        self.instrument = instrument
        self.data_handler = data_handler
    # OUTPut[:STATe] {OFF|ON|0|1}
    def enable_output(self, enable: bool):
        """
        Enable or disable the RF signal output.

        Parameter:
        enable (bool): True to enable, False to disable

        Return:
        None
        """
        self.instrument.write(f":OUTPut:STATe {1 if enable else 0}")

    def is_output_enabled(self) -> bool:
        """
        Query if the RF signal output is enabled.

        Parameter:
        None

        Return:
        bool: True if enabled, False otherwise
        """
        return bool(int(self.instrument.query(":OUTPut:STATe?")))

class Sense:
    """Averaging, calibration, calibration kit management, port
extension, IFBW setting, frequency settings, sweep settings,
frequency offset, channel data transfer."""
    def __init__(self, instrument, data_handler, channel):
        self.instrument = instrument
        self.data_handler = data_handler
        self.n = channel
        # Add instance variables for each direct subclass under Sense
        self.average = self.Average(instrument, data_handler, channel)
        self.bandwidth = self.Bandwidth(instrument, data_handler, channel)
        
        self.impedance = self.Impedance(instrument, data_handler, channel)
        self.offset = self.Offset(instrument, data_handler, channel)
        self.receiver = self.Receiver(instrument, data_handler, channel)
        self.data = self.Data(instrument, data_handler, channel)
        self.sweep = self.Sweep(instrument, data_handler, channel)
        self.reference_source = self.ReferenceSource(instrument, data_handler, channel)
        self.voltage = self.Voltage(instrument, data_handler, channel)
        
        
        
        self.adapter = self.Adapter(instrument, data_handler, channel)
        self.calibration = self.Calibration(instrument, data_handler, channel)
        self.frequency = self.Frequency(instrument, data_handler, channel)
        self.reference_oscillator = self.ReferenceOscillator(instrument, data_handler, channel)
        
    class Average:
        """
        Averaging related commands.
        """
        def __init__(self, instrument, data_handler, channel):
            self.instrument = instrument
            self.data_handler = data_handler
            self.n = channel

        # SENS:AVER - Averaging ON/OFF
        def enable_averaging(self, enable: bool):
            """
            Enable or disable averaging.

            Parameter:
                enable (bool): True to enable, False to disable

            Return:
                None
            """
            self.instrument.write(f":SENS{self.n}:AVER {1 if enable else 0}")

        def is_averaging_enabled(self) -> bool:
            """
            Query if averaging is enabled.

            Parameter:
                None

            Return:
                bool: True if enabled, False otherwise
            """
            return bool(int(self.instrument.query(f":SENS{self.n}:AVER?")))

        # SENS:AVER:CLE - Restart averaging
        def restart_averaging(self):
            """
            Restart averaging.

            Parameter:
                None

            Return:
                None
            """
            self.instrument.write(f":SENS{self.n}:AVER:CLE")

        # SENS:AVER:COUN - Averaging factor
        def set_averaging_factor(self, value: int):
            """
            Set the averaging factor.

            Parameter:
                value (int): Averaging factor

            Return:
                None
            """
            self.instrument.write(f":SENS{self.n}:AVER:COUN {value}")

        def get_averaging_factor(self) -> int:
            """
            Get the averaging factor.

            Parameter:
                None

            Return:
                int: Averaging factor
            """
            return int(self.instrument.query(f":SENS{self.n}:AVER:COUN?"))

    class Bandwidth:
        """
        addition IF bandwidth related commands.
        """
        def __init__(self, instrument, data_handler, channel):
            self.instrument = instrument
            self.data_handler = data_handler
            self.n = channel
            self.resolution = self.Resolution(instrument, data_handler, channel)
            

        class Resolution:
            """
            IF bandwidth resolution related commands.
            """
            def __init__(self, instrument, data_handler, channel):
                self.instrument = instrument
                self.data_handler = data_handler
                self.n = channel

            # SENSe<Ch>:BANDwidth[:RESolution] <frequency>
            def set_bandwidth_resolution(self, value: float):
                """
                Set the IF bandwidth resolution.

                Parameter:
                    value (float): IF bandwidth value in Hz

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:BAND:RES {value}")

            def get_bandwidth_resolution(self) -> float:
                """
                Get the IF bandwidth resolution.

                Parameter:
                    None

                Return:
                    float: IF bandwidth value in Hz
                """
                return float(self.instrument.query(f":SENS{self.n}:BAND:RES?"))
        # SENS:BAND - IF bandwidth
        def set_if_bandwidth(self, value: float):
            """
            Set the IF bandwidth.

            Parameter:
                value (float): IF bandwidth in Hz

            Return:
                None
            """
            self.instrument.write(f":SENS{self.n}:BAND {value}")

        def get_if_bandwidth(self) -> float:
            """
            Get the IF bandwidth.

            Parameter:
                None

            Return:
                float: IF bandwidth in Hz
            """
            return float(self.instrument.query(f":SENS{self.n}:BAND?"))

        # SENS:BWID - IF bandwidth (alias)
        def set_if_bandwidth_alias(self, value: float):
            """
            Set the IF bandwidth (alias command).

            Parameter:
                value (float): IF bandwidth in Hz

            Return:
                None
            """
            self.instrument.write(f":SENS{self.n}:BWID {value}")

        def get_if_bandwidth_alias(self) -> float:
            """
            Get the IF bandwidth (alias command).

            Parameter:
                None

            Return:
                float: IF bandwidth in Hz
            """
            return float(self.instrument.query(f":SENS{self.n}:BWID?"))

    
        
    
    class Impedance:
        """
        System impedance related commands.
        """
        def __init__(self, instrument, data_handler, channel):
            self.instrument = instrument
            self.data_handler = data_handler
            self.n = channel
            self.port = self.Port(instrument, data_handler, channel)


        # SENS:CORR:IMP - System Z0
        def set_system_impedance(self, value: float):
            """
            Set the system impedance Z0.

            Parameter:
                value (float): System impedance

            Return:
                None
            """
            self.instrument.write(f":SENS{self.n}:CORR:IMP {value}")

        def get_system_impedance(self) -> float:
            """
            Get the system impedance Z0.

            Parameter:
                None

            Return:
                float: System impedance
            """
            return float(self.instrument.query(f":SENS{self.n}:CORR:IMP?"))

        # SENS:CORR:IMP:SEL:AUTO - Auto-select Z0 ON/OFF
        def enable_auto_select_impedance(self, enable: bool):
            """
            Enable or disable auto-select Z0.

            Parameter:
                enable (bool): True to enable, False to disable

            Return:
                None
            """
            self.instrument.write(f":SENS{self.n}:CORR:IMP:SEL:AUTO {1 if enable else 0}")

        def is_auto_select_impedance_enabled(self) -> bool:
            """
            Query if auto-select Z0 is enabled.

            Parameter:
                None

            Return:
                bool: True if enabled, False otherwise
            """
            return bool(int(self.instrument.query(f":SENS{self.n}:CORR:IMP:SEL:AUTO?")))

        class Port:
            """
            System Z0 for the specified port.
            """
            def __init__(self, instrument, data_handler, channel):
                self.instrument = instrument
                self.data_handler = data_handler
                self.n = channel

            # SENS:CORR:PORT:IMP - System Z0 for the specified port
            def set_port_impedance(self, port: int, value: float):
                """
                Set the system Z0 for the specified port.

                Parameter:
                    port (int): Port number
                    value (float): Impedance value

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:CORR:PORT{port}:IMP {value}")

            def get_port_impedance(self, port: int) -> float:
                """
                Get the system Z0 for the specified port.

                Parameter:
                    port (int): Port number

                Return:
                    float: Impedance value
                """
                return float(self.instrument.query(f":SENS{self.n}:CORR:PORT{port}:IMP?"))

    
    class Receiver:
        """
        Receiver calibration commands.
        """
        def __init__(self, instrument, data_handler, channel):
            self.instrument = instrument
            self.data_handler = data_handler
            self.n = channel

        # SENS:CORR:REC - Receiver correction ON/OFF
        def enable_receiver_correction(self, enable: bool):
            """
            Enable or disable receiver correction.

            Parameter:
                enable (bool): True to enable, False to disable

            Return:
                None
            """
            self.instrument.write(f":SENS{self.n}:CORR:REC {1 if enable else 0}")

        def is_receiver_correction_enabled(self) -> bool:
            """
            Query if receiver correction is enabled.

            Parameter:
                None

            Return:
                bool: True if enabled, False otherwise
            """
            return bool(int(self.instrument.query(f":SENS{self.n}:CORR:REC?")))
    class Data:
        """
        Channel data transfer commands.
        """
        def __init__(self, instrument, data_handler, channel):
            self.instrument = instrument
            self.data_handler = data_handler
            self.n = channel

        # SENS:DATA:CORR? - Corrected S-parameter or receiver data
        def get_corrected_data(self):
            """
            Get corrected S-parameter data or corrected receiver data.

            Parameter:
                None

            Return:
                list: Corrected data array
            """
            data = self.instrument.query(f":SENS{self.n}:DATA:CORR?")
            if self.data_handler.is_auto_saving_data_enabled():
                self.data_handler.write_to_file(self, f"CORR_S_PARAM", data, file_type = EFileType.CSV)
            return self.data_handler.parse_array(data)
        
        def get_raw_data_array_of_parameter(self, param: str):
                """param (str): S-parameter (e.g., 'S11', 'S21', ...) 
                or receiver ('T11', 'R11', ...)

                Return:
                list: Corrected data array (real/imag pairs)
                """
                allowed_prefixes = ['S', 'T', 'R', 'A', 'B', 'C', 'D']
                if not any(param.startswith(p) for p in allowed_prefixes):
                    raise ValueError("param must start with S, T, R, A, B, C, or D")
                data = self.instrument.query(f":SENS{self.n}:DATA:CORR? {param}")
                if self.data_handler.is_auto_saving_data_enabled():
                    self.data_handler.write_to_file(self, f"RAW_DATA", data, file_type = EFileType.CSV)
                return self.data_handler.parse_array(data)

        # SENS:DATA:RAWD? - Raw S-parameter or receiver data
        def get_raw_data(self):
            """
            Get raw S-parameter data or raw receiver data.

            Parameter:
                None

            Return:
                list: Raw data array
            """
            data = self.instrument.query(f":SENS{self.n}:DATA:RAWD?")
            if self.data_handler.is_auto_saving_data_enabled():
                    self.data_handler.write_to_file(self, f"RAW_S_PARAM", data, file_type = EFileType.CSV)
            return self.data_handler.parse_array(data)

        # SENS:FREQ:DATA? - Stimulus data
        def get_stimulus_data(self):
            """
            Get stimulus data.

            Parameter:
                None

            Return:
                list: Stimulus data array
            """
            data = self.instrument.query(f":SENS{self.n}:FREQ:DATA?")
            if self.data_handler.is_auto_saving_data_enabled():
                self.data_handler.write_to_file(self, "STIMULUS", data, file_type = EFileType.CSV)
            return self.data_handler.parse_array(data)



        
    class Offset:
        "Generic offset setting commands"
        def __init__(self, instrument, data_handler, channel):
            self.instrument = instrument
            self.data_handler = data_handler
            self.n = channel
            self.adjustment = self.Adjustment(instrument, data_handler, channel)
            self.settings = self.Settings(instrument, data_handler, channel)
        class Adjustment:
            """
            Mixer Measurements: Frequency offset adjust commands.
            """
            def __init__(self, instrument, data_handler, channel):
                self.instrument = instrument
                self.data_handler = data_handler
                self.n = channel

            # SENS:OFFS:ADJ - Frequency offset adjust ON/OFF
            def enable_offset_adjust(self, enable: bool):
                """
                Enable or disable frequency offset adjust.

                Parameter:
                    enable (bool): True to enable, False to disable

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:OFFS:ADJ {1 if enable else 0}")

            def is_offset_adjust_enabled(self) -> bool:
                """
                Query if frequency offset adjust is enabled.

                Parameter:
                    None

                Return:
                    bool: True if enabled, False otherwise
                """
                return bool(int(self.instrument.query(f":SENS{self.n}:OFFS:ADJ?")))

            # SENS:OFFS:ADJ:CONT:PER - Adjust period
            def set_adjust_period(self, value: float):
                """
                Set the period for frequency offset adjustment.

                Parameter:
                    value (float): Period value

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:OFFS:ADJ:CONT:PER {value}")

            def get_adjust_period(self) -> float:
                """
                Get the period for frequency offset adjustment.

                Parameter:
                    None

                Return:
                    float: Period value
                """
                return float(self.instrument.query(f":SENS{self.n}:OFFS:ADJ:CONT:PER?"))

            # SENS:OFFS:ADJ:EXEC - Executes adjustment once
            def execute_adjustment_once(self):
                """
                Execute frequency offset adjustment once.

                Parameter:
                    None

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:OFFS:ADJ:EXEC")

            # SENS:OFFS:ADJ:PATH - Adjustment path
            def set_adjustment_path(self, path: str):
                """
                Set the adjustment path.

                Parameter:
                    path (str): Adjustment path string

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:OFFS:ADJ:PATH {path}")

            def get_adjustment_path(self) -> str:
                """
                Get the adjustment path.

                Parameter:
                    None

                Return:
                    str: Adjustment path
                """
                return self.instrument.query(f":SENS{self.n}:OFFS:ADJ:PATH?").strip()

            # SENS:OFFS:ADJ:PORT - Adjusted Ports
            def set_adjusted_ports(self, ports: str):
                """
                Set the adjusted ports.

                Parameter:
                    ports (str): Adjusted ports string

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:OFFS:ADJ:PORT {ports}")

            def get_adjusted_ports(self) -> str:
                """
                Get the adjusted ports.

                Parameter:
                    None

                Return:
                    str: Adjusted ports
                """
                return self.instrument.query(f":SENS{self.n}:OFFS:ADJ:PORT?").strip()

            # SENS:OFFS:ADJ:VAL - Adjust Value
            def set_adjust_value(self, value: float):
                """
                Set the adjust value.

                Parameter:
                    value (float): Adjust value

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:OFFS:ADJ:VAL {value}")

            def get_adjust_value(self) -> float:
                """
                Get the adjust value.

                Parameter:
                    None

                Return:
                    float: Adjust value
                """
                return float(self.instrument.query(f":SENS{self.n}:OFFS:ADJ:VAL?"))

        class Settings:
            """
            Frequency offset and port/source/receiver offset settings.
            """
            def __init__(self, instrument, data_handler, channel):
                self.instrument = instrument
                self.data_handler = data_handler
                self.n = channel

            # SENS:OFFS - Frequency offset ON/OFF
            def enable_frequency_offset(self, enable: bool):
                """
                Enable or disable frequency offset.

                Parameter:
                    enable (bool): True to enable, False to disable

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:OFFS {1 if enable else 0}")

            def is_frequency_offset_enabled(self) -> bool:
                """
                Query if frequency offset is enabled.

                Parameter:
                    None

                Return:
                    bool: True if enabled, False otherwise
                """
                return bool(int(self.instrument.query(f":SENS{self.n}:OFFS?")))

            # SENS:OFFS:PORT:DATA? - Port offset data
            def get_port_offset_data(self):
                """
                Get port offset data.

                Parameter:
                    None

                Return:
                    list: Port offset data array
                """
                data = self.instrument.query(f":SENS{self.n}:OFFS:PORT:DATA?")
                if self.data_handler.is_auto_saving_data_enabled():
                    self.data_handler.write_to_file(self, "PORT_OFFSET", data, file_type = EFileType.CSV)
                return self.data_handler.parse_array(data)

            # SENS:OFFS:PORT:DIV - Port offset divisor
            def set_port_offset_divisor(self, value: float):
                """
                Set port offset divisor.

                Parameter:
                    value (float): Divisor value

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:OFFS:PORT:DIV {value}")

            def get_port_offset_divisor(self) -> float:
                """
                Get port offset divisor.

                Parameter:
                    None

                Return:
                    float: Divisor value
                """
                return float(self.instrument.query(f":SENS{self.n}:OFFS:PORT:DIV?"))

            # SENS:OFFS:PORT:MULT - Port offset multiplier
            def set_port_offset_multiplier(self, value: float):
                """
                Set port offset multiplier.

                Parameter:
                    value (float): Multiplier value

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:OFFS:PORT:MULT {value}")

            def get_port_offset_multiplier(self) -> float:
                """
                Get port offset multiplier.

                Parameter:
                    None

                Return:
                    float: Multiplier value
                """
                return float(self.instrument.query(f":SENS{self.n}:OFFS:PORT:MULT?"))

            # SENS:OFFS:PORT:OFFS - Port offset
            def set_port_offset(self, value: float):
                """
                Set port offset.

                Parameter:
                    value (float): Offset value

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:OFFS:PORT:OFFS {value}")

            def get_port_offset(self) -> float:
                """
                Get port offset.

                Parameter:
                    None

                Return:
                    float: Offset value
                """
                return float(self.instrument.query(f":SENS{self.n}:OFFS:PORT:OFFS?"))

            # SENS:OFFS:PORT:STAR - Port offset start
            def set_port_offset_start(self, value: float):
                """
                Set port offset start.

                Parameter:
                    value (float): Start value

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:OFFS:PORT:STAR {value}")

            def get_port_offset_start(self) -> float:
                """
                Get port offset start.

                Parameter:
                    None

                Return:
                    float: Start value
                """
                return float(self.instrument.query(f":SENS{self.n}:OFFS:PORT:STAR?"))

            # SENS:OFFS:PORT:STOP - Port offset stop
            def set_port_offset_stop(self, value: float):
                """
                Set port offset stop.

                Parameter:
                    value (float): Stop value

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:OFFS:PORT:STOP {value}")

            def get_port_offset_stop(self) -> float:
                """
                Get port offset stop.

                Parameter:
                    None

                Return:
                    float: Stop value
                """
                return float(self.instrument.query(f":SENS{self.n}:OFFS:PORT:STOP?"))

            # SENS:OFFS:REC:DATA? - Receiver offset data
            def get_receiver_offset_data(self):
                """
                Get receiver offset data.

                Parameter:
                    None

                Return:
                    list: Receiver offset data array
                """
                data = self.instrument.query(f":SENS{self.n}:OFFS:REC:DATA?")
                if self.data_handler.is_auto_saving_data_enabled():
                    self.data_handler.write_to_file(self, f"RECIEVER_OFFSET_{self.n}", data, file_type = EFileType.CSV)
                return self.data_handler.parse_array(data)

            # SENS:OFFS:REC:DIV - Receiver offset divisor
            def set_receiver_offset_divisor(self, value: float):
                """
                Set receiver offset divisor.

                Parameter:
                    value (float): Divisor value

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:OFFS:REC:DIV {value}")

            def get_receiver_offset_divisor(self) -> float:
                """
                Get receiver offset divisor.

                Parameter:
                    None

                Return:
                    float: Divisor value
                """
                return float(self.instrument.query(f":SENS{self.n}:OFFS:REC:DIV?"))

            # SENS:OFFS:REC:MULT - Receiver offset multiplier
            def set_receiver_offset_multiplier(self, value: float):
                """
                Set receiver offset multiplier.

                Parameter:
                    value (float): Multiplier value

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:OFFS:REC:MULT {value}")

            def get_receiver_offset_multiplier(self) -> float:
                """
                Get receiver offset multiplier.

                Parameter:
                    None

                Return:
                    float: Multiplier value
                """
                return float(self.instrument.query(f":SENS{self.n}:OFFS:REC:MULT?"))

            # SENS:OFFS:REC:OFFS - Receiver offset
            def set_receiver_offset(self, value: float):
                """
                Set receiver offset.

                Parameter:
                    value (float): Offset value

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:OFFS:REC:OFFS {value}")

            def get_receiver_offset(self) -> float:
                """
                Get receiver offset.

                Parameter:
                    None

                Return:
                    float: Offset value
                """
                return float(self.instrument.query(f":SENS{self.n}:OFFS:REC:OFFS?"))

            # SENS:OFFS:REC:STAR - Receiver offset start
            def set_receiver_offset_start(self, value: float):
                """
                Set receiver offset start.

                Parameter:
                    value (float): Start value

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:OFFS:REC:STAR {value}")

            def get_receiver_offset_start(self) -> float:
                """
                Get receiver offset start.

                Parameter:
                    None

                Return:
                    float: Start value
                """
                return float(self.instrument.query(f":SENS{self.n}:OFFS:REC:STAR?"))

            # SENS:OFFS:REC:STOP - Receiver offset stop
            def set_receiver_offset_stop(self, value: float):
                """
                Set receiver offset stop.

                Parameter:
                    value (float): Stop value

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:OFFS:REC:STOP {value}")

            def get_receiver_offset_stop(self) -> float:
                """
                Get receiver offset stop.

                Parameter:
                    None

                Return:
                    float: Stop value
                """
                return float(self.instrument.query(f":SENS{self.n}:OFFS:REC:STOP?"))

            # SENS:OFFS:SOUR:DATA? - Source offset data
            def get_source_offset_data(self):
                """
                Get source offset data.

                Parameter:
                    None

                Return:
                    list: Source offset data array
                """
                data = self.instrument.query(f":SENS{self.n}:OFFS:SOUR:DATA?")
                if self.data_handler.is_auto_saving_data_enabled():
                    self.data_handler.write_to_file(self, f"SOURCE_OFFSET_{self.n}", data, file_type = EFileType.CSV)
                return self.data_handler.parse_array(data)

            # SENS:OFFS:SOUR:DIV - Source offset divisor
            def set_source_offset_divisor(self, value: float):
                """
                Set source offset divisor.

                Parameter:
                    value (float): Divisor value

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:OFFS:SOUR:DIV {value}")

            def get_source_offset_divisor(self) -> float:
                """
                Get source offset divisor.

                Parameter:
                    None

                Return:
                    float: Divisor value
                """
                return float(self.instrument.query(f":SENS{self.n}:OFFS:SOUR:DIV?"))

            # SENS:OFFS:SOUR:MULT - Source offset multiplier
            def set_source_offset_multiplier(self, value: float):
                """
                Set source offset multiplier.

                Parameter:
                    value (float): Multiplier value

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:OFFS:SOUR:MULT {value}")

            def get_source_offset_multiplier(self) -> float:
                """
                Get source offset multiplier.

                Parameter:
                    None

                Return:
                    float: Multiplier value
                """
                return float(self.instrument.query(f":SENS{self.n}:OFFS:SOUR:MULT?"))

            # SENS:OFFS:SOUR:OFFS - Source offset
            def set_source_offset(self, value: float):
                """
                Set source offset.

                Parameter:
                    value (float): Offset value

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:OFFS:SOUR:OFFS {value}")

            def get_source_offset(self) -> float:
                """
                Get source offset.

                Parameter:
                    None

                Return:
                    float: Offset value
                """
                return float(self.instrument.query(f":SENS{self.n}:OFFS:SOUR:OFFS?"))

            # SENS:OFFS:SOUR:STAR - Source offset start
            def set_source_offset_start(self, value: float):
                """
                Set source offset start.

                Parameter:
                    value (float): Start value

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:OFFS:SOUR:STAR {value}")

            def get_source_offset_start(self) -> float:
                """
                Get source offset start.

                Parameter:
                    None

                Return:
                    float: Start value
                """
                return float(self.instrument.query(f":SENS{self.n}:OFFS:SOUR:STAR?"))

            # SENS:OFFS:SOUR:STOP - Source offset stop
            def set_source_offset_stop(self, value: float):
                """
                Set source offset stop.

                Parameter:
                    value (float): Stop value

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:OFFS:SOUR:STOP {value}")

            def get_source_offset_stop(self) -> float:
                """
                Get source offset stop.

                Parameter:
                    None

                Return:
                    float: Stop value
                """
                return float(self.instrument.query(f":SENS{self.n}:OFFS:SOUR:STOP?"))

            # SENS:OFFS:TYPE - Offset type
            def set_offset_type(self, offset_type: str):
                """
                Set the offset type.

                Parameter:
                    offset_type (str): Offset type string

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:OFFS:TYPE {offset_type}")

            def get_offset_type(self) -> str:
                """
                Get the offset type.

                Parameter:
                    None

                Return:
                    str: Offset type
                """
                return self.instrument.query(f":SENS{self.n}:OFFS:TYPE?").strip()

    class ReferenceSource:
        """
        addition Analyzer reference source commands.
        """
        def __init__(self, instrument, data_handler, channel):
            self.instrument = instrument
            self.data_handler = data_handler
            self.n = channel

        # SENS:ROSC:SOUR - Reference source
        def set_reference_source(self, source: str):
            """
            Set the analyzer reference source.

            Parameter:
                source (str): Reference source string

            Return:
                None
            """
            self.instrument.write(f":SENS{self.n}:ROSC:SOUR {source}")

        def get_reference_source(self) -> str:
            """
            Get the analyzer reference source.

            Parameter:
                None

            Return:
                str: Reference source
            """
            return self.instrument.query(f":SENS{self.n}:ROSC:SOUR?").strip()

    class Voltage:
        """
        DC voltage measurement commands.
        """
        def __init__(self, instrument, data_handler, channel):
            self.instrument = instrument
            self.data_handler = data_handler
            self.n = channel

        # SENS:VOLT:DC:RANG:UPP - DC voltage range
        def set_dc_voltage_range(self, value: float):
            """
            Set the DC voltage range.

            Parameter:
                value (float): DC voltage range

            Return:
                None
            """
            self.instrument.write(f":SENS{self.n}:VOLT:DC:RANG:UPP {value}")

        def get_dc_voltage_range(self) -> float:
            """
            Get the DC voltage range.

            Parameter:
                None

            Return:
                float: DC voltage range
            """
            return float(self.instrument.query(f":SENS{self.n}:VOLT:DC:RANG:UPP?"))
    class Average:
        """addition """
        def __init__(self, instrument, data_handler, channel):
            self.instrument = instrument
            self.data_handler = data_handler
            self.n = channel

        # SENSe<Ch>:AVERage[:STATe] {OFF|ON|0|1}
        def enable_averaging_state(self, enable: bool):
            """
            Enable or disable the measurement averaging function.

            Parameter:
                enable (bool): True to enable, False to disable

            Return:
                None
            """
            self.instrument.write(f":SENS{self.n}:AVER:STAT {1 if enable else 0}")

        def is_averaging_state_enabled(self) -> bool:
            """
            Query if the measurement averaging function is enabled.

            Parameter:
                None

            Return:
                bool: True if enabled, False otherwise
            """
            return bool(int(self.instrument.query(f":SENS{self.n}:AVER:STAT?")))

    

        # SENSe<Ch>:AVERage:CLEar
        def clear_averaging(self):
            """
            Restarts the averaging process when the averaging function is turned on.

            Parameter:
                None

            Return:
                None
            """
            self.instrument.write(f":SENS{self.n}:AVER:CLE")

    
        

        # SENSe<Ch>:AVERage:COUNt <numeric>
        def set_averaging_count(self, value: int):
            """
            Set the averaging factor when the averaging function is turned on.

            Parameter:
                value (int): Averaging factor (1 to 999)

            Return:
                None
            """
            value = max(1, min(999, value))
            self.instrument.write(f":SENS{self.n}:AVER:COUN {value}")

        def get_averaging_count(self) -> int:
            """
            Get the averaging factor when the averaging function is turned on.

            Parameter:
                None

            Return:
                int: Averaging factor
            """
            return int(self.instrument.query(f":SENS{self.n}:AVER:COUN?"))




    class Adapter:
        """
        addition Adapter removal/insertion related commands.
        """
        def __init__(self, instrument, data_handler, channel):
            self.instrument = instrument
            self.data_handler = data_handler
            self.n = channel
           

        # SENSe<Ch>:CORRection:COLLect:ADAPter:DELay <numeric>
        def set_adapter_delay(self, value: float):
            """
            Set the approximate delay value of an adapter for removal/insertion.

            Parameter:
                value (float): Delay value in seconds (negative for removal, positive for insertion)

            Return:
                None
            """
            self.instrument.write(f":SENS{self.n}:CORR:COLL:ADAP:DEL {value}")

        # SENSe<Ch>:CORRection:COLLect:ADAPter:DELay?
        def get_adapter_delay(self) -> float:
            """
            Get the approximate delay value of an adapter for removal/insertion.

            Parameter:
                None

            Return:
                float: Delay value in seconds
            """
            return float(self.instrument.query(f":SENS{self.n}:CORR:COLL:ADAP:DEL?"))

        # SENSe<Ch>:CORRection:COLLect:ADAPter:LENGth <numeric>
        def set_adapter_length(self, value: float):
            """
            Set the approximate mechanical length of an adapter for removal/insertion.

            Parameter:
                value (float): Length value in meters (negative for removal, positive for insertion)

            Return:
                None
            """
            self.instrument.write(f":SENS{self.n}:CORR:COLL:ADAP:LENG {value}")

        # SENSe<Ch>:CORRection:COLLect:ADAPter:LENGth?
        def get_adapter_length(self) -> float:
            """
            Get the approximate mechanical length of an adapter for removal/insertion.

            Parameter:
                None

            Return:
                float: Length value in meters
            """
            return float(self.instrument.query(f":SENS{self.n}:CORR:COLL:ADAP:LENG?"))
    

        # SENSe<Ch>:CORRection:COLLect:ADAPter:UNIT {SEConds|METers}
        def set_delay_unit(self, unit: str):
            """
            Set the display units of the adapter delay (length) in the adapter removal/insertion function.

            Parameter:
                unit (str): 'SEConds' or 'METers'

            Return:
                None
            """
            allowed = ['SEConds', 'METers']
            if unit not in allowed:
                raise ValueError(f"unit must be one of {allowed}")
            self.instrument.write(f":SENS{self.n}:CORR:COLL:ADAP:UNIT {unit}")

        # SENSe<Ch>:CORRection:COLLect:ADAPter:UNIT?
        def get_delay_unit(self) -> str:
            """
            Get the display units of the adapter delay (length) in the adapter removal/insertion function.

            Parameter:
                None

            Return:
                str: 'SEC' or 'MET'
            """
            return self.instrument.query(f":SENS{self.n}:CORR:COLL:ADAP:UNIT?").strip()

        # SENSe<Ch>:CORRection:COLLect:ADAPter:MEDia {COAXial|WAVeguide}
        def set_media(self, media: str):
            """
            Specify the adapter media in the adapter removal/insertion function.

            Parameter:
                media (str): 'COAXial' or 'WAVeguide'

            Return:
                None
            """
            allowed = ['COAXial', 'WAVeguide']
            if media not in allowed:
                raise ValueError(f"media must be one of {allowed}")
            self.instrument.write(f":SENS{self.n}:CORR:COLL:ADAP:MED {media}")

        # SENSe<Ch>:CORRection:COLLect:ADAPter:MEDia?
        def get_media(self) -> str:
            """
            Get the adapter media in the adapter removal/insertion function.

            Parameter:
                None

            Return:
                str: 'COAX' or 'WAV'
            """
            return self.instrument.query(f":SENS{self.n}:CORR:COLL:ADAP:MED?").strip()

        # SENSe<Ch>:CORRection:COLLect:ADAPter:PERMittivity <numeric>
        def set_permittivity(self, value: float):
            """
            Set the value of the permittivity of an adapter media in the adapter removal/insertion function.

            Parameter:
                value (float): Permittivity value

            Return:
                None
            """
            self.instrument.write(f":SENS{self.n}:CORR:COLL:ADAP:PERM {value}")

        # SENSe<Ch>:CORRection:COLLect:ADAPter:PERMittivity?
        def get_permittivity(self) -> float:
            """
            Get the value of the permittivity of an adapter media in the adapter removal/insertion function.

            Parameter:
                None

            Return:
                float: Permittivity value
            """
            return float(self.instrument.query(f":SENS{self.n}:CORR:COLL:ADAP:PERM?"))

        # SENSe<Ch>:CORRection:COLLect:ADAPter:WAVeguide:CUToff <numeric>
        def set_waveguide_cutoff_frequency(self, value: float):
            """
            Set the value of the cutoff frequency of the waveguide adapter.

            Parameter:
                value (float): Cutoff frequency in Hz

            Return:
                None
            """
            self.instrument.write(f":SENS{self.n}:CORR:COLL:ADAP:WAV:CUT {value}")

        # SENSe<Ch>:CORRection:COLLect:ADAPter:WAVeguide:CUToff?
        def get_waveguide_cutoff_frequency(self) -> float:
            """
            Get the value of the cutoff frequency of the waveguide adapter.

            Parameter:
                None

            Return:
                float: Cutoff frequency in Hz
            """
            return float(self.instrument.query(f":SENS{self.n}:CORR:COLL:ADAP:WAV:CUT?"))

        # SENSe<Ch>:CORRection:COLLect:METHod:ADAPter:REMoval <port>
        def set_removal_port(self, port: int):
            """
            Select the port number and set the adapter removal/insertion function for calibration coefficient calculation.

            Parameter:
                port (int): Port number (1-4)

            Return:
                None
            """
            if not (1 <= port <= 4):
                raise ValueError("port must be 1-4")
            self.instrument.write(f":SENS{self.n}:CORR:COLL:METH:ADAP:REM {port}")

    class Calibration:
        """ addition Calibration commands for the instrument. """
        def __init__(self, instrument, data_handler, channel):
            self.instrument = instrument
            self.data_handler = data_handler
            self.n = channel
            self.correction = self.Correction(instrument, data_handler, channel)
            
            self.extension = self.Extension(instrument, data_handler, channel)
            self.auto_impedance = self.AutoImpedance(instrument, data_handler, channel)
            self.offset = self.Offset(instrument, data_handler, channel)
            self.receiver = self.Receiver(instrument, data_handler, channel)
            self.cable_in_time_domain = self.CableInTimeDomain(instrument, data_handler, channel)
            self.trigger = self.Trigger(instrument, data_handler, channel)
            self.type = self.Type(instrument, data_handler, channel)
            self.data = self.Data(instrument, data_handler, channel)
            self.kit = self.Kit(instrument, data_handler, channel)
            self.method = self.Method(instrument, data_handler, channel)
            self.save = self.Save(instrument, data_handler, channel)
            self.trl = self.TRL(instrument, data_handler, channel)
            self.vmc = self.VMC(instrument, data_handler, channel)
            self.collection = self.Collection(instrument, data_handler, channel)
            self.auto_cal = self.AutoCal(instrument, data_handler, channel)
            self.auto_cal2 = self.AutoCal2(instrument, data_handler, channel)
            
            self.isolation = self.Isolation(instrument, data_handler, channel)
            self.load = self.Load(instrument, data_handler, channel)
            self.open = self.Open(instrument, data_handler, channel)
            self.short = self.Short(instrument, data_handler, channel)
            self.thru = self.Thru(instrument, data_handler, channel)
            
            self.subclass = self.SubClass(instrument, data_handler, channel)
            

        # SENSe<Ch>:CORRection:COEFficient:METHod:ERESponse = Ports
        def set_eresponse(self, rcvport: int, srcport: int):
            """
            Set the response calibration (ERESponse) type for written calibration coefficients.

            Parameter:
                rcvport (int): Receiver port number (1-4)
                srcport (int): Source port number (1-4)

            Return:
                None
            """
            if not (1 <= rcvport <= 4 and 1 <= srcport <= 4):
                raise ValueError("rcvport and srcport must be 1-4")
            if rcvport == srcport:
                raise ValueError("rcvport and srcport must be different for ERESponse")
            self.instrument.write(f":SENS{self.n}:CORR:COEF:METH:ERES {rcvport},{srcport}")

        # SENSe<Ch>:CORRection:COEFficient:METHod[:RESPonse]:OPEN <port>
        def set_response_open(self, port: int):
            """
            Set the response calibration (Open) type for written calibration coefficients.

            Parameter:
                port (int): Port number (1-4)

            Return:
                None
            """
            if not (1 <= port <= 4):
                raise ValueError("port must be 1-4")
            self.instrument.write(f":SENS{self.n}:CORR:COEF:METH:RESP:OPEN {port}")

        # SENSe<Ch>:CORRection:COEFficient:METHod[:RESPonse]:SHORt <port>
        def set_response_short(self, port: int):
            """
            Set the response calibration (Short) type for written calibration coefficients.

            Parameter:
                port (int): Port number (1-4)

            Return:
                None
            """
            if not (1 <= port <= 4):
                raise ValueError("port must be 1-4")
            self.instrument.write(f":SENS{self.n}:CORR:COEF:METH:RESP:SHOR {port}")

        # SENSe<Ch>:CORRection:COEFficient:METHod:SOLT1 <port>
        def set_solt1(self, port: int):
            """
            Set the full one-port calibration type for written calibration coefficients.

            Parameter:
                port (int): Port number (1-4)

            Return:
                None
            """
            if not (1 <= port <= 4):
                raise ValueError("port must be 1-4")
            self.instrument.write(f":SENS{self.n}:CORR:COEF:METH:SOLT1 {port}")

        # SENSe<Ch>:CORRection:COEFficient:METHod:SOLT2 <port1>,<port2>
        def set_solt2(self, port1: int, port2: int):
            """
            Set the full two-port calibration type for written calibration coefficients.

            Parameter:
                port1 (int): First port number (1-4)
                port2 (int): Second port number (1-4)

            Return:
                None
            """
            if not (1 <= port1 <= 4 and 1 <= port2 <= 4):
                raise ValueError("port1 and port2 must be 1-4")
            if port1 == port2:
                raise ValueError("port1 and port2 must be different for SOLT2")
            self.instrument.write(f":SENS{self.n}:CORR:COEF:METH:SOLT2 {port1},{port2}")

        # SENSe<Ch>:CORRection:COEFficient:METHod:SOLT3 <port1>,<port2>,<port3>
        def set_solt3(self, port1: int, port2: int, port3: int):
            """
            Set the full three-port calibration type for written calibration coefficients.

            Parameter:
                port1 (int): First port number (1-4)
                port2 (int): Second port number (1-4)
                port3 (int): Third port number (1-4)

            Return:
                None
            """
            ports = [port1, port2, port3]
            if any(not (1 <= p <= 4) for p in ports):
                raise ValueError("All ports must be 1-4")
            if len(set(ports)) != 3:
                raise ValueError("All ports must be different for SOLT3")
            self.instrument.write(f":SENS{self.n}:CORR:COEF:METH:SOLT3 {port1},{port2},{port3}")
            # SENSe<Ch>:CORRection:COEFficient:METHod:SOLT4 <port1>,<port2>,<port3>,<port4>
        def set_solt4(self, port1: int, port2: int, port3: int, port4: int):
            """
            Set the full four-port calibration type for written calibration coefficients.

            Parameter:
                port1 (int): First port number (1-4)
                port2 (int): Second port number (1-4)
                port3 (int): Third port number (1-4)
                port4 (int): Fourth port number (1-4)

            Return:
                None
            """
            ports = [port1, port2, port3, port4]
            if any(not (1 <= p <= 4) for p in ports):
                raise ValueError("All ports must be 1-4")
            if len(set(ports)) != 4:
                raise ValueError("All ports must be different for SOLT4")
            self.instrument.write(f":SENS{self.n}:CORR:COEF:METH:SOLT4 {port1},{port2},{port3},{port4}")

        # SENSe<Ch>:CORRection:COEFficient:METHod[:RESPonse]:THRU <rcvport>,<srcport>
        def set_response_thru(self, rcvport: int, srcport: int):
            """
            Set the response calibration (Thru) type for written calibration coefficients.

            Parameter:
                rcvport (int): Receiver port number (1-4)
                srcport (int): Source port number (1-4)

            Return:
                None
            """
            if not (1 <= rcvport <= 4 and 1 <= srcport <= 4):
                raise ValueError("rcvport and srcport must be 1-4")
            if rcvport == srcport:
                raise ValueError("rcvport and srcport must be different for THRU")
            self.instrument.write(f":SENS{self.n}:CORR:COEF:METH:RESP:THRU {rcvport},{srcport}")

        # SENSe<Ch>:CORRection:COEFficient:SAVE
        def save_coefficients(self):
            """
            Enable the written calibration coefficients depending on the selected calibration type.

            Parameter:
                None

            Return:
                None
            """
            self.instrument.write(f":SENS{self.n}:CORR:COEF:SAVE")

        class Correction:
            """
            Correction related commands.
            """
        
            def __init__(self, instrument, data_handler, channel):
                self.instrument = instrument
                self.data_handler = data_handler
                self.n = channel
                self.offset = self.Offset(instrument, data_handler, channel)
                self.coefficient = self.Coefficient(instrument, data_handler, channel)
                self.extension = self.Extension(instrument, data_handler, channel)
                self.error = self.Error(instrument, data_handler, channel)
            class Offset:
                """
                Scalar mixer calibration and offset correction commands.
                """
                def __init__(self, instrument, data_handler, channel):
                    self.instrument = instrument
                    self.data_handler = data_handler
                    self.n = channel

                # SENS:CORR:OFFS:CLE - Clears calibration coefficient table
                def clear_calibration_coefficient_table(self):
                    """
                    Clear the calibration coefficient table.

                    Parameter:
                        None

                    Return:
                        None
                    """
                    self.instrument.write(f":SENS{self.n}:CORR:OFFS:CLE")

                # SENS:CORR:OFFS:COLL:CLE - Clears calibration data
                def clear_offset_calibration_data(self):
                    """
                    Clear the calibration data for offset correction.

                    Parameter:
                        None

                    Return:
                        None
                    """
                    self.instrument.write(f":SENS{self.n}:CORR:OFFS:COLL:CLE")

                # SENS:CORR:OFFS:COLL:DIR - Calibration direction
                def set_calibration_direction(self, direction: str):
                    """
                    Set the calibration direction for offset correction.

                    Parameter:
                        direction (str): Calibration direction, one of ['FORW', 'REV']

                    Return:
                        None
                    """
                    allowed = ['FORW', 'REV']
                    if direction not in allowed:
                        raise ValueError(f"direction must be one of {allowed}")
                    self.instrument.write(f":SENS{self.n}:CORR:OFFS:COLL:DIR {direction}")

                def get_calibration_direction(self) -> str:
                    """
                    Get the calibration direction for offset correction.

                    Parameter:
                        None

                    Return:
                        str: Calibration direction
                    """
                    return self.instrument.query(f":SENS{self.n}:CORR:OFFS:COLL:DIR?").strip()

                # SENS:CORR:OFFS:COLL:ECAL - Measure all standards using ACM
                def measure_all_standards_acm(self):
                    """
                    Measure all standards using the Automatic Calibration Module (ACM).

                    Parameter:
                        None

                    Return:
                        None
                    """
                    self.instrument.write(f":SENS{self.n}:CORR:OFFS:COLL:ECAL")

                # SENS:CORR:OFFS:COLL:LOAD - Measure the Load standard
                def measure_load_standard(self):
                    """
                    Measure the Load standard for offset correction.

                    Parameter:
                        None

                    Return:
                        None
                    """
                    self.instrument.write(f":SENS{self.n}:CORR:OFFS:COLL:LOAD")

                # SENS:CORR:OFFS:COLL:METH:SMIX2 - Calibration port
                def set_scalar_mixer_calibration_port(self, port: int):
                    """
                    Set the calibration port for scalar mixer calibration.

                    Parameter:
                        port (int): Port number

                    Return:
                        None
                    """
                    self.instrument.write(f":SENS{self.n}:CORR:OFFS:COLL:METH:SMIX2 {port}")

                def get_scalar_mixer_calibration_port(self) -> int:
                    """
                    Get the calibration port for scalar mixer calibration.

                    Parameter:
                        None

                    Return:
                        int: Port number
                    """
                    return int(self.instrument.query(f":SENS{self.n}:CORR:OFFS:COLL:METH:SMIX2?"))

                # SENS:CORR:OFFS:COLL:OPEN - Measure the Open standard
                def measure_open_standard(self):
                    """
                    Measure the Open standard for offset correction.

                    Parameter:
                        None

                    Return:
                        None
                    """
                    self.instrument.write(f":SENS{self.n}:CORR:OFFS:COLL:OPEN")

                # SENS:CORR:OFFS:COLL:PMET - Measure power
                def measure_power(self):
                    """
                    Measure power for offset correction.

                    Parameter:
                        None

                    Return:
                        None
                    """
                    self.instrument.write(f":SENS{self.n}:CORR:OFFS:COLL:PMET")

                # SENS:CORR:OFFS:COLL:SHOR - Measure the Short standard
                def measure_short_standard(self):
                    """
                    Measure the Short standard for offset correction.

                    Parameter:
                        None

                    Return:
                        None
                    """
                    self.instrument.write(f":SENS{self.n}:CORR:OFFS:COLL:SHOR")

                # SENS:CORR:OFFS:COLL:THRU - Measure the Thru standard
                def measure_thru_standard(self):
                    """
                    Measure the Thru standard for offset correction.

                    Parameter:
                        None

                    Return:
                        None
                    """
                    self.instrument.write(f":SENS{self.n}:CORR:OFFS:COLL:THRU")

                # SENS:CORR:OFFS:COLL:SAVE - Completes calibration
                def complete_offset_calibration(self):
                    """
                    Complete the offset calibration.

                    Parameter:
                        None

                    Return:
                        None
                    """
                    self.instrument.write(f":SENS{self.n}:CORR:OFFS:COLL:SAVE")

            class Coefficient:
                """
                Calibration and correction coefficient table and data commands.
                """
                def __init__(self, instrument, data_handler, channel):
                    self.instrument = instrument
                    self.data_handler = data_handler
                    self.n = channel

                # SENSe<Ch>:CORRection:CLEar
                def clear_correction_table(self):
                    """
                    Clear the calibration coefficient table.

                    Parameter:
                        None

                    Return:
                        None
                    """
                    self.instrument.write(f":SENS{self.n}:CORR:CLE")

                # SENSe<Ch>:CORRection:COEFficient[:DATA] <char>,<rcvport>,<srcport>,<numeric list>
                def set_correction_coefficient_data(self, term: str, rcvport: int, srcport: int, coeffs):
                    """
                    Write the calibration coefficient data array.

                    Parameter:
                        term (str): Error term, one of ['ER', 'ED', 'ES', 'ET', 'EX', 'EL']
                        rcvport (int): Receiver port number (1-4)
                        srcport (int): Source port number (1-4)
                        coeffs (list): Calibration coefficient array (2N values)

                    Return:
                        None
                    """
                    allowed_terms = ['ER', 'ED', 'ES', 'ET', 'EX', 'EL']
                    if term not in allowed_terms:
                        raise ValueError(f"term must be one of {allowed_terms}")
                    if not (1 <= rcvport <= 4 and 1 <= srcport <= 4):
                        raise ValueError("rcvport and srcport must be 1-4")
                    coeffs_str = ",".join(str(float(x)) for x in coeffs)
                    self.instrument.write(f":SENS{self.n}:CORR:COEF:DATA {term},{rcvport},{srcport},{coeffs_str}")

                # SENSe<Ch>:CORRection:COEFficient[:DATA]? <char>,<rcvport>,<srcport>
                def get_correction_coefficient_data(self, term: str, rcvport: int, srcport: int):
                    """
                    Read out the calibration coefficient data array.

                    Parameter:
                        term (str): Error term, one of ['ER', 'ED', 'ES', 'ET', 'EX', 'EL']
                        rcvport (int): Receiver port number (1-4)
                        srcport (int): Source port number (1-4)

                    Return:
                        list: Calibration coefficient array (2N values)
                    """
                    allowed_terms = ['ER', 'ED', 'ES', 'ET', 'EX', 'EL']
                    if term not in allowed_terms:
                        raise ValueError(f"term must be one of {allowed_terms}")
                    if not (1 <= rcvport <= 4 and 1 <= srcport <= 4):
                        raise ValueError("rcvport and srcport must be 1-4")
                    data = self.instrument.query(f":SENS{self.n}:CORR:COEF:DATA? {term},{rcvport},{srcport}")
                    if self.data_handler.is_auto_saving_data_enabled():
                        self.data_handler.write_to_file(self, f"CALIB_COEFFECIENTS_{self.n}", data, file_type = EFileType.CSV)
                    return self.data_handler.parse_array(data)

                # SENSe<Ch>:CORRection:COEFficient:METHod:ERESponse <rcvport>,<srcport>
                def set_coefficient_method_eresponse(self, rcvport: int, srcport: int):
                    """
                    Set the 1-path 2-port calibration type for written calibration coefficients.

                    Parameter:
                        rcvport (int): Receiver port number (1-4)
                        srcport (int): Source port number (1-4)

                    Return:
                        None
                    """
                    if not (1 <= rcvport <= 4 and 1 <= srcport <= 4):
                        raise ValueError("rcvport and srcport must be 1-4")
                    if rcvport == srcport:
                        raise ValueError("rcvport and srcport must be different for ERESponse")
                    self.instrument.write(f":SENS{self.n}:CORR:COEF:METH:ERES {rcvport},{srcport}")
            class Extension:
                """
                Port extension correction related commands.
                """
                def __init__(self, instrument, data_handler, channel):
                    self.instrument = instrument
                    self.data_handler = data_handler
                    self.n = channel

                # SENS:CORR:EXT - Port extension ON/OFF
                def enable_port_extension(self, enable: bool):
                    """
                    Enable or disable port extension.

                    Parameter:
                        enable (bool): True to enable, False to disable"""
                    self.instrument.write(f":SENS{self.n}:CORR:EXT {1 if enable else 0}")
                def is_port_extension_enabled(self) -> bool:
                    """
                    Query if port extension is enabled.

                    Parameter:
                        None

                    Return:
                        bool: True if enabled, False otherwise
                    """
                    return bool(int(self.instrument.query(f":SENS{self.n}:CORR:EXT?")))

                # SENS:CORR:EXT:PORT:FREQ - Values of "Frequency1" and "Frequency2"
                def get_port_extension_frequencies(self):
                    """
                    Get the values of Frequency1 and Frequency2 for port extension.

                    Parameter:
                        None

                    Return:
                        tuple: (Frequency1, Frequency2)
                    """
                    data = self.instrument.query(f":SENS{self.n}:CORR:EXT:PORT:FREQ?").strip()
                    return tuple(map(float, data.split(',')))

                # SENS:CORR:EXT:PORT:INCL - Loss compensation ON/OFF
                def enable_loss_compensation(self, enable: bool):
                    """
                    Enable or disable loss compensation for port extension.

                    Parameter:
                        enable (bool): True to enable, False to disable

                    Return:
                        None
                    """
                    self.instrument.write(f":SENS{self.n}:CORR:EXT:PORT:INCL {1 if enable else 0}")

                def is_loss_compensation_enabled(self) -> bool:
                    """
                    Query if loss compensation for port extension is enabled.

                    Parameter:
                        None

                    Return:
                        bool: True if enabled, False otherwise
                    """
                    return bool(int(self.instrument.query(f":SENS{self.n}:CORR:EXT:PORT:INCL?")))

                # SENS:CORR:EXT:PORT:LDC - Value "Loss at DC"
                def set_loss_at_dc(self, value: float):
                    """
                    Set the value of "Loss at DC" for port extension.

                    Parameter:
                        value (float): Loss at DC

                    Return:
                        None
                    """
                    self.instrument.write(f":SENS{self.n}:CORR:EXT:PORT:LDC {value}")

                def get_loss_at_dc(self) -> float:
                    """
                    Get the value of "Loss at DC" for port extension.

                    Parameter:
                        None

                    Return:
                        float: Loss at DC
                    """
                    return float(self.instrument.query(f":SENS{self.n}:CORR:EXT:PORT:LDC?"))

                # SENS:CORR:EXT:PORT:LOSS - Values of "Loss 1" and "Loss 2"
                def set_loss_values(self, loss1: float, loss2: float):
                    """
                    Set the values of "Loss 1" and "Loss 2" for port extension.

                    Parameter:
                        loss1 (float): Loss 1
                        loss2 (float): Loss 2

                    Return:
                        None
                    """
                    self.instrument.write(f":SENS{self.n}:CORR:EXT:PORT:LOSS {loss1},{loss2}")

                def get_loss_values(self):
                    """
                    Get the values of "Loss 1" and "Loss 2" for port extension.

                    Parameter:
                        None

                    Return:
                        tuple: (Loss 1, Loss 2)
                    """
                    data = self.instrument.query(f":SENS{self.n}:CORR:EXT:PORT:LOSS?").strip()
                    return tuple(map(float, data.split(',')))

                # SENS:CORR:EXT:PORT:TIME - Extension Port n
                def set_extension_time(self, value: float):
                    """
                    Set the extension time for port extension.

                    Parameter:
                        value (float): Extension time

                    Return:
                        None
                    """
                    self.instrument.write(f":SENS{self.n}:CORR:EXT:PORT:TIME {value}")

                def get_extension_time(self) -> float:
                    """
                    Get the extension time for port extension.

                    Parameter:
                        None

                    Return:
                        float: Extension time
                    """
                    return float(self.instrument.query(f":SENS{self.n}:CORR:EXT:PORT:TIME?"))

            class Error:
                """
                S-parameter error correction ON/OFF.
                """
                def __init__(self, instrument, data_handler, channel):
                    self.instrument = instrument
                    self.data_handler = data_handler
                    self.n = channel

                # SENSe<Ch>:CORRection:STATe {OFF|ON|0|1}
                def set_error_correction_state(self, enable: bool):
                    """
                    Turn S-parameter error correction ON/OFF.

                    Parameter:
                        enable (bool): True to enable, False to disable

                    Return:
                        None
                    """
                    self.instrument.write(f":SENS{self.n}:CORR:STAT {1 if enable else 0}")

                # SENSe<Ch>:CORRection:STATe?
                def is_error_correction_enabled(self) -> bool:
                    """
                    Query if S-parameter error correction is enabled.

                    Parameter:
                        None

                    Return:
                        bool: True if enabled, False otherwise
                    """
                    return bool(int(self.instrument.query(f":SENS{self.n}:CORR:STAT?")))

            # SENS:CORR:CLE - Clears the table of calibration factors
            def clear_calibration_factors(self):
                """
                Clear the table of calibration factors.

                Parameter:
                    None

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:CORR:CLE")

            # SENS:CORR:COLL:CLE - Clears data of calibration standards
            def clear_calibration_standards(self):
                """
                Clear data of calibration standards.

                Parameter:
                    None

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:CORR:COLL:CLE")

            # SENS:CORR:INF? - Information string of calibration
            def get_calibration_info(self) -> str:
                """
                Get information string of calibration.

                Parameter:
                    None

                Return:
                    str: Calibration information
                """
                return self.instrument.query(f":SENS{self.n}:CORR:INF?").strip()

            # SENS:CORR:STAT - S-parameter error correction state
            def set_error_correction_state(self, enable: bool):
                """
                Set S-parameter error correction state.

                Parameter:
                    enable (bool): True to enable, False to disable

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:CORR:STAT {1 if enable else 0}")

            def is_error_correction_enabled(self) -> bool:
                """
                Query if S-parameter error correction is enabled.

                Parameter:
                    None

                Return:
                    bool: True if enabled, False otherwise
                """
                return bool(int(self.instrument.query(f":SENS{self.n}:CORR:STAT?")))

            # SENS:CORR:TRIG:FREE - Calibration trigger source
            def set_calibration_trigger_source(self, source: str):
                """
                Set calibration trigger source.

                Parameter:
                    source (str): Trigger source, one of ['FREE', 'EXT']

                Return:
                    None
                """
                allowed = ['FREE', 'EXT']
                if source not in allowed:
                    raise ValueError(f"source must be one of {allowed}")
                self.instrument.write(f":SENS{self.n}:CORR:TRIG:FREE {source}")

            def get_calibration_trigger_source(self) -> str:
                """
                Get calibration trigger source.

                Parameter:
                    None

                Return:
                    str: Trigger source
                """
                return self.instrument.query(f":SENS{self.n}:CORR:TRIG:FREE?").strip()

            # SENS:CORR:TYPE? - Information about trace (calibration type, number of ports)
            def get_calibration_type_info(self) -> str:
                """
                Get information about trace (calibration type, number of ports).

                Parameter:
                    None

                Return:
                    str: Calibration type info
                """
                return self.instrument.query(f":SENS{self.n}:CORR:TYPE?").strip()
        
        class Data:
            """
            Calibration standard measurement data commands.
            """
            def __init__(self, instrument, data_handler, channel):
                self.instrument = instrument
                self.data_handler = data_handler
                self.n = channel

            # SENS:CORR:COLL:DATA:LOAD <port>,<numeric list>
            def set_load_standard_data(self, port: int, data_list):
                """
                Write the array of the load calibration standard measurement for the port.

                Parameter:
                    port (int): Port number (1-4)
                    data_list (list): Array of real/imaginary pairs

                Return:
                    None
                """
                if not (1 <= port <= 4):
                    raise ValueError("port must be 1-4")
                data_str = ",".join(str(float(x)) for x in data_list)
                self.instrument.write(f":SENS{self.n}:CORR:COLL:DATA:LOAD {port},{data_str}")

            # SENS:CORR:COLL:DATA:LOAD? <port>
            def get_load_standard_data(self, port: int):
                """
                Read out the array of the load calibration standard measurement for the port.

                Parameter:
                    port (int): Port number (1-4)

                Return:
                    list: Array of real/imaginary pairs
                """
                if not (1 <= port <= 4):
                    raise ValueError("port must be 1-4")
                data = self.instrument.query(f":SENS{self.n}:CORR:COLL:DATA:LOAD? {port}")
                if self.data_handler.is_auto_saving_data_enabled():
                    self.data_handler.write_to_file(self, f"CALIB_STANDARD", data, file_type = EFileType.CSV)
                return self.data_handler.parse_array(data)

            # SENS:CORR:COLL:DATA:OPEN <port>,<numeric list>
            def set_open_standard_data(self, port: int, data_list):
                """
                Write the array of the open calibration standard measurement for the port.

                Parameter:
                    port (int): Port number (1-2)
                    data_list (list): Array of real/imaginary pairs

                Return:
                    None
                """
                if not (1 <= port <= 2):
                    raise ValueError("port must be 1-2")
                data_str = ",".join(str(float(x)) for x in data_list)
                self.instrument.write(f":SENS{self.n}:CORR:COLL:DATA:OPEN {port},{data_str}")

            # SENS:CORR:COLL:DATA:OPEN? <port>
            def get_open_standard_data(self, port: int):
                """
                Read out the array of the open calibration standard measurement for the port.

                Parameter:
                    port (int): Port number (1-2)

                Return:
                    list: Array of real/imaginary pairs
                """
                if not (1 <= port <= 2):
                    raise ValueError("port must be 1-2")
                data = self.instrument.query(f":SENS{self.n}:CORR:COLL:DATA:OPEN? {port}")
                if self.data_handler.is_auto_saving_data_enabled():
                    self.data_handler.write_to_file(self, f"OPEN_CALIB_STAND_CH_{self.n}_PORT_{port}", data, file_type = EFileType.CSV)
                return self.data_handler.parse_array(data)

            # SENS:CORR:COLL:DATA:SHOR <port>,<numeric list>
            def set_short_standard_data(self, port: int, data_list):
                """
                Write the array of the short calibration standard measurement for the port.

                Parameter:
                    port (int): Port number (1-4)
                    data_list (list): Array of real/imaginary pairs

                Return:
                    None
                """
                if not (1 <= port <= 4):
                    raise ValueError("port must be 1-4")
                data_str = ",".join(str(float(x)) for x in data_list)
                self.instrument.write(f":SENS{self.n}:CORR:COLL:DATA:SHOR {port},{data_str}")

            # SENS:CORR:COLL:DATA:SHOR? <port>
            def get_short_standard_data(self, port: int):
                """
                Read out the array of the short calibration standard measurement for the port.

                Parameter:
                    port (int): Port number (1-4)

                Return:
                    list: Array of real/imaginary pairs
                """
                if not (1 <= port <= 4):
                    raise ValueError("port must be 1-4")
                data = self.instrument.query(f":SENS{self.n}:CORR:COLL:DATA:SHOR? {port}")
                if self.data_handler.is_auto_saving_data_enabled():
                    self.data_handler.write_to_file(self, f"SHORT_CALIB_CH{self.n}_PORT{port}", data, file_type = EFileType.CSV)
                return self.data_handler.parse_array(data)

            # SENS:CORR:COLL:DATA:THRU:MATC <rcvport>,<srcport>,<numeric list>
            def set_thru_match_data(self, rcvport: int, srcport: int, data_list):
                """
                Write the array of the reflection measurement of the thru standard.

                Parameter:
                    rcvport (int): Receiver port (1-4)
                    srcport (int): Source port (1-4)
                    data_list (list): Array of real/imaginary pairs

                Return:
                    None
                """
                if not (1 <= rcvport <= 4 and 1 <= srcport <= 4):
                    raise ValueError("rcvport and srcport must be 1-4")
                data_str = ",".join(str(float(x)) for x in data_list)
                self.instrument.write(f":SENS{self.n}:CORR:COLL:DATA:THRU:MATC {rcvport},{srcport},{data_str}")

            # SENS:CORR:COLL:DATA:THRU:MATC? <rcvport>,<srcport>
            def get_thru_match_data(self, rcvport: int, srcport: int):
                """
                Read out the array of the reflection measurement of the thru standard.

                Parameter:
                    rcvport (int): Receiver port (1-4)
                    srcport (int): Source port (1-4)

                Return:
                    list: Array of real/imaginary pairs
                """
                if not (1 <= rcvport <= 4 and 1 <= srcport <= 4):
                    raise ValueError("rcvport and srcport must be 1-4")
                data = self.instrument.query(f":SENS{self.n}:CORR:COLL:DATA:THRU:MATC? {rcvport},{srcport}")
                if self.data_handler.is_auto_saving_data_enabled():
                    self.data_handler.write_to_file(self, f"REFLECT_SRCPORT{srcport}_RCVPORT{rcvport}", data, file_type = EFileType.CSV)
                return self.data_handler.parse_array(data)

            # SENS:CORR:COLL:DATA:THRU:TRAN <rcvport>,<srcport>,<numeric list>
            def set_thru_transmission_data(self, rcvport: int, srcport: int, data_list):
                """
                Write the array of the transmission measurement using the thru standard.

                Parameter:
                    rcvport (int): Receiver port (1-4)
                    srcport (int): Source port (1-4)
                    data_list (list): Array of real/imaginary pairs

                Return:
                    None
                """
                if not (1 <= rcvport <= 4 and 1 <= srcport <= 4):
                    raise ValueError("rcvport and srcport must be 1-4")
                data_str = ",".join(str(float(x)) for x in data_list)
                self.instrument.write(f":SENS{self.n}:CORR:COLL:DATA:THRU:TRAN {rcvport},{srcport},{data_str}")

            # SENS:CORR:COLL:DATA:THRU:TRAN? <rcvport>,<srcport>
            def get_thru_transmission_data(self, rcvport: int, srcport: int):
                """
                Read out the array of the transmission measurement using the thru standard.

                Parameter:
                    rcvport (int): Receiver port (1-4)
                    srcport (int): Source port (1-4)

                Return:
                    list: Array of real/imaginary pairs
                """
                if not (1 <= rcvport <= 4 and 1 <= srcport <= 4):
                    raise ValueError("rcvport and srcport must be 1-4")
                data = self.instrument.query(f":SENS{self.n}:CORR:COLL:DATA:THRU:TRAN? {rcvport},{srcport}")
                if self.data_handler.is_auto_saving_data_enabled():
                    self.data_handler.write_to_file(self, f"TRANSM_MEAS{self.n}_{srcport}_RCVPORT{rcvport}", data, file_type = EFileType.CSV)
                return self.data_handler.parse_array(data)
            
        class Method:
            """
            addition Calibration collection method commands for calibration coefficient calculation.
            """
            def __init__(self, instrument, data_handler, channel):
                self.instrument = instrument
                self.data_handler = data_handler
                self.n = channel
                self.trl = self.TRL(instrument, data_handler, channel)

            # SENS:CORR:COLL:METH:ERES <rcvport>,<srcport>
            def set_eresponse(self, rcvport: int, srcport: int):
                """
                Selects the ports and sets the one path 2–port calibration type for the calculation of the calibration coefficients.

                Parameter:
                    rcvport (int): Receiver port number (1-4)
                    srcport (int): Source port number (1-4)

                Return:
                    None
                """
                if not (1 <= rcvport <= 4 and 1 <= srcport <= 4):
                    raise ValueError("rcvport and srcport must be 1-4")
                if rcvport == srcport:
                    raise ValueError("rcvport and srcport must be different for ERESponse")
                self.instrument.write(f":SENS{self.n}:CORR:COLL:METH:ERES {rcvport},{srcport}")

            # SENS:CORR:COLL:METH:OPEN <port>
            def set_response_open(self, port: int):
                """
                Selects the port and sets the response calibration (Open) type for the calculation of the calibration coefficients.

                Parameter:
                    port (int): Port number (1-4)

                Return:
                    None
                """
                if not (1 <= port <= 4):
                    raise ValueError("port must be 1-4")
                self.instrument.write(f":SENS{self.n}:CORR:COLL:METH:OPEN {port}")

            # SENS:CORR:COLL:METH:SHOR <port>
            def set_response_short(self, port: int):
                """
                Selects the port and sets the response calibration (Short) type for the calculation of the calibration coefficients.

                Parameter:
                    port (int): Port number (1-4)

                Return:
                    None
                """
                if not (1 <= port <= 4):
                    raise ValueError("port must be 1-4")
                self.instrument.write(f":SENS{self.n}:CORR:COLL:METH:SHOR {port}")

            # SENS:CORR:COLL:METH:SOLT1 <port>
            def set_solt1(self, port: int):
                """
                Selects the port and sets the full one-port (SOL) calibration type for the calculation of the calibration coefficients.

                Parameter:
                    port (int): Port number (1-4)

                Return:
                    None
                """
                if not (1 <= port <= 4):
                    raise ValueError("port must be 1-4")
                self.instrument.write(f":SENS{self.n}:CORR:COLL:METH:SOLT1 {port}")

            # SENS:CORR:COLL:METH:SOLT2 <port1>,<port2>
            def set_solt2(self, port1: int, port2: int):
                """
                Selects the ports and sets the full two-port (SOLT) calibration type for the calculation of the calibration coefficients.

                Parameter:
                    port1 (int): First port number (1-4)
                    port2 (int): Second port number (1-4)

                Return:
                    None
                """
                if not (1 <= port1 <= 4 and 1 <= port2 <= 4):
                    raise ValueError("port1 and port2 must be 1-4")
                if port1 == port2:
                    raise ValueError("port1 and port2 must be different for SOLT2")
                self.instrument.write(f":SENS{self.n}:CORR:COLL:METH:SOLT2 {port1},{port2}")

      

            # SENS:CORR:COLL:METH:SOLT3 <port1>,<port2>,<port3>
            def set_solt3(self, port1: int, port2: int, port3: int):
                """
                Selects the ports and sets the full three-port calibration type for the calculation of the calibration coefficients.

                Parameter:
                    port1 (int): First port number (1-4)
                    port2 (int): Second port number (1-4)
                    port3 (int): Third port number (1-4)

                Return:
                    None
                """
                ports = [port1, port2, port3]
                if any(not (1 <= p <= 4) for p in ports):
                    raise ValueError("All ports must be 1-4")
                if len(set(ports)) != 3:
                    raise ValueError("All ports must be different for SOLT3")
                self.instrument.write(f":SENS{self.n}:CORR:COLL:METH:SOLT3 {port1},{port2},{port3}")

            # SENS:CORR:COLL:METH:SOLT4 <port1>,<port2>,<port3>,<port4>
            def set_solt4(self, port1: int, port2: int, port3: int, port4: int):
                """
                Selects the ports and sets the full four-port calibration type for the calculation of the calibration coefficients.

                Parameter:
                    port1 (int): First port number (1-4)
                    port2 (int): Second port number (1-4)
                    port3 (int): Third port number (1-4)
                    port4 (int): Fourth port number (1-4)

                Return:
                    None
                """
                ports = [port1, port2, port3, port4]
                if any(not (1 <= p <= 4) for p in ports):
                    raise ValueError("All ports must be 1-4")
                if len(set(ports)) != 4:
                    raise ValueError("All ports must be different for SOLT4")
                self.instrument.write(f":SENS{self.n}:CORR:COLL:METH:SOLT4 {port1},{port2},{port3},{port4}")

            # SENS:CORR:COLL:METH:THRU <rcvport>,<srcport>
            def set_response_thru(self, rcvport: int, srcport: int):
                """
                Selects the ports and sets the response calibration (Thru) type for the calculation of the calibration coefficients.

                Parameter:
                    rcvport (int): Receiver port number (1-4)
                    srcport (int): Source port number (1-4)

                Return:
                    None
                """
                if not (1 <= rcvport <= 4 and 1 <= srcport <= 4):
                    raise ValueError("rcvport and srcport must be 1-4")
                if rcvport == srcport:
                    raise ValueError("rcvport and srcport must be different for THRU")
                self.instrument.write(f":SENS{self.n}:CORR:COLL:METH:THRU {rcvport},{srcport}")

            


            class TRL:
                """
                Calibration collection method commands for TRL calibration types.
                """
                def __init__(self, instrument, data_handler, channel):
                    self.instrument = instrument
                    self.data_handler = data_handler
                    self.n = channel
                # SENS:CORR:COLL:METH:TRL:MULTiline[:STATe] {OFF|ON|0|1}
                def enable_trl_multiline(self, enable: bool):
                    """
                    Turns the multi-line TRL option ON/OFF for calibration coefficient calculation.

                    Parameter:
                        enable (bool): True to enable, False to disable

                    Return:
                        None
                    """
                    self.instrument.write(f":SENS{self.n}:CORR:COLL:METH:TRL:MULT:STAT {1 if enable else 0}")

                def is_trl_multiline_enabled(self) -> bool:
                    """
                    Query if the multi-line TRL option is enabled for calibration coefficient calculation.

                    Parameter:
                        None

                    Return:
                        bool: True if enabled, False otherwise
                    """
                    return bool(int(self.instrument.query(f":SENS{self.n}:CORR:COLL:METH:TRL:MULT:STAT?")))
                
                # SENS:CORR:COLL:METH:TRL2 <port1>,<port2>
                def set_trl2(self, port1: int, port2: int):
                    """
                    Select the ports and set the two-port TRL calibration type for the calculation of the calibration coefficients.

                    Parameter:
                        port1 (int): First port number (1-4)
                        port2 (int): Second port number (1-4)

                    Return:
                        None
                    """
                    if not (1 <= port1 <= 4 and 1 <= port2 <= 4):
                        raise ValueError("port1 and port2 must be 1-4")
                    if port1 == port2:
                        raise ValueError("port1 and port2 must be different for TRL2")
                    self.instrument.write(f":SENS{self.n}:CORR:COLL:METH:TRL2 {port1},{port2}")

                # SENS:CORR:COLL:METH:TRL3 <port1>,<port2>,<port3>
                def set_trl3(self, port1: int, port2: int, port3: int):
                    """
                    Select the ports and set the three-port TRL calibration type for the calculation of the calibration coefficients.

                    Parameter:
                        port1 (int): First port number (1-4)
                        port2 (int): Second port number (1-4)
                        port3 (int): Third port number (1-4)

                    Return:
                        None
                    """
                    ports = [port1, port2, port3]
                    if any(not (1 <= p <= 4) for p in ports):
                        raise ValueError("All ports must be 1-4")
                    if len(set(ports)) != 3:
                        raise ValueError("All ports must be different for TRL3")
                    self.instrument.write(f":SENS{self.n}:CORR:COLL:METH:TRL3 {port1},{port2},{port3}")

                # SENS:CORR:COLL:METH:TRL4 <port1>,<port2>,<port3>,<port4>
                def set_trl4(self, port1: int, port2: int, port3: int, port4: int):
                    """
                    Select the ports and set the four-port TRL calibration type for the calculation of the calibration coefficients.

                    Parameter:
                        port1 (int): First port number (1-4)
                        port2 (int): Second port number (1-4)
                        port3 (int): Third port number (1-4)
                        port4 (int): Fourth port number (1-4)

                    Return:
                        None
                    """
                    ports = [port1, port2, port3, port4]
                    if any(not (1 <= p <= 4) for p in ports):
                        raise ValueError("All ports must be 1-4")
                    if len(set(ports)) != 4:
                        raise ValueError("All ports must be different for TRL4")
                    self.instrument.write(f":SENS{self.n}:CORR:COLL:METH:TRL4 {port1},{port2},{port3},{port4}")

                # SENS:CORR:COLL:METH:TYPE?
                def get_calibration_method_type(self) -> str:
                    """
                    Read out the calibration method selected for the calculation of the calibration coefficients.

                    Parameter:
                        None

                    Return:
                        str: Calibration method type (e.g., 'RESPO', 'RESPS', 'RESPT', 'SOLT1', 'SOLT2', '1PATH', 'NONE')
                    """
                    return self.instrument.query(f":SENS{self.n}:CORR:COLL:METH:TYPE?").strip()

        class Save:
            """
            Calibration collection save commands.
            """
            def __init__(self, instrument, data_handler, channel):
                self.instrument = instrument
                self.data_handler = data_handler
                self.n = channel
                self.simplified = self.Simplified(instrument, data_handler, channel)
            # SENS:CORR:COLL:SAVE
            def save_calibration_collection(self):
                """
                Calculate the calibration coefficients from the calibration standards measurements depending on the selected calibration type.

                Parameter:
                    None

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:CORR:COLL:SAVE")

            class Simplified:
                """
                addition Simplified calibration collection save commands.
                """
                def __init__(self, instrument, data_handler, channel):
                    self.instrument = instrument
                    self.data_handler = data_handler
                    self.n = channel

                # SENS:CORR:COLL:SIMP:SAVE
                def save_simplified_calibration_collection(self):
                    """
                    Calculate the calibration coefficients for the simplified three- or four-port calibration from the calibration standards measurements.

                    Parameter:
                        None

                    Return:
                        None
                    """
                    self.instrument.write(f":SENS{self.n}:CORR:COLL:SIMP:SAVE")

        class Thru:
            """
            addition Thru addition calibration commands.
            """
            def __init__(self, instrument, data_handler, channel):
                self.instrument = instrument
                self.data_handler = data_handler
                self.n = channel
                self.waveguide = self.Waveguide(instrument, data_handler, channel)
                self.full2port = self.Full2Port(instrument, data_handler, channel)
                self.full3port = self.Full3Port(instrument, data_handler, channel)
                self.full4port = self.Full4Port(instrument, data_handler, channel)

            # SENS:CORR:COLL:THRU <rcvport>,<srcport>
            def measure_thru(self, rcvport: int, srcport: int):
                """
                Measures the calibration data of the thru standard between the receiver port and the source port.

                Parameter:
                    rcvport (int): Receiver port number (1-4)
                    srcport (int): Source port number (1-4)

                Return:
                    None
                """
                if not (1 <= rcvport <= 4 and 1 <= srcport <= 4):
                    raise ValueError("rcvport and srcport must be 1-4")
                if rcvport == srcport:
                    raise ValueError("rcvport and srcport must be different")
                self.instrument.write(f":SENS{self.n}:CORR:COLL:THRU {rcvport},{srcport}")

            # SENSe<Ch>:CORRection:COLLect:THRU:ADDition:DELay <numeric>
            def set_addition_delay(self, value: float):
                """
                Set the approximate delay value of an unknown thru in the thru addition function.

                Parameter:
                    value (float): Delay value in seconds

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:CORR:COLL:THRU:ADD:DEL {value}")

            # SENSe<Ch>:CORRection:COLLect:THRU:ADDition:DELay?
            def get_addition_delay(self) -> float:
                """
                Get the approximate delay value of an unknown thru in the thru addition function.

                Parameter:
                    None

                Return:
                    float: Delay value in seconds
                """
                return float(self.instrument.query(f":SENS{self.n}:CORR:COLL:THRU:ADD:DEL?"))

            # SENSe<Ch>:CORRection:COLLect:THRU:ADDition:LENGth <numeric>
            def set_addition_length(self, value: float):
                """
                Set the approximate mechanical length of an unknown thru in the thru addition function.

                Parameter:
                    value (float): Length value in meters

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:CORR:COLL:THRU:ADD:LENG {value}")

            # SENSe<Ch>:CORRection:COLLect:THRU:ADDition:LENGth?
            def get_addition_length(self) -> float:
                """
                Get the approximate mechanical length of an unknown thru in the thru addition function.

                Parameter:
                    None

                Return:
                    float: Length value in meters
                """
                return float(self.instrument.query(f":SENS{self.n}:CORR:COLL:THRU:ADD:LENG?"))

            # SENSe<Ch>:CORRection:COLLect:THRU:ADDition:UNIT {SEConds|METers}
            def set_addition_unit(self, unit: str):
                """
                Select the display units of the thru delay (length) in the thru addition function.

                Parameter:
                    unit (str): 'SEConds' or 'METers'

                Return:
                    None
                """
                allowed = ['SEConds', 'METers']
                if unit not in allowed:
                    raise ValueError(f"unit must be one of {allowed}")
                self.instrument.write(f":SENS{self.n}:CORR:COLL:THRU:ADD:UNIT {unit}")

            # SENSe<Ch>:CORRection:COLLect:THRU:ADDition:UNIT?
            def get_addition_unit(self) -> str:
                """
                Get the display units of the thru delay (length) in the thru addition function.

                Parameter:
                    None

                Return:
                    str: 'SEC' or 'MET'
                """
                return self.instrument.query(f":SENS{self.n}:CORR:COLL:THRU:ADD:UNIT?").strip()

            # SENSe<Ch>:CORRection:COLLect:THRU:ADDition:MEDia {COAXial|WAVeguide}
            def set_addition_media(self, media: str):
                """
                Specify the media of the thru in the thru addition function.

                Parameter:
                    media (str): 'COAXial' or 'WAVeguide'

                Return:
                    None
                """
                allowed = ['COAXial', 'WAVeguide']
                if media not in allowed:
                    raise ValueError(f"media must be one of {allowed}")
                self.instrument.write(f":SENS{self.n}:CORR:COLL:THRU:ADD:MED {media}")

            # SENSe<Ch>:CORRection:COLLect:THRU:ADDition:MEDia?
            def get_addition_media(self) -> str:
                """
                Get the media of the thru in the thru addition function.

                Parameter:
                    None

                Return:
                    str: 'COAX' or 'WAV'
                """
                return self.instrument.query(f":SENS{self.n}:CORR:COLL:THRU:ADD:MED?").strip()

            # SENSe<Ch>:CORRection:COLLect:THRU:ADDition:PERMittivity <numeric>
            def set_addition_permittivity(self, value: float):
                """
                Set the value of the permittivity of the thru media in the thru addition function.

                Parameter:
                    value (float): Permittivity value

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:CORR:COLL:THRU:ADD:PERM {value}")

            # SENSe<Ch>:CORRection:COLLect:THRU:ADDition:PERMittivity?
            def get_addition_permittivity(self) -> float:
                """
                Get the value of the permittivity of the thru media in the thru addition function.

                Parameter:
                    None

                Return:
                    float: Permittivity value
                """
                return float(self.instrument.query(f":SENS{self.n}:CORR:COLL:THRU:ADD:PERM?"))
            class Waveguide:
                """
                Thru addition waveguide cutoff frequency commands.
                """
                def __init__(self, instrument, data_handler, channel):
                    self.instrument = instrument
                    self.data_handler = data_handler
                    self.n = channel

                # SENSe<Ch>:CORRection:COLLect:THRU:ADDition:WAVeguide:CUToff <numeric>
                def set_waveguide_cutoff(self, value: float):
                    """
                    Set the cutoff frequency of the waveguide thru in the thru addition function.

                    Parameter:
                        value (float): Cutoff frequency in Hz

                    Return:
                        None
                    """
                    self.instrument.write(f":SENS{self.n}:CORR:COLL:THRU:ADD:WAV:CUT {value}")

                # SENSe<Ch>:CORRection:COLLect:THRU:ADDition:WAVeguide:CUToff?
                def get_waveguide_cutoff(self) -> float:
                    """
                    Get the cutoff frequency of the waveguide thru in the thru addition function.

                    Parameter:
                        None

                    Return:
                        float: Cutoff frequency in Hz
                    """
                    return float(self.instrument.query(f":SENS{self.n}:CORR:COLL:THRU:ADD:WAV:CUT?"))

            class Full2Port:
                """
                Thru addition full two-port calibration commands.
                """
                def __init__(self, instrument, data_handler, channel):
                    self.instrument = instrument
                    self.data_handler = data_handler
                    self.n = channel

                # SENSe<Ch>:CORRection:COLLect:THRU:ADDition:FULL2:COMPlete <port1>,<port2>
                def complete_full_two_port_calibration(self, port1: int, port2: int):
                    """
                    Complete the full two-port calibration between the specified ports.

                    Parameter:
                        port1 (int): First port number (1-4)
                        port2 (int): Second port number (1-4)

                    Return:
                        None
                    """
                    if not (1 <= port1 <= 4 and 1 <= port2 <= 4):
                        raise ValueError("port1 and port2 must be 1-4")
                    self.instrument.write(f":SENS{self.n}:CORR:COLL:THRU:ADD:FULL2:COMP {port1},{port2}")

            class Full3Port:
                """
                Thru addition full three-port calibration commands.
                """
                def __init__(self, instrument, data_handler, channel):
                    self.instrument = instrument
                    self.data_handler = data_handler
                    self.n = channel

                # SENSe<Ch>:CORRection:COLLect:THRU:ADDition:FULL3:PORTs <port1>,<port2>,<port3>
                def set_ports(self, port1: int, port2: int, port3: int):
                    """
                    Select the ports to complete the three-port calibration in the thru addition function.

                    Parameter:
                        port1 (int): First port number (1-4)
                        port2 (int): Second port number (1-4)
                        port3 (int): Third port number (1-4)

                    Return:
                        None
                    """
                    ports = [port1, port2, port3]
                    if any(not (1 <= p <= 4) for p in ports):
                        raise ValueError("All ports must be 1-4")
                    self.instrument.write(f":SENS{self.n}:CORR:COLL:THRU:ADD:FULL3:PORT {port1},{port2},{port3}")

                # SENSe<Ch>:CORRection:COLLect:THRU:ADDition:FULL3:PORTs?
                def get_ports(self):
                    """
                    Get the ports selected for three-port calibration in the thru addition function.

                    Parameter:
                        None

                    Return:
                        tuple: (port1, port2, port3)
                    """
                    resp = self.instrument.query(f":SENS{self.n}:CORR:COLL:THRU:ADD:FULL3:PORT?").strip()
                    return tuple(map(int, resp.split(',')))

                # SENSe<Ch>:CORRection:COLLect:THRU:ADDition:FULL3:ACQuire <port1>,<port2>
                def acquire_thru(self, port1: int, port2: int):
                    """
                    Measure an unknown thru between the specified ports for three-port calibration.

                    Parameter:
                        port1 (int): First port number (1-4)
                        port2 (int): Second port number (1-4)

                    Return:
                        None
                    """
                    if not (1 <= port1 <= 4 and 1 <= port2 <= 4):
                        raise ValueError("port1 and port2 must be 1-4")
                    self.instrument.write(f":SENS{self.n}:CORR:COLL:THRU:ADD:FULL3:ACQ {port1},{port2}")

                # SENSe<Ch>:CORRection:COLLect:THRU:ADDition:FULL3:COMPlete
                def complete(self):
                    """
                    Complete the full three-port calibration between the selected ports.

                    Parameter:
                        None

                    Return:
                        None
                    """
                    self.instrument.write(f":SENS{self.n}:CORR:COLL:THRU:ADD:FULL3:COMP")

            class Full4Port:
                """
                Thru addition full four-port calibration commands.
                """
                def __init__(self, instrument, data_handler, channel):
                    self.instrument = instrument
                    self.data_handler = data_handler
                    self.n = channel

                # SENSe<Ch>:CORRection:COLLect:THRU:ADDition:FULL4:ACQuire <port1>,<port2>
                def acquire_thru(self, port1: int, port2: int):
                    """
                    Measure an unknown thru between the specified ports for four-port calibration.

                    Parameter:
                        port1 (int): First port number (1-4)
                        port2 (int): Second port number (1-4)

                    Return:
                        None
                    """
                    if not (1 <= port1 <= 4 and 1 <= port2 <= 4):
                        raise ValueError("port1 and port2 must be 1-4")
                    self.instrument.write(f":SENS{self.n}:CORR:COLL:THRU:ADD:FULL4:ACQ {port1},{port2}")

                # SENSe<Ch>:CORRection:COLLect:THRU:ADDition:FULL4:COMPlete
                def complete(self):
                    """
                    Complete the full four-port calibration.

                    Parameter:
                        None

                    Return:
                        None
                    """
                    self.instrument.write(f":SENS{self.n}:CORR:COLL:THRU:ADD:FULL4:COMP")

        class Extension:
            
            """
            Port extension related commands.
            """
            def __init__(self, instrument, data_handler, channel):
                self.instrument = instrument
                self.data_handler = data_handler
                self.n = channel
                self.auto = self.Auto(instrument, data_handler, channel)
                self.port = self.Port(instrument, data_handler, channel, port=1)  # Example: port=1, user should instantiate as needed

            # SENSe<Ch>:CORRection:EXTension[:STATe] {OFF|ON|0|1}
            def enable_port_extension(self, enable: bool):
                """
                Enable or disable port extension.

                Parameter:
                    enable (bool): True to enable, False to disable

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:CORR:EXT:STAT {1 if enable else 0}")

            # SENSe<Ch>:CORRection:EXTension[:STATe]?
            def is_port_extension_enabled(self) -> bool:
                """
                Query if port extension is enabled.

                Parameter:
                    None

                Return:
                    bool: True if enabled, False otherwise
                """
                return bool(int(self.instrument.query(f":SENS{self.n}:CORR:EXT:STAT?")))

            class Auto:
                """
                Auto port extension related commands.
                """
                def __init__(self, instrument, data_handler, channel):
                    self.instrument = instrument
                    self.data_handler = data_handler
                    self.n = channel

                # SENSe<Ch>:CORRection:EXTension:AUTO:CONFig {CSPN|AMKR|USPN}
                def set_auto_config(self, config: str):
                    """
                    Set the frequency range used for auto port extension calculation.

                    Parameter:
                        config (str): 'CSPN', 'AMKR', or 'USPN'

                    Return:
                        None
                    """
                    allowed = ['CSPN', 'AMKR', 'USPN']
                    if config not in allowed:
                        raise ValueError(f"config must be one of {allowed}")
                    self.instrument.write(f":SENS{self.n}:CORR:EXT:AUTO:CONF {config}")

                # SENSe<Ch>:CORRection:EXTension:AUTO:CONFig?
                def get_auto_config(self) -> str:
                    """
                    Get the frequency range used for auto port extension calculation.

                    Parameter:
                        None

                    Return:
                        str: 'CSPN', 'AMKR', or 'USPN'
                    """
                    return self.instrument.query(f":SENS{self.n}:CORR:EXT:AUTO:CONF?").strip()

                # SENSe<Ch>:CORRection:EXTension:AUTO:DCOFfset {OFF|ON|0|1}
                def enable_dc_offset(self, enable: bool):
                    """
                    Enable or disable usage of "Loss at DC" value for auto port extension.

                    Parameter:
                        enable (bool): True to enable, False to disable

                    Return:
                        None
                    """
                    self.instrument.write(f":SENS{self.n}:CORR:EXT:AUTO:DCOF {1 if enable else 0}")

                # SENSe<Ch>:CORRection:EXTension:AUTO:DCOFfset?
                def is_dc_offset_enabled(self) -> bool:
                    """
                    Query if usage of "Loss at DC" value for auto port extension is enabled.

                    Parameter:
                        None

                    Return:
                        bool: True if enabled, False otherwise
                    """
                    return bool(int(self.instrument.query(f":SENS{self.n}:CORR:EXT:AUTO:DCOF?")))

                # SENSe<Ch>:CORRection:EXTension:AUTO:LOSS {OFF|ON|0|1}
                def enable_loss(self, enable: bool):
                    """
                    Enable or disable usage of "Loss1" and "Loss2" values for auto port extension.

                    Parameter:
                        enable (bool): True to enable, False to disable

                    Return:
                        None
                    """
                    self.instrument.write(f":SENS{self.n}:CORR:EXT:AUTO:LOSS {1 if enable else 0}")

                # SENSe<Ch>:CORRection:EXTension:AUTO:LOSS?
                def is_loss_enabled(self) -> bool:
                    """
                    Query if usage of "Loss1" and "Loss2" values for auto port extension is enabled.

                    Parameter:
                        None

                    Return:
                        bool: True if enabled, False otherwise
                    """
                    return bool(int(self.instrument.query(f":SENS{self.n}:CORR:EXT:AUTO:LOSS?")))

                # SENSe<Ch>:CORRection:EXTension:AUTO:MEASure {SHORt|OPEN}
                def measure_standard(self, standard: str):
                    """
                    Perform measurement of the standard "SHORT" or "OPEN" for auto port extension.

                    Parameter:
                        standard (str): 'SHORt' or 'OPEN'

                    Return:
                        None
                    """
                    allowed = ['SHORt', 'OPEN']
                    if standard not in allowed:
                        raise ValueError(f"standard must be one of {allowed}")
                    self.instrument.write(f":SENS{self.n}:CORR:EXT:AUTO:MEAS {standard}")

                # SENSe<Ch>:CORRection:EXTension:AUTO:PORT<Pt> {OFF|ON|0|1}
                def enable_auto_port(self, port: int, enable: bool):
                    """
                    Enable or disable auto port extension for the specified port.

                    Parameter:
                        port (int): Port number (1-4)
                        enable (bool): True to enable, False to disable

                    Return:
                        None
                    """
                    if not (1 <= port <= 4):
                        raise ValueError("port must be 1-4")
                    self.instrument.write(f":SENS{self.n}:CORR:EXT:AUTO:PORT{port} {1 if enable else 0}")

                # SENSe<Ch>:CORRection:EXTension:AUTO:PORT<Pt>?
                def is_auto_port_enabled(self, port: int) -> bool:
                    """
                    Query if auto port extension is enabled for the specified port.

                    Parameter:
                        port (int): Port number (1-4)

                    Return:
                        bool: True if enabled, False otherwise
                    """
                    if not (1 <= port <= 4):
                        raise ValueError("port must be 1-4")
                    return bool(int(self.instrument.query(f":SENS{self.n}:CORR:EXT:AUTO:PORT{port}?")))
                # SENSe<Ch>:CORRection:EXTension:AUTO:RES - Reset auto port extension measurement data
                def reset_auto_measurement_data(self):
                    """
                    Deletes the finished measurement data of the OPEN and SHORT standards of the auto port extension function.

                    Parameter:
                        None

                    Return:
                        None
                    """
                    self.instrument.write(f":SENS{self.n}:CORR:EXT:AUTO:RES")

                # SENSe<Ch>:CORRection:EXTension:AUTO:STARt <frequency>
                def set_user_span_start(self, frequency: float):
                    """
                    Sets the start value of the user span for auto port extension.

                    Parameter:
                        frequency (float): Start frequency in Hz

                    Return:
                        None
                    """
                    self.instrument.write(f":SENS{self.n}:CORR:EXT:AUTO:STAR {frequency}")

                def get_user_span_start(self) -> float:
                    """
                    Reads out the start value of the user span for auto port extension.

                    Parameter:
                        None

                    Return:
                        float: Start frequency in Hz
                    """
                    return float(self.instrument.query(f":SENS{self.n}:CORR:EXT:AUTO:STAR?"))

                # SENSe<Ch>:CORRection:EXTension:AUTO:STOP <frequency>
                def set_user_span_stop(self, frequency: float):
                    """
                    Sets the stop value of the user span for auto port extension.

                    Parameter:
                        frequency (float): Stop frequency in Hz

                    Return:
                        None
                    """
                    self.instrument.write(f":SENS{self.n}:CORR:EXT:AUTO:STOP {frequency}")

                def get_user_span_stop(self) -> float:
                    """
                    Reads out the stop value of the user span for auto port extension.

                    Parameter:
                        None

                    Return:
                        float: Stop frequency in Hz
                    """
                    return float(self.instrument.query(f":SENS{self.n}:CORR:EXT:AUTO:STOP?"))

            class Port:
                """
                Port-specific extension commands.
                """
                def __init__(self, instrument, data_handler, channel, port):
                    self.instrument = instrument
                    self.data_handler = data_handler
                    self.n = channel
                    self.p = port

                # SENSe<Ch>:CORRection:EXTension:PORT<Pt>:FREQuency{[1]|2} <frequency>
                def set_frequency(self, freq_num: int, frequency: float):
                    """
                    Sets the value of frequency 1 or 2 for port extension loss calculation.

                    Parameter:
                        freq_num (int): Frequency number (1 or 2)
                        frequency (float): Frequency value in Hz

                    Return:
                        None
                    """
                    if freq_num not in [1, 2]:
                        raise ValueError("freq_num must be 1 or 2")
                    self.instrument.write(f":SENS{self.n}:CORR:EXT:PORT{self.p}:FREQ{freq_num} {frequency}")

                def get_frequency(self, freq_num: int) -> float:
                    """
                    Reads out the value of frequency 1 or 2 for port extension loss calculation.

                    Parameter:
                        freq_num (int): Frequency number (1 or 2)

                    Return:
                        float: Frequency value in Hz
                    """
                    if freq_num not in [1, 2]:
                        raise ValueError("freq_num must be 1 or 2")
                    return float(self.instrument.query(f":SENS{self.n}:CORR:EXT:PORT{self.p}:FREQ{freq_num}?"))

                # SENSe<Ch>:CORRection:EXTension:PORT<Pt>:INCLude{[1]|2}[:STATe] {OFF|ON|0|1}
                def enable_loss_compensation(self, loss_num: int, enable: bool):
                    """
                    Turns the loss compensation of loss 1 or loss 2 ON/OFF for port extension.

                    Parameter:
                        loss_num (int): Loss number (1 or 2)
                        enable (bool): True to enable, False to disable

                    Return:
                        None
                    """
                    if loss_num not in [1, 2]:
                        raise ValueError("loss_num must be 1 or 2")
                    self.instrument.write(f":SENS{self.n}:CORR:EXT:PORT{self.p}:INCL{loss_num}:STAT {1 if enable else 0}")

                def is_loss_compensation_enabled(self, loss_num: int) -> bool:
                    """
                    Query if loss compensation of loss 1 or loss 2 is enabled for port extension.

                    Parameter:
                        loss_num (int): Loss number (1 or 2)

                    Return:
                        bool: True if enabled, False otherwise
                    """
                    if loss_num not in [1, 2]:
                        raise ValueError("loss_num must be 1 or 2")
                    return bool(int(self.instrument.query(f":SENS{self.n}:CORR:EXT:PORT{self.p}:INCL{loss_num}:STAT?")))

                # SENSe<Ch>:CORRection:EXTension:PORT<Pt>:LDC <numeric>
                def set_loss_at_dc(self, value: float):
                    """
                    Sets the loss value at DC for the port extension.

                    Parameter:
                        value (float): Loss value at DC in dB (-200 to 200)

                    Return:
                        None
                    """
                    self.instrument.write(f":SENS{self.n}:CORR:EXT:PORT{self.p}:LDC {value}")

                def get_loss_at_dc(self) -> float:
                    """
                    Reads out the loss value at DC for the port extension.

                    Parameter:
                        None

                    Return:
                        float: Loss value at DC in dB
                    """
                    return float(self.instrument.query(f":SENS{self.n}:CORR:EXT:PORT{self.p}:LDC?"))

                # SENSe<Ch>:CORRection:EXTension:PORT<Pt>:LOSS{[1]|2} <numeric>
                def set_loss(self, loss_num: int, value: float):
                    """
                    Sets the value of loss 1 or loss 2 for the port extension.

                    Parameter:
                        loss_num (int): Loss number (1 or 2)
                        value (float): Loss value in dB (-200 to 200)

                    Return:
                        None
                    """
                    if loss_num not in [1, 2]:
                        raise ValueError("loss_num must be 1 or 2")
                    self.instrument.write(f":SENS{self.n}:CORR:EXT:PORT{self.p}:LOSS{loss_num} {value}")

                def get_loss(self, loss_num: int) -> float:
                    """
                    Reads out the value of loss 1 or loss 2 for the port extension.

                    Parameter:
                        loss_num (int): Loss number (1 or 2)

                    Return:
                        float: Loss value in dB
                    """
                    if loss_num not in [1, 2]:
                        raise ValueError("loss_num must be 1 or 2")
                    return float(self.instrument.query(f":SENS{self.n}:CORR:EXT:PORT{self.p}:LOSS{loss_num}?"))

                # SENSe<Ch>:CORRection:EXTension:PORT<Pt>:TIME <time>
                def set_electrical_delay(self, value: float):
                    """
                    Sets the electrical delay value for the port extension.

                    Parameter:
                        value (float): Electrical delay value in seconds (-10 to 10)

                    Return:
                        None
                    """
                    self.instrument.write(f":SENS{self.n}:CORR:EXT:PORT{self.p}:TIME {value}")

                def get_electrical_delay(self) -> float:
                    """
                    Reads out the electrical delay value for the port extension.

                    Parameter:
                        None

                    Return:
                        float: Electrical delay value in seconds
                    """
                    return float(self.instrument.query(f":SENS{self.n}:CORR:EXT:PORT{self.p}:TIME?"))
                # SENS:CORR:INF? <rcvport>,<srcport>
                def get_correction_information(self, rcvport: int, srcport: int) -> str:
                    """
                    Reads out the information string of the calibration applied to the pair of ports.

                    Parameter:
                        rcvport (int): Receiver port number (1-4)
                        srcport (int): Source port number (1-4)

                    Return:
                        str: Information string
                    """
                    if not (1 <= rcvport <= 4 and 1 <= srcport <= 4):
                        raise ValueError("rcvport and srcport must be 1-4")
                    return self.instrument.query(f":SENS{self.n}:CORR:INF? {rcvport},{srcport}").strip()

                # SENS:CORR:IMP[:INPut][:MAGNitude] <numeric>
                def set_system_impedance(self, value: float):
                    """
                    Sets the system impedance Z0 of all Analyzer ports.

                    Parameter:
                        value (float): Z0 value (0.001 to 1000)

                    Return:
                        None
                    """
                    self.instrument.write(f":SENS{self.n}:CORR:IMP:INP:MAGN {value}")

                def get_system_impedance(self) -> float:
                    """
                    Reads out the system impedance Z0 of all Analyzer ports.

                    Parameter:
                        None

                    Return:
                        float: Z0 value
                    """
                    return float(self.instrument.query(f":SENS{self.n}:CORR:IMP:INP:MAGN?"))

                # SENS:CORR:IMP:SEL:AUTO {OFF|ON|0|1}
                def enable_auto_select_impedance(self, enable: bool):
                    """
                    Turns the auto select Z0 function ON/OFF.

                    Parameter:
                        enable (bool): True to enable, False to disable

                    Return:
                        None
                    """
                    self.instrument.write(f":SENS{self.n}:CORR:IMP:INP:SEL:AUTO {1 if enable else 0}")

                def is_auto_select_impedance_enabled(self) -> bool:
                    """
                    Query if auto select Z0 function is enabled.

                    Parameter:
                        None

                    Return:
                        bool: True if enabled, False otherwise
                    """
                    return bool(int(self.instrument.query(f":SENS{self.n}:CORR:IMP:INP:SEL:AUTO?")))
        class AutoImpedance:
            """
            Auto select Z0 function ON/OFF.
            """
            def __init__(self, instrument, data_handler, channel):
                self.instrument = instrument
                self.data_handler = data_handler
                self.n = channel

            # SENS:CORR:IMP:SEL:AUTO {OFF|ON|0|1}
            def enable_auto_select_z0(self, enable: bool):
                """
                Turns the auto select Z0 function ON/OFF.

                Parameter:
                    enable (bool): True to enable, False to disable

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:CORR:IMP:SEL:AUTO {1 if enable else 0}")

            # SENS:CORR:IMP:SEL:AUTO?
            def is_auto_select_z0_enabled(self) -> bool:
                """
                Query if auto select Z0 function is enabled.

                Parameter:
                    None

                Return:
                    bool: True if enabled, False otherwise
                """
                return bool(int(self.instrument.query(f":SENS{self.n}:CORR:IMP:SEL:AUTO?")))

        class Offset:
            """
            Scalar mixer calibration and offset correction commands.
            """
            def __init__(self, instrument, data_handler, channel):
                self.instrument = instrument
                self.data_handler = data_handler
                self.n = channel

            # SENS:CORR:OFFS:CLE
            def clear_scalar_mixer_calibration_table(self):
                """
                Clears the scalar mixer calibration coefficient table.

                Parameter:
                    None

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:CORR:OFFS:CLE")

            # SENS:CORR:OFFS:COLL:CLE
            def clear_scalar_mixer_calibration_data(self):
                """
                Clears the calibration measurement data of scalar mixer calibration when the frequency offset feature is ON.

                Parameter:
                    None

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:CORR:OFFS:COLL:CLE")

            # SENS:CORR:OFFS:COLL:DIR {FORWard|REVerse|BOTH}
            def set_scalar_mixer_calibration_direction(self, direction: str):
                """
                Specifies the direction of the scalar mixer calibration: forward, reverse or both.

                Parameter:
                    direction (str): 'FORW', 'REV', or 'BOTH'

                Return:
                    None
                """
                allowed = ['FORW', 'REV', 'BOTH']
                if direction not in allowed:
                    raise ValueError(f"direction must be one of {allowed}")
                self.instrument.write(f":SENS{self.n}:CORR:OFFS:COLL:DIR {direction}")


            # SENS:CORR:OFFS:COLL:DIR?
            def get_scalar_mixer_calibration_direction(self) -> str:
                """
                Get the direction of the scalar mixer calibration.

                Parameter:
                    None

                Return:
                    str: 'FORW', 'REV', or 'BOTH'
                """
                return self.instrument.query(f":SENS{self.n}:CORR:OFFS:COLL:DIR?").strip()

            # SENS:CORR:OFFS:COLL:ECAL <numeric1>,<numeric2>
            def measure_scalar_mixer_calibration_ecal(self, port1: int, port2: int):
                """
                Measures the calibration data of all reflection standards of the ACM on the specified port when the frequency offset feature is on.

                Parameter:
                    port1 (int): Measurement port number
                    port2 (int): Number of the second port of the SMC port pair

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:CORR:OFFS:COLL:ECAL {port1},{port2}")

            # SENS:CORR:OFFS:COLL:LOAD <numeric1>,<numeric2>
            def measure_scalar_mixer_calibration_load(self, port1: int, port2: int):
                """
                Measures the calibration data of the load standard of the specified port when the frequency offset feature is on.

                Parameter:
                    port1 (int): Measurement port number
                    port2 (int): Number of the second port of the SMC port pair

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:CORR:OFFS:COLL:LOAD {port1},{port2}")

            # SENS:CORR:OFFS:COLL:METH:SMIX2 <numeric1>,<numeric2>
            def set_scalar_mixer_calibration_type(self, port1: int, port2: int):
                """
                Selects the ports and sets the scalar mixer calibration type when the frequency offset feature is on.

                Parameter:
                    port1 (int): First port
                    port2 (int): Second port

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:CORR:OFFS:COLL:METH:SMIX2 {port1},{port2}")

        class Receiver:
            """
            addition Receiver calibration commands.
            """
            def __init__(self, instrument, data_handler, channel):
                self.instrument = instrument
                self.data_handler = data_handler
                self.n = channel
                self.offset_amplitude = self.OffsetAmplitude(instrument, data_handler, channel)

            # SENS:CORR:REC - Receiver correction ON/OFF
            def enable_receiver_correction(self, port: int, enable: bool):
                """
                Enable or disable receiver correction for the specified port.

                Parameter:
                    port (int): Port number (1-4)
                    enable (bool): True to enable, False to disable
                if not (1 <= port <= 4):
                    raise ValueError("port must be 1-4")
                self.instrument.write(f":SENS{self.n}:CORR:REC:RECeiver{port}:STATe {1 if enable else 0}")

                """
                if not (1 <= port <= 4):
                    raise ValueError("port must be 1-4")
                self.instrument.write(f":SENS{self.n}:CORR:REC:RECeiver{port}:STATe {1 if enable else 0}")

            def is_receiver_correction_enabled(self, port: int) -> bool:
                """
                Query if receiver correction is enabled for the specified port.

                Parameter:
                if not (1 <= port <= 4):
                    raise ValueError("port must be 1-4")
                return bool(int(self.instrument.query(f":SENS{self.n}:CORR:REC:RECeiver{port}:STATe?")))

                    bool: True if enabled, False otherwise
                """
                if not (1 <= port <= 4):
                    raise ValueError("port must be 1-4")
                return bool(int(self.instrument.query(f":SENS{self.n}:CORR:REC:RECeiver{port}:STATe?")))

            # SENS:CORR:REC:COLL:ACQ - Receiver calibration (both receivers)
            def acquire_receiver_calibration(self, port: int, srcport: int):
                """
                Execute receiver calibration of both the test receiver and the reference receiver of the specified port.

                Parameter:
                if not (1 <= port <= 4 and 1 <= srcport <= 4):
                    raise ValueError("port and srcport must be 1-4")
                self.instrument.write(f":SENS{self.n}:CORR:REC:RECeiver{port}:COLLect:ACQuire {srcport}")

                Return:
                    None
                """
                if not (1 <= port <= 4 and 1 <= srcport <= 4):
                    raise ValueError("port and srcport must be 1-4")
                self.instrument.write(f":SENS{self.n}:CORR:REC:RECeiver{port}:COLLect:ACQuire {srcport}")

            # SENS:CORR:REC:COLL:RCH:ACQ - Reference receiver calibration
            def acquire_reference_receiver_calibration(self, port: int, srcport: int):
                """
                Execute receiver calibration of the reference receiver of the specified port.

                if not (1 <= port <= 4 and 1 <= srcport <= 4):
                    raise ValueError("port and srcport must be 1-4")
                self.instrument.write(f":SENS{self.n}:CORR:REC:RECeiver{port}:COLLect:RCHannel:ACQuire {srcport}")


                Return:
                    None
                """
                if not (1 <= port <= 4 and 1 <= srcport <= 4):
                    raise ValueError("port and srcport must be 1-4")
                self.instrument.write(f":SENS{self.n}:CORR:REC:RECeiver{port}:COLLect:RCHannel:ACQuire {srcport}")

            # SENS:CORR:REC:COLL:TCH:ACQ - Test receiver calibration
            def acquire_test_receiver_calibration(self, port: int, srcport: int):
                """
                Execute receiver calibration of the test receiver of the specified port.
                if not (1 <= port <= 4 and 1 <= srcport <= 4):
                    raise ValueError("port and srcport must be 1-4")
                self.instrument.write(f":SENS{self.n}:CORR:REC:RECeiver{port}:COLLect:TCHannel:ACQuire {srcport}")

                    srcport (int): Source port number (1-4)

                Return:
                    None
                """
                if not (1 <= port <= 4 and 1 <= srcport <= 4):
                    raise ValueError("port and srcport must be 1-4")
                self.instrument.write(f":SENS{self.n}:CORR:REC:RECeiver{port}:COLLect:TCHannel:ACQuire {srcport}")
            class OffsetAmplitude:
                """
                Power offset value for receiver calibration.
                """
                def __init__(self, instrument, data_handler, channel):
                    self.instrument = instrument
                    self.data_handler = data_handler
                    self.n = channel

                # SENSe<Ch>:CORRection:RECeiver<Pt>:OFFSET:AMPLitude <numeric>
                def set_offset_amplitude(self, port: int, value: float):
                    """
                    Set the power offset value for receiver calibration.

                    Parameter:
                        port (int): Port number (1-4)
                        value (float): Power offset value (-100 to 100 dBm)

                    Return:
                        None
                    """
                    if not (1 <= port <= 4):
                        raise ValueError("port must be 1-4")
                    value = max(-100, min(100, value))
                    self.instrument.write(f":SENS{self.n}:CORR:REC:OFFS:AMPL {port},{value}")

                # SENSe<Ch>:CORRection:RECeiver<Pt>:OFFSET:AMPLitude?
                def get_offset_amplitude(self, port: int) -> float:
                    """
                    Get the power offset value for receiver calibration.

                    Parameter:
                        port (int): Port number (1-4)

                    Return:
                        float: Power offset value in dBm
                    """
                    if not (1 <= port <= 4):
                        raise ValueError("port must be 1-4")
                    return float(self.instrument.query(f":SENS{self.n}:CORR:REC:OFFS:AMPL? {port}"))

        
        class CableInTimeDomain:
            """
            Cable correction function for time domain transformation.
            """
            def __init__(self, instrument, data_handler, channel):
                self.instrument = instrument
                self.data_handler = data_handler
                self.n = channel

            # SENSe<Ch>:CORRection:TRANsform:TIME:FREQuency <frequency>
            def set_cable_loss_frequency(self, value: float):
                """
                Set the frequency value for cable loss specification.

                Parameter:
                    value (float): Frequency value in Hz

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:CORR:TRAN:TIME:FREQ {value}")

            # SENSe<Ch>:CORRection:TRANsform:TIME:FREQuency?
            def get_cable_loss_frequency(self) -> float:
                """
                Get the frequency value for cable loss specification.

                Parameter:
                    None

                Return:
                    float: Frequency value in Hz
                """
                return float(self.instrument.query(f":SENS{self.n}:CORR:TRAN:TIME:FREQ?"))

            # SENSe<Ch>:CORRection:TRANsform:TIME:LOSS <numeric>
            def set_cable_loss_value(self, value: float):
                """
                Set the cable loss value for cable correction.

                Parameter:
                    value (float): Cable loss value in dB/m

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:CORR:TRAN:TIME:LOSS {value}")

            # SENSe<Ch>:CORRection:TRANsform:TIME:LOSS?
            def get_cable_loss_value(self) -> float:
                """
                Get the cable loss value for cable correction.

                Parameter:
                    None

                Return:
                    float: Cable loss value in dB/m
                """
                return float(self.instrument.query(f":SENS{self.n}:CORR:TRAN:TIME:LOSS?"))

            # SENSe<Ch>:CORRection:TRANsform:TIME:RVELocity <numeric>
            def set_cable_velocity_factor(self, value: float):
                """
                Set the cable relative wave speed velocity factor.

                Parameter:
                    value (float): Velocity factor

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:CORR:TRAN:TIME:RVEL {value}")

            # SENSe<Ch>:CORRection:TRANsform:TIME:RVELocity?
            def get_cable_velocity_factor(self) -> float:
                """
                Get the cable relative wave speed velocity factor.

                Parameter:
                    None

                Return:
                    float: Velocity factor
                """
                return float(self.instrument.query(f":SENS{self.n}:CORR:TRAN:TIME:RVEL?"))

        
            # SENSe<Ch>:CORRection:TRANsform:TIME:RVELocity
            def set_relative_velocity(self, value: float):
                """
                Set the cable relative wave speed velocity factor.

                Parameter:
                    value (float): Velocity factor

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:CORR:TRAN:TIME:RVEL {value}")

            def get_relative_velocity(self) -> float:
                """
                Get the cable relative wave speed velocity factor.

                Parameter:
                    None

                Return:
                    float: Velocity factor
                """
                return float(self.instrument.query(f":SENS{self.n}:CORR:TRAN:TIME:RVEL?"))

            # SENSe<Ch>:CORRection:TRANsform:TIME:STATe {OFF|ON|0|1}
            def enable_cable_correction(self, enable: bool):
                """
                Enable or disable cable correction when time domain transformation is ON.

                Parameter:
                    enable (bool): True to enable, False to disable

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:CORR:TRAN:TIME:STAT {1 if enable else 0}")

            def is_cable_correction_enabled(self) -> bool:
                """
                Query if cable correction is enabled when time domain transformation is ON.

                Parameter:
                    None

                Return:
                    bool: True if enabled, False otherwise
                """
                return bool(int(self.instrument.query(f":SENS{self.n}:CORR:TRAN:TIME:STAT?")))

        class Trigger:
            """
            addition Calibration trigger source functions.
            """
            def __init__(self, instrument, data_handler, channel):
                self.instrument = instrument
                self.data_handler = data_handler
                self.n = channel

            # SENSe<Ch>:CORRection:TRIGger:FREE[:STATe] {OFF|ON|0|1}
            def enable_internal_trigger_source(self, enable: bool):
                """
                Enable or disable the internal trigger source for calibration.

                Parameter:
                    enable (bool): True to enable, False to disable

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:CORR:TRIG:FREE:STAT {1 if enable else 0}")

            def is_internal_trigger_source_enabled(self) -> bool:
                """
                Query if the internal trigger source for calibration is enabled.

                Parameter:
                    None

                Return:
                    bool: True if enabled, False otherwise
                """
                return bool(int(self.instrument.query(f":SENS{self.n}:CORR:TRIG:FREE:STAT?")))

        class Type:
            """
            addition Calibration type and port info for trace.
            """
            def __init__(self, instrument, data_handler, channel):
                self.instrument = instrument
                self.data_handler = data_handler
                self.n = channel

            # SENSe<Ch>:CORRection:TYPE<Tr>?
            def get_calibration_type(self, trace: int):
                """
                Reads the calibration type and port numbers for the specified trace.

                Parameter:
                    trace (int): Trace number (1-16)

                Return:
                    tuple: (type, port1, ..., portN)
                """
                resp = self.instrument.query(f":SENS{self.n}:CORR:TYPE{trace}?").strip()
                parts = resp.split(',')
                return (parts[0],) + tuple(map(int, parts[1:]))

        class VMC:
            """
            addition Vector mixer calibration commands.
            """
            def __init__(self, instrument, data_handler, channel):
                self.instrument = instrument
                self.data_handler = data_handler
                self.n = channel

            # SENSe<Ch>:CORRection:OFFSet:COLLect:ECAL:SAVE <string>
            def save_vector_mixer_calibration(self, filename: str = 'vmctemp.S2P'):
                """
                Measures ACM, completes vector mixer calibration, and saves S-parameters to a touchstone file.

                Parameter:
                    filename (str): Destination file name (optional, default 'vmctemp.S2P')

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:CORR:OFFS:COLL:ECAL:SAVE \"{filename}\"")

            # SENSe<Ch>:CORRection:VMC:COLLect:PORT <numeric>
            def set_vmc_port(self, port: int):
                """
                Set the port number used in vector mixer calibration.

                Parameter:
                    port (int): Port number (1-4)

                Return:
                    None
                """
                if not (1 <= port <= 4):
                    raise ValueError("port must be 1-4")
                self.instrument.write(f":SENS{self.n}:CORR:VMC:COLL:PORT {port}")

            def get_vmc_port(self) -> int:
                """
                Get the port number used in vector mixer calibration.

                Parameter:
                    None

                Return:
                    int: Port number
                """
                return int(self.instrument.query(f":SENS{self.n}:CORR:VMC:COLL:PORT?"))

            # SENSe<Ch>:CORRection:VMC:COLLect:LO:FREQuency <numeric>
            def set_vmc_lo_frequency(self, value: float):
                """
                Set the LO frequency value used in vector mixer calibration.

                Parameter:
                    value (float): LO frequency in Hz (0 to 1e15)

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:CORR:VMC:COLL:LO:FREQ {value}")

            def get_vmc_lo_frequency(self) -> float:

                """
                Get the LO frequency value used in vector mixer calibration.

                Parameter:
                    None

                Return:
                    float: LO frequency in Hz
                """
                return float(self.instrument.query(f":SENS{self.n}:CORR:VMC:COLL:LO:FREQ?"))
    
            

            # SENS:CORR:VMC:COLL:IF:SEL
            def set_if_frequency(self, freq_type: str):
                """
                Select the IF frequency for vector mixer calibration.

                Parameter:
                    freq_type (str): One of ['RFPLO', 'RFMLO', 'LOMRF']

                Return:
                    None
                """
                allowed = ['RFPLO', 'RFMLO', 'LOMRF']
                if freq_type not in allowed:
                    raise ValueError(f"freq_type must be one of {allowed}")
                self.instrument.write(f":SENS{self.n}:CORR:VMC:COLL:IF:SEL {freq_type}")

            def get_if_frequency(self) -> str:
                """
                Get the selected IF frequency for vector mixer calibration.

                Parameter:
                    None

                Return:
                    str: IF frequency type
                """
                return self.instrument.query(f":SENS{self.n}:CORR:VMC:COLL:IF:SEL?").strip()

            # SENS:CORR:VMC:COLL:LOAD
            def measure_load_standard(self):
                """
                Measure the load standard for vector mixer calibration.

                Parameter:
                    None

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:CORR:VMC:COLL:LOAD")

            # SENS:CORR:VMC:COLL:OPEN
            def measure_open_standard(self):
                """
                Measure the open standard for vector mixer calibration.

                Parameter:
                    None

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:CORR:VMC:COLL:OPEN")

            # SENS:CORR:VMC:COLL:SHOR
            def measure_short_standard(self):
                """
                Measure the short standard for vector mixer calibration.

                Parameter:
                    None

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:CORR:VMC:COLL:SHOR")

            # SENS:CORR:VMC:COLL:OPT
            def enable_setup_option(self, enable: bool):
                """
                Enable or disable the setup option for vector mixer calibration.

                Parameter:
                    enable (bool): True to enable, False to disable

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:CORR:VMC:COLL:SETup:OPTion {1 if enable else 0}")

            def is_setup_option_enabled(self) -> bool:
                """
                Query if the setup option for vector mixer calibration is enabled.

                Parameter:
                    None

                Return:
                    bool: True if enabled, False otherwise
                """
                return bool(int(self.instrument.query(f":SENS{self.n}:CORR:VMC:COLL:SETup:OPTion?")))

            # SENS:CORR:VMC:COLL:SAVE
            def save_calibration(self, filename: str = None):
                """
                Complete vector mixer calibration and save S-parameters to a touchstone file.

                Parameter:
                    filename (str): Destination file name (optional). If omitted, 'vmctemp.S2P' is used.

                Return:
                    None
                """
                if filename:
                    self.instrument.write(f":SENS{self.n}:CORR:OFFS:COLLect:SAVE \"{filename}\"")
                else:
                    self.instrument.write(f":SENS{self.n}:CORR:OFFS:COLLect:SAVE")

        class Kit:
            """
            Calibration kit management commands.
            """
            def __init__(self, instrument, data_handler, channel):
                self.instrument = instrument
                self.data_handler = data_handler
                self.n = channel
                self.standard = self.Standard(instrument, data_handler, channel)
                self.select = self.Select(instrument, data_handler, channel)
                
                self.arbitrary = self.Arbitrary(instrument, data_handler, channel)
                self.open_capacitance = self.OpenCapacitance(instrument, data_handler, channel)

            class Standard:
                """
                Calibration kit standard management commands.
                """
                def __init__(self, instrument, data_handler, channel):
                    self.instrument = instrument
                    self.data_handler = data_handler
                    self.n = channel
                    self.count = self.Count(instrument, data_handler, channel)
                    self.data = self.Data(instrument, data_handler, channel)
                    self.delay = self.Delay(instrument, data_handler, channel)
                    self.fmax = self.Fmax(instrument, data_handler, channel)
                    self.fmin = self.StandardFmin(instrument, data_handler, channel)
                    self.insert = self.Insert(instrument, data_handler, channel)
                    self.l0 = self.StandardL0(instrument, data_handler, channel)
                    self.l1 = self.L1(instrument, data_handler, channel)
                    self.l2 = self.L2(instrument, data_handler, channel)
                    self.l3 = self.L3(instrument, data_handler, channel)
                    self.label = self.Label(instrument, data_handler, channel)

                # SENS:CORR:COLL:CKIT:STAN<Std>:LOSS - Offset loss value for calibration standard
                def set_standard_offset_loss(self, std: int, value: float):
                    """
                    Set the offset loss value for the calibration standard.

                    Parameter:
                        std (int): Standard number (1..N)
                        value (float): Offset loss value (-1E18 to 1E18)

                    Return:
                        None
                    """
                    self.instrument.write(f":SENS{self.n}:CORR:COLL:CKIT:STAN{std}:LOSS {value}")

                def get_standard_offset_loss(self, std: int) -> float:
                    """
                    Get the offset loss value for the calibration standard.

                    Parameter:
                        std (int): Standard number (1..N)

                    Return:
                        float: Offset loss value
                    """
                    return float(self.instrument.query(f":SENS{self.n}:CORR:COLL:CKIT:STAN{std}:LOSS?"))

                # SENS:CORR:COLL:CKIT:STAN<Std>:REM - Delete calibration standard
                def remove_standard(self, std: int):
                    """
                    Delete the calibration standard from the selected calibration kit.

                    Parameter:
                        std (int): Standard number (1..N)

                    Return:
                        None
                    """
                    self.instrument.write(f":SENS{self.n}:CORR:COLL:CKIT:STAN{std}:REM")

                # SENS:CORR:COLL:CKIT:STAN<Std>:TYPE - Type of calibration standard
                def set_standard_type(self, std: int, std_type: str):
                    """
                    Set the type of calibration standard.

                    Parameter:
                        std (int): Standard number (1..N)
                        std_type (str): Type, one of ['OPEN', 'SHOR', 'LOAD', 'THRU', 'UTHR', 'SLID', 'DATA', 'NONE']

                    Return:
                        None
                    """
                    allowed = ['OPEN', 'SHOR', 'LOAD', 'THRU', 'UTHR', 'SLID', 'DATA', 'NONE']
                    if std_type not in allowed:
                        raise ValueError(f"std_type must be one of {allowed}")
                    self.instrument.write(f":SENS{self.n}:CORR:COLL:CKIT:STAN{std}:TYPE {std_type}")

                def get_standard_type(self, std: int) -> str:
                    """
                    Get the type of calibration standard.

                    Parameter:
                        std (int): Standard number (1..N)

                    Return:
                        str: Standard type
                    """
                    return self.instrument.query(f":SENS{self.n}:CORR:COLL:CKIT:STAN{std}:TYPE?").strip()

                # SENS:CORR:COLL:CKIT:STAN<Std>:Z0 - Offset Z0 value for calibration standard
                def set_standard_offset_z0(self, std: int, value: float):
                    """
                    Set the offset Z0 value for the calibration standard.

                    Parameter:
                        std (int): Standard number (1..N)
                        value (float): Offset Z0 value (-1E18 to 1E18)

                    Return:
                        None
                    """
                    self.instrument.write(f":SENS{self.n}:CORR:COLL:CKIT:STAN{std}:Z0 {value}")

                def get_standard_offset_z0(self, std: int) -> float:
                    """
                    Get the offset Z0 value for the calibration standard.

                    Parameter:
                        std (int): Standard number (1..N)

                    Return:
                        float: Offset Z0 value
                    """
                    return float(self.instrument.query(f":SENS{self.n}:CORR:COLL:CKIT:STAN{std}:Z0?"))
                # SENS:CORR:COLL:CKIT:STAN:LAB - Standard label
                def set_standard_label(self, label: str):
                    """
                    Set standard label.

                    Parameter:
                        label (str): Standard label

                    Return:
                        None
                    """
                    self.instrument.write(f":SENS{self.n}:CORR:COLL:CKIT:STAN:LAB \"{label}\"")

                def get_standard_label(self) -> str:
                    """
                    Get standard label.

                    Parameter:
                        None

                    Return:
                        str: Standard label
                    """
                    return self.instrument.query(f":SENS{self.n}:CORR:COLL:CKIT:STAN:LAB?").strip()

                # SENS:CORR:COLL:CKIT:STAN:LOSS - Offset loss
                def set_standard_offset_loss(self, value: float):
                    """
                    Set offset loss for standard.

                    Parameter:
                        value (float): Offset loss

                    Return:
                        None
                    """
                    self.instrument.write(f":SENS{self.n}:CORR:COLL:CKIT:STAN:LOSS {value}")

                def get_standard_offset_loss(self) -> float:
                    """
                    Get offset loss for standard.

                    Parameter:
                        None

                    Return:
                        float: Offset loss
                    """
                    return float(self.instrument.query(f":SENS{self.n}:CORR:COLL:CKIT:STAN:LOSS?"))

                # SENS:CORR:COLL:CKIT:STAN:TYPE - Standard type
                def set_standard_type(self, std_type: str):
                    """
                    Set standard type.

                    Parameter:
                        std_type (str): Standard type, e.g., 'LOAD', 'OPEN', 'SHORT', 'THRU', etc.

                    Return:
                        None
                    """
                    allowed = ['LOAD', 'OPEN', 'SHORT', 'THRU', 'ARB', 'C0', 'C1', 'C2', 'C3', 'L0', 'L1', 'L2', 'L3']
                    if std_type not in allowed:
                        raise ValueError(f"std_type must be one of {allowed}")
                    self.instrument.write(f":SENS{self.n}:CORR:COLL:CKIT:STAN:TYPE {std_type}")

                def get_standard_type(self) -> str:
                    """
                    Get standard type.

                    Parameter:
                        None

                    Return:
                        str: Standard type
                    """
                    return self.instrument.query(f":SENS{self.n}:CORR:COLL:CKIT:STAN:TYPE?").strip()

                # SENS:CORR:COLL:CKIT:STAN:Z0 - Offset Z0
                def set_standard_offset_z0(self, value: float):
                    """
                    Set offset Z0 for standard.

                    Parameter:
                        value (float): Offset Z0

                    Return:
                        None
                    """
                    self.instrument.write(f":SENS{self.n}:CORR:COLL:CKIT:STAN:Z0 {value}")

                def get_standard_offset_z0(self) -> float:
                    """
                    Get offset Z0 for standard.

                    Parameter:
                        None

                    Return:
                        float: Offset Z0
                    """
                    return float(self.instrument.query(f":SENS{self.n}:CORR:COLL:CKIT:STAN:Z0?"))
                class Count:
                    """
                    Calibration kit standard count commands.
                    """
                    def __init__(self, instrument, data_handler, channel):
                        self.instrument = instrument
                        self.data_handler = data_handler
                        self.n = channel

                    # SENSe:CORRection:COLLect:CKIT:STANdard:COUNt?
                    def get_standard_count(self) -> int:
                        """
                        Reads out the count of standards in the selected calibration kit.

                        Parameter:
                            None

                        Return:
                            int: Number of standards in the calibration kit
                        """
                        return int(self.instrument.query(f":SENS{self.n}:CORR:COLL:CKIT:STAN:COUN?"))

                class Data:
                    """
                    Calibration kit standard data array commands.
                    """
                    def __init__(self, instrument, data_handler, channel):
                        self.instrument = instrument
                        self.data_handler = data_handler
                        self.n = channel

                    # SENSe:CORRection:COLLect:CKIT:STAN<Std>:DATA <numeric list>
                    def set_standard_data(self, std: int, data_list):
                        """
                        Writes the data array of the data-based calibration standard.

                        Parameter:
                            std (int): Standard number (1..N)
                            data_list (list): Data array as per documentation

                        Return:
                            None
                        """
                        data_str = ",".join(str(float(x)) for x in data_list)
                        self.instrument.write(f":SENS{self.n}:CORR:COLL:CKIT:STAN{std}:DATA {data_str}")

                    # SENSe:CORRection:COLLect:CKIT:STAN<Std>:DATA?
                    def get_standard_data(self, std: int):
                        """
                        Reads out the data array of the data-based calibration standard.

                        Parameter:
                            std (int): Standard number (1..N)

                        Return:
                            list: Data array
                        """
                        data = self.instrument.query(f":SENS{self.n}:CORR:COLL:CKIT:STAN{std}:DATA?")
                        if self.data_handler.is_auto_saving_data_enabled():
                            self.data_handler.write_to_file(self, f"KIT_STANDARD_CALIB_{self.n}", data, file_type = EFileType.CSV)
                        return self.data_handler.parse_array(data)

                class Delay:
                    """
                    Calibration kit standard offset delay commands.
                    """
                    def __init__(self, instrument, data_handler, channel):
                        self.instrument = instrument
                        self.data_handler = data_handler
                        self.n = channel

                    # SENSe:CORRection:COLLect:CKIT:STAN<Std>:DELay <numeric>
                    def set_standard_delay(self, std: int, value: float):
                        """
                        Sets the offset delay value for the calibration standard.

                        Parameter:
                            std (int): Standard number (1..N)
                            value (float): Offset delay value (–1E18 to 1E18), in seconds

                        Return:
                            None
                        """
                        self.instrument.write(f":SENS{self.n}:CORR:COLL:CKIT:STAN{std}:DEL {value}")

                    # SENSe:CORRection:COLLect:CKIT:STAN<Std>:Delay?
                    def get_standard_delay(self, std: int) -> float:
                        """
                        Reads out the offset delay value for the calibration standard.

                        Parameter:
                            std (int): Standard number (1..N)

                        Return:
                            float: Offset delay value in seconds
                        """
                        return float(self.instrument.query(f":SENS{self.n}:CORR:COLL:CKIT:STAN{std}:DEL?"))

                class Fmax:
                    """
                    Calibration kit standard maximum frequency commands.
                    """
                    def __init__(self, instrument, data_handler, channel):
                        self.instrument = instrument
                        self.data_handler = data_handler
                        self.n = channel

                    # SENSe:CORRection:COLLect:CKIT:STAN<Std>:FMAXimum <numeric>
                    def set_standard_fmax(self, std: int, value: float):
                        """
                        Sets the maximum frequency limit of the calibration standard.

                        Parameter:
                            std (int): Standard number (1..N)
                            value (float): Maximum frequency limit (0 to 1E14), in Hz

                        Return:
                            None
                        """
                        self.instrument.write(f":SENS{self.n}:CORR:COLL:CKIT:STAN{std}:FMAX {value}")

                    # SENSe:CORRection:COLLect:CKIT:STAN<Std>:FMAXimum?
                    def get_standard_fmax(self, std: int) -> float:
                        """
                        Reads out the maximum frequency limit of the calibration standard.

                        Parameter:
                            std (int): Standard number (1..N)

                        Return:
                            float: Maximum frequency limit in Hz
                        """
                        return float(self.instrument.query(f":SENS{self.n}:CORR:COLL:CKIT:STAN{std}:FMAX?"))

                class StandardFmin:
                    """
                    Calibration kit standard minimum frequency commands.
                    """
                    def __init__(self, instrument, data_handler, channel):
                        self.instrument = instrument
                        self.data_handler = data_handler
                        self.n = channel

                    # SENSe:CORRection:COLLect:CKIT:STAN<Std>:FMINimum <numeric>
                    def set_standard_fmin(self, std: int, value: float):
                        """
                        Sets the minimum frequency limit of the calibration standard.

                        Parameter:
                            std (int): Standard number (1..N)
                            value (float): Minimum frequency limit (0 to 1E14), in Hz

                        Return:
                            None
                        """
                        self.instrument.write(f":SENS{self.n}:CORR:COLL:CKIT:STAN{std}:FMIN {value}")

                    # SENSe:CORRection:COLLect:CKIT:STAN<Std>:FMINimum?
                    def get_standard_fmin(self, std: int) -> float:
                        """
                        Reads out the minimum frequency limit of the calibration standard.

                        Parameter:
                            std (int): Standard number (1..N)

                        Return:
                            float: Minimum frequency limit in Hz
                        """
                        return float(self.instrument.query(f":SENS{self.n}:CORR:COLL:CKIT:STAN{std}:FMIN?"))

                class Insert:
                    """
                    Calibration kit standard insert commands.
                    """
                    def __init__(self, instrument, data_handler, channel):
                        self.instrument = instrument
                        self.data_handler = data_handler
                        self.n = channel

                    # SENSe:CORRection:COLLect:CKIT:STAN<Std>:INSert
                    def insert_standard(self, std: int):
                        """
                        Inserts the calibration standard into the selected calibration kit.

                        Parameter:
                            std (int): Standard number (1..N)

                        Return:
                            None
                        """
                        self.instrument.write(f":SENS{self.n}:CORR:COLL:CKIT:STAN{std}:INS")

                class StandardL0:
                    """
                    Calibration kit short standard L0 commands.
                    """
                    def __init__(self, instrument, data_handler, channel):
                        self.instrument = instrument
                        self.data_handler = data_handler
                        self.n = channel

                    # SENSe:CORRection:COLLect:CKIT:STAN<Std>:L0 <numeric>
                    def set_l0(self, std: int, value: float):
                        """
                        Set the L0 value for the short calibration standard.

                        Parameter:
                            std (int): Standard number (1..N)
                            value (float): L0 value (–1E18 to 1E18), units 1E–12 H

                        Return:
                            None
                        """
                        self.instrument.write(f":SENS{self.n}:CORR:COLL:CKIT:STAN{std}:L0 {value}")

                    # SENSe:CORRection:COLLect:CKIT:STAN<Std>:L0?
                    def get_l0(self, std: int) -> float:
                        """
                        Get the L0 value for the short calibration standard.

                        Parameter:
                            std (int): Standard number (1..N)

                        Return:
                            float: L0 value
                        """
                        return float(self.instrument.query(f":SENS{self.n}:CORR:COLL:CKIT:STAN{std}:L0?"))

                class L1:
                    """
                    Calibration kit short standard L1 commands.
                    """
                    def __init__(self, instrument, data_handler, channel):
                        self.instrument = instrument
                        self.data_handler = data_handler
                        self.n = channel

                    # SENSe:CORRection:COLLect:CKIT:STAN<Std>:L1 <numeric>
                    def set_l1(self, std: int, value: float):
                        """
                        Set the L1 value for the short calibration standard.

                        Parameter:
                            std (int): Standard number (1..N)
                            value (float): L1 value (–1E18 to 1E18), units 1E–24 H/Hz

                        Return:
                            None
                        """
                        self.instrument.write(f":SENS{self.n}:CORR:COLL:CKIT:STAN{std}:L1 {value}")

                    # SENSe:CORRection:COLLect:CKIT:STAN<Std>:L1?
                    def get_l1(self, std: int) -> float:
                        """
                        Get the L1 value for the short calibration standard.

                        Parameter:
                            std (int): Standard number (1..N)

                        Return:
                            float: L1 value
                        """
                        return float(self.instrument.query(f":SENS{self.n}:CORR:COLL:CKIT:STAN{std}:L1?"))

                class L2:
                    """
                    Calibration kit short standard L2 commands.
                    """
                    def __init__(self, instrument, data_handler, channel):
                        self.instrument = instrument
                        self.data_handler = data_handler
                        self.n = channel

                    # SENSe:CORRection:COLLect:CKIT:STAN<Std>:L2 <numeric>
                    def set_l2(self, std: int, value: float):
                        """
                        Set the L2 value for the short calibration standard.

                        Parameter:
                            std (int): Standard number (1..N)
                            value (float): L2 value (–1E18 to 1E18), units 1E–33 H/Hz^2

                        Return:
                            None
                        """
                        self.instrument.write(f":SENS{self.n}:CORR:COLL:CKIT:STAN{std}:L2 {value}")

                    # SENSe:CORRection:COLLect:CKIT:STAN<Std>:L2?
                    def get_l2(self, std: int) -> float:
                        """
                        Get the L2 value for the short calibration standard.

                        Parameter:
                            std (int): Standard number (1..N)

                        Return:
                            float: L2 value
                        """
                        return float(self.instrument.query(f":SENS{self.n}:CORR:COLL:CKIT:STAN{std}:L2?"))

                class L3:
                    """
                    Calibration kit short standard L3 commands.
                    """
                    def __init__(self, instrument, data_handler, channel):
                        self.instrument = instrument
                        self.data_handler = data_handler
                        self.n = channel

                    # SENSe:CORRection:COLLect:CKIT:STAN<Std>:L3 <numeric>
                    def set_l3(self, std: int, value: float):
                        """
                        Set the L3 value for the short calibration standard.

                        Parameter:
                            std (int): Standard number (1..N)
                            value (float): L3 value (–1E18 to 1E18), units 1E–42 H/Hz^3

                        Return:
                            None
                        """
                        self.instrument.write(f":SENS{self.n}:CORR:COLL:CKIT:STAN{std}:L3 {value}")

                    # SENSe:CORRection:COLLect:CKIT:STAN<Std>:L3?
                    def get_l3(self, std: int) -> float:
                        """
                        Get the L3 value for the short calibration standard.

                        Parameter:
                            std (int): Standard number (1..N)

                        Return:
                            float: L3 value
                        """
                        return float(self.instrument.query(f":SENS{self.n}:CORR:COLL:CKIT:STAN{std}:L3?"))

                class Label:
                    """
                    Calibration kit standard label commands.
                    """
                    def __init__(self, instrument, data_handler, channel):
                        self.instrument = instrument
                        self.data_handler = data_handler
                        self.n = channel

                    # SENSe:CORRection:COLLect:CKIT:STAN<Std>:LABel <string>
                    def set_label(self, std: int, label: str):
                        """
                        Set the label for the calibration standard.

                        Parameter:
                            std (int): Standard number (1..N)
                            label (str): Label string (up to 254 characters)

                        Return:
                            None
                        """
                        if len(label) > 254:
                            raise ValueError("label must be up to 254 characters")
                        self.instrument.write(f":SENS{self.n}:CORR:COLL:CKIT:STAN{std}:LAB \"{label}\"")

                    # SENSe:CORRection:COLLect:CKIT:STAN<Std>:LABel?
                    def get_label(self, std: int) -> str:
                        """
                        Get the label for the calibration standard.

                        Parameter:
                            std (int): Standard number (1..N)

                        Return:
                            str: Label string
                        """
                        return self.instrument.query(f":SENS{self.n}:CORR:COLL:CKIT:STAN{std}:LAB?").strip()
                
                    # SENS:CORR:COLL:CKIT - Calibration kit selection
                    def select_calibration_kit(self, kit: int):
                        """
                        Select calibration kit.

                        Parameter:
                            kit (int): Calibration kit number

                        Return:
                            None
                        """
                        self.instrument.write(f":SENS{self.n}:CORR:COLL:CKIT {kit}")

                    # SENS:CORR:COLL:CKIT:LAB - Calibration kit label
                    def set_calibration_kit_label(self, label: str):
                        """
                        Set calibration kit label.

                        Parameter:
                            label (str): Calibration kit label

                        Return:
                            None
                        """
                        self.instrument.write(f":SENS{self.n}:CORR:COLL:CKIT:LAB \"{label}\"")

                    def get_calibration_kit_label(self) -> str:
                        """
                        Get calibration kit label.

                        Parameter:
                            None

                        Return:
                            str: Calibration kit label
                        """
                        return self.instrument.query(f":SENS{self.n}:CORR:COLL:CKIT:LAB?").strip()

                    # SENS:CORR:COLL:CKIT:RES - Remove or restore a calibration kit
                    def remove_calibration_kit(self):
                        """
                        Remove a calibration kit.

                        Parameter:
                            None

                        Return:
                            None
                        """
                        self.instrument.write(f":SENS{self.n}:CORR:COLL:CKIT:RES")


            
            class Select:
                """
                Calibration kit selection commands.
                """
                def __init__(self, instrument, data_handler, channel):
                    self.instrument = instrument
                    self.data_handler = data_handler
                    self.n = channel
                    self.description = self.Description(instrument, data_handler, channel)
                    self.order = self.Order(instrument, data_handler, channel)

                # SENSe:CORRection:COLLect:CKIT[:SELect] <numeric>
                def select_cal_kit(self, kit: int):
                    """
                    Set the number of the selected calibration kit in the table of calibration kits.

                    Parameter:
                        kit (int): Calibration kit number (1-64)

                    Return:
                        None
                    """
                    if not (1 <= kit <= 64):
                        raise ValueError("kit must be 1-64")
                    self.instrument.write(f":SENS{self.n}:CORR:COLL:CKIT:SEL {kit}")

                # SENSe:CORRection:COLLect:CKIT[:SELect]?
                def get_selected_cal_kit(self) -> int:
                    """
                    Get the number of the selected calibration kit in the table of calibration kits.

                    Parameter:
                        None

                    Return:
                        int: Calibration kit number
                    """
                    return int(self.instrument.query(f":SENS{self.n}:CORR:COLL:CKIT:SEL?"))
                class Description:
                    """
                    Calibration kit description string commands.
                    """
                    def __init__(self, instrument, data_handler, channel):
                        self.instrument = instrument
                        self.data_handler = data_handler
                        self.n = channel

                    # SENSe:CORRection:COLLect:CKIT:DESCription <string>
                    def set_description(self, description: str):
                        """
                        Set the calibration kit description string.

                        Parameter:
                            description (str): Description string (up to 254 characters)

                        Return:
                            None
                        """
                        if len(description) > 254:
                            raise ValueError("description must be up to 254 characters")
                        self.instrument.write(f":SENS{self.n}:CORR:COLL:CKIT:DESC \"{description}\"")

                    # SENSe:CORRection:COLLect:CKIT:DESCription?
                    def get_description(self) -> str:
                        """
                        Get the calibration kit description string.

                        Parameter:
                            None

                        Return:
                            str: Description string
                        """
                        return self.instrument.query(f":SENS{self.n}:CORR:COLL:CKIT:DESC?").strip()

                class Order:
                    """
                    Calibration kit order assignment commands.
                    """
                    def __init__(self, instrument, data_handler, channel):
                        self.instrument = instrument
                        self.data_handler = data_handler
                        self.n = channel

                    # SENSe:CORRection:COLLect:CKIT:ORDer:LOAD <port>,<numeric>
                    def set_load_standard(self, port: int, standard_num: int):
                        """
                        Set the number of the calibration standard assigned to the LOAD class for the specified port.

                        Parameter:
                            port (int): Port number (1-4)
                            standard_num (int): Standard number

                        Return:
                            None
                        """
                        if not (1 <= port <= 4):
                            raise ValueError("port must be 1-4")
                        self.instrument.write(f":SENS{self.n}:CORR:COLL:CKIT:ORD:LOAD {port},{standard_num}")

                    # SENSe:CORRection:COLLect:CKIT:ORDer:LOAD? <port>
                    def get_load_standard(self, port: int) -> int:
                        """
                        Get the number of the calibration standard assigned to the LOAD class for the specified port.

                        Parameter:
                            port (int): Port number (1-4)

                        Return:
                            int: Standard number
                        """
                        if not (1 <= port <= 4):
                            raise ValueError("port must be 1-4")
                        return int(self.instrument.query(f":SENS{self.n}:CORR:COLL:CKIT:ORD:LOAD? {port}"))

                    # SENSe:CORRection:COLLect:CKIT:ORDer:OPEN <port>,<numeric>
                    def set_open_standard(self, port: int, standard_num: int):
                        """
                        Set the number of the calibration standard assigned to the OPEN class for the specified port.

                        Parameter:
                            port (int): Port number (1-4)
                            standard_num (int): Standard number

                        Return:
                            None
                        """
                        if not (1 <= port <= 4):
                            raise ValueError("port must be 1-4")
                        self.instrument.write(f":SENS{self.n}:CORR:COLL:CKIT:ORD:OPEN {port},{standard_num}")

                    # SENSe:CORRection:COLLect:CKIT:ORDer:OPEN? <port>
                    def get_open_standard(self, port: int) -> int:
                        """
                        Get the number of the calibration standard assigned to the OPEN class for the specified port.

                        Parameter:
                            port (int): Port number (1-4)

                        Return:
                            int: Standard number
                        """
                        if not (1 <= port <= 4):
                            raise ValueError("port must be 1-4")
                        return int(self.instrument.query(f":SENS{self.n}:CORR:COLL:CKIT:ORD:OPEN? {port}"))

                    # SENSe:CORRection:COLLect:CKIT:ORDer:SELect <numeric>
                    def set_subclass(self, subclass_num: int):
                        """
                        Set the subclass number for calibration standard class assignment.

                        Parameter:
                            subclass_num (int): Subclass number (1-8)

                        Return:
                            None
                        """
                        if not (1 <= subclass_num <= 8):
                            raise ValueError("subclass_num must be 1-8")
                        self.instrument.write(f":SENS{self.n}:CORR:COLL:CKIT:ORD:SEL {subclass_num}")

                    # SENSe:CORRection:COLLect:CKIT:ORDer:SELect?
                    def get_subclass(self) -> int:
                        """
                        Get the subclass number for calibration standard class assignment.

                        Parameter:
                            None

                        Return:
                            int: Subclass number
                        """
                        return int(self.instrument.query(f":SENS{self.n}:CORR:COLL:CKIT:ORD:SEL?"))

                    # SENSe:CORRection:COLLect:CKIT:ORDer:SHORt <port>,<numeric>
                    def set_short_standard(self, port: int, standard_num: int):
                        """
                        Set the number of the calibration standard assigned to the SHORT class for the specified port.

                        Parameter:
                            port (int): Port number (1-4)
                            standard_num (int): Standard number

                        Return:
                            None
                        """
                        if not (1 <= port <= 4):
                            raise ValueError("port must be 1-4")
                        self.instrument.write(f":SENS{self.n}:CORR:COLL:CKIT:ORD:SHOR {port},{standard_num}")

                    # SENSe:CORRection:COLLect:CKIT:ORDer:SHORt? <port>
                    def get_short_standard(self, port: int) -> int:
                        """
                        Get the number of the calibration standard assigned to the SHORT class for the specified port.

                        Parameter:
                            port (int): Port number (1-4)

                        Return:
                            int: Standard number
                        """
                        if not (1 <= port <= 4):
                            raise ValueError("port must be 1-4")
                        return int(self.instrument.query(f":SENS{self.n}:CORR:COLL:CKIT:ORD:SHOR? {port}"))
                    # SENSe:CORRection:COLLect:CKIT:ORDer:THRU <port1>,<port2>,<numeric>
                    def set_thru_standard(self, port1: int, port2: int, standard_num: int):
                        """
                        Set the number of the calibration standard assigned to the THRU class for the measurement between the specified ports.

                        Parameter:
                            port1 (int): Receiver port number (1-4)
                            port2 (int): Source port number (1-4)
                            standard_num (int): Standard number

                        Return:
                            None
                        """
                        if not (1 <= port1 <= 4 and 1 <= port2 <= 4):
                            raise ValueError("port1 and port2 must be 1-4")
                        self.instrument.write(f":SENS{self.n}:CORR:COLL:CKIT:ORD:THRU {port1},{port2},{standard_num}")

                    # SENSe:CORRection:COLLect:CKIT:ORDer:THRU? <port1>,<port2>
                    def get_thru_standard(self, port1: int, port2: int) -> int:
                        """
                        Get the number of the calibration standard assigned to the THRU class for the measurement between the specified ports.

                        Parameter:
                            port1 (int): Receiver port number (1-4)
                            port2 (int): Source port number (1-4)

                        Return:
                            int: Standard number
                        """
                        if not (1 <= port1 <= 4 and 1 <= port2 <= 4):
                            raise ValueError("port1 and port2 must be 1-4")
                        return int(self.instrument.query(f":SENS{self.n}:CORR:COLL:CKIT:ORD:THRU? {port1},{port2}"))

                    # SENSe:CORRection:COLLect:CKIT:ORDer:TRLLine <port1>,<port2>,<numeric>
                    def set_trl_line_standard(self, port1: int, port2: int, standard_num: int):
                        """
                        Set the number of the calibration standard assigned to the TRL LINE class for the measurement between the specified ports.

                        Parameter:
                            port1 (int): Receiver port number (1-4)
                            port2 (int): Source port number (1-4)
                            standard_num (int): Standard number

                        Return:
                            None
                        """
                        if not (1 <= port1 <= 4 and 1 <= port2 <= 4):
                            raise ValueError("port1 and port2 must be 1-4")
                        self.instrument.write(f":SENS{self.n}:CORR:COLL:CKIT:ORD:TRLL {port1},{port2},{standard_num}")

                    # SENSe:CORRection:COLLect:CKIT:ORDer:TRLLine? <port1>,<port2>
                    def get_trl_line_standard(self, port1: int, port2: int) -> int:
                        """
                        Get the number of the calibration standard assigned to the TRL LINE class for the measurement between the specified ports.

                        Parameter:
                            port1 (int): Receiver port number (1-4)
                            port2 (int): Source port number (1-4)

                        Return:
                            int: Standard number
                        """
                        if not (1 <= port1 <= 4 and 1 <= port2 <= 4):
                            raise ValueError("port1 and port2 must be 1-4")
                        return int(self.instrument.query(f":SENS{self.n}:CORR:COLL:CKIT:ORD:TRLL? {port1},{port2}"))

                    # SENSe:CORRection:COLLect:CKIT:ORDer:TRLThru <port1>,<port2>,<numeric>
                    def set_trl_thru_standard(self, port1: int, port2: int, standard_num: int):
                        """
                        Set the number of the calibration standard assigned to the TRL THRU class for the measurement between the specified ports.

                        Parameter:
                            port1 (int): Receiver port number (1-4)
                            port2 (int): Source port number (1-4)
                            standard_num (int): Standard number

                        Return:
                            None
                        """
                        if not (1 <= port1 <= 4 and 1 <= port2 <= 4):
                            raise ValueError("port1 and port2 must be 1-4")
                        self.instrument.write(f":SENS{self.n}:CORR:COLL:CKIT:ORD:TRLT {port1},{port2},{standard_num}")

                    # SENSe:CORRection:COLLect:CKIT:ORDer:TRLThru? <port1>,<port2>
                    def get_trl_thru_standard(self, port1: int, port2: int) -> int:
                        """
                        Get the number of the calibration standard assigned to the TRL THRU class for the measurement between the specified ports.

                        Parameter:
                            port1 (int): Receiver port number (1-4)
                            port2 (int): Source port number (1-4)

                        Return:
                            int: Standard number
                        """
                        if not (1 <= port1 <= 4 and 1 <= port2 <= 4):
                            raise ValueError("port1 and port2 must be 1-4")
                        return int(self.instrument.query(f":SENS{self.n}:CORR:COLL:CKIT:ORD:TRLT? {port1},{port2}"))

                    # SENSe:CORRection:COLLect:CKIT:ORDer:TRLReflect <port>,<numeric>
                    def set_trl_reflect_standard(self, port: int, standard_num: int):
                        """
                        Set the number of the calibration standard assigned to the TRL REFLECT class for the specified port.

                        Parameter:
                            port (int): Port number (1-4)
                            standard_num (int): Standard number

                        Return:
                            None
                        """
                        if not (1 <= port <= 4):
                            raise ValueError("port must be 1-4")
                        self.instrument.write(f":SENS{self.n}:CORR:COLL:CKIT:ORD:TRLR {port},{standard_num}")

                    # SENSe:CORRection:COLLect:CKIT:ORDer:TRLReflect? <port>
                    def get_trl_reflect_standard(self, port: int) -> int:
                        """
                        Get the number of the calibration standard assigned to the TRL REFLECT class for the specified port.

                        Parameter:
                            port (int): Port number (1-4)

                        Return:
                            int: Standard number
                        """
                        if not (1 <= port <= 4):
                            raise ValueError("port must be 1-4")
                        return int(self.instrument.query(f":SENS{self.n}:CORR:COLL:CKIT:ORD:TRLR? {port}"))

                    # SENSe:CORRection:COLLect:CKIT:RESet
                    def reset_calibration_kit(self):
                        """
                        Reset the calibration kit to the factory settings.

                        Parameter:
                            None

                        Return:
                            None
                        """
                        self.instrument.write(f":SENS{self.n}:CORR:COLL:CKIT:RES")
            class Arbitrary:
                """
                Calibration kit arbitrary impedance commands.
                """
                def __init__(self, instrument, data_handler, channel):
                    self.instrument = instrument
                    self.data_handler = data_handler
                    self.n = channel

                # SENSe:CORRection:COLLect:CKIT:STAN<Std>:ARBitrary <numeric>
                def set_arbitrary_impedance(self, std: int, value: float):
                    """
                    Set the arbitrary impedance value for the load standard.

                    Parameter:
                        std (int): Standard number (1..N)
                        value (float): Impedance value (-1E18 to 1E18)

                    Return:
                        None
                    """
                    self.instrument.write(f":SENS{self.n}:CORR:COLL:CKIT:STAN{std}:ARB {value}")

                # SENSe:CORRection:COLLect:CKIT:STAN<Std>:ARBitrary?
                def get_arbitrary_impedance(self, std: int) -> float:
                    """
                    Get the arbitrary impedance value for the load standard.

                    Parameter:
                        std (int): Standard number (1..N)

                    Return:
                        float: Impedance value
                    """
                    return float(self.instrument.query(f":SENS{self.n}:CORR:COLL:CKIT:STAN{std}:ARB?"))

            class OpenCapacitance:
                """
                Calibration kit open standard capacitance commands.
                """
                def __init__(self, instrument, data_handler, channel):
                    self.instrument = instrument
                    self.data_handler = data_handler
                    self.n = channel

                # SENSe:CORRection:COLLect:CKIT:STAN<Std>:C0 <numeric>
                def set_c0(self, std: int, value: float):
                    """
                    Set the C0 value for the open calibration standard.

                    Parameter:
                        std (int): Standard number (1..N)
                        value (float): C0 value (-1E18 to 1E18), units 1E-15 F

                    Return:
                        None
                    """
                    self.instrument.write(f":SENS{self.n}:CORR:COLL:CKIT:STAN{std}:C0 {value}")

                # SENSe:CORRection:COLLect:CKIT:STAN<Std>:C0?
                def get_c0(self, std: int) -> float:
                    """
                    Get the C0 value for the open calibration standard.

                    Parameter:
                        std (int): Standard number (1..N)

                    Return:
                        float: C0 value
                    """
                    return float(self.instrument.query(f":SENS{self.n}:CORR:COLL:CKIT:STAN{std}:C0?"))

                # SENSe:CORRection:COLLect:CKIT:STAN<Std>:C1 <numeric>
                def set_c1(self, std: int, value: float):
                    """
                    Set the C1 value for the open calibration standard.

                    Parameter:
                        std (int): Standard number (1..N)
                        value (float): C1 value (-1E18 to 1E18), units 1E-27 F/Hz

                    Return:
                        None
                    """
                    self.instrument.write(f":SENS{self.n}:CORR:COLL:CKIT:STAN{std}:C1 {value}")

                # SENSe:CORRection:COLLect:CKIT:STAN<Std>:C1?
                def get_c1(self, std: int) -> float:
                    """
                    Get the C1 value for the open calibration standard.

                    Parameter:
                        std (int): Standard number (1..N)

                    Return:
                        float: C1 value
                    """
                    return float(self.instrument.query(f":SENS{self.n}:CORR:COLL:CKIT:STAN{std}:C1?"))

                # SENSe:CORRection:COLLect:CKIT:STAN<Std>:C2 <numeric>
                def set_c2(self, std: int, value: float):
                    """
                    Set the C2 value for the open calibration standard.

                    Parameter:
                        std (int): Standard number (1..N)
                        value (float): C2 value (-1E18 to 1E18), units 1E-36 F/Hz^2

                    Return:
                        None
                    """
                    self.instrument.write(f":SENS{self.n}:CORR:COLL:CKIT:STAN{std}:C2 {value}")

                # SENSe:CORRection:COLLect:CKIT:STAN<Std>:C2?
                def get_c2(self, std: int) -> float:
                    """
                    Get the C2 value for the open calibration standard.

                    Parameter:
                        std (int): Standard number (1..N)

                    Return:
                        float: C2 value
                    """
                    return float(self.instrument.query(f":SENS{self.n}:CORR:COLL:CKIT:STAN{std}:C2?"))

                # SENSe:CORRection:COLLect:CKIT:STAN<Std>:C3 <numeric>
                def set_c3(self, std: int, value: float):
                    """
                    Set the C3 value for the open calibration standard.

                    Parameter:
                        std (int): Standard number (1..N)
                        value (float): C3 value (-1E18 to 1E18), units 1E-45 F/Hz^3

                    Return:
                        None
                    """
                    self.instrument.write(f":SENS{self.n}:CORR:COLL:CKIT:STAN{std}:C3 {value}")

                # SENSe:CORRection:COLLect:CKIT:STAN<Std>:C3?
                def get_c3(self, std: int) -> float:
                    """
                    Get the C3 value for the open calibration standard.

                    Parameter:
                        std (int): Standard number (1..N)

                    Return:
                        float: C3 value
                    """
                    return float(self.instrument.query(f":SENS{self.n}:CORR:COLL:CKIT:STAN{std}:C3?"))
            
        class Collection:
            """
            addition Calibration collection related commands.
            """
            def __init__(self, instrument, data_handler, channel):
                self.instrument = instrument
                self.data_handler = data_handler
                self.n = channel
                self.data = self.Data(instrument, data_handler, channel)
                
            
            # SENS:CORR:COLL:CLE - Clears measurement data of calibration standards
            def clear_collection(self):
                """
                Clear the measurement data of the calibration standards.

                Parameter:
                    None

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:CORR:COLL:CLE")

            class Data:
                """
                Calibration isolation data commands.
                """
                def __init__(self, instrument, data_handler, channel):
                    self.instrument = instrument
                    self.data_handler = data_handler
                    self.n = channel

                # SENS:CORR:COLL:DATA:ISOLation <rcvport>,<srcport>,<numeric list>
                def set_isolation_data(self, rcvport: int, srcport: int, data_list):
                    """
                    Write the array of the isolation calibration measurement.

                    Parameter:
                        rcvport (int): Receiver port (1-4)
                        srcport (int): Source port (1-4)
                        data_list (list): Array of real/imaginary pairs

                    Return:
                        None
                    """
                    if not (1 <= rcvport <= 4 and 1 <= srcport <= 4):
                        raise ValueError("rcvport and srcport must be 1-4")
                    data_str = ",".join(str(float(x)) for x in data_list)
                    self.instrument.write(f":SENS{self.n}:CORR:COLL:DATA:ISOL {rcvport},{srcport},{data_str}")

                # SENS:CORR:COLL:DATA:ISOLation? <rcvport>,<srcport>
                def get_isolation_data(self, rcvport: int, srcport: int):
                    """
                    Read out the array of the isolation calibration measurement.

                    Parameter:
                        rcvport (int): Receiver port (1-4)
                        srcport (int): Source port (1-4)

                    Return:
                        list: Array of real/imaginary pairs
                    """
                    if not (1 <= rcvport <= 4 and 1 <= srcport <= 4):
                        raise ValueError("rcvport and srcport must be 1-4")
                    data = self.instrument.query(f":SENS{self.n}:CORR:COLL:DATA:ISOL? {rcvport},{srcport}")
                    if self.data_handler.is_auto_saving_data_enabled():
                        self.data_handler.write_to_file(self, f"ISO_CALIB_SRCPORT{srcport}_RCVPORT{rcvport}", data, file_type = EFileType.CSV)
                    return self.data_handler.parse_array(data)

        
        class AutoCal:
            """
            AutoCal module related commands.
            """
            def __init__(self, instrument, data_handler, channel):
                self.instrument = instrument
                self.data_handler = data_handler
                self.n = channel
                self.unknown_thru = self.UnknownThru(instrument, data_handler, channel)

            # SENS:CORR:COLL:ECAL:CCH[:ACQuire] - Confidence check of calibration coefficients
            def execute_confidence_check(self):
                """
                Executes the confidence check of the calibration coefficients using the AutoCal module.

                Parameter:
                    None

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:CORR:COLL:ECAL:CCH:ACQuire")

            # SENS:CORR:COLL:ECAL:ERESponse <rcvport>,<srcport>
            def execute_one_path_two_port_cal(self, rcvport: int, srcport: int):
                """
                Executes one path two-port calibration between the specified ports using the AutoCal module.

                Parameter:
                    rcvport (int): Receiver port number (1-4)
                    srcport (int): Source port number (1-4)

                Return:
                    None
                """
                if not (1 <= rcvport <= 4 and 1 <= srcport <= 4):
                    raise ValueError("rcvport and srcport must be 1-4")
                self.instrument.write(f":SENS{self.n}:CORR:COLL:ECAL:ERES {rcvport},{srcport}")

            # SENS:CORR:COLL:ECAL:INFormation?
            def get_autocal_information(self) -> str:
                """
                Gets information on the AutoCal Module connected to the Network Analyzer.

                Parameter:
                    None

                Return:
                    str: Information string (comma separated fields)
                """
                return self.instrument.query(f":SENS{self.n}:CORR:COLL:ECAL:INFormation?").strip()

            # SENS:CORR:COLL:ECAL:ORIentation:EXECute
            def execute_auto_orientation(self):
                """
                Executes the Auto-Orientation procedure of the AutoCal Module.

                Parameter:
                    None

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:CORR:COLL:ECAL:ORIentation:EXECute")

            # SENS:CORR:COLL:ECAL:ORIentation:STATe {OFF|ON|0|1}
            def enable_auto_orientation(self, enable: bool):
                """
                Turns the Auto-Orientation function ON/OFF for AutoCal calibration.

                Parameter:
                    enable (bool): True to enable, False to disable

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:CORR:COLL:ECAL:ORIentation:STATe {1 if enable else 0}")

            def is_auto_orientation_enabled(self) -> bool:
                """
                Query if the Auto-Orientation function is enabled.

                Parameter:
                    None

                Return:
                    bool: True if enabled, False otherwise
                """
                return bool(int(self.instrument.query(f":SENS{self.n}:CORR:COLL:ECAL:ORIentation:STATe?")))

            # SENS:CORR:COLL:ECAL:PATH <numeric1>,<numeric2>
            def set_autocal_path(self, analyzer_port: int, autocal_port: int):
                """
                Sets the AutoCal module port number connected to a specified port of the Network Analyzer.

                Parameter:
                    analyzer_port (int): Network Analyzer Port Number (1-4)
                    autocal_port (int): AutoCal Module Port Number (1-4)

                Return:
                    None
                """
                if not (1 <= analyzer_port <= 4):
                    raise ValueError("analyzer_port must be 1-4")
                if not (1 <= autocal_port <= 4):
                    raise ValueError("autocal_port must be 1-4")
                self.instrument.write(f":SENS{self.n}:CORR:COLL:ECAL:PATH {analyzer_port},{autocal_port}")

            # SENS:CORR:COLL:ECAL:PATH? <numeric1>
            def get_autocal_path(self, analyzer_port: int) -> int:
                """
                Reads out the AutoCal module port number connected to a specified port of the Network Analyzer.

                Parameter:
                    analyzer_port (int): Network Analyzer Port Number (1-4)

                Return:
                    int: AutoCal Module Port Number (1-4)
                """
                if not (1 <= analyzer_port <= 4):
                    raise ValueError("analyzer_port must be 1-4")
                return int(self.instrument.query(f":SENS{self.n}:CORR:COLL:ECAL:PATH? {analyzer_port}"))
            # SENS:CORR:COLL:ECAL:SOLT1 <port>
            def execute_solt1_calibration(self, port: int):
                """
                Executes one-port calibration of the specified port using the AutoCal module.

                Parameter:
                    port (int): Port number (1-4)

                Return:
                    None
                """
                if not (1 <= port <= 4):
                    raise ValueError("port must be 1-4")
                self.instrument.write(f":SENS{self.n}:CORR:COLL:ECAL:SOLT1 {port}")

            # SENS:CORR:COLL:ECAL:SOLT2 <port1>,<port2>
            def execute_solt2_calibration(self, port1: int, port2: int):
                """
                Executes full two-port calibration between the specified ports using the AutoCal module.

                Parameter:
                    port1 (int): First port number (1-4)
                    port2 (int): Second port number (1-4)

                Return:
                    None
                """
                if not (1 <= port1 <= 4 and 1 <= port2 <= 4):
                    raise ValueError("port1 and port2 must be 1-4")
                if port1 == port2:
                    raise ValueError("port1 and port2 must be different for SOLT2")
                self.instrument.write(f":SENS{self.n}:CORR:COLL:ECAL:SOLT2 {port1},{port2}")

            # SENS:CORR:COLL:ECAL:SOLT3 <port1>,<port2>,<port3>
            def execute_solt3_calibration(self, port1: int, port2: int, port3: int):
                """
                Executes full three-port calibration between the specified ports using the AutoCal module.

                Parameter:
                    port1 (int): First port number (1-4)
                    port2 (int): Second port number (1-4)
                    port3 (int): Third port number (1-4)

                Return:
                    None
                """
                ports = [port1, port2, port3]
                if any(not (1 <= p <= 4) for p in ports):
                    raise ValueError("All ports must be 1-4")
                if len(set(ports)) != 3:
                    raise ValueError("All ports must be different for SOLT3")
                self.instrument.write(f":SENS{self.n}:CORR:COLL:ECAL:SOLT3 {port1},{port2},{port3}")

            # SENS:CORR:COLL:ECAL:SOLT4 <port1>,<port2>,<port3>,<port4>
            def execute_solt4_calibration(self, port1: int, port2: int, port3: int, port4: int):
                """
                Executes full four-port calibration between the specified ports using the AutoCal module.

                Parameter:
                    port1 (int): First port number (1-4)
                    port2 (int): Second port number (1-4)
                    port3 (int): Third port number (1-4)
                    port4 (int): Fourth port number (1-4)

                Return:
                    None
                """
                ports = [port1, port2, port3, port4]
                if any(not (1 <= p <= 4) for p in ports):
                    raise ValueError("All ports must be 1-4")
                if len(set(ports)) != 4:
                    raise ValueError("All ports must be different for SOLT4")
                self.instrument.write(f":SENS{self.n}:CORR:COLL:ECAL:SOLT4 {port1},{port2},{port3},{port4}")

            # SENS:CORR:COLL:ECAL:THERmo:COMPensation[:STATe] {OFF|ON|0|1}
            def enable_thermo_compensation(self, enable: bool):
                """
                Turns the thermo compensation function ON/OFF for AutoCal calibration.

                Parameter:
                    enable (bool): True to enable, False to disable

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:CORR:COLL:ECAL:THERmo:COMPensation:STATe {1 if enable else 0}")

            def is_thermo_compensation_enabled(self) -> bool:
                """
                Query if the thermo compensation function is enabled for AutoCal calibration.

                Parameter:
                    None

                Return:
                    bool: True if enabled, False otherwise
                """
                return bool(int(self.instrument.query(f":SENS{self.n}:CORR:COLL:ECAL:THERmo:COMPensation:STATe?")))

            # SENS:CORR:COLL:ECAL:UCHar <char>
            def set_autocal_characterization(self, char: str):
                """
                Sets the characterization number used when executing AutoCal.

                Parameter:
                    char (str): Characterization, one of ['CHAR0', 'CHAR1', 'CHAR2', 'CHAR3']

                Return:
                    None
                """
                allowed = ['CHAR0', 'CHAR1', 'CHAR2', 'CHAR3']
                if char not in allowed:
                    raise ValueError(f"char must be one of {allowed}")
                self.instrument.write(f":SENS{self.n}:CORR:COLL:ECAL:UCHar {char}")

            def get_autocal_characterization(self) -> str:
                """
                Reads out the characterization number used when executing AutoCal.

                Parameter:
                    None

                Return:
                    str: Characterization ('CHAR0', 'CHAR1', 'CHAR2', 'CHAR3')
                """
                return self.instrument.query(f":SENS{self.n}:CORR:COLL:ECAL:UCHar?").strip()
            class UnknownThru:
                """
                AutoCal Unknown Thru feature commands.
                """
                def __init__(self, instrument, data_handler, channel):
                    self.instrument = instrument
                    self.data_handler = data_handler
                    self.n = channel

                # SENS:CORR:COLL:ECAL:UTHRu:STATe {OFF|ON|0|1}
                def enable_unknown_thru(self, enable: bool):
                    """
                    Turns the Unknown Thru feature ON/OFF for AutoCal calibration.

                    Parameter:
                        enable (bool): True to enable, False to disable

                    Return:
                        None
                    """
                    self.instrument.write(f":SENS{self.n}:CORR:COLL:ECAL:UTHRu:STATe {1 if enable else 0}")

                def is_unknown_thru_enabled(self) -> bool:
                    """
                    Query if the Unknown Thru feature is enabled for AutoCal calibration.

                    Parameter:
                        None

                    Return:
                        bool: True if enabled, False otherwise
                    """
                    return bool(int(self.instrument.query(f":SENS{self.n}:CORR:COLL:ECAL:UTHRu:STATe?")))
        class AutoCal2:
            """
            AutoCal 2-port/3-port/4-port calibration commands.
            """
            def __init__(self, instrument, data_handler, channel):
                self.instrument = instrument
                self.data_handler = data_handler
                self.n = channel

            # SENS:CORR:COLL:ECAL2 <port 1>,<port 2>
            def execute_ecal2(self, port1: int, port2: int):
                """
                Executes a calibration step using a two-port ACM connecting port1 and port2.

                Parameter:
                    port1 (int): First port number (1-4)
                    port2 (int): Second port number (1-4)

                Return:
                    None
                """
                if not (1 <= port1 <= 4 and 1 <= port2 <= 4):
                    raise ValueError("port1 and port2 must be 1-4")
                if port1 == port2:
                    raise ValueError("port1 and port2 must be different")
                self.instrument.write(f":SENS{self.n}:CORR:COLL:ECAL2 {port1},{port2}")

            # SENS:CORR:COLL:ECAL2:METH:SOLT3 <port1>,<port2>,<port3>
            def set_method_solt3(self, port1: int, port2: int, port3: int):
                """
                Selects ports and sets the type to full 3-port for calibration with the 2-port AutoCal module.

                Parameter:
                    port1 (int): First port number (1-4)
                    port2 (int): Second port number (1-4)
                    port3 (int): Third port number (1-4)

                Return:
                    None
                """
                ports = [port1, port2, port3]
                if any(not (1 <= p <= 4) for p in ports):
                    raise ValueError("All ports must be 1-4")
                if len(set(ports)) != 3:
                    raise ValueError("All ports must be different for SOLT3")
                self.instrument.write(f":SENS{self.n}:CORR:COLL:ECAL2:METH:SOLT3 {port1},{port2},{port3}")

            # SENS:CORR:COLL:ECAL2:METH:SOLT4 <port1>,<port2>,<port3>,<port4>
            def set_method_solt4(self, port1: int, port2: int, port3: int, port4: int):
                """
                Selects ports and sets the type to full 4-port for calibration with the 2-port AutoCal module.

                Parameter:
                    port1 (int): First port number (must be 1)
                    port2 (int): Second port number (must be 2)
                    port3 (int): Third port number (must be 3)
                    port4 (int): Fourth port number (must be 4)

                Return:
                    None
                """
                ports = [port1, port2, port3, port4]
                if ports != [1, 2, 3, 4]:
                    raise ValueError("Ports must be 1, 2, 3, 4 for SOLT4")
                if len(set(ports)) != 4:
                    raise ValueError("All ports must be different for SOLT4")
                self.instrument.write(f":SENS{self.n}:CORR:COLL:ECAL2:METH:SOLT4 {port1},{port2},{port3},{port4}")

            # SENS:CORR:COLL:ECAL2:THRU <port 1>, <port 2>, {[UNKNown] | FLUSh}
            def measure_thru(self, port1: int, port2: int, thru_type: str = "UNKNown"):
                """
                Measures a THRU between port1 and port2 for 3-port/4-port calibration with 2-port ACM.

                Parameter:
                    port1 (int): First port number (1-4)
                    port2 (int): Second port number (1-4)
                    thru_type (str): 'UNKNown' (default) or 'FLUSh'

                Return:
                    None
                """
                allowed = ['UNKNown', 'FLUSh']
                if not (1 <= port1 <= 4 and 1 <= port2 <= 4):
                    raise ValueError("port1 and port2 must be 1-4")
                if port1 == port2:
                    raise ValueError("port1 and port2 must be different")
                if thru_type not in allowed:
                    raise ValueError(f"thru_type must be one of {allowed}")
                self.instrument.write(f":SENS{self.n}:CORR:COLL:ECAL2:THRU {port1},{port2},{thru_type}")

        

        class Isolation:
            """
            Isolation calibration data measurement.
            """
            def __init__(self, instrument, data_handler, channel):
                self.instrument = instrument
                self.data_handler = data_handler
                self.n = channel

            # SENS:CORR:COLL:ISOLation <rcvport>,<srcport>
            def measure_isolation(self, rcvport: int, srcport: int):
                """
                Measures the isolation calibration data between the receiver port and the source port.

                Parameter:
                    rcvport (int): Receiver port number (1-4)
                    srcport (int): Source port number (1-4)

                Return:
                    None
                """
                if not (1 <= rcvport <= 4 and 1 <= srcport <= 4):
                    raise ValueError("rcvport and srcport must be 1-4")
                if rcvport == srcport:
                    raise ValueError("rcvport and srcport must be different")
                self.instrument.write(f":SENS{self.n}:CORR:COLL:ISOL {rcvport},{srcport}")

        class Load:
            """
            Load standard calibration data measurement.
            """
            def __init__(self, instrument, data_handler, channel):
                self.instrument = instrument
                self.data_handler = data_handler
                self.n = channel

            # SENS:CORR:COLL:LOAD <port>
            def measure_load(self, port: int):
                """
                Measures the calibration data of the load standard for the specified port.

                Parameter:
                    port (int): Port number (1-4)

                Return:
                    None
                """
                if not (1 <= port <= 4):
                    raise ValueError("port must be 1-4")
                self.instrument.write(f":SENS{self.n}:CORR:COLL:LOAD {port}")

        class Open:
            """
            Open standard calibration data measurement.
            """
            def __init__(self, instrument, data_handler, channel):
                self.instrument = instrument
                self.data_handler = data_handler
                self.n = channel

            # SENS:CORR:COLL:OPEN <port>
            def measure_open(self, port: int):
                """
                Measures the calibration data of the open standard for the specified port.

                Parameter:
                    port (int): Port number (1-4)

                Return:
                    None
                """
                if not (1 <= port <= 4):
                    raise ValueError("port must be 1-4")
                self.instrument.write(f":SENS{self.n}:CORR:COLL:OPEN {port}")

        class Short:
            """
            Short standard calibration data measurement.
            """
            def __init__(self, instrument, data_handler, channel):
                self.instrument = instrument
                self.data_handler = data_handler
                self.n = channel

            # SENS:CORR:COLL:SHORt <port>
            def measure_short(self, port: int):
                """
                Measures the calibration data of the short standard for the specified port.

                Parameter:
                    port (int): Port number (1-4)

                Return:
                    None
                """
                if not (1 <= port <= 4):
                    raise ValueError("port must be 1-4")
                self.instrument.write(f":SENS{self.n}:CORR:COLL:SHOR {port}")

        class TRL:
            """addition Look at what TRL stands for in manual"""
            def __init__(self, instrument, data_handler, channel):
                self.instrument = instrument
                self.data_handler = data_handler
                self.n = channel
                self.line = self.Line(instrument, data_handler, channel)
                
            class Line:
                """
                TRL line standard calibration data measurement.
                """
                def __init__(self, instrument, data_handler, channel):
                    self.instrument = instrument
                    self.data_handler = data_handler
                    self.n = channel

                # SENS:CORR:COLL:TRLLine <port1>,<port2>
                def measure_trl_line(self, port1: int, port2: int):
                    """
                    Measures the calibration data of the TRL line standard between port1 and port2.

                    Parameter:
                        port1 (int): Port number (1-4)
                        port2 (int): Port number (1-4)

                    Return:
                        None
                    """
                    if not (1 <= port1 <= 4 and 1 <= port2 <= 4):
                        raise ValueError("port1 and port2 must be 1-4")
                    if port1 == port2:
                        raise ValueError("port1 and port2 must be different")
                    self.instrument.write(f":SENS{self.n}:CORR:COLL:TRLL {port1},{port2}")

            

            # SENS:CORR:COLL:TRLThru <port1>,<port2>
            def measure_trl_thru(self, port1: int, port2: int):
                """
                Measures the calibration data of the TRL thru standard between port1 and port2.

                Parameter:
                    port1 (int): Port number (1-4)
                    port2 (int): Port number (1-4)

                Return:
                    None
                """
                if not (1 <= port1 <= 4 and 1 <= port2 <= 4):
                    raise ValueError("port1 and port2 must be 1-4")
                if port1 == port2:
                    raise ValueError("port1 and port2 must be different")
                self.instrument.write(f":SENS{self.n}:CORR:COLL:TRLT {port1},{port2}")


            # SENS:CORR:COLL:TRLReflect <port>
            def measure_trl_reflect(self, port: int):
                """
                Measures the calibration data of the TRL reflect standard for the specified port.

                Parameter:
                    port (int): Port number (1-4)

                Return:
                    None
                """
                if not (1 <= port <= 4):
                    raise ValueError("port must be 1-4")
                self.instrument.write(f":SENS{self.n}:CORR:COLL:TRLR {port}")

        
        
        class SubClass:
            """
            Calibration standard subclass selection.
            """
            def __init__(self, instrument, data_handler, channel):
                self.instrument = instrument
                self.data_handler = data_handler
                self.n = channel
            # SENS:CORR:COLL:SUBClass <numeric>
            def set_subclass(self, subclass_num: int):
                """
                Selects the subclass number of calibration standard used for measurement.

                Parameter:
                    subclass_num (int): Subclass number (1-8)

                Return:
                    None
                """
                if not (1 <= subclass_num <= 8):
                    raise ValueError("subclass_num must be 1-8")
                self.instrument.write(f":SENS{self.n}:CORR:COLL:SUBC {subclass_num}")

            # SENS:CORR:COLL:SUBClass?
            def get_subclass(self) -> int:
                """
                Gets the subclass number of calibration standard used for measurement.

                Parameter:
                    None

                Return:
                    int: Subclass number
                """
                return int(self.instrument.query(f":SENS{self.n}:CORR:COLL:SUBC?"))
            # SENSe<Ch>:CORRection:COLLect:SUBClass = <numeric>
            def set_subclass(self, subclass_num: int):
                """
                Selects the subclass number of calibration standard used for measurement.

                Parameter:
                    subclass_num (int): Subclass number (1-8)

                Return:
                    None
                """
                if not (1 <= subclass_num <= 8):
                    raise ValueError("subclass_num must be 1-8")
                self.instrument.write(f":SENS{self.n}:CORR:COLL:SUBC {subclass_num}")
    

    class Frequency:
        """
        Frequency settings commands.
        """
        def __init__(self, instrument, data_handler, channel):
            self.instrument = instrument
            self.data_handler = data_handler
            self.n = channel
            self.offset = self.Offset(instrument, data_handler, channel)
            self.receiver = self.Receiver(instrument, data_handler, channel)
            self.source = self.Source(instrument, data_handler, channel)
            self.extender = self.Extender(instrument)
        # SENS:FREQ - Fixed frequency for a power sweep
        def set_fixed_frequency(self, value: float):
            """
            Set fixed frequency for a power sweep.

            Parameters:
                value (float): Frequency in Hz

            Returns:
                None
            """
            self.instrument.write(f":SENS{self.n}:FREQ {value}")

        def get_fixed_frequency(self) -> float:
            """
            Get fixed frequency for a power sweep.

            Returns:
                float: Frequency in Hz
            """
            return float(self.instrument.query(f":SENS{self.n}:FREQ?"))

        # SENS:FREQ:CENT - Center frequency
        def set_center_frequency(self, value: float):
            """
            Set center frequency.

            Parameters:
                value (float): Center frequency in Hz

            Returns:
                None
            """
            self.instrument.write(f":SENS{self.n}:FREQ:CENT {value}")

        def get_center_frequency(self) -> float:
            """
            Get center frequency.

            Returns:
                float: Center frequency in Hz
            """
            return float(self.instrument.query(f":SENS{self.n}:FREQ:CENT?"))

        # SENS:FREQ:SPAN - Span frequency
        def set_span_frequency(self, value: float):
            """
            Set span frequency.

            Parameters:
                value (float): Span frequency in Hz

            Returns:
                None
            """
            self.instrument.write(f":SENS{self.n}:FREQ:SPAN {value}")


        # SENS:FREQ:STAR - Start frequency
        def set_start_frequency(self, value: float):
            """
            Set start frequency.

            Parameters:
                value (float): Start frequency in Hz

            Returns:
                None
            """
            self.instrument.write(f":SENS{self.n}:FREQ:STAR {value}")

        def get_start_frequency(self) -> float:
            """
            Get start frequency.

            Returns:
                float: Start frequency in Hz
            """
            return float(self.instrument.query(f":SENS{self.n}:FREQ:STAR?"))

        # SENS:FREQ:STOP - Stop frequency
        def set_stop_frequency(self, value: float):
            """
            Set stop frequency.

            Parameters:
                value (float): Stop frequency in Hz

            Returns:
                None
            """
            self.instrument.write(f":SENS{self.n}:FREQ:STOP {value}")

        def get_stop_frequency(self) -> float:
            """
            Get stop frequency.

            Returns:
                float: Stop frequency in Hz
            """
            return float(self.instrument.query(f":SENS{self.n}:FREQ:STOP?"))

        # SENS:FREQ:DATA?
        def get_frequency_data(self):
            """
            Reads out the frequency array of the measurement points.

            Returns:
                list: Frequency values at each measurement point
            """
            data = self.instrument.query(f":SENS{self.n}:FREQ:DATA?")
            if self.data_handler.is_auto_saving_data_enabled():
                    self.data_handler.write_to_file(self, f"FREQUENCIES_{self.n}", data, file_type = EFileType.CSV)
            return self.data_handler.parse_array(data)
        
        # SENS:FREQ[:CW] <frequency>
        def set_cw_frequency(self, value: float):
            """
            Set the fixed frequency value for power sweep.

            Parameters:
                value (float): Frequency in Hz

            Returns:
                None
            """
            self.instrument.write(f":SENS{self.n}:FREQ:CW {value}")

        # SENS:FREQ[:CW]?
        def get_cw_frequency(self) -> float:
            """
            Get the fixed frequency value for power sweep.

            Returns:
                float: Frequency in Hz
            """
            return float(self.instrument.query(f":SENS{self.n}:FREQ:CW?"))

        # SENS:FREQ[:FIXed] <frequency>
        def set_fixed_frequency(self, value: float):
            """
            Set the fixed frequency value.

            Parameters:
                value (float): Frequency in Hz

            Returns:
                None
            """
            self.instrument.write(f":SENS{self.n}:FREQ:FIX {value}")

        # SENS:FREQ[:FIXed]?
        def get_fixed_frequency(self) -> float:
            """
            Get the fixed frequency value.

            Returns:
                float: Frequency in Hz
            """
            return float(self.instrument.query(f":SENS{self.n}:FREQ:FIX?"))

        

        # SENS:FREQ:SPAN?
        def get_span_frequency(self) -> float:
            """
            Get the stimulus span value of the sweep range.

            Returns:
                float: Span frequency in Hz
            """
            return float(self.instrument.query(f":SENS{self.n}:FREQ:SPAN?"))
        class Offset:
            """
            Frequency offset feature and adjustment commands.
            """
            def __init__(self, instrument, data_handler, channel):
                self.instrument = instrument
                self.data_handler = data_handler
                self.n = channel
                #TODO CHeck possible port numbers
                self.port = self.Port(instrument, data_handler, channel,1)
                self.receiver = self.Receiver(instrument, data_handler, channel) 
            # SENSe<Ch>:OFFSet[:STATe] {OFF|ON|0|1}
            def enable_frequency_offset(self, enable: bool):
                """
                Enable or disable the frequency offset feature.

                Parameter:
                    enable (bool): True to enable, False to disable

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:OFFS:STAT {1 if enable else 0}")

            def is_frequency_offset_enabled(self) -> bool:
                """
                Query if the frequency offset feature is enabled.

                Parameter:
                    None

                Return:
                    bool: True if enabled, False otherwise
                """
                return bool(int(self.instrument.query(f":SENS{self.n}:OFFS:STAT?")))

            # SENSe<Ch>:OFFSet:ADJust[:STATe] {OFF|ON|0|1}
            def enable_offset_adjust(self, enable: bool):
                """
                Enable or disable the frequency offset adjust function.

                Parameter:
                    enable (bool): True to enable, False to disable

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:OFFS:ADJ:STAT {1 if enable else 0}")

            def is_offset_adjust_enabled(self) -> bool:
                """
                Query if the frequency offset adjust function is enabled.

                Parameter:
                    None

                Return:
                    bool: True if enabled, False otherwise
                """
                return bool(int(self.instrument.query(f":SENS{self.n}:OFFS:ADJ:STAT?")))

            # SENSe<Ch>:OFFSet:ADJust:CONTinuous:PERiod <numeric>
            def set_adjust_period(self, value: float):
                """
                Set the adjust period in seconds for frequency offset adjust.

                Parameter:
                    value (float): Period in seconds (0 disables, 5-10000 enables)

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:OFFS:ADJ:CONT:PER {value}")

            def get_adjust_period(self) -> float:
                """
                Get the adjust period in seconds for frequency offset adjust.

                Parameter:
                    None

                Return:
                    float: Period in seconds
                """
                return float(self.instrument.query(f":SENS{self.n}:OFFS:ADJ:CONT:PER?"))

            class Port:
                """
                Frequency offset feature: Port frequency offset settings.
                """
                def __init__(self, instrument, data_handler, channel, port):
                    self.instrument = instrument
                    self.data_handler = data_handler
                    self.n = channel
                    self.p = port

                # SENSe<Ch>:OFFSet:PORT<Pt>[:FREQuency]:MULTiplier <numeric>
                def set_multiplier(self, value: float):
                    """
                    Sets the basic frequency range multiplier of port <Pt> when frequency offset is ON and type is "PORT".

                    Parameter:
                        value (float): Multiplier value (-1000 to 1000)

                    Return:
                        None
                    """
                    value = max(-1000, min(1000, value))
                    self.instrument.write(f":SENS{self.n}:OFFS:PORT{self.p}:FREQ:MULT {value}")

                # SENSe<Ch>:OFFSet:PORT<Pt>[:FREQuency]:MULTiplier?
                def get_multiplier(self) -> float:
                    """
                    Reads out the basic frequency range multiplier of port <Pt>.

                    Parameter:
                        None

                    Return:
                        float: Multiplier value
                    """
                    return float(self.instrument.query(f":SENS{self.n}:OFFS:PORT{self.p}:FREQ:MULT?"))

                # SENSe<Ch>:OFFSet:PORT<Pt>[:FREQuency]:OFFSet <frequency>
                def set_offset(self, value: float):
                    """
                    Sets the basic frequency range offset of port <Pt> when frequency offset is ON and type is "PORT".

                    Parameter:
                        value (float): Offset value (-1e12 to 1e12 Hz)

                    Return:
                        None
                    """
                    value = max(-1e12, min(1e12, value))
                    self.instrument.write(f":SENS{self.n}:OFFS:PORT{self.p}:FREQ:OFFS {value}")

                # SENSe<Ch>:OFFSet:PORT<Pt>[:FREQuency]:OFFSet?
                def get_offset(self) -> float:
                    """
                    Reads out the basic frequency range offset of port <Pt>.

                    Parameter:
                        None

                    Return:
                        float: Offset value
                    """
                    return float(self.instrument.query(f":SENS{self.n}:OFFS:PORT{self.p}:FREQ:OFFS?"))

                # SENSe<Ch>:OFFSet:PORT<Pt>[:FREQuency]:STARt <frequency>
                def set_start(self, value: float):
                    """
                    Sets the frequency sweep start of port <Pt> when frequency offset is ON and type is "PORT".

                    Parameter:
                        value (float): Start frequency in Hz

                    Return:
                        None
                    """
                    self.instrument.write(f":SENS{self.n}:OFFS:PORT{self.p}:FREQ:STAR {value}")

                # SENSe<Ch>:OFFSet:PORT<Pt>[:FREQuency]:STARt?
                def get_start(self) -> float:
                    """
                    Reads out the frequency sweep start of port <Pt>.

                    Parameter:
                        None

                    Return:
                        float: Start frequency in Hz
                    """
                    return float(self.instrument.query(f":SENS{self.n}:OFFS:PORT{self.p}:FREQ:STAR?"))

                # SENSe<Ch>:OFFSet:PORT<Pt>[:FREQuency]:STOP <frequency>
                def set_stop(self, value: float):
                    """
                    Sets the frequency sweep stop of port <Pt> when frequency offset is ON and type is "PORT".

                    Parameter:
                        value (float): Stop frequency in Hz

                    Return:
                        None
                    """
                    self.instrument.write(f":SENS{self.n}:OFFS:PORT{self.p}:FREQ:STOP {value}")

                # SENSe<Ch>:OFFSet:PORT<Pt>[:FREQuency]:STOP?
                def get_stop(self) -> float:
                    """
                    Reads out the frequency sweep stop of port <Pt>.

                    Parameter:
                        None

                    Return:
                        float: Stop frequency in Hz
                    """
                    return float(self.instrument.query(f":SENS{self.n}:OFFS:PORT{self.p}:FREQ:STOP?"))

            class Receiver:
                """
                Frequency offset feature: Receiver frequency offset settings.
                """
                def __init__(self, instrument, data_handler, channel):
                    self.instrument = instrument
                    self.data_handler = data_handler
                    self.n = channel

                # SENSe<Ch>:OFFSet:RECeiver[:FREQuency]:DATA?
                def get_frequency_data(self):
                    """
                    Reads out the array of the receiver frequency points when frequency offset is ON and type is "SRCRcv".

                    Parameter:
                        None

                    Return:
                        list: Frequency values at each measurement point
                    """
                    data = self.instrument.query(f":SENS{self.n}:OFFS:REC:FREQ:DATA?")
                    if self.data_handler.is_auto_saving_data_enabled():
                        self.data_handler.write_to_file(self, f"FREQ_OFFSET_{self.n}", data, file_type = EFileType.CSV)
                    return self.data_handler.parse_array(data)

                # SENSe<Ch>:OFFSet:RECeiver[:FREQuency]:DIVisor <numeric>
                def set_divisor(self, value: float):
                    """
                    Sets the basic frequency range divisor to get the receiver frequency when frequency offset is ON and type is "SRCRcv".

                    Parameter:
                        value (float): Divisor value (1 to 1000)

                    Return:
                        None
                    """
                    value = max(1, min(1000, value))
                    self.instrument.write(f":SENS{self.n}:OFFS:REC:FREQ:DIV {value}")

                # SENSe<Ch>:OFFSet:RECeiver[:FREQuency]:DIVisor?
                def get_divisor(self) -> float:
                    """
                    Reads out the basic frequency range divisor for receiver frequency.

                    Parameter:
                        None

                    Return:
                        float: Divisor value
                    """
                    return float(self.instrument.query(f":SENS{self.n}:OFFS:REC:FREQ:DIV?"))
        class Receiver:
            """
            Frequency offset feature: Receiver frequency settings.
            """
            def __init__(self, instrument, data_handler, channel):
                self.instrument = instrument
                self.data_handler = data_handler
                self.n = channel

            # SENSe<Ch>:OFFSet:RECeiver[:FREQuency]:MULTiplier <numeric>
            def set_multiplier(self, value: float):
                """
                Sets the basic frequency range multiplier to get the receiver frequency when frequency offset is ON and type is "SRCRcv".

                Parameter:
                    value (float): Multiplier value (-1000 to 1000)

                Return:
                    None
                """
                value = max(-1000, min(1000, value))
                self.instrument.write(f":SENS{self.n}:OFFS:REC:FREQ:MULT {value}")
        class Source:
            """
            Frequency offset feature: Source frequency settings.
            """
            def __init__(self, instrument, data_handler, channel):
                self.instrument = instrument
                self.data_handler = data_handler
                self.n = channel

            # SENSe<Ch>:OFFSet:SOURce[:FREQuency]:DATA?
            def get_frequency_data(self):
                """
                Reads out the array of the frequency points of the source when frequency offset is ON and offset type is "SRCRcv".

                Parameter:
                    None

                Return:
                    list: Frequency values at each measurement point
                """
                data = self.instrument.query(f":SENS{self.n}:OFFS:SOUR:DATA?")
                if self.data_handler.is_auto_saving_data_enabled():
                    self.data_handler.write_to_file(self, f"FREQ_SOURCE_OFFSET_{self.n}", data, file_type = EFileType.CSV)
                return self.data_handler.parse_array(data)

            # SENSe<Ch>:OFFSet:SOURce[:FREQuency]:DIVisor <numeric>
            def set_divisor(self, value: float):
                """
                Sets the basic frequency range divisor to get the source frequency when frequency offset is ON and offset type is "SRCRcv".

                Parameter:
                    value (float): Divisor value (1 to 1000)

                Return:
                    None
                """
                value = max(1, min(1000, value))
                self.instrument.write(f":SENS{self.n}:OFFS:SOUR:DIV {value}")

            # SENSe<Ch>:OFFSet:SOURce[:FREQuency]:DIVisor?
            def get_divisor(self) -> float:
                """
                Reads out the basic frequency range divisor for source frequency.

                Parameter:
                    None

                Return:
                    float: Divisor value
                """
                return float(self.instrument.query(f":SENS{self.n}:OFFS:SOUR:DIV?"))

            # SENSe<Ch>:OFFSet:SOURce[:FREQuency]:MULTiplier <numeric>
            def set_multiplier(self, value: float):
                """
                Sets the basic frequency range multiplier to get the source frequency when frequency offset is ON and offset type is "SRCRcv".

                Parameter:
                    value (float): Multiplier value (-1000 to 1000)

                Return:
                    None
                """
                value = max(-1000, min(1000, value))
                self.instrument.write(f":SENS{self.n}:OFFS:SOUR:MULT {value}")

            # SENSe<Ch>:OFFSet:SOURce[:FREQuency]:MULTiplier?
            def get_multiplier(self) -> float:
                """
                Reads out the basic frequency range multiplier for source frequency.

                Parameter:
                    None

                Return:
                    float: Multiplier value
                """
                return float(self.instrument.query(f":SENS{self.n}:OFFS:SOUR:MULT?"))

            # SENSe<Ch>:OFFSet:SOURce[:FREQuency]:OFFSet <frequency>
            def set_offset(self, value: float):
                """
                Sets the basic frequency range offset to get the source frequency when frequency offset is ON and offset type is "SRCRcv".

                Parameter:
                    value (float): Offset value (-1e12 to 1e12 Hz)

                Return:
                    None
                """
                value = max(-1e12, min(1e12, value))
                self.instrument.write(f":SENS{self.n}:OFFS:SOUR:OFFS {value}")

            # SENSe<Ch>:OFFSet:SOURce[:FREQuency]:OFFSet?
            def get_offset(self) -> float:
                """
                Reads out the basic frequency range offset for source frequency.

                Parameter:
                    None

                Return:
                    float: Offset value
                """
                return float(self.instrument.query(f":SENS{self.n}:OFFS:SOUR:OFFS?"))

            # SENSe<Ch>:OFFSet:SOURce[:FREQuency]:STARt <frequency>
            def set_start(self, value: float):
                """
                Sets the frequency sweep start of the source when frequency offset is ON and offset type is "SRCRcv".

                Parameter:
                    value (float): Start frequency in Hz

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:OFFS:SOUR:STAR {value}")

            # SENSe<Ch>:OFFSet:SOURce[:FREQuency]:STARt?
            def get_start(self) -> float:
                """
                Reads out the frequency sweep start of the source.

                Parameter:
                    None

                Return:
                    float: Start frequency in Hz
                """
                return float(self.instrument.query(f":SENS{self.n}:OFFS:SOUR:STAR?"))

            # SENSe<Ch>:OFFSet:SOURce[:FREQuency]:STOP <frequency>
            def set_stop(self, value: float):
                """
                Sets the frequency sweep stop of the source when frequency offset is ON and offset type is "SRCRcv".

                Parameter:
                    value (float): Stop frequency in Hz

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:OFFS:SOUR:STOP {value}")

            # SENSe<Ch>:OFFSet:SOURce[:FREQuency]:STOP?
            def get_stop(self) -> float:
                """
                Reads out the frequency sweep stop of the source.

                Parameter:
                    None

                Return:
                    float: Stop frequency in Hz
                """
                return float(self.instrument.query(f":SENS{self.n}:OFFS:SOUR:STOP?"))
    

            # SENSe<Ch>:OFFSet:TYPE <char>
            def set_offset_type(self, offset_type: str):
                """
                Set the frequency offset type when the frequency offset feature is ON.

                Parameter:
                    offset_type (str): Offset type, one of ['PORT', 'SRCRcv']

                Return:
                    None
                """
                allowed = ['PORT', 'SRCRcv']
                if offset_type not in allowed:
                    raise ValueError(f"offset_type must be one of {allowed}")
                self.instrument.write(f":SENS{self.n}:OFFS:TYPE {offset_type}")

            # SENSe<Ch>:OFFSet:TYPE?
            def get_offset_type(self) -> str:
                """
                Get the frequency offset type when the frequency offset feature is ON.

                Parameter:
                    None

                Return:
                    str: Offset type ('PORT' or 'SRCRcv')
                """
                return self.instrument.query(f":SENS{self.n}:OFFS:TYPE?").strip()
        class Extender:
            """
            System frequency extender commands.
            """
            def __init__(self, instrument):
                self.instrument = instrument
                self.port = self.Port(instrument)
            # SYSTem:FREQuency:EXTender:RFPort:POWer <numeric>
            def set_rf_port_power(self, value: float):
                """
                Sets the RF Port Power when the Analyzer is configured to work with a frequency extender.

                Parameter:
                    value (float): Power value in dBm

                Return:
                    None
                """
                self.instrument.write(f":SYST:FREQ:EXT:RFR:POW {value}")

            # SYSTem:FREQuency:EXTender:RFPort:POWer?
            def get_rf_port_power(self) -> float:
                """
                Reads out the RF Port Power when the Analyzer is configured to work with a frequency extender.

                Parameter:
                    None

                Return:
                    float: Power value in dBm
                """
                return float(self.instrument.query(":SYST:FREQ:EXT:RFR:POW?"))

            # SYSTem:FREQuency:EXTender:RFPort:PSLope <numeric>
            def set_rf_port_power_slope(self, value: float):
                """
                Sets the RF Port Power Slope when the Analyzer is configured to work with a frequency extender.

                Parameter:
                    value (float): Slope value in dB/GHz

                Return:
                    None
                """
                self.instrument.write(f":SYST:FREQ:EXT:RFP:PSL {value}")

            # SYSTem:FREQuency:EXTender:RFPort:PSLope?
            def get_rf_port_power_slope(self) -> float:
                """
                Reads out the RF Port Power Slope when the Analyzer is configured to work with a frequency extender.

                Parameter:
                    None

                Return:
                    float: Slope value in dB/GHz
                """
                return float(self.instrument.query(":SYST:FREQ:EXT:RFP:PSL?"))

            # SYSTem:FREQuency:EXTender:LOPort:POWer <numeric>
            def set_lo_port_power(self, value: float):
                """
                Sets the LO Port Power when the Analyzer is configured to work with a frequency extender.

                Parameter:
                    value (float): Power value in dBm

                Return:
                    None
                """
                self.instrument.write(f":SYST:FREQ:EXT:LOP:POW {value}")

            # SYSTem:FREQuency:EXTender:LOPort:POWer?
            def get_lo_port_power(self) -> float:
                """
                Reads out the LO Port Power when the Analyzer is configured to work with a frequency extender.

                Parameter:
                    None

                Return:
                    float: Power value in dBm
                """
                return float(self.instrument.query(":SYST:FREQ:EXT:LOP:POW?"))

            # SYSTem:FREQuency:EXTender:LOPort:PSLope <numeric>
            def set_lo_port_power_slope(self, value: float):
                """
                Sets the LO Port Power Slope when the Analyzer is configured to work with a frequency extender.

                Parameter:
                    value (float): Slope value in dB/GHz

                Return:
                    None
                """
                self.instrument.write(f":SYST:FREQ:EXT:LOP:PSL {value}")

            # SYSTem:FREQuency:EXTender:LOPort:PSLope?
            def get_lo_port_power_slope(self) -> float:
                """
                Reads out the LO Port Power Slope when the Analyzer is configured to work with a frequency extender.

                Parameter:
                    None

                Return:
                    float: Slope value in dB/GHz
                """
                return float(self.instrument.query(":SYST:FREQ:EXT:LOP:PSL?"))

            # SYSTem:FREQuency:EXTender:TYPE <char>
            def set_extender_type(self, extender_type: str):
                """
                Selects the frequency extender type.

                Parameter:
                    extender_type (str): One of ['NONE', 'FEV15', 'FEV12', 'FEV10', 'FET1854', 'CUST']

                Return:
                    None
                """
                allowed = ['NONE', 'FEV15', 'FEV12', 'FEV10', 'FET1854', 'CUST']
                if extender_type not in allowed:
                    raise ValueError(f"extender_type must be one of {allowed}")
                self.instrument.write(f":SYST:FREQ:EXT:TYPE {extender_type}")

            # SYSTem:FREQuency:EXTender:TYPE?
            def get_extender_type(self) -> str:
                """
                Reads out the frequency extender type.

                Parameter:
                    None

                Return:
                    str: Extender type
                """
                return self.instrument.query(":SYST:FREQ:EXT:TYPE?").strip()
            class Port:
                """
                System frequency extender port commands.
                """
                def __init__(self, instrument):
                    self.instrument = instrument

                # SYSTem:FREQuency:EXTender:PORT<Pt>:CONNect?
                def is_extender_connected(self, port: int) -> bool:
                    """
                    Reads out whether the frequency extender is connected to the port number <Pt>.

                    Parameter:
                        port (int): Port number (1-4)

                    Return:
                        bool: True if connected, False otherwise
                    """
                    if not (1 <= port <= 4):
                        raise ValueError("port must be 1-4")
                    return bool(int(self.instrument.query(f":SYST:FREQ:EXT:PORT{port}:CONN?")))

                # SYSTem:FREQuency:EXTender:PORT<Pt>:SERial?
                def get_extender_serial(self, port: int) -> str:
                    """
                    Reads out the serial number of the frequency extender connected to the port number <Pt>.

                    Parameter:
                        port (int): Port number (1-4)

                    Return:
                        str: Serial number (8 symbols)
                    """
                    if not (1 <= port <= 4):
                        raise ValueError("port must be 1-4")
                    return self.instrument.query(f":SYST:FREQ:EXT:PORT{port}:SER?").strip()

                # SYSTem:FREQuency:EXTender:PORT<Pt>:TEMPerature:SENSor?
                def get_extender_temperature(self, port: int) -> float:
                    """
                    Reads out the temperature of the frequency extender connected to the port number <Pt>.

                    Parameter:
                        port (int): Port number (1-4)

                    Return:
                        float: Temperature in degrees Celsius
                    """
                    if not (1 <= port <= 4):
                        raise ValueError("port must be 1-4")
                    return float(self.instrument.query(f":SYST:FREQ:EXT:PORT{port}:TEMP:SENS?"))
            # SENSe:ROSCillator:SOURce?
    class ReferenceOscillator:
        """
        Reference oscillator source commands.
        """
        def __init__(self, instrument, data_handler, channel):
            self.instrument = instrument
            self.data_handler = data_handler
            self.n = channel

        # SENSe:ROSCillator:SOURce <char>
        def set_reference_oscillator_source(self, source: str):
            """
            Set the internal or external source of the 10 MHz reference frequency.

            Parameter:
                source (str): Reference source, one of ['INTernal', 'EXTernal']

            Return:
                None
            """
            allowed = ['INTernal', 'EXTernal']
            if source not in allowed:
                raise ValueError(f"source must be one of {allowed}")
            self.instrument.write(f":SENS{self.n}:ROSC:SOUR {source}")

        # SENSe:ROSCillator:SOURce?
        def get_reference_oscillator_source(self) -> str:
            """
            Get the internal or external source of the 10 MHz reference frequency.

            Parameter:
                None

            Return:
                str: Reference source ('INTernal' or 'EXTernal')
            """
            return self.instrument.query(f":SENS{self.n}:ROSC:SOUR?").strip()
        
    
    class Sweep:
        def __init__(self, instrument, data_handler, channel):
            self.instrument = instrument
            self.data_handler = data_handler
            self.n = channel
            self.segment_table_data = self.SegmentTableData(instrument, data_handler, channel)
            self.cw = self.CW(instrument, data_handler, channel)

        class SegmentTableData:
            """
            Segment sweep table commands.
            """
            def __init__(self, instrument, data_handler, channel):
                self.instrument = instrument
                self.data_handler = data_handler
                self.n = channel

            # SENSe<Ch>:SEGMent:DATA <numeric list>
            def set_segment_data(self, data_list):
                """
                Set the array of the segment sweep table.

                Parameter:
                    data_list (list): Segment sweep table data as per documentation

                Return:
                    None
                """
                data_str = ",".join(str(float(x)) for x in data_list)
                self.instrument.write(f":SENS{self.n}:SEGM:DATA {data_str}")

            # SENSe<Ch>:SEGMent:DATA?
            def get_segment_data(self):
                """
                Get the array of the segment sweep table.

                Parameter:
                    None

                Return:
                    list: Segment sweep table data
                """
                data = self.instrument.query(f":SENS{self.n}:SEGM:DATA?")
                if self.data_handler.is_auto_saving_data_enabled():
                    self.data_handler.write_to_file(self, f"SWEEPSEG_TABLE_{self.n}", data, file_type = EFileType.CSV)
                return self.data_handler.parse_array(data)
        # SENS:SWE:REV - Reverse sweep ON/OFF
        def enable_reverse_sweep(self, enable: bool):
            """
            Enable or disable reverse sweep.

            Parameter:
                enable (bool): True to enable, False to disable

            Return:
                None
            """
            self.instrument.write(f":SENS{self.n}:SWE:REV {1 if enable else 0}")

        def is_reverse_sweep_enabled(self) -> bool:
            """
            Query if reverse sweep is enabled.

            Parameter:
                None

            Return:
                bool: True if enabled, False otherwise
            """
            return bool(int(self.instrument.query(f":SENS{self.n}:SWE:REV?")))
        class CW:
            """
            Sweep time value commands for CW time mode.
            """
            def __init__(self, instrument, data_handler, channel):
                self.instrument = instrument
                self.data_handler = data_handler
                self.n = channel

            # SENSe<Ch>:SWEep:CW:TIME <numeric>
            def set_cw_sweep_time(self, value: float):
                """
                Set the sweep time value when the CW time mode is ON.

                Parameter:
                    value (float): Sweep time value in seconds

                Return:
                    None
                """
                self.instrument.write(f":SENS{self.n}:SWE:CW:TIME {value}")

            # SENSe<Ch>:SWEep:CW:TIME?
            def get_cw_sweep_time(self) -> float:
                """
                Get the sweep time value when the CW time mode is ON.

                Parameter:
                    None

                Return:
                    float: Sweep time value in seconds
                """
                return float(self.instrument.query(f":SENS{self.n}:SWE:CW:TIME?"))

        
class Service:
    """
    Analyzer service and diagnostic commands.
    """
    def __init__(self, instrument, data_handler, channel):
        self.instrument = instrument
        self.data_handler = data_handler
        self.n = channel
        self.channel = self.Channel(self.instrument,data_handler)
        self.port = self.Port(self.instrument, data_handler)
        self.sweep = self.Sweep(self.instrument, data_handler)

    # SERV:CHAN:ACT? - Reads out the active channel number
    def get_active_channel(self) -> int:
        """
        Reads out the active channel number.

        Parameter:
            None

        Return:
            int: Active channel number (1-16)
        """
        return int(self.instrument.query(":SERV:CHAN:ACT?"))

    # SERV:CHAN:TRAC:ACT? - Reads out the active trace number of the channel
    def get_active_trace(self, channel: int) -> int:
        """
        Reads out the active trace number of the specified channel.

        Parameter:
            channel (int): Channel number (1-16)

        Return:
            int: Active trace number (1-16)
        """
        if not (1 <= channel <= 16):
            raise ValueError("channel must be 1-16")
        return int(self.instrument.query(f":SERV:CHAN{channel}:TRAC:ACT?"))

    # SERV:CHAN:COUN? - Reads out the maximum number of analyzer channels
    def get_channel_count(self) -> int:
        """
        Reads out the maximum number of analyzer channels.

        Parameter:
            None

        Return:
            int: Maximum number of channels
        """
        return int(self.instrument.query(":SERV:CHAN:COUN?"))

    # SERV:CHAN:TRAC:COUN? - Reads out the maximum number of traces in the channel
    def get_trace_count(self) -> int:
        """
        Reads out the maximum number of traces in the channel.

        Parameter:
            None

        Return:
            int: Maximum number of traces
        """
        return int(self.instrument.query(":SERV:CHAN:TRAC:COUN?"))

    # SERV:PORT:COUN? - Reads out the number of ports
    def get_port_count(self) -> int:
        """
        Reads out the number of ports.

        Parameter:
            None

        Return:
            int: Number of ports
        """
        return int(self.instrument.query(":SERV:PORT:COUN?"))

    # SERV:SWE:FREQ:MAX? - Reads out the upper limit of frequency
    def get_sweep_frequency_max(self) -> float:
        """
        Reads out the upper limit of frequency.

        Parameter:
            None

        Return:
            float: Upper frequency limit
        """
        return float(self.instrument.query(":SERV:SWE:FREQ:MAX?"))

    # SERV:SWE:FREQ:MIN? - Reads out the lower limit of frequency
    def get_sweep_frequency_min(self) -> float:
        """
        Reads out the lower limit of frequency.

        Parameter:
            None

        Return:
            float: Lower frequency limit
        """
        return float(self.instrument.query(":SERV:SWE:FREQ:MIN?"))

    # SERV:SWE:POIN? - Reads out the maximum number of points
    def get_sweep_points_max(self) -> int:
        """
        Reads out the maximum number of points.

        Parameter:
            None

        Return:
            int: Maximum number of points
        """
        return int(self.instrument.query(":SERV:SWE:POIN?"))

    # SERV:SWE:POW:MAX? - Reads out the upper limit of source power
    def get_sweep_power_max(self) -> float:
        """
        Reads out the upper limit of source power.

        Parameter:
            None

        Return:
            float: Upper limit of source power
        """
        return float(self.instrument.query(":SERV:SWE:POW:MAX?"))

    # SERV:SWE:POW:MIN? - Reads out the lower limit of source power
    def get_sweep_power_min(self) -> float:
        """
        Reads out the lower limit of source power.

        Parameter:
            None

        Return:
            float: Lower limit of source power
        """
        return float(self.instrument.query(":SERV:SWE:POW:MIN?"))

    # SERV:CHAN:TRAC:MARK:ACT? - Gets active marker number of the specified trace of the specified channel
    def get_active_marker(self, channel: int, trace: int) -> int:
        """
        Gets the active marker number of the specified trace of the specified channel.

        Parameter:
            channel (int): Channel number (1-16)
            trace (int): Trace number (1-16)

        Return:
            int: Active marker number
        """
        if not (1 <= channel <= 16):
            raise ValueError("channel must be 1-16")
        if not (1 <= trace <= 16):
            raise ValueError("trace must be 1-16")
        return int(self.instrument.query(f":SERV:CHAN{channel}:TRAC{trace}:MARK:ACT?"))
    class Channel:
        """
        Service channel related commands.
        """
        def __init__(self, instrument,data_handler):
            self.instrument = instrument
            self.data_handler = data_handler

        # SERV:CHAN:TRAC:MARK:ACT? - Gets the active marker number of the specified trace of the specified channel
        def get_active_marker(self, channel: int, trace: int) -> int:
            """
            Gets the active marker number of the specified trace of the specified channel.

            Parameter:
                channel (int): Channel number (1-16)
                trace (int): Trace number (1-16)

            Return:
                int: Active marker number
            """
            if not (1 <= channel <= 16):
                        raise ValueError("channel must be 1-16")
            if not (1 <= trace <= 16):
                raise ValueError("trace must be 1-16")
            return int(self.instrument.query(f":SERV:CHAN{channel}:TRAC{trace}:MARK:ACT?"))

    class Port:
        """
        Service port related commands.
        """
        def __init__(self, instrument, data_handler):
            self.instrument = instrument
            self.data_handler = data_handler

        # SERV:PORT:COUN? - Reads out the number of analyzer ports
        def get_port_count(self) -> int:
            """
            Reads out the number of analyzer ports.

            Parameter:
                None

            Return:
                int: Number of analyzer ports
            """
            return int(self.instrument.query(":SERV:PORT:COUN?"))

    class Sweep:
        """
        Service sweep related commands.
        """
        def __init__(self, instrument, data_handler):
            self.instrument = instrument
            self.data_handler = data_handler
        # SERV:SWE:FREQ:MAX? - Reads out the upper limit of the analyzer measurement frequency
        def get_frequency_max(self) -> float:
            """
            Reads out the upper limit of the analyzer measurement frequency.

            Parameter:
                None

            Return:
                float: Upper frequency limit in Hz
            """
            return float(self.instrument.query(":SERV:SWE:FREQ:MAX?"))

        # SERV:SWE:FREQ:MIN? - Reads out the lower limit of the analyzer measurement frequency
        def get_frequency_min(self) -> float:
            """
            Reads out the lower limit of the analyzer measurement frequency.

            Parameter:
                None

            Return:
                float: Lower frequency limit in Hz
            """
            return float(self.instrument.query(":SERV:SWE:FREQ:MIN?"))

        # SERV:SWE:POIN? - Reads the maximum number of analyzer measurement points
        def get_points_max(self) -> int:
            """
            Reads the maximum number of analyzer measurement points.

            Parameter:
                None

            Return:
                int: Maximum number of measurement points
            """
            return int(self.instrument.query(":SERV:SWE:POIN?"))

        # SERV:SWE:POW:MAX? - Reads out the upper limit of the source power
        def get_power_max(self) -> float:
            """
            Reads out the upper limit of the source power.

            Parameter:
                None

            Return:
                float: Upper limit of source power in dBm
            """
            return float(self.instrument.query(":SERV:SWE:POW:MAX?"))

        # SERV:SWE:POW:MIN? - Reads out the lower limit of the source power
        def get_power_min(self) -> float:
            """
            Reads out the lower limit of the source power.

            Parameter:
                None

            Return:
                float: Lower limit of source power in dBm
            """
            return float(self.instrument.query(":SERV:SWE:POW:MIN?"))
class Source:
    """
    Source related commands.
    """
    def __init__(self, instrument, data_handler):
        self.instrument = instrument
        self.data_handler = data_handler
        self.auxiliary = self.Auxiliary(instrument, data_handler)
        self.power = self.Power(instrument, data_handler)
    class Auxiliary:
        """
        Auxiliary RF source related commands.
        """
        def __init__(self, instrument, data_handler):
            self.instrument = instrument
            self.data_handler = data_handler

        # SOURce<Ch>:AUXiliary[:STATe] {OFF|ON|0|1}
        def set_auxiliary_state(self, channel: int, state: str):
            """
            Turns an auxiliary RF source ON/OFF.

            Parameter:
                channel (int): Channel number (1-16)
                state (str): 'ON', 'OFF', '1', or '0'

            Return:
                None
            """
            allowed = ['ON', 'OFF', '1', '0']
            if state not in allowed:
                raise ValueError("state must be one of ['ON', 'OFF', '1', '0']")
            if not (1 <= channel <= 16):
                        raise ValueError("channel must be 1-16")
            self.instrument.write(f":SOUR{channel}:AUX:STAT {state}")

        # SOURce<Ch>:AUXiliary[:STATe]?
        def get_auxiliary_state(self, channel: int) -> bool:
            """
            Query if auxiliary RF source is ON/OFF.

            Parameter:
                channel (int): Channel number (1-16)

            Return:
                bool: True if ON, False if OFF
            """
            if not (1 <= channel <= 16):
                        raise ValueError("channel must be 1-16")
            return bool(int(self.instrument.query(f":SOUR{channel}:AUX:STAT?")))
        # SOURce<Ch>:AUXiliary:FREQuency:DIVisor <numeric>
        def set_auxiliary_frequency_divisor(self, channel: int, divisor: int):
            """
            Set the basic frequency range divisor to derive the frequency of the auxiliary RF source.

            Parameter:
                channel (int): Channel number (1-16)
                divisor (int): Integer divisor (1-1000)

            Return:
                None
            """
            if not (1 <= channel <= 16):
                        raise ValueError("channel must be 1-16")
            divisor = max(1, min(1000, divisor))
            self.instrument.write(f":SOUR{channel}:AUX:FREQ:DIV {divisor}")

        # SOURce<Ch>:AUXiliary:FREQuency:DIVisor?
        def get_auxiliary_frequency_divisor(self, channel: int) -> int:
            """
            Get the basic frequency range divisor for the auxiliary RF source.

            Parameter:
                channel (int): Channel number (1-16)

            Return:
                int: Integer divisor (1-1000)
            """
            if not (1 <= channel <= 16):
                        raise ValueError("channel must be 1-16")
            return int(self.instrument.query(f":SOUR{channel}:AUX:FREQ:DIV?"))

        # SOURce<Ch>:AUXiliary:FREQuency:MULTiplier <numeric>
        def set_auxiliary_frequency_multiplier(self, channel: int, multiplier: float):
            """
            Set the basic frequency range multiplier to derive the frequency of the auxiliary RF source.

            Parameter:
                channel (int): Channel number (1-16)
                multiplier (float): Multiplier (-1000 to 1000)

            Return:
                None
            """
            if not (1 <= channel <= 16):
                        raise ValueError("channel must be 1-16")
            multiplier = max(-1000, min(1000, multiplier))
            self.instrument.write(f":SOUR{channel}:AUX:FREQ:MULT {multiplier}")

        # SOURce<Ch>:AUXiliary:FREQuency:MULTiplier?
        def get_auxiliary_frequency_multiplier(self, channel: int) -> float:
            """
            Get the basic frequency range multiplier for the auxiliary RF source.

            Parameter:
                channel (int): Channel number (1-16)

            Return:
                float: Multiplier (-1000 to 1000)
            """
            if not (1 <= channel <= 16):
                        raise ValueError("channel must be 1-16")
            return float(self.instrument.query(f":SOUR{channel}:AUX:FREQ:MULT?"))

        # SOURce<Ch>:AUXiliary:FREQuency:OFFSet <numeric>
        def set_auxiliary_frequency_offset(self, channel: int, offset: float):
            """
            Set the basic frequency range offset to derive the frequency of the auxiliary RF source.

            Parameter:
                channel (int): Channel number (1-16)
                offset (float): Frequency offset (-1e12 to 1e12 Hz)

            Return:
                None
            """
            if not (1 <= channel <= 16):
                        raise ValueError("channel must be 1-16")
            offset = max(-1e12, min(1e12, offset))
            self.instrument.write(f":SOUR{channel}:AUX:FREQ:OFFS {offset}")

        # SOURce<Ch>:AUXiliary:FREQuency:OFFSet?
        def get_auxiliary_frequency_offset(self, channel: int) -> float:
            """
            Get the basic frequency range offset for the auxiliary RF source.

            Parameter:
                channel (int): Channel number (1-16)

            Return:
                float: Frequency offset (-1e12 to 1e12 Hz)
            """
            if not (1 <= channel <= 16):
                        raise ValueError("channel must be 1-16")
            return float(self.instrument.query(f":SOUR{channel}:AUX:FREQ:OFFS?"))

        # SOURce<Ch>:AUXiliary:FREQuency:STARt <numeric>
        def set_auxiliary_frequency_start(self, channel: int, start: float):
            """
            Set the start of the frequency range of the auxiliary RF source.

            Parameter:
                channel (int): Channel number (1-16)
                start (float): Start frequency in Hz

            Return:
                None
            """
            if not (1 <= channel <= 16):
                        raise ValueError("channel must be 1-16")
            self.instrument.write(f":SOUR{channel}:AUX:FREQ:STAR {start}")

        # SOURce<Ch>:AUXiliary:FREQuency:STARt?
        def get_auxiliary_frequency_start(self, channel: int) -> float:
            """
            Get the start of the frequency range of the auxiliary RF source.

            Parameter:
                channel (int): Channel number (1-16)

            Return:
                float: Start frequency in Hz
            """
            if not (1 <= channel <= 16):
                        raise ValueError("channel must be 1-16")
            return float(self.instrument.query(f":SOUR{channel}:AUX:FREQ:STAR?"))

        # SOURce<Ch>:AUXiliary:FREQuency:STOP <numeric>
        def set_auxiliary_frequency_stop(self, channel: int, stop: float):
            """
            Set the stop of the frequency range of the auxiliary RF source.

            Parameter:
                channel (int): Channel number (1-16)
                stop (float): Stop frequency in Hz

            Return:
                None
            """
            if not (1 <= channel <= 16):
                        raise ValueError("channel must be 1-16")
            self.instrument.write(f":SOUR{channel}:AUX:FREQ:STOP {stop}")

        # SOURce<Ch>:AUXiliary:FREQuency:STOP?
        def get_auxiliary_frequency_stop(self, channel: int) -> float:
            """
            Get the stop of the frequency range of the auxiliary RF source.

            Parameter:
                channel (int): Channel number (1-16)

            Return:
                float: Stop frequency in Hz
            """
            if not (1 <= channel <= 16):
                        raise ValueError("channel must be 1-16")
            return float(self.instrument.query(f":SOUR{channel}:AUX:FREQ:STOP?"))
        # SOURce<Ch>:AUXiliary:PORT <numeric>
        def set_auxiliary_port(self, channel: int, port: int):
            """
            Set the port number assigned to the auxiliary RF source.

            Parameter:
                channel (int): Channel number (1-16)
                port (int): Port number (1-4)

            Return:
                None
            """
            if not (1 <= channel <= 16):
                        raise ValueError("channel must be 1-16")
            if not (1 <= port <= 4):
                raise ValueError("port must be 1-4")
            self.instrument.write(f":SOUR{channel}:AUX:PORT {port}")

        # SOURce<Ch>:AUXiliary:PORT?
        def get_auxiliary_port(self, channel: int) -> int:
            """
            Get the port number assigned to the auxiliary RF source.

            Parameter:
                channel (int): Channel number (1-16)

            Return:
                int: Port number (1-4)
            """
            if not (1 <= channel <= 16):
                        raise ValueError("channel must be 1-16")
            return int(self.instrument.query(f":SOUR{channel}:AUX:PORT?"))

        # SOURce<Ch>:AUXiliary:POWer[:AMPLitude] <numeric>
        def set_auxiliary_power(self, channel: int, power: float):
            """
            Set the power level of the auxiliary RF source.

            Parameter:
                channel (int): Channel number (1-16)
                power (float): Power level in dBm

            Return:
                None
            """
            if not (1 <= channel <= 16):
                        raise ValueError("channel must be 1-16")
            self.instrument.write(f":SOUR{channel}:AUX:POW {power}")

        # SOURce<Ch>:AUXiliary:POWer[:AMPLitude]?
        def get_auxiliary_power(self, channel: int) -> float:
            """
            Get the power level of the auxiliary RF source.

            Parameter:
                channel (int): Channel number (1-16)

            Return:
                float: Power level in dBm
            """
            if not (1 <= channel <= 16):
                        raise ValueError("channel must be 1-16")
            return float(self.instrument.query(f":SOUR{channel}:AUX:POW?"))

    class Power:
        """
        Power related commands.
        """
        def __init__(self, instrument, data_handler):
            self.instrument = instrument
            self.data_handler = data_handler
            self.port = self.Port(instrument, data_handler)
        # SOURce<Ch>:POWer[:LEVel][:IMMediate][:AMPLitude] <power>
        def set_power_level(self, channel: int, power: float):
            """
            Set the power level for the frequency sweep type.

            Parameter:
                channel (int): Channel number (1-16)
                power (float): Power level in dBm

            Return:
                None
            """
            if not (1 <= channel <= 16):
                        raise ValueError("channel must be 1-16")
            self.instrument.write(f":SOUR{channel}:POW {power}")

        # SOURce<Ch>:POWer[:LEVel][:IMMediate][:AMPLitude]?
        def get_power_level(self, channel: int) -> float:
            """
            Get the power level for the frequency sweep type.

            Parameter:
                channel (int): Channel number (1-16)

            Return:
                float: Power level in dBm
            """
            if not (1 <= channel <= 16):
                        raise ValueError("channel must be 1-16")
            return float(self.instrument.query(f":SOUR{channel}:POW?"))

        # SOURce<Ch>:POWer:CENTer <power>
        def set_power_center(self, channel: int, power: float):
            """
            Set the center value of the power sweep type.

            Parameter:
                channel (int): Channel number (1-16)
                power (float): Center power level in dBm

            Return:
                None
            """
            if not (1 <= channel <= 16):
                        raise ValueError("channel must be 1-16")
            self.instrument.write(f":SOUR{channel}:POW:CENT {power}")

        # SOURce<Ch>:POWer:CENTer?
        def get_power_center(self, channel: int) -> float:
            """
            Get the center value of the power sweep type.

            Parameter:
                channel (int): Channel number (1-16)

            Return:
                float: Center power level in dBm
            """
            if not (1 <= channel <= 16):
                        raise ValueError("channel must be 1-16")
            return float(self.instrument.query(f":SOUR{channel}:POW:CENT?"))

        # SOURce<Ch>:POWer:PORT<Pt>[:LEVel][:IMMediate][:AMPLitude] <power>
        def set_port_power_level(self, channel: int, port: int, power: float):
            """
            Set the power level of each port for the frequency sweep type.

            Parameter:
                channel (int): Channel number (1-16)
                port (int): Port number (1-4)
                power (float): Power level in dBm

            Return:
                None
            """
            if not (1 <= channel <= 16):
                        raise ValueError("channel must be 1-16")
            if not (1 <= port <= 4):
                raise ValueError("port must be 1-4")
            self.instrument.write(f":SOUR{channel}:POW:PORT{port} {power}")

        # SOURce<Ch>:POWer:PORT<Pt>[:LEVel][:IMMediate][:AMPLitude]?
        def get_port_power_level(self, channel: int, port: int) -> float:
            """
            Get the power level of each port for the frequency sweep type.

            Parameter:
                channel (int): Channel number (1-16)
                port (int): Port number (1-4)

            Return:
                float: Power level in dBm
            """
            if not (1 <= channel <= 16):
                        raise ValueError("channel must be 1-16")
            if not (1 <= port <= 4):
                raise ValueError("port must be 1-4")
            return float(self.instrument.query(f":SOUR{channel}:POW:PORT{port}?"))
        class Port:
            """
            Port power and correction related commands.
            """
            def __init__(self, instrument, data_handler):
                self.instrument = instrument
                self.data_handler = data_handler

            # SOURce<Ch>:POWer:PORT<Pt>:CORRection[:STATe] {OFF|ON|0|1}
            def enable_power_correction(self, channel: int, port: int, enable: bool):
                """
                Enable or disable the power correction for the specified port.

                Parameter:
                    channel (int): Channel number (1-16)
                    port (int): Port number (1-4)
                    enable (bool): True to enable, False to disable

                Return:
                    None
                """
                if not (1 <= channel <= 16):
                                    raise ValueError("channel must be 1-16")
                if not (1 <= port <= 4):
                    raise ValueError("port must be 1-4")
                self.instrument.write(f":SOUR{channel}:POW:PORT{port}:CORR:STAT {1 if enable else 0}")

            def is_power_correction_enabled(self, channel: int, port: int) -> bool:
                """
                Query if power correction is enabled for the specified port.

                Parameter:
                    channel (int): Channel number (1-16)
                    port (int): Port number (1-4)

                Return:
                    bool: True if enabled, False otherwise
                """
                if not (1 <= channel <= 16):
                                    raise ValueError("channel must be 1-16")
                if not (1 <= port <= 4):
                    raise ValueError("port must be 1-4")
                return bool(int(self.instrument.query(f":SOUR{channel}:POW:PORT{port}:CORR:STAT?")))

            # SOURce<Ch>:POWer:PORT<Pt>:CORRection:INTerpolation[:STATus]?
            def get_power_correction_interpolation_status(self, channel: int, port: int) -> str:
                """
                Reads out the interpolation/extrapolation status of the port power correction.

                Parameter:
                    channel (int): Channel number (1-16)
                    port (int): Port number (1-4)

                Return:
                    str: Status ('NONE', 'PC', 'PC?', 'PC!')
                """
                if not (1 <= channel <= 16):
                                    raise ValueError("channel must be 1-16")
                if not (1 <= port <= 4):
                    raise ValueError("port must be 1-4")
                return self.instrument.query(f":SOUR{channel}:POW:PORT{port}:CORR:INT:STAT?").strip()

            # SOURce<Ch>:POWer:PORT<Pt>:CORRection:COLLect[:ACQuire]
            def acquire_power_calibration(self, channel: int, port: int):
                """
                Measures the power calibration data for the port using the power meter.

                Parameter:
                    channel (int): Channel number (1-16)
                    port (int): Port number (1-4)

                Return:
                    None
                """
                if not (1 <= channel <= 16):
                                    raise ValueError("channel must be 1-16")
                if not (1 <= port <= 4):
                    raise ValueError("port must be 1-4")
                self.instrument.write(f":SOUR{channel}:POW:PORT{port}:CORR:COLL:ACQ")

            # SOURce<Ch>:POWer:PORT<Pt>:CORRection:COLLect:TABLe:LOSS:DATA <numeric list>
            def set_loss_compensation_table(self, channel: int, port: int, data_list):
                """
                Sets the loss compensation table used for power calibration.

                Parameter:
                    channel (int): Channel number (1-16)
                    port (int): Port number (1-4)
                    data_list (list): Array size 1+2N, [N, freq1, loss1, freq2, loss2, ...]

                Return:
                    None
                """
                if not (1 <= channel <= 16):
                                    raise ValueError("channel must be 1-16")
                if not (1 <= port <= 4):
                    raise ValueError("port must be 1-4")
                data_str = ",".join(str(float(x)) for x in data_list)
                self.instrument.write(f":SOUR{channel}:POW:PORT{port}:CORR:COLL:TABL:LOSS:DATA {data_str}")

            def get_loss_compensation_table(self, channel: int, port: int):
                """
                Gets the loss compensation table used for power calibration.

                Parameter:
                    channel (int): Channel number (1-16)
                    port (int): Port number (1-4)

                Return:
                    list: Array size 1+2N, [N, freq1, loss1, freq2, loss2, ...]
                """
                if not (1 <= channel <= 16):
                                    raise ValueError("channel must be 1-16")
                if not (1 <= port <= 4):
                    raise ValueError("port must be 1-4")
                data = self.instrument.query(f":SOUR{channel}:POW:PORT{port}:CORR:COLL:TABL:LOSS:DATA?").strip()
                if self.data_handler.is_auto_saving_data_enabled():
                    self.data_handler.write_to_file(self, f"LOSS_COMP_{channel}_PORT_{port}", data, file_type = EFileType.CSV)
                return [float(x) for x in data.split(',') if x]

            # SOURce<Ch>:POWer:PORT<Pt>:CORRection:COLLect:TABLe:LOSS[:STATe] {OFF|ON|0|1}
            def enable_loss_compensation(self, channel: int, port: int, enable: bool):
                """
                Turns the state of the loss compensation used for power calibration ON/OFF.

                Parameter:
                    channel (int): Channel number (1-16)
                                port (int): Port number (1-4)
                                enable (bool): True to enable, False to disable

                Return:
                    None
                """
                if not (1 <= channel <= 16):
                                    raise ValueError("channel must be 1-16")
                if not (1 <= port <= 4):
                    raise ValueError("port must be 1-4")
                self.instrument.write(f":SOUR{channel}:POW:PORT{port}:CORR:COLL:TABL:LOSS:STAT {1 if enable else 0}")

            def is_loss_compensation_enabled(self, channel: int, port: int) -> bool:
                """
                Query if loss compensation is enabled for power calibration.

                Parameter:
                    channel (int): Channel number (1-16)
                    port (int): Port number (1-4)

                Return:
                    bool: True if enabled, False otherwise
                """
                if not (1 <= channel <= 16):
                                    raise ValueError("channel must be 1-16")
                if not (1 <= port <= 4):
                    raise ValueError("port must be 1-4")
                return bool(int(self.instrument.query(f":SOUR{channel}:POW:PORT{port}:CORR:COLL:TABL:LOSS:STAT?")))


            # SOURce<Ch>:POWer:PORT<Pt>:CORRection:COLLect:TABLe:LOSS[:STATe] {OFF|ON|0|1}
            def enable_loss_compensation(self, channel: int, port: int, enable: bool):
                """
                Turns the state of the loss compensation used for power calibration ON/OFF.

                Parameter:
                    channel (int): Channel number (1-16)
                    port (int): Port number (1-4)
                    enable (bool): True to enable, False to disable

                Return:
                    None
                """
                if not (1 <= channel <= 16):
                                    raise ValueError("channel must be 1-16")
                if not (1 <= port <= 4):
                    raise ValueError("port must be 1-4")
                self.instrument.write(f":SOUR{channel}:POW:PORT{port}:CORR:COLL:TABL:LOSS:STAT {1 if enable else 0}")

            def is_loss_compensation_enabled(self, channel: int, port: int) -> bool:
                """
                Query if loss compensation is enabled for power calibration.

                Parameter:
                    channel (int): Channel number (1-16)
                    port (int): Port number (1-4)

                Return:
                    bool: True if enabled, False otherwise
                """
                if not (1 <= channel <= 16):
                                    raise ValueError("channel must be 1-16")
                if not (1 <= port <= 4):
                    raise ValueError("port must be 1-4")
                return bool(int(self.instrument.query(f":SOUR{channel}:POW:PORT{port}:CORR:COLL:TABL:LOSS:STAT?")))

            # SOURce<Ch>:POWer:PORT<Pt>:CORRection:COLLect:TABLe:LOSS:DATA <numeric list>
            def set_loss_compensation_table(self, channel: int, port: int, data_list):
                """
                Sets the loss compensation table used for power calibration.

                Parameter:
                    channel (int): Channel number (1-16)
                    port (int): Port number (1-4)
                    data_list (list): Array size 1+2N, [N, freq1, loss1, freq2, loss2, ...]

                Return:
                    None
                """
                if not (1 <= channel <= 16):
                                    raise ValueError("channel must be 1-16")
                if not (1 <= port <= 4):
                    raise ValueError("port must be 1-4")
                data_str = ",".join(str(float(x)) for x in data_list)
                self.instrument.write(f":SOUR{channel}:POW:PORT{port}:CORR:COLL:TABL:LOSS:DATA {data_str}")

            def get_loss_compensation_table(self, channel: int, port: int):
                """
                Gets the loss compensation table used for power calibration.

                Parameter:
                    channel (int): Channel number (1-16)
                    port (int): Port number (1-4)

                Return:
                    list: Array size 1+2N, [N, freq1, loss1, freq2, loss2, ...]
                """
                if not (1 <= channel <= 16):
                                    raise ValueError("channel must be 1-16")
                if not (1 <= port <= 4):
                    raise ValueError("port must be 1-4")
                data = self.instrument.query(f":SOUR{channel}:POW:PORT{port}:CORR:COLL:TABL:LOSS:DATA?").strip()
                if self.data_handler.is_auto_saving_data_enabled():
                    self.data_handler.write_to_file(self, f"LOSS_COMP_{channel}_PORT_{port}", data, file_type = EFileType.CSV)
                return [float(x) for x in data.split(',') if x]

            # SOURce<Ch>:POWer:PORT<Pt>:CORRection:DATA <numeric list>
            def set_power_correction_data(self, channel: int, port: int, data_list):
                """
                Sets the power correction array for the port.

                Parameter:
                    channel (int): Channel number (1-16)
                    port (int): Port number (1-4)
                    data_list (list): Correction values (array size NOP)

                Return:
                    None
                """
                if not (1 <= channel <= 16):
                                    raise ValueError("channel must be 1-16")
                if not (1 <= port <= 4):
                    raise ValueError("port must be 1-4")
                data_str = ",".join(str(float(x)) for x in data_list)
                self.instrument.write(f":SOUR{channel}:POW:PORT{port}:CORR:DATA {data_str}")

            def get_power_correction_data(self, channel: int, port: int):
                """
                Gets the power correction array for the port.

                Parameter:
                    channel (int): Channel number (1-16)
                    port (int): Port number (1-4)

                Return:
                    list: Correction values (array size NOP)
                """
                if not (1 <= channel <= 16):
                                    raise ValueError("channel must be 1-16")
                if not (1 <= port <= 4):
                    raise ValueError("port must be 1-4")
                data = self.instrument.query(f":SOUR{channel}:POW:PORT{port}:CORR:DATA?").strip()
                if self.data_handler.is_auto_saving_data_enabled():
                    self.data_handler.write_to_file(self, f"POW_CORRECTION_{channel}_PORT_{port}", data, file_type = EFileType.CSV)
                return [float(x) for x in data.split(',') if x]

        # SOURce<Ch>:POWer:PORT:COUPle {OFF|ON|0|1}
        def enable_port_couple(self, channel: int, enable: bool):
            """
            Turns the port power couple ON/OFF.

            Parameter:
                channel (int): Channel number (1-16)
                enable (bool): True to enable, False to disable

            Return:
                None
            """
            if not (1 <= channel <= 16):
                        raise ValueError("channel must be 1-16")
            self.instrument.write(f":SOUR{channel}:POW:PORT:COUP {1 if enable else 0}")

        def is_port_couple_enabled(self, channel: int) -> bool:
            """
            Query if port power couple is enabled.

            Parameter:
                channel (int): Channel number (1-16)

            Return:
                bool: True if enabled, False otherwise
            """
            if not (1 <= channel <= 16):
                        raise ValueError("channel must be 1-16")
            return bool(int(self.instrument.query(f":SOUR{channel}:POW:PORT:COUP?")))

        # SOURce<Ch>:POWer[:LEVel]:SLOPe[:DATA] <numeric>
        def set_power_slope(self, channel: int, value: float):
            """
            Sets the power slope value for the frequency sweep type.

            Parameter:
                channel (int): Channel number (1-16)
                value (float): Power slope value (-2 to +2 dB/GHz)

            Return:
                None
            """
            if not (1 <= channel <= 16):
                        raise ValueError("channel must be 1-16")
            value = max(-2, min(2, value))
            self.instrument.write(f":SOUR{channel}:POW:SLOP:DATA {value}")

        def get_power_slope(self, channel: int) -> float:
            """
            Gets the power slope value for the frequency sweep type.

            Parameter:
                channel (int): Channel number (1-16)

            Return:
                float: Power slope value (-2 to +2 dB/GHz)
            """
            if not (1 <= channel <= 16):
                        raise ValueError("channel must be 1-16")
            return float(self.instrument.query(f":SOUR{channel}:POW:SLOP:DATA?"))

        # SOURce<Ch>:POWer[:LEVel]:SLOPe:STATe {OFF|ON|0|1}
        def enable_power_slope(self, channel: int, enable: bool):
            """
            Turns the power slope ON/OFF.

            Parameter:
                channel (int): Channel number (1-16)
                enable (bool): True to enable, False to disable

            Return:
                None
            """
            if not (1 <= channel <= 16):
                        raise ValueError("channel must be 1-16")
            self.instrument.write(f":SOUR{channel}:POW:SLOP:STAT {1 if enable else 0}")

        def is_power_slope_enabled(self, channel: int) -> bool:
            """
            Query if power slope is enabled.

            Parameter:
                channel (int): Channel number (1-16)

            Return:
                bool: True if enabled, False otherwise
            """
            if not (1 <= channel <= 16):
                        raise ValueError("channel must be 1-16")
            return bool(int(self.instrument.query(f":SOUR{channel}:POW:SLOP:STAT?")))

        # SOURce<Ch>:POWer:SPAN <power>
        def set_power_span(self, channel: int, value: float):
            """
            Sets the power span when the power sweep type is active.

            Parameter:
                channel (int): Channel number (1-16)
                value (float): Power sweep span value (0 to analyzer max)

            Return:
                None
            """
            if not (1 <= channel <= 16):
                        raise ValueError("channel must be 1-16")
            self.instrument.write(f":SOUR{channel}:POW:SPAN {value}")

        def get_power_span(self, channel: int) -> float:
            """
            Gets the power span when the power sweep type is active.

            Parameter:
                channel (int): Channel number (1-16)

            Return:
                float: Power sweep span value
            """
            if not (1 <= channel <= 16):
                        raise ValueError("channel must be 1-16")
            return float(self.instrument.query(f":SOUR{channel}:POW:SPAN?"))
        
        # SOURce<Ch>:POWer:STARt <power>
        def set_power_start(self, channel: int, value: float):
            """
            Sets the power sweep start value when the power sweep type is active.

            Parameter:
                channel (int): Channel number (1-16)
                value (float): Power sweep start value (within analyzer limits)

            Return:
                None
            """
            if not (1 <= channel <= 16):
                        raise ValueError("channel must be 1-16")
            self.instrument.write(f":SOUR{channel}:POW:STAR {value}")

        # SOURce<Ch>:POWer:STARt?
        def get_power_start(self, channel: int) -> float:
            """
            Gets the power sweep start value when the power sweep type is active.

            Parameter:
                channel (int): Channel number (1-16)

            Return:
                float: Power sweep start value
            """
            if not (1 <= channel <= 16):
                        raise ValueError("channel must be 1-16")
            return float(self.instrument.query(f":SOUR{channel}:POW:STAR?"))

        # SOURce<Ch>:POWer:STOP <power>
        def set_power_stop(self, channel: int, value: float):
            """
            Sets the power sweep stop value when the power sweep type is active.

            Parameter:
                channel (int): Channel number (1-16)
                value (float): Power sweep stop value (within analyzer limits)

            Return:
                None
            """
            if not (1 <= channel <= 16):
                        raise ValueError("channel must be 1-16")
            self.instrument.write(f":SOUR{channel}:POW:STOP {value}")

        # SOURce<Ch>:POWer:STOP?
        def get_power_stop(self, channel: int) -> float:
            """
            Gets the power sweep stop value when the power sweep type is active.

            Parameter:
                channel (int): Channel number (1-16)

            Return:
                float: Power sweep stop value
            """
            if not (1 <= channel <= 16):
                        raise ValueError("channel must be 1-16")
            return float(self.instrument.query(f":SOUR{channel}:POW:STOP?"))

class Status:
    """
    Status system commands.
    """
    def __init__(self, instrument, data_handler):
        self.instrument = instrument
        self.data_handler = data_handler
        self.operation = self.Operation(instrument, data_handler)
        self.questionable = self.Questionable(instrument, data_handler)
        
    # STATus:OPERation[:EVENt]?
    def get_operation_status_event(self) -> int:
        """
        Reads out the value of the Operation Status Event Register.

        Parameter:
            None

        Return:
            int: Operation Status Event Register value
        """
        return int(self.instrument.query(":STAT:OPER?"))
    class Operation:
        """
        Operation status register commands.
        """
        def __init__(self, instrument, data_handler):
            self.instrument = instrument
            self.data_handler = data_handler
        # STATus:OPERation[:EVENt]?
        def get_event(self) -> int:
            """
            Reads out the value of the Operation Status Event Register.

            Parameter:
                None

            Return:
                int: Operation Status Event Register value
            """
            return int(self.instrument.query(":STAT:OPER:EVEN?"))

        # STATus:OPERation:CONDition?
        def get_condition(self) -> int:
            """
            Reads out the value of the Operation Status Condition Register.

            Parameter:
                None

            Return:
                int: Operation Status Condition Register value
            """
            return int(self.instrument.query(":STAT:OPER:COND?"))

        # STATus:OPERation:ENABle <numeric>
        def set_enable(self, value: int):
            """
            Sets the value of the Operation Status Enable Register.

            Parameter:
                value (int): Value from 0 to 65535

            Return:
                None
            """
            value = max(0, min(65535, value))
            self.instrument.write(f":STAT:OPER:ENAB {value}")

        # STATus:OPERation:ENABle?
        def get_enable(self) -> int:
            """
            Reads out the value of the Operation Status Enable Register.

            Parameter:
                None

            Return:
                int: Operation Status Enable Register value
            """
            return int(self.instrument.query(":STAT:OPER:ENAB?"))

        # STATus:OPERation:NTRansition <numeric>
        def set_negative_transition(self, value: int):
            """
            Sets the value of the Negative transition filter of the Operation Status Register.

            Parameter:
                value (int): Value from 0 to 65535

            Return:
                None
            """
            value = max(0, min(65535, value))
            self.instrument.write(f":STAT:OPER:NTR {value}")

        # STATus:OPERation:NTRansition?
        def get_negative_transition(self) -> int:
            """
            Reads out the value of the Negative transition filter of the Operation Status Register.

            Parameter:
                None

            Return:
                int: Negative transition filter value
            """
            return int(self.instrument.query(":STAT:OPER:NTR?"))

        # STATus:OPERation:PTRansition <numeric>
        def set_positive_transition(self, value: int):
            """
            Sets the value of the Positive transition filter of the Operation Status Register.

            Parameter:
                value (int): Value from 0 to 65535

            Return:
                None
            """
            value = max(0, min(65535, value))
            self.instrument.write(f":STAT:OPER:PTR {value}")

        # STATus:OPERation:PTRansition?
        def get_positive_transition(self) -> int:
            """
            Reads out the value of the Positive transition filter of the Operation Status Register.

            Parameter:
                None

            Return:
                int: Positive transition filter value
            """
            return int(self.instrument.query(":STAT:OPER:PTR?"))

    

    # STATus:PRESet
    def preset(self):
        """
        Resets all the status registers to the factory settings.

        Parameter:
            None

        Return:
            None
        """
        self.instrument.write(":STAT:PRES")

    class Questionable:
        """
        Questionable status register commands.
        """
        def __init__(self, instrument, data_handler):
            self.instrument = instrument
            self.limit = self.Limit(instrument,data_handler)
            self.ripple_limit = self.RippleLimit(instrument,data_handler)

        # STATus:QUEStionable:PTRansition <numeric>
        def set_positive_transition(self, value: int):
            """
            Sets the value of the Positive transition filter of the Questionable Status Register.

            Parameter:
            value (int): Value from 0 to 65535

            Return:
            None
            """
            value = max(0, min(65535, value))
            self.instrument.write(f":STAT:QUES:PTR {value}")

        # STATus:QUEStionable:PTRansition?
        def get_positive_transition(self) -> int:
            """
            Reads out the value of the Positive transition filter of the Questionable Status Register.

            Parameter:
            None

            Return:
            int: Positive transition filter value
            """
            return int(self.instrument.query(":STAT:QUES:PTR?"))
        # STATus:QUEStionable:CONDition?
        def get_condition(self) -> int:
            """
            Reads out the value of the Questionable Status Condition Register.

            Parameter:
                None

            Return:
                int: Questionable Status Condition Register value
            """
            return int(self.instrument.query(":STAT:QUES:COND?"))

        # STATus:QUEStionable:ENABle <numeric>
        def set_enable(self, value: int):
            """
            Sets the value of the Questionable Status Enable Register.

            Parameter:
                value (int): Value from 0 to 65535

            Return:
                None
            """
            value = max(0, min(65535, value))
            self.instrument.write(f":STAT:QUES:ENAB {value}")

        # STATus:QUEStionable:ENABle?
        def get_enable(self) -> int:
            """
            Reads out the value of the Questionable Status Enable Register.

            Parameter:
                None

            Return:
                int: Questionable Status Enable Register value
            """
            return int(self.instrument.query(":STAT:QUES:ENAB?"))
        

            
        # STATus:QUEStionable:NTRansition <numeric>
        def set_negative_transition(self, value: int):
            """
            Sets the value of the Negative transition filter of the Questionable Status Register.

            Parameter:
                value (int): Value from 0 to 65535

            Return:
                None
            """
            value = max(0, min(65535, value))
            self.instrument.write(f":STAT:QUES:NTR {value}")

        # STATus:QUEStionable:NTRansition?
        def get_negative_transition(self) -> int:
            """
            Reads out the value of the Negative transition filter of the Questionable Status Register.

            Parameter:
                None

            Return:
                int: Negative transition filter value
            """
            return int(self.instrument.query(":STAT:QUES:NTR?"))

        # STATus:QUEStionable:PTRansition <numeric>
        def set_positive_transition(self, value: int):
            """
            Sets the value of the Positive transition filter of the Questionable Status Register.

            Parameter:
                value (int): Value from 0 to 65535

            Return:
                None
            """
            value = max(0, min(65535, value))
            self.instrument.write(f":STAT:QUES:PTR {value}")

        # STATus:QUEStionable:PTRansition?
        def get_positive_transition(self) -> int:
            """
            Reads out the value of the Positive transition filter of the Questionable Status Register.

            Parameter:
                None

            Return:
                int: Positive transition filter value
            """
            return int(self.instrument.query(":STAT:QUES:PTR?"))

        
        class Limit:
            """
            Status Limit commands.
            """
            def __init__(self, instrument, data_handler):
                self.instrument = instrument
                self.data_handler = data_handler
                self.channel = self.Channel(instrument, data_handler)
            # STATus:QUEStionable:LIMit:CONDition?
            def get_condition(self) -> int:
                """
                Reads out the value of the Questionable Limit Status Condition Register.

                Parameter:
                    None

                Return:
                    int: Questionable Limit Status Condition Register value
                """
                return int(self.instrument.query(":STAT:QUES:LIM:COND?"))

            class Channel:
                """
                Questionable Limit Channel status register commands.
                """
                def __init__(self, instrument, data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler
                # STATus:QUEStionable:LIMit:CHANnel<Ch>:CONDition?
                def get_condition(self, channel: int) -> int:
                    """
                    Reads out the value of the Questionable Limit Channel Status Condition Register.

                    Parameter:
                        channel (int): Channel number (1-16)

                    Return:
                        int: Channel Status Condition Register value
                    """
                    if not (1 <= channel <= 16):
                                        raise ValueError("channel must be 1-16")
                    return int(self.instrument.query(f":STAT:QUES:LIM:CHAN{channel}:COND?"))

                # STATus:QUEStionable:LIMit:CHANnel<Ch>:ENABle <numeric>
                def set_enable(self, channel: int, value: int):
                    """
                    Sets the value of the Questionable Limit Channel Status Enable Register.

                    Parameter:
                        channel (int): Channel number (1-16)
                        value (int): Value from 0 to 65535

                    Return:
                        None
                    """
                    if not (1 <= channel <= 16):
                                        raise ValueError("channel must be 1-16")
                    value = max(0, min(65535, value))
                    self.instrument.write(f":STAT:QUES:LIM:CHAN{channel}:ENAB {value}")

                # STATus:QUEStionable:LIMit:CHANnel<Ch>:ENABle?
                def get_enable(self, channel: int) -> int:
                    """
                    Reads out the value of the Questionable Limit Channel Status Enable Register.

                    Parameter:
                        channel (int): Channel number (1-16)

                    Return:
                        int: Channel Status Enable Register value
                    """
                    if not (1 <= channel <= 16):
                                        raise ValueError("channel must be 1-16")
                    return int(self.instrument.query(f":STAT:QUES:LIM:CHAN{channel}:ENAB?"))

                # STATus:QUEStionable:LIMit:CHANnel<Ch>:NTRansition <numeric>
                def set_negative_transition(self, channel: int, value: int):
                    """
                    Sets the value of the Negative transition filter of the Questionable Limit Channel Status Register.

                    Parameter:
                        channel (int): Channel number (1-16)
                        value (int): Value from 0 to 65535

                    Return:
                        None
                    """
                    if not (1 <= channel <= 16):
                                        raise ValueError("channel must be 1-16")
                    value = max(0, min(65535, value))
                    self.instrument.write(f":STAT:QUES:LIM:CHAN{channel}:NTR {value}")

                # STATus:QUEStionable:LIMit:CHANnel<Ch>:NTRansition?
                def get_negative_transition(self, channel: int) -> int:
                    """
                    Reads out the value of the Negative transition filter of the Questionable Limit Channel Status Register.

                    Parameter:
                        channel (int): Channel number (1-16)

                    Return:
                        int: Negative transition filter value
                    """
                    if not (1 <= channel <= 16):
                                        raise ValueError("channel must be 1-16")
                    return int(self.instrument.query(f":STAT:QUES:LIM:CHAN{channel}:NTR?"))

                # STATus:QUEStionable:LIMit:CHANnel<Ch>:PTRansition <numeric>
                def set_positive_transition(self, channel: int, value: int):
                    """
                    Sets the value of the Positive transition filter of the Questionable Limit Channel Status Register.

                    Parameter:
                        channel (int): Channel number (1-16)
                        value (int): Value from 0 to 65535

                    Return:
                        None
                    """
                    if not (1 <= channel <= 16):
                                        raise ValueError("channel must be 1-16")
                    value = max(0, min(65535, value))
                    self.instrument.write(f":STAT:QUES:LIM:CHAN{channel}:PTR {value}")

                # STATus:QUEStionable:LIMit:CHANnel<Ch>:PTRansition?
                def get_positive_transition(self, channel: int) -> int:
                    """
                    Reads out the value of the Positive transition filter of the Questionable Limit Channel Status Register.

                    Parameter:
                        channel (int): Channel number (1-16)

                    Return:
                        int: Positive transition filter value
                    """
                    if not (1 <= channel <= 16):
                                        raise ValueError("channel must be 1-16")
                    return int(self.instrument.query(f":STAT:QUES:LIM:CHAN{channel}:PTR?"))

                # STATus:QUEStionable:LIMit:CHANnel<Ch>[:EVENt]?
                def get_event(self, channel: int) -> int:
                    """
                    Reads out the value of the Questionable Limit Channel Status Condition Register (Event).

                    Parameter:
                        channel (int): Channel number (1-16)

                    Return:
                        int: Channel Status Condition Register value (Event)
                    """
                    if not (1 <= channel <= 16):
                                        raise ValueError("channel must be 1-16")
                    return int(self.instrument.query(f":STAT:QUES:LIM:CHAN{channel}:EVEN?"))
            # STATus:QUEStionable:LIMit:ENABle <numeric>
            def set_enable(self, value: int):
                """
                Sets the value of the Questionable Limit Status Enable Register.

                Parameter:
                    value (int): Value from 0 to 65535

                Return:
                    None
                """
                value = max(0, min(65535, value))
                self.instrument.write(f":STAT:QUES:LIM:ENAB {value}")

            # STATus:QUEStionable:LIMit:ENABle?
            def get_enable(self) -> int:
                """
                Reads out the value of the Questionable Limit Status Enable Register.

                Parameter:
                    None

                Return:
                    int: Questionable Limit Status Enable Register value
                """
                return int(self.instrument.query(":STAT:QUES:LIM:ENAB?"))

            # STATus:QUEStionable:LIMit:NTRansition <numeric>
            def set_negative_transition(self, value: int):
                """
                Sets the value of the Negative transition filter of the Questionable Limit Status Register.

                Parameter:
                    value (int): Value from 0 to 65535

                Return:
                    None
                """
                value = max(0, min(65535, value))
                self.instrument.write(f":STAT:QUES:LIM:NTR {value}")

            # STATus:QUEStionable:LIMit:NTRansition?
            def get_negative_transition(self) -> int:
                """
                Reads out the value of the Negative transition filter of the Questionable Limit Status Register.

                Parameter:
                    None

                Return:
                    int: Negative transition filter value
                """
                return int(self.instrument.query(":STAT:QUES:LIM:NTR?"))

            # STATus:QUEStionable:LIMit:PTRansition <numeric>
            def set_positive_transition(self, value: int):
                """
                Sets the value of the Positive transition filter of the Questionable Limit Status Register.

                Parameter:
                    value (int): Value from 0 to 65535

                Return:
                    None
                """
                value = max(0, min(65535, value))
                self.instrument.write(f":STAT:QUES:LIM:PTR {value}")

            # STATus:QUEStionable:LIMit:PTRansition?
            def get_positive_transition(self) -> int:
                """
                Reads out the value of the Positive transition filter of the Questionable Limit Status Register.

                Parameter:
                    None

                Return:
                    int: Positive transition filter value
                """
                return int(self.instrument.query(":STAT:QUES:LIM:PTR?"))

            # STATus:QUEStionable:LIMit[:EVENt]?
            def get_event(self) -> int:
                """
                Reads out the value of the Questionable Limit Status Event Register.

                Parameter:
                    None

                Return:
                    int: Questionable Limit Status Event Register value
                """
                return int(self.instrument.query(":STAT:QUES:LIM:EVEN?"))

            # STATus:LIMit:CONDition?
            def get_condition(self) -> int:
                """
                Reads out the value of the Status Limit Condition Register.

                Parameter:
                    None

                Return:
                    int: Status Limit Condition Register value
                """
                return int(self.instrument.query(":STAT:LIM:COND?"))

            # STATus:LIMit:ENABle <numeric>
            def set_enable(self, value: int):
                """
                Sets the value of the Status Limit Enable Register.

                Parameter:
                    value (int): Value from 0 to 65535

                Return:
                    None
                """
                value = max(0, min(65535, value))
                self.instrument.write(f":STAT:LIM:ENAB {value}")

            # STATus:LIMit:ENABle?
            def get_enable(self) -> int:
                """
                Reads out the value of the Status Limit Enable Register.

                Parameter:
                    None

                Return:
                    int: Status Limit Enable Register value
                """
                return int(self.instrument.query(":STAT:LIM:ENAB?"))

            # STATus:LIMit:NTRansition <numeric>
            def set_negative_transition(self, value: int):
                """
                Sets the value of the Negative transition filter of the Status Limit Register.

                Parameter:
                    value (int): Value from 0 to 65535

                Return:
                    None
                """
                value = max(0, min(65535, value))
                self.instrument.write(f":STAT:LIM:NTR {value}")

            # STATus:LIMit:NTRansition?
            def get_negative_transition(self) -> int:
                """
                Reads out the value of the Negative transition filter of the Status Limit Register.

                Parameter:
                    None

                Return:
                    int: Negative transition filter value
                """
                return int(self.instrument.query(":STAT:LIM:NTR?"))

            # STATus:LIMit:PTRansition <numeric>
            def set_positive_transition(self, value: int):
                """
                Sets the value of the Positive transition filter of the Status Limit Register.

                Parameter:
                    value (int): Value from 0 to 65535

                Return:
                    None
                """
                value = max(0, min(65535, value))
                self.instrument.write(f":STAT:LIM:PTR {value}")

            # STATus:LIMit:PTRansition?
            def get_positive_transition(self) -> int:
                """
                Reads out the value of the Positive transition filter of the Status Limit Register.

                Parameter:
                    None

                Return:
                    int: Positive transition filter value
                """
                return int(self.instrument.query(":STAT:LIM:PTR?"))

            # STATus:LIMit[:EVENt]?
            def get_event(self) -> int:
                """
                Reads out the value of the Status Limit Event Register.

                Parameter:
                    None

                Return:
                    int: Status Limit Event Register value
                """
                return int(self.instrument.query(":STAT:LIM:EVEN?"))

        class RippleLimit:
            """
            Status Ripple Limit commands.
            """
            def __init__(self, instrument, data_handler):
                self.instrument = instrument
                self.data_handler = data_handler
                self.channel = self.Channel(instrument, data_handler)
            # STATus:QUEStionable:RLIMit:CONDition?
            def get_condition(self) -> int:
                """
                Reads out the value of the Questionable Ripple Limit Status Condition Register.

                Parameter:
                    None

                Return:
                    int: Ripple Limit Status Condition Register value
                """
                return int(self.instrument.query(":STAT:QUES:RLIM:COND?"))

            class Channel:
                """
                Questionable Ripple Limit Channel status register commands.
                """
                def __init__(self, instrument, data_handler):
                    self.instrument = instrument
                    self.data_handler = data_handler
                # STATus:QUEStionable:RLIMit:CHANnel<Ch>:CONDition?
                def get_condition(self, channel: int) -> int:
                    """
                    Reads out the value of the Questionable Ripple Limit Channel Status Condition Register.

                    Parameter:
                    channel (int): Channel number (1-16)

                    Return:
                    int: Channel Status Condition Register value
                    """
                    if not (1 <= channel <= 16):
                                        raise ValueError("channel must be 1-16")
                    return int(self.instrument.query(f":STAT:QUES:RLIM:CHAN{channel}:COND?"))

                # STATus:QUEStionable:RLIMit:CHANnel<Ch>:ENABle <numeric>
                def set_enable(self, channel: int, value: int):
                    """
                    Sets the value of the Questionable Ripple Limit Channel Status Enable Register.

                    Parameter:
                    channel (int): Channel number (1-16)
                    value (int): Value from 0 to 65535

                    Return:
                    None
                    """
                    if not (1 <= channel <= 16):
                                    raise ValueError("channel must be 1-16")
                    value = max(0, min(65535, value))
                    self.instrument.write(f":STAT:QUES:RLIM:CHAN{channel}:ENAB {value}")

                # STATus:QUEStionable:RLIMit:CHANnel<Ch>:ENABle?
                def get_enable(self, channel: int) -> int:
                    """
                    Reads out the value of the Questionable Ripple Limit Channel Status Enable Register.

                    Parameter:
                    channel (int): Channel number (1-16)

                    Return:
                    int: Channel Status Enable Register value
                    """
                    if not (1 <= channel <= 16):
                                        raise ValueError("channel must be 1-16")
                    return int(self.instrument.query(f":STAT:QUES:RLIM:CHAN{channel}:ENAB?"))

            # STATus:QUEStionable:RLIMit:CHANnel<Ch>:NTRansition <numeric>
            def set_negative_transition(self, channel: int, value: int):
                """
                Sets the value of the Negative transition filter of the Questionable Ripple Limit Channel Status Register.

                Parameter:
                channel (int): Channel number (1-16)
                value (int): Value from 0 to 65535

                Return:
                None
                """
                if not (1 <= channel <= 16):
                        raise ValueError("channel must be 1-16")
                value = max(0, min(65535, value))
                self.instrument.write(f":STAT:QUES:RLIM:CHAN{channel}:NTR {value}")

            # STATus:QUEStionable:RLIMit:CHANnel<Ch>:NTRansition?
            def get_negative_transition(self, channel: int) -> int:
                """
                Reads out the value of the Negative transition filter of the Questionable Ripple Limit Channel Status Register.

                Parameter:
                channel (int): Channel number (1-16)

                Return:
                int: Negative transition filter value
                """
                if not (1 <= channel <= 16):
                        raise ValueError("channel must be 1-16")
                return int(self.instrument.query(f":STAT:QUES:RLIM:CHAN{channel}:NTR?"))

            # STATus:QUEStionable:RLIMit:CHANnel<Ch>:PTRansition <numeric>
            def set_positive_transition(self, channel: int, value: int):
                """
                Sets the value of the Positive transition filter of the Questionable Ripple Limit Channel Status Register.

                Parameter:
                channel (int): Channel number (1-16)
                value (int): Value from 0 to 65535

                Return:
                None
                """
                if not (1 <= channel <= 16):
                        raise ValueError("channel must be 1-16")
                value = max(0, min(65535, value))
                self.instrument.write(f":STAT:QUES:RLIM:CHAN{channel}:PTR {value}")

            # STATus:QUEStionable:RLIMit:CHANnel<Ch>:PTRansition?
            def get_positive_transition(self, channel: int) -> int:
                """
                Reads out the value of the Positive transition filter of the Questionable Ripple Limit Channel Status Register.

                Parameter:
                channel (int): Channel number (1-16)

                Return:
                int: Positive transition filter value
                """
                if not (1 <= channel <= 16):
                        raise ValueError("channel must be 1-16")
                return int(self.instrument.query(f":STAT:QUES:RLIM:CHAN{channel}:PTR?"))

            # STATus:QUEStionable:RLIMit:CHANnel<Ch>[:EVENt]?
            def get_event(self, channel: int) -> int:
                """
                Reads out the value of the Questionable Ripple Limit Channel Status Event Register.

                Parameter:
                channel (int): Channel number (1-16)

                Return:
                int: Channel Status Event Register value
                """
                if not (1 <= channel <= 16):
                        raise ValueError("channel must be 1-16")
                return int(self.instrument.query(f":STAT:QUES:RLIM:CHAN{channel}:EVEN?"))

            # STATus:QUEStionable:RLIMit:ENABle <numeric>
            def set_enable(self, value: int):
                """
                Sets the value of the Questionable Ripple Limit Status Enable Register.

                Parameter:
                    value (int): Value from 0 to 65535

                Return:
                    None
                """
                value = max(0, min(65535, value))
                self.instrument.write(f":STAT:QUES:RLIM:ENAB {value}")

            # STATus:QUEStionable:RLIMit:ENABle?
            def get_enable(self) -> int:
                """
                Reads out the value of the Questionable Ripple Limit Status Enable Register.

                Parameter:
                    None

                Return:
                    int: Ripple Limit Status Enable Register value
                """
                return int(self.instrument.query(":STAT:QUES:RLIM:ENAB?"))

            # STATus:QUEStionable:RLIMit:NTRansition <numeric>
            def set_negative_transition(self, value: int):
                """
                Sets the value of the Negative transition filter of the Questionable Ripple Limit Status Register.

                Parameter:
                    value (int): Value from 0 to 65535

                Return:
                    None
                """
                value = max(0, min(65535, value))
                self.instrument.write(f":STAT:QUES:RLIM:NTR {value}")

            # STATus:QUEStionable:RLIMit:NTRansition?
            def get_negative_transition(self) -> int:
                """
                Reads out the value of the Negative transition filter of the Questionable Ripple Limit Status Register.

                Parameter:
                    None

                Return:
                    int: Negative transition filter value
                """
                return int(self.instrument.query(":STAT:QUES:RLIM:NTR?"))

            # STATus:QUEStionable:RLIMit:PTRansition <numeric>
            def set_positive_transition(self, value: int):
                """
                Sets the value of the Positive transition filter of the Questionable Ripple Limit Status Register.

                Parameter:
                    value (int): Value from 0 to 65535

                Return:
                    None
                """
                value = max(0, min(65535, value))
                self.instrument.write(f":STAT:QUES:RLIM:PTR {value}")

            # STATus:QUEStionable:RLIMit:PTRansition?
            def get_positive_transition(self) -> int:
                """
                Reads out the value of the Positive transition filter of the Questionable Ripple Limit Status Register.

                Parameter:
                    None

                Return:
                    int: Positive transition filter value
                """
                return int(self.instrument.query(":STAT:QUES:RLIM:PTR?"))

            # STATus:QUEStionable:RLIMit[:EVENt]?
            def get_event(self) -> int:
                """
                Reads out the value of the Questionable Ripple Limit Status Event Register.

                Parameter:
                    None

                Return:
                    int: Ripple Limit Status Event Register value
                """
                return int(self.instrument.query(":STAT:QUES:RLIM:EVEN?"))
            # STATus:RLIMit:CONDition?
            def get_condition(self) -> int:
                """
                Reads out the value of the Status Ripple Limit Condition Register.

                Parameter:
                    None

                Return:
                    int: Ripple Limit Condition Register value
                """
                return int(self.instrument.query(":STAT:RLIM:COND?"))

            # STATus:RLIMit:ENABle <numeric>
            def set_enable(self, value: int):
                """
                Sets the value of the Status Ripple Limit Enable Register.

                Parameter:
                    value (int): Value from 0 to 65535

                Return:
                    None
                """
                value = max(0, min(65535, value))
                self.instrument.write(f":STAT:RLIM:ENAB {value}")

            # STATus:RLIMit:ENABle?
            def get_enable(self) -> int:
                """
                Reads out the value of the Status Ripple Limit Enable Register.

                Parameter:
                    None

                Return:
                    int: Ripple Limit Enable Register value
                """
                return int(self.instrument.query(":STAT:RLIM:ENAB?"))

            # STATus:RLIMit:NTRansition <numeric>
            def set_negative_transition(self, value: int):
                """
                Sets the value of the Negative transition filter of the Status Ripple Limit Register.

                Parameter:
                    value (int): Value from 0 to 65535

                Return:
                    None
                """
                value = max(0, min(65535, value))
                self.instrument.write(f":STAT:RLIM:NTR {value}")

            # STATus:RLIMit:NTRansition?
            def get_negative_transition(self) -> int:
                """
                Reads out the value of the Negative transition filter of the Status Ripple Limit Register.

                Parameter:
                    None

                Return:
                    int: Negative transition filter value
                """
                return int(self.instrument.query(":STAT:RLIM:NTR?"))

            # STATus:RLIMit:PTRansition <numeric>
            def set_positive_transition(self, value: int):
                """
                Sets the value of the Positive transition filter of the Status Ripple Limit Register.

                Parameter:
                    value (int): Value from 0 to 65535

                Return:
                    None
                """
                value = max(0, min(65535, value))
                self.instrument.write(f":STAT:RLIM:PTR {value}")

            # STATus:RLIMit:PTRansition?
            def get_positive_transition(self) -> int:
                """
                Reads out the value of the Positive transition filter of the Status Ripple Limit Register.

                Parameter:
                    None

                Return:
                    int: Positive transition filter value
                """
                return int(self.instrument.query(":STAT:RLIM:PTR?"))

            # STATus:RLIMit[:EVENt]?
            def get_event(self) -> int:
                """
                Reads out the value of the Status Ripple Limit Event Register.

                Parameter:
                    None

                Return:
                    int: Ripple Limit Event Register value
                """
                return int(self.instrument.query(":STAT:RLIM:EVEN?"))

class System:
    """
    System commands.
    """
    def __init__(self, instrument, data_handler):
        self.instrument = instrument
        self.data_handler = data_handler
        self.display = self.Display(instrument, data_handler)
        self.datetime = self.DateTime(instrument)
        self.beeper = self.Beeper(instrument)
        self.capability = self.Capability(instrument)
        self.communicate = self.Communicate(instrument)
        self.connect = self.Connect(instrument)
        self.correction = self.Correction(instrument)
        self.cycle = self.Cycle(instrument)
        self.date = self.Date(instrument)
        self.dynamic_range_extension = self.DynamicRangeExtension(instrument)
        
        self.receiver = self.Receiver(instrument)
        self.time = self.Time(instrument)
    # SYSTem:ERRor[:NEXT]?
    def get_error(self) -> str:
        """
        Reads out the next error in the error queue.

        Parameter:
        None

        Return:
        str: Error string
        """
        return self.instrument.query(":SYST:ERR?").strip()

    # SYSTem:VERSion?
    def get_version(self) -> str:
        """
        Reads out the version of the instrument firmware.

        Parameter:
        None

        Return:
        str: Firmware version
        """
        return self.instrument.query(":SYST:VERS?").strip()

    # SYSTem:DATE?
    def get_date(self) -> str:
        """
        Reads out the current date from the instrument.

        Parameter:
        None

        Return:
        str: Date string
        """
        return self.instrument.query(":SYST:DATE?").strip()

    # SYSTem:TIME?
    def get_time(self) -> str:
        """
        Reads out the current time from the instrument.

        Parameter:
        None

        Return:
        str: Time string
        """
        return self.instrument.query(":SYST:TIME?").strip()

    # SYSTem:PRESet
    def preset(self):
        """
        Resets the instrument to its preset state.

        Parameter:
        None

        Return:
        None
        """
        self.instrument.write(":SYST:PRESet")

    class Display:
        """
        System display commands.
        """
        def __init__(self, instrument, data_handler):
            self.instrument = instrument
            self.data_handler = data_handler
        # SYSTem:DISPlay:BRIGhtness <numeric>
        def set_brightness(self, value: int):
            """
            Sets the display brightness.

            Parameter:
                value (int): Brightness value (0-100)

            Return:
                None
            """
            value = max(0, min(100, value))
            self.instrument.write(f":SYST:DISP:BRIG {value}")

        # SYSTem:DISPlay:BRIGhtness?
        def get_brightness(self) -> int:
            """
            Reads out the display brightness.

            Parameter:
                None

            Return:
                int: Brightness value (0-100)
            """
            return int(self.instrument.query(":SYST:DISP:BRIG?"))

    class DateTime:
        """
        System date and time commands.
        """
        def __init__(self, instrument):
            self.instrument = instrument

        # SYSTem:DATE <string>
        def set_date(self, date_str: str):
            """
            Sets the system date.

            Parameter:
                date_str (str): Date string in format 'YYYY-MM-DD'

            Return:
                None
            """
            self.instrument.write(f":SYST:DATE \"{date_str}\"")

        # SYSTem:TIME <string>
        def set_time(self, time_str: str):
            """
            Sets the system time.

            Parameter:
                time_str (str): Time string in format 'HH:MM:SS'

            Return:
                None
            """
            self.instrument.write(f":SYST:TIME \"{time_str}\"")
    class Beeper:
        """
        System beeper commands.
        """
        def __init__(self, instrument):
            self.instrument = instrument

        # SYSTem:BEEPer:COMPlete:IMMediate
        def beep_complete(self):
            """
            Generates a beep to notify of the completion of the operation.

            Parameter:
                None

            Return:
                None
            """
            self.instrument.write(":SYST:BEEP:COMP:IMM")

        # SYSTem:BEEPer:COMPlete:STATe {OFF|ON|0|1}
        def enable_complete_beep(self, enable: bool):
            """
            Turns the beeper denoting completion of the operation ON/OFF.

            Parameter:
                enable (bool): True to enable, False to disable

            Return:
                None
            """
            self.instrument.write(f":SYST:BEEP:COMP:STAT {1 if enable else 0}")

        # SYSTem:BEEPer:COMPlete:STATe?
        def is_complete_beep_enabled(self) -> bool:
            """
            Query if the beeper denoting completion of the operation is enabled.

            Parameter:
                None

            Return:
                bool: True if enabled, False otherwise
            """
            return bool(int(self.instrument.query(":SYST:BEEP:COMP:STAT?")))

        # SYSTem:BEEPer:WARNing:IMMediate
        def beep_warning(self):
            """
            Generates a beep to signify a warning.

            Parameter:
                None

            Return:
                None
            """
            self.instrument.write(":SYST:BEEP:WARN:IMM")

        # SYSTem:BEEPer:WARNing:STATe {OFF|ON|0|1}
        def enable_warning_beep(self, enable: bool):
            """
            Turns the beeper signifying a warning ON/OFF.

            Parameter:
                enable (bool): True to enable, False to disable

            Return:
                None
            """
            self.instrument.write(f":SYST:BEEP:WARN:STAT {1 if enable else 0}")

        # SYSTem:BEEPer:WARNing:STATe?
        def is_warning_beep_enabled(self) -> bool:
            """
            Query if the beeper signifying a warning is enabled.

            Parameter:
                None

            Return:
                bool: True if enabled, False otherwise
            """
            return bool(int(self.instrument.query(":SYST:BEEP:WARN:STAT?")))

    class Capability:
        """
        System capability commands.
        """
        def __init__(self, instrument):
            self.instrument = instrument

        # SYSTem:CAPability:IFBW:MAXimum?
        def get_ifbw_max(self) -> float:
            """
            Reads out the upper limit of the IFBW.

            Parameter:
                None

            Return:
                float: Upper limit of IFBW in Hz
            """
            return float(self.instrument.query(":SYST:CAP:IFBW:MAX?"))

        # SYSTem:CAPability:IFBW:MINimum?
        def get_ifbw_min(self) -> float:
            """
            Reads out the lower limit of the IFBW.

            Parameter:
                None

            Return:
                float: Lower limit of IFBW in Hz
            """
            return float(self.instrument.query(":SYST:CAP:IFBW:MIN?"))
        # SYSTem:CAPability:CURRent:CONSumption?
        def has_current_consumption_measurement(self) -> bool:
            """
            Returns whether or not the Analyzer has its current consumption measurement.

            Parameter:
                None

            Return:
                bool: True if measurement exists, False otherwise
            """
            return bool(int(self.instrument.query(":SYST:CAP:CURR:CONS?")))

        # SYSTem:CURRent:CONSumption?
        def get_current_consumption(self) -> float:
            """
            Reads out the current consumption of the Analyzer.

            Parameter:
                None

            Return:
                float: Current consumption in Amperes
            """
            return float(self.instrument.query(":SYST:CURR:CONS?"))

    class Communicate:
        """
        System communicate commands.
        """
        def __init__(self, instrument):
            self.instrument = instrument
            self.ecal = self.AutoCal(instrument)
            self.psensor = self.PSensor(instrument)
        class AutoCal:
            """
            AutoCal module communicate commands.
            """
            def __init__(self, instrument):
                self.instrument = instrument

            # SYSTem:COMMunicate:ECAL:CHECk
            def set_check_state(self):
                """
                Sets the CHECK state of the AutoCal module (attenuator state).

                Parameter:
                    None

                Return:
                    None
                """
                self.instrument.write(":SYST:COMM:ECAL:CHEC")

            # SYSTem:COMMunicate:ECAL:DATA? <path>, <impedance> [,<characterization>]
            def get_characterization_data(self, path: str, impedance: str, characterization: str = "FACTory"):
                """
                Reads out the AutoCal module characterization data.

                Parameter:
                    path (str): Port number, port pair, or check state ('A','B','C','D','AB','AC','AD','BC','BD','CD','CHECk')
                    impedance (str): Impedance state or S-parameter
                    characterization (str, optional): Characterization name ('FACTory','USER1','USER2','USER3')

                Return:
                    list: S-parameter array (real/imag pairs)
                """
                allowed_paths = ['A','B','C','D','AB','AC','AD','BC','BD','CD','CHECk']
                allowed_impedances = [
                    'SHORt','OPEN','LOAD','OPEN2','LOAD2',
                    'S11','S12','S21','S22','S33','S34','S43','S44'
                ]
                allowed_characterizations = ['FACTory','USER1','USER2','USER3']
                if path not in allowed_paths:
                    raise ValueError(f"path must be one of {allowed_paths}")
                if impedance not in allowed_impedances:
                    raise ValueError(f"impedance must be one of {allowed_impedances}")
                if characterization and characterization not in allowed_characterizations:
                    raise ValueError(f"characterization must be one of {allowed_characterizations}")
                cmd = f":SYST:COMM:ECAL:DATA? {path},{impedance}"
                if characterization:
                    cmd += f",{characterization}"
                data = self.instrument.query(cmd)
                data =  [float(x) for x in data.strip().split(',') if x]
                if self.data_handler.is_auto_saving_data_enabled():
                    self.data_handler.write_to_file(self, f"S_PARAMS", data, file_type = EFileType.CSV)
                return data

            # SYSTem:COMMunicate:ECAL:FREQuency:DATA? [<characterization>]
            def get_characterization_frequency_array(self, characterization: str = "FACTory"):
                """
                Reads out the AutoCal module characterization frequency array.

                Parameter:
                    characterization (str, optional): Characterization name ('FACTory','USER1','USER2','USER3')

                Return:
                    list: Frequency values at each characterization point
                """
                allowed_characterizations = ['FACTory','USER1','USER2','USER3']
                if characterization and characterization not in allowed_characterizations:
                    raise ValueError(f"characterization must be one of {allowed_characterizations}")
                cmd = ":SYST:COMM:ECAL:FREQ:DATA?"
                if characterization:
                    cmd += f" {characterization}"
                data = self.instrument.query(cmd)
                data = [float(x) for x in data.strip().split(',') if x]
                if self.data_handler.is_auto_saving_data_enabled():
                    self.data_handler.write_to_file(self, f"CHAR_POINT_FREQS", data, file_type = EFileType.CSV)
                return data

            # SYSTem:COMMunicate:ECAL:POINts? [<characterization>]
            def get_characterization_point_count(self, characterization: str = "FACTory") -> int:
                """
                Reads out the AutoCal module characterization point number.

                Parameter:
                    characterization (str, optional): Characterization name ('FACTory','USER1','USER2','USER3')

                Return:
                    int: Number of points (0 if characterization does not exist)
                """
                allowed_characterizations = ['FACTory','USER1','USER2','USER3']
                if characterization and characterization not in allowed_characterizations:
                    raise ValueError(f"characterization must be one of {allowed_characterizations}")
                cmd = ":SYST:COMM:ECAL:POIN?"
                if characterization:
                    cmd += f" {characterization}"
                return int(self.instrument.query(cmd))

            # SYSTem:COMMunicate:ECAL:IMPedance <port>,<char>
            def set_impedance_state(self, port: str, state: str):
                """
                Sets the impedance state of the specified port of the AutoCal module.

                Parameter:
                    port (str): Port number ('A','B','C','D')
                    state (str): Impedance state ('OPEN','SHORt','LOAD','LOAD2','OPEN2')

                Return:
                    None
                """
                allowed_ports = ['A','B','C','D']
                allowed_states = ['OPEN','SHORt','LOAD','LOAD2','OPEN2']
                if port not in allowed_ports:
                    raise ValueError(f"port must be one of {allowed_ports}")
                if state not in allowed_states:
                    raise ValueError(f"state must be one of {allowed_states}")
                self.instrument.write(f":SYST:COMM:ECAL:IMP {port},{state}")

            # SYSTem:COMMunicate:ECAL:IMPedance? <port>
            def get_impedance_state(self, port: str) -> str:
                """
                Reads out the impedance state of the specified port of the AutoCal module.

                Parameter:
                    port (str): Port number ('A','B','C','D')

                Return:
                    str: Impedance state ('OPEN','SHOR','LOAD','THRU','LOAD2','OPEN2')
                """
                allowed_ports = ['A','B','C','D']
                if port not in allowed_ports:
                    raise ValueError(f"port must be one of {allowed_ports}")
                return self.instrument.query(f":SYST:COMM:ECAL:IMP? {port}").strip()
            # SYSTem:COMMunicate:ECAL:READy?
            def is_autocal_module_ready(self) -> bool:
                """
                Reads out the readiness status of the AutoCal Module.

                Parameter:
                    None

                Return:
                    bool: True if the AutoCal Module is ready, False otherwise
                """
                return bool(int(self.instrument.query(":SYST:COMM:ECAL:READ?")))

            # SYSTem:COMMunicate:ECAL:TEMPerature:SENSor?
            def get_autocal_temperature(self) -> float:
                """
                Reads out the temperature of the AutoCal module connected to the Analyzer.

                Parameter:
                    None

                Return:
                    float: Temperature in degrees Celsius
                """
                return float(self.instrument.query(":SYST:COMM:ECAL:TEMP:SENS?"))

            # SYSTem:COMMunicate:ECAL:THRU <port1>,<port2>
            def set_thru_state(self, port1: int, port2: int):
                """
                Sets the THRU state between the specified 2 ports of the AutoCal module.

                Parameter:
                    port1 (int): The first port number of the AutoCal module
                    port2 (int): The second port number of the AutoCal module

                Return:
                    None
                """
                self.instrument.write(f":SYST:COMM:ECAL:THRU {port1},{port2}")

        class PSensor:
            """
            Power sensor communicate commands.
            """
            def __init__(self, instrument):
                self.instrument = instrument

            # SYSTem:COMMunicate:PSENsor:NI568x:RESource:NAME <string>
            def set_ni568x_resource_name(self, name: str):
                """
                Sets the NI568x power sensor resource name to be used in a source power calibration.

                Parameter:
                    name (str): Resource name

                Return:
                    None
                """
                self.instrument.write(f":SYST:COMM:PSEN:NI568x:RES:NAME \"{name}\"")

            # SYSTem:COMMunicate:PSENsor:RESource:NAME?
            def get_resource_name(self) -> str:
                """
                Reads out the NI568x power sensor resource name used in a source power calibration.

                Parameter:
                    None

                Return:
                    str: Resource name
                """
                return self.instrument.query(":SYST:COMM:PSEN:RES:NAME?").strip()

            # SYSTem:COMMunicate:PSENsor:READy?
            def is_power_sensor_ready(self) -> bool:
                """
                Reads out the readiness status of the Power Sensor.

                Parameter:
                    None

                Return:
                    bool: True if the Power Sensor is ready, False otherwise
                """
                return bool(int(self.instrument.query(":SYST:COMM:PSEN:READ?")))

            # SYSTem:COMMunicate:PSENsor:TYPE <char>
            def set_power_sensor_type(self, sensor_type: str):
                """
                Selects the power sensor type to be used in a source power calibration.

                Parameter:
                    sensor_type (str): Sensor type, one of ['NRPZ', 'NRPxT', 'NRVS', 'U848x', 'U20xx', 'LB59xx', 'LBxxx', 'NI568x']

                Return:
                    None
                """
                allowed = ['NRPZ', 'NRPxT', 'NRVS', 'U848x', 'U20xx', 'LB59xx', 'LBxxx', 'NI568x']
                if sensor_type not in allowed:
                    raise ValueError(f"sensor_type must be one of {allowed}")
                self.instrument.write(f":SYST:COMM:PSEN:TYPE {sensor_type}")

            # SYSTem:COMMunicate:PSENsor:TYPE?
            def get_power_sensor_type(self) -> str:
                """
                Reads out the power sensor type used in a source power calibration.

                Parameter:
                    None

                Return:
                    str: Sensor type
                """
                return self.instrument.query(":SYST:COMM:PSEN:TYPE?").strip()

            # SYSTem:COMMunicate:PSENsor:ZEROing
            def execute_zeroing(self):
                """
                Executes the zeroing procedure of the power sensor.

                Parameter:
                    None

                Return:
                    None
                """
                self.instrument.write(":SYST:COMM:PSEN:ZERO")

    class Connect:
        """
        System connect commands.
        """
        def __init__(self, instrument):
            self.instrument = instrument

        # SYSTem:CONNect:SERial:NUMBer <string>
        def connect_serial_number(self, serial: str):
            """
            Connects the current program instance to the analyzer with specified serial number.

            Parameter:
                serial (str): Serial number of 8 digits, or '0' for auto-detect

            Return:
                None
            """
            if serial != "0" and (not serial.isdigit() or len(serial) != 8):
                raise ValueError("serial must be 8 digits or '0'")
            self.instrument.write(f":SYST:CONN:SER:NUMB {serial}")

        # SYSTem:CONNect:SERial:NUMBer?
        def get_connected_serial_number(self) -> str:
            """
            Returns the serial number of the connected analyzer.

            Parameter:
                None

            Return:
                str: Serial number of 8 digits, or '0'
            """
            return self.instrument.query(":SYST:CONN:SER:NUMB?").strip()

    class Correction:
        """
        System correction commands.
        """
        def __init__(self, instrument):
            self.instrument = instrument

        # SYSTem:CORRection[:STATe] {OFF|ON|0|1}
        def enable_correction(self, enable: bool):
            """
            Turns the system correction ON/OFF.

            Parameter:
                enable (bool): True to enable, False to disable

            Return:
                None
            """
            self.instrument.write(f":SYST:CORR:STAT {1 if enable else 0}")

        # SYSTem:CORRection[:STATe]?
        def is_correction_enabled(self) -> bool:
            """
            Query if system correction is enabled.

            Parameter:
                None

            Return:
                bool: True if enabled, False otherwise
            """
            return bool(int(self.instrument.query(":SYST:CORR:STAT?")))
        
    class Cycle:
        """
        System cycle time commands.
        """
        def __init__(self, instrument):
            self.instrument = instrument
            self.time = self.Time(instrument)
        class Time:
            """
            Cycle time measurement commands.
            """
            def __init__(self, instrument):
                self.instrument = instrument

            # SYSTem:CYCLe:TIME:MEASurement?
            def get_measured_cycle_time(self) -> float:
                """
                Reads out the measured cycle time (interval between sweeps).

                Parameter:
                    None

                Return:
                    float: Measured cycle time in seconds
                """
                return float(self.instrument.query(":SYST:CYC:TIME:MEAS?"))

            # SYSTem:CYCLe:TIME:METHod <char>
            def set_measurement_method(self, method: str):
                """
                Selects the cycle time measurement method.

                Parameter:
                    method (str): 'AVERaging' or 'MAXHold'

                Return:
                    None
                """
                allowed = ['AVERaging', 'MAXHold']
                if method not in allowed:
                    raise ValueError("method must be 'AVERaging' or 'MAXHold'")
                self.instrument.write(f":SYST:CYC:TIME:METH {method}")

            # SYSTem:CYCLe:TIME:METHod?
            def get_measurement_method(self) -> str:
                """
                Reads out the selected cycle time measurement method.

                Parameter:
                    None

                Return:
                    str: 'AVER' or 'MAXH'
                """
                return self.instrument.query(":SYST:CYC:TIME:METH?").strip()

            # SYSTem:CYCLe:TIME:RESTart
            def restart_cycle_time_measurement(self):
                """
                Restarts the averaging or maximum hold of the cycle time measurement.

                Parameter:
                    None

                Return:
                    None
                """
                self.instrument.write(":SYST:CYC:TIME:REST")

    class Date:
        """
        System date commands.
        """
        def __init__(self, instrument):
            self.instrument = instrument

        # SYSTem:DATE <numeric 1>,<numeric 2>,<numeric 3>
        def set_date(self, year: int, month: int, day: int):
            """
            Sets the current date.

            Parameter:
                year (int): Year (1900-2100)
                month (int): Month (1-12)
                day (int): Day (1-31)

            Return:
                None
            """
            if not (1900 <= year <= 2100):
                raise ValueError("year must be between 1900 and 2100")
            if not (1 <= month <= 12):
                raise ValueError("month must be between 1 and 12")
            if not (1 <= day <= 31):
                raise ValueError("day must be between 1 and 31")
            self.instrument.write(f":SYST:DATE {year},{month},{day}")

        # SYSTem:DATE?
        def get_date(self):
            """
            Reads out the current date.

            Parameter:
                None

            Return:
                tuple: (year, month, day)
            """
            resp = self.instrument.query(":SYST:DATE?").strip()
            parts = resp.split(',')
            return tuple(int(x) for x in parts)

    class DynamicRangeExtension:
        """
        System dynamic range extension commands.
        """
        def __init__(self, instrument):
            self.instrument = instrument

        # SYSTem:DYNamic:RANGe:EXTension[:STATe] {OFF|ON|0|1}
        def set_dynamic_range_extension(self, enable: bool):
            """
            Turns the dynamic range extension function ON/OFF.

            Parameter:
                enable (bool): True to enable, False to disable

            Return:
                None
            """
            self.instrument.write(f":SYST:DYN:RANG:EXT:STAT {1 if enable else 0}")

        # SYSTem:DYNamic:RANGe:EXTension?
        def is_dynamic_range_extension_enabled(self) -> bool:
            """
            Query if dynamic range extension function is enabled.

            Parameter:
                None

            Return:
                bool: True if enabled, False otherwise
            """
            return bool(int(self.instrument.query(":SYST:DYN:RANG:EXT?")))
    

    class Receiver:
        """
        System receiver commands.
        """
        def __init__(self, instrument):
            self.instrument = instrument

        # SYSTem:RECeiver:DIRect:ACCess[:STATe] {OFF|ON|0|1}
        def enable_direct_access(self, enable: bool):
            """
            Turns the direct access to the receiver function ON/OFF.

            Parameter:
                enable (bool): True to enable, False to disable

            Return:
                None
            """
            self.instrument.write(f":SYST:REC:DIR:ACC {1 if enable else 0}")

        # SYSTem:RECeiver:DIRect:ACCess[:STATe]?
        def is_direct_access_enabled(self) -> bool:
            """
            Query if direct access to the receiver function is enabled.

            Parameter:
                None

            Return:
                bool: True if enabled, False otherwise
            """
            return bool(int(self.instrument.query(":SYST:REC:DIR:ACC?")))

        # SYSTem:RECeiver:OVERload:POWer[:STATe] {OFF|ON|0|1}
        def enable_power_trip_at_overload(self, enable: bool):
            """
            Turns the Power Trip at Overload function ON/OFF.

            Parameter:
                enable (bool): True to enable, False to disable

            Return:
                None
            """
            self.instrument.write(f":SYST:REC:OVER:POW {1 if enable else 0}")

        # SYSTem:RECeiver:OVERload:POWer[:STATe]?
        def is_power_trip_at_overload_enabled(self) -> bool:
            """
            Query if Power Trip at Overload function is enabled.

            Parameter:
                None

            Return:
                bool: True if enabled, False otherwise
            """
            return bool(int(self.instrument.query(":SYST:REC:OVER:POW?")))

        def hide_analyzer_window(self):
            """
            Hides the Analyzer main window, removing it from the desktop.

            Parameter:
                None

            Return:
                None
            """
            self.instrument.write(":SYST:HIDE")

        def set_local_mode(self):
            """
            Sets the Analyzer to the local operation mode, when all the keys on the front panel, mouse, and touch screen are active.

            Parameter:
                None

            Return:
                None
            """
            self.instrument.write(":SYST:LOC")

        def preset_analyzer(self):
            """
            Resets the Analyzer to default settings. Differs from *RST: trigger is set to Continuous mode.

            Parameter:
                None

            Return:
                None
            """
            self.instrument.write(":SYST:PRES")

        def is_analyzer_ready(self) -> bool:
            """
            Reads out the Analyzer readiness status.

            Parameter:
                None

            Return:
                bool: True if Analyzer is ready, False otherwise
            """
            return bool(int(self.instrument.query(":SYST:READ?")))

        def set_remote_mode(self):
            """
            Sets the Analyzer to the remote operation mode, disabling all keys except "Return to Local".

            Parameter:
                None

            Return:
                None
            """
            self.instrument.write(":SYST:REM")
    class Time:
        """
        System time commands.
        """
        def __init__(self, instrument):
            self.instrument = instrument

        # SYSTem:TIME <numeric 1>,<numeric 2>,<numeric 3>
        def set_time(self, hour: int, minute: int, second: int):
            """
            Sets the current time.

            Parameter:
                hour (int): Hours from 0 to 23
                minute (int): Minutes from 0 to 59
                second (int): Seconds from 0 to 59

            Return:
                None
            """
            if not (0 <= hour <= 23):
                raise ValueError("hour must be between 0 and 23")
            if not (0 <= minute <= 59):
                raise ValueError("minute must be between 0 and 59")
            if not (0 <= second <= 59):
                raise ValueError("second must be between 0 and 59")
            self.instrument.write(f":SYST:TIME {hour},{minute},{second}")

        # SYSTem:TIME?
        def get_time(self):
            """
            Reads out the current time.

            Parameter:
                None

            Return:
                tuple: (hour, minute, second)
            """
            resp = self.instrument.query(":SYST:TIME?").strip()
            parts = resp.split(',')
            return tuple(int(x) for x in parts)

class Trigger:
    """
    addition Trigger system commands.
    """
    def __init__(self, instrument, data_handler):
        self.instrument = instrument
        self.average = self.Average(instrument)
        self.external = self.External(instrument)
        self.output = self.Output(instrument)
        self.point = self.Point(instrument)
    # TRIGger[:SEQuence][:IMMediate]
    def sequence_immediate(self):
        """
        Generates a trigger signal and initiates a sweep if conditions are met.

        Parameter:
            None

        Return:
            None
        """
        self.instrument.write(":TRIG:SEQ:IMM")

    class Average:
        """
        Trigger averaging commands.
        """
        def __init__(self, instrument):
            self.instrument = instrument

        # TRIGger[:SEQuence]:AVERage {OFF|ON|0|1}
        def enable_average(self, enable: bool):
            """
            Turns the averaging trigger function ON/OFF.

            Parameter:
                enable (bool): True to enable, False to disable

            Return:
                None
            """
            self.instrument.write(f":TRIG:SEQ:AVER {1 if enable else 0}")

        # TRIGger[:SEQuence]:AVERage?
        def is_average_enabled(self) -> bool:
            """
            Query if averaging trigger function is enabled.

            Parameter:
                None

            Return:
                bool: True if enabled, False otherwise
            """
            return bool(int(self.instrument.query(":TRIG:SEQ:AVER?")))

    class External:
        """
        External trigger settings.
        """
        def __init__(self, instrument):
            self.instrument = instrument

        # TRIGger[:SEQuence]:EXTernal:DELay <time>
        def set_delay(self, delay: float):
            """
            Sets the response delay to the external trigger.

            Parameter:
                delay (float): Delay value from 0 to 100 sec.

            Return:
                None
            """
            delay = max(0, min(100, delay))
            self.instrument.write(f":TRIG:SEQ:EXT:DEL {delay}")

        # TRIGger[:SEQuence]:EXTernal:DELay?
        def get_delay(self) -> float:
            """
            Reads out the response delay to the external trigger.

            Parameter:
                None

            Return:
                float: Delay value in seconds
            """
            return float(self.instrument.query(":TRIG:SEQ:EXT:DEL?"))

        # TRIGger[:SEQuence]:EXTernal:SLOPe <char>
        def set_slope(self, slope: str):
            """
            Sets the polarity of the external trigger.

            Parameter:
                slope (str): 'POSitive' or 'NEGative'

            Return:
                None
            """
            allowed = ['POSitive', 'NEGative']
            if slope not in allowed:
                raise ValueError("slope must be 'POSitive' or 'NEGative'")
            self.instrument.write(f":TRIG:SEQ:EXT:SLOP {slope}")

        # TRIGger[:SEQuence]:EXTernal:SLOPe?
        def get_slope(self) -> str:
            """
            Reads out the polarity of the external trigger.

            Parameter:
                None

            Return:
                str: 'POS' or 'NEG'
            """
            return self.instrument.query(":TRIG:SEQ:EXT:SLOP?").strip()
        # TRIGger[:SEQuence]:EXTernal:POSition <char>
        def set_position(self, position: str):
            """
            Sets the position of the external trigger.

            Parameter:
                position (str): 'BSAM' (Before sampling) or 'BSET' (Before frequency setup)

            Return:
                None
            """
            allowed = ['BSAM', 'BSET']
            if position not in allowed:
                raise ValueError("position must be 'BSAM' or 'BSET'")
            self.instrument.write(f":TRIG:SEQ:EXT:POS {position}")

        # TRIGger[:SEQuence]:EXTernal:POSition?
        def get_position(self) -> str:
            """
            Reads out the position of the external trigger.

            Parameter:
                None

            Return:
                str: 'BSAM' or 'BSET'
            """
            return self.instrument.query(":TRIG:SEQ:EXT:POS?").strip()

    class Output:
        """
        Trigger output settings.
        """
        def __init__(self, instrument):
            self.instrument = instrument

        # TRIGger:OUTPut:FUNCtion <char>
        def set_function(self, function: str):
            """
            Sets the trigger output function.

            Parameter:
                function (str): One of ['BSET', 'BSAM', 'ASAM', 'RTRG', 'ESWP', 'MEAS']

            Return:
                None
            """
            allowed = ['BSET', 'BSAM', 'ASAM', 'RTRG', 'ESWP', 'MEAS']
            if function not in allowed:
                raise ValueError(f"function must be one of {allowed}")
            self.instrument.write(f":TRIG:OUTP:FUNC {function}")

        # TRIGger:OUTPut:FUNCtion?
        def get_function(self) -> str:
            """
            Reads out the trigger output function.

            Parameter:
                None

            Return:
                str: Output function ('BSET', 'BSAM', 'ASAM', 'RTRG', 'ESWP', 'MEAS')
            """
            return self.instrument.query(":TRIG:OUTP:FUNC?").strip()

        # TRIGger:OUTPut:POLarity <char>
        def set_polarity(self, polarity: str):
            """
            Sets the polarity of the trigger output.

            Parameter:
                polarity (str): 'POSitive' or 'NEGative'

            Return:
                None
            """
            allowed = ['POSitive', 'NEGative']
            if polarity not in allowed:
                raise ValueError("polarity must be 'POSitive' or 'NEGative'")
            self.instrument.write(f":TRIG:OUTP:POL {polarity}")

        # TRIGger:OUTPut:POLarity?
        def get_polarity(self) -> str:
            """
            Reads out the polarity of the trigger output.

            Parameter:
                None

            Return:
                str: 'POS' or 'NEG'
            """
            return self.instrument.query(":TRIG:OUTP:POL?").strip()

        # TRIGger:OUTPut:STATe {OFF|ON|0|1}
        def enable_output(self, enable: bool):
            """
            Turns the trigger output ON/OFF.

            Parameter:
                enable (bool): True to enable, False to disable

            Return:
                None
            """
            self.instrument.write(f":TRIG:OUTP:STAT {1 if enable else 0}")

        # TRIGger:OUTPut:STATe?
        def is_output_enabled(self) -> bool:
            """
            Query if the trigger output is ON/OFF.

            Parameter:
                None

            Return:
                bool: True if ON, False if OFF
            """
            return bool(int(self.instrument.query(":TRIG:OUTP:STAT?")))

    class Point:
        """
        Point trigger feature settings.
        """
        def __init__(self, instrument):
            self.instrument = instrument

        # TRIGger[:SEQuence]:POINt {OFF|ON|0|1}
        def enable_point_trigger(self, enable: bool):
            """
            Turns the point trigger feature ON/OFF.

            Parameter:
                enable (bool): True to enable, False to disable

            Return:
                None
            """
            self.instrument.write(f":TRIG:SEQ:POIN {1 if enable else 0}")

        # TRIGger[:SEQuence]:POINt?
        def is_point_trigger_enabled(self) -> bool:
            """
            Query if the point trigger feature is ON/OFF.

            Parameter:
                None

            Return:
                bool: True if ON, False if OFF
            """
            return bool(int(self.instrument.query(":TRIG:SEQ:POIN?")))
    # TRIGger[:SEQuence]:SINGle
    def sequence_single(self):
        """
        Generates a trigger signal and initiates a sweep if the trigger source is set to BUS and analyzer is in trigger waiting state.

        Parameter:
            None

        Return:
            None
        """
        self.instrument.write(":TRIG:SEQ:SING")

    # TRIGger[:SEQuence]:SCOPe <char>
    def set_scope(self, scope: str):
        """
        Sets the trigger scope.

        Parameter:
            scope (str): 'ALL' or 'ACTive'

        Return:
            None
        """
        allowed = ['ALL', 'ACTive']
        if scope not in allowed:
            raise ValueError("scope must be 'ALL' or 'ACTive'")
        self.instrument.write(f":TRIG:SEQ:SCOP {scope}")

    # TRIGger[:SEQuence]:SCOPe?
    def get_scope(self) -> str:
        """
        Reads out the trigger scope.

        Parameter:
            None

        Return:
            str: 'ALL' or 'ACT'
        """
        return self.instrument.query(":TRIG:SEQ:SCOP?").strip()

    # TRIGger[:SEQuence]:SOURce <char>
    def set_source(self, source: str):
        """
        Selects the trigger source.

        Parameter:
            source (str): 'INTernal', 'EXTernal', 'MANual', or 'BUS'

        Return:
            None
        """
        allowed = ['INTernal', 'EXTernal', 'MANual', 'BUS']
        if source not in allowed:
            raise ValueError("source must be one of ['INTernal', 'EXTernal', 'MANual', 'BUS']")
        self.instrument.write(f":TRIG:SEQ:SOUR {source}")

    # TRIGger[:SEQuence]:SOURce?
    def get_source(self) -> str:
        """
        Reads out the trigger source.

        Parameter:
            None

        Return:
            str: 'INT', 'EXT', 'MAN', or 'BUS'
        """
        return self.instrument.query(":TRIG:SEQ:SOUR?").strip()

    # TRIGger[:SEQuence]:STATus?
    def get_status(self) -> str:
        """
        Reads out the current state of the Analyzer trigger system.

        Parameter:
            None

        Return:
            str: 'HOLD', 'MEAS', 'WAIT'
        """
        return self.instrument.query(":TRIG:SEQ:STAT?").strip()

    # TRIGger[:SEQuence]:WAIT <char>
    def wait_for_state(self, state: str):
        """
        Delays execution until the specified state of the analyzer trigger system is reached.

        Parameter:
            state (str): 'HOLD', 'MEASure', 'WTRG', or 'ENDM'

        Return:
            None
        """
        allowed = ['HOLD', 'MEASure', 'WTRG', 'ENDM']
        if state not in allowed:
            raise ValueError("state must be one of ['HOLD', 'MEASure', 'WTRG', 'ENDM']")
        self.instrument.write(f":TRIG:SEQ:WAIT {state}")