from typing import Optional

from robot.api import logger
from robot.api.deco import keyword


class StringTools:
    @keyword
    def join_strings(self, *strings: str) -> str:
        """Joins args strings."""
        logger.info("Joining.")
        return " ".join(strings)

    @keyword
    def join_string_with_separator(self, *strings, separator: Optional[str] = None):
        """Joins strings with separator"""
        return f"{separator if separator else self.separator}".join(strings)
