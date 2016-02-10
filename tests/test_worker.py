# -*- coding: utf-8 -*-
import unittest

from zombase import worker


class FakeDbSession(object):
    def __init__(self):
        self.has_been_committed = False

    def commit(self):
        self.has_been_committed = True


class FakeForeman(object):

    def __init__(self):
        self._dbsession = FakeDbSession()


class FakeMapping(object):

    a_prop = 12
    a_req_prop = 'bla'


class BaseTestWorker(unittest.TestCase):

    def setUp(self):
        self.dbsession = FakeDbSession()

    def tearDown(self):
        del self.dbsession


class TestRawWorker(BaseTestWorker):

    def test_init(self):
        worker.RawWorker(self.dbsession)


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
        worker.MappingManagingWorker(
            foreman,
            managed_sqla_map=FakeMapping,
            managed_sqla_map_name='fake',
        )

    def test__get(self):
        foreman = FakeForeman()
        a_worker = worker.MappingManagingWorker(
            foreman,
            managed_sqla_map=FakeMapping,
            managed_sqla_map_name='fake',
        )

        a_worker._get(sqla_obj=FakeMapping())
