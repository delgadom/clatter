
from __future__ import absolute_import

from clatter import Runner
from clatter.validators import (
    SubprocessValidator)


def testfile():

    tester = Runner()
    tester.call_engines['echo'] = SubprocessValidator()
    tester.call_engines['python'] = SubprocessValidator()
    tester.call_engines['cat'] = SubprocessValidator()

    tester.testfile('tests/resources/sample_doc.txt')
