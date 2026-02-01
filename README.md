# Measurement Software

By Mary Grace D'Avanzo

## Overview

Measurement Software is a Python package for controlling and automating a variety of laboratory measurement instruments. It provides a unified interface for experiment setup, data acquisition, and instrument management, enabling users to streamline workflows and automate repetitive tasks. The package version can be downloaded by running pip install -i https://test.pypi.org/simple/ measurement-instruments

## Features

- Modular instrument control via SCPI commands
- Easy integration of new instruments with guided automated coding pipeline
- Reuseable experiments
- Data auto-saving and management
- Network manager for multi-instrument setups
- Opens and closes supporting programs automatically

## Instruments Supported
- Vector Network Analyzer (Copper Mountain)
- Oscilloscope (Rigol)
- Spectrum Analyzer (Signal Hound)
- RF Switch (Vasta)
- DC Power Supply (Siglent)
- Signal Generator (Signal Core)
- Digital Attenuator (Vanuix)
- Flow Meter (Keyence)
- Additional instruments can be added using provided jupyter notebook AddANewInstrument.ipynb

## How to Use
Each instrument contains two components: helper and a main. Helper consists of user made automated functions while the most commonly used commands are kept in the main class. Within the main classes, functions are categorized by what primary command they fall under.

Along with the instrument classes the api contains the classes NetworkHandler for connecting and managing instrument connections and DataHandler for saving and processing raw instrument data.

See template_python.py in the Experiments folder for an coding example.

## Getting Started
If you plan to just use the library and not modify it in any way, instead of cloning the repository go the following address https://test.pypi.org/project/measurement-instruments/ and use the pip install at link.

1. **Clone the repository**  
  `git clone <https://github.com/phoqis-lab/Measurement_Software>`

2. **Install dependencies**  
  See `requirements.txt` for required Python packages.

  If you are setting this up on a new computer, You will also need to install a VISA driver for the program to talk to. Download the appropriate visa for your system on the National Instrument website: [NI-VISA Download](https://www.ni.com/en/support/downloads/drivers/download.ni-visa.html?srsltid=AfmBOorVfmnA2doyRSh73r9AQEBtnI1TnYyEls5m_Z0yTSMRIdfTDlDy#570633)

  If you plan to use the following instruments you'll need to download the corresponding software:
  - Signal Hound Specturm Analyzer - [Spike visualization Software](https://signalhound.com/spike/?srsltid=AfmBOoozG63C7yQ_YqGvtIc8od2RNExMac8wMt943VV0tb1fW7MqZ3x4)
  - Flowmeter -
  - Vector Network Analyzer -

3. **Add a new instrument**  
  Follow the instructions in `Instruments/AddANewInstrument.ipynb` to integrate new hardware.

4. **Updating public library instance**
   
## Contributing

Contributions are welcome! Please update the read me if you add a new instrument.


