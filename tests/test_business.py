# -*- coding: utf-8 -*-
from mozbase.data.user import UserData
from mozbase.biz import BusinessWorker

from . import TestData


class Bli(object):
    pass
bli = Bli()


class Bla(object):
    user = bli


class TestBusinessObject(TestData):

    def setUp(self):
        TestData.setUp(self)
        self.user_data = UserData(dbsession=self.session)
        self.user = self.user_data.create(email='a@b.c')
        self.user = self.user_data.add_permission(
            user=self.user,
            permission='finances')
        self.biz = BusinessWorker(dbsession=self.session, user=self.user)

    def test_get_permission(self):
        user = self.biz.user.get(user_id=self.user.id)
        self.assertTrue('finances' in user.permissions)

    def test_patch_no_export(self):
        bla = Bla()

        with self.assertRaises(TypeError):
            self.biz.patch(bla)

    def test_patch(self):
        bla = Bla()
        setattr(self.biz, '_patch_exports', ['user', 'action'])
        self.biz.patch(bla)

        self.assertEqual(self.biz.action, bla.action)
        self.assertEqual(bli, bla.user)

    def test_patch_children(self):
        bla = Bla()
        setattr(self.biz, '_patch_exports', ['user', 'action'])
        setattr(self.biz.user, '_patch_exports', ['get'])
        self.biz.patch(bla)

        self.assertEqual(self.biz.user.get, bla.user.get)
