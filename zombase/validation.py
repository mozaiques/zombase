# -*- coding: utf-8 -*-
"""Validation utilities and extra schemas. Mostly built around
voluptuous.

"""
import datetime
import decimal
import math
import re
import uuid

from voluptuous import Invalid, Required, Schema

import six


def is_valid_uuid(value):
    if isinstance(value, uuid.UUID):
        return True

    try:
        maybe_value = uuid.UUID(value, version=4)
    except ValueError:
        return False

    return maybe_value.hex == value.replace('-', '').replace(' ', '')


_mail_regexp = re.compile('[^@]+@[^@]+\.[^@]+')


def is_valid_mail(raw_mail):
    if re.match(_mail_regexp, raw_mail) and ' ' not in raw_mail:
        return True
    return False


def Mail(empty_to_none=False, msg=None, lower=False):
    def f(value):
        if value in [None, ''] and empty_to_none:
            return None

        if not is_valid_mail(value):
            raise Invalid(msg or ('Incorrect mail address.'))

        if lower:
            return value.lower()
        return value
    return f


def Integeable(empty_to_none=False, cast=True, msg=None):
    def f(value):
        if value in [None, ''] and empty_to_none:
            return None

        try:
            casted_value = int(value)
        except (ValueError, TypeError):
            raise Invalid(msg or 'Given value cannot be casted to int.')

        if str(value) != str(casted_value):
            raise Invalid(msg or 'Given value cannot be casted to int.')

        if cast:
            return casted_value
        return value
    return f


def Floatable(empty_to_none=False, cast=True, nan_allowed=False, msg=None):
    def f(value):
        if value in [None, ''] and empty_to_none:
            return None

        try:
            casted_value = float(value)
        except (ValueError, TypeError):
            raise Invalid(msg or 'Given value cannot be casted to float.')

        if not nan_allowed and math.isnan(casted_value):
            raise Invalid(msg or 'Given value is NaN.')

        if cast:
            return casted_value
        return value
    return f


def Decimable(empty_to_none=False, cast=True, nan_allowed=False, msg=None):
    def f(value):
        if value in [None, ''] and empty_to_none:
            return None

        try:
            if isinstance(value, float):
                casted_value = decimal.getcontext()\
                    .create_decimal_from_float(value)
            else:
                casted_value = decimal.Decimal(value)
        except decimal.InvalidOperation:
            raise Invalid(msg or 'Given value cannot be casted to a decimal.')

        if not nan_allowed and math.isnan(casted_value):
            raise Invalid(msg or 'Given value is NaN.')

        if cast:
            return casted_value
        return value
    return f


def Dateable(empty_to_none=False, cast=True, format=None, msg=None):
    if format is None:
        format = '%Y-%m-%d'

    def f(value):
        if value in [None, ''] and empty_to_none:
            return None

        if isinstance(value, datetime.date):
            return value

        try:
            casted_value = datetime.datetime.strptime(value, format)
        except ValueError:
            raise Invalid(msg or 'Given value cannot be casted to a date.')

        if cast:
            return casted_value.date()
        return value
    return f


def Choice(in_list, msg=None):
    def f(value):
        if value not in in_list:
            error_msg = 'Incorrect choice, expected one of the '\
                        'following: "{}".'.format(', '.join(in_list))
            raise Invalid(msg or error_msg)
        return value
    return f


def adapt_dict(input_dict, keep=None, remove=None, make_required=None):
    """Adapt a validation dictionary.

    This is intended to transform "base" dictionaries, with all possible
    arguments for a model, into create and update schemas. The returned
    dict can be used to build a Schema.

    Keyword arguments:
        input_dict (mandatory) -- initial dictionary
        keep -- list of keys to keep
        remove -- list of keys to remove
        make_required -- list of keys to wrap in Required() and keep

    If only `d` is given, return Schema(d).

    If both `keep` and `remove` are provided, `remove` is ignored.
    `make_required` (if provided) is applied over the remaining keys
    after keep or remove, i.e. if a key is removed or not kept and still
    mentioned in the `make_required` list, it will be ignored.

    """
    if keep:
        output_dict = {}
        for k in keep:
            output_dict[k] = input_dict[k]

    elif remove:
        output_dict = input_dict.copy()
        for k in remove:
            output_dict.pop(k)

    else:
        output_dict = input_dict.copy()

    if make_required:
        for k in make_required:
            output_dict[Required(k)] = output_dict.pop(k)

    return output_dict


class SchemaDictNone(Schema):
    """Custom implementation of a dict schema where all values except
    thoses specified in `not_none` (and thoses required) could be None.

    The following are equivalent:
        Schema({
            Required('id'): int,
            'name': unicode,
            'value': Any(None, int),
            'target': Any(None, str),
        })

        SchemaDictNone({
            Required('id'): int,
            'name': unicode,
            'value': int,
            'target': int,
        }, not_none=['name'])

    """

    def __init__(self, schema, required=False, extra=False, not_none=False):
        if not isinstance(schema, dict):
            raise ValueError('This special Schema is intented to be used with '
                             'dict only.')
        Schema.__init__(self, schema, required, extra)
        self._not_none = not_none if not_none is not False else ()

    def __call__(self, data):
        _data = data.copy()
        popped = []

        for k, v in six.iteritems(data):
            if v is None and k not in self._not_none:
                _data.pop(k)
                popped.append((k, v))

        schema_out = Schema.__call__(self, _data)
        for k, v in popped:
            schema_out[k] = v

        return schema_out
