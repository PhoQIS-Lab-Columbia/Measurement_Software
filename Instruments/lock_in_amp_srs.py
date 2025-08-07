from Instruments import Instrument
from EInstrument import EInstrument
import pyvisa
import re
from EFileType import EFileType
class LockInAmp(Instrument.Instrument):
    """“NV” nanoVolts “HZ” Hertz “UDEG” microDegrees
“UV” microVolts “KHZ” kiloHertz “MDEG” milliDegrees
“MV” milliVolts “MHZ” megaHertz “DEG” Degrees
“V” Volts"""
    def __init__(self, instrument, name, save_files_path=None):
        super().__init__(instrument, EInstrument.Name, save_files_path)
        self.reference = Reference(instrument, self.data_handler)
        self.signal = Signal(instrument, self.data_handler)
        self.channel1 = Channel(instrument, self.data_handler, 1)
        self.channel2 = Channel(instrument, self.data_handler, 2)
        self.aux = Aux(instrument, self.data_handler)
        self.display = Display(instrument, self.data_handler)
        self.scan = Scan(instrument, self.data_handler)
        self.data = Data(instrument, self.data_handler)
        self.system = System(instrument, self.data_handler)
        #Class objects
    def auto_range(self):
        """
        Performs the Auto Range function (same as pressing [Auto Range])  The outputs may take many time constants to return to
their steady state values.
        """
        self.instrument.write("ARNG")

    def auto_scale(self):
        """
        Performs the Auto Scale function (same as pressing [Auto Scale]).This automatically sets the sensitivity. Measurements with
the synchronous filter on or measurements of Xnoise or Ynoise may take many time
constants to return to their steady state values.
        """
        self.instrument.write("ASCL")
    #TODO: Add SCPI functions below
class Reference:
    """Commands for reference channel control."""
    def __init__(self, instrument, data_handler):
        self.instrument = instrument
        self.data_handler = data_handler
        self.time_base = self.TimeBase(instrument, data_handler)
        self.phase = self.Phase(instrument, data_handler)
        self.frequency = self.Frequency(instrument, data_handler)
        self.harmonics = self.Harmonics(instrument, data_handler)
        self.sr540 = self.SR540(instrument, data_handler)
        self.sine = self.Sine(instrument, data_handler)
        self.source = self.Source(instrument, data_handler)
        self.trigger = self.Trigger(instrument, data_handler)
    
    class TimeBase:
        """Commands which modify the time base settings."""
        def __init__(self, instrument, data_handler):
            self.instrument = instrument
            self.data_handler = data_handler
        
        def set_timebase_mode(self, mode):
            """
            Sets the external 10 MHz timebase mode.
            mode: 'AUTO', 'INTERNAL', 0, or 1
            """
            if isinstance(mode, str):
                mode = mode.upper()
                if mode == "AUTO":
                    cmd = "TBMODE AUTO"
                elif mode == "INTERNAL":
                    cmd = "TBMODE INTERNAL"
                else:
                    raise ValueError("Invalid string mode. Use 'AUTO' or 'INTERNAL'.")
            elif mode in [0, 1]:
                cmd = f"TBMODE {mode}"
            else:
                raise ValueError("Mode must be 'AUTO', 'INTERNAL', 0, or 1.")
            self.instrument.write(cmd)
            

        def get_timebase_mode(self):
            """
            Returns the timebase mode (0 for auto, 1 for internal).
            """
            cmd = "TBMODE?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return int(response)

        def get_timebase_status(self):
            """
            Returns the current 10 MHz timebase source (0 for external, 1 for internal).
            """
            cmd = "TBSTAT?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return int(response)
        # Define methods for TimeBase functionality here
        # For example, setting time base, getting time base, etc.
        pass
    class Phase:
        """Phase related commands"""
        def __init__(self, instrument, data_handler):
            self.instrument = instrument
            self.data_handler = data_handler

        def set_phase(self, value, unit="DEG"):
            """
            Sets the reference phase shift.
            value: float, phase value
            unit: str, one of 'UDEG', 'MDEG', 'DEG', 'URAD', 'MRAD', 'RAD'
            """
            valid_units = ["UDEG", "MDEG", "DEG", "URAD", "MRAD", "RAD"]
            if unit.upper() not in valid_units:
                raise ValueError(f"Invalid unit. Choose from {valid_units}.")
            cmd = f"PHAS {value} {unit.upper()}"
            self.instrument.write(cmd)
            

        def get_phase(self):
            """
            Queries the reference phase in degrees.
            Returns: float
            """
            cmd = "PHAS?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return float(response)

        def auto_phase(self):
            """
            Performs the Auto Phase function (same as pressing [Auto Phase]) *WARNING* Do not spam this function. Allow for calibration to finsih before pressing again.
            """
            cmd = "APHS"
            self.instrument.write(cmd)
            
    class Frequency:
        """Frequency controls and readings."""
        def __init__(self, instrument, data_handler):
            self.instrument = instrument
            self.data_handler = data_handler

        def set_frequency(self, f, unit="HZ"):
            """
            Sets the internal frequency.
            f: float, frequency value (1e-3 Hz ≤ f ≤ 5e5 Hz)
            unit: str, one of 'HZ', 'KHZ', 'MHZ'
            """
            valid_units = ["HZ", "KHZ", "MHZ"]
            if unit.upper() not in valid_units:
                raise ValueError(f"Invalid unit. Choose from {valid_units}.")
            if not (1e-3 <= float(f) <= 5e5):
                raise ValueError("Frequency must be between 1 mHz and 500 kHz.")
            cmd = f"FREQ {f} {unit.upper()}"
            self.instrument.write(cmd)
            

        def get_frequency(self):
            """
            Queries the reference frequency (internal or external depending on mode).
            Returns: float (Hz)
            """
            cmd = "FREQ?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return float(response)

        def set_internal_frequency(self, f, unit="HZ"):
            """
            Sets the internal reference frequency.
            f: float, frequency value (1e-3 Hz ≤ f ≤ 5e5 Hz)
            unit: str, one of 'HZ', 'KHZ', 'MHZ'
            """
            valid_units = ["HZ", "KHZ", "MHZ"]
            if unit.upper() not in valid_units:
                raise ValueError(f"Invalid unit. Choose from {valid_units}.")
            if not (1e-3 <= float(f) <= 5e5):
                raise ValueError("Frequency must be between 1 mHz and 500 kHz.")
            cmd = f"FREQINT {f} {unit.upper()}"
            self.instrument.write(cmd)
            

        def get_internal_frequency(self):
            """
            Queries the internal reference frequency.
            Returns: float (Hz)
            """
            cmd = "FREQINT?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return float(response)

        def get_external_frequency(self):
            """
            Queries the external reference frequency.
            Returns: float (Hz)
            """
            cmd = "FREQEXT?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return float(response)

        def get_detection_frequency(self):
            """
            Queries the actual detection frequency.
            Returns: float (Hz)
            """
            cmd = "FREQDET?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return float(response)
        
        def set_preset(self, j, f, unit="HZ"):
            """
            Sets a frequency preset.
            j: int, preset index (0-3)
            f: float, frequency value (1e-3 Hz ≤ f ≤ 5e5 Hz)
            unit: str, one of 'HZ', 'KHZ', 'MHZ'
            """
            valid_units = ["HZ", "KHZ", "MHZ"]
            if not (0 <= int(j) <= 3):
                raise ValueError("Preset index j must be between 0 and 3.")
            if unit.upper() not in valid_units:
                raise ValueError(f"Invalid unit. Choose from {valid_units}.")
            if not (1e-3 <= float(f) <= 5e5):
                raise ValueError("Frequency must be between 1 mHz and 500 kHz.")
            cmd = f"PSTF {int(j)}, {float(f)} {unit.upper()}"
            self.instrument.write(cmd)
            

        def get_preset(self, j):
            """
            Queries a frequency preset.
            j: int, preset index (0-3)
            Returns: float (Hz)
            """
            if not (0 <= int(j) <= 3):
                raise ValueError("Preset index j must be between 0 and 3.")
            cmd = f"PSTF? {int(j)}"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return float(response)
    class Harmonics:
        def __init__(self, instrument, data_handler):
            self.instrument = instrument
            self.data_handler = data_handler

        def set_harmonic(self, i):
            """
            Sets the lock-in to detect at the ith harmonic of the reference frequency.
            i: int, 1 ≤ i ≤ 99
            """
            if not (1 <= int(i) <= 99):
                raise ValueError("Harmonic number must be between 1 and 99.")
            cmd = f"HARM {int(i)}"
            self.instrument.write(cmd)
            

        def get_harmonic(self):
            """
            Returns the harmonic number i.
            Returns: int
            """
            cmd = "HARM?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return int(response)

        def set_dual_harmonic(self, i):
            """
            Sets the lock-in to detect at the ith harmonic of the external frequency in dual reference mode.
            i: int, 1 ≤ i ≤ 99
            """
            if not (1 <= int(i) <= 99):
                raise ValueError("Dual harmonic number must be between 1 and 99.")
            cmd = f"HARMDUAL {int(i)}"
            self.instrument.write(cmd)
            

        def get_dual_harmonic(self):
            """
            Returns the dual external harmonic number i.
            Returns: int
            """
            cmd = "HARMDUAL?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return int(response)
    class SR540:
        """Class to configure amplifier to work with an external SR540 chopper"""
        def __init__(self, instrument, data_handler):
            self.instrument = instrument
            self.data_handler = data_handler

        def set_blade_slots(self, slots):
            """
            Configures the lock-in for operation with an external SR540 chopper.
            slots: 'SLT6', 'SLT30', 0, or 1
            """
            if isinstance(slots, str):
                slots = slots.upper()
                if slots == "SLT6":
                    cmd = "BLADESLOTS SLT6"
                elif slots == "SLT30":
                    cmd = "BLADESLOTS SLT30"
                else:
                    raise ValueError("Invalid string slots. Use 'SLT6' or 'SLT30'.")
            elif slots in [0, 1]:
                cmd = f"BLADESLOTS {slots}"
            else:
                raise ValueError("Slots must be 'SLT6', 'SLT30', 0, or 1.")
            self.instrument.write(cmd)
            

        def get_blade_slots(self):
            """
            Returns the chopper blade configuration.
            Returns: int (0 for 6-slot, 1 for 30-slot)
            """
            cmd = "BLADESLOTS?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return int(response)

        def set_blade_phase(self, phase, unit="DEG"):
            """
            Sets the phase of the SR540 chopper blade.
            phase: float, phase value
            unit: str, one of 'UDEG', 'MDEG', 'DEG', 'URAD', 'MRAD', 'RAD'
            """
            valid_units = ["UDEG", "MDEG", "DEG", "URAD", "MRAD", "RAD"]
            if unit.upper() not in valid_units:
                raise ValueError(f"Invalid unit. Choose from {valid_units}.")
            cmd = f"BLADEPHASE {phase} {unit.upper()}"
            self.instrument.write(cmd)
            

        def get_blade_phase(self):
            """
            Queries the phase of the SR540 chopper blade.
            Returns: float
            """
            cmd = "BLADEPHASE?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return float(response)
    class Sine:
        """Commands to control sine out."""

        def __init__(self, instrument, data_handler):
            self.instrument = instrument
            self.data_handler = data_handler

        def set_amplitude(self, v, unit="V"):
            """
            Sets the sine out amplitude.
            v: float, amplitude value (1 nV to 2.0 V)
            unit: str, one of 'NV', 'UV', 'MV', 'V'
            """
            valid_units = ["NV", "UV", "MV", "V"]
            if unit.upper() not in valid_units:
                raise ValueError(f"Invalid unit. Choose from {valid_units}.")
            if not (1e-9 <= float(v) <= 2.0):
                raise ValueError("Amplitude must be between 1 nV and 2.0 V.")
            cmd = f"SLVL {v} {unit.upper()}"
            self.instrument.write(cmd)
            

        def get_amplitude(self):
            """
            Queries the sine out amplitude in Volts.
            Returns: float
            """
            cmd = "SLVL?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return float(response)

        def set_dc_level(self, v, unit="V"):
            """
            Sets the sine out DC level.
            v: float, level value (-5.00 V to +5.00 V)
            unit: str, one of 'NV', 'UV', 'MV', 'V'
            """
            valid_units = ["NV", "UV", "MV", "V"]
            if unit.upper() not in valid_units:
                raise ValueError(f"Invalid unit. Choose from {valid_units}.")
            if not (-5.0 <= float(v) <= 5.0):
                raise ValueError("DC level must be between -5.00 V and +5.00 V.")
            cmd = f"SOFF {v} {unit.upper()}"
            self.instrument.write(cmd)
            

        def get_dc_level(self):
            """
            Queries the sine out DC level in Volts.
            Returns: float
            """
            cmd = "SOFF?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return float(response)

        def set_dc_mode(self, mode):
            """
            Sets the sine out DC mode.
            mode: 'COMMON', 'DIFFERENCE', 0, or 1
            """
            if isinstance(mode, str):
                mode = mode.upper()
                if mode in ["COMMON", "COM"]:
                    cmd = "REFM COMMON"
                elif mode in ["DIFFERENCE", "DIF"]:
                    cmd = "REFM DIFFERENCE"
                else:
                    raise ValueError("Invalid string mode. Use 'COMMON' or 'DIFFERENCE'.")
            elif mode in [0, 1]:
                cmd = f"REFM {mode}"
            else:
                raise ValueError("Mode must be 'COMMON', 'DIFFERENCE', 0, or 1.")
            self.instrument.write(cmd)
            

        def get_dc_mode(self):
            """
            Queries the sine out DC mode.
            Returns: int (0 for common, 1 for difference)
            """
            cmd = "REFM?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return int(response)
        
        

        def set_amplitude_preset(self, j, v, unit="V"):
            """
            Sets a sine out amplitude preset.
            j: int, preset index (0-3)
            v: float, amplitude value (1e-9 V ≤ v ≤ 2.0 V)
            unit: str, one of 'NV', 'UV', 'MV', 'V'
            """
            valid_units = ["NV", "UV", "MV", "V"]
            if not (0 <= int(j) <= 3):
                raise ValueError("Preset index j must be between 0 and 3.")
            if unit.upper() not in valid_units:
                raise ValueError(f"Invalid unit. Choose from {valid_units}.")
            if not (1e-9 <= float(v) <= 2.0):
                raise ValueError("Amplitude must be between 1 nV and 2.0 V.")
            cmd = f"PSTA {int(j)}, {float(v)} {unit.upper()}"
            self.instrument.write(cmd)
            

        def get_amplitude_preset(self, j):
            """
            Queries a sine out amplitude preset.
            j: int, preset index (0-3)
            Returns: float (Volts)
            """
            if not (0 <= int(j) <= 3):
                raise ValueError("Preset index j must be between 0 and 3.")
            cmd = f"PSTA? {int(j)}"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return float(response)

        def set_dc_level_preset(self, j, v, unit="V"):
            """
            Sets a sine out DC level preset.
            j: int, preset index (0-3)
            v: float, DC level value (-5.0 V ≤ v ≤ 5.0 V)
            unit: str, one of 'NV', 'UV', 'MV', 'V'
            """
            valid_units = ["NV", "UV", "MV", "V"]
            if not (0 <= int(j) <= 3):
                raise ValueError("Preset index j must be between 0 and 3.")
            if unit.upper() not in valid_units:
                raise ValueError(f"Invalid unit. Choose from {valid_units}.")
            if not (-5.0 <= float(v) <= 5.0):
                raise ValueError("DC level must be between -5.00 V and +5.00 V.")
            cmd = f"PSTL {int(j)}, {float(v)} {unit.upper()}"
            self.instrument.write(cmd)
            

        def get_dc_level_preset(self, j):
            """
            Queries a sine out DC level preset.
            j: int, preset index (0-3)
            Returns: float (Volts)
            """
            if not (0 <= int(j) <= 3):
                raise ValueError("Preset index j must be between 0 and 3.")
            cmd = f"PSTL? {int(j)}"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return float(response)
        
    class Source:
        """Commands to control the internal/external reference source."""
        def __init__(self, instrument, data_handler):
            self.instrument = instrument
            self.data_handler = data_handler

        def set_source(self, source):
            """
            Sets the reference source.
            source: 'INT', 'EXT', 'DUAL', 'CHOP', or integer 0-3
            """
            if isinstance(source, str):
                source = source.upper()
                if source == "INT":
                    cmd = "RSRC INT"
                elif source == "EXT":
                    cmd = "RSRC EXT"
                elif source == "DUAL":
                    cmd = "RSRC DUAL"
                elif source == "CHOP":
                    cmd = "RSRC CHOP"
                else:
                    raise ValueError("Invalid string source. Use 'INT', 'EXT', 'DUAL', or 'CHOP'.")
            elif source in [0, 1, 2, 3]:
                cmd = f"RSRC {source}"
            else:
                raise ValueError("Source must be 'INT', 'EXT', 'DUAL', 'CHOP', or integer 0-3.")
            self.instrument.write(cmd)
            

        def get_reference_source(self):
            """
            Queries the reference source.
            Returns: int (0 for INT, 1 for EXT, 2 for DUAL, 3 for CHOP)
            """
            cmd = "RSRC?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return int(response)
    class Trigger:
        """Commands to control the trigger settings."""
        def __init__(self, instrument, data_handler):
            self.instrument = instrument
            self.data_handler = data_handler

        def set_trigger_mode(self, mode):
            """
            Sets the external reference trigger mode.
            mode: 'SIN', 'POSTTL', 'NEGTTL', or integer 0-2
            """
            if isinstance(mode, str):
                mode = mode.upper()
                if mode == "SIN":
                    cmd = "RTRG SIN"
                elif mode in ["POSTTL", "POS"]:
                    cmd = "RTRG POSTTL"
                elif mode == "NEGTTL":
                    cmd = "RTRG NEGTTL"
                else:
                    raise ValueError("Invalid string mode. Use 'SIN', 'POSTTL', or 'NEGTTL'.")
            elif mode in [0, 1, 2]:
                cmd = f"RTRG {mode}"
            else:
                raise ValueError("Mode must be 'SIN', 'POSTTL', 'NEGTTL', or integer 0-2.")
            self.instrument.write(cmd)
            

        def get_trigger_mode(self):
            """
            Queries the external reference trigger mode.
            Returns: int (0 for SIN, 1 for POSTTL, 2 for NEGTTL)
            """
            cmd = "RTRG?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return int(response)

        def set_impedance(self, impedance):
            """
            Sets the external reference trigger input impedance.
            impedance: '50OHMS', '1MEG', or integer 0-1
            """
            if isinstance(impedance, str):
                imp = impedance.upper()
                if imp in ["50OHMS", "50"]:
                    cmd = "REFZ 50OHMS"
                elif imp in ["1MEG", "1M"]:
                    cmd = "REFZ 1MEG"
                else:
                    raise ValueError("Invalid string impedance. Use '50OHMS' or '1MEG'.")
            elif impedance in [0, 1]:
                cmd = f"REFZ {impedance}"
            else:
                raise ValueError("Impedance must be '50OHMS', '1MEG', or integer 0-1.")
            self.instrument.write(cmd)
            

        def get_impedance(self):
            """
            Queries the external reference input impedance.
            Returns: int (0 for 50Ω, 1 for 1MΩ)
            """
            cmd = "REFZ?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return int(response)
class Signal:
    """Commands for signal channel control."""
    def __init__(self, instrument, data_handler):
        self.instrument = instrument
        self.data_handler = data_handler
        self.voltage = self.Voltage(instrument, data_handler)
        self.current = self.Current(instrument, data_handler)
        self.filter = self.Filter(instrument, data_handler)
    def set_signal_source(self, source):
        """
        Sets the signal source to either voltage or current.
        source: Voltage: 'VOLT', 'VOLTAGE', 0 Current:'CURR', 'CURRENT', 1
        """
        if isinstance(source, str):
            source = source.upper()
            if source in ["VOLT", "VOLTAGE"]:
                cmd = "IVMD VOLTAGE"
            elif source in ["CURR", "CURRENT"]:
                cmd = "IVMD CURRENT"
            else:
                raise ValueError("Invalid string source. Use 'VOLTAGE' or 'CURRENT'.")
        elif source in [0, 1]:
            cmd = f"IVMD {source}"
        else:
            raise ValueError("Source must be 'VOLTAGE', 'CURRENT', 0, or 1.")
        self.instrument.write(cmd)
        

    def get_input_mode(self):
        """
        Queries the signal input mode.
        Returns: int (0 for voltage, 1 for current)
        """
        cmd = "IVMD?"
        response = self.instrument.query(cmd)
        self.data_handler.log_command(cmd, response)
        return int(response)
    
    def get_signal_strength(self):
        """
        Queries the signal strength indicator.
        Returns: int (0 = lowest, 4 = overload)
        """
        cmd = "ILVL?"
        response = self.instrument.query(cmd)
        self.data_handler.log_command(cmd, response)
        return int(response)

    def set_sensitivity(self, i):
        """
        Sets the sensitivity according to the sensitivity table.
        i: int, 0-27
        """
        if not (0 <= int(i) <= 27):
            raise ValueError("Sensitivity index i must be between 0 and 27.")
        cmd = f"SCAL {int(i)}"
        self.instrument.write(cmd)
        
    def print_sensitivity_table(self):
        """
        Prints the sensitivity table for reference.
        """
        sensitivity_table = [
            "0: 1 V [μA]",
            "1: 500 mV [nA]",
            "2: 200 mV [nA]",
            "3: 100 mV [nA]",
            "4: 50 mV [nA]",
            "5: 20 mV [nA]",
            "6: 10 mV [nA]",
            "7: 5 mV [nA]",
            "8: 2 mV [nA]",
            "9: 1 mV [nA]",
            "10: 500 μV [pA]",
            "11: 200 μV [pA]",
            "12: 100 μV [pA]",
            "13: 50 μV [pA]",
            "14: 20 μV [pA]",
            "15: 10 μV [pA]",
            "16: 5 μV [pA]",
            "17: 2 μV [pA]",
            "18: 1 μV [pA]",
            "19: 500 nV [fA]",
            "20: 200 nV [fA]",
            "21: 100 nV [fA]",
            "22: 50 nV [fA]",
            "23: 20 nV [fA]",
            "24: 10 nV [fA]",
            "25: 5 nV [fA]",
            "26: 2 nV [fA]",
            "27: 1 nV [fA]",
        ]
        print("Sensitivity Table:")
        for entry in sensitivity_table:
            print(entry)
    def get_sensitivity(self):
        """
        Queries the sensitivity index.
        Returns: int (0-27)
        """
        cmd = "SCAL?"
        response = self.instrument.query(cmd)
        self.data_handler.log_command(cmd, response)
        return int(response)
    def set_time_constant(self, i):
        """
        Sets the time constant according to the table.
        i: int, 0-21
        """
        if not (0 <= int(i) <= 21):
            raise ValueError("Time constant index i must be between 0 and 21.")
        cmd = f"OFLT {int(i)}"
        self.instrument.write(cmd)
        

    def get_time_constant(self):
        """
        Queries the time constant index.
        Returns: int (0-21)
        """
        cmd = "OFLT?"
        response = self.instrument.query(cmd)
        self.data_handler.log_command(cmd, response)
        return int(response)
    def print_time_constant_table(self):
        """
        Prints the time constant table for reference.
        """
        time_constant_table = [
            "0: 1 μs",
            "1: 3 μs",
            "2: 10 μs",
            "3: 30 μs",
            "4: 100 μs",
            "5: 300 μs",
            "6: 1 ms",
            "7: 3 ms",
            "8: 10 ms",
            "9: 30 ms",
            "10: 100 ms",
            "11: 300 ms",
            "12: 1 s",
            "13: 3 s",
            "14: 10 s",
            "15: 30 s",
            "16: 100 s",
            "17: 300 s",
            "18: 1 ks",
            "19: 3 ks",
            "20: 10 ks",
            "21: 30 ks",
        ]
        print("Time Constant Table:")
        for entry in time_constant_table:
            print(entry)
    class Voltage:
        """Commands to control the signal voltage settings."""
        def __init__(self, instrument, data_handler):
            self.instrument = instrument
            self.data_handler = data_handler
        def set_input_source(self, source):
            """
            Sets the voltage input mode to A (i=0) or A−B (i=1).
            source: 'A', 'A-B', 0, or 1
            """
            if isinstance(source, str):
                src = source.upper().replace("-", "")
                if src == "A":
                    cmd = "ISRC A"
                elif src in ["AB", "A−B"]:
                    cmd = "ISRC A-B"
                else:
                    raise ValueError("Invalid string source. Use 'A' or 'A-B'.")
            elif source in [0, 1]:
                cmd = f"ISRC {source}"
            else:
                raise ValueError("Source must be 'A', 'A-B', 0, or 1.")
            self.instrument.write(cmd)
            

        def get_input_source(self):
            """
            Queries the voltage input mode.
            Returns: int (0 for A, 1 for A−B)
            """
            cmd = "ISRC?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return int(response)

        def set_coupling(self, coupling):
            """
            Sets the voltage input coupling to ac (i=0) or dc (i=1).
            coupling: 'AC', 'DC', 0, or 1
            """
            if isinstance(coupling, str):
                coup = coupling.upper()
                if coup == "AC":
                    cmd = "ICPL AC"
                elif coup == "DC":
                    cmd = "ICPL DC"
                else:
                    raise ValueError("Invalid string coupling. Use 'AC' or 'DC'.")
            elif coupling in [0, 1]:
                cmd = f"ICPL {coupling}"
            else:
                raise ValueError("Coupling must be 'AC', 'DC', 0, or 1.")
            self.instrument.write(cmd)
            

        def get_coupling(self):
            """
            Queries the voltage input coupling mode.
            Returns: int (0 for AC, 1 for DC)
            """
            cmd = "ICPL?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return int(response)

        def set_grounding(self, grounding):
            """
            Sets the voltage input shields to float (i=0) or ground (i=1).
            grounding: 'FLOAT', 'GROUND', 0, or 1
            """
            if isinstance(grounding, str):
                grd = grounding.upper()
                if grd in ["FLOAT", "FLO"]:
                    cmd = "IGND FLOAT"
                elif grd == "GROUND":
                    cmd = "IGND GROUND"
                else:
                    raise ValueError("Invalid string grounding. Use 'FLOAT' or 'GROUND'.")
            elif grounding in [0, 1]:
                cmd = f"IGND {grounding}"
            else:
                raise ValueError("Grounding must be 'FLOAT', 'GROUND', 0, or 1.")
            self.instrument.write(cmd)
            

        def get_grounding(self):
            """
            Queries the voltage input grounding mode.
            Returns: int (0 for float, 1 for ground)
            """
            cmd = "IGND?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return int(response)

        def set_range(self, rng):
            """
            Sets the voltage input range.
            rng: '1V', '1VOLT', '300MV', '300MVOLT', '100MV', '100MVOLT', '30MV', '30MVOLT', '10MV', '10MVOLT', 0-4
            """
            if isinstance(rng, str):
                r = rng.upper().replace(" ", "")
                if r in ["1V", "1VOLT"]:
                    cmd = "IRNG 1VOLT"
                elif r in ["300MV", "300MVOLT"]:
                    cmd = "IRNG 300MVOLT"
                elif r in ["100MV", "100MVOLT"]:
                    cmd = "IRNG 100MVOLT"
                elif r in ["30MV", "30MVOLT"]:
                    cmd = "IRNG 30MVOLT"
                elif r in ["10MV", "10MVOLT"]:
                    cmd = "IRNG 10MVOLT"
                else:
                    raise ValueError("Invalid string range. Use one of '1V', '300MV', '100MV', '30MV', '10MV'.")
            elif rng in [0, 1, 2, 3, 4]:
                cmd = f"IRNG {rng}"
            else:
                raise ValueError("Range must be '1V', '300MV', '100MV', '30MV', '10MV', or integer 0-4.")
            self.instrument.write(cmd)
            

        def get_range(self):
            """
            Queries the voltage input range.
            Returns: int (0 for 1V, 1 for 300mV, 2 for 100mV, 3 for 30mV, 4 for 10mV)
            """
            cmd = "IRNG?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return int(response)
    class Current:
        """Commands to control the signal current settings."""
        def __init__(self, instrument, data_handler):
            self.instrument = instrument
            self.data_handler = data_handler
        
        def set_input_gain(self, gain):
            """
            Sets the current input gain.
            gain: '1MEG', '100MEG', 0, or 1
            """
            if isinstance(gain, str):
                g = gain.upper()
                if g == "1MEG":
                    cmd = "ICUR 1MEG"
                elif g == "100MEG":
                    cmd = "ICUR 100MEG"
                else:
                    raise ValueError("Invalid string gain. Use '1MEG' or '100MEG'.")
            elif gain in [0, 1]:
                cmd = f"ICUR {gain}"
            else:
                raise ValueError("Gain must be '1MEG', '100MEG', 0, or 1.")
            self.instrument.write(cmd)
            

        def get_input_gain(self):
            """
            Queries the current input gain.
            Returns: int (0 for 1MEG, 1 for 100MEG)
            """
            cmd = "ICUR?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return int(response)
    class Filter:
        def __init__(self, instrument, data_handler):
            self.instrument = instrument
            self.data_handler = data_handler
        def set_dual_ref_sync(self, mode):
            """
            Configures the Sync filter in Dual Reference mode.
            mode: 'DIFF', 'INT', 0, or 1
            """
            if isinstance(mode, str):
                m = mode.upper()
                if m == "DIFF":
                    cmd = "DUALREFSYNC DIFF"
                elif m == "INT":
                    cmd = "DUALREFSYNC INT"
                else:
                    raise ValueError("Invalid string mode. Use 'DIFF' or 'INT'.")
            elif mode in [0, 1]:
                cmd = f"DUALREFSYNC {mode}"
            else:
                raise ValueError("Mode must be 'DIFF', 'INT', 0, or 1.")
            self.instrument.write(cmd)
            

        def get_dual_ref_sync(self):
            """
            Queries the Sync filter mode in Dual Reference mode.
            Returns: int (0 for DIFF, 1 for INT)
            """
            cmd = "DUALREFSYNC?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return int(response)
        
        def set_slope(self, i):
            """
            Sets the filter slope.
            i: int, 0 (6 dB/oct), 1 (12 dB/oct), 2 (18 dB/oct), 3 (24 dB/oct)
            """
            if not (0 <= int(i) <= 3):
                raise ValueError("Filter slope index i must be between 0 and 3.")
            cmd = f"OFSL {int(i)}"
            self.instrument.write(cmd)
            

        def get_slope(self):
            """
            Queries the filter slope.
            Returns: int (0-3)
            """
            cmd = "OFSL?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return int(response)

        def set_sync_filter(self, state):
            """
            Sets the synchronous filter.
            state: 'OFF', 'ON', 0, or 1
            """
            if isinstance(state, str):
                s = state.upper()
                if s == "OFF":
                    cmd = "SYNC OFF"
                elif s == "ON":
                    cmd = "SYNC ON"
                else:
                    raise ValueError("Invalid string state. Use 'OFF' or 'ON'.")
            elif state in [0, 1]:
                cmd = f"SYNC {state}"
            else:
                raise ValueError("State must be 'OFF', 'ON', 0, or 1.")
            self.instrument.write(cmd)
            

        def get_sync_filter(self):
            """
            Queries the synchronous filter state.
            Returns: int (0 for OFF, 1 for ON)
            """
            cmd = "SYNC?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return int(response)

        def set_advanced_filter(self, state):
            """
            Sets the advanced filter.
            state: 'OFF', 'ON', 0, or 1
            """
            if isinstance(state, str):
                s = state.upper()
                if s == "OFF":
                    cmd = "ADVFILT OFF"
                elif s == "ON":
                    cmd = "ADVFILT ON"
                else:
                    raise ValueError("Invalid string state. Use 'OFF' or 'ON'.")
            elif state in [0, 1]:
                cmd = f"ADVFILT {state}"
            else:
                raise ValueError("State must be 'OFF', 'ON', 0, or 1.")
            self.instrument.write(cmd)
            

        def get_advanced_filter(self):
            """
            Queries the advanced filter state.
            Returns: int (0 for OFF, 1 for ON)
            """
            cmd = "ADVFILT?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return int(response)

        def get_equiv_noise_bandwidth(self):
            """
            Queries the equivalent noise bandwidth of the output filter, in hertz.
            Returns: float
            """
            cmd = "ENBW?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return float(response)
class Channel:
    """Commands to control the lock-in amplifier channel settings."""
    def __init__(self, instrument, data_handler, channel):
        self.instrument = instrument
        self.data_handler = data_handler
        self.channel = channel
        self.offset = self.Offset(instrument, data_handler, channel)
    def set_basis(self, basis):
        """
        Sets the output basis for the specified channel.
        basis: 'XY', 'RTHETA', 'RTH', 0, or 1
        """
    

        if isinstance(basis, str):
            b = basis.upper()
            if b in ["XY"]:
                basis_idx = 0
            elif b in ["RTHETA", "RTH"]:
                basis_idx = 1
            else:
                try:
                    basis_idx = int(b)
                except ValueError:
                    raise ValueError("Basis must be 'XY', 'RTHETA', 'RTH', or integer 0/1.")
        elif basis in [0, 1]:
            basis_idx = int(basis)
        else:
            raise ValueError("Basis must be 'XY', 'RTHETA', 'RTH', or integer 0/1.")

        cmd = f"COUT {str(self.channel)}, {basis_idx}"
        self.instrument.write(cmd)
    def set_expand(self, channel, mode):
            """
            Sets the output expand for X (0), Y (1), or R (2) to off (0), X10 (1), or X100 (2).
            channel: 'X', 'Y', 'R', or int 0-2
            mode: 'OFF', 'X10', 'X100', or int 0-2
            """
            if isinstance(channel, str):
                ch = channel.upper()
                if ch == "X":
                    j = 0
                elif ch == "Y":
                    j = 1
                elif ch == "R":
                    j = 2
                else:
                    raise ValueError("Channel must be 'X', 'Y', 'R', or integer 0-2.")
            elif channel in [0, 1, 2]:
                j = int(channel)
            else:
                raise ValueError("Channel must be 'X', 'Y', 'R', or integer 0-2.")

            if j == 3:
                raise ValueError("Setting expand for phase is not allowed.")

            if isinstance(mode, str):
                m = mode.upper()
                if m == "OFF":
                    i = 0
                elif m == "X10":
                    i = 1
                elif m == "X100":
                    i = 2
                else:
                    raise ValueError("Mode must be 'OFF', 'X10', 'X100', or integer 0-2.")
            elif mode in [0, 1, 2]:
                i = int(mode)
            else:
                raise ValueError("Mode must be 'OFF', 'X10', 'X100', or integer 0-2.")

            cmd = f"CEXP {j}, {i}"
            self.instrument.write(cmd)

    def get_expand(self, channel):
        """
        Returns the output expand mode for X (0), Y (1), or R (2).
        channel: 'X', 'Y', 'R', or int 0-2
        Returns: int (0 for off, 1 for X10, 2 for X100)
        """
        if isinstance(channel, str):
            ch = channel.upper()
            if ch == "X":
                j = 0
            elif ch == "Y":
                j = 1
            elif ch == "R":
                j = 2
            else:
                raise ValueError("Channel must be 'X', 'Y', 'R', or integer 0-2.")
        elif channel in [0, 1, 2]:
            j = int(channel)
        else:
            raise ValueError("Channel must be 'X', 'Y', 'R', or integer 0-2.")

        cmd = f"CEXP? {j}"
        response = self.instrument.query(cmd)
        self.data_handler.log_command(cmd, response)
        return int(response)
    def set_ratio_mode(self, channel, state):
        """
        Turns the ratio function for X (0), Y (1), or R (2) to off (0) or on (1).
        Setting a ratio for phase is not allowed.

        Formula for X and Y ratio output:
            Output = ((Input - Offset) / Sensitivity) × Expand × 10 × (AuxIn3 / 1.000 V)

        Formula for R ratio output:
            Output = ((Input - Offset) / Sensitivity) × Expand × 10 × (AuxIn4 / 1.000 V)

        channel: 'X', 'Y', 'R', or int 0-2
        state: 'OFF', 'ON', 0, or 1
        """
        if isinstance(channel, str):
            ch = channel.upper()
            if ch == "X":
                j = 0
            elif ch == "Y":
                j = 1
            elif ch == "R":
                j = 2
            else:
                raise ValueError("Channel must be 'X', 'Y', 'R', or integer 0-2.")
        elif channel in [0, 1, 2]:
            j = int(channel)
        else:
            raise ValueError("Channel must be 'X', 'Y', 'R', or integer 0-2.")

        if j == 3:
            raise ValueError("Setting ratio for phase is not allowed.")

        if isinstance(state, str):
            s = state.upper()
            if s == "OFF":
                i = 0
            elif s == "ON":
                i = 1
            else:
                raise ValueError("State must be 'OFF', 'ON', 0, or 1.")
        elif state in [0, 1]:
            i = int(state)
        else:
            raise ValueError("State must be 'OFF', 'ON', 0, or 1.")

        cmd = f"CRAT {j}, {i}"
        self.instrument.write(cmd)

    def get_ratio_mode(self, channel):
        """
        Returns the ratio mode for X (0), Y (1), or R (2).
        channel: 'X', 'Y', 'R', or int 0-2
        Returns: int (0 for off, 1 for on)
        """
        if isinstance(channel, str):
            ch = channel.upper()
            if ch == "X":
                j = 0
            elif ch == "Y":
                j = 1
            elif ch == "R":
                j = 2
            else:
                raise ValueError("Channel must be 'X', 'Y', 'R', or integer 0-2.")
        elif channel in [0, 1, 2]:
            j = int(channel)
        else:
            raise ValueError("Channel must be 'X', 'Y', 'R', or integer 0-2.")

        cmd = f"CRAT? {j}"
        response = self.instrument.query(cmd)
        self.data_handler.log_command(cmd, response)
        return int(response)
    class Offsets:
        """Commands to control the output settings of the lock-in amplifier."""
        def __init__(self, instrument, data_handler, channel):
            self.instrument = instrument
            self.data_handler = data_handler
            self.channel = channel
        def set(self, state, channel):
            """
            Turns the output offset for X (0), Y (1), or R (2) to off (0) or on (1).
            channel: 'X', 'Y', 'R', or int 0-2
            state: 'OFF', 'ON', 0, or 1
            """
            if isinstance(channel, str):
                ch = channel.upper()
                if ch == "X":
                    j = 0
                elif ch == "Y":
                    j = 1
                elif ch == "R":
                    j = 2
                else:
                    raise ValueError("Channel must be 'X', 'Y', 'R', or integer 0-2.")
            elif channel in [0, 1, 2]:
                j = int(channel)
            else:
                raise ValueError("Channel must be 'X', 'Y', 'R', or integer 0-2.")

            if j == 3:
                raise ValueError("Setting offset for phase is not allowed.")

            if isinstance(state, str):
                s = state.upper()
                if s == "OFF":
                    i = 0
                elif s == "ON":
                    i = 1
                else:
                    raise ValueError("State must be 'OFF', 'ON', 0, or 1.")
            elif state in [0, 1]:
                i = int(state)
            else:
                raise ValueError("State must be 'OFF', 'ON', 0, or 1.")

            cmd = f"COFA {j}, {i}"
            self.instrument.write(cmd)

        def get_offset_state(self, channel):
            """
            Returns the output offset state for X (0), Y (1), or R (2).
            channel: 'X', 'Y', 'R', or int 0-2
            Returns: int (0 for off, 1 for on)
            """
            if isinstance(channel, str):
                ch = channel.upper()
                if ch == "X":
                    j = 0
                elif ch == "Y":
                    j = 1
                elif ch == "R":
                    j = 2
                else:
                    raise ValueError("Channel must be 'X', 'Y', 'R', or integer 0-2.")
            elif channel in [0, 1, 2]:
                j = int(channel)
            else:
                raise ValueError("Channel must be 'X', 'Y', 'R', or integer 0-2.")

            cmd = f"COFA? {j}"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return int(response)

        def set_percentage(self, channel, percent):
            """
            Sets the output offset percentage for X (0), Y (1), or R (2).
            channel: 'X', 'Y', 'R', or int 0-2
            percent: float, −999.99 to +999.99
            """
            if isinstance(channel, str):
                ch = channel.upper()
                if ch == "X":
                    j = 0
                elif ch == "Y":
                    j = 1
                elif ch == "R":
                    j = 2
                else:
                    raise ValueError("Channel must be 'X', 'Y', 'R', or integer 0-2.")
            elif channel in [0, 1, 2]:
                j = int(channel)
            else:
                raise ValueError("Channel must be 'X', 'Y', 'R', or integer 0-2.")

            if not (-999.99 <= float(percent) <= 999.99):
                raise ValueError("Offset percentage must be between -999.99 and +999.99.")

            cmd = f"COFP {j}, {float(percent):.2f}"
            self.instrument.write(cmd)

        def get_offset_percentage(self, channel):
            """
            Returns the output offset percentage for X (0), Y (1), or R (2).
            channel: 'X', 'Y', 'R', or int 0-2
            Returns: float
            """
            if isinstance(channel, str):
                ch = channel.upper()
                if ch == "X":
                    j = 0
                elif ch == "Y":
                    j = 1
                elif ch == "R":
                    j = 2
                else:
                    raise ValueError("Channel must be 'X', 'Y', 'R', or integer 0-2.")
            elif channel in [0, 1, 2]:
                j = int(channel)
            else:
                raise ValueError("Channel must be 'X', 'Y', 'R', or integer 0-2.")

            cmd = f"COFP? {j}"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return float(response)

        def auto_offset(self, channel):
            """
            Auto offsets X (0), Y (1), or R (2).
            channel: 'X', 'Y', 'R', or int 0-2
            """
            if isinstance(channel, str):
                ch = channel.upper()
                if ch == "X":
                    j = 0
                elif ch == "Y":
                    j = 1
                elif ch == "R":
                    j = 2
                else:
                    raise ValueError("Channel must be 'X', 'Y', 'R', or integer 0-2.")
            elif channel in [0, 1, 2]:
                j = int(channel)
            else:
                raise ValueError("Channel must be 'X', 'Y', 'R', or integer 0-2.")

            cmd = f"OAUT {j}"
            self.instrument.write(cmd)

class Aux:
    def __init__(self, instrument, data_handler):
        self.instrument = instrument
        self.data_handler = data_handler
        
    def get_aux_input(self, j):
        """
        Queries the aux input voltage.
        j: int, aux input index (0-3)
        Returns: float (Volts)
        """
        if not (0 <= int(j) <= 3):
            raise ValueError("Aux input index j must be between 0 and 3.")
        cmd = f"OAUX? {int(j)}"
        response = self.instrument.query(cmd)
        self.data_handler.log_command(cmd, response)
        return float(response)

    def set_aux_output(self, j, v, unit="V"):
        """
        Sets an aux output to voltage v.
        j: int, aux output index (0-3)
        v: float, voltage value (-10.5 V to +10.5 V)
        unit: str, one of 'NV', 'UV', 'MV', 'V'
        """
        valid_units = ["NV", "UV", "MV", "V"]
        if not (0 <= int(j) <= 3):
            raise ValueError("Aux output index j must be between 0 and 3.")
        if unit.upper() not in valid_units:
            raise ValueError(f"Invalid unit. Choose from {valid_units}.")
        if not (-10.5 <= float(v) <= 10.5):
            raise ValueError("Voltage must be between -10.5 V and +10.5 V.")
        cmd = f"AUXV {int(j)}, {float(v)} {unit.upper()}"
        self.instrument.write(cmd)

    def get_aux_output(self, j):
        """
        Queries the aux output voltage setting.
        j: int, aux output index (0-3)
        Returns: float (Volts)
        """
        if not (0 <= int(j) <= 3):
            raise ValueError("Aux output index j must be between 0 and 3.")
        cmd = f"AUXV? {int(j)}"
        response = self.instrument.query(cmd)
        self.data_handler.log_command(cmd, response)
        return float(response)
    
class Display:
    """Commands to control the display settings of the lock-in amplifier."""
    def __init__(self, instrument, data_handler):
        self.instrument = instrument
        self.data_handler = data_handler
        self.channel1 = self.Channel(instrument, data_handler, 1)
        self.channel2 = self.Channel(instrument, data_handler, 2)
        self.channel3 = self.Channel(instrument, data_handler, 3)
        self.channel4 = self.Channel(instrument, data_handler, 4)
        self.cursor = self.Cursor(instrument, data_handler)
        self.fft = self.FFT(instrument, data_handler)
    def get_screenshot_image(self):
        """
        Queries the instrument for a screen image (BMP format) and returns it as an image object using data_handler.bytes_toimage.
        Returns: Image object (from data_handler.bytes_toimage)
        """
        cmd = "GETSCREEN?"
        # Initiate the screen capture
        self.instrument.write(cmd)
        # Wait for MAV (Message Available) bit to be set in the status byte
        while True:
            stb = self.instrument.read_stb()  # Use VISA Read STB, not *STB?
            if stb & 0x10:  # MAV bit is bit 4 (0x10)
                break
        # Read the binary block
        raw_data = self.instrument.read_raw()
        # Convert the binary block to an image using the data_handler
        image = self.data_handler.bytes_to_image(raw_data)
        if self.data_handler.is_auto_saving_data_enabled():
            self.data_handler.write_to_file(self, f"LOCKIN_SCREENSHOT", file_type = EFileType.PNG)
        self.data_handler.log_command(cmd, "<BMP image>")
        return image
    def set_strip_chart_live(self, state):
        """
        Pauses (OFF/0) or resumes (ON/1) the strip chart.
        state: 'OFF', 'ON', 0, or 1
        """
        if isinstance(state, str):
            s = state.upper()
            if s == "OFF":
                i = 0
            elif s == "ON":
                i = 1
            else:
                raise ValueError("State must be 'OFF', 'ON', 0, or 1.")
        elif state in [0, 1]:
            i = int(state)
        else:
            raise ValueError("State must be 'OFF', 'ON', 0, or 1.")
        cmd = f"GLIV {i}"
        self.instrument.write(cmd)

    def get_strip_chart_live(self):
        """
        Returns the strip chart state.
        Returns: int (0 for paused, 1 for live)
        """
        cmd = "GLIV?"
        response = self.instrument.query(cmd)
        self.data_handler.log_command(cmd, response)
        return int(response)
    def set_strip_chart_time_div(self, i):
        """
        Sets the horizontal time/div for the strip chart according to the table below.

        Index | Time/div
        ------|----------
        0     | 0.5 s
        1     | 1 s
        2     | 2 s
        3     | 5 s
        4     | 10 s
        5     | 30 s
        6     | 1 min
        7     | 2 min
        8     | 5 min
        9     | 10 min
        10    | 30 min
        11    | 1 hour
        12    | 2 hour
        13    | 6 hour
        14    | 12 hour
        15    | 1 day
        16    | 2 day

        i: int, 0-16
        Example: set_strip_chart_time_div(6) sets the strip chart to 1 min/div horizontal scale.
        """
        if not (0 <= int(i) <= 16):
            raise ValueError("Index i must be between 0 and 16.")
        cmd = f"GSPD {int(i)}"
        self.instrument.write(cmd)

    def get_strip_chart_time_div(self):
        """
        Returns the horizontal time/div index for the strip chart (0-16).

        Use the following table for reference:
        Index | Time/div
        ------|----------
        0     | 0.5 s
        1     | 1 s
        2     | 2 s
        3     | 5 s
        4     | 10 s
        5     | 30 s
        6     | 1 min
        7     | 2 min
        8     | 5 min
        9     | 10 min
        10    | 30 min
        11    | 1 hour
        12    | 2 hour
        13    | 6 hour
        14    | 12 hour
        15    | 1 day
        16    | 2 day
        """
        cmd = "GSPD?"
        response = self.instrument.query(cmd)
        self.data_handler.log_command(cmd, response)
        return int(response)
    def set_blank(self, state):
        """
        Turns front panel blanking off (0/OFF) or on (1/ON).
        state: 'OFF', 'ON', 0, or 1
        """
        if isinstance(state, str):
            s = state.upper()
            if s == "OFF":
                i = 0
            elif s == "ON":
                i = 1
            else:
                raise ValueError("State must be 'OFF', 'ON', 0, or 1.")
        elif state in [0, 1]:
            i = int(state)
        else:
            raise ValueError("State must be 'OFF', 'ON', 0, or 1.")
        cmd = f"DBLK {i}"
        self.instrument.write(cmd)

    def get_blank(self):
        """
        Returns the blanking state.
        Returns: int (0 for OFF/displays on, 1 for ON/displays off)
        """
        cmd = "DBLK?"
        response = self.instrument.query(cmd)
        self.data_handler.log_command(cmd, response)
        return int(response)

    def set_layout(self, layout):
        """
        Sets the screen layout.
        layout: 'TREND', 'HIST', 'BARHIST', 'FFT', 'BARFFT', 'BAREIGHT', or int 0-5
        """
        if isinstance(layout, str):
            l = layout.upper()
            if l in ["TREND"]:
                i = 0
            elif l in ["HIST", "HISTORY"]:
                i = 1
            elif l == "BARHIST":
                i = 2
            elif l == "FFT":
                i = 3
            elif l == "BARFFT":
                i = 4
            elif l == "BAREIGHT":
                i = 5
            else:
                raise ValueError("Layout must be 'TREND', 'HIST', 'BARHIST', 'FFT', 'BARFFT', 'BAREIGHT', or integer 0-5.")
        elif layout in [0, 1, 2, 3, 4, 5]:
            i = int(layout)
        else:
            raise ValueError("Layout must be 'TREND', 'HIST', 'BARHIST', 'FFT', 'BARFFT', 'BAREIGHT', or integer 0-5.")
        cmd = f"DLAY {i}"
        self.instrument.write(cmd)

    def get_layout(self):
        """
        Returns the screen layout.
        Returns: int (0=TREND, 1=HIST, 2=BARHIST, 3=FFT, 4=BARFFT, 5=BAREIGHT)
        """
        cmd = "DLAY?"
        response = self.instrument.query(cmd)
        self.data_handler.log_command(cmd, response)
        return int(response)

    def save_screenshot(self):
        """
        Saves a screenshot to a USB memory stick.
        """
        cmd = "DCAP"
        self.instrument.write(cmd)
    class Channel:
        """Commands to control the display of specific channels. CHannel 1: Green, CHannel 2: Blue, CHannel 3: Yellow., CHannel 4: Orange."""
        def __init__(self, instrument, data_handler, channel):
            self.instrument = instrument
            self.data_handler = data_handler
            self.channel = channel
        def get_cursor_value(self, channel):
            """
            Queries the strip chart cursor value for a data channel or status.

            channel: 'DAT1', 'DAT2', 'DAT3', 'DAT4', 'STATUS', or int 0-4
                0: DAT1 (green)
                1: DAT2 (blue)
                2: DAT3 (yellow)
                3: DAT4 (orange)
                4: STATUS (error status at cursor position)

            Returns:
                float: cursor value for DAT1-4
                int: status bitfield for STATUS (see table below)

            Status Bitfield (for STATUS/4):
                Bit | Weight | Definition
                ----|--------|--------------------------
                 0  |   1    | Timebase error
                 1  |   2    | External reference unlock
                 2  |   4    | Signal overload
                 3  |   8    | Sync filter error

            Example:
                get_cursor_value('DAT2')   # Returns value for data channel 2 (blue)
                get_cursor_value('STATUS') # Returns error status at cursor position
            """
            channel_map = {'DAT1': 0, 'DAT2': 1, 'DAT3': 2, 'DAT4': 3, 'STATUS': 4, 'STAT': 4}
            if isinstance(channel, str):
                ch = channel.upper()
                if ch in channel_map:
                    j = channel_map[ch]
                else:
                    try:
                        j = int(ch)
                    except ValueError:
                        raise ValueError("Channel must be 'DAT1', 'DAT2', 'DAT3', 'DAT4', 'STATUS', or integer 0-4.")
            elif channel in [0, 1, 2, 3, 4]:
                j = int(channel)
            else:
                raise ValueError("Channel must be 'DAT1', 'DAT2', 'DAT3', 'DAT4', 'STATUS', or integer 0-4.")

            if j == 4:
                cmd = "SCRY? STATUS"
            else:
                cmd = f"SCRY? {j}"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            if j == 4:
                return int(response)
            else:
                return float(response)
        def set_data_channel_parameter(self, parameter):
            """
            Assigns a parameter to a data channel.
            
            parameter: str or int
                i enumeration:
                0: X output, 1: Y output, 2: R output, 3: Theta output,
                4: AuxIn1, 5: AuxIn2, 6: Aux3, 7: Aux4,
                8: Xnoise, 9: Ynoise, 10: Aux Out1, 11: Aux Out2,
                12: Reference Phase, 13: Sine Out Amplitude, 14: DC Level,
                15: Internal Reference Frequency, 16: External Reference Frequency
                You may also use parameter names: 'X', 'Y', 'R', 'THETA', 'IN1', 'IN2', 'IN3', 'IN4', 'XNOISE', 'YNOISE', 'OUT1', 'OUT2', 'PHASE', 'SAMP', 'LEVEL', 'FINT', 'FEXT'
            """
            channel_map = {'DAT1': 0, 'DAT2': 1, 'DAT3': 2, 'DAT4': 3}
            param_map = {
                'X': 0, 'Y': 1, 'R': 2, 'THETA': 3, 'IN1': 4, 'IN2': 5, 'IN3': 6, 'IN4': 7,
                'XNOISE': 8, 'YNOISE': 9, 'OUT1': 10, 'OUT2': 11, 'PHASE': 12, 'SAMP': 13,
                'LEVEL': 14, 'FINT': 15, 'FEXT': 16
            }
            if isinstance(self.channel, str):
                ch = self.channel.upper()
                if ch in channel_map:
                    j = channel_map[ch]
                else:
                    try:
                        j = int(ch)
                    except ValueError:
                        raise ValueError("Channel must be 'DAT1', 'DAT2', 'DAT3', 'DAT4', or integer 0-3.")
            elif self.channel in [0, 1, 2, 3]:
                j = int(self.channel)
            else:
                raise ValueError("Channel must be 'DAT1', 'DAT2', 'DAT3', 'DAT4', or integer 0-3.")

            if isinstance(parameter, str):
                p = parameter.upper()
                if p in param_map:
                    i = param_map[p]
                else:
                    try:
                        i = int(p)
                    except ValueError:
                        raise ValueError("Parameter must be a valid name or integer 0-16.")
            elif isinstance(parameter, int) and 0 <= parameter <= 16:
                i = int(parameter)
            else:
                raise ValueError("Parameter must be a valid name or integer 0-16.")

            cmd = f"CDSP {j}, {i}"
            self.instrument.write(cmd)

        def get_data_channel_parameter(self, channel):
            """
            Returns the parameter index assigned to a data channel.
            channel: 'DAT1', 'DAT2', 'DAT3', 'DAT4', or int 0-3
                0: DAT1 (green), 1: DAT2 (blue), 2: DAT3 (yellow), 3: DAT4 (orange)
            Returns: int (parameter index 0-16)
            """
            channel_map = {'DAT1': 0, 'DAT2': 1, 'DAT3': 2, 'DAT4': 3}
            if isinstance(channel, str):
                ch = channel.upper()
                if ch in channel_map:
                    j = channel_map[ch]
                else:
                    try:
                        j = int(ch)
                    except ValueError:
                        raise ValueError("Channel must be 'DAT1', 'DAT2', 'DAT3', 'DAT4', or integer 0-3.")
            elif channel in [0, 1, 2, 3]:
                j = int(channel)
            else:
                raise ValueError("Channel must be 'DAT1', 'DAT2', 'DAT3', 'DAT4', or integer 0-3.")

            cmd = f"CDSP? {j}"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return int(response)

        def set_data_channel_graph(self, state):
            """
            Turns the strip chart graph of a data channel on or off.
            
            state: 'OFF', 'ON', 0, or 1
                0: OFF, 1: ON
            """
            channel_map = {'DAT1': 0, 'DAT2': 1, 'DAT3': 2, 'DAT4': 3}
            if isinstance(self.channel, str):
                ch = self.channel.upper()
                if ch in channel_map:
                    j = channel_map[ch]
                else:
                    try:
                        j = int(ch)
                    except ValueError:
                        raise ValueError("Channel must be 'DAT1', 'DAT2', 'DAT3', 'DAT4', or integer 0-3.")
            elif self.channel in [0, 1, 2, 3]:
                j = int(self.channel)
            else:
                raise ValueError("Channel must be 'DAT1', 'DAT2', 'DAT3', 'DAT4', or integer 0-3.")

            if isinstance(state, str):
                s = state.upper()
                if s == "OFF":
                    i = 0
                elif s == "ON":
                    i = 1
                else:
                    raise ValueError("State must be 'OFF', 'ON', 0, or 1.")
            elif state in [0, 1]:
                i = int(state)
            else:
                raise ValueError("State must be 'OFF', 'ON', 0, or 1.")

            cmd = f"CGRF {j}, {i}"
            self.instrument.write(cmd)

        def get_data_channel_graph(self):
            """
            Returns the strip chart graphing state for a data channel.
            
            Returns: int (0 for OFF, 1 for ON)
            """
            channel_map = {'DAT1': 0, 'DAT2': 1, 'DAT3': 2, 'DAT4': 3}
            if isinstance(self.channel, str):
                ch = self.channel.upper()
                if ch in channel_map:
                    j = channel_map[ch]
                else:
                    try:
                        j = int(ch)
                    except ValueError:
                        raise ValueError("Channel must be 'DAT1', 'DAT2', 'DAT3', 'DAT4', or integer 0-3.")
            elif self.channel in [0, 1, 2, 3]:
                j = int(self.channel)
            else:
                raise ValueError("Channel must be 'DAT1', 'DAT2', 'DAT3', 'DAT4', or integer 0-3.")

            cmd = f"CGRF? {j}"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return int(response)
        def set_strip_chart_time_div(self, i):
            """
            Sets the horizontal time/div for the strip chart for this channel.

            Index | Time/div
            ------|----------
            0     | 0.5 s
            1     | 1 s
            2     | 2 s
            3     | 5 s
            4     | 10 s
            5     | 30 s
            6     | 1 min
            7     | 2 min
            8     | 5 min
            9     | 10 min
            10    | 30 min
            11    | 1 hour
            12    | 2 hour
            13    | 6 hour
            14    | 12 hour
            15    | 1 day
            16    | 2 day

            i: int, 0-16
            Example: set_strip_chart_time_div(6) sets the strip chart to 1 min/div horizontal scale.
            """
            if not (0 <= int(i) <= 16):
                raise ValueError("Index i must be between 0 and 16.")
            cmd = f"GSPD {self.channel},{int(i)}"
            self.instrument.write(cmd)

        def get_strip_chart_time_div(self):
            """
            Returns the horizontal time/div index for the strip chart (0-16).

            Use the following table for reference:
            Index | Time/div
            ------|----------
            0     | 0.5 s
            1     | 1 s
            2     | 2 s
            3     | 5 s
            4     | 10 s
            5     | 30 s
            6     | 1 min
            7     | 2 min
            8     | 5 min
            9     | 10 min
            10    | 30 min
            11    | 1 hour
            12    | 2 hour
            13    | 6 hour
            14    | 12 hour
            15    | 1 day
            16    | 2 day
            """
            cmd = f"GSPD? {self.channel}"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return int(response)
        def set_vertical_scale(self, scale):
            """
            Sets the vertical scale of this data channel to scale/div.
            scale: float, desired scale per division (will be set to nearest allowed 1-2-5 sequence)
            Example: set_vertical_scale(0.1)
            """
            cmd = f"GSCL {self.channel}, {float(scale)}"
            self.instrument.write(cmd)

        def get_vertical_scale(self):
            """
            Returns the vertical scale for this data channel.
            Returns: float (scale per division)
            """
            cmd = f"GSCL? {self.channel}"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return float(response)

        def set_vertical_offset(self, offset):
            """
            Sets the vertical offset of this data channel.
            offset: float, desired vertical offset
            Example: set_vertical_offset(0.1)
            """
            cmd = f"GOFF {self.channel}, {float(offset)}"
            self.instrument.write(cmd)

        def get_vertical_offset(self):
            """
            Returns the vertical offset for this data channel.
            Returns: float (vertical offset)
            """
            cmd = f"GOFF? {self.channel}"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return float(response)

        def auto_scale(self):
            """
            Performs an Auto Scale on this data channel (same as pressing the scale palette button).
            """
            cmd = f"GAUT {self.channel}"
            self.instrument.write(cmd)

        def auto_scale_zero_center(self):
            """
            Performs an Auto Scale keeping zero at the center on this data channel.
            """
            cmd = f"GACT {self.channel}"
            self.instrument.write(cmd)

        def auto_find(self):
            """
            Performs an Auto Find on this data channel.
            """
            cmd = f"GAUF {self.channel}"
            self.instrument.write(cmd)

        def set_graph(self, state):
            """
            Turns the graph of this data channel off (0/OFF) or on (1/ON).
            state: 'OFF', 'ON', 0, or 1
            """
            if isinstance(state, str):
                s = state.upper()
                if s == "OFF":
                    i = 0
                elif s == "ON":
                    i = 1
                else:
                    raise ValueError("State must be 'OFF', 'ON', 0, or 1.")
            elif state in [0, 1]:
                i = int(state)
            else:
                raise ValueError("State must be 'OFF', 'ON', 0, or 1.")
            cmd = f"CGRF {self.channel}, {i}"
            self.instrument.write(cmd)

        def get_graph(self):
            """
            Returns the graphing state for this data channel.
            Returns: int (0 for OFF, 1 for ON)
            """
            cmd = f"CGRF? {self.channel}"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return int(response)
    class Cursor:
        """Controls cursor on screen"""
        def __init__(self, instrument, data_handler):
            self.instrument = instrument
            self.data_handler = data_handler
        def get_datetime(self):
            """
            Returns the strip chart cursor horizontal date and time as a string.
            Example: '28Apr14,14:25:35.96'
            Note: Only valid when the display is paused.
            """
            cmd = "CURDATTIM?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return response

        def get_interval(self):
            """
            Returns the strip chart cursor horizontal position as a string.
            Example: '-2d 16:07:30.00'
            Note: Only valid when the display is paused.
            """
            cmd = "CURINTERVAL?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return response
        def set_position(self, i):
            """
            Sets the strip chart cursor position.
            i: int, 0 (right edge) to 639 (left edge)
            """
            if not (0 <= int(i) <= 639):
                raise ValueError("Cursor position i must be between 0 (right edge) and 639 (left edge).")
            cmd = f"PCUR {int(i)}"
            self.instrument.write(cmd)

        def get_position(self):
            """
            Returns the strip chart cursor position.
            Returns: int (0-639)
            """
            cmd = "PCUR?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return int(response)

        def set_relative_mode(self, mode):
            """
            Sets the strip chart cursor to relative (1/ON) or absolute (0/OFF) mode.
            mode: 'OFF', 'ON', 0, or 1
            """
            if isinstance(mode, str):
                m = mode.upper()
                if m == "OFF":
                    i = 0
                elif m == "ON":
                    i = 1
                else:
                    raise ValueError("Mode must be 'OFF', 'ON', 0, or 1.")
            elif mode in [0, 1]:
                i = int(mode)
            else:
                raise ValueError("Mode must be 'OFF', 'ON', 0, or 1.")
            cmd = f"CURREL {i}"
            self.instrument.write(cmd)

        def get_relative_mode(self):
            """
            Returns the cursor relative mode state.
            Returns: int (0 for absolute, 1 for relative)
            """
            cmd = "CURREL?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return int(response)

        def set_display_mode(self, mode):
            """
            Sets the cursor horizontal position display mode.
            mode: 'DATE', 'TIME', 0 (date/time), or 1 (interval)
            """
            if isinstance(mode, str):
                m = mode.upper()
                if m in ["DATE", "TIME", "DATETIME"]:
                    i = 0
                elif m == "INTERVAL":
                    i = 1
                else:
                    raise ValueError("Mode must be 'DATE', 'TIME', 0, or 1.")
            elif mode in [0, 1]:
                i = int(mode)
            else:
                raise ValueError("Mode must be 'DATE', 'TIME', 0, or 1.")
            cmd = f"CURDISP {i}"
            self.instrument.write(cmd)

        def get_display_mode(self):
            """
            Returns the cursor horizontal position display mode.
            Returns: int (0 for date/time, 1 for interval)
            """
            cmd = "CURDISP?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return int(response)

        def set_readout_mode(self, mode):
            """
            Sets the strip chart cursor readout mode.
            mode: 'AVG', 'MEAN', 0 (mean), 'MAX', 1 (maximum), 'MIN', 2 (minimum)
            """
            if isinstance(mode, str):
                m = mode.upper()
                if m in ["AVG", "MEAN"]:
                    i = 0
                elif m == "MAX":
                    i = 1
                elif m == "MIN":
                    i = 2
                else:
                    raise ValueError("Mode must be 'AVG', 'MEAN', 'MAX', 'MIN', 0, 1, or 2.")
            elif mode in [0, 1, 2]:
                i = int(mode)
            else:
                raise ValueError("Mode must be 'AVG', 'MEAN', 'MAX', 'MIN', 0, 1, or 2.")
            cmd = f"CURBUG {i}"
            self.instrument.write(cmd)

        def get_readout_mode(self):
            """
            Returns the cursor readout mode.
            Returns: int (0 for mean, 1 for max, 2 for min)
            """
            cmd = "CURBUG?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return int(response)
        def set_cursor_width(self, width):
            """
            Sets the cursor width.
            width: 'LINE', 'NARROW', 'WIDE', or int 0-2
            """
            if isinstance(width, str):
                w = width.upper()
                if w == "LINE":
                    i = 0
                elif w == "NARROW":
                    i = 1
                elif w == "WIDE":
                    i = 2
                else:
                    raise ValueError("Width must be 'LINE', 'NARROW', 'WIDE', or integer 0-2.")
            elif width in [0, 1, 2]:
                i = int(width)
            else:
                raise ValueError("Width must be 'LINE', 'NARROW', 'WIDE', or integer 0-2.")
            cmd = f"FCRW {i}"
            self.instrument.write(cmd)

        def get_cursor_width(self):
            """
            Returns the cursor width.
            Returns: int (0 for LINE, 1 for NARROW, 2 for WIDE)
            """
            cmd = "FCRW?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return int(response)
    class FFT:
        """Commands related to FFT display controls. You will need a synthesized function generator capable of providing a 100 mVrms
        sine wave at 100.000 kHz, BNC cables and a terminator appropriate for the generator function output.
        You will display the FFT when measuring a signal close to, but not equal to, the internal reference
        frequency."""
        def set_source(self, source):
            """
            Sets the source for the FFT.
            source: 'ADC', 'MIXER', 'FILTER', 0, 1, or 2
            """
            if isinstance(source, str):
                s = source.upper()
                if s == "ADC":
                    i = 0
                elif s == "MIXER":
                    i = 1
                elif s in ["FILTER", "FILT"]:
                    i = 2
                else:
                    raise ValueError("Source must be 'ADC', 'MIXER', 'FILTER', or integer 0-2.")
            elif source in [0, 1, 2]:
                i = int(source)
            else:
                raise ValueError("Source must be 'ADC', 'MIXER', 'FILTER', or integer 0-2.")
            cmd = f"FFTR {i}"
            self.instrument.write(cmd)

        def get_source(self):
            """
            Returns the FFT source.
            Returns: int (0=ADC, 1=MIXER, 2=FILTER)
            """
            cmd = "FFTR?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return int(response)

        def set_scale(self, i):
            """
            Sets the FFT vertical scale (dB/div).
            i: int, -20 ≤ i ≤ 20
            """
            if not (-20 <= int(i) <= 20):
                raise ValueError("FFT scale index i must be between -20 and 20.")
            cmd = f"FFTS {int(i)}"
            self.instrument.write(cmd)

        def get_scale(self):
            """
            Returns the FFT vertical scale index.
            Returns: int
            """
            cmd = "FFTS?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return int(response)

        def set_offset(self, x):
            """
            Sets the FFT vertical offset x (dB).
            x: float
            """
            cmd = f"FFTO {float(x)}"
            self.instrument.write(cmd)

        def get_offset(self):
            """
            Returns the FFT vertical offset (dB).
            Returns: float
            """
            cmd = "FFTO?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return float(response)
        def auto_scale(self):
            """
            Performs an Auto Scale on the FFT display (same as pressing the FFT vertical scale palette button).
            """
            cmd = "FAUT"
            self.instrument.write(cmd)

        def get_max_span(self):
            """
            Returns the maximum allowed FFT span (Hz/div) for the current FFT source and lock-in configuration.
            Returns: float (Hz/div)
            """
            cmd = "FFTMAXSPAN?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return float(response)

        def set_span(self, span):
            """
            Sets the FFT span to span Hz/div. Value may not exceed the maximum allowed span.
            span: float, desired span in Hz/div
            """
            cmd = f"FFTSPAN {float(span)}"
            self.instrument.write(cmd)

        def get_span(self):
            """
            Returns the FFT span in Hz/div.
            Returns: float
            """
            cmd = "FFTSPAN?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return float(response)

        def set_averaging(self, avg):
            """
            Sets the FFT averaging.
            avg: 'AVG1', 'AVG3', 'AVG10', 'AVG30', 'AVG100', or int 0-4
                0: 1, 1: 3, 2: 10, 3: 30, 4: 100
            """
            avg_map = {'AVG1': 0, 'AVG3': 1, 'AVG10': 2, 'AVG30': 3, 'AVG100': 4}
            if isinstance(avg, str):
                a = avg.upper()
                if a in avg_map:
                    i = avg_map[a]
                else:
                    try:
                        i = int(a)
                    except ValueError:
                        raise ValueError("Averaging must be 'AVG1', 'AVG3', 'AVG10', 'AVG30', 'AVG100', or integer 0-4.")
            elif avg in [0, 1, 2, 3, 4]:
                i = int(avg)
            else:
                raise ValueError("Averaging must be 'AVG1', 'AVG3', 'AVG10', 'AVG30', 'AVG100', or integer 0-4.")
            cmd = f"FFTA {i}"
            self.instrument.write(cmd)

        def get_averaging(self):
            """
            Returns the FFT averaging index.
            Returns: int (0: 1, 1: 3, 2: 10, 3: 30, 4: 100)
            """
            cmd = "FFTA?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return int(response)

        def set_graphing(self, state):
            """
            Pauses (OFF/0) or resumes (ON/1) the FFT graphing.
            state: 'OFF', 'ON', 0, or 1
            """
            if isinstance(state, str):
                s = state.upper()
                if s == "OFF":
                    i = 0
                elif s == "ON":
                    i = 1
                else:
                    raise ValueError("State must be 'OFF', 'ON', 0, or 1.")
            elif state in [0, 1]:
                i = int(state)
            else:
                raise ValueError("State must be 'OFF', 'ON', 0, or 1.")
            cmd = f"FFTL {i}"
            self.instrument.write(cmd)

        def get_graphing(self):
            """
            Returns the FFT graphing state.
            Returns: int (0 for paused, 1 for live)
            """
            cmd = "FFTL?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return int(response)
        def get_cursor_frequency(self):
            """
            Returns the frequency value of the FFT cursor readout (in Hz).
            Returns: float
            """
            cmd = "FCRX?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return float(response)

        def get_cursor_amplitude(self):
            """
            Returns the amplitude value of the FFT cursor readout (in dB).
            Only valid when the display is set to FFT mode.
            Returns: float
            """
            cmd = "FCRY?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return float(response)

class Scan:
    """Commands to control and perform a scan."""
    def __init__(self, instrument, data_handler):
        self.instrument = instrument
        self.data_handler = data_handler
    def set_parameter(self, param):
        """
        Sets the scan parameter.
        param: 'FINT', 'REFAmp', 'REFDC', 'OUT1', 'OUT2', or int 0-4
            0: Fint (internal frequency)
            1: Ref Ampl
            2: Ref DC
            3: Out1
            4: Out2
        """
        param_map = {'FINT': 0, 'REFAMP': 1, 'REFDC': 2, 'OUT1': 3, 'OUT2': 4}
        if isinstance(param, str):
            p = param.upper()
            if p in param_map:
                i = param_map[p]
            else:
                try:
                    i = int(p)
                except ValueError:
                    raise ValueError("Parameter must be 'FINT', 'REFAMP', 'REFDC', 'OUT1', 'OUT2', or integer 0-4.")
        elif param in [0, 1, 2, 3, 4]:
            i = int(param)
        else:
            raise ValueError("Parameter must be 'FINT', 'REFAMP', 'REFDC', 'OUT1', 'OUT2', or integer 0-4.")
        cmd = f"SCNPAR {i}"
        self.instrument.write(cmd)

    def get_parameter(self):
        """
        Returns the scan parameter index.
        Returns: int (0=Fint, 1=RefAmp, 2=RefDC, 3=Out1, 4=Out2)
        """
        cmd = "SCNPAR?"
        response = self.instrument.query(cmd)
        self.data_handler.log_command(cmd, response)
        return int(response)

    def set_type(self, scan_type):
        """
        Sets the scan type.
        scan_type: 'LIN', 'LOG', 0, or 1
            0: Linear
            1: Logarithmic
        """
        if isinstance(scan_type, str):
            t = scan_type.upper()
            if t == "LIN":
                i = 0
            elif t == "LOG":
                i = 1
            else:
                raise ValueError("Scan type must be 'LIN', 'LOG', 0, or 1.")
        elif scan_type in [0, 1]:
            i = int(scan_type)
        else:
            raise ValueError("Scan type must be 'LIN', 'LOG', 0, or 1.")
        cmd = f"SCNLOG {i}"
        self.instrument.write(cmd)

    def get_type(self):
        """
        Returns the scan type.
        Returns: int (0=LIN, 1=LOG)
        """
        cmd = "SCNLOG?"
        response = self.instrument.query(cmd)
        self.data_handler.log_command(cmd, response)
        return int(response)

    def set_end_mode(self, mode):
        """
        Sets the scan end mode.
        mode: 'ONCE', 'REPEAT', 'UPDOWN', 0, 1, or 2
            0: Once
            1: Repeat
            2: Up/Down
        """
        if isinstance(mode, str):
            m = mode.upper()
            if m == "ONCE":
                i = 0
            elif m == "REPEAT":
                i = 1
            elif m == "UPDOWN":
                i = 2
            else:
                raise ValueError("Scan end mode must be 'ONCE', 'REPEAT', 'UPDOWN', 0, 1, or 2.")
        elif mode in [0, 1, 2]:
            i = int(mode)
        else:
            raise ValueError("Scan end mode must be 'ONCE', 'REPEAT', 'UPDOWN', 0, 1, or 2.")
        cmd = f"SCNEND {i}"
        self.instrument.write(cmd)

    def get_end_mode(self):
        """
        Returns the scan end mode.
        Returns: int (0=ONCE, 1=REPEAT, 2=UPDOWN)
        """
        cmd = "SCNEND?"
        response = self.instrument.query(cmd)
        self.data_handler.log_command(cmd, response)
        return int(response)

    def set_time(self, seconds):
        """
        Sets the scan time in seconds.
        seconds: float, 0 < seconds <= 1728000 (20 days)
        """
        if not (0 < float(seconds) <= 1728000):
            raise ValueError("Scan time must be between 0 and 1,728,000 seconds (20 days).")
        cmd = f"SCNSEC {float(seconds)}"
        self.instrument.write(cmd)

    def get_time(self):
        """
        Returns the scan time in seconds.
        Returns: float
        """
        cmd = "SCNSEC?"
        response = self.instrument.query(cmd)
        self.data_handler.log_command(cmd, response)
        return float(response)

    def set_amplitude_attenuator_mode(self, mode):
        """
        Sets the output attenuator mode when scanning sine out amplitude.
        mode: 'AUTO', 'FIXED', 0, or 1
            0: Automatic
            1: Fixed
        """
        if isinstance(mode, str):
            m = mode.upper()
            if m == "AUTO":
                i = 0
            elif m == "FIXED":
                i = 1
            else:
                raise ValueError("Mode must be 'AUTO', 'FIXED', 0, or 1.")
        elif mode in [0, 1]:
            i = int(mode)
        else:
            raise ValueError("Mode must be 'AUTO', 'FIXED', 0, or 1.")
        cmd = f"SCNAMPATTN {i}"
        self.instrument.write(cmd)

    def get_amplitude_attenuator_mode(self):
        """
        Returns the output attenuator mode when scanning sine out amplitude.
        Returns: int (0=AUTO, 1=FIXED)
        """
        cmd = "SCNAMPATTN?"
        response = self.instrument.query(cmd)
        self.data_handler.log_command(cmd, response)
        return int(response)
    def set_dc_attenuator_mode(self, mode):
        """
        Sets the operating mode for the output attenuators when scanning DC level.
        mode: 'AUTO', 'FIXED', 0, or 1
            0: Automatic
            1: Fixed
        """
        if isinstance(mode, str):
            m = mode.upper()
            if m == "AUTO":
                i = 0
            elif m == "FIXED":
                i = 1
            else:
                raise ValueError("Mode must be 'AUTO', 'FIXED', 0, or 1.")
        elif mode in [0, 1]:
            i = int(mode)
        else:
            raise ValueError("Mode must be 'AUTO', 'FIXED', 0, or 1.")
        cmd = f"SCNDCATTN {i}"
        self.instrument.write(cmd)

    def get_dc_attenuator_mode(self):
        """
        Returns the mode for DC level output attenuators during scan.
        Returns: int (0=AUTO, 1=FIXED)
        """
        cmd = "SCNDCATTN?"
        response = self.instrument.query(cmd)
        self.data_handler.log_command(cmd, response)
        return int(response)

    def set_update_interval(self, interval):
        """
        Sets the parameter update interval for scan steps.
        interval: int, 0-16
            0: 8 ms, 1: 16 ms, 2: 31 ms, 3: 78 ms, 4: 155 ms, 5: 469 ms,
            6: 938 ms, 7: 1.875 s, 8: 4.688 s, 9: 9.375 s, 10: 28.12 s,
            11: 56.25 s, 12: 112.5 s, 13: 5 m 37 s, 14: 11 m 15 s,
            15: 22 m 30 s, 16: 45 m 00 s
        """
        if not (0 <= int(interval) <= 16):
            raise ValueError("Interval index must be between 0 and 16.")
        cmd = f"SCNINRVL {int(interval)}"
        self.instrument.write(cmd)

    def get_update_interval(self):
        """
        Returns the parameter update interval index for scan steps.
        Returns: int (0-16)
        """
        cmd = "SCNINRVL?"
        response = self.instrument.query(cmd)
        self.data_handler.log_command(cmd, response)
        return int(response)
    def set_enable(self, state):
        """
        Turns scanning off (0/OFF) or on (1/ON).
        state: 'OFF', 'ON', 0, or 1
        """
        if isinstance(state, str):
            s = state.upper()
            if s == "OFF":
                i = 0
            elif s == "ON":
                i = 1
            else:
                raise ValueError("State must be 'OFF', 'ON', 0, or 1.")
        elif state in [0, 1]:
            i = int(state)
        else:
            raise ValueError("State must be 'OFF', 'ON', 0, or 1.")
        cmd = f"SCNENBL {i}"
        self.instrument.write(cmd)

    def get_enable(self):
        """
        Returns the scanning off/on state.
        Returns: int (0 for OFF, 1 for ON)
        """
        cmd = "SCNENBL?"
        response = self.instrument.query(cmd)
        self.data_handler.log_command(cmd, response)
        return int(response)

    def run(self):
        """
        Starts or resumes the scan.
        """
        cmd = "SCNRUN"
        self.instrument.write(cmd)

    def pause(self):
        """
        Pauses the scan.
        """
        cmd = "SCNPAUSE"
        self.instrument.write(cmd)

    def reset(self):
        """
        Resets the scan, sets the scan parameter to its begin value but does not start a scan.
        """
        cmd = "SCNRST"
        self.instrument.write(cmd)

    def get_state(self):
        """
        Returns the current state of the scan:
        0: off/disabled, 1: reset, 2: running, 3: paused, 4: done
        Returns: int
        """
        cmd = "SCNSTATE?"
        response = self.instrument.query(cmd)
        self.data_handler.log_command(cmd, response)
        return int(response)
    def set_frequency(self, j, f, unit="HZ"):
        """
        Sets the scan frequency for begin (j=0/BEG/BEGIN) or end (j=1/END).
        j: 0/'BEG'/'BEGIN' for begin, 1/'END' for end
        f: float, frequency value (1e-3 Hz ≤ f ≤ 5e5 Hz)
        unit: str, one of 'HZ', 'KHZ', 'MHZ'
        """
        valid_units = ["HZ", "KHZ", "MHZ"]
        if isinstance(j, str):
            jj = j.upper()
            if jj in ["BEG", "BEGIN"]:
                idx = 0
            elif jj == "END":
                idx = 1
            else:
                try:
                    idx = int(jj)
                except ValueError:
                    raise ValueError("j must be 0/'BEG'/'BEGIN' or 1/'END'.")
        elif j in [0, 1]:
            idx = int(j)
        else:
            raise ValueError("j must be 0/'BEG'/'BEGIN' or 1/'END'.")
        if unit.upper() not in valid_units:
            raise ValueError(f"Invalid unit. Choose from {valid_units}.")
        if not (1e-3 <= float(f) <= 5e5):
            raise ValueError("Frequency must be between 1 mHz and 500 kHz.")
        cmd = f"SCNFREQ {idx}, {float(f)} {unit.upper()}"
        self.instrument.write(cmd)

    def get_frequency(self, j):
        """
        Queries the scan frequency for begin (j=0/BEG/BEGIN) or end (j=1/END).
        j: 0/'BEG'/'BEGIN' for begin, 1/'END' for end
        Returns: float (Hz)
        """
        if isinstance(j, str):
            jj = j.upper()
            if jj in ["BEG", "BEGIN"]:
                idx = 0
            elif jj == "END":
                idx = 1
            else:
                try:
                    idx = int(jj)
                except ValueError:
                    raise ValueError("j must be 0/'BEG'/'BEGIN' or 1/'END'.")
        elif j in [0, 1]:
            idx = int(j)
        else:
            raise ValueError("j must be 0/'BEG'/'BEGIN' or 1/'END'.")
        cmd = f"SCNFREQ? {idx}"
        response = self.instrument.query(cmd)
        self.data_handler.log_command(cmd, response)
        return float(response)

    def set_amplitude(self, j, v, unit="V"):
        """
        Sets the scan reference amplitude for begin (j=0/BEG/BEGIN) or end (j=1/END).
        j: 0/'BEG'/'BEGIN' for begin, 1/'END' for end
        v: float, amplitude value (1e-9 V ≤ v ≤ 2.0 V)
        unit: str, one of 'NV', 'UV', 'MV', 'V'
        """
        valid_units = ["NV", "UV", "MV", "V"]
        if isinstance(j, str):
            jj = j.upper()
            if jj in ["BEG", "BEGIN"]:
                idx = 0
            elif jj == "END":
                idx = 1
            else:
                try:
                    idx = int(jj)
                except ValueError:
                    raise ValueError("j must be 0/'BEG'/'BEGIN' or 1/'END'.")
        elif j in [0, 1]:
            idx = int(j)
        else:
            raise ValueError("j must be 0/'BEG'/'BEGIN' or 1/'END'.")
        if unit.upper() not in valid_units:
            raise ValueError(f"Invalid unit. Choose from {valid_units}.")
        if not (1e-9 <= float(v) <= 2.0):
            raise ValueError("Amplitude must be between 1 nV and 2.0 V.")
        cmd = f"SCNAMP {idx}, {float(v)} {unit.upper()}"
        self.instrument.write(cmd)

    def get_amplitude(self, j):
        """
        Queries the scan reference amplitude for begin (j=0/BEG/BEGIN) or end (j=1/END).
        j: 0/'BEG'/'BEGIN' for begin, 1/'END' for end
        Returns: float (Volts)
        """
        if isinstance(j, str):
            jj = j.upper()
            if jj in ["BEG", "BEGIN"]:
                idx = 0
            elif jj == "END":
                idx = 1
            else:
                try:
                    idx = int(jj)
                except ValueError:
                    raise ValueError("j must be 0/'BEG'/'BEGIN' or 1/'END'.")
        elif j in [0, 1]:
            idx = int(j)
        else:
            raise ValueError("j must be 0/'BEG'/'BEGIN' or 1/'END'.")
        cmd = f"SCNAMP? {idx}"
        response = self.instrument.query(cmd)
        self.data_handler.log_command(cmd, response)
        return float(response)

    def set_dc_level(self, j, v, unit="V"):
        """
        Sets the scan reference DC level for begin (j=0/BEG/BEGIN) or end (j=1/END).
        j: 0/'BEG'/'BEGIN' for begin, 1/'END' for end
        v: float, DC level value (-5.0 V ≤ v ≤ 5.0 V)
        unit: str, one of 'NV', 'UV', 'MV', 'V'
        """
        valid_units = ["NV", "UV", "MV", "V"]
        if isinstance(j, str):
            jj = j.upper()
            if jj in ["BEG", "BEGIN"]:
                idx = 0
            elif jj == "END":
                idx = 1
            else:
                try:
                    idx = int(jj)
                except ValueError:
                    raise ValueError("j must be 0/'BEG'/'BEGIN' or 1/'END'.")
        elif j in [0, 1]:
            idx = int(j)
        else:
            raise ValueError("j must be 0/'BEG'/'BEGIN' or 1/'END'.")
        if unit.upper() not in valid_units:
            raise ValueError(f"Invalid unit. Choose from {valid_units}.")
        if not (-5.0 <= float(v) <= 5.0):
            raise ValueError("DC level must be between -5.00 V and +5.00 V.")
        cmd = f"SCNDC {idx}, {float(v)} {unit.upper()}"
        self.instrument.write(cmd)

    def get_dc_level(self, j):
        """
        Queries the scan reference DC level for begin (j=0/BEG/BEGIN) or end (j=1/END).
        j: 0/'BEG'/'BEGIN' for begin, 1/'END' for end
        Returns: float (Volts)
        """
        if isinstance(j, str):
            jj = j.upper()
            if jj in ["BEG", "BEGIN"]:
                idx = 0
            elif jj == "END":
                idx = 1
            else:
                try:
                    idx = int(jj)
                except ValueError:
                    raise ValueError("j must be 0/'BEG'/'BEGIN' or 1/'END'.")
        elif j in [0, 1]:
            idx = int(j)
        else:
            raise ValueError("j must be 0/'BEG'/'BEGIN' or 1/'END'.")
        cmd = f"SCNDC? {idx}"
        response = self.instrument.query(cmd)
        self.data_handler.log_command(cmd, response)
        return float(response)
    def set_aux1(self, j, v, unit="V"):
        """
        Sets the scan AuxOut1 value for begin (j=0/BEG/BEGIN) or end (j=1/END).
        j: 0/'BEG'/'BEGIN' for begin, 1/'END' for end
        v: float, voltage value (-10.5 V to +10.5 V)
        unit: str, one of 'NV', 'UV', 'MV', 'V'
        """
        valid_units = ["NV", "UV", "MV", "V"]
        if isinstance(j, str):
            jj = j.upper()
            if jj in ["BEG", "BEGIN"]:
                idx = 0
            elif jj == "END":
                idx = 1
            else:
                try:
                    idx = int(jj)
                except ValueError:
                    raise ValueError("j must be 0/'BEG'/'BEGIN' or 1/'END'.")
        elif j in [0, 1]:
            idx = int(j)
        else:
            raise ValueError("j must be 0/'BEG'/'BEGIN' or 1/'END'.")
        if unit.upper() not in valid_units:
            raise ValueError(f"Invalid unit. Choose from {valid_units}.")
        if not (-10.5 <= float(v) <= 10.5):
            raise ValueError("Voltage must be between -10.5 V and +10.5 V.")
        cmd = f"SCNAUX1 {idx}, {float(v)} {unit.upper()}"
        self.instrument.write(cmd)

    def get_aux1(self, j):
        """
        Queries the scan AuxOut1 value for begin (j=0/BEG/BEGIN) or end (j=1/END).
        j: 0/'BEG'/'BEGIN' for begin, 1/'END' for end
        Returns: float (Volts)
        """
        if isinstance(j, str):
            jj = j.upper()
            if jj in ["BEG", "BEGIN"]:
                idx = 0
            elif jj == "END":
                idx = 1
            else:
                try:
                    idx = int(jj)
                except ValueError:
                    raise ValueError("j must be 0/'BEG'/'BEGIN' or 1/'END'.")
        elif j in [0, 1]:
            idx = int(j)
        else:
            raise ValueError("j must be 0/'BEG'/'BEGIN' or 1/'END'.")
        cmd = f"SCNAUX1? {idx}"
        response = self.instrument.query(cmd)
        self.data_handler.log_command(cmd, response)
        return float(response)

    def set_aux2(self, j, v, unit="V"):
        """
        Sets the scan AuxOut2 value for begin (j=0/BEG/BEGIN) or end (j=1/END).
        j: 0/'BEG'/'BEGIN' for begin, 1/'END' for end
        v: float, voltage value (-10.5 V to +10.5 V)
        unit: str, one of 'NV', 'UV', 'MV', 'V'
        """
        valid_units = ["NV", "UV", "MV", "V"]
        if isinstance(j, str):
            jj = j.upper()
            if jj in ["BEG", "BEGIN"]:
                idx = 0
            elif jj == "END":
                idx = 1
            else:
                try:
                    idx = int(jj)
                except ValueError:
                    raise ValueError("j must be 0/'BEG'/'BEGIN' or 1/'END'.")
        elif j in [0, 1]:
            idx = int(j)
        else:
            raise ValueError("j must be 0/'BEG'/'BEGIN' or 1/'END'.")
        if unit.upper() not in valid_units:
            raise ValueError(f"Invalid unit. Choose from {valid_units}.")
        if not (-10.5 <= float(v) <= 10.5):
            raise ValueError("Voltage must be between -10.5 V and +10.5 V.")
        cmd = f"SCNAUX2 {idx}, {float(v)} {unit.upper()}"
        self.instrument.write(cmd)

    def get_aux2(self, j):
        """
        Queries the scan AuxOut2 value for begin (j=0/BEG/BEGIN) or end (j=1/END).
        j: 0/'BEG'/'BEGIN' for begin, 1/'END' for end
        Returns: float (Volts)
        """
        if isinstance(j, str):
            jj = j.upper()
            if jj in ["BEG", "BEGIN"]:
                idx = 0
            elif jj == "END":
                idx = 1
            else:
                try:
                    idx = int(jj)
                except ValueError:
                    raise ValueError("j must be 0/'BEG'/'BEGIN' or 1/'END'.")
        elif j in [0, 1]:
            idx = int(j)
        else:
            raise ValueError("j must be 0/'BEG'/'BEGIN' or 1/'END'.")
        cmd = f"SCNAUX2? {idx}"
        response = self.instrument.query(cmd)
        self.data_handler.log_command(cmd, response)
        return float(response)

class Data:
    """Commands to control and retrieve data from the instrument."""
    def __init__(self, instrument, data_handler):
        self.instrument = instrument
        self.data_handler = data_handler
        self.transfer = self.Transfer(instrument, data_handler)
        self.capture = self.Capture(instrument, data_handler)
        self.ethernet_streaming = self.Ethernet_Streaming(instrument, data_handler)
        
    class Transfer:
        """Commands to transfer data to/from the instrument."""
        def __init__(self, instrument, data_handler):
            self.instrument = instrument
            self.data_handler = data_handler

        def get_data_channel_value(self, channel):
            """
            Queries the value of a data channel.
            channel: 'DAT1', 'DAT2', 'DAT3', 'DAT4', or int 0-3
            Returns: float
            """
            channel_map = {'DAT1': 0, 'DAT2': 1, 'DAT3': 2, 'DAT4': 3}
            if isinstance(channel, str):
                ch = channel.upper()
                if ch in channel_map:
                    j = channel_map[ch]
                else:
                    try:
                        j = int(ch)
                    except ValueError:
                        raise ValueError("Channel must be 'DAT1', 'DAT2', 'DAT3', 'DAT4', or integer 0-3.")
            elif channel in [0, 1, 2, 3]:
                j = int(channel)
            else:
                raise ValueError("Channel must be 'DAT1', 'DAT2', 'DAT3', 'DAT4', or integer 0-3.")

            cmd = f"OUTR? {j}"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return float(response)

        def get_parameter_value(self, param):
            """
            Queries the value of a single lock-in parameter.
            param: int 0-16 or string enumeration (see documentation)
            Returns: float
            """
            param_map = {
                'X': 0, 'Y': 1, 'R': 2, 'THETA': 3, 'IN1': 4, 'IN2': 5, 'IN3': 6, 'IN4': 7,
                'XNOISE': 8, 'YNOISE': 9, 'OUT1': 10, 'OUT2': 11, 'PHASE': 12, 'SAMP': 13,
                'LEVEL': 14, 'FINT': 15, 'FEXT': 16
            }
            if isinstance(param, str):
                p = param.upper()
                if p in param_map:
                    j = param_map[p]
                else:
                    try:
                        j = int(p)
                    except ValueError:
                        raise ValueError("Parameter must be a valid name or integer 0-16.")
            elif isinstance(param, int) and 0 <= param <= 16:
                j = int(param)
            else:
                raise ValueError("Parameter must be a valid name or integer 0-16.")

            cmd = f"OUTP? {j}"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return float(response)

        def get_parameters_values(self, *params):
            """
            Queries the values of 2 or 3 lock-in parameters at a single instant.
            params: 2 or 3 parameter names or indices (see documentation)
            Returns: tuple of floats
            """
            if not (2 <= len(params) <= 3):
                raise ValueError("SNAP? requires 2 or 3 parameters.")
            param_map = {
                'X': 0, 'Y': 1, 'R': 2, 'THETA': 3, 'IN1': 4, 'IN2': 5, 'IN3': 6, 'IN4': 7,
                'XNOISE': 8, 'YNOISE': 9, 'OUT1': 10, 'OUT2': 11, 'PHASE': 12, 'SAMP': 13,
                'LEVEL': 14, 'FINT': 15, 'FEXT': 16
            }
            indices = []
            for param in params:
                if isinstance(param, str):
                    p = param.upper()
                    if p in param_map:
                        indices.append(str(param_map[p]))
                    else:
                        try:
                            indices.append(str(int(p)))
                        except ValueError:
                            raise ValueError("Parameter must be a valid name or integer 0-16.")
                elif isinstance(param, int) and 0 <= param <= 16:
                    indices.append(str(param))
                else:
                    raise ValueError("Parameter must be a valid name or integer 0-16.")
            cmd = f"SNAP? {', '.join(indices)}"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return tuple(float(x) for x in response.strip().split(','))

        def get_display_parameters(self):
            """
            Queries the values of the 4 parameters presently displayed as Data 1 through Data 4, at a single instant.
            Returns: tuple of 4 floats
            """
            cmd = "SNAPD?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return tuple(float(x) for x in response.strip().split(','))
        
    class Capture:
        """The SR860 can capture data points in an internal capture buffer. These commands control this capture buffer."""
        def __init__(self, instrument, data_handler):
            self.instrument = instrument
            self.data_handler = data_handler
        def set_length(self, n):
            """
            Sets the capture buffer length in kbytes.
            n: int, 1 ≤ n ≤ 4096 (must be even, will be rounded up if odd)
            """
            if not (1 <= int(n) <= 4096):
                raise ValueError("Capture length n must be between 1 and 4096.")
            n = int(n)
            if n % 2 != 0:
                n += 1
            cmd = f"CAPTURELEN {n}"
            self.instrument.write(cmd)

        def get_length(self):
            """
            Queries the capture buffer length in kbytes.
            Returns: int
            """
            cmd = "CAPTURELEN?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return int(response)

        def set_config(self, config):
            """
            Sets the capture configuration.
            config: 'X', 'XY', 'RT', 'XYRT', or int 0-3
                0: X
                1: X and Y
                2: R and Theta
                3: X, Y, R, and Theta
            """
            config_map = {'X': 0, 'XY': 1, 'RT': 2, 'XYRT': 3}
            if isinstance(config, str):
                c = config.upper()
                if c in config_map:
                    i = config_map[c]
                else:
                    try:
                        i = int(c)
                    except ValueError:
                        raise ValueError("Config must be 'X', 'XY', 'RT', 'XYRT', or integer 0-3.")
            elif config in [0, 1, 2, 3]:
                i = int(config)
            else:
                raise ValueError("Config must be 'X', 'XY', 'RT', 'XYRT', or integer 0-3.")
            cmd = f"CAPTURECFG {i}"
            self.instrument.write(cmd)

        def get_config(self):
            """
            Queries the capture configuration.
            Returns: int (0=X, 1=XY, 2=RT, 3=XYRT)
            """
            cmd = "CAPTURECFG?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return int(response)
        def get_max_rate(self):
            """
            Queries the maximum allowed capture rate (at the current time constant) in Hz.
            Returns: float
            """
            cmd = "CAPTURERATEMAX?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return float(response)

        def set_rate(self, n):
            """
            Sets the capture rate to the maximum rate divided by 2^n.
            n: int, 0 ≤ n ≤ 20
            """
            if not (0 <= int(n) <= 20):
                raise ValueError("n must be between 0 and 20.")
            cmd = f"CAPTURERATE {int(n)}"
            self.instrument.write(cmd)

        def get_rate(self):
            """
            Queries the actual capture rate in Hz (not the value n).
            Returns: float
            """
            cmd = "CAPTURERATE?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return float(response)

        def start(self, mode, trigger):
            """
            Starts data capture for either OneShot or Continuous acquisition, with specified trigger mode.
            mode: 'ONE', 'ONESHOT', 0 (OneShot), 'CONT', 'CONTINUOUS', 1 (Continuous)
            trigger: 'IMM', 'IMMEDIATE', 0 (Immediate), 'TRIG', 'TRIGSTART', 1 (Trigger start), 'SAMP', 'SAMPPERTRIG', 2 (Sample per trigger)
            """
            mode_map = {'ONE': 0, 'ONESHOT': 0, 'CONT': 1, 'CONTINUOUS': 1}
            trigger_map = {'IMM': 0, 'IMMEDIATE': 0, 'TRIG': 1, 'TRIGSTART': 1, 'SAMP': 2, 'SAMPPERTRIG': 2}
            if isinstance(mode, str):
                m = mode.upper()
                if m in mode_map:
                    i = mode_map[m]
                else:
                    try:
                        i = int(m)
                    except ValueError:
                        raise ValueError("mode must be 'ONE', 'ONESHOT', 0, 'CONT', 'CONTINUOUS', or 1.")
            elif mode in [0, 1]:
                i = int(mode)
            else:
                raise ValueError("mode must be 'ONE', 'ONESHOT', 0, 'CONT', 'CONTINUOUS', or 1.")

            if isinstance(trigger, str):
                t = trigger.upper()
                if t in trigger_map:
                    j = trigger_map[t]
                else:
                    try:
                        j = int(t)
                    except ValueError:
                        raise ValueError("trigger must be 'IMM', 'IMMEDIATE', 0, 'TRIG', 'TRIGSTART', 1, 'SAMP', 'SAMPPERTRIG', or 2.")
            elif trigger in [0, 1, 2]:
                j = int(trigger)
            else:
                raise ValueError("trigger must be 'IMM', 'IMMEDIATE', 0, 'TRIG', 'TRIGSTART', 1, 'SAMP', 'SAMPPERTRIG', or 2.")

            cmd = f"CAPTURESTART {i}, {j}"
            self.instrument.write(cmd)
        def stop(self):
            """
            Stops data capture in any mode.
            If capture is waiting for a hardware trigger, aborts the capture.
            If capture is in progress, halts capture and preserves data.
            """
            cmd = "CAPTURESTOP"
            self.instrument.write(cmd)

        def get_status(self):
            """
            Queries the data capture state.
            Returns: int (bitfield: 1=in progress, 2=triggered, 4=wrapped)
            """
            cmd = "CAPTURESTAT?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return int(response)

        def get_bytes(self):
            """
            Queries the number of bytes of data that have been captured thus far.
            Returns: int (number of bytes)
            """
            cmd = "CAPTUREBYTES?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return int(response)
        def get_progress(self):
            """
            Queries the number of kilobytes of data written during the most recent capture acquisition.
            Returns: int (kilobytes)
            """
            cmd = "CAPTUREPROG?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return int(response)

        def get_value(self, n):
            """
            Queries data from the capture buffer in plain text (ASCII) format.
            n: int, position in the buffer (0 = oldest)
            Returns: tuple of floats (one, two, or four values depending on CAPTURECFG)
            """
            cmd = f"CAPTUREVAL? {int(n)}"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return tuple(float(x) for x in response.strip().split(','))

        def get_binary(self, i, j):
            """
            Queries a binary block of capture buffer contents.
            i: int, offset in kbytes
            j: int, length in kbytes (max 64)
            Returns: bytes (raw binary block)
            """
            if not (0 <= int(j) <= 64):
                raise ValueError("j (length) must be between 0 and 64 kbytes.")
            cmd = f"CAPTUREGET? {int(i)},{int(j)}"
            self.instrument.write(cmd)
            # Wait for MAV (Message Available) bit to be set in the status byte
            while True:
                stb = self.instrument.read_stb()
                if stb & 0x10:
                    break
            raw_data = self.instrument.read_raw()
            self.data_handler.log_command(cmd, "<binary block>")
            return raw_data
    class Ethernet_Streaming:
        """The SR860 can stream data points continuously in real time over its ethernet interface"""
        def __init__(self, instrument, data_handler):
            self.instrument = instrument
            self.data_handler = data_handler
        def set_channel(self, config):
            """
            Configures the data streaming channel.
            config: 'X', 'XY', 'RT', 'XYRT', or int 0-3
                0: X
                1: X and Y
                2: R and Theta
                3: X, Y, R, and Theta
            """
            config_map = {'X': 0, 'XY': 1, 'RT': 2, 'XYRT': 3}
            if isinstance(config, str):
                c = config.upper()
                if c in config_map:
                    i = config_map[c]
                else:
                    try:
                        i = int(c)
                    except ValueError:
                        raise ValueError("Config must be 'X', 'XY', 'RT', 'XYRT', or integer 0-3.")
            elif config in [0, 1, 2, 3]:
                i = int(config)
            else:
                raise ValueError("Config must be 'X', 'XY', 'RT', 'XYRT', or integer 0-3.")
            cmd = f"STREAMCH {i}"
            self.instrument.write(cmd)

        def get_channel(self):
            """
            Returns the stream configuration index.
            Returns: int (0=X, 1=XY, 2=RT, 3=XYRT)
            """
            cmd = "STREAMCH?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return int(response)

        def get_rate_max(self):
            """
            Returns the maximum allowed streaming rate in Hz.
            Returns: float
            """
            cmd = "STREAMRATEMAX?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return float(response)

        def set_rate(self, n):
            """
            Sets the streaming rate to the maximum rate divided by 2^n.
            n: int, 0 ≤ n ≤ 20
            """
            if not (0 <= int(n) <= 20):
                raise ValueError("n must be between 0 and 20.")
            cmd = f"STREAMRATE {int(n)}"
            self.instrument.write(cmd)

        def get_rate(self):
            """
            Returns the streaming rate divisor n.
            Returns: int (0-20)
            """
            cmd = "STREAMRATE?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return int(response)
        def set_format(self, fmt):
            """
            Sets the stream data format.
            fmt: 'FLOAT32', 'INT16', 0, or 1
                0: float32 (4 bytes per point)
                1: int16 (2 bytes per point)
            """
            if isinstance(fmt, str):
                f = fmt.upper()
                if f in ["FLOAT32", "FLOAT", "F32"]:
                    i = 0
                elif f in ["INT16", "INT", "I16"]:
                    i = 1
                else:
                    raise ValueError("Format must be 'FLOAT32', 'INT16', 0, or 1.")
            elif fmt in [0, 1]:
                i = int(fmt)
            else:
                raise ValueError("Format must be 'FLOAT32', 'INT16', 0, or 1.")
            cmd = f"STREAMFMT {i}"
            self.instrument.write(cmd)

        def get_format(self):
            """
            Returns the stream data format.
            Returns: int (0 for float32, 1 for int16)
            """
            cmd = "STREAMFMT?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return int(response)

        def set_packet_size(self, size):
            """
            Sets the ethernet stream packet size.
            size: 1024, 512, 256, 128, or int 0-3
                0: 1024 bytes
                1: 512 bytes
                2: 256 bytes
                3: 128 bytes
            """
            size_map = {1024: 0, 512: 1, 256: 2, 128: 3}
            if isinstance(size, int) and size in size_map:
                i = size_map[size]
            elif size in [0, 1, 2, 3]:
                i = int(size)
            else:
                raise ValueError("Packet size must be 1024, 512, 256, 128, or integer 0-3.")
            cmd = f"STREAMPCKT {i}"
            self.instrument.write(cmd)

        def get_packet_size(self):
            """
            Returns the ethernet stream packet size index.
            Returns: int (0=1024, 1=512, 2=256, 3=128)
            """
            cmd = "STREAMPCKT?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return int(response)
        def set_port(self, port):
            """
            Sets the ethernet streaming port.
            port: int, 1024 ≤ port ≤ 65535
            """
            if not (1024 <= int(port) <= 65535):
                raise ValueError("Port must be between 1024 and 65535.")
            cmd = f"STREAMPORT {int(port)}"
            self.instrument.write(cmd)

        def get_port(self):
            """
            Returns the ethernet streaming port.
            Returns: int
            """
            cmd = "STREAMPORT?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return int(response)

        def set_option(self, option):
            """
            Sets advanced features of ethernet streaming.
            option: int, 0-3
                Bit 0 (1): Use little-endian if set, big-endian if not.
                Bit 1 (2): Enable data integrity checking if set.
            """
            if not (0 <= int(option) <= 3):
                raise ValueError("Option must be between 0 and 3.")
            cmd = f"STREAMOPTION {int(option)}"
            self.instrument.write(cmd)

        def get_option(self):
            """
            Returns the ethernet streaming option.
            Returns: int (bitfield)
            """
            cmd = "STREAMOPTION?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return int(response)

        def set_enable(self, state):
            """
            Turns ethernet data streaming off (0/OFF) or on (1/ON).
            state: 'OFF', 'ON', 0, or 1
            """
            if isinstance(state, str):
                s = state.upper()
                if s == "OFF":
                    i = 0
                elif s == "ON":
                    i = 1
                else:
                    raise ValueError("State must be 'OFF', 'ON', 0, or 1.")
            elif state in [0, 1]:
                i = int(state)
            else:
                raise ValueError("State must be 'OFF', 'ON', 0, or 1.")
            cmd = f"STREAM {i}"
            self.instrument.write(cmd)

        def get_enable(self):
            """
            Returns the ethernet streaming state.
            Returns: int (0 for OFF, 1 for ON)
            """
            cmd = "STREAM?"
            response = self.instrument.query(cmd)
            self.data_handler.log_command(cmd, response)
            return int(response)
        
class System:
    """general system commands."""
    def __init__(self, instrument, data_handler):
        self.instrument = instrument
        self.data_handler = data_handler
    def set_time(self, unit, value):
        """
        Sets the system clock value.
        unit: 'SEC', 'SECOND', 0; 'MIN', 'MINUTE', 1; 'HOUR', 2
        value: int
        """
        unit_map = {'SEC': 0, 'SECOND': 0, 'MIN': 1, 'MINUTE': 1, 'HOUR': 2}
        if isinstance(unit, str):
            u = unit.upper()
            if u in unit_map:
                j = unit_map[u]
            else:
                try:
                    j = int(u)
                except ValueError:
                    raise ValueError("Unit must be 'SEC', 'MIN', 'HOUR', or integer 0-2.")
        elif unit in [0, 1, 2]:
            j = int(unit)
        else:
            raise ValueError("Unit must be 'SEC', 'MIN', 'HOUR', or integer 0-2.")
        cmd = f"TIME {j}, {int(value)}"
        self.instrument.write(cmd)

    def get_time(self, unit):
        """
        Returns the system clock value for the specified unit.
        unit: 'SEC', 'SECOND', 0; 'MIN', 'MINUTE', 1; 'HOUR', 2
        Returns: int
        """
        unit_map = {'SEC': 0, 'SECOND': 0, 'MIN': 1, 'MINUTE': 1, 'HOUR': 2}
        if isinstance(unit, str):
            u = unit.upper()
            if u in unit_map:
                name = list(unit_map.keys())[list(unit_map.values()).index(unit_map[u])]
            else:
                try:
                    idx = int(u)
                    name = ['SEC', 'MIN', 'HOUR'][idx]
                except Exception:
                    raise ValueError("Unit must be 'SEC', 'MIN', 'HOUR', or integer 0-2.")
        elif unit in [0, 1, 2]:
            name = ['SEC', 'MIN', 'HOUR'][unit]
        else:
            raise ValueError("Unit must be 'SEC', 'MIN', 'HOUR', or integer 0-2.")
        cmd = f"TIME? {name}"
        response = self.instrument.query(cmd)
        self.data_handler.log_command(cmd, response)
        return int(response)

    def set_date(self, unit, value):
        """
        Sets the system date value.
        unit: 'DAY', 0; 'MON', 'MONTH', 1; 'YEAR', 2
        value: int (0-99)
        """
        unit_map = {'DAY': 0, 'MON': 1, 'MONTH': 1, 'YEAR': 2}
        if isinstance(unit, str):
            u = unit.upper()
            if u in unit_map:
                j = unit_map[u]
            else:
                try:
                    j = int(u)
                except ValueError:
                    raise ValueError("Unit must be 'DAY', 'MON', 'MONTH', 'YEAR', or integer 0-2.")
        elif unit in [0, 1, 2]:
            j = int(unit)
        else:
            raise ValueError("Unit must be 'DAY', 'MON', 'MONTH', 'YEAR', or integer 0-2.")
        if not (0 <= int(value) <= 99):
            raise ValueError("Value must be between 0 and 99.")
        cmd = f"DATE {j}, {int(value)}"
        self.instrument.write(cmd)

    def get_date(self, unit):
        """
        Returns the system date value for the specified unit.
        unit: 'DAY', 0; 'MON', 'MONTH', 1; 'YEAR', 2
        Returns: int
        """
        unit_map = {'DAY': 0, 'MON': 1, 'MONTH': 1, 'YEAR': 2}
        if isinstance(unit, str):
            u = unit.upper()
            if u in unit_map:
                name = list(unit_map.keys())[list(unit_map.values()).index(unit_map[u])]
            else:
                try:
                    idx = int(u)
                    name = ['DAY', 'MON', 'YEAR'][idx]
                except Exception:
                    raise ValueError("Unit must be 'DAY', 'MON', 'MONTH', 'YEAR', or integer 0-2.")
        elif unit in [0, 1, 2]:
            name = ['DAY', 'MON', 'YEAR'][unit]
        else:
            raise ValueError("Unit must be 'DAY', 'MON', 'MONTH', 'YEAR', or integer 0-2.")
        cmd = f"DATE? {name}"
        response = self.instrument.query(cmd)
        self.data_handler.log_command(cmd, response)
        return int(response)
    def set_blazex(self, mode):
        """
        Sets the rear panel BlazeX output.
        mode: 'BLAZEX', 'BLX', 0; 'BISYNC', 'BI', 1; 'UNISYNC', 'UNI', 2; or integer 0-2
        """
        if isinstance(mode, str):
            m = mode.upper()
            if m in ["BLAZEX", "BLX"]:
                i = 0
            elif m in ["BISYNC", "BI"]:
                i = 1
            elif m in ["UNISYNC", "UNI"]:
                i = 2
            else:
                raise ValueError("Mode must be 'BLAZEX', 'BISYNC', 'UNISYNC', or integer 0-2.")
        elif mode in [0, 1, 2]:
            i = int(mode)
        else:
            raise ValueError("Mode must be 'BLAZEX', 'BISYNC', 'UNISYNC', or integer 0-2.")
        cmd = f"BLAZEX {i}"
        self.instrument.write(cmd)

    def get_blazex(self):
        """
        Returns the BlazeX output selection.
        Returns: int (0=BLAZEX, 1=BISYNC, 2=UNISYNC)
        """
        cmd = "BLAZEX?"
        response = self.instrument.query(cmd)
        self.data_handler.log_command(cmd, response)
        return int(response)
    def set_system_sounds(self, state):
        """
        Turns system sounds on (0/ON) or off/mute (1/MUTE).
        state: 'ON', 'MUTE', 0, or 1
        """
        if isinstance(state, str):
            s = state.upper()
            if s == "ON":
                i = 0
            elif s in ["MUTE", "OFF"]:
                i = 1
            else:
                raise ValueError("State must be 'ON', 'MUTE', 0, or 1.")
        elif state in [0, 1]:
            i = int(state)
        else:
            raise ValueError("State must be 'ON', 'MUTE', 0, or 1.")
        cmd = f"KEYC {i}"
        self.instrument.write(cmd)

    def get_system_sounds(self):
        """
        Returns the system sounds state.
        Returns: int (0 for ON, 1 for MUTE)
        """
        cmd = "KEYC?"
        response = self.instrument.query(cmd)
        self.data_handler.log_command(cmd, response)
        return int(response)

    def set_screenshot_mode(self, mode):
        """
        Sets the screenshot mode.
        mode: 'SCREEN', 'PRNT', 'MONOCHROME', 0, 1, or 2
        """
        if isinstance(mode, str):
            m = mode.upper()
            if m in ["SCREEN", "SCR"]:
                i = 0
            elif m in ["PRNT", "PRINT"]:
                i = 1
            elif m in ["MONOCHROME", "MONO"]:
                i = 2
            else:
                raise ValueError("Mode must be 'SCREEN', 'PRNT', 'MONOCHROME', 0, 1, or 2.")
        elif mode in [0, 1, 2]:
            i = int(mode)
        else:
            raise ValueError("Mode must be 'SCREEN', 'PRNT', 'MONOCHROME', 0, 1, or 2.")
        cmd = f"PRMD {i}"
        self.instrument.write(cmd)

    def get_screenshot_mode(self):
        """
        Returns the screenshot mode.
        Returns: int (0=SCREEN, 1=PRNT, 2=MONOCHROME)
        """
        cmd = "PRMD?"
        response = self.instrument.query(cmd)
        self.data_handler.log_command(cmd, response)
        return int(response)

    def set_data_file_format(self, fmt):
        """
        Sets the data file format.
        fmt: 'CSV', 'MATFILE', 0, or 1
        """
        if isinstance(fmt, str):
            f = fmt.upper()
            if f == "CSV":
                i = 0
            elif f in ["MATFILE", "MAT"]:
                i = 1
            else:
                raise ValueError("Format must be 'CSV', 'MATFILE', 0, or 1.")
        elif fmt in [0, 1]:
            i = int(fmt)
        else:
            raise ValueError("Format must be 'CSV', 'MATFILE', 0, or 1.")
        cmd = f"SDFM {i}"
        self.instrument.write(cmd)

    def get_data_file_format(self):
        """
        Returns the data file format.
        Returns: int (0=CSV, 1=MATFILE)
        """
        cmd = "SDFM?"
        response = self.instrument.query(cmd)
        self.data_handler.log_command(cmd, response)
        return int(response)

    def set_file_name_prefix(self, prefix):
        """
        Sets the file name prefix to the string prefix (max 7 chars, DOS-allowed, uppercase).
        prefix: str
        """
        if not isinstance(prefix, str):
            raise ValueError("Prefix must be a string.")
        s = prefix.upper()
        if len(s) > 7:
            raise ValueError("Prefix must be at most 7 characters.")
        # DOS filename chars: A-Z, 0-9, _, no spaces or special chars
        if not re.match(r'^[A-Z0-9_]+$', s):
            raise ValueError("Prefix must contain only A-Z, 0-9, or _.")
        cmd = f'FBAS "{s}"'
        self.instrument.write(cmd)

    def get_file_name_prefix(self):
        """
        Returns the file name prefix.
        Returns: str
        """
        cmd = "FBAS?"
        response = self.instrument.query(cmd)
        self.data_handler.log_command(cmd, response)
        return response.strip().strip('"')

    def set_file_name_suffix(self, i):
        """
        Sets the file name suffix to value i.
        i: int
        """
        if not isinstance(i, int):
            raise ValueError("Suffix must be an integer.")
        if i < 0:
            raise ValueError("Suffix must be non-negative.")
        cmd = f"FNUM {i}"
        self.instrument.write(cmd)

    def get_file_name_suffix(self):
        """
        Returns the file name suffix.
        Returns: int
        """
        cmd = "FNUM?"
        response = self.instrument.query(cmd)
        self.data_handler.log_command(cmd, response)
        return int(response)
    def get_next_file_name(self):
        """
        Returns the next file name that will be used for saving data or screenshots.
        Returns: str
        """
        cmd = "FNXT?"
        response = self.instrument.query(cmd)
        self.data_handler.log_command(cmd, response)
        return response.strip().strip('"')

    def save_screenshot_to_usb(self):
        """
        Saves a screenshot to a USB memory stick (same as pressing [Screen Shot]).
        """
        cmd = "DCAP"
        self.instrument.write(cmd)

    def save_data_to_usb(self):
        """
        Saves data to a USB memory stick (same as pressing [Data Save]).
        """
        cmd = "SVDT"
        self.instrument.write(cmd)

    def set_local_remote(self, mode):
        """
        Sets the local/remote function.
        mode: 'LOCAL', 0; 'REMOTE', 1; 'LOCKOUT', 'LOCAL LOCKOUT', 2; or integer 0-2
        """
        if isinstance(mode, str):
            m = mode.upper()
            if m in ["LOCAL"]:
                i = 0
            elif m in ["REMOTE"]:
                i = 1
            elif m in ["LOCKOUT", "LOCAL LOCKOUT"]:
                i = 2
            else:
                raise ValueError("Mode must be 'LOCAL', 'REMOTE', 'LOCKOUT', or integer 0-2.")
        elif mode in [0, 1, 2]:
            i = int(mode)
        else:
            raise ValueError("Mode must be 'LOCAL', 'REMOTE', 'LOCKOUT', or integer 0-2.")
        cmd = f"LOCL {i}"
        self.instrument.write(cmd)

    def get_local_remote(self):
        """
        Queries the local/remote state.
        Returns: int (0=LOCAL, 1=REMOTE, 2=LOCAL LOCKOUT)
        """
        cmd = "LOCL?"
        response = self.instrument.query(cmd)
        self.data_handler.log_command(cmd, response)
        return int(response)

    def set_override_remote(self, state):
        """
        Sets the GPIB Override Remote state.
        state: 'OFF', 0; 'ON', 1; or integer 0-1
        """
        if isinstance(state, str):
            s = state.upper()
            if s == "OFF":
                i = 0
            elif s == "ON":
                i = 1
            else:
                raise ValueError("State must be 'OFF', 'ON', 0, or 1.")
        elif state in [0, 1]:
            i = int(state)
        else:
            raise ValueError("State must be 'OFF', 'ON', 0, or 1.")
        cmd = f"OVRM {i}"
        self.instrument.write(cmd)

    def get_override_remote(self):
        """
        Queries the GPIB Override Remote state.
        Returns: int (0=OFF, 1=ON)
        """
        cmd = "OVRM?"
        response = self.instrument.query(cmd)
        self.data_handler.log_command(cmd, response)
        return int(response)

    def set_power_on_status_clear(self, state):
        """
        Sets the value of the power-on status clear bit.
        state: 0 or 1
        """
        if state not in [0, 1]:
            raise ValueError("State must be 0 or 1.")
        cmd = f"*PSC {int(state)}"
        self.instrument.write(cmd)

    def get_power_on_status_clear(self):
        """
        Queries the value of the power-on status clear bit.
        Returns: int (0 or 1)
        """
        cmd = "*PSC?"
        response = self.instrument.query(cmd)
        self.data_handler.log_command(cmd, response)
        return int(response)

    def set_error_status_enable(self, *args):
        """
        Sets the error status enable register.
        Usage:
            set_error_status_enable(i)         # i: 0-255, sets the whole register
            set_error_status_enable(j, i)      # j: 0-7, i: 0 or 1, sets bit j
        """
        if len(args) == 1:
            i = int(args[0])
            if not (0 <= i <= 255):
                raise ValueError("i must be between 0 and 255.")
            cmd = f"ERRE {i}"
        elif len(args) == 2:
            j, i = int(args[0]), int(args[1])
            if not (0 <= j <= 7):
                raise ValueError("j must be between 0 and 7.")
            if i not in [0, 1]:
                raise ValueError("i must be 0 or 1.")
            cmd = f"ERRE {j}, {i}"
        else:
            raise ValueError("Usage: set_error_status_enable(i) or set_error_status_enable(j, i)")
        self.instrument.write(cmd)

    def get_error_status_enable(self, j=None):
        """
        Queries the error status enable register or a specific bit.
        j: None (returns 0-255), or int 0-7 (returns 0 or 1)
        """
        if j is None:
            cmd = "ERRE?"
        else:
            if not (0 <= int(j) <= 7):
                raise ValueError("j must be between 0 and 7.")
            cmd = f"ERRE? {int(j)}"
        response = self.instrument.query(cmd)
        self.data_handler.log_command(cmd, response)
        return int(response)

    def get_error_status(self, j=None):
        """
        Queries the error status byte or a specific bit.
        j: None (returns 0-255), or int 0-7 (returns 0 or 1)
        """
        if j is None:
            cmd = "ERRS?"
        else:
            if not (0 <= int(j) <= 7):
                raise ValueError("j must be between 0 and 7.")
            cmd = f"ERRS? {int(j)}"
        response = self.instrument.query(cmd)
        self.data_handler.log_command(cmd, response)
        return int(response)

    def set_lockin_status_enable(self, *args):
        """
        Sets the lock-in status enable register.
        Usage:
            set_lockin_status_enable(i)         # i: 0-4095, sets the whole register
            set_lockin_status_enable(j, i)      # j: 0-11, i: 0 or 1, sets bit j
        """
        if len(args) == 1:
            i = int(args[0])
            if not (0 <= i <= 4095):
                raise ValueError("i must be between 0 and 4095.")
            cmd = f"LIAE {i}"
        elif len(args) == 2:
            j, i = int(args[0]), int(args[1])
            if not (0 <= j <= 11):
                raise ValueError("j must be between 0 and 11.")
            if i not in [0, 1]:
                raise ValueError("i must be 0 or 1.")
            cmd = f"LIAE {j}, {i}"
        else:
            raise ValueError("Usage: set_lockin_status_enable(i) or set_lockin_status_enable(j, i)")
        self.instrument.write(cmd)

    def get_lockin_status_enable(self, j=None):
        """
        Queries the lock-in status enable register or a specific bit.
        j: None (returns 0-4095), or int 0-11 (returns 0 or 1)
        """
        if j is None:
            cmd = "LIAE?"
        else:
            if not (0 <= int(j) <= 11):
                raise ValueError("j must be between 0 and 11.")
            cmd = f"LIAE? {int(j)}"
        response = self.instrument.query(cmd)
        self.data_handler.log_command(cmd, response)
        return int(response)

    def get_lockin_status(self, j=None):
        """
        Queries the lock-in status word or a specific bit.
        j: None (returns 0-4095), or int 0-11 (returns 0 or 1)
        """
        if j is None:
            cmd = "LIAS?"
        else:
            if not (0 <= int(j) <= 11):
                raise ValueError("j must be between 0 and 11.")
            cmd = f"LIAS? {int(j)}"
        response = self.instrument.query(cmd)
        self.data_handler.log_command(cmd, response)
        return int(response)

    def get_overload_status(self):
        """
        Queries the present overload states of the lock-in.
        Returns: int (bitfield, see documentation)
        """
        cmd = "CUROVLDSTAT?"
        response = self.instrument.query(cmd)
        self.data_handler.log_command(cmd, response)
        return int(response)