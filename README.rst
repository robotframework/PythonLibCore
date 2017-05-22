Python Library Core
===================

Tools to ease creating larger test libraries for `Robot Framework`_ using
Python.

Code ought to be pretty much ready and it is already used by Selenium2Library.
Better documentation and packaging still to do.

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
