#!/usr/bin/env python3
# -*-coding:utf-8 -*

from setuptools import setup, find_packages

MAJOR = 2
MINOR = 0
PATCH = 0
VERSION = "{}.{}.{}".format(MAJOR, MINOR, PATCH)

AUTHORS = (
    "BCL Mary",
    "Xiaoping Yuan",
    "YM Leroy",
    "Pauline Souloumiac",
    "Chong Wu",
    )

# Set version.py
with open("eccw/version.py", "w") as f:
    f.write("__version__ = '{}'\n".format(VERSION))

# Set authors.py
with open("eccw/authors.py", "w") as f:
    pad = " " * 4
    text = "__authors_list__ = [\n" + pad + "{}\n" + pad + "]\n"
    joiner = ",\n" + pad
    f.write(text.format(joiner.join(AUTHORS)))
    f.write("__authors__ = ', '.join(__authors_list__)\n")

# # Get version
# with open('eccw/version.py') as f:
#     exec(f.read())
#     f.close()
# # Get authors
# with open('eccw/authors.py') as f:
#     exec(f.read())
#     f.close()

setup(
    name='eccw',
    version=VERSION,
    description='Exact Critical Coulomb Wedge',
    long_description='Tools to compute and display the exact solution of any'
                     'parameter of Critical Coulomb Wedge',
    keywords=['Geology', 'accretionnary prism'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: X11 Applications :: Qt',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering ::  Geology',
        ],
    url='http://github.com/???',
    authors=AUTHORS,
    author_email='bclmary@mailoo.org',
    license='MIT',
    packages=find_packages(exclude=['doc', 'test*']),
    install_requires=[
        'all',
        'needed',
        'third',
        'party',
        'numpy>=1.0,<1.13'
        ],
    include_package_data=True,
    # scripts=['bin/eccw'],
    entry_points={'console_scripts': [
        'eccw=bin.eccw:main',
        ],
    },
    zip_safe=False,
    # test_suite='nose.collector',
    # tests_require=['nose'],
    )
