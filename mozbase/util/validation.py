# -*- coding: utf-8 -*-
"""Validation utilities and extra schemas."""
import re

from voluptuous import Invalid, Required


def Email(msg=None):
    def f(v):
        if re.match(r'^[A-Za-z0-9_\-\.\+]+\@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,3}|[0-9]{1,3})(\]?)$', v):
            return v
        else:
            raise Invalid(msg or ('incorrect email address'))
    return f


def Choice(in_list, msg=None):
    def f(v):
        if not v in in_list:
            error_msg = 'incorrect choice, expected one of the following: "{}"'\
                .format(', '.join(in_list))
            raise Invalid(msg or error_msg)
    return f


def adapt_dict(input_dict, keep=None, remove=None, make_required=None):
    """Adapt a validation dictionary.

    This is intended to transform "base" dictionaries, with all possible
    arguments for a model, into create and update schemas. The returned dict
    can be used to build a Schema.

    Keyword arguments:
        input_dict (mandatory) -- initial dictionary
        keep -- list of keys to keep
        remove -- list of keys to remove
        make_required -- list of keys to wrap in Required() and keep

    If only `d` is given, return Schema(d).

    If both `keep` and `remove` are provided, `remove` is ignored.
    `make_required` (if provided) is applied over the remaining keys after
    keep or remove, i.e. if a key is removed or not kept and still mentioned in
    the `make_required` list, it will be ignored.

    """

    # Process keep / remove

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

    # Transform keys of make_required
    if make_required:
        for k in make_required:
            output_dict[Required(k)] = output_dict.pop(k)

    return output_dict
