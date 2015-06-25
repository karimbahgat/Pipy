try: from setuptools import setup
except: from distutils.core import setup

setup(	long_description=open("README.rst").read(), 
	name="""PyPi""",
	license="""MIT""",
	author="""Karim Bahgat""",
	author_email="""karim.bahgat.norway@gmail.com""",
	url="""http://github.com/karimbahgat/PyPi""",
	package_data={'pypi': ['pip\\_vendor\\Makefile', 'pip\\_vendor\\README.rst', 'pip\\_vendor\\vendor.txt', 'pip\\_vendor\\certifi\\cacert.pem', 'pip\\_vendor\\distlib\\t32.exe', 'pip\\_vendor\\distlib\\t64.exe', 'pip\\_vendor\\distlib\\w32.exe', 'pip\\_vendor\\distlib\\w64.exe', 'pip\\_vendor\\distlib\\_backport\\sysconfig.cfg', 'pip\\_vendor\\requests\\cacert.pem']},
	version="""0.3.19""",
	keywords="""bla bla""",
	packages=['pypi', 'pypi\\pip', 'pypi\\pip\\commands', 'pypi\\pip\\compat', 'pypi\\pip\\req', 'pypi\\pip\\utils', 'pypi\\pip\\vcs', 'pypi\\pip\\_vendor', 'pypi\\pip\\_vendor\\cachecontrol', 'pypi\\pip\\_vendor\\cachecontrol\\caches', 'pypi\\pip\\_vendor\\certifi', 'pypi\\pip\\_vendor\\colorama', 'pypi\\pip\\_vendor\\distlib', 'pypi\\pip\\_vendor\\distlib\\_backport', 'pypi\\pip\\_vendor\\html5lib', 'pypi\\pip\\_vendor\\html5lib\\filters', 'pypi\\pip\\_vendor\\html5lib\\serializer', 'pypi\\pip\\_vendor\\html5lib\\treeadapters', 'pypi\\pip\\_vendor\\html5lib\\treebuilders', 'pypi\\pip\\_vendor\\html5lib\\treewalkers', 'pypi\\pip\\_vendor\\html5lib\\trie', 'pypi\\pip\\_vendor\\lockfile', 'pypi\\pip\\_vendor\\progress', 'pypi\\pip\\_vendor\\requests', 'pypi\\pip\\_vendor\\requests\\packages', 'pypi\\pip\\_vendor\\requests\\packages\\chardet', 'pypi\\pip\\_vendor\\requests\\packages\\urllib3', 'pypi\\pip\\_vendor\\requests\\packages\\urllib3\\contrib', 'pypi\\pip\\_vendor\\requests\\packages\\urllib3\\packages', 'pypi\\pip\\_vendor\\requests\\packages\\urllib3\\packages\\ssl_match_hostname', 'pypi\\pip\\_vendor\\requests\\packages\\urllib3\\util', 'pypi\\pip\\_vendor\\_markerlib'],
	classifiers=['License :: OSI Approved', 'Programming Language :: Python', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Intended Audience :: Science/Research', 'Intended Audience :: End Users/Desktop'],
	description="""Blabla""",
	)
