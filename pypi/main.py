
import sys, os
import datetime


pippath = __file__
pippath_folder, filename = os.path.split(pippath)


try:
    import setuptools
except ImportError:
    print("Installing setuptools...")
    # install setuptools
    setuptools_path = '"%s"' %os.path.join(pippath_folder, "ez_setup.py")
    python_folder = os.path.split(sys.executable)[0]
    python_exe = os.path.join(python_folder, "python")
    os.system(" ".join([python_exe, setuptools_path]) )
    # update systempath to look inside setuptools.egg, so don't have to restart python
    sitepackfolder = os.path.join(os.path.split(sys.executable)[0], "Lib", "site-packages")
    for filename in os.listdir(sitepackfolder):
        if filename.startswith("setuptools") and filename.endswith(".egg"):
            sys.path.append(os.path.join(sitepackfolder, filename))
            break

# add current precompiled pip folder to path for later import
sys.path.insert(0, pippath_folder)

###################################

def _commandline_call(action, package, *options):
    # (works on Windows, but needs to be tested on other OS)
    import pip
    from pip import main
    # find the main python executable
    python_folder = os.path.split(sys.executable)[0]
    python_exe = os.path.join(python_folder, "python") # use the executable named "python" instead of "pythonw"
    args = [python_exe]
    # detect installation method (local setup.py VS online pip)
    if package.endswith("setup.py"):
        # local "python setup.py install"
        os.chdir(os.path.split(package)[0]) # changes working directory to setup.py folder
        args.append("setup.py")
        args.append(action)
    else:
        # online "pip install packageorfile"
        if action == "build":
            raise Exception("Build can only be done on a local 'setup.py' filepath, not on '%s'" % package)
        # if github url, auto direct to github master zipfile
        # ...(bleeding edge, not stable release)
        if package.startswith("https://github.com") and not package.endswith((".zip",".gz")):
            if not package.endswith("/"): package += "/"
            package += "archive/master.zip"
        pip_path = os.path.abspath(os.path.split(pip.__file__)[0]) # get entire pip folder path, not the __init__.py file
        args.append('"%s"'%pip_path)
        args.append(action)
        args.append(package)
    # options
    args.extend(options)
    # pause after
    args.append("& pause")
    # send to commandline
    os.system(" ".join(args) ) #os.system('"%s" "%s" '%(python_exe,pip_path) + " ".join(args) + " & pause")

def install(package, *options):
    """
    Install a package from within the IDLE, same way as using the commandline
    and typing "pip install ..." Any number of additional string arguments
    specify the install options that typically come after, such as "-U"
    for update. See pip-documentation for valid option strings. 
    """
    _commandline_call("install", package, *options)

def build(package, *options):
    """
    Test if a local C/C++ package will build (aka compile)
    successfully without actually installing it (ie placing it in
    site-packages), from within the IDLE. Same way as using the commandline
    and typing "pip build ..." Any number of additional string arguments
    specify the build options that typically come after.
    See pip-documentation for valid option strings. 
    """
    _commandline_call("build", package, *options)

def uninstall(package, *options):
    """
    Uninstall a package from within the IDLE, same way as using the commandline
    and typing "pip uninstall ..." Any number of additional string arguments
    specify the uninstall options that typically come after.
    See pip-documentation for valid option strings. 
    """
    _commandline_call("uninstall", package, *options)
    
def login(username, password):
    """
    Creates the .pypirc file with login info (required in order to upload).
    The login (i.e. the file) persists until you call the logout function. 
    
    Note: Assumes same login info for both the testsite
    and the live site, so if different must login for each switch.
    """
    # if still not recognize login bug
    # change to http://stackoverflow.com/questions/1569315/setup-py-upload-is-failing-with-upload-failed-401-you-must-be-identified-t/1569331#1569331
    pypircstring = ""
    pypircstring += "[distutils]" + "\n"
    pypircstring += "index-servers = " + "\n"
    pypircstring += "\t" + "pypi" + "\n"
    pypircstring += "\t" + "testpypi" + "\n"
    pypircstring += "\n"
    pypircstring += "[pypi]" + "\n"
    pypircstring += "repository: https://pypi.python.org/pypi" + "\n"
    pypircstring += "username: " + username + "\n"
    pypircstring += "password: " + password + "\n"
    pypircstring += "\n"
    pypircstring += "[testpypi]" + "\n"
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

def define_upload(package, description, license, **more_info):
    """
    Define and prep a package for upload by creating the necessary files
    (in the parent folder containing the package's meta-data).
    
    - package: the path location of the package you wish to upload (i.e. the folder containing the actual code, not the meta-folder) or the module file (with the .py extension)
    - description: a short sentence describing the package
    - license: the name of the license for your package ('MIT' will automatically create an MIT license.txt file in your package)
    
    - **more_info: optional keyword arguments for defining the upload (see distutils.core.setup for valid arguments)
    
    """
    more_info.update(description=description, license=license)

    # absolute path
    package = os.path.abspath(package)
    
    # autofill "packages" or "py_modules" in case user didnt specify it
    folder , name = os.path.split(package)
    name, ext = os.path.splitext(name)
    if os.path.isdir(package) and not more_info.get("packages"):
        more_info["packages"] = [name]
    elif os.path.isfile(package) and not more_info.get("py_modules"):
        more_info["py_modules"] = [name]
    
    # autofill "name" in case user didnt specify it
    # ...this is taken from the repository folder name,
    # ...not the package/import name.
    if not more_info.get("name"): more_info["name"] = folder

    # autofill "version" in case user didnt specify it
    if not more_info.get("version"):
        # determine file to read
        if os.path.isdir(package):
            topfile = os.path.join(package, "__init__.py")
        else:
            topfile = package
        # find line that starts with __version__
        # ...NOTE: inspired by Sean Gillies' Fiona setup.py
        with open(topfile) as fileobj:
            for line in fileobj:
                if line.startswith("__version__"):
                    version = line.split("=")[1].strip()
                    version = version.strip('"')
                    version = version.strip("'")
                    more_info["version"] = version
                    break
        # raise error if none found
        if not more_info.get("version"):
            raise Exception("""Version argument can only be omitted if your
                            package's __init__.py file or module file contains
                            a __version__ variable.""")
                
            
    
    # make prep files
    _make_readme(package)
    _make_gitpack()
    _make_setup(package, **more_info)
    _make_cfg(package)
    _make_license(package, license, more_info.get("author") )
    print("package metadata prepped for upload")

def generate_docs(package, docfilter=["Module", "Class", "Function"],
                  html_no_source=True, **kwargs):
    """
    Generates full API html docs of all submodules to "buil/doc" folder.
    You do not have to use this function on your own since it
    will be run automatically when uploading your package (assuming
    that autodoc is set to True). However, this function can be used
    for making sure the docs look good before uploading. 
    """
    # absolute path
    package = os.path.abspath(package)
    ###
    _make_docs(package, docfilter=docfilter, html_no_source=html_no_source,
               **kwargs)

def upload_test(package):
    """
    Upload and distribute your package
    to the online PyPi Testing website in a single
    command, to test if your real upload will
    work nicely or not.
    """
    # absolute path
    package = os.path.abspath(package)
    ###
    folder,name = os.path.split(package)
    # first remember to update the readme, in case docstring changed
    _make_readme(package)
    # then try registering
    # instead of typing "python setup.py register -r testpypi" in commandline
    print("registering package (test)")
    setup_path = os.path.join(folder, "setup.py")
    options = ["-r", "testpypi"]
    _commandline_call("register", setup_path, *options)
    # then try uploading
    # instead of typing "python setup.py sdist upload -r testpypi" in commandline
    print("uploading package (test)")
    setup_path = os.path.join(folder, "setup.py")
    options = ["upload", "-r", "testpypi"]
    _commandline_call("sdist", setup_path, *options)
   
def upload(package, autodoc=True):
    """
    Upload and distribute your package
    to the online PyPi website in a single
    command, so others can find it more
    easily and install it using pip.
    """
    # absolute path
    package = os.path.abspath(package)
    ###
    folder,name = os.path.split(package)
    # first remember to update the readme, in case docstring changed
    _make_readme(package)
    # then try registering
    # instead of typing "python setup.py register -r pypi" in commandline
    print("registering package")
    setup_path = os.path.join(folder, "setup.py")
    options = ["-r", "pypi"]
    _commandline_call("register", setup_path, *options)
    # then try uploading
    # instead of typing "python setup.py sdist upload -r pypi" in commandline
    print("uploading package")
    setup_path = os.path.join(folder, "setup.py")
    options = ["upload", "-r", "pypi"]
    _commandline_call("sdist", setup_path, *options)
    
##    # set parameters
##    sys.argv = [setup_path, "register", "-r", "pypi"]
##    # then run setup.py to register package online
##    print("registering package online")
##    _execute_setup(setup_path)
##    # then upload the package
##    print("uploading package")
##    sys.argv = [setup_path, "sdist", "upload", "-r", "pypi"]
##    _execute_setup(setup_path)
##    print("package successfully uploaded")
    
    # finally try generating and uploading documentation
    if autodoc:
        _make_docs(package)
        print("documentation successfully generated")
        _upload_docs(package)
        print("documentation successfully uploaded to pythonhosted.org")







# Internal use only

def _make_readme(package):
    # assumes readme should be based on toplevel package docstring
    import ipandoc # comes packaged in the pypi folder
    folder,name = os.path.split(package)
    name,ext = os.path.splitext(name)
    # get toplevel package docstring
    import imp
    modinfo = imp.find_module(name,[folder])
    mod = imp.load_module(name, *modinfo)
    mdstring = mod.__doc__
    # use ipandoc to convert assumed markdown string to rst for display on pypi
    if mdstring:
        rststring = ipandoc.convert(mdstring, "markdown", "rst")
        readmepath = os.path.join(folder, "README.rst")
        with open(readmepath, "w") as readme:
            readme.write(rststring)

def _make_docs(package, **kwargs):
    # uses pdoc to generate html folder
    # ...TODO: Clean up this section, very messy
    
    # if pdoc not available, install it
    try:
        import pdoc
    except ImportError:
        install("pdoc")

    # non commandline approach
    # ...allowing for docfilter option
    folder,name = os.path.split(package)
    name,ext = os.path.splitext(name)
    docfolder = kwargs.get("html_dir")
    if not docfolder:
        docfolder = os.path.join(folder, "build", "doc")
    # get toplevel package docstring
    import imp
    modinfo = imp.find_module(name,[folder])
    mod = imp.load_module(name, *modinfo)
    # prep pdoc paramters
    mod_kwargs = dict([item for item in kwargs.items() if item[0] in ("docfilter","allsubmodules")])
    # docfilter, either list of type strings or function
    if isinstance(mod_kwargs.get("docfilter"), (list,tuple)):
        def docfilter(obj, filtertypes=mod_kwargs["docfilter"]):
            return any(isinstance(obj, getattr(pdoc, filtertype))
                       for filtertype in filtertypes)
        mod_kwargs["docfilter"] = docfilter
    # remove module prose docstring, only show API classes, funcs, and meths
    mod.__doc__ = """
                  # **API Documentation**
                  """
    # html params
    mod = pdoc.Module(mod, **mod_kwargs)
    html_kwargs = dict([item for item in kwargs.items() if item[0] in ("external_links","link_prefix","html_no_source")])
    if html_kwargs.get("html_no_source"):
        html_kwargs["source"] = not html_kwargs.pop("html_no_source")
    # get and write to files
    if mod.is_package():
        def html_out_package(mod):
            # create output folders
            modtree = mod.name.split('.')
            # remove top package name, to avoid yet another nested folder
            modtree.pop(0) 
            mbase = os.path.join(docfolder, *modtree)
            if mod.is_package():
                outpath = os.path.join(mbase, pdoc.html_package_name)
            else:
                outpath = '%s%s' % (mbase, pdoc.html_module_suffix)
            dirpath = os.path.dirname(outpath)
            if not os.path.lexists(dirpath):
                os.makedirs(dirpath)
            # write html
            with open(outpath, 'w') as writer:
                out = mod.html(**html_kwargs)
                writer.write(out)
            # do same for all submodules
            for submodule in mod.submodules():
                html_out_package(submodule)
        html_out_package(mod)
    else:
        # create output folders
        outpath = os.path.join(docfolder, "index.html")
        dirpath = os.path.dirname(outpath)
        if not os.path.lexists(dirpath):
            os.makedirs(dirpath)
        # write html
        with open(outpath, 'w') as writer:
            out = mod.html(**html_kwargs)
            writer.write(out)

##    # commandline approach
##    # find the main python executable
##    python_folder = os.path.split(sys.executable)[0]
##    python_exe = os.path.join(python_folder, "python") # use the executable named "python" instead of "pythonw"
##    args = [python_exe]
##    
##    # python pdoc_build.py --html packname --html-dir "path" --overwrite --external-links --html-no-source'
##    folder,name = os.path.split(package)
##    name,ext = os.path.splitext(name)
##    pdoc_path = os.path.join(os.path.split(__file__)[0], "pdoc_build.py") # comes packaged in the pypi folder
##    args.append(pdoc_path)
##    args.extend(["--html",'"%s"'%package]) # prefer full module/package path
##    os.chdir(folder) # changes working directory to setup.py folder
##    docfolder = os.path.join(folder, "build", "doc")
##    if not os.path.lexists(docfolder):
##        os.makedirs(docfolder)
##    args.extend(["--html-dir", docfolder])
##
##    # options
##    args.append("--overwrite")
##    args.append("--external-links")
##    args.append("--html-no-source")
##    #args.extend(options)
##    
##    # pause after
##    args.append("& pause")
##    
##    # send to commandline
##    os.system(" ".join(args) )

def _upload_docs(package):
    # instead of typing "python setup.py upload_docs" in commandline
    # by default uploads "build/doc" folder
    
    # NOTE: REQUIRES SETUP.PY TO USE SETUPTOOLS INSTEAD OF DISTUTILS
    # ...from setuptools import setup
    folder,name = os.path.split(package)
    os.chdir(folder)
    setup_path = os.path.join(folder, "setup.py")
    options=["--upload-dir=build/doc"]
    _commandline_call("upload_docs", setup_path, *options)

# doesnt work after all, since upload command does not allow username and password as args
##def _try_upload(setup_path, username, password):
##    if username and password:
##        sys.argv.extend([])
##        _execute_setup()
##    else:
##        # hope that pypirc file is set and works
##        _execute_setup()
##        # if not, ask for interactive login info and try again
##        username = input("Username")
##        password = input("Password")
##        _execute_setup()
##        pass

def _execute_setup(setup_path):
    setupfile = open(setup_path)
    if sys.version.startswith("3"):
        exec(compile(setupfile.read(), 'setup.py', 'exec'))
    else:
        exec(setupfile)

def _make_gitpack():
    # maybe in the future but not really necessary, for prepping and
    # allowing packages to be hosted directly from github
    pass

def _make_setup(package, **kwargs):
    folder,name = os.path.split(package)
    setupstring = ""
    setupstring += "try: from setuptools import setup" + "\n"
    setupstring += "except: from distutils.core import setup" + "\n"
    setupstring += "\n"
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
                setupstring += "\t" + 'long_description=open("%s").read(), '%filename + "\n"
                break

    # general options
    for param,value in kwargs.items():
        if param in ["packages", "classifiers", "platforms", "py_modules"]:
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
    if "README.rst" in os.listdir(folder):
        setupstring = """
[metadata]
description-file = README.rst
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
        
        writer = open(os.path.join(folder, "LICENSE.txt"), "w")
        writer.write(licensestring)
        writer.close()





