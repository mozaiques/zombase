# -*- coding: utf-8 -*-
import locale


def fstrip(value):
    """Stand for "full strip", return a space-less version of a (unicode)
    string.

    """
    return value.replace(u'\xa0', u'').replace(u' ', u'')


def lcast_int(value, strip=False):
    """Locale-aware cast a value to an integer."""
    if isinstance(value, int):
        return value
    if strip:
        value = fstrip(value)
    return locale.atoi(value)


def lcast_float(value, strip=False):
    """Locale-aware cast a value to a float."""
    if isinstance(value, float):
        return value
    if strip:
        value = fstrip(value)
    return locale.atof(value)
