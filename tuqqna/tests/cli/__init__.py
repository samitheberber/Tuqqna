#!/usr/bin/env python

"""\
tuqqna.tests.cli-package init file. This file contains all core test suites.
"""


from tuqqna.tests.cli import TestCliUI
from tuqqna.tests.cli import TestGame


def suites():

    """\
Returns all test suites of cli-package.
"""

    suites = []

    suites.append(TestCliUI.suite()) # Appends suites with TestCliUI-suite.
    suites.append(TestGame.suite()) # Appends suites with TestCliUI-suite.

    return suites
