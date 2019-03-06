#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from follow_path import FollowPath, follow_path

MAP_1 = """
@---A---+
        |
x-B-+   C
    |   |
    +---+
"""

MAP_2 = """
@
|
A
|
x
"""

MAP_3 = """
  @---+
      B
K-----|--A
|     |  |
|  +--E  |
|  |     |
+--E--Ex C
   |     |
   +--F--+
"""


class TestFollowPath(unittest.TestCase):
    def test__init__(self):
        path = FollowPath(MAP_2)
        self.assertEqual(path.matrix, [[], ['@'], ['|'], ['A'], ['|'], ['x'], []])

    def test_letters(self):
        path = FollowPath(MAP_2)
        self.assertIsNone(path.letters)
        path.run()
        self.assertEqual(path.letters, 'A')

    def test_characters(self):
        path = FollowPath(MAP_2)
        self.assertIsNone(path.characters)
        path.run()
        self.assertEqual(path.characters, '@|A|x')

    def test_set_starting_position(self):
        path = FollowPath(MAP_1)
        path.set_starting_position()
        self.assertEqual(path._letters, [])
        self.assertEqual(path._characters, [FollowPath.START])
        self.assertEqual(path.direction, None)
        self.assertEqual(path.position, (1, 0))

    def test_get_relative_position(self):
        path = FollowPath(MAP_1)
        self.assertIsNone(path.get_relative_position(FollowPath.LEFT))
        path.set_starting_position()
        self.assertEqual(path.get_relative_position(FollowPath.LEFT), (1, -1))
        self.assertEqual(path.get_relative_position(FollowPath.UP), (0, 0))
        self.assertEqual(path.get_relative_position(FollowPath.RIGHT), (1, 1))
        self.assertEqual(path.get_relative_position(FollowPath.DOWN), (2, 0))

    def test_get_opposite_direction(self):
        path = FollowPath('')
        self.assertEqual(path.get_opposite_direction(FollowPath.LEFT), FollowPath.RIGHT)
        self.assertEqual(path.get_opposite_direction(FollowPath.UP), FollowPath.DOWN)
        self.assertEqual(path.get_opposite_direction(FollowPath.RIGHT), FollowPath.LEFT)
        self.assertEqual(path.get_opposite_direction(FollowPath.DOWN), FollowPath.UP)

    def test_find_next_position(self):
        path = FollowPath(MAP_1)
        self.assertEqual(path.find_next_position(), (None, None))
        path.set_starting_position()
        self.assertEqual(path.find_next_position(), ((1, 1), FollowPath.RIGHT))
        path = FollowPath(MAP_2)
        path.set_starting_position()
        self.assertEqual(path.find_next_position(), ((2, 0), FollowPath.DOWN))
        # Test respect for direction priority
        path = FollowPath('\n-|\n-@\n-|')
        path.set_starting_position()
        self.assertEqual(path.find_next_position(), ((2, 0), FollowPath.LEFT))
        # Test respect for ignored direction
        path.direction = FollowPath.RIGHT
        self.assertEqual(path.find_next_position(), ((1, 1), FollowPath.UP))

    def test_next_step(self):
        path = FollowPath(MAP_2)
        path.set_starting_position()
        path.next_step()
        self.assertEqual(path.position, (2, 0))
        self.assertEqual(path._characters, ['@', '|'])
        path.next_step()
        self.assertEqual(path._characters, ['@', '|', 'A'])
        self.assertEqual(path._letters, ['A'])

    def test_run(self):
        path = FollowPath(MAP_1)
        path.run()
        self.assertEqual(path.letters, 'ACB')
        self.assertEqual(path.characters, '@---A---+|C|+---+|+-B-x')

    def test_follow_path(self):
        data = follow_path(MAP_3)
        self.assertIsInstance(data, tuple)
        self.assertEqual(data[0], 'BEEFCAKE')
        self.assertEqual(data[1], '@---+B||E--+|E|+--F--+|C|||A--|-----K|||+--E--Ex')


if __name__ == '__main__':
    unittest.main()
