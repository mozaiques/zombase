 # -*- coding: utf-8 -*-
import unittest
import hashlib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from voluptuous import MultipleInvalid

import warbmodel
from warbmodel import *
from warbdata.actions import ActionsData


class TestCreateActionsData(unittest.TestCase):
    def test_wrong_user_id(self):
        engine = create_engine('sqlite:///:memory:', echo=False)
        Session = sessionmaker(bind=engine)
        warbmodel.Base.metadata.create_all(engine)
        self.session = Session()
        with self.assertRaises(AttributeError):
            self.actions_data = ActionsData(session=self.session, user_id=1)


class TestCreateAction(unittest.TestCase):
    def setUp(self):
        engine = create_engine('sqlite:///:memory:', echo=False)
        Session = sessionmaker(bind=engine)
        warbmodel.Base.metadata.create_all(engine)
        self.session = Session()
        self.actions_data = ActionsData(session=self.session,
                                        user=User.User(),
                                        application=Application.Application())

    def tearDown(self):
        del self.session
        del self.actions_data

    def test_correct_create(self):
        action = self.actions_data.create(
            application=Application.Application(),
            message=u'Test message')
        self.assertTrue(True)

    def test_wrong_message(self):
        with self.assertRaises(MultipleInvalid):
            action = self.actions_data.create(
                application=Application.Application(),
                message='Test message')


if __name__ == '__main__':
    unittest.main()
