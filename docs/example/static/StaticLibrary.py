import time
from typing import Optional

from robot.api import logger


class StaticLibrary:
    def __init__(self):
        self.separator = ";"

    def join_strings(self, *strings: str) -> str:
        """Joins args strings."""
        logger.info("Joining.")
        return " ".join(strings)

    def sum(self, value1: int, value2: int) -> int:
        """Do other thing."""
        logger.info(f"Calculating hard.")
        return value1 + value2

    def wait_something_to_happen(self, arg1: str, arg2: int) -> str:
        self._waiter(0.3)
        arg1 = self.join_strings(arg1, arg1)
        self._waiter(0.2)
        arg2 = self.sum(arg2, arg2)
        self._waiter()
        logger.info("Waiting done")
        return f"{arg1} and {arg2}"

    def join_string_with_separator(self, *strings, separator: Optional[str] =None):
        """Joins strings with separator"""
        return f"{separator if separator else self.separator}".join(strings)

    def _waiter(self, timeout: float = 0.1):
        logger.info(f"Waiting {timeout}")
        time.sleep(timeout)
