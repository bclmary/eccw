#!/usr/bin/env python3
# -*-coding:utf-8 -*

"""
Elements dedicated to solve physics.
"""

import numpy as np
from math import pi, cos, sin, tan, atan, asin
from collections import OrderedDict

from eccw.shared import d2r, r2d


class EccwCompute(object):
    """
    Solve any parameter of the critical coulomb wedge.
    """
    _nan = float('nan')
    _numtol = 1e-9
    _h = 1e-5  # Arbitrary small value
    _main_params_list = ['alpha', 'beta', 'phiB', 'phiD']


    def reset(self):
        self._sign = 1
        self._beta = self._nan
        self._alpha = self._nan
        self._phiB = self._nan
        self._phiD = self._nan
        self._rho_f = 0.
        self._rho_sr = 0.
        self._density_ratio = 0.
        self._delta_lambdaB = 0.
        self._delta_lambdaD = 0.
        self._lambdaB = 0.
        self._lambdaD = 0.
        self._lambdaB_D2 = 0.
        self._lambdaD_D2 = 0.
        self._taper_min = -self._numtol
        self._taper_max = float('inf')

    def __init__(self, **kwargs):
        self.reset()
        self.set_params(**kwargs)

        # self.alpha = kwargs.get("alpha", 0.)
        # self.beta = kwargs.get("beta", 0.)
        # self.phiB = kwargs.get("phiB", 0.)
        # self.phiD = kwargs.get("phiD", 0.)
        # self.rho_f = kwargs.get("rho_f", 0.)
        # self.rho_sr = kwargs.get("rho_sr", 0.)
        # self.delta_lambdaB = kwargs.get("delta_lambdaB", 0.)
        # self.delta_lambdaD = kwargs.get("delta_lambdaD", 0.)
        # self.context = kwargs.get("context", "c")

    def __repr__(self):
        out = self.__class__.__name__ + "("
        for key, value in self.params_table().items():
            out += "{}={}, ".format(key, repr(value))
        out = out[:-2] + ")"
        return out


    # Properties ##############################################################

    @property
    def alpha(self):
        """Surface slope [deg], positive downward."""
        return r2d(self._alpha)

    @alpha.setter
    def alpha(self, value):
        try:
            self._alpha = d2r(value)
            self._lambdaD_D2 = self._convert_lambda(self._alpha, self._lambdaD)
            self._lambdaB_D2 = self._convert_lambda(self._alpha, self._lambdaB)
            self._alpha_prime = self._convert_alpha(self._alpha,
                                                    self._lambdaB_D2)
        except TypeError:
            raise TypeError(self._error_message('alpha', 'type', 'a float'))

    @property
    def beta(self):
        """Basal slope [deg], posirtive upward."""
        return r2d(self._beta)

    @beta.setter
    def beta(self, value):
        try:
            self._beta = d2r(value)
        except TypeError:
            raise TypeError(self._error_message('beta', 'type', 'a float'))

    @property
    def phiB(self):
        """Bulk friction angle [deg]."""
        return r2d(self._phiB)

    @phiB.setter
    def phiB(self, value):
        if value < 0:
            raise TypeError(self._error_message('phiB', 'sign', '> 0'))
        if value == 0:
            raise TypeError(self._error_message('phiB', 'value', 'non zero'))
        try:
            self._phiB = d2r(value)
        except TypeError:
            raise TypeError(self._error_message('phiB', 'type', 'a float'))

    @property
    def phiD(self):
        """Basal friction angle [deg]."""
        return r2d(self._sign*self._phiD)

    @phiD.setter
    def phiD(self, value):
        if value < 0:
            raise TypeError(self._error_message('phiD', 'sign', '>= 0'))
        try:
            self._phiD = d2r(value) * (self._sign if self._sign else 1.)
            self._taper_max = pi / 2. - self._phiD + self._numtol
        except TypeError:
            raise TypeError(self._error_message('phiD', 'type', 'a float'))

    @property
    def context(self):
        """Tectonic context: compression or extension."""
        if self._sign == 1:
            return "Compression"
        elif self._sign == -1:
            return "Extension"
        else:
            return None

    @context.setter
    def context(self, value):
        errmessage = self._error_message("context", "value",
                                         "'compression' or 'extension'")
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
        self._taper_max = pi / 2. - self._phiD + self._numtol

    @property
    def rho_f(self):
        """Volumetric mass density of fluids."""
        return self._rho_f

    @rho_f.setter
    def rho_f(self, value):
        try:
            self._rho_f = value + 0.  # +0 test value is a float.
            self._set_density_ratio()
            self._set_lambdaB()
            self._set_lambdaD()
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
            self._set_lambdaB()
            self._set_lambdaD()
        except TypeError:
            raise TypeError(self._error_message('rho_sr', 'type', 'a float'))

    @property
    def delta_lambdaB(self):
        """Bulk fluids overpressure ratio."""
        return self._delta_lambdaB

    @delta_lambdaB.setter
    def delta_lambdaB(self, value):
        try:
            # if 0. <= value <= 1 - self._density_ratio:
                self._delta_lambdaB = value
                self._set_lambdaB()
            # else:
            #     raise ValueError(self._error_message("delta_lambdaB", "value",
            #                      "in [0 : %s]" % (1-self._density_ratio)))
        except TypeError:
            raise TypeError(self._error_message("delta_lambdaB", "type",
                                                "a float"))

    @property
    def delta_lambdaD(self):
        """Basal fluids overpressure ratio."""
        return self._delta_lambdaD

    @delta_lambdaD.setter
    def delta_lambdaD(self, value):
        try:
            # if 0. <= value < 1 - self._density_ratio:
                self._delta_lambdaD = value
                self._set_lambdaD()
            # else:
            #     raise ValueError(self._error_message("delta_lambdaD", "value",
            #                      "in [0 : %s]" % (1-self._density_ratio)))
        except TypeError:
            raise TypeError(self._error_message("delta_lambdaD", "type",
                                                "a float"))

    # 'Private' methods #######################################################

    def _check_params(self):
        out = self.check_params()
        if out:
            raise ValueError(out)

    def check_params(self):
        errors = ""
        if not (0. <= self._delta_lambdaD < 1 - self._density_ratio):
            errors += self._error_message("delta_lambdaD", "value",
                "in [0 : %s]\n" % (1-self._density_ratio))
        if not (0. <= self._delta_lambdaB <= 1 - self._density_ratio):
            errors +=  self._error_message("delta_lambdaB", "value",
                "in [0 : %s]\n" % (1-self._density_ratio))
        return errors


    def _error_message(self, who, problem, solution):
        class_name = self.__class__.__name__
        return ("%s() gets wrong %s for '%s': must be %s" % (class_name,
                problem, who, solution))

    def _set_density_ratio(self):
        """Ratio of mass densities of fluids over saturated rock.
        equivalent to hydrostatic pressure.
        """
        self._density_ratio = (self._rho_f / self._rho_sr if self._rho_sr
                               != 0. else 0.)
        # foo = 1 - self._density_ratio
        # if foo < self.delta_lambdaB:
        #     raise ValueError(self._error_message("delta_lambdaB' after setting"
        #                                          "'rho_f' or rho_sr'", "value",
        #                                          "lower than %s" % foo))
        # if foo < self.delta_lambdaD:
        #     raise ValueError(self._error_message("delta_lambdaD' after setting"
        #                                          "'rho_f' or rho_sr'", "value",
        #                                          "lower than %s" % foo))

    def _set_lambdaD(self):
        self._lambdaD = self._delta_lambdaD + self._density_ratio
        self._lambdaD_D2 = self._convert_lambda(self._alpha, self._lambdaD)

    def _set_lambdaB(self):
        self._lambdaB = self._delta_lambdaB + self._density_ratio
        self._lambdaB_D2 = self._convert_lambda(self._alpha, self._lambdaB)
        self._alpha_prime = self._convert_alpha(self._alpha, self._lambdaB_D2)

    def _convert_lambda(self, alpha, lambdaX):
        return (lambdaX / cos(alpha) ** 2. - self._density_ratio
                * tan(alpha) ** 2.)

    def _convert_alpha(self, alpha, lambdaB_D2):
        return atan((1 - self._density_ratio) / (1 - lambdaB_D2) * tan(alpha))

    def _PSI_D(self, psi0, phiB, phiD, lambdaB_D2, lambdaD_D2):
        """Compute psi_D as Dahlen."""
        dum = (1. - lambdaD_D2) * sin(phiD) / (1. - lambdaB_D2) / sin(phiB)
        dum += ((lambdaD_D2 - lambdaB_D2) * sin(phiD) * cos(2. * psi0)
                / (1. - lambdaB_D2))
        if dum > 1:
            return 0., 0.  # TODO
        return (asin(dum) - phiD) / 2., (pi - asin(dum) - phiD) / 2.

    def _PSI_0(self, alpha_prime, phiB):
        """Compute psi_0 as Dahlen."""
        dum = sin(alpha_prime) / sin(phiB)
        return ((asin(dum) - alpha_prime) / 2.,
                (pi - asin(dum) - alpha_prime) / 2.)

    def _is_valid_taper(self, a, b):
        return self._taper_min < a+b < self._taper_max

    def _test_alpha(self, a):
        return a if self._is_valid_taper(a, self._beta) else None

    def _test_phiB(self, phiB):
        return phiB if -pi < phiB < pi else float('nan')
        # phiB = normalize_angle(phiB, -pi, pi)
        return phiB  # if 0. <= phiB <= pi/2 else None

    def _test_phiD(self, phiD):
        # phiD = self._sign * phiD if copysign(1, phiD) == self._sign else None
        # return phiD if phiD < float('inf') else None
        return abs(phiD) if phiD < float('inf') else None

    def _runtime_alpha(self, alpha):
        lambdaB_D2 = self._convert_lambda(alpha, self._lambdaB)
        lambdaD_D2 = self._convert_lambda(alpha, self._lambdaD)
        alpha_prime = self._convert_alpha(alpha, lambdaB_D2)
        return (alpha, self._phiB, self._phiD, lambdaB_D2, lambdaD_D2,
                alpha_prime)

    def _runtime_phiB(self, phiB):
        return (self._alpha, phiB, self._phiD, self._lambdaB_D2,
                self._lambdaD_D2, self._alpha_prime)

    def _runtime_phiD(self, phiD):
        return (self._alpha, self._phiB, phiD, self._lambdaB_D2,
                self._lambdaD_D2, self._alpha_prime)

    def _function1(self, alpha, beta,  psiD, psi0):
        """First function of function to root."""
        return alpha + beta - psiD + psi0

    def _function2(self, psiD, psi0, phiB, phiD, lambdaB_D2, lambdaD_D2):
        """Second function of function to root."""
        if phiB == 0:
            print("!!!ERROR phiB == 0.")
        f = sin(2 * psiD + phiD)
        f -= (1 - lambdaD_D2) * sin(phiD) / (1 - lambdaB_D2) / sin(phiB)
        f -= ((lambdaD_D2 - lambdaB_D2) * sin(phiD) * cos(2 * psi0)
              / (1 - lambdaB_D2))
        return f

    def _function3(self, psi0, alpha_prime, phiB):
        """Third function of function to root."""
        return sin(2 * psi0 + alpha_prime) * sin(phiB) - sin(alpha_prime)

    def _function_to_root(self, X):
        """Function of wich we are searching the roots.
        Gets an array X of length 3 as input.
        Return an array of length 3.
        """
        psiD, psi0 = X[1:3]
        alpha, phiB, phiD, lambdaB_D2, lambdaD_D2, alpha_prime = (
            self._set_at_runtime(X[0]))
        # Redefine lambda and alpha according to Dahlen's second definition
        f1 = self._function1(alpha, self._beta,  psiD, psi0)
        f2 = self._function2(psiD, psi0, phiB, phiD, lambdaB_D2, lambdaD_D2)
        f3 = self._function3(psi0, alpha_prime, phiB)
        return np.array([f1, f2, f3])

    def _derivative_matrix(self, F, X):
        """Approximation of derivative of F.
        Return a 3×3 matrix of approx. of partial derivatives.
        """
        M = np.zeros((3, 3))
        for j in range(3):
            Y = X.copy()
            Y[j] += self._h
            DF = self._function_to_root(Y)
            for i in range(3):
                M[i][j] = DF[i] - F[i]
            # M[:, j] = DF - F
        return M / self._h

    def _newton_rapson_solve(self, X):
        count = 0
        F = self._function_to_root(X)
        while not (abs(F) < self._numtol).all():
            count += 1
            M = self._derivative_matrix(F, X)  # Approx. of derivative.
            invM = np.linalg.inv(M)
            X = X - invM.dot(F)  # Newton-Rapson iteration.
            F = self._function_to_root(X)
            if count > 99:
                # print("!!!WARNING: More than 99 iteration to converge")
                # print("    Current value is:", r2d(X[0]))
                return float('nan')
        return X[0]

    # 'Public' methods ########################################################


    def compute_beta_old(self, deg=True):
        """Get critical basal slope beta as ECCW.
        Return the 2 possible solutions in tectonic or  collapsing regime.
        Return two None if no physical solutions.
        """
        self._check_params()
        betas = list()
        # weird if statement because asin in PSI_D is your ennemy !
        if -self._phiB <= self._alpha_prime <= self._phiB:
            psi0_1, psi0_2 = self._PSI_0(self._alpha_prime, self._phiB)
            psiD_11, psiD_12 = self._PSI_D(psi0_1, self._phiB, self._phiD,
                                           self._lambdaB_D2, self._lambdaD_D2)
            psiD_21, psiD_22 = self._PSI_D(psi0_2, self._phiB, self._phiD,
                                           self._lambdaB_D2, self._lambdaD_D2)
            beta_dl = psiD_11 - psi0_1 - self._alpha
            beta_ur = psiD_12 - psi0_1 - self._alpha
            beta_dr = psiD_21 - psi0_2 - self._alpha + pi  # Don't ask why +pi
            beta_ul = psiD_22 - psi0_2 - self._alpha

            for b in [beta_dl, beta_dr, beta_ul, beta_ur]:
                if self._is_valid_taper(self._alpha, b):
                    betas.append(b)
            beta1, beta2 = min(betas), max(betas)
            if deg:
                beta1 = r2d(beta1) if beta1 else None
                beta2 = r2d(beta2) if beta2 else None
            return beta1, beta2
        else:
            return None, None

    def compute_beta(self, deg=True):
        """Get critical basal slope beta as ECCW.
        Return the 2 possible solutions in tectonic or  collapsing regime.
        Return two None if no physical solutions.
        """
        self._check_params()
        beta_dw, beta_up = list(), list()
        # weird if statement because asin in PSI_D is your ennemy !
        if -self._phiB <= self._alpha_prime <= self._phiB:
            psi0_1, psi0_2 = self._PSI_0(self._alpha_prime, self._phiB)
            psiD_11, psiD_12 = self._PSI_D(psi0_1, self._phiB, self._phiD,
                                           self._lambdaB_D2, self._lambdaD_D2)
            psiD_21, psiD_22 = self._PSI_D(psi0_2, self._phiB, self._phiD,
                                           self._lambdaB_D2, self._lambdaD_D2)
            beta_dl = psiD_11 - psi0_1 - self._alpha
            beta_ur = psiD_12 - psi0_1 - self._alpha
            beta_dr = psiD_21 - psi0_2 - self._alpha + pi  # Don't ask why +pi
            beta_ul = psiD_22 - psi0_2 - self._alpha

            for b in [beta_dl, beta_dr]:
                if self._is_valid_taper(self._alpha, b):
                    beta_dw.append(b)
            for b in [beta_ul, beta_ur]:
                if self._is_valid_taper(self._alpha, b):
                    beta_up.append(b)
            if deg:
                beta_dw = tuple(r2d(b) for b in beta_dw)
                beta_up = tuple(r2d(b) for b in beta_up)
            return beta_dw, beta_up
        else:
            return None, None

    def compute_alpha(self, deg=True):
        self._check_params()
        """Get critical topographic slope alpha as ECCW.
        Return the 2 possible solutions in tectonic or collapsing regime.
        Return two None if no physical solutions.
        """
        self._set_at_runtime = self._runtime_alpha
        # Inital value of alpha for Newton-Rapson solution.
        alpha = 0.
        # First solution of ECCW (lower).
        # Set initial values:
        psiD = pi
        psi0 = psiD - alpha - self._beta
        alpha1 = self._newton_rapson_solve([alpha, psiD, psi0])
        alpha1 = self._test_alpha(alpha1)
        # Second solution of ECCW (upper).
        # Set initial values:
        psiD = pi / 2.
        psi0 = psiD - alpha - self._beta
        alpha2 = self._newton_rapson_solve([alpha, psiD, psi0])
        alpha2 = self._test_alpha(alpha2)
        if deg:
            alpha1 = r2d(alpha1) if alpha1 else None
            alpha2 = r2d(alpha2) if alpha2 else None
        return alpha1, alpha2

    def compute_phiB(self, deg=True):
        self._check_params()
        self._set_at_runtime = self._runtime_phiB
        # Inital value of phiB for Newton-Rapson solution.
        phiB = pi/7.
        # First solution of ECCW (lower).
        # Set initial values:
        psiD = pi
        psi0 = psiD - self._alpha - self._beta
        phiB1 = self._newton_rapson_solve([phiB, psiD, psi0])
        phiB1 = self._test_phiB(phiB1)
        psiD = pi / 2.
        psi0 = psiD - self._alpha - self._beta
        phiB2 = self._newton_rapson_solve([phiB, psiD, psi0])
        phiB2 = self._test_phiB(phiB2)
        if deg:
            phiB1 = r2d(phiB1) if phiB1 else None
            phiB2 = r2d(phiB2) if phiB2 else None
        return phiB1, phiB2

    def compute_phiD(self, deg=True):
        self._check_params()
        self._set_at_runtime = self._runtime_phiD
        # Inital value of phiB for Newton-Rapson solution.
        phiD = pi/4.
        # First solution of ECCW (lower).
        # Set initial values:
        psiD = pi
        psi0 = psiD - self._alpha - self._beta
        phiD1 = self._newton_rapson_solve([phiD, psiD, psi0])
        phiD1 = self._test_phiD(phiD1)
        psiD = pi / 2.
        psi0 = psiD - self._alpha - self._beta
        phiD2 = self._newton_rapson_solve([phiD, psiD, psi0])
        phiD2 = self._test_phiD(phiD2)
        if deg:
            phiD1 = r2d(phiD1) if phiD1 else None
            phiD2 = r2d(phiD2) if phiD2 else None
        return phiD1, phiD2

    def compute(self, flag):
        parser = {
            "alpha": self.compute_alpha,
            "beta": self.compute_beta,
            "phiB": self.compute_phiB,
            "phiD": self.compute_phiD,
        }
        return parser[flag]()

    def show_params(self):
        out = self.__class__.__name__ + "(\n"
        for key, value in self.params_table().items():
            out += "  {:13} = {},\n".format(key, value)
        out += ")"
        print(out)

    def params_table(self):
        return OrderedDict([
            ("context", self.context),
            ("beta", self.beta),
            ("alpha", self.alpha),
            ("phiB", self.phiB),
            ("phiD", self.phiD),
            ("rho_f", self.rho_f),
            ("rho_sr", self.rho_sr),
            ("delta_lambdaB", self.delta_lambdaB),
            ("delta_lambdaD", self.delta_lambdaD),
            ])

    def set_params(self, **kwargs):
#        self.__dict__.update(kwargs)
        try:
            for key, value in kwargs.items():
                # print(key, value)
                if value is not None:
                    setattr(self, key, value)
        except TypeError:
            raise

    def set_no_fluids(self):
        self.set_params(rho_f=0, rho_sr=0, delta_lambdaB=0, delta_lambdaD=0)

if __name__ == "__main__":

    foo = EccwCompute()
    foo.show_params()

    foo = EccwCompute(phiB=30, phiD=10, beta=0, alpha=3.4365, context="c")
    foo.show_params()
    print("\ndry_inverse")
    print("alphas =", foo.compute("alpha"), "[%s]" % foo.alpha)
    print("betas  =", foo.compute("beta"), "[%s]" % foo.beta)
    print("phiB =", foo.compute("phiB"), "[%s]" % foo.phiB)
    print("phiD =", foo.compute("phiD"), "[%s]" % foo.phiD)

    foo.set_params(phiB=30, phiD=10, beta=0, alpha=23.9463194, context="c")
    print("\ndry_normal - set")
    print("alphas =", foo.compute("alpha"), "[%s]" % foo.alpha)
    print("betas  =", foo.compute("beta"), "[%s]" % foo.beta)
    print("phiB =", foo.compute("phiB"), "[%s]" % foo.phiB)
    print("phiD =", foo.compute("phiD"), "[%s]" % foo.phiD)

    foo = EccwCompute(phiB=30, phiD=10, beta=0, alpha=23.9463194, context="c")
    print("\ndry_normal - init")
    print("alphas =", foo.compute("alpha"), "[%s]" % foo.alpha)
    print("betas  =", foo.compute("beta"), "[%s]" % foo.beta)
    print("phiB =", foo.compute("phiB"), "[%s]" % foo.phiB)
    print("phiD =", foo.compute("phiD"), "[%s]" % foo.phiD)

    foo = EccwCompute(phiB=30, phiD=10, alpha=0., context="c")
    print("\nbetas")
    print("alpha =   0., betas =", foo.compute("beta"))
    foo.alpha = 20
    print("alpha =  20., betas =", foo.compute("beta"))
    foo.alpha = -20
    print("alpha = -20., betas =", foo.compute("beta"))

    # foo = EccwCompute(phiB=30, phiD=10, beta=20, alpha=9.4113, context="e")
    # foo = EccwCompute(phiB=30, phiD=10, beta=0, alpha=3.8353, context="c",
    #                       rho_f=1000, rho_sr=3500,
    #                       delta_lambdaB=0.50, delta_lambdaD=0.3)
    # print("\nfluids_inverse")
    # print("alphas =", foo.compute("alpha"), "[%s]" % foo.alpha)
    # print("betas  =", foo.compute("beta"), "[%s]" % foo.beta)
    # print("phiB =", foo.compute("phiB"), "[%s]" % foo.phiB)
    # print("phiD =", foo.compute("phiD"), "[%s]" % foo.phiD)
    # 
    # 
    # foo = EccwCompute(phiB=30, phiD=10, beta=0, alpha=6.76084021, context="c",
    #                       rho_f=1000, rho_sr=3500,
    #                       delta_lambdaB=0.50, delta_lambdaD=0.3)
    # # print("\nextension")
    # print("\nfluids_normal")
    # print("alphas =", foo.compute("alpha"), "[%s]" % foo.alpha)
    # print("betas  =", foo.compute("beta"), "[%s]" % foo.beta)
    # print("phiB =", foo.compute("phiB"), "[%s]" % foo.phiB)
    # print("phiD =", foo.compute("phiD"), "[%s]" % foo.phiD)

    foo.show_params()
    print(str(foo))
    
