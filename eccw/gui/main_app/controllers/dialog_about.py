#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PyQt5 import QtWidgets

from eccw.gui.main_app.viewers.dialog_about import Ui_Dialog_About
#import eccw.version as version
#import eccw.authors as authors
from eccw import __version__
from eccw import __authors__

class About(QtWidgets.QWidget, Ui_Dialog_About):
    """Widget for software informations display."""
    def __init__(self, parent=None):
        super(About, self).__init__(parent)
        self.setupUi(self)
        self.label_version.setText(__version__)
        self.label_authors.setText("\n".join(__authors__))
        self.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    myapp = About()
    sys.exit(app.exec_())
