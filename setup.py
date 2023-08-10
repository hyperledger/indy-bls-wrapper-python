import os
from setuptools import setup

with open(os.path.abspath("./README.md"), "r") as fh:
    long_description = fh.read()

setup(
    name="indy_bls",
    version="0.1.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hyperledger/indy-bls-wrapper-python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    description="Python wrapper for the Indy BLS signatures implementation",
    license="Apache-2.0",
    author="Andrew Whitehead, Berend Sliedrecht, Stephen Curran",
    author_email="cywolf@gmail.com, berend@animo.id, swcurran@cloudcompass.ca",
    packages=["indy_bls"],
    include_package_data=True,
    package_data={
        "": [
            "indy_blssignatures.dll",
            "libindy_blssignatures.dylib",
            "libindy_blssignatures.so",
        ]
    },
    python_requires=">=3.6.3",
    tests_require=["pytest"],
)
