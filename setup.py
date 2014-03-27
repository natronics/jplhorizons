#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='jplhorizons',
    version='0.1.0',
    description='Interface to JPL HORIZONS via telnet',
    long_description=readme + '\n\n' + history,
    author='Nathan Bergey',
    author_email='nathan.bergey@gmail.com',
    url='https://github.com/natronics/jplhorizons',
    packages=[
        'jplhorizons',
    ],
    package_dir={'jplhorizons': 'jplhorizons'},
    include_package_data=True,
    install_requires=[
    ],
    license="BSD",
    zip_safe=False,
    keywords='jplhorizons',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
)
