#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import string


class FollowPath:
    """
    Extracts path data from an ASCII map

    :Example:

    >>> from follow_path import FollowPath
    >>> path = FollowPath('''
    ...   @---A---+
    ...           |
    ...   x-B-+   C
    ...       |   |
    ...       +---+
    ... ''')
    >>> path.run()
    >>> print(path.letters)
    'ACB'
    >>> print(path.characters)
    '@---A---+|C|+---+|+-B-x'
    """

    # Indicators
    START = '@'
    HORIZONTAL = '-'
    VERTICAL = '|'
    CORNER = '+'
    END = 'x'
    INDICATORS = [START, HORIZONTAL, VERTICAL, CORNER, END]

    # Directions
    LEFT = 'LEFT'
    UP = 'UP'
    RIGHT = 'RIGHT'
    DOWN = 'DOWN'
    DIRECTIONS = [LEFT, UP, RIGHT, DOWN]

    def __init__(self, string):
        self.string = string
        self.matrix = [list(x) for x in self.string.split('\n')]
        self.direction = None
        self.position = None

    @property
    def letters(self):
        return ''.join(self._letters) if hasattr(self, '_letters') else None

    @property
    def characters(self):
        return ''.join(self._characters) if hasattr(self, '_letters') else None

    def set_starting_position(self):
        """
        Sets a starting position and resets paramaters.
        """
        self._letters = []
        self._characters = []
        self.usedPositions = []
        self.direction = None

        for row in range(len(self.matrix)):
            if self.START in self.matrix[row]:
                self.position = row, self.matrix[row].index(self.START)

        if self.position:
            self._characters.append(self.START)

    def get_relative_position(self, direction):
        """Returns new position in the direction relative to the current one"""
        if not self.position:
            return None
        if direction == self.LEFT:
            return (self.position[0], self.position[1] - 1)
        if direction == self.UP:
            return (self.position[0] - 1, self.position[1])
        if direction == self.RIGHT:
            return (self.position[0], self.position[1] + 1)
        if direction == self.DOWN:
            return (self.position[0] + 1, self.position[1])

    def get_opposite_direction(self, direction):
        """Returns the opposite direction from the given one"""
        opposites = [
            (self.LEFT, self.RIGHT),
            (self.UP, self.DOWN),
            (self.RIGHT, self.LEFT),
            (self.DOWN, self.UP),
        ]
        return dict(opposites).get(direction, None)

    def find_next_position(self):
        """
        Returns a tuple containing the next position and direction.
        The previous direction get's prioritized and the opposite one ignored.
        """
        if not self.position:
            return None, None

        choices = [(self.get_relative_position(self.direction), self.direction)] if self.direction else []
        opposite = self.get_opposite_direction(self.direction)
        directions = [x for x in self.DIRECTIONS if x != self.direction and x != opposite]
        choices += [(self.get_relative_position(x), x) for x in directions]

        for (position, direction) in choices:
            try:
                assert position[0] > -1 and position[1] > -1
                char = self.matrix[position[0]][position[1]]
            except (AssertionError, IndexError):
                continue
            if char in string.ascii_uppercase or char in self.INDICATORS:
                return position, direction
        return None, None

    def next_step(self):
        """
        Finds next step in a matrix, updates position and direction.
        """
        if not self.position:
            return None, self.direction

        self.position, self.direction = self.find_next_position()

        if self.position:
            # Store character and letter.
            # Keep track of used positions to avoid letter duplicates.
            formatedPosition = '{}/{}'.format(*self.position)
            char = self.matrix[self.position[0]][self.position[1]]
            self._characters.append(char)
            if char in string.ascii_uppercase and formatedPosition not in self.usedPositions:
                self._letters.append(char)
                self.usedPositions.append(formatedPosition)

    def run(self):
        self.set_starting_position()
        while self.position:
            self.next_step()


def follow_path(string):
    """
    Extracts path data from an ASCII map

    :param string: ASCII map as a string
    :returns: a tuple containing extracted (letters, characters)

    :Example:

    >>> from follow_path import follow_path
    >>> follow_path('''
    ...     @---+
    ...         B
    ...   K-----|--A
    ...   |     |  |
    ...   |  +--E  |
    ...   |  |     |
    ...   +--E--Ex C
    ...      |     |
    ...      +--F--+
    ... ''')
    ('BEEFCAKE', '@---+B||E--+|E|+--F--+|C|||A--|-----K|||+--E--Ex')

    """
    path = FollowPath(string)
    path.run()
    return path.letters, path.characters


if __name__ == '__main__':  # pragma: no cover
    files = [open(file, 'r') for file in sys.argv[1:]]
    if not files:
        files = [sys.stdin]
    for file in files:
        data = follow_path(file.read())
        print('Letters: "{0}"\nPath as characters: "{1}"'.format(*data))
