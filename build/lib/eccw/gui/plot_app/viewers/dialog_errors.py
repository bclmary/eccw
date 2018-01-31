# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../uis/dialog_errors.ui'
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

class Ui_Dialog_Errors(object):
    def setupUi(self, Dialog_Errors):
        Dialog_Errors.setObjectName(_fromUtf8("Dialog_Errors"))
        Dialog_Errors.resize(400, 185)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog_Errors)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.textEdit = QtGui.QTextEdit(Dialog_Errors)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.verticalLayout.addWidget(self.textEdit)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton = QtGui.QPushButton(Dialog_Errors)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout.addWidget(self.pushButton)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog_Errors)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog_Errors.close)
        QtCore.QMetaObject.connectSlotsByName(Dialog_Errors)

    def retranslateUi(self, Dialog_Errors):
        Dialog_Errors.setWindowTitle(_translate("Dialog_Errors", "Errors", None))
        self.pushButton.setText(_translate("Dialog_Errors", "Ok", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog_Errors = QtGui.QDialog()
    ui = Ui_Dialog_Errors()
    ui.setupUi(Dialog_Errors)
    Dialog_Errors.show()
    sys.exit(app.exec_())

