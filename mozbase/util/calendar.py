# -*- coding: utf-8 -*-
import datetime
from sqlalchemy import Column, Date, Time


class CalendarDbItem(object):
    date = Column(Date)
    time_start = Column(Time)
    time_end = Column(Time)

    @property
    def datetime_start(self):
        return datetime.datetime.combine(self.date, self.time_start)

    @property
    def datetime_end(self):
        return datetime.datetime.combine(self.date, self.time_end)
