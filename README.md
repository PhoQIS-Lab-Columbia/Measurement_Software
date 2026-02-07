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

## Getting Started
If you plan to just use the library and not modify it in any way, instead of cloning the repository go the following address https://test.pypi.org/project/measurement-instruments/ and use the pip install at link. See [insert github link] for a template experiment on how to use this library. Full documentation can be found at [insert link].

If this is a new PC, ensure NI0VISA is downloaded along with the following instrument specfic applications for all instruments you plan to use:

 Download the appropriate visa for your system on the National Instrument website: [NI-VISA Download](https://www.ni.com/en/support/downloads/drivers/download.ni-visa.html?srsltid=AfmBOorVfmnA2doyRSh73r9AQEBtnI1TnYyEls5m_Z0yTSMRIdfTDlDy#570633)

  If you plan to use the following instruments you'll need to download the corresponding software:
  - Signal Hound Specturm Analyzer - [Spike visualization Software](https://signalhound.com/spike/?srsltid=AfmBOoozG63C7yQ_YqGvtIc8od2RNExMac8wMt943VV0tb1fW7MqZ3x4)
  - Flowmeter - [NQ Sensor Monitor](https://www.keyence.com/support/user/sensor/network-communication/software/)
  - Vector Network Analyzer - [S4 VNA Software](https://coppermountaintech.com/demo-the-software/)

1. **Clone the repository**  
  `git clone <https://github.com/phoqis-lab/Measurement_Software>`

2. **Install dependencies**  
  See `requirements.txt` for required Python packages.

3. **Add a new instrument**  
  Follow the instructions in `Instruments/AddANewInstrument.ipynb` to integrate new hardware. You may also modify any of the helper .py files to add prebuilt subroutines you may want to frequencyly call in multiple experiments.

4. **Updating public library instance**
  Official PyPi distirbution instructions can be found here: https://packaging.python.org/en/latest/tutorials/packaging-projects/

  First log on to the PyPi account. The PhoQis account can be found in the lab's notion on the measurement software page.

  Next go into the pyproject.toml file and the setup.py file and change the version number. For small changes like adding functions to a helper file, increment the third number by one (1.0.0 -> 1.0.1) and for larger changes like adding a new instrument increment the second number (1.0.0 -> 1.1.0)

  First ensure setuptools and build is upgraded and then use it to build the python library:
  ```python3 -m pip install setuptools```
  ``` python3 -m pip install --upgrade build```
  ``` python3 -m build```

This will package the library to prepare it for distribution. To then publish the update to PyPi, use twine and the following terminal commands.

```python3 -m pip install --upgrade twine```
```python3 -m twine upload dist/*  ```

The updates should be reflected on the PhoQis PyPi account and the it will automatically update the pip install needed to downloaded. Ensure you run a pip --upgrade for the library in whatever python enviroment you are using for your experiments.

5. **Updating the public documentation**


   
## Contributing

Contributions are welcome! Please update the read me if you add a new instrument.


