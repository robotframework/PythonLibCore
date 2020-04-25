#!/usr/bin/env python
import re
from os.path import abspath, join, dirname
from setuptools import find_packages, setup


CURDIR = dirname(abspath(__file__))

CLASSIFIERS = """
Development Status :: 5 - Production/Stable
License :: OSI Approved :: Apache Software License
Operating System :: OS Independent
Programming Language :: Python :: 2
Programming Language :: Python :: 3
Programming Language :: Python :: Implementation :: CPython
Programming Language :: Python :: Implementation :: PyPy
Topic :: Software Development :: Testing
Framework :: Robot Framework
""".strip().splitlines()
with open(join(CURDIR, 'src', 'robotlibcore.py')) as f:
    VERSION = re.search("\n__version__ = '(.*)'", f.read()).group(1)
with open(join(CURDIR, 'README.rst')) as f:
    DESCRIPTION = f.read()

setup(
    name            = 'robotframework-pythontlibcore',
    version         = VERSION,
    author          = 'Tatu Aalto',
    author_email    = 'aalto.tatu@gmail.com',
    url             = 'https://github.com/robotframework/PythonLibCore',
    license         = 'Apache License 2.0',
    description     = DESCRIPTION,
    keywords        = 'robotframework testing testautomation library development',
    platforms       = 'any',
    classifiers     = CLASSIFIERS,
    python_requires = '>=2.7.*, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, <4',
    package_dir     = {'': 'src'},
    packages        = find_packages('src'),
    py_modules      = ['robotlibcore'],
)
