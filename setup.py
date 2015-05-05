# -*- coding: utf-8 -*-
import os

from setuptools import setup, find_packages


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as r_file:
    readme = r_file.read()


setup(
    name='zombase',
    version='0.4.8',
    license='MIT',
    author='Bastien Gandouet',
    author_email='bastien@mozaiqu.es',
    description='A toolset to build beautiful data layer APIs',
    long_description=readme,
    packages=find_packages(),
    test_suite='tests',
    install_requires=[
        'SQLAlchemy>=0.9',
        'voluptuous>=0.8',
        'dogpile.cache>=0.5',
        'six>=1.7',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
