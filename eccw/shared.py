#!/usr/bin/env python3
# -*-coding:utf-8 -*

"""
Various shared tools.
"""

from math import pi


def d2r(value):
    """Convert float value from degree to radian."""
    return value * pi / 180.


def r2d(value):
    """Convert float value from radian to degree."""
    return value / pi * 180.


def normalize_angle(angle, min_, max_):
    """Retreave excess cycles from an angle."""
    turn = max_ - min_
    if angle in (float('inf'), float('-inf'), float('nan'), None):
        return float('nan')
    while angle > max_:
        angle -= turn
    while angle < min_:
        angle += turn
    return angle


def imin(iterable):
    """return index of min value from iterable."""
    return min(range(len(iterable)), key=iterable.__getitem__)


def imax(iterable):
    """return index of max value from iterable."""
    return max(range(len(iterable)), key=iterable.__getitem__)

