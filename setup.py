#!/usr/bin/env python
import sys
from deckconverter import __version__

try:
    from setuptools import setup
    setup
except ImportError:
    from distutils.core import setup

try:
    import multiprocessing
    multiprocessing
except ImportError:
    pass

requirements = open('requirements/base.txt').readlines()

setup(
    name='deckconverter',
    version=__version__,
    author='Matthew Kelly, Norman Joyner',
    author_email='matthew.joseph.kelly@gmail.com, norman.joyner@gmail.com',
    packages=['deckconverter'],
    scripts=['bin/deckconverter'],
    url='http://github.com/mattkelly/deckconverter',
    license='LICENSE',
    classifiers=[],
    description='A utility for converting between card deck formats',
    long_description=open('README.md').read(),
    tests_require=open('requirements/tests.txt').readlines(),
    test_suite='nose.collector',
    install_requires=requirements
)
