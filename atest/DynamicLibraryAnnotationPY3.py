from robotlibcore import DynamicCore, keyword


class DynamicLibraryAnnotationsPY3(DynamicCore):

    def __init__(self):
        DynamicCore.__init__(self, [])

    @keyword
    def kw_annotated_type(self, arg: int):
        pass

    @keyword(types={'arg1': bool, 'arg2': bool})
    def kw_types_from_deco_and_annotation(self, arg1: int, arg2: int):
        pass

    @keyword
    def kw_annotated_type_with_default(self, arg: str='foobar'):
        pass

