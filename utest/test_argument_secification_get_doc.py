from robotlibcore import ArgumentSpecification


def test_no_doc():
    spec = ArgumentSpecification()
    assert spec.documentation is None
    spec = ArgumentSpecification(documentation=None)
    assert spec.documentation is None


def test_doc():
    spec = ArgumentSpecification(documentation='some doc')
    assert spec.documentation == 'some doc'
