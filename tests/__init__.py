 # -*- coding: utf-8 -*-
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from voluptuous import MultipleInvalid

import warbase.model
from warbase.model import *
from warbase.data.users import UsersData


class TestData(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        #self.engine = create_engine(
        #    'postgres://testpgsql:testpgsqlp4ss@localhost/testpgsql')
        Session = sessionmaker(bind=self.engine)
        warbase.model.Base.metadata.create_all(self.engine)
        self.session = Session()

    def tearDown(self):
        self.session.close()
        warbase.model.Base.metadata.drop_all(self.engine)


if __name__ == '__main__':
    unittest.main()
