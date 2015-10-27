# -*- coding: utf-8 -*-
from zombase import worker

import test_worker


class InvalidWorker(worker.MappingManagingWorker):
    pass


class Worker(worker.MappingManagingWorker):

    def _serialize_one(self, item):
        return {'a_prop': item.a_prop}


class TestInvalidWorker(test_worker.BaseTestWorker):

    def test_invalid_worker(self):
        foreman = test_worker.FakeForeman()
        a_worker = InvalidWorker(
            foreman,
            managed_sqla_map=test_worker.FakeMapping,
            managed_sqla_map_name='fake',
        )

        with self.assertRaises(NotImplementedError):
            a_worker.serialize_one(test_worker.FakeMapping())


class TestSerialize(test_worker.BaseTestWorker):

    def setUp(self):
        foreman = test_worker.FakeForeman()
        self.a_worker = Worker(
            foreman,
            managed_sqla_map=test_worker.FakeMapping,
            managed_sqla_map_name='fake',
        )
        test_worker.BaseTestWorker.setUp(self)

    def tearDown(self):
        del self.a_worker
        test_worker.BaseTestWorker.tearDown(self)

    def test_serialize_one(self):
        fake_item = test_worker.FakeMapping()
        serialized = self.a_worker.serialize_one(fake_item)

        self.assertTrue(isinstance(serialized, dict))
        self.assertEqual(serialized['a_prop'], fake_item.a_prop)

    def test_serialize_one_with_func(self):
        fake_item = test_worker.FakeMapping()

        def times_3(item):
            return item.a_prop * 3

        serialized = self.a_worker.serialize_one(fake_item, times_3=times_3)
        self.assertEqual(serialized['times_3'], fake_item.a_prop * 3)

    def test_serialize_list(self):
        fake_item1 = test_worker.FakeMapping()
        fake_item2 = test_worker.FakeMapping()
        fake_item2.a_prop = 13

        def times_2(item):
            return item.a_prop * 2

        serialized = list(self.a_worker.serialize(
            (fake_item1, fake_item2), times_2=times_2))

        self.assertEqual(serialized[0]['a_prop'], fake_item1.a_prop)
        self.assertEqual(serialized[1]['a_prop'], fake_item2.a_prop)

        self.assertEqual(serialized[0]['times_2'], fake_item1.a_prop * 2)
        self.assertEqual(serialized[1]['times_2'], fake_item2.a_prop * 2)
