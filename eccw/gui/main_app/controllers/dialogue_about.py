#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PyQt4 import QtGui

from eccw.gui.main_app.viewers.dialogue_about import Ui_Dialog_About
import eccw.version as version
import eccw.authors as authors


class About(QtGui.QWidget, Ui_Dialog_About):
    """Widget for software informations display."""
    def __init__(self, parent=None):
        super(About, self).__init__(parent)
        self.setupUi(self)
        self.label_version.setText(version.__version__)
        self.label_authors.setText('\n'.join(authors.__authors_list__))
        self.show()


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    myapp = About()
    sys.exit(app.exec_())
