 # -*- coding: utf-8 -*-
import unittest
import hashlib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from voluptuous import MultipleInvalid

import warbmodel
from warbmodel import *
from warbdata.users import UsersData


class TestCreateUser(unittest.TestCase):
    def setUp(self):
        engine = create_engine('sqlite:///:memory:', echo=False)
        Session = sessionmaker(bind=engine)
        warbmodel.Base.metadata.create_all(engine)
        self.session = Session()
        self.users_data = UsersData(session=self.session)

    def tearDown(self):
        del self.session
        del self.users_data

    def test_correct_minimal_create(self):
        user = self.users_data.create(login='wart', mail='a@b.c')
        self.assertTrue(isinstance(user, User.User))
        self.assertEqual('wart', user.login)
        self.assertEqual('a@b.c', user.mail)

    def test_correct_create(self):
        user = self.users_data.create(
            login='wart',
            mail='a@b.c',
            hash_password=hashlib.sha1('12').hexdigest(),
            permissions=set(('warbase', 'admin')),
            firstname=u'Raphaël',
            lastname=u'Gràdübé',)
        self.assertEqual('wart', user.login)
        self.assertEqual('a@b.c', user.mail)
        self.assertEqual(u'Raphaël', user.firstname)
        self.assertEqual(u'Gràdübé', user.lastname)
        self.assertEqual(set(('warbase', 'admin')), user.permissions)

    def test_no_mail(self):
        with self.assertRaises(MultipleInvalid):
            self.users_data.create(login='wart')

    def test_no_login(self):
        with self.assertRaises(MultipleInvalid):
            self.users_data.create(mail='a@b.c')


if __name__ == '__main__':
    unittest.main()
