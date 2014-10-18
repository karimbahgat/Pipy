
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
    
def upload():
    """
    Upload and distribute your package
    to the online PyPi website in a single
    command with includes and docs, so others
    can find it more easily and install
    it using pip.
    (Not yet working)s
    """
    pass



