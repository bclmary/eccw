# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../uis/dialog_about.ui'
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
        Dialog_About.resize(410, 206)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog_About.sizePolicy().hasHeightForWidth())
        Dialog_About.setSizePolicy(sizePolicy)
        Dialog_About.setMinimumSize(QtCore.QSize(410, 0))
        Dialog_About.setMaximumSize(QtCore.QSize(410, 600))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(Dialog_About)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(30, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label_logo = QtGui.QLabel(Dialog_About)
        self.label_logo.setMaximumSize(QtCore.QSize(128, 128))
        self.label_logo.setText(_fromUtf8(""))
        self.label_logo.setPixmap(QtGui.QPixmap(_fromUtf8(":/icons/icon_eccw.png")))
        self.label_logo.setScaledContents(True)
        self.label_logo.setObjectName(_fromUtf8("label_logo"))
        self.horizontalLayout.addWidget(self.label_logo)
        spacerItem1 = QtGui.QSpacerItem(30, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.label_title = QtGui.QLabel(Dialog_About)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_title.setFont(font)
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_title.setObjectName(_fromUtf8("label_title"))
        self.verticalLayout_2.addWidget(self.label_title)
        spacerItem2 = QtGui.QSpacerItem(191, 13, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.line = QtGui.QFrame(Dialog_About)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.horizontalLayout_2.addWidget(self.line)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(Dialog_About)
        self.label.setMinimumSize(QtCore.QSize(160, 0))
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.label_version = QtGui.QLabel(Dialog_About)
        self.label_version.setAlignment(QtCore.Qt.AlignCenter)
        self.label_version.setObjectName(_fromUtf8("label_version"))
        self.verticalLayout.addWidget(self.label_version)
        spacerItem3 = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem3)
        self.label2 = QtGui.QLabel(Dialog_About)
        self.label2.setObjectName(_fromUtf8("label2"))
        self.verticalLayout.addWidget(self.label2)
        self.label_authors = QtGui.QLabel(Dialog_About)
        self.label_authors.setAlignment(QtCore.Qt.AlignCenter)
        self.label_authors.setObjectName(_fromUtf8("label_authors"))
        self.verticalLayout.addWidget(self.label_authors)
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem4)
        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog_About)
        QtCore.QMetaObject.connectSlotsByName(Dialog_About)

    def retranslateUi(self, Dialog_About):
        Dialog_About.setWindowTitle(_translate("Dialog_About", "About", None))
        self.label_title.setText(_translate("Dialog_About", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600;\">ECCW</span><br/>Exact Critical Coulomb Wedge</p></body></html>", None))
        self.label.setText(_translate("Dialog_About", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Version</span></p></body></html>", None))
        self.label_version.setText(_translate("Dialog_About", "version", None))
        self.label2.setText(_translate("Dialog_About", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Authors</span></p></body></html>", None))
        self.label_authors.setText(_translate("Dialog_About", "authors", None))

import eccw.images.ressources_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog_About = QtGui.QDialog()
    ui = Ui_Dialog_About()
    ui.setupUi(Dialog_About)
    Dialog_About.show()
    sys.exit(app.exec_())

