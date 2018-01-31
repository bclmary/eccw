#!/usr/bin/env python3
# -*-coding:utf-8 -*

from setuptools import setup, find_packages

setup(
    entry_points={'console_scripts': [
        'eccw=eccw.bin.eccw:main',
        ],
    },
    # Auto scanning package
    packages=find_packages(),
    # Use MANIFEST.in for custom packaging
    include_package_data=True,
    )
