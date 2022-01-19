#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Learn more: https://github.com/fx-bricks/pfx-brick-py/setup.py

import os
import platform
import sys
import setuptools

PACKAGE_NAME = "pfxbrick"
MINIMUM_PYTHON_VERSION = "3.6"


def check_python_version():
    """Exit when the Python version is too low."""
    if platform.python_version() < MINIMUM_PYTHON_VERSION:
        sv = "Python %s+ is required, not %s" % (MINIMUM_PYTHON_VERSION, sys.version)
        sys.exit(sv)


def read_package_variable(key, filename="__init__.py"):
    """Read the value of a variable from the package without importing."""
    module_path = os.path.join(PACKAGE_NAME, filename)
    with open(module_path) as module:
        for line in module:
            parts = line.strip().split(" ", 2)
            if parts[:-1] == [key, "="]:
                return parts[-1].strip("'")
    sys.exit("'{0}' not found in '{1}'".format(key, module_path))


def build_description():
    """Build a description for the project from documentation files."""
    try:
        readme = open("README.rst").read()
        changelog = open("CHANGELOG.rst").read()
    except IOError:
        return "<placeholder>"
    else:
        return readme + "\n" + changelog


setuptools.setup(
    name=read_package_variable("__project__"),
    version=read_package_variable("__version__"),
    description="A python API for host control of USB connected PFx Bricks.",
    url="https://github.com/fx-bricks/pfx-brick-py",
    author="Fx Bricks Inc.",
    author_email="info@fxbricks.com",
    packages=setuptools.find_packages(),
    long_description=build_description(),
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=["hidapi", "bleak", "rich"],
    entry_points={
        "console_scripts": [
            "pfxcat=pfxbrick.scripts.pfxcat:main",
            "pfxdir=pfxbrick.scripts.pfxdir:main",
            "pfxget=pfxbrick.scripts.pfxget:main",
            "pfxput=pfxbrick.scripts.pfxput:main",
            "pfxrm=pfxbrick.scripts.pfxrm:main",
            "pfxrename=pfxbrick.scripts.pfxrename:main",
            "pfxdump=pfxbrick.scripts.pfxdump:main",
            "pfxmonitor=pfxbrick.scripts.pfxmonitor:main",
            "pfxtest=pfxbrick.scripts.pfxtest:main",
            "pfxinfo=pfxbrick.scripts.pfxinfo:main",
            "pfxplay=pfxbrick.scripts.pfxplay:main",
            "pfxrun=pfxbrick.scripts.pfxrun:main",
            "pfxfat=pfxbrick.scripts.pfxfat:main",
            "pfxrestart=pfxbrick.scripts.pfxrestart:main",
        ],
    },
)
