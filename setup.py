from setuptools import setup

setup(
    name='mozbase',
    version='0.3.0beta',
    packages=['mozbase'],
    test_suite='tests',
    install_requires=['SQLAlchemy', 'voluptuous', 'dogpile.cache'],
    author='Bastien GANDOUET',
    author_email="bastien@mozaiqu.es"
)
