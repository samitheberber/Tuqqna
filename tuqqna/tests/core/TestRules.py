#!/usr/bin/env python

"""\
Test Rules tests all rules relevant matters.
"""


import unittest

from tuqqna.core.button import Button
from tuqqna.core.player import Player
from tuqqna.core.rules import Rules
from tuqqna.core.rules import RulesHorizontal
from tuqqna.core.rules import RulesVertical
from tuqqna.core.rules import RulesCross


class TestHorizontalRules(unittest.TestCase):

    def setUp(self):
        self.player1 = Player("Player 1")
        self.player2 = Player("Player 2")

    def test_no_win_when_only_one_button_on_field(self):
        buttons = [(self.player1, Button(0,0))]
        self.assertFalse(RulesHorizontal.check(self.player1, 0, 0, buttons))

    def test_win_on_four_row_last_at_beginning(self):
        buttons = [(self.player1, Button(0,0)), (self.player1, Button(1,0)), (self.player1, Button(2,0)), (self.player1, Button(3,0))]
        self.assertTrue(RulesHorizontal.check(self.player1, 0, 0, buttons))

    def test_win_on_four_row_last_at_end(self):
        buttons = [(self.player1, Button(0,0)), (self.player1, Button(1,0)), (self.player1, Button(2,0)), (self.player1, Button(3,0))]
        self.assertTrue(RulesHorizontal.check(self.player1, 0, 3, buttons))

    def test_win_on_four_row_last_at_center(self):
        buttons = [(self.player1, Button(0,0)), (self.player1, Button(1,0)), (self.player1, Button(2,0)), (self.player1, Button(3,0))]
        self.assertTrue(RulesHorizontal.check(self.player1, 0, 2, buttons))

    def test_no_win_on_four_row_last_at_center(self):
        buttons = [(self.player1, Button(0,0)), (self.player2, Button(1,0)), (self.player1, Button(2,0)), (self.player1, Button(3,0))]
        self.assertFalse(RulesHorizontal.check(self.player1, 0, 2, buttons))

    def test_win_on_four_row_not_on_borders_last_at_center(self):
        buttons = [(self.player1, Button(4,1)), (self.player1, Button(1,1)), (self.player1, Button(2,1)), (self.player1, Button(3,1))]
        self.assertTrue(RulesHorizontal.check(self.player1, 1, 3, buttons))


class TestVerticalRules(unittest.TestCase):

    def setUp(self):
        self.player1 = Player("Player 1")
        self.player2 = Player("Player 2")

    def test_no_win_when_only_one_button_on_field(self):
        buttons = [(self.player1, Button(0,0))]
        self.assertFalse(RulesVertical.check(self.player1, 0, 0, buttons))

    def test_win_on_four_column(self):
        buttons = [(self.player1, Button(0,0)), (self.player1, Button(0,1)), (self.player1, Button(0,2)), (self.player1, Button(0,3))]
        self.assertTrue(RulesVertical.check(self.player1, 0, 0, buttons))

    def test_no_win_on_four_column(self):
        buttons = [(self.player1, Button(0,0)), (self.player2, Button(0,1)), (self.player1, Button(0,2)), (self.player1, Button(0,3))]
        self.assertFalse(RulesVertical.check(self.player1, 0, 0, buttons))

    def test_win_on_four_column_not_on_borders_last(self):
        buttons = [(self.player1, Button(1,1)), (self.player1, Button(1,2)), (self.player1, Button(1,3)), (self.player1, Button(1,4))]
        self.assertTrue(RulesVertical.check(self.player1, 1, 1, buttons))


class TestCrossRules(unittest.TestCase):

    def setUp(self):
        self.player1 = Player("Player 1")
        self.player2 = Player("Player 2")

    def test_no_win_when_only_one_button_on_field(self):
        buttons = [(self.player1, Button(0,0))]
        self.assertFalse(RulesCross.check(self.player1, 0, 0, buttons))

    def test_win_on_four_row_ascending_last_at_beginning(self):
        buttons = [(self.player1, Button(0,0)), (self.player1, Button(1,1)), (self.player1, Button(2,2)), (self.player1, Button(3,3))]
        self.assertTrue(RulesCross.check(self.player1, 0, 0, buttons))

    def test_win_on_four_row_ascending_last_at_end(self):
        buttons = [(self.player1, Button(0,0)), (self.player1, Button(1,1)), (self.player1, Button(2,2)), (self.player1, Button(3,3))]
        self.assertTrue(RulesCross.check(self.player1, 3, 3, buttons))

    def test_win_on_four_row_ascending_last_at_center(self):
        buttons = [(self.player1, Button(0,0)), (self.player1, Button(1,1)), (self.player1, Button(2,2)), (self.player1, Button(3,3))]
        self.assertTrue(RulesCross.check(self.player1, 2, 2, buttons))

    def test_no_win_on_four_row_ascending_last_at_center(self):
        buttons = [(self.player1, Button(0,0)), (self.player2, Button(1,1)), (self.player1, Button(2,2)), (self.player1, Button(3,3))]
        self.assertFalse(RulesCross.check(self.player1, 2, 2, buttons))

    def test_win_on_four_row_descending_last_at_beginning(self):
        buttons = [(self.player1, Button(0,3)), (self.player1, Button(1,2)), (self.player1, Button(2,1)), (self.player1, Button(3,0))]
        self.assertTrue(RulesCross.check(self.player1, 3, 0, buttons))

    def test_win_on_four_row_descending_last_at_end(self):
        buttons = [(self.player1, Button(0,3)), (self.player1, Button(1,2)), (self.player1, Button(2,1)), (self.player1, Button(3,0))]
        self.assertTrue(RulesCross.check(self.player1, 0, 3, buttons))

    def test_win_on_four_row_descending_last_at_center(self):
        buttons = [(self.player1, Button(0,3)), (self.player1, Button(1,2)), (self.player1, Button(2,1)), (self.player1, Button(3,0))]
        self.assertTrue(RulesCross.check(self.player1, 1, 2, buttons))

    def test_no_win_on_four_row_descending_last_at_center(self):
        buttons = [(self.player1, Button(0,3)), (self.player2, Button(1,2)), (self.player1, Button(2,1)), (self.player1, Button(3,0))]
        self.assertFalse(RulesCross.check(self.player1, 1, 2, buttons))


class TestRules(unittest.TestCase):

    def setUp(self):
        self.player1 = Player("Player 1")
        self.player2 = Player("Player 2")

    def test_no_win_on_any_rule(self):
        buttons = [(self.player1, Button(0,0))]
        self.assertFalse(Rules.check(self.player1, 0, 0, buttons))

    def test_win_on_horizontal_rule(self):
        buttons = [(self.player1, Button(0,0)), (self.player1, Button(1,0)), (self.player1, Button(2,0)), (self.player1, Button(3,0))]
        self.assertTrue(Rules.check(self.player1, 0, 2, buttons))

    def test_win_on_vertical_rule(self):
        buttons = [(self.player1, Button(0,0)), (self.player1, Button(0,1)), (self.player1, Button(0,2)), (self.player1, Button(0,3))]
        self.assertTrue(Rules.check(self.player1, 0, 0, buttons))

    def test_win_on_asscending_cross_rule(self):
        buttons = [(self.player1, Button(0,0)), (self.player1, Button(1,1)), (self.player1, Button(2,2)), (self.player1, Button(3,3))]
        self.assertTrue(Rules.check(self.player1, 2, 2, buttons))

    def test_win_on_descending_cross_rule(self):
        buttons = [(self.player1, Button(0,3)), (self.player1, Button(1,2)), (self.player1, Button(2,1)), (self.player1, Button(3,0))]
        self.assertTrue(Rules.check(self.player1, 1, 2, buttons))


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestHorizontalRules))
    suite.addTest(unittest.makeSuite(TestVerticalRules))
    suite.addTest(unittest.makeSuite(TestCrossRules))
    suite.addTest(unittest.makeSuite(TestRules))
    return suite
