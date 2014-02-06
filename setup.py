# -*- coding: utf-8 -*-
from setuptools import setup


setup(
    name='mozbase',
    version='0.3.10dev',
    packages=['mozbase'],
    test_suite='tests',
    install_requires=[
        'SQLAlchemy==0.9.2',
        'voluptuous==0.8.4',
        'dogpile.cache==0.5.3',
    ],
    author='Bastien GANDOUET',
    author_email="bastien@mozaiqu.es"
)
