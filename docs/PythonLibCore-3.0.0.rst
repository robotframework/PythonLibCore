=========================
Python Library Core 3.0.0
=========================


.. default-role:: code


`Python Library Core`_ is a generic component making it easier to create
bigger `Robot Framework`_ test libraries. Python Library Core 3.0.0 is
a new release with fixing but with RF 4 and typing.Union resulting incorrect
conversion. Also this release drops support for Rf 3.1

All issues targeted for Python Library Core v3.0.0 can be found
from the `issue tracker`_.

**REMOVE ``--pre`` from the next command with final releases.**
If you have pip_ installed, just run

::

   pip install --pre --upgrade pip install robotframework-pythonlibcore

to install the latest available release or use

::

   pip install pip install robotframework-pythonlibcore==3.0.0

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

Python Library Core 3.0.0 was released on Friday June 11, 2021.

.. _PythonLibCore: https://github.com/robotframework/PythonLibCore
.. _Robot Framework: http://robotframework.org
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-robotlibcore
.. _issue tracker: https://github.com/robotframework/PythonLibCore/issues?q=milestone%3Av3.0.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================
${None} type conversion does not work correctly  (`#81`_)
---------------------------------------------------------
When argument contained type hint with typing.Union and None default value,
and keyword was used with ${None} default value, then argument was not converted
correctly with RF 4.

Drop Python 2 and Python 3.5 support (`#76`_)
---------------------------------------------
Python 2 and 3.5 support is not anymore supported. Many thanks for Hugo van Kemenade for
providing the PR.

Support only RF 3.2.2 and 4.0.1 (`#80`_)
----------------------------------------
Support for RF 3.1 is dropped. Only Rf 3.2 and 4.0 are supported by this release.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#81`_
      - bug
      - critical
      - ${None} type conversion does not work correctly 
    * - `#76`_
      - enhancement
      - critical
      - Drop Python 2 and Python 3.5 support
    * - `#80`_
      - enhancement
      - critical
      - Support only RF 3.2.2 and 4.0.1

Altogether 3 issues. View on the `issue tracker <https://github.com/robotframework/PythonLibCore/issues?q=milestone%3Av3.0.0>`__.

.. _#81: https://github.com/robotframework/PythonLibCore/issues/81
.. _#76: https://github.com/robotframework/PythonLibCore/issues/76
.. _#80: https://github.com/robotframework/PythonLibCore/issues/80
