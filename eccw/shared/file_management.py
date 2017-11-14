#!/usr/bin/env python3
# -*-coding:utf-8 -*


from collections import OrderedDict
import xmltodict
from xml.parsers.expat import ExpatError

from eccw.shared.print_tools import graph_print


class EccwFile():
    """
    Read/Write an eccw session file.
    
    **Usage**
    
    >>> f = EccwFile("path/to/file.eccw")
    >>> f.show()
    >>> f.save("path/to/newfile.eccw")
    """

    mime = "eccw"
    
    def __init__(self, filename=None):
        self.values = None
        if filename is not None:
            self.load(filename)

    def load(self, filename):
        fl = ('refpoints', 'points', 'curves')
        xmlfile = open(filename, 'r')
        try:
            tmp = xmltodict.parse(xmlfile.read(), force_list=fl)
        except ExpatError:
            self.values = None
            return
        xmlfile.close()
        try:
            self.values = tmp["main"]
        except KeyError:
            self.values = None
            return
        # Replace wrong elements by proper values.
        tmp = self.values["plot"].get("refpoints")
        if tmp is not None:
            if tmp == [None]:
                tmp = []  # No refpoints must be stored as an empty list entry.
            else :
                for elt in tmp:
                    if elt["label"] == None:
                        elt["label"] = ""  # Empty label must be stored as an empty string.
        tmp = self.values["plot"].get("curves")
        if tmp is not None:
            if tmp == [None]:
                tmp = []  # No curves must be stored as an empty list entry.
            else:
                for elt in tmp:
                    if elt["points"] == [None]:
                        elt["points"] = []
                    else:
                        for pt in elt["points"]:
                            if pt["label"] == None:
                                pt["label"] = ""
                        if elt["label"] == None:
                            elt["label"] = ""

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
        return xmltodict.unparse({"main": values}, pretty=pretty)

if __name__ == "__main__":

    f = EccwFile()
    f.load("../test/test.eccw")
    f.show()

