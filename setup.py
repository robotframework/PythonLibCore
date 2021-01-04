#!/usr/bin/env python
import re
from os.path import abspath, join, dirname
from setuptools import find_packages, setup


CURDIR = dirname(abspath(__file__))

CLASSIFIERS = """
Development Status :: 5 - Production/Stable
License :: OSI Approved :: Apache Software License
Operating System :: OS Independent
Programming Language :: Python :: 3
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3.8
Programming Language :: Python :: 3.9
Programming Language :: Python :: 3 :: Only
Programming Language :: Python :: Implementation :: CPython
Programming Language :: Python :: Implementation :: PyPy
Topic :: Software Development :: Testing
Framework :: Robot Framework
""".strip().splitlines()
with open(join(CURDIR, 'src', 'robotlibcore.py')) as f:
    VERSION = re.search("\n__version__ = '(.*)'", f.read()).group(1)
with open(join(CURDIR, 'README.rst')) as f:
    LONG_DESCRIPTION = f.read()

DESCRIPTION = ('Tools to ease creating larger test libraries for '
               'Robot Framework using Python.')
setup(
    name             = 'robotframework-pythonlibcore',
    version          = VERSION,
    author           = 'Tatu Aalto',
    author_email     = 'aalto.tatu@gmail.com',
    url              = 'https://github.com/robotframework/PythonLibCore',
    license          = 'Apache License 2.0',
    description      = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    keywords         = 'robotframework testing testautomation library development',
    platforms        = 'any',
    classifiers      = CLASSIFIERS,
    python_requires  = '>=3.6, <4',
    package_dir      = {'': 'src'},
    packages         = find_packages('src'),
    py_modules       = ['robotlibcore'],
)
