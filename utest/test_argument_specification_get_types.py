from robotlibcore import ArgumentSpecification


def test_no_types():
    spec = ArgumentSpecification()
    assert spec.typing_hints is None
    spec = ArgumentSpecification(typing_hints=None)
    assert spec.typing_hints is None


def test_types():
    spec = ArgumentSpecification(typing_hints={'arg1': str, 'arg2': None})
    assert spec.typing_hints == {'arg1': str, 'arg2': None}
