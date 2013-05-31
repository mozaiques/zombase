# -*- coding: utf-8 -*-
from sqlalchemy.orm.exc import NoResultFound

from warbase.utils.database import db_method
from warbase.model.ComputedValue import ComputedValue


class DbCache():

    def __init__(self, session):
        self.session = session

    def _check_key(self, key):
        if not isinstance(key, str):
            raise AttributeError('key provided is not a string')

    def get(self, key):
        self._check_key(key)

        try:
            value = self.session.query(ComputedValue)\
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
            value_db = self.session.query(ComputedValue)\
                .filter(ComputedValue.key == key)\
                .one()
        except NoResultFound:
            value_db = ComputedValue()
            value_db.key = key

        value_db.expired = False
        value_db.value = value

        self.session.add(value_db)

    @db_method()
    def expire(self, key):
        self._check_key(key)

        if key[-1] == ':':
            values_db = self.session.query(ComputedValue)\
                .filter(ComputedValue.key.like(key+'%'))\
                .all()
        else:
            value_db = self.session.query(ComputedValue)\
                .filter(ComputedValue.key == key)\
                .one()
            values_db = [value_db]

        for a_val in values_db:
            a_val.expired = True
            self.session.add(a_val)
