from robotlibcore import DynamicCore, keyword


class DynamicTypesLibrary(DynamicCore):

    def __init__(self, arg=None):
        DynamicCore.__init__(self, [])
        self.instance_attribute = 'not keyword'
        self.arg = arg

    @keyword(types={'arg1': str})
    def keyword_with_types(self, arg1):
        return arg1

    @keyword(types=None)
    def keyword_with_disabled_types(self, arg1):
        return arg1

    @keyword(types={'arg1': str})
    def keyword_with_one_type(self, arg1, arg2):
        return arg1, arg2

    @keyword
    def keyword_with_no_args(self):
        return False

    def not_keyword(self):
        return False

    @keyword
    def keyword_default_types(self, arg=None):
        return arg

    @keyword
    def keyword_many_default_types(self, arg1=1, arg2='Foobar'):
        return arg1, arg2

    @keyword
    def keyword_booleans(self, arg1=True, arg2=False):
        return '%s: %s, %s: %s' % (arg1, type(arg1), arg2, type(arg2))

    @keyword
    def keyword_none(self, arg=None):
        return '%s: %s' % (arg, type(arg))
