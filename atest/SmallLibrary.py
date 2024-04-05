from pathlib import Path
from typing import Optional

from robot.api import logger
from robotlibcore import DynamicCore, keyword

class KeywordClass:

    @keyword(name="Execute SomeThing")
    def execute_something(self):
        """This is old"""
        print("Name is here")

class SmallLibrary(DynamicCore):
    """Library documentation."""

    def __init__(self, translation: Optional[Path] = None):
        """__init__ documentation."""
        if not isinstance(translation, Path):
            logger.warn("Convert to Path")
            translation = Path(translation)
        DynamicCore.__init__(self, [KeywordClass()], translation.absolute())

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

    @keyword(name="Name ChanGed", tags=["tag1", "tag2"])
    def name_changed(self, some: int, other: int) -> int:
        """This one too"""
        print(f"{some} {type(some)}, {other} {type(other)}")
        return some + other

    @keyword
    def not_translated(seld, a: int) -> int:
        """This is not replaced."""
        print(f"{a} {type(a)}")
        return a + 1

    @keyword
    def doc_not_translated(seld, a: int) -> int:
        """This is not replaced also."""
        print(f"{a} {type(a)}")
        return a + 1

    @keyword
    def kw_not_translated(seld, a: int) -> int:
        """This is replaced too but name is not."""
        print(f"{a} {type(a)}")
        return a + 1
