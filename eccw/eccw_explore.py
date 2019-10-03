#!/usr/bin/env python3
# -*-coding:utf-8 -*

"""
Elements dedicated to explore solutions.
"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import ticker, cm
from math import pi, degrees, radians, inf, nan
from itertools import product

# import multiprocessing   # fails at pickling the class
# import concurrent.futures   # fail at pickling the class
# import pathos   # <<<<< solution !


from eccw import EccwCompute


class EccwExplore(EccwCompute):

    ## compute elements #######################################################

    def _matrix_of_function_to_root(self, X, PSID, PSI0, runtime_var) -> np.array:
        """Compute a 3D matrix of convergence results.

        The _function_to_root method takes 3 parameters which are
        X in {alpha, phiD, phiB}, psiD and psi0, and returns a triplet.
        The best result is supposed to be close - or equal - to zero.
        
        This method feed _function_to_root with a grid of parameters, then normalise
        the result by using mean(abs(returned_triplet)).

        This method returns a numpy 3D array.
        """
        MAP = map(
            lambda xyz: np.mean(np.abs(self._function_to_root(xyz, runtime_var))),
            product(X, PSID, PSI0),
        )
        return np.reshape(tuple(MAP), (len(X), len(PSID), -1))

    def _solve_for_map_solution(self, X, runtime_var):
        # self._set_at_runtime = self._runtime_alpha
        _ = self._solve(X, runtime_var)
        alpha_path, psiD_path, psi0_path = zip(*self.path)
        alpha_path = [degrees(x) for x in alpha_path]
        psiD_path = [degrees(x) for x in psiD_path]
        psi0_path = [degrees(x) for x in psi0_path]
        return (alpha_path, psiD_path, psi0_path), self.iter_conv

    ## display elements #######################################################

    def _subplot_labels(self, xlabel, ylabel, title, axe):
        axe.set_xlabel(xlabel)
        axe.set_ylabel(ylabel)
        axe.set_title(title)

    def _subplot_conv_map(self, X, Y, MAP, axe):
        # axe.set_aspect('equal', adjustable='box')
        levels = [1e-3, 2e-3, 5e-3, 1e-2, 2e-2, 5e-2, 1e-1, 2e-1, 5e-1, 1e0]
        h = axe.contourf(
            X, Y, MAP, cmap="bone", locator=ticker.LogLocator(), levels=levels
        )
        # plt.colorbar(h1, ax=axe)
        return h

    def _subplot_contour_map(self, X, Y, MAP, axe):
        h = axe.contour(
            X, Y, MAP, colors="k", levels=list(range(-30, 35, 5)), linewidths=1
        )
        axe.clabel(ha, inline=1, fontsize=10)
        return h

    def _subplot_conv_path(self, pathX1, pathY1, pathX2, pathY2, axe):
        axe.plot(pathX1, pathY1, "-or")
        axe.plot(pathX1[-1], pathY1[-1], "ob")
        axe.plot(pathX2, pathY2, "-oy")
        axe.plot(pathX2[-1], pathY2[-1], "ob")

    def draw_map_solution(self, runtime_var, X1, X2, N=32, vmin=-pi / 2, vmax=pi / 2):
        """Draw a convergence map for the 3 parameters X, psiD and psi0.
        X can be {alpha, phiD, phiB}.
        Sélection of X is made through runtime_var parameter.
        X1 and X2 are 3 elements lists containig 2 sets of initial values.
        """
        parser = {
            self._runtime_alpha: "$\\alpha$",
            self._runtime_phiB: "$\phi_B$",
            self._runtime_phiD: "$\phi_D$",
        }
        var_label = parser[runtime_var]
        #### SOLVE ####
        try:
            paths1, count1 = self._solve_for_map_solution(X1, runtime_var)
        except RuntimeError:
            paths1, count1 = [(nan, nan)] * 4, None
        try:
            paths2, count2 = self._solve_for_map_solution(X2, runtime_var)
        except RuntimeError:
            paths2, count2 = [(nan, nan)] * 4, None

        VARs = np.linspace(vmin, vmax, N)
        PSIDs = np.linspace(vmin, vmax, N)
        PSI0s = np.linspace(vmin, vmax, N)
        MATRIX = self._matrix_of_function_to_root(VARs, PSIDs, PSI0s, runtime_var)

        ### PLOT ###
        VARs = [degrees(x) for x in VARs]
        PSIDs = [degrees(x) for x in PSIDs]
        PSI0s = [degrees(x) for x in PSI0s]

        fig = plt.figure("convergence maps", figsize=(10, 9))
        title = f"""
        Convergence maps for parameters
        $\\alpha$={round(self.alpha,2)}
        $\\beta$={round(self.beta,2)}
        $\phi_D$={round(self.phiD,2)}
        $\phi_B$={round(self.phiB,2)} 
        context: {self.context}
        """

        #      0   1
        #   ┌────┬────┐
        # 0 │ax00│ax01│
        #   ├────┼────┤   2x2 subplot grid
        # 1 │ax10│ax11│
        #   └────┴────┘
        ax00 = plt.subplot2grid((2, 2), (0, 0))
        ax10 = plt.subplot2grid((2, 2), (1, 0), sharex=ax00)
        ax01 = plt.subplot2grid((2, 2), (0, 1), sharey=ax00)
        ax11 = plt.subplot2grid((2, 2), (1, 1), sharex=ax01, sharey=ax10)

        PMAP = np.transpose(np.min(MATRIX, axis=0))
        ax11.xaxis.set_ticks_position("both")
        ax11.yaxis.tick_right()
        ax11.yaxis.set_ticks_position("both")
        ax11.yaxis.set_label_position("right")
        self._subplot_labels("$\psi_D$", "$\psi_0$", "", ax11)
        h1 = self._subplot_conv_map(PSIDs, PSI0s, PMAP, ax11)
        self._subplot_conv_path(paths1[1], paths1[2], paths2[1], paths2[2], ax11)
        ax11.grid()

        PMAP = np.transpose(np.min(MATRIX, axis=1))
        ax10.yaxis.set_ticks_position("both")
        self._subplot_labels(var_label, "$\psi_0$", "", ax10)
        self._subplot_conv_map(VARs, PSI0s, PMAP, ax10)
        self._subplot_conv_path(paths1[0], paths1[2], paths2[0], paths2[2], ax10)
        ax10.grid()

        PMAP = np.min(MATRIX, axis=2)
        ax01.xaxis.tick_top()
        ax01.xaxis.set_ticks_position("both")
        ax01.xaxis.set_label_position("top")
        ax01.yaxis.tick_right()
        ax01.yaxis.set_ticks_position("right")
        ax01.yaxis.set_label_position("right")
        self._subplot_labels("$\psi_D$", var_label, "", ax01)
        self._subplot_conv_map(PSIDs, VARs, PMAP, ax01)
        self._subplot_conv_path(paths1[1], paths1[0], paths2[1], paths2[0], ax01)
        ax01.grid()

        ax00.axis("off")
        x = (ax00.get_xlim()[0] + (ax00.get_xlim()[1] - ax00.get_xlim()[0]) / 2) * 0.7
        y = ax00.get_ylim()[1]
        ax00.text(x, y, title, size=14, va="top", ha="center")

        cbar_ax = fig.add_axes([0.1, 0.6, 0.35, 0.04])
        cb = fig.colorbar(h1, cax=cbar_ax, orientation="horizontal")
        cb.ax.set_xlabel("convergence to zero")

        plt.tight_layout()
        plt.draw()
        # fig.savefig("/home/bmary/"+title+".png")
        # fig.savefig("/home/bmary/conv_map.png")
        # plt.close(fig)
        return count1, count2, fig


if __name__ == "__main__":

    do = "phiB"
    loop = False

    if do == "alpha" and not loop:
        foo = EccwExplore(phiB=30, phiD=20, beta=10, context="c")
        X1 = [0.0, 0.0, 0.0]
        X2 = [0.0, foo._sign * pi / 2.0, foo._sign * pi / 4.0]
        c1, c2, fig = foo.draw_map_solution(foo._runtime_alpha, X1, X2)
        print(c1, c2, foo.compute_alpha())
        plt.show()

    if do == "alpha" and loop:
        foo = EccwExplore(phiB=30, phiD=20, beta=10, context="c")
        phiDs, betas = range(0, 35, 5), range(-20, 20, 5)
        for i, (phiD, beta) in enumerate(product(phiDs, betas)):
            foo.set_params(phiD=phiD, beta=beta)
            X1 = [0.0, 0.0, 0.0]
            X2 = [0.0, foo._sign * pi / 2.0, foo._sign * pi / 4.0]
            c1, c2, fig = foo.draw_map_solution(foo._runtime_alpha, X1, X2)
            print(c1, c2, foo.compute_alpha())
            title = f"convergence_map_alpha_{i+1}"
            fig.savefig("/home/bmary/tmp/" + title + ".png")
            plt.close(fig)

    if do == "phiD" and not loop:
        # TODO: extension donne même résultat que compression !!!
        # foo = EccwExplore(phiB=30, alpha=0, beta=10, context="c")
        # foo = EccwExplore(phiB=30, alpha=-20.13, beta=80.8363, context="c") #phiD=5,25
        # foo = EccwExplore(phiB=30, alpha=11.6, beta=-1.5, context="c") #phiD=5,25
        # foo = EccwExplore(phiB=30, alpha=-10, beta=39, context="c")
        foo = EccwExplore(
            phiB=30, alpha=21.86, beta=2.58, context="c"
        )  # phiD=7, 29 collapse
        delta = foo._alpha + foo._beta
        # X1 = [delta, delta, 0.0]
        X1 = [-delta, -pi / 2, -pi / 2]
        # X2 = [0., pi/2, pi/2 - delta]
        X2 = [0.0, delta, 0.0]
        c1, c2, fig = foo.draw_map_solution(
            foo._runtime_phiD, X1, X2, vmin=-3 * pi / 4, vmax=3 * pi / 4, N=50
        )
        print(c1, c2)
        try:
            print(foo.compute_phiD())
        except RuntimeError:
            print("Error")
            pass
        plt.show()

    if do == "phiD" and loop:
        foo = EccwExplore(phiB=30, alpha=0, beta=10, context="c")
        alphas, betas = range(-20, 20, 5), range(-20, 20, 5)
        for i, (alpha, beta) in enumerate(product(alphas, betas)):
            foo.set_params(alpha=alpha, beta=beta)
            delta = foo._alpha + foo._beta
            X1 = [delta, delta, 0.0]
            X2 = [0.0, pi / 2, pi / 2 - delta]
            c1, c2, fig = foo.draw_map_solution(
                foo._runtime_phiD, X1, X2, vmin=-pi / 4, vmax=3 * pi / 4
            )
            print(c1, c2)
            try:
                print(foo.compute_phiD())
            except RuntimeError:
                print("Error")
                pass
            title = f"convergence_map_phiD_{i+1}"
            fig.savefig("/home/bmary/tmp/" + title + ".png")
            plt.close(fig)

    if do == "phiB":
        foo = EccwExplore(phiD=15, alpha=20, beta=10, context="c")
        delta = foo._alpha + foo._beta
        # X1 =[radians(29), radians(13), radians(0)]  # phiD=20, alpha=1, beta=10
        # X1 =[radians(21), radians(28), radians(9)]  # phiD=20, alpha=10, beta=8
        # X1 =[radians(21), radians(28), radians(9)]  # phiD=15, alpha=30, beta=10, extension
        X1 = [foo._phiD, delta, foo._alpha]
        X2 = [-foo._phiD, -pi / 2 + delta, -pi / 2 + foo._alpha]
        c1, c2, fig = foo.draw_map_solution(foo._runtime_phiB, X1, X2)
        print(c1, c2)
        try:
            print(foo.compute_phiB())
        except RuntimeError:
            print("Error")
            pass
        plt.show()
