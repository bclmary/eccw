#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt4 import QtGui

from eccw.gui.shared.viewers.verticalLayout import Ui_Form as UiV
from eccw.gui.shared.viewers.horizontalLayout import Ui_Form as UiH


class VerticalLayout(QtGui.QWidget, UiV):
    """Vertical layout widget.
    This is a Qt derived object.
    """
    def __init__(self, *args):
        super(VerticalLayout, self).__init__()
        self.setupUi(self)
        self.show()


class HorizontalLayout(QtGui.QWidget, UiH):
    """Horizontal layout widget.
    This is a Qt derived object.
    """
    def __init__(self, *args):
        super(HorizontalLayout, self).__init__()
        self.setupUi(self)
        self.show()


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    myapp = VerticalLayout()
    sys.exit(app.exec_())
