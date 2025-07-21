from Instruments import Instrument
import pyvisa

class Instrument(Instrument.Mandatory):

    def __init__(self, instrument):
        
        self.name = "Insert_instrument_name_here"
        self.instrument = instrument
    
    #TODO: Add SCPI functions below

    def enable_conversion(self, channel=1, trace=None):
        """
        Enable S-parameter conversion for a channel or trace.
        """
        if not (1 <= channel <= 16):
            raise ValueError("Channel must be between 1 and 16.")
        cmd = f":CALC{channel}"
        if trace is not None:
            if not (1 <= trace <= 16):
                raise ValueError("Trace must be between 1 and 16.")
            cmd += f":TRAC{trace}:CONV:STAT 1"
        else:
            cmd += ":CONV:STAT 1"
        self.instrument.write(cmd)

    def disable_conversion(self, channel=1, trace=None):
        """
        Disable S-parameter conversion for a channel or trace.
        """
        if not (1 <= channel <= 16):
            raise ValueError("Channel must be between 1 and 16.")
        cmd = f":CALC{channel}"
        if trace is not None:
            if not (1 <= trace <= 16):
                raise ValueError("Trace must be between 1 and 16.")
            cmd += f":TRAC{trace}:CONV:STAT 0"
        else:
            cmd += ":CONV:STAT 0"
        self.instrument.write(cmd)

    def is_conversion_enabled(self, channel=1, trace=None):
        """
        Check if S-parameter conversion is enabled for a channel or trace.
        Returns True if enabled, False otherwise.
        """
        if not (1 <= channel <= 16):
            raise ValueError("Channel must be between 1 and 16.")
        cmd = f":CALC{channel}"
        if trace is not None:
            if not (1 <= trace <= 16):
                raise ValueError("Trace must be between 1 and 16.")
            cmd += f":TRAC{trace}:CONV:STAT?"
        else:
            cmd += ":CONV:STAT?"
        result = int(self.instrument.query(cmd))
        return result == 1

    def abort_sweep(self):
        """
        Abort the current sweep.
        """
        self.instrument.write(":ABOR")

    def set_conversion_state(self, state, channel=1, trace=None):
        """
        Set conversion state ON/OFF for a channel or trace.
        state: 1 (ON) or 0 (OFF)
        """
        if state not in (0, 1):
            raise ValueError("State must be 0 (OFF) or 1 (ON).")
        if not (1 <= channel <= 16):
            raise ValueError("Channel must be between 1 and 16.")
        cmd = f":CALC{channel}"
        if trace is not None:
            if not (1 <= trace <= 16):
                raise ValueError("Trace must be between 1 and 16.")
            cmd += f":TRAC{trace}:CONV:STAT {state}"
        else:
            cmd += f":CONV:STAT {state}"
            self.instrument.write(cmd)
        

    def enable_continuous_initiation(self, channel=1):
        """
        Enable continuous sweep initiation for a channel.
        """
        if not (1 <= channel <= 16):
            raise ValueError("Channel must be between 1 and 16.")
        cmd = f":INIT{channel}:CONT 1"
        self.instrument.write(cmd)

    def disable_continuous_initiation(self, channel=1):
        """
        Disable continuous sweep initiation for a channel.
        """
        if not (1 <= channel <= 16):
            raise ValueError("Channel must be between 1 and 16.")
        cmd = f":INIT{channel}:CONT 0"
        self.instrument.write(cmd)

    def is_continuous_initiation_enabled(self, channel=1):
        """
        Check if continuous sweep initiation is enabled for a channel.
        Returns True if enabled, False otherwise.
        """
        if not (1 <= channel <= 16):
            raise ValueError("Channel must be between 1 and 16.")
        cmd = f":INIT{channel}:CONT?"
        result = int(self.instrument.query(cmd))
        return result == 1

    def enable_single_trigger(self, channel=1):
        """
        Enable single trigger mode for a channel.
        """
        if not (1 <= channel <= 16):
            raise ValueError("Channel must be between 1 and 16.")
        cmd = f":INIT{channel}:SING"
        self.instrument.write(cmd)

    def set_trigger_source(self, source, channel=1):
        """
        Set trigger source for a channel.
        Allowed values: 'INT', 'EXT', 'BUS'
        """
        allowed_sources = {'INT', 'EXT', 'BUS'}
        if source not in allowed_sources:
            raise ValueError(f"Source must be one of {allowed_sources}.")
        if not (1 <= channel <= 16):
            raise ValueError("Channel must be between 1 and 16.")
        cmd = f":TRIG{channel}:SOUR {source}"
        self.instrument.write(cmd)

    def get_trigger_source(self, channel=1):
        """
        Get trigger source for a channel.
        Returns one of 'INT', 'EXT', 'BUS'.
        """
        if not (1 <= channel <= 16):
            raise ValueError("Channel must be between 1 and 16.")
        cmd = f":TRIG{channel}:SOUR?"
        result = self.instrument.query(cmd).strip()
        allowed_sources = {'INT', 'EXT', 'BUS'}
        if result not in allowed_sources:
            raise RuntimeError(f"Unexpected trigger source: {result}")
        return result

    def enable_conversion_selected(self, channel=1):
        """
        Enable S-parameter conversion for the selected trace of a channel.
        """
        if not (1 <= channel <= 16):
            raise ValueError("Channel must be between 1 and 16.")
        cmd = f":CALC{channel}:SEL:CONV:STAT 1"
        self.instrument.write(cmd)

    def disable_conversion_selected(self, channel=1):
        """
        Disable S-parameter conversion for the selected trace of a channel.
        """
        if not (1 <= channel <= 16):
            raise ValueError("Channel must be between 1 and 16.")
        cmd = f":CALC{channel}:SEL:CONV:STAT 0"
        self.instrument.write(cmd)

    def is_conversion_selected_enabled(self, channel=1):
        """
        Check if S-parameter conversion is enabled for the selected trace of a channel.
        Returns True if enabled, False otherwise.
        """
        if not (1 <= channel <= 16):
            raise ValueError("Channel must be between 1 and 16.")
        cmd = f":CALC{channel}:SEL:CONV:STAT?"
        result = int(self.instrument.query(cmd))
        return result == 1