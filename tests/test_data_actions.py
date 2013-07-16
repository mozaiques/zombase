# -*- coding: utf-8 -*-
import unittest

from voluptuous import MultipleInvalid

from . import TestData


class TestCreateAction(TestData):

    def setUp(self):
        TestData.setUp(self)
        self.action_data = self.biz.action

    def tearDown(self):
        TestData.tearDown(self)
        del self.action_data

    def test_correct_create(self):
        self.action_data.create(message=u'Test message')
        self.assertTrue(True)

    def test_wrong_message(self):
        with self.assertRaises(MultipleInvalid):
            self.action_data.create(message='Test message')


if __name__ == '__main__':
    unittest.main()
