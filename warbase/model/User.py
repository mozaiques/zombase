from sqlalchemy import Column, Integer, String, Unicode, PickleType
from voluptuous import Schema, Required, All, Length

from . import Base


class User(Base):
    __tablename__ = 'wb_users'
    id = Column(Integer, primary_key=True)

    # These two fields cannot be null
    login = Column(String(length=10), unique=True, index=True)  # ASCII only
    mail = Column(String(length=50), unique=True, index=True)

    hash_password = Column(String(length=40))  # sha1 hash, wo salt
    permissions = Column(PickleType)  # Store list of tuple

    firstname = Column(Unicode(length=30))
    lastname = Column(Unicode(length=30))

PermissionSchema = Schema((str, str))

UserSchema = Schema({
    Required('login'): All(str, Length(min=3, max=10)),
    Required('mail'): All(str, Length(min=3, max=50)),
    'hash_password': All(str, Length(min=40, max=40)),
    'permissions': [PermissionSchema],
    'firstname': All(unicode, Length(min=3, max=30)),
    'lastname': All(unicode, Length(min=3, max=30)),
})
