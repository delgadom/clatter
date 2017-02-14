import doctest


def test_readme():
    errs, _ = doctest.testfile('../README.rst', report=True)
    if errs > 0:
        raise ValueError(
            '{} errors encountered in README.rst'.format(
                errs))
