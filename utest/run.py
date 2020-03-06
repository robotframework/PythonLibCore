#!/usr/bin/env python
import platform
from os.path import abspath, dirname, join
import sys

import pytest


curdir = dirname(abspath(__file__))
atest_dir = join(curdir, '..', 'atest')
python_version = platform.python_version()
xunit_report = join(atest_dir, 'results', 'xunit-%s.xml' % python_version)
src = join(curdir, '..', 'src')
sys.path.insert(0, src)
sys.path.insert(0, atest_dir)
pytest_args = sys.argv[1:] + [
    '-p', 'no:cacheprovider',
    '--junitxml=%s' % xunit_report,
    '-o', 'junit_family=xunit2',
    '--cov=%s' % src,
    curdir
]
rc = pytest.main(pytest_args)
sys.exit(rc)
