from setuptools import setup, find_packages
import os
import mcr

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='mcr-cli',
    version=mcr.__version__,
    description=mcr.__doc__.strip(),
    author=mcr.__author__,
    author_email='stefan@ellefant.be',
    url='http://sdb.github.com/mcr-cli',
    long_description=read('README.rst'),
    license=mcr.__license__,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'mcr = mcr.__main__:main',
        ],
    }
)