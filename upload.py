import pypi
 
packpath = "pypi"
pypi.define_upload(packpath,
                   author="Karim Bahgat",
                   author_email="karim.bahgat.norway@gmail.com",
                   license="MIT",
                   name="PyPi",
                   description="Blabla",
                   url="http://github.com/karimbahgat/PyPi",
                   keywords="bla bla",
                   classifiers=["License :: OSI Approved",
                                "Programming Language :: Python",
                                "Development Status :: 4 - Beta",
                                "Intended Audience :: Developers",
                                "Intended Audience :: Science/Research",
                                'Intended Audience :: End Users/Desktop'],
                   changes=["leeeeeeeee",
                            "snooooooasnd"],
                   )

#pypi.generate_docs(packpath)
#pypi.upload_test(packpath)
#pypi.upload(packpath)

