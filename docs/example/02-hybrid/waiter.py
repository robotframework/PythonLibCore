import time

from robot.api import logger
from robot.api.deco import keyword


class Waiter:
    @keyword
    def wait_something_to_happen(self, arg1: str, arg2: int) -> str:
        self.waiter(0.3)
        arg1 = self.join_strings(arg1, arg1)
        self.waiter(0.2)
        arg2 = self.sum(arg2, arg2)
        self.waiter()
        logger.info("Waiting done")
        return f"{arg1} and {arg2}"

    def waiter(self, timeout: float = 0.1):
        logger.info(f"Waiting {timeout}")
        time.sleep(timeout)
