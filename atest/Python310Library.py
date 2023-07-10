from robot.api import logger
from robotlibcore import DynamicCore, keyword


class Python310Library(DynamicCore):

    def __init__(self) -> None:
        DynamicCore.__init__(self, [])

    @keyword
    def python310_style(self, arg: int | dict):
        typing = f"arg: {arg}, type: {type(arg)}"
        logger.info(typing)
        return typing
