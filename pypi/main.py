
import subprocess
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
    
def define_upload(folder,
            name,
            version,
            licence,
            description,
            author,
            email,
            homepage,
            download,
            keywords):
    """
    Define and prep a package for upload
    by creating the necessary files
    """
    # first make prep files
    _make_gitpack()
    _make_setup(folder,
                name,
                version,
                description,
                author,
                email,
                homepage,
                download,
                keywords)
    _make_cfg(folder)
    _make_license(folder, licence)

def dryrun_upload(folder):
    """
    Upload and distribute your package
    to the online PyPi Testing website in a single
    command with includes and docs, to test
    if your real upload will work nicely or not.
    (Not yet working)
    """
    # then try uploading
    # instead of typing "python setup.py register -r pypitest" in commandline
    # set parameters as sysarg
    setup_path = os.path.join(folder, "setup.py")
    sys.argv = [setup_path, "register", "-r", "pypitest"]
    # then run setup.py
    rawcode = open(setup_path, "r").read()
    exec(rawcode)
    # then validate for no errors
    sys.argv = [setup_path, "sdist", "upload", "-r", "pypitest"]
    exec(rawcode)
    
##    # make commandline accessible from IDLE
##    python_path = os.path.split(sys.executable)[0]
##    os.system('PATH="%s"'%python_path)
##    # then run setup.py
##    os.system('python %s'%setup_path)
##    # then validate for no errors
##    sys.argv = [setup_path, "sdist", "upload", "-r", "pypitest"]
##    os.system('python %s'%setup_path)
    
def upload(folder):
    """
    Upload and distribute your package
    to the online PyPi website in a single
    command with includes and docs, so others
    can find it more easily and install
    it using pip.
    (Not yet working)
    """
    # then try uploading
    # instead of typing "python setup.py register -r pypitest" in commandline
    # set parameters as sysarg
    setup_path = os.path.join(folder, "setup.py")
    sys.argv = [setup_path, "register", "-r", "pypi"]
    # then run setup.py
    rawcode = open(setup_path, "r").read()
    exec(rawcode)
    # then validate for no errors
    sys.argv = [setup_path, "sdist", "upload", "-r", "pypi"]
    exec(rawcode)




# Internal use only

def _make_gitpack():
    pass

def _make_setup(folder,
                name,
                version,
                description,
                author,
                email,
                homepage,
                download,
                keywords):
    setupstring = ""
    setupstring += "from distutils.core import setup" + "\n"
    setupstring += "setup("
    setupstring += "\t" + 'name="%s",'%name + "\n"
    setupstring += "\t" + 'packages=["%s"],'%name + "\n"
    setupstring += "\t" + 'version="%s",'%version + "\n"
    setupstring += "\t" + 'description="%s",'%description + "\n"
    setupstring += "\t" + 'author="%s",'%author + "\n"
    setupstring += "\t" + 'author_email="%s",'%email + "\n"
    setupstring += "\t" + 'url="%s",'%homepage + "\n"
    setupstring += "\t" + 'download_url="%s",'%download + "\n"
    setupstring += "\t" + 'keywords=%s,'%keywords + "\n"
    setupstring += "\t" + "classifiers=[]" + "\n"
    setupstring += "\t" + ")" + "\n"
    writer = open(os.path.join(folder, "setup.py"), "w")
    writer.write(setupstring)
    writer.close()

def _make_cfg(folder):
    setupstring = """
[metadata]
description-file = README.md
"""
    writer = open(os.path.join(folder, "setup.cfg"), "w")
    writer.write(setupstring)
    writer.close()

def _make_license(folder, type="MIT"):
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




if __name__ == "__main__":
    define_upload(folder="C:\Users\kimo\Desktop\code",
                name="testcode",
                version="0.1",
                licence="MIT",
                description="",
                author="me",
                email="karim.bahgat.norway@gmail.com",
                homepage="",
                download="",
                keywords=["wakawaka"])

    dryrun_upload("C:\Users\kimo\Desktop\code")

