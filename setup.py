try: from setuptools import setup
except: from distutils.core import setup

setup(	long_description=open("README.rst").read(), 
	name="""Pipy""",
	license="""MIT""",
	author="""Karim Bahgat""",
	author_email="""karim.bahgat.norway@gmail.com""",
	url="""http://github.com/karimbahgat/Pipy""",
	package_data={'pipy': ['pip/_vendor/Makefile', 'pip/_vendor/README.rst', 'pip/_vendor/vendor.txt', 'pip/_vendor/certifi/cacert.pem', 'pip/_vendor/distlib/t32.exe', 'pip/_vendor/distlib/t64.exe', 'pip/_vendor/distlib/w32.exe', 'pip/_vendor/distlib/w64.exe', 'pip/_vendor/distlib/_backport/sysconfig.cfg', 'pip/_vendor/requests/cacert.pem']},
	version="""0.1.0""",
	keywords="""bla bla""",
	packages=['pipy', 'pipy/pip', 'pipy/pip/commands', 'pipy/pip/compat', 'pipy/pip/req', 'pipy/pip/utils', 'pipy/pip/vcs', 'pipy/pip/_vendor', 'pipy/pip/_vendor/cachecontrol', 'pipy/pip/_vendor/cachecontrol/caches', 'pipy/pip/_vendor/certifi', 'pipy/pip/_vendor/colorama', 'pipy/pip/_vendor/distlib', 'pipy/pip/_vendor/distlib/_backport', 'pipy/pip/_vendor/html5lib', 'pipy/pip/_vendor/html5lib/filters', 'pipy/pip/_vendor/html5lib/serializer', 'pipy/pip/_vendor/html5lib/treeadapters', 'pipy/pip/_vendor/html5lib/treebuilders', 'pipy/pip/_vendor/html5lib/treewalkers', 'pipy/pip/_vendor/html5lib/trie', 'pipy/pip/_vendor/lockfile', 'pipy/pip/_vendor/progress', 'pipy/pip/_vendor/requests', 'pipy/pip/_vendor/requests/packages', 'pipy/pip/_vendor/requests/packages/chardet', 'pipy/pip/_vendor/requests/packages/urllib3', 'pipy/pip/_vendor/requests/packages/urllib3/contrib', 'pipy/pip/_vendor/requests/packages/urllib3/packages', 'pipy/pip/_vendor/requests/packages/urllib3/packages/ssl_match_hostname', 'pipy/pip/_vendor/requests/packages/urllib3/util', 'pipy/pip/_vendor/_markerlib'],
	classifiers=['License :: OSI Approved', 'Programming Language :: Python', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Intended Audience :: Science/Research', 'Intended Audience :: End Users/Desktop'],
	description="""Blabla""",
	)
