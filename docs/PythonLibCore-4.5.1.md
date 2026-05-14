# Python Library Core 4.5.1


[Python Library Core](https://github.com/robotframework/PythonLibCore)
is a generic component making it easier to create bigger
[Robot Framework](http://robotframework.org) test libraries. Python Library Core
4.5.1 is a new hotfix release with fixes bug in opening localization files.

All issues targeted for Python Library Core v4.5.1 can be found
from the
[issue tracker](https://github.com/robotframework/PythonLibCore/issues?q=milestone%3Av4.5.1).

If you have pip_ installed, just run

```bash
   pip install --upgrade pip install robotframework-pythonlibcore
```

to install the latest available release or use

```bash
   pip install pip install robotframework-pythonlibcore==4.5.1
```

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

Python Library Core 4.5.1 was released on Thursday May 14, 2026.


## Most important enhancements


### Specify UTF-8 encoding for translation file opening ([#172](https://github.com/robotframework/PythonLibCore/issues/172))
There was bug when opening localization files with wrong encoding at Windows.
This is now fixed. Many thanks for Yuri Verweij for providing fix to the problem.

## Full list of fixes and enhancements

| ID | Type | Priority | Summary |
|---|---|---|---|
| [#172](https://github.com/robotframework/PythonLibCore/issues/172) | bug | high | Specify UTF-8 encoding for translation file opening |

Altogether 1 issue. View on the [issue tracker](https://github.com/robotframework/PythonLibCore/issues?q=milestone%3Av4.5.1).
