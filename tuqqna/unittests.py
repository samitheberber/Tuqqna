#!/usr/bin/env python

"""\
Unittests-file contains all information to launch unit test framework.

To run tests, just run this file and you will see the result of tests.
"""


import unittest

import tests


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(tests.getTestSuites())
