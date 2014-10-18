# Documentation for # PyPi

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
    

## Functions and Classes

### pypi.install(...):
Install a package from the IDLE,
same way as using the commandline
and typing "pip install ..."

### pypi.upload(...):
Upload and distribute your package
to the online PyPi website in a single
command with includes and docs, so others
can find it more easily and install
it using pip.
(Not yet working)s

