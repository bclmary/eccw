#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt4 import QtGui

from eccw.gui.shared.viewers.colorButton import Ui_Form
from eccw.shared.checkers import float_check
from eccw.gui.shared.wrappers import Wrapper


class ColorButton(QtGui.QWidget, Ui_Form, Wrapper):

    def __init__(self, *args):
        super(ColorButton, self).__init__()
        self.setupUi(self)
        self.svg = ("<?xml version='1.0' encoding='UTF-8' standalone='no'?>"
                    "<svg version='1.1'><rect  style='fill:%s;stroke:#000000;stroke-linejoin:round;"
                    "stroke-width:0.2' width='10'"
                    " height='5' x='-1' y='50' rx='0.75' ry='0.75' /></svg>")
        self.svg_path = "../../../images/color.svg"
        self.style_sheet = ("color: white;"
                            "background-color: %s;"
                            # "background:" + self.svg_path + ";"
                            # "qlineargradient("
                            # "x1: 0, y1: 0, x2: 0, y2: 1,"
                            # # "stop: 0 #eaebfe, stop: 1 #76878a);"
                            # "stop: 0 %s, stop: 1 black);"
                            "border-style: solid;"
                            "border-style:raised;"
                            "border-width: 1px;"
                            "border-color: gray;"
                            "border-radius: 4px;"
                            "min-width: 50px;"
                            "max-width: 50px;"
                            "min-height: 26px;"
                            "max-height: 26px;")
        self.setToolTip("Color")
        self.change_color(QtGui.QColor(0, 0, 0))
        self.toolButton.clicked.connect(self.showDialog)
        # Fill values with args
        if args:
            self.set_params(*args)
        self.show()

    def showDialog(self):
        col = QtGui.QColorDialog.getColor()
        if col.isValid():
            self.change_color(col)
            self.value = col.getRgbF()

    def change_color(self, col):
        """col is an QColor object"""
        f = open(self.svg_path, 'w')
        f.write(self.svg % col.name())
        f.close()
        self.toolButton.setIcon(QtGui.QIcon(self.svg_path))
        # txt = self.style_sheet % col.name()
        # self.toolButton.setStyleSheet("QWidget {" + txt + " }")

    def set_params(self, arg):
        errmessage = "ColorButton() gets invalid color format '"+str(arg)+"'."
        try:
            color = [float_check(c) for c in arg]
            if all([c <= 1. for c in color]) and len(color) == 4:
                col = QtGui.QColor()
                col.setRgbF(*color)
                Wrapper.set_params(self, arg, fn=self.change_color(col))
            else:
                raise TypeError(errmessage)
        except TypeError:
            raise TypeError(errmessage)


if __name__ == "__main__":
    import sys
    try:
        app = QtGui.QApplication(sys.argv)
        myapp = ColorButton((0, 1, 0, 1))
        sys.exit(app.exec_())
    finally:
        print("params =", myapp.get_params())
        print("select =", myapp.get_select())
