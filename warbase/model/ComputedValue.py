from sqlalchemy import Column, PickleType, Integer, String, Boolean
from sqlalchemy.schema import UniqueConstraint, Index

import warbase.model


class ComputedValue(warbase.model.Base):
    __tablename__ = 'wb_computed_values'
    id = Column(Integer, primary_key=True)

    key = Column(String)

    expired = Column(Boolean)
    value = Column(PickleType)

    __table_args__ = (
        UniqueConstraint('key'),
        Index('idx_computed_values', 'key'))
