 # -*- coding: utf-8 -*-
import unittest
import hashlib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from voluptuous import MultipleInvalid

import warbase.model
from warbase.model import *
from warbase.data.users import UsersData

from . import TestData


class TestCreateUser(TestData):

    def setUp(self):
        TestData.setUp(self)
        self.users_data = UsersData(session=self.session)

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
            permissions=['warbase'],
            firstname=u'Raphaël',
            lastname=u'Gràdübé',)
        self.assertEqual('wart', user.login)
        self.assertEqual('a@b.c', user.mail)
        self.assertEqual(u'Raphaël', user.firstname)
        self.assertEqual(u'Gràdübé', user.lastname)
        self.assertEqual(['warbase'], user.permissions)

    def test_no_mail(self):
        with self.assertRaises(MultipleInvalid):
            self.users_data.create(login='wart')

    def test_no_login(self):
        with self.assertRaises(MultipleInvalid):
            self.users_data.create(mail='a@b.c')

    def test_add_permission(self):
        user = self.users_data.create(
            login='wart',
            mail='a@b.c')


if __name__ == '__main__':
    unittest.main()
