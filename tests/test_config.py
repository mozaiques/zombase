# -*- coding: utf-8 -*-
import os
import tempfile
import unittest

from zombase import config


class AbstractTestConfig(object):

    def test_common(self):

        self.assertEqual(self.a_config['KEY_ONE'], 'blaé')
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
            'KEY_ONE': 'blaé',
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
        setattr(test_object, 'KEY_ONE', 'blaé')
        setattr(test_object, 'KEY_TWO', 12)
        setattr(test_object, 'key_three', 'non_capital')

        self.a_config = config.Config()
        self.a_config.from_object(test_object)


class TestFileConfig(unittest.TestCase, AbstractTestConfig):

    def setUp(self):
        self.test_file = tempfile.NamedTemporaryFile(mode='wb', delete=False)

        self.test_file.write(u'# -*- coding: utf-8 -*-\n'.encode('utf-8'))
        self.test_file.write(u'KEY_ONE = "blaé"\n'.encode('utf-8'))
        self.test_file.write(u'KEY_TWO = 12\n'.encode('utf-8'))
        self.test_file.write(u'key_three = "non_capital"\n'.encode('utf-8'))

        self.test_file.close()

        self.a_config = config.Config()
        self.a_config.from_pyfile(self.test_file.name)

    def tearDown(self):
        del self.a_config
        os.remove(self.test_file.name)
        del self.test_file
