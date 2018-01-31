# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../uis/dialog_about.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog_About(object):
    def setupUi(self, Dialog_About):
        Dialog_About.setObjectName("Dialog_About")
        Dialog_About.resize(410, 206)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog_About.sizePolicy().hasHeightForWidth())
        Dialog_About.setSizePolicy(sizePolicy)
        Dialog_About.setMinimumSize(QtCore.QSize(410, 0))
        Dialog_About.setMaximumSize(QtCore.QSize(410, 600))
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(Dialog_About)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label_logo = QtWidgets.QLabel(Dialog_About)
        self.label_logo.setMaximumSize(QtCore.QSize(128, 128))
        self.label_logo.setText("")
        self.label_logo.setPixmap(QtGui.QPixmap(":/icons/icon_eccw.png"))
        self.label_logo.setScaledContents(True)
        self.label_logo.setObjectName("label_logo")
        self.horizontalLayout.addWidget(self.label_logo)
        spacerItem1 = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.label_title = QtWidgets.QLabel(Dialog_About)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_title.setFont(font)
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_title.setObjectName("label_title")
        self.verticalLayout_2.addWidget(self.label_title)
        spacerItem2 = QtWidgets.QSpacerItem(191, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.line = QtWidgets.QFrame(Dialog_About)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_2.addWidget(self.line)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Dialog_About)
        self.label.setMinimumSize(QtCore.QSize(160, 0))
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_version = QtWidgets.QLabel(Dialog_About)
        self.label_version.setAlignment(QtCore.Qt.AlignCenter)
        self.label_version.setObjectName("label_version")
        self.verticalLayout.addWidget(self.label_version)
        spacerItem3 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem3)
        self.label2 = QtWidgets.QLabel(Dialog_About)
        self.label2.setObjectName("label2")
        self.verticalLayout.addWidget(self.label2)
        self.label_authors = QtWidgets.QLabel(Dialog_About)
        self.label_authors.setAlignment(QtCore.Qt.AlignCenter)
        self.label_authors.setObjectName("label_authors")
        self.verticalLayout.addWidget(self.label_authors)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem4)
        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog_About)
        QtCore.QMetaObject.connectSlotsByName(Dialog_About)

    def retranslateUi(self, Dialog_About):
        _translate = QtCore.QCoreApplication.translate
        Dialog_About.setWindowTitle(_translate("Dialog_About", "About"))
        self.label_title.setText(_translate("Dialog_About", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600;\">ECCW</span><br/>Exact Critical Coulomb Wedge</p></body></html>"))
        self.label.setText(_translate("Dialog_About", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Version</span></p></body></html>"))
        self.label_version.setText(_translate("Dialog_About", "version"))
        self.label2.setText(_translate("Dialog_About", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Authors</span></p></body></html>"))
        self.label_authors.setText(_translate("Dialog_About", "authors"))

import eccw.images.ressources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog_About = QtWidgets.QDialog()
    ui = Ui_Dialog_About()
    ui.setupUi(Dialog_About)
    Dialog_About.show()
    sys.exit(app.exec_())

