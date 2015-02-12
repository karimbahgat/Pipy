
import sys, os
import datetime


pippath = __file__
pippath_folder, filename = os.path.split(pippath)


try:
    import setuptools
except ImportError:
    print("Installing setuptools...")
    # install setuptools
    setuptools_path = os.path.join(pippath_folder, "ez_setup.py")
    python_path = os.path.split(sys.executable)[0]
    os.system('PATH="%s"'%python_path)
    os.system('python "%s"'%setuptools_path)
    # update systempath to look inside setuptools.egg, so don't have to restart python
    sitepackfolder = os.path.join(os.path.split(sys.executable)[0], "Lib", "site-packages")
    for filename in os.listdir(sitepackfolder):
        if filename.startswith("setuptools") and filename.endswith(".egg"):
            sys.path.append(os.path.join(sitepackfolder, filename))
            break

# add current precompiled pip folder to path for later import
sys.path.insert(0, pippath_folder)

###################################

def install(package, *options):
    """
    Install a package from the IDLE, same way as using the commandline
    and typing "pip install ..." Any number of additional string arguments
    specify the install options that typically come after, such as "-u"
    for update. See pip-documentation for valid option strings. 
    """
    from pip import main
    args = ["install", package]
    args.extend(options)
    main(args)

def login(username, password):
    """
    Creates the .pypirc file with login info (required in order to upload).
    The login (i.e. the file) persists until you call the logout function. 
    
    Note: Assumes same login info for both the testsite
    and the live site, so if different must login for each switch.
    """
    pypircstring = ""
    pypircstring += "[distutils]" + "\n"
    pypircstring += "index-servers = " + "\n"
    pypircstring += "\t" + "pypi" + "\n"
    pypircstring += "\t" + "pypitest" + "\n"
    pypircstring += "\n"
    pypircstring += "[pypi]" + "\n"
    pypircstring += "repository: https://pypi.python.org/pypi" + "\n"
    pypircstring += "username: " + username + "\n"
    pypircstring += "password: " + password + "\n"
    pypircstring += "\n"
    pypircstring += "[pypitest]" + "\n"
    pypircstring += "repository: https://testpypi.python.org/pypi" + "\n"
    pypircstring += "username: " + username + "\n"
    pypircstring += "password: " + password + "\n"
    # create the file
    home = os.path.expanduser("~")
    path = os.path.join(home, ".pypirc")
    writer = open(path, "w")
    writer.write(pypircstring)
    writer.close()
    print("logged in")

def logout():
    """
    Deletes the .pypirc file with your login info.
    Requires you to login again before uploading
    another package. 
    """
    # delete the .pypirc file for better security
    home = os.path.expanduser("~")
    path = os.path.join(home, ".pypirc")
    os.remove(path)
    print("logged out (.pypirc file removed)")

def define_upload(package, version, license, **more_info):
    """
    Define and prep a package for upload by creating the necessary files
    (in the parent folder containing the package's meta-data).
    
    - package: the path location of the package you wish to upload (i.e. the folder containing the actual code, not the meta-folder)
    - version: the version of the upload (as a string)
    - license: the name of the license for your package ('MIT' will automatically create an MIT license.txt file in your package)
    
    - **more_info: optional keyword arguments for defining the upload (see distutils.core.setup for valid arguments)
    
    """
    more_info.update(version=version, license=license)
    
    # autofill "packages" in case user didnt specify it
    folder , name = os.path.split(package)
    if not more_info.get("packages"): more_info["packages"] = [name]
    
    # autofill "name" in case user didnt specify it
    if not more_info.get("name"): more_info["name"] = name
    
    # make prep files
    _make_gitpack()
    _make_setup(package, **more_info)
    _make_cfg(package)
    _make_license(package, license, more_info.get("author") )
    print("package metadata prepped for upload")

def upload_test(package):
    """
    Upload and distribute your package
    to the online PyPi Testing website in a single
    command, to test if your real upload will
    work nicely or not.
    """
    folder,name = os.path.split(package)
    # then try uploading
    # instead of typing "python setup.py register -r pypitest" in commandline
    os.chdir(folder)
    # set parameters as sysarg
    setup_path = os.path.join(folder, "setup.py")
    sys.argv = [setup_path, "register", "-r", "pypitest"]
    # then run setup.py to register package online
    print("registering package online (test)")
    try: _execute_setup(setup_path)
    except SystemExit as err: print(err)
    # then upload the package
    print("uploading package (test)")
    sys.argv = [setup_path, "sdist", "upload", "-r", "pypitest"]
    try: _execute_setup(setup_path)
    except SystemExit as err: print(err)
    print("package successfully uploaded (test)")
   
def upload(package):
    """
    Upload and distribute your package
    to the online PyPi website in a single
    command, so others can find it more
    easily and install it using pip.
    """
    folder,name = os.path.split(package)
    # then try uploading
    # instead of typing "python setup.py register -r pypitest" in commandline
    os.chdir(folder)
    # set parameters as sysarg
    setup_path = os.path.join(folder, "setup.py")
    sys.argv = [setup_path, "register", "-r", "pypi"]
    # then run setup.py to register package online
    print("registering package online")
    try: _execute_setup(setup_path)
    except SystemExit as err: print(err)
    # then upload the package
    print("uploading package")
    sys.argv = [setup_path, "sdist", "upload", "-r", "pypi"]
    try: _execute_setup(setup_path)
    except SystemExit as err: print(err)
    print("package successfully uploaded")







# Internal use only

def _execute_setup(setup_path):
    setupfile = open(setup_path, "r")
    if sys.version.startswith("3"):
        exec(compile(setupfile.read(), 'setup.py', 'exec'))
    else:
        exec(setupfile)

def _make_gitpack():
    pass

def _make_setup(package, **kwargs):
    folder,name = os.path.split(package)
    setupstring = ""
    setupstring += "from distutils.core import setup" + "\n\n"
    setupstring += "setup("

    # description/readme info
    long_description = kwargs.pop("long_description", None)   
    if long_description:
        setupstring += "\t" + 'long_description="""%s""",'%long_description + "\n"
    else:
        # make the setup.py script dynamically autofill "long_description"
        # ...from README in case user didnt specify it
        for filename in os.listdir(folder):
            if filename.startswith("README"):
                readmepath = os.path.join(folder, filename)
                setupstring += "\t" + 'long_description=open("%s").read(), '%readmepath + "\n"
                break

    # general options
    for param,value in kwargs.items():
        if param in ["packages", "classifiers", "platforms"]:
            valuelist = value
            setupstring += "\t" + '%s=%s,'%(param,valuelist) + "\n"
        else:
            setupstring += "\t" + '%s="""%s""",'%(param,value) + "\n"
        
    setupstring += "\t" + ")" + "\n"
        
##    setupstring += "\t" + 'name="%s",'%name + "\n"
##    setupstring += "\t" + 'packages=["%s"],'%name + "\n"
##    setupstring += "\t" + 'version="%s",'%version + "\n"
##    setupstring += "\t" + 'description="%s",'%description + "\n"
##    setupstring += "\t" + 'author="%s",'%author + "\n"
##    setupstring += "\t" + 'author_email="%s",'%email + "\n"
##    setupstring += "\t" + 'url="%s",'%homepage + "\n"
##    setupstring += "\t" + 'download_url="%s",'%download + "\n"
##    setupstring += "\t" + 'keywords=%s,'%keywords + "\n"
##    setupstring += "\t" + "classifiers=[]" + "\n"
##    setupstring += "\t" + ")" + "\n"
    
    writer = open(os.path.join(folder, "setup.py"), "w")
    writer.write(setupstring)
    writer.close()

def _make_cfg(package):
    folder,name = os.path.split(package)
    if "README.md" in os.listdir(folder):
        setupstring = """
[metadata]
description-file = README.md
"""
        writer = open(os.path.join(folder, "setup.cfg"), "w")
        writer.write(setupstring)
        writer.close()

def _make_license(package, type="MIT", author=None):
    if not author: author = ""
    folder,name = os.path.split(package)
    if type == "MIT":
        licensestring = """
The MIT License (MIT)

Copyright (c) %i %s

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
""" % (datetime.datetime.today().year, author)
        
        writer = open(os.path.join(folder, "license.txt"), "w")
        writer.write(licensestring)
        writer.close()





