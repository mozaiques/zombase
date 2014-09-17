# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(
    name='zombase',
    version='0.2.1dev',
    packages=find_packages(),
    test_suite='tests',
    install_requires=[
        'SQLAlchemy>=0.9',
        'voluptuous>=0.8',
        'dogpile.cache>=0.5',
        'click>=3',
        'six>=1.7',
    ],
    author='Bastien GANDOUET',
    author_email="bastien@mozaiqu.es",
)
