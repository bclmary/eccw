#!/usr/bin/env python3
# -*-coding:utf-8 -*


from collections import OrderedDict
import xmltodict
from xml.parsers.expat import ExpatError

from eccw.shared.print_tools import graph_print


class EccwFile():
    """Read/Write an eccw session file.

    **Usage**

    >>> f = EccwFile("path/to/file.eccw")
    >>> f.show()
    >>> f.save("path/to/newfile.eccw")
    """
    mime = "eccw"

    def __init__(self, data=None, filename=None):
        self.values = data
        if filename is not None:
            self.load(filename)

    def _check(self, elt, key):
        if elt[key] == [None]:
            # No elts must be stored as an empty list entry.
            elt[key] = []

    def load(self, filename):
        # Keywords that must be present in the result even if empty.
        fl = ('refpoints', 'points', 'curves')
        xmlfile = open(filename, 'r')
        try:
            tmp = xmltodict.parse(xmlfile.read(), force_list=fl)
        except ExpatError:
            self.values = None
            return
        xmlfile.close()
        try:
            self.values = tmp["session"]
            # Replace wrong formated elements by proper values.
            self._check(self.values["plot"], "refpoints")
            self._check(self.values["plot"], "curves")
            for i in range(len(self.values["plot"]["curves"])):
                self._check(self.values["plot"]["curves"][i], "points")
        except KeyError:
            self.values = None
            return

    def save(self, filename):
        xmlfile = open(filename, 'w')
        xmlfile.write(self.xml())
        xmlfile.close()

    def show(self):
        graph_print(self.values)

    def xml(self, pretty=True):
        values = OrderedDict(self.values)
        # Replace empty list elements by [None] for xmltodict.
        tmp1 = values["plot"].get("refpoints")
        if tmp1 is not None:
            if tmp1 == []:
                tmp1 = [None]
        tmp2 = values["plot"].get("curves")
        if tmp2 is not None:
            for elt in values["plot"]["curves"]:
                if elt["points"] == []:
                    elt["points"] = [None]
        return xmltodict.unparse({"session": values}, pretty=pretty)


if __name__ == "__main__":

    f = EccwFile()
    f.load("../test/test.eccw")
    f.show()
