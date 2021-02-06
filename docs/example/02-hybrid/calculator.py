from robot.api import logger
from robot.api.deco import keyword


class Calculator:
    @keyword
    def sum(self, value1: int, value2: int) -> int:
        """Do other thing."""
        logger.info(f"Calculating hard.")
        return value1 + value2
