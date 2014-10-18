"""
# PyPi

Install or upload your Python packages from/to the PyPi package index website.
Easy to use, IDLE/shell access, and no dependencies.

Karim Bahgat, 2014


## Installation

Make pypi available by putting the folder anywhere it can be imported (eg site-packages).

## Import

Import as pypi (will install setuptools if you don't already have it):

    import pypi

## Usage

Download packages from the pypi website (ala pip install)

    pypi.install("numpy")

Upload and share your own package to the pypi website (Not yet working).

    pypi.upload("C:/MyPackageFolder") 
    
"""
from .main import install, upload
