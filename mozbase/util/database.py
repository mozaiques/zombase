# -*- coding: utf-8 -*-
import json

from sqlalchemy.types import TypeDecorator, VARCHAR
from sqlalchemy.orm import object_session
from dogpile.cache.api import NoValue


class transaction():
    """Context manager for database operations.

    Example usage:

        with transaction(dbsession):
            dummy = dbsession.query(Dummy).first()
            dummy.douze = 13

    """

    def __init__(self, dbsession):
        self._dbsession = dbsession

    def __enter__(self):
        """Set the `mozbase_transaction` attribute in the session."""
        setattr(self._dbsession, 'mozbase_transaction', True)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Unset the `mozbase_transaction` attribute and commit the
        given session.

        """
        setattr(self._dbsession, 'mozbase_transaction', False)
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
        if getattr(self._dbsession, 'mozbase_transaction', False):
            commit = False

        retval = func(self, *args, **kwargs)

        if commit:
            self._dbsession.commit()

        return retval

    return wrapped_commit_func


def cached_property(key_template):
    """Decorator for a method of a SQLA-object.

    Act like the `@property` decorator, but handle interactions with
    the cache.

    Argument:
        key_template -- template of the key that will be used in cache.

    Example usage:

        @cached_property('prestation:{prestation.id}:margin')
        def margin(self):
            return self.selling_price - self.cost

    """

    def decorator(func):

        def wrapped(self, *args, **kwargs):
            cache = object_session(self).cache
            format_dict = dict()
            format_dict[self._name] = self

            key = key_template.format(**format_dict)
            cache_value = cache.get(key)

            # If we have the value in cache, we just return it.
            if not isinstance(cache_value, NoValue):
                return cache_value

            # Run the computation
            value = func(self, *args, **kwargs)

            # Store value in cache
            cache.set(key, value)

            # Add the new key to the key store
            key_store_key = self._key_store_key_template.format(**format_dict)
            key_store = cache.get(key_store_key)

            # If the key_store hasn't been created yet, we initialize it
            if isinstance(key_store, NoValue):
                key_store = []

            key_store.append(key)
            cache.set(key_store_key, key_store)

            return value

        return property(wrapped)

    return decorator


class JSONType(TypeDecorator):
    """Represent an immutable structure as a json-encoded string.

    Example usage:

        permissions = JSONType(255)

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
