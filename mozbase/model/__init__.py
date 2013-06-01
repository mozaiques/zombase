# -*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base


__all__ = ['Action', 'User']

# ComputedValue is not imported automaticaly because it's useless in 99%
# of the cases. To get it (as well as other models) one have to do:
# from mozbase.model import *
# from mozbase.model import ComputedValie

Base = declarative_base()
