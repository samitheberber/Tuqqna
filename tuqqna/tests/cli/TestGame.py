#!/usr/bin/env python

"""\
Test Game tests all game relevant cli ui matters.
"""


import unittest

from tuqqna.cli.game import CliUIGame


class TestCliUIConstruction(unittest.TestCase):

    def setUp(self):
        self.uigame = CliUIGame()

    def test_add_player(self):
        playerName = "Player 1"
        self.uigame.addPlayer(playerName)
        self.assertTrue(playerName in self.uigame.getPlayers())

    def test_set_board(self):
        self.uigame.setBoard(7,6)
        self.assertTrue(self.uigame.boardWidth() == 7 and
                        self.uigame.boardHeight() == 6)

    def test_set_players_to_game(self):
        self.uigame.addPlayer("Player 1")
        self.uigame.addPlayer("Player 2")
        try:
            self.uigame.player1("Player 1")
            self.uigame.player2("Player 2")
        except:
            self.fail("Failed to set players.")


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCliUIConstruction))
    return suite
