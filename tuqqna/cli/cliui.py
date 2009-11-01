#!/usr/bin/env python


"""\
"""

import curses
import sys

from tuqqna.cli.gamewin import CliUIGameWindow


def initUI(stdscr):
    curses.start_color()
    stdscr.keypad(1)
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    stdscr.box()
    stdscr.leaveok(0)
    stdscr.refresh()

def quitUI(stdscr):
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()

def main(win):
    stdscr = win
    initUI(stdscr)
    gameWindow = CliUIGameWindow(stdscr)
    gameWindow.start()
    quitUI(stdscr)

def start():
    sys.stderr.write('\x1b]0;%s\x07' % 'Tuqqna')
    sys.stderr.flush()

    curses.wrapper(main)
