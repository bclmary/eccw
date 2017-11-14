#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from collections import OrderedDict

from eccw.gui.plot_app.viewers.curve_settings import Ui_Form
from eccw.gui.plot_app.controllers.curve_graphicSettings import \
    SwitchCurveGraphicSettings
from eccw.gui.plot_app.controllers.point_settings import CurvePointSettings
from eccw.gui.shared.controllers.lineEdit import SwitchScalarRange
from eccw.gui.shared.controllers.comboBox import ComboBoxContext
from eccw.gui.shared.controllers.lineEdit import StringLineEdit
from eccw.gui.shared.controllers.label import Label
from eccw.gui.shared.wrappers import Wrapper, WrapperDict, WrapperList
from eccw.shared.print_tools import graph_print


class CurveController(QtGui.QWidget, Ui_Form, WrapperDict):
    """Widget for curve parameters and settings entry.

    Keyword arguments:
    label         -- awaits a string label.
    context       -- awaits a string among 'Compression' and 'Extension'.
    fluids        -- awaits a boolean.
    phiB          -- awaits a dict of keyword arguments for a SwitchScalarRange
                     element.
    phiD          -- awaits a dict of keyword arguments for a SwitchScalarRange
                     element.
    delta_lambdaB -- awaits a dict of keyword arguments for a SwitchScalarRange
                     element.
    delta_lambdaD -- awaits a dict of keyword arguments for a SwitchScalarRange
                     element.
    rho_f         -- awaits a dict of keyword arguments for a SwitchScalarRange
                     element.
    rho_sr        -- awaits a dict of keyword arguments for a SwitchScalarRange
                     element.
    settings      -- awaits a dict of keyword arguments for a
                     SwitchCurveGraphicSettings element.
    points        -- awaits a dict of keyword arguments for a
                     CurvePointSettings element.

    This is a Qt derived object.
    """
    def __init__(self, **kwargs):
        super(CurveController, self).__init__()
        self.setupUi(self)
        self.setAutoFillBackground(True)  # Needed by QTabWidget in plot_main.
        # Init local attributs.
        self.closed = False
        # Init additional objects
        # Mechanic.
        self.phiB = SwitchScalarRange()
        self.phiD = SwitchScalarRange()
        # Fluids.
        self.fluids = Wrapper(False, fn=self.groupBox_fluids.setChecked)
        self.delta_lambdaB = SwitchScalarRange()
        self.delta_lambdaD = SwitchScalarRange()
        self.rho_f = SwitchScalarRange()
        self.rho_sr = SwitchScalarRange()
        self.context = ComboBoxContext()
        # Label
        self.label_label = Label("label")
        self.label = StringLineEdit()
        # Graphic settings.
        self.settings = SwitchCurveGraphicSettings()
        # Curve points
        self.points = WrapperList()
        if kwargs:
            # Create N points.
            # they will be setted later with self.set_params.
            N = len(kwargs.get("points", []))
            for i in range(N):
                self.add_curve_point()
        # Put additional elements in self.
        self.horizontalLayout_phiB.addWidget(self.phiB)
        self.horizontalLayout_phiD.addWidget(self.phiD)
        self.horizontalLayout_lamdaB.addWidget(self.delta_lambdaB)
        self.horizontalLayout_lamdaD.addWidget(self.delta_lambdaD)
        self.horizontalLayout_rhof.addWidget(self.rho_f)
        self.horizontalLayout_rhosr.addWidget(self.rho_sr)
        self.verticalLayout_context.addWidget(self.context)
        self.verticalLayout_settings.addWidget(self.settings)
        self.horizontalLayout_label.addWidget(self.label_label)
        self.horizontalLayout_label.addWidget(self.label)
        # List for SwitchScalarRange objects control.
        self.param_object_list = [
            self.phiB, self.phiD, self.delta_lambdaB,
            self.delta_lambdaD, self.rho_f, self.rho_sr
        ]
        # Define events
        self.pushButton_addCurvePoint.clicked.connect(self.add_curve_point)
        self.pushButton_killAllCurvePoints.clicked.connect(
            self.kill_all_curve_point)
        self.checkBox_splittedCurves.clicked.connect(self._auto_set_settings)
        self.groupBox_fluids.clicked.connect(self._fluids_changed)
        tmp = lambda elt: lambda: self._there_can_be_only_one(elt)
        for elt in self.param_object_list:
            elt.pushButton.clicked.connect(tmp(elt))
        self.checkBox_autoLabel.clicked.connect(self._set_auto_label)
        self.pushButton_kill.clicked.connect(self._set_closed)
        # Dictionnary (WrapperDict)
        self.dict = OrderedDict([
            ("label",         self.label),
            ("context",       self.context),
            ("fluids",        self.fluids),
            ("phiB",          self.phiB),
            ("phiD",          self.phiD),
            ("delta_lambdaB", self.delta_lambdaB),
            ("delta_lambdaD", self.delta_lambdaD),
            ("rho_f",         self.rho_f),
            ("rho_sr",        self.rho_sr),
            ("settings",      self.settings),
            ("points",        self.points)
        ])
        # Fill values with kwargs
        if kwargs:
            self.set_params(**kwargs)
        self._auto_set_settings()
        self.show()

    # Events management.

    def _set_closed(self):
        self.closed = True

    def _is_range_activated(self):
        return not all([Obj.focus.value == "scalar"
                        for Obj in self.param_object_list])

    def _there_can_be_only_one(self, elt):
        for Obj in self.param_object_list:
            if Obj is not elt:
                Obj.set_scalar_visible(True)
        self._auto_set_settings()

    def _auto_set_settings(self):
        # Next line solves blinking when switching from a focus to another.
        self.settings.set_visible_manual("")
        if self._is_range_activated():
            self.settings.set_visible_manual("range")
            self.checkBox_splittedCurves.setEnabled(False)
            self.checkBox_autoLabel.setEnabled(True)
            self.checkBox_reverseColormap.setEnabled(True)
            self._set_auto_label()
        else:
            self.checkBox_splittedCurves.setEnabled(True)
            self.checkBox_autoLabel.setEnabled(False)
            self.checkBox_reverseColormap.setEnabled(False)
            self.label.setEnabled(True)
            if self.checkBox_splittedCurves.isChecked():
                self.settings.set_visible_manual("double")
            else:
                self.settings.set_visible_manual("default")

    def _fluids_changed(self):
        self.fluids.value = self.groupBox_fluids.isChecked()

    def _set_auto_label(self):
        self.label.setDisabled(self.checkBox_autoLabel.isChecked())

    # Curve Points management.

    def add_curve_point(self):
        if not self.points.list:
            self.pushButton_killAllCurvePoints.setEnabled(True)
        new_curve_point = CurvePointSettings()
        new_curve_point.pushButton_kill.clicked.connect(
            self.remove_curve_point)
        self.verticalLayout_points_settings.addWidget(new_curve_point)
        self.points.list.append(new_curve_point)

    def remove_curve_point(self):
        """un-list all invisible CurvePointSettings."""
        for elt in list(self.points.list):
            if elt.closed:
                del self.points.list[self.points.list.index(elt)]
        if not self.points.list:
            self.pushButton_killAllCurvePoints.setEnabled(False)

    def kill_all_curve_point(self):
        for elt in list(self.points.list):
            elt.close()
            elt.closed = True
        self.remove_curve_point()


if __name__ == "__main__":
    import sys
    try:
        app = QtGui.QApplication(sys.argv)

        phiB = {"range": {"begin": 25, "step": 5, "end": 45},
                "scalar": 30, "focus": "range"}
        point = {"alpha": {"bound": {"min": 0, "max": 4},
                           "scalar": 2, "focus": "bound"},
                 "beta": {"bound": {"min": -1, "max": 1},
                          "scalar": 0, "focus": "scalar"},
                 "sketch": True, "color": (0, 1, 0, 1), "size": 5,
                 "style": "square", "label": "poulpe"}
        params = {"fluids": True, "phiB": phiB, "label": "poulpe",
                  "context": "Extension", "points": [point, point]}
        myapp = CurveController(**params)

        sys.exit(app.exec_())
    finally:
        print("params =")
        graph_print(myapp.get_params(), indent=2)
        print("select =")
        graph_print(myapp.get_select(), indent=2)
