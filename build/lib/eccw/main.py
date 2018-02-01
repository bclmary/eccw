#!/usr/bin/env python3
# -*-coding:utf-8 -*


"""
ECCW
allows to compute the exact solution of critical Coulomb wedge, draw it, sketch it, with love. 
Are available compressive or extensive geological context, with or without fluid pore pressure.

Created on Nov 6 10:58:41 2017
@author: bcl mary
"""

import sys
from PyQt5 import QtWidgets


from eccw.tui.main import options_parser
from eccw.gui.main_app.controllers.main import MainController
from eccw.shared.file_management import EccwFile


def launch() :
    out = options_parser()
    app = QtWidgets.QApplication(sys.argv)
    params = dict()
    if out:
        eccwf = EccwFile(filename=out)
        params = eccwf.values
    myapp = MainController(**params)
    sys.exit(app.exec_())


if __name__ == "__main__":
    launch()
