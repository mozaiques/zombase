# -*- coding: utf-8 -*-
import unittest

from voluptuous import Schema

from mozbase.util.validation import Email, Choice


class TestModelBase(unittest.TestCase):

    def test_email(self):
        schema = Schema(Email())
        schema('a@b.c')

    def test_choice(self):
        schema = Schema(Choice(['a', 'b']))
        schema('a')

    def test_wrong_choice(self):
        schema = Schema(Choice(['a', 'b']))
        schema('c')


if __name__ == '__main__':
    unittest.main()
