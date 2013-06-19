# -*- coding: utf-8 -*-
import unittest

from mozbase.util import database


class TestDatabase(unittest.TestCase):

    class FakeDbSession():
        def __init__(self):
            self.has_been_committed = False
        def commit(self):
            self.has_been_committed = True

    @database.db_method()
    def fake_method(self):
        pass

    def setUp(self):
        self._dbsession = self.FakeDbSession()

    def tearDown(self):
        del self._dbsession

    def test_transaction(self):
        self.assertTrue(not self._dbsession.has_been_committed)
        self.assertTrue(
            not getattr(self._dbsession,
                    'mozbase_transaction',
                    False))

        with database.transaction(self._dbsession):
            self.assertTrue(not self._dbsession.has_been_committed)
            self.assertTrue(getattr(
                self._dbsession,
                'mozbase_transaction'))

        self.assertTrue(self._dbsession.has_been_committed)
        self.assertTrue(
            not getattr(self._dbsession,
                    'mozbase_transaction',
                    False))

    def test_db_method(self):
        self.fake_method()
        # Default is to auto commit.
        self.assertTrue(self._dbsession.has_been_committed)

    def test_db_method_with_commit_true(self):
        self.fake_method(commit=True)
        self.assertTrue(self._dbsession.has_been_committed)

    def test_db_method_with_commit_false(self):
        self.fake_method(commit=False)
        self.assertTrue(not self._dbsession.has_been_committed)

    def test_db_method_with_transaction(self):
        with database.transaction(self._dbsession):
            self.fake_method()
            self.assertTrue(not self._dbsession.has_been_committed)

            # Even if `commit=True`, we don't commit inside a
            # transaction
            self.fake_method(commit=True)
            self.assertTrue(not self._dbsession.has_been_committed)

        self.assertTrue(self._dbsession.has_been_committed)


if __name__ == '__main__':
    unittest.main()
