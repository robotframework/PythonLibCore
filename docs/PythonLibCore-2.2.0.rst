=========================
Python Library Core 2.2.0
=========================


.. default-role:: code


`Python Library Core`_ is a generic component making it easier to create
bigger `Robot Framework`_ test libraries. Python Library Core 2.2.0 is
a new release with fixes when using complex decorators in keywords.

All issues targeted for Python Library Core v2.2.0 can be found
from the `issue tracker`_.

If you have pip_ installed, just run

::

   pip install --upgrade pip install robotframework-pythonlibcore

to install the latest available release or use

::

   pip install pip install robotframework-pythonlibcore==2.2.0

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

SeleniumLibrary 2.2.0 was released on Friday January 1, 2021.

.. _PythonLibCore: https://github.com/robotframework/PythonLibCore
.. _Robot Framework: http://robotframework.org
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-robotlibcore
.. _issue tracker: https://github.com/robotframework/PythonLibCore/issues?q=milestone%3Av2.2.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

- With decorators containing arguments, argument specification is not correctly resolved. (`#71`_)
--------------------------------------------------------------------------------------------------
With decorators that uses arguments and calls the decorated method, the argument specification
was not correctly resolved. This is not fixed.

robotframework-robotlibcore or robotframework-pythonlibcore (`#69`_)
--------------------------------------------------------------------
There was a bug in release note generation and incorrect installation
command was put in the release notes.

Acknowledgements
================

Add licence information in the installation packages (`#68`_)
-------------------------------------------------------------
Licence text is added to source files. Many thanks to bollwyvl
for fixing the issue.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#71`_
      - bug
      - critical
      - With decorators containing arguments, argument specifucation is not correctly resolved.
    * - `#69`_
      - bug
      - high
      - robotframework-robotlibcore or robotframework-pythonlibcore
    * - `#68`_
      - enhancement
      - medium
      - Add licence information in the installation packages

Altogether 3 issues. View on the `issue tracker <https://github.com/robotframework/PythonLibCore/issues?q=milestone%3Av2.2.0>`__.

.. _#71: https://github.com/robotframework/PythonLibCore/issues/71
.. _#69: https://github.com/robotframework/PythonLibCore/issues/69
.. _#68: https://github.com/robotframework/PythonLibCore/issues/68
