# -*- coding: utf-8 -*-
"""Default implementation of a File object."""
from sqlalchemy import Column, String, DateTime

from mozbase.util.database import GUIDType

import mozbase.model


class File(mozbase.model.Base):
    __tablename__ = 'files'
    uuid = Column(GUIDType(), primary_key=True)

    key = Column(String())
    path = Column(String())
    datetime = Column(DateTime())
