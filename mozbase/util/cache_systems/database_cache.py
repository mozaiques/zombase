# -*- coding: utf-8 -*-
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.schema import UniqueConstraint, Index

from mozbase.util.database import db_method, JSONType
import mozbase.model


class DatabaseCache():

    def __init__(self, dbsession):
        self._dbsession = dbsession

    def _check_key(self, key):
        if not isinstance(key, str):
            raise AttributeError('key provided is not a string')

    def get(self, key):
        self._check_key(key)

        try:
            value = self._dbsession.query(ComputedValue)\
                .filter(ComputedValue.key == key)\
                .one()
        except NoResultFound:
            return None

        if value.expired:
            return None

        return value.value

    @db_method()
    def set(self, key, value):
        self._check_key(key)

        try:
            value_db = self._dbsession.query(ComputedValue)\
                .filter(ComputedValue.key == key)\
                .one()
        except NoResultFound:
            value_db = ComputedValue()
            value_db.key = key

        value_db.expired = False
        value_db.value = value

        self._dbsession.add(value_db)

    @db_method()
    def expire(self, key):
        self._check_key(key)

        if key[-1] == ':':
            values_db = self._dbsession.query(ComputedValue)\
                .filter(ComputedValue.key.like(key+'%'))\
                .all()
        else:
            value_db = self._dbsession.query(ComputedValue)\
                .filter(ComputedValue.key == key)\
                .one()
            values_db = [value_db]

        for a_val in values_db:
            a_val.expired = True
            self._dbsession.add(a_val)


class ComputedValue(mozbase.model.Base):
    __tablename__ = 'wb_computed_values'
    id = Column(Integer, primary_key=True)

    key = Column(String)

    expired = Column(Boolean)
    value = Column(JSONType())

    __table_args__ = (
        UniqueConstraint('key'),
        Index('idx_computed_values', 'key'))
