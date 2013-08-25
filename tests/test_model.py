# -*- coding: utf-8 -*-
import uuid
import datetime

from mozbase.util.database import MetaBase
from mozbase.model import User, Action, File

from . import TestData


class TestModelBase(TestData):

    def test_user(self):
        User.User()

    def test_action(self):
        Action.Action()

    def test_file(self):
        a_uuid = uuid.uuid4()
        a_file = File.File(
            uuid=a_uuid,
            datetime=datetime.datetime.now())

        self.session.add(a_file)
        self.session.commit()

        self.session.query(File.File).filter(File.File.uuid == a_uuid).one()

    def test_inheritance(self):
        self.assertTrue(issubclass(Action.Action, MetaBase))
