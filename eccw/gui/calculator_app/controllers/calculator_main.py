#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from collections import OrderedDict

from eccw.gui.calculator_app.viewers.calculator_main import Ui_Form
from eccw.gui.shared.controllers.lineEdit import SwitchScalarRange
from eccw.gui.shared.controllers.comboBox import ComboBoxContext
from eccw.shared.print_tools import graph_print
from eccw.gui.shared.wrappers import Wrapper, WrapperDict
from eccw.physics.eccw_compute import EccwCompute


class CalculatorController(QtGui.QWidget, Ui_Form, WrapperDict):

    def __init__(self, **kwargs):
        super(CalculatorController, self).__init__()
        self.setupUi(self)
        # Init local attributs.
        self.alpha = SwitchScalarRange(scalar=3.44)
        self.beta = SwitchScalarRange(scalar=0, range={'begin': -2, 'end': 2})
        self.phiB = SwitchScalarRange(scalar=30)
        self.phiD = SwitchScalarRange(scalar=10)
        self.delta_lambdaB = SwitchScalarRange()
        self.delta_lambdaD = SwitchScalarRange()
        self.rho_f = SwitchScalarRange()
        self.rho_sr = SwitchScalarRange()
        self.range = Wrapper(None)
        self.compute_core = EccwCompute()
        # List for SwitchScalarRange objects control.
        self.param_flag_list = [
            "alpha", "beta", "phiB", "phiD",
            "delta_lambdaB", "delta_lambdaD", "rho_f", "rho_sr"]
        self.param_object_list = [
            self.alpha, self.beta, self.phiB, self.phiD,
            self.delta_lambdaB, self.delta_lambdaD, self.rho_f, self.rho_sr]
        self.context = ComboBoxContext()
        self.results = Wrapper(action=self._set_results)
        self.fluids = Wrapper(False, process=lambda x: eval(str(x)),
                              action=self.groupBox_fluids.setChecked)
        self.fluids_flag_list = ["delta_lambdaB", "delta_lambdaD",
                                 "rho_f", "rho_sr"]
        # List of radioButton defining focus
        self.focus_object_list = [self.radioButton_alpha,
                                  self.radioButton_beta,
                                  self.radioButton_phiB,
                                  self.radioButton_phiD]
        self.focus_flag_list = ["alpha", "beta", "phiB", "phiD"]
        for elt, txt in zip(self.focus_object_list, self.focus_flag_list):
            elt.ID = txt
        self.focus = Wrapper("alpha", action=self.set_focus)
        # Put them in self
        self.horizontalLayout_alpha.addWidget(self.alpha)
        self.horizontalLayout_beta.addWidget(self.beta)
        self.horizontalLayout_phiB.addWidget(self.phiB)
        self.horizontalLayout_phiD.addWidget(self.phiD)
        self.horizontalLayout_lamdaB.addWidget(self.delta_lambdaB)
        self.horizontalLayout_lamdaD.addWidget(self.delta_lambdaD)
        self.horizontalLayout_rhof.addWidget(self.rho_f)
        self.horizontalLayout_rhosr.addWidget(self.rho_sr)
        self.verticalLayout_context.addWidget(self.context)
        # Define behaviours
        tmp = lambda elt: lambda: self._there_can_be_only_one(elt)
        for i, elt in enumerate(self.param_object_list):
            elt.pushButton.clicked.connect(tmp(elt))
            # param objects needs to be identified later.
            elt.id = self.param_flag_list[i]
        for elt in self.focus_object_list:
            elt.clicked.connect(self._auto_set_focus)
        self.groupBox_fluids.clicked.connect(self._fluidsChanged)
        self.pushButton_Clear.clicked.connect(self._clean_all)
        self.pushButton_Go.clicked.connect(self.click_compute)
        # Dictionnary (WrapperDict)
        self.dict = OrderedDict([
            ("context",       self.context),
            ("fluids",        self.fluids),
            ("focus",         self.focus),
            ("range",         self.range),
            ("alpha",         self.alpha),
            ("beta",          self.beta),
            ("phiB",          self.phiB),
            ("phiD",          self.phiD),
            ("delta_lambdaB", self.delta_lambdaB),
            ("delta_lambdaD", self.delta_lambdaD),
            ("rho_f",         self.rho_f),
            ("rho_sr",        self.rho_sr),
            ("results",       self.results)
        ])
        # Additional variables
        self.name_convert = {
            "alpha":         "α",
            "beta":          "β",
            "phiB":          "Φ<sub>B</sub>",
            "phiD":          "Φ<sub>D</sub>",
            "delta_lambdaB": "∆λ<sub>B</sub>",
            "delta_lambdaD": "∆λ<sub>D</sub>",
            "rho_f":         "ρ<sub>f</sub>",
            "rho_sr":        "ρ<sub>sr</sub>"
        }
        self._result_table_header = self._make_result_table_line(
            [self.name_convert[elt] for elt in self.param_flag_list])
        # Fill values with kwargs
        if kwargs:
            self.set_params(**kwargs)
        self.show()

    # Methods.

    def _set_results(self, x):
        self.textEdit_results.setText(x)
        scroll_bar = self.textEdit_results.verticalScrollBar()
        scroll_bar.setSliderPosition(scroll_bar.maximum())

    def _make_result_table_line(self, iterable, arg=""):
        td = "<td align='center', "+arg+">"
        dttd = "</td>" + td
        return "<tr>" + td + dttd.join(iterable) + "</td></tr>"

    def _there_can_be_only_one(self, elt):
        if elt.focus.value == "scalar":
            self.range.value = None
        else:
            self.range.value = elt.id
        for Obj in self.param_object_list:
            if Obj is not elt:
                Obj.set_scalar_visible(True)

    def set_focus(self, arg):
        for elt in self.focus_object_list:
            if elt.ID == arg:
                elt.setChecked(True)
        for elt in self.focus_object_list:
            self.__dict__[elt.ID].setEnabled(not elt.ID == arg)

    def _auto_set_focus(self):
        for elt in self.focus_object_list:
            if elt.isChecked():
                self.focus.value = elt.ID
                break
        for elt in self.focus_object_list:
            self.__dict__[elt.ID].setEnabled(not elt.ID == self.focus.value)

    def _fluidsChanged(self):
        self.fluids.value = self.groupBox_fluids.isChecked()

    def _clean_all(self):
        for elt in self.param_object_list:
            elt.clear()
        self.textEdit_results.clear()

    def click_compute(self):
        txt_result = "<p align='center'>"
        select = self.get_select()
        errors = self._check_arguments(select)
        if errors != "":
            txt_result += errors
        else:
            focus = self.focus.value
            range_id = self.range.value
            range_ = [None] if range_id is None else select[range_id]['value']
            result = []
            for x in range_:
                params = [select[flag]['value'] if flag != range_id else x
                          for flag in self.param_flag_list]
                self._load_params_in_compute_core(*params)
                result.append(self.compute_core.compute(focus))
            result = [(i, j, k) for i, (j, k) in zip(range_, result)]
            txt_result += self._format_results(select, result)
        txt_result += "<br/></p>"
        self.textEdit_results.append(txt_result)
        self.results.value += txt_result

    def _format_results(self, select, results):
        i = 1 if len(results) == 1 else 0
        txt = self._get_resume_params(select)
        txt += "<table width='" + str((5-i)*10) + "%'>"
        headers = ["●", "inverse", "normal"]
        txt += self._make_result_table_line(headers[i:],
                                            arg="style='color: blue'")
        for res in results:
            txt += self._make_result_table_line([str(round(elt, 4))
                                                 if elt is not None else "-"
                                                 for elt in res[i:]])
        txt += "</table>"
        return txt

    def _check_arguments(self, select):
        errors = ""
        message = " gets empty or invalid value<br/>"
        focus = self.focus.value
        for p_name in self.focus_flag_list:
            if select[p_name]["value"] is None and p_name != focus:
                errors += self.name_convert[p_name] + message
        if self.fluids.value:
            for p_name in self.fluids_flag_list:
                if select[p_name]["value"] is None:
                    errors += self.name_convert[p_name] + message
        return errors + ""

    def _get_resume_params(self, select):
        focus = self.focus.value
        context = " "+self.context.get_params()+" "
        n = 50 - len(context)
        title = "-"*n + context + "-"*n
        text = "<table width='100%'>"
        text += self._make_result_table_line([title], arg="colspan='8',"
                                             "style='color: blue'")
        text += self._result_table_header
        values = []
        for elt in self.param_flag_list:
            value = select[elt]['value']
            if elt == focus:
                value = "<span style='color: red'>⯅</span>"
            if value is None:
                value = "-"
            if select[elt]["type"] == "range":
                value = "<span style='color: blue'>●</span>"
            values.append(str(value))
        text += self._make_result_table_line(values)
        text += "</table>"
        return text

    def _load_params_in_compute_core(self, a, b, pB, pD, lB, lD, rf, rs):
        try:
            self.compute_core.alpha = a if a else 0.
            self.compute_core.beta = b if b else 0.
            self.compute_core.phiB = pB if pB else 0.
            self.compute_core.phiD = pD if pD else 0.
            flag = self.fluids.value
            self.compute_core.rho_f = rf if flag else 0.
            self.compute_core.rho_sr = rs if flag else 0.
            self.compute_core.delta_lambdaB = lB if flag else 0.
            self.compute_core.delta_lambdaD = lD if flag else 0.
        except TypeError:
            print("Wrong arguments")
        self.compute_core.context = self.context.get_params()


if __name__ == "__main__":
    import sys
    try:
        from eccw.shared.file_management import EccwFile
        eccwf = EccwFile(filename="../../../test/test.eccw")
        params = eccwf.values['calculator']

        app = QtGui.QApplication(sys.argv)
        myapp = CalculatorController(**params)
        sys.exit(app.exec_())
    finally:
        print("values :")
        graph_print(myapp.get_select())
