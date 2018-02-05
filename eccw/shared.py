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


def _is_leaf(elt):
    """Return True if elt if not an iterable."""
    if isinstance(elt, dict):
        return False
    elif isinstance(elt, list):
        return False
    elif isinstance(elt, tuple):
        return False
    else:
        return True


def graph_print(elt, indent=0, level=0):
    """Print 'elt' and all its contained elements (if any) in a pretty way.

How dictionaries are printed
----------------------------

::

    { key1 : value1
      key2 : value2
      ...
      keyN : valueN
    }

How list and tuple are printed
----------------------------

::

    [0] value1
    [1] value2
    ...
    [N] valueN

.. note:: Brackets are used for tuples display.

.. note:: If lists or tuples are leafs of the graph (ie they do not contains
          iterable elements) they are printed simply using repr().
"""
    if level == 0:
        print(" "*indent, end="")
    if isinstance(elt, dict):
        print("{ ", end="")
        keysizemax = max([len(key) for key in elt.keys()])
        m = indent + 2
        for i, (key, value) in enumerate(elt.items()):
            n = keysizemax - len(key)
            if i != 0:
                print("\n" + " "*(indent + 2), end="")
            print(str(key) + " "*n + " : ", end="")
            graph_print(value, indent + keysizemax + 5, level+1)
        print("\n" + " "*(m-2) + "}", end="")
    elif isinstance(elt, list) or isinstance(elt, tuple):
        A = "[" if isinstance(elt, list) else "("
        Z = "]" if isinstance(elt, list) else ")"
        if all([_is_leaf(e) for e in elt]):
            print(repr(elt), end="")
        else:
            for i, e in enumerate(elt):
                if i != 0:
                    print("\n" + " "*indent, end="")
                print("%s%i%s " % (A, i, Z), end="")
                graph_print(e, indent + 4 if i < 10 else 5, level+1)
                print(" "*indent, end="")
    else:
        print(repr(elt), end="")
    if level == 0:
        print()


if __name__ == "__main__":

    from collections import OrderedDict as OD

    test = OD([
        ("value", 1.),
        ("text", "foo"),
        ("bool", True),
        ("dict", OD([
            ("value", 1.),
            ("text", "foo"),
            ("bool", True),
            ("tuple", (1, 2, 3)),
            ("list", ["A", "B", "C"])
            ])),
        ("list", [1., "foo", True, (1, 2, 3), ["A", "B", "C"]]),
        ("tuple", (1., "foo", True, (1, 2, 3), ["A", "B", "C"]))
        ])
    graph_print(test)  # , indent=4)
