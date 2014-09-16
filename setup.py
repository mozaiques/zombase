# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(
    name='zombase',
    version='0.1.3dev',
    packages=find_packages(),
    test_suite='tests',
    install_requires=[
        'SQLAlchemy==0.9.7',
        'voluptuous==0.8.5',
        'dogpile.cache==0.5.4',
        'click==3.3',
        'six==1.8.0',
    ],
    author='Bastien GANDOUET',
    author_email="bastien@mozaiqu.es",
)
