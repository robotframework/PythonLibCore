from robotlibcore import HybridCore, keyword

import librarycomponents


class HybridLibrary(HybridCore):
    """General library documentation."""
    class_attribute = 'not keyword'

    def __init__(self):
        components = [librarycomponents,
                      librarycomponents.Names(),
                      librarycomponents.Arguments(),
                      librarycomponents.DocsAndTags()]
        HybridCore.__init__(self, components)
        self.instance_attribute = 'not keyword'

    @keyword
    def keyword_in_main(self):
        pass

    def not_keyword_in_main(self):
        pass
