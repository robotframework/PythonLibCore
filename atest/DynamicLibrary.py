from robotlibcore import DynamicCore

import librarycomponents


class DynamicLibrary(DynamicCore):
    """General library documentation."""
    class_attribute = 'not keyword'

    def __init__(self, arg=None):
        """Library init doc."""
        components = [librarycomponents,
                      librarycomponents.Names(),
                      librarycomponents.Arguments(),
                      librarycomponents.DocsAndTags()]
        DynamicCore.__init__(self, components)
        self.instance_attribute = 'not keyword'
