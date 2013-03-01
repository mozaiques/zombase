from sqlalchemy import Column, Float, Integer, String, DateTime, Boolean
from sqlalchemy.orm import backref, relationship
from sqlalchemy.schema import UniqueConstraint, Index

import warbase.model


class ComputedValue(warbase.model.Base):
    __tablename__ = 'wb_computed_values'
    id = Column(Integer, primary_key=True)

    key = Column(String)
    target_id = Column(Integer)

    expired = Column(Boolean)
    value = Column(Float)

    datetime = Column(DateTime, index=True)

    __table_args__ = (
        UniqueConstraint('key', 'target_id'),
        Index('idx_computed_values', 'key', 'target_id'))
