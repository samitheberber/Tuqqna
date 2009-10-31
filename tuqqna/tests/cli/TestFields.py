#!/usr/bin/env python

"""\
Test Cli fields tests all field relevant cli ui matters.
"""


import unittest

from tuqqna.cli.game import CliUIGame


class TestPlayersField(unittest.TestCase):

    def setUp(self):
        pass

    def test_test(self):
        self.fail("not made")


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPlayersField))
    return suite
