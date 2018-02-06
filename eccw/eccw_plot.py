#!/usr/bin/env python3
# -*-coding:utf-8 -*

"""
Elements dedicated to plot physics.
"""


import numpy as np
from math import pi, tan, atan, cos, sin, sqrt, asin
from matplotlib import pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.offsetbox import DrawingArea, AnnotationBbox
from matplotlib import patches, lines
import warnings


from eccw import EccwCompute
from eccw.shared import r2d, imin, imax


warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")


class EccwPlot(EccwCompute):
    """
    Plot critical enveloppes of the critical coulomb wedge.
    """
    _point_center = (0., 0.)
    _point_top = (0., 0.)
    _point_bottom = (0., 0.)
    _point_left = (0., 0.)
    _point_right = (0., 0.)
    _sketch_box_width = 0.
    _sketch_box_height = 0.
    _padding = 10.
    _sketch_size_factor = 1.
    _sketch_surface = 5000.
    _fault_gap = 1.
    _arrow_L = 1.
    _arrow_gap = 1.
    _arrow_head_width = 1.
    _arrow_head_length = 1.

    def __init__(self, **kwargs):
        EccwCompute.__init__(self, **kwargs)
        self.sketch_size_factor = kwargs.get('sketch_size_factor', 1.)
        self.legend = None
        self.init_figure()

    @property
    def sketch_size_factor(self):
        return self._sketch_size_factor

    @sketch_size_factor.setter
    def sketch_size_factor(self, value):
        self._sketch_size_factor = float(value)
        # Surface of sketeched prism :
        # arbitrary set, allows a cst looking.
        self._sketch_surface = 5000. * self._sketch_size_factor
        self._fault_gap = (self._sketch_surface / sqrt(self._sketch_surface)
                           / 4.)
        self._arrow_L = self._fault_gap * 2. / 3.
        self._arrow_gap = self._arrow_L / 2.
        self._arrow_head_width = self._arrow_L / 3.
        self._arrow_head_length = self._arrow_L / 2.

    # Private methods

    def _get_alphamax(self):
        return atan((1 - self._lambdaB) / (1 - self._density_ratio)
                    * tan(self._phiB))

    def _store_if_valid(self, beta, alpha, betas, alphas):
        if self._is_valid_taper(alpha, beta):
            betas.append(r2d(beta))
            alphas.append(r2d(alpha))

    def _compute_betas_alphas(self, alphas):
        """Return nested lists of valid values of beta, alpha"""
        # self._check_params()
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

    def _get_centroid(self, X, Y):
        """Compute the centroid of a polygon.
        Fisrt and last points are differents.
        """
        Ss, Cxs, Cys = [], [], []
        # Explore Polygon by element triangles.
        for i in range(1, len(X)-2):
            # Surface of triangle times 2.
            Ss.append((X[i] - X[0]) * (Y[i+1] - Y[0])
                      - (X[i+1] - X[0]) * (Y[i] - Y[0]))
            # Centroid of triangle.
            Cxs.append((X[0] + X[i] + X[i+1]) / 3.)
            Cys.append((Y[0] + Y[i] + Y[i+1]) / 3.)
        Ss.append((X[-2] - X[0]) * (Y[-1] - Y[0])
                  - (X[-1] - X[0]) * (Y[-2] - Y[0]))
        Cxs.append((X[0] + X[-2] + X[-1]) / 3.)
        Cys.append((Y[0] + Y[-2] + Y[-1]) / 3.)
        A = sum(Ss)
        if abs(A) < self._numtol:
            raise Exception("!!!ERROR : polygon gets surface lower than tol.")
        # Centroid is weighed average of element triangle centroids.
        x = sum([Cx * S for Cx, S in zip(Cxs, Ss)]) / A
        y = sum([Cy * S for Cy, S in zip(Cys, Ss)]) / A
        return x, y

    def _test_value(self, value, other, values, others, v_min, v_max):
        if value is not None:
            if v_min < value < v_max:
                values.append(value)
                others.append(other)

    def _draw_arrow(self, angle, x, y, solution, gamma=True):
        xL, yL = self._arrow_L * cos(angle), self._arrow_L * sin(angle)
        dum_l = sqrt(self._arrow_gap ** 2. + self._arrow_L ** 2.) / 2.
        dum_angle = atan(self._arrow_gap / self._arrow_L)
        if solution is "B":
            dx = dum_l * cos(angle - dum_angle)
            dy = dum_l * sin(angle - dum_angle)
            way = "right" if gamma else "left"
        else:
            dx = dum_l * cos(angle + dum_angle)
            dy = dum_l * sin(angle + dum_angle)
            way = "left" if gamma else "right"
        if gamma:
            p1 = patches.FancyArrow(x - dx, y - dy, xL, yL, lw=1,
                                    head_width=self._arrow_head_width,
                                    head_length=self._arrow_head_length,
                                    fc='k', ec='k', shape=way,
                                    length_includes_head=True)
            p2 = patches.FancyArrow(x + dx, y + dy, -xL, -yL, lw=1,
                                    head_width=self._arrow_head_width,
                                    head_length=self._arrow_head_length,
                                    fc='k', ec='k', shape=way,
                                    length_includes_head=True)
        else:
            p1 = patches.FancyArrow(x - dx, y + dy, xL, -yL, lw=1,
                                    head_width=self._arrow_head_width,
                                    head_length=self._arrow_head_length,
                                    fc='k', ec='k', shape=way,
                                    length_includes_head=True)
            p2 = patches.FancyArrow(x + dx, y - dy, -xL, yL, lw=1,
                                    head_width=self._arrow_head_width,
                                    head_length=self._arrow_head_length,
                                    fc='k', ec='k', shape=way,
                                    length_includes_head=True)
        self.drawing_aera.add_artist(p1)
        self.drawing_aera.add_artist(p2)

    def _draw_faults(self, a_f, x_f, y_f, xgap_f, ygap_f, ifirst,
                     incr, col="gray"):
        xt, yt = self._prism_tip
        i = ifirst
        while 1:
            i += incr
            Ni = [x_f - i * xgap_f, y_f - i * ygap_f]
            b_f = Ni[1] - a_f * Ni[0]
            X, Y = [], []
            # Fault intersection with base
            x = (self._b_basal - b_f) / (a_f - self._a_basal)
            y = a_f * x + b_f
            self._is_node_in_box(x, y, X, Y)
            # Fault intersection with topo
            x = (self._b_topo - b_f) / (a_f - self._a_topo)
            y = a_f * x + b_f
            self._is_node_in_box(x, y, X, Y)
            # Fault intersection with rear arc
            A = 1 + a_f ** 2.
            B = 2. * (a_f * (b_f - yt) - xt)
            C = xt ** 2. + (b_f - yt) ** 2. - self._L ** 2.
            D = B ** 2. - 4 * A * C
            if D >= 0.:
                x = (-B - sqrt(D)) / 2. / A
                y = a_f * x + b_f
                self._is_node_in_box(x, y, X, Y)
                x = (-B + sqrt(D)) / 2. / A
                y = a_f * x + b_f
                self._is_node_in_box(x, y, X, Y)
            if len(X) < 2:
                break
            p = lines.Line2D(X, Y, lw=1, c=col)
            self.drawing_aera.add_artist(p)

    def _get_gamma_A(self):
        return (pi / 2. + self._phiB - 2. * self._alpha + self._alpha_prime
                + asin(sin(self._alpha_prime) / sin(self._phiB))) / 2.

    def _get_theta_A(self):
        return (pi / 2. + self._phiB + 2. * self._alpha - self._alpha_prime
                - asin(sin(self._alpha_prime) / sin(self._phiB))) / 2.

    def _get_gamma_B(self):
        return (pi / 2. - self._phiB - 2. * self._alpha + self._alpha_prime
                - asin(sin(self._alpha_prime) / sin(self._phiB))) / 2.

    def _get_theta_B(self):
        return (pi / 2. - self._phiB + 2. * self._alpha - self._alpha_prime
                + asin(sin(self._alpha_prime) / sin(self._phiB))) / 2.

    def _is_node_in_box(self, x, y, X, Y):
        foo = self._padding - self._numtol
        bar = self._padding + self._numtol
        if foo <= x <= self._sketch_box_width - bar:
            if foo <= y <= self._sketch_box_height - bar:
                X.append(x)
                Y.append(y)

    def _get_curve_settings(self, **kwargs):
        return {
            'c':      kwargs.get('color', 'k'),
            'lw':     kwargs.get('thickness', 2),
            'ls':     kwargs.get('style', '-'),
            'figure': self.figure
            }

    # Public methods

    def init_figure(self):
        self.figure = plt.figure("ECCW", figsize=(8, 6))
        self.axe = self.figure.gca()
        self.axe.set_xlabel(r"Décollement angle $\beta$ [deg]", fontsize=12)
        self.axe.set_ylabel(r"Critical slope $\alpha_c$ [deg]", fontsize=12)
        self.axe.grid(True)

    def reset_figure(self):
#        plt.close('all')
        self.init_figure()

    def show(self, block=True):
        plt.show()
#        plt.show(block=block)

    def add_title(self, title=''):
        self.axe.set_title(title, fontsize=16)

    def add_legend(self):
        self.legend = plt.legend(loc='best', fontsize='10')
        if self.legend is not None:
            self.legend.draggable()

    def add_refpoint(self, *args, **kwargs):
        try:
            beta = kwargs['beta']
            alpha = kwargs['alpha']
        except KeyError:
            raise KeyError("EccwPlot.add_refpoint method awaits at least the "
                           "following key word arguments: 'beta' and 'alpha'")
        label = kwargs.get('label', '')
        size = kwargs.get('size', 5)
        style = kwargs.get('style', 'o')
        color = kwargs.get('color', 'k')
        path_effects = [pe.PathPatchEffect(edgecolor='k', facecolor=color,
                                           linewidth=0.5)]
        plt.plot(beta, alpha, ls='', marker=style, ms=size, label=label,
                 path_effects=path_effects, figure=self.figure)

    def add_curve(self, **kwargs):
        """Plot complete solution plus a given solution.
        Use directe solution f(alpha) = beta.
        """
        inverse = kwargs.get('inverse', dict())
        normal = kwargs.get('normal', dict())
        label = kwargs.get('label', '')
        alphamax = self._get_alphamax()
        alphas = np.arange(-alphamax, alphamax, alphamax * 2 / 1e4)
        bs_up, as_up, bs_dw, as_dw = self._compute_betas_alphas(alphas)
        betas, alphas = bs_up + bs_dw[::-1], as_up + as_dw[::-1]
        if normal or inverse:
            n_settings = self._get_curve_settings(**normal)
            i_settings = self._get_curve_settings(**inverse)
            l_norm, l_inv = label + " normal", label + " inverse"
            path_effects = [pe.Stroke(linewidth=n_settings['lw']+0.5,
                            foreground='k'), pe.Normal()]
            plt.plot(bs_up, as_up, label=l_norm, path_effects=path_effects,
                     **n_settings)
            # Bottom line is inverse mecanism.
            path_effects = [pe.Stroke(linewidth=i_settings['lw']+0.5,
                            foreground='k'), pe.Normal()]
            plt.plot(bs_dw, as_dw, label=l_inv, path_effects=path_effects,
                     **i_settings)
        else:
            settings = self._get_curve_settings(**kwargs)
            path_effects = [pe.Stroke(linewidth=settings['lw']+0.5,
                            foreground='k'), pe.Normal()]
            plt.plot(betas, alphas, label=label, path_effects=path_effects,
                     **settings)

        # Get bounding and central points (used by sketch).
        b, a = self._get_centroid(betas, alphas)
        self._point_center = (b, a)
        i = imax(as_up)
        self._point_top = (bs_up[i], r2d(alphamax))
        i = imin(as_dw)
        self._point_bottom = (bs_dw[i], -r2d(alphamax))
        self._point_left = (bs_up[0], as_up[0])
        self._point_right = (bs_up[-1], as_up[-1])

    def add_point(self, **kwargs):
        beta = kwargs.get('beta', None)
        alpha = kwargs.get('alpha', None)
        sketch = kwargs.get('sketch', False)
        # line = kwargs.get('line', True)
        settings = {
            'linestyle':    '',
            'marker':       kwargs.get('style', 'o'),
            'markersize':   kwargs.get('size', 5),
            'label':        kwargs.get('label', ''),
            'path_effects': [
                pe.PathPatchEffect(
                    edgecolor='k',
                    facecolor=kwargs.get('color', 'k'),
                    linewidth=0.5
                    )
                ],
            'figure':       self.figure
            }
        betas, alphas = [], []
        pinf, minf = float('inf'), float('-inf')
        if beta is not None:
            a_min = kwargs.get('alpha_min', minf)
            a_max = kwargs.get('alpha_max', pinf)
            # if a_min == minf and a_max == pinf and line:
            #     plt.axvline(beta, lw=1.5, c='gray', figure=self.figure)
            self.beta = beta
            alpha1, alpha2 = self.compute_alpha()
            self._test_value(alpha1, beta, alphas, betas, a_min, a_max)
            self._test_value(alpha2, beta, alphas, betas, a_min, a_max)
            if sketch is True:
                for alpha in alphas:
                    self.alpha = alpha
                    self.add_sketch(**kwargs)
        elif alpha is not None:
            b_min = kwargs.get('beta_min', minf)
            b_max = kwargs.get('beta_max', pinf)
            # if b_min == minf and b_max == pinf and line:
            #     plt.axhline(alpha, lw=1, c='gray', figure=self.figure)
            self.alpha = alpha
            beta1, beta2 = self.compute_beta_old()
            self._test_value(beta1, alpha, betas, alphas, b_min, b_max)
            self._test_value(beta2, alpha, betas, alphas, b_min, b_max)
            if sketch is True:
                for beta in betas:
                    self.beta = beta
                    self.add_sketch(**kwargs)
        plt.plot(betas, alphas, **settings)

    def add_line(self, **kwargs):
        beta = kwargs.get('beta', None)
        alpha = kwargs.get('alpha', None)
        setting = {
            'ls':     '-',
            'lw':     2.,
            'c':      (0.8, 0.8, 0.8, 1),
            'zorder': -10,
            'figure': self.figure
            }
        xmin, xmax = self.axe.get_xlim()
        ymin, ymax = self.axe.get_ylim()
        pinf, minf = float('inf'), float('-inf')
        if beta is not None:
            a_min = kwargs.get('alpha_min', minf)
            a_max = kwargs.get('alpha_max', pinf)
            if a_min == minf and a_max == pinf:
                plt.axvline(beta, **setting)
            elif a_min == minf:
                x = (a_max - xmin) / (xmax - xmin) - 0.1
                plt.axvline(beta, xmax=x, **setting)
                plt.plot((beta, beta), (xmin, a_max), **setting)
            elif a_max == pinf:
                x = (a_min - xmin) / (xmax - xmin) + 0.1
                plt.axvline(beta, xmin=x, **setting)
                plt.plot((beta, beta), (a_min, xmax), **setting)
            else:
                plt.plot((beta, beta), (a_min, a_max), **setting)
        if alpha is not None:
            b_min = kwargs.get('beta_min', minf)
            b_max = kwargs.get('beta_max', pinf)
            if b_min == minf and b_max == pinf:
                plt.axhline(alpha, **setting)
            elif b_min == minf:
                x = (b_max - xmin) / (xmax - xmin) - 0.1
                plt.axhline(alpha, xmax=x, **setting)
                plt.plot((xmin, b_max), (alpha, alpha), **setting)
            elif b_max == pinf:
                x = (b_min - xmin) / (xmax - xmin) + 0.1
                plt.axhline(alpha, xmin=x, **setting)
                plt.plot((b_min, xmax), (alpha, alpha), **setting)
            else:
                plt.plot((b_min, b_max), (alpha, alpha), **setting)

    def add_sketch(self, **kwargs):
        """Draw section sketch at current value [beta, alpha].
        Draw also:
        * potential preferential fault network;
        * slip directions on fault network.
        """
        self.sketch_size_factor = kwargs.get('sketch_size_factor', 1.)
        # Renaming is cheapper than multiple access.
        alpha, beta = self._alpha, self._beta
        a_deg, b_deg = r2d(alpha), r2d(beta)
        padding = self._padding
        # Surface of prism : arbitrary set, allows a cst looking.
        # Box distance from enveloppe.
        box_dist_from_curve = (self._point_top[1]
                               - self._point_bottom[1]) / 10.
        try:
            L = sqrt(self._sketch_surface / sin((alpha + beta) / 2.)
                     * cos((alpha + beta) / 2.))
        except ZeroDivisionError:
            # alpha + beta == 0. means there is no prism !
            return
        self._L = L
        # Init sketching aera ans draw background of prism.
        # Prism is a basal and a topo line, so discribed by 3 points.
        if alpha < 0.:
            x1 = (padding + 2. * L * sin((alpha + beta) / 2.)
                  * sin((beta - alpha)/2.))
            y1 = padding
        elif beta < 0.:
            x1, y1 = padding, padding + L * sin(-beta)
        else:
            x1, y1 = padding + L * (1. - cos(beta)), padding
        x2, y2 = x1 + L * cos(beta), y1 + L * sin(beta)
        x3, y3 = x2 - L * cos(alpha), y2 + L * sin(alpha)
        self._prism_tip = (x2, y2)
        # Prism is also discribed by two lines.
        # Slope of vectors [1-2] and [2-3]
        self._a_basal, self._a_topo = tan(beta), -tan(alpha)
        # Initial ordinates
        self._b_basal = y2 - self._a_basal * x2
        self._b_topo = y2 - self._a_topo * x2
        self._sketch_box_width = x2 + padding
        self._sketch_box_height = max(y3, y2) - min(y1, y2) + 2 * padding
        # Content of annotationbox
        self.drawing_aera = DrawingArea(self._sketch_box_width,
                                        self._sketch_box_height, 0., 0.)
        # Fill the prism
        XY = [[x1, y1], [x2, y2]]
        for angle in np.arange(alpha, -beta, -(alpha + beta) / 1.e2):
            XY.append([x2 - L * cos(angle), y2 + L * sin(angle)])
        p = patches.Polygon(XY, edgecolor="none", facecolor="w")
        self.drawing_aera.add_artist(p)
        # Identify wich part of critical enveloppe is concerned.
        slope = abs(atan((self._point_center[1] - a_deg)
                         / (self._point_center[0] - b_deg)))
        dist_from_curve_b = box_dist_from_curve * cos(slope)
        dist_from_curve_a = box_dist_from_curve * sin(slope)
        alpha1, alpha2 = self.compute_alpha(deg=False)
        a_mid = (alpha1 + (alpha2 - alpha1) / 2.)
        if alpha <= a_mid:  # bottom part -> inverse faults
            if b_deg < self._point_bottom[0]:  # bottom left quadrant
                quadrant, solution = "BL", "B"
            else:  # bottom right quadrant
                quadrant, solution = "BR", "A"
        else:  # upper part -> normal faults
            if b_deg < self._point_top[0]:  # Top left quadrant
                quadrant, solution = "TL", "A"
            else:  # Top right quadrant
                quadrant, solution = "TR", "B"
        if solution == "A":
            g = self._get_gamma_A()
            t = self._get_theta_A()
        else:
            g = self._get_gamma_B()
            t = self._get_theta_B()
        if quadrant == "TL":
            box_alignment, xshift, yshift = (1., 0.), -1., 1.
        elif quadrant == "TR":
            box_alignment, xshift, yshift = (0., 0.), 1., 1.
        elif quadrant == "BL":
            box_alignment, xshift, yshift = (1., 1.), -1., -1.
        elif quadrant == "BR":
            box_alignment, xshift, yshift = (0., 1.), 1., -1.

        # Fault network.
        xgap = self._fault_gap * cos((beta - alpha)/2.)
        ygap = self._fault_gap * sin((beta - alpha)/2.)
        L_A, L_B, angle = L / 3., L * 2. / 3., alpha - (alpha + beta) / 2.
        # Gamma oriented faults
        L_g = L_A if quadrant in ["TL", "BL"] else L_B
        x_g, y_g = x2 - L_g * cos(angle), y2 + L_g * sin(angle)
        xgap_g = xgap / sin(g - (beta - alpha)/2.)
        ygap_g = ygap / sin(g - (beta - alpha)/2.)
        a_g = tan(g)
        self._draw_faults(a_g, x_g, y_g, xgap_g, ygap_g, -1, 1)
        self._draw_faults(a_g, x_g, y_g, xgap_g, ygap_g, 0, -1)
        # Theta oriented faults
        L_t = L_B if quadrant in ["TL", "BL"] else L_A
        x_t, y_t = x2 - L_t * cos(angle), y2 + L_t * sin(angle)
        xgap_t = xgap / sin(t + (beta - alpha)/2.)
        ygap_t = ygap / sin(t + (beta - alpha)/2.)
        a_t = -tan(t)  # Fault slope theta
        self._draw_faults(a_t, x_t, y_t, xgap_t, ygap_t, -1, 1)
        self._draw_faults(a_t, x_t, y_t, xgap_t, ygap_t, 0, -1)

        # Prism limits.
        # Drawed above faults to mask faults tips.
        p = lines.Line2D([x1, x2, x3], [y1, y2, y3], lw=2, color="gray")
        self.drawing_aera.add_artist(p)

        # Arrows.
        # Gamma oriented inverse arrows.
        self._draw_arrow(g, x_g, y_g, solution, gamma=True)
        # Theta oriented inverse arrows.
        self._draw_arrow(t, x_t, y_t, solution, gamma=False)
        # arrows base
        x, y = x1 + L * cos(beta) / 2., y1 + L * sin(beta) / 2.
        if self.context == "Compression":
            solution = "B"
        else:
            solution = "A"
        self._draw_arrow(beta, x, y, solution, gamma=True)

        # Set and display annotation box.
        ab = AnnotationBbox(
                self.drawing_aera,
                [b_deg, a_deg],
                xybox=(b_deg + xshift * dist_from_curve_b, a_deg + yshift
                       * dist_from_curve_a),
                xycoords='data',
                boxcoords=("data", "data"),
                box_alignment=box_alignment,
                bboxprops=dict(
                    boxstyle="round",
                    fc=(0.9, 0.9, 0.9),
                    ec="none"
                    ),
                arrowprops=dict(
                    arrowstyle="wedge,tail_width=2.",
                    fc=(0.9, 0.9, 0.9),
                    ec=(0.8, 0.8, 0.8),
                    patchA=None,
                    relpos=(0.5, 0.5),
                    )
                )
        self.axe.add_artist(ab).draggable()


if __name__ == "__main__":

    foo = EccwPlot(phiB=30, phiD=10, context="c")
    foo.add_point(style='', label=r"$\bf{ghost}$")
    foo.add_curve(color=(0.1, 1, 0.1, 1), label="compression", thickness=3)
    foo.add_point(beta=20, style='s', sketch=True)  # alpha=[-9.7921, 29.5148]
    foo.add_point(alpha=10, style='^', size=8, sketch=True, beta_min=50, color='r')
    # foo.show_params()

    foo.context = 'e'
    # foo.add_curve(color_inv=(1, 0, 0, 1), label_inv="extension inverse",
    #               color_norm=(0, 0, 1, 1), label_norm="extension normal",
    #               split=True)
    foo.add_curve(
        inverse={'color': (1, 0, 0, 1), 'label': "extension inverse"},
        normal={'color': (0, 0, 1, 1), 'label': "extension normal"}
        )
    foo.add_line(alpha=20, beta_max=20)
    foo.add_point(alpha=-8, style='o', color='y')  # , beta_max=60)
    foo.title = "my self.title"
    foo.add_title("my title")
    foo.add_refpoint(beta=0, alpha=0, color="w", label='star', style='*',
                     size=10)
    foo.add_refpoint(beta=2.5, alpha=-1.5)
    foo.add_legend()
    foo.show(block=True)
