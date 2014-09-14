# -*- coding: utf-8 -*-
import unittest

from zombase import config


class AbstractTestConfig(object):

    def test_common(self):

        self.assertEqual(self.a_config['KEY_ONE'], 'bla')
        self.assertEqual(self.a_config['KEY_TWO'], 12)

        with self.assertRaises(config.ConfigError):
            self.a_config['key_three']

        with self.assertRaises(config.ConfigError):
            self.a_config['KEY_FOUR']

    def tearDown(self):
        del self.a_config


class TestDictConfig(unittest.TestCase, AbstractTestConfig):

    def setUp(self):
        test_dict = {
            'KEY_ONE': 'bla',
            'KEY_TWO': 12,
            'key_three': 'non_capital'
        }

        self.a_config = config.Config()
        self.a_config.from_dict(test_dict)


class TestObjectConfig(unittest.TestCase, AbstractTestConfig):

    def setUp(self):
        class DummyObject(object):
            pass

        test_object = DummyObject()
        setattr(test_object, 'KEY_ONE', 'bla')
        setattr(test_object, 'KEY_TWO', 12)
        setattr(test_object, 'key_three', 'non_capital')

        self.a_config = config.Config()
        self.a_config.from_object(test_object)
