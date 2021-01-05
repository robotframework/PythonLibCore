from robotlibcore import keyword


@keyword
def function():
    return 1


class Names:
    attribute = 'not keyword'

    @keyword
    def method(self):
        return 2

    @keyword('Custom name')
    def _custom_name(self):
        return 3

    def not_keyword(self):
        pass

    @keyword
    def keyword_in_main(self):
        raise AssertionError('Should be overridden by the main library!')

    @property
    def dont_touch_property(self):
        raise RuntimeError('Should not touch property!!')


class Arguments:

    @keyword
    def mandatory(self, arg1, arg2):
        return self.format_args(arg1, arg2)

    @keyword
    def defaults(self, arg1, arg2='default', arg3=3):
        return self.format_args(arg1, arg2, arg3)

    @keyword
    def varargs_and_kwargs(self, *args, **kws):
        return self.format_args(*args, **kws)

    @keyword
    def kwargs_only(self, **kws):
        return self.format_args(**kws)

    @keyword
    def all_arguments(self, mandatory, default='value', *varargs, **kwargs):
        return self.format_args(mandatory, default, *varargs, **kwargs)

    @keyword('Embedded arguments "${here}"')
    def embedded(self, arg):
        assert arg == 'work', arg

    def format_args(self, *args, **kwargs):
        def ru(item):
            return repr(item).lstrip('u')
        args = [ru(a) for a in args]
        kwargs = ['{}={}'.format(k, ru(kwargs[k])) for k in sorted(kwargs)]
        return ', '.join(args + kwargs)


class DocsAndTags:

    @keyword
    def one_line_doc(self):
        """I got doc!"""

    @keyword
    def multi_line_doc(self):
        """I got doc!

        With multiple lines!!
        Yeah!!!!
        """

    @keyword(tags=['tag', 'another tag'])
    def tags(self):
        pass

    @keyword(tags=['tag'])
    def doc_and_tags(self):
        """I got doc!"""
