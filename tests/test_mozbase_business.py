# -*- coding: utf-8 -*-
import unittest

from mozbase.data.user import UserData
from mozbase.biz import BusinessWorker

from . import TestData


class TestGetAvailableApp(TestData):

    def setUp(self):
        TestData.setUp(self)
        self.user_data = UserData(dbsession=self.session)
        self.user = self.user_data.create(
            login='wart',
            mail='a@b.c')
        self.user = self.user_data.add_permission(
            user=self.user,
            permission='finances')
        self.biz = BusinessWorker(dbsession=self.session, user=self.user)

    def test_get_apps(self):
        user = self.biz.user.get(user_id=self.user.id)
        self.assertTrue('finances' in user.permissions)


if __name__ == '__main__':
    unittest.main()
