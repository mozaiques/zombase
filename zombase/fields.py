# -*- coding: utf-8 -*-
import datetime

from wtforms import IntegerField, Field


class CheckboxSelectField(Field):
    false_values = ('false', '')
    checked_value = 'checked'
    unchecked_value = 'unchecked_value'

    def __init__(self, label=None, validators=None, checked_value=None,
                 unchecked_value=None, checked_by_default=False, **kwargs):
        Field.__init__(self, label, validators, **kwargs)

        self.checked_by_default = checked_by_default

        if checked_value is not None:
            self.checked_value = checked_value

        if unchecked_value is not None:
            self.unchecked_value = unchecked_value

    def process_data(self, value):
        if value is None:
            if self.checked_by_default:
                self.data = self.checked_value
            else:
                self.data = self.unchecked_value

        elif value in (self.checked_value, self.unchecked_value):
            self.data = value

        else:
            raise AttributeError('Unrecognized value.')

    def process_formdata(self, valuelist):
        if not valuelist or valuelist[0] in self.false_values:
            self.data = self.unchecked_value
        else:
            self.data = self.checked_value


class TimeField(Field):

    def __init__(self, label=None, validators=None, format='%H:%M',
                 empty_to_none=False, **kwargs):
        Field.__init__(self, label, validators, **kwargs)
        self.format = format
        self.empty_to_none = empty_to_none

    def process_formdata(self, valuelist):
        if valuelist:
            time_str = ' '.join(valuelist)

            if not time_str and self.empty_to_none:
                self.data = None
                return

            try:
                self.data = datetime.datetime.strptime(
                    time_str, self.format).time()
            except ValueError:
                self.data = None
                raise ValueError(self.gettext('Not a valid time value.'))


class CustomIntegerField(IntegerField):

    def __init__(self, label=None, validators=None, empty_to_none=False,
                 **kwargs):
        Field.__init__(self, label, validators, **kwargs)
        self.empty_to_none = empty_to_none

    def process_formdata(self, valuelist):
        if valuelist:
            int_str = ' '.join(valuelist)

            if int_str == '' and self.empty_to_none:
                self.data = None
                return

            return IntegerField.process_formdata(self, valuelist)
