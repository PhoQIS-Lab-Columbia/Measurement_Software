# Measurement Software

## Overview

Measurement Software is a Python package for controlling and automating a variety of laboratory measurement instruments. It provides a unified interface for experiment setup, data acquisition, and instrument management, enabling users to streamline workflows and automate repetitive tasks.

## Features

- Modular instrument control via SCPI commands
- Easy integration of new instruments with guided automated coding pipeline
- Reuseable experiments
- Data auto-saving and management
- Network manager for multi-instrument setups

## Instruments Supported
- Vector Network Analyzer (Copper Mountain)
- Oscilloscope (Rigol)
- Spectrum Analyzer (Signal Hound)
- Additional instruments can be added using provided jupyter notebook AddANewInstrument.ipynb

## How to Use
Each instrument contains two components: helper and secondary. Helper consists of user made automated functions while secondary contains all the less commonly used commands (like display cursor toggles and lan configurations) while the most commonly used commands are kept in the main class. Within the main and secondary classes, functions are categorized by what primary command they fall under. The standard list of components is:

- CALibrate: Used for performing instrument calibration routines.
- CONFigure: Configures measurement settings and operational modes.
- DATA: Handles the transfer and manipulation of arbitrary data blocks.
- DISPlay: Controls the instrument's display settings and output.
- FORMat: Specifies the format of data for input or output operations (e.g., ASCII, binary).
- HCOPy: Manages hardcopy (print or plot) functions.
- INITiate: Controls the initiation of measurements or operations.
- INPut: Handles settings related to the instrument's input channels.
- MEASure: Initiates and configures specific measurements.
- MEMory: Manages the instrument's internal memory for saving and recalling data.
- MMEMory: Deals with mass storage memory (e.g., hard drives, flash drives) for saving and recalling files.
- OUTPut: Controls the instrument's output functions and levels.
- SENSe: Defines measurement parameters and ranges for input signals.
- SOURce: Controls signal generation and sourcing functions.
- STATus: Provides access to instrument status registers and error information.
- SYSTem: Deals with general instrument functions like identification and communication.
- TRIGger: Controls all aspects of instrument triggering.
- UNIT: Specifies and queries the measurement units used by the instrument.
- VXI: Provides commands specific to VXIbus systems for configuring and controlling VXI devices.

Along with the instrument classes the api contains the classes NetworkHandler for connecting and managing instrument connections and DataHandler for saving and processing raw instrument data.

See template_python.py in the Experiments folder for an coding example.

## Getting Started

1. **Clone the repository**  
  `git clone <repo-url>`

2. **Install dependencies**  
  See `requirements.txt` for required Python packages.

3. **Run an experiment**  
  Use the provided experiment template in the `Experiments/` directory to get started and view coding examples.

4. **Add a new instrument**  
  Follow the instructions in `Instruments/AddANewInstrument.ipynb` to integrate new hardware.

## Folder Structure
- `Experiments/` — Example and template experiments
- `Instruments/` — Instrument drivers and helpers
  - `Documentation/` - Instrument programming manuals
  - `Generic Classes/` - Common insturment type superclasses
  - `SCPICommandTree/` - Common SCPI commands
- `Reference/` — Simulation notebooks and documentation,graveyard
- `Testing` — Unit tests

## Contributing

Contributions are welcome! Please update the read me if you add a new instrument.


