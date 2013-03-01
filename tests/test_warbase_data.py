 # -*- coding: utf-8 -*-
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import warbase.data

from . import TestData


class DataRepository(TestData):

    # def test_binding_session(self):
    #     with self.assertRaises(AttributeError):
    #         warbase.data.DataRepository(session='foo')

    pass


if __name__ == '__main__':
    unittest.main()
