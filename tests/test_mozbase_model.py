 # -*- coding: utf-8 -*-
import unittest

from mozbase.model import User, Action

from . import TestData


class TestModelBase(TestData):

    def test_user(self):
        User.User()
        self.assertTrue(True)

    def test_action(self):
        Action.Action()
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
