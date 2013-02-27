 # -*- coding: utf-8 -*-
import unittest
import hashlib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from voluptuous import MultipleInvalid

import warbase.model
from warbase.model import *
from warbase.data.computed_values import ComputedValuesData

from . import TestData


class TestComputedValues(TestData):
    
    def setUp(self):
        TestData.setUp(self)
        self.compval_data = ComputedValuesData(session=self.session)

    

class TestSetComputedValues(TestComputedValues):

    def test_set_compval(self):
        compval = self.compval_data.set(
            key='foo:bar',
            target_id=12,
            value=float(14))
        self.assertEqual(compval.key, 'foo:bar')

    def test_set_compval_no_value(self):
        with self.assertRaises(TypeError):
            compval = self.compval_data.set(
                key='foo:bar',
                target_id=12)

    def test_set_compval_wrong_value(self):
        with self.assertRaises(AttributeError):
            compval = self.compval_data.set(
                key='foo:bar',
                target_id=12,
                value='bla')

class TestExpireComputedValues(TestComputedValues):

    def test_expire_compval(self):
        compval = self.compval_data.set(
            key='foo:bar',
            target_id=12,
            value=float(14))
        daBool = self.compval_data.expire(
            key='foo:bar',
            target_id=12)
        self.assertTrue(daBool)
        self.assertTrue(compval.expired)

    def test_expire_set_compval(self):
        compval1 = self.compval_data.set(
            key='foo:bar',
            target_id=12,
            value=float(14))
        compval2 = self.compval_data.set(
            key='foo:foo',
            target_id=12,
            value=float(16))
        daBool = self.compval_data.expire(
            key='foo:',
            target_id=12)
        self.assertTrue(daBool)
        self.assertTrue(compval1.expired)
        self.assertTrue(compval2.expired)


if __name__ == '__main__':
    unittest.main()
