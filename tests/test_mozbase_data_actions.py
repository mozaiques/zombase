 # -*- coding: utf-8 -*-
import unittest

from sqlalchemy.orm.exc import NoResultFound
from voluptuous import MultipleInvalid

from mozbase.model import User
from mozbase.data.action import ActionData

from . import TestData


class TestCreateActionsData(TestData):

    def test_wrong_user_id(self):
        with self.assertRaises(NoResultFound):
            self.action_data = ActionData(dbsession=self.session, user_id=1)


class TestCreateAction(TestData):

    def setUp(self):
        TestData.setUp(self)
        self.action_data = ActionData(dbsession=self.session,
                                        user=User.User())

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
