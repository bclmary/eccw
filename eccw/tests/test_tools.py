#!/usr/bin/env python3
# -*-coding:utf-8 -*

import unittest
from math import pi

from eccw.shared.tools import normalize_angle


class TestNormalizeAngle(unittest.TestCase):

    def test_normalize_angle(self):
        self.assertEqual(normalize_angle(30, -180, 180), 30)
        self.assertEqual(normalize_angle(-30, -180, 180), -30)
        self.assertEqual(normalize_angle(90, -180, 180), 90)
        self.assertEqual(normalize_angle(-170, -180, 180), -170)
        self.assertEqual(normalize_angle(181, -180, 180), -179)
        self.assertEqual(normalize_angle(330, -180, 180), -30)
        self.assertEqual(normalize_angle(361, -180, 180), 1)
        self.assertEqual(normalize_angle(359, -180, 180), -1)
        self.assertEqual(normalize_angle(-361, -180, 180), -1)
        self.assertAlmostEqual(normalize_angle(-3*pi - pi/2., -pi, pi), pi/2.)


if __name__ == '__main__':
    unittest.main()
