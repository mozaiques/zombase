# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, UnicodeText, ForeignKey
from sqlalchemy.orm import backref, relationship
from voluptuous import Schema, Required

import mozbase.model
import User


class Action(mozbase.model.Base):
    __tablename__ = 'wb_actions'
    id = Column(Integer, primary_key=True)

    datetime = Column(DateTime, index=True)
    message = Column(UnicodeText)

    created_by_id = Column(Integer, ForeignKey('wb_users.id'))
    created_by = relationship(
        'User', backref=backref('actions', order_by=id))


ActionSchema = Schema({
    Required('datetime'): datetime,
    Required('message'): unicode,
    Required('created_by'): User.User,
})
