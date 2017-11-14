#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PyQt4 import QtCore,QtGui

from dialogue_about_viewer import Ui_Dialog_About


class About(QtGui.QWidget, Ui_Dialog_About):

    """Just an alias of QLineEdit object, used by 
CurvePointGraphicSettings."""

    def __init__(self, parent=None):
        super(About, self).__init__(parent)
        self.setupUi(self)
        self.show()


if __name__=="__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    myapp = About()
    sys.exit(app.exec_())

