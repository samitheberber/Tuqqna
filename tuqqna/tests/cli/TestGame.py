#!/usr/bin/env python

"""\
Test Game tests all game relevant cli ui matters.
"""


import unittest

from tuqqna.cli.game import CliUIGame
from tuqqna.core.errors.game import Player1Wins
from tuqqna.core.errors.game import Player2Wins
from tuqqna.core.errors.game import GameHasBeenEnded
#from tuqqna.cli.game import CliUIGameWindow


class CliUITestCase(unittest.TestCase):

    def setUp(self):
        self.uigame = CliUIGame()


class TestCliUIConstruction(CliUITestCase):

    def test_players(self):
        self.assertEquals(self.uigame.getPlayers(), [])
        self.assertEquals(self.uigame.getPlayer1(), "(none)")
        self.assertEquals(self.uigame.getPlayer2(), "(none)")

    def test_game_start_message(self):
        self.assertEquals(self.uigame.latestMessage(), "Game started.")

    def test_set_board(self):
        self.uigame.setBoard(7,6)
        self.assertTrue(self.uigame.boardWidth() == 7 and
                        self.uigame.boardHeight() == 6)
        self.assertEquals(self.uigame.latestMessage(), "Set board to 7x6.")

    def test_game_is_not_started_at_construction(self):
        self.assertFalse(self.uigame.isStarted())

    def test_coin_position_at_construction(self):
        self.assertEquals(self.uigame.coinPosition(), None)


class TestPlayerAssign(CliUITestCase):

    def test_add_player(self):
        playerName = "Player 1"
        self.uigame.addPlayer(playerName)
        self.assertTrue(playerName in self.uigame.getPlayers())
        self.assertEquals(self.uigame.latestMessage(), "Added Player 1.")

    def test_set_players_to_game(self):
        self.uigame.addPlayer("Player 1")
        self.uigame.addPlayer("Player 2")
        self.uigame.player1("Player 1")
        self.assertEquals(self.uigame.latestMessage(), "Selected Player 1 "\
        "to player 1.")
        self.assertEquals(self.uigame.getPlayer1(), "Player 1")
        self.uigame.player2("Player 2")
        self.assertEquals(self.uigame.latestMessage(), "Selected Player 2 "\
        "to player 2.")
        self.assertEquals(self.uigame.getPlayer2(), "Player 2")

    def test_set_invalid_player_to_player1(self):
        self.uigame.player1("Player 1")
        self.assertEquals(self.uigame.latestMessage(), "Not found Player 1.")
        self.uigame.player2("Player 1")
        self.assertEquals(self.uigame.latestMessage(), "Not found Player 1.")


class TestGameplay(CliUITestCase):

    def setUp(self):
        self.uigame = CliUIGame()
        self.uigame.addPlayer("Player 1")
        self.uigame.addPlayer("Player 2")
        self.uigame.player1("Player 1")
        self.uigame.player2("Player 2")
        self.uigame.setBoard(7,6)

    def test_game_is_ready(self):
        self.assertTrue(self.uigame.isStarted())
        self.assertEquals(self.uigame.latestMessage(), "Game is started.")

    def test_coin_position(self):
        self.assertEquals(self.uigame.coinPosition(), 3)

    def test_move_coin_to_left(self):
        self.uigame.moveCoinLeft()
        self.assertEquals(self.uigame.latestMessage(), "")
        self.assertEquals(self.uigame.coinPosition(), 2)

    def test_move_coin_to_far_left(self):
        for i in xrange(3):
            self.uigame.moveCoinLeft()
        self.assertEquals(self.uigame.latestMessage(), "")
        self.assertEquals(self.uigame.coinPosition(), 0)

    def test_move_coin_to_over_far_left(self):
        for i in xrange(4):
            self.uigame.moveCoinLeft()
        self.assertEquals(self.uigame.latestMessage(), "Can't move more to left.")
        self.assertEquals(self.uigame.coinPosition(), 0)

    def test_move_coin_to_right(self):
        self.uigame.moveCoinRight()
        self.assertEquals(self.uigame.latestMessage(), "")
        self.assertEquals(self.uigame.coinPosition(), 4)

    def test_move_coin_to_far_right(self):
        for i in xrange(3):
            self.uigame.moveCoinRight()
        self.assertEquals(self.uigame.latestMessage(), "")
        self.assertEquals(self.uigame.coinPosition(), 6)

    def test_move_coin_to_over_far_right(self):
        for i in xrange(4):
            self.uigame.moveCoinRight()
        self.assertEquals(self.uigame.coinPosition(), 6)
        self.assertEquals(self.uigame.latestMessage(), "Can't move more to "\
            "right.")

    def test_drop_coin_to_center(self):
        self.uigame.dropCoin()
        self.assertEquals(self.uigame.coinLanded(), (3,5))
        self.assertEquals(self.uigame.latestMessage(), "")

    def test_drop_two_coins_to_center(self):
        self.uigame.dropCoin()
        self.uigame.dropCoin()
        self.assertEquals(self.uigame.coinLanded(), (3,4))
        self.assertEquals(self.uigame.latestMessage(), "")

    def test_drop_coin_to_far_left(self):
        for i in xrange(3):
            self.uigame.moveCoinLeft()
        self.uigame.dropCoin()
        self.assertEquals(self.uigame.latestMessage(), "")
        self.assertEquals(self.uigame.coinLanded(), (0,5))

    def test_drop_coin_to_far_right(self):
        for i in xrange(3):
            self.uigame.moveCoinRight()
        self.uigame.dropCoin()
        self.assertEquals(self.uigame.coinLanded(), (6,5))

    def test_player1_wins(self):
        for i in xrange(3):
            self.uigame.moveCoinLeft()
        for i in xrange(3):
            self.uigame.dropCoin()
            self.uigame.moveCoinRight()
            self.uigame.dropCoin()
            self.uigame.moveCoinLeft()
        self.assertRaises(Player1Wins, self.uigame.dropCoin)
        self.assertEquals(self.uigame.latestMessage(), "Winner is Player 1.")

    def test_player2_wins(self):
        for i in xrange(3):
            self.uigame.moveCoinLeft()
        for i in xrange(2):
            self.uigame.dropCoin()
            self.uigame.moveCoinRight()
            self.uigame.dropCoin()
            self.uigame.moveCoinLeft()
        for i in xrange(2):
            self.uigame.dropCoin()
            self.uigame.moveCoinRight()
        self.uigame.dropCoin()
        self.uigame.moveCoinLeft()
        self.assertRaises(Player2Wins, self.uigame.dropCoin)
        self.assertEquals(self.uigame.latestMessage(), "Winner is Player 2.")

    def test_game_ends_draw(self):
        landes = [(0,5), (1,5), (0,4), (1,4), (0,3), (1,3), (2,5), (3,5), (2,4),
                (3,4), (2,3), (3,3), (4,5), (5,5), (4,4), (5,4), (4,3), (5,3),
                (6,5), (0,2), (6,4), (0,1), (6,3), (0,0), (1,2), (2,2), (1,1),
                (2,1), (1,0), (2,0), (3,2), (4,2), (3,1), (4,1), (3,0), (4,0),
                (5,2), (6,2), (5,1), (6,1), (5,0), (6,0)]
        for i in xrange(3):
            self.uigame.moveCoinLeft()
        for i in xrange(3):
            for j in xrange(3):
                self.uigame.moveCoinLeft()
                self.uigame.dropCoin()
                self.assertEquals(self.uigame.coinLanded(), landes.pop(0))
                self.uigame.moveCoinRight()
                self.uigame.dropCoin()
                self.assertEquals(self.uigame.coinLanded(), landes.pop(0))
            self.uigame.moveCoinRight()
            self.uigame.moveCoinRight()
        for i in xrange(5):
            self.uigame.moveCoinLeft()
        for i in xrange(3):
            for j in xrange(6):
                self.uigame.moveCoinRight()
            self.uigame.dropCoin()
            self.assertEquals(self.uigame.coinLanded(), landes.pop(0))
            for j in xrange(6):
                self.uigame.moveCoinLeft()
            self.uigame.dropCoin()
            self.assertEquals(self.uigame.coinLanded(), landes.pop(0))
        for i in xrange(2):
            self.uigame.moveCoinRight()
            self.uigame.dropCoin()
            for j in xrange(2):
                self.assertEquals(self.uigame.coinLanded(), landes.pop(0))
                self.uigame.moveCoinRight()
                self.uigame.dropCoin()
                self.assertEquals(self.uigame.coinLanded(), landes.pop(0))
                self.uigame.moveCoinLeft()
                self.uigame.dropCoin()
            self.assertEquals(self.uigame.coinLanded(), landes.pop(0))
            self.uigame.moveCoinRight()
            self.uigame.dropCoin()
            self.assertEquals(self.uigame.coinLanded(), landes.pop(0))
        self.uigame.moveCoinRight()
        self.uigame.dropCoin()
        for j in xrange(2):
            self.assertEquals(self.uigame.coinLanded(), landes.pop(0))
            self.uigame.moveCoinRight()
            self.uigame.dropCoin()
            self.assertEquals(self.uigame.coinLanded(), landes.pop(0))
            self.uigame.moveCoinLeft()
            self.uigame.dropCoin()
        self.assertEquals(self.uigame.coinLanded(), landes.pop(0))
        self.uigame.moveCoinRight()
        self.assertRaises(GameHasBeenEnded, self.uigame.dropCoin)
        self.assertEquals(self.uigame.coinLanded(), landes.pop(0))
        self.assertEquals(landes, [])
        self.assertEquals(self.uigame.latestMessage(), "Game ends draw.")


#class GameWindowData(unittest.TestCase):
#
#    def setUp(self):
#        self.gamewin = CliUIGameWindow()
#
#    def test_test(self):
#        pass


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCliUIConstruction))
    suite.addTest(unittest.makeSuite(TestPlayerAssign))
    suite.addTest(unittest.makeSuite(TestGameplay))
#    suite.addTest(unittest.makeSuite(GameWindowData))
    return suite
