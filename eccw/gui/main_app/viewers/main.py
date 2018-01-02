# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../uis/main.ui'
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
        Form.resize(714, 528)
        font = QtGui.QFont()
        font.setKerning(True)
        Form.setFont(font)
        self.verticalLayout_18 = QtGui.QVBoxLayout(Form)
        self.verticalLayout_18.setObjectName(_fromUtf8("verticalLayout_18"))
        self.horizontalLayout_topmenu = QtGui.QHBoxLayout()
        self.horizontalLayout_topmenu.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.horizontalLayout_topmenu.setObjectName(_fromUtf8("horizontalLayout_topmenu"))
        self.pushButton_Open = QtGui.QPushButton(Form)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/buttons/button_open.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Open.setIcon(icon)
        self.pushButton_Open.setObjectName(_fromUtf8("pushButton_Open"))
        self.horizontalLayout_topmenu.addWidget(self.pushButton_Open)
        self.pushButton_Save = QtGui.QPushButton(Form)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/buttons/button_save.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Save.setIcon(icon1)
        self.pushButton_Save.setObjectName(_fromUtf8("pushButton_Save"))
        self.horizontalLayout_topmenu.addWidget(self.pushButton_Save)
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setEnabled(False)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 32))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/buttons/button_export.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon2)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout_topmenu.addWidget(self.pushButton)
        self.line_2 = QtGui.QFrame(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_2.sizePolicy().hasHeightForWidth())
        self.line_2.setSizePolicy(sizePolicy)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.horizontalLayout_topmenu.addWidget(self.line_2)
        self.pushButton_About = QtGui.QPushButton(Form)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/buttons/button_about.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_About.setIcon(icon3)
        self.pushButton_About.setObjectName(_fromUtf8("pushButton_About"))
        self.horizontalLayout_topmenu.addWidget(self.pushButton_About)
        self.pushButton_Documentation = QtGui.QPushButton(Form)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/buttons/button_documentation.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Documentation.setIcon(icon4)
        self.pushButton_Documentation.setObjectName(_fromUtf8("pushButton_Documentation"))
        self.horizontalLayout_topmenu.addWidget(self.pushButton_Documentation)
        self.verticalLayout_18.addLayout(self.horizontalLayout_topmenu)
        self.tabWidget_main = QtGui.QTabWidget(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget_main.sizePolicy().hasHeightForWidth())
        self.tabWidget_main.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.tabWidget_main.setFont(font)
        self.tabWidget_main.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.tabWidget_main.setToolTip(_fromUtf8(""))
        self.tabWidget_main.setAutoFillBackground(True)
        self.tabWidget_main.setTabPosition(QtGui.QTabWidget.South)
        self.tabWidget_main.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabWidget_main.setElideMode(QtCore.Qt.ElideLeft)
        self.tabWidget_main.setDocumentMode(True)
        self.tabWidget_main.setTabsClosable(False)
        self.tabWidget_main.setObjectName(_fromUtf8("tabWidget_main"))
        self.tab_calculator = QtGui.QWidget()
        self.tab_calculator.setAutoFillBackground(True)
        self.tab_calculator.setObjectName(_fromUtf8("tab_calculator"))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/tabs/tab_calculate.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget_main.addTab(self.tab_calculator, icon5, _fromUtf8(""))
        self.tab_plot = QtGui.QWidget()
        self.tab_plot.setAutoFillBackground(True)
        self.tab_plot.setObjectName(_fromUtf8("tab_plot"))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8(":/tabs/tab_plot.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget_main.addTab(self.tab_plot, icon6, _fromUtf8(""))
        self.verticalLayout_18.addWidget(self.tabWidget_main)

        self.retranslateUi(Form)
        self.tabWidget_main.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.pushButton_Open.setToolTip(_translate("Form", "Open previously saved session (Crtl+O)", None))
        self.pushButton_Open.setText(_translate("Form", "Open", None))
        self.pushButton_Open.setShortcut(_translate("Form", "Ctrl+O", None))
        self.pushButton_Save.setToolTip(_translate("Form", "Save current session (Crtl+S)", None))
        self.pushButton_Save.setText(_translate("Form", "Save", None))
        self.pushButton_Save.setShortcut(_translate("Form", "Ctrl+S", None))
        self.pushButton.setToolTip(_translate("Form", "Export datas of current session in cvs format (Crtl+E)", None))
        self.pushButton.setText(_translate("Form", "Export", None))
        self.pushButton.setShortcut(_translate("Form", "Ctrl+E", None))
        self.pushButton_About.setToolTip(_translate("Form", "About ECCW software", None))
        self.pushButton_About.setText(_translate("Form", "About", None))
        self.pushButton_Documentation.setToolTip(_translate("Form", "Display pdf fulll documentation (Crtl+D)", None))
        self.pushButton_Documentation.setText(_translate("Form", "Documentation", None))
        self.pushButton_Documentation.setShortcut(_translate("Form", "Ctrl+D", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_calculator), _translate("Form", "Calculator                    ", None))
        self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_plot), _translate("Form", "Plot                              ", None))

import eccw.images.ressources_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

