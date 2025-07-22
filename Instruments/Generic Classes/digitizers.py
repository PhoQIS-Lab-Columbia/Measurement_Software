from time import sleep
from time import sleep
from EFileType import EFileType
from Instruments import Instrument
import pyvisa
from EInstrument import EInstrument
from SCPICommandTree.input import Input
from SCPICommandTree.sense import Sense
from SCPICommandTree.format import Format
from SCPICommandTree.trigger import Trigger
class Digitizer(Instrument.Instrument):
    def __init__(self, instru, name=None):
        super().__init__(instru, name)
        self.input = self.inputClass(instru)
        self.sense = self.senseClass(instru)
        self.format = self.formatClass(instru)
        self.trigger = self.triggerClass(instru)
        self.name = name
    class inputClass():
        def __init__(self, instrument):
            self.input_obj = Input(instrument)

        def set_input_coupling(self, coupling_type: str, input_num = None):
            """Selects AC or DC coupling for the specified signal, or GROund coupling.
            Parameters:
            coupling_type: AC|DC|GROund
            input_num: Optional. The input channel number (if applicable)."""
            self.input_obj.set_input_coupling(coupling_type, input_num)

        def get_input_coupling(self, input_num = None) -> str:
            """Returns the coupling type for the input signal ('AC', 'DC', or 'GROUND')."""
            self.input_obj.get_input_channel(input_num)
    
    class senseClass():
        def __init__(self, instrument):
            self.sense_obj = Sense(instrument)

        def set_sense_sweep_points(self, value: int):
            """Sets the number of points in a stepped sweep or acquisition.
            Parameters:
            value: The number of points (numeric value)."""
            self.sense_obj.set_sense_sweep_points(value)

        def get_sense_sweep_points(self) -> int:
            """Returns the number of points in a stepped sweep or acquisition."""
            return self.sense_obj.get_sense_sweep_points()
        
        def set_sense_sweep_time(self, value_seconds: float):
            """Sets the duration of the sweep or acquisition in seconds.
            Parameters:
            value_seconds: The duration in seconds (numeric value)."""
            self.sense_obj.set_sense_sweep_time(value_seconds)
        def get_sense_sweep_time(self) -> float:
            """Returns the duration of the sweep or acquisition in seconds."""
            return self.sense_obj.get_sense_sweep_time()
        
        def set_sense_sweep_tinterval(self, value_seconds: float):
            """Sets the time interval between points of the sweep or acquisition in seconds.
            Parameters:
            value_seconds: The time interval in seconds (numeric value)."""
            self.sense_obj.set_sense_sweep_tinterval(value_seconds)
            
        def get_sense_sweep_tinterval(self) -> float:
            """Returns the time interval between points of the sweep or acquisition in seconds."""
            return self.sense_obj.get_sense_sweep_tinterval()
        def get_sense_data(self, data_handle: str = None):
            """
            Returns measurement data from the instrument.
            Parameters:
            data_handle: (Optional) The data handle to specify which data to return.
            Returns: The measurement data as returned by the instrument.
            """
            return self.sense_obj.get_sense_data(data_handle)

        def set_sense_function(self, function_string: str):
            """
            Selects the sensor function(s) to be measured.
            Parameters:
            function_string: The function string specifying the sensor function(s).
            """
            self.sense_obj.set_sense_function(function_string)

        def get_sense_function(self) -> str:
            """
            Returns the currently selected sensor function(s).
            Returns: The function string specifying the sensor function(s).
            """
            return self.sense_obj.get_sense_function()

        def set_sense_function_concurrent(self, enable: bool):
            """
            Enables or disables concurrent measurement of multiple sensor functions.
            Parameters:
            enable: True to enable concurrent measurement, False to disable.
            """
            self.sense_obj.set_sense_function_concurrent(enable)

        def get_sense_function_concurrent(self) -> bool:
            """
            Returns True if concurrent measurement is enabled, False if disabled.
            Returns: Boolean indicating concurrent measurement state.
            """
            return self.sense_obj.get_sense_function_concurrent()

        def set_sense_function_off(self, sensor_functions: str):
            """
            Turns off the specified sensor function(s).
            Parameters:
            sensor_functions: The sensor function(s) to turn off.
            """
            self.sense_obj.set_sense_function_off(sensor_functions)

        def get_sense_function_off(self) -> list[str]:
            """
            Returns a list of sensor functions that are currently turned off.
            Returns: List of sensor function names.
            """
            return self.sense_obj.get_sense_function_off()

        def sense_function_off_all(self):
            """
            Turns off all sensor functions.
            """
            self.sense_obj.sense_function_off_all()

        def turn_sense_function_off_count(self) -> int:
            """
            Returns the number of sensor functions that are currently turned off.
            Returns: Integer count of off sensor functions.
            """
            return self.sense_obj.turn_sense_function_off()

        def turn_sense_function_on(self, sensor_functions: str):
            """
            Turns on the specified sensor function(s).
            Parameters:
            sensor_functions: The sensor function(s) to turn on.
            """
            self.sense_obj.turn_sense_function_on(sensor_functions)

        def which_sense_function_on(self) -> list[str]:
            """
            Returns a list of sensor functions that are currently turned on.
            Returns: List of sensor function names.
            """
            return self.sense_obj.which_sense_function_on()

        def sense_function_on_all(self):
            """
            Turns on all sensor functions.
            """
            self.sense_obj.sense_function_on_all()

        def get_sense_function_on_count(self) -> int:
            """
            Returns the number of sensor functions that are currently turned on.
            Returns: Integer count of on sensor functions.
            """
            return self.sense_obj.get_sense_function_on_count()

        def get_sense_function_state(self, sensor_function: str) -> bool:
            """
            Returns True if the specified sensor function is on, False if off.
            Parameters:
            sensor_function: The sensor function to query.
            Returns: Boolean indicating the state of the sensor function.
            """
            return self.sense_obj.get_sense_function_state(sensor_function)
    class formatClass():
        def __init__(self, instrument):
            self.instrument = instrument
            self.format_obj = Format(instrument)
        def set_format_data(self, data_type: str, length: float = None):
            """Sets the format for measurement data.
            Parameters:
            data_type: The type of data (e.g., "ASCII", "INT", "UINT", "REAL", "HEX", "OCT", "BIN", "PACK")."""
            self.format_obj.set_format_data(data_type, length)
        def get_format_data(self) -> tuple[str, float]:
            """Returns the selected data format type and its length.
            Returns: A tuple containing (data_type: str, length: float or None)."""
            return self.format_obj.get_format_data()
        
    class triggerClass():
        def __init__(self, instrument):
            self.instrument = instrument
            self.trigger_obj = Trigger(instrument)
        def initiate_immediate(self):
            """
            Causes all sequences to exit the IDLE state; they are initiated.
            The IMMediate command causes the trigger system to initiate and complete one full trigger cycle,
            returning to IDLE on completion.
            This command is an event and cannot be queried as there is no state associated with it.
            """
            self.trigger_obj.initiate_immediate()

        def initiate_immediate_all(self):
            """
            Causes all SEQuences to be INITiated, except those defined to behave otherwise.
            This command is an event and has no query form.
            """
            self.trigger_obj.initiate_immediate_all()

        def abort(self):
            """
            Resets the trigger system and places all trigger sequences in the IDLE state.
            Any actions related to the trigger system that are in progress shall also be aborted.
            This command is an event and has no associated *RST condition or query form.
            """
            self.trigger_obj.abort()

        def trigger(self):
            """
            Purpose of the TRIGger subsystem is to qualify a single event before enabling
            the triggered sequence operation, such as enabling a sweep, starting a measurement,
            or changing the state of the device.
            This command is an event and has no query form.
            """
            self.trigger_obj.trigger()

        def set_trigger_sequence_coupling(self, coupling_type: str, sequence_number: int = None):
            """
            Selects AC or DC coupling for the SOURced signal. Only has effect if the source
            for the event detector is an analog electrical signal.
            Parameters:
            coupling_type: "AC" or "DC".
            sequence_number: Optional. The numeric suffix (sequence number) to apply the setting to.
            Notes: At *RST, this value is device-dependent.
            """
            self.trigger_obj.set_trigger_sequence_coupling(coupling_type, sequence_number)

        def get_trigger_sequence_coupling(self, sequence_number: int = None) -> str:
            """
            Queries the coupling type for the TRIGger sequence.
            Parameters:
            sequence_number: Optional. The numeric suffix (sequence number) to query.
            Returns: The coupling type ("AC" or "DC").
            """
            return self.trigger_obj.get_trigger_sequence_coupling(sequence_number)

        def set_trigger_sequence_level(self, value: float):
            """
            Qualifies the characteristic of the selected SOURce signal that generates an event.
            Only has effect if the source is an analog electrical signal.
            Units default to current amplitude unit.
            Parameters:
            value: The level value (numeric value).
            Notes: At *RST, this value is instrument-dependent.
            """
            self.trigger_obj.set_trigger_sequence_level(value)

        def get_trigger_sequence_level(self) -> float:
            """
            Queries the level value for the TRIGger sequence.
            Returns: The level value.
            """
            return self.trigger_obj.get_trigger_sequence_level()

        def set_trigger_sequence_slope(self, slope_type: str):
            """
            Qualifies whether the event occurs on the rising edge, falling edge, or either edge of the signal.
            Parameters:
            slope_type: "POSitive", "NEGative", or "EITHer".
            Notes: At *RST, this value is set to POS.
            """
            self.trigger_obj.set_trigger_sequence_slope(slope_type)

        def get_trigger_sequence_slope(self) -> str:
            """
            Queries the slope type for the TRIGger sequence.
            Returns: The slope type ("POSitive", "NEGative", or "EITHer").
            """
            return self.trigger_obj.get_trigger_sequence_slope()

        def set_trigger_sequence_source(self, source_type: str, source_index: int = None):
            """
            Selects the source for the event detector. Only one source may be specified at a time.
            Parameters:
            source_type: The type of source (e.g., "AINTernal", "BUS", "ECLTrg", "EXTernal", "HOLD",
                 "IMMediate", "INTernal", "LINE", "LINK", "MANual", "OUTPut", "TIMer", "TTLTrg").
            source_index: Optional. Numeric suffix for sources like ECLTrg, EXTernal, INTernal, OUTPut, TTLTrg.
            Notes: At *RST, IMMediate shall be selected as the SOURce.
            """
            self.trigger_obj.set_trigger_sequence_source(source_type, source_index)

        def get_trigger_sequence_source(self) -> str:
            """
            Queries the source for the event detector for the TRIGger sequence.
            Returns: The source type string (e.g., "IMMediate", "TTLTrg0").
            """
            return self.trigger_obj.get_trigger_sequence_source()
        