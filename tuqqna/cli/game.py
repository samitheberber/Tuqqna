#!/usr/bin/env python

"""\
"""


import curses

from tuqqna.core.game import Game
from tuqqna.core.errors.game import Player1Wins
from tuqqna.core.errors.game import Player2Wins
from tuqqna.core.errors.game import GameHasBeenEnded
from tuqqna.core.errors.game import AtFirstStartNewGame


class CliUIGame(object):

    def __init__(self):
        self._game = Game()
        self._coinPosition = None
        self._message = "Game started."

    def addPlayer(self, name):
        self._game.addPlayer(name)
        self._message = "Added %s." % name

    def getPlayers(self):
        return map(lambda player: player.getName(), self._game.getPlayers())

    def getPlayer1(self):
        player = self._game.getPlayer(1)
        if player:
            return player.getName()
        else:
            return "(none)"

    def getPlayer2(self):
        player = self._game.getPlayer(2)
        if player:
            return player.getName()
        else:
            return "(none)"

    def hasPlayers(self):
        return self._game.getPlayer(1) and self._game.getPlayer(2)

    def setBoard(self, width, height):
        self._game.setBoard(width, height)
        self._message = "Set board to %ix%i." % (width, height)

    def boardWidth(self):
        return self._game.getWidth()

    def boardHeight(self):
        return self._game.getHeight()

    def player1(self, name):
        if not name in self.getPlayers():
            self._message = "Not found %s." % name
        else:
            self._game.changePlayer(1, self.getPlayers().index(name))
            self._message = "Selected %s to player 1." % name

    def player2(self, name):
        if not name in self.getPlayers():
            self._message = "Not found %s." % name
        else:
            self._game.changePlayer(2, self.getPlayers().index(name))
            self._message = "Selected %s to player 2." % name

    def isStarted(self):
        if self._game.isStarted():
            self._message = "Game is started."
            return True
        else:
            return False

    def coinPosition(self):
        msg = self._message
        if self.isStarted() and self._coinPosition == None:
            self._coinPosition = int(self.boardWidth() / 2)
        self._message = msg
        return self._coinPosition

    def moveCoinLeft(self):
        if not self.isStarted():
            return
        position = self.coinPosition()-1
        if position >= 0:
            self._coinPosition = position
            self._message = ""
        else:
            self._message = "Can't move more to left."

    def moveCoinRight(self):
        if not self.isStarted():
            return
        position = self.coinPosition()+1
        if position < self.boardWidth():
            self._coinPosition = position
            self._message = ""
        else:
            self._message = "Can't move more to right."

    def dropCoin(self):
        msg = self._message
        if not self.isStarted():
            return
        self._message = msg
        try:
            self._game.drop(self.coinPosition())
            self._message = ""
        except Player1Wins:
            self._message = "Winner is %s." % self._game.getPlayer(1)
        except Player2Wins:
            self._message = "Winner is %s." % self._game.getPlayer(2)
        except GameHasBeenEnded:
            self._message = "Game ends draw."

    def coinLanded(self):
        return self._game.getLast()

    def latestMessage(self):
        return str(self._message)


class CliUIWindow(object):

    def _getMaxX(self):
        getMaxX = lambda (_,x): x
        return getMaxX(self._stdscr.getmaxyx())

    def _getMaxY(self):
        getMaxY = lambda (y,_): y
        return getMaxY(self._stdscr.getmaxyx())


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
                key = self._stdscr.getkey()
                self._msgWindow.clear()
                if key == 'q':
                    return
                elif key == "1":
                    self._playerWindow.setPlayer1()
                    self._msgWindow.setMessage(self._game.latestMessage())
                    self._checkStartCondition()
                elif key == "2":
                    self._playerWindow.setPlayer2()
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
                    self._msgWindow.setMessage("Unknown key: " + key)
            except KeyboardInterrupt:
                return

    def _addNewPlayer(self):
        self._msgWindow.setMessage("Add new player: ")
        self._game.addPlayer(self._msgWindow.getStr())
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
        self._msgWindow.setMessage(self._game.latestMessage())
        self._helpWindow.setHelpText(
            'a: add player ; 1: set player 1 ; 2: set player 2 ; s : start')


class CliUIGameMsgWindow(CliUIWindow):

    def __init__(self, stdscr):
        self._stdscr = stdscr
        windowWidth = self._getMaxX() - 2
        self._win = stdscr.subwin(1, windowWidth, 1, 1)

    def setMessage(self, msg):
        self._win.clear()
        self._win.addstr(0, 0, msg)
        self._win.refresh()

    def getStr(self):
        curses.echo()
        value = self._win.getstr()
        curses.noecho()
        return value

    def clear(self):
        self._win.clear()
        self._win.refresh()


class CliUIHelpWindow(CliUIWindow):

    def __init__(self, stdscr):
        self._stdscr = stdscr
        self._win = self._stdscr.subwin(3, self._getMaxX()-2, self._getMaxY()-4, 1)
        self._win.box()
        self._win.refresh()

    def setHelpText(self, text):
        if len(text) > self._getMaxX()-4:
            raise Error("Too small window.")
        self.clear()
        self._win.addstr(1, 1, text)
        self._win.refresh()

    def clear(self):
        self._win.clear()
        self._win.box()


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
            return
        self._engine.player1(players[self._current])
        self.refresh()

    def setPlayer2(self):
        players = self._engine.getPlayers()
        if len(players) == 0:
            return
        self._engine.player2(players[self._current])
        self.refresh()

    def checkReady(self):
        return self._engine.hasPlayers()


class CliUIGameplayWindow(CliUIWindow):

    def __init__(self, stdscr, engine, msg, help):
        self._stdscr = stdscr
        self._engine = engine
        self._helpWindow = help
        self._msgWindow = msg
        windowWidth = self._getMaxX()-2
        windowHeight = self._getMaxY()-6
        self._win = stdscr.subwin(windowHeight, windowWidth, 2, 1)

    def play(self):
        self._setBoardSize()

    def _setBoardSize(self):
        width = None
        while not width:
            self._msgWindow.setMessage("Add board width: ")
            widthstr = self._msgWindow.getStr()
            try:
                widthint = int(widthstr)
                #TODO: add integer size check.
                width = widthint
            except:
                pass

        height = None
        while not height:
            self._msgWindow.setMessage("Add board height: ")
            heightstr = self._msgWindow.getStr()
            try:
                heightint = int(heightstr)
                #TODO: add integer size check.
                height = heightint
            except:
                pass

        self._engine.setBoard(width, height)
