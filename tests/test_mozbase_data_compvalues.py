# -*- coding: utf-8 -*-
import unittest

import pylibmc
from nose.plugins.skip import SkipTest

from mozbase.util.cache import Cache
from mozbase.util.cache_systems.database_cache import DatabaseCache
from mozbase.util.cache_systems.memcached_cache import MemcachedCache

from . import TestData


class CacheSystemTestSuite():

    def test_set_and_get_compval(self):
        self.cache.set(
            key='foo:1:bar',
            value=float(14))
        val = self.cache.get(key='foo:1:bar')
        self.assertEqual(val, float(14))

    def test_reset_and_get_compval(self):
        self.cache.set(
            key='foo:1:bar',
            value=float(14))
        self.cache.set(
            key='foo:1:bar',
            value=float(19))
        val = self.cache.get(key='foo:1:bar')
        self.assertEqual(val, float(19))

    def test_set_compval_no_value(self):
        with self.assertRaises(TypeError):
            self.cache.set(key='foo:1:bar')

    def test_expire_single_value(self):
        self.cache.set(
            key='foo:1:bar',
            value=float(14))
        self.cache.expire(key='foo:1:bar')
        value = self.cache.get(key='foo:1:bar')
        self.assertTrue(not value)

    def test_expire_multiple_values(self):
        self.cache.set(
            key='foo:1:bar',
            value=float(14))
        self.cache.set(
            key='foo:1:blo',
            value=float(11))
        self.cache.expire(
            key='foo:1:')
        valuebar = self.cache.get(key='foo:1:bar')
        valueblo = self.cache.get(key='foo:1:blo')
        self.assertTrue(not valuebar)
        self.assertTrue(not valueblo)


class TestDatabaseCache(TestData, CacheSystemTestSuite):

    def setUp(self):
        TestData.setUp(self)
        self.cache = Cache()
        db_cache = DatabaseCache(self.session)
        self.cache.append_cache(db_cache)


class TestMemcachedCache(unittest.TestCase, CacheSystemTestSuite):

    def setUp(self):
        self.cache = Cache()
        self.memcached_cache = MemcachedCache(server='127.0.0.1:11211')
        self.cache.append_cache(self.memcached_cache)
        try:
            self.cache.set(key='test:1:bla', value=12)
        except pylibmc.ConnectionError:
            raise SkipTest

    def test_split_key(self):
        with self.assertRaises(AttributeError):
            _key, _property_name = self.memcached_cache._check_key(key='foo:bar')


if __name__ == '__main__':
    unittest.main()
