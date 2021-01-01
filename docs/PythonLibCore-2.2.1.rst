=========================
Python Library Core 2.2.1
=========================


.. default-role:: code


`Python Library Core`_ is a generic component making it easier to create
bigger `Robot Framework`_ test libraries. Python Library Core 2.2.1 is
a new release with bug fixe for aruguments caused in 2.2.0.

All issues targeted for Python Library Core v2.2.1 can be found
from the `issue tracker`_.

If you have pip_ installed, just run

::

   pip install --upgrade pip install robotframework-pythonlibcore

to install the latest available release or use

::

   pip install pip install robotframework-pythonlibcore==2.2.1

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

Python Library Core 2.2.1 was released on Saturday January 2, 2021.

.. _PythonLibCore: https://github.com/robotframework/PythonLibCore
.. _Robot Framework: http://robotframework.org
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-robotlibcore
.. _issue tracker: https://github.com/robotframework/PythonLibCore/issues?q=milestone%3Av2.2.1


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Using inspect.unwrap for generating keyword arguments caused adding self to argument list (`#74`_)
--------------------------------------------------------------------------------------------------
Adding self is not needed and causes problems in libraries. This is now fixed.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#74`_
      - bug
      - critical
      - Using inspect.unwrap for generating keyword arguments caused adding self to argument list

Altogether 1 issue. View on the `issue tracker <https://github.com/robotframework/PythonLibCore/issues?q=milestone%3Av2.2.1>`__.

.. _#74: https://github.com/robotframework/PythonLibCore/issues/74
