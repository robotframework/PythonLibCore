class MockLibraryPy3:

    def named_only(self, *varargs, key1, key2):
        pass

    def named_only_with_defaults(self, *varargs, key1, key2, key3='default1', key4=True):
        pass

    def args_with_type_hints(self, arg1, arg2, arg3: str, arg4: None) -> bool:
        pass
