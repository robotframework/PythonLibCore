=========================
Python Library Core 2.0.1
=========================


.. default-role:: code


`PythonLibraryCore`_ is a generic component making it easier to create
bigger `Robot Framework`_ test libraries. Python Library Core 2.0.1 is
a new release with support of Robot Framework 3.2 dynamic library API
changes.

All issues targeted for Python Library Core v2.0.1 can be found
from the `issue tracker`_.

If you have pip_ installed, just run

::

   pip install --upgrade robotframework-robotlibcore

to install the latest available release or use

::

   pip install robotframework-robotlibcore==2.0.1

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

PythonLibCore 2.0.1was released on Sunday April 26, 2020. PythonLibCore
supports Python 2.7 and 3.6+ and Robot Framework 3.1.2+. This is last release
which contains new development for Python 2.7 and users should migrate to Python 3.

.. _PythonLibCore: https://github.com/robotframework/PythonLibCore
.. _Robot Framework: http://robotframework.org
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-pythontlibcore
.. _issue tracker: https://github.com/robotframework/PythonLibCore/issues?q=milestone%3Av2.0.1


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Support type information (`#10`_)
---------------------------------
PythonLibCore support dynamic library API `get_keyword_types`_ method and
is able to return arguments types for keywords.

Add support for get_keyword_source API method for Robot Framework 3.2 (`#26`_)
------------------------------------------------------------------------------
Robot Framework 3.2 has new method, get_keyword_source, in the dynamic library
API. PythonLibCore 2.0 supports get_keyword_source method.


Enhance get_keyword_arguments to support new format in Rf 3.2 (`#27`_)
----------------------------------------------------------------------
Robot Framework 3.2 changed how get_keyword_arguments dynamic library API method
should return keyword arguments. PythonLibCore now supports Robot Framework 3.2
and 3.1 for the get_keyword_arguments method.

Support keyword-only arguments (`#9`_)
--------------------------------------
PythonLibCore supports keyword only arguments for keyword methods.

Backwards incompatible changes
==============================

Drop support for RF 3.0 (`#37`_)
--------------------------------
PythonLibCore release supports only RF 3.1 and 3.2.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#10`_
      - enhancement
      - critical
      - Support type information
    * - `#26`_
      - enhancement
      - critical
      - Add support for get_keyword_source API method for Robot Framework 3.2
    * - `#27`_
      - enhancement
      - critical
      - Enhance get_keyword_arguments to support new format in Rf 3.2
    * - `#9`_
      - enhancement
      - critical
      - Support keyword-only arguments
    * - `#42`_
      - bug
      - high
      - Fix get_keyword_types if self has typing hints
    * - `#37`_
      - enhancement
      - high
      - Drop support for RF 3.0
    * - `#11`_
      - bug
      - medium
      - Error with kwargs when using DynamicCore with Remote interface
    * - `#1`_
      - enhancement
      - medium
      - Common base class
    * - `#3`_
      - enhancement
      - ---
      - Documentation
    * - `#4`_
      - enhancement
      - ---
      - Packaging

Altogether 10 issues. View on the `issue tracker <https://github.com/robotframework/PythonLibCore/issues?q=milestone%3Av2.0.1>`__.

.. _#10: https://github.com/robotframework/PythonLibCore/issues/10
.. _#26: https://github.com/robotframework/PythonLibCore/issues/26
.. _#27: https://github.com/robotframework/PythonLibCore/issues/27
.. _#9: https://github.com/robotframework/PythonLibCore/issues/9
.. _#42: https://github.com/robotframework/PythonLibCore/issues/42
.. _#37: https://github.com/robotframework/PythonLibCore/issues/37
.. _#11: https://github.com/robotframework/PythonLibCore/issues/11
.. _#1: https://github.com/robotframework/PythonLibCore/issues/1
.. _#3: https://github.com/robotframework/PythonLibCore/issues/3
.. _#4: https://github.com/robotframework/PythonLibCore/issues/4
.. _get_keyword_types: https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#getting-keyword-argument-types