#!/usr/bin/env python

"""\
This module contains cli ui window for gameplay.
"""

import curses

from tuqqna.cli.window import CliUIWindow


class CliUIGameplayWindow(CliUIWindow):
    """\
Cli ui window for gameplay.

Methods are enough describing.
"""

    def __init__(self, stdscr, engine, msg, help):
        self._stdscr = stdscr
        self._engine = engine
        self._helpWindow = help
        self._msgWindow = msg
        self._color = True
        windowWidth = self._getMaxX()-2
        windowHeight = self._getMaxY()-6
        self._win = stdscr.subwin(windowHeight, windowWidth, 2, 1)

    def play(self):
        self._setBoardSize()
        assert(self._engine.boardWidth() and self._engine.boardHeight() and
                self._engine.isStarted())
        self._gameLoop()
        self._win.erase()
        self._win.refresh()

    def _updateMsg(self):
        self._msgWindow.setMessage(self._engine.latestMessage())

    def _setBoardSize(self):
        width = None
        while not width:
            self._msgWindow.setMessage("Add board width (7): ")
            widthstr = self._msgWindow.getStr()
            if not widthstr:
                widthstr = 7
            try:
                widthint = int(widthstr)
                if widthint < 4:
                    raise ValueError("Use better width.")
                width = widthint
            except:
                pass

        height = None
        while not height:
            self._msgWindow.setMessage("Add board height (6): ")
            heightstr = self._msgWindow.getStr()
            if not heightstr:
                heightstr = 6
            try:
                heightint = int(heightstr)
                if heightint < 4:
                    raise ValueError("Use better height.")
                height = heightint
            except:
                pass

        self._engine.setBoard(width, height)

    def _gameLoop(self):
        self._drawBoard()
        self._updateMsg()
        self._helpWindow.setHelpText(
            '<arrows>: move coin ; <space>: drop ; q: return main window')
        while self._engine.isStarted():
            try:
                key = self._stdscr.getkey()
            except:
                continue
            self._msgWindow.clear()
            if key == 'q':
                return
            elif key == "KEY_LEFT":
                self._moveLeft()
            elif key == "KEY_RIGHT":
                self._moveRight()
            elif key == " ":
                try:
                    self._drop()
                except:
                    self._updateMsg()
                    return
            else:
                pass

    def _moveLeft(self):
        self._engine.moveCoinLeft()
        self._drawHeader()
        self._win.refresh()
        self._updateMsg()

    def _moveRight(self):
        self._engine.moveCoinRight()
        self._drawHeader()
        self._win.refresh()
        self._updateMsg()

    def _drop(self):
        try:
            self._engine.dropCoin()
            self._updateMsg()
            (x,y) = self._engine.coinLanded()
            curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
            self._win.addch(2*y+3, 2*x+2, 'O', curses.color_pair(1) if self._color else
                curses.color_pair(2))
            self._color = False if self._color else True
            self._drawHeader()
            self._win.refresh()
        except NoMoreSlotsInColumn:
            self._msgWindow.setMessage("The column is full.")

    def _drawBoard(self):
        width = self._engine.boardWidth()
        height = self._engine.boardHeight()
        self._drawHeader()
        self._win.hline(2, 1, '-', 2*width+1)
        row = '|'
        for i in range(width):
            row += ' |'
        for i in [x*2 for x in range(height)]:
            self._win.addstr(i+3, 1, row)
            self._win.hline(i+4, 1, '-', 2*width+1)
        self._win.refresh()

    def _drawHeader(self):
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        player1 = self._engine.getPlayer1()
        player2 = self._engine.getPlayer2()
        self._win.addstr(0, 1, player1, curses.color_pair(1))
        self._win.addstr(0, len(player1)+2, "VS")
        self._win.addstr(0, len(player1)+5, player2, curses.color_pair(2))
        coinPosition = self._engine.coinPosition()
        width = self._engine.boardWidth()
        header = ' '
        for i in range(width):
            if i == coinPosition:
                header += 'O '
            else:
                header += '  '
        self._win.addstr(1,1, header, curses.color_pair(1) if self._color else
                curses.color_pair(2))
