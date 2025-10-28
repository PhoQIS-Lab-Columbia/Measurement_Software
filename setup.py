from setuptools import setup, find_packages
from os import path
work_dir = path.abspath(path.dirname(__file__))
with open(path.join(work_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='measurement_instruments',
    version='0.1.12',
    url='https://github.com/phoqis-lab/Measurement_Software',
    author='Mary Grace D Avanzo',
    author_email='mgd2157@columbia.edu',
    description='A Python package for controlling and interfacing with various measurement instruments specficially for the PhoQIS Lab.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(include=['Instruments', 'Instruments.*']),
    install_requires=[
        
    ],
)