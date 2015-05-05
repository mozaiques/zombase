# -*- coding: utf-8 -*-
"""Validation utilities and extra schemas. Mostly built around
voluptuous.

"""
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


_email_regexp = re.compile("^[A-Za-z0-9_\-\.\+]+\@(\[?)[a-zA-Z0-9\-\.]"
                           "+\.([a-zA-Z]{2,3}|[0-9]{1,3})(\]?)$")


def is_valid_email(raw_email):
    if re.match(_email_regexp, raw_email):
        return True
    return False


def Email(msg=None, lower=False):
    def f(value):
        if not is_valid_email(value):
            raise Invalid(msg or ('Incorrect email address.'))

        if lower:
            return value.lower()
        return value
    return f


def Floatable(empty_to_none=False, cast=True, msg=None):
    def f(value):
        if not value and empty_to_none:
            return None

        try:
            casted_value = float(value)
        except (ValueError, TypeError):
            raise Invalid(msg or 'Given value cannot be casted to float.')

        if cast:
            return casted_value
        return value
    return f


def Integeable(empty_to_none=False, cast=True, msg=None):
    def f(value):
        if not value and empty_to_none:
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
