# -*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base


__all__ = ['Action', 'User']

# ComputedValue is not imported automaticaly because it's not useful in 99% of
# cases. To get it (as well as other models) one have to do:
# from warbase.model import *
# from warbase.model import ComputedValie

Base = declarative_base()
