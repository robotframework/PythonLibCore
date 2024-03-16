#!/usr/bin/env python
import argparse
import platform
import sys
from pathlib import Path

import pytest
from robot.version import VERSION as RF_VERSION

curdir = Path(__file__).parent
atest_dir = curdir / ".." / "atest"
python_version = platform.python_version()
xunit_report = atest_dir / "results" / f"xunit-python-{python_version}-robot{RF_VERSION}.xml"
src = curdir / ".." / "src"
sys.path.insert(0, src)
sys.path.insert(0, atest_dir)
helpers = curdir / "helpers"
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
