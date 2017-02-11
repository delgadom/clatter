import shlex
import re
import doctest
import functools

class Runner(object):

    def __init__(self, call_engines=None, default=None):

        if call_engines is None:
            call_engines = {}

        self.call_engines = call_engines

        self.default = default

    def _parse_cli_statement(self, string):
        """
        Parses string statements into command arguments, results, and options

        """

        for i, parsed in enumerate(re.finditer((
                    r'(?<=\n)'
                    r'(?P<space>[\ \t]*)'
                    r'(\$[\ \t]+)'
                    r'(?P<cmd>[^\r\n\\]+(\\[\ \t]*\n[^\n\\]*)*)'
                    r'(?P<res>((\r\n|\n)\ +[^\$\>\s][^\r\n\\]*)'
                    r'*(\\[\ \t]*(\r\n|\n)\g<space>[^\r\n\\]+)*)'
                ), string)):

            command = parsed.group('cmd')
            expected = parsed.group('res')

            expected = re.sub(re.escape('<BLANKLINE>'), '', expected)

            if expected is None:
                expected = ''

            formatted = ''.join(re.split(
                r'\\[\ \t]*(\r\n|\n)[\ \t]*>', command))

            args = shlex.split(formatted, comments=True)
            args_comment = shlex.split(formatted, comments=False)

            assert args == args_comment[:len(args)]

            comments = list(map(
                lambda s: s.upper(), args_comment[len(args)+1:]))

            if 'CLATTER:' in comments:
                option_flags = comments[comments.index('CLATTER:')+1:]
            else:
                option_flags = []

            parser = doctest.DocTestParser()

            options_dict = parser.parse('>>> None # doctest: {}'.format(
                ' '.join(option_flags)))[1].options

            options = options = functools.reduce(
                lambda o1, o2: o1 | o2,
                options_dict.keys(),
                0)

            expected = '\n'.join(map(
                lambda s: s.strip(),
                expected.strip().split('\n')))+'\n'

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
