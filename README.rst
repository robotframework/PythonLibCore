Python Library Core
===================

Tools to ease creating larger test libraries for `Robot Framework`_ using
Python.

At the moment work-in-progress. Planned to be used with Selenium2Library.

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
