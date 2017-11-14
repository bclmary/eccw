#!/usr/bin/env python3
# -*-coding:utf-8 -*

import unittest
from collections import OrderedDict as OD

from eccw.shared.print_tools import graph_print

class PrintToolsTests(unittest.TestCase):
    """Tests for `eccw.shared.print_tools.py`."""

    def test_graph_print(self):
        in_ = OD([
            ("value" , 1.),
            ("text" , "foo"),
            ("bool" , True),
            ("dict"  , OD([("value", 1.), ("text" , "foo"), ("bool" , True), ("tuple", (1, 2, 3)), ("list" , ["A", "B", "C"])])),
            ("list", [1., "foo", True, (1, 2, 3), ["A", "B", "C"]]),
            ("tuple", (1., "foo", True, (1, 2, 3), ["A", "B", "C"]))
            ])
        out = """
{ value : 1.0
  text  : 'foo'
  bool  : True
  dict  : { value : 1.0
            text  : 'foo'
            bool  : True
            tuple : (1, 2, 3)
            list  : ['A', 'B', 'C']
          }
  list  : [0] 1.0
          [1] 'foo'
          [2] True
          [3] (1, 2, 3)
          [4] ['A', 'B', 'C']
  tuple : (0) 1.0
          (1) 'foo'
          (2) True
          (3) (1, 2, 3)
          (4) ['A', 'B', 'C']
}
"""
        self.assertEqual(graph_print(in_), out)

if __name__ == '__main__':
    unittest.main()
