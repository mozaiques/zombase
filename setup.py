# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(
    name='zombase',
    version='0.2.2dev',
    license='MIT',
    author='Bastien GANDOUET',
    author_email="bastien@mozaiqu.es",
    packages=find_packages(),
    test_suite='tests',
    install_requires=[
        'SQLAlchemy>=0.9',
        'voluptuous>=0.8',
        'dogpile.cache>=0.5',
        'click>=3',
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
