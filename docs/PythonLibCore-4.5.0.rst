# Python Library Core 4.5.0


`Python Library Core`_ is a generic component making it easier to create
bigger `Robot Framework`_ test libraries. Python Library Core 4.5.0 is
a new release with to refactor internal structure and bug fix to avoid
maximum recursion depth exceeded error on getattr.

All issues targeted for Python Library Core v4.5.0 can be found
from the `issue tracker`_.

If you have pip_ installed, just run

::

   pip install --upgrade robotframework-pythonlibcore

to install the latest available release or use

::

   pip install pip install robotframework-pythonlibcore==4.5.0

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

Python Library Core 4.5.0 was released on Friday January 16, 2026.
It support Python versions 3.10+ and Robot Framework versions 6.1 and newer.

.. _PythonLibCore: https://github.com/robotframework/PythonLibCore
.. _Robot Framework: http://robotframework.org
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-robotlibcore
.. _issue tracker: https://github.com/robotframework/PythonLibCore/issues?q=milestone%3Av4.5.0


## Most important enhancements

Maximum Recursion Depth Exceeded on getattr ([#158](https://github.com/robotframework/PythonLibCore/issues/158))
----------------------------------------------------------------------------------------------------------------
If one attempts to get any attribute on a child class of HybridCore or DynamicCore before the initializer is called
(so the attributes object has yet to be initialized) the custom getattr implementation on the class causes an
infinite recursion. getattr is called on the attribute of the class then HybridCore attempts to evaluate if name
in self.attributes: but attributes is undef because since attributes is undef, python calls getattr on self.attributes
then HybridCore attempts to evaluate if name in self.attributes: but attributes is undef and so on.

HybridCore should fall back to the standard implementation of getattr if self.attributes is undefined which would avoid this issue.

Many thanks to Joe Rendleman for reporting this issue and providing a PR with a fix.

robotlibcore.py placed right into root of site-packages/  ([#149](https://github.com/robotframework/PythonLibCore/issues/149))
------------------------------------------------------------------------------------------------------------------------------
To improve compatibility with various tools and IDEs, robotlibcore.py is now in own folder and package is refactored
logical modules. This change should be transparent to end users as the package structure is unchanged.

many thanks to Jani Mikkonen to reporting this issue and providing a PR with a fix.

## Full list of fixes and enhancements

| ID | Type | Priority | Summary |
|---|---|---|---|
| [#158](https://github.com/robotframework/PythonLibCore/issues/158) | bug | high | Maximum Recursion Depth Exceeded on getattr |
| [#149](https://github.com/robotframework/PythonLibCore/issues/149) | enhancement | high | robotlibcore.py placed right into root of site-packages/  |

Altogether 2 issues. View on the [issue tracker](https://github.com/robotframework/PythonLibCore/issues?q=milestone%3Av4.5.0).
