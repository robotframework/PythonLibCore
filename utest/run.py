#!/usr/bin/env python
import argparse
import platform
import sys
from os.path import abspath, dirname, join

import pytest
from robot.version import VERSION as rf_version

curdir = dirname(abspath(__file__))
atest_dir = join(curdir, "..", "atest")
python_version = platform.python_version()
xunit_report = join(atest_dir, "results", "xunit-python-{}-robot{}.xml".format(python_version, rf_version))
src = join(curdir, "..", "src")
sys.path.insert(0, src)
sys.path.insert(0, atest_dir)
helpers = join(curdir, "helpers")
sys.path.append(helpers)

parser = argparse.ArgumentParser()
parser.add_argument("--no-cov", dest="cov", action="store_false")
parser.add_argument("--cov", dest="cov", action="store_true")
parser.set_defaults(cov=True)
args = parser.parse_args()

pytest_args = [
    f"--ignore={helpers}",
    "-p",
    "no:cacheprovider",
    "--junitxml=%s" % xunit_report,
    "-o",
    "junit_family=xunit2",
    "--showlocals",
    curdir,
]
if args.cov:
    pytest_args.insert(0, "--cov=%s" % src)
rc = pytest.main(pytest_args)
sys.exit(rc)
