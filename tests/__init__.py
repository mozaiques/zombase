 # -*- coding: utf-8 -*-
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import mozbase.model
from mozbase.model import *


class TestData(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Session = sessionmaker(bind=self.engine)
        mozbase.model.Base.metadata.create_all(self.engine)
        self.session = Session()

    def tearDown(self):
        self.session.close()
        mozbase.model.Base.metadata.drop_all(self.engine)


if __name__ == '__main__':
    unittest.main()
