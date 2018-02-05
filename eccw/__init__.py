#!/usr/bin/env python3
# -*-coding:utf-8 -*

"""
Main eccw library.
"""

import pkg_resources
from os import path
from setuptools.config import read_configuration

from eccw.physics.eccw_compute import EccwCompute
from eccw.physics.eccw_plot import EccwPlot


def _extract_metadata(package_name, metadata_name):
    try:
        # ECCW is installed with pip.
        return getattr(pkg_resources.get_distribution(package_name), metadata_name)
    except (AttributeError, pkg_resources.DistributionNotFound):
        # Not installed ? Go read what you need at proper place.
        _conf = read_configuration(path.join(
            path.dirname(path.dirname(__file__)), 'setup.cfg')
            )
        return _conf['metadata'][metadata_name]


__version__ = _extract_metadata("eccw", "version")

__location__ = _extract_metadata("eccw", "location")

__authors__ = [
    'BCL Mary',
    'Xiaoping Yuan',
    'YM Leroy',
    'Pauline Souloumiac',
    'Chong Wu',
    ]

__license__ = "GNU GPL-v3"

__url__ = "https://github.com/bclmary"

__contact__ = "bclmary@mailoo.org"


__all__ = [
    'EccwCompute',
    'EccwPlot',
    ]

