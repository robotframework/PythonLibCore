# Python Library Core

Tools to ease creating larger test libraries for [Robot
Framework](http://robotframework.org) using Python. The Robot Framework
[hybrid](https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#hybrid-library-api)
and [dynamic library
API](https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#dynamic-library-api)
gives more flexibility for library than the static library API, but they
also sets requirements for libraries which needs to be implemented in
the library side. PythonLibCore eases the problem by providing simpler
interface and handling all the requirements towards the Robot Framework
library APIs.

Code is stable and version 1.0 is already used by
[SeleniumLibrary](https://github.com/robotframework/SeleniumLibrary/)
and
[WhiteLibrary](https://pypi.org/project/robotframework-whitelibrary/).
The version 2.0 support changes in the Robot Framework 3.2.

[![Version](https://img.shields.io/pypi/v/robotframework-pythonlibcore.svg)](https://pypi.python.org/pypi/robotframework-pythonlibcore/)
[![Actions Status](https://github.com/robotframework/PythonLibCore/workflows/CI/badge.svg)](https://github.com/robotframework/PythonLibCore/actions)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Usage

There are two ways to use PythonLibCore, either by
`HybridCore` or by using `DynamicCore`. `HybridCore` provides support for
the hybrid library API and `DynamicCore` provides support for dynamic library API.
Consult the Robot Framework [User
Guide](https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#creating-test-libraries),
for choosing the correct API for library.

Regardless which library API is chosen, both have similar requirements.

1)  Library must inherit either the `HybridCore` or `DynamicCore`.
2)  Library keywords must be decorated with Robot Framework
    [\@keyword](https://github.com/robotframework/robotframework/blob/master/src/robot/api/deco.py)
    decorator.
3)  Provide a list of class instances implementing keywords to
    `library_components` argument in the `HybridCore` or `DynamicCore` `__init__`.

It is also possible implement keywords in the library main class, by marking method with
`@keyword` as keywords. It is not required pass main library instance in the
`library_components` argument.

All keyword, also keywords implemented in the classes outside of the
main library are available in the library instance as methods. This
automatically publish library keywords in as methods in the Python
public API.

The example in below demonstrates how the PythonLibCore can be used with
a library.

# Example

``` python
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
```

``` python
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
```

# Plugin API

It is possible to create plugin API to a library by using PythonLibCore.
This allows extending library with external Python classes. Plugins can
be imported during library import time, example by defining argumet in
library [\_\_init\_\_]{.title-ref} which allows defining the plugins. It
is possible to define multiple plugins, by seperating plugins with with
comma. Also it is possible to provide arguments to plugin by seperating
arguments with semicolon.

``` python
from robot.api.deco import keyword  # noqa F401

from robotlibcore import DynamicCore, PluginParser

from mystuff import Library1, Library2


class PluginLib(DynamicCore):

    def __init__(self, plugins):
        plugin_parser = PluginParser()
        libraries = [Library1(), Library2()]
        parsed_plugins = plugin_parser.parse_plugins(plugins)
        libraries.extend(parsed_plugins)
        DynamicCore.__init__(self, libraries)
```

When plugin class can look like this:

``` python
class MyPlugi:

    @keyword
    def plugin_keyword(self):
        return 123
```

Then Library can be imported in Robot Framework side like this:

``` robotframework
Library    ${CURDIR}/PluginLib.py    plugins=${CURDIR}/MyPlugin.py
```
