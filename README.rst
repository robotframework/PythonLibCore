Python Library Core
===================

Tools to ease creating larger test libraries for `Robot Framework`_ using
Python.

Code is stable and version 1.0 is already used by SeleniumLibrary_.
Better documentation and packaging still to do.

https://github.com/robotframework/PythonLibCore/workflows/CI/badge.svg

Example
-------

.. sourcecode:: python

    """Main library."""

    from robotlibcore import HybridCore

    from mystuff import Library1, Library2


    class MyLibrary(HybridCore):
        """General library documentation."""

        def __init__(self):
            libraries = [Library1(), Library2()]
            HybridCore.__init__(self, libraries)


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
