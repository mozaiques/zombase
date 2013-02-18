 # -*- coding: utf-8 -*-
import unittest

from voluptuous import MultipleInvalid

import warbmodel
from warbmodel import *
from warbdata.users import UsersData
from warbdata.applications import ApplicationsData
from warbbiz.users import UsersBusiness

from . import TestData


class TestGetAvailableApp(TestData):

    def setUp(self):
        TestData.setUp(self)
        self.users_data = UsersData(session=self.session)
        self.apps_data = ApplicationsData(session=self.session)
        self.users_biz = UsersBusiness(session=self.session)
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
        apps = self.users_biz.get_applications(user_id=self.user.id)
        self.assertTrue('warfinance' in apps)


if __name__ == '__main__':
    unittest.main()
