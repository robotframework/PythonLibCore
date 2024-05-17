import os
import sys
from pathlib import Path

from invoke import task
from rellu import ReleaseNotesGenerator, Version, initialize_labels
from rellu.tasks import clean  # noqa

assert Path.cwd() == Path(__file__).parent  # noqa: S101


REPOSITORY = "robotframework/PythonLibCore"
VERSION_PATH = Path("src/robotlibcore/__init__.py")
VERSION_PATTERN = '__version__ = "(.*)"'
RELEASE_NOTES_PATH = Path("docs/PythonLibCore-{version}.rst")
RELEASE_NOTES_TITLE = "Python Library Core {version}"
RELEASE_NOTES_INTRO = """
`Python Library Core`_ is a generic component making it easier to create
bigger `Robot Framework`_ test libraries. Python Library Core {version} is
a new release with **UPDATE** enhancements and bug fixes. **MORE intro stuff**

**REMOVE this section with final releases or otherwise if release notes contain
all issues.**
All issues targeted for Python Library Core {version.milestone} can be found
from the `issue tracker`_.

**REMOVE ``--pre`` from the next command with final releases.**
If you have pip_ installed, just run

::

   pip install --pre --upgrade pip install robotframework-pythonlibcore

to install the latest available release or use

::

   pip install pip install robotframework-pythonlibcore=={version}

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

Python Library Core {version} was released on {date}.

.. _PythonLibCore: https://github.com/robotframework/PythonLibCore
.. _Robot Framework: http://robotframework.org
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-robotlibcore
.. _issue tracker: https://github.com/robotframework/PythonLibCore/issues?q=milestone%3A{version.milestone}
"""


@task
def set_version(ctx, version):  # noqa: ARG001
    """Set project version in ``src/robotlibcore.py`` file.

    Args:
        version: Project version to set or ``dev`` to set development version.

    Following PEP-440 compatible version numbers are supported:
    - Final version like 3.0 or 3.1.2.
    - Alpha, beta or release candidate with ``a``, ``b`` or ``rc`` postfix,
      respectively, and an incremented number like 3.0a1 or 3.0.1rc1.
    - Development version with ``.dev`` postfix and an incremented number like
      3.0.dev1 or 3.1a1.dev2.

    When the given version is ``dev``, the existing version number is updated
    to the next suitable development version. For example, 3.0 -> 3.0.1.dev1,
    3.1.1 -> 3.1.2.dev1, 3.2a1 -> 3.2a2.dev1, 3.2.dev1 -> 3.2.dev2.
    """
    version = Version(version, VERSION_PATH, VERSION_PATTERN)
    version.write()
    print(version)


@task
def print_version(ctx):  # noqa: ARG001
    """Print the current project version."""
    print(Version(path=VERSION_PATH))


@task
def release_notes(ctx, version=None, username=None, password=None, write=False):  # noqa: FBT002, ARG001
    """Generates release notes based on issues in the issue tracker.

    Args:
        version:  Generate release notes for this version. If not given,
                  generated them for the current version.
        username: GitHub username.
        password: GitHub password.
        write:    When set to True, write release notes to a file overwriting
                  possible existing file. Otherwise, just print them to the
                  terminal.

    Username and password can also be specified using ``GITHUB_USERNAME`` and
    ``GITHUB_PASSWORD`` environment variable, respectively. If they aren't
    specified at all, communication with GitHub is anonymous and typically
    pretty slow.
    """
    version = Version(version, VERSION_PATH)
    file = RELEASE_NOTES_PATH if write else sys.stdout
    generator = ReleaseNotesGenerator(
        REPOSITORY,
        RELEASE_NOTES_TITLE,
        RELEASE_NOTES_INTRO,
    )
    generator.generate(version, username, password, file)


@task
def init_labels(ctx, username=None, password=None):  # noqa: ARG001
    """Initialize project by setting labels in the issue tracker.

    Args:
        username: GitHub username.
        password: GitHub password.

    Username and password can also be specified using ``GITHUB_USERNAME`` and
    ``GITHUB_PASSWORD`` environment variable, respectively.

    Should only be executed once when taking ``rellu`` tooling to use or
    when labels it uses have changed.
    """
    initialize_labels(REPOSITORY, username, password)


@task
def lint(ctx):
    in_ci = os.getenv("GITHUB_WORKFLOW")
    print("Run ruff")
    ruff_cmd = ["ruff", "check"]
    if not in_ci:
        ruff_cmd.append("--fix")
    ruff_cmd.append("./src")
    ruff_cmd.append("./tasks.py")
    ruff_cmd.append("./utest")
    ctx.run(" ".join(ruff_cmd))
    print("Run black")
    ctx.run("black src/ tasks.py utest atest/run.py")
    print("Run tidy")
    print(f"Lint Robot files {'in ci' if in_ci else ''}")
    command = [
        "robotidy",
        "--transform",
        "RenameTestCases",
        "-c",
        "RenameTestCases:capitalize_each_word=True",
        "--lineseparator",
        "unix",
        "atest/",
    ]
    if in_ci:
        command.insert(1, "--check")
        command.insert(1, "--diff")
    ctx.run(" ".join(command))


@task
def atest(ctx):
    ctx.run("python atest/run.py")


@task
def utest(ctx):
    ctx.run("python utest/run.py")


@task(utest, atest)
def test(ctx):  # noqa: ARG001
    pass
