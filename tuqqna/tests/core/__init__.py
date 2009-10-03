#!/usr/bin/env python

"""\
tuqqna.tests.core-package init file. This file contains all core test suites.
"""


from tuqqna.tests.core import TestBoard


def suites():

    """\
Returns all test suites of core-package.
"""

    suites = []

    suites.append(TestBoard.suite()) # Appends suites with TestBoard-suite.

    return suites
