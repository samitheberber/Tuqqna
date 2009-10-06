#!/usr/bin/env python

"""\
Game engine module.
"""


from tuqqna.core.board import Board
from tuqqna.core.errors.game import InvalidPlayerId
from tuqqna.core.errors.game import InvalidPlayerNumber
from tuqqna.core.errors.game import Player1Wins
from tuqqna.core.errors.game import Player2Wins
from tuqqna.core.errors.game import AtFirstStartNewGame


class Game(object):

    def __init__(self):
        self._board = None
        self._players = []
        self._isEnded = False

    def setBoard(self, board):
        self._board = board

    def newGame(self):
        if isinstance(self._board, Board):
            self._board.reset()
            self._isEnded = False

    def addPlayer(self, player):
        self._players.append(player)

    def getPlayers(self):
        return self._players

    def changePlayer(self, player, playerId):
        try:
            if player == 1:
                self._board.setPlayer1(self._players[playerId])
            elif player == 2:
                self._board.setPlayer2(self._players[playerId])
            else:
                raise InvalidPlayerNumber
        except IndexError:
            raise InvalidPlayerId

    def getPlayer(self, player):
        if player == 1:
            return self._board.getPlayer1()
        elif player == 2:
            return self._board.getPlayer2()
        else:
            raise InvalidPlayerNumber

    def isStarted(self):
        return isinstance(self._board, Board) and self._board.isReady()

    def drop(self, column):
        if self._isEnded:
            raise AtFirstStartNewGame

        try:
            self._board.drop(column)
        except Player1Wins:
            self._board.getPlayer1().wins()
            self._board.getPlayer2().defeats()
            self._isEnded = True
            raise Player1Wins
        except Player2Wins:
            self._board.getPlayer2().wins()
            self._board.getPlayer1().defeats()
            self._isEnded = True
            raise Player2Wins

    def __str__(self):
        if self.isStarted():
            return str(self._board)
        else:
            return ""
