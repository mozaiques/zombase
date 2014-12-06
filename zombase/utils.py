# -*- coding: utf-8 -*-
import locale


def fstrip(value):
    """Stand for "full strip", return a space-less version of a string."""
    return value.replace(' ', '')


def lcast_int(value):
    """Locale-aware cast a value to an integer."""
    if isinstance(value, int):
        return value
    return locale.atoi(value)


def lcast_float(value):
    """Locale-aware cast a value to a float."""
    if isinstance(value, float):
        return value
    return locale.atof(value)
