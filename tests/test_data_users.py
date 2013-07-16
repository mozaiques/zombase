# -*- coding: utf-8 -*-
import unittest
import hashlib

from voluptuous import MultipleInvalid

from mozbase.model import User

from . import TestData


class TestCreateUser(TestData):

    def setUp(self):
        TestData.setUp(self)
        self.user_data = self.biz.user

    def test_correct_minimal_create(self):
        user = self.user_data.create(email='a@b.c')
        self.assertTrue(isinstance(user, User.User))
        self.assertEqual('a@b.c', user.email)

    def test_correct_create(self):
        user = self.user_data.create(
            email='a@b.c',
            password_hash=hashlib.sha1('12').hexdigest(),
            permissions=['mozbase'],
            name=u'Raphaël Gràdübé',
            shortname=u'Wäert',)
        self.assertEqual('a@b.c', user.email)
        self.assertEqual(u'Raphaël Gràdübé', user.name)
        self.assertEqual(u'Wäert', user.shortname)
        self.assertEqual(['mozbase'], user.permissions)

    def test_no_mail(self):
        with self.assertRaises(MultipleInvalid):
            self.user_data.create(login='wart')

    def test_add_permission(self):
        us = self.user_data.create(email='a@b.c')
        self.user_data.add_permission(user=us, permission='bla')
        self.assertTrue('bla' in us.permissions)


if __name__ == '__main__':
    unittest.main()
