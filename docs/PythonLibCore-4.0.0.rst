=========================
Python Library Core 4.0.0
=========================


.. default-role:: code


`Python Library Core`_ is a generic component making it easier to create
bigger `Robot Framework`_ test libraries. Python Library Core 4.0.0 is
a new release with support for plugin API and bug fixe for library source.

All issues targeted for Python Library Core v4.0.0 can be found
from the `issue tracker`_.

If you have pip_ installed, just run

::

   pip install --upgrade pip install robotframework-pythonlibcore

to install the latest available release or use

::

   pip install pip install robotframework-pythonlibcore==4.0.0

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

Python Library Core 4.0.0 was released on Saturday November 5, 2022.

.. _PythonLibCore: https://github.com/robotframework/PythonLibCore
.. _Robot Framework: http://robotframework.org
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-robotlibcore
.. _issue tracker: https://github.com/robotframework/PythonLibCore/issues?q=milestone%3Av4.0.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Add support for plugin API from SeleniumLibrary (`#103`_)
---------------------------------------------------------
PLC now support similar plugin API as SeleniumLibrary. This makes
implementation of plugin easier for other libraries in community.

Support Python 3.10 and ensure that new type hints works (`#87`_)
----------------------------------------------------------------
Support for Python 3.10.

Decorator resolves as wron file path  (`#99`_)
----------------------------------------------
Keyword with decorators did not resolve correct path when decorator
was in different file. This is now fixed.

Backwards incompatible changes
==============================

Drop RF 3.2 support (`#85`_)
----------------------------
RF 3.2 is not tested and therefore not officially supported.

Drop Python 3.6 suopport (`#92`_)
---------------------------------
Python 3.6 has been end of life for some time and therefore it is
not anymore supported.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#103`_
      - enhancement
      - critical
      - Add support for plugin API from SeleniumLibrary
    * - `#85`_
      - enhancement
      - critical
      - Drop RF 3.2 support
    * - `#87`_
      - enhancement
      - critical
      - Support Python 3.10 and ensure that new type hints works
    * - `#92`_
      - enhancement
      - critical
      - Drop Python 3.6 suopport
    * - `#99`_
      - bug
      - high
      - Decorator resolves as wron file path 

Altogether 5 issues. View on the `issue tracker <https://github.com/robotframework/PythonLibCore/issues?q=milestone%3Av4.0.0>`__.

.. _#103: https://github.com/robotframework/PythonLibCore/issues/103
.. _#85: https://github.com/robotframework/PythonLibCore/issues/85
.. _#87: https://github.com/robotframework/PythonLibCore/issues/87
.. _#92: https://github.com/robotframework/PythonLibCore/issues/92
.. _#99: https://github.com/robotframework/PythonLibCore/issues/99
