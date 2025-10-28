from Instruments.data_handler import DataHandler
from Instruments.EFileType import EFileType
from PIL import Image
from Instruments.EFileType import EFileType
class Instrument():
    """Generic Instrument class meant to contain required functionality of all IEEE 488.2 instruments"""
    def __init__(self, instrument, name, save_files_path = None):
        self.instrument = instrument
        
        self.name = name
        if save_files_path is None:
            self.data_handler = DataHandler()  # Default format set to JSON
        else:
            self.data_handler = DataHandler(save_files_path)
        
    def disconnect(self):
        """Disconnect from instrument and shut down all data reading and controls."""
        self.instrument.close()
        print("Disconnected from "+str(self.name))


    def save_data(self, data, file_name = "data", format = EFileType.CSV):
        """Save data to a file in the specified save path.
        
        Parameters:
        data (dict): The data to be saved.
        filename (str): The name of the file to save the data in.
        format (EFileType): The format in which to save the data. Default is EFileType.CSV."""
        self.data_handler.write_to_file(file_name, data, format)

    def clear_event_registers(self):
        """Clear all the event registers and clear the error queue."""
        self.instrument.write("*CLS")
    
    def set_enable_event_status(self, value):
        """Set the enable register for the standard event status register set.

        Parameters:
        value (int): An integer value where bit 1 and bit 6 are not used (always 0).
        The range corresponds to binary numbers X0XXXX0X."""
        # Basic validation for the value based on the description
        if isinstance(value, int) and 0 <= value <= 255: # Max 255 for an 8-bit register
            # Further validation for bits 1 and 6 being 0 could be added:
            # if (value & 0b01000010) == 0: # Check if bit 1 (0b00000010) or bit 6 (0b01000000) are set
            self.instrument.write(f"*ESE {value}")
        else:
            print(f"Invalid value ({value}). Must be an integer between 0 and 255 (with bits 1 and 6 effectively 0).")
    
    def get_standard_event_status_enable(self):
        """Query the enable register for the standard event status register set.

        Returns:
        int: An integer which equals the sum of the weights of all the bits that have
        already been set in the register.
        """
        response = self.instrument.query("*ESE?")
        return int(response.strip())
    
    def get_and_clear_standard_event_status_register(self):
        """Query and clear the event register for the standard event status register.

        Returns:
        int: An integer which equals the sum of the weights of all the bits in the register.
        The value of the register is set to 0 after this command is executed.
        """
        response = self.instrument.query("*ESR?")
        return int(response.strip())
    
    def get_id(self):
        """Query the ID string of the instrument.

        Returns:
        str: The ID string in the format "RIGOL TECHNOLOGIES,<model>,<serial number>,<software version>".
        """
        response = self.instrument.query("*IDN?")
        return response.strip()
    
    def set_operation_complete(self):
        """Set the Operation Complete bit (bit 0) in the standard event status register to 1
        after the current operation is finished.
        """
        self.instrument.write("*OPC")

    def is_operation_complete(self):
        """Query whether the current operation is finished.

        Returns:
        bool: True (1) if the current operation is finished; False (0) otherwise.
        """
        response = self.instrument.query("*OPC?")
        return bool(int(response.strip()))


    def reset_instrument(self):
        """Restore the instrument to the default state .
        """
        self.instrument.write("*RST")

    def set_enable_service_request(self, value):
        """Set the enable register for the status byte register set.

        Parameters:
        value (int): An integer value from 0 to 255. Bit 0 and bit 1 of the status byte register are not used and are always treated as 0.
        """
        # Basic validation for the value
        if isinstance(value, int) and 0 <= value <= 255:
            # Further validation for bits 0 and 1 being 0 could be added:
            # if (value & 0b00000011) == 0: # Check if bit 0 (0b00000001) or bit 1 (0b00000010) are set
            self.instrument.write(f"*SRE {value}")
        else:
            print(f"Invalid value ({value}). Must be an integer between 0 and 255 (with bits 0 and 1 effectively 0).")

    def get_enable_service_request(self):
        """Query the enable register for the status byte register set.

        Returns:
        int: An integer which equals the sum of the weights of all the bits that have already been set in the register.
        """
        response = self.instrument.query("*SRE?")
        return int(response.strip())
    
    def read_status_byte(self):
        """Query the event register for the status byte register.
        The value of the status byte register is set to 0 after this command is executed.

        Returns:
        int: An integer which equals the sum of the weights of all the bits in the register.
        """
        response = self.instrument.query("*STB?")
        return int(response.strip())

    def self_test(self):
        """Perform a self-test and then return the self-test results.

        Returns:
        int: A decimal integer representing the self-test results.
        """
        response = self.instrument.query("*TST?")
        return int(response.strip())

    def wait_for_operation_finish(self):
        """Wait for the current operation to finish.
        The subsequent command can only be carried out after the current command has been executed.
        """
        self.instrument.write("*WAI")
    
    #Required commands
    def get_system_error(self) -> str:
        """Queries the next error from the error queue, returning its code and message.
        Notes: Query only.
        """
        response = self.instrument.query(":SYST:ERR:NEXT?").strip()
        return response
    
    def get_system_version(self) -> str:
        """Returns the SCPI version supported by the instrument.
        Notes: Query only.
        """
        response = self.instrument.query(":SYST:VERS?").strip()
        return response
    
    def set_status_operation_enable(self, value: int):
        """Sets the enable mask for the OPERation register.
        :param value: The integer value of the enable mask (range: 0 through 65535).
        
        """
        #TODO: Fix value to be boolean?
        self._set_status_enable(":STAT:OPER:ENAB", value)

    def get_status_operation_enable(self) -> int:
        """Returns the contents of the enable mask for the OPERation register.
        """
        return self._get_status_enable(":STAT:OPER:ENAB?")