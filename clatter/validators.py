import traceback
import doctest
import subprocess
from click.testing import CliRunner


class CommandValidator(object):

    def validate(self, command, args, expected, options):

        if (options & doctest.SKIP):
            return

        stdout, stderr = self.run_command(command, args)

        checker = doctest.OutputChecker()

        if checker.check_output(expected.rstrip(), stdout.rstrip(), options):
            return

        if checker.check_output(expected.rstrip(), stderr.rstrip(), options):
            return

        msg = 'Clatter test failed. {0} != {1}\n\n+ {0}\n- {1}'.format(
            (stdout if stdout else stderr),
            expected)

        raise ValueError(msg)


class ClickValidator(CommandValidator):

    def __init__(self, app, prefix=None):
        super(ClickValidator, self).__init__()

        self.app = app

        if prefix is None:
            prefix = []

        self.prefix = prefix

    def run_command(self, command, args):

        runner = CliRunner()

        result = runner.invoke(self.app, self.prefix + args)

        tb = ''.join(traceback.format_exception(*result.exc_info))

        return result.output, tb


class SkipValidator(CommandValidator):

    def __init__(self):
        super(SkipValidator, self).__init__()

    def validate(self, command, args, expected, options):
        pass


class SubprocessValidator(CommandValidator):

    def __init__(self):
        super(SubprocessValidator, self).__init__()

    def run_command(self, command, args):

        p = subprocess.Popen(
            [command] + args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        p.wait()

        return p.communicate()
