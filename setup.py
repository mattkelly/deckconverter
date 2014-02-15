#!/usr/bin/env python
import sys
from deckbuilder import __version__

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
    name='deckbuilder',
    version=__version__,
    author='Matthew Kelly, Norman Joyner',
    author_email='matthew.joseph.kelly@gmail.com, norman.joyner@gmail.com',
    packages=['deckbuilder'],
    scripts=['bin/deckbuilder'],
    url='http://github.com/mattkelly/deckbuilder',
    license='LICENSE',
    classifiers=[],
    description='A utility for converting between card deck formats',
    long_description=open('README.md').read()
    install_requires=requirements
)
