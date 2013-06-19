# -*- coding: utf-8 -*-
import unittest

from . import TestData


class CacheSystemTestSuite(TestData):

    def setUp(self):
        TestData.setUp(self)
        self.cache = self.session.cache

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
        self.cache.delete(key='foo:1:bar')
        value = self.cache.get(key='foo:1:bar')
        self.assertTrue(not value)


if __name__ == '__main__':
    unittest.main()
