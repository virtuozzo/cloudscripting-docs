#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from setuptools import setup, find_packages
import re
import os
import sys

PY26 = sys.version_info[:2] == (2, 6)


def get_version(package):
    """Return package version as listed in `__version__` in `init.py`."""
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


if sys.argv[-1] == 'publish':
    if os.system("pip freeze | grep wheel"):
        print("wheel not installed.\nUse `pip install wheel`.\nExiting.")
        sys.exit()
    if os.system("pip freeze | grep twine"):
        print("twine not installed.\nUse `pip install twine`.\nExiting.")
        sys.exit()
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload dist/*")
    print("You probably want to also tag the version now:")
    print("  git tag -a {0} -m 'version {0}'".format(
        get_version("mkdocs_versioned")))
    print("  git push --tags")
    sys.exit()


setup(
    name="mkdocs-versioned",
    version=get_version("mkdocs_versioned"),
    url='http://www.mkdocs.org',
    license='BSD',
    description='Build multiple versions of MkDocs documentation',
    long_description="",
    author='Dougal Matthews',
    author_email='dougal@dougalmatthews.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click>=4.0',
        'gitpython',
    ],
    entry_points={
        'console_scripts': [
            'mkdocs_versioned = mkdocs_versioned.cli:build_command',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        "Programming Language :: Python :: Implementation :: CPython",
        'Topic :: Documentation',
        'Topic :: Text Processing',
    ],
    zip_safe=False
)
