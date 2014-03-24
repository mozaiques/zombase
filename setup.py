# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from pip.req import parse_requirements


setup(
    name='mozbase',
    version='0.4.0dev',
    packages=find_packages(),
    test_suite='tests',
    install_requires=[
        str(ir.req) for ir in parse_requirements('requirements.txt')
    ],
    author='Bastien GANDOUET',
    author_email="bastien@mozaiqu.es"
)
