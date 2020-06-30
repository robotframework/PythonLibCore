Python Library Core
===================

Tools to ease creating larger test libraries for `Robot Framework`_ using
Python. The Robot Framework `hybrid`_ and `dynamic library API`_ gives more
flexibility for library than the static library API, but they also sets requirements
for libraries which needs to be implemented in the library side. PythonLibCore
eases the problem by providing simpler interface and handling all the requirements
towards the Robot Framework library APIs.

Code is stable and version 1.0 is already used by SeleniumLibrary_ and
WhiteLibrary_. The version 2.0 support changes in the Robot Framework
3.2.

.. image:: https://github.com/robotframework/PythonLibCore/workflows/CI/badge.svg?branch=master
   :target: https://github.com/robotframework/PythonLibCore

Usage
-----
There are two ways to use PythonLibCore, either by `HybridCore` or by using `DynamicCore`.
`HybridCore` provides support for the hybrid library API and `DynamicCore` provides support
for dynamic library API. Consult the Robot Framework `User Guide`_, for choosing the
correct API for library.

Regardless which library API is chosen, both have similar requirements.

1) Library must inherit either the `HybridCore` or `DynamicCore`.
2) Library keywords must be decorated with Robot Framework `@keyword`_ decorator.
3) Provide a list of class instances implementing keywords to `library_components` argument in the `HybridCore` or `DynamicCore` `__init__`.

It is also possible implement keywords in the library main class, by marking method with
`@keyword` as keywords. It is not requires pass main library instance in the
`library_components` argument.

All keyword, also keywords implemented in the classes outside of the main library are
available in the library instance as methods. This automatically publish library keywords
in as methods in the Python public API.

The example in below demonstrates how the PythonLibCore can be used with a library.

Example
-------

.. sourcecode:: python

    """Main library."""

    from robotlibcore import DynamicCore

    from mystuff import Library1, Library2


    class MyLibrary(DynamicCore):
        """General library documentation."""

        def __init__(self):
            libraries = [Library1(), Library2()]
            DynamicCore.__init__(self, libraries)

        @keyword
        def keyword_in_main(self):
            pass

.. sourcecode:: python

    """Library components."""

    from robotlibcore import keyword


    class Library1(object):

        @keyword
        def example(self):
            """Keyword documentation."""
            pass

        @keyword
        def another_example(self, arg1, arg2='default'):
            pass

        def not_keyword(self):
            pass


    class Library2(object):

        @keyword('Custom name')
        def this_name_is_not_used(self):
            pass

        @keyword(tags=['tag', 'another'])
        def tags(self):
            pass


.. _Robot Framework: http://robotframework.org
.. _SeleniumLibrary: https://github.com/robotframework/SeleniumLibrary/
.. _WhiteLibrary: https://pypi.org/project/robotframework-whitelibrary/
.. _hybrid: https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#hybrid-library-api
.. _dynamic library API: https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#dynamic-library-api
.. _User Guide: https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#creating-test-libraries
.. _@keyword: https://github.com/robotframework/robotframework/blob/master/src/robot/api/deco.py
