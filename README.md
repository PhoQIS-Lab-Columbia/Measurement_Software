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

Each instrument contains two components: helper and secondary. Helper consists of user made automated functions while secondary contains all the less commonly used commands (like display cursor toggles and lan configurations) while the most commonly used commands are kept in the main class. Within the main and secondary classes, functions are categorized by what primary function

'''py
>>> import
'''

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

- `Instruments/` — Instrument drivers and helpers
  - 'SCPICommandTree
- `Experiments/` — Example and template experiments
- `Reference/` — Simulation notebooks and documentation
- `README.md` — Project overview and instructions

## Contributing

Contributions are welcome! Please submit pull requests or open issues for bugs and feature requests.


