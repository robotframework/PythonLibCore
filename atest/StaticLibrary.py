from robotlibcore import StaticCore, keyword

import librarycomponents


class StaticLibrary(StaticCore,
                    librarycomponents.Names,
                    librarycomponents.Arguments,
                    librarycomponents.DocsAndTags):
    """General library documentation."""
    class_attribute = 'not keyword'

    def __init__(self):
        self.instance_attribute = 'not keyword'
        self.function = librarycomponents.function
        StaticCore.__init__(self)

    @keyword
    def keyword_in_main(self):
        pass

    def not_keyword_in_main(self):
        pass
