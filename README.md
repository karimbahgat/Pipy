# Documentation for # PyPi

Install or upload your Python packages from/to the PyPi package index website.
Easy to use, IDLE/shell access, and no dependencies.

Karim Bahgat, 2015

## Disclaimer

This package has no relation to the makers of PyPi or pip, and
may or may not behave differently to how pip normally works when called from
a commandline window. Installing very large packages can take a long time.
As with pip, installing binary C, C#, or C++ packages will only work if
you have a compiler, and know all sorts of tech-wizardry. 

## Installation

Make pypi available by putting the folder anywhere it can be imported (eg site-packages).

Note: Comes pre-packaged with pip and will automatically install the necessary setuptools package
the first time you import pypi if you don't already have setuptools.

## Import

Import as pypi:

```
import pypi
```

## Usage

Download packages from the pypi website (ala pip install)

```
pypi.install("somepackage")
```

If you just want to upgrade an existing package, use "-U" as secondary
argument, and/or a series of other valid pip-options.

```
pypi.install("somepackage", "-U", "--no-compile")
```

As with pip, you can also specify links to github-repository .zip files or a
path to a local setup.py, .tar.gz, or .egg file.

```
pypi.install("https://github.com/packageauthor/packagename/archive/master.zip")
```

Upload and share your own package to the pypi website. 

```
pypi.login("myusername", "mypassword")
pypi.define_upload(package="C:/MyPackageFolder",
                    name="MyPackageFolder",
                    version="0.1",
                    license="MIT",
                    ...)
pypi.upload("C:/MyPackageFolder")
pypi.logout()
```

When defining your upload use the traditional arguments from distutils.core.setup.
For testing your upload at the test website, use upload_test(...) instead.     
    

## Functions and Classes

### pypi.define_upload(...):
Define and prep a package for upload by creating the necessary files
(in the parent folder containing the package's meta-data).

- package: the path location of the package you wish to upload (i.e. the folder containing the actual code, not the meta-folder)
- version: the version of the upload (as a string)
- license: the name of the license for your package ('MIT' will automatically create an MIT license.txt file in your package)

- **more_info: optional keyword arguments for defining the upload (see distutils.core.setup for valid arguments)

### pypi.install(...):
Install a package from the IDLE, same way as using the commandline
and typing "pip install ..." Any number of additional string arguments
specify the install options that typically come after, such as "-u"
for update. See pip-documentation for valid option strings. 

### pypi.login(...):
Creates the .pypirc file with login info (required in order to upload).
The login (i.e. the file) persists until you call the logout function. 

Note: Assumes same login info for both the testsite
and the live site, so if different must login for each switch.

### pypi.logout(...):
Deletes the .pypirc file with your login info.
Requires you to login again before uploading
another package. 

### pypi.upload(...):
Upload and distribute your package
to the online PyPi website in a single
command, so others can find it more
easily and install it using pip.

### pypi.upload_test(...):
Upload and distribute your package
to the online PyPi Testing website in a single
command, to test if your real upload will
work nicely or not.

