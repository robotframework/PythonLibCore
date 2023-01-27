from robot.api import logger


from robotlibcore import DynamicCore, keyword


class ListenerCore(DynamicCore):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        self.keyword_name = None
        self.keyword_args = {}
        self.ROBOT_LISTENER_API_VERSION = 2
        second_comp = SecondComponent()
        self.ROBOT_LIBRARY_LISTENER = second_comp.listener
        components = [FirstComponent(), second_comp]
        super().__init__(components)

    @keyword
    def listener_core(self, arg: str):
        logger.info(arg)
        assert arg == self.keyword_args.get("args", [None])[0], "First argument should be detected by listener, but was not."

    def start_keyword(self, name, args):
        self.keyword_name = name
        self.keyword_args = args
        logger.info(f"start: {name}")


class FirstComponent:

    def __init__(self):
        self.ROBOT_LISTENER_API_VERSION = 2
        self.suite_name = ''

    def _start_suite(self, name, attrs):
        self.suite_name = name
        logger.console(f"start suite: {name}")

    @keyword
    def first_component(self, arg: str):
        logger.info(arg)
        assert arg == self.suite_name, f"Suite name '{self.suite_name}' should be detected by listener, but was not."


class SecondComponent:

    def __init__(self):
        self.listener = ExternalListener()

    @keyword
    def second_component(self, arg: str):
        logger.info(arg)
        assert self.listener.test.name == arg, "Test case name should be detected by listener, but was not."


class ExternalListener:

    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self):
        self.test = None

    def start_test(self, test, _):
        self.test = test
