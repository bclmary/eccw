# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../uis/lineEdit_range.ui'
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
        Form.setMaximumSize(QtCore.QSize(120, 16777215))
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lineEdit_begin = QtGui.QLineEdit(Form)
        self.lineEdit_begin.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_begin.sizePolicy().hasHeightForWidth())
        self.lineEdit_begin.setSizePolicy(sizePolicy)
        self.lineEdit_begin.setMinimumSize(QtCore.QSize(40, 0))
        self.lineEdit_begin.setMaximumSize(QtCore.QSize(40, 30))
        self.lineEdit_begin.setWhatsThis(_fromUtf8(""))
        self.lineEdit_begin.setText(_fromUtf8(""))
        self.lineEdit_begin.setObjectName(_fromUtf8("lineEdit_begin"))
        self.horizontalLayout.addWidget(self.lineEdit_begin)
        self.lineEdit_step = QtGui.QLineEdit(Form)
        self.lineEdit_step.setMinimumSize(QtCore.QSize(40, 0))
        self.lineEdit_step.setMaximumSize(QtCore.QSize(40, 30))
        self.lineEdit_step.setText(_fromUtf8(""))
        self.lineEdit_step.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_step.setObjectName(_fromUtf8("lineEdit_step"))
        self.horizontalLayout.addWidget(self.lineEdit_step)
        self.lineEdit_end = QtGui.QLineEdit(Form)
        self.lineEdit_end.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_end.sizePolicy().hasHeightForWidth())
        self.lineEdit_end.setSizePolicy(sizePolicy)
        self.lineEdit_end.setMinimumSize(QtCore.QSize(40, 0))
        self.lineEdit_end.setMaximumSize(QtCore.QSize(40, 30))
        self.lineEdit_end.setText(_fromUtf8(""))
        self.lineEdit_end.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_end.setObjectName(_fromUtf8("lineEdit_end"))
        self.horizontalLayout.addWidget(self.lineEdit_end)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.lineEdit_begin.setToolTip(_translate("Form", "Interval begin", None))
        self.lineEdit_step.setToolTip(_translate("Form", "Interval step", None))
        self.lineEdit_end.setToolTip(_translate("Form", "Interval end", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

