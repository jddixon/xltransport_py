#!/usr/bin/python3
# xltransport_py/setup.py

""" Setuptools project configuration for xltransport_py. """

from os.path import exists
from setuptools import setup

long_desc = None
if exists('README.md'):
    with open('README.md', 'r') as file:
        long_desc = file.read()

setup(name='xltransport_py',
      version='0.0.8',
      author='Jim Dixon',
      author_email='jddixon@gmail.com',
      long_description=long_desc,
      packages=['xltransport'],
      package_dir={'': 'src'},
      py_modules=[],
      include_package_data=False,
      zip_safe=False,
      scripts=[],
      description='transport layer for xlattice_py',
      url='https://jddixon.github.io/xltransport_py',
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Programming Language :: Python 3.5',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],)
