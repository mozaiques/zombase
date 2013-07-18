# -*- coding: utf-8 -*-
from setuptools import setup


setup(
    name='mozbase',
    version='0.3.5',
    packages=['mozbase'],
    test_suite='tests',
    install_requires=[
        'SQLAlchemy==0.8.2',
        'voluptuous==0.7.2',
        'dogpile.cache==0.5.0'],
    author='Bastien GANDOUET',
    author_email="bastien@mozaiqu.es"
)
