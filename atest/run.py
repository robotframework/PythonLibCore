#!/usr/bin/env python

from __future__ import print_function

import platform
from os.path import abspath, dirname, join
import sys

from robot import run, rebot
from robotstatuschecker import process_output


library_variants = ['Hybrid', 'Dynamic', 'Static', 'ExtendExisting']
curdir = dirname(abspath(__file__))
outdir = join(curdir, 'results')
tests = join(curdir, 'tests.robot')
sys.path.insert(0, join(curdir, '..', 'src'))
python_version = platform.python_version()
for variant in library_variants:
    output = join(outdir, '%s-%s.xml' % (variant, python_version))
    rc = run(tests, name=variant, variable='LIBRARY:%sLibrary' % variant,
             output=output, report=None, log=None)
    if rc > 250:
        sys.exit(rc)
    process_output(output, verbose=False)
print('\nCombining results.')
rc = rebot(*(join(outdir, '%s-%s.xml' % (variant, python_version)) for variant in library_variants),
           **dict(name='Acceptance Tests', outputdir=outdir, log='log-%s.html' % python_version,
                  report='report-%s.html' % python_version))
if rc == 0:
    print('\nAll tests passed/failed as expected.')
else:
    print('\n%d test%s failed.' % (rc, 's' if rc != 1 else ''))
sys.exit(rc)
