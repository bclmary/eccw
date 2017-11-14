#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from os.path import dirname, realpath
from collections import OrderedDict
import csv

from eccw.gui.plot_app.viewers.plot_main import Ui_Form
from eccw.gui.plot_app.controllers.curve_settings import CurveController
from eccw.gui.plot_app.controllers.point_settings import RefPointSettings
from eccw.gui.shared.wrappers import Wrapper, WrapperDict, WrapperList
from eccw.shared.file_management import EccwFile
from eccw.shared.print_tools import graph_print


class PlotController(QtGui.QWidget, Ui_Form, WrapperDict):
    """Main widget for plotting curve and points.

    Keyword arguments:
    curves    -- awaits a dict of keyword arguments for a CurveController
                 element.
    refpoints -- awaits a dict of keyword arguments for a RefPointSettings
                 element.
    legend    -- awaits a boolean.
    title     -- awaits a boolean.

    This is a Qt derived object.
    """
    def __init__(self, **kwargs):
        super(PlotController, self).__init__()
        self.setupUi(self)
        self.current_dir = QtCore.QDir.homePath()
        self.current_dir = "/home/bmary/Programmation/eccw/eccw/test/"
        # self.mimetypes = ("Fichier eccw (*.%s);;Tout les Fichiers (*.*)" %
        #                   EccwFile.mime)
        self.import_mimetypes = ("Fichiers texte (*.txt *.dat *.csv);;"
                                 "Tout les Fichiers (*.*)")
        # Init local attributs.
        self.curve_count = 0
        self.curves = WrapperList()
        self.refpoints = WrapperList()
        if kwargs:
            # Create curves and refpoints.
            # They will be setted later with self.set_params.
            N = len(kwargs.get("curves", []))
            for i in range(N):
                self.add_curve_tab()
            N = len(kwargs.get("refpoints", []))
            for i in range(N):
                self.add_ref_point()
        self.legend = Wrapper(False, fn=self.radioButton_legend.setChecked)
        self.title = Wrapper(False, fn=self.radioButton_title.setChecked)
        # Init events
        self.pushButton_addRefPoint.clicked.connect(self.add_ref_point)
        self.pushButton_killAllRefPoints.clicked.connect(
            self.kill_all_ref_points)
        self.pushButton_openRefPoints.clicked.connect(self.import_ref_points)
        self.pushButton_addCurve.clicked.connect(self.add_curve_tab)
        self.pushButton_killAllCurves.clicked.connect(self.kill_all_curves)
        self.radioButton_legend.clicked.connect(self._set_legend)
        self.radioButton_title.clicked.connect(self._set_title)
        self.pushButton_plotOne.clicked.connect(self.plot_one)
        self.pushButton_plotAll.clicked.connect(self.plot_all)
        # Dictionnary (WrapperDict)
        self.dict = OrderedDict([
            ("curves",    self.curves),
            ("refpoints", self.refpoints),
            ("legend",    self.legend),
            ("title",     self.title)
        ])
        # Fill values with kwargs
        if kwargs:
            self.set_params(**kwargs)
        if self.curve_count == 0:
            self.add_curve_tab()
        self.show()

    # Param settings

    def _set_legend(self):
        self.legend.value = self.radioButton_legend.isChecked()

    def _set_title(self):
        self.title.value = self.radioButton_title.isChecked()

    # Save and load file management.

    def get_load_data(self):  # TODO this will move too main_app
        OpenDialog = QtGui.QFileDialog.getOpenFileName
        file_name = OpenDialog(self, "Open file", self.current_dir,
                               self.mimetypes)
        if file_name == "":
            return None
        self.current_dir = dirname(realpath(file_name))
        eccwf = EccwFile(file_name=file_name)
        if eccwf.values is None:
            message = ("Wrong file type.\n"
                       "Chosen file must be a *.eccw mime type.")
            QtGui.QMessageBox.about(self, "Error", message)
            return None
        else:
            return eccwf.values

    def get_save_file_name(self, submime=""):  # TODO  this will move too main_app
        SaveDialog = QtGui.QFileDialog.getSaveFileNameAndFilter
        file_name, _ = SaveDialog(self, "Save file", self.current_dir,
                                  self.import_mimetypes)
        if file_name:
            self.current_dir = dirname(realpath(file_name))
            mime = "." + EccwFile.mime
            N = len(submime) + 5
            if file_name[-N:] != submime+mime:
                if file_name[-5:] != mime:
                    file_name += submime+mime
                else:
                    file_name = file_name[:-5] + submime+mime
        return file_name

#    def loadCurves(self):
#        data = self.get_load_data()
#        if data is None:
#            return
#        curves = data["plot"].get("curves")
#        if curves:
#            self.setCurves(curves)
#        else:
#            message = "The chosen file has no curve data."
#            QtGui.QMessageBox.about(self, "Info", message)

#    def saveCurves(self):
#        file_name = self.get_save_file_name(submime='.curves')
#        if file_name == "":
#            return
#        params = OrderedDict([("plot", self.get_params())])
#        eccwf = EccwFile(params)
#        eccwf.save(file_name, target="curves")

    def import_ref_points(self):
        """Add ref points using data from csv file.

        Awaited format:
        beta, alpha, size, style, label, red, green, blue, alpha_chanel

        beta in deg
        alpha in deg
        size in pixels
        style among ['c', 's', 'd', 't', '*', '+', 'p']
        label is any string value
        rgba color channels red, green , blue and alpha are floats in [0:1]
        """
        OpenDialog = QtGui.QFileDialog.getOpenFileName
        file_name = OpenDialog(self, "Import from csv file", self.current_dir,
                               self.import_mimetypes)
        if file_name == "":
            return None  # Squip if no file selected.
        with open(file_name, 'r') as csvfile:
            # dialect = csv.Sniffer().sniff(csvfile.read(1024),
            #                               delimiters=';,\t')
            # csvfile.seek(0)
            parsed_data = csv.reader(csvfile)  # , dialect)
            errors = ["datas from file<br>%s<br> gets wrong items at lines:"
                      "<br>" % file_name]
            for i, row in enumerate(parsed_data):
                row = [elt.strip() for elt in row]
                self.add_ref_point()
                params = {}
                params['beta'] = row[0]
                params['alpha'] = row[1]
                params['size'] = row[2] or 3. if len(row) > 2 else 3.
                params['style'] = row[3] or 'c' if len(row) > 3 else 'circle'
                params['label'] = row[4] if len(row) > 4 else ''
                params['color'] = row[5:9] if len(row) > 8 else (0, 0, 0, 1)
                try:
                    self.refpoints.list[-1].set_params(**params)
                except TypeError:
                    errors.append("%s, " % (i+1))
            if len(errors) > 1:
                errors.append("<br><br><b>Awaited parameters:</b><br>"
                              "beta, alpha, [size, style, label, color]<br>"
                              "<br><b>Awaited format:</b>"
                              "<table>"
                              "<tr><td>beta</th><td>float</th></tr>"
                              "<tr><td>alpha      </td><td>float</td></tr>"
                              "<tr><td>size</td><td>float &gt; 0</td></tr>"
                              "<tr><td>style</td><td>caracter in [c s d t * +"
                              " p]</td></tr>"
                              "<tr><td>label</td><td>string</td></tr>"
                              "<tr><td>color</td><td>4 floats in [0:1]</td>"
                              "</tr></table>")
                QtGui.QMessageBox.about(self, "Warning", ''.join(errors))

    # Curve tab management.

    def add_curve_tab(self):
        self.curve_count += 1
        name = "Curve "+str(self.curve_count)
        newCurve = CurveController(label=name)
        self.curves.list.append(newCurve)
        ncurve = len(self.curves.list)
        newCurve.pushButton_kill.clicked.connect(self.kill_curve_tab)
        # Single curve : put in frame widget
        if ncurve == 1:
            self.set_single_curve(newCurve)
            self.pushButton_killAllCurves.setEnabled(True)
        # Second curve : switch to tab widget
        elif ncurve == 2:
            firstCurve = self.curves.list[0]
            firstname = firstCurve.label.get_params()
            firstCurve.label.lineEdit.textChanged.connect(self._edit_tab_title)
            self.tabWidget.setVisible(True)
            self.tabWidget.addTab(firstCurve, firstname)
            self.frame_singleCurve.setVisible(False)
            firstCurve.setVisible(False)
        if ncurve > 1:
            self.tabWidget.addTab(newCurve, name)
            self.tabWidget.setCurrentWidget(newCurve)
            newCurve.label.lineEdit.textChanged.connect(self._edit_tab_title)

    def set_single_curve(self, curve):
        self.tabWidget.removeTab(0)
        self.tabWidget.setVisible(False)
        self.verticalLayout_singleCurve.addWidget(curve)
        curve.setVisible(True)
        self.frame_singleCurve.setVisible(True)

    def kill_curve_tab(self):
        for elt in list(self.curves.list):
            if elt.closed:
                i = self.tabWidget.indexOf(elt)
                self.tabWidget.setCurrentIndex(i-1)
                self.tabWidget.removeTab(i)
                del self.curves.list[self.curves.list.index(elt)]
                break
        if len(self.curves.list) == 1:
            singlecurve = self.curves.list[0]
            self.set_single_curve(singlecurve)
            singlecurve.label.lineEdit.textChanged.disconnect(
                self._edit_tab_title)
        elif len(self.curves.list) == 0:
            self.pushButton_killAllCurves.setEnabled(False)

    def kill_all_curves(self):
        if len(self.curves.list) == 1:
            self.curves.list[0].close()
            self.curves.list[0].closed = True
            self.kill_curve_tab()
        else:
            for elt in list(self.curves.list):
                i = self.tabWidget.indexOf(elt)
                self.tabWidget.removeTab(i)
                del self.curves.list[self.curves.list.index(elt)]
        self.frame_singleCurve.setVisible(True)
        self.tabWidget.setVisible(False)
        self.pushButton_killAllCurves.setEnabled(False)

    def _edit_tab_title(self):
        i = self.tabWidget.currentIndex()
        title = self.tabWidget.currentWidget().label.get_params()
        self.tabWidget.setTabText(i, title)

    # RefPoint management.

    def add_ref_point(self):
        if not self.refpoints.list:
            self.pushButton_killAllRefPoints.setEnabled(True)
        newRefPoint = RefPointSettings()
        newRefPoint.pushButton_kill.clicked.connect(self.remove_ref_point)
        self.verticalLayout_points_settings.addWidget(newRefPoint)
        self.refpoints.list.append(newRefPoint)

    def remove_ref_point(self):
        for elt in list(self.refpoints.list):
            if elt.closed:
                del self.refpoints.list[self.refpoints.list.index(elt)]
        if not self.refpoints.list:
            self.pushButton_killAllRefPoints.setEnabled(False)

    def kill_all_ref_points(self):
        for elt in list(self.refpoints.list):
            elt.close()
            elt.closed = True
        self.remove_ref_point()
        self.pushButton_killAllRefPoints.setEnabled(False)

    # Main action !

    def plot_one(self):  # TODO
        tmp = WrapperDict.get_select(self)
        if len(self.curves.list) > 1:
            i = self.tabWidget.currentIndex()
            tmp["curves"] = tmp["curves"][i:i+1]
        graph_print(tmp)

    def plot_all(self):  # TODO
        graph_print(self.get_select())


if __name__ == "__main__":
    import sys
    try:
        app = QtGui.QApplication(sys.argv)
#        eccwf = EccwFile(file_name="test_in.session.eccw")
        myapp = PlotController()
#        myapp.add_curve_tab()
        sys.exit(app.exec_())
    finally:
        print("params =")
        graph_print(myapp.get_params())
        graph_print(myapp.get_select())
