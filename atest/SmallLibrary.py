from pathlib import Path
from typing import Optional

from robot.api import logger
from robotlibcore import DynamicCore, keyword

class SmallLibrary(DynamicCore):
    """Library documentation."""

    def __init__(self, translation: Optional[Path] = None):
        """__init__ documentation."""
        logger.warn(translation.absolute())
        logger.warn(type(translation))
        
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
