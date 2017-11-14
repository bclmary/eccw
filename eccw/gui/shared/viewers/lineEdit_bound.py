# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../uis/lineEdit_bound.ui'
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
        Form.resize(120, 30)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMaximumSize(QtCore.QSize(200, 16777215))
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lineEdit_min = QtGui.QLineEdit(Form)
        self.lineEdit_min.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_min.sizePolicy().hasHeightForWidth())
        self.lineEdit_min.setSizePolicy(sizePolicy)
        self.lineEdit_min.setMinimumSize(QtCore.QSize(40, 0))
        self.lineEdit_min.setMaximumSize(QtCore.QSize(40, 30))
        self.lineEdit_min.setText(_fromUtf8(""))
        self.lineEdit_min.setObjectName(_fromUtf8("lineEdit_min"))
        self.horizontalLayout.addWidget(self.lineEdit_min)
        self.label_1 = QtGui.QLabel(Form)
        self.label_1.setMinimumSize(QtCore.QSize(10, 0))
        self.label_1.setMaximumSize(QtCore.QSize(10, 30))
        self.label_1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_1.setObjectName(_fromUtf8("label_1"))
        self.horizontalLayout.addWidget(self.label_1)
        self.lineEdit = QtGui.QLineEdit(Form)
        self.lineEdit.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setMinimumSize(QtCore.QSize(20, 0))
        self.lineEdit.setMaximumSize(QtCore.QSize(20, 30))
        self.lineEdit.setToolTip(_fromUtf8(""))
        self.lineEdit.setText(_fromUtf8(""))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.horizontalLayout.addWidget(self.lineEdit)
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setMinimumSize(QtCore.QSize(10, 0))
        self.label_2.setMaximumSize(QtCore.QSize(10, 30))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.lineEdit_max = QtGui.QLineEdit(Form)
        self.lineEdit_max.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_max.sizePolicy().hasHeightForWidth())
        self.lineEdit_max.setSizePolicy(sizePolicy)
        self.lineEdit_max.setMinimumSize(QtCore.QSize(40, 0))
        self.lineEdit_max.setMaximumSize(QtCore.QSize(40, 30))
        self.lineEdit_max.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEdit_max.setText(_fromUtf8(""))
        self.lineEdit_max.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_max.setObjectName(_fromUtf8("lineEdit_max"))
        self.horizontalLayout.addWidget(self.lineEdit_max)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.lineEdit_min.setToolTip(_translate("Form", "Minimal value", None))
        self.label_1.setText(_translate("Form", "<", None))
        self.label_2.setText(_translate("Form", "<", None))
        self.lineEdit_max.setToolTip(_translate("Form", "Maximal value", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

