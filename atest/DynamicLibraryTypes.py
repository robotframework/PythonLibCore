from typing import List

from robotlibcore import DynamicCore, keyword

import librarycomponents


class DynamicLibraryTypes(DynamicCore):

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

    @keyword
    def keyword_with_one_annotation(self, arg: str):
        return arg

    @keyword
    def keyword_with_multiple_annotations(self, arg1: str, arg2: List):
        return arg1, arg2
