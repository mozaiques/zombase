# -*- coding: utf-8 -*-
import unittest

from zombase import worker


class FakeCache(object):
    pass


class FakeDbSession(object):
    def __init__(self, with_cache=False):
        self.has_been_committed = False

        if with_cache:
            self.cache = FakeCache()

    def commit(self):
        self.has_been_committed = True


class FakeForeman(object):

    def __init__(self):
        self._dbsession = FakeDbSession(with_cache=True)


class FakeMapping(object):

    a_prop = 12
    a_req_prop = 'bla'


class BaseTestWorker(unittest.TestCase):

    def setUp(self):
        self.dbsession = FakeDbSession()

    def tearDown(self):
        del self.dbsession


class TestRawWorker(BaseTestWorker):

    def test_sanity(self):
        worker.RawWorker(self.dbsession, check_sanity=False)

        with self.assertRaises(ValueError):
            worker.RawWorker(self.dbsession)

        dbsession_w_cache = FakeDbSession(with_cache=True)
        worker.RawWorker(dbsession_w_cache)


class TestSupervisedWorker(BaseTestWorker):

    def test_init(self):
        foreman = FakeForeman()
        supervised_worker = worker.SupervisedWorker(foreman)
        self.assertEqual(supervised_worker._foreman, foreman)

        supervised_worker = worker.SupervisedWorker(foreman, '_for')
        self.assertEqual(supervised_worker._for, foreman)


class TestObjectManagingWorker(BaseTestWorker):

    def test_init(self):
        foreman = FakeForeman()
        worker.ObjectManagingWorker(
            foreman, managed_object=FakeMapping, managed_object_name='fake')

    def test__get(self):
        foreman = FakeForeman()
        a_worker = worker.ObjectManagingWorker(
            foreman, managed_object=FakeMapping, managed_object_name='fake')

        a_worker._get(instance=FakeMapping())
