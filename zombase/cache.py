# -*- coding: utf-8 -*-
import collections
import datetime
import time

from dogpile.cache.api import NoValue
from sqlalchemy.orm import object_session

import six


def _get_keystores(keystores_kt, instance, cache):
    if keystores_kt is None:
        try:
            keystores_kt = getattr(instance, '_keystores_kt')
        except AttributeError:
            raise ValueError('`keystores_kt` not provided.')

    if isinstance(keystores_kt, six.string_types):
        for keystore_tuple in _get_keystores((keystores_kt,), instance, cache):
            yield keystore_tuple

    elif isinstance(keystores_kt, collections.Iterable):
        for keystore_kt in keystores_kt:
            keystore_key = keystore_kt.format(instance=instance, it=instance)
            yield (keystore_key, cache.get(keystore_key))

    else:
        raise ValueError('`keystores_kt` must be a string or an iterable.')


def is_valid(timestamp, validity):
    if validity is None:
        return True

    if isinstance(timestamp, NoValue):
        return False

    now = datetime.datetime.now()
    value_created = datetime.datetime.fromtimestamp(timestamp)

    if validity == 'same_day':
        delta = now.date() - value_created.date()
        if delta.days == 0:
            return True
        return False

    raise ValueError('Unknown validity.')


def cached_property(kt, keystores_kt=None, cache=None, validity=None):
    """Decorator for a method of a sqlalchemy mapping.

    Act like the `@property` decorator, but handle interactions with
    the cache.

    Value will be stored with the key provided in `kt`, and key will be
    added to the stores whose keys are provided with `keystores_kt`.

    Argument:
        kt -- template of the key that will be used in cache.

    Keyword argument:
        keystores_kt -- string or iterable
                        default: object._keystores_kt

                        Key's template(s) of the store(s) in which a
                        potential new key will be added. Useful to track
                        dependencies.

        cache -- dogpile.cache region
                 default: object_session(object).cache

                 dogpile.cache's region which will be used.

        validity -- None or 'same_day'

                    Validity of the computed value.

    Example usage:

        @cached_property('prestation:{it.id}:margin')
        def margin(self):
            return self.selling_price - self.cost

    """

    def decorator(func):

        def wrapped(self, *args, **kwargs):
            if cache:
                _cache = getattr(self, cache)
            else:
                _cache = object_session(self).cache

            format_dict = dict(instance=self, it=self)

            key = kt.format(**format_dict)
            timestamp_key = '_zom_ts:{}'.format(key)

            cached_value = _cache.get(key)
            cached_value_timestamp = _cache.get(timestamp_key)

            # If we have the value in cache, depending on `validity`,
            # we just return it.
            if (not isinstance(cached_value, NoValue)
                    and is_valid(cached_value_timestamp, validity)):
                return cached_value

            # Run the computation
            value = func(self, *args, **kwargs)

            # Store value in cache
            _cache.set(key, value)
            _cache.set(timestamp_key, time.time())

            keystores = _get_keystores(keystores_kt, self, _cache)

            for (keystore_key, keystore) in keystores:
                # If the key_store hasn't been created yet, we initialize it
                if isinstance(keystore, NoValue):
                    keystore = []

                keystore.append(key)
                _cache.set(keystore_key, keystore)

            return value

        return property(wrapped)

    return decorator
