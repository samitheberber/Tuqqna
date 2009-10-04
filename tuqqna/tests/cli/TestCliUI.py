#!/usr/bin/env python

"""\
Test Board tests all board relevant matters.
"""


import unittest

from tuqqna.cli.cliui import CliUI


class TestCliUIConstruction(unittest.TestCase):

    def test_create_simple_ui(self):
        try:
            ui = CliUI()
        except:
            self.fail()


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCliUIConstruction))
    return suite
