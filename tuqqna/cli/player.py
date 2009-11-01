#!/usr/bin/env python

import curses

from tuqqna.cli.window import CliUIWindow


class CliUIGamePlayerWindow(CliUIWindow):

    def __init__(self, stdscr, engine):
        self._stdscr = stdscr
        self._engine = engine
        windowWidth = self._getMaxX()-2
        windowHeight = self._getMaxY()-6
        self._win = stdscr.subwin(windowHeight, windowWidth, 2, 1)
        self.show()
        self._current = 0

    def hide(self):
        self._win.erase()
        self._win.refresh()

    def show(self):
        pass
        self._win.box()
        self._addSelectedPlayers()
        self._addPlayers()
        self._win.refresh()

    def _addSelectedPlayers(self):
        (winX, winY) = self._win.getmaxyx()
        player1 = self._engine.getPlayer1()
        player2 = self._engine.getPlayer2()
        self._win.addstr(1, 1, "Player 1: " + player1)
        self._win.addstr(2, 1, "Player 2: " + player2)
        self._win.hline(3, 1, '-', winY-2)

    def _addPlayers(self):
        (winX, winY) = self._win.getmaxyx()
        players = self._engine.getPlayers()
        if len(players) == 0:
            self._win.addstr(4, 1, "(No players in game)")
        else:
            for i in xrange(len(players)):
                if i == self._current:
                    self._win.addstr(4+i, 1, players[i], curses.A_UNDERLINE)
                else:
                    self._win.addstr(4+i, 1, players[i])

    def refresh(self):
        self._win.clear()
        self._win.box()
        self._addSelectedPlayers()
        self._addPlayers()
        self._win.refresh()

    def moveUp(self):
        if (len(self._engine.getPlayers()) == 0 or len(self._engine.getPlayers()) == 1):
            return
        curPos = self._current
        curPos-=1
        if curPos >= 0:
            self._current = curPos
        self.refresh()

    def moveDown(self):
        if (len(self._engine.getPlayers()) == 0 or len(self._engine.getPlayers()) == 1):
            return
        curPos = self._current
        curPos+=1
        if curPos < len(self._engine.getPlayers()):
            self._current = curPos
        self.refresh()

    def setPlayer1(self):
        players = self._engine.getPlayers()
        if len(players) == 0:
            return False
        self._engine.player1(players[self._current])
        self.refresh()
        return True

    def setPlayer2(self):
        players = self._engine.getPlayers()
        if len(players) == 0:
            return False
        self._engine.player2(players[self._current])
        self.refresh()
        return True

    def checkReady(self):
        return self._engine.hasPlayers()
