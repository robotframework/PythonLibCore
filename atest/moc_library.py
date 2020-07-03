class MockLibrary(object):

    def no_args(self):
        pass

    def positional_args(self, arg1, arg2):
        """Some documentation

        Multi line docs
        """
        pass

    def positional_and_default(self, arg1, arg2, named1='string1', named2=123):
        pass

    def default_only(self, named1='string1', named2=123):
        pass

    def varargs_kwargs(self, *vargs, **kwargs):
        pass
