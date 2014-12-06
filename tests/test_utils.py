# -*- coding: utf-8 -*-
import unittest

from zombase import utils


class TestUtils(unittest.TestCase):

    def test_fstrip(self):
        self.assertEqual(utils.fstrip('1 1 1'), '111')

    def test_lcast_int(self):
        self.assertEqual(utils.lcast_int(8), 8)
        self.assertEqual(utils.lcast_int('1'), 1)
        self.assertEqual(utils.lcast_int('1 2', strip=True), 12)

    def test_lcast_float(self):
        self.assertEqual(utils.lcast_float(2.4), 2.4)
        self.assertEqual(utils.lcast_float('1.1'), 1.1)
        self.assertEqual(utils.lcast_float('1 2.4', strip=True), 12.4)
