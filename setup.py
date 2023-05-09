import os
from setuptools import setup

with open(os.path.abspath("./README.md"), "r") as fh:
    long_description = fh.read()

setup(
    name='python-indy-bls',
    version='0.1.1',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/hyperledger/indy-bls-wrapper-python',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    description='python wrapper for the indy bls signatures rust implementation',
    license='Apache-2.0',
    author='Andrew Whitehead, Berend Sliedrecht, Stephen Curran',
    author_email='cywolf@gmail.com, berend@animo.id, swcurran@cloudcompass.ca',
    packages=['indy-bls'],
    install_requires=['pytest'],
    tests_require=['pytest']
)
