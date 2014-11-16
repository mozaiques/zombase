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


class FakeMappingWithID(object):

    a_prop = 12
    a_req_prop = 'bla'

    id = ''


class FakeMappingWithUUID(object):

    a_prop = 12
    a_req_prop = 'bla'

    uuid = 'bla'


class TestWorkerIDs(unittest.TestCase):

    def setUp(self):
        self.dbsession = FakeDbSession()
        self.foreman = FakeForeman()

    def tearDown(self):
        del self.dbsession

    def test_init_without_id_or_uuid(self):
        foreman = FakeForeman()
        a_worker = worker.ObjectManagingWorker(
            foreman,
            managed_object=FakeMapping,
            managed_object_name='fake',
        )

        self.assertFalse(a_worker._with_id)
        self.assertFalse(a_worker._with_uuid)

    def test_init_with_id(self):
        foreman = FakeForeman()
        a_worker = worker.ObjectManagingWorker(
            foreman,
            managed_object=FakeMappingWithID,
            managed_object_name='fake',
        )

        self.assertTrue(a_worker._with_id)
        self.assertFalse(a_worker._with_uuid)

    def test_init_with_uuid(self):
        foreman = FakeForeman()
        a_worker = worker.ObjectManagingWorker(
            foreman,
            managed_object=FakeMappingWithUUID,
            managed_object_name='fake',
        )

        self.assertTrue(a_worker._with_uuid)
        self.assertFalse(a_worker._with_id)

    def test_init_forced(self):
        foreman = FakeForeman()
        a_worker = worker.ObjectManagingWorker(
            foreman,
            managed_object=FakeMapping,
            managed_object_name='fake',
            id_type='uuid',
        )

        self.assertTrue(a_worker._with_uuid)
        self.assertFalse(a_worker._with_id)

        a_second_worker = worker.ObjectManagingWorker(
            foreman,
            managed_object=FakeMapping,
            managed_object_name='fake',
            id_type='id',
        )

        self.assertTrue(a_second_worker._with_id)
        self.assertFalse(a_second_worker._with_uuid)
