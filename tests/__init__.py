 # -*- coding: utf-8 -*-
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from voluptuous import MultipleInvalid

import warbmodel
from warbmodel import *
from warbdata.users import UsersData
from warbdata.applications import ApplicationsData
from warbbiz.users import UsersBusiness


class TestData(unittest.TestCase):

    def setUp(self):
        #self.engine = create_engine('sqlite:///:memory:')
        self.engine = create_engine(
            'postgres://testpgsql:testpgsqlp4ss@localhost/testpgsql')
        Session = sessionmaker(bind=self.engine)
        warbmodel.Base.metadata.create_all(self.engine)
        self.session = Session()

    def tearDown(self):
        self.session.close()
        warbmodel.Base.metadata.drop_all(self.engine)


if __name__ == '__main__':
    unittest.main()
