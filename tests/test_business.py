# -*- coding: utf-8 -*-
from . import TestData


class Bli(object):
    pass
bli = Bli()


class Bla(object):
    user = bli


class TestBusinessObject(TestData):

    def setUp(self):
        TestData.setUp(self)
        self.user = self.biz.user.add_permission(
            user=self.user,
            permission='finances')

    def test_get_permission(self):
        user = self.biz.user.get(user_id=self.user.id)
        self.assertTrue('finances' in user.permissions)

    def test_patch_no_export(self):
        bla = Bla()

        with self.assertRaises(TypeError):
            self.biz._patch(bla)

    def test_patch(self):
        bla = Bla()
        setattr(self.biz, '_patch_exports', ['user', 'action'])
        self.biz._patch(bla)

        self.assertEqual(self.biz.action, bla.action)
        self.assertEqual(bli, bla.user)

    def test_patch_children(self):
        bla = Bla()
        setattr(self.biz, '_patch_exports', ['user', 'action'])
        setattr(self.biz.user, '_patch_exports', ['get'])
        self.biz._patch(bla)

        self.assertEqual(self.biz.user.get, bla.user.get)
