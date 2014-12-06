# -*- coding: utf-8 -*-
import locale


def fstrip(value):
    """Stand for "full strip", return a space-less version of a string."""
    return value.replace(' ', '')


def lcast_int(value):
    """Locale-aware cast a string to an integer."""
    return locale.atoi(value)


def lcast_float(value):
    """Locale-aware cast a string to a float."""
    return locale.atof(value)
