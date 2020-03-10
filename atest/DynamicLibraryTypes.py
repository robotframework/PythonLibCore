from robotlibcore import DynamicCore, keyword

import librarycomponents


class DynamicLibraryTypes(DynamicCore):

    def __init__(self, arg=None):
        # components = [librarycomponents,
        #               librarycomponents.Names(),
        #               librarycomponents.Arguments(),
        #               librarycomponents.DocsAndTags()]
        DynamicCore.__init__(self, [])
        self.instance_attribute = 'not keyword'

    @keyword(types={'arg1': str})
    def keyword_in_main(self, arg1):
        return arg1
