PyPi
====

Install or upload your Python packages from/to the PyPi package index
website. Easy to use, IDLE/shell access, and no dependencies.

PyPi is a one-stop tool for all your package needs. It is meant to be
dead-set simple, easy for beginners, and you never have to leave your
code editor. Its main features can be summarized as:

-  install with pypi.install(package).
-  for each package you wish to share:

   -  write an introduction text inside your toplevel module in
      Markdown.
   -  write docstrings for all your classes, functions, and methods in
      Markdown.
   -  create an upload.py script, and run it!

Motivation (LONG VERSION)
-------------------------

Python has received some criticism for its lack of a builtin easy to use
package management system, for both installing new packages,
uploading/sharing your own work, an d.

Installing
~~~~~~~~~~

Pip in itself is an easy and great tool in my opinion. The problem with
pip is that until Python 2.7 you had to download and get pip separately,
which was ironically enough difficult. The situation is much better now
that it is part of the standard library, but is still somewhat hindered
by the fact that it is restricted to being a commandline tool (see
below).

Uploading
~~~~~~~~~

There are numerous reports of frustration with PyPi: ... So much that
unofficial guides on using it is necessary: ... Regardless, as seen even
in the simplified guides, the steps are many, spanning the creation of
multiple files and configurations and require lengthy explanation and
understanding.

Documenting
~~~~~~~~~~~

Readme
^^^^^^

Writing READMEs in markdown is really easy and has become quite popular
due to GitHub supporting it. However PyPi still only accepts reST,
despite calls for change and some progress being made. #### Code
docstrings Many types of markup languages and in-code standards... ####
API Sphinx huge and lots of config, not builtin. Pydoc builtin but very
outdated. #### Docs hosting Even after creating documentation it is not
straightforward how to get it online along with your package.

The commandline
~~~~~~~~~~~~~~~

This next point is more of a personal opinion, and many might disagree
with me. Speaking as a recent Python beginner myself and for the sake of
other beginners, an additional impedement to all of these tasks is the
fact that all solutions are limited to the commandline only, with the
implied extra setup and learning curve that comes with that such as
adding paths to environment variables, or managing multiple versions of
Python. My feeling is that use of the commandline is a highly personal
and individual preference, usually only by hard scientists, people in
technical positions or who frequently use Python in the workplace, or
who have years of experience or a passion for computers. It is sometimes
just taken for granted that beginners should know how to or feel
comfertable using the commandline. For advanced users and beginners
alike, the fact that one has to switch away from the main code editor
for some tasks but not others adds conceptual overhead and potential
confusion, and brings in a lot of OS specific contingencies and
challenges.

The Bottom Line
---------------

I'm sorry but this just isn't okay. Tired of feeling frustrated by it, I
decided to do something. And so the PyPi package was born. It started
out small, but has now grown to incorporate all major aspects of package
management in one lightweight and easy to use package: installing,
documenting, and uploading. Primarily for my own use, this is the only
way I handle packages and it was the turning stone that made it fun to
install new packages and finally allowed me to share my work on the PyPi
website.

Other auto tools
----------------

Admittedly, there are other auto tools out there already. However, these
tend to focus only on one or parts of the steps mentioned here, and as
usual are almost exclusively commandline centered. For instance:

-  https://github.com/michaeljoseph/changes
-  http://seed.readthedocs.org/en/latest/
-  Also zest.releaser...
-  Maybe more at
   https://opensourcehacker.com/2012/08/14/high-quality-automated-package-releases-for-python-with-zest-releaser/

These may have advantages of their own, but with pypi you can have all
of the steps gathered in one package, and can run them from within the
Python IDLE shell or automate it in a Python script, which is
particularly useful for beginners or those who prefer to stay away from
the commandline.

Karim Bahgat, 2015

Disclaimer
----------

This package has no relation to the makers of PyPi or pip, and may or
may not behave differently to how pip normally works when called from a
commandline window. Installing very large packages can take a long time.
As with pip, installing binary C, C#, or C++ packages will only work if
you have a compiler, and know all sorts of tech-wizardry.

Installation
------------

Make pypi available by putting the folder anywhere it can be imported
(eg site-packages).

Note: Comes pre-packaged with pip and will automatically install the
necessary setuptools package the first time you import pypi if you don't
already have setuptools.

Import
------

Import as pypi:

::

    import pypi

Usage
-----

Installing packages
~~~~~~~~~~~~~~~~~~~

Download packages from the pypi website (ala pip install)

::

    pypi.install("packagename")

If you just want to upgrade an existing package, use "-U" as secondary
argument, and/or a series of other valid pip-options.

::

    pypi.install("somepackage", "-U", "--no-compile")

As with pip, you can also specify links to either online urls or local
filepaths to .zip, .tar.gz, .egg, or .whl files. You can even link it to
the home page of a GitHub repository and it will grab the newest master
file.

::

    pypi.install("https://github.com/packageauthor/packagename")

Documenting packages
~~~~~~~~~~~~~~~~~~~~

PyPi can be used to automatically document your package by scanning all
of your scripts and creating a complete set of linked html files of the
contents of your package, with a modern and sleek design. Currently it
focuses only on creating an API reference (an overview of functions,
classes, and methods). Upon uploading your package, these API reference
files will be automatically sent and hosted for public viewing at
www.pythonhosted.org/yourpackage.

Longer text such as the name, introduction, installation, and basic
usage should all be written in your package's top level docstring. When
defining your setup script and updated at upload-time, PyPi will take
the top level docstring, and convert and write it to a README file in
reStructuredText that can be properly rendered on both Pypi.org and
GitHub.

As far as documentation formatting goes, PyPi uses the excellent
up-and-coming `pdoc <>`__ package, which looks for Markdown formatting
in order to style the output documentation. This is great for new
packages since Markdown is very easy to write and flexible. For existing
packages that already use some other docstring formatting like
reStructuredText or Google Style, this may produce some unwanted
artifacts in the output html files unless you rewrite it in Markdown.
**In a future version I hope to add support for these other formats.**

Uploading packages
~~~~~~~~~~~~~~~~~~

To upload a package to PyPi.org you must first have a user account. This
has to be done manually on their website, and is required only once.
First time you use the PyPi package you must tell it which username and
password to use when uploading packages. Just open the interactive
Python shell (not the script editor) and use the "login" function, which
will store this information in a file on your computer.

::

    pypi.login("myusername", "mypassword")

If you need to switch accounts or want to protect your information you
can also call "logout" which will delete the login file.

::

    pypi.logout()

Uploading and sharing your package to the pypi website can then be fully
automated. In fact, let me suggest a very simple single-file recipe for
uploading your packages, which is how I have personally started doing it
for all my packages. Simply create an upload.py script in your
repository folder, based on the following template and just fill in the
name of the package folder or the module.py file, the license to use,
the keywords, and the classifier tags:

::

    import pypi
     
    packpath = "mymodule.py"
    pypi.define_upload(packpath,
                       author="Your name",
                       author_email="Your email",
                       license="MIT",
                       name="Official name of package",
                       description="Short sentence describing package.",
                       url="www.github.com/yourpackage",
                       keywords="a bunch of key words",
                       classifiers=["License :: OSI Approved",
                                    "Programming Language :: Python",
                                    "Development Status :: 4 - Beta",
                                    "Intended Audience :: Developers",
                                    "Intended Audience :: Science/Research",
                                    'Intended Audience :: End Users/Desktop'],
                       )

    pypi.generate_docs(packpath)
    #pypi.upload_test(packpath)
    pypi.upload(packpath)

The script above defines how the setup.py script will look, which is
made simpler, does some autofilling for you, and produces the setup
script for you. It also generates the documentation, and finally uploads
your package. Sharing a package or releasing a new version is then as
simple as running this upload.py script, with all documentation updated
and the version automatically taken from your package's **version**
attribute.

Note that you should try uploading to the test website first, before
uploading to the real site.

**Tips:** If the upload process complains about needing your account
details even though you have logged in, make sure that you have indeed
registered on the site that you are trying to upload to (the test site
and the real site have different accounts).

To do
-----

-  Ask mailing list about pypi package name conflict/ethics.
-  Automate uploading as wheel, http://pythonwheels.com/
-  Prevent running all upload steps after one of the steps fail, maybe
   by switching to subprocess and listen for result.
-  Add support for changelog:

   a. Either auto detect a changelog file, and append to README.rst.
   b. And/or add a ``changes`` str or list of str arg to pypi.upload().
      The new version nr will be written as a new heading to a changelog
      file, along with bulletpoints of the given text of changes for
      that version upload.
   c. Or maybe...read changes from git somehow, but would be limited to
      people using GitHub. See eg
      https://github.com/michaeljoseph/changes

-  Make all hidden methods into public, so that user can more easily
   customize.
-  Possibly also upload each new pypi release as a new version to
   GitHub, would be really nice?
-  Add autoincr arg defaulting to True for detecting and incrementing
   the **version** var in your top script.

CHANGES
-------

0.3.19
~~~~~~

-  leeeeeeeee
-  snooooooasnd
