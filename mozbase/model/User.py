# -*- coding: utf-8 -*-
"""Default implementation of an User object which would be a perfect
base for 99% of the use cases.

Authentication-wise, an email adress is all that we need to authenticate
an user. In addition, having a salt generated randomly for each user and
storing it next to the hashed+salted password is a best practice.

Regarding the name(s) of an user, it makes sense to store the "full"
name of an user for really specific use cases (document editing for
instance) and to also ask for a shortname that will be used to identify
the user in some part of the application.

"""
from sqlalchemy import Column, Integer, String, Unicode, PickleType
from voluptuous import Schema, Required, All, Length

import mozbase.model


class User(mozbase.model.Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)

    email = Column(String(length=50), unique=True, index=True)

    # sha1 hash, with salt:
    #     hashlib.sha1('{}{}'.format(salt, password)).hexdigest()
    password_hash = Column(String(length=40))

    # salt generated with: `'{:x}'.format(random.randrange(256**15))`
    password_salt = Column(String(length=30))

    # could be anything, here we store a list of roles (strings)
    permissions = Column(PickleType())

    # does not make sense to separate firstname/lastname
    name = Column(Unicode(length=60))

    # A shorter name for interface/application needs, might be set as
    # "unique".
    shortname = Column(Unicode(length=15))


PermissionSchema = Schema(str)


UserSchema = Schema({
    Required('email'): All(str, Length(min=3, max=50)),
    'password_hash': All(str, Length(min=40, max=40)),
    'password_salt': All(str, Length(min=30, max=30)),
    'permissions': [PermissionSchema],
    'name': All(unicode, Length(min=3, max=50)),
    'shortname': All(unicode, Length(min=3, max=15)),
})
