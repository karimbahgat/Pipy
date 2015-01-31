"""
# PyPi

Install or upload your Python packages from/to the PyPi package index website.
Easy to use, IDLE/shell access, and no dependencies.

Karim Bahgat, 2014


## Installation

Make pypi available by putting the folder anywhere it can be imported (eg site-packages).

Note: Comes pre-packaged with pip and will automatically install the necessary setuptools package
the first time you import pypi if you don't already have setuptools.

## Import

Import as pypi:

    import pypi

## Usage

Download packages from the pypi website (ala pip install)

    pypi.install("numpy")

Upload and share your own package to the pypi website. 

    pypi.login("myusername", "mypassword")
    pypi.define_upload(package="C:/MyPackageFolder",
                        name="MyPackageFolder",
                        version="0.1",
                        license="MIT",
                        ...)
    pypi.upload("C:/MyPackageFolder")
    pypi.logout()

When defining your upload use the traditional arguments from distutils.core.setup.
For testing your upload at the test website, use upload_test(...) instead.     
    
"""
from .main import *
