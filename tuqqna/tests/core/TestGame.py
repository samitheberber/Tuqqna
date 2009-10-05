#!/usr/bin/env python

"""\
Test Game engine tests all game engine relevant matters.
"""


import unittest

from tuqqna.core.board import Board
from tuqqna.core.game import Game
from tuqqna.core.player import Player


class TestGameCreation(unittest.TestCase):

    def setUp(self):
        self.game = Game()

    def test_create_the_game_with_board(self):
        board = Board(7,6)
        self.game.setBoard(board)
        self.assertEquals(self.game.getBoard(), board)

    def test_add_new_player_in_game(self):
        player = Player("Test player")
        self.game.addPlayer(player)
        self.assertTrue(player in self.game.getPlayers())

    def test_add_few_more_players_in_game(self):
        try:
            for i in xrange(4):
                player = Player("Player no. %i" % i)
                self.game.addPlayer(player)
                if player in self.game.getPlayers():
                    continue
                else:
                    raise ValueError
        except ValueError:
            self.fail("Not every player added in game.")


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestGameCreation))
    return suite
