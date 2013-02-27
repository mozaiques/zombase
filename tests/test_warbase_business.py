 # -*- coding: utf-8 -*-
import unittest

from voluptuous import MultipleInvalid

import warbase.model
from warbase.model import *
from warbase.data.users import UsersData
from warbase.data.applications import ApplicationsData
from warbase.biz import BusinessWorker

from . import TestData


class TestGetAvailableApp(TestData):

    def setUp(self):
        TestData.setUp(self)
        self.users_data = UsersData(session=self.session)
        self.apps_data = ApplicationsData(session=self.session)
        self.biz = BusinessWorker(session=self.session)
        self.user = self.users_data.create(
            login='wart',
            mail='a@b.c')
        self.app = self.apps_data.create(
            name='warfinance',
            url='http://warfinance.wartisans.fr/',
            min_permission='view',
            title='WArtisans Finance')
        self.user = self.users_data.add_permission(
            user=self.user,
            permission=('warfinance', 'view'))

    def test_get_apps(self):
        user = self.biz.get.user(user_id=self.user.id)
        self.assertTrue('warfinance' in user.applications)


if __name__ == '__main__':
    unittest.main()
