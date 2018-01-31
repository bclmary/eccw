# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../uis/point_settings.ui'
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
        Form.resize(465, 28)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(0, 0))
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_beta = QtGui.QLabel(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_beta.sizePolicy().hasHeightForWidth())
        self.label_beta.setSizePolicy(sizePolicy)
        self.label_beta.setMaximumSize(QtCore.QSize(12, 24))
        self.label_beta.setText(_fromUtf8(""))
        self.label_beta.setPixmap(QtGui.QPixmap(_fromUtf8(":/params/params_beta.png")))
        self.label_beta.setScaledContents(True)
        self.label_beta.setObjectName(_fromUtf8("label_beta"))
        self.horizontalLayout.addWidget(self.label_beta)
        self.horizontalLayout_beta = QtGui.QHBoxLayout()
        self.horizontalLayout_beta.setObjectName(_fromUtf8("horizontalLayout_beta"))
        self.horizontalLayout.addLayout(self.horizontalLayout_beta)
        self.label_alpha = QtGui.QLabel(Form)
        self.label_alpha.setMaximumSize(QtCore.QSize(12, 24))
        self.label_alpha.setText(_fromUtf8(""))
        self.label_alpha.setPixmap(QtGui.QPixmap(_fromUtf8(":/params/params_alpha.png")))
        self.label_alpha.setScaledContents(True)
        self.label_alpha.setObjectName(_fromUtf8("label_alpha"))
        self.horizontalLayout.addWidget(self.label_alpha)
        self.horizontalLayout_alpha = QtGui.QHBoxLayout()
        self.horizontalLayout_alpha.setObjectName(_fromUtf8("horizontalLayout_alpha"))
        self.horizontalLayout.addLayout(self.horizontalLayout_alpha)
        self.horizontalLayout_settings = QtGui.QHBoxLayout()
        self.horizontalLayout_settings.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.horizontalLayout_settings.setObjectName(_fromUtf8("horizontalLayout_settings"))
        self.horizontalLayout.addLayout(self.horizontalLayout_settings)
        spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_kill = QtGui.QPushButton(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_kill.sizePolicy().hasHeightForWidth())
        self.pushButton_kill.setSizePolicy(sizePolicy)
        self.pushButton_kill.setMaximumSize(QtCore.QSize(28, 28))
        self.pushButton_kill.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/buttons/button_close.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_kill.setIcon(icon)
        self.pushButton_kill.setObjectName(_fromUtf8("pushButton_kill"))
        self.horizontalLayout.addWidget(self.pushButton_kill)

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.pushButton_kill, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.close)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label_beta.setToolTip(_translate("Form", "Basal slope [deg]", None))
        self.label_alpha.setToolTip(_translate("Form", "Surface slope [deg]", None))
        self.pushButton_kill.setToolTip(_translate("Form", "Delete this point", None))

import eccw.images.ressources_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

