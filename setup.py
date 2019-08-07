
from setuptools import setup

setup(
    name='ursacl',
    version='0.1.0',
    url='https://github.com/cam-parra/python-ursa',
    description='python wrapper for ursa universal crypto library',
    license='Apache-2.0',
    author='Cam Parra, Vyacheslav Gudkov',
    author_email='camilo.parra@evernym.com, vyacheslav.gudkov@dsr-company.com',
    packages=['ursa'],
    install_requires=['pytest'],
    tests_require=['pytest']
)
