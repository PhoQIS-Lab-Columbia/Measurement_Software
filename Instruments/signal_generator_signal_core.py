from Instruments.Instrument import Instrument
from Instruments.EInstrument import EInstrument
import pyvisa
from ctypes import *
import ctypes
from Instruments.data_handler import DataHandler
class signal_generator():

    def __init__(self, instrument, handle, save_files_path = None):
        self.instrument = instrument
        self.name = EInstrument.SIGNAL_GENERATOR
        self.handle = handle
        if save_files_path is None:
            self.data_handler = DataHandler()  # Default format set to JSON
        else:
            self.data_handler = DataHandler(save_files_path)  # Default format set to JSON
        #Class objects
    def disconnect(self):
        """Disconnects the instrument."""
        self.instrument.sc5510a_close_device(self.handle)

    
    #TODO: figure out register bytes options, read and write 
    #Look up instruction words options for reg_write reg_read
    def hard_reset(self):
        """Resets to the default power up state."""
        self.instrument.sc5510a_init_device(self.handle, 1)
    def soft_reset(self):
        """Resets but keep current state."""
        self.instrument.sc5510a_init_device(self.handle, 0)
    def set_frequency(self, frequency):
        """Sets RF1 frequency in Hz.
        params: frequency: int - frequency in Hz
        Returns: None"""
        result = self.instrument.sc5510a_set_frequency(self.handle, ctypes.c_ulonglong(frequency))
        if result != 0:
            raise RuntimeError("Failed to set frequency")

    def set_signal_phase(self, phase):
        """Sets the relative phase of the signal on CH1.
        params: phase: float - phase"""
        result = self.instrument.sc5510a_set_signal_phase(self.handle, ctypes.c_float(phase))
        if result != 0:
            raise RuntimeError("Failed to set signal phase")

    def set_synth_mode(self, disable_spur_suppression, loop_gain, lock_mode):
        """Sets synthesizer mode of RF1.
        TODO Look up what these parameters values are."""
        #TODO Change Ctypes values to correct ones
        result = self.instrument.sc5510a_set_synth_mode(
            self.handle,
            ctypes.c_char(disable_spur_suppression),
            ctypes.c_char(loop_gain),
            ctypes.c_char(lock_mode)
        )
        if result != 0:
            raise RuntimeError("Failed to set synthesizer mode")
        
    def set_rf_mode(self, rf_mode):
        """
        Sets RF1 to fixed tone or sweep mode.

        Parameters:
            rf_mode (int): Set RF mode of RF1.
                0 - Fixed tone
                1 - Sweep

        """
        #TODO: Look up if correct c type
        result = self.instrument.sc5510a_set_rf_mode(
            self.handle,
            ctypes.c_ubyte(rf_mode)
        )
        if result != 0:
            raise RuntimeError("Failed to set RF mode")
    def list_mode_config(self, list_mode):
        """
        Configures the list mode behavior.

        Parameters:
            list_mode: ctypes.Structure or compatible object representing list_mode_t
        """
        result = self.instrument.sc5510a_list_mode_config(
            self.handle,
            ctypes.byref(list_mode)
        )
        if result != 0:
            raise RuntimeError("Failed to configure list mode")

    def list_start_freq(self, freq):
        """
        Sets the sweep start frequency.

        Parameters:
            freq (int): Frequency in Hz
        """
        result = self.instrument.sc5510a_list_start_freq(
            self.handle,
            ctypes.c_ulonglong(freq)
        )
        if result != 0:
            raise RuntimeError("Failed to set list start frequency")

    def list_stop_freq(self, freq):
        """
        Sets the sweep stop frequency.

        Parameters:
            freq (int): Frequency in Hz
        """
        result = self.instrument.sc5510a_list_stop_freq(
            self.handle,
            ctypes.c_ulonglong(freq)
        )
        if result != 0:
            raise RuntimeError("Failed to set list stop frequency")

    def list_step_freq(self, freq):
        """
        Sets the sweep step frequency.

        Parameters:
            freq (int): Frequency in Hz
        """
        result = self.instrument.sc5510a_list_step_freq(
            self.handle,
            ctypes.c_ulonglong(freq)
        )
        if result != 0:
            raise RuntimeError("Failed to set list step frequency")

    def list_dwell_time(self, dwell_time):
        """
        Sets the sweep/list dwell time at each frequency point.

        Parameters:
            dwell_time (int): Time in 500 µs increments (1 = 500 µs, 2 = 1 ms, etc.)
        """
        result = self.instrument.sc5510a_list_dwell_time(
            self.handle,
            ctypes.c_uint(dwell_time)
        )
        if result != 0:
            raise RuntimeError("Failed to set list dwell time")
    def list_cycle_count(self, cycle_count):
        """
        Sets the number of sweep cycles to perform before stopping.

        Parameters:
            cycle_count (int): Number of cycles. Set to 0 for continuous sweep.

        Returns:
            None

        Raises:
            RuntimeError: If setting the cycle count fails.
        """
        result = self.instrument.sc5510a_list_cycle_count(
            self.handle,
            ctypes.c_uint(cycle_count)
        )
        if result != 0:
            raise RuntimeError("Failed to set list cycle count")

    def list_buffer_points(self, list_points):
        """
        Sets the number of list points in the list buffer to sweep or step through.

        Parameters:
            list_points (int): Number of points in the list buffer.

        Returns:
            None

        Raises:
            RuntimeError: If setting the buffer points fails.
        """
        result = self.instrument.sc5510a_list_buffer_points(
            self.handle,
            ctypes.c_uint(list_points)
        )
        if result != 0:
            raise RuntimeError("Failed to set list buffer points")

    def list_buffer_write(self, freq):
        """
        Writes the frequency buffer sequentially.

        Parameters:
            freq (int): Frequency in Hz. If 0, resets buffer pointer. If 0xFFFFFFFFFF, terminates sequential write.

        Returns:
            None

        Raises:
            RuntimeError: If writing to the buffer fails.
        """
        result = self.instrument.sc5510a_list_buffer_write(
            self.handle,
            ctypes.c_ulonglong(freq)
        )
        if result != 0:
            raise RuntimeError("Failed to write to list buffer")

    def list_buffer_transfer(self, transfer_mode):
        """
        Transfers the frequency list buffer from RAM to EEPROM or vice versa.

        Parameters:
            transfer_mode (int): Transfer mode (to EEPROM or RAM).

        Returns:
            None

        Raises:
            RuntimeError: If buffer transfer fails.
        """
        result = self.instrument.sc5510a_list_buffer_transfer(
            self.handle,
            ctypes.c_ubyte(transfer_mode)
        )
        if result != 0:
            raise RuntimeError("Failed to transfer list buffer")

    def list_soft_trigger(self):
        """
        Triggers the device when configured for list mode and soft trigger is selected.

        Returns:
            None

        Raises:
            RuntimeError: If soft trigger fails.
        """
        result = self.instrument.sc5510a_list_soft_trigger(self.handle)
        if result != 0:
            raise RuntimeError("Failed to soft trigger list mode")
    
    def set_power_level(self, power_level):
        """
        Sets the power output level of RF1.

        Parameters:
            power_level (float): Level in dBm.

        Returns:
            None

        Raises:
            RuntimeError: If setting the power level fails.
        """
        result = self.instrument.sc5510a_set_level(
            self.handle,
            ctypes.c_float(power_level)
        )
        if result != 0:
            raise RuntimeError("Failed to set power level")

    def set_output(self, enable):
        """
        Enables or disables the output RF1.

        Parameters:
            enable (int): 1 to enable output, 0 to disable.

        Returns:
            None

        Raises:
            RuntimeError: If setting the output fails.
        """
        result = self.instrument.sc5510a_set_output(
            self.handle,
            ctypes.c_ubyte(enable)
        )
        if result != 0:
            raise RuntimeError("Failed to set output")

    def set_auto_level_disable(self, disable):
        """
        Disables the leveling compensation after the frequency is changed for channel RF1.

        Parameters:
            disable (int): 1 to disable leveling, 0 to enable.

        Returns:
            None

        Raises:
            RuntimeError: If setting auto level disable fails.
        """
        result = self.instrument.sc5510a_set_auto_level_disable(
            self.handle,
            ctypes.c_ubyte(disable)
        )
        if result != 0:
            raise RuntimeError("Failed to set auto level disable")

    def set_alc_mode(self, mode):
        """
        Sets the ALC to close (0) or open (1) mode operation for channel RF1.

        Parameters:
            mode (int): 0 for close, 1 for open.

        Returns:
            None

        Raises:
            RuntimeError: If setting ALC mode fails.
        """
        result = self.instrument.sc5510a_set_alc_mode(
            self.handle,
            ctypes.c_ubyte(mode)
        )
        if result != 0:
            raise RuntimeError("Failed to set ALC mode")

    def set_standby(self, enable):
        """
        Powers down channel RF1 if enabled.

        Parameters:
            enable (int): 1 to enable standby (power down), 0 to disable.

        Returns:
            None

        Raises:
            RuntimeError: If setting standby fails.
        """
        result = self.instrument.sc5510a_set_standby(
            self.handle,
            ctypes.c_ubyte(enable)
        )
        if result != 0:
            raise RuntimeError("Failed to set standby mode")
    def set_clock_reference(self, ext_ref_select, ext_direct_clk, select_freq, lock_external):
        """
        Configures the reference clock behavior.

        Parameters:
            ext_ref_select (int): Selects input as 10 MHz (0) or 100 MHz (1).
            ext_direct_clk (int): Bypass internal reference, clocks synth directly (0 = no bypass, 1 = bypass).
            select_freq (int): Selects 10 MHz (0) or 100 MHz (1).
            lock_external (int): Locks to external reference (0 = do not lock, 1 = lock).

        Raises:
            RuntimeError: If setting the clock reference fails.
        """
        result = self.instrument.sc5510a_set_clock_reference(
            self.handle,
            ctypes.c_ubyte(ext_ref_select),
            ctypes.c_ubyte(ext_direct_clk),
            ctypes.c_ubyte(select_freq),
            ctypes.c_ubyte(lock_external)
        )
        if result != 0:
            raise RuntimeError("Failed to set clock reference")

    def set_reference_dac(self, dac_value):
        """
        Sets the DAC value that controls the TCXO frequency.

        Parameters:
            dac_value (int): DAC value to be written (unsigned short: 0-65535).

        Raises:
            RuntimeError: If setting the reference DAC fails.
        """
        result = self.instrument.sc5510a_set_reference_dac(
            self.handle,
            ctypes.c_ushort(dac_value)
        )
        if result != 0:
            raise RuntimeError("Failed to set reference DAC")

    def set_alc_dac(self, dac_value):
        """
        Sets the value of the ALC DAC to make amplitude adjustments.

        Parameters:
            dac_value (int): DAC value to be written (unsigned short: 0-65535).

        Raises:
            RuntimeError: If setting the ALC DAC fails.
        """
        result = self.instrument.sc5510a_set_alc_dac(
            self.handle,
            ctypes.c_ushort(dac_value)
        )
        if result != 0:
            raise RuntimeError("Failed to set ALC DAC")

    def store_default_state(self):
        """
        Stores the current configuration into EEPROM memory as the default state upon reset or power-up.

        Raises:
            RuntimeError: If storing the default state fails.
        """
        result = self.instrument.sc5510a_store_default_state(self.handle)
        if result != 0:
            raise RuntimeError("Failed to store default state")
    def set_rf2_frequency(self, freq):
        """
        Sets the frequency for channel RF2.

        Parameters:
            freq (int): Frequency in MHz (unsigned short: 0-65535)

        Raises:
            RuntimeError: If setting RF2 frequency fails.
        """
        result = self.instrument.sc5510a_set_rf2_frequency(
            self.handle,
            ctypes.c_ushort(freq)
        )
        if result != 0:
            raise RuntimeError("Failed to set RF2 frequency")

    def synth_self_cal(self):
        """
        Performs a self calibration of the DAC values to properly set the VCO up for phase lock.

        Description:
            When the device uses the harmonic generator as the offset loop, the VCO could potentially
            lock to a wrong reference harmonic causing the sum PLL to fail. Perform this function if
            the sum PLL fails when the synthesizer is in harmonic lock mode. Allow 2-3 seconds for
            the calibration routine to execute, and upon completion the device will reset. The status
            indicator of RF1 will go off, then red, then amber, and then finally green.

        Raises:
            RuntimeError: If self calibration fails.
        """
        result = self.instrument.sc5510a_synth_self_cal(self.handle)
        if result != 0:
            raise RuntimeError("Failed to perform synthesizer self calibration")

    def get_rf_parameters(self, rf_params):
        """
        Gets the current RF parameters such as RF1 frequency, RF2 frequency, and sweep start frequency.

        Parameters:
            rf_params (ctypes.Structure): Structure compatible with rf_params_t to receive parameters.

        Raises:
            RuntimeError: If getting RF parameters fails.
        """
        result = self.instrument.sc5510a_get_rf_parameters(
            self.handle,
            ctypes.byref(rf_params)
        )
        if result != 0:
            raise RuntimeError("Failed to get RF parameters")

    def get_signal_phase(self):
        """
        Obtains the current relative phase of the signal on CH1.

        Returns:
            float: The current phase value.

        Raises:
            RuntimeError: If getting the signal phase fails.
        """
        phase = ctypes.c_float()
        result = self.instrument.sc5511a_get_signal_phase(
            self.handle,
            ctypes.byref(phase)
        )
        if result != 0:
            raise RuntimeError("Failed to get signal phase")
        return phase.value
    def get_device_status(self, device_status):
        """
        Gets the current device status such as the PLL lock status, sweep modes, and other operating conditions.

        Parameters:
            device_status (ctypes.Structure): Structure compatible with device_status_t to receive status.

        Raises:
            RuntimeError: If getting device status fails.
        """
        result = self.instrument.sc5510a_get_device_status(
            self.handle,
            ctypes.byref(device_status)
        )
        if result != 0:
            raise RuntimeError("Failed to get device status")

    def get_clock_config(self, clock_config):
        """
        Retrieves the current reference clock configuration.

        Parameters:
            clock_config (ctypes.Structure): Structure compatible with clock_config_t to receive configuration.

        Raises:
            RuntimeError: If getting clock config fails.
        """
        result = self.instrument.sc5510a_get_clock_config(
            ctypes.byref(self.handle),
            ctypes.byref(clock_config)
        )
        if result != 0:
            raise RuntimeError("Failed to get clock configuration")

    def get_device_info(self, device_info):
        """
        Obtains the device information such as serial number, hardware revision, firmware revision, and manufactured date.

        Parameters:
            device_info (ctypes.Structure): Structure compatible with device_info_t to receive information.

        Raises:
            RuntimeError: If getting device info fails.
        """
        result = self.instrument.sc5510a_get_device_info(
            self.handle,
            ctypes.byref(device_info)
        )
        if result != 0:
            raise RuntimeError("Failed to get device info")

    def list_buffer_read(self, address):
        """
        Reads the frequency at an offset address of the list buffer.

        Parameters:
            address (int): Buffer offset address.

        Returns:
            int: Frequency in Hz at the specified buffer address.

        Raises:
            RuntimeError: If reading from the list buffer fails.
        """
        freq = ctypes.c_ulonglong()
        result = self.instrument.sc5510a_list_buffer_read(
            self.handle,
            ctypes.c_uint(address),
            ctypes.byref(freq)
        )
        if result != 0:
            raise RuntimeError("Failed to read from list buffer")
        return freq.value
    
    def get_alc_dac(self):
        """
        Retrieves the current value of the ALC DAC which sets the power level of channel RF1.

        Returns:
            int: The current ALC DAC value (unsigned short: 0-65535).

        Raises:
            RuntimeError: If retrieving the ALC DAC value fails.
        """
        dac_value = ctypes.c_ushort()
        result = self.instrument.sc5510a_get_alc_adc(
            self.handle,
            ctypes.byref(dac_value)
        )
        if result != 0:
            raise RuntimeError("Failed to get ALC DAC value")
        return dac_value.value
    