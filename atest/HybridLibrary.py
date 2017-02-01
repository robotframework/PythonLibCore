from robotlibcore import HybridCore

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
