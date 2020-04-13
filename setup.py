# Filename: setup.py

import os
import sys
from os.path import join as pjoin

import myeda

try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension

NAME = myeda.__name__

VERSION = myeda.__version__

AUTHOR = "Philipp van Kempen"

AUTHOR_EMAIL = "philipp DOT van DASH kempen AT tum DOT de"

DESCRIPTION = "Electronic Design Automation Helper Scripts making use of cjdrake/pyeda and tpircher/quine-mccluskey"

KEYWORDS = [
    "Boolean algebra",
    "digital logic",
    "EDA",
    "electronic design automation",
    "Quine McCluskey",
    "logic",
    "cube diagram",
    "cover table",
    "truth table",
    "logic minimization",
]

with open('README.md') as fin:
    README = fin.read()

with open('LICENSE') as fin:
    LICENSE = fin.read()

URL = "https://github.com/PhilippvK/python-myeda"

DOWNLOAD_URL = "https://github.com/PhilippvK/python-myeda/releases"

CLASSIFIERS = [
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Topic :: Scientific/Engineering",
    "Topic :: Scientific/Engineering :: Mathematics",
]

MYEDA_PKGS = [
    'myeda',
    'myeda.simulation',
    'myeda.visualization',
    'myeda.misc',
]

TEST_PKGS = [
    'myeda.test',
]

PACKAGES = MYEDA_PKGS + TEST_PKGS

# EXT_MODULES = [
#    Extension('myeda.qm', **QUINEMCCLUSKEY),
# ]
EXT_MODULES = []

SCRIPTS = [
]

install_requires = [
    'termcolor>=1.1.0',
    'pyeda>=0.28.0',
    'quine-mccluskey @ https://github.com/tpircher/quine-mccluskey',
    'wavedrom>=2.0.3.post2'
]

setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    keywords=KEYWORDS,
    long_description=README,
    license=LICENSE,
    url=URL,
    download_url=DOWNLOAD_URL,
    classifiers=CLASSIFIERS,
    packages=PACKAGES,
    ext_modules=EXT_MODULES,
    scripts=SCRIPTS,
    test_suite='nose.collector',
    python_requires='>=3.5',
    install_requires=install_requires,
)
