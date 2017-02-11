
from clatter import Runner

def test_parser_1():

    tester = Runner()

    test = r'''
    .. code-block:: bash

        $ echo "my string"
        ['echo', 'my string']

    '''

    next(tester._parse_cli_statement(test))
    (['echo', 'my string'], "['echo', 'my string']", {})


def test_parser_2():

    tester = Runner()

    test = r'''

    This is the first block. It has an error.

    .. code-block:: bash

        $ pytest test_nonexistant.py --cov=mymodule \
        >     --cov=docs --doctest-modules \
        >     --cov-report term-missing \
        >     # clatter: +ELLIPSIS +NORMALIZE_WHITESPACE
        Traceback (most recent call last):
        ...
        ERROR: file not found: test_nonexistant.py

        $ pytest test_real.py --cov=mymodule \
        >     --cov=docs --doctest-modules \
        >     --cov-report term-missing # clatter: +SKIP

    '''

    parser = tester._parse_cli_statement(test)

    expected = (
        [
            'pytest',
            'test_nonexistant.py',
            '--cov=mymodule',
            '--cov=docs',
            '--doctest-modules',
            '--cov-report',
            'term-missing'],
        (
            'Traceback (most recent call last):'\
            '\n...\n'\
            'ERROR: file not found: test_nonexistant.py\n'),
        12)

    assert next(parser) == expected

    assert next(parser) == (
        [
            'pytest',
            'test_real.py',
            '--cov=mymodule',
            '--cov=docs',
            '--doctest-modules',
            '--cov-report',
            'term-missing'],
        '\n',
        16)
