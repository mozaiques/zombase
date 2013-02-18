 # -*- coding: utf-8 -*-
import unittest

from warbmodel import Application, User

from . import TestData


class TestModelBase(TestData):

    def test_application(self):
        application = Application.Application()
        self.assertTrue(True)

    def test_user(self):
        user = User.User()
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
