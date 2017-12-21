#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from os.path import dirname, realpath
from collections import OrderedDict
from matplotlib.cm import get_cmap
import csv

from eccw.gui.plot_app.viewers.plot_main import Ui_Form
from eccw.gui.plot_app.controllers.curve_settings import CurveController
from eccw.gui.plot_app.controllers.point_settings import RefPointSettings
from eccw.gui.shared.wrappers import Wrapper, WrapperDict, WrapperList
# from eccw.shared.file_management import EccwFile
from eccw.physics.eccw_plot import EccwPlot
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
        self.plot_core = EccwPlot()
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
        self.legend = Wrapper(False, process=lambda x: eval(str(x)),
                              action=self.radioButton_legend.setChecked)
        self.title = Wrapper(False, process=lambda x: eval(str(x)),
                             action=self.radioButton_title.setChecked)
        # Init events
        self.pushButton_addRefPoint.clicked.connect(self.add_ref_point)
        self.pushButton_killAllRefPoints.clicked.connect(
            self.kill_all_refpoints)
        self.pushButton_openRefPoints.clicked.connect(self.import_ref_points)
        self.pushButton_addCurve.clicked.connect(self.add_curve_tab)
        self.pushButton_killAllCurves.clicked.connect(self.kill_all_curves)
        self.radioButton_legend.clicked.connect(self._set_legend)
        self.radioButton_title.clicked.connect(self._set_title)
        self.pushButton_plotOne.clicked.connect(self.plot_one)
        self.pushButton_plotAll.clicked.connect(self.plot_all)
        # Parameters list for dry and fluids cases.
        self.params_list_dry = ('phiB', 'phiD')
        self.params_list_fluids = ('phiB', 'phiD', 'delta_lambdaB',
                                   'delta_lambdaD', 'rho_f', 'rho_sr')
        # Dictionnary (WrapperDict)
        self.dict = OrderedDict([
            ("curves",    self.curves),
            ("refpoints", self.refpoints),
            ("legend",    self.legend),
            ("title",     self.title)
        ])
        # Additional variables
        self.latex_convert = {
            "alpha":         r"$\alpha$",
            "beta":          r"$\beta$",
            "phiB":          r"$\phi_{B}$",
            "phiD":          r"$\phi_{D}$",
            "delta_lambdaB": r"$\Delta \lambda_{B}$",
            "delta_lambdaD": r"$\Delta \lambda_{D}$",
            "rho_f":         r"\rho_{f}$",
            "rho_sr":        r"\rho_{sr}$"
        }
        # Fill values with kwargs
        if kwargs:
            self.set_params(**kwargs)
        if self.curve_count == 0:
            self.add_curve_tab()
        self.show()

    def set_params(self, **kwargs):
        # There must be as many curves and refpoints as asked to set.
        self.kill_all_curves()
        self.kill_all_refpoints()
        N = len(kwargs['curves'])
        for i in range(N):
            self.add_curve_tab(kwargs['curves'][i]['label'])
        N = len(kwargs['refpoints'])
        for i in range(N):
            self.add_ref_point()
        WrapperDict.set_params(self, **kwargs)

    def _set_legend(self):
        self.legend.value = self.radioButton_legend.isChecked()

    def _set_title(self):
        self.title.value = self.radioButton_title.isChecked()

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

    def add_curve_tab(self, label=None):
        self.curve_count += 1
        name = "Curve "+str(self.curve_count) if label is None else label
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

    def kill_all_refpoints(self):
        for elt in list(self.refpoints.list):
            elt.close()
            elt.closed = True
        self.remove_ref_point()
        self.pushButton_killAllRefPoints.setEnabled(False)

    # Main action !

    def _format_point_params(self, point_params):
        params = dict(point_params)
        if point_params['beta']['type'] == 'scalar':
            params['beta'] = point_params['beta']['value']
            params['alpha'] = None
            params['alpha_min'] = point_params['alpha']['value']['min']
            params['alpha_max'] = point_params['alpha']['value']['max']
        if point_params['alpha']['type'] == 'scalar':
            params['beta'] = None
            params['beta_min'] = point_params['beta']['value']['min']
            params['beta_max'] = point_params['beta']['value']['max']
            params['alpha'] = point_params['alpha']['value']
        return params

    def plot_one(self):  # TODO
        self.plot_core.reset_figure()
        select = self.get_select()
        
        for curve in select['curves']:
            if curve['fluids']:
                params_list = self.params_list_fluids
            else:
                params_list = self.params_list_dry
                self.plot_core.set_no_fluids()
            settings_type = curve['settings']['type']
            settings = curve['settings']['value']
            if settings_type in ('default', 'double'):
                params = {param: curve[param]['value']
                          for param in params_list}
                params['context'] = curve['context']
                settings['label'] = curve['label']
                graph_print(params)
                self.plot_core.set_params(**params)
                self.plot_core.add_curve(**settings)
                for point in curve['points']:
                    params = self._format_point_params(point)
                    self.plot_core.add_point(**params)
            elif settings_type == 'range':
                ranged_parameter = curve['range']
                range_ = curve[ranged_parameter]['value']
                if curve['reverse_cmap']:
                    cmap = get_cmap(settings.pop('colormap')+'_r')
                else:
                    cmap = get_cmap(settings.pop('colormap'))
                Ncolor = len(range_) - 1
                # Draw vertical or horizontal lines below curves
                # if points with no bounds.
                for point in curve['points']:
                    a, b = point['alpha'], point['beta']
                    beta = (b['value']
                            if b['type'] == 'scalar'
                            and a['value']['min'] == float('-inf')
                            and a['value']['max'] == float('inf')
                            else None)
                    alpha = (a['value']
                             if a['type'] == 'scalar'
                             and b['value']['min'] == float('-inf')
                             and b['value']['max'] == float('inf')
                             else None)
                    self.plot_core.add_line(beta=beta, alpha=alpha)
                # Draw ranged curves.
                for i, x in enumerate(range_):
                    params = {param: curve[param]['value']
                              if param != ranged_parameter else x
                              for param in params_list}
                    params['context'] = curve['context']
                    if curve['auto_label']:
                        settings['label'] = self.latex_convert[curve['range']] + " = " + str(x)
                    self.plot_core.set_params(**params)
                    settings['color'] = cmap(i/Ncolor)
                    self.plot_core.add_curve(**settings)
                    for point in curve['points']:
                        params = self._format_point_params(point)
                        self.plot_core.add_point(line=False, **params)
        for refpoint in select['refpoints']:
            self.plot_core.add_refpoint(**refpoint)
        if select['legend']:
            self.plot_core.add_legend()
        # if select['title']:
        #     curve = self.tabWidget.currentWidget().get_select()
        #     params = [self.latex_convert[curve[param]['value']
        #               if param != ranged_parameter else x
        #               for param in params_list}
        #     title=", ".join(
        #     self.plot_core.add_title()
        self.plot_core.show(block=True)

    def plot_all(self):  # TODO
        graph_print(self.get_params())


if __name__ == "__main__":
    import sys
    from eccw.shared.file_management import EccwFile
    eccwf = EccwFile(filename="../../../../tests/test.eccw")
    eccwf.show()
    params = eccwf.values['plot']

    try:
        app = QtGui.QApplication(sys.argv)
        myapp = PlotController(**params)
        sys.exit(app.exec_())
    finally:
        print("params =")
        # graph_print(myapp.get_params())
        graph_print(myapp.get_select())
