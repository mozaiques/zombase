 # -*- coding: utf-8 -*-
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import warbdata

from . import TestData


class DataRepository(TestData):

    def test_binding_session(self):
        with self.assertRaises(AttributeError):
            warbdata.DataRepository(session='foo')


if __name__ == '__main__':
    unittest.main()
