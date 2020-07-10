=========================
Python Library Core 2.1.0
=========================


.. default-role:: code


The `Python Library Core`_ is a generic component making it easier to create
bigger `Robot Framework`_ test libraries. Python Library Core 2.1.0 is
a new release with with Enum conversion and not providing type hints
for bool and None default values.

All issues targeted for Python Library Core v2.1.0 can be found
from the `issue tracker`_.

If you have pip_ installed, just run

::

   pip install --upgrade robotframework-robotlibcore

to install the latest available release or use

::

   pip install robotframework-robotlibcore==2.1.0

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

PythonLibCore 2.1.0 was released on Thursday July 9, 2020. PythonLibCore
supports Python 2.7 and 3.6+ and Robot Framework 3.1.2+. This is last release
which contains new development for Python 2.7 and users should migrate to Python 3.

.. _PythonLibCore: https://github.com/robotframework/PythonLibCore
.. _Robot Framework: http://robotframework.org
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-robotlibcore
.. _issue tracker: https://github.com/robotframework/PythonLibCore/issues?q=milestone%3Av2.1.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================
Fix typing hints for None and bool types (`#60`_)
-------------------------------------------------
PythonLibCore does not anymore provide type hints for bool and None default values in
keyword arguments.

Remove static core (`#62`_)
---------------------------
Static core is removed.

param:Optional[x] = None type hint behaves differently than Robot Framework (`#64`_)
____________________________________________________________________________________
This offers better Enum conversion and better typing hints in libdoc for
"Optional[x] = None".

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#60`_
      - enhancement
      - critical
      - Fix typing hints for None and bool types
    * - `#62`_
      - enhancement
      - high
      - Remove static core
    * - `#64`_
      - enhancement
      - high
      - param:Optional[x] = None type hint behaves differently than Robot Framework

Altogether 3 issues. View on the `issue tracker <https://github.com/robotframework/PythonLibCore/issues?q=milestone%3Av2.1.0>`__.

.. _#60: https://github.com/robotframework/PythonLibCore/issues/60
.. _#62: https://github.com/robotframework/PythonLibCore/issues/62
.. _#64: https://github.com/robotframework/PythonLibCore/issues/64
