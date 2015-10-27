# -*- coding: utf-8 -*-
import voluptuous

from zombase import mapping

import test_worker

a_schema = voluptuous.Schema({
    'a_prop': int,
    voluptuous.Required('a_req_prop'): str,
})


class TestWorkerUpdate(test_worker.BaseTestWorker):

    def test(self):
        an_object = test_worker.FakeMapping()

        self.assertEqual(an_object.a_prop, 12)

        update = mapping.update(
            sqla_obj=an_object, schema=a_schema, a_prop=13)
        self.assertEqual(an_object.a_prop, 13)
        self.assertTrue(update)

        update = mapping.update(
            sqla_obj=an_object, schema=a_schema, a_prop=13)
        self.assertFalse(update)

        update = mapping.update(
            sqla_obj=an_object, schema=a_schema)
        self.assertFalse(update)

        update = mapping.update(
            sqla_obj=an_object, schema=a_schema, a_req_prop='bb')
        self.assertEqual(an_object.a_req_prop, 'bb')
        self.assertTrue(update)
