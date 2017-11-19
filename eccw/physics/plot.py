#!/usr/bin/env python3
# -*-coding:utf-8 -*

import numpy as np
from math import pi, tan, atan
# from matplotlib import patches, lines, rcParams
from matplotlib import pyplot as plt
import matplotlib.patheffects as pe

from eccw.physics.compute import EccwCompute
# from eccw.shared.tools import Min, Max


class EccwPlot(EccwCompute):

    def __init__(self, **kwargs):
        EccwCompute.__init__(self, **kwargs)
        self.legend = None
        self.figure = plt.figure("ECCW", figsize=(8, 6))
        self.axe = self.figure.gca()
        self.axe.set_xlabel(r"Décollement angle $\beta$ [deg]", fontsize=12)
        self.axe.set_ylabel(r"Critical slope $\alpha_c$ [deg]", fontsize=12)
        self.axe.grid()
        if self.legend:
            self.add_legend()

    def _get_alphamax(self):
        return atan((1 - self._lambdaB) / (1 - self._density_ratio)
                    * tan(self._phiB))

    def _store_if_valid(self, beta, alpha, betas, alphas):
        if self._is_valid_taper(alpha, beta):
            betas.append(self._r2d(beta))
            alphas.append(self._r2d(alpha))

    def _compute_betas_alphas(self, alphas):
        """Return nested lists of valid values of beta, alpha"""
        betas_ul, betas_ur, betas_dr, betas_dl = [], [], [], []
        alphas_ul, alphas_ur, alphas_dr, alphas_dl = [], [], [], []
        for alpha in alphas:
            lambdaB_D2 = self._convert_lambda(alpha, self._lambdaB)
            lambdaD_D2 = self._convert_lambda(alpha, self._lambdaD)
            alpha_prime = self._convert_alpha(alpha, lambdaB_D2)
            # Weird if statement because asin in PSI_D is your ennemy !
            if -self._phiB <= alpha_prime <= self._phiB:
                psi0_1, psi0_2 = self._PSI_0(alpha_prime, self._phiB)
                psiD_11, psiD_12 = self._PSI_D(psi0_1, self._phiB, self._phiD,
                                               lambdaB_D2, lambdaD_D2)
                psiD_21, psiD_22 = self._PSI_D(psi0_2, self._phiB, self._phiD,
                                               lambdaB_D2, lambdaD_D2)
                beta_dl = psiD_11 - psi0_1 - alpha
                beta_ur = psiD_12 - psi0_1 - alpha
                beta_dr = psiD_21 - psi0_2 - alpha + pi  # Don't ask why +pi
                beta_ul = psiD_22 - psi0_2 - alpha
                # beta, alpha, betas_alphas, i
                self._store_if_valid(beta_dl, alpha, betas_dl, alphas_dl)
                self._store_if_valid(beta_ur, alpha, betas_ur, alphas_ur)
                self._store_if_valid(beta_dr, alpha, betas_dr, alphas_dr)
                self._store_if_valid(beta_ul, alpha, betas_ul, alphas_ul)
        betas_up = betas_ul + betas_ur[::-1]
        alphas_up = alphas_ul + alphas_ur[::-1]
        betas_down = betas_dl[::-1] + betas_dr
        alphas_down = alphas_dl[::-1] + alphas_dr
        return betas_up, alphas_up, betas_down, alphas_down

    def add_title(self, title=''):
        self.axe.set_title(title, fontsize=16)

    def add_legend(self):
        self.legend = plt.legend(loc='best', fontsize='10')
        self.legend.draggable()

    def add_curve(self, **kwargs):
        """Plot complete solution plus a given solution.
        Use directe solution f(alpha) = beta.
        """
        split = kwargs.get('split', False)
        alphamax = self._get_alphamax()
        alphas = np.arange(-alphamax, alphamax, alphamax * 2 / 1e4)
        bs_up, as_up, bs_dw, as_dw = self._compute_betas_alphas(alphas)
        if split:
            label_inv = kwargs.get('label_norm', '')
            label_norm = kwargs.get('label_inv', '')
            thickness_inv = kwargs.get('thickness_inv', 2)
            thickness_norm = kwargs.get('thickness_norm', 2)
            style_inv = kwargs.get('style_inv', '-')
            style_norm = kwargs.get('style_norm', '-')
            color_inv = kwargs.get('color_inv', 'k')
            color_norm = kwargs.get('color_norm', 'k')
            # Upper line is normal mecanism.
            path_effects = [pe.Stroke(linewidth=thickness_norm+0.5,
                            foreground='k'), pe.Normal()]
            plt.plot(bs_up, as_up, c=color_norm, label=label_norm,
                     lw=thickness_norm, ls=style_norm, figure=self.figure,
                     path_effects=path_effects)
            # Bottom line is inverse mecanism.
            path_effects = [pe.Stroke(linewidth=thickness_inv+0.5,
                            foreground='k'), pe.Normal()]
            plt.plot(bs_dw, as_dw, c=color_inv, label=label_inv,
                     lw=thickness_inv, ls=style_inv, figure=self.figure,
                     path_effects=path_effects)
        else:
            label = kwargs.get('label', '')
            thickness = kwargs.get('thickness', 2)
            style = kwargs.get('style', '-')
            color = kwargs.get('color', 'k')
            betas, alphas = bs_up + bs_dw[::-1], as_up + as_dw[::-1]
            path_effects = [pe.Stroke(linewidth=thickness+0.5,
                            foreground='k'), pe.Normal()]
            plt.plot(betas, alphas, c=color, label=label, lw=thickness,
                     ls=style, path_effects=path_effects, figure=self.figure)

    def _test_value(self, value, other, values, others, v_min, v_max):
        if value is not None:
            if v_min < value < v_max:
                values.append(value)
                others.append(other)

    def add_point(self, beta=None, alpha=None, **kwargs):
        label = kwargs.get('label', '')
        size = kwargs.get('size', 5)
        style = kwargs.get('style', 'o')
        color = kwargs.get('color', 'k')
        path_effects = [pe.PathPatchEffect(edgecolor='k', facecolor=color,
                        linewidth=0.5)]
        betas, alphas = [], []
        if beta is not None:
            a_min = kwargs.get('alpha_min', float('-inf'))
            a_max = kwargs.get('alpha_max', float('inf'))
            if a_min == float('-inf') and a_max == float('inf'):
                plt.axvline(beta, lw=1.5, c='gray', figure=self.figure)
            self.beta = beta
            alpha1, alpha2 = self.compute_alpha()
            self._test_value(alpha1, beta, alphas, betas, a_min, a_max)
            self._test_value(alpha2, beta, alphas, betas, a_min, a_max)
        if alpha is not None:
            b_min = kwargs.get('beta_min', float('-inf'))
            b_max = kwargs.get('beta_max', float('inf'))
            if b_min == float('-inf') and b_max == float('inf'):
                plt.axhline(alpha, lw=1, c='gray', figure=self.figure)
            self.alpha = alpha
            beta1, beta2 = self.compute_beta()
            self._test_value(beta1, alpha, betas, alphas, b_min, b_max)
            self._test_value(beta2, alpha, betas, alphas, b_min, b_max)
        plt.plot(betas, alphas, ls='', marker=style, ms=size, label=label,
                 path_effects=path_effects, figure=self.figure)

    def add_refpoint(self, beta, alpha, **kwargs):
        label = kwargs.get('label', '')
        size = kwargs.get('size', 5)
        style = kwargs.get('style', 'o')
        color = kwargs.get('color', 'k')
        path_effects = [pe.PathPatchEffect(edgecolor='k', facecolor=color,
                                           linewidth=0.5)]
        plt.plot(beta, alpha, ls='', marker=style, ms=size, label=label,
                 path_effects=path_effects, figure=self.figure)

    def show(self):
        plt.show(self.figure)


if __name__ == "__main__":

    foo = EccwPlot(phiB=30, phiD=10, context="c")
    foo.add_curve(color=(0.1, 1, 0.1, 1), label="compression", thickness=3)
    foo.add_point(beta=20, style='s')  # alpha=[-9.7921, 29.5148]
    foo.add_point(alpha=10, beta_min=50, style='^', size=8)
    # foo.show_params()
    foo.context = 'e'
    foo.add_curve(color_inv=(1, 0, 0, 1), label_inv="extension inverse",
                  color_norm=(0, 0, 1, 1), label_norm="extension normal",
                  split=True)
    foo.add_point(alpha=-8, style='o', color='c')  # , beta_max=60)
    foo.title = "my self.title"
    foo.add_title("my title")
    foo.add_refpoint(0, 0, color="w", label='star', style='*', size=10)
    foo.add_refpoint(2.5, -1.5)
    foo.add_legend()
    foo.show()
