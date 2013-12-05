# -*- coding: utf-8 -*-
from setuptools import setup

from mozbase import __version__


setup(
    name='mozbase',
    version=__version__,
    packages=['mozbase'],
    test_suite='tests',
    install_requires=[
        'SQLAlchemy==0.8.3',
        'voluptuous==0.8.4',
        'dogpile.cache==0.5.2'],
    author='Bastien GANDOUET',
    author_email="bastien@mozaiqu.es"
)
