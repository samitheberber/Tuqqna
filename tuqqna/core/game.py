#!/usr/bin/env python

"""\
Game engine module. Handles the core game classes.
"""


class Game(object):

    def __init__(self):
        self._board = None
        self._players = []

    def setBoard(self, board):
        self._board = board

    def getBoard(self):
        return self._board

    def addPlayer(self, player):
        self._players.append(player)

    def getPlayers(self):
        return self._players
