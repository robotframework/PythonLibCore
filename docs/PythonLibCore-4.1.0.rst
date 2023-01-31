=========================
Python Library Core 4.1.0
=========================


.. default-role:: code


`PythonLibCore`_ is a generic component making it easier to create
bigger `Robot Framework`_ test libraries. Python Library Core 4.1.0 is
a new release with support registering Robot Framework listener from
keyword class.

All issues targeted for Python Library Core v4.1.0 can be found
from the `issue tracker`_.

If you have pip_ installed, just run

::

   pip install --upgrade pip install robotframework-pythonlibcore

to install the latest available release or use

::

   pip install pip install robotframework-pythonlibcore==4.1.0

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

Python Library Core 4.1.0 was released on Tuesday January 31, 2023.

.. _PythonLibCore: https://github.com/robotframework/PythonLibCore
.. _Robot Framework: http://robotframework.org
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-robotlibcore
.. _issue tracker: https://github.com/robotframework/PythonLibCore/issues?q=milestone%3Av4.1.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Add support adding classes also as a listener.  (`#107`_)
---------------------------------------------------------
Now it is possible to register Robot Framework listener also from the
class which implements keyword and not only from the library main class.


Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#107`_
      - enhancement
      - critical
      - Add support adding classes also as a listener. 

Altogether 1 issue. View on the `issue tracker <https://github.com/robotframework/PythonLibCore/issues?q=milestone%3Av4.1.0>`__.

.. _#107: https://github.com/robotframework/PythonLibCore/issues/107
