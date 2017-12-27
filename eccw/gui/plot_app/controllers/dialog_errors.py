#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PyQt4 import QtGui

from eccw.gui.plot_app.viewers.dialog_errors import Ui_Dialog_Errors


class Errors(QtGui.QWidget, Ui_Dialog_Errors):
    """Widget for software informations display."""
    def __init__(self, message="", parent=None):
        super(Errors, self).__init__(parent)
        self.setupUi(self)
        self.add_message(message)
        self.show()

    def add_message(self, text):
        self.textEdit.append(text)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    myapp = Errors("Des erreurs")
    sys.exit(app.exec_())
