#!/usr/bin/env python3
# -*-coding:utf-8 -*

from math import pi


def d2r(value):
    return value * pi / 180.


def r2d(value):
    return value / pi * 180.


def imin(iterable):
    return min(range(len(iterable)), key=iterable.__getitem__)


def imax(iterable):
    return max(range(len(iterable)), key=iterable.__getitem__)
