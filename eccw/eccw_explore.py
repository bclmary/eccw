#!/usr/bin/env python3
# -*-coding:utf-8 -*

"""
Elements dedicated to explore solutions.
"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import ticker, cm
from math import pi, degrees, inf
from itertools import product
#import multiprocessing   # fails at pickling the class
#import concurrent.futures   # fail at pickling the class
#import pathos   # <<<<< solution !


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
            product(X, PSID, PSI0)
        )
        return np.reshape(tuple(MAP), (len(X),len(PSID),-1))

    def _solve_for_map_solution(self, X):
        # self._set_at_runtime = self._runtime_alpha
        _ = self._newton_raphson_solve(X, self._runtime_alpha)
        alpha_path, psiD_path, psi0_path = zip(*self.path)
        alpha_path = [degrees(x) for x in alpha_path]
        psiD_path = [degrees(x) for x in psiD_path]
        psi0_path = [degrees(x) for x in psi0_path]
        return alpha_path, psiD_path, psi0_path, self.iter_conv

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
        axe.plot(pathX2, pathY2, "-or")
        axe.plot(pathX2[-1], pathY2[-1], "ob")

    def draw_map_solution(self, N=32):
        psimin, psimax = -pi / 2, pi / 2
        amin, amax = -self._phiB, self._phiB

        #### SOLVE ####
        X = [0.0, 0.0, 0.0]
        alpha_path1, psiD_path1, psi0_path1, c1 = self._solve_for_map_solution(X)

        X = [0.0, self._sign * pi / 2.0, self._sign * pi / 4.0]
        alpha_path2, psiD_path2, psi0_path2, c2 = self._solve_for_map_solution(X)

        ALPHAs = np.linspace(amin, amax, N)
        PSIDs = np.linspace(psimin, psimax, N)
        PSI0s = np.linspace(psimin, psimax, N)
        MATRIX = self._matrix_of_function_to_root(
            ALPHAs, PSIDs, PSI0s, self._runtime_alpha
        )

        ### PLOT ###
        ALPHAs = [degrees(x) for x in ALPHAs]
        PSIDs = [degrees(x) for x in PSIDs]
        PSI0s = [degrees(x) for x in PSI0s]

        title = f"conv_map_phiD{round(self.phiD,1)}"
        fig = plt.figure(title, figsize=(10, 10))
        fig.suptitle(
            f"Convergence maps for parameters $\\beta$={round(self.beta,2)}, "
            f"$\phi_B$={round(self.phiB,2)} and $\phi_D$={round(self.phiD,2)}",
            fontsize=14,
        )
        #     0  1  2
        #   ┌──┬──┬──┐
        # 0 │  │░░│░░│   ▓ ax1
        #   ├──┼──┼──┤
        # 1 │▒▒│▓▓│▓▓│   ▒ ax2      3x3 subplot grid
        #   ├──┼──┼──┤
        # 2 │▒▒│▓▓│▓▓│   ░ ax3
        #   └──┴──┴──┘
        ax1 = plt.subplot2grid((3, 3), (1, 1), colspan=2, rowspan=2)
        ax2 = plt.subplot2grid((3, 3), (1, 0), rowspan=2, sharey=ax1)
        ax3 = plt.subplot2grid((3, 3), (0, 1), colspan=2, sharex=ax1)

        PMAP = np.transpose(np.min(MATRIX, axis=0))
        self._subplot_labels("$\psi_D$", "", "", ax1)
        h1 = self._subplot_conv_map(PSIDs, PSI0s, PMAP, ax1)
        self._subplot_conv_path(psiD_path1, psi0_path1, psiD_path2, psi0_path2, ax1)

        PMAP = np.transpose(np.min(MATRIX, axis=1))
        self._subplot_labels("$\\alpha$", "$\psi_0$", "", ax2)
        self._subplot_conv_map(ALPHAs, PSI0s, PMAP, ax2)
        self._subplot_conv_path(alpha_path1, psi0_path1, alpha_path2, psi0_path2, ax2)

        PMAP = np.min(MATRIX, axis=2)
        self._subplot_labels("", "$\\alpha$", "", ax3)
        self._subplot_conv_map(PSIDs, ALPHAs, PMAP, ax3)
        self._subplot_conv_path(psiD_path1, alpha_path1, psiD_path2, alpha_path2, ax3)

        fig.subplots_adjust(right=0.8)
        cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
        cb = fig.colorbar(h1, cax=cbar_ax)
        cb.ax.set_ylabel("convergence to zero")

        # plt.tight_layout()
        plt.show()

        # fig.savefig("/home/bmary/"+title+".png")
        # fig.savefig("/home/bmary/conv_map.png")
        # plt.draw()
        # plt.close(fig)
        return c1, c2


if __name__ == "__main__":

    foo = EccwExplore(phiB=30, phiD=20, beta=0)
    c1, c2 = foo.draw_map_solution()
    print(foo.phiD, c1, c2)
