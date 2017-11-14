#!/usr/bin/env python3
# -*-coding:utf-8 -*

#Copyright 2016-2017 Baptiste C.L. Mary, Xiaoping Yuan, Yves M. Leroy

#This file is part of ECCW.
#
#    ECCW is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    ECCW is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with ECCW.  If not, see <http://www.gnu.org/licenses/>. 2

"""
Created 10 Jan 2016
Last edited 27 Oct 2017
@author: bcl mary
"""

if __name__ == "__main__":
    import os
    parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.sys.path.insert(0,parentdir) 

import numpy as np
from math import pi, copysign, cos, sin, tan, atan, asin

#numtol = 1e-9

###############################################################################
###############################################################################
###############################################################################



###############################################################################
class EccwCompute(object):
    """
    Poulpe.
    """
    _numtol = 1e-9
    _h = 1e-5  # Arbitrary small value
    _sign = 1
    _phiB = None
    _phiD = None
    _rho_f = 0.
    _rho_sr = 0.
    _density_ratio = 0.
    _delta_lambdaB = 0.
    _delta_lambdaD = 0.
    _lambdaB = 0.
    _lambdaD = 0.
    _lambdaB_D2 = 0.
    _lambdaD_D2 = 0.
    _taper_min = -float('inf')
    _taper_max = float('inf')

    def __init__(self, **kwargs):
        self.alpha = kwargs.get("alpha", 0.)
        self.beta = kwargs.get("beta", 0.)
        self.phiB = kwargs.get("phiB", 0.)
        self.phiD = kwargs.get("phiD", 0.)
        self.rho_f = kwargs.get("rho_f", 0.)
        self.rho_sr = kwargs.get("rho_sr", 0.)
        self.delta_lambdaB = kwargs.get("delta_lambdaB", 0.)
        self.delta_lambdaD = kwargs.get("delta_lambdaD", 0.)
        self.context =  kwargs.get("context", "c")


    ##### properies #####

    @property
    def alpha(self):
        """Surface slope [deg], positive downward."""
        return self._r2d(self._alpha)
    @alpha.setter
    def alpha(self, value):
        try:
            self._alpha = self._d2r(value)
        except TypeError:
            raise TypeError(self._error_message('alpha', 'type', 'a float'))

    @property
    def beta(self):
        """Basal slope [deg], posirtive upward."""
        return self._r2d(self._beta)
    @beta.setter
    def beta(self, value):
        try:
            self._beta = self._d2r(value)
        except TypeError:
            raise TypeError(self._error_message('beta', 'type', 'a float'))

    @property
    def phiB(self):
        """Bulk friction angle [deg]."""
        return self._r2d(self._phiB)
    @phiB.setter
    def phiB(self, value):
        try:
            self._phiB = self._d2r(value)
        except TypeError:
            raise TypeError(self._error_message('phiB', 'type', 'a float'))

    @property
    def phiD(self):
        """Basal friction angle [deg]."""
        return self._r2d(self._sign*self._phiD)
    @phiD.setter
    def phiD(self, value):
        try:
            self._phiD = self._d2r(value)
            self._taper_min = -self._numtol
            self._taper_max = pi / 2. - self._phiD + self._numtol
        except TypeError:
            raise TypeError(self._error_message('phiD', 'type', 'a float'))

    @property
    def context(self):
        """Tectonic context: compression or extension."""
        if self._sign == 1:
            return "Compression"
        else:
            return "Extension"
    @context.setter
    def context(self, value):
        errmessage = self._error_message("context", "value", "'compression' or 'extension'")
        try:
            if value.lower() in ("compression", "c"):
                self._sign = 1
            elif value.lower() in ("extension", "e"):
                self._sign = -1
            else:
                raise ValueError(errmessage)
        except AttributeError:
            raise ValueError(errmessage)
        self._phiD *= self._sign

    @property
    def rho_f(self):
        """Volumetric mass density of fluids."""
        return self._rho_f
    @rho_f.setter
    def rho_f(self, value):
        try:
            self._rho_f = value + 0.  # +0 test value is a float.
            self._set_density_ratio()
        except TypeError:
            raise TypeError(self._error_message('rho_f', 'type', 'a float'))

    @property
    def rho_sr(self):
        """Volumetric mass density of saturated rock."""
        return self._rho_sr
    @rho_sr.setter
    def rho_sr(self, value):
        try:
            self._rho_sr = value + 0.  # +0 test value is a float.
            self._set_density_ratio()
        except TypeError:
            raise TypeError(self._error_message('rho_sr', 'type', 'a float'))

    @property
    def delta_lambdaB(self):
        """Bulk fluids overpressure ratio."""
        return self._delta_lambdaB
    @delta_lambdaB.setter
    def delta_lambdaB(self, value):
        try:
            if 0. <= value <= 1 - self._density_ratio:
                self._delta_lambdaB = value
                self._lambdaB = self._delta_lambdaB + self._density_ratio
                self._lambdaB_D2 = self._convert_lambda(self._alpha, self._lambdaB)
                self._alpha_prime = self._convert_alpha(self._alpha, self._lambdaB_D2)
            else:
                raise ValueError(self._error_message("delta_lambdaB", "value", "in [0 : %s]" % (1-self._density_ratio)))
        except TypeError:
            raise TypeError(self._error_message("delta_lambdaB", "type", "a float"))

    @property
    def delta_lambdaD(self):
        """Basal fluids overpressure ratio."""
        return self._delta_lambdaD
    @delta_lambdaD.setter
    def delta_lambdaD(self, value):
        try:
            if 0. <= value < 1 - self._density_ratio:
                self._delta_lambdaD = value
                self._lambdaD = self._delta_lambdaD + self._density_ratio
                self._lambdaD_D2 = self._convert_lambda(self._alpha, self._lambdaD)
            else:
                raise ValueError(self._error_message("delta_lambdaD", "value", "in [0 : %s]" % (1-self._density_ratio)))
        except TypeError:
            raise TypeError(self._error_message("delta_lambdaD", "type", "a float"))



    ##### private methods #####

    def _error_message(self, who, problem, solution):
        class_name = self.__class__.__name__
        return "%s() gets wrong %s for '%s': must be %s" % (class_name , problem, who, solution)


    def _d2r(self, value):
        return value * pi / 180.

    def _r2d(self, value):
        return value / pi * 180.

    def _set_density_ratio(self):
        """Ratio of mass densities of fluids over saturated rock  = hydrostatic pressure."""
        self._density_ratio = self._rho_f / self._rho_sr if self._rho_sr != 0. else 0.
        foo = 1 - self._density_ratio
        if foo < self.delta_lambdaB :
            raise ValueError(self._error_message("delta_lambdaB' after setting 'rho_f' or rho_sr'", "value", "lower than %s" % foo))
        if foo < self.delta_lambdaD :
            raise ValueError(self._error_message("delta_lambdaD' after setting 'rho_f' or rho_sr'", "value", "lower than %s" % foo))


    def _convert_lambda(self, alpha, lambdaX) :
        return lambdaX / cos(alpha) ** 2. - self._density_ratio * tan(alpha) ** 2. 

    def _convert_alpha(self, alpha, lambdaB_D2) :
        return atan((1 - self._density_ratio) / (1 - lambdaB_D2) * tan(alpha))

    def _PSI_D(self, psi0, phiB, phiD, lambdaB_D2, lambdaD_D2):
        """Compute psi_D as Dahlen."""
        dum = (1. - lambdaD_D2) * sin(phiD) / (1. - lambdaB_D2) / sin(phiB)
        dum = dum + (lambdaD_D2 - lambdaB_D2) * sin(phiD) * cos(2. * psi0) / (1. - lambdaB_D2)
        return (asin(dum) - phiD) / 2., (pi - asin(dum) - phiD) / 2.
        
    def _PSI_0(self, alpha_prime, phiB):
        """Compute psi_0 as Dahlen."""
        dum = sin(alpha_prime) / sin(phiB)
        return (asin(dum) - alpha_prime) / 2., (pi - asin(dum) - alpha_prime) / 2.


    def _is_valid_taper(self, a, b):
        return self._taper_min < a+b < self._taper_max

    def _test_alpha(self, a):
        return a if self._is_valid_taper(a, self._beta) else None

    def _test_phiB(self, phiB):
        return phiB if 0. <= phiB <= pi/2. else None

    def _test_phiD(self, phiD):
        return self._sign * phiD if copysign(1, phiD) == self._sign else None


    def _runtime_alpha(self, alpha):
        lambdaB_D2 = self._convert_lambda(alpha, self._lambdaB)
        lambdaD_D2 = self._convert_lambda(alpha, self._lambdaD)
        alpha_prime = self._convert_alpha(alpha, lambdaB_D2)
        return alpha, self._phiB, self._phiD, lambdaB_D2, lambdaD_D2, alpha_prime

    def _runtime_phiB(self, phiB):
        return self._alpha, phiB, self._phiD, self._lambdaB_D2, self._lambdaD_D2, self._alpha_prime

    def _runtime_phiD(self, phiD):
        return self._alpha, self._phiB, phiD, self._lambdaB_D2, self._lambdaD_D2, self._alpha_prime



    def _function1(self, alpha, beta,  psiD, psi0):
        """First function of function to root."""
        return alpha + beta - psiD + psi0 

    def _function2(self, psiD, psi0, phiB, phiD, lambdaB_D2, lambdaD_D2):
        """Second function of function to root."""
        f = sin(2 * psiD + phiD)
        f = f - (1 - lambdaD_D2) * sin(phiD) / (1 - lambdaB_D2) / sin(phiB) 
        f = f - (lambdaD_D2 - lambdaB_D2) * sin(phiD) * cos(2 * psi0) / (1 - lambdaB_D2)
        return f

    def _function3(self, psi0, alpha_prime, phiB) :
        """Third function of function to root."""
        return sin(2 * psi0 + alpha_prime) * sin(phiB) - sin(alpha_prime)

    def _function_to_root(self, X):
        """Function of wich we are searching the roots.
        Gets an array X of length 3 as input.
        Return an array of length 3.
        """
        psiD, psi0 = X[1:3]
        alpha, phiB, phiD, lambdaB_D2, lambdaD_D2, alpha_prime = self._set_at_runtime(X[0])
        #Redefine lambda and alpha according to Dahlen's second definition
        f1 = self._function1(alpha, self._beta,  psiD, psi0)
        f2 = self._function2(psiD, psi0, phiB, phiD, lambdaB_D2, lambdaD_D2)
        f3 = self._function3(psi0, alpha_prime, phiB)
        return np.array([f1, f2, f3])

    def _derivative_matrix(self, F, X):
        """Approximation of derivative of F. 
        Return a 3×3 matrix of approx. of partial derivatives.
        """
        M = np.zeros((3,3))
        for j in range(3) :
            Y = X.copy()
            Y[j] += self._h
            DF = self._function_to_root(Y)
            M[:,j] = DF - F
        return M / self._h

    def _newton_rapson_solve(self, X):
        count = 0
        F = self._function_to_root(X)
        while not (abs(F) < self._numtol).all() : 
            count += 1
            M = self._derivative_matrix(F, X) #Approx. of derivative.
            invM = np.linalg.inv(M)
            X = X - invM.dot(F) #Newton-Rapson iteration.
            F = self._function_to_root(X)
            if count > 50 : 
                print("!!! ERROR : More than 50 iteration to converge, abort.")
                return None
        return X[0]


    ##### public methods #####

    def compute_beta(self, deg=True):
        """Get critical basal slope beta as ECCW.
        Return the 2 possible solutions in tectonic or  collapsing regime.
        Return two None if no physical solutions.
        """
        BETA = list()
        if -self._phiB <= self._alpha_prime <= self._phiB : # asin in PSI_D is your ennemy !
            psi0_1, psi0_2 = self._PSI_0(self._alpha_prime, self._phiB)
            psiD_11, psiD_12 = self._PSI_D(psi0_1, self._phiB, self._phiD, self._lambdaB_D2, self._lambdaD_D2)
            psiD_21, psiD_22 = self._PSI_D(psi0_2, self._phiB, self._phiD, self._lambdaB_D2, self._lambdaD_D2)
            beta_11 = psiD_11 - psi0_1 - self._alpha
            beta_12 = psiD_12 - psi0_1 - self._alpha
            beta_21 = psiD_21 - psi0_2 - self._alpha + pi # Don't ask why "+pi"…
            beta_22 = psiD_22 - psi0_2 - self._alpha
            for b in [beta_11, beta_12, beta_21, beta_22]:
                if self._is_valid_taper(self._alpha, b):
                    BETA.append(b)
            beta1, beta2 = min(BETA), max(BETA)
            if deg:
                beta1 = self._r2d(beta1)
                beta2 = self._r2d(beta2)
            return beta1, beta2
        else:
            return None, None


    def compute_alpha(self, deg=True):
        """Get critical topographic slope alpha as ECCW.
        Return the 2 possible solutions in tectonic or collapsing regime.
        Return two None if no physical solutions.
        """
        self._set_at_runtime = self._runtime_alpha
        # Inital value of alpha for Newton-Rapson solution.
        alpha = 0.
        # First solution of ECCW (lower).
        ## Set initial values:
        psiD = pi
        psi0 = psiD - alpha - self._beta
        alpha1 = self._newton_rapson_solve([alpha, psiD, psi0])
        alpha1 = self._test_alpha(alpha1)
        # Second solution of ECCW (upper).
        ## Set initial values:
        psiD = pi / 2.
        psi0 = psiD - alpha - self._beta
        alpha2 = self._newton_rapson_solve([alpha, psiD, psi0])
        alpha2 = self._test_alpha(alpha2)
        if deg:
            alpha1 = self._r2d(alpha1) if alpha1 else None
            alpha2 = self._r2d(alpha2) if alpha2 else None
        return alpha1, alpha2


    def compute_phiB(self, deg=True):
        self._set_at_runtime = self._runtime_phiB
        # Inital value of phiB for Newton-Rapson solution.
        phiB = pi/3.
        # First solution of ECCW (lower).
        ## Set initial values:
        psiD = pi
        psi0 = psiD - self._alpha - self._beta
        phiB1 = self._newton_rapson_solve([phiB, psiD, psi0])
        phiB1 = self._test_phiB(phiB1)
        psiD = pi / 2.
        psi0 = psiD - self._alpha - self._beta
        phiB2 = self._newton_rapson_solve([phiB, psiD, psi0])
        phiB2 = self._test_phiB(phiB2)
        if deg:
            phiB1 = self._r2d(phiB1) if phiB1 else None
            phiB2 = self._r2d(phiB2) if phiB2 else None
        return phiB1, phiB2

    def compute_phiD(self, deg=True):
        self._set_at_runtime = self._runtime_phiD
        # Inital value of phiB for Newton-Rapson solution.
        phiD = pi/3.
        # First solution of ECCW (lower).
        ## Set initial values:
        psiD = pi
        psi0 = psiD - self._alpha - self._beta
        phiD1 = self._newton_rapson_solve([phiD, psiD, psi0])
        phiD1 = self._test_phiD(phiD1)
        psiD = pi / 2.
        psi0 = psiD - self._alpha - self._beta
        phiD2 = self._newton_rapson_solve([phiD, psiD, psi0])
        phiD2 = self._test_phiD(phiD2)
        if deg:
            phiD1 = self._r2d(phiD1) if phiD1 else None
            phiD2 = self._r2d(phiD2) if phiD2 else None
        return phiD1, phiD2

    def compute(self, flag):
        parser = {
            "alpha": self.compute_alpha,
            "beta": self.compute_beta,
            "phiB": self.compute_phiB,
            "phiD": self.compute_phiD,
        }
        return parser[flag]()


###############################################################################
class EccwPlot(object):


    def plot(PARAMS, alpha_in1, alpha_in2, beta_in, rect=None, figure=None, legend=None) :
        """Plot complete solution plus a given solution.
    Use directe solution f(alpha) = beta.
    """

    #--------------------------------------------------------------------------
        def store(i, beta) :
            #Append solution to BETALPHA if valid. 
            #Parent's namespace is used.
            if alpha + beta > abmin and alpha + beta < abmax : 
                BETALPHA[i][0].append(beta * 180. / pi)
                BETALPHA[i][1].append(alpha * 180. / pi)
        #--------------------------------------------------------------------------

        #Set figure handler
        if figure is None :
            figure = plt.figure("ECCW", figsize=(8,6))
        axe = figure.gca()
        #Rename some parameters.
        phiB, phiD = PARAMS["phiB"], PARAMS["phiD"]
        delta_lambdaB, delta_lambdaD = PARAMS["delta_lambdaB"], PARAMS["delta_lambdaD"]
        density_ratio = PARAMS["density_ratio"]
        lambdaB, lambdaD = PARAMS["lambdaB"], PARAMS["lambdaD"]
        #min and max values of alpha + beta.
        abmin, abmax = -numtol, pi / 2. - phiD + numtol    
        #Define highest value of alpha.
        alphamax = get_alphamax(phiB, density_ratio, lambdaB)
        #Init solution container.
        BETALPHA = [[[] for i in range(2)] for i in range(4)]
        #Init values of alpha.
        ALPHA = np.arange(-alphamax, alphamax, alphamax * 2 / 1e4) #10,000 nodes
        #Compute betas for all alphas.    
        for alpha in ALPHA :
            lambdaB_D2 = convert_lambda(alpha, density_ratio, lambdaB)
            lambdaD_D2 = convert_lambda(alpha, density_ratio, lambdaD)
            alpha_prime = convert_alpha(alpha, density_ratio, lambdaB_D2)
            if alpha_prime < phiB and alpha_prime > -phiB : #asin in PSI_D is your ennemy ! 
                psi0_1, psi0_2 = PSI_0(alpha_prime, phiB)
                psiD_11, psiD_12 = PSI_D(psi0_1, phiB, phiD, lambdaB_D2, lambdaD_D2)
                psiD_21, psiD_22 = PSI_D(psi0_2, phiB, phiD, lambdaB_D2, lambdaD_D2)
                beta_11 = psiD_11 - psi0_1 - alpha
                beta_12 = psiD_12 - psi0_1 - alpha
                beta_21 = psiD_21 - psi0_2 - alpha + pi #Don't ask why "+pi"…
                beta_22 = psiD_22 - psi0_2 - alpha
                store(0, beta_11)
                store(1, beta_12)
                store(2, beta_21)
                store(3, beta_22)
        #Plot upper solution.
        label = "normal faults\n(gravitational collapse)" if phiD > 0. else "normal faults\n(tectonic)"
        BETA_upper = BETALPHA[3][0] + BETALPHA[1][0][::-1]
        ALPHA_upper = BETALPHA[3][1] + BETALPHA[1][1][::-1]
        plt.plot(BETA_upper, ALPHA_upper,"b", lw=2, figure=figure, label=label)
        #Plot lower solution.
        label = "inverse faults\n(tectonic)" if phiD > 0. else "inverse faults\n(gravitational collapse)"
        BETA_lower = BETALPHA[0][0][::-1] + BETALPHA[2][0]
        ALPHA_lower = BETALPHA[0][1][::-1] + BETALPHA[2][1]
        plt.plot(BETA_lower, ALPHA_lower,"r", lw=2, figure=figure, label=label)
        #Plot given solution if any
        if beta_in is not None :
            plt.axvline(beta_in, linewidth=1, color='gray', figure=figure) #vertical line
            plt.plot(beta_in, alpha_in1,"ok", figure=figure)
            plt.plot(beta_in, alpha_in2,"ok", figure=figure)
        #Set axis, grid, legend, …
        if density_ratio != 0. :     
            title_elts = (phiB * 180./pi, phiD * 180./pi, delta_lambdaB, delta_lambdaD, density_ratio)
            axe.set_title(r"$\phi_B$={:.1f}, $\phi_D$={:.1f}, $\Delta\lambda_B$={:.2f}, $\Delta\lambda_D$={:.2f}, $\frac{{\rho_f}}{{\rho}}$={:.2f}".format(*title_elts), fontsize=16)    
        else :
            title_elts = (phiB * 180./pi, phiD * 180./pi)
            axe.set_title(r"$\phi_B$={:.1f}, $\phi_D$={:.1f}".format(*title_elts), fontsize=16)    
        axe.set_xlabel(r"Décollement angle $\beta$ [deg]", fontsize=16)
        axe.set_ylabel(r"Critical slope $\alpha_c$ [deg]", fontsize=16)
        axe.grid()
        if legend :
            plt.legend(loc='best', fontsize='10').draggable()
        if rect :
            plt.xlim(rect[0:2])
            plt.ylim(rect[2:4])

        #Get reference points
        X = BETA_lower[::100] + BETA_upper[::-100]
        Y = ALPHA_lower[::100] + ALPHA_upper[::-100]    
        P = Polygon(x=X, y=Y)
        P.set_centrosurf()
        refpoints = dict()
        refpoints["C"] = (P.centroid.x, P.centroid.y)
        i, _ = Max(ALPHA_upper)
        refpoints["T"] = (BETA_upper[i], alphamax * 180. / pi)
        i, _ = Min(ALPHA_lower)
        refpoints["B"] = (BETA_lower[i], -alphamax * 180. / pi)
        refpoints["L"] = (BETA_upper[0], ALPHA_upper[0])
        refpoints["R"] = (BETA_upper[-1], ALPHA_upper[-1])
        
    #    plt.plot(refpoints["C"][0], refpoints["C"][1],"ok")
    #    plt.plot(refpoints["T"][0], refpoints["T"][1],"*k")
    #    plt.plot(refpoints["B"][0], refpoints["B"][1],"ok")
    #    plt.plot(refpoints["L"][0], refpoints["L"][1],"+k")
    #    plt.plot(refpoints["R"][0], refpoints["R"][1],"sk")

        #Set axis 
    #    plt.show(figure)
        return figure, refpoints



###############################################################################
###############################################################################
###############################################################################
if __name__ == "__main__":


#    foo = EccwCompute(phiB=30, phiD=10, beta=0, alpha=3.436532)
#    foo = EccwCompute(phiB=30, phiD=10, beta=0, alpha=3.436532, context="e")
    foo = EccwCompute(phiB=30, phiD=10, beta=20, alpha=9.413, context="e")
#    foo = EccwCompute(phiB=30, phiD=10, beta=20, alpha=9.413, context="Extension")
#    print("alphas =", foo.compute_alpha())
    print("alphas =", foo.compute("alpha"))
    print("betas  =", foo.compute_beta())
    print("phiB =", foo.compute_phiB())
    print("phiD =", foo.compute_phiD())
    print(foo.beta)


    #foo = EccwCompute(bulk_friction=30, basal_friction=10, basal_slope=20, surface_slope=9.413, bulk_overpressure=0., basal_overpressure=0., fluid_density=0., rock_density=)

