 # -*- coding: utf-8 -*-
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from voluptuous import MultipleInvalid

import warbmodel
from warbmodel import *
from warbdata.users import UsersData
from warbdata.applications import ApplicationsData


class TestGetAvailableApp(unittest.TestCase):
    def setUp(self):
        engine = create_engine('sqlite:///:memory:', echo=False)
        Session = sessionmaker(bind=engine)
        warbmodel.Base.metadata.create_all(engine)
        self.session = Session()
        self.users_data = UsersData(session=self.session)
        self.apps_data = ApplicationsData(session=self.session)
        self.user = self.users_data.create(
            login='wart',
            mail='a@b.c')
        self.app = self.apps_data.create(
            login='wart',
            mail='a@b.c')

    def tearDown(self):
        del self.session
        del self.users_data

    def test_get_apps(self):
        pass


if __name__ == '__main__':
    unittest.main()
