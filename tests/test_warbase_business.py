 # -*- coding: utf-8 -*-
import unittest

from voluptuous import MultipleInvalid

import warbase.model
from warbase.model import *
from warbase.data.users import UsersData
from warbase.biz import BusinessWorker

from . import TestData


class TestGetAvailableApp(TestData):

    def setUp(self):
        TestData.setUp(self)
        self.users_data = UsersData(session=self.session)
        self.biz = BusinessWorker(session=self.session)
        self.user = self.users_data.create(
            login='wart',
            mail='a@b.c')
        self.user = self.users_data.add_permission(
            user=self.user,
            permission='finances')

    def test_get_apps(self):
        user = self.biz.get.user(user_id=self.user.id)
        self.assertTrue('finances' in user.permissions)


if __name__ == '__main__':
    unittest.main()
