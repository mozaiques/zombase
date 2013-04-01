 # -*- coding: utf-8 -*-
import unittest

import pylibmc
from nose.plugins.skip import SkipTest

from warbase.data.computed_values import ComputedValuesData
from warbase.data.cache_systems.db_cache import DbCache
from warbase.data.cache_systems.memcached_cache import MemcachedCache

from . import TestData


class CacheBusinessTestSuite():

    def test_set_and_get_compval(self):
        self.cvalues_data.set(
            key='foo:1:bar',
            value=float(14))
        val = self.cvalues_data.get(key='foo:1:bar')
        self.assertEqual(val, float(14))

    def test_set_compval_no_value(self):
        with self.assertRaises(TypeError):
            self.cvalues_data.set(key='foo:1:bar')

    def test_expire_single_value(self):
        self.cvalues_data.set(
            key='foo:1:bar',
            value=float(14))
        self.cvalues_data.expire(key='foo:1:bar')
        value = self.cvalues_data.get(key='foo:1:bar')
        self.assertTrue(not value)

    def test_expire_multiple_values(self):
        self.cvalues_data.set(
            key='foo:1:bar',
            value=float(14))
        self.cvalues_data.set(
            key='foo:1:blo',
            value=float(11))
        self.cvalues_data.expire(
            key='foo:1:')
        valuebar = self.cvalues_data.get(key='foo:1:bar')
        valueblo = self.cvalues_data.get(key='foo:1:blo')
        self.assertTrue(not valuebar)
        self.assertTrue(not valueblo)


class TestComputedValuesDbCache(TestData, CacheBusinessTestSuite):

    def setUp(self):
        TestData.setUp(self)
        self.cvalues_data = ComputedValuesData()
        db_cache = DbCache(session=self.session)
        self.cvalues_data.append_cache(db_cache)


class TestComputedValuesMemcachedCache(unittest.TestCase, CacheBusinessTestSuite):

    def setUp(self):
        self.cvalues_data = ComputedValuesData()
        self.memcached_cache = MemcachedCache(server='127.0.0.1:11211')
        self.cvalues_data.append_cache(self.memcached_cache)
        try:
            self.cvalues_data.set(key='test:1:bla', value=12)
        except pylibmc.ConnectionError:
            raise SkipTest

    def test_split_key(self):
        split_key = self.memcached_cache._split_key(key='foo:bar')
        self.assertTrue(not split_key)


if __name__ == '__main__':
    unittest.main()
