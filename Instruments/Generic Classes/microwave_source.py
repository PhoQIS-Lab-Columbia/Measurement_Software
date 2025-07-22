from time import sleep
from time import sleep
from EFileType import EFileType
from Instruments import Instrument
import pyvisa
from EInstrument import EInstrument
from SCPICommandTree.source import Source
from SCPICommandTree.output import Output
from SCPICommandTree.trigger import Trigger
from SCPICommandTree.unit import Unit

class MicrowaveSource(Instrument.Instrument):

    def __init__(self, instru, name=None):
        super().__init__(instru, name)
        self.source = self.sourceClass(instru)
        self.output = self.outputClass(instru)
        self.trigger = self.triggerClass(instru)
        self.unit = self.unitClass(instru)
        self.name = name
    class sourceClass:
        def __init__(self, instrument):
            self.source_obj = Source(instrument)
        def set_frequency_cw(self, value: float):
            """
            Sets the continuous wave (CW) frequency of the source.
            Parameters:
            value (float): The frequency in Hz.
            """
            self.source_obj.set_source_frequency_cw(value)

        def get_frequency_cw(self) -> float:
            """
            Returns the continuous wave (CW) frequency of the source.
            Returns:
            float: The frequency in Hz.
            """
            return self.source_obj.get_source_frequency_cw()

        def set_frequency_fixed(self, value: float):
            """
            Sets the fixed frequency of the source.
            Parameters:
            value (float): The frequency in Hz.
            """
            self.source_obj.set_source_frequency_fixed(value)

        def get_frequency_fixed(self) -> float:
            """
            Returns the fixed frequency of the source.
            Returns:
            float: The frequency in Hz.
            """
            return self.source_obj.get_source_frequency_fixed()

        def set_power_level_immediate_amplitude(self, value: float):
            """
            Sets the immediate amplitude of the power level.
            Parameters:
            value (float): The amplitude value (units depend on instrument).
            """
            self.source_obj.set_source_power_level_immediate_amplitude(value)

        def get_power_level_immediate_amplitude(self) -> float:
            """
            Returns the immediate amplitude of the power level.
            Returns:
            float: The amplitude value.
            """
            return self.source_obj.get_source_power_level_immediate_amplitude()

        def set_power_alc_state(self, enable: bool):
            """
            Enables or disables the Automatic Level Control (ALC) for power.
            Parameters:
            enable (bool): True to enable ALC, False to disable.
            """
            self.source_obj.set_source_power_alc_state(enable)

        def get_power_alc_state(self) -> bool:
            """
            Returns the state of the Automatic Level Control (ALC) for power.
            Returns:
            bool: True if ALC is enabled, False otherwise.
            """
            return self.source_obj.get_source_power_alc_state()
        
    class outputClass:
        def __init__(self, instrument):
            self.output_obj = Output(instrument)
        def set_output_state(self, enable: bool):
            """
            Controls whether the output terminals are open or closed.
            Parameters:
            enable (bool): True to close terminals, False for maximum isolation.
            """
            self.output_obj.set_output_state(enable)

        def get_output_state(self) -> bool:
            """
            Returns True if the output terminals are closed, False if open.
            Returns:
            bool: Output state.
            """
            return self.output_obj.get_output_state()
    class triggerClass:
        def __init__(self, instrument):
            self.trigger_obj = Trigger(instrument)
        def set_initiate_continuous(self, enable: bool):
            """
            Selects whether the trigger system is continuously initiated or not.
            Parameters:
            enable (bool): True for continuous initiation, False to remain in IDLE until IMMediate.
            """
            self.trigger_obj.set_initiate_continuous(enable)

        def get_initiate_continuous(self) -> bool:
            """
            Queries whether the trigger system is continuously initiated.
            Returns:
            bool: True if continuous initiation, False otherwise.
            """
            return self.trigger_obj.get_initiate_continuous()

        def set_initiate_continuous_all(self, enable: bool):
            """
            Sets whether or not all sequences are continuously initiated.
            Parameters:
            enable (bool): True to continuously initiate all sequences, False otherwise.
            """
            self.trigger_obj.set_initiate_continuous_all(enable)

        def get_initiate_continuous_all(self) -> bool:
            """
            Queries whether or not all sequences are continuously initiated.
            Returns:
            bool: True if all sequences are continuously initiated, False otherwise.
            """
            return self.trigger_obj.get_initiate_continuous_all()

        def set_initiate_continuous_name(self, sequence_name: str, enable: bool):
            """
            Sets whether or not the SEQuence with the alias specified by <sequence_name> is continuously initiated.
            Parameters:
            sequence_name (str): The character program data for the sequence alias.
            enable (bool): True for continuous initiation, False otherwise.
            """
            self.trigger_obj.set_initiate_continuous_name(sequence_name, enable)

        def get_initiate_continuous_name(self, sequence_name: str) -> bool:
            """
            Queries whether or not the SEQuence with the alias specified by <sequence_name> is continuously initiated.
            Parameters:
            sequence_name (str): The character program data for the sequence alias.
            Returns:
            bool: True if continuously initiated, False otherwise.
            """
            return self.trigger_obj.get_initiate_continuous_name(sequence_name)

        def set_initiate_continuous_sequence(self, sequence_number: int, enable: bool):
            """
            Sets whether or not the specified SEQuence is continuously initiated.
            Parameters:
            sequence_number (int): The numeric suffix on SEQuence corresponds to the sequence number.
            enable (bool): True for continuous initiation, False otherwise.
            """
            self.trigger_obj.set_initiate_continuous_sequence(sequence_number, enable)

        def get_initiate_continuous_sequence(self, sequence_number: int) -> bool:
            """
            Queries whether or not the specified SEQuence is continuously initiated.
            Parameters:
            sequence_number (int): The numeric suffix on SEQuence corresponds to the sequence number.
            Returns:
            bool: True if continuously initiated, False otherwise.
            """
            return self.trigger_obj.get_initiate_continuous_sequence(sequence_number)

        def initiate_immediate(self):
            """
            Causes all sequences to exit the IDLE state; they are initiated.
            The IMMediate command causes the trigger system to initiate and complete one full trigger cycle,
            returning to IDLE on completion.
            """
            self.trigger_obj.initiate_immediate()

        def initiate_immediate_all(self):
            """
            Causes all SEQuences to be INITiated, except those defined to behave otherwise.
            """
            self.trigger_obj.initiate_immediate_all()

        def initiate_immediate_name(self, sequence_name: str):
            """
            Causes the SEQuence with the alias specified by <sequence_name> to be INITiated.
            Parameters:
            sequence_name (str): The character program data for the sequence alias.
            """
            self.trigger_obj.initiate_immediate_name(sequence_name)

        def initiate_immediate_sequence(self, sequence_number: int):
            """
            Causes the specified SEQuence to be INITiated.
            Parameters:
            sequence_number (int): The numeric suffix on SEQuence corresponds to the sequence number.
            """
            self.trigger_obj.initiate_immediate_sequence(sequence_number)

        def abort(self):
            """
            Resets the trigger system and places all trigger sequences in the IDLE state.
            Any actions related to the trigger system that are in progress shall also be aborted.
            """
            self.trigger_obj.abort()

        def trigger(self):
            """
            Qualifies a single event before enabling the triggered sequence operation, such as enabling a sweep,
            starting a measurement, or changing the state of the device.
            """
            self.trigger_obj.instrument.write(":TRIGger")

        def trigger_sequence(self):
            """
            Initiates all trigger sequences as a group, except those defined otherwise.
            """
            self.trigger_obj.instrument.write(":TRIGger:SEQuence")

        def trigger_sequence_immediate(self):
            """
            Provides a one-time override of the normal process of the downward traverse of the event detection layer.
            Causes immediate exit of the specified event detection layer if the trigger system is in that layer.
            """
            self.trigger_obj.trigger_sequence_immediate()

        def set_trigger_sequence_source(self, source_type: str, source_index: int = None):
            """
            Selects the source for the event detector. Only one source may be specified at a time.
            Parameters:
            source_type (str): The type of source (e.g., "AINTernal", "BUS", "ECLTrg", "EXTernal", "HOLD",
                       "IMMediate", "INTernal", "LINE", "LINK", "MANual", "OUTPut", "TIMer", "TTLTrg").
            source_index (int, optional): Numeric suffix for sources like ECLTrg, EXTernal, INTernal, OUTPut, TTLTrg.
            """
            self.trigger_obj.set_trigger_sequence_source(source_type, source_index)

        def get_trigger_sequence_source(self) -> str:
            """
            Queries the source for the event detector for the TRIGger sequence.
            Returns:
            str: The source type string (e.g., "IMMediate", "TTLTrg0").
            """
            return self.trigger_obj.get_trigger_sequence_source()
