import shlex
import re
import doctest
import functools


class Runner(object):

    _NEWLINE = r'(\n)'
    _SPACE = r'(?P<space>[\ \t]*)'
    _CMD_START = r'(\$[\ \t]+)'
    _CMD_CONTENTS_FIRST = r'(?P<cmd>[^\r\n\\]+'
    _CMD_CONTENTS_REST = r'(\\[\ \t]*(\r\n|\n)(?P=space)[^\n\\]+)*)'
    _CMD_END_RETURN = r'(\r\n|\n)'
    _RESPONSE_PREFIX = r'((?P=space)'
    _RESPONSE_FIRST = r'(?P<res>(([^\$\r\n][^\r\n]+(\r\n|\n))'
    _RESPONSE_REST = r'((?P=space)[^\$\r\n][^\r\n]+(\r\n|\n))*)))?'

    _COMMAND_REGEX = re.compile((
        _NEWLINE
        + _SPACE
        + _CMD_START
        + _CMD_CONTENTS_FIRST
        + _CMD_CONTENTS_REST
        + _CMD_END_RETURN
        + _RESPONSE_PREFIX
        + _RESPONSE_FIRST
        + _RESPONSE_REST))

    def __init__(self, call_engines=None, default=None):

        if call_engines is None:
            call_engines = {}

        self.call_engines = call_engines

        self.default = default

    def _parse_cli_statement(self, string):
        """
        Parses string statements into command arguments, results, and options

        """

        for i, parsed in enumerate(re.finditer(self._COMMAND_REGEX, string)):

            space = parsed.group('space')
            command = parsed.group('cmd')
            expected = parsed.group('res')

            if expected is None:
                expected = ''

            formatted = ''.join(re.split(
                r'\\[\ \t]*(\r\n|\n){}>'.format(re.escape(space)), command))

            args = shlex.split(formatted, comments=True)
            args_comment = shlex.split(formatted, comments=False)

            assert args == args_comment[:len(args)]

            comments = list(map(
                lambda s: s.upper(), args_comment[len(args)+1:]))

            if 'DOCTEST:' in comments:
                option_flags = comments[comments.index('DOCTEST:')+1:]
            else:
                option_flags = []

            parser = doctest.DocTestParser()

            options_dict = parser.parse('>>> None # doctest: {}'.format(
                ' '.join(option_flags)))[1].options

            options = options = functools.reduce(
                lambda o1, o2: o1 | o2,
                options_dict.keys(),
                0)

            # Remove extra leading space from lines 1+ in expected
            expected = functools.reduce(
                lambda first, second: first + '\n' + second[len(space):],
                expected.split('\n'))

            yield args, expected, options

    def teststring(self, command):
        '''
        Checks command blocks in a string
        '''

        for command, expected, options in self._parse_cli_statement(command):

            if command[0] not in self.call_engines:
                raise ValueError(
                    'Command "{}" not allowed. '.format(command[0]) +
                    'Add command caller to call_engines to whitelist.')

            call_engine = self.call_engines[command[0]]

            call_engine.validate(
                command=command[0],
                args=command[1:],
                expected=expected,
                options=options)

    def testfile(self, filepath):
        '''
        Checks command blocks in a file
        '''

        with open(filepath, 'r') as f:
            self.teststring(f.read())
