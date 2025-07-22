class Input():
    def __init__(self,instrument):
        self.instrument = instrument
    

    def set_input_attenuation(self, value: float):
        """Sets the input attenuation.
        Parameters:
        value: The attenuation value (numeric value) in current relative amplitude units."""
        self.instrument.write(f":INP:ATT {value}")

    def get_input_attenuation(self) -> float:
        """Returns the input attenuation."""
        response = self.instrument.query(":INP:ATT?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for input attenuation (not numeric): '{response}'")

    def set_input_attenuation_auto(self, auto_state: str):
        """Changes the attenuation to achieve maximum sensitivity without overloading the input channel.
        Parameters:
        auto_state: AUTO|ONCE (Boolean equivalent for AUTO, or 'ONCE')."""
        normalized_state = auto_state.upper()
        if normalized_state in {1, "ON"}:
            scpi_value = "ON"



            
        elif normalized_state in {0, "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto attenuation state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":INP:ATT:AUTO {scpi_value}")

    def get_input_attenuation_auto(self) -> str:
        """Returns whether attenuation is automatically controlled ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query(":INP:ATT:AUTO?").strip()
        if response == 1:
            return "ON"
        elif response == 0:
            return "OFF"
        else:
            return response.upper()

    def set_input_attenuation_state(self, enable: bool):
        """Turns the input attenuator ON and OFF.
        Parameters:
        enable: True to turn the attenuator ON, False to turn OFF."""
        scpi_value = 1 if enable else 0
        self.instrument.write(f":INP:ATT:STATE {scpi_value}")

    def get_input_attenuation_state(self) -> bool:
        """Returns True if the input attenuator is ON, False if OFF."""
        response = self.instrument.query(":INP:ATT:STATE?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for input attenuation state: '{response}'")

    
    def set_input_bias_current_ac(self, current: float):
        """Specifies the AC component of the bias current in Amperes.
        Parameters:
        current: The AC current component in Amperes (numeric value)."""
        self.instrument.write(f":INP:BIAS:CURR:AC {current}")

    def get_input_bias_current_ac(self) -> float:
        """Returns the AC component of the bias current in Amperes."""
        response = self.instrument.query(":INP:BIAS:CURR:AC?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for input bias AC current (not numeric): '{response}'")

    def set_input_bias_current_dc(self, current: float):
        """Specifies the DC component of the bias current in Amperes.
        Parameters:
        current: The DC current component in Amperes (numeric value)."""
        self.instrument.write(f":INP:BIAS:CURR:DC {current}")

    def get_input_bias_current_dc(self) -> float:
        """Returns the DC component of the bias current in Amperes."""
        response = self.instrument.query(":INP:BIAS:CURR:DC?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for input bias DC current (not numeric): '{response}'")

    def set_input_bias_state(self, enable: bool):
        """Sets whether or not input biasing is enabled.
        Parameters:
        enable: True to enable input biasing, False to disable."""
        scpi_value = 1 if enable else 0
        self.instrument.write(f":INP:BIAS:STATE {scpi_value}")

    def get_input_bias_state(self) -> bool:
        """Returns True if input biasing is enabled, False if not."""
        response = self.instrument.query(":INP:BIAS:STATE?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for input bias state: '{response}'")

    def set_input_bias_type(self, bias_type: str):
        """Specifies the type of bias to be generated.
        Parameters:
        bias_type: CURRent|VOLTage"""
        valid_types = {"CURRENT", "VOLTAGE", "CURR", "VOLT"}
        type_upper = bias_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid bias type: '{bias_type}'. Must be 'CURRENT' or 'VOLTAGE'.")

        if type_upper == "CURRENT": scpi_value = "CURR"
        elif type_upper == "VOLTAGE": scpi_value = "VOLT"
        else: scpi_value = type_upper

        self.instrument.write(f":INP:BIAS:TYPE {scpi_value}")

    def get_input_bias_type(self) -> str:
        """Returns the type of bias being generated ('CURRENT' or 'VOLTAGE')."""
        response = self.instrument.query(":INP:BIAS:TYPE?").strip().upper()
        if response.startswith("CURR"):
            return "CURRENT"
        elif response.startswith("VOLT"):
            return "VOLTAGE"
        return response

    def set_input_bias_voltage_ac(self, voltage: float):
        """Specifies the AC component of the bias voltage in Volts.
        Parameters:
        voltage: The AC voltage component in Volts (numeric value)."""
        self.instrument.write(f":INP:BIAS:VOLT:AC {voltage}")

    def get_input_bias_voltage_ac(self) -> float:
        """Returns the AC component of the bias voltage in Volts."""
        response = self.instrument.query(":INP:BIAS:VOLT:AC?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for input bias AC voltage (not numeric): '{response}'")

    def set_input_bias_voltage_dc(self, voltage: float):
        """Specifies the DC component of the bias voltage in Volts.
        Parameters:
        voltage: The DC voltage component in Volts (numeric value)."""
        self.instrument.write(f":INP:BIAS:VOLT:DC {voltage}")

    def get_input_bias_voltage_dc(self) -> float:
        """Returns the DC component of the bias voltage in Volts."""
        response = self.instrument.query(":INP:BIAS:VOLT:DC?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for input bias DC voltage (not numeric): '{response}'")

    def set_input_coupling(self, coupling_type: str, input_num = None):
        """Selects AC or DC coupling for the specified signal, or GROund coupling.
        Parameters:
        coupling_type: AC|DC|GROund
        input_num: Optional. The input channel number (if applicable)."""
        valid_types = {"AC", "DC", "GROUND", "GRO"}
        type_upper = coupling_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid coupling type: '{coupling_type}'. Must be 'AC', 'DC', or 'GROUND'.")

        if type_upper == "GROUND": scpi_value = "GRO"
        else: scpi_value = type_upper
        command = ":INP"
        if input_num is not None:
            command += f":{input_num}"
        command += f":COUP {scpi_value}"
        self.instrument.write(command)

    def get_input_coupling(self, input_num = None) -> str:
        """Returns the coupling type for the input signal ('AC', 'DC', or 'GROUND').
        input_num: Optional. The input channel number (if applicable)."""
        command = ":INP"
        if input_num is not None:
            command += f":{input_num}"
        command += ":COUP?"
        response = self.instrument.query(":INP:COUP?").strip().upper()
        if response.startswith("GRO"):
            return "GROUND"
        return response

    
    def set_input_filter_aweighting_state(self, enable: bool):
        """Turns the "A" weighting input filter on and off.
        Parameters:
        enable: True to turn the filter ON, False to turn OFF."""
        scpi_value = 1 if enable else 0
        self.instrument.write(f":INP:FILT:AWE:STATE {scpi_value}")

    def get_input_filter_aweighting_state(self) -> bool:
        """Returns True if the "A" weighting input filter is ON, False if OFF."""
        response = self.instrument.query(":INP:FILT:AWE:STATE?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for A-weighting filter state: '{response}'")

    def set_input_filter_hpass_frequency(self, frequency: float):
        """Determines the cutoff frequency of the high pass filter in Hertz.
        Parameters:
        frequency: The cutoff frequency in Hertz (numeric value)."""
        self.instrument.write(f":INP:FILT:HPAS:FREQ {frequency}")

    def get_input_filter_hpass_frequency(self) -> float:
        """Returns the cutoff frequency of the high pass filter in Hertz."""
        response = self.instrument.query(":INP:FILT:HPAS:FREQ?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for high pass filter frequency (not numeric): '{response}'")

    def set_input_filter_hpass_state(self, enable: bool):
        """Turns the high pass filter ON and OFF.
        Parameters:
        enable: True to turn the filter ON, False to turn OFF."""
        scpi_value = 1 if enable else 0
        self.instrument.write(f":INP:FILT:HPAS:STATE {scpi_value}")

    def get_input_filter_hpass_state(self) -> bool:
        """Returns True if the high pass filter is ON, False if OFF."""
        response = self.instrument.query(":INP:FILT:HPAS:STATE?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for high pass filter state: '{response}'")

    def set_input_filter_lpass_frequency(self, frequency: float):
        """Determines the cutoff frequency of the low pass filter in Hertz.
        Parameters:
        frequency: The cutoff frequency in Hertz (numeric value)."""
        self.instrument.write(f":INP:FILT:LPAS:FREQ {frequency}")

    def get_input_filter_lpass_frequency(self) -> float:
        """Returns the cutoff frequency of the low pass filter in Hertz."""
        response = self.instrument.query(":INP:FILT:LPAS:FREQ?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for low pass filter frequency (not numeric): '{response}'")

    def set_input_filter_lpass_state(self, enable: bool):
        """Turns the low pass filter ON and OFF.
        Parameters:
        enable: True to turn the filter ON, False to turn OFF."""
        scpi_value = 1 if enable else 0
        self.instrument.write(f":INP:FILT:LPAS:STATE {scpi_value}")

    def get_input_filter_lpass_state(self) -> bool:
        """Returns True if the low pass filter is ON, False if OFF."""
        response = self.instrument.query(":INP:FILT:LPAS:STATE?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for low pass filter state: '{response}'")

    
    def set_input_gain(self, value: float):
        """Sets the input gain.
        Parameters:
        value: The gain value (numeric value) in current relative amplitude units."""
        self.instrument.write(f":INP:GAIN {value}")

    def get_input_gain(self) -> float:
        """Returns the input gain."""
        response = self.instrument.query(":INP:GAIN?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for input gain (not numeric): '{response}'")

    def set_input_gain_auto(self, auto_state: str):
        """Changes the gain to achieve maximum sensitivity without overloading the input channel.
        Parameters:
        auto_state: AUTO|ONCE (Boolean equivalent for AUTO, or 'ONCE')."""
        normalized_state = auto_state.upper()
        if normalized_state in {1, "ON"}:
            scpi_value = "ON"
        elif normalized_state in {0, "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto gain state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":INP:GAIN:AUTO {scpi_value}")

    def get_input_gain_auto(self) -> str:
        """Returns whether gain is automatically controlled ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query(":INP:GAIN:AUTO?").strip()
        if response == 1:
            return "ON"
        elif response == 0:
            return "OFF"
        else:
            return response.upper()

    def set_input_gain_state(self, enable: bool):
        """Turns the input gain (preamplifier) ON and OFF.
        Parameters:
        enable: True to turn the preamplifier ON, False to turn OFF."""
        scpi_value = 1 if enable else 0
        self.instrument.write(f":INP:GAIN:STATE {scpi_value}")

    def get_input_gain_state(self) -> bool:
        """Returns True if the input gain (preamplifier) is ON, False if OFF."""
        response = self.instrument.query(":INP:GAIN:STATE?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for input gain state: '{response}'")

    def set_input_guard(self, guard_type: str):
        """Connects guard to signal low terminal or allows guard to float.
        Parameters:
        guard_type: LOW|FLOat"""
        valid_types = {"LOW", "FLOAT", "FLO"}
        type_upper = guard_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid guard type: '{guard_type}'. Must be 'LOW' or 'FLOAT'.")

        if type_upper == "FLOAT": scpi_value = "FLO"
        else: scpi_value = type_upper

        self.instrument.write(f":INP:GUAR {scpi_value}")

    def get_input_guard(self) -> str:
        """Returns how the guard is connected ('LOW' or 'FLOAT')."""
        response = self.instrument.query(":INP:GUAR?").strip().upper()
        if response.startswith("FLO"):
            return "FLOAT"
        return response

    def set_input_impedance(self, impedance_ohms: float):
        """Sets the termination input impedance for the input signal in Ohms.
        Parameters:
        impedance_ohms: Impedance in Ohms (numeric value)."""
        self.instrument.write(f":INP:IMP {impedance_ohms}")

    def get_input_impedance(self) -> float:
        """Returns the termination input impedance for the input signal in Ohms."""
        response = self.instrument.query(":INP:IMP?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for input impedance (not numeric): '{response}'")

    def set_input_low(self, low_type: str):
        """Connects the low signal terminal to ground or allows it to float.
        Parameters:
        low_type: FLOat|GROund"""
        valid_types = {"FLOAT", "GROUND", "FLO", "GRO"}
        type_upper = low_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid low connection type: '{low_type}'. Must be 'FLOAT' or 'GROUND'.")

        if type_upper == "FLOAT": scpi_value = "FLO"
        elif type_upper == "GROUND": scpi_value = "GRO"
        else: scpi_value = type_upper

        self.instrument.write(f":INP:LOW {scpi_value}")

    def get_input_low(self) -> str:
        """Returns how the low signal terminal is connected ('FLOAT' or 'GROUND')."""
        response = self.instrument.query(":INP:LOW?").strip().upper()
        if response.startswith("FLO"):
            return "FLOAT"
        elif response.startswith("GRO"):
            return "GROUND"
        return response

    
    def set_input_offset(self, offset_value: float):
        """Sets the input offset.
        Parameters:
        offset_value: The offset value (numeric value) in current amplitude units."""
        self.instrument.write(f":INP:OFFS {offset_value}")

    def get_input_offset(self) -> float:
        """Returns the input offset."""
        response = self.instrument.query(":INP:OFFS?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for input offset (not numeric): '{response}'")

    def set_input_offset_state(self, enable: bool):
        """Turns the effect of OFFSet ON or OFF.
        Parameters:
        enable: True to turn offset effect ON, False to turn OFF."""
        scpi_value = 1 if enable else 0
        self.instrument.write(f":INP:OFFS:STATE {scpi_value}")

    def get_input_offset_state(self) -> bool:
        """Returns True if the effect of OFFSet is ON, False if OFF."""
        response = self.instrument.query(":INP:OFFS:STATE?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for input offset state: '{response}'")

    def set_input_polarity(self, polarity_type: str):
        """Sets or queries the input polarity.
        Parameters:
        polarity_type: NORMal|INVerted"""
        valid_types = {"NORMAL", "INVERTED", "NORM", "INV"}
        type_upper = polarity_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid polarity type: '{polarity_type}'. Must be 'NORMAL' or 'INVERTED'.")

        if type_upper == "NORMAL": scpi_value = "NORM"
        elif type_upper == "INVERTED": scpi_value = "INV"
        else: scpi_value = type_upper

        self.instrument.write(f":INP:POL {scpi_value}")

    def get_input_polarity(self) -> str:
        """Returns the input polarity ('NORMAL' or 'INVERTED')."""
        response = self.instrument.query(":INP:POL?").strip().upper()
        if response.startswith("NORM"):
            return "NORMAL"
        elif response.startswith("INV"):
            return "INVERTED"
        return response

    def set_input_polarization(self, value_radians: float):
        """Sets the polarization of the input in radians.
        Parameters:
        value_radians: Polarization value in radians (numeric value)."""
        self.instrument.write(f":INP:POLZ {value_radians}")

    def get_input_polarization(self) -> float:
        """Returns the polarization of the input in radians."""
        response = self.instrument.query(":INP:POLZ?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for input polarization (not numeric): '{response}'")

    def set_input_polarization_horizontal(self):
        """Sets the polarization of the input to zero (horizontal).
        Notes: This is an event command; no query."""
        self.instrument.write(f":INP:POLZ:HOR")

    def set_input_polarization_vertical(self):
        """Sets the polarization of the input to PI/2 radians (vertical).
        Notes: This is an event command; no query."""
        self.instrument.write(f":INP:POLZ:VERT")

    
    def set_input_position_x_angle_direction(self, direction: str):
        """Controls the direction of the movement for X-axis angle rotation.
        Parameters:
        direction: UP|DOWN"""
        valid_directions = {"UP", "DOWN"}
        direction_upper = direction.upper()
        if direction_upper not in valid_directions:
            raise ValueError(f"Invalid direction: '{direction}'. Must be 'UP' or 'DOWN'.")
        self.instrument.write(f":INP:POS:X:ANG:DIR {direction_upper}")

    def get_input_position_x_angle_direction(self) -> str:
        """Returns the direction of the movement for X-axis angle rotation ('UP' or 'DOWN')."""
        response = self.instrument.query(":INP:POS:X:ANG:DIR?").strip().upper()
        return response

    def set_input_position_x_angle_immediate(self, value: float):
        """Indicates that the input is moved to the specified X-axis angle position without waiting for further commands.
        Parameters:
        value: The immediate position value (numeric value)."""
        self.instrument.write(f":INP:POS:X:ANG:IMM {value}")

    def get_input_position_x_angle_immediate(self) -> float:
        """Returns the immediate position value for X-axis angle."""
        response = self.instrument.query(":INP:POS:X:ANG:IMM?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for X-axis angle immediate position (not numeric): '{response}'")

    def set_input_position_x_angle_limit_high(self, value: float):
        """Sets the maximum for the X-axis angle position limit.
        Parameters:
        value: The maximum position value (numeric value)."""
        self.instrument.write(f":INP:POS:X:ANG:LIM:HIGH {value}")

    def get_input_position_x_angle_limit_high(self) -> float:
        """Returns the maximum for the X-axis angle position limit."""
        response = self.instrument.query(":INP:POS:X:ANG:LIM:HIGH?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for X-axis angle limit high (not numeric): '{response}'")

    def set_input_position_x_angle_limit_low(self, value: float):
        """Sets the minimum for the X-axis angle position limit.
        Parameters:
        value: The minimum position value (numeric value)."""
        self.instrument.write(f":INP:POS:X:ANG:LIM:LOW {value}")

    def get_input_position_x_angle_limit_low(self) -> float:
        """Returns the minimum for the X-axis angle position limit."""
        response = self.instrument.query(":INP:POS:X:ANG:LIM:LOW?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for X-axis angle limit low (not numeric): '{response}'")

    def set_input_position_x_angle_limit_state(self, enable: bool):
        """Controls whether the X-axis angle limit is enabled.
        Parameters:
        enable: True to enable the limit, False to disable."""
        scpi_value = 1 if enable else 0
        self.instrument.write(f":INP:POS:X:ANG:LIM:STATE {scpi_value}")

    def get_input_position_x_angle_limit_state(self) -> bool:
        """Returns True if the X-axis angle limit is enabled, False if not."""
        response = self.instrument.query(":INP:POS:X:ANG:LIM:STATE?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for X-axis angle limit state: '{response}'")

    def set_input_position_x_angle_offset(self, value: float):
        """Defines a single value that is subtracted from the physical X-axis angle position.
        Parameters:
        value: The offset value (numeric value)."""
        self.instrument.write(f":INP:POS:X:ANG:OFFS {value}")

    def get_input_position_x_angle_offset(self) -> float:
        """Returns the offset value for the X-axis angle position."""
        response = self.instrument.query(":INP:POS:X:ANG:OFFS?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for X-axis angle offset (not numeric): '{response}'")

    
    def set_input_position_x_angle_velocity(self, value: float):
        """Controls the velocity of the angular rotation around the x-axis.
        Parameters:
        value: The velocity value (numeric value)."""
        self.instrument.write(f":INP:POS:X:ANG:VEL {value}")

    def get_input_position_x_angle_velocity(self) -> float:
        """Returns the velocity of the angular rotation around the x-axis."""
        response = self.instrument.query(":INP:POS:X:ANG:VEL?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for X-axis angle velocity (not numeric): '{response}'")

    def set_input_position_x_distance_direction(self, direction: str):
        """Controls the direction of the movement for X-axis linear distance.
        Parameters:
        direction: UP|DOWN"""
        valid_directions = {"UP", "DOWN"}
        direction_upper = direction.upper()
        if direction_upper not in valid_directions:
            raise ValueError(f"Invalid direction: '{direction}'. Must be 'UP' or 'DOWN'.")
        self.instrument.write(f":INP:POS:X:DIST:DIR {direction_upper}")

    def get_input_position_x_distance_direction(self) -> str:
        """Returns the direction of the movement for X-axis linear distance ('UP' or 'DOWN')."""
        response = self.instrument.query(":INP:POS:X:DIST:DIR?").strip().upper()
        return response

    def set_input_position_x_distance_immediate(self, value: float):
        """Indicates that the input is moved to the specified X-axis linear distance position without waiting for further commands.
        Parameters:
        value: The immediate position value (numeric value)."""
        self.instrument.write(f":INP:POS:X:DIST:IMM {value}")

    def get_input_position_x_distance_immediate(self) -> float:
        """Returns the immediate position value for X-axis linear distance."""
        response = self.instrument.query(":INP:POS:X:DIST:IMM?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for X-axis distance immediate position (not numeric): '{response}'")

    def set_input_position_x_distance_limit_high(self, value: float):
        """Sets the maximum for the X-axis linear distance position limit.
        Parameters:
        value: The maximum position value (numeric value)."""
        self.instrument.write(f":INP:POS:X:DIST:LIM:HIGH {value}")

    def get_input_position_x_distance_limit_high(self) -> float:
        """Returns the maximum for the X-axis linear distance position limit."""
        response = self.instrument.query(":INP:POS:X:DIST:LIM:HIGH?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for X-axis distance limit high (not numeric): '{response}'")

    def set_input_position_x_distance_limit_low(self, value: float):
        """Sets the minimum for the X-axis linear distance position limit.
        Parameters:
        value: The minimum position value (numeric value)."""
        self.instrument.write(f":INP:POS:X:DIST:LIM:LOW {value}")

    def get_input_position_x_distance_limit_low(self) -> float:
        """Returns the minimum for the X-axis linear distance position limit."""
        response = self.instrument.query(":INP:POS:X:DIST:LIM:LOW?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for X-axis distance limit low (not numeric): '{response}'")

    def set_input_position_x_distance_limit_state(self, enable: bool):
        """Controls whether the X-axis linear distance limit is enabled.
        Parameters:
        enable: True to enable the limit, False to disable."""
        scpi_value = 1 if enable else 0
        self.instrument.write(f":INP:POS:X:DIST:LIM:STATE {scpi_value}")

    def get_input_position_x_distance_limit_state(self) -> bool:
        """Returns True if the X-axis linear distance limit is enabled, False if not."""
        response = self.instrument.query(":INP:POS:X:DIST:LIM:STATE?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for X-axis distance limit state: '{response}'")

    def set_input_position_x_distance_offset(self, value: float):
        """Defines a single value that is subtracted from the physical X-axis linear distance position.
        Parameters:
        value: The offset value (numeric value)."""
        self.instrument.write(f":INP:POS:X:DIST:OFFS {value}")

    def get_input_position_x_distance_offset(self) -> float:
        """Returns the offset value for the X-axis linear distance position."""
        response = self.instrument.query(":INP:POS:X:DIST:OFFS?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for X-axis distance offset (not numeric): '{response}'")

    
    def set_input_position_x_distance_velocity(self, value: float):
        """Controls the velocity of the displacement on the x-axis.
        Parameters:
        value: The velocity value (numeric value)."""
        self.instrument.write(f":INP:POS:X:DIST:VEL {value}")

    def get_input_position_x_distance_velocity(self) -> float:
        """Returns the velocity of the displacement on the x-axis."""
        response = self.instrument.query(":INP:POS:X:DIST:VEL?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for X-axis distance velocity (not numeric): '{response}'")

    def set_input_position_y_angle_direction(self, direction: str):
        """Controls the direction of the movement for Y-axis angle rotation.
        Parameters:
        direction: UP|DOWN"""
        valid_directions = {"UP", "DOWN"}
        direction_upper = direction.upper()
        if direction_upper not in valid_directions:
            raise ValueError(f"Invalid direction: '{direction}'. Must be 'UP' or 'DOWN'.")
        self.instrument.write(f":INP:POS:Y:ANG:DIR {direction_upper}")

    def get_input_position_y_angle_direction(self) -> str:
        """Returns the direction of the movement for Y-axis angle rotation ('UP' or 'DOWN')."""
        response = self.instrument.query(":INP:POS:Y:ANG:DIR?").strip().upper()
        return response

    def set_input_position_y_angle_immediate(self, value: float):
        """Indicates that the input is moved to the specified Y-axis angle position without waiting for further commands.
        Parameters:
        value: The immediate position value (numeric value)."""
        self.instrument.write(f":INP:POS:Y:ANG:IMM {value}")

    def get_input_position_y_angle_immediate(self) -> float:
        """Returns the immediate position value for Y-axis angle."""
        response = self.instrument.query(":INP:POS:Y:ANG:IMM?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Y-axis angle immediate position (not numeric): '{response}'")

    def set_input_position_y_angle_limit_high(self, value: float):
        """Sets the maximum for the Y-axis angle position limit.
        Parameters:
        value: The maximum position value (numeric value)."""
        self.instrument.write(f":INP:POS:Y:ANG:LIM:HIGH {value}")

    def get_input_position_y_angle_limit_high(self) -> float:
        """Returns the maximum for the Y-axis angle position limit."""
        response = self.instrument.query(":INP:POS:Y:ANG:LIM:HIGH?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Y-axis angle limit high (not numeric): '{response}'")

    def set_input_position_y_angle_limit_low(self, value: float):
        """Sets the minimum for the Y-axis angle position limit.
        Parameters:
        value: The minimum position value (numeric value)."""
        self.instrument.write(f":INP:POS:Y:ANG:LIM:LOW {value}")

    def get_input_position_y_angle_limit_low(self) -> float:
        """Returns the minimum for the Y-axis angle position limit."""
        response = self.instrument.query(":INP:POS:Y:ANG:LIM:LOW?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Y-axis angle limit low (not numeric): '{response}'")

    def set_input_position_y_angle_limit_state(self, enable: bool):
        """Controls whether the Y-axis angle limit is enabled.
        Parameters:
        enable: True to enable the limit, False to disable."""
        scpi_value = 1 if enable else 0
        self.instrument.write(f":INP:POS:Y:ANG:LIM:STATE {scpi_value}")

    def get_input_position_y_angle_limit_state(self) -> bool:
        """Returns True if the Y-axis angle limit is enabled, False if not."""
        response = self.instrument.query(":INP:POS:Y:ANG:LIM:STATE?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for Y-axis angle limit state: '{response}'")

    def set_input_position_y_angle_offset(self, value: float):
        """Defines a single value that is subtracted from the physical Y-axis angle position.
        Parameters:
        value: The offset value (numeric value)."""
        self.instrument.write(f":INP:POS:Y:ANG:OFFS {value}")

    def get_input_position_y_angle_offset(self) -> float:
        """Returns the offset value for the Y-axis angle position."""
        response = self.instrument.query(":INP:POS:Y:ANG:OFFS?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Y-axis angle offset (not numeric): '{response}'")

    
    def set_input_position_y_angle_velocity(self, value: float):
        """Controls the velocity of the angular rotation around the y-axis.
        Parameters:
        value: The velocity value (numeric value)."""
        self.instrument.write(f":INP:POS:Y:ANG:VEL {value}")

    def get_input_position_y_angle_velocity(self) -> float:
        """Returns the velocity of the angular rotation around the y-axis."""
        response = self.instrument.query(":INP:POS:Y:ANG:VEL?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Y-axis angle velocity (not numeric): '{response}'")

    def set_input_position_y_distance_direction(self, direction: str):
        """Controls the direction of the movement for Y-axis linear distance.
        Parameters:
        direction: UP|DOWN"""
        valid_directions = {"UP", "DOWN"}
        direction_upper = direction.upper()
        if direction_upper not in valid_directions:
            raise ValueError(f"Invalid direction: '{direction}'. Must be 'UP' or 'DOWN'.")
        self.instrument.write(f":INP:POS:Y:DIST:DIR {direction_upper}")

    def get_input_position_y_distance_direction(self) -> str:
        """Returns the direction of the movement for Y-axis linear distance ('UP' or 'DOWN')."""
        response = self.instrument.query(":INP:POS:Y:DIST:DIR?").strip().upper()
        return response

    def set_input_position_y_distance_immediate(self, value: float):
        """Indicates that the input is moved to the specified Y-axis linear distance position without waiting for further commands.
        Parameters:
        value: The immediate position value (numeric value)."""
        self.instrument.write(f":INP:POS:Y:DIST:IMM {value}")

    def get_input_position_y_distance_immediate(self) -> float:
        """Returns the immediate position value for Y-axis linear distance."""
        response = self.instrument.query(":INP:POS:Y:DIST:IMM?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Y-axis distance immediate position (not numeric): '{response}'")

    def set_input_position_y_distance_limit_high(self, value: float):
        """Sets the maximum for the Y-axis linear distance position limit.
        Parameters:
        value: The maximum position value (numeric value)."""
        self.instrument.write(f":INP:POS:Y:DIST:LIM:HIGH {value}")

    def get_input_position_y_distance_limit_high(self) -> float:
        """Returns the maximum for the Y-axis linear distance position limit."""
        response = self.instrument.query(":INP:POS:Y:DIST:LIM:HIGH?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Y-axis distance limit high (not numeric): '{response}'")

    def set_input_position_y_distance_limit_low(self, value: float):
        """Sets the minimum for the Y-axis linear distance position limit.
        Parameters:
        value: The minimum position value (numeric value)."""
        self.instrument.write(f":INP:POS:Y:DIST:LIM:LOW {value}")

    def get_input_position_y_distance_limit_low(self) -> float:
        """Returns the minimum for the Y-axis linear distance position limit."""
        response = self.instrument.query(":INP:POS:Y:DIST:LIM:LOW?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Y-axis distance limit low (not numeric): '{response}'")

    def set_input_position_y_distance_limit_state(self, enable: bool):
        """Controls whether the Y-axis linear distance limit is enabled.
        Parameters:
        enable: True to enable the limit, False to disable."""
        scpi_value = 1 if enable else 0
        self.instrument.write(f":INP:POS:Y:DIST:LIM:STATE {scpi_value}")

    def get_input_position_y_distance_limit_state(self) -> bool:
        """Returns True if the Y-axis linear distance limit is enabled, False if not."""
        response = self.instrument.query(":INP:POS:Y:DIST:LIM:STATE?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for Y-axis distance limit state: '{response}'")

    def set_input_position_y_distance_offset(self, value: float):
        """Defines a single value that is subtracted from the physical Y-axis linear distance position.
        Parameters:
        value: The offset value (numeric value)."""
        self.instrument.write(f":INP:POS:Y:DIST:OFFS {value}")

    def get_input_position_y_distance_offset(self) -> float:
        """Returns the offset value for the Y-axis linear distance position."""
        response = self.instrument.query(":INP:POS:Y:DIST:OFFS?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Y-axis distance offset (not numeric): '{response}'")

    
    def set_input_position_z_angle_direction(self, direction: str):
        """Controls the direction of the movement for Z-axis angle rotation.
        Parameters:
        direction: UP|DOWN"""
        valid_directions = {"UP", "DOWN"}
        direction_upper = direction.upper()
        if direction_upper not in valid_directions:
            raise ValueError(f"Invalid direction: '{direction}'. Must be 'UP' or 'DOWN'.")
        self.instrument.write(f":INP:POS:Z:ANG:DIR {direction_upper}")

    def get_input_position_z_angle_direction(self) -> str:
        """Returns the direction of the movement for Z-axis angle rotation ('UP' or 'DOWN')."""
        response = self.instrument.query(":INP:POS:Z:ANG:DIR?").strip().upper()
        return response

    def set_input_position_z_angle_immediate(self, value: float):
        """Indicates that the input is moved to the specified Z-axis angle position without waiting for further commands.
        Parameters:
        value: The immediate position value (numeric value)."""
        self.instrument.write(f":INP:POS:Z:ANG:IMM {value}")

    def get_input_position_z_angle_immediate(self) -> float:
        """Returns the immediate position value for Z-axis angle."""
        response = self.instrument.query(":INP:POS:Z:ANG:IMM?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Z-axis angle immediate position (not numeric): '{response}'")

    def set_input_position_z_angle_limit_high(self, value: float):
        """Sets the maximum for the Z-axis angle position limit.
        Parameters:
        value: The maximum position value (numeric value)."""
        self.instrument.write(f":INP:POS:Z:ANG:LIM:HIGH {value}")

    def get_input_position_z_angle_limit_high(self) -> float:
        """Returns the maximum for the Z-axis angle position limit."""
        response = self.instrument.query(":INP:POS:Z:ANG:LIM:HIGH?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Z-axis angle limit high (not numeric): '{response}'")

    def set_input_position_z_angle_limit_low(self, value: float):
        """Sets the minimum for the Z-axis angle position limit.
        Parameters:
        value: The minimum position value (numeric value)."""
        self.instrument.write(f":INP:POS:Z:ANG:LIM:LOW {value}")

    def get_input_position_z_angle_limit_low(self) -> float:
        """Returns the minimum for the Z-axis angle position limit."""
        response = self.instrument.query(":INP:POS:Z:ANG:LIM:LOW?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Z-axis angle limit low (not numeric): '{response}'")

    def set_input_position_z_angle_limit_state(self, enable: bool):
        """Controls whether the Z-axis angle limit is enabled.
        Parameters:
        enable: True to enable the limit, False to disable."""
        scpi_value = 1 if enable else 0
        self.instrument.write(f":INP:POS:Z:ANG:LIM:STATE {scpi_value}")

    def get_input_position_z_angle_limit_state(self) -> bool:
        """Returns True if the Z-axis angle limit is enabled, False if not."""
        response = self.instrument.query(":INP:POS:Z:ANG:LIM:STATE?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for Z-axis angle limit state: '{response}'")

    def set_input_position_z_angle_offset(self, value: float):
        """Defines a single value that is subtracted from the physical Z-axis angle position.
        Parameters:
        value: The offset value (numeric value)."""
        self.instrument.write(f":INP:POS:Z:ANG:OFFS {value}")

    def get_input_position_z_angle_offset(self) -> float:
        """Returns the offset value for the Z-axis angle position."""
        response = self.instrument.query(":INP:POS:Z:ANG:OFFS?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Z-axis angle offset (not numeric): '{response}'")

    
    def set_input_position_z_angle_velocity(self, value: float):
        """Controls the velocity of the angular rotation around the z-axis.
        Parameters:
        value: The velocity value (numeric value)."""
        self.instrument.write(f":INP:POS:Z:ANG:VEL {value}")

    def get_input_position_z_angle_velocity(self) -> float:
        """Returns the velocity of the angular rotation around the z-axis."""
        response = self.instrument.query(":INP:POS:Z:ANG:VEL?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Z-axis angle velocity (not numeric): '{response}'")

    def set_input_position_z_distance_direction(self, direction: str):
        """Controls the direction of the movement for Z-axis linear distance.
        Parameters:
        direction: UP|DOWN"""
        valid_directions = {"UP", "DOWN"}
        direction_upper = direction.upper()
        if direction_upper not in valid_directions:
            raise ValueError(f"Invalid direction: '{direction}'. Must be 'UP' or 'DOWN'.")
        self.instrument.write(f":INP:POS:Z:DIST:DIR {direction_upper}")

    def get_input_position_z_distance_direction(self) -> str:
        """Returns the direction of the movement for Z-axis linear distance ('UP' or 'DOWN')."""
        response = self.instrument.query(":INP:POS:Z:DIST:DIR?").strip().upper()
        return response

    def set_input_position_z_distance_immediate(self, value: float):
        """Indicates that the input is moved to the specified Z-axis linear distance position without waiting for further commands.
        Parameters:
        value: The immediate position value (numeric value)."""
        self.instrument.write(f":INP:POS:Z:DIST:IMM {value}")

    def get_input_position_z_distance_immediate(self) -> float:
        """Returns the immediate position value for Z-axis linear distance."""
        response = self.instrument.query(":INP:POS:Z:DIST:IMM?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Z-axis distance immediate position (not numeric): '{response}'")

    def set_input_position_z_distance_limit_high(self, value: float):
        """Sets the maximum for the Z-axis linear distance position limit.
        Parameters:
        value: The maximum position value (numeric value)."""
        self.instrument.write(f":INP:POS:Z:DIST:LIM:HIGH {value}")

    def get_input_position_z_distance_limit_high(self) -> float:
        """Returns the maximum for the Z-axis linear distance position limit."""
        response = self.instrument.query(":INP:POS:Z:DIST:LIM:HIGH?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Z-axis distance limit high (not numeric): '{response}'")

    def set_input_position_z_distance_limit_low(self, value: float):
        """Sets the minimum for the Z-axis linear distance position limit.
        Parameters:
        value: The minimum position value (numeric value)."""
        self.instrument.write(f":INP:POS:Z:DIST:LIM:LOW {value}")

    def get_input_position_z_distance_limit_low(self) -> float:
        """Returns the minimum for the Z-axis linear distance position limit."""
        response = self.instrument.query(":INP:POS:Z:DIST:LIM:LOW?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Z-axis distance limit low (not numeric): '{response}'")

    def set_input_position_z_distance_limit_state(self, enable: bool):
        """Controls whether the Z-axis linear distance limit is enabled.
        Parameters:
        enable: True to enable the limit, False to disable."""
        scpi_value = 1 if enable else 0
        self.instrument.write(f":INP:POS:Z:DIST:LIM:STATE {scpi_value}")

    def get_input_position_z_distance_limit_state(self) -> bool:
        """Returns True if the Z-axis linear distance limit is enabled, False if not."""
        response = self.instrument.query(":INP:POS:Z:DIST:LIM:STATE?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for Z-axis distance limit state: '{response}'")

    def set_input_position_z_distance_offset(self, value: float):
        """Defines a single value that is subtracted from the physical Z-axis linear distance position.
        Parameters:
        value: The offset value (numeric value)."""
        self.instrument.write(f":INP:POS:Z:DIST:OFFS {value}")

    def get_input_position_z_distance_offset(self) -> float:
        """Returns the offset value for the Z-axis linear distance position."""
        response = self.instrument.query(":INP:POS:Z:DIST:OFFS?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Z-axis distance offset (not numeric): '{response}'")

    
    def set_input_position_z_distance_velocity(self, value: float):
        """Controls the velocity of the displacement on the z-axis.
        Parameters:
        value: The velocity value (numeric value)."""
        self.instrument.write(f":INP:POS:Z:DIST:VEL {value}")

    def get_input_position_z_distance_velocity(self) -> float:
        """Returns the velocity of the displacement on the z-axis."""
        response = self.instrument.query(":INP:POS:Z:DIST:VEL?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for Z-axis distance velocity (not numeric): '{response}'")

    def set_input_state(self, enable: bool):
        """Connects the input terminal to the measurement signal path when ON.
        Parameters:
        enable: True to connect input terminal, False for maximum isolation."""
        scpi_value = 1 if enable else 0
        self.instrument.write(f":INP:STATE {scpi_value}")

    def get_input_state(self) -> bool:
        """Returns True if the input terminal is connected to the measurement signal path, False if not."""
        response = self.instrument.query(":INP:STATE?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for input state: '{response}'")

    def set_input_type(self, input_type_char: str):
        """Selects the input characteristic to be used if more than one is available.
        Parameters:
        input_type_char: BALanced|UNBalanced"""
        valid_types = {"BALANCED", "UNBALANCED", "BAL", "UNB"}
        type_upper = input_type_char.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid input type: '{input_type_char}'. Must be 'BALANCED' or 'UNBALANCED'.")

        if type_upper == "BALANCED": scpi_value = "BAL"
        elif type_upper == "UNBALANCED": scpi_value = "UNB"
        else: scpi_value = type_upper

        self.instrument.write(f":INP:TYPE {scpi_value}")

    def get_input_type(self) -> str:
        """Returns the input characteristic being used ('BALANCED' or 'UNBALANCED')."""
        response = self.instrument.query(":INP:TYPE?").strip().upper()
        if response.startswith("BAL"):
            return "BALANCED"
        elif response.startswith("UNB"):
            return "UNBALANCED"
        return response

