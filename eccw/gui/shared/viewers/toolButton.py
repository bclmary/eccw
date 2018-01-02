# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../uis/toolButton.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(30, 30)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.toolButton = QtGui.QToolButton(Form)
        self.toolButton.setMinimumSize(QtCore.QSize(30, 30))
        self.toolButton.setMaximumSize(QtCore.QSize(30, 30))
        self.toolButton.setToolTip(_fromUtf8(""))
        self.toolButton.setText(_fromUtf8(""))
        self.toolButton.setIconSize(QtCore.QSize(23, 23))
        self.toolButton.setAutoRaise(False)
        self.toolButton.setArrowType(QtCore.Qt.NoArrow)
        self.toolButton.setObjectName(_fromUtf8("toolButton"))
        self.verticalLayout.addWidget(self.toolButton)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

