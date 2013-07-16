# -*- coding: utf-8 -*-
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dogpile.cache import make_region

import mozbase.model
from mozbase.model import *
from mozbase.biz import BusinessWorker


class TestData(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')

        mozbase.model.Base.metadata.create_all(self.engine)

        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        cache_region = make_region().configure('dogpile.cache.memory')
        setattr(self.session, 'cache', cache_region)

        self.user = User.User(email='a@bb.cc')
        self.session.add(self.user)
        self.session.commit()
        self.biz = BusinessWorker(dbsession=self.session, user=self.user)

    def tearDown(self):
        del self.user
        del self.biz
        self.session.close()
        mozbase.model.Base.metadata.drop_all(self.engine)


if __name__ == '__main__':
    unittest.main()
