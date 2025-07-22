class Sense():
    def __init__(self,instrument):
        self.instrument = instrument
    
     
    def set_sense_am_depth_range_auto(self, auto_state: str):
        """Sets the range for the AM sensor function to a value determined to give the most dynamic range.
        Parameters:
        auto_state: Boolean (ON|OFF) or 'ONCE'. Selecting 'ONCE' sets AUTO to ON and then OFF."""
        normalized_state = auto_state.upper()
        if normalized_state in {1, "ON"}:
            scpi_value = "ON"
        elif normalized_state in {0, "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":SENS:AM:DEP:RANG:AUTO {scpi_value}")

    def get_sense_am_depth_range_auto(self) -> str:
        """Returns the auto state of the AM depth range ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query(":SENS:AM:DEP:RANG:AUTO?").strip()
        if response == 1:
            return "ON"
        elif response == 0:
            return "OFF"
        else:
            return response.upper()

    def set_sense_am_depth_range_upper(self, value: float):
        """Specifies the maximum signal level expected for the AM sensor input.
        Parameters:
        value: The upper range value (numeric value)."""
        self.instrument.write(f":SENS:AM:DEP:RANG:UPP {value}")

    def get_sense_am_depth_range_upper(self) -> float:
        """Returns the maximum signal level expected for the AM sensor input."""
        response = self.instrument.query(":SENS:AM:DEP:RANG:UPP?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for AM depth range upper (not numeric): '{response}'")

    def set_sense_am_depth_range_lower(self, value: float):
        """Specifies the smallest signal level expected for the AM sensor input.
        Parameters:
        value: The lower range value (numeric value)."""
        self.instrument.write(f":SENS:AM:DEP:RANG:LOW {value}")

    def get_sense_am_depth_range_lower(self) -> float:
        """Returns the smallest signal level expected for the AM sensor input."""
        response = self.instrument.query(":SENS:AM:DEP:RANG:LOW?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for AM depth range lower (not numeric): '{response}'")

    def set_sense_am_type(self, demod_type: str):
        """Sets the type of amplitude demodulation technique the demodulator uses.
        Parameters:
        demod_type: LINear|LOGarithmic"""
        valid_types = {"LINEAR", "LOGARITHMIC", "LIN", "LOG"}
        type_upper = demod_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid AM demodulation type: '{demod_type}'. Must be 'LINEAR' or 'LOGARITHMIC'.")

        if type_upper == "LINEAR": scpi_value = "LIN"
        elif type_upper == "LOGARITHMIC": scpi_value = "LOG"
        else: scpi_value = type_upper

        self.instrument.write(f":SENS:AM:TYPE {scpi_value}")

    def get_sense_am_type(self) -> str:
        """Returns the type of amplitude demodulation technique ('LINEAR' or 'LOGARITHMIC')."""
        response = self.instrument.query(":SENS:AM:TYPE?").strip().upper()
        if response.startswith("LIN"):
            return "LINEAR"
        elif response.startswith("LOG"):
            return "LOGARITHMIC"
        return response

    
    def set_sense_average_count(self, value: int):
        """Specifies the number of measurements to combine using the :TYPE setting.
        Parameters:
        value: The number of measurements (numeric value)."""
        if not isinstance(value, int) or value < 1:
            raise ValueError("Count must be a positive integer.")
        self.instrument.write(f":SENS:AVER:COUN {value}")

    def get_sense_average_count(self) -> int:
        """Returns the number of measurements to combine for averaging."""
        response = self.instrument.query(":SENS:AVER:COUN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for average count (not integer): '{response}'")

    def set_sense_average_count_auto(self, auto_state: str):
        """Allows the device to select an appropriate value for :COUNt.
        Parameters:
        auto_state: Boolean (ON|OFF) or 'ONCE'. Selecting 'ONCE' sets AUTO to ON and then OFF."""
        normalized_state = auto_state.upper()
        if normalized_state in {1, "ON"}:
            scpi_value = "ON"
        elif normalized_state in {0, "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":SENS:AVER:COUN:AUTO {scpi_value}")

    def get_sense_average_count_auto(self) -> str:
        """Returns the auto state of the average count ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query(":SENS:AVER:COUN:AUTO?").strip()
        if response == 1:
            return "ON"
        elif response == 0:
            return "OFF"
        else:
            return response.upper()

    def set_sense_average_state(self, enable: bool):
        """Turns averaging ON and OFF.
        Parameters:
        enable: True to turn averaging ON, False to turn OFF."""
        scpi_value = 1 if enable else 0
        self.instrument.write(f":SENS:AVER:STATE {scpi_value}")

    def get_sense_average_state(self) -> bool:
        """Returns True if averaging is ON, False if OFF."""
        response = self.instrument.query(":SENS:AVER:STATE?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for average state: '{response}'")

    def set_sense_average_tcontrol(self, tcontrol_type: str):
        """Specifies the action of the AVERage subsystem when more than AVERage:COUNt measurement results are generated.
        Parameters:
        tcontrol_type: EXPonential|MOVing|NORMal|REPeat"""
        valid_types = {"EXPONENTIAL", "MOVING", "NORMAL", "REPEAT", "EXP", "MOV", "NORM", "REP"}
        type_upper = tcontrol_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid TCONtrol type: '{tcontrol_type}'.")

        if type_upper == "EXPONENTIAL": scpi_value = "EXP"
        elif type_upper == "MOVING": scpi_value = "MOV"
        elif type_upper == "NORMAL": scpi_value = "NORM"
        elif type_upper == "REPEAT": scpi_value = "REP"
        else: scpi_value = type_upper

        self.instrument.write(f":SENS:AVER:TCON {scpi_value}")

    def get_sense_average_tcontrol(self) -> str:
        """Returns the action of the AVERage subsystem ('EXPONENTIAL', 'MOVING', 'NORMAL', or 'REPEAT')."""
        response = self.instrument.query(":SENS:AVER:TCON?").strip().upper()
        if response.startswith("EXP"):
            return "EXPONENTIAL"
        elif response.startswith("MOV"):
            return "MOVING"
        elif response.startswith("NORM"):
            return "NORMAL"
        elif response.startswith("REP"):
            return "REPeat"
        return response

    def set_sense_average_type(self, average_type: str):
        """Selects the type of averaging.
        Parameters:
        average_type: COMPlex|ENVelope|MAXimum|MINimum|RMS|SCALar"""
        valid_types = {"COMPLEX", "ENVELOPE", "MAXIMUM", "MINIMUM", "RMS", "SCALAR", "COMP", "ENV", "MAX", "MIN", "SCAL"}
        type_upper = average_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid average type: '{average_type}'.")

        if type_upper == "COMPLEX": scpi_value = "COMP"
        elif type_upper == "ENVELOPE": scpi_value = "ENV"
        elif type_upper == "MAXIMUM": scpi_value = "MAX"
        elif type_upper == "MINIMUM": scpi_value = "MIN"
        elif type_upper == "SCALAR": scpi_value = "SCAL"
        else: scpi_value = type_upper

        self.instrument.write(f":SENS:AVER:TYPE {scpi_value}")

    def get_sense_average_type(self) -> str:
        """Returns the type of averaging ('COMPLEX', 'ENVELOPE', 'MAXIMUM', 'MINIMUM', 'RMS', or 'SCALAR')."""
        response = self.instrument.query(":SENS:AVER:TYPE?").strip().upper()
        if response.startswith("COMP"):
            return "COMPLEX"
        elif response.startswith("ENV"):
            return "ENVELOPE"
        elif response.startswith("MAX"):
            return "MAXIMUM"
        elif response.startswith("MIN"):
            return "MINIMUM"
        elif response.startswith("SCAL"):
            return "SCALAR"
        return response

    
    def set_sense_bandwidth_resolution(self, value: float):
        """Controls the resolution bandwidth of the instrument in Hz.
        Parameters:
        value: The resolution bandwidth in Hz (numeric value)."""
        self.instrument.write(f":SENS:BAND:RES {value}")

    def get_sense_bandwidth_resolution(self) -> float:
        """Returns the resolution bandwidth of the instrument in Hz."""
        response = self.instrument.query(":SENS:BAND:RES?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for bandwidth resolution (not numeric): '{response}'")

    def set_sense_bandwidth_resolution_auto(self, auto_state: str):
        """Couples the resolution bandwidth to other parameters of the measurement.
        Parameters:
        auto_state: Boolean (ON|OFF) or 'ONCE'. Selecting 'ONCE' sets AUTO to ON and then OFF."""
        normalized_state = auto_state.upper()
        if normalized_state in {1, "ON"}:
            scpi_value = "ON"
        elif normalized_state in {0, "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":SENS:BAND:RES:AUTO {scpi_value}")

    def get_sense_bandwidth_resolution_auto(self) -> str:
        """Returns the auto state of the resolution bandwidth ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query(":SENS:BAND:RES:AUTO?").strip()
        if response == 1:
            return "ON"
        elif response == 0:
            return "OFF"
        else:
            return response.upper()

    def set_sense_bandwidth_resolution_ratio(self, value: float):
        """Controls the ratio of resolution bandwidth to span when coupled (RESolution (Hz)/SPAN(Hz)).
        Parameters:
        value: The ratio (numeric value)."""
        self.instrument.write(f":SENS:BAND:RES:RAT {value}")

    def get_sense_bandwidth_resolution_ratio(self) -> float:
        """Returns the ratio of resolution bandwidth to span."""
        response = self.instrument.query(":SENS:BAND:RES:RAT?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for bandwidth resolution ratio (not numeric): '{response}'")

    def set_sense_bandwidth_resolution_track(self, enable: bool):
        """Allows the resolution bandwidth to dynamically change during a logarithmic frequency sweep.
        Parameters:
        enable: True to enable tracking, False to disable."""
        scpi_value = 1 if enable else 0
        self.instrument.write(f":SENS:BAND:RES:TRACK {scpi_value}")

    def get_sense_bandwidth_resolution_track(self) -> bool:
        """Returns True if resolution bandwidth tracking is ON, False if OFF."""
        response = self.instrument.query(":SENS:BAND:RES:TRACK?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for bandwidth resolution track state: '{response}'")

    def set_sense_bandwidth_video(self, value: float):
        """Controls the video filtering (post-detection filtering) in Hertz.
        Parameters:
        value: The video bandwidth in Hz (numeric value)."""
        self.instrument.write(f":SENS:BAND:VID {value}")

    def get_sense_bandwidth_video(self) -> float:
        """Returns the video filtering bandwidth in Hertz."""
        response = self.instrument.query(":SENS:BAND:VID?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for bandwidth video (not numeric): '{response}'")

    
    def set_sense_bandwidth_video_auto(self, auto_state: str):
        """Couples the value of video bandwidth to instrument-determined values.
        Parameters:
        auto_state: Boolean (ON|OFF) or 'ONCE'. Selecting 'ONCE' sets AUTO to ON and then OFF."""
        normalized_state = auto_state.upper()
        if normalized_state in {1, "ON"}:
            scpi_value = "ON"
        elif normalized_state in {0, "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":SENS:BAND:VID:AUTO {scpi_value}")

    def get_sense_bandwidth_video_auto(self) -> str:
        """Returns the auto state of the video bandwidth ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query(":SENS:BAND:VID:AUTO?").strip()
        if response == 1:
            return "ON"
        elif response == 0:
            return "OFF"
        else:
            return response.upper()

    def set_sense_bandwidth_video_ratio(self, value: float):
        """Controls the ratio of video bandwidth to resolution bandwidth when coupled (VIDeo(Hz)/RESolution(Hz)).
        Parameters:
        value: The ratio (numeric value)."""
        self.instrument.write(f":SENS:BAND:VID:RAT {value}")

    def get_sense_bandwidth_video_ratio(self) -> float:
        """Returns the ratio of video bandwidth to resolution bandwidth."""
        response = self.instrument.query(":SENS:BAND:VID:RAT?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for bandwidth video ratio (not numeric): '{response}'")

    
    def set_sense_concentration_cset(self, slope: float, y_intercept: float):
        """Specifies the correction set(s) used for the current range(s) as slope and Y intercept.
        Parameters:
        slope: The slope value (numeric value).
        y_intercept: The Y intercept value (numeric value)."""
        self.instrument.write(f":SENS:CONC:CSET {slope},{y_intercept}")

    def get_sense_concentration_cset(self) -> tuple[float, float]:
        """Returns the correction set values (slope and Y intercept) for the current range(s)."""
        response = self.instrument.query(":SENS:CONC:CSET?").strip()
        parts = response.split(',')
        if len(parts) != 2:
            raise ValueError(f"Unexpected response format for concentration CSET: '{response}'")
        try:
            return float(parts[0]), float(parts[1])
        except ValueError:
            raise ValueError(f"Failed to parse concentration CSET values from: '{response}'")

    def set_sense_concentration_lower(self, value: float):
        """Specifies the lowest measurable concentration for the currently-selected range.
        Parameters:
        value: The lower concentration value (numeric value)."""
        self.instrument.write(f":SENS:CONC:LOW {value}")

    def get_sense_concentration_lower(self) -> float:
        """Returns the lowest measurable concentration for the currently-selected range."""
        response = self.instrument.query(":SENS:CONC:LOW?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for concentration lower (not numeric): '{response}'")

    def set_sense_concentration_lset(self, curve_type: str, n: int, coefficients: list[float]):
        """Sets the curve fit type and coefficients that are currently in use.
        Parameters:
        curve_type: POLYnomial|SRATional
        n: The curve order (positive integer).
        coefficients: A list of numeric values representing the curve coefficients, starting with the 0th order term."""
        valid_types = {"POLYNOMIAL", "SRATIONAL", "POLY", "SRAT"}
        type_upper = curve_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid curve type: '{curve_type}'. Must be 'POLYNOMIAL' or 'SRATIONAL'.")
        if not isinstance(n, int) or n < 0:
            raise ValueError("Curve order 'n' must be a non-negative integer.")
        if len(coefficients) != (n + 1):
            raise ValueError(f"Number of coefficients ({len(coefficients)}) must be equal to n+1 ({n+1}).")

        if type_upper == "POLYNOMIAL": scpi_curve_type = "POLY"
        elif type_upper == "SRATIONAL": scpi_curve_type = "SRAT"
        else: scpi_curve_type = type_upper

        coeff_str = ",".join(map(str, coefficients))
        self.instrument.write(f":SENS:CONC:LSET {scpi_curve_type}{n},{coeff_str}")

    def get_sense_concentration_lset(self) -> tuple[str, int, list[float]]:
        """Returns the curve fit type, order, and coefficients.
        Returns: A tuple (curve_type: str, n: int, coefficients: list[float])."""
        response = self.instrument.query(":SENS:CONC:LSET?").strip()
        parts = response.split(',', 1) # Split only on the first comma
        if len(parts) != 2:
            raise ValueError(f"Unexpected response format for concentration LSET: '{response}'")

        curve_type_n = parts[0].strip().upper()
        if curve_type_n.startswith("POLY"):
            curve_type = "POLYNOMIAL"
            n_str = curve_type_n[4:]
        elif curve_type_n.startswith("SRAT"):
            curve_type = "SRATIONAL"
            n_str = curve_type_n[4:]
        else:
            raise ValueError(f"Unknown curve type in response: '{curve_type_n}'")

        try:
            n = int(n_str)
        except ValueError:
            raise ValueError(f"Failed to parse curve order from: '{n_str}'")

        coeff_str = parts[1].strip()
        coefficients = [float(c) for c in coeff_str.split(',')]
        return curve_type, n, coefficients

    
    def set_sense_concentration_range_auto_lower(self, value: float):
        """Specifies the lower concentration in ppm for automatic ranging.
        Parameters:
        value: The lower concentration value (numeric value)."""
        self.instrument.write(f":SENS:CONC:RANG:AUTO:LOW {value}")

    def get_sense_concentration_range_auto_lower(self) -> float:
        """Returns the lower concentration in ppm for automatic ranging."""
        response = self.instrument.query(":SENS:CONC:RANG:AUTO:LOW?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for concentration range auto lower (not numeric): '{response}'")

    def set_sense_concentration_range_auto_state(self, enable: bool):
        """Turns the automatic range switching feature on or off.
        Parameters:
        enable: True to turn auto-ranging ON, False to turn OFF."""
        scpi_value = 1 if enable else 0
        self.instrument.write(f":SENS:CONC:RANG:AUTO:STATE {scpi_value}")

    def get_sense_concentration_range_auto_state(self) -> bool:
        """Returns True if automatic range switching is ON, False if OFF."""
        response = self.instrument.query(":SENS:CONC:RANG:AUTO:STATE?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for concentration range auto state: '{response}'")

    def set_sense_concentration_range_auto_upper(self, value: float):
        """Specifies the upper concentration in ppm for automatic ranging.
        Parameters:
        value: The upper concentration value (numeric value)."""
        self.instrument.write(f":SENS:CONC:RANG:AUTO:UPP {value}")

    def get_sense_concentration_range_auto_upper(self) -> float:
        """Returns the upper concentration in ppm for automatic ranging."""
        response = self.instrument.query(":SENS:CONC:RANG:AUTO:UPP?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for concentration range auto upper (not numeric): '{response}'")

    def set_sense_concentration_range_fixed(self, range_number: float):
        """Specifies the range number of the already-selected instrument(s).
        Parameters:
        range_number: The range number (numeric value)."""
        self.instrument.write(f":SENS:CONC:RANG:FIX {range_number}")

    def get_sense_concentration_range_fixed(self) -> float:
        """Returns the range number of the already-selected instrument(s)."""
        response = self.instrument.query(":SENS:CONC:RANG:FIX?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for concentration range fixed (not numeric): '{response}'")

    def set_sense_concentration_talign(self, delay_seconds: float):
        """Sets the time delay in seconds for the Time Alignment of the continuously measured data.
        Parameters:
        delay_seconds: The time delay in seconds (numeric value)."""
        self.instrument.write(f":SENS:CONC:TAL {delay_seconds}")

    def get_sense_concentration_talign(self) -> float:
        """Returns the time delay for the Time Alignment of the continuously measured data."""
        response = self.instrument.query(":SENS:CONC:TAL?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for concentration time align (not numeric): '{response}'")

    
    def set_sense_concentration_upper(self, value: float):
        """Specifies the full scale concentration for the currently-selected range.
        Parameters:
        value: The full scale concentration value (numeric value)."""
        self.instrument.write(f":SENS:CONC:UPP {value}")

    def get_sense_concentration_upper(self) -> float:
        """Returns the full scale concentration for the currently-selected range."""
        response = self.instrument.query(":SENS:CONC:UPP?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for concentration upper (not numeric): '{response}'")

    
    def set_sense_condition_level(self, level_value: float = None, level_type: str = None):
        """Specifies the characteristics that causes the transition between an ON and OFF condition of the sensed signal.
        Parameters:
        level_value: The numeric level value.
        level_type: TTL|ECL. If 'level_value' is provided, 'level_type' should be None. If 'level_type' is provided, 'level_value' should be None."""
        if level_value is not None and level_type is not None:
            raise ValueError("Only one of 'level_value' or 'level_type' can be provided.")
        if level_value is not None:
            self.instrument.write(f":SENS:COND:LEV {level_value}")
        elif level_type is not None:
            valid_types = {"TTL", "ECL"}
            type_upper = level_type.upper()
            if type_upper not in valid_types:
                raise ValueError(f"Invalid level type: '{level_type}'. Must be 'TTL' or 'ECL'.")
            self.instrument.write(f":SENS:COND:LEV {type_upper}")
        else:
            raise ValueError("Either 'level_value' or 'level_type' must be provided.")

    def get_sense_condition_level(self):
        """Returns the level or type that causes the transition between an ON and OFF condition.
        Returns: A float if a numeric level, or a string ('TTL'|'ECL') if a type."""
        response = self.instrument.query(":SENS:COND:LEV?").strip()
        try:
            return float(response)
        except ValueError:
            return response.upper()

    
    def sense_correction_auto(self):
        """Performs an automatic correction of the selected instruments.
        Notes: This is an event command; no query."""
        self.instrument.write(":SENS:CORR:AUTO")

    def sense_correction_calculate(self):
        """Initiates a calculation for the CORRection subsystem if needed.
        Notes: This is an event command; no query."""
        self.instrument.write(":SENS:CORR:CALC")

    def sense_correction_collect_acquire_standard(self):
        """Performs a measurement and saves it as data for the standard of the chosen correction method.
        Notes: This is an event command; no query."""
        self.instrument.write(":SENS:CORR:COLL:ACQ STAN")

    def set_sense_correction_collect_method(self, method_type: str):
        """Selects the correction method to be used for the correction that is about to be performed.
        Parameters:
        method_type: TPORt (Two Port)"""
        valid_types = {"TPORT", "TPOR"}
        type_upper = method_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid method type: '{method_type}'. Must be 'TPORt'.")
        self.instrument.write(f":SENS:CORR:COLL:METH {type_upper}")

    def get_sense_correction_collect_method(self) -> str:
        """Returns the correction method currently selected."""
        response = self.instrument.query(":SENS:CORR:COLL:METH?").strip().upper()
        if response.startswith("TPOR"):
            return "TPORT"
        return response

    def sense_correction_collect_save(self, trace_name: str = None):
        """Calculates the correction data and then saves it.
        Parameters:
        trace_name: (Optional) The name of the trace to save the correction data in."""
        if trace_name:
            self.instrument.write(f":SENS:CORR:COLL:SAVE '{trace_name}'")
        else:
            self.instrument.write(":SENS:CORR:COLL:SAVE")

    def set_sense_correction_cset_select(self, name: str):
        """Specifies the active CORRection set.
        Parameters:
        name: The name of the trace or table (character data)."""
        self.instrument.write(f":SENS:CORR:CSET:SEL '{name}'")

    def get_sense_correction_cset_select(self) -> str:
        """Returns the name of the active CORRection set."""
        response = self.instrument.query(":SENS:CORR:CSET:SEL?").strip().strip("'\"")
        return response

    def set_sense_correction_cset_state(self, enable: bool):
        """Determines whether the correction data defined in the selected set is applied to the measurement.
        Parameters:
        enable: True to apply correction, False to not apply."""
        scpi_value = 1 if enable else 0
        self.instrument.write(f":SENS:CORR:CSET:STATE {scpi_value}")

    def get_sense_correction_cset_state(self) -> bool:
        """Returns True if the correction data is applied, False if not."""
        response = self.instrument.query(":SENS:CORR:CSET:STATE?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for correction CSET state: '{response}'")

    
    def set_sense_correction_edelay_distance(self, distance_meters: float):
        """Sets the electrical delay with the distance parameter.
        Parameters:
        distance_meters: The distance in meters (numeric value)."""
        self.instrument.write(f":SENS:CORR:EDEL:DIST {distance_meters}")

    def get_sense_correction_edelay_distance(self) -> float:
        """Returns the electrical delay distance in meters."""
        response = self.instrument.query(":SENS:CORR:EDEL:DIST?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for electrical delay distance (not numeric): '{response}'")

    def set_sense_correction_edelay_state(self, enable: bool):
        """Enables or disables the electrical delay correction.
        Parameters:
        enable: True to enable, False to disable."""
        scpi_value = 1 if enable else 0
        self.instrument.write(f":SENS:CORR:EDEL:STATE {scpi_value}")

    def get_sense_correction_edelay_state(self) -> bool:
        """Returns True if electrical delay correction is enabled, False if disabled."""
        response = self.instrument.query(":SENS:CORR:EDEL:STATE?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for electrical delay state: '{response}'")

    def set_sense_correction_edelay_time(self, time_seconds: float):
        """Sets the electrical delay with the time parameter.
        Parameters:
        time_seconds: The time in seconds (numeric value)."""
        self.instrument.write(f":SENS:CORR:EDEL:TIME {time_seconds}")

    def get_sense_correction_edelay_time(self) -> float:
        """Returns the electrical delay time in seconds."""
        response = self.instrument.query(":SENS:CORR:EDEL:TIME?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for electrical delay time (not numeric): '{response}'")

    
    def set_sense_correction_impedance_input_magnitude(self, value: float):
        """Sets the magnitude of the input impedance.
        Parameters:
        value: The magnitude value (numeric value) in Ohms."""
        self.instrument.write(f":SENS:CORR:IMP:INP:MAGN {value}")

    def get_sense_correction_impedance_input_magnitude(self) -> float:
        """Returns the magnitude of the input impedance."""
        response = self.instrument.query(":SENS:CORR:IMP:INP:MAGN?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for impedance input magnitude (not numeric): '{response}'")

    def set_sense_correction_impedance_output_magnitude(self, value: float):
        """Sets the magnitude of the output impedance.
        Parameters:
        value: The magnitude value (numeric value) in Ohms."""
        self.instrument.write(f":SENS:CORR:IMP:OUTP:MAGN {value}")

    def get_sense_correction_impedance_output_magnitude(self) -> float:
        """Returns the magnitude of the output impedance."""
        response = self.instrument.query(":SENS:CORR:IMP:OUTP:MAGN?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for impedance output magnitude (not numeric): '{response}'")

    def set_sense_correction_impedance_state(self, enable: bool):
        """Enables or disables external IMPedance correction factors.
        Parameters:
        enable: True to enable, False to disable."""
        scpi_value = 1 if enable else 0
        self.instrument.write(f":SENS:CORR:IMP:STATE {scpi_value}")

    def get_sense_correction_impedance_state(self) -> bool:
        """Returns True if external IMPedance correction factors are enabled, False if disabled."""
        response = self.instrument.query(":SENS:CORR:IMP:STATE?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for impedance state: '{response}'")

        # Grouping LOSS, GAIN, SLOPE as they share parameters and structure.

    def set_sense_correction_loss_gain_slope_input_auto(self, type_prefix: str, enable: bool):
        """When AUTO is ON, the OUTPut correction values must track those of the INPut.
        Parameters:
        type_prefix: 'LOSS'|'GAIN'|'SLOPe'
        enable: True to enable auto-tracking, False to disable."""
        valid_prefixes = {"LOSS", "GAIN", "SLOPE", "LOS", "GAI", "SLOP"}
        prefix_upper = type_prefix.upper()
        if prefix_upper not in valid_prefixes:
            raise ValueError(f"Invalid type prefix: '{type_prefix}'. Must be 'LOSS', 'GAIN', or 'SLOPe'.")

        scpi_value = 1 if enable else 0
        self.instrument.write(f":SENS:CORR:{prefix_upper}:INP:AUTO {scpi_value}")

    def get_sense_correction_loss_gain_slope_input_auto(self, type_prefix: str) -> bool:
        """Returns True if OUTPut correction values track INPut, False if not."""
        valid_prefixes = {"LOSS", "GAIN", "SLOPE", "LOS", "GAI", "SLOP"}
        prefix_upper = type_prefix.upper()
        if prefix_upper not in valid_prefixes:
            raise ValueError(f"Invalid type prefix: '{type_prefix}'. Must be 'LOSS', 'GAIN', or 'SLOPe'.")

        response = self.instrument.query(f":SENS:CORR:{prefix_upper}:INP:AUTO?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for {type_prefix} input auto state: '{response}'")

    def set_sense_correction_loss_gain_slope_input_magnitude(self, type_prefix: str, value: float):
        """Sets the magnitude value of the correction data for LOSS, GAIN or SLOPe.
        Parameters:
        type_prefix: 'LOSS'|'GAIN'|'SLOPe'
        value: The magnitude value (numeric value). Units vary (relative amplitude, or relative amplitude/Hz for SLOPe)."""
        valid_prefixes = {"LOSS", "GAIN", "SLOPE", "LOS", "GAI", "SLOP"}
        prefix_upper = type_prefix.upper()
        if prefix_upper not in valid_prefixes:
            raise ValueError(f"Invalid type prefix: '{type_prefix}'. Must be 'LOSS', 'GAIN', or 'SLOPe'.")

        self.instrument.write(f":SENS:CORR:{prefix_upper}:INP:MAGN {value}")

    def get_sense_correction_loss_gain_slope_input_magnitude(self, type_prefix: str) -> float:
        """Returns the magnitude value of the correction data for LOSS, GAIN or SLOPe."""
        valid_prefixes = {"LOSS", "GAIN", "SLOPE", "LOS", "GAI", "SLOP"}
        prefix_upper = type_prefix.upper()
        if prefix_upper not in valid_prefixes:
            raise ValueError(f"Invalid type prefix: '{type_prefix}'. Must be 'LOSS', 'GAIN', or 'SLOPe'.")

        response = self.instrument.query(f":SENS:CORR:{prefix_upper}:INP:MAGN?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for {type_prefix} input magnitude (not numeric): '{response}'")

    def set_sense_correction_loss_gain_slope_input_phase(self, type_prefix: str, value: float):
        """Sets the phase value of the correction data for LOSS, GAIN or SLOPe.
        Parameters:
        type_prefix: 'LOSS'|'GAIN'|'SLOPe'
        value: The phase value (numeric value). Units vary (angle units, or angle units/Hz for SLOPe)."""
        valid_prefixes = {"LOSS", "GAIN", "SLOPE", "LOS", "GAI", "SLOP"}
        prefix_upper = type_prefix.upper()
        if prefix_upper not in valid_prefixes:
            raise ValueError(f"Invalid type prefix: '{type_prefix}'. Must be 'LOSS', 'GAIN', or 'SLOPe'.")

        self.instrument.write(f":SENS:CORR:{prefix_upper}:INP:PHAS {value}")

    def get_sense_correction_loss_gain_slope_input_phase(self, type_prefix: str) -> float:
        """Returns the phase value of the correction data for LOSS, GAIN or SLOPe."""
        valid_prefixes = {"LOSS", "GAIN", "SLOPE", "LOS", "GAI", "SLOP"}
        prefix_upper = type_prefix.upper()
        if prefix_upper not in valid_prefixes:
            raise ValueError(f"Invalid type prefix: '{type_prefix}'. Must be 'LOSS', 'GAIN', or 'SLOPe'.")

        response = self.instrument.query(f":SENS:CORR:{prefix_upper}:INP:PHAS?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for {type_prefix} input phase (not numeric): '{response}'")

    def set_sense_correction_loss_gain_slope_output_auto(self, type_prefix: str, enable: bool):
        """When AUTO is ON, the OUTPut correction values must track those of the INPut.
        Parameters:
        type_prefix: 'LOSS'|'GAIN'|'SLOPe'
        enable: True to enable auto-tracking, False to disable."""
        valid_prefixes = {"LOSS", "GAIN", "SLOPE", "LOS", "GAI", "SLOP"}
        prefix_upper = type_prefix.upper()
        if prefix_upper not in valid_prefixes:
            raise ValueError(f"Invalid type prefix: '{type_prefix}'. Must be 'LOSS', 'GAIN', or 'SLOPe'.")

        scpi_value = 1 if enable else 0
        self.instrument.write(f":SENS:CORR:{prefix_upper}:OUTP:AUTO {scpi_value}")

    def get_sense_correction_loss_gain_slope_output_auto(self, type_prefix: str) -> bool:
        """Returns True if OUTPut correction values track INPut, False if not."""
        valid_prefixes = {"LOSS", "GAIN", "SLOPE", "LOS", "GAI", "SLOP"}
        prefix_upper = type_prefix.upper()
        if prefix_upper not in valid_prefixes:
            raise ValueError(f"Invalid type prefix: '{type_prefix}'. Must be 'LOSS', 'GAIN', or 'SLOPe'.")

        response = self.instrument.query(f":SENS:CORR:{prefix_upper}:OUTP:AUTO?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for {type_prefix} output auto state: '{response}'")

    def set_sense_correction_loss_gain_slope_output_magnitude(self, type_prefix: str, value: float):
        """Sets the magnitude value of the correction data for LOSS, GAIN or SLOPe.
        Parameters:
        type_prefix: 'LOSS'|'GAIN'|'SLOPe'
        value: The magnitude value (numeric value). Units vary (relative amplitude, or relative amplitude/Hz for SLOPe)."""
        valid_prefixes = {"LOSS", "GAIN", "SLOPE", "LOS", "GAI", "SLOP"}
        prefix_upper = type_prefix.upper()
        if prefix_upper not in valid_prefixes:
            raise ValueError(f"Invalid type prefix: '{type_prefix}'. Must be 'LOSS', 'GAIN', or 'SLOPe'.")

        self.instrument.write(f":SENS:CORR:{prefix_upper}:OUTP:MAGN {value}")

    def get_sense_correction_loss_gain_slope_output_magnitude(self, type_prefix: str) -> float:
        """Returns the magnitude value of the correction data for LOSS, GAIN or SLOPe."""
        valid_prefixes = {"LOSS", "GAIN", "SLOPE", "LOS", "GAI", "SLOP"}
        prefix_upper = type_prefix.upper()
        if prefix_upper not in valid_prefixes:
            raise ValueError(f"Invalid type prefix: '{type_prefix}'. Must be 'LOSS', 'GAIN', or 'SLOPe'.")

        response = self.instrument.query(f":SENS:CORR:{prefix_upper}:OUTP:MAGN?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for {type_prefix} output magnitude (not numeric): '{response}'")

    def set_sense_correction_loss_gain_slope_output_phase(self, type_prefix: str, value: float):
        """Sets the phase value of the correction data for LOSS, GAIN or SLOPe.
        Parameters:
        type_prefix: 'LOSS'|'GAIN'|'SLOPe'
        value: The phase value (numeric value). Units vary (angle units, or angle units/Hz for SLOPe)."""
        valid_prefixes = {"LOSS", "GAIN", "SLOPE", "LOS", "GAI", "SLOP"}
        prefix_upper = type_prefix.upper()
        if prefix_upper not in valid_prefixes:
            raise ValueError(f"Invalid type prefix: '{type_prefix}'. Must be 'LOSS', 'GAIN', or 'SLOPe'.")

        self.instrument.write(f":SENS:CORR:{prefix_upper}:OUTP:PHAS {value}")

    def get_sense_correction_loss_gain_slope_output_phase(self, type_prefix: str) -> float:
        """Returns the phase value of the correction data for LOSS, GAIN or SLOPe."""
        valid_prefixes = {"LOSS", "GAIN", "SLOPE", "LOS", "GAI", "SLOP"}
        prefix_upper = type_prefix.upper()
        if prefix_upper not in valid_prefixes:
            raise ValueError(f"Invalid type prefix: '{type_prefix}'. Must be 'LOSS', 'GAIN', or 'SLOPe'.")

        response = self.instrument.query(f":SENS:CORR:{prefix_upper}:OUTP:PHAS?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for {type_prefix} output phase (not numeric): '{response}'")

    
    def set_sense_correction_loss_gain_slope_state(self, type_prefix: str, enable: bool):
        """Enables or disables the LOSS, GAIN or SLOPe correction factors.
        Parameters:
        type_prefix: 'LOSS'|'GAIN'|'SLOPe'
        enable: True to enable, False to disable."""
        valid_prefixes = {"LOSS", "GAIN", "SLOPE", "LOS", "GAI", "SLOP"}
        prefix_upper = type_prefix.upper()
        if prefix_upper not in valid_prefixes:
            raise ValueError(f"Invalid type prefix: '{type_prefix}'. Must be 'LOSS', 'GAIN', or 'SLOPe'.")

        scpi_value = 1 if enable else 0
        self.instrument.write(f":SENS:CORR:{prefix_upper}:STATE {scpi_value}")

    def get_sense_correction_loss_gain_slope_state(self, type_prefix: str) -> bool:
        """Returns True if the LOSS, GAIN or SLOPe correction factors are enabled, False if disabled."""
        valid_prefixes = {"LOSS", "GAIN", "SLOPE", "LOS", "GAI", "SLOP"}
        prefix_upper = type_prefix.upper()
        if prefix_upper not in valid_prefixes:
            raise ValueError(f"Invalid type prefix: '{type_prefix}'. Must be 'LOSS', 'GAIN', or 'SLOPe'.")

        response = self.instrument.query(f":SENS:CORR:{prefix_upper}:STATE?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for {type_prefix} state: '{response}'")

    def set_sense_correction_offset_magnitude(self, value: float):
        """Sets the magnitude value of the correction offset data.
        Parameters:
        value: The magnitude value (numeric value)."""
        self.instrument.write(f":SENS:CORR:OFFS:MAGN {value}")

    def get_sense_correction_offset_magnitude(self) -> float:
        """Returns the magnitude value of the correction offset data."""
        response = self.instrument.query(":SENS:CORR:OFFS:MAGN?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for offset magnitude (not numeric): '{response}'")

    def set_sense_correction_offset_phase(self, value: float):
        """Sets the phase value of the correction offset data.
        Parameters:
        value: The phase value (numeric value) in current angle units."""
        self.instrument.write(f":SENS:CORR:OFFS:PHAS {value}")

    def get_sense_correction_offset_phase(self) -> float:
        """Returns the phase value of the correction offset data."""
        response = self.instrument.query(":SENS:CORR:OFFS:PHAS?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for offset phase (not numeric): '{response}'")

    
    def set_sense_correction_offset_state(self, enable: bool):
        """Enables or disables the offset correction.
        Parameters:
        enable: True to enable, False to disable."""
        scpi_value = 1 if enable else 0
        self.instrument.write(f":SENS:CORR:OFFS:STATE {scpi_value}")

    def get_sense_correction_offset_state(self) -> bool:
        """Returns True if the offset correction is enabled, False if disabled."""
        response = self.instrument.query(":SENS:CORR:OFFS:STATE?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for offset state: '{response}'")

    def set_sense_correction_rvelocity_coax(self, value: float):
        """Sets the relative velocity factor for coaxial lines.
        Parameters:
        value: The unitless relative velocity factor (numeric value)."""
        self.instrument.write(f":SENS:CORR:RVEL:COAX {value}")

    def get_sense_correction_rvelocity_coax(self) -> float:
        """Returns the relative velocity factor for coaxial lines."""
        response = self.instrument.query(":SENS:CORR:RVEL:COAX?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for relative velocity coax (not numeric): '{response}'")

    def set_sense_correction_rvelocity_medium(self, medium_type: str):
        """Selects the correction algorithm for the media through which the detected signal is transmitted.
        Parameters:
        medium_type: COAX|WAVeguide"""
        valid_types = {"COAX", "WAVEGUIDE", "WAV"}
        type_upper = medium_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid medium type: '{medium_type}'. Must be 'COAX' or 'WAVeguide'.")

        if type_upper == "WAVEGUIDE": scpi_value = "WAV"
        else: scpi_value = type_upper

        self.instrument.write(f":SENS:CORR:RVEL:MED {scpi_value}")

    def get_sense_correction_rvelocity_medium(self) -> str:
        """Returns the correction algorithm for the media ('COAX' or 'WAVeguide')."""
        response = self.instrument.query(":SENS:CORR:RVEL:MED?").strip().upper()
        if response.startswith("WAV"):
            return "WAVEGUIDE"
        return response

    def set_sense_correction_rvelocity_state(self, enable: bool):
        """Enables or disables the relative velocity correction.
        Parameters:
        enable: True to enable, False to disable."""
        scpi_value = 1 if enable else 0
        self.instrument.write(f":SENS:CORR:RVEL:STATE {scpi_value}")

    def get_sense_correction_rvelocity_state(self) -> bool:
        """Returns True if the relative velocity correction is enabled, False if disabled."""
        response = self.instrument.query(":SENS:CORR:RVEL:STATE?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for relative velocity state: '{response}'")

    def set_sense_correction_rvelocity_waveguide(self, value: float):
        """Sets the relative velocity factor for waveguide.
        Parameters:
        value: The unitless relative velocity factor (numeric value)."""
        self.instrument.write(f":SENS:CORR:RVEL:WAV {value}")

    def get_sense_correction_rvelocity_waveguide(self) -> float:
        """Returns the relative velocity factor for waveguide."""
        response = self.instrument.query(":SENS:CORR:RVEL:WAV?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for relative velocity waveguide (not numeric): '{response}'")

    def set_sense_correction_rvelocity_waveguide_fcutoff(self, frequency_hz: float):
        """Specifies the frequency cutoff of the waveguide medium in Hertz.
        Parameters:
        frequency_hz: The cutoff frequency in Hz (numeric value)."""
        self.instrument.write(f":SENS:CORR:RVEL:WAV:FCUT {frequency_hz}")

    def get_sense_correction_rvelocity_waveguide_fcutoff(self) -> float:
        """Returns the frequency cutoff of the waveguide medium in Hertz."""
        response = self.instrument.query(":SENS:CORR:RVEL:WAV:FCUT?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for relative velocity waveguide fcutoff (not numeric): '{response}'")

    
    def sense_correction_spoint_acquire(self):
        """Supplies a known signal to the selected instruments and waits for stabilization criteria to be met.
        Notes: This is an event command; no query."""
        self.instrument.write(":SENS:CORR:SPO:ACQ")

    def set_sense_correction_spoint_dtolerance(self, tolerance_percent_fs: float):
        """Specifies the drift tolerance for a set point correction procedure in percentage of full scale (%FS).
        Parameters:
        tolerance_percent_fs: The drift tolerance (numeric value)."""
        self.instrument.write(f":SENS:CORR:SPO:DTOL {tolerance_percent_fs}")

    def get_sense_correction_spoint_dtolerance(self) -> float:
        """Returns the drift tolerance for a set point correction procedure in percentage of full scale (%FS)."""
        response = self.instrument.query(":SENS:CORR:SPO:DTOL?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for set point drift tolerance (not numeric): '{response}'")

    def set_sense_correction_state(self, enable: bool):
        """Determines whether the correction data defined in this section is applied to the measurement.
        Parameters:
        enable: True to apply, False to not apply."""
        scpi_value = 1 if enable else 0
        self.instrument.write(f":SENS:CORR:STATE {scpi_value}")

    def get_sense_correction_state(self) -> bool:
        """Returns True if the correction data is applied, False if not."""
        response = self.instrument.query(":SENS:CORR:STATE?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for correction state: '{response}'")

    def sense_correction_zero_acquire(self):
        """Sends a zero signal to the selected instruments and waits for the stabilization criteria to be met.
        Notes: This is an event command; no query."""
        self.instrument.write(":SENS:CORR:ZERO:ACQ")

    def set_sense_correction_zero_dtolerance(self, tolerance_percent_fs: float):
        """Specifies the drift tolerance for a zero procedure for the selected instrument(s).
        Parameters:
        tolerance_percent_fs: The drift tolerance (numeric value)."""
        self.instrument.write(f":SENS:CORR:ZERO:DTOL {tolerance_percent_fs}")

    def get_sense_correction_zero_dtolerance(self) -> float:
        """Returns the drift tolerance for a zero procedure for the selected instrument(s)."""
        response = self.instrument.query(":SENS:CORR:ZERO:DTOL?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for zero drift tolerance (not numeric): '{response}'")

    
    def set_sense_current_ac_aperture(self, value: float):
        """Specifies the acquisition/sampling/gate time for a single measurement point for AC Current.
        Parameters:
        value: The aperture time in seconds (numeric value)."""
        self.instrument.write(f":SENS:CURR:AC:APER {value}")

    def get_sense_current_ac_aperture(self) -> float:
        """Returns the acquisition/sampling/gate time for AC Current."""
        response = self.instrument.query(":SENS:CURR:AC:APER?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for current AC aperture (not numeric): '{response}'")

    def set_sense_current_ac_nplcycles(self, value: float):
        """Specifies the acquisition/sampling/gate time for AC Current in terms of number of power line cycles.
        Parameters:
        value: The number of power line cycles (numeric value)."""
        self.instrument.write(f":SENS:CURR:AC:NPL {value}")

    def get_sense_current_ac_nplcycles(self) -> float:
        """Returns the acquisition/sampling/gate time for AC Current in terms of number of power line cycles."""
        response = self.instrument.query(":SENS:CURR:AC:NPL?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for current AC NPLCycles (not numeric): '{response}'")

    def set_sense_current_ac_attenuation(self, value: float):
        """Sets the attenuation level for AC Current.
        Parameters:
        value: The attenuation value (numeric value). Default units determined by UNITS system."""
        self.instrument.write(f":SENS:CURR:AC:ATT {value}")

    def get_sense_current_ac_attenuation(self) -> float:
        """Returns the attenuation level for AC Current."""
        response = self.instrument.query(":SENS:CURR:AC:ATT?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for current AC attenuation (not numeric): '{response}'")

    def set_sense_current_ac_attenuation_auto(self, enable: bool):
        """Couples the attenuator to RANGe for AC Current such that maximum dynamic range is assured.
        Parameters:
        enable: True to enable auto-attenuation, False to disable."""
        scpi_value = 1 if enable else 0
        self.instrument.write(f":SENS:CURR:AC:ATT:AUTO {scpi_value}")

    def get_sense_current_ac_attenuation_auto(self) -> bool:
        """Returns True if auto-attenuation is enabled for AC Current, False if disabled."""
        response = self.instrument.query(":SENS:CURR:AC:ATT:AUTO?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for current AC attenuation auto state: '{response}'")

    
    def set_sense_current_ac_protection_level(self, value: float):
        """Sets the input level at which the input protection circuit will trip for AC Current.
        Parameters:
        value: The trip level (numeric value)."""
        self.instrument.write(f":SENS:CURR:AC:PROT:LEV {value}")

    def get_sense_current_ac_protection_level(self) -> float:
        """Returns the input level at which the input protection circuit will trip for AC Current."""
        response = self.instrument.query(":SENS:CURR:AC:PROT:LEV?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for current AC protection level (not numeric): '{response}'")

    def set_sense_current_ac_protection_state(self, enable: bool):
        """Controls whether the input protection circuit is enabled for AC Current.
        Parameters:
        enable: True to enable, False to disable."""
        scpi_value = 1 if enable else 0
        self.instrument.write(f":SENS:CURR:AC:PROT:STATE {scpi_value}")

    def get_sense_current_ac_protection_state(self) -> bool:
        """Returns True if the input protection circuit is enabled for AC Current, False if disabled."""
        response = self.instrument.query(":SENS:CURR:AC:PROT:STATE?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for current AC protection state: '{response}'")

    def get_sense_current_ac_protection_tripped(self) -> bool:
        """Returns True if the protection circuit is tripped for AC Current, False if untripped.
        Notes: Query only."""
        response = self.instrument.query(":SENS:CURR:AC:PROT:TRIP?").strip()
        if response == 1:
            return True
        elif response == 0:
            return False
        else:
            raise ValueError(f"Unexpected response for current AC protection tripped status: '{response}'")

    def clear_sense_current_ac_protection(self):
        """Causes the protection circuit to be cleared for AC Current.
        Notes: This is an event command; no query."""
        self.instrument.write(":SENS:CURR:AC:PROT:CLE")

    
    def set_sense_current_ac_range_upper(self, value: float):
        """Specifies the most positive signal level expected for the AC Current sensor input.
        Parameters:
        value: The upper range value (numeric value)."""
        self.instrument.write(f":SENS:CURR:AC:RANG:UPP {value}")

    def get_sense_current_ac_range_upper(self) -> float:
        """Returns the most positive signal level expected for the AC Current sensor input."""
        response = self.instrument.query(":SENS:CURR:AC:RANG:UPP?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for current AC range upper (not numeric): '{response}'")

    def set_sense_current_ac_range_lower(self, value: float):
        """Specifies the most negative signal level expected for the AC Current sensor input.
        Parameters:
        value: The lower range value (numeric value)."""
        self.instrument.write(f":SENS:CURR:AC:RANG:LOW {value}")

    def get_sense_current_ac_range_lower(self) -> float:
        """Returns the most negative signal level expected for the AC Current sensor input."""
        response = self.instrument.query(":SENS:CURR:AC:RANG:LOW?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for current AC range lower (not numeric): '{response}'")

    def set_sense_current_ac_range_auto(self, auto_state: str):
        """Sets the range for AC Current to the value determined to give the most dynamic range.
        Parameters:
        auto_state: Boolean (ON|OFF) or 'ONCE'. Selecting 'ONCE' sets AUTO to ON and then OFF."""
        normalized_state = auto_state.upper()
        if normalized_state in {1, "ON"}:
            scpi_value = "ON"
        elif normalized_state in {0, "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":SENS:CURR:AC:RANG:AUTO {scpi_value}")

    def get_sense_current_ac_range_auto(self) -> str:
        """Returns the auto state of the AC Current range ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query(":SENS:CURR:AC:RANG:AUTO?").strip()
        if response == 1:
            return "ON"
        elif response == 0:
            return "OFF"
        else:
            return response.upper()

    def set_sense_current_ac_range_auto_direction(self, direction: str):
        """Defines the manner in which AUTO works for AC Current ranging.
        Parameters:
        direction: UP|DOWN|EITHer"""
        valid_directions = {"UP", "DOWN", "EITHER", "EITH"}
        direction_upper = direction.upper()
        if direction_upper not in valid_directions:
            raise ValueError(f"Invalid direction: '{direction}'. Must be 'UP', 'DOWN', or 'EITHer'.")

        if direction_upper == "EITHER": scpi_value = "EITH"
        else: scpi_value = direction_upper

        self.instrument.write(f":SENS:CURR:AC:RANG:AUTO:DIR {scpi_value}")

    def get_sense_current_ac_range_auto_direction(self) -> str:
        """Returns the auto-ranging direction for AC Current ('UP', 'DOWN', or 'EITHER')."""
        response = self.instrument.query(":SENS:CURR:AC:RANG:AUTO:DIR?").strip().upper()
        if response.startswith("EITH"):
            return "EITHER"
        return response

    def set_sense_current_ac_range_auto_llimit(self, value: float):
        """Sets the smallest range to which the instrument will go while auto-ranging for AC Current.
        Parameters:
        value: The lower limit (numeric value)."""
        self.instrument.write(f":SENS:CURR:AC:RANG:AUTO:LLIM {value}")

    def get_sense_current_ac_range_auto_llimit(self) -> float:
        """Returns the smallest range to which the instrument will go while auto-ranging for AC Current."""
        response = self.instrument.query(":SENS:CURR:AC:RANG:AUTO:LLIM?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for current AC range auto lower limit (not numeric): '{response}'")

    def set_sense_current_ac_range_auto_ulimit(self, value: float):
        """Sets the largest range to which the instrument will go while auto-ranging for AC Current.
        Parameters:
        value: The upper limit (numeric value)."""
        self.instrument.write(f":SENS:CURR:AC:RANG:AUTO:ULIM {value}")

    def get_sense_current_ac_range_auto_ulimit(self) -> float:
        """Returns the largest range to which the instrument will go while auto-ranging for AC Current."""
        response = self.instrument.query(":SENS:CURR:AC:RANG:AUTO:ULIM?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for current AC range auto upper limit (not numeric): '{response}'")

    
    def set_sense_current_ac_range_offset(self, value: float):
        """Determines the midpoint of the range for AC Current.
        Parameters:
        value: The offset value (numeric value)."""
        self.instrument.write(f":SENS:CURR:AC:RANG:OFFS {value}")

    def get_sense_current_ac_range_offset(self) -> float:
        """Returns the midpoint of the range for AC Current."""
        response = self.instrument.query(":SENS:CURR:AC:RANG:OFFS?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for current AC range offset (not numeric): '{response}'")

    def set_sense_current_ac_range_ptpeak(self, value: float):
        """Specifies the dynamic range required for the AC Current sensor (Peak To Peak).
        Parameters:
        value: The peak-to-peak value (numeric value)."""
        self.instrument.write(f":SENS:CURR:AC:RANG:PTP {value}")

    def get_sense_current_ac_range_ptpeak(self) -> float:
        """Returns the dynamic range required for the AC Current sensor (Peak To Peak)."""
        response = self.instrument.query(":SENS:CURR:AC:RANG:PTP?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for current AC range PTPeak (not numeric): '{response}'")

    def set_sense_current_ac_reference(self, value: float):
        """Sets a reference amplitude for AC Current sensor instruments.
        Parameters:
        value: The reference amplitude (numeric value)."""
        self.instrument.write(f":SENS:CURR:AC:REF {value}")

    def get_sense_current_ac_reference(self) -> float:
        """Returns the reference amplitude for AC Current sensor instruments."""
        response = self.instrument.query(":SENS:CURR:AC:REF?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for current AC reference (not numeric): '{response}'")

    def set_sense_current_ac_reference_state(self, enable: bool):
        """Determines whether amplitude is measured in absolute or relative mode for AC Current.
        Parameters:
        enable: True to reference to the value set in REFerence, False for absolute mode."""
        scpi_value = 1 if enable else 0
        self.instrument.write(f":SENS:CURR:AC:REF:STATE {scpi_value}")

    def get_sense_current_ac_reference_state(self) -> bool:
        """Returns True if amplitude is measured in relative mode for AC Current, False for absolute mode."""
        response = self.instrument.query(":SENS:CURR:AC:REF:STATE?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for current AC reference state: '{response}'")

    def set_sense_current_ac_resolution(self, value: float):
        """Specifies the absolute resolution of the AC Current measurement.
        Parameters:
        value: The resolution value (numeric value)."""
        self.instrument.write(f":SENS:CURR:AC:RES {value}")

    def get_sense_current_ac_resolution(self) -> float:
        """Returns the absolute resolution of the AC Current measurement."""
        response = self.instrument.query(":SENS:CURR:AC:RES?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for current AC resolution (not numeric): '{response}'")

    def set_sense_current_ac_resolution_auto(self, auto_state: str):
        """Allows the system to determine the best resolution for the other measurement conditions for AC Current.
        Parameters:
        auto_state: Boolean (ON|OFF) or 'ONCE'. Selecting 'ONCE' sets AUTO to ON and then OFF."""
        normalized_state = auto_state.upper()
        if normalized_state in {1, "ON"}:
            scpi_value = "ON"
        elif normalized_state in {0, "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":SENS:CURR:AC:RES:AUTO {scpi_value}")

    def get_sense_current_ac_resolution_auto(self) -> str:
        """Returns the auto state of the AC Current resolution ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query(":SENS:CURR:AC:RES:AUTO?").strip()
        if response == 1:
            return "ON"
        elif response == 0:
            return "OFF"
        else:
            return response.upper()

    
    def set_sense_current_detector(self, detector_type: str):
        """Specifies the detector for Current as internal or external.
        Parameters:
        detector_type: INTernal|EXTernal"""
        valid_types = {"INTERNAL", "EXTERNAL", "INT", "EXT"}
        type_upper = detector_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid detector type: '{detector_type}'. Must be 'INTernal' or 'EXTernal'.")

        if type_upper == "INTERNAL": scpi_value = "INT"
        elif type_upper == "EXTERNAL": scpi_value = "EXT"
        else: scpi_value = type_upper

        self.instrument.write(f":SENS:CURR:DET {scpi_value}")

    def get_sense_current_detector(self) -> str:
        """Returns the detector type for Current ('INTERNAL' or 'EXTERNAL')."""
        response = self.instrument.query(":SENS:CURR:DET?").strip().upper()
        if response.startswith("INT"):
            return "INTERNAL"
        elif response.startswith("EXT"):
            return "EXTERNAL"
        return response

    
    def set_sense_detector_bandwidth(self, value: float):
        """Controls the bandwidth after an intermediate signal has been processed within the SENSe block.
        Parameters:
        value: The bandwidth value (numeric value)."""
        self.instrument.write(f":SENS:DET:BAND {value}")

    def get_sense_detector_bandwidth(self) -> float:
        """Returns the bandwidth after an intermediate signal has been processed."""
        response = self.instrument.query(":SENS:DET:BAND?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for detector bandwidth (not numeric): '{response}'")

    def set_sense_detector_function(self, function_type: str):
        """Specifies the detector sampling characteristics.
        Parameters:
        function_type: GROund|NEGative|POSitive|SAMPle|SIGNal|PAVerage|AAVerage|RMS"""
        valid_types = {
            "GROUND", "NEGATIVE", "POSITIVE", "SAMPLE", "SIGNAL",
            "PEAKAVERAGE", "ABSOLUTEAVERAGE", "RMS",
            "GRO", "NEG", "POS", "SAMP", "SIGN", "PAV", "AAV"
        }
        type_upper = function_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid detector function type: '{function_type}'.")

        if type_upper == "GROUND": scpi_value = "GRO"
        elif type_upper == "NEGATIVE": scpi_value = "NEG"
        elif type_upper == "POSITIVE": scpi_value = "POS"
        elif type_upper == "SAMPLE": scpi_value = "SAMP"
        elif type_upper == "SIGNAL": scpi_value = "SIGN"
        elif type_upper == "PEAKAVERAGE": scpi_value = "PAV"
        elif type_upper == "ABSOLUTEAVERAGE": scpi_value = "AAV"
        elif type_upper == "RMS": scpi_value = "RMS" # RMS is often not abbreviated
        else: scpi_value = type_upper

        self.instrument.write(f":SENS:DET:FUNC {scpi_value}")

    def get_sense_detector_function(self) -> str:
        """Returns the detector sampling characteristics."""
        response = self.instrument.query(":SENS:DET:FUNC?").strip().upper()
        if response.startswith("GRO"): return "GROUND"
        elif response.startswith("NEG"): return "NEGATIVE"
        elif response.startswith("POS"): return "POSITIVE"
        elif response.startswith("SAMP"): return "SAMPLE"
        elif response.startswith("SIGN"): return "SIGNAL"
        elif response.startswith("PAV"): return "PEAKAVERAGE"
        elif response.startswith("AAV"): return "ABSOLUTEAVERAGE"
        elif response.startswith("RMS"): return "RMS"
        return response

    
    def set_sense_detector_function_auto(self, auto_state: str):
        """Couples the detector function to several settings within the instrument.
        Parameters:
        auto_state: Boolean (ON|OFF) or 'ONCE'. Selecting 'ONCE' sets AUTO to ON and then OFF."""
        normalized_state = auto_state.upper()
        if normalized_state in {1, "ON"}:
            scpi_value = "ON"
        elif normalized_state in {0, "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":SENS:DET:FUNC:AUTO {scpi_value}")

    def get_sense_detector_function_auto(self) -> str:
        """Returns the auto state of the detector function ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query(":SENS:DET:FUNC:AUTO?").strip()
        if response == 1:
            return "ON"
        elif response == 0:
            return "OFF"
        else:
            return response.upper()

    def set_sense_detector_shape(self, shape_type: str):
        """Controls the linearity of the detector.
        Parameters:
        shape_type: LINear|LOGarithmic"""
        valid_types = {"LINEAR", "LOGARITHMIC", "LIN", "LOG"}
        type_upper = shape_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid shape type: '{shape_type}'. Must be 'LINEAR' or 'LOGARITHMIC'.")

        if type_upper == "LINEAR": scpi_value = "LIN"
        elif type_upper == "LOGARITHMIC": scpi_value = "LOG"
        else: scpi_value = type_upper

        self.instrument.write(f":SENS:DET:SHAP {scpi_value}")

    def get_sense_detector_shape(self) -> str:
        """Returns the linearity of the detector ('LINEAR' or 'LOGARITHMIC')."""
        response = self.instrument.query(":SENS:DET:SHAP?").strip().upper()
        if response.startswith("LIN"):
            return "LINEAR"
        elif response.startswith("LOG"):
            return "LOGARITHMIC"
        return response

    
    def sense_distance_reset(self):
        """Sets DISTance to 0.
        Notes: This is an event command; no query."""
        self.instrument.write(":SENS:DIST:RES")

    
    def set_sense_filter_lpass_state(self, enable: bool):
        """Turns the sensor low pass filter on and off.
        Parameters:
        enable: True to turn ON, False to turn OFF."""
        scpi_value = 1 if enable else 0
        self.instrument.write(f":SENS:FILT:LPAS:STATE {scpi_value}")

    def get_sense_filter_lpass_state(self) -> bool:
        """Returns True if the sensor low pass filter is ON, False if OFF."""
        response = self.instrument.query(":SENS:FILT:LPAS:STATE?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for filter low pass state: '{response}'")

    def set_sense_filter_lpass_frequency(self, frequency_hz: float):
        """Determines the cutoff frequency of the low pass filter.
        Parameters:
        frequency_hz: The cutoff frequency in Hz (numeric value)."""
        self.instrument.write(f":SENS:FILT:LPAS:FREQ {frequency_hz}")

    def get_sense_filter_lpass_frequency(self) -> float:
        """Returns the cutoff frequency of the low pass filter."""
        response = self.instrument.query(":SENS:FILT:LPAS:FREQ?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for filter low pass frequency (not numeric): '{response}'")

    def set_sense_filter_hpass_state(self, enable: bool):
        """Turns the sensor high pass filter on and off.
        Parameters:
        enable: True to turn ON, False to turn OFF."""
        scpi_value = 1 if enable else 0
        self.instrument.write(f":SENS:FILT:HPAS:STATE {scpi_value}")

    def get_sense_filter_hpass_state(self) -> bool:
        """Returns True if the sensor high pass filter is ON, False if OFF."""
        response = self.instrument.query(":SENS:FILT:HPAS:STATE?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for filter high pass state: '{response}'")

    def set_sense_filter_hpass_frequency(self, frequency_hz: float):
        """Determines the cutoff frequency of the high pass filter.
        Parameters:
        frequency_hz: The cutoff frequency in Hz (numeric value)."""
        self.instrument.write(f":SENS:FILT:HPAS:FREQ {frequency_hz}")

    def get_sense_filter_hpass_frequency(self) -> float:
        """Returns the cutoff frequency of the high pass filter."""
        response = self.instrument.query(":SENS:FILT:HPAS:FREQ?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for filter high pass frequency (not numeric): '{response}'")

    
    def set_sense_filter_demphasis_state(self, enable: bool):
        """Turns the FM de-emphasis filter on and off.
        Parameters:
        enable: True to turn ON, False to turn OFF."""
        scpi_value = 1 if enable else 0
        self.instrument.write(f":SENS:FILT:DEMP:STATE {scpi_value}")

    def get_sense_filter_demphasis_state(self) -> bool:
        """Returns True if the FM de-emphasis filter is ON, False if OFF."""
        response = self.instrument.query(":SENS:FILT:DEMP:STATE?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for filter de-emphasis state: '{response}'")

    def set_sense_filter_demphasis_tconstant(self, time_constant_seconds: float):
        """Determines the Time CONstant of the FM de-emphasis filter.
        Parameters:
        time_constant_seconds: The time constant in seconds (numeric value)."""
        self.instrument.write(f":SENS:FILT:DEMP:TCON {time_constant_seconds}")

    def get_sense_filter_demphasis_tconstant(self) -> float:
        """Returns the Time CONstant of the FM de-emphasis filter."""
        response = self.instrument.query(":SENS:FILT:DEMP:TCON?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for filter de-emphasis time constant (not numeric): '{response}'")

    def set_sense_filter_ccitt_state(self, enable: bool):
        """Turns the CCITT filter on and off.
        Parameters:
        enable: True to turn ON, False to turn OFF."""
        scpi_value = 1 if enable else 0
        self.instrument.write(f":SENS:FILT:CCIT:STATE {scpi_value}")

    def get_sense_filter_ccitt_state(self) -> bool:
        """Returns True if the CCITT filter is ON, False if OFF."""
        response = self.instrument.query(":SENS:FILT:CCIT:STATE?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for filter CCITT state: '{response}'")

    def set_sense_filter_cmessage_state(self, enable: bool):
        """Turns the C-Message sensor filter on and off.
        Parameters:
        enable: True to turn ON, False to turn OFF."""
        scpi_value = 1 if enable else 0
        self.instrument.write(f":SENS:FILT:CMES:STATE {scpi_value}")

    def get_sense_filter_cmessage_state(self) -> bool:
        """Returns True if the C-Message sensor filter is ON, False if OFF."""
        response = self.instrument.query(":SENS:FILT:CMES:STATE?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for filter C-Message state: '{response}'")

    
    def set_sense_filter_ccir_state(self, enable: bool):
        """Turns the CCIR weighting filter on and off.
        Parameters:
        enable: True to turn ON, False to turn OFF."""
        scpi_value = 1 if enable else 0
        self.instrument.write(f":SENS:FILT:CCIR:STATE {scpi_value}")

    def get_sense_filter_ccir_state(self) -> bool:
        """Returns True if the CCIR weighting filter is ON, False if OFF."""
        response = self.instrument.query(":SENS:FILT:CCIR:STATE?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for filter CCIR state: '{response}'")

    def set_sense_filter_carm_state(self, enable: bool):
        """Turns the CCIR/ARM weighting filter on and off.
        Parameters:
        enable: True to turn ON, False to turn OFF."""
        scpi_value = 1 if enable else 0
        self.instrument.write(f":SENS:FILT:CARM:STATE {scpi_value}")

    def get_sense_filter_carm_state(self) -> bool:
        """Returns True if the CCIR/ARM weighting filter is ON, False if OFF."""
        response = self.instrument.query(":SENS:FILT:CARM:STATE?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for filter CARM state: '{response}'")

    def set_sense_filter_aweighting_state(self, enable: bool):
        """Turns the "A" weighting sensor filter on and off.
        Parameters:
        enable: True to turn ON, False to turn OFF."""
        scpi_value = 1 if enable else 0
        self.instrument.write(f":SENS:FILT:AW:STATE {scpi_value}")

    def get_sense_filter_aweighting_state(self) -> bool:
        """Returns True if the "A" weighting sensor filter is ON, False if OFF."""
        response = self.instrument.query(":SENS:FILT:AW:STATE?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for filter A-Weighting state: '{response}'")

    
    def set_sense_fm_deviation_range_auto(self, auto_state: str):
        """Sets the range for the FM sensor function to a value determined to give the most dynamic range.
        Parameters:
        auto_state: Boolean (ON|OFF) or 'ONCE'. Selecting 'ONCE' sets AUTO to ON and then OFF."""
        normalized_state = auto_state.upper()
        if normalized_state in {1, "ON"}:
            scpi_value = "ON"
        elif normalized_state in {0, "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":SENS:FM:DEV:RANG:AUTO {scpi_value}")

    def get_sense_fm_deviation_range_auto(self) -> str:
        """Returns the auto state of the FM deviation range ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query(":SENS:FM:DEV:RANG:AUTO?").strip()
        if response == 1:
            return "ON"
        elif response == 0:
            return "OFF"
        else:
            return response.upper()

    def set_sense_fm_deviation_range_upper(self, value: float):
        """Specifies the maximum signal level expected for the FM sensor input.
        Parameters:
        value: The upper range value (numeric value)."""
        self.instrument.write(f":SENS:FM:DEV:RANG:UPP {value}")

    def get_sense_fm_deviation_range_upper(self) -> float:
        """Returns the maximum signal level expected for the FM sensor input."""
        response = self.instrument.query(":SENS:FM:DEV:RANG:UPP?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for FM deviation range upper (not numeric): '{response}'")

    def set_sense_fm_deviation_range_lower(self, value: float):
        """Specifies the smallest signal level expected for the FM sensor input.
        Parameters:
        value: The lower range value (numeric value)."""
        self.instrument.write(f":SENS:FM:DEV:RANG:LOW {value}")

    def get_sense_fm_deviation_range_lower(self) -> float:
        """Returns the smallest signal level expected for the FM sensor input."""
        response = self.instrument.query(":SENS:FM:DEV:RANG:LOW?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for FM deviation range lower (not numeric): '{response}'")

    
    def set_sense_frequency_aperture(self, value: float):
        """Specifies the acquisition/sampling/gate time for a single measurement point for Frequency.
        Parameters:
        value: The aperture time in seconds (numeric value)."""
        self.instrument.write(f":SENS:FREQ:APER {value}")

    def get_sense_frequency_aperture(self) -> float:
        """Returns the acquisition/sampling/gate time for Frequency."""
        response = self.instrument.query(":SENS:FREQ:APER?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for frequency aperture (not numeric): '{response}'")

    def set_sense_frequency_center(self, value: float):
        """Sets the center frequency of the sweep or measurement.
        Parameters:
        value: The center frequency in Hz (numeric value)."""
        self.instrument.write(f":SENS:FREQ:CENT {value}")

    def get_sense_frequency_center(self) -> float:
        """Returns the center frequency of the sweep or measurement."""
        response = self.instrument.query(":SENS:FREQ:CENT?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for frequency center (not numeric): '{response}'")

    def set_sense_frequency_cw_fixed(self, value: float):
        """Selects a frequency of a non-swept signal (Continuous Wave or FIXed).
        Parameters:
        value: The frequency in Hz (numeric value)."""
        self.instrument.write(f":SENS:FREQ:CW {value}")

    def get_sense_frequency_cw_fixed(self) -> float:
        """Returns the frequency of a non-swept signal (Continuous Wave or FIXed)."""
        response = self.instrument.query(":SENS:FREQ:CW?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for frequency CW/FIXed (not numeric): '{response}'")

    
    def set_sense_frequency_cw_afc(self, afc_state: str):
        """If AFC is ON the sensor is coupled to the frequency of the signal.
        Parameters:
        afc_state: Boolean (ON|OFF) or 'ONCE'. Selecting 'ONCE' sets AUTO to ON and then OFF."""
        normalized_state = afc_state.upper()
        if normalized_state in {1, "ON"}:
            scpi_value = "ON"
        elif normalized_state in {0, "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid AFC state: '{afc_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":SENS:FREQ:CW:AFC {scpi_value}")

    def get_sense_frequency_cw_afc(self) -> str:
        """Returns the AFC state of the CW frequency ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query(":SENS:FREQ:CW:AFC?").strip()
        if response == 1:
            return "ON"
        elif response == 0:
            return "OFF"
        else:
            return response.upper()

    def set_sense_frequency_cw_auto(self, auto_state: str):
        """Couples the CW frequency to center frequency.
        Parameters:
        auto_state: Boolean (ON|OFF) or 'ONCE'. Selecting 'ONCE' sets AUTO to ON and then OFF."""
        normalized_state = auto_state.upper()
        if normalized_state in {1, "ON"}:
            scpi_value = "ON"
        elif normalized_state in {0, "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":SENS:FREQ:CW:AUTO {scpi_value}")

    def get_sense_frequency_cw_auto(self) -> str:
        """Returns the auto state of the CW frequency ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query(":SENS:FREQ:CW:AUTO?").strip()
        if response == 1:
            return "ON"
        elif response == 0:
            return "OFF"
        else:
            return response.upper()

    def set_sense_frequency_manual(self, value: float):
        """Sets the manual frequency for a sweep, limited by START and STOP.
        Parameters:
        value: The manual frequency in Hz (numeric value)."""
        self.instrument.write(f":SENS:FREQ:MAN {value}")

    def get_sense_frequency_manual(self) -> float:
        """Returns the manual frequency."""
        response = self.instrument.query(":SENS:FREQ:MAN?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for frequency manual (not numeric): '{response}'")

    def set_sense_frequency_mode(self, mode_type: str):
        """Determines which set of commands control the frequency.
        Parameters:
        mode_type: CW|FIXed|SWEep|LIST|SOURce"""
        valid_types = {"CW", "FIXED", "SWEEP", "LIST", "SOURCE", "FIX", "SWE", "SOUR"}
        type_upper = mode_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid frequency mode: '{mode_type}'.")

        if type_upper == "FIXED": scpi_value = "FIX"
        elif type_upper == "SWEEP": scpi_value = "SWE"
        elif type_upper == "SOURCE": scpi_value = "SOUR"
        else: scpi_value = type_upper

        self.instrument.write(f":SENS:FREQ:MODE {scpi_value}")

    def get_sense_frequency_mode(self) -> str:
        """Returns which set of commands control the frequency ('CW', 'FIXED', 'SWEEP', 'LIST', or 'SOURCE')."""
        response = self.instrument.query(":SENS:FREQ:MODE?").strip().upper()
        if response == "CW": return "CW"
        elif response.startswith("FIX"): return "FIXED"
        elif response.startswith("SWE"): return "SWEEP"
        elif response.startswith("LIST"): return "LIST"
        elif response.startswith("SOUR"): return "SOURCE"
        return response

    
    def set_sense_frequency_multiplier(self, value: float):
        """Sets a reference multiplier for all other frequency settings in the instrument.
        Parameters:
        value: The multiplier (numeric value)."""
        self.instrument.write(f":SENS:FREQ:MULT {value}")

    def get_sense_frequency_multiplier(self) -> float:
        """Returns the reference multiplier for all other frequency settings."""
        response = self.instrument.query(":SENS:FREQ:MULT?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for frequency multiplier (not numeric): '{response}'")

    def set_sense_frequency_offset(self, value: float):
        """Sets a reference frequency offset for all other absolute frequency settings in the instrument.
        Parameters:
        value: The offset in Hz (numeric value)."""
        self.instrument.write(f":SENS:FREQ:OFFS {value}")

    def get_sense_frequency_offset(self) -> float:
        """Returns the reference frequency offset."""
        response = self.instrument.query(":SENS:FREQ:OFFS?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for frequency offset (not numeric): '{response}'")

    def set_sense_frequency_range_upper(self, value: float):
        """Specifies the maximum value expected for the frequency sensor input.
        Parameters:
        value: The upper range value in Hz (numeric value)."""
        self.instrument.write(f":SENS:FREQ:RANG:UPP {value}")

    def get_sense_frequency_range_upper(self) -> float:
        """Returns the maximum value expected for the frequency sensor input."""
        response = self.instrument.query(":SENS:FREQ:RANG:UPP?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for frequency range upper (not numeric): '{response}'")

    def set_sense_frequency_range_lower(self, value: float):
        """Specifies the lowest value expected for frequency sensor input.
        Parameters:
        value: The lower range value in Hz (numeric value)."""
        self.instrument.write(f":SENS:FREQ:RANG:LOW {value}")

    def get_sense_frequency_range_lower(self) -> float:
        """Returns the lowest value expected for frequency sensor input."""
        response = self.instrument.query(":SENS:FREQ:RANG:LOW?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for frequency range lower (not numeric): '{response}'")

    def set_sense_frequency_range_auto(self, auto_state: str):
        """Sets the frequency range to the value determined by the instrument.
        Parameters:
        auto_state: Boolean (ON|OFF) or 'ONCE'. Selecting 'ONCE' sets AUTO to ON and then OFF."""
        normalized_state = auto_state.upper()
        if normalized_state in {1, "ON"}:
            scpi_value = "ON"
        elif normalized_state in {0, "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":SENS:FREQ:RANG:AUTO {scpi_value}")

    def get_sense_frequency_range_auto(self) -> str:
        """Returns the auto state of the frequency range ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query(":SENS:FREQ:RANG:AUTO?").strip()
        if response == 1:
            return "ON"
        elif response == 0:
            return "OFF"
        else:
            return response.upper()

    
    def set_sense_frequency_resolution(self, value: float):
        """Specifies the absolute resolution of the frequency measurement.
        Parameters:
        value: The resolution value in Hz (numeric value)."""
        self.instrument.write(f":SENS:FREQ:RES {value}")

    def get_sense_frequency_resolution(self) -> float:
        """Returns the absolute resolution of the frequency measurement."""
        response = self.instrument.query(":SENS:FREQ:RES?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for frequency resolution (not numeric): '{response}'")

    def set_sense_frequency_resolution_auto(self, auto_state: str):
        """Allows the system to determine the best resolution for the other measurement conditions.
        Parameters:
        auto_state: Boolean (ON|OFF) or 'ONCE'. Selecting 'ONCE' sets AUTO to ON and then OFF."""
        normalized_state = auto_state.upper()
        if normalized_state in {1, "ON"}:
            scpi_value = "ON"
        elif normalized_state in {0, "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":SENS:FREQ:RES:AUTO {scpi_value}")

    def get_sense_frequency_resolution_auto(self) -> str:
        """Returns the auto state of the frequency resolution ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query(":SENS:FREQ:RES:AUTO?").strip()
        if response == 1:
            return "ON"
        elif response == 0:
            return "OFF"
        else:
            return response.upper()

    def set_sense_frequency_span(self, value: float):
        """Sets the frequency span.
        Parameters:
        value: The span in Hz (numeric value)."""
        self.instrument.write(f":SENS:FREQ:SPAN {value}")

    def get_sense_frequency_span(self) -> float:
        """Returns the frequency span."""
        response = self.instrument.query(":SENS:FREQ:SPAN?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for frequency span (not numeric): '{response}'")

    def set_sense_frequency_span_hold(self, enable: bool):
        """Prevents the SPAN from being changed implicitly by coupling.
        Parameters:
        enable: True to hold, False to allow changes."""
        scpi_value = 1 if enable else 0
        self.instrument.write(f":SENS:FREQ:SPAN:HOLD {scpi_value}")

    def get_sense_frequency_span_hold(self) -> bool:
        """Returns True if SPAN is held, False if not."""
        response = self.instrument.query(":SENS:FREQ:SPAN:HOLD?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for frequency span hold state: '{response}'")

    def set_sense_frequency_span_link(self, link_parameter: str):
        """Allows default couplings for SPAN to be overridden, selecting the parameter that shall not be changed.
        Parameters:
        link_parameter: CENTer|STARt|STOP"""
        valid_params = {"CENTER", "START", "STOP", "CENT", "STAR", "STOP"}
        param_upper = link_parameter.upper()
        if param_upper not in valid_params:
            raise ValueError(f"Invalid link parameter: '{link_parameter}'. Must be 'CENTer', 'STARt', or 'STOP'.")

        if param_upper == "CENTER": scpi_value = "CENT"
        elif param_upper == "START": scpi_value = "STAR"
        else: scpi_value = param_upper

        self.instrument.write(f":SENS:FREQ:SPAN:LINK {scpi_value}")

    def get_sense_frequency_span_link(self) -> str:
        """Returns the parameter that shall not be changed when SPAN's value is changed ('CENTER', 'START', or 'STOP')."""
        response = self.instrument.query(":SENS:FREQ:SPAN:LINK?").strip().upper()
        if response.startswith("CENT"):
            return "CENTER"
        elif response.startswith("STAR"):
            return "START"
        elif response.startswith("STOP"):
            return "STOP"
        return response

    def sense_frequency_span_full(self):
        """Sets start frequency to its minimum, stop frequency to its maximum, and center/span to coupled values.
        Notes: This is an event command; no query."""
        self.instrument.write(":SENS:FREQ:SPAN:FULL")

    
    def set_sense_frequency_start(self, value: float):
        """Sets the starting frequency for a sweep or measurement.
        Parameters:
        value: The starting frequency in Hz (numeric value)."""
        self.instrument.write(f":SENS:FREQ:STAR {value}")

    def get_sense_frequency_start(self) -> float:
        """Returns the starting frequency for a sweep or measurement."""
        response = self.instrument.query(":SENS:FREQ:STAR?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for frequency start (not numeric): '{response}'")

    def set_sense_frequency_stop(self, value: float):
        """Sets the stop frequency of a sweep or measurement.
        Parameters:
        value: The stop frequency in Hz (numeric value)."""
        self.instrument.write(f":SENS:FREQ:STOP {value}")

    def get_sense_frequency_stop(self) -> float:
        """Returns the stop frequency of a sweep or measurement."""
        response = self.instrument.query(":SENS:FREQ:STOP?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for frequency stop (not numeric): '{response}'")

    
    def get_sense_data(self, data_handle: str = None):
        """Provides access to the result(s) of the SENSe block.
        Parameters:
        data_handle: (Optional) The data handle (e.g., 'VOLTage:AC 2').
        Returns: The sensed data. The format depends on the instrument and FORMat subsystem."""
        if data_handle:
            return self.instrument.query(f":SENS:DATA? '{data_handle}'")
        else:
            return self.instrument.query(":SENS:DATA?")

    def get_sense_data_preamble(self, data_handle: str = None):
        """Returns the preamble information supporting the DATA(CURVe(VALues)).
        Parameters:
        data_handle: (Optional) The data handle.
        Returns: The preamble information string."""
        if data_handle:
            return self.instrument.query(f":SENS:DATA:PRE? '{data_handle}'")
        else:
            return self.instrument.query(":SENS:DATA:PRE?")

    def set_sense_function_concurrent(self, enable: bool):
        """Indicates whether the SENSor block should be configured to SENSe one function at a time or concurrently.
        Parameters:
        enable: True for concurrent sensing, False for one function at a time."""
        scpi_value = 1 if enable else 0
        self.instrument.write(f":SENS:FUNC:CONC {scpi_value}")

    def get_sense_function_concurrent(self) -> bool:
        """Returns True if concurrent sensing is enabled, False if not."""
        response = self.instrument.query(":SENS:FUNC:CONC?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for function concurrent state: '{response}'")

    
    def set_sense_function_off(self, sensor_functions: str):
        """Selects the <sensor_function>s to be turned off.
        Parameters:
        sensor_functions: A comma-separated string of sensor functions (e.g., '"VOLT:AC","CURR:DC"')."""
        self.instrument.write(f":SENS:FUNC:OFF {sensor_functions}")

    def get_sense_function_off(self) -> list[str]:
        """Returns a comma-separated list of functions which are currently OFF.
        Returns: A list of sensor function short form mnemonics."""
        response = self.instrument.query(":SENS:FUNC:OFF?").strip()
        if not response:
            return []
        # Response is comma-separated quoted strings (e.g., '"VOLT:AC","CURR:DC"')
        return [func.strip().strip("'\"") for func in response.split(',')]

    def sense_function_off_all(self):
        """Turns OFF all of the <sensor_function>s which the instrument can concurrently sense.
        Notes: No query."""
        self.instrument.write(":SENS:FUNC:OFF:ALL")

    def get_sense_function_off_count(self) -> int:
        """Returns the number of <sensor_function>s which are OFF.
        Notes: Query only."""
        response = self.instrument.query(":SENS:FUNC:OFF:COUN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for function off count (not integer): '{response}'")

    def turn_sense_function_on(self, sensor_functions: str):
        """Selects the <sensor_function>(s) to be SENSed by the instrument.
        Parameters:
        sensor_functions: A comma-separated string of sensor functions (e.g., '"VOLT:AC"'). If CONCurrent is OFF, only one function is allowed."""
        self.instrument.write(f":SENS:FUNC:ON {sensor_functions}")

    def which_sense_function_on(self) -> list[str]:
        """Returns a comma-separated list of functions which are on.
        Returns: A list of sensor function short form mnemonics."""
        response = self.instrument.query(":SENS:FUNC:ON?").strip()
        if not response:
            return []
        # Response is comma-separated quoted strings (e.g., '"VOLT:AC"')
        return [func.strip().strip("'\"") for func in response.split(',')]

    
    def sense_function_on_all(self):
        """Turns ON all of the <sensor_function>s which the instrument can concurrently sense.
        Notes: No query."""
        self.instrument.write(":SENS:FUNC:ON:ALL")

    def get_sense_function_on_count(self) -> int:
        """Returns the number of <sensor_function>s which are ON.
        Notes: Query only."""
        response = self.instrument.query(":SENS:FUNC:ON:COUN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for function on count (not integer): '{response}'")

    def get_sense_function_state(self, sensor_function: str) -> bool:
        """Returns a Boolean indicating whether the specified <sensor_function> is currently ON or OFF.
        Parameters:
        sensor_function: The sensor function to query (e.g., 'VOLT:AC').
        Returns: True if ON, False if OFF."""
        response = self.instrument.query(f":SENS:FUNC:STATE? '{sensor_function}'").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for sensor function state: '{response}'")

        # These functions are for the specific format of SENSe:FUNCtion "<function_name>" commands.
    # The `set_sense_function` below is a general one for the main command.

    def set_sense_function(self, function_string: str):
        """Sets the sensor function, allowing for presentation layer, function name, input blocks, and subnodes.
        Parameters:
        function_string: The complete sensor function string (e.g., '"XVOLtage:VOLTage:AC 2 ON AVER:TYPE RMS"')."""
        self.instrument.write(f":SENS:FUNC '{function_string}'")

    def get_sense_function(self) -> str:
        """Returns the currently configured sensor function string.
        Returns: The sensor function string (e.g., '"VOLT:AC 2"')."""
        response = self.instrument.query(":SENS:FUNC?").strip().strip("'\"")
        return response

        # These are illustrative wrappers for common function calls based on the FUNCTION tree.
    # They demonstrate how you might construct the `function_string` for `set_sense_function`.
    # A complete set would require a much larger number of functions or a more dynamic approach.

    def sense_function_acceleration(self):
        """Sets the sensor function to ACCeleration."""
        self.set_sense_function("ACCEL")

    def sense_function_am(self):
        """Sets the sensor function to AM (Amplitude modulation)."""
        self.set_sense_function("AM")

    def sense_function_am_depth(self):
        """Sets the sensor function to AM:DEPTh."""
        self.set_sense_function("AM:DEP")

    def sense_function_am_distortion(self):
        """Sets the sensor function to AM:DISTortion."""
        self.set_sense_function("AM:DIST")

    def sense_function_am_frequency(self):
        """Sets the sensor function to AM:FREQuency."""
        self.set_sense_function("AM:FREQ")

    def sense_function_am_sndratio(self):
        """Sets the sensor function to AM:SNDRatio (SINAD)."""
        self.set_sense_function("AM:SNDR")

    def sense_function_am_snr(self):
        """Sets the sensor function to AM:SNR (Signal to Noise Ratio)."""
        self.set_sense_function("AM:SNR")

    def sense_function_am_thd(self):
        """Sets the sensor function to AM:THD (Total Harmonic Distortion)."""
        self.set_sense_function("AM:THD")

    def sense_function_concentration(self):
        """Sets the sensor function to CONCentration (Non-time-aligned)."""
        self.set_sense_function("CONC")

    def sense_function_concentration_raw(self):
        """Sets the sensor function to CONCentration:RAW."""
        self.set_sense_function("CONC:RAW")

    def sense_function_concentration_sdeviation(self):
        """Sets the sensor function to CONCentration:SDEViation (Standard Deviation)."""
        self.set_sense_function("CONC:SDEV")

    def sense_function_concentration_talign(self):
        """Sets the sensor function to CONCentration:TALign (Time-aligned analyzer)."""
        self.set_sense_function("CONC:TAL")

    def sense_function_condition(self):
        """Sets the sensor function to CONDition (True/False condition of a signal)."""
        self.set_sense_function("COND")

    def sense_function_current_dc(self):
        """Sets the sensor function to CURRent:DC."""
        self.set_sense_function("CURR:DC")

    def sense_function_current_ac(self):
        """Sets the sensor function to CURRent:AC."""
        self.set_sense_function("CURR:AC")

    def sense_function_distance(self):
        """Sets the sensor function to DISTance."""
        self.set_sense_function("DIST")

    def sense_function_fm(self):
        """Sets the sensor function to FM (Frequency modulation)."""
        self.set_sense_function("FM")

    def sense_function_fm_deviation(self):
        """Sets the sensor function to FM:DEViation."""
        self.set_sense_function("FM:DEV")

    def sense_function_fm_distortion(self):
        """Sets the sensor function to FM:DISTortion."""
        self.set_sense_function("FM:DIST")

    def sense_function_fm_frequency(self):
        """Sets the sensor function to FM:FREQuency."""
        self.set_sense_function("FM:FREQ")

    def sense_function_fm_sndratio(self):
        """Sets the sensor function to FM:SNDRatio (SINAD)."""
        self.set_sense_function("FM:SNDR")

    def sense_function_fm_snr(self):
        """Sets the sensor function to FM:SNR (Signal to Noise Ratio)."""
        self.set_sense_function("FM:SNR")

    def sense_function_fm_thd(self):
        """Sets the sensor function to FM:THD (Total Harmonic Distortion)."""
        self.set_sense_function("FM:THD")

    def sense_function_ferror(self):
        """Sets the sensor function to FERRor (Force Error)."""
        self.set_sense_function("FERR")

    def sense_function_force(self):
        """Sets the sensor function to FORCe."""
        self.set_sense_function("FORC")

    def sense_function_frequency(self):
        """Sets the sensor function to FREQuency (Direct sensing of frequency)."""
        self.set_sense_function("FREQ")

    def sense_function_fresistance(self):
        """Sets the sensor function to FRESistance (Four-wire resistance)."""
        self.set_sense_function("FRES")

    def sense_function_period(self):
        """Sets the sensor function to PERiod (Inverse of frequency)."""
        self.set_sense_function("PER")

    def sense_function_phase(self):
        """Sets the sensor function to PHASe (Direct sensing of phase)."""
        self.set_sense_function("PHAS")

    def sense_function_pm(self):
        """Sets the sensor function to PM (Pulse modulation)."""
        self.set_sense_function("PM")

    def sense_function_pm_deviation(self):
        """Sets the sensor function to PM:DEViation."""
        self.set_sense_function("PM:DEV")

    def sense_function_pm_distortion(self):
        """Sets the sensor function to PM:DISTortion."""
        self.set_sense_function("PM:DIST")

    def sense_function_pm_frequency(self):
        """Sets the sensor function to PM:FREQuency."""
        self.set_sense_function("PM:FREQ")

    def sense_function_pm_sndratio(self):
        """Sets the sensor function to PM:SNDRatio (SINAD)."""
        self.set_sense_function("PM:SNDR")

    def sense_function_pm_snr(self):
        """Sets the sensor function to PM:SNR (Signal to Noise Ratio)."""
        self.set_sense_function("PM:SNR")

    def sense_function_pm_thd(self):
        """Sets the sensor function to PM:THD (Total Harmonic Distortion)."""
        self.set_sense_function("PM:THD")

    def sense_function_power_ac(self):
        """Sets the sensor function to POWer:AC."""
        self.set_sense_function("POW:AC")

    def sense_function_power_achannel(self):
        """Sets the sensor function to POWer:ACHannel (Adjacent Channel Power)."""
        self.set_sense_function("POW:ACH")

    def sense_function_power_achannel_lower(self):
        """Sets the sensor function to POWer:ACHannel:LOWer (Lower Adjacent Channel Power)."""
        self.set_sense_function("POW:ACH:LOW")

    def sense_function_power_achannel_upper(self):
        """Sets the sensor function to POWer:ACHannel:UPPer (Upper Adjacent Channel Power)."""
        self.set_sense_function("POW:ACH:UPP")

    def sense_function_power_coherence(self):
        """Sets the sensor function to POWer:COHerence."""
        self.set_sense_function("POW:COH")

    def sense_function_power_cross(self):
        """Sets the sensor function to POWer:CROSs (Cross Product)."""
        self.set_sense_function("POW:CROS")

    def sense_function_power_dc(self):
        """Sets the sensor function to POWer:DC."""
        self.set_sense_function("POW:DC")

    def sense_function_power_distortion(self):
        """Sets the sensor function to POWer:DISTortion."""
        self.set_sense_function("POW:DIST")

    def sense_function_power_psdensity(self):
        """Sets the sensor function to POWer:PSDensity (Power Spectral Density)."""
        self.set_sense_function("POW:PSD")

    def sense_function_power_s11(self):
        """Sets the sensor function to POWer:S11 (Scattering Parameter Function)."""
        self.set_sense_function("POW:S11")

    def sense_function_power_s12(self):
        """Sets the sensor function to POWer:S12 (Scattering Parameter Function)."""
        self.set_sense_function("POW:S12")

    def sense_function_power_s21(self):
        """Sets the sensor function to POWer:S21 (Scattering Parameter Function)."""
        self.set_sense_function("POW:S21")

    def sense_function_power_s22(self):
        """Sets the sensor function to POWer:S22 (Scattering Parameter Function)."""
        self.set_sense_function("POW:S22")

    def sense_function_power_sndratio(self):
        """Sets the sensor function to POWer:SNDRatio (SINAD)."""
        self.set_sense_function("POW:SNDR")

    def sense_function_power_snr(self):
        """Sets the sensor function to POWer:SNR (Signal to Noise Ratio)."""
        self.set_sense_function("POW:SNR")

    def sense_function_power_thd(self):
        """Sets the sensor function to POWer:THD (Total Harmonic Distortion)."""
        self.set_sense_function("POW:THD")

    def sense_function_pulm(self):
        """Sets the sensor function to PULM (Pulse modulation)."""
        self.set_sense_function("PULM")

    def sense_function_resistance(self):
        """Sets the sensor function to RESistance (Two wire resistance)."""
        self.set_sense_function("RES")

    def sense_function_speed(self):
        """Sets the sensor function to SPEed."""
        self.set_sense_function("SPE")

    def sense_function_speed_front(self):
        """Sets the sensor function to SPEed:FRONt (Front Roll Speed)."""
        self.set_sense_function("SPE:FRON")

    def sense_function_speed_rear(self):
        """Sets the sensor function to SPEed[:REAR] (Rear Roll Speed)."""
        self.set_sense_function("SPE:REAR")

    def sense_function_ssb(self):
        """Sets the sensor function to SSB (Single sideband modulation)."""
        self.set_sense_function("SSB")

    def sense_function_temperature(self):
        """Sets the sensor function to TEMPerature."""
        self.set_sense_function("TEMP")

    def sense_function_timer(self):
        """Sets the sensor function to TIMer."""
        self.set_sense_function("TIM")

    def sense_function_timer_count(self):
        """Sets the sensor function to TIMer:COUNt."""
        self.set_sense_function("TIM:COUN")

    def sense_function_tinterval(self):
        """Sets the sensor function to TINTerval (Time Interval)."""
        self.set_sense_function("TINT")

    def sense_function_totalize(self):
        """Sets the sensor function to TOTalize (Totalize Events)."""
        self.set_sense_function("TOT")

    def sense_function_tploss(self):
        """Sets the sensor function to TPLoss (Target Parasitic Loss)."""
        self.set_sense_function("TPL")

    def sense_function_voltage_ac(self):
        """Sets the sensor function to VOLTage:AC."""
        self.set_sense_function("VOLT:AC")

    def sense_function_voltage_cdfunction(self):
        """Sets the sensor function to VOLTage:CDFunction (Cumulative Density Function)."""
        self.set_sense_function("VOLT:CDF")

    def sense_function_voltage_dc(self):
        """Sets the sensor function to VOLTage:DC."""
        self.set_sense_function("VOLT:DC")

    def sense_function_voltage_histogram(self):
        """Sets the sensor function to VOLTage:HISTogram."""
        self.set_sense_function("VOLT:HIST")

    def sense_function_voltage_pdfunction(self):
        """Sets the sensor function to VOLTage:PDFunction (Probability Density Function)."""
        self.set_sense_function("VOLT:PDF")

    
    def set_sense_list_count(self, value: int):
        """Controls the number of times the sequence list is scanned when a trigger is received.
        Parameters:
        value: The count (numeric value)."""
        if not isinstance(value, int) or value < 1:
            raise ValueError("Count must be a positive integer.")
        self.instrument.write(f":SENS:LIST:COUN {value}")

    def get_sense_list_count(self) -> int:
        """Returns the number of times the sequence list is scanned."""
        response = self.instrument.query(":SENS:LIST:COUN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for list count (not integer): '{response}'")

    def set_sense_list_direction(self, direction: str):
        """Specifies the direction that the sequence list is scanned.
        Parameters:
        direction: UP|DOWN"""
        valid_directions = {"UP", "DOWN"}
        direction_upper = direction.upper()
        if direction_upper not in valid_directions:
            raise ValueError(f"Invalid direction: '{direction}'. Must be 'UP' or 'DOWN'.")
        self.instrument.write(f":SENS:LIST:DIR {direction_upper}")

    def get_sense_list_direction(self) -> str:
        """Returns the direction that the sequence list is scanned ('UP' or 'DOWN')."""
        response = self.instrument.query(":SENS:LIST:DIR?").strip().upper()
        return response

    def set_sense_list_dwell(self, dwell_times: list[float]):
        """Specifies the dwell time points of the lists in seconds.
        Parameters:
        dwell_times: A list of numeric values representing dwell times."""
        data_str = ",".join(map(str, dwell_times))
        self.instrument.write(f":SENS:LIST:DWEL {data_str}")

    def get_sense_list_dwell(self) -> list[float]:
        """Returns the dwell time points of the lists in seconds."""
        response = self.instrument.query(":SENS:LIST:DWEL?").strip()
        return [float(x) for x in response.split(',')]

    def get_sense_list_dwell_points(self) -> int:
        """Returns the number of points currently in the DWELl list."""
        response = self.instrument.query(":SENS:LIST:DWEL:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for list dwell points (not integer): '{response}'")

    
    def set_sense_list_frequency(self, frequencies_hz: list[float]):
        """Specifies the frequency points of the list set in Hz.
        Parameters:
        frequencies_hz: A list of numeric values representing frequencies."""
        data_str = ",".join(map(str, frequencies_hz))
        self.instrument.write(f":SENS:LIST:FREQ {data_str}")

    def get_sense_list_frequency(self) -> list[float]:
        """Returns the frequency points of the list set in Hz."""
        response = self.instrument.query(":SENS:LIST:FREQ?").strip()
        return [float(x) for x in response.split(',')]

    def get_sense_list_frequency_points(self) -> int:
        """Returns the number of points currently in the FREQuency list."""
        response = self.instrument.query(":SENS:LIST:FREQ:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for list frequency points (not integer): '{response}'")

    def set_sense_list_sequence(self, sequence_indices: list[int]):
        """Defines a sequence for stepping through the list using 1-based indices.
        Parameters:
        sequence_indices: A list of numeric values representing indices into the lists."""
        if not all(isinstance(n, int) and n >= 1 for n in sequence_indices):
            raise ValueError("All sequence indices must be positive integers.")
        data_str = ",".join(map(str, sequence_indices))
        self.instrument.write(f":SENS:LIST:SEQ {data_str}")

    def get_sense_list_sequence(self) -> list[int]:
        """Returns the sequence for stepping through the list."""
        response = self.instrument.query(":SENS:LIST:SEQ?").strip()
        return [int(x) for x in response.split(',')]

    def set_sense_list_sequence_auto(self, auto_state: str):
        """When on, the sequence list is set to 1 through N, where N is the longest list.
        Parameters:
        auto_state: Boolean (ON|OFF) or 'ONCE'. Selecting 'ONCE' sets AUTO to ON and then OFF."""
        normalized_state = auto_state.upper()
        if normalized_state in {1, "ON"}:
            scpi_value = "ON"
        elif normalized_state in {0, "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":SENS:LIST:SEQ:AUTO {scpi_value}")

    def get_sense_list_sequence_auto(self) -> str:
        """Returns the auto state of the list sequence ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query(":SENS:LIST:SEQ:AUTO?").strip()
        if response == 1:
            return "ON"
        elif response == 0:
            return "OFF"
        else:
            return response.upper()

    def get_sense_list_sequence_points(self) -> int:
        """Returns the number of points currently in the SEQuence list."""
        response = self.instrument.query(":SENS:LIST:SEQ:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for list sequence points (not integer): '{response}'")

    
    def set_sense_mixer_bias(self, value: float):
        """Controls the mixer bias.
        Parameters:
        value: The bias value (numeric value)."""
        self.instrument.write(f":SENS:MIX:BIAS {value}")

    def get_sense_mixer_bias(self) -> float:
        """Returns the mixer bias."""
        response = self.instrument.query(":SENS:MIX:BIAS?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for mixer bias (not numeric): '{response}'")

    def set_sense_mixer_bias_auto(self, auto_state: str):
        """Allows the mixer bias to be automatically set by other parameters in the system.
        Parameters:
        auto_state: Boolean (ON|OFF) or 'ONCE'. Selecting 'ONCE' sets AUTO to ON and then OFF."""
        normalized_state = auto_state.upper()
        if normalized_state in {1, "ON"}:
            scpi_value = "ON"
        elif normalized_state in {0, "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":SENS:MIX:BIAS:AUTO {scpi_value}")

    def get_sense_mixer_bias_auto(self) -> str:
        """Returns the auto state of the mixer bias ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query(":SENS:MIX:BIAS:AUTO?").strip()
        if response == 1:
            return "ON"
        elif response == 0:
            return "OFF"
        else:
            return response.upper()

    def set_sense_mixer_bias_limit(self, value: float):
        """Controls the maximum mixer bias level.
        Parameters:
        value: The limit value (numeric value)."""
        self.instrument.write(f":SENS:MIX:BIAS:LIM {value}")

    def get_sense_mixer_bias_limit(self) -> float:
        """Returns the maximum mixer bias level."""
        response = self.instrument.query(":SENS:MIX:BIAS:LIM?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for mixer bias limit (not numeric): '{response}'")

    def set_sense_mixer_harmonic(self, value: int):
        """Selects which harmonic of the local oscillator will be used for mixing.
        Parameters:
        value: The harmonic number (numeric value)."""
        if not isinstance(value, int):
            raise ValueError("Harmonic must be an integer.")
        self.instrument.write(f":SENS:MIX:HARM {value}")

    def get_sense_mixer_harmonic(self) -> int:
        """Returns which harmonic of the local oscillator will be used for mixing."""
        response = self.instrument.query(":SENS:MIX:HARM?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for mixer harmonic (not integer): '{response}'")

    def set_sense_mixer_harmonic_auto(self, auto_state: str):
        """When AUTO is ON, the harmonic is chosen by the system or instrument.
        Parameters:
        auto_state: Boolean (ON|OFF) or 'ONCE'. Selecting 'ONCE' sets AUTO to ON and then OFF."""
        normalized_state = auto_state.upper()
        if normalized_state in {1, "ON"}:
            scpi_value = "ON"
        elif normalized_state in {0, "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":SENS:MIX:HARM:AUTO {scpi_value}")

    def get_sense_mixer_harmonic_auto(self) -> str:
        """Returns the auto state of the mixer harmonic ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query(":SENS:MIX:HARM:AUTO?").strip()
        if response == 1:
            return "ON"
        elif response == 0:
            return "OFF"
        else:
            return response.upper()

    
    def set_sense_mixer_loss(self, value: float):
        """Compensates for losses external to the instrument.
        Parameters:
        value: The loss value (numeric value) in current relative amplitude unit."""
        self.instrument.write(f":SENS:MIX:LOSS {value}")

    def get_sense_mixer_loss(self) -> float:
        """Returns the external loss compensation value."""
        response = self.instrument.query(":SENS:MIX:LOSS?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for mixer loss (not numeric): '{response}'")

    def set_sense_mixer_loss_auto(self, enable: bool):
        """Sets the LOSS to the value appropriate to the connected external mixer.
        Parameters:
        enable: True to enable auto-loss compensation, False to disable."""
        scpi_value = 1 if enable else 0
        self.instrument.write(f":SENS:MIX:LOSS:AUTO {scpi_value}")

    def get_sense_mixer_loss_auto(self) -> bool:
        """Returns True if auto-loss compensation is enabled, False if disabled."""
        response = self.instrument.query(":SENS:MIX:LOSS:AUTO?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for mixer loss auto state: '{response}'")

    
    def set_sense_pm_deviation_range_auto(self, auto_state: str):
        """Sets the range for the PM sensor function to a value determined to give the most dynamic range.
        Parameters:
        auto_state: Boolean (ON|OFF) or 'ONCE'. Selecting 'ONCE' sets AUTO to ON and then OFF."""
        normalized_state = auto_state.upper()
        if normalized_state in {1, "ON"}:
            scpi_value = "ON"
        elif normalized_state in {0, "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":SENS:PM:DEV:RANG:AUTO {scpi_value}")

    def get_sense_pm_deviation_range_auto(self) -> str:
        """Returns the auto state of the PM deviation range ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query(":SENS:PM:DEV:RANG:AUTO?").strip()
        if response == 1:
            return "ON"
        elif response == 0:
            return "OFF"
        else:
            return response.upper()

    def set_sense_pm_deviation_range_upper(self, value: float):
        """Specifies the maximum signal level expected for the PM sensor input.
        Parameters:
        value: The upper range value (numeric value)."""
        self.instrument.write(f":SENS:PM:DEV:RANG:UPP {value}")

    def get_sense_pm_deviation_range_upper(self) -> float:
        """Returns the maximum signal level expected for the PM sensor input."""
        response = self.instrument.query(":SENS:PM:DEV:RANG:UPP?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for PM deviation range upper (not numeric): '{response}'")

    def set_sense_pm_deviation_range_lower(self, value: float):
        """Specifies the smallest signal level expected for the PM sensor input.
        Parameters:
        value: The lower range value (numeric value)."""
        self.instrument.write(f":SENS:PM:DEV:RANG:LOW {value}")

    def get_sense_pm_deviation_range_lower(self) -> float:
        """Returns the smallest signal level expected for the PM sensor input."""
        response = self.instrument.query(":SENS:PM:DEV:RANG:LOW?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for PM deviation range lower (not numeric): '{response}'")

    
    def set_sense_power_achannel_spacing_lower(self, value: float):
        """Controls the channel spacing to the lower Adjacent Channel for Power.
        Parameters:
        value: The spacing value (numeric value)."""
        self.instrument.write(f":SENS:POW:ACH:SPAC:LOW {value}")

    def get_sense_power_achannel_spacing_lower(self) -> float:
        """Returns the channel spacing to the lower Adjacent Channel for Power."""
        response = self.instrument.query(":SENS:POW:ACH:SPAC:LOW?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for power ACHannel spacing lower (not numeric): '{response}'")

    
    def set_sense_power_achannel_spacing_lower_auto(self, enable: bool):
        """When AUTO is ON, the value of LOWer is coupled to the value of UPPER for Power Adjacent Channel Spacing.
        Parameters:
        enable: True to enable auto-coupling, False to disable."""
        scpi_value = 1 if enable else 0
        self.instrument.write(f":SENS:POW:ACH:SPAC:LOW:AUTO {scpi_value}")

    def get_sense_power_achannel_spacing_lower_auto(self) -> bool:
        """Returns True if the lower spacing is auto-coupled to upper for Power Adjacent Channel Spacing, False if disabled."""
        response = self.instrument.query(":SENS:POW:ACH:SPAC:LOW:AUTO?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for power ACHannel spacing lower auto state: '{response}'")

    def set_sense_power_achannel_spacing_upper(self, value: float):
        """Controls the channel spacing to the upper Adjacent Channel for Power.
        Parameters:
        value: The spacing value (numeric value)."""
        self.instrument.write(f":SENS:POW:ACH:SPAC:UPP {value}")

    def get_sense_power_achannel_spacing_upper(self) -> float:
        """Returns the channel spacing to the upper Adjacent Channel for Power."""
        response = self.instrument.query(":SENS:POW:ACH:SPAC:UPP?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for power ACHannel spacing upper (not numeric): '{response}'")

    def set_sense_power_ac_aperture(self, value: float):
        """Specifies the acquisition/sampling/gate time for a single measurement point for AC Power.
        Parameters:
        value: The aperture time in seconds (numeric value)."""
        self.instrument.write(f":SENS:POW:AC:APER {value}")

    def get_sense_power_ac_aperture(self) -> float:
        """Returns the acquisition/sampling/gate time for AC Power."""
        response = self.instrument.query(":SENS:POW:AC:APER?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for power AC aperture (not numeric): '{response}'")

    def set_sense_power_ac_nplcycles(self, value: float):
        """Specifies the acquisition/sampling/gate time for AC Power in terms of the number of power line cycles.
        Parameters:
        value: The number of power line cycles (numeric value)."""
        self.instrument.write(f":SENS:POW:AC:NPL {value}")

    def get_sense_power_ac_nplcycles(self) -> float:
        """Returns the acquisition/sampling/gate time for AC Power in terms of the number of power line cycles."""
        response = self.instrument.query(":SENS:POW:AC:NPL?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for power AC NPLCycles (not numeric): '{response}'")

    def set_sense_power_ac_attenuation(self, value: float):
        """Sets the attenuation level for AC Power.
        Parameters:
        value: The attenuation value (numeric value). Default units determined by UNITS system."""
        self.instrument.write(f":SENS:POW:AC:ATT {value}")

    def get_sense_power_ac_attenuation(self) -> float:
        """Returns the attenuation level for AC Power."""
        response = self.instrument.query(":SENS:POW:AC:ATT?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for power AC attenuation (not numeric): '{response}'")

    
    def set_sense_power_ac_attenuation_auto(self, enable: bool):
        """Couples the attenuator to RANGe for AC Power such that maximum dynamic range is assured.
        Parameters:
        enable: True to enable auto-attenuation, False to disable."""
        scpi_value = 1 if enable else 0
        self.instrument.write(f":SENS:POW:AC:ATT:AUTO {scpi_value}")

    def get_sense_power_ac_attenuation_auto(self) -> bool:
        """Returns True if auto-attenuation is enabled for AC Power, False if disabled."""
        response = self.instrument.query(":SENS:POW:AC:ATT:AUTO?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for power AC attenuation auto state: '{response}'")

    def set_sense_power_ac_protection_level(self, value: float):
        """Sets the input level at which the input protection circuit will trip for AC Power.
        Parameters:
        value: The trip level (numeric value)."""
        self.instrument.write(f":SENS:POW:AC:PROT:LEV {value}")

    def get_sense_power_ac_protection_level(self) -> float:
        """Returns the input level at which the input protection circuit will trip for AC Power."""
        response = self.instrument.query(":SENS:POW:AC:PROT:LEV?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for power AC protection level (not numeric): '{response}'")

    def set_sense_power_ac_protection_state(self, enable: bool):
        """Controls whether the input protection circuit is enabled for AC Power.
        Parameters:
        enable: True to enable, False to disable."""
        scpi_value = 1 if enable else 0
        self.instrument.write(f":SENS:POW:AC:PROT:STATE {scpi_value}")

    def get_sense_power_ac_protection_state(self) -> bool:
        """Returns True if the input protection circuit is enabled for AC Power, False if disabled."""
        response = self.instrument.query(":SENS:POW:AC:PROT:STATE?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for power AC protection state: '{response}'")

    def get_sense_power_ac_protection_tripped(self) -> bool:
        """Returns True if the protection circuit is tripped for AC Power, False if untripped.
        Notes: Query only."""
        response = self.instrument.query(":SENS:POW:AC:PROT:TRIP?").strip()
        if response == 1:
            return True
        elif response == 0:
            return False
        else:
            raise ValueError(f"Unexpected response for power AC protection tripped status: '{response}'")

    def clear_sense_power_ac_protection(self):
        """Causes the protection circuit to be cleared for AC Power.
        Notes: This is an event command; no query."""
        self.instrument.write(":SENS:POW:AC:PROT:CLE")

    
    def set_sense_power_ac_range_upper(self, value: float):
        """Specifies the most positive signal level expected for the AC Power sensor input.
        Parameters:
        value: The upper range value (numeric value)."""
        self.instrument.write(f":SENS:POW:AC:RANG:UPP {value}")

    def get_sense_power_ac_range_upper(self) -> float:
        """Returns the most positive signal level expected for the AC Power sensor input."""
        response = self.instrument.query(":SENS:POW:AC:RANG:UPP?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for power AC range upper (not numeric): '{response}'")

    def set_sense_power_ac_range_lower(self, value: float):
        """Specifies the most negative signal level expected for the AC Power sensor input.
        Parameters:
        value: The lower range value (numeric value)."""
        self.instrument.write(f":SENS:POW:AC:RANG:LOW {value}")

    def get_sense_power_ac_range_lower(self) -> float:
        """Returns the most negative signal level expected for the AC Power sensor input."""
        response = self.instrument.query(":SENS:POW:AC:RANG:LOW?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for power AC range lower (not numeric): '{response}'")

    def set_sense_power_ac_range_auto(self, auto_state: str):
        """Sets the range for AC Power to the value determined to give the most dynamic range.
        Parameters:
        auto_state: Boolean (ON|OFF) or 'ONCE'. Selecting 'ONCE' sets AUTO to ON and then OFF."""
        normalized_state = auto_state.upper()
        if normalized_state in {1, "ON"}:
            scpi_value = "ON"
        elif normalized_state in {0, "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":SENS:POW:AC:RANG:AUTO {scpi_value}")

    def get_sense_power_ac_range_auto(self) -> str:
        """Returns the auto state of the AC Power range ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query(":SENS:POW:AC:RANG:AUTO?").strip()
        if response == 1:
            return "ON"
        elif response == 0:
            return "OFF"
        else:
            return response.upper()

    def set_sense_power_ac_range_auto_direction(self, direction: str):
        """Defines the manner in which AUTO works for AC Power ranging.
        Parameters:
        direction: UP|DOWN|EITHer"""
        valid_directions = {"UP", "DOWN", "EITHER", "EITH"}
        direction_upper = direction.upper()
        if direction_upper not in valid_directions:
            raise ValueError(f"Invalid direction: '{direction}'. Must be 'UP', 'DOWN', or 'EITHer'.")

        if direction_upper == "EITHER": scpi_value = "EITH"
        else: scpi_value = direction_upper

        self.instrument.write(f":SENS:POW:AC:RANG:AUTO:DIR {scpi_value}")

    def get_sense_power_ac_range_auto_direction(self) -> str:
        """Returns the auto-ranging direction for AC Power ('UP', 'DOWN', or 'EITHER')."""
        response = self.instrument.query(":SENS:POW:AC:RANG:AUTO:DIR?").strip().upper()
        if response.startswith("EITH"):
            return "EITHER"
        return response

    def set_sense_power_ac_range_auto_llimit(self, value: float):
        """Sets the smallest range to which the instrument will go while auto-ranging for AC Power.
        Parameters:
        value: The lower limit (numeric value)."""
        self.instrument.write(f":SENS:POW:AC:RANG:AUTO:LLIM {value}")

    def get_sense_power_ac_range_auto_llimit(self) -> float:
        """Returns the smallest range to which the instrument will go while auto-ranging for AC Power."""
        response = self.instrument.query(":SENS:POW:AC:RANG:AUTO:LLIM?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for power AC range auto lower limit (not numeric): '{response}'")

    def set_sense_power_ac_range_auto_ulimit(self, value: float):
        """Sets the largest range to which the instrument will go while auto-ranging for AC Power.
        Parameters:
        value: The upper limit (numeric value)."""
        self.instrument.write(f":SENS:POW:AC:RANG:AUTO:ULIM {value}")

    def get_sense_power_ac_range_auto_ulimit(self) -> float:
        """Returns the largest range to which the instrument will go while auto-ranging for AC Power."""
        response = self.instrument.query(":SENS:POW:AC:RANG:AUTO:ULIM?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for power AC range auto upper limit (not numeric): '{response}'")

    
    def set_sense_power_ac_range_offset(self, value: float):
        """Determines the midpoint of the range for AC Power.
        Parameters:
        value: The offset value (numeric value)."""
        self.instrument.write(f":SENS:POW:AC:RANG:OFFS {value}")

    def get_sense_power_ac_range_offset(self) -> float:
        """Returns the midpoint of the range for AC Power."""
        response = self.instrument.query(":SENS:POW:AC:RANG:OFFS?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for power AC range offset (not numeric): '{response}'")

    def set_sense_power_ac_range_ptpeak(self, value: float):
        """Specifies the dynamic range required for the AC Power sensor (Peak To Peak).
        Parameters:
        value: The peak-to-peak value (numeric value)."""
        self.instrument.write(f":SENS:POW:AC:RANG:PTP {value}")

    def get_sense_power_ac_range_ptpeak(self) -> float:
        """Returns the dynamic range required for the AC Power sensor (Peak To Peak)."""
        response = self.instrument.query(":SENS:POW:AC:RANG:PTP?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for power AC range PTPeak (not numeric): '{response}'")

    def set_sense_power_ac_reference(self, value: float):
        """Sets a reference amplitude for AC Power sensor instruments.
        Parameters:
        value: The reference amplitude (numeric value)."""
        self.instrument.write(f":SENS:POW:AC:REF {value}")

    def get_sense_power_ac_reference(self) -> float:
        """Returns the reference amplitude for AC Power sensor instruments."""
        response = self.instrument.query(":SENS:POW:AC:REF?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for power AC reference (not numeric): '{response}'")

    def set_sense_power_ac_reference_state(self, enable: bool):
        """Determines whether amplitude is measured in absolute or relative mode for AC Power.
        Parameters:
        enable: True to reference to the value set in REFerence, False for absolute mode."""
        scpi_value = 1 if enable else 0
        self.instrument.write(f":SENS:POW:AC:REF:STATE {scpi_value}")

    def get_sense_power_ac_reference_state(self) -> bool:
        """Returns True if amplitude is measured in relative mode for AC Power, False for absolute mode."""
        response = self.instrument.query(":SENS:POW:AC:REF:STATE?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for power AC reference state: '{response}'")

    def set_sense_power_ac_resolution(self, value: float):
        """Specifies the absolute resolution of the AC Power measurement.
        Parameters:
        value: The resolution value (numeric value)."""
        self.instrument.write(f":SENS:POW:AC:RES {value}")

    def get_sense_power_ac_resolution(self) -> float:
        """Returns the absolute resolution of the AC Power measurement."""
        response = self.instrument.query(":SENS:POW:AC:RES?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for power AC resolution (not numeric): '{response}'")

    def set_sense_power_ac_resolution_auto(self, auto_state: str):
        """Allows the system to determine the best resolution for the other measurement conditions for AC Power.
        Parameters:
        auto_state: Boolean (ON|OFF) or 'ONCE'. Selecting 'ONCE' sets AUTO to ON and then OFF."""
        normalized_state = auto_state.upper()
        if normalized_state in {1, "ON"}:
            scpi_value = "ON"
        elif normalized_state in {0, "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":SENS:POW:AC:RES:AUTO {scpi_value}")

    def get_sense_power_ac_resolution_auto(self) -> str:
        """Returns the auto state of the AC Power resolution ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query(":SENS:POW:AC:RES:AUTO?").strip()
        if response == 1:
            return "ON"
        elif response == 0:
            return "OFF"
        else:
            return response.upper()

    
    def set_sense_power_detector(self, detector_type: str):
        """Specifies the detector for Power as internal or external.
        Parameters:
        detector_type: INTernal|EXTernal"""
        valid_types = {"INTERNAL", "EXTERNAL", "INT", "EXT"}
        type_upper = detector_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid detector type: '{detector_type}'. Must be 'INTernal' or 'EXTernal'.")

        if type_upper == "INTERNAL": scpi_value = "INT"
        elif type_upper == "EXTERNAL": scpi_value = "EXT"
        else: scpi_value = type_upper

        self.instrument.write(f":SENS:POW:DET {scpi_value}")

    def get_sense_power_detector(self) -> str:
        """Returns the detector type for Power ('INTERNAL' or 'EXTERNAL')."""
        response = self.instrument.query(":SENS:POW:DET?").strip().upper()
        if response.startswith("INT"):
            return "INTERNAL"
        elif response.startswith("EXT"):
            return "EXTERNAL"
        return response

        # Resistance / Four-wire Resistance (FRESistance) Subsystem

    def set_sense_resistance_aperture(self, value: float):
        """Specifies the acquisition/sampling/gate time for a single measurement point for Resistance.
        Parameters:
        value: The aperture time in seconds (numeric value)."""
        self.instrument.write(f":SENS:RES:APER {value}")

    def get_sense_resistance_aperture(self) -> float:
        """Returns the acquisition/sampling/gate time for Resistance."""
        response = self.instrument.query(":SENS:RES:APER?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for resistance aperture (not numeric): '{response}'")

    def set_sense_resistance_nplcycles(self, value: float):
        """Specifies the acquisition/sampling/gate time for Resistance in terms of the number of power line cycles.
        Parameters:
        value: The number of power line cycles (numeric value)."""
        self.instrument.write(f":SENS:RES:NPL {value}")

    def get_sense_resistance_nplcycles(self) -> float:
        """Returns the acquisition/sampling/gate time for Resistance in terms of the number of power line cycles."""
        response = self.instrument.query(":SENS:RES:NPL?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for resistance NPLCycles (not numeric): '{response}'")

    def set_sense_resistance_ocompensated(self, enable: bool):
        """Enables or disables the offset compensation when measuring resistance.
        Parameters:
        enable: True to enable, False to disable."""
        scpi_value = 1 if enable else 0
        self.instrument.write(f":SENS:RES:OCOM {scpi_value}")

    def get_sense_resistance_ocompensated(self) -> bool:
        """Returns: True if offset compensation is enabled for Resistance, False if disabled."""
        response = self.instrument.query(":SENS:RES:OCOM?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for resistance OCOMPensated state: '{response}'")

    
    def set_sense_resistance_range_upper(self, value: float):
        """Specifies the maximum resistance expected for the Resistance sensor input.
        Parameters:
        value: The upper range value (numeric value)."""
        self.instrument.write(f":SENS:RES:RANG:UPP {value}")

    def get_sense_resistance_range_upper(self) -> float:
        """Returns the maximum resistance expected for the Resistance sensor input."""
        response = self.instrument.query(":SENS:RES:RANG:UPP?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for resistance range upper (not numeric): '{response}'")

    def set_sense_resistance_range_lower(self, value: float):
        """Specifies the smallest resistance expected for the Resistance sensor input.
        Parameters:
        value: The lower range value (numeric value)."""
        self.instrument.write(f":SENS:RES:RANG:LOW {value}")

    def get_sense_resistance_range_lower(self) -> float:
        """Returns the smallest resistance expected for the Resistance sensor input."""
        response = self.instrument.query(":SENS:RES:RANG:LOW?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for resistance range lower (not numeric): '{response}'")

    def set_sense_resistance_range_auto(self, auto_state: str):
        """Sets the range for Resistance to the value determined to give the most dynamic range.
        Parameters:
        auto_state: Boolean (ON|OFF) or 'ONCE'. Selecting 'ONCE' sets AUTO to ON and then OFF."""
        normalized_state = auto_state.upper()
        if normalized_state in {1, "ON"}:
            scpi_value = "ON"
        elif normalized_state in {0, "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":SENS:RES:RANG:AUTO {scpi_value}")

    def get_sense_resistance_range_auto(self) -> str:
        """Returns the auto state of the Resistance range ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query(":SENS:RES:RANG:AUTO?").strip()
        if response == 1:
            return "ON"
        elif response == 0:
            return "OFF"
        else:
            return response.upper()

    def set_sense_resistance_range_auto_direction(self, direction: str):
        """Defines the manner in which AUTO works for Resistance ranging.
        Parameters:
        direction: UP|DOWN|EITHer"""
        valid_directions = {"UP", "DOWN", "EITHER", "EITH"}
        direction_upper = direction.upper()
        if direction_upper not in valid_directions:
            raise ValueError(f"Invalid direction: '{direction}'. Must be 'UP', 'DOWN', or 'EITHer'.")

        if direction_upper == "EITHER": scpi_value = "EITH"
        else: scpi_value = direction_upper

        self.instrument.write(f":SENS:RES:RANG:AUTO:DIR {scpi_value}")

    def get_sense_resistance_range_auto_direction(self) -> str:
        """Returns the auto-ranging direction for Resistance ('UP', 'DOWN', or 'EITHER')."""
        response = self.instrument.query(":SENS:RES:RANG:AUTO:DIR?").strip().upper()
        if response.startswith("EITH"):
            return "EITHER"
        return response

    def set_sense_resistance_range_auto_llimit(self, value: float):
        """Sets the smallest range to which the instrument will go while auto-ranging for Resistance.
        Parameters:
        value: The lower limit (numeric value)."""
        self.instrument.write(f":SENS:RES:RANG:AUTO:LLIM {value}")

    def get_sense_resistance_range_auto_llimit(self) -> float:
        """Returns the smallest range to which the instrument will go while auto-ranging for Resistance."""
        response = self.instrument.query(":SENS:RES:RANG:AUTO:LLIM?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for resistance range auto lower limit (not numeric): '{response}'")

    def set_sense_resistance_range_auto_ulimit(self, value: float):
        """Sets the largest range to which the instrument will go while auto-ranging for Resistance.
        Parameters:
        value: The upper limit (numeric value)."""
        self.instrument.write(f":SENS:RES:RANG:AUTO:ULIM {value}")

    def get_sense_resistance_range_auto_ulimit(self) -> float:
        """Returns the largest range to which the instrument will go while auto-ranging for Resistance."""
        response = self.instrument.query(":SENS:RES:RANG:AUTO:ULIM?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for resistance range auto upper limit (not numeric): '{response}'")

    
    def set_sense_resistance_reference(self, value: float):
        """Sets a reference resistance for sensor instruments.
        Parameters:
        value: The reference resistance (numeric value)."""
        self.instrument.write(f":SENS:RES:REF {value}")

    def get_sense_resistance_reference(self) -> float:
        """Returns the reference resistance for sensor instruments."""
        response = self.instrument.query(":SENS:RES:REF?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for resistance reference (not numeric): '{response}'")

    def set_sense_resistance_reference_state(self, enable: bool):
        """Determines whether resistance is measured in absolute or relative mode.
        Parameters:
        enable: True to reference to the value set in REFerence, False for absolute mode."""
        scpi_value = 1 if enable else 0
        self.instrument.write(f":SENS:RES:REF:STATE {scpi_value}")

    def get_sense_resistance_reference_state(self) -> bool:
        """Returns True if resistance is measured in relative mode, False for absolute mode."""
        response = self.instrument.query(":SENS:RES:REF:STATE?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for resistance reference state: '{response}'")

    def set_sense_resistance_resolution(self, value: float):
        """Specifies the absolute resolution of the Resistance measurement.
        Parameters:
        value: The resolution value (numeric value)."""
        self.instrument.write(f":SENS:RES:RES {value}")

    def get_sense_resistance_resolution(self) -> float:
        """Returns the absolute resolution of the Resistance measurement."""
        response = self.instrument.query(":SENS:RES:RES?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for resistance resolution (not numeric): '{response}'")

    def set_sense_resistance_resolution_auto(self, auto_state: str):
        """Allows the system to determine the best resolution for the other measurement conditions.
        Parameters:
        auto_state: Boolean (ON|OFF) or 'ONCE'. Selecting 'ONCE' sets AUTO to ON and then OFF."""
        normalized_state = auto_state.upper()
        if normalized_state in {1, "ON"}:
            scpi_value = "ON"
        elif normalized_state in {0, "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":SENS:RES:RES:AUTO {scpi_value}")

    def get_sense_resistance_resolution_auto(self) -> str:
        """Returns the auto state of the Resistance resolution ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query(":SENS:RES:RES:AUTO?").strip()
        if response == 1:
            return "ON"
        elif response == 0:
            return "OFF"
        else:
            return response.upper()

    
    def set_sense_roscillator_internal_frequency(self, frequency_hz: float):
        """Specifies the frequency of the internal reference oscillator in Hz.
        Parameters:
        frequency_hz: The frequency in Hz (numeric value)."""
        self.instrument.write(f":SENS:ROSC:INT:FREQ {frequency_hz}")

    def get_sense_roscillator_internal_frequency(self) -> float:
        """Returns the frequency of the internal reference oscillator in Hz."""
        response = self.instrument.query(":SENS:ROSC:INT:FREQ?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for roscillator internal frequency (not numeric): '{response}'")

    def set_sense_roscillator_external_frequency(self, frequency_hz: float):
        """Specifies the frequency of the external reference oscillator in Hz.
        Parameters:
        frequency_hz: The frequency in Hz (numeric value)."""
        self.instrument.write(f":SENS:ROSC:EXT:FREQ {frequency_hz}")

    def get_sense_roscillator_external_frequency(self) -> float:
        """Returns the frequency of the external reference oscillator in Hz."""
        response = self.instrument.query(":SENS:ROSC:EXT:FREQ?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for roscillator external frequency (not numeric): '{response}'")

    def set_sense_roscillator_source(self, source_type: str):
        """Controls the selection of the reference oscillator source.
        Parameters:
        source_type: INTernal|EXTernal|NONE|CLK10|CLK100"""
        valid_types = {"INTERNAL", "EXTERNAL", "NONE", "CLK10", "CLK100", "INT", "EXT"}
        type_upper = source_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid source type: '{source_type}'.")

        if type_upper == "INTERNAL": scpi_value = "INT"
        elif type_upper == "EXTERNAL": scpi_value = "EXT"
        else: scpi_value = type_upper

        self.instrument.write(f":SENS:ROSC:SOUR {scpi_value}")

    def get_sense_roscillator_source(self) -> str:
        """Returns the selected reference oscillator source ('INTERNAL', 'EXTERNAL', 'NONE', 'CLK10', or 'CLK100')."""
        response = self.instrument.query(":SENS:ROSC:SOUR?").strip().upper()
        if response.startswith("INT"): return "INTERNAL"
        elif response.startswith("EXT"): return "EXTERNAL"
        elif response.startswith("NONE"): return "NONE"
        elif response.startswith("CLK10"): return "CLK10"
        elif response.startswith("CLK100"): return "CLK100"
        return response

    
    def set_sense_roscillator_source_auto(self, auto_state: str):
        """When AUTO is ON, the system automatically selects which oscillator will be used by the instrument.
        Parameters:
        auto_state: Boolean (ON|OFF) or 'ONCE'. Selecting 'ONCE' sets AUTO to ON and then OFF."""
        normalized_state = auto_state.upper()
        if normalized_state in {1, "ON"}:
            scpi_value = "ON"
        elif normalized_state in {0, "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":SENS:ROSC:SOUR:AUTO {scpi_value}")

    def get_sense_roscillator_source_auto(self) -> str:
        """Returns the auto state of the reference oscillator source ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query(":SENS:ROSC:SOUR:AUTO?").strip()
        if response == 1:
            return "ON"
        elif response == 0:
            return "OFF"
        else:
            return response.upper()

    
    def set_sense_smoothing_state(self, enable: bool):
        """Determines whether the smoothing algorithm is enabled.
        Parameters:
        enable: True to enable, False to disable."""
        scpi_value = 1 if enable else 0
        self.instrument.write(f":SENS:SMO:STATE {scpi_value}")

    def get_sense_smoothing_state(self) -> bool:
        """Returns True if the smoothing algorithm is enabled, False if disabled."""
        response = self.instrument.query(":SENS:SMO:STATE?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for smoothing state: '{response}'")

    def set_sense_smoothing_aperture(self, value: float):
        """Specifies the size of the smoothing APERture as a ratio of smoothing window points/trace points.
        Parameters:
        value: The aperture ratio (numeric value)."""
        self.instrument.write(f":SENS:SMO:APER {value}")

    def get_sense_smoothing_aperture(self) -> float:
        """Returns the size of the smoothing APERture."""
        response = self.instrument.query(":SENS:SMO:APER?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for smoothing aperture (not numeric): '{response}'")

    def set_sense_smoothing_points(self, value: int):
        """Controls the number of points to be included in the running average.
        Parameters:
        value: The number of points (numeric value)."""
        if not isinstance(value, int) or value < 1:
            raise ValueError("Points must be a positive integer.")
        self.instrument.write(f":SENS:SMO:POIN {value}")

    def get_sense_smoothing_points(self) -> int:
        """Returns the number of points to be included in the running average."""
        response = self.instrument.query(":SENS:SMO:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for smoothing points (not integer): '{response}'")

    
    def set_sense_ssb_type(self, ssb_type: str):
        """Sets or queries the type of SSB demodulation technique the demodulator uses.
        Parameters:
        ssb_type: USB|LSB|A1"""
        valid_types = {"USB", "LSB", "A1"}
        type_upper = ssb_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid SSB type: '{ssb_type}'. Must be 'USB', 'LSB', or 'A1'.")
        self.instrument.write(f":SENS:SSB:TYPE {type_upper}")

    def get_sense_ssb_type(self) -> str:
        """Returns the type of SSB demodulation technique ('USB', 'LSB', or 'A1')."""
        response = self.instrument.query(":SENS:SSB:TYPE?").strip().upper()
        return response

    
    def set_sense_stabilize_ntolerance(self, value_percent_fs: float):
        """Specifies the allowable tolerance between averaged readings for a stabilized read, in percentage of full scale (%FS).
        Parameters:
        value_percent_fs: The tolerance value (numeric value)."""
        self.instrument.write(f":SENS:STAB:NTOL {value_percent_fs}")

    def get_sense_stabilize_ntolerance(self) -> float:
        """Returns the allowable tolerance between averaged readings for a stabilized read in percentage of full scale (%FS)."""
        response = self.instrument.query(":SENS:STAB:NTOL?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for stabilize NTOLerance (not numeric): '{response}'")

    def set_sense_stabilize_state(self, enable: bool):
        """Sets or queries the stabilization state for all sensors.
        Parameters:
        enable: True to enable stabilization, False to disable."""
        scpi_value = 1 if enable else 0
        self.instrument.write(f":SENS:STAB:STATE {scpi_value}")

    def get_sense_stabilize_state(self) -> bool:
        """Returns True if stabilization is enabled, False if disabled."""
        response = self.instrument.query(":SENS:STAB:STATE?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for stabilize state: '{response}'")

    
    def set_sense_stabilize_time_n(self, time_index: int, value_seconds: float):
        """Sets the nth time parameter for the stabilization procedure.
        Parameters:
        time_index: The time parameter index (1, 2, 3, or 4).
        value_seconds: The time in seconds (numeric value)."""
        if time_index not in {1, 2, 3, 4}:
            raise ValueError("Time index must be 1, 2, 3, or 4.")
        self.instrument.write(f":SENS:STAB:TIME{time_index} {value_seconds}")

    def get_sense_stabilize_time_n(self, time_index: int) -> float:
        """Returns the nth time parameter for the stabilization procedure in seconds."""
        if time_index not in {1, 2, 3, 4}:
            raise ValueError("Time index must be 1, 2, 3, or 4.")
        response = self.instrument.query(f":SENS:STAB:TIME{time_index}?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for stabilize TIME{time_index} (not numeric): '{response}'")

    
    def set_sense_sweep_count(self, value: int):
        """Determines the number of sweeps initiated or vectors acquired by a single trigger event.
        Parameters:
        value: The count (numeric value)."""
        if not isinstance(value, int) or value < 1:
            raise ValueError("Count must be a positive integer.")
        self.instrument.write(f":SENS:SWE:COUN {value}")

    def get_sense_sweep_count(self) -> int:
        """Returns the number of sweeps initiated or vectors acquired by a single trigger event."""
        response = self.instrument.query(":SENS:SWE:COUN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for sweep count (not integer): '{response}'")

    def set_sense_sweep_direction(self, direction: str):
        """Controls the direction of the sweep.
        Parameters:
        direction: UP|DOWN"""
        valid_directions = {"UP", "DOWN"}
        direction_upper = direction.upper()
        if direction_upper not in valid_directions:
            raise ValueError(f"Invalid direction: '{direction}'. Must be 'UP' or 'DOWN'.")
        self.instrument.write(f":SENS:SWE:DIR {direction_upper}")

    def get_sense_sweep_direction(self) -> str:
        """Returns the direction of the sweep ('UP' or 'DOWN')."""
        response = self.instrument.query(":SENS:SWE:DIR?").strip().upper()
        return response

    def set_sense_sweep_dwell(self, value_seconds: float):
        """Controls the amount of time spent at each point during a sweep in seconds.
        Parameters:
        value_seconds: The dwell time in seconds (numeric value)."""
        self.instrument.write(f":SENS:SWE:DWEL {value_seconds}")

    def get_sense_sweep_dwell(self) -> float:
        """Returns the amount of time spent at each point during a sweep in seconds."""
        response = self.instrument.query(":SENS:SWE:DWEL?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for sweep dwell (not numeric): '{response}'")

    
    def set_sense_sweep_dwell_auto(self, auto_state: str):
        """When ON is selected, the dwell time is calculated internally when SWEep:TINTerval is changed.
        Parameters:
        auto_state: Boolean (ON|OFF) or 'ONCE'. Selecting 'ONCE' sets AUTO to ON and then OFF."""
        normalized_state = auto_state.upper()
        if normalized_state in {1, "ON"}:
            scpi_value = "ON"
        elif normalized_state in {0, "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":SENS:SWE:DWEL:AUTO {scpi_value}")

    def get_sense_sweep_dwell_auto(self) -> str:
        """Returns the auto state of the sweep dwell time ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query(":SENS:SWE:DWEL:AUTO?").strip()
        if response == 1:
            return "ON"
        elif response == 0:
            return "OFF"
        else:
            return response.upper()

    def set_sense_sweep_generation(self, generation_type: str):
        """Determines if the sweep or acquisition is stepped or analog.
        Parameters:
        generation_type: STEPped|ANALog"""
        valid_types = {"STEPPED", "ANALOG", "STEP", "ANAL"}
        type_upper = generation_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid generation type: '{generation_type}'. Must be 'STEPped' or 'ANALog'.")

        if type_upper == "STEPPED": scpi_value = "STEP"
        elif type_upper == "ANALOG": scpi_value = "ANAL"
        else: scpi_value = type_upper

        self.instrument.write(f":SENS:SWE:GEN {scpi_value}")

    def get_sense_sweep_generation(self) -> str:
        """Returns whether the sweep or acquisition is stepped or analog ('STEPPED' or 'ANALOG')."""
        response = self.instrument.query(":SENS:SWE:GEN?").strip().upper()
        if response.startswith("STEP"):
            return "STEPPED"
        elif response.startswith("ANAL"):
            return "ANALOG"
        return response

    def set_sense_sweep_mode(self, mode_type: str):
        """Determines whether the sweep is performed automatically, or if the actual swept entity is controlled manually.
        Parameters:
        mode_type: AUTO|MANual"""
        valid_types = {"AUTO", "MANUAL", "MAN"}
        type_upper = mode_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid sweep mode: '{mode_type}'. Must be 'AUTO' or 'MANual'.")

        if type_upper == "MANUAL": scpi_value = "MAN"
        else: scpi_value = type_upper

        self.instrument.write(f":SENS:SWE:MODE {scpi_value}")

    def get_sense_sweep_mode(self) -> str:
        """Returns whether the sweep is performed automatically or manually ('AUTO' or 'MANUAL')."""
        response = self.instrument.query(":SENS:SWE:MODE?").strip().upper()
        if response.startswith("MAN"):
            return "MANUAL"
        return response

    def set_sense_sweep_offset_points(self, value: int):
        """Sets the offset in terms of points between the offset reference point and the trigger point.
        Parameters:
        value: The offset in points (numeric value)."""
        if not isinstance(value, int):
            raise ValueError("Offset points must be an integer.")
        self.instrument.write(f":SENS:SWE:OFFS:POIN {value}")

    def get_sense_sweep_offset_points(self) -> int:
        """Returns the offset in terms of points."""
        response = self.instrument.query(":SENS:SWE:OFFS:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for sweep offset points (not integer): '{response}'")

    def set_sense_sweep_offset_time(self, value_seconds: float):
        """Sets the offset in units of time between the offset reference point and the trigger point.
        Parameters:
        value_seconds: The offset time in seconds (numeric value)."""
        self.instrument.write(f":SENS:SWE:OFFS:TIME {value_seconds}")

    def get_sense_sweep_offset_time(self) -> float:
        """Returns the offset in units of time."""
        response = self.instrument.query(":SENS:SWE:OFFS:TIME?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for sweep offset time (not numeric): '{response}'")

    
    def set_sense_sweep_oreference_location(self, value: float):
        """Sets the offset reference by specifying a relative location (0 to 1).
        Parameters:
        value: The location (numeric value). 0 for first point, 1 for last point."""
        if not (0 <= value <= 1):
            raise ValueError("Location must be between 0 and 1.")
        self.instrument.write(f":SENS:SWE:OREF:LOC {value}")

    def get_sense_sweep_oreference_location(self) -> float:
        """Returns the relative location of the offset reference point."""
        response = self.instrument.query(":SENS:SWE:OREF:LOC?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for sweep OReference location (not numeric): '{response}'")

    def set_sense_sweep_oreference_points(self, value: int):
        """Sets the offset reference by specifying a number of points (1 to N, where N is max SWEep:POINts).
        Parameters:
        value: The number of points (numeric value)."""
        if not isinstance(value, int) or value < 1:
            raise ValueError("Points must be a positive integer.")
        self.instrument.write(f":SENS:SWE:OREF:POIN {value}")

    def get_sense_sweep_oreference_points(self) -> int:
        """Returns the number of points for the offset reference."""
        response = self.instrument.query(":SENS:SWE:OREF:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for sweep OReference points (not integer): '{response}'")

    def set_sense_sweep_points(self, value: int):
        """Sets the number of points in a stepped sweep or acquisition.
        Parameters:
        value: The number of points (numeric value)."""
        if not isinstance(value, int) or value < 1:
            raise ValueError("Points must be a positive integer.")
        self.instrument.write(f":SENS:SWE:POIN {value}")

    def get_sense_sweep_points(self) -> int:
        """Returns the number of points in a stepped sweep or acquisition."""
        response = self.instrument.query(":SENS:SWE:POIN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for sweep points (not integer): '{response}'")

    
    def set_sense_sweep_realtime_state(self, enable: bool):
        """When STATE is ON, the instrument is required to collect data in real time.
        Parameters:
        enable: True for real time, False to allow reconstruction techniques."""
        scpi_value = 1 if enable else 0
        self.instrument.write(f":SENS:SWE:REAL:STATE {scpi_value}")

    def get_sense_sweep_realtime_state(self) -> bool:
        """Returns True if real time data collection is enabled, False if not."""
        response = self.instrument.query(":SENS:SWE:REAL:STATE?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for sweep real time state: '{response}'")

    def set_sense_sweep_spacing(self, spacing_type: str):
        """Determines the time vs. swept entity characteristics of the sweep.
        Parameters:
        spacing_type: LINear|LOGarithmic"""
        valid_types = {"LINEAR", "LOGARITHMIC", "LIN", "LOG"}
        type_upper = spacing_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid spacing type: '{spacing_type}'. Must be 'LINear' or 'LOGarithmic'.")

        if type_upper == "LINEAR": scpi_value = "LIN"
        elif type_upper == "LOGARITHMIC": scpi_value = "LOG"
        else: scpi_value = type_upper

        self.instrument.write(f":SENS:SWE:SPAC {scpi_value}")

    def get_sense_sweep_spacing(self) -> str:
        """Returns the time vs. swept entity characteristics of the sweep ('LINEAR' or 'LOGARITHMIC')."""
        response = self.instrument.query(":SENS:SWE:SPAC?").strip().upper()
        if response.startswith("LIN"):
            return "LINEAR"
        elif response.startswith("LOG"):
            return "LOGARITHMIC"
        return response

    
    def set_sense_sweep_step(self, value: float):
        """Controls the swept entity step size for a stepped linear sweep.
        Parameters:
        value: The step size (numeric value). Default units are those of the associated <swept_subsystem>:SPAN command."""
        self.instrument.write(f":SENS:SWE:STEP {value}")

    def get_sense_sweep_step(self) -> float:
        """Returns the swept entity step size for a stepped linear sweep."""
        response = self.instrument.query(":SENS:SWE:STEP?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for sweep step (not numeric): '{response}'")

    def set_sense_sweep_time(self, value_seconds: float):
        """Sets the duration of the sweep or acquisition in seconds.
        Parameters:
        value_seconds: The duration in seconds (numeric value)."""
        self.instrument.write(f":SENS:SWE:TIME {value_seconds}")

    def get_sense_sweep_time(self) -> float:
        """Returns the duration of the sweep or acquisition in seconds."""
        response = self.instrument.query(":SENS:SWE:TIME?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for sweep time (not numeric): '{response}'")

    
    def set_sense_sweep_time_auto(self, auto_state: str):
        """When ON is selected, SWEep:TIME and SWEep:TINTerval are calculated internally.
        Parameters:
        auto_state: Boolean (ON|OFF) or 'ONCE'. Selecting 'ONCE' sets AUTO to ON and then OFF."""
        normalized_state = auto_state.upper()
        if normalized_state in {1, "ON"}:
            scpi_value = "ON"
        elif normalized_state in {0, "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":SENS:SWE:TIME:AUTO {scpi_value}")

    def get_sense_sweep_time_auto(self) -> str:
        """Returns the auto state of the sweep time ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query(":SENS:SWE:TIME:AUTO?").strip()
        if response == 1:
            return "ON"
        elif response == 0:
            return "OFF"
        else:
            return response.upper()

    def set_sense_sweep_time_llimit(self, value: float):
        """Defines a lower limit for sweep time.
        Parameters:
        value: The lower limit (numeric value)."""
        self.instrument.write(f":SENS:SWE:TIME:LLIM {value}")

    def get_sense_sweep_time_llimit(self) -> float:
        """Returns the lower limit for sweep time."""
        response = self.instrument.query(":SENS:SWE:TIME:LLIM?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for sweep time lower limit (not numeric): '{response}'")

    def set_sense_sweep_tinterval(self, value_seconds: float):
        """Sets the time interval between points of the sweep or acquisition in seconds.
        Parameters:
        value_seconds: The time interval in seconds (numeric value)."""
        self.instrument.write(f":SENS:SWE:TINT {value_seconds}")

    def get_sense_sweep_tinterval(self) -> float:
        """Returns the time interval between points of the sweep or acquisition in seconds."""
        response = self.instrument.query(":SENS:SWE:TINT?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for sweep time interval (not numeric): '{response}'")

    
    def set_sense_voltage_ac_aperture(self, value: float):
        """Specifies the acquisition/sampling/gate time for a single measurement point for AC Voltage.
        Parameters:
        value: The aperture time in seconds (numeric value)."""
        self.instrument.write(f":SENS:VOLT:AC:APER {value}")

    def get_sense_voltage_ac_aperture(self) -> float:
        """Returns the acquisition/sampling/gate time for AC Voltage."""
        response = self.instrument.query(":SENS:VOLT:AC:APER?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for voltage AC aperture (not numeric): '{response}'")

    def set_sense_voltage_ac_nplcycles(self, value: float):
        """Specifies the acquisition/sampling/gate time for AC Voltage in terms of the number of power line cycles.
        Parameters:
        value: The number of power line cycles (numeric value)."""
        self.instrument.write(f":SENS:VOLT:AC:NPL {value}")

    def get_sense_voltage_ac_nplcycles(self) -> float:
        """Returns the acquisition/sampling/gate time for AC Voltage in terms of the number of power line cycles."""
        response = self.instrument.query(":SENS:VOLT:AC:NPL?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for voltage AC NPLCycles (not numeric): '{response}'")

    def set_sense_voltage_ac_attenuation(self, value: float):
        """Sets the attenuation level for AC Voltage.
        Parameters:
        value: The attenuation value (numeric value). Default units determined by UNITS system."""
        self.instrument.write(f":SENS:VOLT:AC:ATT {value}")

    def get_sense_voltage_ac_attenuation(self) -> float:
        """Returns the attenuation level for AC Voltage."""
        response = self.instrument.query(":SENS:VOLT:AC:ATT?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for voltage AC attenuation (not numeric): '{response}'")

    
    def set_sense_voltage_ac_attenuation_auto(self, enable: bool):
        """Couples the attenuator to RANGe for AC Voltage such that maximum dynamic range is assured.
        Parameters:
        enable: True to enable auto-attenuation, False to disable."""
        scpi_value = 1 if enable else 0
        self.instrument.write(f":SENS:VOLT:AC:ATT:AUTO {scpi_value}")

    def get_sense_voltage_ac_attenuation_auto(self) -> bool:
        """Returns True if auto-attenuation is enabled for AC Voltage, False if disabled."""
        response = self.instrument.query(":SENS:VOLT:AC:ATT:AUTO?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for voltage AC attenuation auto state: '{response}'")

    def set_sense_voltage_ac_protection_level(self, value: float):
        """Sets the input level at which the input protection circuit will trip for AC Voltage.
        Parameters:
        value: The trip level (numeric value)."""
        self.instrument.write(f":SENS:VOLT:AC:PROT:LEV {value}")

    def get_sense_voltage_ac_protection_level(self) -> float:
        """Returns the input level at which the input protection circuit will trip for AC Voltage."""
        response = self.instrument.query(":SENS:VOLT:AC:PROT:LEV?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for voltage AC protection level (not numeric): '{response}'")

    def set_sense_voltage_ac_protection_state(self, enable: bool):
        """Controls whether the input protection circuit is enabled for AC Voltage.
        Parameters:
        enable: True to enable, False to disable."""
        scpi_value = 1 if enable else 0
        self.instrument.write(f":SENS:VOLT:AC:PROT:STATE {scpi_value}")

    def get_sense_voltage_ac_protection_state(self) -> bool:
        """Returns True if the input protection circuit is enabled for AC Voltage, False if disabled."""
        response = self.instrument.query(":SENS:VOLT:AC:PROT:STATE?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for voltage AC protection state: '{response}'")

    def get_sense_voltage_ac_protection_tripped(self) -> bool:
        """Returns True if the protection circuit is tripped for AC Voltage, False if untripped.
        Notes: Query only."""
        response = self.instrument.query(":SENS:VOLT:AC:PROT:TRIP?").strip()
        if response == 1:
            return True
        elif response == 0:
            return False
        else:
            raise ValueError(f"Unexpected response for voltage AC protection tripped status: '{response}'")

    def clear_sense_voltage_ac_protection(self):
        """Causes the protection circuit to be cleared for AC Voltage.
        Notes: This is an event command; no query."""
        self.instrument.write(":SENS:VOLT:AC:PROT:CLE")

    
    def set_sense_voltage_ac_range_upper(self, value: float):
        """Specifies the most positive signal level expected for the AC Voltage sensor input.
        Parameters:
        value: The upper range value (numeric value)."""
        self.instrument.write(f":SENS:VOLT:AC:RANG:UPP {value}")

    def get_sense_voltage_ac_range_upper(self) -> float:
        """Returns the most positive signal level expected for the AC Voltage sensor input."""
        response = self.instrument.query(":SENS:VOLT:AC:RANG:UPP?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for voltage AC range upper (not numeric): '{response}'")

    def set_sense_voltage_ac_range_lower(self, value: float):
        """Specifies the most negative signal level expected for the AC Voltage sensor input.
        Parameters:
        value: The lower range value (numeric value)."""
        self.instrument.write(f":SENS:VOLT:AC:RANG:LOW {value}")

    def get_sense_voltage_ac_range_lower(self) -> float:
        """Returns the most negative signal level expected for the AC Voltage sensor input."""
        response = self.instrument.query(":SENS:VOLT:AC:RANG:LOW?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for voltage AC range lower (not numeric): '{response}'")

    def set_sense_voltage_ac_range_auto(self, auto_state: str):
        """Sets the range for AC Voltage to the value determined to give the most dynamic range.
        Parameters:
        auto_state: Boolean (ON|OFF) or 'ONCE'. Selecting 'ONCE' sets AUTO to ON and then OFF."""
        normalized_state = auto_state.upper()
        if normalized_state in {1, "ON"}:
            scpi_value = "ON"
        elif normalized_state in {0, "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":SENS:VOLT:AC:RANG:AUTO {scpi_value}")

    def get_sense_voltage_ac_range_auto(self) -> str:
        """Returns the auto state of the AC Voltage range ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query(":SENS:VOLT:AC:RANG:AUTO?").strip()
        if response == 1:
            return "ON"
        elif response == 0:
            return "OFF"
        else:
            return response.upper()

    def set_sense_voltage_ac_range_auto_direction(self, direction: str):
        """Defines the manner in which AUTO works for AC Voltage ranging.
        Parameters:
        direction: UP|DOWN|EITHer"""
        valid_directions = {"UP", "DOWN", "EITHER", "EITH"}
        direction_upper = direction.upper()
        if direction_upper not in valid_directions:
            raise ValueError(f"Invalid direction: '{direction}'. Must be 'UP', 'DOWN', or 'EITHer'.")

        if direction_upper == "EITHER": scpi_value = "EITH"
        else: scpi_value = direction_upper

        self.instrument.write(f":SENS:VOLT:AC:RANG:AUTO:DIR {scpi_value}")

    def get_sense_voltage_ac_range_auto_direction(self) -> str:
        """Returns the auto-ranging direction for AC Voltage ('UP', 'DOWN', or 'EITHER')."""
        response = self.instrument.query(":SENS:VOLT:AC:RANG:AUTO:DIR?").strip().upper()
        if response.startswith("EITH"):
            return "EITHER"
        return response

    def set_sense_voltage_ac_range_auto_llimit(self, value: float):
        """Sets the smallest range to which the instrument will go while auto-ranging for AC Voltage.
        Parameters:
        value: The lower limit (numeric value)."""
        self.instrument.write(f":SENS:VOLT:AC:RANG:AUTO:LLIM {value}")

    def get_sense_voltage_ac_range_auto_llimit(self) -> float:
        """Returns the smallest range to which the instrument will go while auto-ranging for AC Voltage."""
        response = self.instrument.query(":SENS:VOLT:AC:RANG:AUTO:LLIM?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for voltage AC range auto lower limit (not numeric): '{response}'")

    def set_sense_voltage_ac_range_auto_ulimit(self, value: float):
        """Sets the largest range to which the instrument will go while auto-ranging for AC Voltage.
        Parameters:
        value: The upper limit (numeric value)."""
        self.instrument.write(f":SENS:VOLT:AC:RANG:AUTO:ULIM {value}")

    def get_sense_voltage_ac_range_auto_ulimit(self) -> float:
        """Returns the largest range to which the instrument will go while auto-ranging for AC Voltage."""
        response = self.instrument.query(":SENS:VOLT:AC:RANG:AUTO:ULIM?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for voltage AC range auto upper limit (not numeric): '{response}'")

    
    def set_sense_voltage_ac_range_offset(self, value: float):
        """Determines the midpoint of the range for AC Voltage.
        Parameters:
        value: The offset value (numeric value)."""
        self.instrument.write(f":SENS:VOLT:AC:RANG:OFFS {value}")

    def get_sense_voltage_ac_range_offset(self) -> float:
        """Returns the midpoint of the range for AC Voltage."""
        response = self.instrument.query(":SENS:VOLT:AC:RANG:OFFS?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for voltage AC range offset (not numeric): '{response}'")

    def set_sense_voltage_ac_range_ptpeak(self, value: float):
        """Specifies the dynamic range required for the AC Voltage sensor (Peak To Peak).
        Parameters:
        value: The peak-to-peak value (numeric value)."""
        self.instrument.write(f":SENS:VOLT:AC:RANG:PTP {value}")

    def get_sense_voltage_ac_range_ptpeak(self) -> float:
        """Returns the dynamic range required for the AC Voltage sensor (Peak To Peak)."""
        response = self.instrument.query(":SENS:VOLT:AC:RANG:PTP?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for voltage AC range PTPeak (not numeric): '{response}'")

    def set_sense_voltage_ac_reference(self, value: float):
        """Sets a reference amplitude for AC Voltage sensor instruments.
        Parameters:
        value: The reference amplitude (numeric value)."""
        self.instrument.write(f":SENS:VOLT:AC:REF {value}")

    def get_sense_voltage_ac_reference(self) -> float:
        """Returns the reference amplitude for AC Voltage sensor instruments."""
        response = self.instrument.query(":SENS:VOLT:AC:REF?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for voltage AC reference (not numeric): '{response}'")

    def set_sense_voltage_ac_reference_state(self, enable: bool):
        """Determines whether amplitude is measured in absolute or relative mode for AC Voltage.
        Parameters:
        enable: True to reference to the value set in REFerence, False for absolute mode."""
        scpi_value = 1 if enable else 0
        self.instrument.write(f":SENS:VOLT:AC:REF:STATE {scpi_value}")

    def get_sense_voltage_ac_reference_state(self) -> bool:
        """Returns True if amplitude is measured in relative mode for AC Voltage, False for absolute mode."""
        response = self.instrument.query(":SENS:VOLT:AC:REF:STATE?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for voltage AC reference state: '{response}'")

    def set_sense_voltage_ac_resolution(self, value: float):
        """Specifies the absolute resolution of the AC Voltage measurement.
        Parameters:
        value: The resolution value (numeric value)."""
        self.instrument.write(f":SENS:VOLT:AC:RES {value}")

    def get_sense_voltage_ac_resolution(self) -> float:
        """Returns the absolute resolution of the AC Voltage measurement."""
        response = self.instrument.query(":SENS:VOLT:AC:RES?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for voltage AC resolution (not numeric): '{response}'")

    def set_sense_voltage_ac_resolution_auto(self, auto_state: str):
        """Allows the system to determine the best resolution for the other measurement conditions for AC Voltage.
        Parameters:
        auto_state: Boolean (ON|OFF) or 'ONCE'. Selecting 'ONCE' sets AUTO to ON and then OFF."""
        normalized_state = auto_state.upper()
        if normalized_state in {1, "ON"}:
            scpi_value = "ON"
        elif normalized_state in {0, "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":SENS:VOLT:AC:RES:AUTO {scpi_value}")

    def get_sense_voltage_ac_resolution_auto(self) -> str:
        """Returns the auto state of the AC Voltage resolution ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query(":SENS:VOLT:AC:RES:AUTO?").strip()
        if response == 1:
            return "ON"
        elif response == 0:
            return "OFF"
        else:
            return response.upper()

    
    def set_sense_voltage_detector(self, detector_type: str):
        """Specifies the detector for Voltage as internal or external.
        Parameters:
        detector_type: INTernal|EXTernal"""
        valid_types = {"INTERNAL", "EXTERNAL", "INT", "EXT"}
        type_upper = detector_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid detector type: '{detector_type}'. Must be 'INTernal' or 'EXTernal'.")

        if type_upper == "INTERNAL": scpi_value = "INT"
        elif type_upper == "EXTERNAL": scpi_value = "EXT"
        else: scpi_value = type_upper

        self.instrument.write(f":SENS:VOLT:DET {scpi_value}")

    def get_sense_voltage_detector(self) -> str:
        """Returns the detector type for Voltage ('INTERNAL' or 'EXTERNAL')."""
        response = self.instrument.query(":SENS:VOLT:DET?").strip().upper()
        if response.startswith("INT"):
            return "INTERNAL"
        elif response.startswith("EXT"):
            return "EXTERNAL"
        return response

    
    def set_sense_window_type(self, window_type: str):
        """Selects from among several well-known or standard window types.
        Parameters:
        window_type: RECTangular|UNIForm|FLATtop|HAMMing|HANNing|KBESsel|FORCe|EXPonential"""
        valid_types = {
            "RECTANGULAR", "UNIFORM", "FLATTOP", "HAMMING", "HANNING",
            "KBESSEL", "FORCE", "EXPONENTIAL",
            "RECT", "UNIF", "FLAT", "HAMM", "HANN", "KBES", "FORC", "EXP"
        }
        type_upper = window_type.upper()
        if type_upper not in valid_types:
            raise ValueError(f"Invalid window type: '{window_type}'.")

        if type_upper == "RECTANGULAR": scpi_value = "RECT"
        elif type_upper == "UNIFORM": scpi_value = "UNIF"
        elif type_upper == "FLATTOP": scpi_value = "FLAT"
        elif type_upper == "HAMMING": scpi_value = "HAMM"
        elif type_upper == "HANNING": scpi_value = "HANN"
        elif type_upper == "KBESSEL": scpi_value = "KBES"
        elif type_upper == "FORCE": scpi_value = "FORC"
        elif type_upper == "EXPONENTIAL": scpi_value = "EXP"
        else: scpi_value = type_upper

        self.instrument.write(f":SENS:WIND:TYPE {scpi_value}")

    def get_sense_window_type(self) -> str:
        """Returns the currently selected window type."""
        response = self.instrument.query(":SENS:WIND:TYPE?").strip().upper()
        if response.startswith("RECT"): return "RECTANGULAR"
        elif response.startswith("UNIF"): return "UNIFORM"
        elif response.startswith("FLAT"): return "FLATTOP"
        elif response.startswith("HAMM"): return "HAMMING"
        elif response.startswith("HANN"): return "HANNING"
        elif response.startswith("KBES"): return "KBESSEL"
        elif response.startswith("FORC"): return "FORCE"
        elif response.startswith("EXP"): return "EXPONENTIAL"
        return response

    def set_sense_window_type_kbessel(self, time_constant_seconds: float):
        """Enters the exponential decay time constant which characterizes the KBESsel window.
        Parameters:
        time_constant_seconds: The time constant in seconds (numeric value)."""
        self.instrument.write(f":SENS:WIND:TYPE:KBES {time_constant_seconds}")

    def get_sense_window_type_kbessel(self) -> float:
        """Returns the exponential decay time constant for the KBESsel window."""
        response = self.instrument.query(":SENS:WIND:TYPE:KBES?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for window type KBESsel (not numeric): '{response}'")

    def set_sense_window_type_exponential(self, time_constant_seconds: float):
        """Enters the exponential decay time constant which characterizes the EXPonential window.
        Parameters:
        time_constant_seconds: The time constant in seconds (numeric value)."""
        self.instrument.write(f":SENS:WIND:TYPE:EXP {time_constant_seconds}")

    def get_sense_window_type_exponential(self) -> float:
        """Returns the exponential decay time constant for the EXPonential window."""
        response = self.instrument.query(":SENS:WIND:TYPE:EXP?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for window type EXPonential (not numeric): '{response}'")

    def set_sense_window_type_force(self, time_value_seconds: float):
        """Enters the time value parameter corresponding to the width of the gated portion of the input time record for FORCe windows.
        Parameters:
        time_value_seconds: The time value in seconds (numeric value)."""
        self.instrument.write(f":SENS:WIND:TYPE:FORC {time_value_seconds}")

    def get_sense_window_type_force(self) -> float:
        """Returns the time value parameter for the width of the gated portion of the input time record for FORCe windows."""
        response = self.instrument.query(":SENS:WIND:TYPE:FORC?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for window type FORCe (not numeric): '{response}'")

