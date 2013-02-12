 # -*- coding: utf-8 -*-
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import warbdata


class DataRepository(unittest.TestCase):
    def setUp(self):
        engine = create_engine('sqlite:///:memory:', echo=True)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def tearDown(self):
        del self.session

    def test_binding_session(self):
        with self.assertRaises(AttributeError):
            warbdata.DataRepository(session='foo')


if __name__ == '__main__':
    unittest.main()
