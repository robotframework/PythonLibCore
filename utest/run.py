#!/usr/bin/env python

from os.path import abspath, dirname, join
import sys

import pytest


curdir = dirname(abspath(__file__))
sys.path.insert(0, join(curdir, '..', 'src'))
sys.path.insert(0, join(curdir, '..', 'atest'))
rc = pytest.main(sys.argv[1:] + ['-p', 'no:cacheprovider', curdir])
sys.exit(rc)
