from HybridLibrary import HybridLibrary, keyword


class ExtendExistingLibrary(HybridLibrary):

    def __init__(self):
        HybridLibrary.__init__(self)
        self.add_library_components([ExtendingComponent()])


class ExtendingComponent:

    @keyword
    def keyword_in_extending_library(self):
        pass
