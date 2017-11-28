#!/usr/bin/env python3
# -*-coding:utf-8 -*

from math import pi


def d2r(value):
    return value * pi / 180.


def r2d(value):
    return value / pi * 180.


def normalize_angle(angle, min_, max_):
    turn = max_ - min_
    if angle in (float('inf'), float('-inf'), float('nan'), None):
        return float('nan')
    while angle > max_:
        angle -= turn
    while angle < min_:
        angle += turn
    return angle


def imin(iterable):
    return min(range(len(iterable)), key=iterable.__getitem__)


def imax(iterable):
    return max(range(len(iterable)), key=iterable.__getitem__)

