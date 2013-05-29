# -*- coding: utf-8 -*-
import pylibmc


class MemcachedCache():
    """Cache system using memcached.

    This cache system is designed to only accept keys in the
    'object_type:object_id:object_property' form (called full-form). In certain
    cases, keys in the 'object_type:object_id:' form (reduced-form) can be
    accepted.

    Internaly we store values with the key 'object_type:object_id', and then
    in a dict.

    """

    def __init__(self, server):
        """Initialize the cache system with the given server. Expect a full
        server adress, including port. Eg: '127.0.0.1:11211'.

        """
        self._server = server
        self._cache = pylibmc.Client([server])

    def _check_key(self, key):
        """Check if the given key is valid, raise AttributeError if not."""
        if not isinstance(key, str):
            raise AttributeError('key provided is not a string')

        if len(key.split(':')) != 3:
            raise AttributeError('Incorrect key')

    def _split_key(self, key):
        """Split the given key in order to get the 'internal' key and the
        'internal' property name, and return these two values.

        """
        split_key = key.split(':')
        return ('{}:{}'.format(split_key[0], split_key[1]), split_key[2])

    def get(self, key):
        """Return the value corresponding to the given key, or `None`."""
        self._check_key(key)
        _key, _property_name = self._split_key(key)

        # `cache_value` is None (if there is no corresponding value in memcached)
        # or is a dict.
        cache_value = self._cache.get(_key)

        if not cache_value or not _property_name in cache_value:
            return None

        return cache_value[_property_name]

    def set(self, key, value):
        """Set the association key/value."""
        self._check_key(key)
        _key, _property_name = self._split_key(key)

        cache_value = self._cache.get(_key)

        # `cache_value` hasn't been initialized yet, so we create a dict.
        if not cache_value:
            cache_value = {}

        # Set the value
        cache_value[_property_name] = value

        # Store in cache
        self._cache.set(_key, cache_value)

    def expire(self, key):
        """Remove the given key from the cache. Accept reduced-form keys."""
        self._check_key(key)
        _key, _property_name = self._split_key(key)

        # A reduced-form key has been given, so we delete the whole data
        # concerning this object.
        if not _property_name:
            self._cache.delete(_key)
            return

        cache_value = self._cache.get(_key)

        # This key doesn't exist, we don't have to do anything.
        if cache_value is None:
            return

        # Remove the property from the dict.
        cache_value.pop(_property_name, None)

        # Store in cache.
        self._cache.set(_key, cache_value)
