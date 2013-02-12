from setuptools import setup

setup(
    name='warbase',
    version='0.0.1dev',
    packages=['warbmodel', 'warbdata', 'warbbiz'],
    test_suite='tests',
    install_requires=['SQLAlchemy', 'voluptuous'],
    author='Bastien GANDOUET',
    author_email="bastien@pectoribus.net",
    license="MIT",
)
