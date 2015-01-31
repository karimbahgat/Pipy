
import sys, os


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

def install(package):
    """
    Install a package from the IDLE,
    same way as using the commandline
    and typing "pip install ..."
    """
    from pip import main
    main(["install", package])

def login(username, password):
    """
    Creates the .pypirc file with login info (required in order to upload).
    Once logged in, no need to do it again ever. 
    
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
    # delete the .pypirc file for better security
    home = os.path.expanduser("~")
    path = os.path.join(home, ".pypirc")
    os.remove(path)
    print("logged out (.pypirc file removed)")

def define_upload(package, name, version, license, **more_info):
    """
    Define and prep a package for upload
    by creating the necessary files
    """
    more_info.update(name=name, version=version, license=license)
    # make prep files
    _make_gitpack()
    _make_setup(package, **more_info)
    _make_cfg(package)
    _make_license(package, license)
    print("package metadata prepped for upload")

def upload_test(package):
    """
    Upload and distribute your package
    to the online PyPi Testing website in a single
    command with includes and docs, to test
    if your real upload will work nicely or not.
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
    setupfile = open(setup_path, "r")
    try: exec(setupfile)
    except SystemExit as err: print err
    # then upload the package
    print("uploading package (test)")
    sys.argv = [setup_path, "sdist", "upload", "-r", "pypitest"]
    setupfile = open(setup_path, "r")
    try: exec(setupfile)
    except SystemExit as err: print err
    print("package successfully uploaded (test)")
   
def upload(package):
    """
    Upload and distribute your package
    to the online PyPi website in a single
    command with includes and docs, so others
    can find it more easily and install
    it using pip.
    (Not yet working)
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
    setupfile = open(setup_path, "r")
    try: exec(setupfile)
    except SystemExit as err: print err
    # then upload the package
    print("uploading package")
    sys.argv = [setup_path, "sdist", "upload", "-r", "pypi"]
    setupfile = open(setup_path, "r")
    try: exec(setupfile)
    except SystemExit as err: print err
    print("package successfully uploaded")







# Internal use only

def _make_gitpack():
    pass

def _make_setup(package, **kwargs):
    folder,name = os.path.split(package)
    setupstring = ""
    setupstring += "from distutils.core import setup" + "\n"
    setupstring += "setup("

    for param,value in kwargs.items():
        if param in ["classifiers", "platforms"]:
            valuelist = value
            setupstring += "\t" + '%s=%s,'%(param,valuelist) + "\n"
        else:
            setupstring += "\t" + '%s="%s",'%(param,value) + "\n"
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

def _make_license(package, type="MIT"):
    folder,name = os.path.split(package)
    if type == "MIT":
        licensestring = """
The MIT License (MIT)

Copyright (c) <year> <copyright holders>

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
"""
        writer = open(os.path.join(folder, "license.txt"), "w")
        writer.write(licensestring)
        writer.close()





