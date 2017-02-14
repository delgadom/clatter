import doctest


def test_readme():
    errs, _ = doctest.testfile('../README.rst', report=True)
    assert not errs
