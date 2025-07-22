from time import sleep
from time import sleep
from EFileType import EFileType
from Instruments import Instrument
import pyvisa
from EInstrument import EInstrument
from SCPICommandTree.source import Source
from SCPICommandTree.output import Output
from SCPICommandTree.status import Status
from SCPICommandTree.trigger import Trigger

class PowerSupplies(Instrument.Instrument):

    def __init__(self, instru, name=None):
        super().__init__(instru, name)
        self.source = self.sourceClass(instru)
        self.output = self.outputClass(instru)
        self.status = self.statusClass(instru)
        self.trigger = self.triggerClass(instru)
        self.name = name
    
    class outputClass:
        def __init__(self, instrument):
            self.output_obj = Output(instrument)
        def set_state(self, enable: bool):
            """Controls whether the output terminals are open or closed.
            Parameters:
            enable: True to close terminals, False for maximum isolation."""
            self.output_obj.set_output_state(enable)

        def get_state(self) -> bool:
            """Returns True if the output terminals are closed, False if open."""
            return self.output_obj.get_output_state()
    
    class sourceClass:
        def __init__(self, instrument):
            self.source_obj = Source(instrument)
        def set_current_level_immediate_amplitude(self, value: float):
            """
            Sets the actual magnitude of the unswept output signal for Current in terms of current operating units.
            Parameters:
            value: The amplitude (numeric value).
            """
            self.source_obj.set_source_current_level_immediate_amplitude(value)

        def get_current_level_immediate_amplitude(self) -> float:
            """
            Returns the actual magnitude of the unswept output signal for Current.
            Returns: The amplitude as a float.
            """
            return self.source_obj.get_source_current_level_immediate_amplitude()

        def set_voltage_level_immediate_amplitude(self, value: float):
            """
            Sets the actual magnitude of the unswept output signal for Voltage in terms of voltage operating units.
            Parameters:
            value: The amplitude (numeric value).
            """
            self.source_obj.set_source_voltage_level_immediate_amplitude(value)

        def get_voltage_level_immediate_amplitude(self) -> float:
            """
            Returns the actual magnitude of the unswept output signal for Voltage.
            Returns: The amplitude as a float.
            """
            return self.source_obj.get_source_voltage_level_immediate_amplitude()
    class statusClass:
        def __init__(self, instrument):
            self.status_obj = Status(instrument)

        def get_operation_condition(self) -> int:
            """
            Returns the contents of the OPERation condition register.
            Returns: The integer value of the condition register.
            """
            return self.status_obj.get_status_operation_condition()

        def set_operation_enable(self, value: int):
            """
            Sets the enable mask for the OPERation register.
            Parameters:
            value: The integer value of the enable mask (range: 0 through 65535).
            """
            self.status_obj._set_status_enable("OPER", value)

        def get_operation_enable(self) -> int:
            """
            Returns the contents of the enable mask for the OPERation register.
            Returns: The integer value of the enable mask.
            """
            return self.status_obj._get_status_enable("OPER")

        def get_operation_event(self) -> int:
            """
            Returns the contents of the OPERation event register. Reading clears it.
            Returns: The integer value of the event register.
            """
            return self.status_obj.get_status_operation_event()

        def get_operation_isummary_condition(self, n: int) -> int:
            """
            Returns the contents of the ISUMmary<n> condition register for OPERation.
            Parameters:
            n: The summary number.
            Returns: The integer value of the condition register.
            """
            return self.status_obj.get_status_isummary_condition(n)

        def set_operation_isummary_enable(self, n: int, value: int):
            """
            Sets the enable mask for the ISUMmary<n> register for OPERation.
            Parameters:
            n: The summary number.
            value: The integer value of the enable mask (range: 0 through 65535).
            """
            self.status_obj.set_status_isummary_enable(n, value)

        def get_operation_isummary_enable(self, n: int) -> int:
            """
            Returns the contents of the enable mask for the ISUMmary<n> register for OPERation.
            Parameters:
            n: The summary number.
            Returns: The integer value of the enable mask.
            """
            return self.status_obj.get_status_isummary_enable(n)

        def get_operation_isummary_event(self, n: int) -> int:
            """
            Returns the contents of the ISUMmary<n> event register for OPERation. Reading clears it.
            Parameters:
            n: The summary number.
            Returns: The integer value of the event register.
            """
            return self.status_obj.get_status_isummary_event(n)

        def get_questionable_condition(self) -> int:
            """
            Returns the contents of the QUEStionable condition register.
            Returns: The integer value of the condition register.
            """
            return self.status_obj.get_status_questionable_condition()

        def set_questionable_enable(self, value: int):
            """
            Sets the enable mask for the QUEStionable register.
            Parameters:
            value: The integer value of the enable mask (range: 0 through 65535).
            """
            self.status_obj.set_status_questionable_enable(value)

        def get_questionable_enable(self) -> int:
            """
            Returns the contents of the enable mask for the QUEStionable register.
            Returns: The integer value of the enable mask.
            """
            return self.status_obj.get_status_questionable_enable()

        def get_questionable_event(self) -> int:
            """
            Returns the contents of the QUEStionable event register. Reading clears it.
            Returns: The integer value of the event register.
            """
            return self.status_obj.get_status_questionable_event()

        def get_questionable_isummary_condition(self, n: int) -> int:
            """
            Returns the contents of the ISUMmary<n> condition register for QUEStionable.
            Parameters:
            n: The summary number.
            Returns: The integer value of the condition register.
            """
            return self.status_obj.get_status_isummary_condition(n)

        def set_questionable_isummary_enable(self, n: int, value: int):
            """
            Sets the enable mask for the ISUMmary<n> register for QUEStionable.
            Parameters:
            n: The summary number.
            value: The integer value of the enable mask (range: 0 through 65535).
            """
            self.status_obj.set_status_isummary_enable(n, value)

        def get_questionable_isummary_enable(self, n: int) -> int:
            """
            Returns the contents of the enable mask for the ISUMmary<n> register for QUEStionable.
            Parameters:
            n: The summary number.
            Returns: The integer value of the enable mask.
            """
            return self.status_obj.get_status_isummary_enable(n)

        def get_questionable_isummary_event(self, n: int) -> int:
            """
            Returns the contents of the ISUMmary<n> event register for QUEStionable. Reading clears it.
            Parameters:
            n: The summary number.
            Returns: The integer value of the event register.
            """
            return self.status_obj.get_status_isummary_event(n)
        
    class triggerClass:
        def __init__(self, instrument):
            self.source_obj = Trigger(instrument)
        def set_initiate_continuous(self, enable: bool):
            """
            Selects whether the trigger system is continuously initiated or not.
            Parameters:
            enable (bool): True for continuous initiation, False to remain in IDLE until IMMediate.
            """
            self.source_obj.set_initiate_continuous(enable)

        def get_initiate_continuous(self) -> bool:
            """
            Queries whether the trigger system is continuously initiated.
            Returns:
            bool: True if continuous initiation, False otherwise.
            """
            return self.source_obj.get_initiate_continuous()

        def set_initiate_continuous_all(self, enable: bool):
            """
            Sets whether or not all sequences are continuously initiated.
            Parameters:
            enable (bool): True to continuously initiate all sequences, False otherwise.
            """
            self.source_obj.set_initiate_continuous_all(enable)

        def get_initiate_continuous_all(self) -> bool:
            """
            Queries whether or not all sequences are continuously initiated.
            Returns:
            bool: True if all sequences are continuously initiated, False otherwise.
            """
            return self.source_obj.get_initiate_continuous_all()

        def set_initiate_continuous_name(self, sequence_name: str, enable: bool):
            """
            Sets whether or not the SEQuence with the alias specified by <sequence_name> is continuously initiated.
            Parameters:
            sequence_name (str): The character program data for the sequence alias.
            enable (bool): True for continuous initiation, False otherwise.
            """
            self.source_obj.set_initiate_continuous_name(sequence_name, enable)

        def get_initiate_continuous_name(self, sequence_name: str) -> bool:
            """
            Queries whether or not the SEQuence with the alias specified by <sequence_name> is continuously initiated.
            Parameters:
            sequence_name (str): The character program data for the sequence alias.
            Returns:
            bool: True if continuously initiated, False otherwise.
            """
            return self.source_obj.get_initiate_continuous_name(sequence_name)

        def set_initiate_continuous_sequence(self, sequence_number: int, enable: bool):
            """
            Sets whether or not the specified SEQuence is continuously initiated.
            Parameters:
            sequence_number (int): The numeric suffix on SEQuence corresponds to the sequence number.
            enable (bool): True for continuous initiation, False otherwise.
            """
            self.source_obj.set_initiate_continuous_sequence(sequence_number, enable)

        def get_initiate_continuous_sequence(self, sequence_number: int) -> bool:
            """
            Queries whether or not the specified SEQuence is continuously initiated.
            Parameters:
            sequence_number (int): The numeric suffix on SEQuence corresponds to the sequence number.
            Returns:
            bool: True if continuously initiated, False otherwise.
            """
            return self.source_obj.get_initiate_continuous_sequence(sequence_number)

        def initiate_immediate(self):
            """
            Causes all sequences to exit the IDLE state; they are initiated.
            The IMMediate command causes the trigger system to initiate and complete one full trigger cycle,
            returning to IDLE on completion.
            """
            self.source_obj.initiate_immediate()

        def initiate_immediate_all(self):
            """
            Causes all SEQuences to be INITiated, except those defined to behave otherwise.
            """
            self.source_obj.initiate_immediate_all()

        def initiate_immediate_name(self, sequence_name: str):
            """
            Causes the SEQuence with the alias specified by <sequence_name> to be INITiated.
            Parameters:
            sequence_name (str): The character program data for the sequence alias.
            """
            self.source_obj.initiate_immediate_name(sequence_name)

        def initiate_immediate_sequence(self, sequence_number: int):
            """
            Causes the specified SEQuence to be INITiated.
            Parameters:
            sequence_number (int): The numeric suffix on SEQuence corresponds to the sequence number.
            """
            self.source_obj.initiate_immediate_sequence(sequence_number)

        def set_trigger_sequence_source(self, source_type: str, source_index: int = None):
            """
            Selects the source for the event detector. Only one source may be specified at a time.
            Parameters:
            source_type (str): The type of source (e.g., "AINTernal", "BUS", "ECLTrg", "EXTernal", "HOLD",
                       "IMMediate", "INTernal", "LINE", "LINK", "MANual", "OUTPut", "TIMer", "TTLTrg").
            source_index (int, optional): Numeric suffix for sources like ECLTrg, EXTernal, INTernal, OUTPut, TTLTrg.
            """
            self.source_obj.set_trigger_sequence_source(source_type, source_index)

        def get_trigger_sequence_source(self) -> str:
            """
            Queries the source for the event detector for the TRIGger sequence.
            Returns:
            str: The source type string (e.g., "IMMediate", "TTLTrg0").
            """
            return self.source_obj.get_trigger_sequence_source()

        def trigger_sequence_immediate(self):
            """
            Provides a one-time override of the normal process of the downward traverse of the event detection layer.
            Causes immediate exit of the specified event detection layer if the trigger system is in that layer.
            """
            self.source_obj.trigger_sequence_immediate()