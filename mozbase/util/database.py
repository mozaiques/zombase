# -*- coding: utf-8 -*-
import threading
import json

from sqlalchemy.types import TypeDecorator, VARCHAR


class transaction():
    """Context manager for database operations.

    Example usage:

        with transaction(dbsession):
            dummy = dbsession.query(Dummy).first()
            dummy.douze = 13

    """

    def __init__(self, dbsession):
        self._dbsession = dbsession
        self.current_thread = threading.current_thread()

    def __enter__(self):
        """Set the thread global `mozbase_transaction` attribute."""
        setattr(self.current_thread, 'warbase_transaction', True)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Unset the thread global `mozbase_transaction` attribute and
        commit the given session.

        """
        setattr(self.current_thread, 'mozbase_transaction', False)
        self._dbsession.commit()


def db_method():
    """Decorator for a database method of a `DataRepository` object.

    The decorated method's object must have its database session
    stored in self._dbsession`.

    """

    def decorator_func(func):

        def wrapper_func(self, *args, **kwargs):

            # Determine if we'll issue a commit or not. Remove 'commit'
            # from kwargs anyway.
            commit = kwargs.pop('commit', True)
            if getattr(threading.current_thread(), 'mozbase_transaction', False):
                commit = False

            retval = func(self, *args, **kwargs)

            if commit:
                self._dbsession.commit()

            return retval

        return wrapper_func

    return decorator_func


class JSONType(TypeDecorator):
    """Represent an immutable structure as a json-encoded string.

    Example usage:

        permission = JSONType(255)

    """

    impl = VARCHAR

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)

        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value
