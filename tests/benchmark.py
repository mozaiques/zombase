 # -*- coding: utf-8 -*-
import time
import hashlib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import warbase.model
from warbase.model import *
from warbase.data.users import UsersData
from warbase.biz.users import UsersBusiness


class Benchmark():

    def setUp(self):
        self.engine = create_engine(
            'postgres://testpgsql:testpgsqlp4ss@localhost/testpgsql')
        Session = sessionmaker(bind=self.engine)
        warbase.model.Base.metadata.create_all(self.engine)
        self.session = Session()
        self.users_data = UsersData(session=self.session)

    def tearDown(self):
        self.session.close()
        warbase.model.Base.metadata.drop_all(self.engine)

    def run(self):
        t1 = time.time()
        for i in range(1000):
            u = hashlib.md5(str(i)).hexdigest()
            u = u[0:9]
            self.users_data.create(login=u, mail=u + '@b.c')
        t2 = time.time()
        print 'Inserting 1k users took {} ms'.format((t2 - t1) * 1000.0)
        t1 = time.time()
        for i in range(1000):
            u = hashlib.md5(str(i)).hexdigest()
            u = u[0:9]
            user = self.session.query(User.User).filter(User.User.login == u).one()
        t2 = time.time()
        print 'Selecting 1k users took {} ms'.format((t2 - t1) * 1000.0)


if __name__ == '__main__':
    benchmark = Benchmark()
    benchmark.setUp()
    benchmark.run()
    benchmark.tearDown()
