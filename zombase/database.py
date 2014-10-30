# -*- coding: utf-8 -*-
import json
import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import TypeDecorator, VARCHAR, CHAR


class MetaBase(object):
    """A meta base class for declarative base.

    Example usage:

        isinstance(SomeSQLAClass, MetaBase):
            ...

    """


class transaction(object):
    """Context manager for database operations.

    Example usage:

        with transaction(dbsession):
            dummy = dbsession.query(Dummy).first()
            dummy.douze = 13

    """

    def __init__(self, dbsession):
        self._dbsession = dbsession

    def __enter__(self):
        """Set the `_zom_in_transaction` attribute in the session."""
        setattr(self._dbsession, '_zom_in_transaction', True)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Unset the `_zom_in_transaction` attribute and commit the
        given session.

        """
        setattr(self._dbsession, '_zom_in_transaction', False)
        self._dbsession.commit()


def db_method(func):
    """Decorator for a database method of a `DataRepository` object.

    The decorated method's object must have its database session
    stored in self._dbsession`.

    """
    def wrapped_commit_func(self, *args, **kwargs):

        # Determine if we'll issue a commit or not. Remove 'commit'
        # from kwargs anyway.
        commit = kwargs.pop('commit', True)
        if getattr(self._dbsession, '_zom_in_transaction', False):
            commit = False

        retval = func(self, *args, **kwargs)

        if commit:
            self._dbsession.commit()

        return retval

    return wrapped_commit_func


class JSONType(TypeDecorator):
    """Represent an immutable structure as a json-encoded string.

    Beware, because of JSON structure, dict can only be keyed with
    strings (in particular, integer cannot be used as key).

    Example usage:

        permissions = Column(JSONType(255))

    """

    impl = VARCHAR

    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value)
        return None

    def process_result_value(self, value, dialect):
        if value is not None:
            return json.loads(value)
        return None


class GUIDType(TypeDecorator):
    """Platform-independent GUID type.

    Uses Postgresql's UUID type, otherwise uses CHAR(32), storing as
    stringified hex values.

    Inspired from: http://docs.sqlalchemy.org/en/rel_0_8/core/types.html

    """

    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value)
            else:
                return "%.32x" % value

    def process_result_value(self, value, dialect):
        if value is not None:
            return uuid.UUID(value)
        return None
