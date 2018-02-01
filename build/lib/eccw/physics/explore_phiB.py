#!/usr/bin/env python3
# -*-coding:utf-8 -*

"""
Explore values returned by EccwCompute object for phiB parameter.
"""

import numpy as np
from math import pi, tan, atan, cos, sin, sqrt, asin
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from eccw.physics.eccw_compute import EccwCompute
from eccw.shared.tools import d2r, r2d, imin, imax


def fun(b, a, foo):
    foo.beta = b
    foo.alpha = a
    x1, x2 = foo.compute("phiB")
    return x1


foo = EccwCompute(phiB=30, phiD=10, context="c")
amin, amax, astep = -10, 10, 1
bmin, bmax, bstep = -10, 20, 1

fig = plt.figure()
ax = Axes3D(fig)

alphas = np.arange(amin, amax, astep)
betas = np.arange(bmin, bmax, bstep)
X, Y = np.meshgrid(betas, alphas)
zs = np.array([fun(x, y, foo) for x, y in zip(np.ravel(X), np.ravel(Y))])
Z = zs.reshape(X.shape)

X, Y = np.meshgrid(betas, alphas)
ax.plot_surface(X, Y, Z)

ax.set_xlabel('beta')
ax.set_ylabel('alpha')
ax.set_zlabel('phiB')

plt.show()
