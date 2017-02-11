
import os
import click
import pytest
from click.testing import CliRunner
from clatter import Runner
from clatter.validators import (
    ClickValidator,
    SubprocessValidator,
    SkipValidator)


@click.command()
@click.argument('name')
def hello(name):
    click.echo('Hello %s!' % name)


@click.command()
@click.argument('name')
def badcmd(name):
    raise IOError("This command doesn't work!")

def test_hello_world():
    runner = CliRunner()
    result = runner.invoke(hello, ['Peter'])
    assert result.exit_code == 0
    assert result.output == 'Hello Peter!\n'

def test_string_command():

    teststr = '''

    .. code-block:: bash

        $ hello Polly
        Hello Polly!

        $ hello Polly Parrot
        Usage: hello [OPTIONS] NAME
        <BLANKLINE>
        Error: Got unexpected extra argument (Parrot)

        $ hello 'Polly Parrot' # clatter: +NORMALIZE_WHITESPACE
        Hello Polly Parrot!

    '''

    tester = Runner()
    tester.call_engines['hello'] = ClickValidator(hello)

    tester.validate(teststr)

def test_bad_command():

    badstr = '''

    .. code-block:: bash

        $ badcmd Polly # clatter: +ELLIPSIS +NORMALIZE_WHITESPACE
        Traceback (most recent call last):
        ...
        IOError: This command doesn't work!

    '''

    tester = Runner()
    tester.call_engines['badcmd'] = ClickValidator(badcmd)

    tester.validate(badstr)

def test_validator():

    teststr = r'''

    .. code-block:: bash

        $ hello Polly
        Hello Polly!

        $ echo 'Pining for the fjords'
        Pining for the fjords

    Pipes don't work, so we can't redirect this value into a file. But we can
    write a file with python:

    .. code-block:: bash

        $ python -c \
        >     "with open('tmp.txt', 'w+') as f: f.write('Pushing up daisies')"

        $ cat tmp.txt
        Pushing up daisies

    '''

    tester = Runner()
    tester.call_engines['hello'] = ClickValidator(hello)
    tester.call_engines['echo'] = SubprocessValidator()
    tester.call_engines['python'] = SubprocessValidator()
    tester.call_engines['cat'] = SubprocessValidator()

    tester.validate(teststr)

    badstr = '''

    The following block of code should cause an error:

    .. code-block:: bash

        $ rm tmp.txt

    '''

    with pytest.raises(ValueError):
        tester.validate(badstr)

    os.remove('tmp.txt')


def test_skipper():

    skipstr = '''

    The following command will be skipped:

    .. code-block:: bash

        $ aws storage buckets list

    '''

    tester = Runner()
    tester.call_engines['aws'] = SkipValidator()

    tester.validate(skipstr)


    noskip = '''

    Unrecognized commands will raise an error, even if +SKIP is specified

    .. code-block:: bash

        $ nmake all # clatter: +SKIP

    '''

    with pytest.raises(ValueError):
        tester.validate(noskip)


def test_string_failure():

    teststr = r'''

    Lines failing to match the command's output will raise an error

    .. code-block:: bash

        $ echo "There, it moved!"
        "No it didn't!"
        <BLANKLINE>

    '''

    tester = Runner()
    tester.call_engines['echo'] = SubprocessValidator()

    with pytest.raises(ValueError):
        tester.validate(teststr)


def test_skip():

    teststr = r'''

    Of course, you can always skip them!

    .. code-block:: bash

        $ echo "There, it moved!" # clatter: +SKIP
        "No it didn't!"
        <BLANKLINE>

    '''

    tester = Runner()
    tester.call_engines['echo'] = SubprocessValidator()

    tester.validate(teststr)