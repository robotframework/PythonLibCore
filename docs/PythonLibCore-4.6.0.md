# Python Library Core 4.6.0


[Python Library Core](https://github.com/robotframework/PythonLibCore)
is a generic component making it easier to create bigger
[Robot Framework](http://robotframework.org) test libraries. Python Library Core
4.6.0 is a new release with allows defining translation with a dictionary and
requires Python 3.10+. Support for Python 3.8 and 3.9 are dropped.

All issues targeted for Python Library Core v4.6.0 can be found
from the
[issue tracker](https://github.com/robotframework/PythonLibCore/issues?q=milestone%3Av4.6.0).

If you have pip_ installed, just run

```bash
   pip install --upgrade pip install robotframework-pythonlibcore
```

to install the latest available release or use

```bash
   pip install pip install robotframework-pythonlibcore==4.6.0
```

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

Python Library Core 4.6.0 was released on Thursday May 14, 2026.


## Most important enhancements

### Support Python 3.10+ ([#174](https://github.com/robotframework/PythonLibCore/issues/174))
This release drops support for Python 3.8 and 3.9. Python 3.10+ is required from
this release onwards.

## Acknowledgements

### Support also dictionaries as translations source ([#176](https://github.com/robotframework/PythonLibCore/issues/176))
Many thanks for Basti csvtuda to provide PR to enhance translation support. Now
the translation can be also provided as dictionary. The json file format
support stays as it is. This is just an extending the support.

## Full list of fixes and enhancements

| ID | Type | Priority | Summary |
|---|---|---|---|
| [#174](https://github.com/robotframework/PythonLibCore/issues/174) | feature | high | Support Python 3.10+ |
| [#176](https://github.com/robotframework/PythonLibCore/issues/176) | feature | high | Support also dictionaries as translations source |

Altogether 2 issues. View on the [issue tracker](https://github.com/robotframework/PythonLibCore/issues?q=milestone%3Av4.6.0).
