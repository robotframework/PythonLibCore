=========================
Python Library Core 4.4.0
=========================


.. default-role:: code


`Python Library Core`_ is a generic component making it easier to create
bigger `Robot Framework`_ test libraries. Python Library Core 4.4.0 is
a new release with enhancement to support keyword translation. Python Library
Core can translate keyword names and keyword documentation. It is also
possible to translate library init and class documentation.

All issues targeted for Python Library Core v4.4.0 can be found
from the `issue tracker`_.

If you have pip_ installed, just run

::

   pip install --upgrade pip install robotframework-pythonlibcore

to install the latest available release or use

::

   pip install pip install robotframework-pythonlibcore==4.4.0

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

Python Library Core supports Robot Framework 5.0.1 or older and Python
3.8+. Python Library Core 4.4.0 was released on Friday March 22, 2024.

.. _PythonLibCore: https://github.com/robotframework/PythonLibCore
.. _Robot Framework: http://robotframework.org
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-robotlibcore
.. _issue tracker: https://github.com/robotframework/PythonLibCore/issues?q=milestone%3Av4.4.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Add translation for for keywords in PLC (`#139`_)
-------------------------------------------------
Robot Framework core has supported translations since release 6.0. Now also Python Lib Core
provides support to translate library keyword and documentation. Also it is possible to
translate library init and class level documentation. Keyword or library init argument names, argument
types and argument default values are not translated.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#139`_
      - enhancement
      - critical
      - Add translation for for keywords in PLC

Altogether 1 issue. View on the `issue tracker <https://github.com/robotframework/PythonLibCore/issues?q=milestone%3Av4.4.0>`__.

.. _#139: https://github.com/robotframework/PythonLibCore/issues/139
