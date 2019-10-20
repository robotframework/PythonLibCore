from robotlibcore import DynamicCore, keyword


class DynamicLibraryAnnotations(DynamicCore):

    def __init__(self):
        DynamicCore.__init__(self, [])

    @keyword
    def kw_no_args(self):
        pass

    @keyword
    def kw_no_type(self, arg):
        pass

    @keyword(types=[int, list])
    def kw_types_from_deco_as_list(self, arg1, arg2):
        pass

    @keyword(types={'arg1': int, 'arg2': bool})
    def kw_types_from_deco_as_dict(self, arg1, arg2):
        pass

    @keyword
    def kw_types_from_default_type(self, arg1=True, arg2=None):
        pass

    @keyword
    def kw_types_from_varargs(self, arg=False, *varargs):
        pass

    @keyword
    def kw_types_from_kwargs(self, **kwargs):
        pass
