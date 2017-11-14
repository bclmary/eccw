# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialogue_about.ui'
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

class Ui_Dialog_About(object):
    def setupUi(self, Dialog_About):
        Dialog_About.setObjectName(_fromUtf8("Dialog_About"))
        Dialog_About.resize(400, 159)
        self.horizontalLayout = QtGui.QHBoxLayout(Dialog_About)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_logo = QtGui.QLabel(Dialog_About)
        self.label_logo.setMaximumSize(QtCore.QSize(128, 128))
        self.label_logo.setText(_fromUtf8(""))
        self.label_logo.setPixmap(QtGui.QPixmap(_fromUtf8("../images/icon_eccw.png")))
        self.label_logo.setScaledContents(True)
        self.label_logo.setObjectName(_fromUtf8("label_logo"))
        self.horizontalLayout.addWidget(self.label_logo)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_title = QtGui.QLabel(Dialog_About)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_title.setFont(font)
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_title.setObjectName(_fromUtf8("label_title"))
        self.verticalLayout.addWidget(self.label_title)
        self.label_version = QtGui.QLabel(Dialog_About)
        self.label_version.setAlignment(QtCore.Qt.AlignCenter)
        self.label_version.setObjectName(_fromUtf8("label_version"))
        self.verticalLayout.addWidget(self.label_version)
        self.label_authors = QtGui.QLabel(Dialog_About)
        self.label_authors.setAlignment(QtCore.Qt.AlignCenter)
        self.label_authors.setObjectName(_fromUtf8("label_authors"))
        self.verticalLayout.addWidget(self.label_authors)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog_About)
        QtCore.QMetaObject.connectSlotsByName(Dialog_About)

    def retranslateUi(self, Dialog_About):
        Dialog_About.setWindowTitle(_translate("Dialog_About", "About", None))
        self.label_title.setText(_translate("Dialog_About", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">ECCW</span><br/>Exact Critical Coulomb Wedge</p></body></html>", None))
        self.label_version.setText(_translate("Dialog_About", "Version 1.00", None))
        self.label_authors.setText(_translate("Dialog_About", "B.C.L Mary, Chong Wu", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog_About = QtGui.QDialog()
    ui = Ui_Dialog_About()
    ui.setupUi(Dialog_About)
    Dialog_About.show()
    sys.exit(app.exec_())

