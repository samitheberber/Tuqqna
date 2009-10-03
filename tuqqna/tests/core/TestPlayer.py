#!/usr/bin/env python

"""\
Test Player tests all player relevant matters.
"""


import unittest

from tuqqna.core.player import Player


class TestPlayerCreation(unittest.TestCase):

    def setUp(self):
        self.player = Player("Player 1")

    def test_player_name(self):
        self.assertEquals(self.player.getName(), "Player 1")

    def test_player_string_transform_returns_name(self):
        self.assertEquals(str(self.player), "Player 1")

    def test_player_victories_are_0_at_beginning(self):
        self.assertEquals(self.player.getVictories(), 0)

    def test_player_wins_once(self):
        self.player.wins()
        self.assertEquals(self.player.getVictories(), 1)

    def test_player_defeats_are_0_at_beginning(self):
        self.assertEquals(self.player.getDefeats(), 0)

    def test_player_defeat_once(self):
        self.player.defeats()
        self.assertEquals(self.player.getDefeats(), 1)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPlayerCreation))
    return suite

