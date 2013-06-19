# -*- coding: utf-8 -*-
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dogpile.cache import make_region

import mozbase.model
from mozbase.model import *


class TestData(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Session = sessionmaker(bind=self.engine)
        mozbase.model.Base.metadata.create_all(self.engine)
        self.session = Session()
        cache_region = make_region().configure('dogpile.cache.memory')
        setattr(self.session, 'cache', cache_region)

    def tearDown(self):
        self.session.close()
        mozbase.model.Base.metadata.drop_all(self.engine)


if __name__ == '__main__':
    unittest.main()
