#!/usr/bin/env python

"""\
Game engine module. Handles the core game classes.
"""


from tuqqna.core.board import Board
from tuqqna.core.player import Player
from tuqqna.core.errors.game import InvalidPlayerId
from tuqqna.core.errors.game import InvalidPlayerNumber
from tuqqna.core.errors.game import Player1Wins
from tuqqna.core.errors.game import Player2Wins
from tuqqna.core.errors.game import GameHasBeenEnded
from tuqqna.core.errors.game import AtFirstStartNewGame


class Game(object):

    def __init__(self):
        self._board = None
        self._players = []
        self._player1 = None
        self._player2 = None
        self._isEnded = False

    def setBoard(self, width, height):
        self._board = Board(width, height)

    def getWidth(self):
        if isinstance(self._board, Board):
            return self._board.getWidth()
        else:
            return None

    def getHeight(self):
        if isinstance(self._board, Board):
            return self._board.getHeight()
        else:
            return None

    def newGame(self):
        if isinstance(self._board, Board):
            self._board.reset()
            self._isEnded = False

    def addPlayer(self, player):
        if not isinstance(player, str):
            raise ValueError
        self._players.append(Player(player))

    def getPlayers(self):
        return self._players

    def changePlayer(self, player, playerId):
        try:
            if player == 1:
                self._player1 = self._players[playerId]
            elif player == 2:
                self._player2 = self._players[playerId]
            else:
                raise InvalidPlayerNumber
        except IndexError:
            raise InvalidPlayerId

    def getPlayer(self, player):
        if player == 1:
            return self._player1
        elif player == 2:
            return self._player2
        else:
            raise InvalidPlayerNumber

    def isStarted(self):
        return isinstance(self._board, Board) and isinstance(self._player1,
            Player) and isinstance(self._player2, Player)

    def drop(self, column):
        if self._isEnded:
            raise AtFirstStartNewGame

        try:
            self._board.drop(column)
        except Player1Wins:
            self._player1.wins()
            self._player2.defeats()
            self._isEnded = True
            raise Player1Wins
        except Player2Wins:
            self._player2.wins()
            self._player1.defeats()
            self._isEnded = True
            raise Player2Wins
        except GameHasBeenEnded:
            self._isEnded = True
            raise GameHasBeenEnded

    def getLast(self):
        return (self._board.lastSlotWhereDropped(), self._board.lastRowtWhereLanded())

    def __str__(self):
        if self.isStarted():
            return str(self._board)
        else:
            return ""
