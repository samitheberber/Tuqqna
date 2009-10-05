#!/usr/bin/env python

"""\
tuqqna.tests-package init file. This file contains all test suites.
"""


import unittest

from tuqqna.tests import ai
from tuqqna.tests import cli
from tuqqna.tests import core
from tuqqna.tests import gui


def getTestSuites():

    """\
Collects all tests in one suite.
"""

    suites = unittest.TestSuite()

    _parseSuitesFromSubSuites(suites, ai.suites()) # Adds core suites in all tests suite.
    _parseSuitesFromSubSuites(suites, cli.suites()) # Adds core suites in all tests suite.
    _parseSuitesFromSubSuites(suites, core.suites()) # Adds core suites in all tests suite.
    _parseSuitesFromSubSuites(suites, gui.suites()) # Adds core suites in all tests suite.

    return suites


def _parseSuitesFromSubSuites(suite, subsuites):

    """\
Parses subsuites and add them in suite.
"""

    for subsuite in subsuites:
        suite.addTest(subsuite)
