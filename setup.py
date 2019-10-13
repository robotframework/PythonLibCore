#!/usr/bin/env python

from os.path import abspath, join, dirname
from setuptools import find_packages, setup


CURDIR = dirname(abspath(__file__))

with open(join(CURDIR, 'src', 'robotlibcore.py')) as f:
    exec(f.read())
    VERSION = __version__
with open(join(CURDIR, 'README.rst')) as f:
    LONG_DESCRIPTION = f.read()
CLASSIFIERS = """
Development Status :: 5 - Production/Stable
License :: OSI Approved :: Apache Software License
Operating System :: OS Independent
Programming Language :: Python :: 2
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3
Programming Language :: Python :: 3.4
Programming Language :: Python :: 3.5
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Programming Language :: Python :: Implementation :: CPython
Programming Language :: Python :: Implementation :: Jython
Programming Language :: Python :: Implementation :: IronPython
Programming Language :: Python :: Implementation :: PyPy
Topic :: Software Development :: Testing
Topic :: Software Development :: Testing :: Acceptance
Topic :: Software Development :: Testing :: BDD
Framework :: Robot Framework
""".strip().splitlines()
DESCRIPTION = ('Tools to ease creating larger test libraries for '
               'Robot Framework using Python.')
KEYWORDS = ('robotframework automation testautomation rpa '
            'testing acceptancetesting atdd bdd')


setup(
    name         = 'robotlibcore',
    version      = VERSION,
    author       = u'Pekka Kl\xe4rck',
    author_email = 'peke@eliga.fi',
    url          = 'http://robotframework.org',
    download_url = 'https://pypi.python.org/pypi/robotlibcore',
    license      = 'Apache License 2.0',
    description  = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    keywords     = KEYWORDS,
    platforms    = 'any',
    classifiers  = CLASSIFIERS,
    package_dir  = {'': 'src'},
    packages     = find_packages('src'),
    py_modules   = ['robotlibcore'],
)
