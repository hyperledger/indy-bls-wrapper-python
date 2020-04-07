import os
from setuptools import setup

with open(os.path.abspath("./README.md"), "r") as fh:
    long_description = fh.read()

setup(
    name='python-ursa',
    version='0.1.1',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/hyperledger/ursa-python',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    description='python wrapper for ursa universal crypto library',
    license='Apache-2.0',
    author='Cam Parra, Vyacheslav Gudkov',
    author_email='camilo.parra@evernym.com, vyacheslav.gudkov@dsr-company.com',
    packages=['ursa'],
    install_requires=['pytest'],
    tests_require=['pytest']
)
