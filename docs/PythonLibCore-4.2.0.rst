=========================
Python Library Core 4.2.0
=========================


.. default-role:: code


`Python Library Core`_ is a generic component making it easier to create
bigger `Robot Framework`_ test libraries. Python Library Core 4.2.0 is
a new release with supporting list when importing plugins and
dropping Python 3.7 support.

All issues targeted for Python Library Core v4.2.0 can be found
from the `issue tracker`_.

**REMOVE ``--pre`` from the next command with final releases.**
If you have pip_ installed, just run

::

   pip install --pre --upgrade pip install robotframework-pythonlibcore

to install the latest available release or use

::

   pip install pip install robotframework-pythonlibcore==4.2.0

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

Python Library Core 4.2.0 was released on Monday July 10, 2023.

.. _PythonLibCore: https://github.com/robotframework/PythonLibCore
.. _Robot Framework: http://robotframework.org
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-robotlibcore
.. _issue tracker: https://github.com/robotframework/PythonLibCore/issues?q=milestone%3Av4.2.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Support list in plugin import (`#122`_)
---------------------------------------
Now plugins can be imported as a list and not only a comma separated string.

Backwards incompatible changes
==============================

Drop Python 3.7 support (`#125`_)
---------------------------------
Python 3.7 has been end of life for while and it is time to drop
support for Python 3.7. 

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#122`_
      - enhancement
      - high
      - Support list in plugin import
    * - `#125`_
      - enhancement
      - high
      - Drop Python 3.7 support

Altogether 2 issues. View on the `issue tracker <https://github.com/robotframework/PythonLibCore/issues?q=milestone%3Av4.2.0>`__.

.. _#122: https://github.com/robotframework/PythonLibCore/issues/122
.. _#125: https://github.com/robotframework/PythonLibCore/issues/125
