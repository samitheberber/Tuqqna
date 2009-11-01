#!/usr/bin/env python

"""\
Game rules module.
"""

class Rules(object):

    def check(cls, row, column, buttons):
        return RulesHorizontal.check(row, column, buttons) \
            or RulesVertical.check(row, column, buttons) \
            or RulesCross.check(row, column, buttons)

    check = classmethod(check)


class RulesAxis:

    def _checkLesserCount(cls, number, buttons):
        if len(buttons) == 0:
            return 0
        buttons.sort()
        buttons.reverse()
        matches = 0
        while True:
            try:
                current = buttons.pop(0)
                if matches > 3:
                    break
                elif current == number - matches - 1:
                    matches += 1
                else:
                    break
            except IndexError:
                break
        return matches

    def _checkGreaterCount(cls, number, buttons):
        if len(buttons) == 0:
            return 0
        buttons.sort()
        matches = 0
        while True:
            try:
                current = buttons.pop(0)
                if matches > 3:
                    break
                elif current == number + matches + 1:
                    matches += 1
                else:
                    break
            except IndexError:
                break
        return matches

    _checkLesserCount = classmethod(_checkLesserCount)
    _checkGreaterCount = classmethod(_checkGreaterCount)


class RulesHorizontal(RulesAxis):

    def check(cls, row, column, buttons):
        buttons = [btn.x() for btn in buttons if btn.y() == row]
        if len(buttons) < 4:
            return False
        return cls._checkLesserCount(column, [btn for btn in buttons if btn <
            column]) + cls._checkGreaterCount(column, [btn for btn in buttons if btn >
            column]) + 1 >= 4

    check = classmethod(check)


class RulesVertical(RulesAxis):

    def check(cls, row, column, buttons):
        buttons = [btn.y() for btn in buttons if btn.x() == column]
        if len(buttons) < 4:
            return False
        return cls._checkGreaterCount(row, [btn for btn in buttons if btn > row]) + 1 >= 4

    check = classmethod(check)


class RulesCross:

    def check(cls, row, column, buttons):
        buttons = [(btn.x(), btn.y()) for btn in buttons if cls._isInCross(row,
            column, btn.x(), btn.y())]
        if len(buttons) < 4:
            return False
        return cls._checkAscending(row, column, buttons) \
            or cls._checkDescending(row, column, buttons)

    def _isInCross(cls, row, column, x, y):
        try:
            if x == column and y == row:
                return True
            elif row == column and x == y and row-y == column-x:
                return True
            elif float(column-x)/float(row-y) == -1 or float(column-x)/float(row-y) == 1:
                return True
            else:
                return False
        except ZeroDivisionError:
            return False

    def _checkAscending(cls, row, column, buttons):
        return cls._checkLesserAscCount(row, column, [btn for btn in buttons if
            btn[0] < column and btn[1] < row]) + cls._checkGreaterAscCount(row, 
            column, [btn for btn in buttons if btn[0] > column and btn[1] > row]
            ) + 1 >= 4

    def _checkLesserAscCount(cls, row, column, buttons):
        if len(buttons) == 0:
            return 0
        buttons.sort()
        buttons.reverse()
        matches = 0
        while True:
            try:
                (cx, cy) = buttons.pop(0)
                if matches > 3:
                    break
                elif cx == column - matches - 1 and cy == row - matches - 1:
                    matches += 1
                else:
                    break
            except IndexError:
                break
        return matches

    def _checkGreaterAscCount(cls, row, column, buttons):
        if len(buttons) == 0:
            return 0
        buttons.sort()
        matches = 0
        while True:
            try:
                (cx, cy) = buttons.pop(0)
                if matches > 3:
                    break
                elif cx == column + matches + 1 and cy == row + matches + 1:
                    matches += 1
                else:
                    break
            except IndexError:
                break
        return matches

    def _checkDescending(cls, row, column, buttons):
        return cls._checkLesserDescCount(row, column, [btn for btn in buttons if
            btn[0] < column and btn[1] > row]) + cls._checkGreaterDescCount(row, 
            column, [btn for btn in buttons if btn[0] > column and btn[1] < row]
            ) + 1 >= 4

    def _checkLesserDescCount(cls, row, column, buttons):
        if len(buttons) == 0:
            return 0
        buttons.sort()
        buttons.reverse()
        matches = 0
        while True:
            try:
                (cx, cy) = buttons.pop(0)
                if matches > 3:
                    break
                elif cx == column - matches - 1 and cy == row + matches + 1:
                    matches += 1
                else:
                    break
            except IndexError:
                break
        return matches

    def _checkGreaterDescCount(cls, row, column, buttons):
        if len(buttons) == 0:
            return 0
        buttons.sort()
        matches = 0
        while True:
            try:
                (cx, cy) = buttons.pop(0)
                if matches > 3:
                    break
                elif cx == column + matches + 1 and cy == row - matches - 1:
                    matches += 1
                else:
                    break
            except IndexError:
                break
        return matches

    check = classmethod(check)
    _isInCross = classmethod(_isInCross)
    _checkAscending = classmethod(_checkAscending)
    _checkLesserAscCount = classmethod(_checkLesserAscCount)
    _checkGreaterAscCount = classmethod(_checkGreaterAscCount)
    _checkDescending = classmethod(_checkDescending)
    _checkLesserDescCount = classmethod(_checkLesserDescCount)
    _checkGreaterDescCount = classmethod(_checkGreaterDescCount)
