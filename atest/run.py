#!/usr/bin/env python
import platform
import shutil
import sys
from os.path import abspath, dirname, isdir, join
from pathlib import Path

from robot import rebot, run
from robot.version import VERSION as rf_version
from robotstatuschecker import process_output

library_variants = ["Hybrid", "Dynamic", "ExtendExisting"]
curdir = dirname(abspath(__file__))
outdir = join(curdir, "results")
if isdir(outdir):
    shutil.rmtree(outdir, ignore_errors=True)
tests = join(curdir, "tests.robot")
tests_types = join(curdir, "tests_types.robot")
plugin_api = join(curdir, "plugin_api")
sys.path.insert(0, join(curdir, "..", "src"))
python_version = platform.python_version()
for variant in library_variants:
    output = join(outdir, "lib-{}-python-{}-robot-{}.xml".format(variant, python_version, rf_version))
    rc = run(
        tests,
        name=variant,
        variable="LIBRARY:%sLibrary" % variant,
        output=output,
        report=None,
        log=None,
        loglevel="debug",
    )
    if rc > 250:
        sys.exit(rc)
    process_output(output, verbose=False)
output = join(outdir, "lib-DynamicTypesLibrary-python-{}-robot-{}.xml".format(python_version, rf_version))
exclude = "py310" if sys.version_info < (3, 10) else ""
rc = run(tests_types, name="Types", output=output, report=None, log=None, loglevel="debug", exclude=exclude)
if rc > 250:
    sys.exit(rc)
process_output(output, verbose=False)
output = join(outdir, "lib-PluginApi-python-{}-robot-{}.xml".format(python_version, rf_version))
rc = run(plugin_api, name="Plugin", output=output, report=None, log=None, loglevel="debug")
if rc > 250:
    sys.exit(rc)
process_output(output, verbose=False)
print("\nCombining results.")
library_variants.append("DynamicTypesLibrary")
xml_files = [str(xml_file) for xml_file in Path(outdir).glob("*.xml")]
for xxx in xml_files:
    print(xxx)
rc = rebot(
    *xml_files,
    **dict(
        name="Acceptance Tests",
        outputdir=outdir,
        log="log-python-{}-robot-{}.html".format(python_version, rf_version),
        report="report-python-{}-robot-{}.html".format(python_version, rf_version),
    ),
)
if rc == 0:
    print("\nAll tests passed/failed as expected.")
else:
    print("\n%d test%s failed." % (rc, "s" if rc != 1 else ""))
sys.exit(rc)
