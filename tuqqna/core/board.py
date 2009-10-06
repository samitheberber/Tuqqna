#!/usr/bin/env python

"""\
Game board module.
"""

from tuqqna.core.player import Player
from tuqqna.core.button import Button
from tuqqna.core.rules import Rules
from tuqqna.core.errors.game import GameNotStartedError
from tuqqna.core.errors.game import GameHasBeenEnded
from tuqqna.core.errors.game import Player1Wins
from tuqqna.core.errors.game import Player2Wins
from tuqqna.core.errors.board import NoMoreSlotsInColumn


class Board(object):

    def __init__(self, width, height):
        self._width = width
        self._height = height
        self.reset()

    def getWidth(self):
        return self._width

    def getHeight(self):
        return self._height

    def reset(self):
        self._player1Drops = []
        self._player2Drops = []
        self._lastSlot = None
        self._lastRow = None

    def drop(self, column):
        if column < 0 or column > self._width:
            raise ValueError
        self._lastSlot = column
        row = self._getFirstEmptyRow(column)
        self._lastRow = row
        button = Button(column, row)
        if self.playerInTurn() == 1:
            self._player1Drops.append(button)
            self._checkEndConditions(1, row, column)
        else:
            self._player2Drops.append(button)
            self._checkEndConditions(2, row, column)

    def _checkEndConditions(self, player, row, column):
        if len(self._player1Drops) + len(self._player2Drops) < 7:
            return
        elif len(self._player1Drops) + len(self._player2Drops) == self._width * self._height:
            raise GameHasBeenEnded
        elif player == 1 and Rules.check(row, column, self._player1Drops):
            raise Player1Wins
        elif player == 2 and Rules.check(row, column, self._player2Drops):
            raise Player2Wins

    def lastSlotWhereDropped(self):
        return self._lastSlot

    def lastRowtWhereLanded(self):
        return self._lastRow

    def playerInTurn(self):
        if len(self._player1Drops) == len(self._player2Drops):
            return 1
        else:
            return 2

    def _getFirstEmptyRow(self, column):
        if len(self._player1Drops) == 0 and len(self._player2Drops) == 0:
            return self._height-1
        else:
            buttonsInSelectedColumn = map(lambda btn: btn.y() ,filter(
                lambda btn: btn.x() == column,
                self._player1Drops + self._player2Drops))

            if len(buttonsInSelectedColumn) == 0:
                return self._height-1
            else:
                buttonsInSelectedColumn.sort()
                firstEmpty = buttonsInSelectedColumn[0]-1
                if firstEmpty < 0:
                    raise NoMoreSlotsInColumn
                else:
                    return firstEmpty

    def __str__(self):
        buttonsInTuple = self._createButtonsInTuple()
        stringFormat = ""
        for i in xrange(self._width):
            stringFormat += "--"
        stringFormat += "-\n"
        for i in xrange(self._height):
            stringFormat += self._slotRowToString(filter(
                lambda (x, y, z): y == i
                , buttonsInTuple))
        return stringFormat

    def _slotRowToString(self, rowItems):
        string = ""
        for i in xrange(self._width):
            matches = map(lambda (x, y, z): z, filter(lambda (x, y, z): x == i, rowItems))
            if len(matches) == 0:
                string += "| "
            else:
                string += "|%s" % matches[0]
        string += "|\n"
        for i in xrange(self._width):
            string += "--"
        return string + "-\n"

    def _createButtonsInTuple(self):
        ready = []
        for i in self._player1Drops:
            ready.append((i.x(), i.y(), "O"))
        for i in self._player2Drops:
            ready.append((i.x(), i.y(), "X"))
        return ready
