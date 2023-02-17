=========================
Python Library Core 4.1.1
=========================


.. default-role:: code


`Python Library Core`_ is a generic component making it easier to create
bigger `Robot Framework`_ test libraries. Python Library Core 4.1.1 is
a new hotfix release with bug fixes for named arguments support.

All issues targeted for Python Library Core v4.1.1 can be found
from the `issue tracker`_.

If you have pip_ installed, just run

::

   pip install --upgrade pip install robotframework-pythonlibcore

to install the latest available release or use

::

   pip install pip install robotframework-pythonlibcore==4.1.1

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

Python Library Core 4.1.1 was released on Friday February 17, 2023.

.. _PythonLibCore: https://github.com/robotframework/PythonLibCore
.. _Robot Framework: http://robotframework.org
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-robotlibcore
.. _issue tracker: https://github.com/robotframework/PythonLibCore/issues?q=milestone%3Av4.1.1


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

`DynamicCore` doesn't handle named only arguments properly (`#111`_)
--------------------------------------------------------------------
PLC did not handle named only argumets correctly. If keyword looked like:
`def kw(self, *, arg)` then argument secification not correcly returned.


Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#111`_
      - bug
      - high
      - `DynamicCore` doesn't handle named only arguments properly

Altogether 1 issue. View on the `issue tracker <https://github.com/robotframework/PythonLibCore/issues?q=milestone%3Av4.1.1>`__.

.. _#111: https://github.com/robotframework/PythonLibCore/issues/111
