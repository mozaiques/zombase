# -*- coding: utf-8 -*-
"""Extra validation schemas"""
import re

from voluptuous import Invalid


# from http://stackoverflow.com/a/15292968/2536838
def Email(msg=None):
    def f(v):
        if re.match('[\w\.\-]*@[\w\.\-]*\.\w+', v):
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
