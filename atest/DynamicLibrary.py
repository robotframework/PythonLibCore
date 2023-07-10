import librarycomponents
from robotlibcore import DynamicCore, keyword


class DynamicLibrary(DynamicCore):
    """General library documentation."""
    class_attribute = 'not keyword'

    def __init__(self, arg=None) -> None:
        """Library init doc."""
        components = [librarycomponents,
                      librarycomponents.Names(),
                      librarycomponents.Arguments(),
                      librarycomponents.DocsAndTags()]
        DynamicCore.__init__(self, components)
        self.instance_attribute = 'not keyword'

    @keyword
    def keyword_in_main(self):
        pass

    def not_keyword_in_main(self):
        pass
