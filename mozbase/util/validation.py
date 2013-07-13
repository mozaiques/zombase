# -*- coding: utf-8 -*-
"""Extra validation schemas"""
import re

from voluptuous import Invalid


def Email(msg=None):
    def f(v):
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", v):
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
