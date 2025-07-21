import enum

class MeterFunction(enum.Enum):
    DCVOLTMETER = "VOLT:DC"
    ACVOLTMETER = "VOLT:AC"
    DCAMMETER = "CURR:DC"
    ACAMMETER = "CURR:AC"
    OHMMETER = "RES"
    FOHMMETER = "FRES"

class Terminal(enum.Enum):
    FRONT = "FRON"
    REAR = "REAR"

def set_function(self, meter_fn):
    """Set the measurement function."""
    self.write(f":SENS:FUNC \"{meter_fn}\"")

def get_function(self):
    """Get the current measurement function."""
    return self.query(":SENS:FUNC?")

def set_range(self, meter_fn, value: float):
    """Set the upper range for the selected function."""
    self.write(f":SENS:{meter_fn}:RANG {value}")

def enable_autorange(self, meter_fn, enable: bool = True):
    """Enable or disable autorange for the selected function."""
    val = 1 if enable else 0
    self.write(f":SENS:{meter_fn}:RANG:AUTO {val}")

def is_autorange_enabled(self, meter_fn):
    """Check if autorange is enabled for the selected function."""
    return bool(int(self.query(f":SENS:{meter_fn.value}:RANG:AUTO?")))

def set_resolution(self, meter_fn, value: float):
    """Set the resolution for the selected function."""
    self.write(f":SENS:{meter_fn.value}:RES {value}")

def set_trigger_count(self, count: int):
    """Set the trigger count."""
    self.write(f":TRIG:COUN {count}")

def set_trigger_delay(self, delay: float):
    """Set the trigger delay."""
    self.write(f":TRIG:DEL {delay}")

def set_trigger_source(self, source: str):
    """Set the trigger source. Allowed: BUS, IMM, EXT."""
    allowed = {"BUS", "IMM", "EXT"}
    src = source.upper()
    if src not in allowed:
        raise ValueError(f"Invalid trigger source: {source}")
    self.write(f":TRIG:SOUR {src}")

def set_arm_source(self, source: str):
    """Set the ARM source. Allowed: BUS, IMM, EXT."""
    allowed = {"BUS", "IMM", "EXT"}
    src = source.upper()
    if src not in allowed:
        raise ValueError(f"Invalid ARM source: {source}")
    self.write(f":TRIG:ARM:SOUR {src}")

def set_arm_count(self, count: int):
    """Set the ARM count."""
    self.write(f":TRIG:ARM:COUN {count}")

def set_terminal(self, terminal: Terminal):
    """Set the input terminal (FRONT or REAR)."""
    self.write(f":ROUT:TERM {terminal.value}")

def get_terminal(self):
    """Get the current input terminal."""
    val = self.query(":ROUT:TERM?")
    return Terminal(val.strip().upper())

def enable_offset_compensation(self, meter_fn, enable: bool = True):
    """Enable or disable offset compensation for resistance measurements."""
    if meter_fn not in {MeterFunction.OHMMETER, MeterFunction.FOHMMETER}:
        raise ValueError("Offset compensation only valid for resistance functions.")
    val = 1 if enable else 0
    self.write(f":SENS:{meter_fn.value}:OCOM {val}")

def is_offset_compensation_enabled(self, meter_fn):
    """Check if offset compensation is enabled for resistance measurements."""
    if meter_fn not in {MeterFunction.OHMMETER, MeterFunction.FOHMMETER}:
        raise ValueError("Offset compensation only valid for resistance functions.")
    return bool(int(self.query(f":SENS:{meter_fn.value}:OCOM?")))