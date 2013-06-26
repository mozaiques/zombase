# -*- coding: utf-8 -*-
"""Default organisation for a package regrouping the models of an app.
Also contains some default implementations of the most common objects.

"""
from sqlalchemy.ext.declarative import declarative_base


__all__ = ['User', 'Action']


Base = declarative_base()
