from typing import List

from robotlibcore import DynamicCore, keyword


class DynamicLibraryTypesAnnotations(DynamicCore):

    def __init__(self, arg=None):
        DynamicCore.__init__(self, [])
        self.instance_attribute = 'not keyword'
        self.arg = arg

    @keyword
    def keyword_with_one_annotation(self, arg: str):
        return arg

    @keyword
    def keyword_with_multiple_annotations(self, arg1: str, arg2: List):
        return arg1, arg2
