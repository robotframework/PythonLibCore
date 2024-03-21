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

Code is stable and is already used by
[SeleniumLibrary](https://github.com/robotframework/SeleniumLibrary/)
and
[Browser library](https://github.com/MarketSquare/robotframework-browser/).
Project supports two latest version of Robot Framework.

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

# Translation

PLC supports translation of keywords names and documentation, but arguments names, tags and types
can not be currently translated. Translation is provided as a file containing
[Json](https://www.json.org/json-en.html) and as a
[Path](https://docs.python.org/3/library/pathlib.html) object. Translation is provided in
`translation` argument in the `HybridCore` or `DynamicCore` `__init__`. Providing translation
file is optional, also it is not mandatory to provide translation to all keyword.

The keys of json are the methods names, not the keyword names, which implements keyword. Value
of key is json object which contains two keys: `name` and `doc`. `name` key contains the keyword
translated name and `doc` contains keyword translated documentation. Providing
`doc` and `name` is optional, example translation json file can only provide translations only
to keyword names or only to documentatin. But it is always recomended to provide translation to
both `name` and `doc`.

Library class documentation and instance documetation has special keys, `__init__` key will
replace instance documentation and `__intro__` will replace libary class documentation.

## Example

If there is library like this:
```python
from pathlib import Path

from robotlibcore import DynamicCore, keyword

class SmallLibrary(DynamicCore):
    """Library documentation."""

    def __init__(self, translation: Path):
        """__init__ documentation."""
        DynamicCore.__init__(self, [], translation.absolute())

    @keyword(tags=["tag1", "tag2"])
    def normal_keyword(self, arg: int, other: str) -> str:
        """I have doc

        Multiple lines.
        Other line.
        """
        data = f"{arg} {other}"
        print(data)
        return data

    def not_keyword(self, data: str) -> str:
        print(data)
        return data

    @keyword(name="This Is New Name", tags=["tag1", "tag2"])
    def name_changed(self, some: int, other: int) -> int:
        """This one too"""
        print(f"{some} {type(some)}, {other} {type(other)}")
        return some + other
```

And when there is translation file like:
```json
{
    "normal_keyword": {
        "name": "other_name",
        "doc": "This is new doc"
    },
    "name_changed": {
        "name": "name_changed_again",
        "doc": "This is also replaced.\n\nnew line."
    },
    "__init__": {
        "name": "__init__",
        "doc": "Replaces init docs with this one."
    },
    "__intro__": {
        "name": "__intro__",
        "doc": "New __intro__ documentation is here."
    },
}
```
Then `normal_keyword` is translated to `other_name`. Also this keyword documentions is
translted to `This is new doc`. The keyword is `name_changed` is translted to
`name_changed_again` keyword and keyword documentation is translted to
`This is also replaced.\n\nnew line.`. The library class documentation is translated
to `Replaces init docs with this one.` and class documentation is translted to
`New __intro__ documentation is here.`
