#!/usr/bin/env python


"""\
"""

import curses
from curses import panel


def main(win):
    stdscr = win
    initUI(stdscr)

    while True:
        pass

    quitUI(stdscr)


def initTuqqna(stdscr):
    name = "~ Tuqqna ~"
    maxX = lambda (y,x): x
    center = maxX(stdscr.getmaxyx())/2 - len(name)/2
    stdscr.addstr(1, center, name)


def initPlayers(stdscr):
    pass


def initGame(stdscr):
    pass


def initUI(stdscr):
    curses.start_color()
    stdscr.keypad(1)
    curses.noecho()
    curses.cbreak()
    stdscr.border(0)

    initTuqqna(stdscr)

    stdscr.refresh()


def quitUI(stdscr):
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()


def start():
    curses.wrapper(main)
