#!/usr/bin/env python
import re
from pathlib import Path
from os.path import join

from setuptools import find_packages, setup

CURDIR = Path(__file__).parent

CLASSIFIERS = """
Development Status :: 5 - Production/Stable
License :: OSI Approved :: Apache Software License
Operating System :: OS Independent
Programming Language :: Python :: 3
Programming Language :: Python :: 3.8
Programming Language :: Python :: 3.9
Programming Language :: Python :: 3.10
Programming Language :: Python :: 3.11
Programming Language :: Python :: 3 :: Only
Programming Language :: Python :: Implementation :: CPython
Programming Language :: Python :: Implementation :: PyPy
Topic :: Software Development :: Testing
Framework :: Robot Framework
""".strip().splitlines()

version_file = Path(CURDIR / 'src' / 'robotlibcore' / '__init__.py')
VERSION = re.search('\n__version__ = "(.*)"', version_file.read_text()).group(1)

LONG_DESCRIPTION = Path(CURDIR / 'README.md').read_text()

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
    long_description_content_type = "text/markdown",
    keywords         = 'robotframework testing testautomation library development',
    platforms        = 'any',
    classifiers      = CLASSIFIERS,
    python_requires  = '>=3.8, <4',
    package_dir      = {'': 'src'},
    packages         = ["robotlibcore","robotlibcore.core", "robotlibcore.keywords", "robotlibcore.plugin", "robotlibcore.utils"]
)
