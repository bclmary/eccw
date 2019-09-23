#!/usr/bin/env python3
# -*-coding:utf-8 -*

"""
Elements dedicated to explore solutions.
"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import ticker, cm
from math import pi, degrees

from eccw import EccwCompute


class EccwExplore(EccwCompute):

    ## compute elements #######################################################

    def _prepare_Pmap(self, N, amin, amax, psimin, psimax):
        self._set_at_runtime = self._runtime_alpha
        ALPHAs= np.linspace(amin, amax, N)
        PSIDs = np.linspace(psimin, psimax, N)
        PSI0s = np.linspace(psimin, psimax, N)
        Pmap = np.zeros((N, N))
        return ALPHAs, PSIDs, PSI0s, Pmap

    def _compute_Pmap_psiD_vs_psi0(self, N, amin, amax, psimin, psimax):
        ALPHAs, PSIDs, PSI0s, Pmap = self._prepare_Pmap(N, amin, amax, psimin, psimax)
        Amap = np.zeros((N, N))
        for i, psi0 in enumerate(PSI0s):
            for j, psiD in enumerate(PSIDs):
                p = float("+inf")
                for alpha in ALPHAs:
                    X = self._function_to_root([alpha, psiD, psi0], self._runtime_alpha)
                    if (abs(X) < p).all():
                        p = max(abs(X))
                        x = degrees(alpha)
                Pmap[i,j] = p
                Amap[i,j] = x
        return Pmap, Amap

    def _compute_Pmap_psiD_vs_alpha(self, N, amin, amax, psimin, psimax):
        ALPHAs, PSIDs, PSI0s, Pmap = self._prepare_Pmap(N, amin, amax, psimin, psimax)
        psi0map = np.zeros((N, N))
        for i, alpha in enumerate(ALPHAs):
            for j, psiD in enumerate(PSIDs):
                p = float("+inf")
                for psi0 in PSI0s:
                    X = self._function_to_root([alpha, psiD, psi0], self._runtime_alpha)
                    if (abs(X) < p).all():
                        p = max(abs(X))
                        x = degrees(psi0)
                Pmap[i,j] = p
                psi0map[i,j] = x
        return Pmap, psi0map

    def _compute_Pmap_alpha_vs_psi0(self, N, amin, amax, psimin, psimax):
        ALPHAs, PSIDs, PSI0s, Pmap = self._prepare_Pmap(N, amin, amax, psimin, psimax)
        psiDmap = np.zeros((N, N))
        for i, psi0 in enumerate(PSI0s):
            for j, alpha in enumerate(ALPHAs):
                p = float("+inf")
                for psiD in PSIDs:
                    X = self._function_to_root([alpha, psiD, psi0], self._runtime_alpha)
                    if (abs(X) < p).all():
                        p = max(abs(X))
                        x = degrees(psiD)
                Pmap[i,j] = p
                psiDmap[i,j] = x
        return Pmap, psiDmap

    def _solve_for_map_solution(self, X):
        #self._set_at_runtime = self._runtime_alpha
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
        #axe.set_aspect('equal', adjustable='box')
        levels = [1e-3, 2e-3, 5e-3, 1e-2, 2e-2, 5e-2, 1e-1, 2e-1, 5e-1, 1e0]
        h = axe.contourf(X, Y, MAP,
            cmap="bone", locator=ticker.LogLocator(), levels=levels,
        )
        #plt.colorbar(h1, ax=axe)
        return h

    def _subplot_contour_map(self, X, Y, MAP, axe):
        h = axe.contour(X, Y, MAP, 
            colors='k',levels=list(range(-30,35,5)),
            linewidths=1,
        )
        axe.clabel(ha, inline=1, fontsize=10)
        return h

    def _subplot_conv_path(self, pathX1, pathY1, pathX2, pathY2, axe):
        axe.plot(pathX1, pathY1, "-or")
        axe.plot(pathX1[-1], pathY1[-1], "ob")
        axe.plot(pathX2, pathY2, "-or")
        axe.plot(pathX2[-1], pathY2[-1], "ob")

    def draw_map_solution(self, N=32):
        #### SOLVE ####
        X = [0., 0., 0.]
        alpha_path1, psiD_path1, psi0_path1, c1 = self._solve_for_map_solution(X)

        X = [0., self._sign*pi/2., self._sign*pi/4.]
        #X = [self._sign*self._phiB/4, self._sign*pi/2., self._sign*pi/4.]
        #X = [self._sign*self._phiB/2, self._sign*3*pi/8, self._sign*3*pi/8]
        alpha_path2, psiD_path2, psi0_path2, c2 = self._solve_for_map_solution(X)

        ### PLOT ###
        psimin, psimax = -pi/2, pi/2
        amin, amax = -self._phiB, self._phiB
        ALPHAs, PSIDs, PSI0s, _ = self._prepare_Pmap(
            N, degrees(amin), degrees(amax), degrees(psimin), degrees(psimax)
        )
        title = f"conv_map_phiD{round(self.phiD,1)}"
        fig = plt.figure(title, figsize=(10,10))
        fig.suptitle(
            f"Convergence maps for parameters $\\beta$={round(self.beta,2)}, "
            f"$\phi_B$={round(self.phiB,2)} and $\phi_D$={round(self.phiD,2)}", 
            fontsize=14
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

        # f"contour lines are best {title} value"
        PMAP, aMAP = self._compute_Pmap_psiD_vs_psi0(N, amin, amax, psimin, psimax)
        self._subplot_labels("$\psi_D$", "", "", ax1)
        h1 = self._subplot_conv_map(PSIDs, PSI0s, PMAP, ax1)
        self._subplot_conv_path(psiD_path1, psi0_path1, psiD_path2, psi0_path2, ax1)

        PMAP, psiDMAP = self._compute_Pmap_alpha_vs_psi0(N, amin, amax, psimin, psimax)
        self._subplot_labels("$\\alpha$", "$\psi_0$", "", ax2)
        self._subplot_conv_map(ALPHAs, PSI0s, PMAP, ax2)
        self._subplot_conv_path(alpha_path1, psi0_path1, alpha_path2, psi0_path2, ax2)

        PMAP, psi0MAP = self._compute_Pmap_psiD_vs_alpha(N, amin, amax, psimin, psimax)
        self._subplot_labels("", "$\\alpha$", "", ax3)
        self._subplot_conv_map(PSIDs, ALPHAs, PMAP, ax3)
        self._subplot_conv_path(psiD_path1, alpha_path1, psiD_path2, alpha_path2, ax3)

        fig.subplots_adjust(right=0.8)
        cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
        cb = fig.colorbar(h1, cax=cbar_ax)
        cb.ax.set_ylabel('convergence to zero')

        #plt.tight_layout()
        plt.show()

        #fig.savefig("/home/bmary/"+title+".png")
        #fig.savefig("/home/bmary/conv_map.png")
        #plt.draw()
        #plt.close(fig)
        return c1, c2


if __name__ == "__main__":

    foo = EccwExplore(phiB=30, phiD=20, beta=0)
    c1, c2 = foo.draw_map_solution()
    print(foo.phiD, c1, c2)
