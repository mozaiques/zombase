# -*- coding: utf-8 -*-
"""Default organisation for a package regrouping the models of an app.
Also contains some default implementations of the most common objects.

"""
from sqlalchemy.ext.declarative import declarative_base

from mozbase.util.database import MetaBase


__all__ = ['User', 'Action', 'File']


Base = declarative_base(cls=MetaBase)
