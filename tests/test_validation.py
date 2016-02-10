# -*- coding: utf-8 -*-
import datetime
import unittest
import uuid

from voluptuous import Schema, MultipleInvalid, Required, Invalid

from zombase import validation


class TestUUID(unittest.TestCase):

    def test_uuid(self):
        self.assertTrue(validation.is_valid_uuid(uuid.uuid4()))
        self.assertTrue(validation.is_valid_uuid(str(uuid.uuid4())))
        self.assertFalse(validation.is_valid_uuid('bla'))


class TestMail(unittest.TestCase):

    def test_mail(self):
        schema = Schema(validation.Mail())
        schema('a@b.cc')

    def test_other_mail(self):
        schema = Schema(validation.Mail())
        schema('a+d@b.cc')
        schema('a+d@dudouze.paris')
        schema('a+d@joebla.dudouze.paris')

    def test_lower_mail(self):
        schema = Schema(validation.Mail())
        schema_lower = Schema(validation.Mail(lower=True))

        self.assertEqual(schema('aZ@b.cc'), 'aZ@b.cc')
        self.assertEqual(schema_lower('aZ@b.cc'), 'az@b.cc')

    def test_invalid_mail(self):
        schema = Schema(validation.Mail())

        with self.assertRaises(MultipleInvalid):
            schema('a a@b.c')


class TestFloatable(unittest.TestCase):

    def test_simple_floatable(self):
        schema = Schema(validation.Floatable())
        self.assertEqual(schema('1.12'), 1.12)
        self.assertEqual(schema(1.12), 1.12)

    def test_empty_to_none_floatable(self):
        schema = Schema(validation.Floatable(empty_to_none=True))
        self.assertEqual(schema(''), None)

    def test_uncasted_floatable(self):
        schema = Schema(validation.Floatable(cast=False))
        self.assertEqual(schema('3.0'), '3.0')

    def test_invalid_floatable(self):
        schema = Schema(validation.Floatable())

        with self.assertRaises(MultipleInvalid):
            schema('3.a')

        with self.assertRaises(MultipleInvalid):
            schema(None)


class TestIntegeable(unittest.TestCase):

    def test_simple_integeable(self):
        schema = Schema(validation.Integeable())
        self.assertEqual(schema('1'), 1)

    def test_empty_to_none_integeable(self):
        schema = Schema(validation.Integeable(empty_to_none=True))
        self.assertEqual(schema(''), None)

    def test_uncasted_integeable(self):
        schema = Schema(validation.Integeable(cast=False))
        self.assertEqual(schema('3'), '3')

    def test_invalid_integeable(self):
        schema = Schema(validation.Integeable())
        with self.assertRaises(MultipleInvalid):
            schema('a')

    def test_invalid_integeable_but_floatable(self):
        schema = Schema(validation.Integeable())

        with self.assertRaises(MultipleInvalid):
            schema('3.2')

        with self.assertRaises(MultipleInvalid):
            schema(3.2)

        with self.assertRaises(MultipleInvalid):
            schema(None)


class TestDateable(unittest.TestCase):

    def test_simple_no_cast(self):
        schema = Schema(validation.Dateable())
        self.assertEqual(
            schema(datetime.date(2015, 11, 13)), datetime.date(2015, 11, 13))

    def test_simple_cast(self):
        schema = Schema(validation.Dateable())
        self.assertEqual(schema('2015-11-13'), datetime.date(2015, 11, 13))

    def test_cast_w_format(self):
        schema = Schema(validation.Dateable(format='%Y%m%d'))
        self.assertEqual(schema('20151113'), datetime.date(2015, 11, 13))

    def test_nocast_w_format(self):
        schema = Schema(validation.Dateable(cast=False, format='%Y%m%d'))
        value = '20151113'
        nocast = schema('20151113')
        self.assertEqual(nocast, value)

    def test_wrong_choice_in_dict(self):
        schema = Schema(validation.Dateable())
        with self.assertRaises(Invalid):
            schema('20151113')


class TestChoice(unittest.TestCase):

    def test_choice(self):
        schema = Schema(validation.Choice(['a', 'b']))
        schema('a')

    def test_wrong_choice(self):
        schema = Schema(validation.Choice(['a', 'b']))
        with self.assertRaises(MultipleInvalid):
            schema('c')

    def test_wrong_choice_in_dict(self):
        # The error message system is different in a dict.
        schema = Schema({
            'bla': validation.Choice(['a', 'b']),
        })
        with self.assertRaises(MultipleInvalid):
            schema({'bla': 'c'})


class TestAdaptDict(unittest.TestCase):

    input_dict = {
        'to_keep': 'dummy',
        'to_remove': 'dummy',
        'to_make_required': 'dummy'
    }

    def test_keep(self):
        output_dict = validation.adapt_dict(self.input_dict, keep=['to_keep'])
        self.assertEqual(output_dict, {'to_keep': 'dummy'})

    def test_remove(self):
        output_dict = validation.adapt_dict(
            self.input_dict, remove=['to_remove'])
        self.assertEqual(output_dict, {'to_keep': 'dummy',
                                       'to_make_required': 'dummy'})

    def test_make_required(self):
        output_dict = validation.adapt_dict(
            self.input_dict, make_required=['to_make_required'])

        def the_assert(output_dict):
            for key in output_dict:
                if (str(key) == 'to_make_required' and
                        not isinstance(key, Required)):
                    return False
                elif (str(key) != 'to_make_required' and
                        isinstance(key, Required)):
                    return False
            return True
        self.assertTrue(the_assert(output_dict))


class TestSchemaDictNone(unittest.TestCase):

    schema_dict = {
        Required('id'): int,
        'name': str,
        'value': int,
        'target': int,
    }

    def test_wrong_init(self):
        with self.assertRaises(ValueError):
            validation.SchemaDictNone(['a', 'b'])

    def test_basic_schema(self):
        schema = validation.SchemaDictNone(self.schema_dict)

        data = {'id': 2, 'name': 'bla', 'value': None}
        new_data = schema(data)

        self.assertEqual(new_data['value'], None)
        self.assertEqual(new_data['name'], 'bla')

    def test_schema_with_not_none(self):
        schema = validation.SchemaDictNone(
            self.schema_dict, not_none=('name',))

        data = {'id': 2, 'value': None, 'name': None}

        with self.assertRaises(MultipleInvalid):
            schema(data)
