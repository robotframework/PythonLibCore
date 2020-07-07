from robot.api.deco import keyword


class MockLibrary(object):

    def no_args(self):
        pass

    @keyword(types={'arg1': str, 'arg2': int})
    def positional_args(self, arg1, arg2):
        """Some documentation

        Multi line docs
        """
        pass

    @keyword(types=None)
    def types_disabled(self, arg=False):
        pass

    @keyword
    def positional_and_default(self, arg1, arg2, named1='string1', named2=123):
        pass

    def default_only(self, named1='string1', named2=123):
        pass

    def varargs_kwargs(self, *vargs, **kwargs):
        pass
