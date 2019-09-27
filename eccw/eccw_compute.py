#!/usr/bin/env python3
# -*-coding:utf-8 -*

"""
Elements dedicated to solve physics.
"""

import numpy as np
from math import pi, cos, sin, tan, atan, asin, nan, inf, degrees, radians
from collections import OrderedDict


class EccwCompute(object):
    """
    Solve any parameter of the critical coulomb wedge.

    Based on [Yuan, 2015], https://doi.org/10.1002/2014JB011612
    """

    # _numtol = 1e-12  # Convergence with 5 digits after degrees conversion.
    _numtol = 1e-15  # Convergence with 8 digits after degrees conversion.
    _h = 1e-6  # Arbitrary small value
    _main_params_list = ["alpha", "beta", "phiB", "phiD"]

    def reset(self):
        """Set all parameters to an (meaningless) initial state."""
        self._sign = 1  # Determine context: +1 for compression, -1 for extension.
        self._beta = nan
        self._alpha = nan
        self._phiB = nan
        self._phiD = nan
        self._rho_f = 0.0
        self._rho_sr = 0.0
        self._density_ratio = 0.0
        self._delta_lambdaB = 0.0
        self._delta_lambdaD = 0.0
        self._lambdaB = 0.0  # lambdaB parametrized as Yuan, 2015
        self._lambdaD = 0.0  # lambdaD parametrized as Yuan, 2015
        self._lambdaB_D2 = 0.0  # lambdaB parametrized as Dahlen, 1984
        self._lambdaD_D2 = 0.0  # lambdaD parametrized as Dahlen, 1984
        self._taper_min = -self._numtol
        self._taper_max = +inf

    def __init__(self, **kwargs):
        """See 'Data descriptors' section of help for available named parameters."""
        self.reset()
        self.set_params(**kwargs)

    def __repr__(self):
        out = self.__class__.__name__ + "("
        for key, value in self.params_table().items():
            out += "{}={}, ".format(key, repr(value))
        out = out[:-2] + ")"
        return out

    ## Properties (aka descriptors) ###########################################

    @property
    def alpha(self):
        """Surface slope [deg], positive downward."""
        return degrees(self._alpha)

    @alpha.setter
    def alpha(self, value):
        try:
            self._alpha = radians(value)
            self._lambdaD_D2 = self._convert_lambda(self._alpha, self._lambdaD)
            self._lambdaB_D2 = self._convert_lambda(self._alpha, self._lambdaB)
            self._alpha_prime = self._convert_alpha(self._alpha, self._lambdaB_D2)
        except TypeError:
            raise TypeError(self._error_message("alpha", "type", "a float"))

    @property
    def beta(self):
        """Basal slope [deg], positive upward."""
        return degrees(self._beta)

    @beta.setter
    def beta(self, value):
        try:
            self._beta = radians(value)
        except TypeError:
            raise TypeError(self._error_message("beta", "type", "a float"))

    @property
    def phiB(self):
        """Bulk friction angle [deg], positive."""
        return degrees(self._phiB)

    @phiB.setter
    def phiB(self, value):
        if value < 0:
            raise TypeError(self._error_message("phiB", "sign", "> 0"))
        if value == 0:
            raise TypeError(self._error_message("phiB", "value", "non zero"))
        try:
            self._phiB = radians(value)
        except TypeError:
            raise TypeError(self._error_message("phiB", "type", "a float"))

    @property
    def phiD(self):
        """Basal friction angle [deg], positive."""
        return degrees(self._sign * self._phiD)

    @phiD.setter
    def phiD(self, value):
        if value < 0:
            raise TypeError(self._error_message("phiD", "sign", ">= 0"))
        try:
            self._phiD = radians(value) * (self._sign if self._sign else 1.0)
            self._taper_max = pi / 2.0 - self._phiD + self._numtol
        except TypeError:
            raise TypeError(self._error_message("phiD", "type", "a float"))

    @property
    def context(self):
        """Tectonic context: 'compression' or 'extension' (shortcuts: 'c' or 'e')."""
        if self._sign == 1:
            return "Compression"
        elif self._sign == -1:
            return "Extension"
        else:
            return None

    @context.setter
    def context(self, value):
        errmessage = self._error_message(
            "context", "value", "'compression' or 'extension'"
        )
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
        self._taper_max = pi / 2.0 - self._phiD + self._numtol

    @property
    def rho_f(self):
        """Volumetric mass density of fluids."""
        return self._rho_f

    @rho_f.setter
    def rho_f(self, value):
        try:
            self._rho_f = value + 0.0  # +0 test value is a float.
            self._set_density_ratio()
            self._set_lambdaB()
            self._set_lambdaD()
        except TypeError:
            raise TypeError(self._error_message("rho_f", "type", "a float"))

    @property
    def rho_sr(self):
        """Volumetric mass density of saturated rock."""
        return self._rho_sr

    @rho_sr.setter
    def rho_sr(self, value):
        try:
            self._rho_sr = value + 0.0  # +0 test value is a float.
            self._set_density_ratio()
            self._set_lambdaB()
            self._set_lambdaD()
        except TypeError:
            raise TypeError(self._error_message("rho_sr", "type", "a float"))

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
            raise TypeError(self._error_message("delta_lambdaB", "type", "a float"))

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
            raise TypeError(self._error_message("delta_lambdaD", "type", "a float"))

    ## 'Private' methods ######################################################

    def _check_params(self) -> None:
        """Raise error(s) if fluid related parameters are not set correctly."""
        out = self.check_params()
        if out:
            raise ValueError(out)

    def check_params(self) -> str:
        """Ckeck sanity of fluid related parameters."""
        errors = ""
        if not (0.0 <= self._delta_lambdaD < 1 - self._density_ratio):
            errors += self._error_message(
                "delta_lambdaD", "value", "in [0 : %s]\n" % (1 - self._density_ratio)
            )
        if not (0.0 <= self._delta_lambdaB <= 1 - self._density_ratio):
            errors += self._error_message(
                "delta_lambdaB", "value", "in [0 : %s]\n" % (1 - self._density_ratio)
            )
        return errors

    def _error_message(self, who: str, problem: str, solution: str) -> str:
        """Error message formater."""
        class_name = self.__class__.__name__
        return "%s() gets wrong %s for '%s': must be %s" % (
            class_name,
            problem,
            who,
            solution,
        )

    def _set_density_ratio(self) -> None:
        """Ratio of mass densities of fluids over saturated rock.
        Equivalent to hydrostatic pressure.
        """
        self._density_ratio = self._rho_f / self._rho_sr if self._rho_sr != 0.0 else 0.0
        # foo = 1 - self._density_ratio
        # if foo < self.delta_lambdaB:
        #     raise ValueError(self._error_message("delta_lambdaB' after setting"
        #                                          "'rho_f' or rho_sr'", "value",
        #                                          "lower than %s" % foo))
        # if foo < self.delta_lambdaD:
        #     raise ValueError(self._error_message("delta_lambdaD' after setting"
        #                                          "'rho_f' or rho_sr'", "value",
        #                                          "lower than %s" % foo))

    def _set_lambdaD(self) -> None:
        self._lambdaD = self._delta_lambdaD + self._density_ratio
        self._lambdaD_D2 = self._convert_lambda(self._alpha, self._lambdaD)

    def _set_lambdaB(self) -> None:
        self._lambdaB = self._delta_lambdaB + self._density_ratio
        self._lambdaB_D2 = self._convert_lambda(self._alpha, self._lambdaB)
        self._alpha_prime = self._convert_alpha(self._alpha, self._lambdaB_D2)

    def _convert_lambda(self, alpha: float, lambdaX: float) -> float:
        """Convert lambda paramétrization from [Hubbert and Rubey, 1959]'s to [Dahlen, 1984]'s.
        From [Yuan, 2015]: reverse equation of equation (A3).
        """
        # Naive writing.
        # return lambdaX / cos(alpha) ** 2. - self._density_ratio * tan(alpha) ** 2.
        # Less computation versions.
        return self._density_ratio + (lambdaX - self._density_ratio) / cos(alpha) ** 2.0
        # return lambdaX + (lambdaX - self._density_ratio) * tan(alpha) ** 2.

    def _convert_alpha(self, alpha: float, lambdaB_D2: float) -> float:
        """Compute alpha prime as [Yuan, 2015], equation (B6)."""
        return atan((1 - self._density_ratio) / (1 - lambdaB_D2) * tan(alpha))

    def _PSI_D(
        self,
        psi0: float,
        phiB: float,
        phiD: float,
        lambdaB_D2: float,
        lambdaD_D2: float,
    ) -> float:
        """Compute psi_D as [Yuan, 2015], equation (B6)."""
        tmp = (1.0 - lambdaD_D2) * sin(phiD) / (1.0 - lambdaB_D2) / sin(phiB)
        tmp += (
            (lambdaD_D2 - lambdaB_D2) * sin(phiD) * cos(2.0 * psi0) / (1.0 - lambdaB_D2)
        )
        if tmp > 1:
            return 0.0, 0.0  # TODO
        return (asin(tmp) - phiD) * 0.5, (pi - asin(tmp) - phiD) * 0.5

    def _PSI_0(self, alpha_prime: float, phiB: float) -> float:
        """Compute psi_0 as [Yuan, 2015], equ (B6)."""
        tmp = sin(alpha_prime) / sin(phiB)
        return ((asin(tmp) - alpha_prime) * 0.5, (pi - asin(tmp) - alpha_prime) * 0.5)

    def _is_valid_taper(self, a: float, b: float) -> bool:
        return self._taper_min < a + b < self._taper_max

    def _test_alpha(self, a: float) -> "float or None":
        """Test if an alpha solution is physically meaningfull."""
        return a if self._is_valid_taper(a, self._beta) else None

    def _test_phiB(self, phiB: float) -> "float or None":
        """Test if a phiB solution is physically meaningfull."""
        # return phiB if -pi < phiB < pi else None
        return phiB if -self._numtol < phiB < pi + self._numtol else None

    def _test_phiD(self, phiD: float) -> "float or None":
        """Test if a phiD solution is physically meaningfull."""
        # return abs(phiD) if phiD is not nan else None
        # return phiD if phiD is not nan else None
        return phiD if -self._numtol < phiD < self._phiB + self._numtol else None

    def _degrees_if_not_none(self, value: "float or None") -> "float or None":
        return degrees(value) if value is not None else None

    def _runtime_alpha(self, alpha: float) -> tuple:
        """return a set of values disconnected from self's attributes.

        The set of returned values is : 
        (alpha, phiB, phiD, lambdaB_D2, lambdaD_D2, alpha_prime)
        This function takes a value of alpha disconnected from self.alpha, 
        and re-compute the other values which are alpha dependants.
        """
        lambdaB_D2 = self._convert_lambda(alpha, self._lambdaB)
        lambdaD_D2 = self._convert_lambda(alpha, self._lambdaD)
        alpha_prime = self._convert_alpha(alpha, lambdaB_D2)
        return (alpha, self._phiB, self._phiD, lambdaB_D2, lambdaD_D2, alpha_prime)

    def _runtime_phiB(self, phiB: float) -> tuple:
        """return a set of values disconnected from self's attributes.

        The set of returned values is : 
        (alpha, phiB, phiD, lambdaB_D2, lambdaD_D2, alpha_prime)
        This function takes a value of phiB disconnected from self.phiB.
        """
        return (
            self._alpha,
            phiB,
            self._phiD,
            self._lambdaB_D2,
            self._lambdaD_D2,
            self._alpha_prime,
        )

    def _runtime_phiD(self, phiD: float) -> tuple:
        """return a set of values disconnected from self's attributes.

        The set of returned values is : 
        (alpha, phiB, phiD, lambdaB_D2, lambdaD_D2, alpha_prime)
        This function takes a value of phiD disconnected from self.phiD.
        """
        return (
            self._alpha,
            self._phiB,
            phiD,
            self._lambdaB_D2,
            self._lambdaD_D2,
            self._alpha_prime,
        )

    def _function1(self, alpha: float, beta: float, psiD: float, psi0: float) -> float:
        """First sub-function of function to root."""
        return alpha + beta - psiD + psi0

    def _function2(
        self,
        psiD: float,
        psi0: float,
        phiB: float,
        phiD: float,
        lambdaB_D2: float,
        lambdaD_D2: float,
    ) -> float:
        """Second sub-function of function to root."""
        if phiB == 0:
            print("!!!ERROR phiB == 0.")
        f = sin(2 * psiD + phiD)
        f -= (1 - lambdaD_D2) * sin(phiD) / (1 - lambdaB_D2) / sin(phiB)
        f -= (lambdaD_D2 - lambdaB_D2) * sin(phiD) * cos(2 * psi0) / (1 - lambdaB_D2)
        return f

    def _function3(self, psi0: float, alpha_prime: float, phiB: float) -> float:
        """Third sub-function of function to root."""
        return sin(2 * psi0 + alpha_prime) * sin(phiB) - sin(alpha_prime)

    def _function_to_root(self, X: np.array, runtime_var: "function") -> np.array:
        """Function of wich we are searching the roots.
        Gets an array X of length 3 as input.
        Return an array of length 3.
        """
        # Unpack input X.
        # variable is the value to solve: if we want to solve alpha, variable = alpha.
        variable, psiD, psi0 = X
        # Get needed values, disconnected from self's attributes.
        # '_set_at_runtime' method must be defined before to call this method.
        alpha, phiB, phiD, lambdaB_D2, lambdaD_D2, alpha_prime = runtime_var(variable)
        # In this context (solving alpha, phiD or phiB), beta is a constant.
        return np.array(
            (
                self._function1(alpha, self._beta, psiD, psi0),
                self._function2(psiD, psi0, phiB, phiD, lambdaB_D2, lambdaD_D2),
                self._function3(psi0, alpha_prime, phiB),
            )
        )

    def _derivative_matrix(
        self, F: np.array, X: np.array, runtime_var: "function"
    ) -> np.array:
        """Approximation of derivative of F.
        Return a 3×3 matrix of approx. of partial derivatives.
        """
        M = np.zeros((3, 3))
        for j in range(3):
            Y = X.copy()
            Y[j] += self._h
            DF = self._function_to_root(Y, runtime_var)
            # for i in range(3):
            #    M[i][j] = DF[i] - F[i]
            M[:, j] = DF - F
        return M / self._h

    def _newton_raphson_solve(self, X: tuple, runtime_var: "function") -> float:
        """
        Solve the "function to root" iteratively using Newton/Raphson's method.
        
        Solve is made accordingly with parameter X (array of size 3).
        Function to root takes X as an input and return an array of same size.
        """
        count = 0
        X = np.array(X)
        F = self._function_to_root(X, runtime_var)
        if __debug__:
            self.path = [X]
            self.iter_conv = 0
        while not (abs(F) < self._numtol).all():
            count += 1
            M = self._derivative_matrix(F, X, runtime_var)  # Approx. of derivative.
            invM = np.linalg.inv(M)
            X = X - invM.dot(F)  # Newton-Raphson iteration.
            if __debug__:
                self.path.append(X)
                self.iter_conv = count
            F = self._function_to_root(X, runtime_var)
            if count > 999:
                raise RuntimeError(
                    f"""Error in {self.__class__.__name__}._newton_raphson_solve
                    More than 99 iterations to converge.
                    Current values (in rad) are: 
                      var  = {X[0]}
                      psiD = {X[1]}
                      psi0 = {X[2]}
                    """
                )
        return X[0] if abs(X[0]) > self._numtol else 0.0
        # return X[0]

    ## 'Public' methods #######################################################

    def compute_beta_old(self, deg=True) -> tuple:
        """Get critical basal slope beta as ECCW.
        Return the 2 possible solutions in tectonic or  collapsing regime.
        Return two None if no physical solutions.
        """
        self._check_params()
        # weird if statement because asin in PSI_D is your ennemy !
        if -self._phiB <= self._alpha_prime <= self._phiB:
            psi0_1, psi0_2 = self._PSI_0(self._alpha_prime, self._phiB)
            psiD_11, psiD_12 = self._PSI_D(
                psi0_1, self._phiB, self._phiD, self._lambdaB_D2, self._lambdaD_D2
            )
            psiD_21, psiD_22 = self._PSI_D(
                psi0_2, self._phiB, self._phiD, self._lambdaB_D2, self._lambdaD_D2
            )
            beta_dl = psiD_11 - psi0_1 - self._alpha
            beta_ur = psiD_12 - psi0_1 - self._alpha
            beta_dr = psiD_21 - psi0_2 - self._alpha + pi  # Don't ask why +pi
            beta_ul = psiD_22 - psi0_2 - self._alpha

            betas = tuple(
                b for b in [beta_dl, beta_dr, beta_ul, beta_ur] 
                if self._is_valid_taper(self._alpha, b)
            )
            beta1, beta2 = min(betas), max(betas)
            if deg:
                beta1 = self._degrees_if_not_none(beta1)
                beta2 = self._degrees_if_not_none(beta2)
            return beta1, beta2
        else:
            return None, None

    def compute_beta(self, deg=True) -> tuple:
        """Get critical basal slope beta as ECCW.

        Return the 2 possible solutions in two tuples respectively representing
        tectonic and collapsing regime. The solutions can be in the same tuple, or
        one in each tuple.

        Return two empty tuples if no physical solutions exist.

        .. note:: it may occurs that one of the solutions is a double solution
            that is on both tectonic and collapsing regime (for a given phiB, phiD 
            values, two double solutions exist). In that case, the double solution
            appears in both returned tuples, so 3 solutions are displayed.

        Summary of possible sets of returned solutions :
        
        * 2 tectonic solutions : (x, y), ()
        * 1 tectonic and 1 collapsing : (x,), (y,)
        * 2 collapsing solutions : (), (x, y)
        * 1 double solution and 1 collapsing : (x,), (x, y)
        * 1 tectonic  and 1 double solution : (x, y), (y, )
        * no solutions : (), ()
        """
        self._check_params()
        # weird if statement because asin in PSI_D is your ennemy !
        if -self._phiB <= self._alpha_prime <= self._phiB:
            psi0_1, psi0_2 = self._PSI_0(self._alpha_prime, self._phiB)
            psiD_11, psiD_12 = self._PSI_D(
                psi0_1, self._phiB, self._phiD, self._lambdaB_D2, self._lambdaD_D2
            )
            psiD_21, psiD_22 = self._PSI_D(
                psi0_2, self._phiB, self._phiD, self._lambdaB_D2, self._lambdaD_D2
            )
            beta_dl = psiD_11 - psi0_1 - self._alpha
            beta_ur = psiD_12 - psi0_1 - self._alpha
            beta_dr = psiD_21 - psi0_2 - self._alpha + pi  # Don't ask why +pi
            beta_ul = psiD_22 - psi0_2 - self._alpha

            beta_dw = tuple(
                b for b in [beta_dl, beta_dr] if self._is_valid_taper(self._alpha, b)
            )
            beta_up = tuple(
                b for b in [beta_ul, beta_ur] if self._is_valid_taper(self._alpha, b)
            )
            if deg:
                beta_dw = tuple(degrees(b) for b in beta_dw)
                beta_up = tuple(degrees(b) for b in beta_up)
            return beta_dw, beta_up
        else:
            return tuple(), tuple()

    def compute_alpha(self, deg=True) -> tuple:
        """Get critical topographic slope alpha as ECCW.
        Return the 2 possible solutions in tectonic or collapsing regime.
        Return two None if no physical solutions.
        """
        self._check_params()
        # Inital values for Newton-Raphson solution.
        alpha, psiD, psi0 = 0.0, 0.0, 0.0
        # First solution of ECCW (lower).
        alpha1 = self._newton_raphson_solve([alpha, psiD, psi0], self._runtime_alpha)
        alpha1 = self._test_alpha(alpha1)
        # Other inital values for Newton-Raphson solution.
        alpha, psiD, psi0 = 0.0, self._sign * pi / 2.0, self._sign * pi / 4.0
        # Second solution of ECCW (upper).
        alpha2 = self._newton_raphson_solve([alpha, psiD, psi0], self._runtime_alpha)
        alpha2 = self._test_alpha(alpha2)
        if deg:
            alpha1 = self._degrees_if_not_none(alpha1)
            alpha2 = self._degrees_if_not_none(alpha2)
        return alpha1, alpha2

    def compute_phiB(self, deg=True) -> tuple:
        self._check_params()
        # Inital values for Newton-Raphson solution.
        phiB = pi / 7.0
        psiD = pi
        psi0 = psiD - self._alpha - self._beta
        # First solution of ECCW (lower).
        phiB1 = self._newton_raphson_solve([phiB, psiD, psi0], self._runtime_phiB)
        phiB1 = self._test_phiB(phiB1)
        # Other inital values for Newton-Raphson solution.
        phiB = pi / 7.0
        psiD = pi / 2.0
        psi0 = psiD - self._alpha - self._beta
        # Second solution of ECCW (upper).
        phiB2 = self._newton_raphson_solve([phiB, psiD, psi0], self._runtime_phiB)
        phiB2 = self._test_phiB(phiB2)
        if deg:
            phiB1 = self._degrees_if_not_none(phiB1)
            phiB2 = self._degrees_if_not_none(phiB2)
        return phiB1, phiB2

    def compute_phiD(self, deg=True) -> tuple:
        self._check_params()
        # Inital values for Newton-Raphson solution.
        phiD = pi / 4.0
        psiD = pi
        psi0 = psiD - self._alpha - self._beta
        # First solution of ECCW (lower).
        phiD1 = self._newton_raphson_solve([phiD, psiD, psi0], self._runtime_phiD)
        phiD1 = self._test_phiD(phiD1)
        # Other inital values for Newton-Raphson solution.
        phiD = pi / 4.0
        psiD = pi / 2.0
        psi0 = psiD - self._alpha - self._beta
        # Second solution of ECCW (upper).
        phiD2 = self._newton_raphson_solve([phiD, psiD, psi0], self._runtime_phiD)
        phiD2 = self._test_phiD(phiD2)
        if deg:
            phiD1 = self._degrees_if_not_none(phiD1)
            phiD2 = self._degrees_if_not_none(phiD2)
        return phiD1, phiD2

    def compute(self, flag: str) -> tuple:
        """Compute solution for given parameter.
        Parameter is a string value among: 'alpha', 'beta', 'phiB' or 'phiD'.
        """
        parser = {
            "alpha": self.compute_alpha,
            "beta": self.compute_beta,
            "phiB": self.compute_phiB,
            "phiD": self.compute_phiD,
        }
        return parser[flag]()

    def show_params(self) -> None:
        out = self.__class__.__name__ + "(\n"
        for key, value in self.params_table().items():
            out += "  {:13} = {},\n".format(key, value)
        out += ")"
        print(out)

    def params_table(self) -> OrderedDict:
        return OrderedDict(
            [
                ("context", self.context),
                ("beta", self.beta),
                ("alpha", self.alpha),
                ("phiB", self.phiB),
                ("phiD", self.phiD),
                ("rho_f", self.rho_f),
                ("rho_sr", self.rho_sr),
                ("delta_lambdaB", self.delta_lambdaB),
                ("delta_lambdaD", self.delta_lambdaD),
            ]
        )

    def set_params(self, **kwargs) -> None:
        try:
            for key, value in kwargs.items():
                if value is not None:
                    setattr(self, key, value)
        except TypeError:
            raise

    def set_no_fluids(self) -> None:
        """Shortcut of set_params method with all fluid parameters set to zero."""
        self.set_params(rho_f=0, rho_sr=0, delta_lambdaB=0, delta_lambdaD=0)


if __name__ == "__main__":

    foo = EccwCompute()
    #    foo.show_params()

    #    foo = EccwCompute(phiB=30, phiD=10, beta=0, alpha=3.4365, context="c")
    #    foo.show_params()
    #    print("\ndry_inverse")
    #    print("alphas =", foo.compute("alpha"), "[%s]" % foo.alpha)
    #    print("betas  =", foo.compute("beta"), "[%s]" % foo.beta)
    #    print("phiB =", foo.compute("phiB"), "[%s]" % foo.phiB)
    #    print("phiD =", foo.compute("phiD"), "[%s]" % foo.phiD)
    #
    #    foo.set_params(phiB=30, phiD=10, beta=0, alpha=23.9463194, context="c")
    #    print("\ndry_normal - set")
    #    print("alphas =", foo.compute("alpha"), "[%s]" % foo.alpha)
    #    print("betas  =", foo.compute("beta"), "[%s]" % foo.beta)
    #    print("phiB =", foo.compute("phiB"), "[%s]" % foo.phiB)
    #    print("phiD =", foo.compute("phiD"), "[%s]" % foo.phiD)
    #
    #    foo = EccwCompute(phiB=30, phiD=10, beta=0, alpha=23.9463194, context="c")
    #    print("\ndry_normal - init")
    #    print("alphas =", foo.compute("alpha"), "[%s]" % foo.alpha)
    #    print("betas  =", foo.compute("beta"), "[%s]" % foo.beta)
    #    print("phiB =", foo.compute("phiB"), "[%s]" % foo.phiB)
    #    print("phiD =", foo.compute("phiD"), "[%s]" % foo.phiD)
    #
    #    foo = EccwCompute(phiB=30, phiD=10, alpha=0., context="c")
    #    print("\nbetas")
    #    print("alpha =   0., betas =", foo.compute("beta"))
    #    foo.alpha = 20
    #    print("alpha =  20., betas =", foo.compute("beta"))
    #    foo.alpha = -20
    #    print("alpha = -20., betas =", foo.compute("beta"))

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

    #    foo.show_params()
    #    print(str(foo))

    foo = EccwCompute(phiB=30, beta=0)
    for phiD in [x * 0.10000 for x in range(270, 301)]:
        foo.phiD = phiD
        print(f"phiD={round(foo.phiD,3)}", foo.compute_alpha())

    print()

    foo = EccwCompute(phiB=30, beta=0)
    for alpha in [x * 0.10000 for x in range(0, 50)]:
        foo.alpha = alpha
        print(f"alpha={round(foo.alpha,3)}", foo.compute_phiD())

    # foo._draw_full_solution_alpha(64)
    # foo._draw_map_solution_alpha()

#    for phiD in range(0, 31):
#        foo.phiD = phiD
#        c1, c2 = foo._draw_map_solution(32)
#        print(phiD, c1, c2)


# foo._draw_full_solution_given_alpha(13.669311606640086)
# foo._draw_full_solution_given_alpha(24.869179540184476)

# test(29)
# foo._draw_full_solution_alpha(64)
# foo._draw_full_solution_given_alpha(15.204367691585336)
# foo._draw_full_solution_given_alpha(20)

# X = [13.669311606640086, 200.93740947118232, 187.26809786454226]
# X = [24.869179540184476, 41.062590530584281, 16.193410990399805]
# X = [radians(x) for x in X]
# print(foo._function_to_root(X))

#    foo.alpha=12
#    print(foo.compute_beta())
