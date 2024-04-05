=========================
Python Library Core 4.4.1
=========================


.. default-role:: code


`Python Library Core`_ is a generic component making it easier to create
bigger `Robot Framework`_ test libraries. Python Library Core 4.4.1 is
a new release with a bug fix to not leak keywords names if @keyword
decorator defines custom name.

All issues targeted for Python Library Core v4.4.1 can be found
from the `issue tracker`_.

If you have pip_ installed, just run

::

   pip install --pre --upgrade pip install robotframework-pythonlibcore

to install the latest available release or use

::

   pip install pip install robotframework-pythonlibcore==4.4.1

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

Python Library Core 4.4.1 was released on Saturday April 6, 2024.

.. _PythonLibCore: https://github.com/robotframework/PythonLibCore
.. _Robot Framework: http://robotframework.org
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-robotlibcore
.. _issue tracker: https://github.com/robotframework/PythonLibCore/issues?q=milestone%3Av4.4.1


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

If @keyword deco has custom name, original name leaks to keywords (`#146`_)
---------------------------------------------------------------------------
If @keyword deco has custom name, then original and not translated method name
leaks to keywords. This issue is now fixed.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#146`_
      - bug
      - critical
      - If @keyword deco has custom name, original name leaks to keywords

Altogether 1 issue. View on the `issue tracker <https://github.com/robotframework/PythonLibCore/issues?q=milestone%3Av4.4.1>`__.

.. _#146: https://github.com/robotframework/PythonLibCore/issues/146
