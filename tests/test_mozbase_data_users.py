 # -*- coding: utf-8 -*-
import unittest
import hashlib

from voluptuous import MultipleInvalid

from mozbase.model import User
from mozbase.data.user import UserData

from . import TestData


class TestCreateUser(TestData):

    def setUp(self):
        TestData.setUp(self)
        self.user_data = UserData(dbsession=self.session)

    def test_correct_minimal_create(self):
        user = self.user_data.create(login='wart', mail='a@b.c')
        self.assertTrue(isinstance(user, User.User))
        self.assertEqual('wart', user.login)
        self.assertEqual('a@b.c', user.mail)

    def test_correct_create(self):
        user = self.user_data.create(
            login='wart',
            mail='a@b.c',
            hash_password=hashlib.sha1('12').hexdigest(),
            permissions=['mozbase'],
            firstname=u'Raphaël',
            lastname=u'Gràdübé',)
        self.assertEqual('wart', user.login)
        self.assertEqual('a@b.c', user.mail)
        self.assertEqual(u'Raphaël', user.firstname)
        self.assertEqual(u'Gràdübé', user.lastname)
        self.assertEqual(['mozbase'], user.permissions)

    def test_no_mail(self):
        with self.assertRaises(MultipleInvalid):
            self.user_data.create(login='wart')

    def test_no_login(self):
        with self.assertRaises(MultipleInvalid):
            self.user_data.create(mail='a@b.c')

    def test_add_permission(self):
        self.user_data.create(
            login='wart',
            mail='a@b.c')


if __name__ == '__main__':
    unittest.main()
