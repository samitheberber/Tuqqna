#!/usr/bin/env python

import curses

from tuqqna.cli.window import CliUIWindow
from tuqqna.cli.help import CliUIHelpWindow
from tuqqna.cli.game import CliUIGame
from tuqqna.cli.message import CliUIGameMsgWindow
from tuqqna.cli.player import CliUIGamePlayerWindow
from tuqqna.cli.gameplay import CliUIGameplayWindow


class CliUIGameWindow(CliUIWindow):

    def __init__(self, stdscr):
        self._game = CliUIGame()
        self._stdscr = stdscr
        self._titleWindow = self._createTitleWindow()
        self._msgWindow = CliUIGameMsgWindow(stdscr)
        self._playerWindow = CliUIGamePlayerWindow(stdscr, self._game)
        self._helpWindow = CliUIHelpWindow(stdscr)

    def _createTitleWindow(self):
        maxX = self._getMaxX()
        win = self._stdscr.subwin(1,maxX,0,0)
        name = "[ ~ Tuqqna ~ ]"
        if len(name) >= maxX:
            raise ValueError
        center = maxX/2 - len(name)/2
        win.addstr(0, center, name)
        win.refresh()
        return win

    def start(self):
        self._helpWindow.setHelpText('a: add player ; 1: set player 1 ; 2: set player 2')
        while True:
            try:
                try:
                    key = self._stdscr.getkey()
                except:
                    continue
                self._msgWindow.clear()
                if key == 'q':
                    return
                elif key == "1":
                    if self._playerWindow.setPlayer1():
                        self._msgWindow.setMessage(self._game.latestMessage())
                        self._checkStartCondition()
                elif key == "2":
                    if self._playerWindow.setPlayer2():
                        self._msgWindow.setMessage(self._game.latestMessage())
                        self._checkStartCondition()
                elif key == "a":
                    self._addNewPlayer()
                elif key == "s" and self._playerWindow.checkReady():
                    self.startGame()
                elif key == "KEY_UP":
                    self._playerWindow.moveUp()
                elif key == "KEY_DOWN":
                    self._playerWindow.moveDown()
                else:
                    pass
            except KeyboardInterrupt:
                return

    def _addNewPlayer(self):
        name = None
        while not name:
            self._msgWindow.setMessage("Add new player: ")
            name = self._msgWindow.getStr()
        assert(name)
        self._game.addPlayer(name)
        self._msgWindow.setMessage(self._game.latestMessage())
        self._playerWindow.refresh()

    def _checkStartCondition(self):
        if self._playerWindow.checkReady():
            self._helpWindow.setHelpText(
                'a: add player ; 1: set player 1 ; 2: set player 2 ; s : start')

    def startGame(self):
        self._playerWindow.hide()
        self._helpWindow.clear()
        gameplayWindow = CliUIGameplayWindow(self._stdscr, self._game,
                self._msgWindow, self._helpWindow)
        gameplayWindow.play()
        self._playerWindow.show()
        self._helpWindow.setHelpText(
            'a: add player ; 1: set player 1 ; 2: set player 2 ; s : start')
