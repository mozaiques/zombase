# -*- coding: utf-8 -*-
import unittest

from dogpile.cache import make_region

from zombase.cache import cached_property


class TestDatabase(unittest.TestCase):

    class FakeObject():
        id = 1
        _keystores_kt = 'default_ksk_tpl'

        def __init__(self, cache):
            self.cache = cache

        @cached_property(
            'fake:{instance.id}:dum', keystores_kt='bli', cache='cache')
        def dummy(self):
            return 12

        @cached_property(
            'fake:{instance.id}:duml',
            keystores_kt=('bli:{instance.id}', 'blo:{instance.id}'),
            cache='cache')
        def dummy_list(self):
            return 13

        @cached_property('fake:{instance.id}:dumd', cache='cache')
        def dummy_default(self):
            return 14

    def setUp(self):
        self.cache = make_region().configure('dogpile.cache.memory')
        self.object = self.FakeObject(self.cache)

    def tearDown(self):
        del self.object
        del self.cache

    def test_simple_comput(self):
        # Result is correct
        self.assertEqual(self.object.dummy, 12)

        # Result is stored in cache
        self.assertEqual(self.cache.get('fake:1:dum'), 12)

        # Key is added to store
        self.assertEqual(self.cache.get('bli'), ['fake:1:dum'])

    def test_list_store(self):
        self.object.dummy_list

        # Key is added to store
        self.assertEqual(self.cache.get('bli:1'), ['fake:1:duml'])
        self.assertEqual(self.cache.get('blo:1'), ['fake:1:duml'])

    def test_default_key(self):
        self.object.dummy_default
        self.assertEqual(self.cache.get('default_ksk_tpl'), ['fake:1:dumd'])
