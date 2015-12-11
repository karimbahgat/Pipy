import pipy

packpath = "pipy"
pipy.define_upload(packpath,
                   author="Karim Bahgat",
                   author_email="karim.bahgat.norway@gmail.com",
                   license="MIT",
                   name="Pipy",
                   description="Blabla",
                   url="http://github.com/karimbahgat/Pipy",
                   keywords="bla bla",
                   classifiers=["License :: OSI Approved",
                                "Programming Language :: Python",
                                "Development Status :: 4 - Beta",
                                "Intended Audience :: Developers",
                                "Intended Audience :: Science/Research",
                                'Intended Audience :: End Users/Desktop'],
                   changes=["testing",
                            "testing2"],
                   )

#pipy.generate_docs(packpath)
#pipy.upload_test(packpath)
#pipy.upload(packpath)

