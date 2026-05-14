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

## Installation
To install this library, run the following command in your terminal:
``` bash
pip install robotframework-pythonlibcore
```
This command installs the latest version of `robotframework-pythonlibcore`, ensuring you have all the current features and updates.

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

PLC supports translation of keywords names and documentation. Translations must be provided in 
the `translation` argument in the `HybridCore`  or `DynamicCore` `__init__`, either as a 
dictionary or through a [Path](https://docs.python.org/3/library/pathlib.html) to a 
[JSON](https://www.json.org/json-en.html) file. Providing translation data is optional, also it 
is not mandatory to provide translation to all keyword.

The keys of the dictionary are the methods names, not the keyword names, which implements keyword. 
Values are objects which contains two keys: `name` and `doc`. `name` key contains the keyword
translated name and `doc` contains keyword translated documentation. Providing
`doc` and `name` is optional, i.e. translations data can also provide translations only
to keyword names or only to documentation. But it is always recommended to provide translation to
both `name` and `doc`.

Library class documentation and instance documentation has special keys, `__init__` key will
replace instance documentation and `__intro__` will replace library class documentation.

> [!NOTE]
> Arguments names, tags and types can not be currently translated.

## Example

If there is library like this:
```python
from robotlibcore import DynamicCore, keyword

class SmallLibrary(DynamicCore):
    """Library documentation."""

    def __init__(self):
        """__init__ documentation."""
        DynamicCore.__init__(self, [])

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

And we want to translate it as follows:

- keyword `normal_keyword` to `other_name`
  - its documentation to `This is new doc`
- keyword `name_changed` to `name_changed_again`
  - its documentation to `This is also replaced.\n\nnew line.`.
- the library constructor documentation to `Replaces init docs with this one.`
- the library documentation to `New __intro__ documentation is here.`


### Provide Translation As File

To provide the translation as a file, simply pass the path to a JSON file containing the translations:

```jsonc
// my_translation.json
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
    }
}
```

```python
from pathlib import Path

class SmallLibrary(DynamicCore):
    """Library documentation."""

    def __init__(self):
        """__init__ documentation."""
        DynamicCore.__init__(self, [], translation=Path("/path/to/my_translation.json"))

    # ...
```

> [!IMPORTANT]
> Translation files passed as paths must always be in JSON format.

### Provide Translation As Dictionary

You can also pass the translation data as a dictionary:

```python
import json
from pathlib import Path

class SmallLibrary(DynamicCore):
    """Library documentation."""

    def __init__(self):
        """__init__ documentation."""
        translation_data = json.loads(Path("/path/to/my_translation.json").read_text(encoding="utf-8"))
        DynamicCore.__init__(self, [], translation=translation_data)

    # ...
```

This also allows you to use other data formats such as YAML:

```yaml
normal_keyword:
  name: other_name
  doc: This is new doc
name_changed:
  name: name_changed_again
  doc: |
    This is also replaced.

    new line.
__init__:
  name: __init__
  doc: Replaces init docs with this one.
__intro__:
  name: __intro__
  doc: New __intro__ documentation is here.
```

```python
import yaml
from pathlib import Path

class SmallLibrary(DynamicCore):
    """Library documentation."""

    def __init__(self, translation_file: Path):
        """__init__ documentation."""
        translation_data = yaml.safe_load(translation_file.read_text(encoding="utf-8"))
        DynamicCore.__init__(self, [], translation=translation_data)

    # ...
```
