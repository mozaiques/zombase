from setuptools import setup

setup(
    name='mozbase',
    version='0.3.0dev',
    packages=['mozbase'],
    test_suite='tests',
    install_requires=['SQLAlchemy', 'voluptuous'],
    author='Bastien GANDOUET',
    author_email="bastien@mozaiqu.es"
)
