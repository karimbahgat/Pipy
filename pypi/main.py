
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
        package = os.path.abspath(package) # absolute path
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
    os.system(" ".join(args) ) 

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

def define_upload(package, description, license, changes, **more_info):
    """
    Define and prep a package for upload by creating the necessary files
    (in the parent folder containing the package's meta-data).
    
    - package: the path location of the package you wish to upload (i.e. the folder containing the actual code, not the meta-folder) or the module file (with the .py extension)
    - description: a short sentence describing the package
    - license: the name of the license for your package ('MIT' will automatically create an MIT license.txt file in your package)
    - changes: list of change descriptions in the current upload version, used to create a changes.txt file and automatically include as a changelog in the README. 
    - **more_info: optional keyword arguments for defining the upload (see distutils.core.setup for valid arguments)
    
    """
    more_info.update(description=description, license=license)

    # absolute path
    package = os.path.abspath(package)
    
    # disect path
    folder , name = os.path.split(package)
    name, ext = os.path.splitext(name)

    # autofill "packages" in case user didnt specify it
    # ...toplevel and all subpackages
    if os.path.isdir(package) and not "packages" in more_info:
        subpacks = []
        for dirr,_,files in os.walk(package):
            reldirr = os.path.relpath(dirr, folder)
            if "__init__.py" in files:
                subpacks.append(reldirr)
        more_info["packages"] = subpacks

    # autofill "py_modules" in case user didnt specify it
    elif os.path.isfile(package) and not "py_modules" in more_info:
        more_info["py_modules"] = [name]

    # autofill "package_data" arg in case user didnt specify
    if os.path.isdir(package) and not "package_data" in more_info:
        data = []
        for dirr,_,files in os.walk(package):
            reldirr = os.path.relpath(dirr, package)
            # look for data
            data += [os.path.join(reldirr,filename)
                     for filename in files
                     if not filename.endswith((".py",".pyc"))]
        if data:
            package_data = dict([(name, data)])
            more_info["package_data"] = package_data

    # autofill "name" in case user didnt specify it
    # ...this is taken from the repository folder name,
    # ...not the package/import name.
    if not "name" in more_info: more_info["name"] = folder

    # autofill "version" in case user didnt specify it
    if not "version" in more_info:
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
        if not "version" in more_info:
            raise Exception("""Version argument can only be omitted if your
                            package's __init__.py file or module file contains
                            a __version__ variable.""")
    
    # make prep files
    _make_changelog(package, version, changes)
    _make_readme(package)
    _make_gitpack()
    _make_setup(package, **more_info)
    _make_cfg(package)
    _make_license(package, license, more_info.get("author") )
    print("package metadata prepped for upload")

def generate_docs(package, **kwargs):
    """
    Generates full API html docs of all submodules to "build/doc" folder.
    You do not have to use this function on your own since it
    will be run automatically when uploading your package (assuming
    that autodoc is set to True). However, this function can be used
    for making sure the docs look good before uploading. 
    """
    # absolute path
    package = os.path.abspath(package)
    ###
    _make_docs(package, **kwargs)
    print("documentation successfully generated")

def upload_docs(package, **kwargs):
    """
    Upload documentation html docs located in "build/doc" folder.
    """
    # absolute path
    package = os.path.abspath(package)
    ###
    _upload_docs(package, **kwargs)
    print("documentation successfully uploaded to pythonhosted.org")

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
    
    # finally try generating and uploading documentation
    if autodoc:
        generate_docs(package)
        upload_docs(package)







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
    if mdstring:
        # add changes text to mdstring (so it will be included in readme)
        changespath = os.path.join(folder, "CHANGES.txt")
        with open(changespath) as changesfile:
            for line in changesfile.readlines():
                mdstring += line
        # use ipandoc to convert assumed markdown string to rst for display on pypi
        rststring = ipandoc.convert(mdstring, "markdown", "rst")
        readmepath = os.path.join(folder, "README.rst")
        with open(readmepath, "w") as readme:
            readme.write(rststring)

def _make_docs(package, **kwargs):
    # uses pdoc to generate html folder
    # ...TODO: Clean up this section, very messy

    # set some defaults
    if not kwargs.get("docfilter"):
        kwargs["docfilter"] = ["Module", "Class", "Function"]
    if kwargs.get("html_no_source") == None:
        kwargs["html_no_source"] = True
    
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

def _upload_docs(package, **kwargs):
    # instead of typing "python setup.py upload_docs" in commandline
    # by default uploads "build/doc" folder
    
    # NOTE: REQUIRES SETUP.PY TO USE SETUPTOOLS INSTEAD OF DISTUTILS
    # ...from setuptools import setup
    folder,name = os.path.split(package)
    os.chdir(folder)
    setup_path = os.path.join(folder, "setup.py")
    upload_dir = kwargs.get("upload_dir", "build/doc")
    options = ["--upload-dir=%s" % upload_dir]
    _commandline_call("upload_docs", setup_path, *options)

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

def _make_changelog(package, version, changes):
    folder,name = os.path.split(package)
    changespath = os.path.join(folder, "CHANGES.txt")

    # if changes file already exists
    if os.path.exists(changespath):

        # read in existing changes file
        rawlines = open(changespath).readlines()
        rawlines = (line for line in rawlines)

        # how to detect version start
        def detectversion(_line):
            # ignore strings "version" and "v"
            _line = _line.lower().replace("version","").replace("v","")
            _line = _line.strip()
            if _line:
                # ignore anything after parentheses (such as version date)
                _split = _line.split("(")
                if len(_split) >= 2:
                    _line,_date = _split[:2]
                    _date = _date.rstrip(")")
                else:
                    _line,_date = _split[0],None
                # is version line if all chars on line are nrs or symbols (eg dots, spaces, or hashtags), so can build on existing changes files, though it will reformat it.
                if all(char.isdigit() or not char.isalpha() for char in _line):
                    # clean version string by stripping away anything that is not number or dot
                    _line = "".join([char for char in _line if char.isdigit() or char == "."])
                    return _line,_date

        # parse into version-changes dict
        versiondict = dict()
        line = next(rawlines, None)
        while line:
            # detect version start
            _versionresult = detectversion(line)
            if _versionresult: 
                # collect change lines until next version start
                _version,_date = _versionresult
                _changes = []
                line = next(rawlines, None)
                while line != None and not detectversion(line):
                    line = line.strip()
                    if line:
                        # clean change string by stripping away from the left any non letter characters
                        firstcharindex = next( (line.index(char) for char in line if char.isalpha()) )
                        line = line[firstcharindex:]
                        _changes.append(line)
                    line = next(rawlines, None)
                # add to versiondict
                versiondict[_version] = dict(date=_date, changes=_changes)
            else:
                line = next(rawlines, None)

        # add current version to versiondict, overwriting/updating if already exists
        versiondict[version] = dict(date=datetime.date.today(), changes=changes)
        
        # write to new updated changes file
        writer = open(changespath, "w")
        writer.write("\n"+"## Changes"+"\n")
        for version in sorted(versiondict.keys(),
                              key=lambda x: map(int, x.split(".")), # sort on each version nr as int not str
                              reverse=True):
            versionstring = version
            date = versiondict[version]["date"]
            if date: versionstring += " (%s)"%date
            changes = versiondict[version]["changes"]
            writer.write("\n"+"### "+versionstring+"\n\n")
            for change in changes:
                writer.write("- "+change+"\n")
        writer.close()

    else:
        # no changes file exists, write current changes to a new document
        writer = open(changespath, "w")
        writer.write("\n"+"## Changes"+"\n")
        versionstring = version
        date = datetime.date.today()
        if date: versionstring += " (%s)"%date
        writer.write("\n"+"### "+versionstring+"\n\n")
        for change in changes:
            writer.write("- "+change+"\n")
        writer.close()

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
        if param in ["packages", "classifiers", "platforms",
                     "py_modules", "requires", "data_files",
                     "package_data"]:
            valuelist = value
            # paths should be crossplatform
            if param in ["packages", "py_modules"]:
                valuelist = [path.replace("\\","/") for path in valuelist]
            elif param in ["package_data", "data_files"]:
                valuelist = dict([ (
                                    folder.replace("\\","/"),
                                    [path.replace("\\","/") for path in pathlist]
                                    )
                                   for folder,pathlist in valuelist.items()
                                   ])
            # write valuelist as list
            setupstring += "\t" + '%s=%s,'%(param,valuelist) + "\n"
        else:
            # write single values enclosed in quote marks
            setupstring += "\t" + '%s="""%s""",'%(param,value) + "\n"
            
    setupstring += "\t" + ")" + "\n"
    
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





