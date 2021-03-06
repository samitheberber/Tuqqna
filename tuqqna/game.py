#!/usr/bin/env python

"""
This is main game file of Tuqqna.
"""


import sys
import getopt

from tuqqna.cli import cliui


def main():
    """\
This is main game function, which handles arguments.
"""

    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help", "cli"])
    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)
    # process options
    for o, a in opts:
        if o in ("-h", "--help"):
            print help()
            sys.exit(0)

    try:
        cliui.start()
    except KeyboardInterrupt:
        return

def help():
    """\
This function returns help documentation.
"""

    return """\
usage: ./run.py [option]
Options and arguments:
-h      : print this help message and exit (also --help)
"""
