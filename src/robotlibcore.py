import inspect
import sys

try:
    from robot.api.deco import keyword
except ImportError:  # Support RF < 2.9
    def keyword(name=None, tags=()):
        if callable(name):
            return keyword()(name)
        def decorator(func):
            func.robot_name = name
            func.robot_tags = tags
            return func
        return decorator


PY2 = sys.version_info < (3,)


class HybridCore(object):

    def __init__(self, libraries):
        self.keywords = dict(self._find_keywords(*libraries))
        self.keywords.update(self._find_keywords(self))

    def _find_keywords(self, *libraries):
        for library in libraries:
            for name, func in self._get_members(library):
                if callable(func) and hasattr(func, 'robot_name'):
                    kw_name = func.robot_name or name
                    yield kw_name, getattr(library, name)

    def _get_members(self, library):
        # Avoid calling properties by getting members from class, not instance.
        if inspect.isclass(library):
            library = type(library)
        return inspect.getmembers(library)

    def __getattr__(self, name):
        if name in self.keywords:
            return self.keywords[name]
        raise AttributeError('{!r} object has no attribute {!r}'
                             .format(type(self).__name__, name))

    def __dir__(self):
        if PY2:
            my_attrs = dir(type(self)) + list(self.__dict__)
        else:
            my_attrs = super().__dir__()
        return sorted(set(my_attrs + list(self.keywords)))

    def get_keyword_names(self):
        return sorted(self.keywords)


class DynamicCore(HybridCore):

    def run_keyword(self, name, args, kwargs):
        return self.keywords[name](*args, **kwargs)

    def get_keyword_arguments(self, name):
        kw = self.keywords[name] if name != '__init__' else self.__init__
        args, defaults, varargs, kwargs = self._get_arg_spec(kw)
        args += ['{}={}'.format(name, value) for name, value in defaults]
        if varargs:
            args.append('*{}'.format(varargs))
        if kwargs:
            args.append('**{}'.format(kwargs))
        return args

    def _get_arg_spec(self, kw):
        spec = inspect.getargspec(kw)
        args = spec.args[1:] if inspect.ismethod(kw) else spec.args  # drop self
        defaults = spec.defaults or ()
        nargs = len(args) - len(defaults)
        mandatory = args[:nargs]
        defaults = zip(args[nargs:], defaults)
        return mandatory, defaults, spec.varargs, spec.keywords

    def get_keyword_documentation(self, name):
        doc, tags = self._get_doc_and_tags(name)
        doc = doc or ''
        tags = 'Tags: {}'.format(', '.join(tags)) if tags else ''
        sep = '\n\n' if doc and tags else ''
        return doc + sep + tags

    def _get_doc_and_tags(self, name):
        if name == '__intro__':
            return inspect.getdoc(self), None
        if name == '__init__':
            return inspect.getdoc(self.__init__), None
        kw = self.keywords[name]
        return inspect.getdoc(kw), kw.robot_tags
