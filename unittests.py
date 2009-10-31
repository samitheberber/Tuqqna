#!/usr/bin/env python

"""\
Unittests-file contains all information to launch unit test framework.

To run tests, just run this file and you will see the result of tests.
"""


import sys
from cStringIO import StringIO
import unittest

from tuqqna import tests

def main():

    old_stdout, old_stderr = sys.stdout, sys.stderr
    sys.stdout = StringIO()
    sys.stderr = StringIO()

    unittest.TextTestRunner(verbosity=2).run(tests.getTestSuites())

    old_stdout.write(sys.stdout.getvalue())
    old_stderr.write(sys.stderr.getvalue())


if __name__ == "__main__":
    main()
