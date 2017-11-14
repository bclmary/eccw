#!/usr/bin/env python3
# -*-coding:utf-8 -*

from setuptools import setup

# TODO : some stuffs


def myfunc(a):
    """poulpe. """
    return a+1


setup(
    name='eccw',
    version='2.0',
    description='Exact Critical Coulomb Wedge',
    long_description='Tools to compute and display the exact solution of any'
                     'parameter of Critical Coulomb Wedge',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: X11 Applications :: Qt',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering ::  Geology',
        ],
    url='http://github.com/???',
    author='BCL Mary',
    author_email='bclmary@mailoo.org',
    license='MIT',
    packages=['eccw'],
    install_requires=[
        'all',
        'needed',
        'third',
        'party'
        ],
    scripts=['bin/eccw'],
    zip_safe=False,
    include_package_data=True,
    # test_suite='nose.collector',
    # tests_require=['nose'],
    )
