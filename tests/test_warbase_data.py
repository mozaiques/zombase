 # -*- coding: utf-8 -*-
import unittest

from werkzeug.contrib.cache import MemcachedCache

import warbase.data
from warbase.model import ComputedValue

from . import TestData


class DataRepository(TestData):

    def setUp(self):
        TestData.setUp(self)
        self.cache = MemcachedCache(['127.0.0.1:11211'])

    def tearDown(self):
        TestData.tearDown(self)
        self.cache.clear()
        del self.cache

    def test_instancing_data_repo(self):
        data_repo = warbase.data.DataRepository(session=self.session)

    def test_instancing_data_repo_without_session(self):
        with self.assertRaises(TypeError):
            data_repo = warbase.data.DataRepository(cache=self.cache)

    def test_instancing_data_repo_with_cache(self):
        data_repo = warbase.data.DataRepository(
            session=self.session,
            cache=self.cache)
        self.assertEqual(self.cache, data_repo.cache)

    def test_generation_cache_key(self):
        data_repo = warbase.data.DataRepository(
            session=self.session,
            cache=self.cache)
        self.assertEqual('bla:vi:12', data_repo._cache_key(key='bla:vi', target_id=12))

    def test_set_in_cache(self):
        cv_repo = warbase.data.computed_values.ComputedValuesData(
            session=self.session,
            cache=self.cache)
        cv = cv_repo.set(key='bla:vi', target_id=12, value=float(30))
        self.assertEqual(cv.value, self.cache.get('bla:vi:12').value)

    def test_get_from_db_set_in_cache(self):
        cv_repo = warbase.data.computed_values.ComputedValuesData(
            session=self.session)
        # Set without cache
        cv = cv_repo.set(key='bla:vi', target_id=12, value=float(30))

        del cv_repo
        cv_repo = warbase.data.DataRepository(
            session=self.session,
            cache=self.cache)

        # Get in DB, set in cache
        another_cv = cv_repo._get_computed_value(key='bla:vi', target_id=12)

        cache_cv = cv_repo._get_from_cache(key='bla:vi', target_id=12)

        self.assertEqual(cache_cv.value, cv.value)


if __name__ == '__main__':
    unittest.main()
