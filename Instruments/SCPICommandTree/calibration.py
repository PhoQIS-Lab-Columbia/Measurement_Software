class Calibration():
    def __init__(self, instrument):
        self.instrument = instrument
        
    def calibrate_all(self):
        """Performs a full calibration of the instrument.
        Notes: This is an event command; no query. Errors are reported via status-reporting."""
        self.instrument.write(":CAL:ALL")

    def get_calibrate_all_status(self) -> int:
        """Returns the success status of a full calibration.
        Returns: 0 if calibration is successful; otherwise, a non-zero error number."""
        response = self.instrument.query(":CAL:ALL?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for calibration all status (not integer): '{response}'")

    def set_calibrate_auto(self, auto_state: str):
        """Sets whether or not the instrument should perform auto calibration at device-dependent intervals.
        Parameters:
        auto_state: AUTO|ONCE (Boolean equivalent for AUTO, or 'ONCE'). 'ONCE' is also a valid state."""
        normalized_state = auto_state.upper()
        if normalized_state in {1, "ON"}:
            scpi_value = "ON"
        elif normalized_state in {0, "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid auto calibration state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":CAL:AUTO {scpi_value}")

    def get_calibrate_auto(self) -> str:
        """Returns whether the instrument performs auto calibration ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query(":CAL:AUTO?").strip()
        if response == 1:
            return "ON"
        elif response == 0:
            return "OFF"
        else:
            return response.upper() # Return ONCE as is if that's what the instrument sends
    # LINearize command tree SCPI wrappers

    def linearize_accept(self):
        """Accepts the current linearization data."""
        self.calibration_obj.instrument.write(":LIN:ACC")

    def linearize_acquire(self):
        """Acquires linearization data."""
        self.calibration_obj.instrument.write(":LIN:ACQ")

    def linearize_auto(self, state: str):
        """Sets or queries the linearization auto mode ('ON', 'OFF', or 'ONCE')."""
        state = state.upper()
        if state not in {"ON", "OFF", "ONCE"}:
            raise ValueError("State must be 'ON', 'OFF', or 'ONCE'.")
        self.calibration_obj.instrument.write(f":LIN:AUTO {state}")

    def get_linearize_auto(self) -> str:
        """Returns the linearization auto mode ('ON', 'OFF', or 'ONCE')."""
        response = self.calibration_obj.instrument.query(":LIN:AUTO?").strip().upper()
        return response

    def linearize_calculate(self, mode: str, n: int = None):
        """Calculates the linearization curve.
        mode: 'AUTO', 'POLYNOMIAL', or 'SRATIONAL'
        n: Optional, degree/order for polynomial or srational
        """
        mode = mode.upper()
        if mode == "AUTO":
            self.calibration_obj.instrument.write(":LIN:CALC AUTO")
        elif mode in {"POLYNOMIAL", "SRATIONAL"}:
            if n is None:
                raise ValueError("n must be specified for POLYNOMIAL or SRATIONAL mode.")
            scpi_mode = "POLY" if mode == "POLYNOMIAL" else "SRAT"
            self.calibration_obj.instrument.write(f":LIN:CALC {scpi_mode}{n}")
        else:
            raise ValueError("Mode must be 'AUTO', 'POLYNOMIAL', or 'SRATIONAL'.")

    def linearize_curve(self, curve_type: str, n: int = None, values: list = None):
        """Sets the linearization curve type and values.
        curve_type: 'POLYNOMIAL' or 'SRATIONAL'
        n: degree/order
        values: list of numeric values for SRATIONAL
        """
        curve_type = curve_type.upper()
        if curve_type == "POLYNOMIAL":
            if n is None:
                raise ValueError("n must be specified for POLYNOMIAL curve.")
            self.calibration_obj.instrument.write(f":LIN:CURV:TYPE POLY{n}")
        elif curve_type == "SRATIONAL":
            if n is None or values is None or not isinstance(values, list):
                raise ValueError("n and values list must be specified for SRATIONAL curve.")
            values_str = ",".join(map(str, values))
            self.calibration_obj.instrument.write(f":LIN:CURV:TYPE SRAT{n},{values_str}")
        else:
            raise ValueError("curve_type must be 'POLYNOMIAL' or 'SRATIONAL'.")

    def linearize_curve_zforce(self, enable: bool):
        """Enables or disables ZFORce for linearization curve."""
        scpi_value = "ON" if enable else "OFF"
        self.calibration_obj.instrument.write(f":LIN:CURV:ZFOR {scpi_value}")

    def linearize_verify(self):
        """Starts the linearization verification procedure."""
        self.calibration_obj.instrument.write(":LIN:VER")

    def linearize_verify_acquire(self):
        """Acquires verification data for linearization."""
        self.calibration_obj.instrument.write(":LIN:VER:ACQ")

    def linearize_verify_tolerance(self, value: float):
        """Sets the tolerance for linearization verification."""
        self.calibration_obj.instrument.write(f":LIN:VER:TOL {value}")

    def get_linearize_verify_tolerance(self) -> float:
        """Returns the tolerance for linearization verification."""
        response = self.calibration_obj.instrument.query(":LIN:VER:TOL?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for linearization verify tolerance: '{response}'")

    def linearize_verify_type(self, verify_type: str):
        """Sets the verification type: 'CCURVE' or 'NCURVE'."""
        verify_type = verify_type.upper()
        if verify_type not in {"CCURVE", "NCURVE"}:
            raise ValueError("verify_type must be 'CCURVE' or 'NCURVE'.")
        scpi_value = "CCUR" if verify_type == "CCURVE" else "NCUR"
        self.calibration_obj.instrument.write(f":LIN:VER:TYPE {scpi_value}")

    def get_binertia_average(self) -> float:
        """Returns the running average of all base inertia values acquired since the last :CALibration:BINertia:INITiate was invoked."""
        response = self.instrument.query(":CAL:BIN:AVER?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for binertia average (not numeric): '{response}'")

    def set_binertia_hspeed(self, speed: float):
        """Sets the higher magnitude speed (m/s) of the speed interval for base inertia.
        Parameters:
        speed: The high speed in m/s (numeric value)."""
        self.instrument.write(f":CAL:BIN:HSP {speed}")

    def get_binertia_hspeed(self) -> float:
        """Returns the higher magnitude speed (m/s) of the speed interval for base inertia."""
        response = self.instrument.query(":CAL:BIN:HSP?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for binertia high speed (not numeric): '{response}'")

    def initiate_binertia(self):
        """Begins motoring the dynamometer through acceleration/deceleration pairs for base inertia calculation.
        Notes: This is an event command; no query."""
        self.instrument.write(":CAL:BIN:INIT")

    def set_binertia_lspeed(self, speed: float):
        """Sets the lower magnitude speed (m/s) of the speed interval for base inertia.
        Parameters:
        speed: The low speed in m/s (numeric value)."""
        self.instrument.write(f":CAL:BIN:LSP {speed}")

    def get_binertia_lspeed(self) -> float:
        """Returns the lower magnitude speed (m/s) of the speed interval for base inertia."""
        response = self.instrument.query(":CAL:BIN:LSP?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for binertia low speed (not numeric): '{response}'")

    def set_binertia_nruns(self, runs: int):
        """Sets the number of acceleration/deceleration pairs to perform for base inertia.
        Parameters:
        runs: The number of runs (integer numeric value)."""
        if not isinstance(runs, int) or runs < 0:
            raise ValueError("Number of runs must be a non-negative integer.")
        self.instrument.write(f":CAL:BIN:NRUN {runs}")

    def get_binertia_nruns(self) -> int:
        """Returns the number of acceleration/deceleration pairs to perform for base inertia."""
        response = self.instrument.query(":CAL:BIN:NRUN?").strip()
        try:
            return int(response)
        except ValueError:
            raise ValueError(f"Unexpected response for binertia number of runs (not integer): '{response}'")

    def get_binertia_sdeviation(self) -> float:
        """Returns the running standard deviation of all base inertia values acquired since the last :CALibration:BINertia:INITiate was invoked."""
        response = self.instrument.query(":CAL:BIN:SDEV?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for binertia standard deviation (not numeric): '{response}'")

    def update_binertia(self):
        """Places on-line the last determined average base mechanical inertia value.
        Notes: This is an event command; no query."""
        self.instrument.write(":CAL:BIN:UPD")

    def set_calibration_data(self, data: bytes):
        """Transfers calibration data as arbitrary block program data.
        Parameters:
        data: The calibration data as bytes."""
        # SCPI arbitrary block data format: #<num_digits><num_bytes><raw_data>
        # Example: #3123ABC... (3 digits for length, 123 bytes of data)
        num_bytes = len(data)
        num_digits = len(str(num_bytes))
        self.instrument.write(f":CAL:DATA #{num_digits}{num_bytes}" + data.decode('latin-1')) # Assuming latin-1 for byte representation

    def get_calibration_data(self) -> bytes:
        """Returns the current calibration data as arbitrary block program data.
        Returns: The calibration data as bytes."""
        # This will query and parse the arbitrary block data response.
        # This is a simplified approach, a robust parser would be more complex.
        response = self.instrument.query(":CAL:DATA?").strip()
        if not response.startswith('#'):
            raise ValueError(f"Unexpected response format for calibration data: '{response}'")
        
        num_digits = int(response[1])
        length_str = response[2 : 2 + num_digits]
        data_length = int(length_str)
        
        # Extract data part (assuming the query returns the full block)
        data_start_index = 2 + num_digits
        return response[data_start_index:].encode('latin-1') # Encode back to bytes

    def set_ploss_apcoeffs(self, coeffs: list[float]):
        """Sets the active parasitic loss coefficients.
        Parameters:
        coeffs: A list of numeric values (up to 4) representing the parasitic loss coefficients."""
        if not (1 <= len(coeffs) <= 4):
            raise ValueError("Coefficients list must contain 1 to 4 numeric values.")
        data_str = ",".join(map(str, coeffs))
        self.instrument.write(f":CAL:PLOS:APCO {data_str}")

    def get_ploss_apcoeffs(self) -> list[float]:
        """Returns the presently active parasitic loss coefficients."""
        response = self.instrument.query(":CAL:PLOS:APCO?").strip()
        try:
            return [float(x) for x in response.split(',')]
        except ValueError:
            raise ValueError(f"Unexpected response for parasitic loss coefficients: '{response}'")

    def initiate_ploss(self):
        """Starts the parasitic loss procedure.
        Notes: This is an overlapped command (event); no query."""
        self.instrument.write(":CAL:PLOS:INIT")

    def set_ploss_latime(self, time_in_seconds: float):
        """Sets the length of time in seconds to average the losses at a speed point.
        Parameters:
        time_in_seconds: Loss Averaging Time in seconds (numeric value)."""
        self.instrument.write(f":CAL:PLOS:LATI {time_in_seconds}")

    def get_ploss_latime(self) -> float:
        """Returns the length of time in seconds to average the losses at a speed point."""
        response = self.instrument.query(":CAL:PLOS:LATI?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for parasitic loss averaging time (not numeric): '{response}'")

    def set_ploss_stime(self, time_in_seconds: float):
        """Sets the stabilization time in seconds prior to Loss Averaging Time.
        Parameters:
        time_in_seconds: Stabilization Time in seconds (numeric value)."""
        self.instrument.write(f":CAL:PLOS:STIM {time_in_seconds}")

    def get_ploss_stime(self) -> float:
        """Returns the stabilization time in seconds prior to Loss Averaging Time."""
        response = self.instrument.query(":CAL:PLOS:STIM?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for parasitic loss stabilization time (not numeric): '{response}'")

    def update_ploss(self):
        """Updates the dynamometer parasitic loss coefficients with the coefficients contained in memory table Pcoeff.
        Notes: This is an event command; no query."""
        self.instrument.write(":CAL:PLOS:UPD")

    def set_calibration_source(self, source_type: str):
        """Controls the source of the calibration signal.
        Parameters:
        source_type: INTernal|EXTernal"""
        valid_sources = {"INTERNAL", "EXTERNAL", "INT", "EXT"}
        source_type_upper = source_type.upper()
        if source_type_upper not in valid_sources:
            raise ValueError(f"Invalid source type: '{source_type}'. Must be 'INTERNAL' or 'EXTERNAL'.")
        
        if source_type_upper == "INTERNAL": scpi_value = "INT"
        elif source_type_upper == "EXTERNAL": scpi_value = "EXT"
        else: scpi_value = source_type_upper # Use the provided abbreviation if it's valid
        
        self.instrument.write(f":CAL:SOUR {scpi_value}")

    def get_calibration_source(self) -> str:
        """Returns the source of the calibration signal ('INTERNAL' or 'EXTERNAL')."""
        response = self.instrument.query(":CAL:SOUR?").strip().upper()
        if response.startswith("INT"):
            return "INTERNAL"
        elif response.startswith("EXT"):
            return "EXTERNAL"
        return response # Return as-is if unexpected

    def set_calibration_state(self, enable: bool):
        """Selects if the calibration data is applied or not.
        Parameters:
        enable: True to use calibration data for correction, False to make no correction."""
        scpi_value = 1 if enable else 0
        self.instrument.write(f":CAL:STATE {scpi_value}")

    def get_calibration_state(self) -> bool:
        """Returns True if calibration data is applied, False if not."""
        response = self.instrument.query(":CAL:STATE?").strip()
        if response == 1 or response.upper() == "ON":
            return True
        elif response == 0 or response.upper() == "OFF":
            return False
        else:
            raise ValueError(f"Unexpected response for calibration state: '{response}'")

    def set_calibration_value(self, value: float):
        """Enters the value of the reference signal used in the calibration.
        Parameters:
        value: The reference signal value (numeric value)."""
        self.instrument.write(f":CAL:VAL {value}")

    def get_calibration_value(self) -> float:
        """Returns the value of the reference signal used in the calibration."""
        response = self.instrument.query(":CAL:VAL?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for calibration value (not numeric): '{response}'")

    def initiate_warmup(self):
        """Starts the warmup procedure.
        Notes: This is an event command; no query."""
        self.instrument.write(":CAL:WARM:INIT")

    def set_warmup_speed(self, speed: float):
        """Sets the fixed roll speed (m/s) at which the warm-up will be run for chassis dynamometers.
        Parameters:
        speed: The roll speed in m/s (numeric value)."""
        self.instrument.write(f":CAL:WARM:SPE {speed}")

    def get_warmup_speed(self) -> float:
        """Returns the fixed roll speed (m/s) at which the warm-up will be run for chassis dynamometers."""
        response = self.instrument.query(":CAL:WARM:SPE?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for warmup speed (not numeric): '{response}'")

    def set_warmup_timeout(self, timeout_seconds: float):
        """Sets the length of time in seconds the warm-up will run before automatically returning to zero speed.
        Parameters:
        timeout_seconds: The timeout period in seconds (numeric value)."""
        self.instrument.write(f":CAL:WARM:TIM {timeout_seconds}")

    def get_warmup_timeout(self) -> float:
        """Returns the length of time in seconds the warm-up will run."""
        response = self.instrument.query(":CAL:WARM:TIM?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for warmup timeout (not numeric): '{response}'")

    def set_zero_auto(self, auto_state: str):
        """Controls whether autozeroing calibration occurs.
        Parameters:
        auto_state: AUTO|ONCE (Boolean equivalent for AUTO, or 'ONCE'). 'ONCE' is also a valid state."""
        normalized_state = auto_state.upper()
        if normalized_state in {1, "ON"}:
            scpi_value = "ON"
        elif normalized_state in {0, "OFF"}:
            scpi_value = "OFF"
        elif normalized_state == "ONCE":
            scpi_value = "ONCE"
        else:
            raise ValueError(f"Invalid autozero state: '{auto_state}'. Must be 'ON', 'OFF', or 'ONCE'.")
        self.instrument.write(f":CAL:ZERO:AUTO {scpi_value}")

    def get_zero_auto(self) -> str:
        """Returns whether autozeroing calibration occurs ('ON', 'OFF', or 'ONCE')."""
        response = self.instrument.query(":CAL:ZERO:AUTO?").strip()
        if response == 1:
            return "ON"
        elif response == 0:
            return "OFF"
        else:
            return response.upper()

    def initiate_zero_fsensor(self):
        """Performs the measurement of the roll force for mathematical zero correction.
        Notes: This is an overlapped command (event); no query."""
        self.instrument.write(":CAL:ZERO:FSEN:INIT")

    def set_zero_fsensor_latime(self, time_in_seconds: float):
        """Sets the length of time to average the measured zero reading.
        Parameters:
        time_in_seconds: Loss Averaging Time in seconds (numeric value)."""
        self.instrument.write(f":CAL:ZERO:FSEN:LATI {time_in_seconds}")

    def get_zero_fsensor_latime(self) -> float:
        """Returns the length of time to average the measured zero reading."""
        response = self.instrument.query(":CAL:ZERO:FSEN:LATI?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for force sensor zero averaging time (not numeric): '{response}'")

    def get_zero_fsensor_level(self) -> float:
        """Returns the measured force value used to determine the mathematical zero correction."""
        response = self.instrument.query(":CAL:ZERO:FSEN:LEVE?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for force sensor zero level (not numeric): '{response}'")

    def set_zero_fsensor_speed(self, speed: float):
        """Sets the roll speed set point for the force measurement period.
        Parameters:
        speed: The roll speed set point in m/s (numeric value)."""
        self.instrument.write(f":CAL:ZERO:FSEN:SPE {speed}")

    def get_zero_fsensor_speed(self) -> float:
        """Returns the roll speed set point for the force measurement period."""
        response = self.instrument.query(":CAL:ZERO:FSEN:SPE?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for force sensor zero speed (not numeric): '{response}'")

    def set_zero_fsensor_stime(self, time_in_seconds: float):
        """Sets the stabilization time prior to Loss Averaging Time for force sensor zero.
        Parameters:
        time_in_seconds: Stabilization Time in seconds (numeric value)."""
        self.instrument.write(f":CAL:ZERO:FSEN:STIM {time_in_seconds}")

    def get_zero_fsensor_stime(self) -> float:
        """Returns the stabilization time prior to Loss Averaging Time for force sensor zero."""
        response = self.instrument.query(":CAL:ZERO:FSEN:STIM?").strip()
        try:
            return float(response)
        except ValueError:
            raise ValueError(f"Unexpected response for force sensor zero stabilization time (not numeric): '{response}'")

    def update_zero_fsensor(self):
        """Applies the mathematical zero correction to the on-line calibration.
        Notes: This is an event command; no query."""
        self.instrument.write(":CAL:ZERO:FSEN:UPD")
