#!/usr/bin/env python

"""\
tuqqna.tests.core-package init file. This file contains all core test suites.
"""


from tuqqna.tests.core import TestBoard
from tuqqna.tests.core import TestButton
from tuqqna.tests.core import TestGame
from tuqqna.tests.core import TestPlayer
from tuqqna.tests.core import TestRules


def suites():

    """\
Returns all test suites of core-package.
"""

    suites = []

    suites.append(TestBoard.suite()) # Appends suites with TestBoard-suite.
    suites.append(TestButton.suite()) # Appends suites with TestButton-suite.
    suites.append(TestGame.suite()) # Appends suites with TestGame-suite.
    suites.append(TestPlayer.suite()) # Appends suites with TestPlayer-suite.
    suites.append(TestRules.suite()) # Appends suites with TestRules-suite.

    return suites
