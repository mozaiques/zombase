 # -*- coding: utf-8 -*-
import unittest
import hashlib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from voluptuous import MultipleInvalid

import warbase.model
from warbase.model import *
from warbase.data.actions import ActionsData

from . import TestData


class TestCreateActionsData(TestData):

    def test_wrong_user_id(self):
        with self.assertRaises(NoResultFound):
            self.actions_data = ActionsData(session=self.session, user_id=1)


class TestCreateAction(TestData):

    def setUp(self):
        TestData.setUp(self)
        self.actions_data = ActionsData(session=self.session,
                                        user=User.User())

    def tearDown(self):
        TestData.tearDown(self)
        del self.actions_data

    def test_correct_create(self):
        action = self.actions_data.create(message=u'Test message')
        self.assertTrue(True)

    def test_wrong_message(self):
        with self.assertRaises(MultipleInvalid):
            action = self.actions_data.create(message='Test message')


if __name__ == '__main__':
    unittest.main()
