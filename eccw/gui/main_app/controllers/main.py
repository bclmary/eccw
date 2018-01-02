#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from collections import OrderedDict
from os.path import dirname, realpath
import sys
import webbrowser

from eccw.gui.main_app.viewers.main import Ui_Form
from eccw.gui.main_app.controllers.dialog_about import About
from eccw.gui.calculator_app.controllers.calculator_main import CalculatorController
from eccw.gui.plot_app.controllers.plot_main import PlotController
from eccw.gui.shared.wrappers import WrapperDict
from eccw.shared.print_tools import graph_print
from eccw.shared.file_management import EccwFile


class MainController(QtGui.QWidget, Ui_Form, WrapperDict):
    """Main window of ECCW app."""
    def __init__(self, parent=None, **kwargs):
        super(MainController, self).__init__(parent)
        self.setupUi(self)
        self.current_dir = QtCore.QDir.homePath()
        self.current_dir = "/home/bmary/Programmation/eccw/tests/"  # debug
        self.mime_types = ("Fichier eccw (*.%s);;Tout les Fichiers (*.*)" %
                           EccwFile.mime)
        # Set calculator tab.
        self.calculator = CalculatorController()
        layoutC = QtGui.QVBoxLayout()
        layoutC.addWidget(self.calculator)
        self.tabWidget_main.widget(0).setLayout(layoutC)
        # Set plot tab.
        self.plot = PlotController()
        layoutP = QtGui.QVBoxLayout()
        layoutP.addWidget(self.plot)
        self.tabWidget_main.widget(1).setLayout(layoutP)
        # Define behaviours
        self.pushButton_Open.clicked.connect(self.load_session)
        self.pushButton_Save.clicked.connect(self.save_session)
        self.pushButton_About.clicked.connect(self.click_about)
        self.pushButton_Documentation.clicked.connect(self.click_doc)
        # Defines keyboard shortcuts.
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+Q"), self, self.close)
        TabW = self.tabWidget_main
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+Page up"), self,
                        lambda: TabW.setCurrentIndex(TabW.currentIndex()-1))
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+Page down"), self,
                        lambda: TabW.setCurrentIndex(TabW.currentIndex()+1))
        # Dictionnary (WrapperDict)
        self.dict = OrderedDict([
            ("calculator", self.calculator),
            ("plot",       self.plot)
        ])
        # Fill values with kwargs.
        if kwargs:
            self.set_params(**kwargs)
        self.show()

    def click_about(self):
        self.about = About()

    def click_doc(self):
        file_name = "/eccw/documentation/ECCW.pdf"
        file_name = "".join([p for p in sys.path if p[-4:] == "eccw"]
                            + [file_name])
        webbrowser.open(file_name, new=0, autoraise=True)

    # Save and load file management.

    def load_session(self):
        OpenDialog = QtGui.QFileDialog.getOpenFileName
        file_name = OpenDialog(self, "Open file", self.current_dir,
                               self.mime_types)
        if file_name == "":
            return
        self.current_dir = dirname(realpath(file_name))
        eccwf = EccwFile(filename=file_name)
        if eccwf.values is None:
            message = ("Wrong file type.\n"
                       "Chosen file must be a *.eccw mime type.")
            QtGui.QMessageBox.about(self, "Error", message)
            return
        self.set_params(**eccwf.values)

    def save_session(self):
        SaveDialog = QtGui.QFileDialog.getSaveFileNameAndFilter
        file_name, _ = SaveDialog(self, "Save file", self.current_dir,
                                  self.mime_types)
        if file_name:
            eccwf = EccwFile(data=self.get_params())
            eccwf.save(file_name)


if __name__ == "__main__":
    import sys
    eccwf = EccwFile(filename="../../../../tests/test.eccw")
    params = eccwf.values

    try:
        app = QtGui.QApplication(sys.argv)
        myapp = MainController(**params)
        sys.exit(app.exec_())
    finally:
        pass
        # print("params =")
        # graph_print(myapp.get_select())
