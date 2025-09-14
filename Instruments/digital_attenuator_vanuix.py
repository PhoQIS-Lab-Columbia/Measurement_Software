from Instruments.Instrument import Instrument
from Instruments.EInstrument import EInstrument
from EConnection import EConnection
import platform
from Instruments.data_handler import DataHandler
import os 
import ctypes

class digital_attenuator(Instrument):

    def __init__(self, instrument, devid, save_files_path=None):
        self.instrument = instrument
        self.name = EInstrument.DIGITAL_ATTENUATOR
        self.minumum_attenuation_increment = 0.25 #dB
        #Choose which dll to load based on native system
        self.instrument = instrument
        
        if save_files_path is None:
            self.data_handler = DataHandler()  # Default format set to JSON
        else:
            self.data_handler = DataHandler(save_files_path)
        self.devid = devid
        self.minAttenuation = int(self.instrument.fnLDA_GetMinAttenuation(devid) / 4)
        self.maxAttenuation = int(self.instrument.fnLDA_GetMaxAttenuation(devid) / 4)
        self.numChannels = self.instrument.fnLDA_GetNumChannels(devid)
   
    def enable_testing(self):
        """Enables testting mode for the digital attenuator."""
        self.instrument.fnLDA_SetTestMode(False)
    def disable_testing(self):
        """Disables testing mode for the digital attenuator."""
        self.instrument.fnLDA_SetTestMode(True)


    def get_model_name(self):
        """Gets the model name of the digital attenuator."""
        # First, get the length of the model name
        length = self.instrument.fnLDA_GetModelName(self.devid, None)
        if length <= 0:
            return None
        # Allocate buffer for model name
        MAX_MODELNAME = 64  # Use actual value from VNX_atten.h if available
        buf = ctypes.create_string_buffer(MAX_MODELNAME)
        self.instrument.fnLDA_GetModelName(self.devid, buf)
        return buf.value.decode('utf-8')

    def get_serial_number(self):
        """Gets the serial number of the digital attenuator."""
        return self.instrument.fnLDA_GetSerialNumber(self.devid)

    def get_device_status(self):
        """Gets the status of the digital attenuator."""
        return self.instrument.fnLDA_GetDeviceStatus(self.devid)
    def disconnect(self):
        """Disconnects the digital attenuator."""
        self.instrument.fnLDA_CloseDevice(self.devid)
        print(f"Disconnected {self.get_model_name()} with serial number {self.get_serial_number()}")
    
    def set_channel(self, channel):
        """Sets the channel to be controlled."""
        status = self.instrument.fnLDA_SetChannel(self.devid, int(channel))
        return status

    def set_working_frequency(self, frequency_mhz):
        """
        Sets the midband working frequency of the attenuator.
        frequency_mhz: Frequency in MHz (e.g., 1500 for 1.5 GHz)
        """
        freq_code = int(frequency_mhz * 10)  # Convert MHz to 100 kHz units
        status = self.instrument.fnLDA_SetWorkingFrequency(self.devid, freq_code)
        return status

    def set_attenuation(self, attenuation_db):
        """
        Sets the attenuation level for 0.25 dB step attenuators.
        attenuation_db: Desired attenuation in dB (e.g., 10 for 10 dB)
        """
        att_code = int(attenuation_db / 0.25)
        status = self.instrument.fnLDA_SetAttenuation(self.devid, att_code)
        return status

    def set_attenuation_hr(self, attenuation_db):
        """
        Sets the attenuation level for 0.05 dB step attenuators.
        attenuation_db: Desired attenuation in dB (e.g., 5 for 5 dB)
        """
        att_code = int(attenuation_db / 0.05)
        status = self.instrument.fnLDA_SetAttenuationHR(self.devid, att_code)
        return status
    def set_attenuation_hrq(self, attenuation_db, channel):
        """
        Sets the attenuation level for 0.05 dB step attenuators on a specific channel.
        attenuation_db: Desired attenuation in dB (e.g., 5 for 5 dB)
        channel: Channel number (1 to 4)
        """
        att_code = int(attenuation_db / 0.05)
        status = self.instrument.fnLDA_SetAttenuationHRQ(self.devid, att_code, int(channel))
        return status

    def set_ramp_start(self, attenuation_db):
        """
        Sets the attenuation level at the beginning of an attenuation ramp (0.25 dB steps).
        attenuation_db: Desired attenuation in dB (e.g., 10 for 10 dB)
        """
        att_code = int(attenuation_db / 0.25)
        status = self.instrument.fnLDA_SetRampStart(self.devid, att_code)
        return status

    def set_ramp_start_hr(self, attenuation_db):
        """
        Sets the attenuation level at the beginning of an attenuation ramp (0.05 dB steps).
        attenuation_db: Desired attenuation in dB (e.g., 5 for 5 dB)
        """
        att_code = int(attenuation_db / 0.05)
        status = self.instrument.fnLDA_SetRampStartHR(self.devid, att_code)
        return status
    def set_ramp_end(self, attenuation_db):
        """
        Sets the attenuation level at the end of an attenuation ramp (0.25 dB steps).
        attenuation_db: Desired attenuation in dB (e.g., 10 for 10 dB)
        """
        att_code = int(attenuation_db / 0.25)
        status = self.instrument.fnLDA_SetRampEnd(self.devid, att_code)
        return status

    def set_ramp_end_hr(self, attenuation_db):
        """
        Sets the attenuation level at the end of an attenuation ramp (0.05 dB steps).
        attenuation_db: Desired attenuation in dB (e.g., 5 for 5 dB)
        """
        att_code = int(attenuation_db / 0.05)
        status = self.instrument.fnLDA_SetRampEndHR(self.devid, att_code)
        return status

    def set_attenuation_step(self, step_db):
        """
        Sets the size of the attenuation step for ramp/sweep (0.25 dB steps).
        step_db: Step size in dB (e.g., 2 for 2 dB)
        """
        step_code = int(step_db / 0.25)
        status = self.instrument.fnLDA_SetAttenuationStep(self.devid, step_code)
        return status

    def set_attenuation_step_hr(self, step_db):
        """
        Sets the size of the attenuation step for ramp/sweep (0.05 dB steps).
        step_db: Step size in dB (e.g., 2 for 2 dB)
        """
        step_code = int(step_db / 0.05)
        status = self.instrument.fnLDA_SetAttenuationStepHR(self.devid, step_code)
        return status
    def set_attenuation_step_two(self, step_db):
        """
        Sets the size of the attenuation step for the second phase of a bidirectional sweep (0.25 dB steps).
        step_db: Step size in dB (e.g., 2 for 2 dB)
        """
        step_code = int(step_db / 0.25)
        status = self.instrument.fnLDA_SetAttenuationStepTwo(self.devid, step_code)
        return status

    def set_attenuation_step_two_hr(self, step_db):
        """
        Sets the size of the attenuation step for the second phase of a bidirectional sweep (0.05 dB steps).
        step_db: Step size in dB (e.g., 2 for 2 dB)
        """
        step_code = int(step_db / 0.05)
        status = self.instrument.fnLDA_SetAttenuationStepTwoHR(self.devid, step_code)
        return status

    def set_dwell_time(self, dwell_time_ms):
        """
        Sets the dwell time at each attenuation step during a ramp (in milliseconds).
        dwell_time_ms: Dwell time in milliseconds (minimum 1 ms)
        """
        status = self.instrument.fnLDA_SetDwellTime(self.devid, int(dwell_time_ms))
        return status

    def set_dwell_time_two(self, dwell_time_ms):
        """
        Sets the dwell time at each attenuation step during the second phase of a ramp (in milliseconds).
        dwell_time_ms: Dwell time in milliseconds (minimum 1 ms)
        """
        status = self.instrument.fnLDA_SetDwellTimetwo(self.devid, int(dwell_time_ms))
        return status

    def set_idle_time(self, idle_time_ms):
        """
        Sets the idle time at the end of an attenuation ramp before repeating (in milliseconds).
        idle_time_ms: Idle time in milliseconds (minimum 0 ms)
        """
        status = self.instrument.fnLDA_SetIdleTime(self.devid, int(idle_time_ms))
        return status

    def set_hold_time(self, hold_time_ms):
        """
        Sets the time delay between the first and second phases of a ramp (in milliseconds).
        hold_time_ms: Hold time in milliseconds (minimum 0 ms)
        """
        status = self.instrument.fnLDA_SetHoldTime(self.devid, int(hold_time_ms))
        return status
    def set_profile_element(self, index, attenuation_db):
        """
        Sets the value of a profile element (0.25 dB steps).
        index: Index of the profile element (0 to PROFILE_MAX-1)
        attenuation_db: Desired attenuation in dB
        """
        att_code = int(attenuation_db / 0.25)
        status = self.instrument.fnLDA_SetProfileElement(self.devid, int(index), att_code)
        return status

    def set_profile_element_hr(self, index, attenuation_db):
        """
        Sets the value of a profile element (0.05 dB steps).
        index: Index of the profile element (0 to PROFILE_MAX-1)
        attenuation_db: Desired attenuation in dB
        """
        att_code = int(attenuation_db / 0.05)
        status = self.instrument.fnLDA_SetProfileElementHR(self.devid, int(index), att_code)
        return status

    def set_profile_count(self, profile_count):
        """
        Sets the number of elements in the profile to be used.
        profile_count: Number of elements (1 to PROFILE_MAX-1)
        """
        status = self.instrument.fnLDA_SetProfileCount(self.devid, int(profile_count))
        return status

    def set_profile_idle_time(self, idle_time_ms):
        """
        Sets the idle time after a profile is played before repeating (in ms).
        idle_time_ms: Idle time in milliseconds
        """
        status = self.instrument.fnLDA_SetProfileIdleTime(self.devid, int(idle_time_ms))
        return status

    def set_profile_dwell_time(self, dwell_time_ms):
        """
        Sets the time duration of each element in the profile during playback (in ms).
        dwell_time_ms: Dwell time in milliseconds
        """
        status = self.instrument.fnLDA_SetProfileDwellTime(self.devid, int(dwell_time_ms))
        return status

    def start_profile(self, mode):
        """
        Starts the playback of a profile.
        mode: 1 = play once, 2 = play repeatedly
        """
        status = self.instrument.fnLDA_StartProfile(self.devid, int(mode))
        return status

    def set_rf_on(self, on):
        """
        Rapidly switches the attenuator from its set value ("on"=True) to max attenuation ("on"=False).
        on: Boolean value
        """
        status = self.instrument.fnLDA_SetRFOn(self.devid, bool(on))
        return status
    def set_ramp_direction(self, up):
        """
        Sets the direction of the attenuation ramp.
        up: True for increasing attenuation, False for decreasing.
        """
        status = self.instrument.fnLDA_SetRampDirection(self.devid, bool(up))
        return status

    def set_ramp_mode(self, repeat):
        """
        Sets the ramp mode.
        repeat: True for repeated ramp, False for single ramp.
        """
        status = self.instrument.fnLDA_SetRampMode(self.devid, bool(repeat))
        return status

    def set_ramp_bidirectional(self, bidir_enable):
        """
        Enables or disables bidirectional ramp.
        bidir_enable: True to enable, False to disable.
        """
        status = self.instrument.fnLDA_SetRampBidirectional(self.devid, bool(bidir_enable))
        return status

    def start_ramp(self, go):
        """
        Starts or stops the attenuation ramp.
        go: True to start, False to stop.
        """
        status = self.instrument.fnLDA_StartRamp(self.devid, bool(go))
        return status

    def save_settings(self):
        """
        Saves the current settings to the device.
        """
        status = self.instrument.fnLDA_SaveSettings(self.devid)
        return status
    def get_working_frequency(self):
        """
        Gets the current working frequency of the selected device (in MHz).
        """
        freq_code = self.instrument.fnLDA_GetWorkingFrequency(self.devid)
        # freq_code is in 100 kHz units, convert to MHz
        return freq_code / 10.0

    def get_min_working_frequency(self):
        """
        Gets the minimum working frequency of the selected device (in MHz).
        """
        freq_code = self.instrument.fnLDA_GetMinWorkingFrequency(self.devid)
        # freq_code is in 100 kHz units, convert to MHz
        return freq_code / 10.0
    def get_max_working_frequency(self):
        """
        Gets the maximum working frequency of the selected device (in MHz).
        """
        freq_code = self.instrument.fnLDA_GetMaxWorkingFrequency(self.devid)
        # freq_code is in 100 kHz units, convert to MHz
        return freq_code / 10.0

    def get_attenuation(self):
        """
        Gets the current attenuation setting of the selected device (in dB, 0.25 dB steps).
        """
        att_code = self.instrument.fnLDA_GetAttenuation(self.devid)
        return att_code * 0.25

    def get_attenuation_hr(self):
        """
        Gets the current attenuation setting of the selected device (in dB, 0.05 dB steps).
        """
        att_code = self.instrument.fnLDA_GetAttenuationHR(self.devid)
        return att_code * 0.05

    def get_ramp_start(self):
        """
        Gets the current attenuation ramp start value (in dB, 0.25 dB steps).
        """
        att_code = self.instrument.fnLDA_GetRampStart(self.devid)
        return att_code * 0.25

    def get_ramp_start_hr(self):
        """
        Gets the current attenuation ramp start value (in dB, 0.05 dB steps).
        """
        att_code = self.instrument.fnLDA_GetRampStartHR(self.devid)
        return att_code * 0.05

    def get_ramp_end(self):
        """
        Gets the current attenuation ramp end value (in dB, 0.25 dB steps).
        """
        att_code = self.instrument.fnLDA_GetRampEnd(self.devid)
        return att_code * 0.25

    def get_ramp_end_hr(self):
        """
        Gets the current attenuation ramp end value (in dB, 0.05 dB steps).
        """
        att_code = self.instrument.fnLDA_GetRampEndHR(self.devid)
        return att_code * 0.05

    def get_attenuation_step(self):
        """
        Gets the current attenuation step size (in dB, 0.25 dB steps).
        """
        step_code = self.instrument.fnLDA_GetAttenuationStep(self.devid)
        return step_code * 0.25
    def get_attenuation_step_hr(self):
        """
        Gets the current attenuation step size (in dB, 0.05 dB steps).
        """
        step_code = self.instrument.fnLDA_GetAttenuationStepHR(self.devid)
        return step_code * 0.05

    def get_attenuation_step_two(self):
        """
        Gets the current attenuation step size for the second phase of a bidirectional sweep (in dB, 0.25 dB steps).
        """
        step_code = self.instrument.fnLDA_GetAttenuationStepTwo(self.devid)
        return step_code * 0.25

    def get_attenuation_step_two_hr(self):
        """
        Gets the current attenuation step size for the second phase of a bidirectional sweep (in dB, 0.05 dB steps).
        """
        step_code = self.instrument.fnLDA_GetAttenuationStepTwoHR(self.devid)
        return step_code * 0.05

    def get_dwell_time(self):
        """
        Gets the current dwell time for each step on the attenuation ramp (in milliseconds).
        """
        return self.instrument.fnLDA_GetDwellTime(self.devid)

    def get_dwell_time_two(self):
        """
        Gets the current dwell time for each step on the second phase of a bidirectional attenuation ramp (in milliseconds).
        """
        return self.instrument.fnLDA_GetDwellTimeTwo(self.devid)

    def get_idle_time(self):
        """
        Gets the idle time between attenuation ramps in repeating ramp mode (in milliseconds).
        """
        return self.instrument.fnLDA_GetIdleTime(self.devid)

    def get_hold_time(self):
        """
        Gets the hold time between attenuation ramps in bidirectional ramp mode (in milliseconds).
        """
        return self.instrument.fnLDA_GetHoldTime(self.devid)

    def get_rf_on(self):
        """
        Gets the RF on/off state. Returns 1 if on, 0 if off.
        """
        return self.instrument.fnLDA_GetRF_On(self.devid)
    
    def get_profile_element(self, index):
        """
        Gets the value of a profile element (0.25 dB steps).
        index: Index of the profile element (0 to PROFILE_MAX-1)
        Returns: Attenuation in dB
        """
        att_code = self.instrument.fnLDA_GetProfileElement(self.devid, int(index))
        return att_code * 0.25

    def get_profile_element_hr(self, index):
        """
        Gets the value of a profile element (0.05 dB steps).
        index: Index of the profile element (0 to PROFILE_MAX-1)
        Returns: Attenuation in dB
        """
        att_code = self.instrument.fnLDA_GetProfileElementHR(self.devid, int(index))
        return att_code * 0.05

    def get_profile_count(self):
        """
        Gets the number of elements in the profile that will be used.
        Returns: Number of elements (int)
        """
        return self.instrument.fnLDA_GetProfileCount(self.devid)

    def get_profile_dwell_time(self):
        """
        Gets the time duration of each element in the profile during playback (in ms).
        Returns: Dwell time in milliseconds (int)
        """
        return self.instrument.fnLDA_GetProfileDwellTime(self.devid)

    def get_profile_idle_time(self):
        """
        Gets the idle time after a profile is played before repeating (in ms).
        Returns: Idle time in milliseconds (int)
        """
        return self.instrument.fnLDA_GetProfileIdleTime(self.devid)

    def get_profile_index(self):
        """
        Gets the current profile index.
        Returns: Profile index (int)
        """
        return self.instrument.fnLDA_GetProfileIndex(self.devid)

    def get_max_attenuation(self):
        """
        Gets the maximum attenuation value that the device can provide (in dB).
        Returns: Maximum attenuation in dB (float)
        """
        att_code = self.instrument.fnLDA_GetMaxAttenuation(self.devid)
        return att_code * 0.25
    
    def get_max_attenuation_hr(self):
        """
        Gets the maximum attenuation value that the device can provide (in dB, 0.05 dB steps).
        Returns: Maximum attenuation in dB (float)
        """
        att_code = self.instrument.fnLDA_GetMaxAttenuationHR(self.devid)
        return att_code * 0.05

    def get_min_attenuation(self):
        """
        Gets the minimum attenuation value that the device can provide (in dB, 0.25 dB steps).
        Returns: Minimum attenuation in dB (float)
        """
        att_code = self.instrument.fnLDA_GetMinAttenuation(self.devid)
        return att_code * 0.25

    def get_min_attenuation_hr(self):
        """
        Gets the minimum attenuation value that the device can provide (in dB, 0.05 dB steps).
        Returns: Minimum attenuation in dB (float)
        """
        att_code = self.instrument.fnLDA_GetMinAttenuationHR(self.devid)
        return att_code * 0.05

    def get_min_attenuation_step(self):
        """
        Gets the minimum attenuation step size that the device can provide (in dB).
        Returns: Minimum attenuation step size in dB (float)
        """
        step_code = self.instrument.fnLDA_GetMinAttenuationStep(self.devid)
        return step_code * 0.25

    def get_max_attenuation_step_hr(self):
        """
        Gets the maximum attenuation step size that the device can provide (in dB, 0.05 dB steps).
        Returns: Maximum attenuation step size in dB (float)
        """
        step_code = self.instrument.fnLDA_GetMaxAttenuationStepHR(self.devid)
        return step_code * 0.05