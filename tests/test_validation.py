# -*- coding: utf-8 -*-
import unittest

from voluptuous import Schema, MultipleInvalid, Required

from mozbase.util.validation import Email, Choice, adapt_dict


class TestModelBase(unittest.TestCase):

    def test_email(self):
        schema = Schema(Email())
        schema('a@b.cc')

    def test_other_email(self):
        schema = Schema(Email())
        schema('a+d@b.cc')

    def test_choice(self):
        schema = Schema(Choice(['a', 'b']))
        schema('a')

    def test_wrong_choice(self):
        schema = Schema(Choice(['a', 'b']))
        with self.assertRaises(MultipleInvalid):
            schema('c')


class TestValidationAdaptDict(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.input_dict = {
            'to_keep': 'dummy',
            'to_remove': 'dummy',
            'to_make_required': 'dummy'
        }

    def test_keep(self):
        output_dict = adapt_dict(self.input_dict, keep=['to_keep'])
        self.assertEqual(output_dict, {'to_keep': 'dummy'})

    def test_remove(self):
        output_dict = adapt_dict(self.input_dict, remove=['to_remove'])
        self.assertEqual(output_dict, {'to_keep': 'dummy',
                                       'to_make_required': 'dummy'})

    def test_make_required(self):
        output_dict = adapt_dict(
            self.input_dict,
            make_required=['to_make_required'])

        def the_assert(output_dict):
            for key in output_dict:
                if str(key) == 'to_make_required' and isinstance(key, Required):
                    return True
            return False
        self.assertTrue(the_assert(output_dict))

if __name__ == '__main__':
    unittest.main()
