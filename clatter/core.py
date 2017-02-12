import shlex
import re
import doctest
import functools


class Runner(object):

    NEWLINE = r'(\n)'
    SPACE = r'(?P<space>[\ \t]*)'
    CMD_START = r'(\$[\ \t]+)'
    CMD_CONTENTS_FIRST = r'(?P<cmd>[^\r\n\\]+'
    CMD_CONTENTS_REST = r'(\\[\ \t]*(\r\n|\n)(?P=space)[^\n\\]+)*)'
    CMD_END_RETURN = r'(\r\n|\n)'
    RESPONSE_PREFIX = r'((?P=space)'
    RESPONSE_FIRST = r'(?P<res>(([^\$\r\n][^\r\n]+(\r\n|\n))'
    RESPONSE_REST = r'((?P=space)[^\$\r\n][^\r\n]+(\r\n|\n))*)))?'

    COMMAND_REGEX = re.compile((
        NEWLINE
        +SPACE
        +CMD_START
        +CMD_CONTENTS_FIRST
        +CMD_CONTENTS_REST
        +CMD_END_RETURN
        +RESPONSE_PREFIX
        +RESPONSE_FIRST
        +RESPONSE_REST))

    def __init__(self, call_engines=None, default=None):

        if call_engines is None:
            call_engines = {}

        self.call_engines = call_engines

        self.default = default

    def _parse_cli_statement(self, string):
        """
        Parses string statements into command arguments, results, and options

        """

        for i, parsed in enumerate(re.finditer(self.COMMAND_REGEX, string)):

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

    def validate(self, command):
        '''
        Checks the result of running command against expected output
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
