#!/usr/bin/env python


"""\
"""

import curses
import sys

from tuqqna.cli.gamewin import CliUIGameWindow


def initUI(stdscr):
    """\
This function makes all required configurations.
"""

    curses.start_color()
    stdscr.keypad(1)
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    stdscr.box()
    stdscr.leaveok(0)
    stdscr.refresh()

def quitUI(stdscr):
    """\
This function return terminal in usable mode after the game.
"""

    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()

def main(win):
    """\
This function takes the curses screen, calls for modification funtion, starts
the game window and calls for quitting function.
"""

    stdscr = win
    initUI(stdscr)
    gameWindow = CliUIGameWindow(stdscr)
    gameWindow.start()
    quitUI(stdscr)

def start():
    """\
Makes all preparation for starting.
"""

    # Hack, which makes title visible in terminal title
    sys.stderr.write('\x1b]0;%s\x07' % 'Tuqqna')
    sys.stderr.flush()

    curses.wrapper(main)
